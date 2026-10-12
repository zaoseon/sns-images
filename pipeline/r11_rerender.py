"""10/12 예약 릴스 수정 1단계: 옛 5요소 틀 릴스를 '마음 코치 정월' 라벨로 다시 렌더 -> 2026-r11/src/<묶음>/<키>.mp4 (끝 장면은 r11_batch.py 가 R11로 교체).
사용: EDITOR_HTML=pipeline/assets/carousel_editor_2026-10-03_v5.html python3 pipeline/r11_rerender.py [sched|w40|gapeul|swap]"""
import sys, os
sys.path.insert(0, 'pipeline'); sys.path.insert(0, 'content')
import carousel_sets as CS, carousel_editor as CE, reel_v2 as RV, reel_plan as RP
OUT = os.path.join(CE.ROOT, "2026-r11", "src"); which = sys.argv[1:] or ["sched", "w40", "gapeul", "swap"]
CHAIN = {"기": "경(庚)일생 편", "경": "신(辛)일생 편", "신": "임(壬)일생 편", "임": "계(癸)일생 편", "계": "갑(甲)일생 편", "갑": "을(乙)일생 편", "을": "사주·별자리·숫자 테스트"}
if "sched" in which or "w40" in which:
    defs = RP.ig_defs()
    if "sched" in which:
        keep = {}
        for k in ("2026-10-07", "2026-10-08", "2026-10-09"):
            d, ov = defs[k]; d = dict(d); ov = dict(ov); nt = CHAIN[CS.SETS[k]["dayChar"]]; d["nextTitle"] = nt; ov["nextTitle"] = nt; ov["nextBadge"] = "다음 편"; keep[k] = (d, ov)
        RV.render(list(keep), keep, os.path.join(OUT, "sched"))
    if "w40" in which: RV.render(["2026-10-10", "2026-10-11"], defs, os.path.join(OUT, "w40"))
if "gapeul" in which:
    import runpy; sys.argv = ["x"]; src = open("pipeline/gapeul_reels_v5.py", encoding="utf-8").read().split("root=os.path.join")[0]
    ns = {}; exec(compile(src, "gapeul", "exec"), ns); root = os.path.join(OUT, "gapeul"); RV.render(['gab', 'eul'], ns["igd"], root)
if "swap" in which:
    import swap_reels_w43 as W, swap_reels_w43b as W2
    RV.render(list(W.defs), W.defs, os.path.join(OUT, "swap")); RV.render(list(W2.defs), W2.defs, os.path.join(OUT, "swap"))
print("R11_RERENDER_DONE", which)
