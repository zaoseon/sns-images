"""띠 릴스 12편(2026-w42/v2/reel_NN.mp4, 영상은 무음이었음)에 경쾌한 음악을 입힌다. 영상 화면은 다시 인코딩하지 않고 소리 줄만 바꾼다(-c:v copy).
10/3 밤 대표 지적: \"릴스에 왜 음악이 없어?\" 스타일 4종(상큼 팝·발랄 우쿨렐레·경쾌 신스팝·통통 마림바)을 돌려 쓰고 시드·조성을 달리한다.
사용: python3 pipeline/zodiac_music.py  -> 2026-w42/v3/reel_NN.mp4 (원본 v2는 그대로 둔다)"""
import os, sys, subprocess, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); ROOT = os.path.join(HERE, "..")
import reel_music as RM
NS = ["03","05","07","09","11","13","17","19","21","23","25","27"]
STY = ["상큼 팝", "발랄 우쿨렐레", "경쾌 신스팝", "통통 마림바"]; KEYS = ["C", "D", "G", "F", "A", "E"]
def dur(p): return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]).decode().strip())
out = os.path.join(ROOT, "2026-w42", "v3"); os.makedirs(out, exist_ok=True)
for i, n in enumerate(NS):
    src = os.path.join(ROOT, "2026-w42", "v2", f"reel_{n}.mp4"); d = dur(src)
    style = STY[i % 4]; seed = 60 + i; bpm = RM.pick_bpm(style, seed); beats = int((d - 0.3) * bpm / 60.0)
    wav = f"/tmp/zod_{n}.wav"; RM.compose_up(style, beats, seed, wav, key=KEYS[i % 6], bpm=bpm, cuts=[])
    dst = os.path.join(out, f"reel_{n}.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-i", wav, "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "128k", "-t", f"{d:.3f}", "-shortest", "-movflags", "+faststart", dst], check=True)
    print(n, style, bpm, f"{d:.1f}s")
