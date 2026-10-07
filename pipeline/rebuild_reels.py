"""릴스 14편을 새 엔진 장면으로 다시 렌더(10/7, 확정 규칙 적용). 호출 시간 한도 안에서 나눠 진행하고 이어서 할 수 있다.
사용: python3 pipeline/rebuild_reels.py --budget=150"""
import os, sys, json, time, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.abspath(os.path.join(HERE, "..")); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(R, "content"))
import clip_motion as M, reels_engine as RE, music_plan as MP
DONE = os.path.join(R, "content", "reels_rebuild_done.json"); done = set(json.load(open(DONE, encoding="utf-8"))) if os.path.exists(DONE) else set()
budget = float(next((a.split("=")[1] for a in sys.argv[1:] if a.startswith("--budget=")), 1e9)); T0 = time.time()
D = RE.all_defs()
for (dd, key), (d, hint) in D.items():
    tag = f"{dd}/{key}"
    if tag in done: continue
    if time.time() - T0 > budget: print("시간 한도 — 다음 호출에서 이어서", flush=True); break
    t1 = time.time(); sc = RE.scenes(d, hint); outdir = os.path.join(R, dd); os.makedirs(outdir, exist_ok=True)
    p, dur = M.render(key, sc, outdir); mi = MP.choose("data", f"reel-{key}"); MP.mux(p, [x for x, _ in sc], mi, 200 + len(done))
    done.add(tag); json.dump(sorted(done), open(DONE, "w", encoding="utf-8")); print(tag, round(dur, 1), "초 · 음악", mi["style"], mi["bpm"], f"· {time.time() - t1:.0f}초 걸림", flush=True)
