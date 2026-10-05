"""연결표(links_plan.py)를 아직 예약하지 않은 모든 원고에 맞춘다 (10/5 대표: 네이버 발행 시간을 옮기면 연결 글도 거기에 맞게 반영).
 - 함께 볼 글(related) · 본문의 👇 유도 문구 · 넣을 클립(clips) · "예약은 이때부터 걸어요"(reserve)를 연결표·발행 시각 기준으로 다시 쓴다.
 - 기준 발행 시각은 pages.json의 dt. published.json의 날짜·시각도 먼저 pages.json에 맞춘다(옮긴 시각이 연결표에 반영되지 않던 원인).
 - 이 도구는 pages.json만 고친다. 사이트 페이지는 make_page.render_all()이 만든다(SITE=<zaoseon-site 경로>).
다시 실행해도 같은 결과.  사용: python3 naver/apply_links_sync.py [--dry]"""
import os, sys, re, json
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE); sys.path.insert(0, HERE)
def sync_published():
    pub = json.load(open("published.json", encoding="utf-8")); reg = json.load(open("pages.json", encoding="utf-8")); n = []
    for k, v in pub.items():
        r = (reg.get(k) or {}).get("dt")
        if r and (v.get("date") != r[:10] or str(v.get("time", ""))[:5] != r[11:16]): v["date"] = r[:10]; v["time"] = r[11:16]; n.append(k)
    if n: json.dump(pub, open("published.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return n
def main(dry=False):
    moved = sync_published()
    import links_plan as LP
    reg = json.load(open("pages.json", encoding="utf-8")); titles = json.load(open("clip_titles.json", encoding="utf-8")); pub = json.load(open("published.json", encoding="utf-8"))
    urls = json.load(open("urls.json", encoding="utf-8")) if os.path.exists("urls.json") else {}; changed = []
    for k, v in reg.items():
        if v.get("done") or "body" not in v or k not in LP.REL: continue
        tgt, phrase = LP.REL[k]; before = json.dumps([v.get("related"), v.get("clips"), v.get("reserve"), v["body"]], ensure_ascii=False)
        body, n = re.subn(r"<p><b>👇 [^<]*</b></p>", lambda m: f"<p><b>👇 {phrase}</b></p>", v["body"], count=1)
        if n: v["body"] = body
        old = v.get("related") or {}; same = old.get("id") == tgt   # 연결 글이 그대로면 기존 제목 표기를 유지하고, 바뀐 글만 새로 정한다
        v["related"] = {"id": tgt, "title": (old.get("title") if same and old.get("title") else (LP.TITLE.get(tgt) or reg.get(tgt, {}).get("title") or pub.get(tgt, {}).get("title", ""))), "phrase": phrase, "url": (old.get("url") if same and old.get("url") else (urls.get(tgt) or pub.get(tgt, {}).get("url", "")))}
        if k in LP.EMBED:
            cl = [titles[c] for c in LP.EMBED[k] if c in titles]
            if cl or v.get("clips"): v["clips"] = cl or None
        h, so = LP.reserve_window(k); v["reserve"] = {"hard": LP.fmt(h), "soft": LP.fmt(so), "needsClip": so != h}
        if json.dumps([v.get("related"), v.get("clips"), v.get("reserve"), v["body"]], ensure_ascii=False) != before: changed.append(k)
    if not dry: json.dump(reg, open("pages.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("published.json 맞춤:", moved or "없음"); print("원고 자료를 고친 글:", changed or "없음"); return changed
if __name__ == "__main__": main("--dry" in sys.argv)
