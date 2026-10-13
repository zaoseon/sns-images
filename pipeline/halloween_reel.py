"""할로윈(10/31 12:00 인스타 릴스) 영상 다시 만들기 (10/13 대표 "표를 읽을 수 있게": 옛 표는 5행을 한 화면에 넣어 설명 글이 30px이었다).
새 틀: 표지 2.6초 + 표 3장면(2행·2행·1행+질문) 각 4초. 한 행 = 마녀 이름 88px·설명 54px·오행 글자 64px(R06 44px 이상), 안전 영역(x 50~900, y 330~1470) 안.
본문 뒤에 R11 끝 장면(r11_tail.attach, 질문 "올해 핼러윈 / 나는 어떤 마녀?")을 붙여 `2026-halloween/halloween.mp4` 로 낸다.
음악은 지정한 곡(경쾌 신스팝 D 126, 씨앗 1031)을 저장소의 합성기(reel_music)로 만들어 입히고 content/music_log.json 에 'earlybird-halloween' 으로 기록한다.
사용: python3 pipeline/halloween_reel.py"""
import os, sys, json, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "..")); sys.path.insert(0, HERE)
from PIL import Image, ImageDraw, ImageFont
import fonts_kit as F
W, H, FPS = 1080, 1920, 30
BG = (38, 31, 51); CARD = (58, 49, 78); GOLD = (255, 205, 60); WHITE = (255, 255, 255); SOFT = (240, 235, 252)
GM = F.P["gm_bold"]; PR = F.P["pr_xb"]; SR = F.P["serif"]
ROWS = [("甲乙 나무", "숲의 마녀", "조용히 힘을 키우는 타입", (150, 220, 130)), ("丙丁 불", "불꽃 마녀", "등장하는 순간 시선 집중", (255, 140, 110)),
        ("戊己 흙", "고대 마녀", "오래된 지혜를 가진 타입", (245, 185, 80)), ("庚辛 쇠", "냉정한 마녀", "날카로운 눈빛의 심판자", (214, 219, 232)),
        ("壬癸 물", "환영 마녀", "사람 마음을 흔드는 타입", (130, 170, 255))]
SC = [("cover", 2.6), ("t1", 4.0), ("t2", 4.0), ("t3", 4.0)]
MUSIC = dict(name="earlybird-halloween", kind="fun", style="경쾌 신스팝", mode="up", bpm=126, key="D", seed=1031)
def font(p, s): return ImageFont.truetype(p, s)
def ease(t): t = max(0.0, min(1.0, t)); return 1 - (1 - t) ** 3
def paste_fade(base, layer, xy, a):
    if a <= 0: return
    if a < 1: layer = layer.copy(); layer.putalpha(layer.getchannel("A").point(lambda v: int(v * a)))
    base.paste(layer, xy, layer)
def text_layer(txt, f, fill, stroke=0, sfill=None):
    d0 = ImageDraw.Draw(Image.new("RGBA", (1, 1))); bb = d0.textbbox((0, 0), txt, font=f, stroke_width=stroke); w = bb[2] - bb[0] + 8 + stroke * 2; h = bb[3] - bb[1] + 8 + stroke * 2
    L = Image.new("RGBA", (w, h), (0, 0, 0, 0)); ImageDraw.Draw(L).text((4 + stroke - bb[0], 4 + stroke - bb[1]), txt, font=f, fill=fill, stroke_width=stroke, stroke_fill=sfill)
    return L
def center_text(base, txt, f, fill, cy, a=1.0, stroke=0, sfill=None, cx=None):
    L = text_layer(txt, f, fill + (255,), stroke, (sfill + (255,)) if sfill else None); paste_fade(base, L, (int((cx if cx else W // 2) - L.width / 2), int(cy - L.height / 2)), a)
def card(base, row, y, t, t0):
    a = ease((t - t0) / 0.45); h, x0, x1 = 340, 70, 900
    if a <= 0: return
    el, name, desc, col = row; L = Image.new("RGBA", (x1 - x0, h), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.rounded_rectangle([0, 0, x1 - x0 - 1, h - 1], 34, fill=CARD + (255,), outline=col + (255,), width=5)
    d.text((44, 22), el, font=font(SR, 62), fill=col + (255,)); d.text((44, 126), name, font=font(GM, 88), fill=WHITE + (255,)); d.text((44, 250), desc, font=font(PR, 54), fill=SOFT + (255,))
    paste_fade(base, L, (x0, int(y + (1 - a) * 60)), a)
def pill(base, txt, cy):
    L = text_layer(txt, font(GM, 44), (255, 255, 255, 255)); w, h = L.width + 70, 84; P = Image.new("RGBA", (w, h), (0, 0, 0, 0)); ImageDraw.Draw(P).rounded_rectangle([0, 0, w - 1, h - 1], 42, fill=(168, 108, 214, 255))
    P.paste(L, ((w - L.width) // 2, (h - L.height) // 2), L); base.paste(P, ((W - w) // 2, int(cy - h / 2)), P)
CH = None
def draw(kind, t):
    global CH
    im = Image.new("RGB", (W, H), BG)
    if kind == "cover":
        if CH is None:
            c = Image.open(os.path.join(ROOT, "characters", "cut", "v9_halloween.png")).convert("RGBA"); s = 1010 / c.width; c = c.resize((1010, int(c.height * s)), Image.LANCZOS); CH = c.crop((0, 0, 1010, 860)); m = Image.new("L", CH.size, 255); md = ImageDraw.Draw(m)
            for yy in range(740, 860): md.line([(0, yy), (1010, yy)], fill=int(255 * (860 - yy) / 120))
            CH.putalpha(Image.composite(CH.getchannel("A"), Image.new("L", CH.size, 0), m))
        z = 1.0 + 0.04 * (t / 2.6); a = ease(t / 0.5); cc = CH if z == 1.0 else CH.resize((int(CH.width * z), int(CH.height * z)), Image.LANCZOS)
        im.paste(cc, (int(W / 2 - cc.width / 2), 330 + int((1 - a) * 40)), cc)
        pill(im, "정월의 할로윈", 380)
        for i, (txt, cy) in enumerate((("할로윈에 보는", 1030), ("나의 숨은 얼굴", 1150))):
            center_text(im, txt, font(GM, 104), GOLD, cy, a=ease((t - 0.1 * i) / 0.4), stroke=7, sfill=BG)
        center_text(im, "태어난 날 첫 글자로 알아보는 마녀 유형", font(PR, 50), WHITE, 1290, a=ease((t - 0.5) / 0.4), stroke=4, sfill=BG)
        center_text(im, "정월은 AI로 생성한 가상 캐릭터예요", font(PR, 32), (200, 195, 215), 1430)
    elif kind in ("t1", "t2"):
        i = 0 if kind == "t1" else 2
        pill(im, "정월의 할로윈", 380); center_text(im, "태어난 날 첫 글자로", font(PR, 56), WHITE, 520, a=ease(t / 0.3)); center_text(im, "보는 마녀 유형", font(GM, 76), GOLD, 610, a=ease(t / 0.3))
        card(im, ROWS[i], 700, t, 0.25); card(im, ROWS[i + 1], 1070, t, 1.0)
    else:
        pill(im, "정월의 할로윈", 380); card(im, ROWS[4], 500, t, 0.1)
        center_text(im, "내 태어난 날 첫 글자는?", font(GM, 76), GOLD, 940, a=ease((t - 0.8) / 0.4))
        for k, (el, _, _, col) in enumerate(ROWS):
            a = ease((t - 1.3 - 0.12 * k) / 0.3); cw, ch = 150, 120; x = 70 + int(k * (830 - cw) / 4); L = Image.new("RGBA", (cw, ch), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
            d.rounded_rectangle([0, 0, cw - 1, ch - 1], 28, fill=CARD + (255,), outline=col + (255,), width=4); g = el.split()[0]
            f = font(SR, 56); bb = d.textbbox((0, 0), g, font=f); d.text(((cw - (bb[2] - bb[0])) // 2 - bb[0], (ch - (bb[3] - bb[1])) // 2 - bb[1]), g, font=f, fill=col + (255,)); paste_fade(im, L, (x, 1060 + int((1 - a) * 30)), a)
    return im
def render_body(out):
    total = sum(d for _, d in SC); n = int(round(total * FPS))
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-crf", "15", "-preset", "medium", "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", out], stdin=subprocess.PIPE)
    acc = [0.0]
    for _, d in SC: acc.append(acc[-1] + d)
    for fi in range(n):
        t = fi / FPS; k = next((i for i in range(len(SC)) if t < acc[i + 1] - 1e-9), len(SC) - 1)
        p.stdin.write(draw(SC[k][0], t - acc[k]).tobytes())
    p.stdin.close(); p.wait(); return total
def main():
    import music_plan as MP, r11_tail as R
    outdir = os.path.join(ROOT, "2026-halloween"); os.makedirs(outdir, exist_ok=True); mb = os.path.join(outdir, "body.mp4")
    total = render_body(mb); print("본문", total, "초")
    log = json.load(open(MP.LOG, encoding="utf-8")); log = [x for x in log if x["name"] != MUSIC["name"]] + [MUSIC]; json.dump(log, open(MP.LOG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    MP.mux(mb, [d for _, d in SC], MUSIC, MUSIC["seed"])
    R.attach(mb, os.path.join(outdir, "halloween.mp4"), "올해 핼러윈\n나는 어떤 마녀?", cut=total, fx="zoom")
if __name__ == "__main__": main()
