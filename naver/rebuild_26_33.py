"""10/3: n26~n33 다시 만들기 - 정사각 대표 이미지 + 컴팩트 본문 이미지 + 작은 CTA 배너."""
import os, sys, re, runpy, json
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
sys.path.insert(0, os.path.join(HERE, "..", "pipeline")); sys.path.insert(0, HERE)
import naver2 as N, thumb_sq as TQ, compact as C
def hero(path, el, kicker, lines, sub, mark, face):
    pid = "n" + re.search(r"_z(\d\d)_a", path).group(1); TQ.render(pid, path)
N.hero = hero; N.table = C.table_c; N.rows = C.rows_c
C.cta_c(os.path.join(HERE, "img", "naver_cta2_1초무료풀이.jpg"), os.path.join(HERE, "img", "naver_cta3_1초무료풀이.jpg"))
runpy.run_path("build_naver_26_33.py", run_name="__main__")
reg = json.load(open("pages.json", encoding="utf-8"))
for k in [f"n{i}" for i in range(26, 34)]:
    reg[k]["body"] = reg[k]["body"].replace("naver_cta2_", "naver_cta3_")
json.dump(reg, open("pages.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
import make_page as MP; MP.render_all()
