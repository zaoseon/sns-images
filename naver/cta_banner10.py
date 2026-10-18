"""글별 CTA 배너 (10/18 17:00 대표 "CTA 배너도 원고글마다 해당 주제를 활용해야 눌러볼 거 같다").
cta_banner6(9판 5세트, 1280x240)를 그대로 쓰되 제목·부제를 naver/cta_copy.json 의 글별 문구로 바꿔 그린다.
판은 make_page.cta_pick 이 고르던 판(원고 페이지에 이미 들어 있는 naver_cta9_<판>.jpg)을 따른다.
naver/img 규칙: 새 이름(naver_cta10_<글번호>_<판>.jpg)으로 추가만, 덮어쓰지 않는다.
만들기: python3 naver/cta_banner10.py [n34 n35 ...]  (없으면 cta_copy.json 전부)
"""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cta_banner6 as C
SITE = os.environ.get("ZS_SITE", "/home/claude/zaoseon-site")

def pal_of(pid):
    p = os.path.join(SITE, "public", "naver", pid + ".html")
    m = re.search(r"naver_cta9_([a-z_]+)\.jpg", open(p, encoding="utf-8").read()) if os.path.exists(p) else None
    return m.group(1) if m else "v_navy"

def name_of(pid, pal): return f"naver_cta10_{pid}_{pal}.jpg"

def build_one(pid, copy):
    pal = pal_of(pid)
    C.PAL, C.TITLE, C.SUB, C.NAME = pal, copy["title"], copy["sub"], name_of(pid, pal)
    return C.build()

if __name__ == "__main__":
    posts = json.load(open(os.path.join(HERE, "cta_copy.json"), encoding="utf-8"))["posts"]
    ids = sys.argv[1:] or list(posts)
    for pid in ids:
        try: r = build_one(pid, posts[pid]); print(pid, r["title_px"], r["sub_px"], r["button_px"])
        except SystemExit as e: print(pid, "실패:", e)
