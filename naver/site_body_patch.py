"""사이트 원고 페이지(zaoseon-site public/naver/nXX.html)의 본문 조각만 pages.json 새 판으로 바꾼다 (① 자동 실행 10/19 19:45).
render_all 은 CT가 사이트 페이지에 직접 넣은 글별 CTA 배너(cta12~14)·utm_campaign·클립 칸을 옛 판으로 되돌리므로 금지(HANDOFF 10/18).
그래서 write_page 로 임시 폴더에 새 페이지를 그린 뒤, 지금 사이트 페이지의 본문(<div id="body">…)과 문단 단위로 견줘
바뀐 조각 중 지켜야 할 낱말(CTA·연결글·클립·발행 정보)이 든 조각은 지금 판을 남기고, 나머지(본문 글·새 그림)만 받는다.
사용: python3 naver/site_body_patch.py n72 n32 …   (끝에 글마다 받은 조각·남긴 조각 수를 찍는다)"""
import os, sys, re, json, difflib, tempfile, datetime as D
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import make_page as M

KEEP = ("cta", "LINKCARD", "👇", "blog.naver.com", "올릴 날", "다음 원고", "utm_", "클립")
START = '<div id="body">'


def _cut(page):
    a = page.index(START) + len(START); b = page.index("</div></div>\n", a)
    return a, b


def _parts(body):
    return re.split(r"(?=<p[ >]|<table)", body)


def patch(pid):
    reg = M.load(); v = reg[pid]
    site = M.SITE; tmp = tempfile.mkdtemp(); os.makedirs(f"{tmp}/public/naver/img", exist_ok=True)
    M.SITE = tmp
    try:
        M.write_page(pid, D.datetime.fromisoformat(v["dt"]), v["title"], v["tags"], v["body"], None, None, v.get("related"),
                     M.new_cat(pid, v.get("category") or M.CATS.get(pid)), v.get("thumbs"), v.get("cid"), v.get("clips"), v.get("reserve"))
        new = open(f"{tmp}/public/naver/{pid}.html", encoding="utf-8").read()
    finally:
        M.SITE = site
    path = f"{site}/public/naver/{pid}.html"; old = open(path, encoding="utf-8").read()
    oa, ob = _cut(old); na, nb = _cut(new)
    o, n = _parts(old[oa:ob]), _parts(new[na:nb])
    out, took, kept = [], 0, 0
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, o, n, autojunk=False).get_opcodes():
        if tag == "equal": out += o[i1:i2]; continue
        chunk = "".join(o[i1:i2]) + "".join(n[j1:j2])
        if any(k in chunk for k in KEEP): out += o[i1:i2]; kept += 1
        else: out += n[j1:j2]; took += 1
    open(path, "w", encoding="utf-8").write(old[:oa] + "".join(out) + old[ob:])
    return took, kept


if __name__ == "__main__":
    for pid in sys.argv[1:]: print(pid, "받은 조각 %d · 남긴 조각 %d" % patch(pid))
