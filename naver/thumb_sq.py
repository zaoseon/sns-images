"""네이버 블로그 대표 이미지(정사각) 생성기 v2 (10/3 대표 피드백 반영).
- 1:1, 글자는 중앙 안전영역, 정월 얼굴은 잘리지 않게(머리 전체+어깨), AI 표시 우하단 연회색, 정월 원본 v5_halfup 금지.
- 시스템은 고정(폰트·라벨 위치·로고·AI 표시·원소색), 구도는 돌려 쓰고, 어두운 판(dark)을 4~5개에 1개꼴로 섞는다.
- 조사 근거(10/3): 손톱 크기에서 0.5초 안에 읽힘, 정보형은 굵은 글씨+숫자+라벨 하나, 강조는 색·박스 중 하나, 같은 폰트·색을 계속 쓰면 블로그 홈이 정돈됨.
사용: python3 thumb_sq.py [출력폴더]  -> sq_<id>.jpg(800x800) 전부 / render(pid, path, dark=None)"""
import os, sys, json
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__))
FD = os.path.join(HERE, "..", "pipeline", "fonts") + "/"
SER, SEMI, MED, BLK = FD + "serif.otf", FD + "PRETENDARD-SEMIBOLD.OTF", FD + "PRETENDARD-MEDIUM.OTF", FD + "PRETENDARD-BLACK.OTF"
CH = os.path.join(HERE, "..", "characters", "cut") + "/"
S = 1080
EL = {"불": ((251, 231, 222), (196, 74, 52), (238, 170, 150)), "물": ((222, 232, 244), (36, 62, 112), (150, 178, 214)),
      "흙": ((244, 236, 220), (150, 108, 50), (222, 200, 160)), "나무": ((226, 240, 226), (54, 110, 70), (160, 200, 165)),
      "쇠": ((246, 243, 236), (140, 112, 50), (215, 200, 160))}
GOLD = (214, 178, 108); DARKBG = (24, 22, 30)
DARKMD = {"불": (96, 44, 40), "물": (40, 56, 96), "흙": (88, 70, 40), "나무": (40, 78, 60), "쇠": (70, 66, 60)}
_f = {}
def F(p, s):
    if (p, s) not in _f: _f[(p, s)] = ImageFont.truetype(p, s)
    return _f[(p, s)]
class Ctx:
    def __init__(s, el, dark):
        bg, dk, md = EL[el]; s.dark = dark
        if dark:
            s.bg, s.fg, s.acc, s.md, s.card, s.line, s.gray, s.pillfg, s.tintk = DARKBG, (244, 238, 226), GOLD, DARKMD[el], (38, 35, 46), GOLD, (150, 144, 136), DARKBG, .10
            s.tint = tuple(int(DARKBG[i] * .88 + 255 * .12) for i in range(3))
        else:
            s.bg, s.fg, s.acc, s.md, s.card, s.line, s.gray, s.pillfg, s.tintk = bg, (38, 32, 28), dk, md, (255, 255, 255), md, (150, 144, 136), bg, .07
            s.tint = tuple(int(bg[i] * (1 - .07) + md[i] * .07) for i in range(3))
        s.ring_bg = (255, 255, 255) if not dark else (38, 35, 46)
def fit(d, lines, maxw, start, lo=90, path=SER):
    s = start
    while s > lo and max(d.textlength(l, font=F(path, s)) for l in lines) > maxw: s -= 4
    return s
def head_circle(face, D, c):
    """머리 전체+어깨가 원 안에 들어오게. 머리 폭 기준으로 크기를 맞추고 위쪽에 여백을 둔다."""
    face = "v5_halfup_v2" if face == "v5_halfup" else face
    ch = Image.open(CH + face + ".png").convert("RGBA"); a = np.array(ch)[:, :, 3]; h, w = a.shape
    ys, xs = np.where(a[:int(h * .40)] > 40); x0, x1, y0 = xs.min(), xs.max(), ys.min()
    sc = D * 0.72 / (x1 - x0); cw, chh = int(w * sc), int(h * sc); chs = ch.resize((cw, chh), Image.LANCZOS)
    cv = Image.new("RGBA", (D, D), c.md + (255,))
    ox = int(D / 2 - ((x0 + x1) / 2) * sc); oy = int(D * 0.15 - y0 * sc)
    cv.alpha_composite(chs, (ox, oy)) if ox >= 0 and oy >= 0 else cv.paste(chs, (ox, oy), chs)
    m = Image.new("L", (D, D), 0); ImageDraw.Draw(m).ellipse([0, 0, D - 1, D - 1], fill=255); cv.putalpha(m); return cv
def badge(img, d, face, c, cx, cy, r):
    d.ellipse([cx - r - 10, cy - r - 10, cx + r + 10, cy + r + 10], fill=(255, 255, 255) if not c.dark else GOLD)
    cv = head_circle(face, 2 * r, c); img.paste(cv, (cx - r, cy - r), cv)
def figure(img, d, face, c, h, cx):
    """상반신 큰 정월: 얼굴 전체가 보이게. 아래쪽이 화면 끝에 닿는다."""
    face = "v5_halfup_v2" if face == "v5_halfup" else face
    ch = Image.open(CH + face + ".png").convert("RGBA"); r = h / ch.height; ch = ch.resize((int(ch.width * r), h), Image.LANCZOS)
    d.ellipse([cx - 280, S - h - 20, cx + 280, S + 400], fill=c.md); img.paste(ch, (cx - ch.width // 2, S - h), ch)
def ailabel(d, c):
    t = "AI로 생성한 가상의 캐릭터입니다"; f = F(MED, 30); tw = d.textlength(t, font=f)
    d.rounded_rectangle([S - 56 - tw - 30, S - 104, S - 56, S - 48], 28, fill=c.bg); d.text((S - 71, S - 76), t, font=f, fill=c.gray, anchor="rm")
def pill(d, c, x, y, t, center=False):
    f = F(SEMI, 46); w = d.textlength(t, font=f) + 70
    if center: x = (S - w) / 2
    d.rounded_rectangle([x, y, x + w, y + 86], 43, fill=c.acc); d.text((x + 35, y + 43), t, font=f, fill=c.pillfg, anchor="lm")
def logo(d, c): d.text((90, S - 100), "子午線 자오선", font=F(SER, 44), fill=c.acc)
def lines_at(d, lines, x, y, size, col, center=False, path=SER):
    for l in lines:
        d.text((S // 2 if center else x, y), l, font=F(path, size), fill=col, anchor="ma" if center else "la"); y += int(size * 1.2)
    return y
def accent(d, c, x, y, center=False):
    x0 = S // 2 - 80 if center else x; d.line([(x0, y), (x0 + 160, y)], fill=c.acc, width=11)
def card_rect(d, c, box, r=44): d.rounded_rectangle(box, r, fill=c.card, outline=c.line, width=6)

def q_left(d, img, T, c, face):
    d.text((760, 540), T["glyph"], font=F(SER, 760), fill=c.tint, anchor="mm")
    pill(d, c, 90, 90, T["kick"]); badge(img, d, face, c, S - 185, 190, 105)
    s = fit(d, T["hook"], 900, 160); h = int(s * 1.2) * len(T["hook"]); y = lines_at(d, T["hook"], 90, max(705 - h, 290), s, c.fg)
    accent(d, c, 90, y + 30); d.text((90, y + 62), T["sub"], font=F(SEMI, 56), fill=c.acc)
def q_center(d, img, T, c, face):
    d.text((S // 2, 600), T["glyph"], font=F(SER, 760), fill=c.tint, anchor="mm")
    pill(d, c, 0, 90, T["kick"], center=True); badge(img, d, face, c, S // 2, 345, 115)
    s = fit(d, T["hook"], 900, 150); y = lines_at(d, T["hook"], 0, 462, s, c.fg, center=True); accent(d, c, 0, y + 30, center=True)
    d.text((S // 2, y + 62), T["sub"], font=F(SEMI, 56), fill=c.acc, anchor="ma")
def q_card(d, img, T, c, face):
    d.text((S - 230, S - 260), T["glyph"], font=F(SER, 600), fill=c.tint, anchor="mm")
    pill(d, c, 90, 90, T["kick"]); card_rect(d, c, [70, 240, S - 70, 890])
    s = fit(d, T["hook"], 800, 150); h = int(s * 1.2) * len(T["hook"]); y0 = 240 + (650 - h - 100) // 2 + 20
    y = lines_at(d, T["hook"], 0, y0, s, c.fg, center=True); accent(d, c, 0, y + 28, center=True)
    d.text((S // 2, y + 56), T["sub"], font=F(SEMI, 52), fill=c.acc, anchor="ma"); badge(img, d, face, c, S - 175, 215, 100)
def big(d, img, T, c, face):
    """큰 숫자·키워드형: 굵은 고딕 거대 글자 + 한 줄 후크. 정보형(숫자 하나)"""
    pill(d, c, 90, 90, T["kick"]); badge(img, d, face, c, S - 185, 190, 105)
    hk = T["hook"]; s1 = fit(d, hk, 880, 78, 50, MED); y = 240
    for l in hk: d.text((90, y), l, font=F(SEMI, s1), fill=c.fg); y += int(s1 * 1.25)
    bs = fit(d, [T["big"]], 900, 360, 150, BLK); d.text((90, y + 10), T["big"], font=F(BLK, bs), fill=c.acc)
    y2 = y + 10 + int(bs * 1.12); d.text((90, y2), T["sub"], font=F(SEMI, 46), fill=c.fg)
def char_top(d, img, T, c, face):
    """정월 큰 상반신(오른쪽 아래) + 글자는 위. 얼굴 전체 보임."""
    figure(img, d, face, c, 560, S - 270)
    pill(d, c, 90, 90, T["kick"]); s = fit(d, T["hook"], 900, 128); y = lines_at(d, T["hook"], 90, 200, s, c.fg); accent(d, c, 90, y + 24)
    sub = T["sub"].split(" "); k = (len(sub) + 1) // 2; ls = [" ".join(sub[:k]), " ".join(sub[k:])]
    yy = max(y + 70, 680)
    for l in ls: d.text((90, yy), l, font=F(SEMI, 40), fill=c.acc); yy += 54
def ring(d, c, cx, cy, r, ch, size):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=c.ring_bg, outline=c.acc, width=10); d.text((cx, cy - 4), ch, font=F(SER, size), fill=c.acc, anchor="mm")
def n_chips(d, img, T, c, face):
    pill(d, c, 90, 90, T["kick"]); badge(img, d, face, c, S - 185, 190, 105)
    s = fit(d, T["hook"], 900, 156); y = lines_at(d, T["hook"], 90, 245, s, c.fg); d.text((90, y + 14), T["sub"], font=F(SEMI, 56), fill=c.acc)
    it = T["items"]; rows = (len(it) + 2) // 3; cw, ch, g = 290, 100, 20; y0 = y + 112
    if y0 + rows * ch + (rows - 1) * g > 900: ch = 86
    for i, t in enumerate(it):
        x = 90 + (i % 3) * (cw + g); yy = y0 + (i // 3) * (ch + g)
        d.rounded_rectangle([x, yy, x + cw, yy + ch], 26, fill=c.card, outline=c.line, width=4); d.text((x + cw // 2, yy + ch // 2), t, font=F(SEMI, 54), fill=c.fg, anchor="mm")
def s_gua(d, img, T, c, face):
    pat = [1, 0, 1, 1, 0, 1]; x0, x1 = 830, 990; y = 130
    for i, p in enumerate(pat):
        yy = y + i * 68; col = c.acc if i != 2 else (196, 74, 52)
        if p: d.rounded_rectangle([x0, yy, x1, yy + 32], 10, fill=col)
        else: d.rounded_rectangle([x0, yy, x0 + 64, yy + 32], 10, fill=col); d.rounded_rectangle([x1 - 64, yy, x1, yy + 32], 10, fill=col)
    pill(d, c, 90, 90, T["kick"]); s = fit(d, T["hook"], 700, 150); y = lines_at(d, T["hook"], 90, 250, s, c.fg)
    accent(d, c, 90, y + 30); d.text((90, y + 62), T["sub"], font=F(SEMI, 56), fill=c.acc); badge(img, d, face, c, S - 190, 790, 105)
def s_ring(d, img, T, c, face):
    pill(d, c, 90, 90, T["kick"]); ring(d, c, S - 260, 290, 150, T["glyph"], 190); badge(img, d, face, c, 200, 350, 110)
    s = fit(d, T["hook"], 900, 140); y = lines_at(d, T["hook"], 90, 470, s, c.fg); accent(d, c, 90, y + 26); d.text((90, y + 62), T["sub"], font=F(SEMI, 56), fill=c.acc)
def s_trio(d, img, T, c, face):
    pill(d, c, 90, 90, T["kick"]); badge(img, d, face, c, S - 185, 190, 105)
    s = fit(d, T["hook"], 900, 156); y = lines_at(d, T["hook"], 90, 250, s, c.fg)
    for i, ch in enumerate(T["glyph"]): ring(d, c, 250 + i * 290, y + 150, 104, ch, 130)
    d.text((90, y + 280), T["sub"], font=F(SEMI, 56), fill=c.acc)
def s_cal(d, img, T, c, face):
    pill(d, c, 90, 90, T["kick"]); badge(img, d, face, c, S - 185, 190, 105)
    s = fit(d, T["hook"], 900, 150); y = lines_at(d, T["hook"], 90, 235, s, c.fg); hot = T["hot"]; cw, chh, g = 118, 64, 10; y0 = y + 36
    for k in range(31):
        day = k + 1; pos = k + 4; x = 90 + (pos % 7) * (cw + g); yy = y0 + (pos // 7) * (chh + g); on = day in hot
        d.rounded_rectangle([x, yy, x + cw, yy + chh], 16, fill=c.acc if on else c.card, outline=c.acc if on else c.line, width=3)
        d.text((x + cw // 2, yy + chh // 2), str(day), font=F(SEMI, 34), fill=(c.bg if c.dark else (255, 255, 255)) if on else c.fg, anchor="mm")
DRAW = {"QL": q_left, "QC": q_center, "QK": q_card, "BIG": big, "CH": char_top, "N": n_chips, "gua": s_gua, "ring": s_ring, "trio": s_trio, "cal": s_cal}
SUB3 = "사주 · 별자리 · 숫자로 읽었어요"; K3 = "정월의 세 지도"; SIX = ["사주", "자미두수", "당사주", "하락이수", "점성술", "수비학"]
T = {
 "s10": dict(d="cal", el="흙", kick="10월 손없는날", hook=["이사 날짜,", "이 날만 피해요"], hot=[9, 10, 19, 20, 29, 30]),
 "n01": dict(d="QL", el="불", kick="2027 띠별 운세", hook=["기운 좋은 띠", "따로 있어요"], sub="12띠 한눈에 보기", glyph="未"),
 "n02": dict(d="trio", el="물", kick="2027 삼재띠", hook=["내 띠도", "삼재일까?"], sub="해당 띠를 확인하세요", glyph="亥卯未"),
 "n03": dict(d="BIG", el="나무", kick="띠별 궁합표", hook=["우리 둘의 띠,", "잘 맞을까?"], big="12띠", sub="궁합 한 장 정리"),
 "n04": dict(d="ring", el="불", kick="2027 양띠", hook=["양띠에게 온", "변화의 해"], sub="월별 · 재물 · 연애운", glyph="未"),
 "n05": dict(d="BIG", el="흙", kick="2027 재물운", hook=["내년에 돈이", "모이는 띠는?"], big="TOP3", sub="순위 공개"),
 "n06": dict(d="ring", el="나무", kick="2027 소띠", hook=["소띠의", "내년 흐름은?"], sub="월별 · 재물 · 연애운", glyph="丑"),
 "n07": dict(d="BIG", el="불", kick="태어난 날 연애", hook=["내 연애는", "어떤 스타일?"], big="10가지", sub="태어난 날로 보는 유형"),
 "n08": dict(d="ring", el="나무", kick="2027 토끼띠", hook=["토끼띠에게", "사람이 모여요"], sub="월별 · 재물 · 연애운", glyph="卯"),
 "n09": dict(d="ring", el="쇠", kick="2027 원숭이띠", hook=["원숭이띠,", "인정받는 해?"], sub="책임과 인정의 흐름", glyph="申"),
 "n10": dict(d="BIG", el="불", kick="2027 연애운", hook=["연애운 좋은 띠,", "인연의 달까지"], big="TOP5", sub="띠별 인연 시기"),
 "n11": dict(d="N", el="쇠", kick="자오선 소개", hook=["사주 하나로", "부족할 때"], sub="여섯 운명학을 겹쳐요", items=SIX),
 "n12": dict(d="QK", el="쇠", kick="절기 이야기", hook=["상강이 지나면", "무엇이 달라질까?"], sub="이사 날짜와 11월 운세", glyph="霜"),
 "n13": dict(d="BIG", el="흙", kick="같은 생년월일", hook=["같은 생일인데", "해석은 이만큼"], big="6가지", sub="어디서 겹치고 갈릴까?"),
 "n14": dict(d="CH", el="불", kick="2027 운세", hook=["같은 해인데", "결과가 다르다?"], sub="사주 · 별자리 · 숫자로 겹쳐 보니", face="v1_lowbun"),
 "n15": dict(d="gua", el="물", kick="정월에게 묻다", hook=["지금 고민,", "괘가 답해요"], sub="주역에 오행을 더한 육효 풀이"),
}
SER_HOOK = {16: ["눈물이 많은 건", "약한 게 아니에요"], 17: ["헤어진 뒤에", "왜 연락할까?"], 18: ["돈 모으는 사람", "결이 똑같아요"], 19: ["싸우면 늘", "내가 먼저 사과"],
 20: ["화나면 말이", "없어지는 이유"], 21: ["혼자 떠나야", "마음이 풀려요"], 22: ["첫눈에 반하면", "이유가 있어요"], 23: ["참다가 한 번에", "터지는 이유"],
 24: ["압박이 올수록", "더 강해져요"], 25: ["자꾸 뭔가", "배우고 싶다면"], 26: ["마음은 큰데", "표현은 느린 이유"], 27: ["말 한마디로", "분위기가 바뀐다"],
 28: ["세 지도가 모두", "맞다고 하면?"], 29: ["회의보다", "혼자가 편해요"], 30: ["금방 뜨거워져", "금방 식나요?"], 31: ["일단 하자?", "한 번 더 생각?"],
 32: ["무대에 서면", "달라지는 사람"], 33: ["약속 취소 문자,", "속으로 웃었다면"],
 34: ["일요일 밤마다", "생각이 많아져요"], 35: ["월요일이 유독", "무거운 이유"], 36: ["시작만 하고", "끝을 못 낸다면"], 37: ["남과 비교하면", "작아지는 이유"]}
_ser = json.load(open(os.path.join(HERE, "series.json"), encoding="utf-8"))
for n, hook in SER_HOOK.items():
    face, el, mark = _ser[str(n)]
    if n == 28: T[f"n{n}"] = dict(d="N", el=el, kick=K3, hook=hook, sub=SUB3, items=["사주", "별자리", "수비학"], face=face)
    else: T[f"n{n}"] = dict(d=["QL", "CH", "QK", "QC"][n % 4], el=el, kick=K3, hook=hook, sub=SUB3, glyph=mark, face=face)
T["n35"].update(kick="정월의 자미두수 읽기", sub="자미두수 · 사주를 겹쳐 읽었어요")
T["n36"].update(kick="정월의 당사주 읽기", sub="당사주 · 사주를 겹쳐 읽었어요")
FACES = ["v1_lowbun", "v2_straight", "v3_ponytail", "v4_glasses", "v5_halfup_v2", "v13_horn_glasses", "v8_gesture"]
# 어두운 판: 발행 순서로 4번째마다(홈 화면에서 어둡고 밝은 칸이 섞이게). 정월 ID는 published.json 날짜순.
def dark_set():
    try: pub = json.load(open(os.path.join(HERE, "published.json"), encoding="utf-8"))
    except Exception: return set()
    order = sorted(T, key=lambda k: (pub.get(k, {}).get("date", "9999"), pub.get(k, {}).get("time", "12:00") or "12:00", k))
    return {k for i, k in enumerate(order) if i % 4 == 2}
DARK = dark_set()
def render(pid, path, size=1080, dark=None):
    t = T[pid]; dk = (pid in DARK) if dark is None else dark; c = Ctx(t["el"], dk)
    face = t.get("face") or FACES[sum(map(ord, pid)) % len(FACES)]
    img = Image.new("RGB", (S, S), c.bg); d = ImageDraw.Draw(img)
    DRAW[t["d"]](d, img, t, c, face); logo(d, c); ailabel(d, c)
    (img if size == S else img.resize((size, size), Image.LANCZOS)).save(path, quality=96, subsampling=0, optimize=True)
if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "img")
    for pid in T: render(pid, os.path.join(out, f"sq_{pid}.jpg"))
    print(len(T), "done; dark:", sorted(DARK))
