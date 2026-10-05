# 10/5 대표 요청: 네이버 발행 시간을 옮기면 연결 글도 거기에 맞게 반영. 기준 파일이 어긋나거나 연결 순서가 틀리면 실패.  python3 naver/test_links_sync.py
import json, os, sys, re, datetime as D
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, H); os.chdir(H)
import links_plan as L
ok = True
def t(m, c, extra=""):
    global ok; print(("OK   " if c else "FAIL ") + m + (" " + extra if extra and not c else "")); ok = ok and bool(c)
pub = json.load(open("published.json", encoding="utf-8")); reg = json.load(open("pages.json", encoding="utf-8"))
mis = [k for k in pub if reg.get(k, {}).get("dt") and (pub[k]["date"] != reg[k]["dt"][:10] or str(pub[k].get("time", ""))[:5] != reg[k]["dt"][11:16])]
t("published.json의 날짜·시각이 pages.json(실제 예약 시각)과 같음", not mis, str(mis))
t("연결표 점검(함께 볼 글·클립·스티커 순서, 예약 24시간 여유, 대상 중복 없음)", not L.check(), str(L.check()))
t("예약·발행된 글 연결표 점검(REL_FIX)", not L.check_fix(), str(L.check_fix()))
bad = []; live = [k for k, v in reg.items() if not v.get("done") and "body" in v and v.get("related")]
for k in live:
    r = reg[k]["related"]; tp = L.POST_DT.get(k); tt = L.POST_DT.get(r["id"])
    if not tp or not tt or D.datetime.fromisoformat(tp) - D.datetime.fromisoformat(tt) < D.timedelta(hours=24): bad.append((k, r["id"]))
    m = re.search(r"<p><b>👇 ([^<]*)</b></p>", reg[k]["body"])
    if k in L.REL and (r["id"] != L.REL[k][0] or not m or m.group(1) != r["phrase"]): bad.append((k, "연결표·본문 불일치"))
t(f"원고 {len(live)}편의 함께 볼 글이 24시간 이상 먼저 발행되고 연결표·본문 유도 문구와 같음", not bad, str(bad))
print("모두 통과" if ok else "실패"); sys.exit(0 if ok else 1)
