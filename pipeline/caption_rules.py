"""캡션 규칙 R17(10/6 확정): 캡션에는 ① 영상마다 다른 한 줄(그 영상 주제에 맞춘 홈페이지 유입 문장) ② 팔로우 유도 한 줄을 넣는다. 같은 문장을 반복하지 않는다.
홈페이지 유입 문장은 대표가 정한 표현(생년월일 입력 · 내 첫글자 · 타고난 기운)만 쓰고, 영상 주제에 맞춘 앞말과 끝말을 돌려 쓴다. 사실이 아닌 기능은 말하지 않는다.
사용: python3 pipeline/caption_rules.py  (앱 대기 항목 캡션에 적용·검사)"""
import os, re, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.abspath(os.path.join(HERE, ".."))
TAIL = ["프로필 링크에서 생년월일 입력하고 내 첫글자와 타고난 기운 알아보기", "프로필 링크에서 생년월일만 넣으면 내 첫글자와 타고난 기운을 볼 수 있어요", "프로필 링크에서 내 생년월일로 첫글자와 타고난 기운을 확인해 보세요"]
FOLLOW = ["팔로우하고 더 많은 이야기 나눠요.", "팔로우하면 다음 편을 놓치지 않아요.", "팔로우하고 다음 이야기도 같이 봐요.", "팔로우해 두면 다음 풀이도 이어서 볼 수 있어요."]
LEADS = {"swap-card-1009": "연애에서 한 번 정하면 뒤돌아보지 않는 편인지 궁금하다면", "swap-card-1011": "먼저 말할지 기다릴지, 내 연락의 결이 궁금하다면", "swap-card-1023": "읽고 답장하기까지 나는 어느 쪽인지 더 알고 싶다면",
         "add-pick-1031": "읽고도 답장 못 한 날 내 마음이 궁금하다면", "add-pick-1107": "말 걸고 싶은 날 필요한 한 걸음이 궁금하다면", "add-motion-dots": "나랑 같은 말을 하는 운명학이 몇 개인지 궁금하다면",
         "add-kinetic-reply": "내 연락의 리듬이 어느 쪽인지 궁금하다면", "add-kinetic-talk": "먼저 말 걸고 싶은 날의 내 결이 궁금하다면", "add-litho": "내 별자리가 사주와 같은 말을 하는지 궁금하다면",
         "add-subway": "지금 내 10년이 어느 역인지 궁금하다면", "add-boarding": "2027 정미년행 탑승권, 내 열두 달이 궁금하다면", "add-ticket": "2027년 내 열두 달의 흐름이 궁금하다면",
         "clip-s10-video": "내 이사 날짜가 궁금하다면"}
def _strip(c):
    c = re.sub(r"[^.!?\n※#]*프로필 링크[^.!?\n※#]*[.!?]?\s*", "", c); c = re.sub(r"[^.!?\n※#]*팔로우[^.!?\n※#]*[.!?]?\s*", "", c); return re.sub(r"\s{2,}", " ", c).strip()
def home_line(i, idx): return f"{LEADS[i]} {TAIL[idx % len(TAIL)]}."
def apply(caption, i, idx):
    c = _strip(caption); ins = f"{home_line(i, idx)} {FOLLOW[idx % len(FOLLOW)]} "
    m = re.search(r"※|#", c)
    return (c[:m.start()].rstrip() + " " + ins + c[m.start():]) if m else (c + " " + ins).strip()
def check(caption):
    """한 캡션: 프로필 링크 문장 정확히 1개, 팔로우 문장 1개 이상."""
    out = []; n1 = len(re.findall(r"프로필 링크", caption)); n2 = len(re.findall(r"팔로우", caption))
    if n1 != 1: out.append(f"프로필 링크 문장이 {n1}개(1개여야 함)")
    if n2 < 1: out.append("팔로우 유도 문장 없음")
    return out
def audit_all(d):
    seen = {}; res = []
    for r in d:
        if r.get("status") in ("new", "wait", "hold") and r.get("caption"):
            line = next((s for s in re.split(r"(?<=[.!?])\s+", r["caption"]) if "프로필 링크" in s), ""); prob = check(r["caption"])
            if line and line in seen: prob.append(f"{seen[line]}와 같은 문장 반복")
            seen.setdefault(line, r["id"]); res.append((r["id"], prob))
    return res
if __name__ == "__main__":
    sys.path.insert(0, HERE); import precheck as P
    f = os.path.join(R, "content", "reel_swaps.json"); d = json.load(open(f, encoding="utf-8")); n = 0
    for k, r in enumerate(d):
        if r["id"] in LEADS and r.get("caption") and r.get("status") in ("new", "wait", "hold"):
            r["caption"] = apply(r["caption"], r["id"], list(LEADS).index(r["id"])); n += 1
    json.dump(d, open(f, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    bad = [(i, p) for i, p in audit_all(d) if p]; print("캡션 적용", n, "개 · 규칙 위반", len(bad), bad[:4])
    for r in d:
        if r["id"] in LEADS and r.get("caption"):
            t = P.check_text(r["caption"])
            if t: print("문구 검사 걸림", r["id"], t)
    print("예시:", next(r["caption"] for r in d if r["id"] == "add-litho")[:520])
