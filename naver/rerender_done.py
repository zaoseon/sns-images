"""예약·발행이 끝난 글(n04~n25)의 본문 이미지를 새 제작 도구(imgkit)로 다시 만든다 (10/10 대표: 예약 글도 본문·이미지 전부 규칙대로).
옛 도구의 제목 카드·월별 칸·칸 목록은 imgkit.title_card·months·cells2로 옮긴다. 이미지 속 '지도'는 '풀이'로 바꿔 그린다.
사용: python3 naver/rerender_done.py   결과: img/master·img/m1280·img/ 에 같은 파일 이름으로 쓴다."""
import os, sys, re, io, contextlib
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "pipeline"))
import naver2 as N
import imgkit as K
SCRIPTS = ["build_naver_04_07.py", "build_naver_08_12.py", "build_naver_13_15.py", "build_naver_16_22.py", "build_naver_23_25.py"]
def fixt(t):
    if not isinstance(t, str): return t
    t = t.replace("지도별", "풀이별").replace("지도", "풀이").replace("교차", "겹침")
    return t
def fx(o):
    if isinstance(o, str): return fixt(o)
    if isinstance(o, (list, tuple)): return type(o)(fx(x) for x in o)
    return o
def main():
    K.ONLY = None
    N.hero = lambda *a, **k: None
    import make_page as MP
    MP.add = lambda *a, **k: None; MP.PUB = "/tmp/_pub_dummy.json"
    if hasattr(MP, "render_all"): MP.render_all = lambda *a, **k: None
    import compact as C
    N.rows = lambda path, head, items, note="": K.rows(path, fx(head), fx(items), fx(note))
    N.table = lambda path, head, cols, rows_, widths: K.table(path, fx(head), fx(cols), fx(rows_), widths)
    C.rows_c = N.rows; C.table_c = lambda path, head, cols, rows_, widths: K.rows(path, fx(head), [tuple(fx(r[:3])) for r in rows_])
    N.title = lambda path, kicker, lines, sub, mark: K.title_card(path, fx(kicker), fx(lines), fx(sub), mark)
    N.months = lambda path, head, good, save, lucky: K.months(path, fx(head), good, save, lucky)
    N.grid = lambda path, head, cells, note="": K.cells2(path, fx(head), fx(cells), fx(note))
    N.ring = N.grid
    import naver as N0                           # n04~n07 제작 스크립트는 옛 도구 naver를 쓰고 원소 색이 없다 → 대표 이미지 색에 맞춘다
    TH = {"y": "불", "m": "흙", "o": "나무", "l": "불"}
    def th(path):
        if os.path.basename(path)[6] in TH and re.match(r"naver_[ymol]0\d_", os.path.basename(path)): N.theme(TH[os.path.basename(path)[6]])
    def w(fn):
        def g(path, *a, **k): th(path); return fn(path, *a, **k)
        return g
    N0.rows = w(N.rows); N0.table = w(N.table); N0.title = w(N.title); N0.months = w(N.months); N0.grid = w(N.grid)
    for sc in SCRIPTS:
        f = os.path.join(HERE, sc)
        src = open(f, encoding="utf-8").read().split("# ===== 등록 =====")[0]
        ns = {"__file__": f, "__name__": "build_x"}; buf = io.StringIO()
        try:
            with contextlib.redirect_stdout(buf): exec(compile(src, sc, "exec"), ns)
        except Exception as e: print("ERR", sc, repr(e)[:200])
    print("경고", len(K.WARN)); [print(w) for w in K.WARN[:40]]
if __name__ == "__main__": main()
