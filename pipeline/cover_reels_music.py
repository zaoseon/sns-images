"""12:00 릴스 표지 교체본(2026-w40car-reel3/2026-10-NN.mp4, 9.5초)이 무음이라 경쾌한 음악을 입힌다(화면은 그대로, 소리만).
10/3 밤 대표 지적 \"릴스에 왜 음악이 없어?\"의 두 번째 원인. 사용: python3 pipeline/cover_reels_music.py -> 2026-w40car-reel3/music/2026-10-NN.mp4"""
import os, sys, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); ROOT = os.path.join(HERE, "..")
import reel_music as RM
DAYS = ["04", "05", "06", "07", "08", "09", "10", "11"]
STY = ["상큼 팝", "발랄 우쿨렐레", "경쾌 신스팝", "통통 마림바"]; KEYS = ["G", "D", "C", "F", "A", "E", "G", "D"]
out = os.path.join(ROOT, "2026-w40car-reel3", "music"); os.makedirs(out, exist_ok=True)
def dur(p): return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]).decode().strip())
for i, d in enumerate(DAYS):
    src = os.path.join(ROOT, "2026-w40car-reel3", f"2026-10-{d}.mp4"); L = dur(src)
    style = STY[i % 4]; seed = 80 + i; bpm = RM.pick_bpm(style, seed); beats = max(8, int((L - 0.3) * bpm / 60.0))
    wav = f"/tmp/cov_{d}.wav"; RM.compose_up(style, beats, seed, wav, key=KEYS[i], bpm=bpm, cuts=[])
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-i", wav, "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "128k", "-t", f"{L:.3f}", "-shortest", "-movflags", "+faststart", os.path.join(out, f"2026-10-{d}.mp4")], check=True)
    print(d, style, bpm, f"{L:.1f}s")
