"""확신·불안 조장·단정 금지 문구 검사(10/7, '운세 서비스 콘텐츠 제작 가이드라인' 6장 + 자오선 감정서 가이드의 단정 금지 목록).
- 확신·보장: 적중률·반드시·무조건·확실합니다·보장  - 불안 조장: 큰일 납니다·이대로면·지금 안 하면
- 단정 금지 소재: 사망·중병·사고·이혼·파산·범죄·임신을 확정적으로 말하는 표현
사용: python3 pipeline/claims_audit.py  (앱 대기 캡션·영상 문구·카드 문구를 훑어 걸린 곳을 보여 준다. 걸러서 막지는 않고 사람이 본다)"""
import os, re, json, glob
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.abspath(os.path.join(HERE, ".."))
PAT = {"확신·보장": r"적중률|100\s?%\s*(맞|적중|정확)|반드시|무조건|틀림없|확실(합니다|해요)|확실히 (됩니다|될 겁니다|이뤄|맞)|장담|보장",
       "불안 조장": r"큰일\s?(납니다|나요|난다|날 수)|이대로(면| 가면)|지금 안 (하|보)면|안 (하|보)면 (위험|큰일|후회)|놓치면 (안 돼|후회)|(상담|확인)(을 )?(받지|하지) 않으면 (위험|큰일|후회)|당장 .{0,12}(안 하면|않으면) 위험",
       "단정 금지 소재": r"(사망|죽음|중병|큰 병|암에 걸|사고(가| 수) (납니다|난다|나요|날 수)|이혼(할 운|합니다|하게 됩니다)|파산(할 운|합니다)|범죄|임신(합니다|하게 됩니다|했습니다))"}
def scan_text(t): return [(k, m.group(0)) for k, p in PAT.items() for m in re.finditer(p, t)]
def corpus():
    d = json.load(open(os.path.join(R, "content", "reel_swaps.json"), encoding="utf-8")); out = []
    for r in d:
        if r.get("status") in ("new", "wait", "hold") and r.get("caption"): out.append((f"캡션 {r['id']}", r["caption"]))
    for f in sorted(glob.glob(os.path.join(R, "content", "*.py")) + [os.path.join(R, "pipeline", x) for x in ("data_reels.py", "new_tri_reels.py", "pick_reel.py", "motion_dots.py", "motion_kinetic.py", "card_kit.py")]):
        if not os.path.exists(f): continue
        for ln, line in enumerate(open(f, encoding="utf-8", errors="replace"), 1):
            for s in re.findall(r"[\"']([^\"'\n]{6,200})[\"']", line):
                if re.search(r"[가-힣]", s): out.append((f"{os.path.basename(f)}:{ln}", s))
    return out
if __name__ == "__main__":
    hits = [(w, k, m, t[:60]) for w, t in corpus() for k, m in scan_text(t)]
    print("훑은 문구", len(corpus()), "개 · 걸린 곳", len(hits))
    import collections; c = collections.Counter((k, m) for _, k, m, _ in hits); print(dict(c.most_common(12)))
    for h in hits[:10]: print(h)
    json.dump(hits, open(os.path.join(R, "content", "audit", "claims_audit.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
