"""인스타 캐러셀 7장(1080x1350). CARD_STYLE_GUIDE.md(10/1)를 따른다.
표지 / 성격 / 연애 / 돈 / 오행차트 / 조언 / CTA. 세트마다 강조색·얼굴·문구만 바뀐다.
사용: python3 pipeline/carousel.py 2026-w40car   (content/carousel_sets.py 의 SETS 전부를 그린다)"""
import os, re, sys
from PIL import Image, ImageDraw, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__))
FD = os.path.join(HERE, "fonts") + "/"
CUT = os.path.join(HERE, "..", "characters", "cut") + "/"
W, H = 1080, 1350
BG = (26, 24, 23)
WHITE, DIMW, GRAY = (255, 255, 255), (205, 200, 195), (150, 146, 142)
BLACK_F, SEMI_F, MED_F, SER_F = FD + "PRETENDARD-BLACK.OTF", FD + "PRETENDARD-SEMIBOLD.OTF", FD + "PRETENDARD-MEDIUM.OTF", FD + "serif.otf"
# 한자: Pretendard에 한자가 없어 고딕 한자 글꼴로 채운다(샘플 이미지에서도 시스템 고딕이 한자를 채움). 없으면 명조
HZ = "/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc"
if not os.path.exists(HZ): HZ = SER_F
_fc = {}
def F(p, s):
    k = (p, s)
    if k not in _fc:
        IF = __import__("PIL.ImageFont", fromlist=["x"])
        _fc[k] = IF.truetype(p, s, index=1) if p.endswith(".ttc") else IF.truetype(p, s)
    return _fc[k]
def hz(c): return "\u4e00" <= c <= "\u9fff"
def hexrgb(h): h = h.lstrip("#"); return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

# ---------- 글자 그리기: 한자는 명조로 한 글자씩, *강조*는 강조색 ----------
def runs(t):
    out, hi = [], False
    for part in re.split(r"(\*)", t):
        if part == "*": hi = not hi
        elif part: out.append((part, hi))
    return out
def width(d, t, path, size):
    return sum(d.textlength(c, font=F(HZ if hz(c) else path, size)) for c in t.replace("*", ""))
def fit(d, t, path, start, lo, maxw):
    s = start
    while s > lo and max(width(d, l, path, s) for l in t.split("\n")) > maxw: s -= 2
    return s
def draw_line(d, x, y, t, path, size, col, acc, align="l"):
    w = width(d, t, path, size)
    cx = x - w/2 if align == "c" else (x - w if align == "r" else x)
    for txt, hi in runs(t):
        for c in txt:
            f = F(HZ if hz(c) else path, size)
            d.text((cx, y), c, font=f, fill=acc if hi else col, anchor="ls"); cx += d.textlength(c, font=f)
def draw_block(d, cx, top, text, path, size, col, acc, gap=1.3, align="c", x=None):
    y = top + size
    for l in text.split("\n"):
        draw_line(d, cx if x is None else x, y, l, path, size, col, acc, align); y += int(size*gap)
    return y - int(size*gap) + int(size*0.3)  # 마지막 줄 아래 y

# ---------- 공통 요소 ----------
def pill(d, x, y, text, bgc, fgc, size=30, align="l", padx=24, pady=12):
    w = int(width(d, text, SEMI_F, size)) + padx*2; h = size + pady*2
    x0 = x if align == "l" else (x - w//2 if align == "c" else x - w)
    d.rounded_rectangle([x0, y, x0+w, y+h], h//2, fill=bgc)
    draw_line(d, x0 + w//2, y + h//2 + int(size*0.36), text, SEMI_F, size, fgc, fgc, "c")
    return x0, y, w, h
def handle(d, acc):
    d.ellipse([56, H-86, 80, H-62], fill=acc)
    draw_line(d, 94, H-64, "zaoseon.com", SEMI_F, 28, WHITE, WHITE)
def page_badge(d, n, m):
    t = f"{n}/{m}"; w = int(width(d, t, SEMI_F, 26)) + 36
    d.rounded_rectangle([W-56-w, 48, W-56, 94], 23, fill=(60, 57, 55))
    draw_line(d, W-56-w//2, 80, t, SEMI_F, 26, DIMW, DIMW, "c")
def ai_notice(d):
    for i, t in enumerate(["※ 자오선의 상담가 정월은", "AI로 생성한 가상 캐릭터입니다"]):
        draw_line(d, W-56, H-84+i*26, t, MED_F, 20, GRAY, GRAY, "r")
def bg_space(accent=None):
    im = Image.open(CUT + "bg_sunmoon.jpg").convert("RGB"); r = max(W/im.width, H/im.height)
    im = im.resize((int(im.width*r)+1, int(im.height*r)+1)); x = (im.width-W)//2; y = (im.height-H)//2
    im = im.crop((x, y, x+W, y+H))
    ov = Image.new("RGB", (W, H), BG); return Image.blend(im, ov, 0.72)
def face_img(name, h):
    im = Image.open(CUT + name + ".png").convert("RGBA"); r = h/im.height
    return im.resize((int(im.width*r), h), Image.LANCZOS)
def new(bg=BG): img = Image.new("RGB", (W, H), bg); return img, ImageDraw.Draw(img)

# ---------- 슬라이드 ----------
def cover(S, n, m):
    img, d = new(); acc = hexrgb(S["accent"])
    f = face_img(S["face"], 900); img.paste(f, (W - f.width + 60, H - 900), f)  # 얼굴 우측 하단, 얼굴 위 글자 없음
    d = ImageDraw.Draw(img)
    pill(d, 56, 56, S["kicker"], acc, (20, 18, 16), 32)
    y = 150
    ss = fit(d, S["coverSub"], SEMI_F, 52, 30, W-120)
    draw_line(d, 56, y+ss, S["coverSub"], SEMI_F, ss, acc, acc); y += int(ss*1.25) + 14
    ts = fit(d, S["coverTitle"], BLACK_F, 100, 60, W-120)
    draw_block(d, 0, y, S["coverTitle"], BLACK_F, ts, WHITE, acc, 1.22, "l", x=56)
    handle(d, acc); ai_notice(d); page_badge(d, n, m); return img
def body(S, key, badge, n, m):
    img = bg_space(); d = ImageDraw.Draw(img); acc = hexrgb(S["accent"])
    title, text = S[key]
    ts = fit(d, title, BLACK_F, 100, 56, W-120)
    bs = fit(d, text, MED_F, 50, 34, W-130)
    tl = title.count("\n")+1; bl = text.count("\n")+1
    total = 54+40 + int(ts*1.3)*tl + 40 + int(bs*1.5)*bl
    top = (H - total)//2 + 20
    pill(d, W//2, top, badge, acc, (20, 18, 16), 32, "c")
    y = top + 54 + 44
    y = draw_block(d, W//2, y, title, BLACK_F, ts, WHITE, acc, 1.3) + 36
    draw_block(d, W//2, y, text, MED_F, bs, DIMW, acc, 1.5)
    handle(d, acc); page_badge(d, n, m); return img
def chart(S, n, m):
    img = bg_space(); d = ImageDraw.Draw(img); acc = hexrgb(S["accent"])
    head = f"{S['dayChar']}({S['hanja']})일생의 오행 균형"
    draw_line(d, W//2, 200, head, BLACK_F, 60, WHITE, WHITE, "c")
    names = ["木", "火", "土", "金", "水"]; kor = ["나무", "불", "흙", "쇠", "물"]
    bw, gap = 140, 44; total = 5*bw + 4*gap; x0 = (W-total)//2; base = 900; maxh = 520
    for i, v in enumerate(S["values"]):
        h = int(maxh*v); x = x0 + i*(bw+gap)
        col = acc if i == S["highlight"] else (92, 89, 86)
        d.rounded_rectangle([x, base-h, x+bw, base], 16, fill=col)
        draw_line(d, x+bw//2, base+58, names[i], HZ, 44, WHITE if i == S["highlight"] else DIMW, WHITE, "c")
        draw_line(d, x+bw//2, base+98, kor[i], MED_F, 26, GRAY, GRAY, "c")
    d.rounded_rectangle([60, 1090, W-60, 1200], 24, fill=(46, 43, 41))
    ns = fit(d, S["chartNote"], SEMI_F, 32, 24, W-170)
    draw_line(d, W//2, 1160 - (0), S["chartNote"], SEMI_F, ns, DIMW, DIMW, "c")
    handle(d, acc); page_badge(d, n, m); return img
def advice(S, n, m):
    img, d = new(); acc = hexrgb(S["accent"])
    f = face_img(S["face"], 1000); fw = f.width
    img.paste(f, ((W-fw)//2, 0), f)          # 위쪽 절반: 얼굴만(배경 없음)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 640, W, H], fill=(34, 31, 30))
    title, text = S["advice"]
    ts = fit(d, title, BLACK_F, 70, 46, W-120); bs = fit(d, text, MED_F, 40, 30, W-140)
    pill(d, W//2, 690, "조언", acc, (20, 18, 16), 28, "c")
    y = 690 + 52 + 30
    y = draw_block(d, W//2, y, title, BLACK_F, ts, WHITE, acc, 1.3) + 26
    draw_block(d, W//2, y, text, MED_F, bs, DIMW, acc, 1.5)
    handle(d, acc); page_badge(d, n, m); return img
def cta(S, n, m):
    img, d = new(); acc = hexrgb(S["accent"])
    f = face_img(S["face"], 820); img.paste(f, ((W-f.width)//2, 0), f)
    d = ImageDraw.Draw(img); d.rectangle([0, 700, W, H], fill=(30, 28, 27))
    qs = fit(d, S["ctaQ"], BLACK_F, 84, 48, W-100)
    y = draw_block(d, W//2, 730, S["ctaQ"], BLACK_F, qs, WHITE, acc, 1.25) + 22
    bt = "+ 태그하고 팔로우까지"; bw = int(width(d, bt, BLACK_F, 46)) + 90
    d.rounded_rectangle([(W-bw)//2, y, (W+bw)//2, y+96], 48, fill=acc)
    draw_line(d, W//2, y+64, bt, BLACK_F, 46, (20, 18, 16), (20, 18, 16), "c"); y += 96 + 34
    pill(d, W//2, y, "내일 밤 9시", (70, 66, 63), WHITE, 30, "c"); y += 78 + 18
    ns = fit(d, S["nextTitle"], BLACK_F, 60, 40, W-120)
    y = draw_block(d, W//2, y, S["nextTitle"], BLACK_F, ns, WHITE, acc, 1.2) + 14
    draw_line(d, W//2, y+26, "프로필 링크에서 내 첫 글자 1초 확인", MED_F, 30, GRAY, GRAY, "c")
    handle(d, acc); page_badge(d, n, m); return img

def build(S, outdir, prefix):
    os.makedirs(outdir, exist_ok=True); m = 7
    slides = [cover(S, 1, m), body(S, "personality", "성격", 2, m), body(S, "love", "연애", 3, m), body(S, "money", "돈", 4, m),
              chart(S, 5, m), advice(S, 6, m), cta(S, 7, m)]
    paths = []
    for i, im in enumerate(slides):
        p = f"{outdir}/{prefix}_{i+1}.jpg"; im.save(p, quality=92); paths.append(p)
    return paths
