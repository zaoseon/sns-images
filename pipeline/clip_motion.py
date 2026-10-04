"""네이버 클립 SOP판 v2 (10/2, 대표 지적 "영상이 너무 성의 없다"): 움직이는 글자 + 정월 캐릭터 + 내용을 보여 주는 그림.
 - 글자는 줄마다 시간차로 올라오고, 강조 단어는 금색. 장면이 끝나면 위로 사라지며 다음 장면이 들어온다.
 - 배경: 해·달 하늘 그림(어둡게) + 반짝이는 별 + 천천히 도는 지지 고리(子丑寅卯…). 위쪽 진행 막대.
 - 그림: 사주·별자리·숫자 카드, 오행 상생 고리(木→火→土→金→水), 별자리 짝, 숫자 무리, 충전 배터리, 체크 표시, 알림, 취소선, 점수 줄.
 - 1080x1920, 30fps, 소리 없음, 네이버 클립 안전 영역(글자 x70~880, y190~1440).
 - 캐릭터 정월(AI 생성)이 나오는 장면이 있으므로 영상 안에 "AI 생성 캐릭터" 작은 글씨를 넣는다.
사용: python3 pipeline/clip_motion.py n28-c1 12   (clip id, 길이)  → clips_sop/<id>_<길이>s.mp4"""
import os, sys, math, random, subprocess, functools
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, "..")
BLACK = os.path.join(HERE, "fonts", "PRETENDARD-BLACK.OTF"); MED = os.path.join(HERE, "fonts", "PRETENDARD-MEDIUM.OTF")
SERIF = "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc"
W, H, FPS = 1080, 1920, 30; CX = 470
GOLD, WHITE, DIM, INK = (224, 184, 102, 255), (255, 255, 255, 255), (214, 218, 228, 255), (23, 20, 15, 255)
EL = {"木": (96, 160, 104), "火": (214, 98, 82), "土": (206, 168, 84), "金": (200, 204, 214), "水": (92, 142, 214)}
def cl(x, a=0.0, b=1.0): return max(a, min(b, x))
def e_out(x): x = cl(x); return 1 - (1 - x) ** 3
def e_back(x): x = cl(x); c1 = 1.70158; c3 = c1 + 1; return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2
@functools.lru_cache(maxsize=None)
def font(path, size, idx=0): return ImageFont.truetype(path, size, index=idx) if path.endswith(".ttc") else ImageFont.truetype(path, size)
def serif(size): return font(SERIF, size, 2)   # KR
# ---------- 배경 ----------
@functools.lru_cache(maxsize=1)
def bg_static():
    im = Image.new("RGB", (W, H), (14, 17, 27)); d = ImageDraw.Draw(im)
    for y in range(H):
        t = abs(y / H - .42); k = max(0, 1 - t * 1.6); d.line((0, y, W, y), fill=(int(14 + 14 * k), int(17 + 18 * k), int(27 + 30 * k)))
    sm = Image.open(os.path.join(ROOT, "characters", "cut", "bg_sunmoon.jpg")).convert("RGB")
    sm = sm.resize((int(H * sm.width / sm.height), H)); sm = sm.crop(((sm.width - W) // 2, 0, (sm.width - W) // 2 + W, H)).filter(ImageFilter.GaussianBlur(6))
    im = Image.blend(im, sm, .16)
    vg = Image.new("L", (W, H), 0); ImageDraw.Draw(vg).ellipse((-260, -200, W + 260, H + 200), fill=255); vg = vg.filter(ImageFilter.GaussianBlur(160))
    im = Image.composite(im, Image.new("RGB", (W, H), (8, 10, 18)), vg)
    import numpy as np
    a = np.asarray(im).astype("int16"); rng = np.random.default_rng(5); n = rng.normal(0, 1.7, (H, W, 1)); a = np.clip(a + n, 0, 255).astype("uint8")
    return Image.fromarray(a)
@functools.lru_cache(maxsize=1)
def stars():
    r = random.Random(11); return [(r.randint(20, W - 20), r.randint(160, 1460), r.choice([1, 2, 2, 3]), r.random() * 6.28, .6 + r.random() * 1.4) for _ in range(95)]
@functools.lru_cache(maxsize=1)
def ring_img():
    S = 1000; im = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im); c = S // 2
    for r, a, w in ((470, 70, 2), (452, 40, 1), (330, 30, 1)): d.ellipse((c - r, c - r, c + r, c + r), outline=(224, 184, 102, a), width=w)
    f = serif(40)
    for i, ch in enumerate("子丑寅卯辰巳午未申酉戌亥"):
        a = math.radians(i * 30 - 90); x, y = c + 400 * math.cos(a), c + 400 * math.sin(a); g = Image.new("RGBA", (70, 70), (0, 0, 0, 0)); ImageDraw.Draw(g).text((35, 35), ch, font=f, fill=(224, 184, 102, 120), anchor="mm")
        g = g.rotate(-(i * 30), resample=Image.BICUBIC); im.alpha_composite(g, (int(x - 35), int(y - 35)))
        for k in range(1, 3):
            b = math.radians(i * 30 + k * 10 - 90); d.line((c + 452 * math.cos(b), c + 452 * math.sin(b), c + 470 * math.cos(b), c + 470 * math.sin(b)), fill=(224, 184, 102, 60), width=2)
    return im
def background(fr, t, total_t):
    fr.paste(bg_static())
    d = ImageDraw.Draw(fr, "RGBA")
    for x, y, r, ph, sp in stars():
        a = int(90 + 120 * (0.5 + 0.5 * math.sin(t * sp + ph))); d.ellipse((x - r, y - r, x + r, y + r), fill=(255, 236, 190, a))
    rg = ring_img().rotate(-t * 3.2, resample=Image.BICUBIC); fr.paste(rg, (CX - 500, 800 - 500), rg)
    d.rectangle((70, 143, 880, 147), fill=(255, 255, 255, 40)); d.rectangle((70, 143, 70 + int(810 * cl(t / total_t)), 147), fill=GOLD)
# ---------- 글자 ----------
def _dep(wd):
    """앞 말에 붙여 읽어야 하는 짧은 서술어(걸까요? 이에요 …) - 줄 맨 앞에 혼자 떨어지면 어색하다"""
    t = "".join(c[0] for c in wd)
    return len(t) <= 6 and t.endswith(("요", "요?", "요.", "요!", "까?", "죠?", "다", "다.", "가요?", "까요?", "나요?"))
def _split_line(words, w, maxw):
    """한 줄(수동 줄바꿈 하나)이 maxw를 넘으면 의미 단위로 균형 있게 나눈다.
    규칙: 필요한 최소 줄 수로, 가장 긴 줄이 짧아지게(균형) · 3글자 이하 짜투리 줄 금지 · 서술어(걸까요?)가 줄 맨 앞에 혼자 오지 않게."""
    sp = (" ", False)
    def width(g): return w([c for i, wd in enumerate(g) for c in (([sp] if i else []) + wd)])
    if len(words) < 2 or width(words) <= maxw: return [words]
    n = len(words); best = None
    import itertools
    for k in range(2, min(n, 4) + 1):
        for cuts in itertools.combinations(range(1, n), k - 1):
            idx = (0,) + cuts + (n,); groups = [words[idx[i]:idx[i + 1]] for i in range(k)]; ws = [width(g) for g in groups]
            cost = max(ws) + (1000 if max(ws) > maxw else 0)
            for i, g in enumerate(groups):
                chars = sum(len(wd) for wd in g)
                if chars <= 3 and n > 2: cost += 400                  # 짜투리 줄
                if i > 0 and _dep(g[0]): cost += 250                  # 서술어가 줄 맨 앞
            cost += (k - 2) * 120                                      # 줄 수는 적을수록
            if best is None or cost < best[0]: best = (cost, groups)
        if best is not None and k >= 2 and best[0] < 10 ** 6 and max(width(g) for g in best[1]) <= maxw: break
    return best[1] if best else [words]
def wrap(text, fnt, maxw):
    chars, hl = [], False
    for ch in text:
        if ch == "*": hl = not hl; continue
        chars.append((ch, hl))
    segs, words = [], []
    cur = []
    for c in chars:
        if c[0] == " ":
            if cur: words.append(cur); cur = []
        elif c[0] == "\n":
            if cur: words.append(cur); cur = []
            segs.append(words); words = []
        else: cur.append(c)
    if cur: words.append(cur)
    segs.append(words)
    w = lambda cs: fnt.getlength("".join(c[0] for c in cs))
    lines = []
    for sg in segs:
        for g in _split_line(sg, w, maxw):
            lines.append([c for i, wd in enumerate(g) for c in (([(" ", False)] if i else []) + wd)])
    return lines
@functools.lru_cache(maxsize=None)
def line_layers(text, size, color, path, maxw, lh):
    """줄마다 그림자가 있는 RGBA 조각과 줄 높이를 돌려준다"""
    fnt = font(path, size); out = []
    hfnt = font(os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts", "serif.otf"), size)   # 한자는 Pretendard에 없어 명조로(깨져 보이는 문제)
    pick = lambda ch: hfnt if "\u4e00" <= ch <= "\u9fff" else fnt
    for ln in wrap(text, fnt, maxw):
        tw = int(sum(pick(c[0]).getlength(c[0]) for c in ln)) + 60; th = int(size * 1.4) + 40
        sh = Image.new("RGBA", (tw, th), (0, 0, 0, 0)); sd = ImageDraw.Draw(sh); x = 30
        for ch, h in ln: sd.text((x, 22 + 6), ch, font=pick(ch), fill=(0, 0, 0, 150)); x += pick(ch).getlength(ch)
        sh = sh.filter(ImageFilter.GaussianBlur(7)); im = Image.new("RGBA", (tw, th), (0, 0, 0, 0)); d = ImageDraw.Draw(im); x = 30
        for ch, h in ln: d.text((x, 22), ch, font=pick(ch), fill=GOLD if h else color); x += pick(ch).getlength(ch)
        sh.alpha_composite(im); out.append(sh)
    return out, int(size * lh)
class Ctx:
    def __init__(s, fr, t, dur): s.fr, s.t, s.dur = fr, t, dur; s.ex = e_out(cl((dur - t) / 0.24))   # 장면 끝 0.24초: 위로 사라짐
    def alpha(s, a): return a * s.ex
def blit(fr, layer, x, y, a=1.0):
    if a <= 0.01: return
    if a < 0.99:
        tb = [int(i * a) for i in range(256)]; r, g, b, al = layer.split(); layer = Image.merge("RGBA", (r, g, b, al.point(tb)))
    fr.paste(layer, (int(x), int(y)), layer)
def eff_size(s, size, maxw, path):
    """가장 긴 수동 줄이 maxw를 최대 20%만 넘으면 글자를 줄여 그 줄을 한 줄로 둔다(문구가 중간에서 끊기는 것보다 낫다)."""
    fnt = font(path, size); widest = max((fnt.getlength(seg.replace("*", "")) for seg in s.split("\n")), default=0)
    if maxw < widest <= maxw * 1.2: return int(size * maxw / widest)
    return size
def text(c, s, y, t0, size=104, color=WHITE, path=BLACK, maxw=800, lh=1.3, stagger=0.2, cx=CX, anim="rise"):
    size = eff_size(s, size, maxw, path)
    ls, step = line_layers(s, size, color, path, maxw, lh); y0 = y
    for i, L in enumerate(ls):
        p = e_out((c.t - t0 - i * stagger) / 0.42); a = c.alpha(cl(p * 1.4)); dy = (1 - p) * 46 + (1 - c.ex) * -26
        blit(c.fr, L, cx - L.width / 2, y0 + dy - 20, a); y0 += step
    return y0
def text_h(s, size, maxw=800, lh=1.3, path=BLACK): size = eff_size(s, size, maxw, path); return len(wrap(s, font(path, size), maxw)) * int(size * lh)
@functools.lru_cache(maxsize=None)
def chip_layer(label, size):
    fnt = font(BLACK, size); w = int(fnt.getlength(label)) + 60; h = size + 30; im = Image.new("RGBA", (w + 8, h + 8), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((4, 4, 4 + w, 4 + h), radius=h // 2, fill=(224, 184, 102, 28), outline=GOLD, width=3); d.text((4 + w / 2, 4 + h / 2 + 1), label, font=fnt, fill=GOLD, anchor="mm"); return im
def chip(c, label, y, t0, size=44):
    L = chip_layer(label, size); p = e_back((c.t - t0) / 0.4); s = max(.01, p)
    im = L.resize((max(1, int(L.width * s)), max(1, int(L.height * s)))); blit(c.fr, im, CX - im.width / 2, y + (L.height - im.height) / 2, c.alpha(cl(p * 2))); return y + L.height
# ---------- 캐릭터 ----------
@functools.lru_cache(maxsize=None)
def char_layer(name, width=900, crop=0.66):
    im = Image.open(os.path.join(ROOT, "characters", "cut", name + ".png")).convert("RGBA"); im = im.crop((0, 0, im.width, int(im.height * crop)))
    im = im.resize((width, int(im.height * width / im.width)), Image.LANCZOS)
    al = im.getchannel("A"); fade = Image.new("L", im.size, 255); fd = ImageDraw.Draw(fade); fh = 170
    for y in range(fh): fd.line((0, im.height - fh + y, im.width, im.height - fh + y), fill=int(255 * (1 - y / fh)))
    im.putalpha(ImageChops.multiply(al, fade)); return im
@functools.lru_cache(maxsize=1)
def glow(): 
    im = Image.new("RGBA", (800, 800), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for r in range(380, 0, -8): d.ellipse((400 - r, 400 - r, 400 + r, 400 + r), fill=(224, 184, 102, int(46 * (1 - r / 380) ** 1.5)))
    return im
def character(c, name, t0=0.1, width=900, bottom=1440, dx=0):
    L = char_layer(name, width); p = e_out((c.t - t0) / 0.55); br = 5 * math.sin(c.t * 2.2)
    blit(c.fr, glow(), CX - 400 + dx, bottom - L.height + 80, c.alpha(p * .9))
    blit(c.fr, L, CX - L.width / 2 + dx, bottom - L.height + (1 - p) * 190 + br + (1 - c.ex) * 40, c.alpha(cl(p * 1.6)))
    f = font(MED, 22); d = ImageDraw.Draw(c.fr, "RGBA"); d.text((CX + width // 2 - 20 + dx, bottom - 6), "AI 생성 캐릭터", font=f, fill=(255, 255, 255, int(120 * c.ex)), anchor="rd")
# ---------- 그림 ----------
def rr(w, h, fill, outline=None, r=36, ow=3):
    im = Image.new("RGBA", (w + 8, h + 8), (0, 0, 0, 0)); ImageDraw.Draw(im).rounded_rectangle((4, 4, 4 + w, 4 + h), radius=r, fill=fill, outline=outline, width=ow); return im
def pop(c, layer, cx, cy, t0, dur=0.45, a=1.0):
    p = e_back((c.t - t0) / dur); s = max(.02, p)
    if s != 1: layer = layer.resize((max(1, int(layer.width * s)), max(1, int(layer.height * s))))
    blit(c.fr, layer, cx - layer.width / 2, cy - layer.height / 2, c.alpha(cl(p * 2) * a))
@functools.lru_cache(maxsize=None)
def map_card(kind, filled=True):
    w, h = 250, 330; im = rr(w, h, (26, 33, 54, 235) if filled else (26, 33, 54, 70), GOLD if filled else (224, 184, 102, 90), ow=3 if filled else 2); d = ImageDraw.Draw(im)
    if not filled:
        d.text((w / 2 + 4, h / 2 + 4), "?", font=font(BLACK, 120), fill=(224, 184, 102, 110), anchor="mm"); return im
    names = {"saju": "사주", "star": "별자리", "num": "숫자"}; d.text((w / 2 + 4, 52), names[kind], font=font(BLACK, 44), fill=GOLD, anchor="mm")
    if kind == "saju":
        for i, ch in enumerate("木火土金水"):
            a = math.radians(i * 72 - 90); x, y = w / 2 + 4 + 62 * math.cos(a), 190 + 62 * math.sin(a); col = EL[ch] + (255,)
            d.ellipse((x - 28, y - 28, x + 28, y + 28), fill=col); d.text((x, y), ch, font=serif(34), fill=INK if ch in "金土" else WHITE, anchor="mm")
    elif kind == "star":
        for i, (t, col) in enumerate((("불", (214, 98, 82)), ("공기", (170, 196, 230)), ("흙", (206, 168, 84)), ("물", (92, 142, 214)))):
            x = 4 + 66 + (i % 2) * 118; y = 130 + (i // 2) * 100; d.rounded_rectangle((x - 50, y - 34, x + 50, y + 34), radius=34, fill=col + (255,)); d.text((x, y), t, font=font(BLACK, 36), fill=INK if t != "물" else WHITE, anchor="mm")
    else:
        for i, g in enumerate(("1·5·7", "2·4·8", "3·6·9")): d.text((w / 2 + 4, 130 + i * 70), g, font=font(BLACK, 46), fill=WHITE, anchor="mm")
    return im
@functools.lru_cache(maxsize=None)
def map_card_s(kind, filled, sc):
    im = map_card(kind, filled); return im.resize((int(im.width * sc), int(im.height * sc)), Image.LANCZOS)
def three_maps(c, y, t0, filled=3, gap=0.28, caption=None, sc=1.05):
    for i, k in enumerate(("saju", "star", "num")):
        cx = CX + (i - 1) * 280; cy = y + 175
        pop(c, map_card_s(k, i < filled, sc), cx, cy, t0 + i * gap)
    if caption: text(c, caption, y + 380, t0 + 1.0, 64, color=GOLD, path=BLACK, lh=1.3, stagger=0.2)
def wuxing(c, cx, cy, t0, dur=3.0, R=220):
    """木→火→土→金→水→木 상생 고리. 화살표가 차례로 이어진다"""
    S = 640; im = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im); m = S // 2
    p = cl((c.t - t0) / dur) * 5; pos = []
    for i in range(5): a = math.radians(i * 72 - 90); pos.append((m + R * math.cos(a), m + R * math.sin(a)))
    for i in range(5):
        seg = cl(p - i)
        if seg <= 0: continue
        (x0, y0), (x1, y1) = pos[i], pos[(i + 1) % 5]; dx, dy = x1 - x0, y1 - y0; L = math.hypot(dx, dy); ux, uy = dx / L, dy / L
        sx, sy = x0 + ux * 66, y0 + uy * 66; ex, ey = x1 - ux * 70, y1 - uy * 70; px, py = sx + (ex - sx) * seg, sy + (ey - sy) * seg
        d.line((sx, sy, px, py), fill=GOLD, width=8)
        if seg > .98:
            nx, ny = -uy, ux; d.polygon([(ex, ey), (ex - ux * 26 + nx * 16, ey - uy * 26 + ny * 16), (ex - ux * 26 - nx * 16, ey - uy * 26 - ny * 16)], fill=GOLD)
    for i, ch in enumerate("木火土金水"):
        x, y = pos[i]; on = p >= i - .2; col = EL[ch] + (255 if on else 90,)
        d.ellipse((x - 62, y - 62, x + 62, y + 62), fill=col); d.text((x, y), ch, font=serif(70), fill=INK if ch in "金土" else WHITE, anchor="mm")
    blit(c.fr, im, cx - S / 2, cy - S / 2, c.alpha(e_out((c.t - t0 + .1) / .3)))
def pairs(c, y, t0):
    rows = [(("불", (214, 98, 82)), ("공기", (170, 196, 230)), "불은 바람을 만나 커져요"), (("흙", (206, 168, 84)), ("물", (92, 142, 214)), "흙은 물을 머금어요")]
    for i, (a, b, note) in enumerate(rows):
        t = t0 + i * 0.9; im = Image.new("RGBA", (860, 210), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        for (lab, col), x in ((a, 190), (b, 650)): d.rounded_rectangle((x - 130, 20, x + 130, 120), radius=50, fill=col + (255,)); d.text((x, 70), lab, font=font(BLACK, 62), fill=INK if lab != "물" else WHITE, anchor="mm")
        d.text((420, 70), "+", font=font(BLACK, 80), fill=GOLD, anchor="mm"); d.text((420, 170), note, font=font(MED, 40), fill=DIM, anchor="mm")
        p = e_out((c.t - t) / .5); blit(c.fr, im, CX - 430, y + i * 240 + (1 - p) * 40, c.alpha(cl(p * 1.5)))
def groups(c, y, t0):
    for i, g in enumerate(("1 · 5 · 7", "2 · 4 · 8", "3 · 6 · 9")):
        im = rr(640, 130, (26, 33, 54, 235), GOLD); ImageDraw.Draw(im).text((324, 70), g, font=font(BLACK, 82), fill=WHITE, anchor="mm")
        p = e_out((c.t - t0 - i * .35) / .5); blit(c.fr, im, CX - 324 + (1 - p) * -120, y + i * 160, c.alpha(cl(p * 1.5)))
def battery(c, cx, cy, t0, frm=.12, to=1.0, dur=2.0, label=None):
    p = e_out((c.t - t0) / dur); lv = frm + (to - frm) * p; w, h = 640, 290; im = Image.new("RGBA", (w + 70, h + 20), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((6, 10, 6 + w, 10 + h), radius=40, outline=WHITE, width=10); d.rounded_rectangle((w + 14, 10 + h / 2 - 40, w + 46, 10 + h / 2 + 40), radius=12, fill=WHITE)
    col = (214, 98, 82, 255) if lv < .3 else GOLD; bw = int((w - 36) * lv)
    if bw > 10: d.rounded_rectangle((24, 28, 24 + bw, 10 + h - 18), radius=28, fill=col)
    blit(c.fr, im, cx - im.width / 2, cy - im.height / 2, c.alpha(e_out((c.t - t0 + .2) / .3)))
    if label: blit(c.fr, line_layers(label, 64, WHITE, BLACK, 800, 1.2)[0][0], cx - line_layers(label, 64, WHITE, BLACK, 800, 1.2)[0][0].width / 2, cy - h / 2 - 120, c.alpha(e_out((c.t - t0) / .4)))
    pc = f"{int(lv * 100)}%"; L = line_layers(pc, 110, GOLD, BLACK, 400, 1.2)[0][0]; blit(c.fr, L, cx - L.width / 2, cy + h / 2 + 10, c.alpha(1))
def check_row(c, y, label, t0, size=64):
    p = e_out((c.t - t0) / .45); im = Image.new("RGBA", (860, 150), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 8, 840, 138), radius=40, fill=(26, 33, 54, 235), outline=(224, 184, 102, 120), width=2)
    cp = cl((c.t - t0 - .25) / .35); d.ellipse((24, 33, 104, 113), fill=(224, 184, 102, 255 if cp > 0 else 60))
    if cp > 0:
        pts = [(44, 74), (60, 92), (86, 56)]; seg = cp * 2
        d.line([pts[0], (pts[0][0] + (pts[1][0] - pts[0][0]) * cl(seg), pts[0][1] + (pts[1][1] - pts[0][1]) * cl(seg))], fill=INK, width=10)
        if seg > 1: d.line([pts[1], (pts[1][0] + (pts[2][0] - pts[1][0]) * cl(seg - 1), pts[1][1] + (pts[2][1] - pts[1][1]) * cl(seg - 1))], fill=INK, width=10)
    fnt = font(BLACK, size)
    for sz in range(size, 40, -2):
        fnt = font(BLACK, sz)
        if fnt.getlength(label) < 690: break
    d.text((130, 74), label, font=fnt, fill=WHITE, anchor="lm"); blit(c.fr, im, CX - 430 + (1 - p) * -90, y, c.alpha(cl(p * 1.5)))
def strike(c, label, y, t0, size=96, color=WHITE):
    ls, step = line_layers(label, size, color, BLACK, 800, 1.3); L = ls[0]; blit(c.fr, L, CX - L.width / 2, y - 20, c.alpha(1))
    p = e_out((c.t - t0) / .4); wd = L.width - 60; d = ImageDraw.Draw(c.fr, "RGBA")
    d.line((CX - wd / 2 - 10, y + size * .62, CX - wd / 2 - 10 + (wd + 20) * p, y + size * .62), fill=(214, 98, 82, int(255 * c.ex)), width=12)
def notice(c, t0, label="약속 취소할게 ㅠㅠ"):
    p = e_out((c.t - t0) / .55); im = rr(760, 170, (245, 245, 250, 255), None, r=44); d = ImageDraw.Draw(im)
    d.ellipse((30, 40, 118, 128), fill=(224, 184, 102, 255)); d.text((74, 86), "💬"[0] if False else "!", font=font(BLACK, 56), fill=INK, anchor="mm")
    d.text((140, 68), "친구", font=font(BLACK, 38), fill=(30, 30, 40, 255), anchor="lm"); d.text((140, 116), label, font=font(MED, 46), fill=(60, 60, 72, 255), anchor="lm")
    blit(c.fr, im, CX - im.width / 2, 300 + (1 - p) * -240, c.alpha(cl(p * 2)))
def score_rows(c, y, t0, rows, step=172):
    for i, (lab, txt_) in enumerate(rows):
        p = e_out((c.t - t0 - i * .5) / .45); im = rr(840, 150, (26, 33, 54, 235), GOLD if i == 0 else (224, 184, 102, 120)); d = ImageDraw.Draw(im)
        d.ellipse((24, 36, 112, 124), fill=(224, 184, 102, 255)); d.text((68, 82), lab, font=font(BLACK, 54), fill=INK, anchor="mm")
        fnt = font(BLACK, 56)
        for sz in range(56, 36, -2):
            fnt = font(BLACK, sz)
            if fnt.getlength(txt_) < 680: break
        d.text((140, 80), txt_, font=fnt, fill=WHITE, anchor="lm"); blit(c.fr, im, CX - 424 + (1 - p) * 100, y + i * step, c.alpha(cl(p * 1.5)))
def cta(c, lines, t0=0.2, pill="블로그 스티커 눌러 보기", face="v8_gesture"):
    y0 = 300; y = text(c, lines, y0, t0, 92, lh=1.33)
    if face: character(c, face, t0=.5, width=760)
    fnt = font(BLACK, 60); w = int(fnt.getlength(pill)) + 90; pl = Image.new("RGBA", (w + 20, 140), (0, 0, 0, 0)); d = ImageDraw.Draw(pl)
    d.rounded_rectangle((10, 10, 10 + w, 130), radius=60, fill=GOLD); d.text((10 + w / 2, 71), pill, font=fnt, fill=INK, anchor="mm")
    pulse = 1 + .035 * math.sin(c.t * 6); L = pl.resize((int(pl.width * pulse), int(pl.height * pulse))); p = e_back((c.t - t0 - .6) / .45)
    blit(c.fr, L, CX - L.width / 2, y + 60 + (1 - e_out(p)) * 60, c.alpha(cl(p * 2)))
    bob = 12 * math.sin(c.t * 7); ar = Image.new("RGBA", (90, 70), (0, 0, 0, 0)); ImageDraw.Draw(ar).polygon([(10, 8), (80, 8), (45, 62)], fill=GOLD); blit(c.fr, ar, CX - 45, y + 215 + bob, c.alpha(cl(p * 2)))
# ---------- 장면 목록과 렌더 ----------
def render(name, scenes, outdir, kicker=None):
    """scenes: [(길이(초), 함수(c))]. 프레임을 ffmpeg로 바로 흘려 보낸다."""
    total = sum(d for d, _ in scenes); os.makedirs(outdir, exist_ok=True); out = os.path.join(outdir, name + ".mp4")
    pr = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-vf", "scale=in_range=full:out_range=tv:out_color_matrix=bt709,format=yuv420p", "-c:v", "libx264", "-profile:v", "high", "-crf", "14", "-preset", "medium", "-x264-params", "aq-mode=3:aq-strength=0.9", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv", "-an", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    t_acc = 0.0; n = 0; fr = Image.new("RGB", (W, H))
    for dur, fn in scenes:
        for i in range(int(round(dur * FPS))):
            t = i / FPS; background(fr, t_acc + t, total); fn(Ctx(fr, t, dur)); pr.stdin.write(fr.tobytes()); n += 1
        t_acc += dur
    pr.stdin.close(); pr.wait(); return out, n / FPS
def still(scenes, idx, t, path, total=None):
    fr = Image.new("RGB", (W, H)); total = total or sum(d for d, _ in scenes); acc = sum(d for d, _ in scenes[:idx]); background(fr, acc + t, total); scenes[idx][1](Ctx(fr, t, scenes[idx][0])); fr.save(path); return path
# 공통 조각
def hook(kick, lines, face, size=112):
    def f(c):
        chip(c, kick, 250, 0.05)
        hh = text_h(lines, size, maxw=820, lh=1.3); text(c, lines, 400, 0.25, size, maxw=820, lh=1.3, stagger=0.26)
        character(c, face, t0=0.2)
    return f
def point(kick, lines, extra=None, y=None, size=104):
    def f(c):
        yy = 330 if y is None else y; chip(c, kick, yy - 100, 0.05); text(c, lines, yy, 0.2, size, maxw=820, lh=1.32, stagger=0.22)
        if extra: extra(c)
    return f
