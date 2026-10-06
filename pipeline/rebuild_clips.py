"""글 연결 클립을 새 확정 규칙(상단 문구·주소·AI 고지)으로 다시 렌더한다(10/6). 장면 길이가 같으므로 기존 영상의 음악을 그대로 꺼내 새 영상에 입힌다.
사용: python3 pipeline/rebuild_clips.py n34-c1 n35-c1 ...  (기본: n34~n46)"""
import os, sys, shutil, subprocess, time
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.abspath(os.path.join(HERE, "..")); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(R, "content"))
import clip_motion as M, engine_conflicts as EC
SC = EC.load_all(); M.BRAND = True; M.AVOID = True
import json
DONE = os.path.join(R, "content", "clip_rebuild_done.json"); done = set(json.load(open(DONE, encoding="utf-8"))) if os.path.exists(DONE) else set()
args = [a for a in sys.argv[1:] if not a.startswith("--")]; budget = float(next((a.split("=")[1] for a in sys.argv[1:] if a.startswith("--budget=")), 1e9)); T0 = time.time()
ids = [c for c in (args or [f"n{n}-c1" for n in range(34, 47)]) if c not in done]
out = os.path.join(R, "clips_sop")
for cid in ids:
    if time.time() - T0 > budget: print("시간 한도 — 다음 호출에서 이어서", flush=True); break
    t0 = time.time(); mp4 = os.path.join(out, f"{cid}_12s.mp4"); aud = f"/tmp/aud_{cid}.m4a"
    has = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "stream=codec_type", "-of", "csv=p=0", mp4], capture_output=True, text=True).stdout.strip()
    if has: subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", mp4, "-vn", "-c:a", "copy", aud], check=True)
    p, d = M.render(f"{cid}_12s", SC[(cid, "12")], out)                      # 무음 새 영상(같은 이름으로 덮음)
    nm = mp4.replace(".mp4", "_nomusic.mp4"); shutil.copy(mp4, nm)
    if has:
        tmp = mp4 + ".tmp.mp4"; subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", nm, "-i", aud, "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "128k", "-shortest", "-movflags", "+faststart", tmp], check=True); os.replace(tmp, mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", "0.8", "-i", mp4, "-frames:v", "1", os.path.join(out, f"{cid}_thumb.png")], check=True)
    done.add(cid); json.dump(sorted(done), open(DONE, "w", encoding="utf-8")); print(cid, round(d, 1), "초", "음악" if has else "무음", f"{time.time() - t0:.0f}초 걸림", flush=True)
