"""네이버 본문 사진의 좌우 흰 여백을 잘라 폰에서 꽉 차게 보이게 한다 (대표 10/18 "이미지가 작아 보인다", K-137).
원인: 그림 안에 좌우 흰 여백이 있다(imgkit CW=1100/1280 = 86%, 글에 따라 더 넓다). 네이버 편집기는 사진을 문서 폭으로 붙이므로 여백이 그대로 보인다.
방법: 색이 있는 부분의 좌우 끝으로 자르고 가로 1280으로 맞춘다. 같은 이름의 master(2560)가 있으면 거기서 잘라 줄이고(선명), 없으면 1280 판을 늘려 약하게 선명화한다.
파일은 새 이름만: naver_z05_w5.jpg → naver_z05_w5f.jpg (CLAUDE.md 사진 보존 규칙 — 옛 파일은 건드리지 않는다).
사용: python3 naver/fullbleed.py <글id ...>|--all [--out DIR] [--dry]   결과: img/ 와 img/m1280/ (또는 --out 아래)에 새 사진, 글별 계획은 fullbleed_plan.json"""
import os, sys, re, json, urllib.parse
from PIL import Image, ImageFilter
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); IMG = os.path.join(HERE, "img")
TH = 30; MIN_MARGIN = 40; SUF = "f"

def bbox_x(im):
    a = np.asarray(im.convert("RGB")).astype(int)
    nonw = np.abs(a - 255).sum(2) > TH
    c = np.where(nonw.any(0))[0]
    return int(c.min()), int(c.max()) + 1

def convert(name, outdirs):
    """-> (새 이름 | None, 사유)"""
    src = os.path.join(IMG, "m1280", name)
    if not os.path.exists(src): src = os.path.join(IMG, name)
    if not os.path.exists(src): return None, "원본 없음"
    im = Image.open(src).convert("RGB")
    if im.size[0] != 1280: return None, "가로 %d (1280 아님)" % im.size[0]
    l, r = bbox_x(im); ml, mr = l, 1280 - r
    if min(ml, mr) < MIN_MARGIN: return None, "여백 없음(좌 %d·우 %d)" % (ml, mr)
    if abs(ml - mr) > 6: return None, "좌우 여백이 다름(좌 %d·우 %d)" % (ml, mr)
    m = os.path.join(IMG, "master", name)
    if os.path.exists(m):
        M = Image.open(m).convert("RGB")
        if M.size[0] == 2560 and M.size[1] == im.size[1] * 2:
            how = "master 2560에서 잘라 줄임"
            out = M.crop((l * 2, 0, r * 2, M.size[1])).resize((1280, round(M.size[1] * 1280 / ((r - l) * 2))), Image.LANCZOS)
        else: M = None
    else: M = None
    if M is None:
        how = "1280판을 잘라 %.2f배 늘림" % (1280 / (r - l))
        c = im.crop((l, 0, r, im.size[1]))
        out = c.resize((1280, round(c.size[1] * 1280 / (r - l))), Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=1.0, percent=60, threshold=2))
    new = re.sub(r"\.jpg$", SUF + ".jpg", name)
    for d in outdirs:
        os.makedirs(d, exist_ok=True); out.save(os.path.join(d, new), quality=93, subsampling=0)
    return (new, how, out.size, 1280 / (r - l)), ""

def post_images(pid, pages):
    s = json.dumps(pages[pid], ensure_ascii=False); out = []
    for m in re.findall(r'naver/img/((?:wide/)?[^"\\ )?]+\.jpg)', s):
        n = urllib.parse.unquote(m)
        if n not in out: out.append(n)
    return out

def main(argv):
    out = None; dry = "--dry" in argv
    if "--out" in argv: out = argv[argv.index("--out") + 1]
    ids = [a for a in argv if re.match(r"^(n|s)\d+$", a)]
    pages = json.load(open(os.path.join(HERE, "pages.json"), encoding="utf-8"))
    if "--all" in argv: ids = list(pages)
    dirs = [os.path.join(out, "m1280")] if out else [IMG, os.path.join(IMG, "m1280")]
    plan = {}
    for pid in ids:
        rows = []
        for pos, n in enumerate(post_images(pid, pages), 1):
            if n.startswith("wide/") or "_cta" in n: rows.append({"pos": pos, "old": n, "new": None, "why": "표지·배너는 따로"}); continue
            if dry: rows.append({"pos": pos, "old": n}); continue
            r, why = convert(n, dirs)
            rows.append({"pos": pos, "old": n, "new": r[0] if r else None, "how": r[1] if r else why, "size": list(r[2]) if r else None, "scale": round(r[3], 2) if r else None})
        plan[pid] = rows
    json.dump(plan, open(out and os.path.join(out, "fullbleed_plan.json") or os.path.join(HERE, "fullbleed_plan.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("글 %d편, 새 사진 %d장" % (len(plan), sum(1 for v in plan.values() for x in v if x.get("new"))))

if __name__ == "__main__": main(sys.argv[1:])
