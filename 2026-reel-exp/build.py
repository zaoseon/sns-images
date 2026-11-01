"""릴스 첫 3초 실험 3편 — 쥐띠·말띠·호랑이띠 2027 (CT 11/1 17:20 → ①, 대표 11/1 17:08 "진행해").
근거: Metricool 9/29~10/31 릴스 66편 — 3초 시청률 대부분 3~13%, 예외 뱀띠 2027(10/31, cover1030 새 표지) 34.5%.
같은 주제는 그대로 두고 첫 3초만 바꾼다.

편마다 9:16 · 10초 · 장면 4개
  0.0~1.5초  첫 프레임 = cover1030 (가) 띠+생년 표지. 띠 이름이 가장 큰 글자 + 한 줄 훅. 위 고정 줄 없음(표지 장면).
  1.5~5.0초  힘 쓸 달 3개 큰 숫자(하나씩 나타남)
  5.0~8.0초  아낄 달 + 해 볼 것 한 줄
  8.0~10.0초 "주변 ○띠 태그해 줘"
정월 없음 · 성찰 문장('마음을 돌아봐'·💛) 없음 · 검정 빈 첫 프레임 없음 · 브랜드 고정 줄은 2장면부터.
값: zaoseon-site tools/tti_extra.json(= n80·/2027/ 띠 페이지) assert. 훅·해 볼 것은 발행된 n80 문장에서 줄였다(새 주장 없음).
관문: 장면마다 card_gate.before(reel) · 글자 층 after(reel) · 완성 프레임 faint_gate(K-138).
결과: silent/rx-<띠>.mp4(음악 없음, 기본 — 대표가 인스타 앱에서 유행 음원을 붙임) · 음악 판은
  ZS_SRC=2026-reel-exp/silent ZS_OUT=2026-reel-exp/music ZS_PRE=rx- python3 pipeline/clip_v3_music.py  (음악 도구는 이것 하나, K-070)
실행: python3 2026-reel-exp/build.py   (sns-images 옆에 zaoseon-site)"""
import os, sys, json, math, random, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
SITE = os.environ.get("ZS_SITE", os.path.join(os.path.dirname(ROOT), "zaoseon-site"))
sys.path.insert(0, os.path.join(ROOT, "pipeline"))
import channel_specs as CS, card_gate as G, fonts_kit as FK, faint_gate as FG

CHN = "reel"; C = CS.CH[CHN]; W, H = C["w"], C["h"]
SX0, SY0, SX1, SY1 = C["safe"]; CX = (SX0 + SX1) // 2
Z = {z[0]: z[1:5] for z in C["zones"]}
PAL = {p["id"]: p for p in json.load(open(os.path.join(ROOT, "assets/palettes/color_combos.json"), encoding="utf-8"))["palettes"]}
FPS = 30; T = [0.0, 1.5, 5.0, 8.0, 10.0]
OUTD = {k: os.path.join(HERE, k) for k in ("silent", "frames")}
for p in OUTD.values(): os.makedirs(p, exist_ok=True)
def F(k, s): return ImageFont.truetype(FK.P[k], s)
TITLE, BODY, HANJA = "gm_bold", "pr_xb", FK.P["serif"]
YEL = (255, 214, 0); WHITE = (255, 255, 255)
def hx(h): h = h.lstrip("#"); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
def tw(d, s, f): b = d.textbbox((0, 0), s, font=f); return b[2] - b[0]

# ── 값(계산값만) ─────────────────────────────────────────────────────
TTI = json.load(open(os.path.join(SITE, "tools/tti_extra.json"), encoding="utf-8"))
BR = "子丑寅卯辰巳午未申酉戌亥"
def years(i): return [y for y in range(1970, 2023) if (y - 4) % 12 == i]
REELS = [
    # slug, 이름, 지지 순번, 판, 훅(n80 발행 문장에서), 해 볼 달, 해 볼 것(n80), 근거
    dict(slug="rat", name="쥐띠", i=0, pal="k_gold", bgk="블랙", hook=("돈 기회", "열리는 해"), m="4월", todo=("미뤄 둔 돈 이야기", "글로 정리하기"),
         why="물인 쥐띠에게 해의 불(丁)은 재물(n80)"),
    dict(slug="horse", name="말띠", i=6, pal="dg_gold", bgk="딥그린", hook=("좋은 짝과", "손잡는 해"), m="2월", todo=("함께할 사람과", "첫 약속 날짜 정하기"),
         why="말(午)과 양(未)은 육합(n80)"),
    dict(slug="tiger", name="호랑이띠", i=2, pal="w_navy_butter", bgk="네이비", hook=("실력이", "눈에 띄는 해"), m="6월", todo=("보여 줄 결과물 하나에", "마감 날짜 붙이기"),
         why="나무(寅)가 불(丁)을 키움 = 밖으로 나가는 힘(n80)"),
]
assert (2027 - 4) % 12 == BR.index("未")
LIUHE = {0: 1, 2: 11, 3: 10, 4: 9, 5: 8, 6: 7}
assert LIUHE[6] == BR.index("未")                                           # 말–양 육합
for r in REELS:
    t = TTI[r["slug"]]; r["good"], r["care"] = t["good"], t["care"]
    assert r["m"] in r["good"], (r["name"], r["m"], r["good"])             # 해 볼 달은 힘 쓸 달 안에서(n80과 같은 규칙)
    r["years"] = years(r["i"])[-4:]
    assert all((y - 4) % 12 == r["i"] for y in r["years"])
assert REELS[0]["years"] == [1984, 1996, 2008, 2020] and REELS[1]["years"] == [1978, 1990, 2002, 2014] and REELS[2]["years"] == [1986, 1998, 2010, 2022]
assert REELS[0]["good"] == ["4월", "8월", "이듬해 1월"] and REELS[1]["good"] == ["2월", "7월", "10월"] and REELS[2]["good"] == ["6월", "10월", "11월"]

# ── 바탕(표지 시안 (가)와 같은 그림 방식: 별밤 + 띠 한자 + 열두 띠 눈금) ───────
def grad(top, bot):
    im = Image.new("RGB", (W, H)); d = ImageDraw.Draw(im)
    for y in range(H):
        k = y / (H - 1); d.line([(0, y), (W, y)], fill=tuple(int(a + (b - a) * k) for a, b in zip(top, bot)))
    return im
def stars(im, n, seed):
    r = random.Random(seed); d = ImageDraw.Draw(im)
    for _ in range(n):
        x, y = r.randrange(W), r.randrange(H); s = 1 if r.random() > .04 else r.choice((2, 3)); a = r.randint(90, 255)
        d.ellipse([x - s, y - s, x + s, y + s], fill=(a, a, a))
def scrim(im, y0, y1, alpha):
    m = Image.new("L", (W, H), 0); dm = ImageDraw.Draw(m)
    for y in range(max(0, y0 - 160), min(H, y1 + 160)):
        k = 1.0 if y0 <= y <= y1 else max(0.0, 1 - min(abs(y - y0), abs(y - y1)) / 160)
        dm.line([(0, y), (W, y)], fill=int(alpha * k))
    return Image.composite(Image.new("RGB", (W, H), (0, 0, 0)), im, m)
def background(r):
    p = PAL[r["pal"]]["colors"]; base = hx(p[r["bgk"]]); acc = hx(list(p.values())[1])
    glyph_alpha = 26 if sum(acc) < 600 else 12            # 밝은 버터색 한자 무늬는 K-138이 글자로 읽어서(1.16) 더 옅게
    top = tuple(min(255, int(c * 1.0 + 22)) for c in base)
    im = grad(top, base); stars(im, 700, 100 + r["i"])
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.text((W // 2, 980), BR[r["i"]], font=ImageFont.truetype(HANJA, 1100), fill=acc + (glyph_alpha,), anchor="mm")
    for rr, a in ((560, 70), (640, 40)): d.ellipse([W // 2 - rr, 980 - rr, W // 2 + rr, 980 + rr], outline=acc + (a,), width=3)
    for k in range(12):
        t = math.radians(k * 30 - 90); x, y = W // 2 + 600 * math.cos(t), 980 + 600 * math.sin(t)
        d.ellipse([x - 9, y - 9, x + 9, y + 9], fill=acc + (220 if k == r["i"] else 70,))
    im = Image.alpha_composite(im.convert("RGBA"), lay.filter(ImageFilter.GaussianBlur(1))).convert("RGB")
    return scrim(im, 560, 1330, 120), acc

# ── 글자 층 그리기(투명 RGBA 위) ──────────────────────────────────────
def center(d, y, parts, size, font=TITLE):
    f = F(font, size); x = CX - sum(tw(d, s, f) for s, _ in parts) // 2
    for s, col in parts: d.text((x, y), s, font=f, fill=col); x += tw(d, s, f)
def pill(d, y, text, size, fg, bg, pad=(34, 16), outline=None, x_center=CX):
    f = F(BODY, size); w = tw(d, text, f); b = d.textbbox((0, 0), text, font=f); h = b[3] - b[1]
    d.rounded_rectangle([x_center - w // 2 - pad[0], y, x_center + w // 2 + pad[0], y + h + pad[1] * 2], radius=(h + pad[1] * 2) // 2,
                        fill=bg, outline=outline, width=4 if outline else 0)
    d.text((x_center - w // 2, y + pad[1] - b[1]), text, font=f, fill=fg); return y + h + pad[1] * 2
def brand(d, acc):
    """고정 요소(2장면부터): 상단 왼쪽 자오선 · 오른쪽 동서양 6개 운명학 교차분석 · 하단 오른쪽 zaoseon.com."""
    z = Z["상단 왼쪽 고정"]; d.text((z[0], z[1]), "자오선", font=F(TITLE, 40), fill=WHITE)
    z = Z["상단 오른쪽 고정"]; f = F(BODY, 34); s = "동서양 6개 운명학 교차분석"; d.text((z[2] - tw(d, s, f), z[1] + 4), s, font=f, fill=(225, 225, 225))
    url(d, acc)
def url(d, acc):
    f = F(TITLE, 36); z = Z["하단 고정"]; d.text((z[2] - tw(d, "zaoseon.com", f), z[1]), "zaoseon.com", font=f, fill=acc)
def layer(): im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); return im, ImageDraw.Draw(im)
def mlabel(s): return s.replace("이듬해 ", "")

def scene_cover(r, acc):
    im, d = layer(); cream = (246, 240, 229)
    pill(d, Z["상단 라벨"][1], "정미년 띠별 운세", 40, (18, 18, 18), acc)
    sz = 150
    while tw(d, "2027 " + r["name"], F(TITLE, sz)) > SX1 - SX0 - 60: sz -= 4
    assert sz > 92, sz                                                                              # 띠 이름이 가장 큰 글자(훅 92px보다 커야 함)
    center(d, 610 + (150 - sz) // 2, [("2027 ", WHITE), (r["name"], YEL)], sz)
    center(d, 800, [(r["hook"][0] + " ", WHITE), (r["hook"][1], WHITE)], 92)
    yy = 960
    for s in (f"{r['years'][0]} · {r['years'][1]}", f"{r['years'][2]} · {r['years'][3]}년생"):
        yy = pill(d, yy, s, 60, (18, 18, 18), cream, pad=(40, 14)) + 22
    pill(d, 1282, "내 띠 힘 쓸 달 3개 보기", 48, cream, (18, 18, 18), outline=acc)
    return im
def scene_good(r, acc, shown):
    im, d = layer()
    pill(d, Z["상단 라벨"][1], f"2027 {r['name']}", 44, (18, 18, 18), acc)
    center(d, 640, [("힘 쓸 달", WHITE)], 112)
    bw, bh, gap = 250, 300, 30; x0 = CX - (3 * bw + 2 * gap) // 2; y0 = 900
    for k, mm in enumerate(r["good"]):
        if k >= shown: break
        x = x0 + k * (bw + gap)
        d.rounded_rectangle([x, y0, x + bw, y0 + bh], radius=30, fill=(18, 18, 18), outline=acc, width=6)
        n = mlabel(mm).replace("월", ""); f = F(TITLE, 150)
        d.text((x + bw // 2, y0 + 130), n, font=f, fill=YEL, anchor="mm")
        d.text((x + bw // 2, y0 + 245), "월 · 내년" if "이듬해" in mm else "월", font=F(BODY, 48), fill=WHITE, anchor="mm")
    pill(d, 1282, "새 일 시작하기 좋은 달이에요", 48, (246, 240, 229), (18, 18, 18), outline=acc)
    return im
def scene_care(r, acc):
    im, d = layer()
    pill(d, Z["상단 라벨"][1], f"2027 {r['name']}", 44, (18, 18, 18), acc)
    care = " · ".join(mlabel(x) if "이듬해" not in x else "내년 1월" for x in r["care"])
    center(d, 640, [("아낄 달 ", WHITE), (care, YEL)], 96 if len(care) < 10 else 80)
    d.rounded_rectangle([SX0 + 10, 900, SX1 - 10, 1220], radius=36, fill=(18, 18, 18), outline=acc, width=5)
    center(d, 940, [(f"{r['m']}에 해 볼 것", acc)], 56, font=BODY)
    lines = list(r["todo"])                                   # 의미 단위 두 줄(손으로 끊음)
    for k, s in enumerate(lines): center(d, 1040 + k * 76, [(s, WHITE)], 56, font=BODY)
    pill(d, 1282, "아낄 달엔 큰 결정 한 번 더 보기", 48, (246, 240, 229), (18, 18, 18), outline=acc)
    return im
def scene_tag(r, acc):
    im, d = layer()
    pill(d, Z["상단 라벨"][1], f"2027 {r['name']}", 44, (18, 18, 18), acc)
    center(d, 640, [("주변 ", WHITE), (r["name"], YEL)], 120)
    center(d, 800, [("태그해 줘", WHITE)], 120)
    pill(d, 1282, "같은 띠라도 내 날 기운은 프로필 링크", 48, (246, 240, 229), (18, 18, 18), outline=acc)
    return im

def spec(r, sid, layout, hook, cta=""):
    return dict(id=f"rx-{r['slug']}-{sid}", 이름=f"{r['name']} {sid}", pal=r["pal"], bg=PAL[r["pal"]]["colors"][r["bgk"]], accent="#FFD600",
                **{"강조색 까닭": "표지 시안 cover1030(대표 10/31 승인)과 같은 노랑 강조 — y_black 판 옐로우, 어두운 바탕 대비"},
                hook=hook, kick="정미년 띠별 운세", cta=cta, 훅="상황 지목", layout=layout, method="M1 배경 이미지")

def gate(r, sid, layout, hook, lay_im, bg_rgb, cta=""):
    c = spec(r, sid, layout, hook, cta)
    G.before(c, CHN)
    flat = Image.new("RGB", (W, H), bg_rgb); flat.paste(lay_im, (0, 0), lay_im)
    fp = os.path.join(OUTD["frames"], f"{c['id']}_layer.png"); flat.save(fp)
    G.after(fp, {k: v for k, v in c.items() if k != "method"}, CHN)

def build(r):
    bg, acc = background(r); bgc = hx(PAL[r["pal"]]["colors"][r["bgk"]])
    L = {"cover": scene_cover(r, acc), "care": scene_care(r, acc), "tag": scene_tag(r, acc)}
    L.update({f"good{k}": scene_good(r, acc, k) for k in (1, 2, 3)})
    FX = {}                                              # 고정 요소 층(관문 글자 층에는 넣지 않음 — 표지 시안과 같은 방식)
    FX["cover"], d0 = layer(); url(d0, acc)
    FX["brand"], d1 = layer(); brand(d1, acc)
    def fixed(key): return FX["cover"] if key == "cover" else FX["brand"]
    # 관문(장면마다): before + 글자 층 after
    gate(r, "s1", "L2", [f"2027 {r['name']}", " ".join(r["hook"])], L["cover"], bgc, "내 띠 힘 쓸 달 3개 보기")
    gate(r, "s2", "L6", ["힘 쓸 달", " · ".join(r["good"])], L["good3"], bgc)
    gate(r, "s3", "L3", ["아낄 달", " ".join(r["todo"])], L["care"], bgc)
    gate(r, "s4", "L1", [f"주변 {r['name']}", "태그해 줘"], L["tag"], bgc)
    keyf = {}
    def frame(t):
        if t < T[1]:                                     # 표지: 첫 프레임부터 완성. 바탕만 아주 천천히 다가옴(1.0→1.04)
            z = 1 + 0.04 * t / T[1]; b = bg.resize((int(W * z), int(H * z))); ox, oy = (b.width - W) // 2, (b.height - H) // 2
            im = b.crop((ox, oy, ox + W, oy + H)); im.paste(L["cover"], (0, 0), L["cover"]); im.paste(FX["cover"], (0, 0), FX["cover"]); return im
        if t < T[2]:
            k = 1 + min(2, int((t - T[1]) / 0.45)); key = f"good{k}"
        elif t < T[3]: key = "care"
        else: key = "tag"
        if key not in keyf: im = bg.copy(); im.paste(L[key], (0, 0), L[key]); im.paste(fixed(key), (0, 0), fixed(key)); keyf[key] = im
        return keyf[key]
    out = os.path.join(OUTD["silent"], f"rx-{r['slug']}.mp4"); n = int(T[-1] * FPS)
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", "-preset", "medium", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    shots = {}
    for i in range(n):
        t = i / FPS; im = frame(t); p.stdin.write(im.tobytes())
        for nm, ts in (("s1", 0.0), ("s2", 4.0), ("s3", 6.0), ("s4", 9.0)):
            if i == int(ts * FPS): shots[nm] = im.copy()
    p.stdin.close(); assert p.wait() == 0
    for nm, im in shots.items():
        fp = os.path.join(OUTD["frames"], f"rx-{r['slug']}_{nm}.jpg"); im.save(fp, quality=90)
        h = FG.hits(fp)
        if h: raise SystemExit(f"[K-138] {r['slug']} {nm} 글자 묻힘 {h[:3]}")
    cover = os.path.join(HERE, f"rx-{r['slug']}_cover.jpg"); shots["s1"].save(cover, quality=90)
    return out

def sheet():
    """세 편 × 장면 4개 한 장(운영앱 카드용)."""
    s = 0.25; w, h = int(W * s), int(H * s); pad = 20
    sh = Image.new("RGB", (pad + 4 * (w + pad), pad + 3 * (h + pad)), (245, 242, 236))
    for j, r in enumerate(REELS):
        for k, nm in enumerate(("s1", "s2", "s3", "s4")):
            im = Image.open(os.path.join(OUTD["frames"], f"rx-{r['slug']}_{nm}.jpg")).resize((w, h)); sh.paste(im, (pad + k * (w + pad), pad + j * (h + pad)))
    p = os.path.join(HERE, "rx_sheet.jpg"); sh.save(p, quality=86); return p

if __name__ == "__main__":
    for r in REELS: print("만듦", build(r))
    print("한 장", sheet())
