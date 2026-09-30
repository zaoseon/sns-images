"""릴스 새 틀 (9/30, 경쟁 분석 반영): 어두운 바탕 + 정월 얼굴 크게 + 노랑 대형 자막 + 상단 고정 배지.
장면: A 훅(2.5초) → B 내용(5.5초) → C 팔로우(2.5초)"""
import os, sys, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render as R, brand2 as B
from PIL import Image, ImageDraw, ImageFilter
W, H = 1080, 1920; YEL = (255, 214, 64); DARK = (16, 14, 13)
def face_bg(h=1150):
    im = Image.open(B.JW).convert("RGB"); r = W/im.width; im = im.resize((W, int(im.height*r)))
    im = im.crop((0, 0, W, min(h, im.height)))
    base = Image.new("RGB", (W, H), DARK); base.paste(im, (0, 0))
    g = Image.new("L", (1, 400)); [g.putpixel((0, y), int(255*y/399)) for y in range(400)]
    g = g.resize((W, 400)); dark = Image.new("RGB", (W, 400), DARK)
    base.paste(dark, (0, im.height-400), g); return base
def badge(d, text, y=70):
    f = R.F(R.SEMI, 36); w = int(d.textlength(text, font=f)) + 60
    d.rounded_rectangle([(W-w)//2, y, (W+w)//2, y+64], 32, fill=YEL); d.text((W//2, y+32), text, font=f, fill=DARK, anchor="mm")
def big(d, lines, y, size=112, col=YEL):
    for l in lines:
        f = R.HF(l, R.F(R.SEMI, size))
        d.text((W//2, y), l, font=f, fill=col, anchor="mm", stroke_width=6, stroke_fill=DARK); y += int(size*1.22)
    return y
def scene_a(path, series, hook_lines, sub):
    img = face_bg(); d = ImageDraw.Draw(img); badge(d, series)
    y = big(d, hook_lines, 1230); d.text((W//2, y+40), sub, font=R.F(R.MED, 46), fill=(255, 255, 255), anchor="mm")
    d.text((W-36, H-30), "정월은 AI로 생성한 가상 캐릭터예요", font=R.F(R.MED, 24), fill=(150, 144, 136), anchor="rs"); img.save(path, quality=92)
def scene_b_card(path, series, card_img):
    img = Image.new("RGB", (W, H), DARK); d = ImageDraw.Draw(img); badge(d, series)
    c = Image.open(card_img).convert("RGB").resize((960, 1200)); img.paste(c, (60, 220))
    d.text((W//2, 1540), "나는 몇 개 겹쳐?", font=R.F(R.SEMI, 80), fill=YEL, anchor="mm", stroke_width=5, stroke_fill=DARK)
    d.text((W//2, 1650), "댓글로 숫자만 남겨 주세요", font=R.F(R.MED, 46), fill=(255, 255, 255), anchor="mm"); img.save(path, quality=92)
def scene_b_text(path, series, hanja, lines):
    img = Image.new("RGB", (W, H), DARK); d = ImageDraw.Draw(img); badge(d, series)
    d.text((W//2, 560), hanja, font=R.F(R.SER, 420), fill=(60, 54, 48), anchor="mm")
    y = 950
    for l in lines:
        for ll in R.wrap(d, l, R.F(R.SEMI, 64), W-140): d.text((W//2, y), ll, font=R.F(R.SEMI, 64), fill=(255, 255, 255), anchor="mm"); y += 88
        y += 40
    d.text((W//2, 1650), "맞으면 ♥, 떠오르는 사람은 태그", font=R.F(R.MED, 46), fill=YEL, anchor="mm"); img.save(path, quality=92)
def scene_c(path):
    img = face_bg(900); d = ImageDraw.Draw(img)
    y = big(d, ["매일 밤 9시", "세 지도 테스트"], 1080, 100)
    d.text((W//2, y+30), "팔로우하면 다음 편을 놓치지 않아요", font=R.F(R.MED, 48), fill=(255, 255, 255), anchor="mm")
    d.text((W//2, y+120), "내 태어난 날 기운은 프로필 링크에서 1초", font=R.F(R.MED, 40), fill=(190, 182, 170), anchor="mm")
    d.text((W-36, H-30), "정월은 AI로 생성한 가상 캐릭터예요", font=R.F(R.MED, 24), fill=(150, 144, 136), anchor="rs"); img.save(path, quality=92)
def make(mp4, fa, fb, fc, dur=(2.5, 5.5, 2.5), fade=0.35):
    cmd = ["ffmpeg", "-y", "-loglevel", "error"]
    for f, t in zip((fa, fb, fc), dur): cmd += ["-loop", "1", "-t", str(t), "-i", f]
    cmd += ["-f", "lavfi", "-t", str(sum(dur)-2*fade), "-i", "anullsrc=r=44100:cl=stereo"]
    fl = f"[0:v][1:v]xfade=transition=fade:duration={fade}:offset={dur[0]-fade:.2f}[v1];[v1][2:v]xfade=transition=fade:duration={fade}:offset={dur[0]+dur[1]-2*fade:.2f}[v2];[v2]format=yuv420p,fps=30[vout]"
    cmd += ["-filter_complex", fl, "-map", "[vout]", "-map", "3:a", "-c:v", "libx264", "-crf", "21", "-c:a", "aac", "-b:a", "96k", "-shortest", "-movflags", "+faststart", mp4]
    subprocess.run(cmd, check=True)
