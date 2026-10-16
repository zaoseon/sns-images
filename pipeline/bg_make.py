"""배경 라이브러리를 만든다 — 대표 10/16 "배경이나 에셋 라이브러리처럼 만들어놓고 이거저거 골라서 쓰도록".

그동안 배경이 우주 고리 한 장뿐이었고 색만 다섯 가지로 입히고 있었다. 색만 바꾸면
K-071 이 말하는 '큰 층'이 안 바뀌어서 아무리 돌려도 양산형으로 읽힌다. 그래서 **짜임이
서로 다른** 배경을 만들어 둔다. 색은 입히지 않는다 — 색은 판(color_combos)이 입힌다.

여덟 가지 모두 어두운 바탕이다(흰 글자를 얹는다). 그리는 규칙:
  - K-041: 배경 전체에 흐린 빛 방울(보케)을 깔지 않는다
  - 글이 앉는 가운데 세로 띠(y 490~1380)는 어둡고 조용하게 둔다
  - 모양은 가장자리·위아래로 몰아 글을 방해하지 않게 한다

사용: python3 pipeline/bg_make.py          -> assets/brand_bg/scenes/*.jpg 8장
      python3 pipeline/bg_make.py --one 별밭
"""
import os, sys, math, random
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
import channel_specs as CS

CH = CS.CH["reel"]
W, H = CH["w"], CH["h"]
GLASS = (CH["zones"][2][2], CH["zones"][-2][4])      # 글이 앉는 세로 구간 — 조용히 둔다


def 바탕(d, 위, 아래):
    """위에서 아래로 두 색 사이를 메운다. 보케가 아니라 고른 면이라 K-041 에 걸리지 않는다."""
    for y in range(H):
        k = y / H
        d.line((0, y, W, y), fill=tuple(int(위[i] + (아래[i] - 위[i]) * k) for i in range(3)))


def 별(d, rnd, n=240, 위로=True):
    for _ in range(n):
        x, y = rnd.randrange(W), rnd.randrange(H)
        r = rnd.choice([1, 1, 1, 2, 2, 3])
        a = rnd.randint(70, 215)
        if GLASS[0] < y < GLASS[1]:
            a = int(a * 0.45)                        # 글 자리에서는 조용히
        d.ellipse((x - r, y - r, x + r, y + r), fill=(255, 244, 226, a))


def 안개(im, 중심, 반지름, 색, 세기=70):
    """한 군데만 은은하게. 전체에 까는 것이 아니라 가장자리 한 점이라 K-041 금지에 해당하지 않는다."""
    L = Image.new("L", (W, H), 0)
    ImageDraw.Draw(L).ellipse((중심[0] - 반지름, 중심[1] - 반지름, 중심[0] + 반지름, 중심[1] + 반지름), fill=세기)
    L = L.filter(ImageFilter.GaussianBlur(반지름 // 2))
    return Image.composite(Image.new("RGB", (W, H), 색), im, L)


def 별밭(rnd):
    im = Image.new("RGB", (W, H)); d = ImageDraw.Draw(im, "RGBA")
    바탕(d, (10, 12, 22), (6, 7, 14)); 별(d, rnd, 420)
    return 안개(im, (900, 260), 520, (40, 46, 86), 60)


def 지평선달(rnd):
    im = Image.new("RGB", (W, H)); d = ImageDraw.Draw(im, "RGBA")
    바탕(d, (8, 10, 20), (26, 22, 30)); 별(d, rnd, 200)
    d.ellipse((760, 1500, 1120, 1860), fill=(246, 240, 226, 36))
    for i in range(7):                                # 아래쪽 능선
        y = 1620 + i * 46
        d.polygon([(0, H), (0, y + 40), (W * .3, y - 20), (W * .62, y + 30), (W, y - 10), (W, H)],
                  fill=(10 + i * 3, 11 + i * 3, 20 + i * 4, 255))
    return im


def 성운띠(rnd):
    im = Image.new("RGB", (W, H)); d = ImageDraw.Draw(im, "RGBA")
    바탕(d, (9, 9, 18), (7, 10, 16)); 별(d, rnd, 300)
    band = Image.new("L", (W, H), 0); bd = ImageDraw.Draw(band)
    bd.polygon([(-200, 300), (W + 200, -150), (W + 200, 260), (-200, 700)], fill=64)
    band = band.filter(ImageFilter.GaussianBlur(90))
    return Image.composite(Image.new("RGB", (W, H), (58, 44, 92)), im, band)


def 동심원(rnd):
    im = Image.new("RGB", (W, H)); d = ImageDraw.Draw(im, "RGBA")
    바탕(d, (11, 13, 20), (6, 8, 13)); 별(d, rnd, 160)
    cx, cy = 150, 1680                                 # 한쪽 구석에 몰아 글을 안 건드린다
    for r in range(120, 1500, 86):
        d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=(190, 200, 230, 26), width=3)
    return im


def 종이결(rnd):
    im = Image.new("RGB", (W, H)); d = ImageDraw.Draw(im, "RGBA")
    바탕(d, (28, 24, 20), (16, 14, 12))
    for _ in range(9000):                              # 종이 결 — 보케가 아니라 미세한 알갱이
        x, y = rnd.randrange(W), rnd.randrange(H)
        d.point((x, y), fill=(255, 240, 215, rnd.randint(6, 26)))
    return 안개(im, (160, 220), 460, (74, 58, 38), 54)


def 별자리선(rnd):
    im = Image.new("RGB", (W, H)); d = ImageDraw.Draw(im, "RGBA")
    바탕(d, (8, 12, 18), (6, 9, 15)); 별(d, rnd, 180)
    pts = [(rnd.randrange(60, W - 60), rnd.choice([rnd.randrange(120, 440), rnd.randrange(1420, 1820)]))
           for _ in range(11)]
    for a, b in zip(pts, pts[1:]):
        d.line((a[0], a[1], b[0], b[1]), fill=(200, 212, 240, 42), width=2)
    for x, y in pts:
        d.ellipse((x - 5, y - 5, x + 5, y + 5), fill=(236, 240, 252, 150))
    return im


def 빛기둥(rnd):
    im = Image.new("RGB", (W, H)); d = ImageDraw.Draw(im, "RGBA")
    바탕(d, (10, 10, 16), (14, 12, 18)); 별(d, rnd, 140)
    L = Image.new("L", (W, H), 0); ld = ImageDraw.Draw(L)
    for x in (80, 300, 820, 1000):                     # 세로 빛 — 가장자리에만
        ld.polygon([(x, 0), (x + 120, 0), (x + 220, H), (x + 40, H)], fill=40)
    L = L.filter(ImageFilter.GaussianBlur(70))
    return Image.composite(Image.new("RGB", (W, H), (70, 72, 108)), im, L)


def 산능선(rnd):
    im = Image.new("RGB", (W, H)); d = ImageDraw.Draw(im, "RGBA")
    바탕(d, (12, 14, 24), (20, 18, 26)); 별(d, rnd, 220)
    for i in range(5):
        y = 1450 + i * 100; c = 12 + i * 6
         # 능선 하나마다 높낮이를 다르게
        pts = [(0, H), (0, y)]
        for k in range(1, 8):
            pts.append((W * k / 7, y + rnd.randint(-70, 70)))
        pts += [(W, y), (W, H)]
        d.polygon(pts, fill=(c, c + 2, c + 8, 255))
    return im


틀 = {"별밭": 별밭, "지평선달": 지평선달, "성운띠": 성운띠, "동심원": 동심원,
      "종이결": 종이결, "별자리선": 별자리선, "빛기둥": 빛기둥, "산능선": 산능선}
OUT = os.path.join(ROOT, "assets", "brand_bg", "scenes")


def main():
    os.makedirs(OUT, exist_ok=True)
    하나 = next((a for a in sys.argv[1:] if not a.startswith("--")), None) \
        if "--one" in sys.argv else None
    for i, (이름, fn) in enumerate(틀.items()):
        if 하나 and 이름 != 하나:
            continue
        im = fn(random.Random(4000 + i))
        p = os.path.join(OUT, 이름 + ".jpg")
        im.save(p, quality=92)
        print(" ", 이름, "->", os.path.relpath(p, ROOT))


if __name__ == "__main__":
    main()
