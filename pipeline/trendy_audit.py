"""트렌디 표현 사용 규칙 검사(R24·R25, 10/7 대표: 무조건 우르르 쓰지 말고 맥락을 보고 섞어 쓴다).
확인: ① 같은 낱말은 한 달 2번 이하 ② 같은 종류(클립·릴스·카드) 안에서 날짜가 이웃한 영상에 연속 사용 금지 ③ 한 주 영상의 40% 이하 ④ 마음이 무거운 소재는 비움 ⑤ 쓰는 표현마다 근거·맥락 이유·점검일(오늘 이후)이 있음 ⑥ 한 종류만 몰리지 않음
사용: python3 pipeline/trendy_audit.py"""
import os, json, datetime as D, collections
R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
def kind_group(i):
    return "clip" if i.startswith("sopclip") or i.startswith("clip-") else "card" if "pick" in i or i.startswith("swap") else "reel"
def run(today=None):
    T = json.load(open(os.path.join(R, "content", "trendy_lines.json"), encoding="utf-8")); S = {r["id"]: r for r in json.load(open(os.path.join(R, "content", "reel_swaps.json"), encoding="utf-8"))}
    today = today or D.date(2026, 10, 8).isoformat(); out = []
    used = {k: v for k, v in T.items() if v["opener"]}
    c = collections.Counter(v["term"] for v in used.values())
    for t, n in c.items():
        if n > 2: out.append(f"같은 낱말 '{t}' {n}번(한 달 2번 이하)")
    # 날짜 정렬
    def when(k): r = S.get(k, {}); return (r.get("date") or "9999-99-99") + " " + (r.get("time") or "99:99")
    for g in ("clip", "reel", "card"):
        ks = sorted([k for k in T if kind_group(k) == g and k in S and (S[k].get("date") or "")[:4] == "2026"], key=when)
        for a, b in zip(ks, ks[1:]):
            if T[a]["opener"] and T[b]["opener"]: out.append(f"이웃한 {g} 연속 사용: {a} → {b}")
    wk = collections.defaultdict(lambda: [0, 0])
    for k, v in T.items():
        d = (S.get(k, {}).get("date") or "")
        if len(d) == 10 and d[:4] == "2026":
            iso = D.date.fromisoformat(d).isocalendar()[:2]; wk[iso][1] += 1; wk[iso][0] += 1 if v["opener"] else 0
    for iso, (a, b) in sorted(wk.items()):
        if b >= 3 and a / b > .4: out.append(f"{iso[0]}년 {iso[1]}주 {a}/{b} = {a / b:.0%} (40% 이하)")
    for k, v in T.items():
        if v.get("heavy") and v["opener"]: out.append(f"마음이 무거운 소재에 사용: {k}")
        if v["opener"]:
            if not v.get("fit") or not v.get("source"): out.append(f"맥락 이유·근거 없음: {k}")
            if not v.get("review_by") or v["review_by"] < today: out.append(f"점검일 지남/없음: {k}")
    types = collections.Counter(v["type"] for v in used.values())
    if types and max(types.values()) / len(used) > .6: out.append(f"한 종류가 60% 넘음: {dict(types)}")
    return out, len(used), len(T), types
if __name__ == "__main__":
    o, n, m, t = run(); print(f"트렌디 표현 {n}/{m} ({n / m:.0%}) · 종류 {dict(t)}"); print("걸린 곳:", o if o else "없음")
