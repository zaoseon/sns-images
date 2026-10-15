"""네이버 본문 '심리 개념 도식' (10/15, AI 브리핑 기준 문서 이미지 방침 C · OSMU O6).
같은 틀(한눈에 보기·핵심 표·해 볼 것)이 54편에서 반복되는 문제를 줄이려고, '🧠 심리학으로 읽으면' 단락마다 그 개념 모양의 도식을 1장 넣는다.
반추=고리, 사회 비교=저울, 결정=선택지 칸, 소비=영수증, 애착=대화 화면(O6 표). 글 안에 있는 말만 쓴다(그림에만 있는 정보 금지).
이미지 안에 설명·안내 문구(예시·출처·실제 화면 등)는 넣지 않고 원고 본문 문장으로 쓴다(대표 10/15, 기준 대장 K-036). 넣을 때 쓸 본문 문장은 BODY_LINE.
imgkit 규칙(1280 납품·2배 원본·글자 42px 이상·로고 오른쪽 위)을 그대로 쓴다. 파일은 새 이름 naver_zNN_p.jpg 로만 추가(덮어쓰기 금지).
사용: python3 naver/concept_img.py n34   -> img/naver_z34_p.jpg (+ master/·m1280/)"""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "pipeline"))
import imgkit as K, naver2 as N2
from imgkit import Cv, L, RT, TITLE, BODY, DIM, WHITE
# 10/15 대표 "색감이 칙칙하다, 깔끔하고 세련되게": 오행 탁한 바탕·차트 무늬 대신 흰 바탕 + 남색 하나 + 금색 포인트, 연회색 칸
CLEAN = dict(bg=(250, 250, 248), ink=(22, 24, 32), sub=(110, 114, 124), acc=(27, 42, 82), gold=(196, 154, 64), cell=(241, 243, 248), line=(226, 229, 236), red=(214, 72, 56))
def clean_theme(): return CLEAN["bg"], CLEAN["acc"], CLEAN["ink"], CLEAN["line"]

def arrow(cv, x0, y0, x1, y1, col, w=6, head=22):
    cv.line(x0, y0, x1, y1, col, w); a = math.atan2(y1 - y0, x1 - x0)
    p = [(x1, y1), (x1 - head * math.cos(a - .45), y1 - head * math.sin(a - .45)), (x1 - head * math.cos(a + .45), y1 - head * math.sin(a + .45))]
    cv.d.polygon([(x * K.S, y * K.S) for x, y in p], fill=col)

def box_text(cv, cx, cy, lines, size, fg, path=BODY):
    step = size * 1.3; y = cy - step * (len(lines) - 1) / 2
    for l in lines: cv.text(cx, y, l, path, size, fg, "mm"); y += step

def loop(name, head, nodes, exit_label, exit_text, note, el="물"):
    """되풀이 고리: nodes 4개가 시계 방향으로 돌고, 아래 '끊는 법' 띠로 빠져나가는 빨간 화살표."""
    bg, acc, fg, line = clean_theme()
    H = 960 if not note else 1025; cv = Cv(H, bg); K.head_block(cv, head, acc, fg)
    cx, cy, r = (L + RT) / 2, 465, 225; bw, bh = 300, 118
    pos = [(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)]
    for i in range(4):
        a0 = -90 + i * 90 + 26; a1 = -90 + (i + 1) * 90 - 26; pts = []
        for k in range(13):
            t = math.radians(a0 + (a1 - a0) * k / 12); pts.append((cx + r * math.cos(t), cy + r * math.sin(t)))
        for p_, q in zip(pts, pts[1:]): cv.line(p_[0], p_[1], q[0], q[1], CLEAN["gold"], 5)
        arrow(cv, pts[-2][0], pts[-2][1], pts[-1][0], pts[-1][1], CLEAN["gold"])
    cv.text(cx, cy, "되풀이", TITLE, 46, CLEAN["gold"], "mm")
    for (x, y), t in zip(pos, nodes):
        cv.rr([x - bw / 2, y - bh / 2, x + bw / 2, y + bh / 2], 26, fill=CLEAN["cell"])
        box_text(cv, x, y, t, 42, fg)
    by0, by1 = 795, 915                                     # 끊는 법 띠
    cv.rr([L, by0, RT, by1], 32, fill=acc)
    lw = cv.tw(exit_label, TITLE, 50); cv.text(L + 40, (by0 + by1) / 2, exit_label, TITLE, 50, CLEAN["gold"], "lm")
    cv.text(L + 40 + lw + 36, (by0 + by1) / 2, exit_text, BODY, cv.fit(exit_text, BODY, 46, RT - L - lw - 110, 42), WHITE, "lm")
    arrow(cv, cx + r + bw / 2 - 30, cy + bh / 2 + 6, cx + r + bw / 2 - 30, by0 - 10, acc, 6, 26)
    if note: cv.text(L, H - 52, note, BODY, cv.fit(note, BODY, 42, RT - L, 36), DIM, "lm")
    cv.save(name)


def screen(name, head, shot, crop_h, notes, caption, el="흙"):
    """실제 화면 캡처 1장(AI 브리핑 기준 B·N5 '실제 화면'): 폰 화면 + 오른쪽에 화면 속 내용을 짚는 말. 가상 생년월일은 '예시'로 적는다."""
    from PIL import Image
    bg, acc, fg, line = clean_theme()
    im = Image.open(shot).convert("RGB"); im = im.crop((0, 0, im.width, min(crop_h, im.height)))
    pw = 430; ph = int(im.height * pw / im.width); H = ph + 230
    cv = Cv(H, bg); K.head_block(cv, head, acc, fg)
    x0, y0 = L + 10, 170
    cv.rr([x0 - 14, y0 - 14, x0 + pw + 14, y0 + ph + 14], 40, fill=(20, 20, 26))
    sm = im.resize((pw * K.S, ph * K.S)); cv.img.paste(sm, (x0 * K.S, y0 * K.S))
    tx = x0 + pw + 70; y = y0 + 20
    for lab, txt in notes:
        cv.text(tx, y, lab, BODY, 42, CLEAN["sub"], "la"); y += 58
        for l in cv.wrap(txt, BODY, 50, RT - tx): cv.text(tx, y, l, BODY, 50, fg, "la"); y += 66
        cv.line(tx, y + 18, RT, y + 18, CLEAN["line"], 2); y += 58
    if caption: cv.text(L, H - 52, caption, BODY, cv.fit(caption, BODY, 40, RT - L, 34), DIM, "lm")
    cv.save(name)

# 10/15 대표 "애플처럼 세련되게"(slide_design_master_guide: Apple Keynote 프리셋) — 단일 초점, 큰 글자, 테두리 없는 카드, 회색으로 계층, 강조색 하나(브랜드 금색)
FD = os.path.join(HERE, "..", "pipeline", "fonts") + "/"
PB, PS, PM = FD + "PRETENDARD-BOLD.OTF", FD + "PRETENDARD-SEMIBOLD.OTF", FD + "PRETENDARD-MEDIUM.OTF"
PX = FD + "PRETENDARD-EXTRABOLD.OTF"
# v3(10/15 대표 "검은 바탕 도식은 칸·원을 다른 색으로, 디자인 자료 참고"): 저장된 대표 기준 반영 — 검정+금색 금지(다른 운세 블로그 같음),
# 밝은 애플 판(#F5F5F7·흰 카드) + 디자인 기준(10/5) 강조색 4종(코랄·노랑·민트·하늘)을 칸마다 다르게, 진한 남색(#29335C, 대표 색 조합2) 띠, 회색 글자도 굵고 진하게
POP = [(255, 138, 115), (246, 176, 66), (127, 214, 200), (111, 183, 255)]          # 코랄·노랑·민트·하늘
def tint(c, k=.16): return tuple(int(255 - (255 - v) * k) for v in c)
def deep(c, k=.55): return tuple(int(v * k) for v in c)
NAVY = (41, 51, 92)
# v4(10/15 대표 "검정도 괜찮다, 칙칙해서 그런 것. 검정에 노랑·민트·핫핑크 강조가 예쁘다"): 어두운 판은 순검정 대신 #121214(다크 모드 권장),
# 칸은 한 단 밝은 면 + 칸마다 다른 쨍한 강조색(노랑·민트·핫핑크·하늘), 글자는 흰색, 강조색은 화면 일부에만(띠·화살표·이름표)
NEON = [(255, 216, 77), (62, 230, 193), (255, 61, 139), (77, 184, 255)]          # 노랑·민트·핫핑크·하늘
def mix(a, b, k): return tuple(int(a[i] * (1 - k) + b[i] * k) for i in range(3))
KEY = {"dark": dict(bg=(18, 18, 20), card=(30, 30, 34), ink=(250, 250, 250), sub=(161, 161, 170), acc=(255, 216, 77), quiet=(58, 58, 62)),
       "light": dict(bg=(245, 245, 247), card=(255, 255, 255), ink=(29, 29, 31), sub=(81, 81, 86), acc=NAVY, quiet=(200, 200, 206))}
def k_head(cv, head, st):
    cv.text(L + 10, 118, head, PX, cv.fit(head, PX, 64, RT - L - 210, 50), st["ink"], "ls")
    cv.text(RT - 10, 114, "子午線 자오선", K.SER, 28, st["sub"], "rs")

ICONS = []
def loop_k(name, head, nodes, exit_label, exit_text, mode="dark", icons=()):
    global ICONS; ICONS = list(icons)
    st = KEY[mode]; H = 1060; cv = Cv(H, st["bg"])
    if mode == "dark": glow(cv, H, [(NEON[3], (L + 120, 260), 260, .55), (NEON[2], (RT - 80, 620), 280, .45), (NEON[1], ((L + RT) / 2, 980), 240, .30)])
    k_head(cv, head, st)
    cx, cy, r = (L + RT) / 2, 500, 252; bw, bh = 370, 132
    pos = [(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)]
    for i in range(4):
        a0 = -90 + i * 90 + 27; a1 = -90 + (i + 1) * 90 - 27; pts = []
        for k in range(13):
            t = math.radians(a0 + (a1 - a0) * k / 12); pts.append((cx + r * math.cos(t), cy + r * math.sin(t)))
        ac = (POP if mode == "light" else NEON)[(i + 1) % 4]
        for p_, q in zip(pts, pts[1:]): cv.line(p_[0], p_[1], q[0], q[1], ac, 6)
        arrow(cv, pts[-2][0], pts[-2][1], pts[-1][0], pts[-1][1], ac, 6, 24)
    if mode == "dark": put_icon(cv, "repeat", st["sub"], cx, cy - 26, 46); cv.text(cx, cy + 30, "되풀이", PX, 36, st["sub"], "mm")
    else: cv.text(cx, cy, "되풀이", PX, 42, st["sub"], "mm")
    for i, ((x, y), t) in enumerate(zip(pos, nodes)):
        c = POP[i]
        if mode == "light":
            cv.rr([x - bw / 2, y - bh / 2, x + bw / 2, y + bh / 2], 30, fill=tint(c, .22))
            cv.rr([x - bw / 2, y - bh / 2, x - bw / 2 + 12, y + bh / 2], 6, fill=c)
            box_text(cv, x + 6, y, t, 42, deep(c, .38) if i != 1 else (110, 70, 10), PX)
        else:
            c = NEON[i]
            cv.rr([x - bw / 2, y - bh / 2, x + bw / 2, y + bh / 2], 34, fill=(28, 28, 33), outline=mix((28, 28, 33), c, .5), w=2)
            put_icon(cv, ICONS[i] if i < len(ICONS) else "circle", (18, 18, 20), x - bw / 2 + 58, y, 40, chip=c)
            box_text(cv, x + 40, y, t, 40, st["ink"], PX)
    by0, by1 = 880, 1000
    band, lab_c, txt_c = (NAVY, POP[1], WHITE) if mode == "light" else (NEON[0], (18, 18, 20), (18, 18, 20))
    cv.rr([L, by0, RT, by1], 32, fill=band)
    if mode == "dark": put_icon(cv, "notebook-pen", (18, 18, 20), L + 70, (by0 + by1) / 2, 46); L0 = L + 60
    else: L0 = L
    lw = cv.tw(exit_label, PX, 46); cv.text(L0 + 44, (by0 + by1) / 2, exit_label, PX, 46, lab_c, "lm")
    cv.text(L0 + 44 + lw + 34, (by0 + by1) / 2, exit_text, PX, cv.fit(exit_text, PX, 46, RT - L - lw - 120, 42), txt_c, "lm")
    arrow(cv, cx + r + bw / 2 - 34, cy + bh / 2 + 8, cx + r + bw / 2 - 34, by0 - 12, NAVY if mode == "light" else NEON[0], 6, 24)
    cv.save(name)

def screen_k(name, head, shot, crop_h, notes, mode="dark"):
    from PIL import Image
    st = KEY[mode]; im = Image.open(shot).convert("RGB"); im = im.crop((0, 0, im.width, min(crop_h, im.height)))
    pad_px = 60; bgc = im.getpixel((im.width - 4, 6)); cvs = Image.new("RGB", (im.width + pad_px * 2, im.height + pad_px), bgc); cvs.paste(im, (pad_px, pad_px)); im = cvs   # 캡처 글자가 틀에 붙지 않게 화면 안쪽 여백
    pw = 420; ph = int(im.height * pw / im.width); H = ph + 260; cv = Cv(H, st["bg"])
    x0, y0, pad = L + 34, 186, 22                              # 폰 틀: 화면 둘레에 검은 테두리 여백
    if mode == "dark":
        glow(cv, H, [(NEON[2], (x0 + pw / 2 - 40, y0 + 120), 300, .55), (NEON[3], (x0 + pw / 2 + 120, y0 + ph), 300, .5), (NEON[0], (RT - 60, 180), 200, .25)])
        soft_shadow(cv, [x0 - pad, y0 - pad, x0 + pw + pad, y0 + ph + pad], 48)
    k_head(cv, head, st)
    cv.rr([x0 - pad, y0 - pad, x0 + pw + pad, y0 + ph + pad], 48, fill=(0, 0, 0) if mode == "dark" else (29, 29, 31), outline=(70, 70, 78) if mode == "dark" else None, w=2)
    cv.img.paste(im.resize((pw * K.S, ph * K.S)), (x0 * K.S, y0 * K.S))
    tx = x0 + pw + pad + 40; n = len(notes); gap = 20; ch = (ph - gap * (n - 1)) / n; y = y0
    for j, (lab, txt) in enumerate(notes):                    # 벤토 카드: 칸마다 다른 강조색 띠 + 이름표 + 큰 값
        c = POP[j % 4] if mode == "light" else NEON[[0, 1, 2][j % 3]]
        cv.rr([tx, y, RT, y + ch], 30, fill=st["card"] if mode == "dark" else tint(c, .2))
        if mode == "dark":
            cv.rr([tx, y, RT, y + ch], 30, fill=(28, 28, 33), outline=mix((28, 28, 33), c, .45), w=2)
            put_icon(cv, ["calendar-days", "sparkles", "list-checks"][j % 3], (18, 18, 20), RT - 62, y + 50, 34, chip=c)
        else: cv.rr([tx, y + 22, tx + 10, y + ch - 22], 5, fill=c)
        cv.text(tx + 36, y + 44, lab, PB, 34, c if mode == "dark" else deep(c, .45) if j != 1 else (120, 76, 10), "lm")
        cv.text(tx + 36, y + ch - 34, txt, PB if not any('\u4e00' <= c <= '\u9fff' for c in txt) else PB, cv.fit(txt, PX, 50, RT - tx - 140, 38), st["ink"], "ls")
        y += ch + gap
    cv.save(name)


# ---- v5(10/15 대표 "디자인 감 좀 올려라", docs/디자인_레퍼런스_라이브러리): 아이콘(Lucide)·빛 방울 배경(Haikei 방식)·기기 목업(Shots.so 방식) ----
ICON_DIR = os.path.join(HERE, "..", "assets", "icons", "lucide")
def icon(name, color, px, stroke=2.2):
    import cairosvg, io
    from PIL import Image
    svg = open(os.path.join(ICON_DIR, name + ".svg"), encoding="utf-8").read().replace("currentColor", "#%02x%02x%02x" % color).replace('stroke-width="2"', f'stroke-width="{stroke}"')
    return Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg.encode(), output_width=px * K.S, output_height=px * K.S))).convert("RGBA")
def put_icon(cv, name, color, cx, cy, px, chip=None):
    if chip: cv.rr([cx - px * .9, cy - px * .9, cx + px * .9, cy + px * .9], px * .45, fill=chip)
    im = icon(name, color, px); cv.img.paste(im, (int((cx - px / 2) * K.S), int((cy - px / 2) * K.S)), im)
def glow(cv, H, spots):
    """어두운 판 위에 흐린 빛 방울(색, 중심, 반지름, 세기). 바탕 판 안에서만."""
    from PIL import Image, ImageDraw, ImageFilter
    W = K.BW * K.S; layer = Image.new("RGB", (W, H * K.S), (0, 0, 0)); d = ImageDraw.Draw(layer)
    for col, (x, y), r, a in spots:
        d.ellipse([(x - r) * K.S, (y - r) * K.S, (x + r) * K.S, (y + r) * K.S], fill=tuple(int(v * a) for v in col))
    layer = layer.filter(ImageFilter.GaussianBlur(140 * K.S))
    from PIL import ImageChops
    m = Image.new("L", layer.size, 0); ImageDraw.Draw(m).rounded_rectangle([K.OX * K.S, 0, (K.OX + K.CW) * K.S - 1, H * K.S - 1], 44 * K.S, fill=255)
    lit = ImageChops.add(cv.img, layer); cv.img.paste(lit, (0, 0), m); cv.d = ImageDraw.Draw(cv.img)
def soft_shadow(cv, box, r, blur=40, alpha=170):
    from PIL import Image, ImageDraw, ImageFilter
    W, Hh = cv.img.size; sh = Image.new("L", (W, Hh), 0)
    ImageDraw.Draw(sh).rounded_rectangle([v * K.S for v in (box[0], box[1] + 24, box[2], box[3] + 24)], r * K.S, fill=alpha)
    sh = sh.filter(ImageFilter.GaussianBlur(blur * K.S)); black = Image.new("RGB", (W, Hh), (0, 0, 0)); cv.img.paste(black, (0, 0), sh); cv.d = ImageDraw.Draw(cv.img)

BODY_LINE = {   # 이미지 바로 위에 넣을 본문 문장(이미지에 박지 않는 설명)
 "n47": "아래는 1995년 3월 19일(예시 생일)로 자오선 무료 풀이를 직접 열어 본 화면이에요.",
 "n34": "같은 생각이 되풀이되는 모양을 그림으로 그려 보면 이래요.",
}
SPEC = {
 "n47": lambda m="dark": screen_k("naver_z47_s.jpg" if m == "dark" else "naver_z47_s_light.jpg", "무료 풀이를 직접 열어 봤어요", os.environ.get("SHOT", "free.png"), 1365,
                       [("생년월일", "1995년 3월 19일"), ("태어난 날 첫 글자", "기(己) · 기름진 논밭"), ("이어서 나오는 것", "성격 · 사랑 · 일 · 돈")], m),
 "n34": lambda m="dark": loop_k("naver_z34_p.jpg" if m == "dark" else "naver_z34_p_light.jpg", "생각이 같은 자리를 도는 고리",
                       [["같은 걱정이", "떠올라요"], ["그 장면을", "되짚어요"], ["기분이 더", "가라앉아요"], ["잠이 줄고", "월요일이 무겁죠"]],
                       "끊는 법", "종이에 다 적고, 내일 할 일 하나만 정해요", m, ["brain", "history", "cloud-rain", "moon"]),
}
if __name__ == "__main__":
    m = os.environ.get("MODE", "dark")
    for k in sys.argv[1:]: SPEC[k](m); print(k, m, "만듦", K.WARN or "")
