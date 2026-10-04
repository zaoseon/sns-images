"""네이버 본문 이미지 컴팩트판. 10/4 선명도·글자 크기 개선: 2배(1280x560) 해상도로 직접 그리고 4:4:4로 저장한다.
이전: 640x280, 작은 글씨 16~19px(폰에서 약 10px) -> 지금: 같은 비율, 작은 글씨 21(640 기준)로 키움, 해상도 2배.
naver2.table / naver2.rows 를 이 함수로 바꿔 쓴다(시그니처 동일)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "pipeline"))
import render as R
from PIL import Image, ImageDraw
SC = 2                      # 해상도 배율
W, H = 640 * SC, 300 * SC   # 높이 280->300: 큰 글자와 작은 글자 줄 간격 확보
def _fit(d, t, path, start, lo, maxw):
    s = start
    while s > lo and d.textlength(t, font=R.HF(t, R.F(path, s))) > maxw: s -= 1
    return s
def rows_c(path, head, items, note=""):
    img = Image.new("RGB", (W, H), R.INK); d = ImageDraw.Draw(img); k = SC
    d.rounded_rectangle([5 * k, 5 * k, W - 6 * k, H - 6 * k], 14 * k, outline=R.LINE, width=2 * k)
    d.text((24 * k, 14 * k), head, font=R.F(R.SER, 31 * k), fill=R.PAPER)
    d.text((W - 24 * k, 31 * k), "子午線 자오선", font=R.F(R.SER, 20 * k), fill=R.GOLD, anchor="rm")
    items = [tuple(i) + (None,) * (4 - len(i)) for i in items]; n = len(items)
    top, bottom, gap = 66 * k, H - 16 * k, 8 * k; bh = (bottom - top - (n - 1) * gap) // n; x0 = 164 * k; avail = W - 24 * k - 16 * k - x0
    for i, (lab, big, small, col) in enumerate(items):
        y = top + i * (bh + gap); cy = y + bh // 2; c = R.GOLD if col == "gold" else R.LINE
        d.rounded_rectangle([24 * k, y, W - 24 * k, y + bh], 12 * k, outline=c, width=(3 if col == "gold" else 2) * k)
        d.text((40 * k, cy), lab, font=R.HF(lab, R.F(R.SER, _fit(d, lab, R.SER, 27 * k, 20 * k, 114 * k))), fill=R.GOLD, anchor="lm")
        sb = _fit(d, big, R.SEMI, 27 * k, 19 * k, avail); d.text((x0, cy - (13 * k if small else 0)), big, font=R.HF(big, R.F(R.SEMI, sb)), fill=R.PAPER, anchor="lm")
        if small:
            ss = _fit(d, small, R.MED, 20 * k, 17 * k, avail); d.text((x0, cy + 16 * k), small, font=R.HF(small, R.F(R.MED, ss)), fill=R.DIM, anchor="lm")
    img.save(path, quality=96, subsampling=0, optimize=True)
def table_c(path, head, cols, rows, widths):
    rows_c(path, head, [tuple(r[:3]) for r in rows])
def cta_c(src, dst):
    """CTA 배너를 1280x400으로 직접 그린다(전: 960x300 원본을 640x200으로 줄임). 문구·배치는 원본과 같다."""
    k = 1280 / 960; Wc, Hc = 1280, 400
    img = Image.new("RGB", (Wc, Hc), R.INK); d = ImageDraw.Draw(img)
    d.rounded_rectangle([int(14 * k), int(14 * k), Wc - int(15 * k), Hc - int(15 * k)], int(18 * k), outline=R.GOLD, width=int(2 * k))
    d.text((Wc // 2, int(80 * k)), "생년월일만 넣으면 1초면 돼요", font=R.HF("생년월일만", R.F(R.SER, int(40 * k))), fill=R.GOLD, anchor="mm")
    d.text((Wc // 2, int(140 * k)), "내 태어난 날의 기운과 2027년 한 줄 풀이, 무료", font=R.HF("내 태어난", R.F(R.MED, int(24 * k))), fill=R.PAPER, anchor="mm")
    bw, bh = int(404 * k), int(74 * k); x0 = (Wc - bw) // 2; y0 = int(181 * k)
    d.rounded_rectangle([x0, y0, x0 + bw, y0 + bh], bh // 2, fill=R.GOLD)
    d.text((Wc // 2, y0 + bh // 2), "1초 만에 내 기운 보기", font=R.HF("1초 만에", R.F(R.SEMI, int(30 * k))), fill=R.INK, anchor="mm")
    img.save(dst, quality=96, subsampling=0, optimize=True)

def cta_small(dst, ratio=2 / 3):
    """CTA 배너를 지금의 2/3 크기로 보이게 한다(10/4 대표 지적: 맨 아래 배너가 너무 크다).
    네이버는 글 폭에 맞춰 그림을 보여 주므로, 그림 파일 폭을 줄이면 크기가 글마다 달라진다. 그래서 1280 폭 흰 바탕 가운데에 배너를 ratio(2/3) 폭·높이로 놓는다.
    -> 글 폭이 얼마든 배너는 가로·세로 모두 지금의 2/3, 가운데 정렬. 배너는 큰 그림(1280x400)을 줄여 놓아 선명하다. 흰 바탕은 글 바탕과 같은 색이다."""
    import tempfile, os
    tmp = os.path.join(tempfile.gettempdir(), "_cta_full.jpg"); cta_c(None, tmp)
    full = Image.open(tmp).convert("RGB"); bw, bh = int(round(1280 * ratio)), int(round(400 * ratio))
    small = full.resize((bw, bh), Image.LANCZOS); can = Image.new("RGB", (1280, bh), (255, 255, 255)); can.paste(small, ((1280 - bw) // 2, 0))
    can.save(dst, quality=96, subsampling=0, optimize=True); return can.size

