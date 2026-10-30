"""클립·릴스 표지 고침 시안 3장(전·후) — CT 10/29 14:45, 대표 10/29 14:39 "정월 크게 넣는 건 보류".
근거: zaoseon-site docs/표지_조사_운세심리_인스타_2026-10-29.md (인스타 237편 · 우리 클립 12편).

시안 = 승인 전 그림이다. 예약 글을 바꾸지 않고, 제작 가이드라인·card_gate 규칙도 아직 바꾸지 않는다.
  (가) 띠+생년형  2027 돼지띠 — 값은 zaoseon-site tools/tti_extra.json 에서 읽고 assert 로 잰다
  (나) 절기 날짜형 2026 입동 — 날짜·시각은 zaoseon-site engine.get_solar_terms_kst(2026) 에서 읽는다
  (다) 번호 고르기형 · 돈 — 운세를 단정하지 않는 '돈 버릇' 자가진단(허황·단정 문구 없음)

규칙: 판은 color_combos.json, 규격은 channel_specs(reel = naver_clip 같은 영상), 글꼴은 fonts_kit.
그리기 전 card_gate.before(), 그린 뒤 card_gate.after() — 화면 전체 그림(M1)은 바탕 무늬가 가장자리까지 가서
after() 의 좌우 여백 검사가 바탕을 글로 읽는다. 그래서 같은 자리의 '글자 층'(단색 바탕)을 따로 그려 after() 로
안전 영역·좌우 균형·세로 가운데를 재고, 완성본은 faint_gate(K-138 글자 묻힘)로 잰다.
실행: python3 2026-cover-sian/build.py  (sns-images 바로 위에 zaoseon-site 가 나란히 있어야 함)
"""
import os, sys, json, math, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SITE = os.environ.get("ZS_SITE", os.path.join(os.path.dirname(ROOT), "zaoseon-site"))
sys.path.insert(0, os.path.join(ROOT, "pipeline"))
import channel_specs as CS, card_gate as G, fonts_kit as FK, faint_gate as FG

CHN = "reel"                      # 릴스와 네이버 클립은 같은 영상(안전 영역 교집합)
C = CS.CH[CHN]
W, H = C["w"], C["h"]
SX0, SY0, SX1, SY1 = C["safe"]
CX = (SX0 + SX1) // 2
Z = {z[0]: z[1:5] for z in C["zones"]}
PAL = {p["id"]: p for p in json.load(open(os.path.join(ROOT, "assets/palettes/color_combos.json"), encoding="utf-8"))["palettes"]}
OUT = os.path.join(HERE, "out"); os.makedirs(OUT, exist_ok=True)

def F(k, s): return ImageFont.truetype(FK.P[k], s)
TITLE, BODY = "gm_bold", "pr_xb"
HANJA = FK.P["serif"]

# ── 값 확인(엔진·계산값만) ───────────────────────────────────────────
TTI = json.load(open(os.path.join(SITE, "tools/tti_extra.json"), encoding="utf-8"))
assert TTI["pig"]["good"] == ["2월", "3월", "7월"] and TTI["pig"]["care"] == ["4월", "5월"], TTI["pig"]
PIG_YEARS = [1983, 1995, 2007, 2019]
assert all((y - 1983) % 12 == 0 and (y - 4) % 12 == 11 for y in PIG_YEARS)       # 해(亥)년 = (연도-4) mod 12 == 11
sys.path.insert(0, os.path.join(SITE, "engine"))
try:
    import engine as EN
    IPDONG = [t for t in EN.get_solar_terms_kst(2026) if t[0] == "입동"][0][2]
except Exception as e:                                                          # pyswisseph 없으면 멈춘다(짐작 날짜 금지)
    raise SystemExit(f"입동 날짜를 엔진으로 못 셌어요: {e}")
assert (IPDONG.month, IPDONG.day) == (11, 7), IPDONG
YO = "월화수목금토일"[IPDONG.weekday()]

# ── 그리기 도구 ───────────────────────────────────────────────────────
def hx(h): h = h.lstrip("#"); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
def grad(top, bot):
    im = Image.new("RGB", (W, H)); d = ImageDraw.Draw(im)
    for y in range(H):
        t = y / (H - 1); d.line([(0, y), (W, y)], fill=tuple(int(a + (b - a) * t) for a, b in zip(top, bot)))
    return im
def tw(d, s, f): b = d.textbbox((0, 0), s, font=f); return b[2] - b[0]

# 어두운 판에서는 검정 테두리·그림자가 바탕과 같은 색이라 보이지도 않고 K-138 검사가 '묻힌 글'로 잡는다(10/30 실측 대비 1.06).
# 대신 글자 칸 뒤를 scrim 으로 어둡게 한다. 밝은 사진 바탕을 쓸 때만 OUTLINE=True.
OUTLINE = False

def line(d, y, parts, size, font=TITLE, stroke=10, shadow=True, base=None):
    """parts=[(글, 색)] 한 줄을 가운데에. 두꺼운 테두리(검정) — 조사 3절 '두꺼운 테두리·그림자'."""
    f = F(font, size)
    if not OUTLINE: stroke, shadow = 0, False
    total = sum(tw(d, s, f) for s, _ in parts)
    x = CX - total // 2
    for s, col in parts:
        if shadow:
            d.text((x + 6, y + 8), s, font=f, fill=(0, 0, 0), stroke_width=stroke, stroke_fill=(0, 0, 0))
        d.text((x, y), s, font=f, fill=col, stroke_width=stroke, stroke_fill=(10, 10, 14))
        x += tw(d, s, f)
    return total

def pill(d, y, text, size, fg, bg, pad=(34, 16), outline=None):
    f = F(BODY, size); w = tw(d, text, f); b = d.textbbox((0, 0), text, font=f)
    h = b[3] - b[1]; x0 = CX - w // 2 - pad[0]
    d.rounded_rectangle([x0, y, CX + w // 2 + pad[0], y + h + pad[1] * 2], radius=(h + pad[1] * 2) // 2, fill=bg, outline=outline, width=4 if outline else 0)
    d.text((CX - w // 2, y + pad[1] - b[1]), text, font=f, fill=fg)
    return y + h + pad[1] * 2

def url(d, col):
    f = F(TITLE, 36); z = Z["하단 고정"]
    d.text((z[2] - tw(d, "zaoseon.com", f), z[1]), "zaoseon.com", font=f, fill=col)

def stars(im, n, seed, col=(255, 255, 255), big=0.04):
    r = random.Random(seed); d = ImageDraw.Draw(im)
    for _ in range(n):
        x, y = r.randrange(W), r.randrange(H); s = 1 if r.random() > big else r.choice((2, 3))
        a = r.randint(90, 255); d.ellipse([x - s, y - s, x + s, y + s], fill=tuple(int(c * a / 255) for c in col))

def scrim(im, y0, y1, alpha=150):
    """글자 칸 뒤만 살짝 어둡게(가운데 진하고 위아래 흐림) — 그림을 살리고 글은 읽히게."""
    m = Image.new("L", (W, H), 0); dm = ImageDraw.Draw(m)
    for y in range(max(0, y0 - 160), min(H, y1 + 160)):
        k = 1.0 if y0 <= y <= y1 else max(0.0, 1 - min(abs(y - y0), abs(y - y1)) / 160)
        dm.line([(0, y), (W, y)], fill=int(alpha * k))
    return Image.composite(Image.new("RGB", (W, H), (0, 0, 0)), im, m)

# ── (가) 띠+생년형 · k_gold ────────────────────────────────────────
def bg_ga():
    p = PAL["k_gold"]["colors"]
    im = grad((14, 16, 30), hx(p["블랙"])); stars(im, 900, 27)
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    gold = hx(p["골드"])
    d.text((W // 2, 980), "亥", font=ImageFont.truetype(HANJA, 1100), fill=gold + (26,), anchor="mm")   # 돼지(亥) 한자 큰 무늬
    for r_, a in ((560, 70), (640, 40)): d.ellipse([W // 2 - r_, 980 - r_, W // 2 + r_, 980 + r_], outline=gold + (a,), width=3)
    for i in range(12):                                                        # 열두 띠 자리 눈금
        t = math.radians(i * 30 - 90); x, y = W // 2 + 600 * math.cos(t), 980 + 600 * math.sin(t)
        d.ellipse([x - 9, y - 9, x + 9, y + 9], fill=gold + (200 if i == 11 else 70,))
    d.ellipse([800, 170, 980, 350], fill=(245, 236, 210, 235)); d.ellipse([850, 150, 1030, 330], fill=(14, 16, 30, 255))  # 초승달
    im = Image.alpha_composite(im.convert("RGBA"), lay.filter(ImageFilter.GaussianBlur(1))).convert("RGB")
    return scrim(im, 560, 1330, 120)

def text_ga(d, flat=False):
    p = PAL["k_gold"]["colors"]; gold, cream = hx(p["골드"]), hx(p["크림"])
    y = Z["상단 라벨"][1]
    pill(d, y, "정미년 띠별 운세", 40, (18, 18, 18), gold)
    line(d, 612, [("2027 돼지띠", (255, 255, 255))], 118, stroke=0 if flat else 10, shadow=not flat)
    line(d, 760, [("힘 쓸 달 ", (255, 255, 255)), ("2·3·7월", (255, 214, 0))], 112, stroke=0 if flat else 10, shadow=not flat)
    yy = 960
    for s in ("1983 · 1995", "2007 · 2019년생"):
        yy = pill(d, yy, s, 60, (18, 18, 18), cream, pad=(40, 14)) + 22
    pill(d, 1282, "아낄 달은 4·5월, 내 해 찾아보세요", 48, cream, (18, 18, 18), outline=gold)

# ── (나) 절기 날짜형 · w_navy_butter ─────────────────────────────────
def bg_na():
    p = PAL["w_navy_butter"]["colors"]; navy = hx(p["네이비"])
    im = grad((40, 62, 96), navy); stars(im, 260, 7, col=(230, 236, 246))
    d = ImageDraw.Draw(im)
    d.ellipse([140, 210, 380, 450], fill=(236, 238, 230))                          # 겨울 저녁 달
    r = random.Random(11)
    for k, (base, amp, col) in enumerate(((1250, 170, (52, 74, 108)), (1430, 140, (34, 52, 82)), (1600, 120, (20, 34, 58)))):
        pts = [(0, H)]
        for x in range(0, W + 40, 40):
            pts.append((x, base - amp * abs(math.sin(x / (180 + 60 * k) + k)) - r.randint(0, 30)))
        pts.append((W, H)); d.polygon(pts, fill=col)
        for x in range(0, W, 40):                                                 # 산등성이 서리
            yv = base - amp * abs(math.sin(x / (180 + 60 * k) + k)); d.line([(x, yv), (x + 40, yv)], fill=(200, 214, 232), width=2)
    for _ in range(420):                                                          # 첫 서리·눈 알갱이
        x, y, s = r.randrange(W), r.randrange(H), r.choice((2, 3, 4)); d.ellipse([x, y, x + s, y + s], fill=(240, 244, 250))
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dl = ImageDraw.Draw(lay)
    dl.text((W // 2, 930), "立冬", font=ImageFont.truetype(HANJA, 520), fill=hx(p["소프트 버터"]) + (34,), anchor="mm")
    im = Image.alpha_composite(im.convert("RGBA"), lay).convert("RGB")
    return scrim(im, 560, 1330, 110)

def text_na(d, flat=False):
    p = PAL["w_navy_butter"]["colors"]; butter, navy = hx(p["소프트 버터"]), hx(p["네이비"])
    pill(d, Z["상단 라벨"][1], f"{IPDONG.month}월 {IPDONG.day}일 {YO}요일", 44, navy, butter)
    line(d, 640, [("입동, 오늘부터", (255, 255, 255))], 112, stroke=0 if flat else 10, shadow=not flat)
    line(d, 800, [("겨울", butter), ("이에요", (255, 255, 255))], 150, stroke=0 if flat else 12, shadow=not flat)
    line(d, 1040, [("절기로 보는 겨울 첫날", (255, 255, 255))], 58, font=BODY, stroke=0 if flat else 6, shadow=not flat)
    pill(d, 1282, f"저녁 {IPDONG.hour - 12}시 {IPDONG.minute}분에 바뀌어요", 48, (255, 255, 255), navy, outline=butter)

# ── (다) 번호 고르기 · 돈 · dg_gold ──────────────────────────────────
def bg_da():
    p = PAL["dg_gold"]["colors"]; green, gold = hx(p["딥그린"]), hx(p["골드"])
    im = grad((30, 78, 64), green); lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    r = random.Random(3)
    for _ in range(26):                                                            # 엽전(가운데 네모 구멍)
        x, y, s = r.randrange(-60, W), r.choice([r.randrange(0, 520), r.randrange(1350, H)]), r.randrange(70, 150)
        d.ellipse([x, y, x + s, y + s], outline=gold + (150,), width=8, fill=gold + (60,))
        q = s // 5; d.rectangle([x + s // 2 - q // 2, y + s // 2 - q // 2, x + s // 2 + q // 2, y + s // 2 + q // 2], outline=gold + (160,), width=5)
    d.text((W // 2, 300), "財", font=ImageFont.truetype(HANJA, 520), fill=gold + (22,), anchor="mm")
    im = Image.alpha_composite(im.convert("RGBA"), lay.filter(ImageFilter.GaussianBlur(1.2))).convert("RGB")
    return scrim(im, 560, 1330, 90)

def text_da(d, flat=False):
    p = PAL["dg_gold"]["colors"]; green, gold, ivory = hx(p["딥그린"]), hx(p["골드"]), hx(p["아이보리"])
    pill(d, Z["상단 라벨"][1], "1초 마음 고르기", 44, green, ivory)
    line(d, 612, [("끌리는 번호 하나", (255, 255, 255))], 104, stroke=0 if flat else 10, shadow=not flat)
    line(d, 752, [("내 ", (255, 255, 255)), ("돈", (255, 214, 0)), (" 버릇 보기", (255, 255, 255))], 112, stroke=0 if flat else 10, shadow=not flat)
    cw, ch, gap = 180, 250, 26; x0 = CX - (4 * cw + 3 * gap) // 2; y0 = 948
    for i in range(4):
        x = x0 + i * (cw + gap)
        d.rounded_rectangle([x, y0, x + cw, y0 + ch], radius=22, fill=green, outline=gold, width=6)
        d.rounded_rectangle([x + 14, y0 + 14, x + cw - 14, y0 + ch - 14], radius=14, outline=gold, width=2)
        f = F(TITLE, 120); s = str(i + 1); d.text((x + cw // 2, y0 + ch // 2), s, font=f, fill=ivory, anchor="mm")
    pill(d, 1282, "고른 번호를 댓글로 남겨 주세요", 48, (18, 18, 18), gold)

# ── 사양(관문용) ─────────────────────────────────────────────────────
SPECS = [
    dict(id="ga", 이름="(가) 띠+생년형", pal="k_gold", bg=PAL["k_gold"]["colors"]["블랙"], accent="#FFD600",
         **{"강조색 까닭": "조사 3절 '노랑 큰 글자' — y_black 판의 옐로우, 검정 바탕 대비 확인"},
         hook=["2027 돼지띠", "힘 쓸 달 2·3·7월"], kick="정미년 띠별 운세", cta="아낄 달은 4·5월, 내 해 찾아보세요",
         훅="상황 지목", layout="L2", method="M1 배경 이미지", draw=(bg_ga, text_ga), before="clips_reel/rc-1025-pig_thumb.png",
         before_name="지금: 10/25 클립 '2027 돼지띠'(조회 87)"),
    dict(id="na", 이름="(나) 절기 날짜형", pal="w_navy_butter", bg=PAL["w_navy_butter"]["colors"]["네이비"], accent=PAL["w_navy_butter"]["colors"]["소프트 버터"],
         hook=["입동, 오늘부터", "겨울이에요"], kick=f"{IPDONG.month}월 {IPDONG.day}일 {YO}요일", cta=f"저녁 {IPDONG.hour - 12}시 {IPDONG.minute}분에 바뀌어요",
         훅="계산 내역 공개", layout="L6", method="M1 배경 이미지", draw=(bg_na, text_na), before="clips_reel/rc-1020-star_thumb.png",
         before_name="지금: 10/20 클립 표지(같은 별밤 틀)"),
    dict(id="da", 이름="(다) 번호 고르기형 · 돈", pal="dg_gold", bg=PAL["dg_gold"]["colors"]["딥그린"], accent="#FFD600",
         **{"강조색 까닭": "조사 3절 '핵심 한 단어만 색' — y_black 판의 옐로우, 딥그린 대비 확인"},
         hook=["끌리는 번호 하나", "내 돈 버릇 보기"], kick="1초 마음 고르기", cta="고른 번호를 댓글로 남겨 주세요",
         훅="자가진단·번호 고르기", layout="L8", method="M1 배경 이미지", draw=(bg_da, text_da), before="clips_reel/rc-1015-pick_thumb.png",
         before_name="지금: 10/15 클립 '카드 고르기'"),
]

def build(c, prev_layouts):
    G.before(c, CHN, prev_layouts=prev_layouts)                                  # 그리기 전 관문
    bgf, txf = c["draw"]
    # 1) 글자 층(단색 바탕)으로 자리 검사
    flat = Image.new("RGB", (W, H), hx(c["bg"])); txf(ImageDraw.Draw(flat), flat=True)
    fp = os.path.join(OUT, f"{c['id']}_layer.png"); flat.save(fp)
    cc = {k: v for k, v in c.items() if k != "method"}
    G.after(fp, cc, CHN)
    # 2) 완성본
    im = bgf(); d = ImageDraw.Draw(im); txf(d); url(d, (231, 200, 141))
    op = os.path.join(OUT, f"{c['id']}_after.jpg"); im.save(op, quality=90)
    h = FG.hits(op)
    if h: raise SystemExit(f"[K-138] {c['id']} 글자 묻힘: {h[:3]}")
    return op

def sheet(c, after_path):
    """전·후 나란히 — 운영앱 '승인해 주세요'에 그림으로 올림(대표는 그림으로 봄)."""
    import subprocess
    bp = os.path.join(OUT, f"{c['id']}_before.png")
    if not os.path.exists(bp):
        with open(bp, "wb") as fh: fh.write(subprocess.check_output(["git", "-C", ROOT, "show", "HEAD:" + c["before"]]))
    s = 0.5; w, h = int(W * s), int(H * s); pad, top = 40, 150
    sh = Image.new("RGB", (w * 2 + pad * 3, h + top + 170), (245, 242, 236)); d = ImageDraw.Draw(sh)
    a = Image.open(after_path).convert("RGB")
    a2 = a   # 캐릭터 자리는 그림에 점선을 덮지 않고 아래 글로 적는다(점선이 글·주소를 덮었다, 10/30 눈으로 확인)
    sh.paste(Image.open(bp).convert("RGB").resize((w, h)), (pad, top)); sh.paste(a2.resize((w, h)), (pad * 2 + w, top))
    d.text((pad, 30), c["이름"], font=F(TITLE, 56), fill=(20, 20, 20))
    d.text((pad, top - 46), c["before_name"], font=F(BODY, 30), fill=(90, 90, 90))
    d.text((pad * 2 + w, top - 46), "고친 시안(정월 없음, 위 고정 줄 뺌)", font=F(BODY, 30), fill=(150, 60, 40))
    d.text((pad, top + h + 30), "캐릭터 자리는 비워 둠. 정해지면 글을 왼쪽으로 옮기고 오른쪽 아래에 세워요.\n영상 0초 프레임이 이 표지예요(빈 검정 첫 화면 없음).", font=F(BODY, 30), fill=(60, 60, 60))
    p = os.path.join(OUT, f"{c['id']}_sheet.jpg"); sh.save(p, quality=88); return p

if __name__ == "__main__":
    prev = []
    for c in SPECS:
        op = build(c, prev); prev.append(c["layout"]); print("통과", c["id"], op, sheet(c, op))
