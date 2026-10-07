"""영상 엔진 장면이 고정 요소(상단 문구·주소·AI 표시) 자리를 침범하는지 자동으로 찾는다(10/6 확정 규칙 R01~R03).
방법: 고정 요소를 끄고 장면을 그려, 고정 요소가 들어갈 자리 상자에 밝은 화소(글자·그림)가 있으면 충돌로 센다.
사용: python3 pipeline/engine_conflicts.py"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.abspath(os.path.join(HERE, "..")); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(R, "content"))
import numpy as np
import clip_motion as M
BOX = dict(상단왼쪽=(50, 335, 240, 395), 상단오른쪽=(440, 338, 905, 392), 주소=(640, 1418, 905, 1470), AI=(55, 1418, 540, 1470), 안전영역위=(50, 140, 900, 325))   # 안전영역위: 인스타 상단 버튼에 가려지는 곳(R04) — 배지·글자가 있으면 위반
def bright(a, b, thr=150):
    x0, y0, x1, y1 = b; r = a[y0:y1, x0:x1].mean(axis=2); return int((r > thr).sum())
def scan_pos(SC):
    """배지·글자를 놓은 위치를 기록해 안전 영역 위(y<330)에 있는 것을 센다(R04). 밝기로 재면 배경 금색 선과 섞여서 위치를 직접 기록한다."""
    M.BRAND = False; out = []
    for key, scenes in SC.items():
        for i, (dur, fn) in enumerate(scenes):
            M.LOG = []; M.still(scenes, i, min(dur * .65, dur - .05), "/tmp/_ec.png"); bad = [e for e in M.LOG if e[1] < 330]
            if bad: out.append((key[0], i, bad[:2]))
    M.LOG = None; M.BRAND = True; return out
def scan(SC, only=None):
    M.BRAND = False; out = []
    for key, scenes in SC.items():
        if only and key[0] not in only: continue
        for i, (dur, fn) in enumerate(scenes):
            p = "/tmp/_ec.png"; M.still(scenes, i, min(dur * .65, dur - .05), p)
            from PIL import Image
            a = np.asarray(Image.open(p).convert("RGB")).astype(int); hits = {k: bright(a, b) for k, b in BOX.items() if k != "AI"}; hits["안전영역위"] = bright(a, BOX["안전영역위"], 150) if bright(a, BOX["안전영역위"], 150) > 500 else 0
            ai_box = bright(a, BOX["AI"]); bad = [k for k, v in hits.items() if v > (500 if k == "안전영역위" else 60)]
            if ai_box > 60: bad.append("AI(정월이 나올 때만)")
            if bad: out.append((key[0], i, bad))
    M.BRAND = True; return out
def load_all():
    import clips_motion as CM
    for m in ("clips_motion_w41", "clips_motion_w42"):
        try: __import__(m)
        except Exception as e: print("불러오기 실패", m, str(e)[:60])
    return CM.SC
if __name__ == "__main__":
    SC = load_all(); res = scan(SC); ids = sorted({k[0] for k in SC}); print("클립", len(ids), "개 · 충돌 장면", len(res))
    from collections import Counter
    c = Counter(r[0] for r in res); print({k: v for k, v in sorted(c.items())})
    for r in res[:14]: print(r)
    json.dump(res, open("/tmp/engine_conflicts.json", "w", encoding="utf-8"), ensure_ascii=False)
