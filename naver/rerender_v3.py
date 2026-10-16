"""네이버 원고 안 이미지(핵심 표 b·해 볼 것 c·한눈에 보기 i 등)를 표지 v3c와 같은 톤으로 다시 만든다 (10/16 대표 K-062:
"원고 내부 이미지들도 다 저런 톤으로 바꾸고 한마디 결론 같은 데만 정월 이미지를 쓰든가").
- 색: 그 글 표지 판(cover_v3_pick.json)의 밝은 쪽. 두 색 조합 진한 판(v_royal 등)은 반전(_inv) 판을 쓴다(흰 칸 위 글자가 읽히게).
- 한자 워터마크(cv.watermark) 없음. 정월은 '한눈에 보기'(한 줄 결론) 카드에만 남긴다.
- 파일은 새 이름만: naver_z53_b.jpg → naver_z53_b3.jpg (CLAUDE.md 사진 보존 규칙). pages.json 본문 주소도 새 이름으로 바꾼다(--write).
사용: python3 naver/rerender_v3.py n53 [n54 ...] [--write]"""
import os, sys, json, re, urllib.parse
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "pipeline"))
import imgkit as K, render as R
import cover_v3 as V

def body_pal(pid, pick):
    p = pick.get(pid) or V.EL_PAL_B[V.all_configs()[pid]["el"]]
    e = next(x for x in V.PAL if x["id"] == p.replace("_inv", ""))
    if "pair" in e and not p.endswith("_inv"): p += "_inv"
    if p == "y_pink": return "p_red"        # 핑크 판은 강조색이 흰색이라 흰 칸 위 글자가 안 보인다 → 본문은 같은 계열 핑크&레드(옅은 핑크 바탕)
    if p == "k_white" or p.startswith("y_"): return p
    return p

def run(ids, write=False):
    pick = json.load(open(os.path.join(HERE, "cover_v3_pick.json"), encoding="utf-8"))
    made = []
    K.Cv.watermark = lambda *a, **k: None
    _save = K.Cv.save
    def save(s_, name):
        nn = re.sub(r"\.jpg$", "3.jpg", name); made.append((name, nn)); _save(s_, nn)
    K.Cv.save = save
    import add_extra_images as AX
    cur = {}
    AX.cfg = lambda pid: (V.Ctx(cur["pal"]), cur["face"])
    import naver2 as N
    _theme = N.theme
    def theme(el):
        out = _theme(el); c = V.Ctx(cur["pal"])
        R.INK, R.GOLD, R.PAPER, R.LINE = c.bg, c.acc, c.fg, c.line
        return out
    N.theme = theme
    import rerender_body_images as RB, urllib.parse
    import naver2 as N2_
    _m = RB.main
    def main_(ids_):
        N2_.title = K.title_card; N2_.months = K.months; N2_.grid = K.cells2; N2_.ring = K.cells2   # 옛 글(n04~n15) 그리기 함수 → 같은 모양의 새 함수(저장은 새 이름)
        import naver as N1_                                                     # n04~n07은 더 옛 모듈(pipeline/naver.py)을 쓴다 — 그대로 두면 옛 이름에 덮어쓴다(10/16 겪음)
        N1_.title = K.title_card; N1_.months = K.months; N1_.grid = K.cells2; N1_.rows = K.rows; N1_.table = K.table
        N1_.hero = lambda *a, **k: None; N1_.theme = N2_.theme
        for fn in dir(N1_):                                                     # 남은 그리기 함수(경로 인자)는 아무것도 안 하게 — 옛 이름 덮어쓰기 방지
            f_ = getattr(N1_, fn)
            if callable(f_) and fn not in ("title", "months", "grid", "rows", "table", "theme", "hero") and not fn.startswith("_") and getattr(f_, "__module__", "") == N1_.__name__:
                setattr(N1_, fn, lambda *a, **k: None)
        return _m(ids_)
    RB.main = main_
    RB.SCRIPTS = ["build_naver_04_07.py", "build_naver_08_12.py", "build_naver_13_15.py", "build_naver_23_25.py"] + RB.SCRIPTS   # 10/16: 발행·예약 글(n04~n15)도
    reg0 = json.load(open(os.path.join(HERE, "pages.json"), encoding="utf-8"))
    def want_of(pid):   # 그 글 본문에 있는 사진 이름만 그린다(글마다 판 색이 달라서 글 하나씩)
        w = {urllib.parse.unquote(os.path.basename(u)) for u in re.findall(r'naver/img/(?:m1280/)?([^"]+?\.jpg)', reg0[pid]["body"])}
        return w | {re.sub(r"3\.jpg$", ".jpg", x) for x in w}                  # 이미 *3.jpg로 바뀐 본문도 다시 그릴 수 있게
    want = set()
    K._skip = lambda path: urllib.parse.unquote(os.path.basename(path)) not in want   # 글 번호가 없는 옛 이름(naver_y03_양띠할일 등)도 본문에 있으면 그린다
    T = V.all_configs()
    PG = os.path.join(HERE, "pages.json"); keep = open(PG, encoding="utf-8").read()
    # 한눈에 보기·점수 카드는 본문에 옛 이름(_i.jpg)이 있어야 다시 그린다 → 그리는 동안만 *3.jpg를 옛 이름으로 돌려 둔다(끝나면 원래대로)
    open(PG, "w", encoding="utf-8").write(re.sub(r"(naver_z(?!53_[kvs])\d+_[a-z]+)3\.jpg", r"\1.jpg", keep))
    try:
      for pid in ids:
        cur["pal"] = body_pal(pid, pick); cur["face"] = T[pid].get("face") or "v1_lowbun"; want.clear(); want.update(want_of(pid))
        c0 = V.Ctx(cur["pal"]); R.INK, R.GOLD, R.PAPER, R.LINE = c0.bg, c0.acc, c0.fg, c0.line   # theme()를 부르지 않는 옛 스크립트(n04~n07)도 그 글 판으로
        RB.main([pid])
    finally:
        open(PG, "w", encoding="utf-8").write(keep)
    if write:
        reg = json.load(open(os.path.join(HERE, "pages.json"), encoding="utf-8"))
        for pid in ids:
            b = reg[pid]["body"]
            for old, new in made:
                for o, nn in ((old, new), (urllib.parse.quote(old), urllib.parse.quote(new))):
                    for pre in ("/naver/img/", "/naver/img/m1280/"):
                        b = b.replace(pre + o, "/naver/img/" + nn)
            reg[pid]["body"] = b
        json.dump(reg, open(os.path.join(HERE, "pages.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return made

if __name__ == "__main__":
    ids = [a for a in sys.argv[1:] if a.startswith("n")]
    m = run(ids, "--write" in sys.argv); print("만듦", len(m), [n for _, n in m][:12])
