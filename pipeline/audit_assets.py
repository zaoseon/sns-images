"""앱에 올라온 영상·그림이 확정 규칙(상단 문구 R01, 주소 R02)을 지키는지 화면에서 직접 잰다(10/6).
방법: 영상은 앞·가운데·뒤 3장을, 그림은 그대로 가져와 규칙 위치에 금색·흰 글자 화소가 있는지 센다. 해당 규격(1080x1920·1080x1350)이 아니면 '해당 없음'.
사용: python3 pipeline/audit_assets.py -> content/audit/rules_audit.json + 표"""
import os, sys, json, subprocess, re
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.abspath(os.path.join(HERE, ".."))
RAW_RE = re.compile(r"^https://raw\.githubusercontent\.com/zaoseon/sns-images/[^/]+/")
SKIP_KINDS = ("스토리보드", "제작 기준", "영상 형태", "영상 스타일", "확정 규칙", "페이지별 안전영역", "정월 움직임", "템플릿 틀 시제품", "릴스 표지 시안", "네이버 카페", "블로그 대표 이미지")   # 대표 검토용 내부 그림·다른 규격은 대상 아님
GOLD = np.array([231, 200, 141])
BOX = {(1080, 1920): dict(hl=(40, 330, 260, 400), hr=(430, 335, 905, 395), url=(640, 1410, 905, 1470)),
       (1080, 1350): dict(hl=(40, 40, 260, 110), hr=(540, 40, 1040, 110), url=(760, 1250, 1040, 1312)),
       (1080, 1440): dict(hl=(40, 40, 260, 110), hr=(540, 40, 1040, 110), url=(760, 1340, 1040, 1402))}
def gold(a, b): 
    x0, y0, x1, y1 = b; r = a[y0:y1, x0:x1].astype(int); return int((np.abs(r - GOLD).sum(axis=2) < 70).sum())
def white(a, b):
    x0, y0, x1, y1 = b; r = a[y0:y1, x0:x1].astype(int); return int((r.min(axis=2) > 205).sum())
def check_frame(im):
    a = np.asarray(im.convert("RGB")); k = (im.width, im.height)
    if k not in BOX: return None
    b = BOX[k]; return dict(R01=gold(a, b["hl"]) >= 150 and white(a, b["hr"]) >= 450, R02=gold(a, b["url"]) >= 200)
def frames(path):
    d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path], capture_output=True, text=True).stdout.strip() or 0); out = []
    for f in (.35, .6, .85):
        p = "/tmp/_au.png"; subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{d * f:.2f}", "-i", path, "-frames:v", "1", p], check=True); out.append(Image.open(p).convert("RGB"))
    return out
def audit():
    d = json.load(open(os.path.join(R, "content", "reel_swaps.json"), encoding="utf-8")); res = []
    for r in d:
        if r.get("status") not in ("new", "wait", "hold"): continue
        if any(k in (r.get("kind") or "") for k in SKIP_KINDS): continue
        urls = [r["video"]] if r.get("video") else list(r.get("images") or [])
        if not urls: continue
        oks = {"R01": [], "R02": []}; na = 0; miss = 0
        for u in urls:
            p = os.path.join(R, RAW_RE.sub("", u.split("?")[0]))
            if not os.path.exists(p): miss += 1; continue
            try: fr = frames(p) if p.endswith(".mp4") else [Image.open(p)]
            except Exception: miss += 1; continue
            rs = [check_frame(x) for x in fr]
            if rs[0] is None: na += 1; continue
            for k in ("R01", "R02"): oks[k].append(sum(1 for x in rs if x[k]) >= (2 if len(rs) == 3 else 1))
        tot = len(oks["R01"])
        status = "해당없음" if tot == 0 and na else ("파일없음" if tot == 0 else ("통과" if all(oks["R01"]) and all(oks["R02"]) else "미적용"))
        res.append(dict(id=r["id"], kind=r.get("kind"), title=r.get("title", "")[:40], status=status, n=len(urls), R01=sum(oks["R01"]), R02=sum(oks["R02"]), checked=tot))
    return res
if __name__ == "__main__":
    res = audit(); os.makedirs(os.path.join(R, "content", "audit"), exist_ok=True); json.dump(res, open(os.path.join(R, "content", "audit", "rules_audit.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    from collections import Counter
    c = Counter(x["status"] for x in res); print("합계", dict(c), "총", len(res))
    by = {}
    for x in res: by.setdefault(x["kind"], Counter())[x["status"]] += 1
    for k, v in sorted(by.items(), key=lambda kv: -sum(kv[1].values())): print(f'{sum(v.values()):>3} · {k}: ' + ", ".join(f"{a} {b}" for a, b in v.items()))
