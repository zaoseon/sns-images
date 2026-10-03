"""n26~n33 원고에 연결표(links_plan.py)를 적용한다: 함께 볼 글 교체(제목·주소·유도 문구), 클립 넣기 칸 추가. 다시 실행해도 같은 결과."""
import os, sys, re, json
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE); sys.path.insert(0, HERE)
import make_page as MP, links_plan as LP
reg = json.load(open("pages.json", encoding="utf-8")); titles = json.load(open("clip_titles.json", encoding="utf-8"))
urls = json.load(open("urls.json", encoding="utf-8")) if os.path.exists("urls.json") else {}
pub = json.load(open("published.json", encoding="utf-8"))
for k in [f"n{i}" for i in range(26, 47)]:
    tgt, phrase = LP.REL[k]; v = reg[k]
    v["body"] = re.sub(r"<p><b>👇 [^<]*</b></p>", lambda m: f"<p><b>👇 {phrase}</b></p>", v["body"], count=1)
    v["related"] = {"id": tgt, "title": LP.TITLE.get(tgt) or pub.get(tgt, {}).get("title", ""), "phrase": phrase, "url": urls.get(tgt) or pub.get(tgt, {}).get("url", "")}
    v["clips"] = [titles[c] for c in LP.EMBED[k]]
    h, so = LP.reserve_window(k); v["reserve"] = {"hard": LP.fmt(h), "soft": LP.fmt(so), "needsClip": so != h}
json.dump(reg, open("pages.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
MP.render_all(); print("ok", LP.check() or "규칙 위반 없음")
