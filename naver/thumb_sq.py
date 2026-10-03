"""네이버 블로그 대표 이미지(정사각) 생성기. 10/3 대표 결정: 네이버 홈·목록이 정사각 중앙을 보여 주므로 1:1, 글자는 중앙, 정월은 작은 원형 배지.
규칙: 밝은 바탕만, 정월 얼굴 밝게, AI 표시 우하단 연회색, 이미지 문구는 글 제목과 다른 말, v5_halfup 원본 금지(v5_halfup_v2만).
사용: python3 thumb_sq.py  -> img/sq_<id>.jpg (800x800) 전부 생성 / render(pid, path)"""
import os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__))
FD = os.path.join(HERE, "..", "pipeline", "fonts") + "/"
SER, SEMI, MED = FD + "serif.otf", FD + "PRETENDARD-SEMIBOLD.OTF", FD + "PRETENDARD-MEDIUM.OTF"
CH = os.path.join(HERE, "..", "characters", "cut") + "/"
S = 1080
EL = {"불": ((251, 231, 222), (196, 74, 52), (238, 170, 150)), "물": ((222, 232, 244), (36, 62, 112), (150, 178, 214)),
      "흙": ((244, 236, 220), (150, 108, 50), (222, 200, 160)), "나무": ((226, 240, 226), (54, 110, 70), (160, 200, 165)),
      "쇠": ((246, 243, 236), (140, 112, 50), (215, 200, 160))}
INK = (38, 32, 28); GRAY = (150, 144, 136); WHITE = (255, 255, 255)
_f = {}
def F(p, s):
    if (p, s) not in _f: _f[(p, s)] = ImageFont.truetype(p, s)
    return _f[(p, s)]
def fit(d, lines, maxw, start, lo=96, path=SER):
    s = start
    while s > lo and max(d.textlength(l, font=F(path, s)) for l in lines) > maxw: s -= 4
    return s
def badge(img, d, face, bg, md, cx, cy, r):
    face = "v5_halfup_v2" if face == "v5_halfup" else face
    ch = Image.open(CH + face + ".png").convert("RGBA"); ch = ch.crop(ch.getbbox())
    a = ch.split()[3].filter(ImageFilter.MinFilter(5)).filter(ImageFilter.GaussianBlur(1)); ch.putalpha(a)
    w, h = ch.size; side = int(h * 0.44); x0 = max(0, min(w - side, int(w * 0.5 - side / 2)))
    head = ch.crop((x0, 0, x0 + side, side)).resize((2 * r, 2 * r), Image.LANCZOS)
    d.ellipse([cx - r - 10, cy - r - 10, cx + r + 10, cy + r + 10], fill=WHITE); d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=md)
    m = Image.new("L", (2 * r, 2 * r), 0); ImageDraw.Draw(m).ellipse([0, 0, 2 * r - 1, 2 * r - 1], fill=255)
    img.paste(head, (cx - r, cy - r), Image.composite(head.split()[3], Image.new("L", (2 * r, 2 * r), 0), m))
def ailabel(d, bg):
    t = "AI로 생성한 가상의 캐릭터입니다"; f = F(MED, 22); tw = d.textlength(t, font=f)
    d.rounded_rectangle([S - 60 - tw - 24, S - 82, S - 60, S - 44], 19, fill=bg); d.text((S - 72, S - 63), t, font=f, fill=GRAY, anchor="rm")
def pill(d, x, y, t, dk, bg, center=False):
    f = F(SEMI, 34); w = d.textlength(t, font=f) + 52
    if center: x = (S - w) / 2
    d.rounded_rectangle([x, y, x + w, y + 64], 32, fill=dk); d.text((x + 26, y + 32), t, font=f, fill=bg, anchor="lm")
def tint(bg, md, k=.07): return tuple(int(bg[i] * (1 - k) + md[i] * k) for i in range(3))
def logo(d, dk): d.text((90, S - 84), "子午線 자오선", font=F(SER, 32), fill=dk)
def lines_at(d, lines, x, y, size, col=INK, center=False):
    for l in lines:
        d.text((S // 2 if center else x, y), l, font=F(SER, size), fill=col, anchor="ma" if center else "la"); y += int(size * 1.2)
    return y
def accent(d, x, y, dk, center=False):
    x0 = S // 2 - 70 if center else x; d.line([(x0, y), (x0 + 140, y)], fill=dk, width=8)

def q_left(d, img, T, bg, dk, md, face):
    d.text((760, 540), T["glyph"], font=F(SER, 760), fill=tint(bg, md), anchor="mm")
    pill(d, 90, 90, T["kick"], dk, bg); badge(img, d, face, bg, md, S - 175, 170, 95)
    s = fit(d, T["hook"], 900, 160); h = int(s * 1.2) * len(T["hook"]); y0 = 880 - 130 - h
    y = lines_at(d, T["hook"], 90, max(y0, 270), s); accent(d, 90, y + 30, dk)
    d.text((90, y + 62), T["sub"], font=F(SEMI, 46), fill=dk)
def q_center(d, img, T, bg, dk, md, face):
    d.text((S // 2, 600), T["glyph"], font=F(SER, 760), fill=tint(bg, md), anchor="mm")
    pill(d, 0, 90, T["kick"], dk, bg, center=True); badge(img, d, face, bg, md, S // 2, 330, 105)
    s = fit(d, T["hook"], 900, 150); y = lines_at(d, T["hook"], 0, 480, s, center=True); accent(d, 0, y + 30, dk, center=True)
    d.text((S // 2, y + 62), T["sub"], font=F(SEMI, 46), fill=dk, anchor="ma")
def q_card(d, img, T, bg, dk, md, face):
    d.text((S - 230, S - 260), T["glyph"], font=F(SER, 600), fill=tint(bg, md, .10), anchor="mm")
    pill(d, 90, 90, T["kick"], dk, bg)
    d.rounded_rectangle([70, 230, S - 70, 880], 44, fill=WHITE, outline=md, width=6)
    s = fit(d, T["hook"], 800, 150); h = int(s * 1.2) * len(T["hook"]); y0 = 230 + (650 - h - 100) // 2 + 20
    y = lines_at(d, T["hook"], 0, y0, s, center=True); accent(d, 0, y + 28, dk, center=True)
    d.text((S // 2, y + 56), T["sub"], font=F(SEMI, 42), fill=dk, anchor="ma")
    badge(img, d, face, bg, md, S - 170, 215, 90)
def n_chips(d, img, T, bg, dk, md, face):
    pill(d, 90, 90, T["kick"], dk, bg); badge(img, d, face, bg, md, S - 170, 170, 95)
    s = fit(d, T["hook"], 900, 156); y = lines_at(d, T["hook"], 90, 215, s)
    d.text((90, y + 14), T["sub"], font=F(SEMI, 46), fill=dk)
    it = T["items"]; cols = 3; n = len(it); rows = (n + 2) // 3; cw, ch, g = 290, 104, 20; y0 = y + 100
    if y0 + rows * ch + (rows - 1) * g > 920: ch = 90
    for i, t in enumerate(it):
        x = 90 + (i % cols) * (cw + g); yy = y0 + (i // cols) * (ch + g)
        d.rounded_rectangle([x, yy, x + cw, yy + ch], 26, fill=WHITE, outline=md, width=4); d.text((x + cw // 2, yy + ch // 2), t, font=F(SEMI, 46), fill=INK, anchor="mm")
def s_gua(d, img, T, bg, dk, md, face):
    pat = [1, 0, 1, 1, 0, 1]; x0, x1 = 820, 990; y = 130
    for i, p in enumerate(pat):
        yy = y + i * 68; col = dk if i != 2 else (196, 74, 52)
        if p: d.rounded_rectangle([x0, yy, x1, yy + 32], 10, fill=col)
        else: d.rounded_rectangle([x0, yy, x0 + 68, yy + 32], 10, fill=col); d.rounded_rectangle([x1 - 68, yy, x1, yy + 32], 10, fill=col)
    pill(d, 90, 90, T["kick"], dk, bg); s = fit(d, T["hook"], 720, 150); y = lines_at(d, T["hook"], 90, 250, s)
    accent(d, 90, y + 30, dk); d.text((90, y + 62), T["sub"], font=F(SEMI, 46), fill=dk); badge(img, d, face, bg, md, S - 175, 760, 95)
def ring(d, cx, cy, r, ch, dk, bg, size):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=WHITE, outline=dk, width=10); d.text((cx, cy - 4), ch, font=F(SER, size), fill=dk, anchor="mm")
def s_ring(d, img, T, bg, dk, md, face):
    pill(d, 90, 90, T["kick"], dk, bg); ring(d, S - 260, 270, 150, T["glyph"], dk, bg, 190); badge(img, d, face, bg, md, 190, 330, 100)
    s = fit(d, T["hook"], 900, 156); y = lines_at(d, T["hook"], 90, 450, s); accent(d, 90, y + 30, dk); d.text((90, y + 62), T["sub"], font=F(SEMI, 46), fill=dk)
def s_trio(d, img, T, bg, dk, md, face):
    pill(d, 90, 90, T["kick"], dk, bg); badge(img, d, face, bg, md, S - 170, 170, 95)
    s = fit(d, T["hook"], 900, 156); y = lines_at(d, T["hook"], 90, 230, s)
    for i, ch in enumerate(T["glyph"]): ring(d, 250 + i * 290, y + 160, 104, ch, dk, bg, 130)
    d.text((90, y + 300), T["sub"], font=F(SEMI, 46), fill=dk)
def s_cal(d, img, T, bg, dk, md, face):
    pill(d, 90, 90, T["kick"], dk, bg); badge(img, d, face, bg, md, S - 170, 170, 95)
    s = fit(d, T["hook"], 900, 150); y = lines_at(d, T["hook"], 90, 215, s); hot = T["hot"]; cw, ch, g = 118, 66, 10; y0 = y + 40
    for k in range(31):
        day = k + 1; pos = k + 4; x = 90 + (pos % 7) * (cw + g); yy = y0 + (pos // 7) * (ch + g); on = day in hot
        d.rounded_rectangle([x, yy, x + cw, yy + ch], 16, fill=dk if on else WHITE, outline=dk if on else md, width=3)
        d.text((x + cw // 2, yy + ch // 2), str(day), font=F(SEMI, 34), fill=WHITE if on else INK, anchor="mm")
DRAW = {"QL": q_left, "QC": q_center, "QK": q_card, "N": n_chips, "gua": s_gua, "ring": s_ring, "trio": s_trio, "cal": s_cal}
SUB3 = "사주 · 별자리 · 숫자로 읽었어요"; K3 = "정월의 세 지도"; SIX = ["사주", "자미두수", "당사주", "하락이수", "점성술", "수비학"]
T = {
 "s10": dict(d="cal", el="흙", kick="10월 손없는날", hook=["이사 날짜,", "이 날만 피해요"], hot=[9, 10, 19, 20, 29, 30]),
 "n01": dict(d="QL", el="불", kick="2027 띠별 운세", hook=["기운 좋은 띠", "따로 있어요"], sub="12띠 한눈에 보기", glyph="未"),
 "n02": dict(d="trio", el="물", kick="2027 삼재띠", hook=["내 띠도", "삼재일까?"], sub="해당 띠를 확인하세요", glyph="亥卯未"),
 "n03": dict(d="QC", el="나무", kick="띠별 궁합표", hook=["우리 둘의 띠,", "잘 맞을까?"], sub="12띠 궁합 한 장 정리", glyph="合"),
 "n04": dict(d="ring", el="불", kick="2027 양띠", hook=["양띠에게 온", "변화의 해"], sub="월별 · 재물 · 연애운", glyph="未"),
 "n05": dict(d="QK", el="흙", kick="2027 재물운", hook=["내년에 돈이", "모이는 띠는?"], sub="TOP3 공개", glyph="財"),
 "n06": dict(d="ring", el="나무", kick="2027 소띠", hook=["소띠의", "내년 흐름은?"], sub="월별 · 재물 · 연애운", glyph="丑"),
 "n07": dict(d="QC", el="불", kick="태어난 날 연애", hook=["내 연애는", "어떤 스타일?"], sub="태어난 날로 보는 10가지", glyph="戀"),
 "n08": dict(d="ring", el="나무", kick="2027 토끼띠", hook=["토끼띠에게", "사람이 모여요"], sub="월별 · 재물 · 연애운", glyph="卯"),
 "n09": dict(d="ring", el="쇠", kick="2027 원숭이띠", hook=["원숭이띠,", "인정받는 해?"], sub="책임과 인정의 흐름", glyph="申"),
 "n10": dict(d="QL", el="불", kick="2027 연애운", hook=["연애운 좋은", "다섯 띠는?"], sub="띠별 인연의 달까지", glyph="戀"),
 "n11": dict(d="N", el="쇠", kick="자오선 소개", hook=["사주 하나로", "부족할 때"], sub="여섯 운명학을 겹쳐요", items=SIX),
 "n12": dict(d="QK", el="쇠", kick="절기 이야기", hook=["상강이 지나면", "무엇이 달라질까?"], sub="이사 날짜와 11월 운세", glyph="霜"),
 "n13": dict(d="N", el="흙", kick="같은 생년월일", hook=["해석은", "6가지"], sub="어디서 겹치고 갈릴까?", items=SIX),
 "n14": dict(d="QL", el="불", kick="2027 운세", hook=["같은 해인데", "결과가 다르다?"], sub="사주 · 별자리 · 숫자로 겹쳐 보니", glyph="運"),
 "n15": dict(d="gua", el="물", kick="정월에게 묻다", hook=["지금 고민,", "괘가 답해요"], sub="주역에 오행을 더한 육효 풀이"),
}
SER_HOOK = {16: ["눈물이 많은 건", "약한 게 아니에요"], 17: ["헤어진 뒤에", "왜 연락할까?"], 18: ["돈 모으는 사람", "결이 똑같아요"], 19: ["싸우면 늘", "내가 먼저 사과"],
 20: ["화나면 말이", "없어지는 이유"], 21: ["혼자 떠나야", "마음이 풀려요"], 22: ["첫눈에 반하면", "이유가 있어요"], 23: ["참다가 한 번에", "터지는 이유"],
 24: ["압박이 올수록", "더 강해져요"], 25: ["자꾸 뭔가", "배우고 싶다면"], 26: ["마음은 큰데", "표현은 느린 이유"], 27: ["말 한마디로", "분위기가 바뀐다"],
 28: ["세 지도가 모두", "맞다고 하면?"], 29: ["회의보다", "혼자가 편해요"], 30: ["금방 뜨거워져", "금방 식나요?"], 31: ["일단 하자?", "한 번 더 생각?"],
 32: ["무대에 서면", "달라지는 사람"], 33: ["약속 취소 문자,", "속으로 웃었다면"]}
import json
_ser = json.load(open(os.path.join(HERE, "series.json"), encoding="utf-8")) if os.path.exists(os.path.join(HERE, "series.json")) else {}
for n, hook in SER_HOOK.items():
    face, el, mark = _ser[str(n)]
    if n == 28: T[f"n{n}"] = dict(d="N", el=el, kick=K3, hook=hook, sub=SUB3, items=["사주", "별자리", "수비학"], face=face)
    else: T[f"n{n}"] = dict(d=["QL", "QC", "QK"][n % 3], el=el, kick=K3, hook=hook, sub=SUB3, glyph=mark, face=face)
FACES = ["v1_lowbun", "v2_straight", "v3_ponytail", "v4_glasses", "v5_halfup_v2", "v13_horn_glasses", "v8_gesture"]
def render(pid, path, size=800):
    t = T[pid]; bg, dk, md = EL[t["el"]]
    face = t.get("face") or FACES[sum(map(ord, pid)) % len(FACES)]
    img = Image.new("RGB", (S, S), bg); d = ImageDraw.Draw(img)
    DRAW[t["d"]](d, img, t, bg, dk, md, face); logo(d, dk); ailabel(d, bg)
    img.resize((size, size), Image.LANCZOS).save(path, quality=92)
if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "img")
    for pid in T: render(pid, os.path.join(out, f"sq_{pid}.jpg"))
    print(len(T), "done")
