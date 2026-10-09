"""본문 이미지(표 b·해 볼 것 c·한눈에 보기 i·점수 카드 s)를 새 제작 도구(imgkit)로 전부 다시 만든다 (10/8 대표: 저화질·작은 글씨).
데이터는 기존 제작 스크립트(build_naver_*.py의 N.table/N.rows 호출)와 pages.json 본문에서 그대로 읽는다. pages.json·본문은 건드리지 않는다(이미지 파일만).
사용: python3 naver/rerender_body_images.py [n20 n26 ...]   (비우면 아직 예약 안 한 글 전부 = public/naver/index.html 목록)
결과: img/master/<이름> (2560폭 원본), img/m1280/<이름>·img/<이름> (1280 납품판)."""
import os, sys, re, json, io, contextlib
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "pipeline"))
import naver2 as N
import imgkit as K
SCRIPTS = ["build_naver_16_22.py", "build_naver_26_33.py", "build_naver_34_37.py", "build_naver_38_41.py", "build_naver_42_46.py",
           "build_naver_47_52.py", "build_naver_53_63.py", "build_naver_64_69.py", "build_naver_70.py", "build_naver_71.py", "build_naver_72_74.py", "build_naver_75_79.py"]

def pending_ids():
    p = os.path.join(HERE, "..", "..", "zaoseon-site", "public", "naver", "index.html")
    if not os.path.exists(p): p = "/home/claude/site/public/naver/index.html"
    return set(re.findall(r'href="/naver/(n\d+)\.html"', open(p, encoding="utf-8").read()))

def main(ids):
    K.ONLY = set(ids); done = {"b/c": 0}
    N.hero = lambda *a, **k: None
    import make_page as MP                       # 일부 제작 스크립트는 등록 구간 표시가 없어 끝까지 돌면 pages.json·원고 페이지를 다시 만든다(10/8 실제로 겪음) -> 등록 함수를 막는다
    MP.add = lambda *a, **k: None; MP.PUB = "/tmp/_pub_dummy.json"
    if hasattr(MP, "render_all"): MP.render_all = lambda *a, **k: None
    N.rows = K.rows; N.table = K.table
    import compact as C   # n47 이후 글은 compact.table_c/rows_c로 그린다(10/4 개선판이 10/5 640 납품으로 다시 흐려졌다)
    C.rows_c = K.rows; C.table_c = lambda path, head, cols, rows_, widths: K.rows(path, head, [tuple(r[:3]) for r in rows_])
    for sc in SCRIPTS:
        f = os.path.join(HERE, sc)
        if not os.path.exists(f): continue
        src = open(f, encoding="utf-8").read().split("# ===== 등록 =====")[0]
        ns = {"__file__": f, "__name__": "build_x"}
        buf = io.StringIO()
        try:
            with contextlib.redirect_stdout(buf): exec(compile(src, sc, "exec"), ns)
        except Exception as e: print("ERR", sc, repr(e)[:160])
    reg = json.load(open(os.path.join(HERE, "pages.json"), encoding="utf-8"))
    import regen_badges as RB, add_extra_images as AX
    n_i = n_s = 0
    for pid in sorted(ids, key=lambda x: int(x[1:])):
        b = reg[pid]["body"]; pre = f"naver_z{int(pid[1:])}"
        if f"{pre}_i.jpg" in b:
            try:
                summ, maps, label = RB.summary_maps(b); K.intro(pid, summ, maps, os.path.join(K.IMG, f"{pre}_i.jpg"), label=label); n_i += 1
            except Exception as e: print("i 실패", pid, repr(e)[:100])
        if f"{pre}_s.jpg" in b:
            try:
                title, rws = AX.parse_rows(b); rws = [(l, t) for l, t in rws if t][:4]; K.bars(pid, title, rws, os.path.join(K.IMG, f"{pre}_s.jpg")); n_s += 1
            except Exception as e: print("s 실패", pid, repr(e)[:100])
    print("한눈에", n_i, "점수", n_s, "경고", len(K.WARN)); [print(w) for w in K.WARN[:30]]

if __name__ == "__main__":
    ids = [a for a in sys.argv[1:] if re.fullmatch(r"n\d+", a)] or sorted(pending_ids(), key=lambda x: int(x[1:]))
    main(ids)
