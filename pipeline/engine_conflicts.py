"""영상 엔진 장면이 고정 요소(상단 문구·주소·AI 표시) 자리를 침범하는지 자동으로 찾는다(10/6 확정 규칙 R01~R03).
방법: 고정 요소를 끄고 장면을 그려, 고정 요소가 들어갈 자리 상자에 밝은 화소(글자·그림)가 있으면 충돌로 센다.
사용: python3 pipeline/engine_conflicts.py"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.abspath(os.path.join(HERE, "..")); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(R, "content"))
import numpy as np
import clip_motion as M
BOX = dict(상단왼쪽=(50, 335, 240, 395), 상단오른쪽=(440, 338, 905, 392), 주소=(640, 1418, 905, 1470), AI=(55, 1418, 540, 1470))
def bright(a, b, thr=150):
    x0, y0, x1, y1 = b; r = a[y0:y1, x0:x1].mean(axis=2); return int((r > thr).sum())
def scan(SC, only=None):
    M.BRAND = False; out = []
    for key, scenes in SC.items():
        if only and key[0] not in only: continue
        for i, (dur, fn) in enumerate(scenes):
            p = "/tmp/_ec.png"; M.still(scenes, i, min(dur * .65, dur - .05), p)
            from PIL import Image
            a = np.asarray(Image.open(p).convert("RGB")).astype(int); hits = {k: bright(a, b) for k, b in BOX.items() if k != "AI"}
            ai_box = bright(a, BOX["AI"]); bad = [k for k, v in hits.items() if v > 60]
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
