"""K-128(대표 10/17 11:50): '이 글은 재미로…' 같은 면책 문장은 캡션·스레드·네이버 원고·클립에 넣지 않는다.
글로만 있던 기준을 검사로 바꾼다(10/17~10/24 '기준을 검사로' 주간).

보는 곳
1. 글을 만드는 코드(pipeline/·content/·naver/ 의 .py): 면책 문장을 '써 넣는' 글자. 찾아 지우는 코드(정규식·assert·주석)는 건너뛴다.
   지난 주 한 번 쓰고 끝난 옛 빌드 스크립트는 content/audit/disclaimer_baseline.json 에 빚으로 적어 두고 새로 생기는 것만 막는다.
2. 아직 안 나간 글: 승인 대기·보류 카드 캡션(reel_swaps status new·hold), 아직 안 올린 릴스 재활용 클립 설명(clips_from_reels, 올릴 날이 내일부터),
   클립 v3 설명(clips_v3.json), 네이버 원고 원본 중 아직 발행 안 한 글(pages.json done 아님 — 그릴 때 make_page 가 빼지만 원본에도 없게).
이미 예약·발행한 글은 보지 않는다(K-128: 다른 이유로 고칠 때 같이 뺀다).
사용: python3 pipeline/disclaimer_audit.py   (qa_all 이 같이 돌린다)"""
import os, re, json, glob, datetime as D
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAT = re.compile(r"(이 (?:내용|글)은 재미로|재미로,\s*(?:그리고\s*)?나를 돌아보는|재미로 즐기는|재미로 참고|재미로 보는 풀이|재미로 본 순위|재미와 자기 이해를 위한)")
SKIP_LINE = re.compile(r"re\.compile|re\.search|re\.sub|DISC_RE|PAT\b|assert |^\s*#|bad\.append|not in body")
BASE = os.path.join(R, "content", "audit", "disclaimer_baseline.json")

def code_hits():
    out = []
    for f in sorted(glob.glob(os.path.join(R, "pipeline", "*.py")) + glob.glob(os.path.join(R, "content", "**", "*.py"), recursive=True) + glob.glob(os.path.join(R, "naver", "*.py"))):
        if f.endswith("disclaimer_audit.py"): continue
        for i, line in enumerate(open(f, encoding="utf-8", errors="ignore"), 1):
            if PAT.search(line) and not SKIP_LINE.search(line):
                out.append((os.path.relpath(f, R), i, PAT.search(line).group(0)))
    return out

def data_hits(today=None):
    today = today or D.date.today().isoformat(); out = []
    try:
        for x in json.load(open(os.path.join(R, "content", "reel_swaps.json"), encoding="utf-8")):
            if x.get("status") in ("new", "hold") and PAT.search(json.dumps(x.get("caption", ""), ensure_ascii=False)):
                out.append(("reel_swaps.json", x.get("id"), "승인 대기 카드 캡션"))
    except FileNotFoundError: pass
    try:
        for c in json.load(open(os.path.join(R, "content", "clips_from_reels.json"), encoding="utf-8")).get("clips", []):
            if (c.get("upload") or "") > today and PAT.search(c.get("desc", "")): out.append(("clips_from_reels.json", c.get("id"), "아직 안 올린 클립 설명"))
    except FileNotFoundError: pass
    try:
        for k, c in json.load(open(os.path.join(R, "content", "clips_v3.json"), encoding="utf-8")).get("clips", {}).items():
            if PAT.search(c.get("desc", "")): out.append(("clips_v3.json", k, "클립 v3 설명"))
    except FileNotFoundError: pass
    try:
        for k, v in json.load(open(os.path.join(R, "naver", "pages.json"), encoding="utf-8")).items():
            if not v.get("done") and PAT.search(v.get("body", "")): out.append(("naver/pages.json", k, "발행 전 네이버 원고 원본"))
    except FileNotFoundError: pass
    return out

def run(verbose=False):
    base = set(json.load(open(BASE, encoding="utf-8")).get("files", [])) if os.path.exists(BASE) else set()
    new = [h for h in code_hits() if h[0] not in base] + data_hits()
    if verbose:
        for h in new: print("  [면책 문장]", *h)
    return new

if __name__ == "__main__":
    import sys
    if "--baseline" in sys.argv:   # 옛 빌드 스크립트를 빚으로 적는다(처음 한 번)
        files = sorted({h[0] for h in code_hits()})
        json.dump({"note": "K-128 이전에 한 번 쓰고 끝난 옛 빌드 스크립트. 건드리는 김에 지우고 이 목록에서 뺀다.", "files": files}, open(BASE, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("빚", len(files), "파일"); sys.exit(0)
    bad = run(True)
    print(f"면책 문장(K-128) 새로 생긴 곳 {len(bad)}곳")
    sys.exit(1 if bad else 0)
