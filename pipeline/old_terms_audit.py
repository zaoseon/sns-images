"""K-086 '세 지도' 같은 옛 표현 검사(대표 10/16 '세 지도라는 말을 쓰지 않는다', 기준 대장 K-086 · 10/17~24 '미반영을 검사로' 주간).

낱말 원본은 copy_rules.옛표현 하나(새로 적지 않는다). 재는 곳 — 앞으로 나갈 글자만(지난 글·메모·작업 기록은 안 잰다):
  1) naver/pages.json : 발행 전(done 아님, dt 가 오늘 이후) 원고 제목·본문
  2) content/reel_swaps.json : 오늘 이후 날짜이고 status 가 new/ok 인 카드의 title·caption·posts[].caption (인스타·스레드·릴스·클립 글)
  3) content/naver_clip_kit.json : 오늘 이후 클립 설명·제목(있으면)
사용: python3 pipeline/old_terms_audit.py   (걸리면 종료 코드 1)"""
import os, sys, json, datetime as D
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
import copy_rules as CR

WORDS = CR.옛표현


def _hit(t):
    return [w for w in WORDS if w in (t or "")]


def run(today=None):
    today = today or D.date.today().isoformat(); bad = []
    pages = json.load(open(os.path.join(R, "naver", "pages.json"), encoding="utf-8"))
    for pid, v in pages.items():
        if v.get("done") or (v.get("dt") or "")[:10] < today: continue
        for f in ("title", "body"):
            for w in _hit(v.get(f)): bad.append(("네이버 원고", pid, f, w))
    for x in json.load(open(os.path.join(R, "content", "reel_swaps.json"), encoding="utf-8")):
        if x.get("status") not in ("new", "ok") or (x.get("date") or "") < today: continue
        texts = [("title", x.get("title")), ("caption", x.get("caption"))] + [(f"posts[{k}]", p.get("caption")) for k, p in enumerate(x.get("posts") or [])]
        for f, t in texts:
            for w in _hit(t): bad.append(("승인 카드", x.get("id"), f, w))
    kp = os.path.join(R, "content", "naver_clip_kit.json")
    if os.path.exists(kp):
        kit = json.load(open(kp, encoding="utf-8"))
        items = kit if isinstance(kit, list) else (kit.get("clips") or kit.get("items") or list(kit.values()) if isinstance(kit, dict) else [])
        for it in items:
            if not isinstance(it, dict) or (str(it.get("rec") or it.get("date") or ""))[:10] < today: continue
            for f in ("title", "desc", "caption"):
                for w in _hit(it.get(f)): bad.append(("네이버 클립", it.get("id"), f, w))
    return bad


if __name__ == "__main__":
    bad = run()
    for b in bad: print("✗", " · ".join(map(str, b)))
    print(f"K-086 옛 표현({'·'.join(WORDS)}): 앞으로 나갈 글 걸림 {len(bad)}곳")
    sys.exit(1 if bad else 0)
