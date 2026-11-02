"""일간 성격 3회차 릴스 8편 — 갑·을·병·정·무·기·경·신 (11/18~11/27 평일 17:00 후보, 편성표 content/plan_sns_1115_1128.json).
CT 11/1 07:20 항목(대표 "권장안대로", 11/15~28 같은 양 채우기) · ① 자동 11/2 11:45.

왜 이렇게 만들었나
  첫 화면  cover1030 표지 틀(대표 10/31 승인) — 화면 전체 그림(별밤 + 천간 한자 + 열 칸 눈금) · 큰 글자 2줄 · 강조 한 줄 노랑.
           11/1 릴스 실험에서 이 틀을 쓴 뱀띠 2027만 3초 시청률 34.5%(나머지 3~13%). 위 고정 줄은 표지 장면에서 뺀다.
  첫 줄    여덟 편 모두 '상황·행동'(1회차 1·2위가 행동형, 꼴찌 둘이 형용사형). 2회차의 행동/형용사 시험 결과는
           11/17에 끝나서 아직 없다 — 그 결과로 이어 간다는 편성표 문장은 틀렸다(그래서 1회차 근거만 썼다).
           체계 이름(사주·일간·갑목)은 첫 줄에 넣지 않는다(K-102). 물음표 훅 아님(K-107).
  내용     2회차 문장과 겹치지 않게 새로 썼다(첫 줄·풀이·해 볼 것). 일반적인 십간 풀이를 입말로, 단정 없이.
  소리     clip_v3_music.py 하나(K-070). 11/5부터 음악 라이브러리 자동.
관문: 장면마다 card_gate.before(reel) · 글자 층 after(reel) · 완성 프레임 faint_gate(K-138) · after_video(첫 프레임).
결과: silent/ilgan3-<id>.mp4 → 음악판
  ZS_SRC=2026-ilgan3/silent ZS_OUT=2026-ilgan3/music ZS_PRE=ilgan3- python3 pipeline/clip_v3_music.py
실행: python3 2026-ilgan3/build.py [id …]"""
import os, sys, json, math, random, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "pipeline"))
import channel_specs as CS, card_gate as G, fonts_kit as FK, faint_gate as FG, copy_rules as CR

CHN = "reel"; C = CS.CH[CHN]; W, H = C["w"], C["h"]
SX0, SY0, SX1, SY1 = C["safe"]; CX = (SX0 + SX1) // 2
Z = {z[0]: z[1:5] for z in C["zones"]}
PAL = {p["id"]: p for p in json.load(open(os.path.join(ROOT, "assets/palettes/color_combos.json"), encoding="utf-8"))["palettes"]}
FPS = 30; T = [0.0, 1.8, 5.6, 9.0, 11.0]
OUTD = {k: os.path.join(HERE, k) for k in ("silent", "frames")}
for p in OUTD.values(): os.makedirs(p, exist_ok=True)
def F(k, s): return ImageFont.truetype(FK.P[k], s)
TITLE, BODY, HANJA = "gm_bold", "pr_xb", FK.P["serif"]
YEL = (255, 214, 0); WHITE = (255, 255, 255); INK = (18, 18, 18); CREAM = (246, 240, 229)
def hx(h): h = h.lstrip("#"); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
def tw(d, s, f): b = d.textbbox((0, 0), s, font=f); return b[2] - b[0]

GAN = "甲乙丙丁戊己庚辛壬癸"
# id, 이름, 천간 순번, 판, 바탕 키, 강조 키, 첫 줄(2줄), 둘째 줄(알약), 풀이 3줄(기운 · 까닭 · 해 볼 것)
REELS = [
 dict(id="gab", name="갑", i=0, pal="dg_gold", bgk="딥그린", acck="골드", hook=("시작은 늘", "내가 먼저 해요"), sub="누가 안 하면 결국 내가 해요",
      gi="곧게 뻗는 큰 나무 기운이에요", why=("앞장서는 만큼", "혼자 지칠 때가 많아요"), todo=("쉬는 시간을", "일정에 먼저 넣어 보세요"), tag="#갑목"),
 dict(id="eul", name="을", i=1, pal="v_emerald", bgk="진한 색", acck="옅은 색", hook=("싫다는 말 대신", "다른 길로 돌아가요"), sub="부딪히기보다 결국 해내는 쪽이에요",
      gi="어디든 뻗어 가는 덩굴 기운이에요", why=("맞춰 주다가", "내 뜻을 놓칠 때가 있어요"), todo=("원하는 것 하나를", "먼저 말해 보세요"), tag="#을목"),
 dict(id="byeong", name="병", i=2, pal="m_young", bgk="미드나잇 블루", acck="코랄", hook=("들어서기만 하면", "분위기가 바뀌어요"), sub="조용한 자리가 제일 어색해요",
      gi="한낮을 비추는 해 기운이에요", why=("밝게 비추느라", "내 기분은 뒤로 미뤄요"), todo=("혼자 쉬는 30분을", "따로 잡아 보세요"), tag="#병화"),
 dict(id="jeong", name="정", i=3, pal="v_violet", bgk="진한 색", acck="옅은 색", hook=("남이 흘린 말을", "다 기억해 둬요"), sub="작은 걸 챙기는 데 진심이에요",
      gi="밤을 밝히는 촛불 기운이에요", why=("챙긴 만큼 안 돌아오면", "서운해지기도 해요"), todo=("오늘 나를 챙긴 일", "하나를 적어 보세요"), tag="#정화"),
 dict(id="mu", name="무", i=4, pal="v_choco", bgk="진한 색", acck="옅은 색", hook=("다들 흔들릴 때", "제일 늦게 움직여요"), sub="급할수록 더 차분해져요",
      gi="넓고 높은 산 기운이에요", why=("버티는 게 익숙해서", "힘든 티를 안 내요"), todo=("힘든 것 하나를", "말로 꺼내 보세요"), tag="#무토"),
 dict(id="gi", name="기", i=5, pal="k_gold", bgk="블랙", acck="골드", hook=("모임이 끝나면", "뒷정리는 내 차지예요"), sub="티 안 나는 일을 먼저 챙겨요",
      gi="씨앗을 키우는 밭 기운이에요", why=("챙기는 게 당연해지면", "금방 지쳐요"), todo=("정리 하나를", "남에게 부탁해 보세요"), tag="#기토"),
 dict(id="gyeong", name="경", i=6, pal="w_ink", bgk="딥 인디고", acck="아이보리", hook=("칭찬도", "빈말로는 못 해요"), sub="진짜일 때만 말하는 쪽이에요",
      gi="단단한 바위와 쇠 기운이에요", why=("정직한 말이", "차갑게 닿을 때가 있어요"), todo=("말하기 전에", "좋은 점 하나 먼저요"), tag="#경금"),
 dict(id="sin", name="신", i=7, pal="w_navy_butter", bgk="네이비", acck="소프트 버터", hook=("마음에 안 들면", "처음부터 다시 해요"), sub="대충 끝내는 게 제일 불편해요",
      gi="빛나게 다듬은 보석 기운이에요", why=("다듬느라", "끝내는 날이 늦어지기도 해요"), todo=("80점에서", "한 번 마쳐 보세요"), tag="#신금"),
]
# 2회차 문장과 겹치지 않는지(첫 줄 그대로 쓰지 않기)
OLD = json.load(open(os.path.join(ROOT, "2026-ilgan2/cards.json"), encoding="utf-8"))["cards"]
OLD_HOOK = {" ".join(c["hook"]) for c in OLD}
for r in REELS:
    assert GAN[r["i"]] and " ".join(r["hook"]) not in OLD_HOOK, r["id"]
    bad = CR.첫줄검사(" ".join(r["hook"]))
    assert not bad, (r["id"], bad)                                # K-102 첫 줄 금지(체계 이름 등)
    assert not r["hook"][1].endswith("?")                          # K-107

# ── 바탕(cover1030 방식: 별밤 + 천간 한자 + 열 칸 눈금) ─────────────
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
    p = PAL[r["pal"]]["colors"]; base = hx(p[r["bgk"]]); acc = hx(p[r["acck"]])
    ga = r.get("glyph", 22 if sum(acc) < 600 else 10)
    top = tuple(min(255, int(c + 22)) for c in base)
    im = grad(top, base); stars(im, 700, 300 + r["i"])
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.text((W // 2, 980), GAN[r["i"]], font=ImageFont.truetype(HANJA, 1000), fill=acc + (ga,), anchor="mm")
    for rr, a in ((560, 70), (640, 40)): d.ellipse([W // 2 - rr, 980 - rr, W // 2 + rr, 980 + rr], outline=acc + (a,), width=3)
    for k in range(10):
        t = math.radians(k * 36 - 90); x, y = W // 2 + 600 * math.cos(t), 980 + 600 * math.sin(t)
        d.ellipse([x - 9, y - 9, x + 9, y + 9], fill=acc + (220 if k == r["i"] else 70,))
    im = Image.alpha_composite(im.convert("RGBA"), lay.filter(ImageFilter.GaussianBlur(1))).convert("RGB")
    return scrim(im, 560, 1330, 130), acc

# ── 글자 층 ───────────────────────────────────────────────────────
def center(d, y, parts, size, font=TITLE):
    f = F(font, size); x = CX - sum(tw(d, s, f) for s, _ in parts) // 2
    for s, col in parts: d.text((x, y), s, font=f, fill=col); x += tw(d, s, f)
def fit(d, lines, size, font=TITLE, lo=60):
    while max(tw(d, s, F(font, size)) for s in lines) > SX1 - SX0 - 40: size -= 2
    assert size >= lo, (lines, size); return size
def pill(d, y, text, size, fg, bg, pad=(34, 16), outline=None):
    f = F(BODY, size)
    while tw(d, text, f) + pad[0] * 2 > SX1 - SX0: size -= 2; f = F(BODY, size)
    w = tw(d, text, f); b = d.textbbox((0, 0), text, font=f); h = b[3] - b[1]
    d.rounded_rectangle([CX - w // 2 - pad[0], y, CX + w // 2 + pad[0], y + h + pad[1] * 2], radius=(h + pad[1] * 2) // 2,
                        fill=bg, outline=outline, width=4 if outline else 0)
    d.text((CX - w // 2, y + pad[1] - b[1]), text, font=f, fill=fg); return y + h + pad[1] * 2
def brand(d, acc):
    z = Z["상단 고정"]; f1, f = F(TITLE, 40), F(BODY, 34); s = "  ·  동서양 6개 운명학 교차분석"; x = (z[0] + z[2]) / 2 - (tw(d, "자오선", f1) + tw(d, s, f)) / 2   # 11/2 대표 K-166 가운데 한 줄
    d.text((x, z[1]), "자오선", font=f1, fill=WHITE); d.text((x + tw(d, "자오선", f1), z[1] + 4), s, font=f, fill=(225, 225, 225))
    url(d, acc)
def url(d, acc):
    f = F(TITLE, 36); z = Z["하단 고정"]; d.text((z[2] - tw(d, "zaoseon.com", f), z[1]), "zaoseon.com", font=f, fill=acc)
def layer(): im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); return im, ImageDraw.Draw(im)
def label(r): return f"태어난 날 첫 글자 {r['name']}"   # 본문 글꼴엔 한자가 없어 알약 글자에 한자를 넣지 않는다(한자는 바탕 그림에만)

def scene_cover(r, acc):
    im, d = layer()
    pill(d, Z["상단 라벨"][1], label(r), 44, INK, acc)
    s = fit(d, r["hook"], 116)
    center(d, 640, [(r["hook"][0], WHITE)], s)
    center(d, 640 + int(s * 1.3), [(r["hook"][1], YEL)], s)
    pill(d, 980, r["sub"], 52, INK, CREAM, pad=(40, 18))
    pill(d, 1282, "맞으면 끝까지 보기", 48, CREAM, INK, outline=acc)
    return im, s
def scene_why(r, acc):
    im, d = layer()
    pill(d, Z["상단 라벨"][1], label(r), 44, INK, acc)
    lines = [r["gi"][:r["gi"].rfind(" ")], r["gi"][r["gi"].rfind(" ") + 1:]]   # '곧게 뻗는 큰 나무' / '기운이에요'
    s = fit(d, lines, 96)
    center(d, 640, [(lines[0], WHITE)], s); center(d, 640 + int(s * 1.3), [(lines[1], WHITE)], s)
    d.rounded_rectangle([SX0 + 10, 960, SX1 - 10, 1210], radius=36, fill=INK, outline=acc, width=5)
    for k, ln in enumerate(r["why"]): center(d, 1000 + k * 84, [(ln, CREAM)], 54, font=BODY)   # 의미 단위 두 줄(손으로 끊음)
    pill(d, 1282, "내 첫 글자는 생년월일로 정해져요", 46, CREAM, INK, outline=acc)
    return im
def scene_todo(r, acc):
    im, d = layer()
    pill(d, Z["상단 라벨"][1], label(r), 44, INK, acc)
    center(d, 640, [("오늘 해 볼 것", YEL)], 108)
    d.rounded_rectangle([SX0 + 10, 900, SX1 - 10, 1210], radius=36, fill=INK, outline=acc, width=5)
    s = fit(d, r["todo"], 66, font=BODY)
    for k, ln in enumerate(r["todo"]): center(d, 975 + k * int(s * 1.45), [(ln, WHITE)], s, font=BODY)
    pill(d, 1282, "떠오르는 사람에게 보내 주기", 48, CREAM, INK, outline=acc)
    return im
def scene_end(r, acc):
    im, d = layer()
    pill(d, Z["상단 라벨"][1], label(r), 44, INK, acc)
    center(d, 640, [("내 첫 글자는", WHITE)], 104)
    center(d, 640 + 135, [("프로필 링크에서 1초", YEL)], fit(d, ["프로필 링크에서 1초"], 104))
    pill(d, 1282, "생년월일만 넣으면 바로 나와요", 48, CREAM, INK, outline=acc)
    return im

def spec(r, sid, layout, hook, cta=""):
    return dict(id=f"ilgan3-{r['id']}-{sid}", 이름=f"일간 3회차 {r['name']} {sid}", pal=r["pal"], bg=PAL[r["pal"]]["colors"][r["bgk"]], accent="#FFD600",
                **{"강조색 까닭": "표지 시안 cover1030(대표 10/31 승인)과 같은 노랑 강조 — 어두운 바탕 대비"},
                hook=hook, kick=label(r), cta=cta, 훅="상황 지목", layout=layout, method="M1 배경 이미지")
def gate(r, sid, layout, hook, lay_im, bg_rgb, cta=""):
    c = spec(r, sid, layout, hook, cta)
    G.before(c, CHN)
    flat = Image.new("RGB", (W, H), bg_rgb); flat.paste(lay_im, (0, 0), lay_im)
    fp = os.path.join(OUTD["frames"], f"{c['id']}_layer.png"); flat.save(fp)
    G.after(fp, {k: v for k, v in c.items() if k != "method"}, CHN)

def build(r):
    bg, acc = background(r); bgc = hx(PAL[r["pal"]]["colors"][r["bgk"]])
    cov, _ = scene_cover(r, acc)
    L = {"cover": cov, "why": scene_why(r, acc), "todo": scene_todo(r, acc), "end": scene_end(r, acc)}
    FX = {}; FX["cover"], d0 = layer(); url(d0, acc); FX["brand"], d1 = layer(); brand(d1, acc)
    gate(r, "s1", "L2", list(r["hook"]), L["cover"], bgc, "맞으면 끝까지 보기")
    gate(r, "s2", "L3", [r["gi"], " ".join(r["why"])], L["why"], bgc)
    gate(r, "s3", "L3", ["오늘 해 볼 것", " ".join(r["todo"])], L["todo"], bgc)
    gate(r, "s4", "L1", ["내 첫 글자는", "프로필 링크에서 1초"], L["end"], bgc)
    keyf = {}
    def frame(t):
        if t < T[1]:
            z = 1 + 0.04 * t / T[1]; b = bg.resize((int(W * z), int(H * z))); ox, oy = (b.width - W) // 2, (b.height - H) // 2
            im = b.crop((ox, oy, ox + W, oy + H)); im.paste(L["cover"], (0, 0), L["cover"]); im.paste(FX["cover"], (0, 0), FX["cover"]); return im
        key = "why" if t < T[2] else "todo" if t < T[3] else "end"
        if key not in keyf: im = bg.copy(); im.paste(L[key], (0, 0), L[key]); im.paste(FX["brand"], (0, 0), FX["brand"]); keyf[key] = im
        return keyf[key]
    out = os.path.join(OUTD["silent"], f"ilgan3-{r['id']}.mp4"); n = int(T[-1] * FPS)
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", "-preset", "medium", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    shots = {}
    for i in range(n):
        t = i / FPS; im = frame(t); p.stdin.write(im.tobytes())
        for nm, ts in (("s1", 0.0), ("s2", 3.0), ("s3", 7.0), ("s4", 10.0)):
            if i == int(ts * FPS): shots[nm] = im.copy()
    p.stdin.close(); assert p.wait() == 0
    for nm, im in shots.items():
        fp = os.path.join(OUTD["frames"], f"ilgan3-{r['id']}_{nm}.jpg"); im.save(fp, quality=90)
        h = FG.hits(fp)
        if h: raise SystemExit(f"[K-138] {r['id']} {nm} 글자 묻힘 {h[:3]}")
    shots["s1"].save(os.path.join(HERE, f"ilgan3-{r['id']}_cover.jpg"), quality=90)
    G.after_video(out)
    return out

def sheet(rs):
    s = 0.2; w, h = int(W * s), int(H * s); pad = 16
    sh = Image.new("RGB", (pad + 4 * (w + pad), pad + len(rs) * (h + pad)), (245, 242, 236))
    for j, r in enumerate(rs):
        for k, nm in enumerate(("s1", "s2", "s3", "s4")):
            im = Image.open(os.path.join(OUTD["frames"], f"ilgan3-{r['id']}_{nm}.jpg")).resize((w, h)); sh.paste(im, (pad + k * (w + pad), pad + j * (h + pad)))
    p = os.path.join(HERE, "ilgan3_sheet.jpg"); sh.save(p, quality=84); return p

if __name__ == "__main__":
    want = sys.argv[1:]; rs = [r for r in REELS if not want or r["id"] in want]
    for r in rs: print("만듦", build(r), flush=True)
    print("한 장", sheet(rs))
