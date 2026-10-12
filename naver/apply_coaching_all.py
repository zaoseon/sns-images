"""10/12 대표 지시: 아직 안 올린 네이버 원고 전부에 코칭 블록·제목 40자·말투 고침을 적용하고 페이지를 다시 만든다.
사용: python3 naver/apply_coaching_all.py   (여러 번 돌려도 같은 결과 - 이미 들어간 블록은 다시 넣지 않는다)
- 대상: coaching_data.COACH의 글(발행 전 전부). 이미 발행된 글(n26·n27·n28·n47·n48·n57)은 coaching_data에 없어 건드리지 않는다.
- 하는 일: pages.json 제목·태그·본문 갱신 → published.json 제목 맞춤 → 다른 글의 '함께 볼 글' 제목 맞춤 → 원고 페이지 다시 만들기
- 예약 완료(done) 글은 목록에서 빠져 있어 render_all이 안 그리므로 여기서 한 편씩 그린다."""
import json, os, sys, datetime as D
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); os.chdir(HERE)
import make_page as MP, coaching_data as CD
def main():
    reg = MP.load(); pub = json.load(open(MP.PUB, encoding="utf-8")); changed = []
    for pid in CD.COACH:
        v = reg[pid]; t0, g0, b0 = v["title"], v["tags"], v["body"]
        t, g, b = MP.apply_coaching(pid, t0, g0, b0)
        if (t, g, b) != (t0, g0, b0): v["title"], v["tags"], v["body"] = t, g, b; changed.append(pid)
        if pid in pub and pub[pid].get("title") != t: pub[pid]["title"] = t
    for pid, v in reg.items():                      # 다른 글이 가리키는 '함께 볼 글' 제목도 새 제목으로
        r = v.get("related")
        if r and r.get("id") in reg and r.get("title") and r["id"] in CD.TITLES: r["title"] = CD.TITLES[r["id"]]
    json.dump(reg, open(MP.REG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(pub, open(MP.PUB, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("바뀐 글", len(changed), changed)
    reg = MP.load(); open_ids = [k for k, v in reg.items() if not v.get("done") and "body" in v]
    PAST = {"n26", "n27", "n28", "n47", "n48", "n57"}      # 이미 발행됨: 다시 그리지 않는다
    live = sorted((v["dt"], k) for k, v in reg.items() if not v.get("done") and "body" in v)
    for i, (dt, k) in enumerate(live):
        if k in PAST: continue
        v = reg[k]; nxt = live[i + 1][1] if i + 1 < len(live) else None
        while nxt in PAST: nxt = None
        MP.write_page(k, D.datetime.fromisoformat(dt), v["title"], v["tags"], v["body"], nxt, v.get("cover"), v.get("related"), MP.new_cat(k, v.get("category") or MP.CATS.get(k)), v.get("thumbs"), v.get("cid"), v.get("clips"), v.get("reserve"))
    for k in ("n24", "n12", "n07", "n25", "n09", "n04"):     # 예약 완료(done) 글: 페이지 파일은 남아 있어 한 편씩 다시 그린다
        v = reg[k]
        MP.write_page(k, D.datetime.fromisoformat(v["dt"]), v["title"], v["tags"], v["body"], None, v.get("cover"), v.get("related"), MP.new_cat(k, v.get("category") or MP.CATS.get(k)), v.get("thumbs"), v.get("cid"), v.get("clips"), v.get("reserve"))
    MP.write_index()
if __name__ == "__main__": main()
