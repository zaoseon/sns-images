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
# v3b(10/16 대표 "칙칙한 베이지, 탁한 블루, 어중간한 그린 — 캡처해 준 조합을 써라"): 캡처·영상의 선명한 두 색 조합으로
EL_PAL_B = {"나무": "v_emerald", "물": "v_royal", "흙": "v_navy_inv", "불": "y_pink", "쇠": "k_white"}
DARK_PAL = "v_violet"
h2 = lambda c: tuple(int(c[i:i + 2], 16) for i in (1, 3, 5))
mix = lambda a, b, k: tuple(int(a[i] * (1 - k) + b[i] * k) for i in range(3))

class Ctx:
    """thumb_sq 그리기 함수가 쓰는 색 이름(bg·fg·acc·md·card·line·gray·pillfg·tint·ring_bg·dark)을 색 조합 판에서 만든다."""
    def __init__(s, pid):
        inv = pid.endswith("_inv"); e = next(x for x in PAL if x["id"] == (pid[:-4] if inv else pid))
        if "pair" in e and inv:      # 옅은 색 바탕 + 진한 색 글자·배지
            d, l = (h2(c) for c in e["pair"])
            s.bg, s.fg, s.acc, s.card, s.line, s.gray = l, d, d, (255, 255, 255), mix(l, d, .18), mix(d, l, .35)
            s.md, s.pillfg, s.dark = (255, 255, 255), l, False
        elif "pair" in e:
            d, l = (h2(c) for c in e["pair"])
            s.bg, s.fg, s.acc, s.card, s.line, s.gray = d, (255, 255, 255), l, mix(d, (255, 255, 255), .10), mix(d, (255, 255, 255), .22), mix((255, 255, 255), d, .3)
            s.md, s.pillfg, s.dark = l, d, True
        else:
            t = {k: h2(v) for k, v in e["theme"].items()}
            s.bg, s.fg, s.card, s.line, s.gray = t["bg"], t["ink"], t["card"], t["line"], t["sub"]
            s.acc = t.get("head", t["acc"]); s.dark = sum(t["bg"]) < 300
            s.md = t["card"] if sum(t["card"]) < 760 else mix(t["bg"], (255, 255, 255), .5)   # 얼굴 원 바탕은 판의 옅은 색 하나로(10/16 "배지 배경색 제각각")
            s.pillfg = t["bg"] if sum(s.acc) < 400 or s.dark else t["ink"]
        s.tint = mix(s.bg, s.acc, .045); s.ring_bg = s.card

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
    rc = c if sum(c.acc) < 700 else type("C", (), dict(vars(c), acc=c.fg))   # 강조색이 흰색인 판(핑크)에서는 고리를 글자색으로
    for i, ch in enumerate(T["glyph"]): ring(d, rc, x0 + i * (2 * r + g), y + 110, r, ch, 104)
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

# v3c(10/16 대표 "정월이 표지에 꼭 나오지 않아도 된다. 동그란 배지 배경색이 제각각이라 지저분하고, 글자도 정월 얼굴도 잘 안 보인다"):
# 얼굴·배지·한자 워터마크를 빼고 글자만 크게. 굵은 고딕(Pretendard ExtraBold), 가운데 정렬 → 정사각으로 어디를 잘라도 글자가 남는다.
# 캐릭터가 없으니 AI 표기도 넣지 않는다(캐릭터 이미지에만 표기).
XB = TQ.FD + "PRETENDARD-EXTRABOLD.OTF"
def kick(d, c, y=110):
    f = F(SEMI, 44); t = T_KICK[0]; w = d.textlength(t, font=f) + 64; x = (S - w) / 2
    d.rounded_rectangle([x, y, x + w, y + 82], 41, fill=c.acc); d.text((S / 2, y + 41), t, font=f, fill=c.pillfg, anchor="mm")
T_KICK = [""]
def hook_block(d, c, lines, y_top, y_bot, maxsize=150):
    s = fit(d, lines, 900, maxsize, 70, XB); lh = int(s * 1.22); h = lh * len(lines)
    y = y_top + max(0, (y_bot - y_top - h) // 2)
    for l in lines: d.text((S // 2, y), l, font=F(XB, s), fill=c.fg, anchor="ma"); y += lh
    return y
def nf_text(d, img, T, c, face):
    kick(d, c); y = hook_block(d, c, T["hook"], 250, 760)
    d.line([(S // 2 - 70, y + 24), (S // 2 + 70, y + 24)], fill=c.acc, width=10)
    d.text((S // 2, y + 62), T.get("sub", ""), font=F(SEMI, 54), fill=c.acc if not c.dark else c.fg, anchor="ma")
def nf_ring(d, img, T, c, face):
    kick(d, c); g = T.get("glyph", ""); r = 112
    d.ellipse([S // 2 - r, 245, S // 2 + r, 245 + 2 * r], fill=c.acc); d.text((S // 2, 245 + r - 4), g, font=F(SER, 140), fill=c.pillfg, anchor="mm")
    y = hook_block(d, c, T["hook"], 500, 800, 128)
    d.text((S // 2, y + 30), T.get("sub", ""), font=F(SEMI, 52), fill=c.acc if not c.dark else c.fg, anchor="ma")
def nf_big(d, img, T, c, face):
    kick(d, c); hk = T["hook"]; s1 = fit(d, hk, 900, 84, 56, XB); y = 250
    for l in hk: d.text((S // 2, y), l, font=F(XB, s1), fill=c.fg, anchor="ma"); y += int(s1 * 1.22)
    bs = fit(d, [T["big"]], 820, 360, 160, BLK)
    while y + 10 + int(bs * 1.05) + 80 > 960 and bs > 160: bs -= 8
    d.text((S // 2, y + 10), T["big"], font=F(BLK, bs), fill=c.acc, anchor="ma")
    d.text((S // 2, y + 10 + int(bs * 1.05) + 14), T["sub"], font=F(SEMI, 50), fill=c.fg, anchor="ma")
def nf_n(d, img, T, c, face):
    kick(d, c); rows = (len(T["items"]) + 2) // 3
    y = hook_block(d, c, T["hook"], 240, 900 - rows * 112 - 90, 140)
    d.text((S // 2, y + 10), T["sub"], font=F(SEMI, 50), fill=c.acc if not c.dark else c.fg, anchor="ma")
    it = T["items"]; cw, ch, g = 280, 92, 20; y0 = y + 96
    for r_ in range(rows):
        row = it[r_ * 3:(r_ + 1) * 3]; x0 = (S - (len(row) * cw + (len(row) - 1) * g)) // 2; yy = y0 + r_ * (ch + g)
        for i, t in enumerate(row):
            x = x0 + i * (cw + g); d.rounded_rectangle([x, yy, x + cw, yy + ch], 24, fill=c.card, outline=c.line, width=4)
            d.text((x + cw // 2, yy + ch // 2), t, font=F(SEMI, 50), fill=c.fg, anchor="mm")
def nf_trio(d, img, T, c, face):
    kick(d, c); y = hook_block(d, c, T["hook"], 240, 560, 140)
    n = len(T["glyph"]); r = 96; g = 44; x0 = (S - (n * 2 * r + (n - 1) * g)) // 2 + r
    for i, ch in enumerate(T["glyph"]):
        cx = x0 + i * (2 * r + g); d.ellipse([cx - r, y + 40, cx + r, y + 40 + 2 * r], fill=c.acc); d.text((cx, y + 40 + r - 4), ch, font=F(SER, 116), fill=c.pillfg, anchor="mm")
    d.text((S // 2, y + 40 + 2 * r + 40), T["sub"], font=F(SEMI, 50), fill=c.acc if not c.dark else c.fg, anchor="ma")
def nf_cal(d, img, T, c, face):
    kick(d, c); y = hook_block(d, c, T["hook"], 230, 430, 100)
    hot = T["hot"]; cw, chh, g = 116, 66, 10; x0 = (S - (7 * cw + 6 * g)) // 2; y0 = y + 30
    for k in range(T.get("days", 31)):
        day = k + 1; pos = k + T.get("off", 4); x = x0 + (pos % 7) * (cw + g); yy = y0 + (pos // 7) * (chh + g); on = day in hot
        d.rounded_rectangle([x, yy, x + cw, yy + chh], 14, fill=c.acc if on else c.card, outline=c.acc if on else c.line, width=3)
        d.text((x + cw // 2, yy + chh // 2), str(day), font=F(SEMI, 34), fill=c.pillfg if on else c.fg, anchor="mm")
DRAW_NF = {"QL": nf_text, "QC": nf_text, "QCS": nf_text, "QK": nf_text, "CH": nf_text, "gua": nf_text, "ring": nf_ring,
           "BIG": nf_big, "N": nf_n, "trio": nf_trio, "cal": nf_cal}
def logo_nf(d, c): d.text((S // 2, S - 82), "子午線 자오선", font=F(SER, 40), fill=c.fg if c.dark else c.acc, anchor="mm")

def pick(order, T, every_dark=6):
    """발행 순서대로 판을 정한다: 오행 판(EL_PAL_B), 두 색 조합 판은 같은 오행이 이어 나오면 반전(_inv)을 번갈아, 6편에 1편 어두운 보라 판."""
    seen = {}; out = {}
    for i, k in enumerate(order):
        el = T[k]["el"]; base = EL_PAL_B[el]; n = seen.get(el, 0); seen[el] = n + 1
        if i % every_dark == every_dark - 1: out[k] = DARK_PAL; continue
        is_pair = any(x["id"] == base.replace("_inv", "") and "pair" in x for x in PAL)
        out[k] = (base[:-4] if base.endswith("_inv") else base + "_inv") if is_pair and n % 2 == 1 else base
    return out
def render(pid, T, out, pal=None, wide=True, face_on=False):
    c = Ctx(pal or EL_PAL[T["el"]]); face = T.get("face") or TQ.FACES[sum(map(ord, pid)) % len(TQ.FACES)]
    if T["d"] in ("ring",) and "glyph" in T and "sub" not in T: T = dict(T, sub="")
    img = Image.new("RGB", (S, S), c.bg); d = ImageDraw.Draw(img)
    if face_on: DRAW[T["d"]](d, img, T, c, face); logo(d, c); ailabel(d, c)
    else: T_KICK[0] = T["kick"]; DRAW_NF[T["d"]](d, img, T, c, face); logo_nf(d, c)
    sq = img.resize((720, 720), Image.LANCZOS)
    if not wide: sq.save(out, quality=94); return out
    can = Image.new("RGB", (1200, 720), c.bg); can.paste(sq, (240, 0)); can.save(out, quality=94); return out


def all_configs():
    """모든 글의 표지 설정: n01~n46(thumb_sq.T), art(...) 호출(build_naver_47_52·53_63·70·71·72_74·75_79), mk(...) 호출(build_naver_64_69 띠)."""
    import ast, regen_badges as R
    R.load_47_63(); T = dict(TQ.T)
    for fn in ("build_naver_70.py", "build_naver_71.py", "build_naver_72_74.py", "build_naver_75_79.py"):
        tree = ast.parse(open(os.path.join(HERE, fn), encoding="utf-8").read())
        for n in ast.walk(tree):
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "art" and len(n.args) >= 7:
                try:
                    no, face, el, cfg = (ast.literal_eval(n.args[i]) for i in (0, 3, 4)), None, None, None
                except Exception: pass
                vals = []
                for i in (0, 3, 4, 6):
                    try: vals.append(eval(compile(ast.Expression(n.args[i]), "x", "eval"), dict(vars(TQ))))
                    except Exception: vals.append(None)
                if vals[3]: t = dict(vals[3]); t.update(el=vals[2], face=vals[1]); T[f"n{vals[0]}"] = t
    tree = ast.parse(open(os.path.join(HERE, "build_naver_64_69.py"), encoding="utf-8").read())
    for n in ast.walk(tree):
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "mk" and len(n.args) >= 12:
            try:
                no, name, glyph, el, face, hook = (ast.literal_eval(n.args[i]) for i in (0, 2, 3, 4, 5, 11))
                T[f"n{no}"] = dict(d="ring", el=el, face=face, kick=f"2027 {name}", hook=hook, sub="힘 쓸 달 · 아낄 달", glyph=glyph)
            except Exception: pass
    return T
