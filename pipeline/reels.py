"""띠별 캐러셀(5장) -> 세로 릴스 영상(1080x1920, 무음). 사용: python3 reels.py ../content/2026-w42.json
출력: <폴더>/reel_NN.mp4 (NN = 게시물 번호)"""
import json, os, sys, subprocess
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render as R
DUR = [2.5, 4.0, 4.5, 4.5, 4.0]; FADE = 0.4
BOTTOM = ["끝까지 보면 내 띠의 좋은 달이 나와요"]*2 + ["저장해 두고 달마다 꺼내 보세요"]*2 + ["내 태어난 날 기운은 프로필 링크에서"]
def frame(src, dst, name, k):
    img = Image.new("RGB", (1080, 1920), R.INK); d = ImageDraw.Draw(img)
    img.paste(Image.open(src), (0, 285))
    d.rectangle([0, 285 + 1350 - 135, 1080, 285 + 1350], fill=R.INK)  # 캐러셀용 하단(넘겨 보세요, 점) 가리기
    d.text((540, 150), f"2027 {name} 운세", font=R.F(R.SER, 64), fill=R.GOLD, anchor="mm")
    d.text((540, 225), "정미년 · 붉은 양의 해", font=R.F(R.MED, 32), fill=R.DIM, anchor="mm")
    d.text((540, 1720), BOTTOM[k-1], font=R.F(R.MED, 36), fill=R.PAPER, anchor="mm")
    img.save(dst, quality=95)
def build(src):
    folder = os.path.join(os.path.dirname(os.path.abspath(src)), "..", os.path.splitext(os.path.basename(src))[0])
    out = []
    for i, p in enumerate(json.load(open(src))["posts"]):
        if p["image"]["type"] != "tti": continue
        pre = f"{i+1:02d}"; fr = []
        for k in range(1, 6):
            f = f"/tmp/reel_{pre}_{k}.jpg"; frame(f"{folder}/{pre}_{k}.jpg", f, p["image"]["name"], k); fr.append(f)
        cmd = ["ffmpeg", "-y", "-loglevel", "error"]
        for f, t in zip(fr, DUR): cmd += ["-loop", "1", "-t", str(t), "-i", f]
        cmd += ["-f", "lavfi", "-t", str(sum(DUR) - 4*FADE), "-i", "anullsrc=r=44100:cl=stereo"]
        fl, last, off = [], "[0:v]", 0.0
        for k in range(1, 5):
            off += DUR[k-1] - FADE
            fl.append(f"{last}[{k}:v]xfade=transition=fade:duration={FADE}:offset={off:.2f}[v{k}]"); last = f"[v{k}]"
        fl.append(f"{last}format=yuv420p,fps=30[vout]")
        mp4 = f"{folder}/reel_{pre}.mp4"
        cmd += ["-filter_complex", ";".join(fl), "-map", "[vout]", "-map", "5:a", "-c:v", "libx264", "-crf", "20",
                "-preset", "medium", "-c:a", "aac", "-b:a", "96k", "-shortest", "-movflags", "+faststart", mp4]
        subprocess.run(cmd, check=True); out.append(mp4)
    return out
if __name__ == "__main__":
    for m in build(sys.argv[1]): print(m, os.path.getsize(m)//1024, "KB")
