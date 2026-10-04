"""카드 1장 → 훅 릴스(1080x1920, 약 10초, 무음). 9/30: 인스타 조회가 거의 없어 릴스 중심으로 전환.
구성: 훅 화면 2.2초 → 카드 5.5초 → 팔로우 유도 2.5초"""
import os, sys, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render as R
from PIL import Image, ImageDraw
def frames(card, hook, sub, out, bottom="나는 몇 개 겹쳐? 댓글로 알려 주세요"):
    W, H = 1080, 1920; fs = []
    a = Image.new("RGB", (W, H), R.INK); d = ImageDraw.Draw(a)
    d.text((W//2, 560), "자오선 · 사주·별자리·숫자 테스트", font=R.F(R.MED, 38), fill=R.GOLD, anchor="mm")
    y = 700
    for l in R.wrap(d, hook, R.F(R.SER, 92), W-140): d.text((W//2, y), l, font=R.HF(l, R.F(R.SER, 92)), fill=R.PAPER, anchor="mm"); y += 120
    y += 40
    for l in R.wrap(d, sub, R.F(R.MED, 44), W-160): d.text((W//2, y), l, font=R.F(R.MED, 44), fill=R.GOLD, anchor="mm"); y += 66
    a.save(out+"_a.jpg", quality=92); fs.append(out+"_a.jpg")
    b = Image.new("RGB", (W, H), R.INK); b.paste(Image.open(card), (0, 285)); d = ImageDraw.Draw(b)
    d.rectangle([0, 285+1350-135, W, 285+1350], fill=R.INK)
    d.text((W//2, 170), hook if len(hook) <= 18 else hook[:17]+"…", font=R.HF(hook, R.F(R.SER, 56)), fill=R.PAPER, anchor="mm")
    d.text((W//2, 1720), bottom, font=R.F(R.MED, 40), fill=R.GOLD, anchor="mm")
    b.save(out+"_b.jpg", quality=92); fs.append(out+"_b.jpg")
    c = Image.new("RGB", (W, H), R.INK); d = ImageDraw.Draw(c)
    for i, (t, f, col) in enumerate([("매일 저녁", R.F(R.SER, 80), R.GOLD), ("나를 알아보는 테스트", R.F(R.SER, 80), R.PAPER),
                                        ("팔로우하면 다음 편을", R.F(R.MED, 50), R.PAPER), ("놓치지 않아요", R.F(R.MED, 50), R.PAPER),
                                        ("내 태어난 날 기운은 프로필 링크에서 1초", R.F(R.MED, 38), R.DIM)]):
        d.text((W//2, 700 + i*120 + (40 if i >= 2 else 0) + (60 if i == 4 else 0)), t, font=f, fill=col, anchor="mm")
    c.save(out+"_c.jpg", quality=92); fs.append(out+"_c.jpg")
    return fs
def reel(card, hook, sub, mp4, bottom="나는 몇 개 겹쳐? 댓글로 알려 주세요"):
    fs = frames(card, hook, sub, mp4[:-4], bottom); dur = [2.2, 5.5, 2.5]; fade = 0.35
    cmd = ["ffmpeg", "-y", "-loglevel", "error"]
    for f, t in zip(fs, dur): cmd += ["-loop", "1", "-t", str(t), "-i", f]
    cmd += ["-f", "lavfi", "-t", str(sum(dur)-2*fade), "-i", "anullsrc=r=44100:cl=stereo"]
    fl = f"[0:v][1:v]xfade=transition=fade:duration={fade}:offset={dur[0]-fade:.2f}[v1];[v1][2:v]xfade=transition=fade:duration={fade}:offset={dur[0]+dur[1]-2*fade:.2f}[v2];[v2]format=yuv420p,fps=30[vout]"
    cmd += ["-filter_complex", fl, "-map", "[vout]", "-map", "3:a", "-c:v", "libx264", "-crf", "20", "-c:a", "aac", "-b:a", "96k", "-shortest", "-movflags", "+faststart", mp4]
    subprocess.run(cmd, check=True)
    for f in fs: os.remove(f)
