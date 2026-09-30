"""새 비주얼 시안 (9/30): 밝은 바탕 + 원소 색 + 정월 캐릭터. 기존 render.py 글꼴 사용."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render as R
from PIL import Image, ImageDraw, ImageFilter
JW = "/home/claude/zaoseon-site/public/img/jeongwol.jpg"
EL = {  # 원소별: 배경, 진한 색, 중간 색
 "불": ((251,231,222), (196,74,52), (238,170,150)), "물": ((222,232,244), (36,62,112), (150,178,214)),
 "흙": ((244,236,220), (150,108,50), (222,200,160)), "나무": ((226,240,226), (54,110,70), (160,200,165)),
 "쇠": ((246,243,236), (140,112,50), (215,200,160))}
INKD = (38,32,28); GRAY = (120,112,104)
def portrait(w, h, radius=40, arch=True):
    im = Image.open(JW).convert("RGB"); r = max(w/im.width, h/im.height)
    im = im.resize((int(im.width*r)+1, int(im.height*r)+1)); x = (im.width-w)//2; im = im.crop((x, 0, x+w, h))
    m = Image.new("L", (w, h), 0); d = ImageDraw.Draw(m)
    if arch: d.rounded_rectangle([0, 0, w, h+radius], radius=w//2, fill=255)
    else: d.rounded_rectangle([0, 0, w, h], radius=radius, fill=255)
    return im, m
def ailabel(d, W, H):
    d.text((W-36, H-30), "정월은 AI로 생성한 가상 캐릭터예요", font=R.F(R.MED, 22), fill=GRAY, anchor="rs")
def logo(d, x, y, col):
    d.text((x, y), "子午線 자오선", font=R.F(R.SER, 30), fill=col)
def cover(path, el, series, hook_lines, sub):
    W, H = 1080, 1350; bg, dk, md = EL[el]
    img = Image.new("RGB", (W, H), bg); d = ImageDraw.Draw(img)
    d.ellipse([W-640, H-760, W+220, H+100], fill=md)
    p, m = portrait(470, 640); img.paste(p, (W-520, H-700), m)
    logo(d, 64, 64, dk)
    d.rounded_rectangle([64, 150, 64+int(d.textlength(series, font=R.F(R.SEMI, 30)))+44, 204], 27, fill=dk)
    d.text((86, 177), series, font=R.F(R.SEMI, 30), fill=bg, anchor="lm")
    y = 260
    for l in hook_lines: d.text((64, y), l, font=R.F(R.SER, 92), fill=INKD); y += 118
    d.text((64, y+20), sub, font=R.F(R.MED, 36), fill=dk)
    d.rounded_rectangle([64, H-190, 480, H-120], 35, outline=dk, width=3)
    d.text((272, H-155), "넘겨서 확인하기 →", font=R.F(R.SEMI, 32), fill=dk, anchor="mm")
    ailabel(d, W, H); img.save(path, quality=92)
def test_card(path, el, title, rows, note):
    W, H = 1080, 1350; bg, dk, md = EL[el]
    img = Image.new("RGB", (W, H), (250, 247, 241)); d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 16], fill=dk); logo(d, 64, 56, dk)
    d.text((64, 140), "세 가지 지도로 보면", font=R.F(R.MED, 32), fill=GRAY)
    ts = 70
    while ts > 44 and d.textlength(title, font=R.F(R.SER, ts)) > W-128: ts -= 2
    d.text((64, 190), title, font=R.HF(title, R.F(R.SER, ts)), fill=INKD)
    y = 330
    for badge, lab, val, desc, c in rows:
        d.rounded_rectangle([64, y, W-64, y+220], 28, fill=(255, 255, 255), outline=(232, 226, 216), width=2)
        d.ellipse([96, y+50, 216, y+170], fill=c); d.text((156, y+110), badge, font=R.F(R.SER, 54), fill=(255, 255, 255), anchor="mm")
        d.text((250, y+48), lab, font=R.F(R.SEMI, 28), fill=GRAY)
        d.text((250, y+92), val, font=R.HF(val, R.F(R.SEMI, 44)), fill=INKD)
        d.text((250, y+154), desc, font=R.HF(desc, R.F(R.MED, 28)), fill=GRAY)
        y += 250
    nl = R.wrap(d, note, R.F(R.SEMI, 32), W-200)[:2]; nh = 60 + 46*len(nl)
    d.rounded_rectangle([64, y+10, W-64, y+10+nh], 28, fill=bg); yy = y+10+nh//2-23*(len(nl)-1)
    for l in nl: d.text((W//2, yy), l, font=R.F(R.SEMI, 32), fill=dk, anchor="mm"); yy += 46
    d.text((64, H-60), "나는 몇 개 겹쳐? 댓글로 · 내일 밤 9시 다음 편", font=R.F(R.MED, 28), fill=GRAY)
    img.save(path, quality=92)
def reel_first(path, el, series, hook_lines, sub):
    W, H = 1080, 1920; bg, dk, md = EL[el]
    img = Image.new("RGB", (W, H), bg); d = ImageDraw.Draw(img)
    p, m = portrait(760, 900); img.paste(p, ((W-760)//2, 140), m)
    d.rounded_rectangle([W//2-190, 1080, W//2+190, 1140], 30, fill=dk)
    d.text((W//2, 1110), series, font=R.F(R.SEMI, 32), fill=bg, anchor="mm")
    y = 1210
    for l in hook_lines: d.text((W//2, y), l, font=R.F(R.SER, 96), fill=INKD, anchor="mm"); y += 124
    d.text((W//2, y+30), sub, font=R.F(R.MED, 40), fill=dk, anchor="mm")
    logo(d, W//2-110, 70, dk); ailabel(d, W, H); img.save(path, quality=92)
