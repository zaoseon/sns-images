"""장면 배치 검사(10/7 대표 지적: 글이 아래로 쏠림 · 하단 글이 하단 주소에 붙음).
방법: 같은 장면을 '내용 있음/없음' 두 번 그려 차이로 실제 글·그림이 차지한 세로 범위를 잰다(상단 문구·주소는 끈다). 고정 요소 기준:
  상단 문구 아래 395 ~ 하단 주소 위 1425 → 가운데 910 · 맨 위 475 이상(R21) · 맨 아래 1375 이하(주소와 50px 이상, R21 확장)
사용: python3 pipeline/layout_audit.py"""
import os, sys
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.abspath(os.path.join(HERE, "..")); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(R, "content"))
import clip_motion as M
CENTER, TOP_MIN, BOT_MAX = 910, 475, 1375
def bbox(sc, i, t=None, y0=400, y1=1440):
    M.BRAND = False; t = sc[i][0] * .86 if t is None else t
    M.still(sc, i, t, "/tmp/_l1.png"); sc2 = list(sc); sc2[i] = (sc[i][0], lambda c: None); M.still(sc2, i, t, "/tmp/_l2.png")
    a = np.asarray(Image.open("/tmp/_l1.png").convert("RGB")).astype(int); b = np.asarray(Image.open("/tmp/_l2.png").convert("RGB")).astype(int)
    m = (np.abs(a - b).sum(axis=2)[y0:y1] > 40); ys = np.where(m.sum(axis=1) > 2)[0]; M.BRAND = True
    return None if len(ys) == 0 else (y0 + int(ys.min()), y0 + int(ys.max()))
def audit(name, sc, tol=35, char_scenes=()):
    """char_scenes: 정월이 화면 아래에 붙어 나오는 장면 번호(1부터) — 바닥 규칙·가운데 규칙에서 뺀다."""
    out = []
    for i in range(len(sc)):
        bb = bbox(sc, i)
        if bb is None: continue
        top, bot = bb; c = (top + bot) / 2; why = []
        if top < TOP_MIN: why.append(f"맨 위 {top} (475 이상이어야 함)")
        if (i + 1) not in char_scenes:
            if bot > BOT_MAX: why.append(f"맨 아래 {bot} (주소와 {1425 - bot}px, 50px 이상이어야 함)")
            if abs(c - CENTER) > tol: why.append(f"가운데 {c:.0f} ({'아래' if c > CENTER else '위'}로 {abs(c - CENTER):.0f}px 쏠림)")
        out.append((name, i + 1, top, bot, round(c), why))
    return out
if __name__ == "__main__":
    import pilot_variety as PV, clips_motion_2027 as S27
    PV.AUDIT = True; bad = 0
    for nm, sc, cs in (("시범 A 데이터", PV.SC_A, ()), ("시범 B 비교", PV.SC_B, ()), ("시범 C 오행", PV.SC_C, (6,)), ("수성 역행", S27.SC, (4,)), ("수성 역행 표지", [(4.0, S27.S_cover)], ())):
        for r in audit(nm, sc, char_scenes=cs):
            bad += 1 if r[5] else 0
            print(f"{r[0]} {r[1]}번 장면: 범위 {r[2]}~{r[3]} · 가운데 {r[4]}", "→ " + " / ".join(r[5]) if r[5] else "")
    print("기준을 벗어난 장면:", bad)
