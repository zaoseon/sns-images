"""10/4: n34~n37 만들기 - 정사각 대표 이미지 + 컴팩트 본문 이미지 + 작은 CTA 배너 (rebuild_26_33.py 와 같은 방식)."""
import os, sys, re, runpy, json
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
sys.path.insert(0, os.path.join(HERE, "..", "pipeline")); sys.path.insert(0, HERE)
import naver2 as N, thumb_sq as TQ, compact as C
def hero(path, el, kicker, lines, sub, mark, face):
    pid = "n" + re.search(r"_z(\d\d)_a", path).group(1); TQ.render(pid, path)
N.hero = hero; N.table = C.table_c; N.rows = C.rows_c
runpy.run_path("build_naver_34_37.py", run_name="__main__")
import make_page as MP, links_plan as LP
reg = json.load(open("pages.json", encoding="utf-8"))
for k in [f"n{i}" for i in range(34, 38)]:
    reg[k]["body"] = reg[k]["body"].replace("naver_cta2_", "naver_cta3_")
json.dump(reg, open("pages.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
