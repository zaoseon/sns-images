"""네이버 본문 이미지 컴팩트판(10/3 대표 지적: 본문 이미지가 너무 큼). 640x280 낮은 가로형, 글자는 모바일에서도 읽히게 크게.
naver2.table / naver2.rows 를 이 함수로 바꿔 쓴다(시그니처 동일)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "pipeline"))
import render as R
from PIL import Image, ImageDraw
W, H = 640, 280
def _fit(d, t, path, start, lo, maxw):
    s = start
    while s > lo and d.textlength(t, font=R.HF(t, R.F(path, s))) > maxw: s -= 1
    return s
def rows_c(path, head, items, note=""):
    img = Image.new("RGB", (W, H), R.INK); d = ImageDraw.Draw(img)
    d.rounded_rectangle([5, 5, W - 6, H - 6], 14, outline=R.LINE, width=2)
    d.text((24, 16), head, font=R.F(R.SER, 30), fill=R.PAPER)
    d.text((W - 24, 32), "子午線 자오선", font=R.F(R.SER, 20), fill=R.GOLD, anchor="rm")
    items = [tuple(i) + (None,) * (4 - len(i)) for i in items]; n = len(items)
    top, bottom, gap = 66, H - 16, 8; bh = (bottom - top - (n - 1) * gap) // n; x0 = 170; avail = W - 24 - 16 - x0
    for i, (lab, big, small, col) in enumerate(items):
        y = top + i * (bh + gap); cy = y + bh // 2; c = R.GOLD if col == "gold" else R.LINE
        d.rounded_rectangle([24, y, W - 24, y + bh], 12, outline=c, width=3 if col == "gold" else 2)
        d.text((40, cy), lab, font=R.HF(lab, R.F(R.SER, _fit(d, lab, R.SER, 26, 20, 120))), fill=R.GOLD, anchor="lm")
        sb = _fit(d, big, R.SEMI, 25, 17, avail); d.text((x0, cy - (12 if small else 0)), big, font=R.HF(big, R.F(R.SEMI, sb)), fill=R.PAPER, anchor="lm")
        if small:
            ss = _fit(d, small, R.MED, 19, 16, avail); d.text((x0, cy + 15), small, font=R.HF(small, R.F(R.MED, ss)), fill=R.DIM, anchor="lm")
    img.save(path, quality=90)
def table_c(path, head, cols, rows, widths):
    rows_c(path, head, [tuple(r[:3]) for r in rows])
def cta_c(src, dst):
    im = Image.open(src).convert("RGB"); im.resize((640, 200), Image.LANCZOS).save(dst, quality=92)
