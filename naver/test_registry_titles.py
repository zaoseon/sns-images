# 10/5 대표 지적: 앱에 제목 대신 "3편"만 보이는 글이 있었다(n03). 레지스트리 제목이 비었거나 번호뿐이면 실패.  python3 naver/test_registry_titles.py
import json, os, re, sys
pg = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "pages.json"), encoding="utf-8")); bad = []
for k, v in pg.items():
    t = str(v.get("title") or "").strip()
    if not t or re.fullmatch(r"\d+\s*편|n\d+|\d+", t) or len(t) < 6: bad.append((k, t))
print(f"레지스트리 제목 점검: {len(pg)}편 중 문제 {len(bad)}건"); [print(" -", b) for b in bad]
sys.exit(1 if bad else 0)
