"""네이버 카페(·블로그) 프로필·대문 이미지 (10/3 대표: 카페 프로필용 이미지 + "해상도가 떨어지고 퀄리티가 없어 보인다").
원칙: 모든 도형·글자는 최종 크기로 직접 그린다(작은 그림을 늘리지 않음). 정월 얼굴은 원본(1086x1448) 크기 이하로만 쓴다 - 원본보다 크게 쓰면 흐려진다.
사용: python3 pipeline/cafe_assets.py   -> cafe/ 에 프로필(800x800)·대문(2760x780) JPEG(4:4:4, q96)와 PNG"""
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, ".."); sys.path.insert(0, HERE)
from PIL import Image, ImageDraw, ImageFont, ImageFilter
FD = os.path.join(HERE, "fonts") + "/"; CUT = os.path.join(ROOT, "characters", "cut") + "/"
SER, SEMI, MED = FD + "serif.otf", FD + "PRETENDARD-SEMIBOLD.OTF", FD + "PRETENDARD-MEDIUM.OTF"
GOLD = (224, 184, 102); NAVY = (14, 17, 34)
def F(p, s): return ImageFont.truetype(p, s)
def cosmos(w, h, cx, cy, seed=7, stars=None):
    """우주 배경: 남색 바탕 + 얼굴 뒤 은은한 빛 + 별(최종 크기로 그림) + 황도 고리(한자)"""
    r = random.Random(seed); im = Image.new("RGB", (w, h), NAVY); d = ImageDraw.Draw(im)
    for y in range(h): t = y / h; d.line((0, y, w, y), fill=(int(12 + 10 * t), int(15 + 14 * t), int(30 + 26 * t)))
    glow = Image.new("RGB", (w, h), (0, 0, 0)); gd = ImageDraw.Draw(glow); R = int(h * 0.95)
    for k in range(14): rr = int(R * (1 - k / 14)); c = int(10 + 5.5 * k); gd.ellipse((cx - rr, cy - rr, cx + rr, cy + rr), fill=(c // 2, int(c * .75), int(c * 1.5)))
    glow = glow.filter(ImageFilter.GaussianBlur(h // 7)); from PIL import ImageChops; im = ImageChops.add(im, glow)
    lay = Image.new("RGBA", (w, h), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
    n = stars or int(w * h / 2400)
    for _ in range(n):
        x, y = r.randint(0, w), r.randint(0, h); s = r.choice([1, 1, 2, 2, 3]) * max(1, h // 700 + 1) // 1; a = r.randint(70, 230)
        ld.ellipse((x - s / 2, y - s / 2, x + s / 2, y + s / 2), fill=(255, 238, 200, a))
    for _ in range(int(n / 90)):
        x, y = r.randint(0, w), r.randint(0, h); ld.ellipse((x - 4, y - 4, x + 4, y + 4), fill=(255, 244, 214, 255))
    gl = lay.filter(ImageFilter.GaussianBlur(3)); im.paste(gl, (0, 0), gl); im.paste(lay, (0, 0), lay)
    ring = Image.new("RGBA", (w, h), (0, 0, 0, 0)); rd = ImageDraw.Draw(ring)
    for rad, a, wd in ((int(h * .78), 70, 3), (int(h * .70), 40, 2), (int(h * .50), 34, 2)): rd.ellipse((cx - rad, cy - rad, cx + rad, cy + rad), outline=GOLD + (a,), width=wd)
    f = F(SER, int(h * 0.062))
    for i, ch in enumerate("子丑寅卯辰巳午未申酉戌亥"):
        a = math.radians(i * 30 - 90); rad = h * .74; x, y = cx + rad * math.cos(a), cy + rad * math.sin(a)
        g = Image.new("RGBA", (200, 200), (0, 0, 0, 0)); ImageDraw.Draw(g).text((100, 100), ch, font=f, fill=GOLD + (120,), anchor="mm")
        g = g.rotate(-(i * 30), resample=Image.BICUBIC); ring.alpha_composite(g, (int(x - 100), int(y - 100)))
    im.paste(ring, (0, 0), ring); return im
def clean(ch):
    a = ch.split()[3].filter(ImageFilter.MinFilter(5)).filter(ImageFilter.GaussianBlur(1.2)); ch = ch.copy(); ch.putalpha(a); return ch
def figure(name, height, native=True):
    ch = Image.open(CUT + name + ".png").convert("RGBA"); bb = ch.getbbox(); ch = ch.crop(bb)
    if height != ch.height:
        assert height <= ch.height or not native, "원본보다 크게 쓰면 흐려져요"
        ch = ch.resize((int(ch.width * height / ch.height), height), Image.LANCZOS)
    return ch
def save(im, path):
    im.save(path + ".jpg", quality=96, subsampling=0, optimize=True); im.save(path + ".png", optimize=True)
    return os.path.getsize(path + ".jpg") // 1024, os.path.getsize(path + ".png") // 1024
def profile(name="v2_straight", S=800):
    """프로필(정사각): 얼굴은 원본 크기 이하. 원형으로 잘려도 머리·얼굴이 안 잘리게 가운데에."""
    im = cosmos(S, S, S // 2, int(S * .46), seed=3, stars=1100); ch = Image.open(CUT + name + ".png").convert("RGBA"); bb = ch.getbbox(); ch = clean(ch.crop(bb))
    # 머리 폭 기준으로 원본의 66% 크기(= 원본 이하)로 줄여 선명하게
    sc = 0.78; ch = ch.resize((int(ch.width * sc), int(ch.height * sc)), Image.LANCZOS)
    x = (S - ch.width) // 2 + int(S * .01); y = int(S * .10); im.paste(ch, (x, y), ch)
    d = ImageDraw.Draw(im, "RGBA"); m = int(S * .035); d.ellipse((m, m, S - m, S - m), outline=GOLD + (210,), width=max(4, S // 160))
    return im
def cover(name="v2_straight", W=2760, H=780):
    cx, cy = int(W * .76), int(H * .56); im = cosmos(W, H, cx, cy, seed=11)
    d = ImageDraw.Draw(im, "RGBA"); d.rectangle((int(W * .043), 0, int(W * .043) + 5, H), fill=GOLD + (230,))
    # 초승달(오른쪽 아래)
    mc = Image.new("RGBA", (W, H), (0, 0, 0, 0)); md = ImageDraw.Draw(mc); mx, my, mr = int(W * .955), int(H * .86), int(H * .20)
    md.ellipse((mx - mr, my - mr, mx + mr, my + mr), fill=(214, 224, 255, 255)); md.ellipse((mx - mr + int(mr * .42), my - mr - int(mr * .08), mx + mr + int(mr * .42), my + mr - int(mr * .08)), fill=(0, 0, 0, 0))
    cut = Image.new("L", (W, H), 0); cd = ImageDraw.Draw(cut); cd.ellipse((mx - mr, my - mr, mx + mr, my + mr), fill=255); cd.ellipse((mx - mr + int(mr * .42), my - mr - int(mr * .08), mx + mr + int(mr * .42), my + mr - int(mr * .08)), fill=0)
    gl = Image.new("RGBA", (W, H), (150, 170, 255, 0)); gl.putalpha(cut.filter(ImageFilter.GaussianBlur(26)).point(lambda v: int(v * .55))); im.paste(gl, (0, 0), gl)
    moon = Image.new("RGBA", (W, H), (214, 224, 255, 255)); moon.putalpha(cut); im.paste(moon, (0, 0), moon)
    ch = Image.open(CUT + name + ".png").convert("RGBA"); bb = ch.getbbox(); ch = clean(ch.crop(bb))       # 원본 크기 그대로(확대 없음)
    fx = int(W * .565); im.paste(ch, (fx, -int(H * .02)), ch)
    d = ImageDraw.Draw(im, "RGBA"); x0 = int(W * .09)
    d.text((x0, int(H * .07)), "子午線", font=F(SER, int(H * .40)), fill=GOLD)
    d.text((x0 + 6, int(H * .585)), "자오선", font=F(SEMI, int(H * .115)), fill=(255, 255, 255))
    d.text((x0 + 6, int(H * .745)), "동양과 서양의 하늘이 만나는 선에서, 당신을 읽어요", font=F(MED, int(H * .072)), fill=(226, 218, 200))
    d.text((x0 + 6, int(H * .875)), "zaoseon.com", font=F(MED, int(H * .058)), fill=(160, 156, 150))
    t = "AI로 생성한 가상의 캐릭터입니다"; f = F(MED, int(H * .046)); tw = d.textlength(t, font=f)
    d.rounded_rectangle((W - 80 - tw - 36, H - 24 - int(H * .085), W - 80, H - 24), int(H * .043), fill=(14, 17, 34, 150)); d.text((W - 98, H - 24 - int(H * .0425)), t, font=f, fill=(190, 186, 180), anchor="rm")
    return im
if __name__ == "__main__":
    out = os.path.join(ROOT, "cafe"); os.makedirs(out, exist_ok=True)
    print("프로필", save(profile(), os.path.join(out, "cafe_profile_800")), "KB(jpg, png)")
    print("대문", save(cover(), os.path.join(out, "cafe_cover_2760x780")), "KB(jpg, png)")
