"""예약 전 자동 점검(①, 10/4 밤). 눈으로 확인하다 놓친 것(무음 영상, 내부 용어, 슬래시 날짜, 같은 시각 겹침, 근거 없는 숫자)을 기계가 먼저 거른다.
사용:
  python3 pipeline/precheck.py video <mp4...>            소리 크기(-30dB보다 커야 함)·소리 줄 있음·1080x1920
  python3 pipeline/precheck.py text "<캡션>" | <파일>     내부 용어·슬래시 날짜·근거(cross_data)에 없는 퍼센트/명수
  python3 pipeline/precheck.py schedule                   앱 일정(sns_plan)에서 같은 채널 같은 분 겹침·하루 인스타 4개 초과·자료 나이
  python3 pipeline/precheck.py slot YYYY-MM-DDTHH:MM [net] 그 시각 칸이 비었는지(앱 일정 기준; 최신은 Metricool getScheduledPosts로 한 번 더)
  python3 pipeline/precheck.py all                         reel_swaps.json의 영상 전부 + 일정 점검
종료 코드 0=통과, 1=걸림. 샘플 서체 대조와 최종 눈 확인은 사람이 한다(QA_CHECKLIST.md)."""
import os, re, sys, json, subprocess, datetime as D, collections
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, "..")
SITE = os.environ.get("ZAOSEON_SITE", os.path.join(ROOT, "..", "zaoseon-site"))
BANNED = ["엔진", "의미축", "환산", "데이터 릴스", "교차 시험", "기궁", "6체계", "초안", "리포트", "흉성", "수린"]
SLASH = re.compile(r"(?<![\d./])(\d{1,2})/(\d{1,2})(?![\d/])")
def vol(path):
    out = subprocess.run(["ffmpeg", "-hide_banner", "-i", path, "-af", "volumedetect", "-vn", "-f", "null", "-"], capture_output=True, text=True).stderr
    m = re.search(r"mean_volume: (-?[\d.]+) dB", out); return float(m.group(1)) if m else None
def check_video(p):
    bad = []
    if not os.path.exists(p): return [f"{p}: 파일 없음"]
    pr = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,width,height", "-of", "csv=p=0", p], capture_output=True, text=True).stdout.split()
    if not any(x.startswith("audio") for x in pr): bad.append(f"{p}: 소리 줄 없음")
    v = vol(p)
    if v is None or v < -30: bad.append(f"{p}: 소리 너무 작음({v}dB, -30dB보다 커야 함)")
    return bad
def facts_text():
    f = os.path.join(ROOT, "content", "cross_data", "README.md")
    return open(f, encoding="utf-8").read() if os.path.exists(f) else ""
def check_text(t, facts=True):
    bad = []
    for w in BANNED:
        if w in t: bad.append(f"내부 용어 '{w}'")
    for m in SLASH.finditer(t):
        a, b = int(m.group(1)), int(m.group(2))
        if 1 <= a <= 12 and 1 <= b <= 31: bad.append(f"슬래시 날짜 '{m.group(0)}' ('{a}월 {b}일'로)")
    if facts:
        F = facts_text()
        if "무작위" in t or "자오선으로 계산" in t:
            for m in re.finditer(r"(\d+(?:\.\d+)?)\s*%", t):
                n = m.group(1)
                if n not in F and str(round(float(n))) not in F: bad.append(f"근거에 없는 퍼센트 {n}%")
    return bad
def load_plan():
    d = json.load(open(os.path.join(SITE, "public", "admin", "data.json"), encoding="utf-8")); return d, d["sns_plan"]
def check_schedule():
    d, plan = load_plan(); bad = []; age = D.datetime.now(D.timezone(D.timedelta(hours=9))) - D.datetime.fromisoformat(d["at"])
    if age > D.timedelta(hours=3): bad.append(f"앱 자료가 {age} 전 것이다. 새로 읽고 판단")
    seen = collections.defaultdict(list)
    for r in plan:
        for n in r["n"]: seen[(n, r["t"])].append((r["x"] or "")[:20])
    for (n, t), v in sorted(seen.items(), key=lambda x: x[0][1]):
        if len(v) > 1: bad.append(f"겹침 {t} {n} x{len(v)}: {' | '.join(v)}")
    ig = collections.Counter(r["t"][:10] for r in plan if "instagram" in r["n"])
    for day, c in sorted(ig.items()):
        if c > 4: bad.append(f"{day} 인스타 {c}개(4개 초과)")
    return bad
def main():
    a = sys.argv[1:]
    if not a: print(__doc__); return 0
    cmd, rest = a[0], a[1:]; bad = []
    if cmd == "video":
        for p in rest: bad += check_video(p)
    elif cmd == "text":
        t = rest[0]; t = open(t, encoding="utf-8").read() if os.path.exists(t) else t; bad = check_text(t)
    elif cmd == "schedule": bad = check_schedule()
    elif cmd == "slot":
        t = rest[0]; net = rest[1] if len(rest) > 1 else None; d, plan = load_plan()
        hit = [(r["n"], (r["x"] or "")[:24]) for r in plan if r["t"][:16] == t[:16] and (net is None or net in r["n"])]
        bad = [f"이미 있음 {t}: {hit}"] if hit else []
    elif cmd == "all":
        sw = json.load(open(os.path.join(ROOT, "content", "reel_swaps.json"), encoding="utf-8")); prefix = "https://raw.githubusercontent.com/zaoseon/sns-images/main/"
        for e in sw:
            v = e.get("video") or ""
            if v.startswith(prefix) and e.get("status") != "skip":
                bad += check_video(os.path.join(ROOT, v[len(prefix):].split("?")[0]))
        bad += check_schedule()
    else: print(__doc__); return 1
    for b in bad: print("걸림:", b)
    print("통과" if not bad else f"{len(bad)}건 걸림"); return 1 if bad else 0
if __name__ == "__main__": sys.exit(main())
