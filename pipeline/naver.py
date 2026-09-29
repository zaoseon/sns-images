"""네이버 블로그 본문 이미지 (가로 960x640, 3:2). 본문에서 화면을 다 덮지 않는 크기.
render.py의 색·글꼴을 그대로 쓴다."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render as R
from PIL import Image, ImageDraw
W, H = 960, 640
def base():
    img = Image.new("RGB", (W, H), R.INK); d = ImageDraw.Draw(img)
    d.rectangle([14, 14, W-15, H-15], outline=R.LINE, width=2)
    d.text((48, 44), "子午線 자오선", font=R.F(R.SER, 24), fill=R.GOLD)
    d.text((W-48, H-44), "동서양 6가지 운명학 · zaoseon.com", font=R.F(R.MED, 20), fill=R.DIM, anchor="rs")
    return img, d
def title(path, kicker, lines, sub, mark):
    img, d = base()
    d.text((W-60, H//2), mark, font=R.F(R.SER, 330), fill=(40, 37, 32), anchor="rm")
    d.text((48, 150), kicker, font=R.F(R.MED, 30), fill=R.GOLD)
    y = 205
    for l in lines: d.text((48, y), l, font=R.HF(l, R.F(R.SER, 76)), fill=R.PAPER); y += 100
    d.line([(48, y+14), (128, y+14)], fill=R.GOLD, width=3)
    d.text((48, y+40), sub, font=R.F(R.MED, 30), fill=R.PAPER)
    img.save(path, quality=88)
def months(path, head, good, save, lucky):
    img, d = base()
    d.text((48, 100), head, font=R.F(R.SER, 44), fill=R.PAPER)
    cw, ch, g = 136, 96, 12; x0, y0 = 48, 180
    for m in range(12):
        x = x0 + (m % 6)*(cw+g); y = y0 + (m//6)*(ch+g); mm = m+1
        if mm in good: d.rounded_rectangle([x, y, x+cw, y+ch], 14, fill=R.GOLD); c = R.INK
        elif mm in save: d.rounded_rectangle([x, y, x+cw, y+ch], 14, outline=R.RED, width=3); c = (205, 110, 100)
        else: d.rounded_rectangle([x, y, x+cw, y+ch], 14, outline=R.LINE, width=2); c = R.DIM
        d.text((x+cw//2, y+ch//2), f"{mm}월", font=R.F(R.SER, 36), fill=c, anchor="mm")
    y = y0 + 2*(ch+g) + 10
    d.rounded_rectangle([48, y+4, 74, y+30], 5, fill=R.GOLD); d.text((86, y+17), "힘을 쓸 달", font=R.F(R.MED, 24), fill=R.PAPER, anchor="lm")
    d.rounded_rectangle([250, y+4, 276, y+30], 5, outline=R.RED, width=3); d.text((288, y+17), "아낄 달", font=R.F(R.MED, 24), fill=R.PAPER, anchor="lm")
    if 13 in save: d.text((W-48, y+17), "+ 이듬해 1월도 아껴요", font=R.F(R.MED, 24), fill=(205,110,100), anchor="rm")
    if 13 in good: d.text((W-48, y+17), "+ 이듬해 1월도 좋아요", font=R.F(R.MED, 24), fill=R.GOLD, anchor="rm")
    d.text((48, y+62), lucky, font=R.F(R.SEMI, 28), fill=R.GOLD)
    d.text((48, y+104), "※ 사주의 달은 절기로 바뀌어요. 달마다 6~8일 무렵에 시작해요.", font=R.F(R.MED, 25), fill=R.DIM)
    img.save(path, quality=88)
def rows(path, head, items, note=""):
    """items: [(라벨, 큰 글, 작은 글, 색 'gold'|'red'|None)]"""
    img, d = base()
    d.text((48, 100), head, font=R.F(R.SER, 44), fill=R.PAPER)
    n = len(items); top = 178; bottom = H - (110 if note else 70); bh = (bottom - top - (n-1)*12)//n
    y = top
    for lab, big, small, col in items:
        c = {"gold": R.GOLD, "red": (205,110,100)}.get(col, R.LINE)
        d.rounded_rectangle([48, y, W-48, y+bh], 14, outline=c, width=2)
        d.text((76, y+bh//2), lab, font=R.HF(lab, R.F(R.SER, 34)), fill=R.GOLD if col != "red" else (205,110,100), anchor="lm")
        bf = R.F(R.SEMI, 36 if bh > 100 else 32)
        if small:
            d.text((250, y+bh//2-4), big, font=R.HF(big, bf), fill=R.PAPER, anchor="ls")
            d.text((250, y+bh//2+8), small, font=R.HF(small, R.F(R.MED, 27)), fill=R.DIM, anchor="lt")
        else:
            d.text((250, y+bh//2), big, font=R.HF(big, bf), fill=R.PAPER, anchor="lm")
        y += bh + 12
    if note: d.text((48, H-92), note, font=R.F(R.MED, 26), fill=R.GOLD)
    img.save(path, quality=88)
def grid(path, head, cells, note=""):
    """cells: 10개 [(한자, 이름, 키워드)] 5x2"""
    img, d = base()
    d.text((48, 100), head, font=R.F(R.SER, 44), fill=R.PAPER)
    cw, ch, g = 164, 170, 12; x0, y0 = 48, 176
    for i, (hz, name, kw) in enumerate(cells):
        x = x0 + (i % 5)*(cw+g); y = y0 + (i//5)*(ch+g)
        d.rounded_rectangle([x, y, x+cw, y+ch], 14, outline=R.LINE, width=2)
        d.text((x+cw//2, y+52), hz, font=R.F(R.SER, 60), fill=R.PAPER, anchor="mm")
        d.text((x+cw//2, y+108), name, font=R.F(R.SEMI, 26), fill=R.GOLD, anchor="mm")
        d.text((x+cw//2, y+143), kw, font=R.F(R.MED, 25), fill=R.DIM, anchor="mm")
    if note: d.text((48, H-88), note, font=R.F(R.MED, 24), fill=R.GOLD)
    img.save(path, quality=88)
