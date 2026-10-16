"""네이버 대표 이미지 v3 시안 (10/16 대표: "호랑이띠·상강 섬네일 또 잘림, 피드 전체가 칙칙, 양산형 AI 콘텐츠 같다.
대표 이미지 톤과 맞춰 색조합 쓰라고 했잖아").
1) 잘림: 네이버 목록은 가로 판을 정사각으로 자를 때 얼굴 쪽으로 자른다(K-034). v2는 글자형만 얼굴 가운데로 바꾸고
   띠(ring)·큰 숫자(BIG)·칩(N)·달력(cal) 구도는 얼굴이 왼쪽/오른쪽 위에 그대로라 n64 호랑이띠가 또 잘렸다.
   v3는 모든 구도에서 얼굴을 가운데 위에 둔다.
2) 색: 오행 파스텔 + 어두운 남색·금색 판 → 색 조합 목록(sns-images assets/palettes/color_combos.json)의 맑은 판.
   오행은 그대로 뜻을 갖고 판만 바뀐다: 나무=그린&아이보리, 불=핑크&레드, 흙=옐로우&올리브(머스타드), 쇠=블랙&화이트, 물=블루&화이트.
   어두운 판은 6편에 1편꼴로만, 남색·금색 대신 보라&탠저린 크림(v_violet).
사용: python3 naver/cover_v3.py <출력폴더> n64 n53 ...   (시안 단계: naver/img 에는 쓰지 않는다)"""
import os, sys, json
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import thumb_sq as TQ
from thumb_sq import S, F, SER, SEMI, MED, BLK, badge, pill, lines_at, accent, fit, ring, logo, ailabel, q_center_safe
PAL = json.load(open(os.path.join(HERE, "..", "assets", "palettes", "color_combos.json"), encoding="utf-8"))["palettes"]
EL_PAL = {"나무": "g_ivory", "불": "p_red", "흙": "y_olive", "쇠": "k_white", "물": "b_white"}
DARK_PAL = "v_violet"
h2 = lambda c: tuple(int(c[i:i + 2], 16) for i in (1, 3, 5))
mix = lambda a, b, k: tuple(int(a[i] * (1 - k) + b[i] * k) for i in range(3))

class Ctx:
    """thumb_sq 그리기 함수가 쓰는 색 이름(bg·fg·acc·md·card·line·gray·pillfg·tint·ring_bg·dark)을 색 조합 판에서 만든다."""
    def __init__(s, pid):
        e = next(x for x in PAL if x["id"] == pid)
        if "pair" in e:
            d, l = (h2(c) for c in e["pair"])
            s.bg, s.fg, s.acc, s.card, s.line, s.gray = d, (255, 255, 255), l, mix(d, (255, 255, 255), .10), mix(d, (255, 255, 255), .22), mix((255, 255, 255), d, .3)
            s.md, s.pillfg, s.dark = l, d, True
        else:
            t = {k: h2(v) for k, v in e["theme"].items()}
            s.bg, s.fg, s.card, s.line, s.gray = t["bg"], t["ink"], t["card"], t["line"], t["sub"]
            s.acc = t.get("head", t["acc"]); s.dark = sum(t["bg"]) < 300
            s.md = t.get("hl", t["card"]) if not s.dark else t["card"]
            s.pillfg = t["bg"] if sum(s.acc) < 400 or s.dark else t["ink"]
        s.tint = mix(s.bg, s.acc, .06); s.ring_bg = s.card

def head(d, img, T, c, face, y_face=290, r=95):
    pill(d, c, 0, 80, T["kick"], center=True); badge(img, d, face, c, S // 2, y_face, r)
def big_c(d, img, T, c, face):
    """큰 숫자형, 얼굴 가운데: 라벨 → 얼굴 → 한 줄 후크 → 큰 숫자 → 부제 (모두 가운데 정렬)"""
    head(d, img, T, c, face, 280, 88)
    hk = T["hook"]; s1 = fit(d, hk, 864, 72, 50, SEMI); y = 395
    for l in hk: d.text((S // 2, y), l, font=F(SEMI, s1), fill=c.fg, anchor="ma"); y += int(s1 * 1.25)
    bs = fit(d, [T["big"]], 860, 340, 140, BLK)
    while y + 6 + int(bs * 1.05) + 70 > 950 and bs > 140: bs -= 8
    d.text((S // 2, y + 6), T["big"], font=F(BLK, bs), fill=c.acc, anchor="ma")
    d.text((S // 2, y + 6 + int(bs * 1.05) + 10), T["sub"], font=F(SEMI, 44), fill=c.fg, anchor="ma")
def n_c(d, img, T, c, face):
    head(d, img, T, c, face, 280, 88)
    rows = (len(T["items"]) + 2) // 3; s = fit(d, T["hook"], 864, 120)
    while s > 70 and 400 + int(s * 1.2) * len(T["hook"]) + 100 + rows * 104 > 950: s -= 4
    y = lines_at(d, T["hook"], 0, 400, s, c.fg, center=True)
    d.text((S // 2, y + 14), T["sub"], font=F(SEMI, 46), fill=c.acc, anchor="ma")
    it = T["items"]; cw, ch, g = 270, 86, 18; y0 = y + 100; per = 3; rows = (len(it) + per - 1) // per
    for r_ in range(rows):
        row = it[r_ * per:(r_ + 1) * per]; x0 = (S - (len(row) * cw + (len(row) - 1) * g)) // 2; yy = y0 + r_ * (ch + g)
        for i, t in enumerate(row):
            x = x0 + i * (cw + g); d.rounded_rectangle([x, yy, x + cw, yy + ch], 24, fill=c.card, outline=c.line, width=4)
            d.text((x + cw // 2, yy + ch // 2), t, font=F(SEMI, 48), fill=c.fg, anchor="mm")
def trio_c(d, img, T, c, face):
    head(d, img, T, c, face, 280, 88)
    s = fit(d, T["hook"], 864, 120); y = lines_at(d, T["hook"], 0, 400, s, c.fg, center=True)
    n = len(T["glyph"]); r = 84; g = 40; x0 = (S - (n * 2 * r + (n - 1) * g)) // 2 + r
    for i, ch in enumerate(T["glyph"]): ring(d, c, x0 + i * (2 * r + g), y + 110, r, ch, 104)
    d.text((S // 2, y + 230), T["sub"], font=F(SEMI, 46), fill=c.acc, anchor="ma")
def cal_c(d, img, T, c, face):
    head(d, img, T, c, face, 250, 74)
    s = fit(d, T["hook"], 864, 84, 60); y = lines_at(d, T["hook"], 0, 350, s, c.fg, center=True)
    hot = T["hot"]; cw, chh, g = 112, 58, 10; x0 = (S - (7 * cw + 6 * g)) // 2; y0 = y + 24
    for k in range(T.get("days", 31)):
        day = k + 1; pos = k + T.get("off", 4); x = x0 + (pos % 7) * (cw + g); yy = y0 + (pos // 7) * (chh + g); on = day in hot
        d.rounded_rectangle([x, yy, x + cw, yy + chh], 14, fill=c.acc if on else c.card, outline=c.acc if on else c.line, width=3)
        d.text((x + cw // 2, yy + chh // 2), str(day), font=F(SEMI, 32), fill=c.pillfg if on else c.fg, anchor="mm")
DRAW = {"QL": q_center_safe, "QC": q_center_safe, "QCS": q_center_safe, "QK": q_center_safe, "CH": q_center_safe, "ring": q_center_safe, "gua": q_center_safe,
        "BIG": big_c, "N": n_c, "trio": trio_c, "cal": cal_c}

def render(pid, T, out, pal=None, wide=True):
    c = Ctx(pal or EL_PAL[T["el"]]); face = T.get("face") or TQ.FACES[sum(map(ord, pid)) % len(TQ.FACES)]
    if T["d"] in ("ring",) and "glyph" in T and "sub" not in T: T = dict(T, sub="")
    img = Image.new("RGB", (S, S), c.bg); d = ImageDraw.Draw(img); DRAW[T["d"]](d, img, T, c, face); logo(d, c); ailabel(d, c)
    sq = img.resize((720, 720), Image.LANCZOS)
    if not wide: sq.save(out, quality=94); return out
    can = Image.new("RGB", (1200, 720), c.bg); can.paste(sq, (240, 0)); can.save(out, quality=94); return out
