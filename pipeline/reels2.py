"""띠 릴스 v2 (10/3 대표: 피드에서 제목·안내가 잘리고 순수 검정). 캐러셀 5장을 4:5(피드 크롭)에 맞춰 y=285에 그대로 놓고,
위·아래 막대는 우주 배경으로 채우며, 잘리는 곳(y 150, 1720)에 있던 글자는 없앤다. 안내 문구는 카드 하단 가림띠(피드 안, y≈1567)로 옮긴다.
출력: 2026-w42/v2/reel_NN.mp4 (원본 reel_NN.mp4는 그대로). 무음(기존과 같음). 사용: python3 pipeline/reels2.py ../content/2026-w42.json [번호 ...]"""
import json, os, sys, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import render as R, clip_motion as M
from PIL import Image, ImageDraw, ImageFilter
DUR = [2.5, 4.0, 4.5, 4.5, 4.0]; FADE = 0.4
HINT = ["끝까지 보면 내 띠의 좋은 달이 나와요"] * 2 + ["저장해 두고 달마다 꺼내 보세요"] * 2 + ["내 태어난 날 기운은 프로필 링크에서"]
_bg = None
def bg():
    global _bg
    if _bg is None: _bg = M.bg_static().convert("RGB")
    return _bg
def frame(src, dst, k):
    img = bg().copy(); card = Image.open(src).convert("RGB")
    m = Image.new("L", card.size, 255); md = ImageDraw.Draw(m)
    for i in range(26): a = int(255 * i / 26); md.line((0, i, card.width, i), fill=a); md.line((0, card.height - 1 - i, card.width, card.height - 1 - i), fill=a)
    band = card.getpixel((8, card.height - 140)); d = ImageDraw.Draw(card); d.rectangle([0, 1350 - 135, 1080, 1350], fill=band)    # 캐러셀 하단(넘겨 보세요, 점) 가림
    d.text((540, 1350 - 68), HINT[k - 1], font=R.F(R.MED, 40), fill=R.PAPER, anchor="mm")
    img.paste(card, (0, 285), m); img.save(dst, quality=95)
def build(src, only=None):
    folder = os.path.join(os.path.dirname(os.path.abspath(src)), "..", os.path.splitext(os.path.basename(src))[0]); outd = os.path.join(folder, "v2"); os.makedirs(outd, exist_ok=True); out = []
    for i, p in enumerate(json.load(open(src))["posts"]):
        if p["image"]["type"] != "tti": continue
        pre = f"{i+1:02d}"
        if only and pre not in only: continue
        fr = []
        for k in range(1, 6):
            f = f"/tmp/reel2_{pre}_{k}.jpg"; frame(f"{folder}/{pre}_{k}.jpg", f, k); fr.append(f)
        cmd = ["ffmpeg", "-y", "-loglevel", "error"]
        for f, t in zip(fr, DUR): cmd += ["-loop", "1", "-t", str(t), "-i", f]
        cmd += ["-f", "lavfi", "-t", str(sum(DUR) - 4 * FADE), "-i", "anullsrc=r=44100:cl=stereo"]
        fl, last, off = [], "[0:v]", 0.0
        for k in range(1, 5):
            off += DUR[k - 1] - FADE; fl.append(f"{last}[{k}:v]xfade=transition=fade:duration={FADE}:offset={off:.2f}[v{k}]"); last = f"[v{k}]"
        fl.append(f"{last}format=yuv420p,fps=30[vout]"); mp4 = f"{outd}/reel_{pre}.mp4"
        cmd += ["-filter_complex", ";".join(fl), "-map", "[vout]", "-map", "5:a", "-c:v", "libx264", "-crf", "20", "-preset", "medium", "-c:a", "aac", "-b:a", "96k", "-shortest", "-movflags", "+faststart", mp4]
        subprocess.run(cmd, check=True); out.append(mp4)
    return out
if __name__ == "__main__":
    for m in build(sys.argv[1], set(sys.argv[2:]) or None): print(m, os.path.getsize(m) // 1024, "KB")
