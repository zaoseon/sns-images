"""네이버 블로그 본문 이미지 (가로 960x640, 3:2). 본문에서 화면을 다 덮지 않는 크기.
render.py의 색·글꼴을 그대로 쓴다."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render as R
from PIL import Image, ImageDraw
W, H = 960, 480   # 2:1. 9/30 대표: 3:2도 본문에서 너무 크다
def base():
    img = Image.new("RGB", (W, H), R.INK); d = ImageDraw.Draw(img)
    d.rectangle([12, 12, W-13, H-13], outline=R.LINE, width=2)
    d.text((40, 32), "子午線 자오선", font=R.F(R.SER, 22), fill=R.GOLD)
    d.text((W-40, H-30), "동서양 6가지 운명학 · zaoseon.com", font=R.F(R.MED, 18), fill=R.DIM, anchor="rs")
    return img, d
def title(path, kicker, lines, sub, mark):
    img, d = base()
    d.text((W-50, H//2+10), mark, font=R.F(R.SER, 270), fill=(40, 37, 32), anchor="rm")
    d.text((40, 96), kicker, font=R.F(R.MED, 28), fill=R.GOLD)
    y = 140
    for l in lines: d.text((40, y), l, font=R.HF(l, R.F(R.SER, 66)), fill=R.PAPER); y += 84
    d.line([(40, y+12), (120, y+12)], fill=R.GOLD, width=3)
    d.text((40, y+30), sub, font=R.F(R.MED, 28), fill=R.PAPER)
    img.save(path, quality=88)
def months(path, head, good, save, lucky):
    img, d = base()
    d.text((40, 72), head, font=R.F(R.SER, 38), fill=R.PAPER)
    cw, ch, g = 140, 72, 10; x0, y0 = 40, 136
    for m in range(12):
        x = x0 + (m % 6)*(cw+g); y = y0 + (m//6)*(ch+g); mm = m+1
        if mm in good: d.rounded_rectangle([x, y, x+cw, y+ch], 12, fill=R.GOLD); c = R.INK
        elif mm in save: d.rounded_rectangle([x, y, x+cw, y+ch], 12, outline=R.RED, width=3); c = (205, 110, 100)
        else: d.rounded_rectangle([x, y, x+cw, y+ch], 12, outline=R.LINE, width=2); c = R.DIM
        d.text((x+cw//2, y+ch//2), f"{mm}월", font=R.F(R.SER, 32), fill=c, anchor="mm")
    y = y0 + 2*(ch+g) + 6
    d.rounded_rectangle([40, y+4, 64, y+28], 5, fill=R.GOLD); d.text((74, y+16), "힘을 쓸 달", font=R.F(R.MED, 24), fill=R.PAPER, anchor="lm")
    d.rounded_rectangle([230, y+4, 254, y+28], 5, outline=R.RED, width=3); d.text((264, y+16), "아낄 달", font=R.F(R.MED, 24), fill=R.PAPER, anchor="lm")
    if 13 in save: d.text((W-40, y+16), "+ 이듬해 1월도 아껴요", font=R.F(R.MED, 24), fill=(205,110,100), anchor="rm")
    if 13 in good: d.text((W-40, y+16), "+ 이듬해 1월도 좋아요", font=R.F(R.MED, 24), fill=R.GOLD, anchor="rm")
    d.text((40, y+52), lucky, font=R.F(R.SEMI, 28), fill=R.GOLD)
    img.save(path, quality=88)
def rows(path, head, items, note=""):
    """items: [(라벨, 큰 글, 작은 글, 색 'gold'|'red'|None)]. 4개면 2x2 칸"""
    img, d = base()
    d.text((40, 72), head, font=R.F(R.SER, 38), fill=R.PAPER)
    n = len(items); top = 132; bottom = H - (88 if note else 52)
    if n == 4:
        cw = (W - 80 - 14)//2; ch = (bottom - top - 14)//2
        boxes = [(40 + (i%2)*(cw+14), top + (i//2)*(ch+14), cw, ch) for i in range(4)]
    else:
        bh = (bottom - top - (n-1)*12)//n; boxes = [(40, top + i*(bh+12), W-80, bh) for i in range(n)]
    for (x, y, w, h), (lab, big, small, col) in zip(boxes, items):
        c = {"gold": R.GOLD, "red": (205,110,100)}.get(col, R.LINE)
        d.rounded_rectangle([x, y, x+w, y+h], 12, outline=c, width=2)
        lc = R.GOLD if col != "red" else (205,110,100)
        if n == 4:
            d.text((x+22, y+30), lab, font=R.HF(lab, R.F(R.SER, 28)), fill=lc, anchor="lm")
            d.text((x+22, y+h//2+12), big, font=R.HF(big, R.F(R.SEMI, 28)), fill=R.PAPER, anchor="lm")
            if small: d.text((x+22, y+h-22), small, font=R.HF(small, R.F(R.MED, 22)), fill=R.DIM, anchor="lm")
        else:
            d.text((x+24, y+h//2), lab, font=R.HF(lab, R.F(R.SER, 30)), fill=lc, anchor="lm")
            if small:
                d.text((x+210, y+h//2-2), big, font=R.HF(big, R.F(R.SEMI, 30)), fill=R.PAPER, anchor="ls")
                d.text((x+210, y+h//2+6), small, font=R.HF(small, R.F(R.MED, 24)), fill=R.DIM, anchor="lt")
            else:
                d.text((x+210, y+h//2), big, font=R.HF(big, R.F(R.SEMI, 30)), fill=R.PAPER, anchor="lm")
    if note: d.text((40, H-76), note, font=R.F(R.MED, 24), fill=R.GOLD)
    img.save(path, quality=88)
def grid(path, head, cells, note=""):
    img, d = base()
    d.text((40, 72), head, font=R.F(R.SER, 38), fill=R.PAPER)
    cw, ch, g = 168, 124, 10; x0, y0 = 40, 128
    for i, (hz, name, kw) in enumerate(cells):
        x = x0 + (i % 5)*(cw+g); y = y0 + (i//5)*(ch+g)
        d.rounded_rectangle([x, y, x+cw, y+ch], 12, outline=R.LINE, width=2)
        d.text((x+cw//2, y+36), hz, font=R.F(R.SER, 44), fill=R.PAPER, anchor="mm")
        d.text((x+cw//2, y+76), name, font=R.F(R.SEMI, 24), fill=R.GOLD, anchor="mm")
        d.text((x+cw//2, y+104), kw, font=R.F(R.MED, 21), fill=R.DIM, anchor="mm")
    if note: d.text((40, H-70), note, font=R.F(R.MED, 23), fill=R.GOLD)
    img.save(path, quality=88)
def table(path, head, cols, rows, widths):
    img, d = base()
    d.text((40, 72), head, font=R.F(R.SER, 36), fill=R.PAPER)
    x0, y = 40, 122; rh = (H - 48 - y) // (len(rows) + 1)
    x = x0
    for c, w in zip(cols, widths):
        d.text((x + 10, y + rh//2), c, font=R.F(R.SEMI, 24), fill=R.GOLD, anchor="lm"); x += w
    d.line([(x0, y + rh), (W - 40, y + rh)], fill=R.GOLD, width=2)
    for r in rows:
        y += rh; x = x0
        for i, (c, w) in enumerate(zip(r, widths)):
            f = R.F(R.SER if i == 0 else R.MED, 27 if i == 0 else 25)
            d.text((x + 10, y + rh//2), c, font=R.HF(c, f), fill=R.PAPER, anchor="lm"); x += w
        d.line([(x0, y + rh), (W - 40, y + rh)], fill=R.LINE, width=1)
    img.save(path, quality=88)
