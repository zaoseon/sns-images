"""규칙 층(R01~R04·R18)을 적용해 영향받은 영상을 대기열로 다시 렌더한다(10/7). 호출 시간 한도 안에서 나눠 진행하고 이어서 한다.
대기열: 릴스 14 → 글 연결 클립 13 → 손 없는 날 9:16 클립 1 → 카드 고르기 4.   사용: python3 pipeline/rebuild_all.py --budget=190"""
import os, sys, json, time, shutil, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.abspath(os.path.join(HERE, "..")); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(R, "content"))
import clip_motion as M, reels_engine as RE, music_plan as MP, engine_conflicts as EC
DONE = os.path.join(R, "content", "rebuild_all_done.json"); done = set(json.load(open(DONE, encoding="utf-8"))) if os.path.exists(DONE) else set()
budget = float(next((a.split("=")[1] for a in sys.argv[1:] if a.startswith("--budget=")), 1e9)); T0 = time.time()
def job_reel(dd, key, d, hint, n):
    sc = RE.scenes(d, hint); out = os.path.join(R, dd); p, dur = M.render(key, sc, out); mi = MP.choose("data", f"reel-{key}"); MP.mux(p, [x for x, _ in sc], mi, 300 + n); return f"{dur:.1f}초 · 음악 {mi['style']}"
def job_clip(cid, SC):
    out = os.path.join(R, "clips_sop"); mp4 = os.path.join(out, f"{cid}_12s.mp4"); aud = f"/tmp/aud_{cid}.m4a"
    has = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "stream=codec_type", "-of", "csv=p=0", mp4], capture_output=True, text=True).stdout.strip()
    if has: subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", mp4, "-vn", "-c:a", "copy", aud], check=True)
    p, d = M.render(f"{cid}_12s", SC[(cid, "12")], out); nm = mp4.replace(".mp4", "_nomusic.mp4"); shutil.copy(mp4, nm)
    if has:
        tmp = mp4 + ".tmp.mp4"; subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", nm, "-i", aud, "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "128k", "-shortest", "-movflags", "+faststart", tmp], check=True); os.replace(tmp, mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", "0.8", "-i", mp4, "-frames:v", "1", os.path.join(out, f"{cid}_thumb.png")], check=True); return f"{d:.1f}초 · 음악 유지"
def job_s10():
    import clips_motion_s10 as S; out = os.path.join(R, "clips_post", "s10_9x16"); p, d = M.render("s10_12s", S.SC, out); mi = MP.choose("fun", "s10-clip-9x16"); MP.mux(p, [x for x, _ in S.SC], mi, 117)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", "0.8", "-i", p, "-frames:v", "1", os.path.join(out, "s10_thumb.png")], check=True); return f"{d:.1f}초 · 음악 {mi['style']}"
def job_pick(k):
    r = subprocess.run([sys.executable, os.path.join(HERE, "pick_reel.py"), k], capture_output=True, text=True, cwd=R)
    if r.returncode: raise RuntimeError((r.stdout + r.stderr)[-200:])
    return (r.stdout.strip().split("\n") or [""])[-1][:60]
D14 = RE.all_defs(); Q = [("릴스", f"{dd}/{key}", (dd, key, d, h, i)) for i, ((dd, key), (d, h)) in enumerate(D14.items())]
Q += [("클립", f"clips/{cid}", cid) for cid in [f"n{n}-c1" for n in range(34, 47)]] + [("s10", "s10", None)] + [("픽", f"pick/{k}", k) for k in ("oct17", "oct24", "oct31", "nov7")]
SC = EC.load_all() if any(q[0] == "클립" and q[1] not in done for q in Q) else None
for kind, tag, arg in Q:
    if tag in done: continue
    if time.time() - T0 > budget: print("시간 한도 — 다음 호출에서 이어서", flush=True); break
    t1 = time.time(); M.BRAND = True; M.AVOID = True
    msg = job_reel(*arg) if kind == "릴스" else job_clip(arg, SC) if kind == "클립" else job_s10() if kind == "s10" else job_pick(arg)
    done.add(tag); json.dump(sorted(done), open(DONE, "w", encoding="utf-8")); print(f"{kind} {tag} · {msg} · {time.time() - t1:.0f}초 걸림", flush=True)
print("남은 작업", sum(1 for _, t, _ in Q if t not in done), "/", len(Q))
