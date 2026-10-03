"""12:00 릴스(편집기 방식 `2026-w40car-reel2/`)의 표지만 안전 영역·우주 배경·조합2 색으로 다시 만들어 붙인다 (10/3 대표: 배지가 피드에서 잘리고 표지 위가 순수 검정).
표지 2.6초(검정 바탕, 배지 y≈285)를 새 표지로 바꾸고, 뒤의 성격·연애·돈·CTA 장면은 원본을 그대로 쓴다. 원본에는 손대지 않고 `2026-w40car-reel3/`에 쓴다.
사용: python3 pipeline/reel_cover.py 2026-10-04 [2026-10-05 ...]"""
import os, sys, subprocess, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, ".."); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(ROOT, "content"))
import clip_motion as M, safezone as Z, palette as P
P.apply_to_engine(M)
import reel_sets as RS
from PIL import Image, ImageChops
SER = os.path.join(HERE, "fonts", "serif.otf")
def cover_scene(r):
    hook = r["hook"].split("\n"); hook_t = hook[0] + "\n*" + "\n".join(hook[1:]) + "*" if len(hook) > 1 else "*" + hook[0] + "*"
    def f(c):
        M.chip(c, r["kicker"], 345, .05)
        y = M.text(c, hook_t, 445, .2, 104, color=M.WHITE, path=SER, maxw=820, lh=1.25, stagger=.2)
        M.text(c, r["sub"], y + 28, .8, 42, color=(255, 255, 255, 255), path=M.MED, maxw=820, lh=1.3, stagger=.15)
        M.character(c, r["face"], t0=.3, width=730, bottom=1455)
    return f
def check(scene, dur):
    bad = []
    for t in (.8, 1.4, 2.0):
        a = Image.new("RGB", (Z.W, Z.H)); M.background(a, t, 10); b = a.copy(); scene(M.Ctx(b, t, dur))
        bb = ImageChops.difference(a, b).convert("L").point(lambda v: 255 if v > 24 else 0).getbbox()
        if bb and not Z.inside(bb): bad.append((t, bb))
    return bad
def build(date):
    r = RS.REELS[date]; dur = 2.9; sc = cover_scene(r); bad = check(sc, dur)
    if bad: raise SystemExit(f"안전 영역 밖: {date} {bad}")
    out_dir = os.path.join(ROOT, "2026-w40car-reel3"); os.makedirs(out_dir, exist_ok=True)
    cov, _ = M.render("cover_" + date, [(dur, sc)], "/tmp/covers")
    orig = os.path.join(ROOT, "2026-w40car-reel2", date + ".mp4"); out = os.path.join(out_dir, date + ".mp4")
    fl = "[0:v][1:v]xfade=transition=fade:duration=0.3:offset=2.6,format=yuv420p,fps=30[v]"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", cov, "-ss", "2.6", "-i", orig, "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-filter_complex", fl, "-map", "[v]", "-map", "2:a", "-c:v", "libx264", "-crf", "20", "-c:a", "aac", "-b:a", "96k", "-shortest", "-movflags", "+faststart", out], check=True)
    return out
if __name__ == "__main__":
    for d in sys.argv[1:]:
        o = build(d); print(d, "->", o, subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", o], capture_output=True, text=True).stdout.strip(), "초")
