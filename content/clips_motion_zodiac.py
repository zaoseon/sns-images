"""2027 띠 릴스 5편 새 틀 제작(10/7 대표 승인: 옛 v3 방식(명조·검은 바탕·작은 글씨) -> 새 틀로 같은 칸 덮어쓰기). 구성 그림: https://claude.ai/artifact/CSAxkf1JuXZNMQJssNi5MS
편마다 달력 장면·돈 일 사람 장면·마무리를 다르게(R19). 데이터는 build_2026-w42.py의 T(기존 띠 글과 같은 값)만 쓴다. 정월은 말띠·돼지띠 마무리에만(R03).
장면: 표지(훅) -> 왜 그럴까 -> 힘 쓸 달·아낄 달 -> 돈·일·사람 -> 마무리. 사용: python3 content/clips_motion_zodiac.py [이름 ...] -> 2026-motion/zodiac/<이름>.mp4 + _cover.jpg"""
import sys, os, math, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "..")); sys.path.insert(0, os.path.join(ROOT, "pipeline"))
from clip_motion import *
import fonts_kit as _FK, music_plan as MP
import clip_motion as _CM
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, ".."))   # clip_motion이 HERE·ROOT를 덮어써서 다시 정한다
src = open(os.path.join(HERE, "build_2026-w42.py"), encoding="utf-8").read(); _i = src.find("\nT = ["); _j = src.find("\n]\n", _i); _ns = {}; exec(src[_i:_j + 3], _ns); T = {t["name"]: t for t in _ns["T"]}
CORAL = (255, 138, 115, 255); GREEN = (70, 170, 120, 255); BROWN = (139, 90, 43, 255)
MONTHS = list(range(2, 14))
def ML(m): return "1월" if m == 13 else f"{m}월"
def lay(h=900): im = Image.new("RGBA", (1080, h), (0, 0, 0, 0)); return im, ImageDraw.Draw(im)
def hj_font(size): return font(_FK.P["serif"], size)
def circ(d, x, y, r, hj, fill, outline=None, fg=(255, 255, 255, 255), fs=None, ow=6):
    d.ellipse((x - r, y - r, x + r, y + r), fill=fill, outline=outline, width=ow if outline else 0); d.text((x, y - 3), hj, font=hj_font(fs or int(r * 1.1)), fill=fg, anchor="mm")
def title(c, s, t0=.05, size=96): return text(c, s, 500, t0, size, maxw=840, lh=1.2, stagger=0)


def text_in_box(c, s_, cx, cy, t0, size, maxw, color=WHITE, lh=1.3):
    """박스 안 글은 가로·세로 정중앙(R18): 글 높이를 재서 박스 가운데에 맞춘다"""
    H = text_h(s_, size, maxw, lh); return text(c, s_, cy - H / 2, t0, size, color=color, maxw=maxw, cx=cx, lh=lh, stagger=0)
def group_in_box(c, parts, cx, cy, t0, maxw, gap=22):
    """박스 안에 제목+본문처럼 여러 덩어리가 있으면 덩어리 전체를 정중앙에. parts=[(글, 크기, 색, 줄간격)]"""
    hs = [text_h(t_, sz, maxw, lh) for t_, sz, col, lh in parts]; y = cy - (sum(hs) + gap * (len(parts) - 1)) / 2
    for (t_, sz, col, lh), h_ in zip(parts, hs): text(c, t_, y, t0, sz, color=col, maxw=maxw, cx=cx, lh=lh, stagger=0); y += h_ + gap

def S_hook(name):
    t = T[name]
    def f(c):
        lines = t["hook"]; H = 62 + text_h(lines, 100, 820, 1.25) + 30 + text_h(t["one"], 56, 820, 1.35) + 30 + 50; y0 = 910 - H / 2
        y = text(c, f"2027 {name}", y0, .05, 58, color=GOLD, maxw=820, stagger=0)
        y = text(c, lines, y + 6, .25, 100, maxw=820, lh=1.25, stagger=.22)
        y = text(c, t["one"], y + 30, 1.1, 56, color=DIM, maxw=820, lh=1.35, stagger=0)
        text(c, t["y"].replace(" · ", "·") + "년생", y + 30, 1.5, 44, color=DIM, maxw=820, stagger=0)
    return f
# ── 왜 그럴까 장면 (띠마다 다른 도형)
def S_why(name):
    t = T[name]
    def f(c):
        tt = c.t; y = title(c, "왜 그럴까")
        im, d = lay(700); Y0 = 640
        def pop_r(k, t0): return e_back(cl((tt - t0) / .45))
        if name == "말띠":
            a, b = pop_r(0, .4), pop_r(1, .9)
            L1 = Image.new("RGBA", (1080, 700), (0, 0, 0, 0)); L2 = Image.new("RGBA", (1080, 700), (0, 0, 0, 0)); d1 = ImageDraw.Draw(L1); d2 = ImageDraw.Draw(L2)
            r = int(150 * min(a, 1.05)); d1.ellipse((CX - 110 - r, 250 - r, CX - 110 + r, 250 + r), fill=(232, 193, 90, 90), outline=GOLD, width=6)
            r = int(150 * min(b, 1.05)); d2.ellipse((CX + 110 - r, 250 - r, CX + 110 + r, 250 + r), fill=(244, 140, 4, 90), outline=(244, 140, 4, 255), width=6)
            im = Image.alpha_composite(L1, L2); d = ImageDraw.Draw(im)
            if a > .6: d.text((CX - 215, 250), "午", font=hj_font(120), fill=(255, 255, 255, 255), anchor="mm")
            if b > .6: d.text((CX + 215, 250), "未", font=hj_font(120), fill=(255, 255, 255, 255), anchor="mm")
            blit(c.fr, im, 0, Y0, 1.0); text(c, "겹치는 곳이 짝이에요", y + 450, 1.8, 62, color=GOLD, maxw=800, stagger=0); text(c, "午와 未는 짝이 되는 글자(육합)", y + 540, 2.4, 46, color=DIM, maxw=840, stagger=0)
        elif name == "양띠":
            for k, x in enumerate((CX - 230, CX + 230)):
                g = pop_r(k, .4 + k * .5)
                if g > 0: circ(d, x, 250, int(150 * min(g, 1.05)), "未", (255, 255, 255, 30), GOLD, fs=130)
            g = e_out(cl((tt - 1.1) / .4))
            if g > 0: d.text((CX, 250), "=", font=font(BLACK, 130), fill=(255, 255, 255, int(255 * g)), anchor="mm")
            blit(c.fr, im, 0, Y0, 1.0); text(c, "2027년 丁未, 내 띠가 돌아와요", y + 450, 1.7, 56, color=GOLD, maxw=840, stagger=0); text(c, "내 띠가 돌아온 해(본명년)", y + 540, 2.4, 46, color=DIM, maxw=840, stagger=0)
        elif name == "닭띠":
            g1, g2 = pop_r(0, .4), pop_r(1, 1.2); circ(d, CX - 250, 250, int(140 * min(g1, 1.05)), "丁", CORAL, fg=(255, 255, 255, 255), fs=130) if g1 > 0 else None
            ar = e_out(cl((tt - .8) / .4)); d.text((CX, 250), "→", font=font(BLACK, 110), fill=(255, 255, 255, int(255 * ar)), anchor="mm")
            circ(d, CX + 250, 250, int(140 * min(g2, 1.05)), "酉", GOLD, fg=(30, 24, 40, 255), fs=130) if g2 > 0 else None
            blit(c.fr, im, 0, Y0, 1.0); text(c, "불에 다듬어지는 보석", y + 450, 1.9, 62, color=GOLD, maxw=840, stagger=0); text(c, "丁은 불, 酉는 보석 같은 글자", y + 540, 2.5, 46, color=DIM, maxw=840, stagger=0)
        elif name == "돼지띠":
            pts = [(CX, 130, "亥"), (CX - 230, 480, "卯"), (CX + 230, 480, "未")]
            prog = e_out(cl((tt - 1.3) / 1.2))
            for k, (a, b) in enumerate([(0, 1), (1, 2), (2, 0)]):
                seg = cl(prog * 3 - k)
                if seg > 0: d.line([(pts[a][0], pts[a][1]), (pts[a][0] + (pts[b][0] - pts[a][0]) * seg, pts[a][1] + (pts[b][1] - pts[a][1]) * seg)], fill=GOLD, width=8)
            for k, (x, yy, hj) in enumerate(pts):
                g = pop_r(k, .3 + k * .35)
                if g > 0: circ(d, x, yy, int(105 * min(g, 1.08)), hj, GOLD if hj == "未" else (255, 255, 255, 40), GOLD, fg=(30, 24, 40, 255) if hj == "未" else (255, 255, 255, 255), fs=100)
            blit(c.fr, im, 0, Y0, 1.0); text(c, "세 글자가 한 팀(삼합)", y + 720, 2.2, 62, color=GOLD, maxw=840, stagger=0)
        else:  # 쥐띠
            circ(d, CX - 250, 250, int(140 * min(pop_r(0, .4), 1.05)), "子", (255, 255, 255, 30), GOLD, fs=130)
            x2 = e_out(cl((tt - .8) / .4)); a2 = int(255 * x2); d.line([(CX - 45, 205), (CX + 45, 295)], fill=(CORAL[0], CORAL[1], CORAL[2], a2), width=16); d.line([(CX + 45, 205), (CX - 45, 295)], fill=(CORAL[0], CORAL[1], CORAL[2], a2), width=16)
            g = pop_r(1, 1.1)
            if g > 0: circ(d, CX + 250, 250, int(140 * min(g, 1.05)), "未", (255, 255, 255, 30), CORAL, fs=130)
            blit(c.fr, im, 0, Y0, 1.0); text(c, "서로 서운하게 만드는 사이(해)", y + 450, 1.9, 58, color=CORAL, maxw=840, stagger=0); text(c, "子와 未는 해이면서 원진이에요", y + 540, 2.5, 46, color=DIM, maxw=840, stagger=0)
    return f
# ── 힘 쓸 달·아낄 달
def S_cal(name):
    t = T[name]; good, save = t["good"], t["save"]
    def f(c):
        tt = c.t; y = title(c, "힘 쓸 달 · 아낄 달", size=88)
        im, d = lay(900); Y0 = 600; fm = font(BLACK, 46)
        def st(m): return "g" if m in good else ("s" if m in save else "n")
        if name == "말띠":  # 12칸 격자
            for i, m in enumerate(MONTHS):
                g = e_back(cl((tt - (.25 + i * .12)) / .35)); r_, c_ = divmod(i, 4); x0 = 130 + c_ * 220; y0 = 40 + r_ * 160
                if g <= 0: continue
                k = st(m); w = int(200 * min(g, 1.0)); h = 130
                if k == "g": d.rounded_rectangle((x0, y0, x0 + w, y0 + h), 22, fill=GOLD); col = (30, 24, 40, 255)
                elif k == "s": d.rounded_rectangle((x0, y0, x0 + w, y0 + h), 22, outline=CORAL, width=6); col = CORAL
                else: d.rounded_rectangle((x0, y0, x0 + w, y0 + h), 22, fill=(255, 255, 255, 36)); col = (255, 255, 255, 170)
                if g > .8: d.text((x0 + 100, y0 + 65), ML(m), font=fm, fill=col, anchor="mm")
            blit(c.fr, im, 0, Y0, 1.0); text(c, "금색은 힘 쓸 달 · 붉은 테두리는 아낄 달", Y0 + 560, 4.0, 46, color=DIM, maxw=840, stagger=0)
        elif name == "양띠":  # 노선도 두 줄
            for row, ms in enumerate((MONTHS[:6], MONTHS[6:])):
                yy = 120 + row * 300; d.line([(90, yy), (990, yy)], fill=(255, 255, 255, 90), width=8)
                for i, m in enumerate(ms):
                    g = e_back(cl((tt - (.25 + (row * 6 + i) * .22)) / .4)); x = 120 + i * 168
                    if g <= 0: continue
                    k = st(m)
                    if k == "g": d.ellipse((x - 62 * min(g, 1.05), yy - 62 * min(g, 1.05), x + 62 * min(g, 1.05), yy + 62 * min(g, 1.05)), fill=GOLD); d.text((x, yy - 2), ML(m), font=fm, fill=(30, 24, 40, 255), anchor="mm")
                    elif k == "s": d.ellipse((x - 62, yy - 62, x + 62, yy + 62), outline=CORAL, width=7); d.text((x, yy - 2), ML(m), font=fm, fill=CORAL, anchor="mm")
                    else: d.ellipse((x - 22, yy - 22, x + 22, yy + 22), fill=(255, 255, 255, 130)); d.text((x, yy + 52), ML(m).replace("월", ""), font=font(BLACK, 34), fill=(255, 255, 255, 150), anchor="mm")
            blit(c.fr, im, 0, Y0, 1.0); text(c, "큰 금색 역은 힘 쓸 달 · 붉은 역은 아낄 달", Y0 + 560, 5.4, 46, color=DIM, maxw=840, stagger=0)
        elif name == "닭띠":  # 막대
            for i, m in enumerate(MONTHS):
                g = e_out(cl((tt - (.25 + i * .14)) / .5)); x = 100 + i * 72; k = st(m); h = 380 if k == "g" else (110 if k == "s" else 230)
                col = GOLD if k == "g" else (CORAL if k == "s" else (255, 255, 255, 110))
                d.rounded_rectangle((x, 520 - h * g, x + 54, 520), 12, fill=col)
                d.text((x + 27, 560), ML(m).replace("월", ""), font=font(BLACK, 36), fill=(255, 255, 255, 190), anchor="mm")
            blit(c.fr, im, 0, Y0, 1.0); text(c, "높은 막대는 힘 쓸 달 · 낮은 막대는 아낄 달", Y0 + 640, 4.4, 46, color=DIM, maxw=840, stagger=0)
        elif name == "돼지띠":  # 키네틱 글자
            g1 = e_out(cl((tt - .3) / .4)); g2 = e_out(cl((tt - 2.4) / .4))
            def kin(label, ms, col, t0, ys):
                text(c, label, ys, t0, 56, color=col, maxw=800, stagger=0)
                for i, m in enumerate(ms): text(c, ML(m), ys + 90 + i * 0, t0 + .3 + i * .5, 120, color=col, maxw=300, cx=CX - 260 + i * 260, stagger=0, anim="rise")
            kin("힘 쓸 달", good, GOLD, .3, 640); kin("아낄 달", save, CORAL, 2.8, 960)
        else:  # 쥐띠 점 격자
            for i, m in enumerate(MONTHS):
                g = e_back(cl((tt - (.25 + i * .12)) / .35)); r_, c_ = divmod(i, 6); x = 140 + c_ * 160; yy = 120 + r_ * 220; k = st(m)
                if g <= 0: continue
                if k == "g": d.ellipse((x - 68 * min(g, 1.05), yy - 68 * min(g, 1.05), x + 68 * min(g, 1.05), yy + 68 * min(g, 1.05)), fill=GOLD); d.text((x, yy - 2), ML(m), font=fm, fill=(30, 24, 40, 255), anchor="mm")
                elif k == "s": d.ellipse((x - 68, yy - 68, x + 68, yy + 68), outline=CORAL, width=8); d.text((x, yy - 2), ML(m), font=fm, fill=CORAL, anchor="mm")
                else: d.ellipse((x - 30, yy - 30, x + 30, yy + 30), fill=(255, 255, 255, 100)); d.text((x, yy + 62), ML(m).replace("월", ""), font=font(BLACK, 34), fill=(255, 255, 255, 150), anchor="mm")
            blit(c.fr, im, 0, Y0, 1.0); text(c, "금색 동그라미는 힘 쓸 달\n붉은 테두리는 아낄 달", Y0 + 520, 4.2, 46, color=DIM, maxw=840, stagger=0, lh=1.4)
    return f
SHORT = {"말띠": [("돈", "좋은 조건의 제안이 들어와요"), ("일", "나를 알아봐 주는 파트너가 생겨요"), ("사람", "오래된 관계가 한 단계 깊어져요")],
         "양띠": [("돈", "새 투자보다 정리가 먼저예요"), ("일", "더 적은 힘으로 하는 법을 찾아요"), ("사람", "편하지만 부딪히기도 쉬워요")],
         "닭띠": [("돈", "전문성이 돈이 돼요"), ("일", "품질로 평가받는 일이 잘 풀려요"), ("사람", "까다롭다는 오해를 받기 쉬워요")],
         "돼지띠": [("돈", "소개와 연결로 수입이 생겨요"), ("일", "함께하는 일이 잘 풀려요"), ("사람", "도와주는 사람이 늘어요")],
         "쥐띠": [("돈", "들어올 기회는 분명해요"), ("일", "혼자 끝낼 수 있는 일에서 성과가 나요"), ("사람", "서운한 건 그때그때 말하세요")]}
def S_work(name):
    s = SHORT[name]
    def f(c):
        tt = c.t; y = title(c, "돈 · 일 · 사람", size=88)
        if name == "말띠":  # 체크 목록
            for i, (a, b) in enumerate(s):
                yy = 640 + i * 190; g = e_back(cl((tt - (.3 + i * .7)) / .4))
                if g > 0:
                    im, d = lay(140); d.ellipse((60, 20, 60 + 100 * min(g, 1.05), 20 + 100 * min(g, 1.05)), fill=GOLD); d.line([(82, 72), (104, 94), (140, 46)], fill=(30, 24, 40, 255), width=14, joint="curve"); blit(c.fr, im, 0, yy, 1.0)
                text_in_box(c, f"{a}  {b}", CX + 100, yy + 70, .35 + i * .7, 52, 700, lh=1.25)
        elif name == "양띠":  # 카드 뒤집기
            for i, (a, b) in enumerate(s):
                yy = 640 + i * 230; p = cl((tt - (.3 + i * 1.3)) / .55); w = int(780 * abs(math.cos((1 - e_out(p)) * math.pi / 2)))
                im = Image.new("RGBA", (1080, 200), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
                if p < .5: d.rounded_rectangle((CX - w // 2, 10, CX + w // 2, 190), 30, fill=(255, 255, 255, 28), outline=(255, 255, 255, 120), width=4)
                else: d.rounded_rectangle((CX - w // 2, 10, CX + w // 2, 190), 30, fill=GOLD if i == 0 else (255, 255, 255, 40), outline=GOLD, width=4)
                blit(c.fr, im, 0, yy, 1.0)
                if p > .85: text_in_box(c, f"{a}  {b}", CX, yy + 100, 0, 46, 700, color=INK if i == 0 else WHITE, lh=1.2)
        elif name == "닭띠":  # 좌우 비교
            g = e_back(cl((tt - .3) / .5)); im, d = lay(520)
            d.rounded_rectangle((70, 20, 520, 500), 30, fill=GOLD); d.rounded_rectangle((560, 20, 1010, 500), 30, outline=CORAL, width=7); blit(c.fr, im, 0, 620, c.alpha(cl(g * 2)))
            group_in_box(c, [("좋은 신호", 52, INK, 1.2), (f"{s[0][1]}\n{s[1][1]}", 44, INK, 1.35)], 295, 880, .5, 390)
            group_in_box(c, [("조심", 52, CORAL, 1.2), (s[2][1], 44, WHITE, 1.35)], 785, 880, 1.6, 390)
        elif name == "돼지띠":  # 나무
            im, d = lay(720); g = e_out(cl((tt - .3) / .9))
            d.rounded_rectangle((165, 260, 235, 260 + int(380 * g)), 20, fill=BROWN)
            d.ellipse((60, 20, 340, 20 + int(280 * g)), fill=GREEN); d.ellipse((50, 600, 350, 690), fill=(107, 68, 35, 255))
            blit(c.fr, im, 0, 600, 1.0)
            for i, (a, b) in enumerate(s):
                text(c, f"{a}  {b}", [680, 880, 1090][i], 1.0 + i * .8, 46, maxw=620, cx=690, lh=1.25, stagger=0)
            text(c, "가지는 돈 · 줄기는 일 · 뿌리는 사람", 1300, 3.8, 42, color=DIM, maxw=840, stagger=0)
        else:  # 큰 숫자 3
            g = e_back(cl((tt - .3) / .5)); text(c, "3", 560, .3, 300, color=GOLD, maxw=400, stagger=0)
            text(c, "가지만 기억해요", 880, 1.0, 62, maxw=800, stagger=0)
            for i, (a, b) in enumerate(s): text(c, f"{a}  {b}", 1000 + i * 100, 1.6 + i * .7, 46, maxw=840, lh=1.2, stagger=0)
    return f
# ── 마무리: 댓글 질문 -> 팔로우 -> 프로필 링크 (R11), 마무리 5종 돌려 쓰기
def pill(c, t0, y):
    fnt = font(BLACK, 54); pl = "팔로우하고 더 많은 이야기 나눠요"; pw = int(fnt.getlength(pl)) + 80; im = Image.new("RGBA", (pw + 20, 140), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((10, 10, 10 + pw, 130), radius=60, fill=(244, 140, 4, 255)); d.text((10 + pw / 2, 71), pl, font=fnt, fill=(255, 255, 255, 255), anchor="mm")
    q = e_back((c.t - t0) / .45); pulse = 1 + .02 * math.sin(c.t * 6); L = im.resize((int(im.width * pulse), int(im.height * pulse))); blit(c.fr, L, CX - L.width / 2, y + (1 - e_out(q)) * 40, c.alpha(cl(q * 2)))
def prof(c, y, t0): text(c, "프로필 링크에서 생년월일 입력하고\n내 첫글자와 타고난 기운 알아보기", y, t0, 44, color=DIM, maxw=840, lh=1.4, stagger=0)
def S_cta(name):
    t = T[name]
    def f(c):
        if name == "말띠":      # ① 팔로우 카드 + 정월
            text(c, "내년에 만나고 싶은 짝은\n어떤 사람인가요?", 505, .1, 56, maxw=840, lh=1.25, stagger=0); character(c, "v3_ponytail", t0=.4, width=470, bottom=1060); pill(c, 1.2, 1075); prof(c, 1235, 1.9)
        elif name == "양띠":    # ④ 한 줄 정리 + 팔로우
            text(c, "댓글로 올해 정리할 것을 알려 주세요", 500, .1, 48, maxw=840, stagger=0); y = text(c, "정리부터 하면\n다시 서는 해", 620, .6, 92, color=GOLD, maxw=840, lh=1.25); pill(c, 1.4, y + 50); prof(c, y + 220, 2.0)
        elif name == "닭띠":    # ② 댓글 질문 크게
            y = text(c, "올해 가장\n인정받고 싶은 건\n무엇인가요?", 520, .1, 100, color=GOLD, maxw=840, lh=1.25); pill(c, 1.5, y + 50); prof(c, y + 220, 2.1)
        elif name == "돼지띠":  # ③ 정월 + 알약
            text(c, "올해 도움 받고 싶은 일은\n무엇인가요?", 505, .1, 52, maxw=840, lh=1.25, stagger=0); character(c, "v4_glasses", t0=.4, width=470, bottom=1060); pill(c, 1.2, 1075); prof(c, 1235, 1.9)
        else:                   # ⑤ 숫자 반복 + 팔로우
            text(c, "내 행운의 숫자는 몇 번일까요?", 505, .1, 50, maxw=840, stagger=0); g = e_back(cl((c.t - .5) / .5)); text(c, "4 · 9 · 4 · 9", 660, .5, 160, color=GOLD, maxw=900, stagger=0); pill(c, 1.6, 930); prof(c, 1110, 2.2)
    return f

# ───────── 두 번째 묶음: 원숭이·개·용·뱀띠 (10/7 대표 "권장안대로", 앞서 만든 5편과 도형·장면·마무리가 겹치지 않게)
NEW4 = ("원숭이띠", "개띠", "용띠", "뱀띠")
SHORT2 = {"원숭이띠": [("돈", "노력한 만큼 평가가 따라와요"), ("일", "무거운 일은 나눠서 맡아요"), ("사람", "윗사람께 보고와 확인을 자주 해요")],
          "개띠": [("돈", "계약과 서류를 꼼꼼히 봐요"), ("일", "변화에 먼저 맞추는 사람이 유리해요"), ("사람", "가까운 사이의 약속이 엇갈리기 쉬워요")],
          "용띠": [("돈", "새는 곳을 막고 쌓아요"), ("일", "자격·공부·기록이 무기예요"), ("사람", "비교보다 내 속도를 지켜요")],
          "뱀띠": [("돈", "큰 지출은 하루 자고 정해요"), ("일", "벌인 일은 끝까지 마무리해요"), ("사람", "말이 세게 나가지 않게 한 박자 쉬어요")]}
def arrow(d, x0, x1, y, col=(255, 255, 255, 255), w=10):
    d.line([(x0, y), (x1, y)], fill=col, width=w); s_ = 1 if x1 > x0 else -1; d.polygon([(x1, y), (x1 - 28 * s_, y - 20), (x1 - 28 * s_, y + 20)], fill=col)
def S_why2(name):
    t = T[name]
    def f(c):
        tt = c.t; y = title(c, "왜 그럴까"); im, d = lay(700); Y0 = 640
        g = lambda t0: e_back(cl((tt - t0) / .45))
        if name == "원숭이띠":
            r = 170 * min(g(.4), 1.05); pulse = 1 + .05 * math.sin(tt * 5)
            for k, w_ in enumerate((46, 30, 16)):
                rr_ = (r + 40 + k * 34) * pulse; d.ellipse((CX - rr_, 260 - rr_, CX + rr_, 260 + rr_), outline=(CORAL[0], CORAL[1], CORAL[2], 200 - k * 55), width=w_ // 4 + 2)
            circ(d, CX, 260, int(r), "申", GOLD, fg=(30, 24, 40, 255), fs=190)
            blit(c.fr, im, 0, Y0 - 20, 1.0); text(c, "불에 다듬어지는 쇠", y + 520, 1.6, 62, color=GOLD, maxw=840, stagger=0); text(c, "丁은 불, 申은 쇠 같은 글자", y + 610, 2.2, 46, color=DIM, maxw=840, stagger=0)
        elif name == "개띠":
            a, b = g(.4), g(.9); circ(d, CX - 260, 230, int(135 * min(a, 1.05)), "戌", (255, 255, 255, 30), GOLD, fs=125); circ(d, CX + 260, 230, int(135 * min(b, 1.05)), "未", (255, 255, 255, 30), GOLD, fs=125)
            ar = e_out(cl((tt - 1.2) / .5))
            if ar > 0: arrow(d, CX - 95, CX + 95 * ar, 190, GOLD); arrow(d, CX + 95, CX - 95 * ar, 280, CORAL)
            blit(c.fr, im, 0, Y0, 1.0); text(c, "서로 조율이 필요한 사이", y + 450, 1.9, 60, color=GOLD, maxw=840, stagger=0); text(c, "戌와 未는 맞춰 가야 하는 글자", y + 540, 2.5, 46, color=DIM, maxw=840, stagger=0)
        elif name == "용띠":
            a, b = g(.4), g(1.0); circ(d, CX, 110, int(100 * min(a, 1.05)), "辰", (206, 168, 84, 120), GOLD, fs=96); circ(d, CX, 440, int(100 * min(b, 1.05)), "未", (206, 168, 84, 120), GOLD, fs=96)
            ln = e_out(cl((tt - 1.4) / .5)); d.line([(CX, 215), (CX, 215 + 120 * ln)], fill=GOLD, width=8)
            blit(c.fr, im, 0, Y0, 1.0); text(c, "같은 흙끼리 만나요", y + 650, 2.0, 60, color=GOLD, maxw=840, stagger=0)
        else:  # 뱀띠
            d.rounded_rectangle((150, 215, 930, 245), 15, fill=(255, 138, 115, int(255 * e_out(cl((tt - 1.3) / .6))))) if tt > 1.3 else None
            for k, (x, hj) in enumerate(((CX - 300, "巳"), (CX, "午"), (CX + 300, "未"))):
                gg = g(.3 + k * .45)
                if gg > 0: circ(d, x, 230, int(115 * min(gg, 1.05)), hj, CORAL if hj == "午" else (255, 255, 255, 30), CORAL, fs=110, fg=(255, 255, 255, 255))
            blit(c.fr, im, 0, Y0, 1.0); text(c, "여름의 불로 함께 모여요", y + 450, 2.0, 60, color=CORAL, maxw=840, stagger=0); text(c, "巳午未는 여름을 이루는 세 글자", y + 540, 2.6, 46, color=DIM, maxw=840, stagger=0)
    return f
def S_cal2(name):
    t = T[name]; good, save = t["good"], t["save"]
    def f(c):
        tt = c.t; y = title(c, "힘 쓸 달 · 아낄 달", size=88); im, d = lay(900); Y0 = 600; fm = font(BLACK, 44)
        if name == "원숭이띠":   # 원형 시계: 2월이 맨 위, 시계 방향
            R = 300; cx_, cy_ = CX, 330
            d.ellipse((cx_ - R, cy_ - R, cx_ + R, cy_ + R), outline=(255, 255, 255, 70), width=4)
            for i, m in enumerate(MONTHS):
                g = e_back(cl((tt - (.25 + i * .15)) / .35)); ang = -math.pi / 2 + i * math.pi / 6; x = cx_ + R * math.cos(ang); yy = cy_ + R * math.sin(ang)
                if g <= 0: continue
                if m in good: rr_ = 56 * min(g, 1.05); d.ellipse((x - rr_, yy - rr_, x + rr_, yy + rr_), fill=GOLD); d.text((x, yy - 2), ML(m), font=fm, fill=(30, 24, 40, 255), anchor="mm")
                elif m in save: rr_ = 56; d.ellipse((x - rr_, yy - rr_, x + rr_, yy + rr_), outline=CORAL, width=7); d.text((x, yy - 2), ML(m), font=fm, fill=CORAL, anchor="mm")
                else: d.ellipse((x - 16, yy - 16, x + 16, yy + 16), fill=(255, 255, 255, 120))
            d.text((cx_, cy_ - 12), "2027", font=font(BLACK, 80), fill=(255, 255, 255, 200), anchor="mm"); d.text((cx_, cy_ + 56), "2월부터 한 바퀴", font=font(BLACK, 40), fill=(255, 255, 255, 150), anchor="mm")
            blit(c.fr, im, 0, Y0, 1.0); text(c, "금색은 힘 쓸 달 · 붉은 테두리는 아낄 달", Y0 + 700, 4.6, 44, color=DIM, maxw=840, stagger=0)
        elif name == "개띠":    # 칩 두 열
            for col, (label, ms, colr, cx_) in enumerate((("힘 쓸 달", good, GOLD, 290), ("아낄 달", save, CORAL, 790))):
                g0 = e_out(cl((tt - (.3 + col * 2.0)) / .4)); d.text((cx_, 40), label, font=font(BLACK, 60), fill=(colr[0], colr[1], colr[2], int(255 * g0)), anchor="mm")
                for i, m in enumerate(ms):
                    g = e_back(cl((tt - (.7 + col * 2.0 + i * .5)) / .4))
                    if g <= 0: continue
                    w, h = int(300 * min(g, 1.0)), 150; x0 = cx_ - 150; y0 = 110 + i * 190
                    if colr == GOLD: d.rounded_rectangle((x0, y0, x0 + w, y0 + h), 75, fill=GOLD); fc = (30, 24, 40, 255)
                    else: d.rounded_rectangle((x0, y0, x0 + w, y0 + h), 75, outline=CORAL, width=8); fc = CORAL
                    if g > .8: d.text((cx_, y0 + 75), ML(m), font=font(BLACK, 64), fill=fc, anchor="mm")
            blit(c.fr, im, 0, Y0 + 80, 1.0)
        elif name == "용띠":    # 세로 타임라인
            RH = 56; X0 = 250; tlt = 590
            im, d = lay(RH * 12 + 20)
            for i, m in enumerate(MONTHS):
                g = e_out(cl((tt - (.2 + i * .18)) / .3)); a = int(255 * g); yy = i * RH + RH // 2 + 10
                d.text((110, yy), ML(m), font=font(BLACK, 44), fill=(255, 255, 255, int(a * (1 if m in good + save else .6))), anchor="lm")
                d.rounded_rectangle((250, yy - 3, 900, yy + 3), 3, fill=(255, 255, 255, int(a * .2)))
                if m in good or m in save:
                    gg = e_out(cl((tt - (.5 + i * .18)) / .5)); colr = GOLD if m in good else CORAL
                    d.rounded_rectangle((250, yy - 20, 250 + 650 * gg, yy + 20), 20, fill=colr)
            blit(c.fr, im, 0, tlt, 1.0); text(c, "금색 힘 쓸 달 · 붉은색 아낄 달", tlt + RH * 12 + 20, 4.2, 44, color=DIM, maxw=840, stagger=0)
        else:  # 뱀띠: 물결선
            n = 12; xs = [110 + i * (860 / 11) for i in range(n)]
            def yv(m): return 90 if m in good else (430 if m in save else 260)
            pts = []
            for i in range(n - 1):
                for k in range(20):
                    u = k / 20; ease = (1 - math.cos(u * math.pi)) / 2; pts.append((xs[i] + (xs[i + 1] - xs[i]) * u, yv(MONTHS[i]) + (yv(MONTHS[i + 1]) - yv(MONTHS[i])) * ease))
            pts.append((xs[-1], yv(MONTHS[-1]))); prog = e_out(cl((tt - .3) / 2.8)); k = int(len(pts) * prog)
            if k > 1: d.line(pts[:k], fill=(255, 255, 255, 220), width=8, joint="curve")
            for i, m in enumerate(MONTHS):
                if tt < .3 + 2.8 * (i / 11): continue
                x, yy = xs[i], yv(m)
                if m in good: d.ellipse((x - 34, yy - 34, x + 34, yy + 34), fill=GOLD)
                elif m in save: d.ellipse((x - 34, yy - 34, x + 34, yy + 34), outline=CORAL, width=7)
                else: d.ellipse((x - 12, yy - 12, x + 12, yy + 12), fill=(255, 255, 255, 140))
                d.text((x, 560), ML(m).replace("월", ""), font=font(BLACK, 36), fill=(255, 255, 255, 190 if (m in good or m in save) else 120), anchor="mm")
            blit(c.fr, im, 0, Y0, 1.0); text(c, "파도의 높은 곳은 힘 쓸 달 · 낮은 곳은 아낄 달", Y0 + 640, 4.0, 44, color=DIM, maxw=840, stagger=0)
    return f
def S_work2(name):
    s = SHORT2[name]
    def f(c):
        tt = c.t; y = title(c, "돈 · 일 · 사람", size=88)
        if name == "원숭이띠":   # 큰 동그라미 세 개
            im, d = lay(260)
            for i, (a, b) in enumerate(s):
                g = e_back(cl((tt - (.3 + i * .7)) / .45)); x = 190 + i * 350
                if g > 0: d.ellipse((x - 105 * min(g, 1.05), 130 - 105 * min(g, 1.05), x + 105 * min(g, 1.05), 130 + 105 * min(g, 1.05)), fill=GOLD); d.text((x, 128), a, font=font(BLACK, 58), fill=(30, 24, 40, 255), anchor="mm")
                text(c, b, 900, .5 + i * .7, 44, maxw=310, cx=x, lh=1.3, stagger=0)
            blit(c.fr, im, 0, 650, 1.0)
        elif name == "개띠":    # 말풍선
            for i, (a, b) in enumerate(s):
                yy = 640 + i * 240; g = e_back(cl((tt - (.3 + i * 1.1)) / .45)); left = i % 2 == 0; x0, x1 = (90, 830) if left else (250, 990)
                if g > 0:
                    im, d = lay(210); d.rounded_rectangle((x0, 10, x1, 190), 44, fill=GOLD if i == 1 else (255, 255, 255, 40), outline=GOLD, width=4)
                    tx = (x0 + 70) if left else (x1 - 70); d.polygon([(tx - 20, 188), (tx + 20, 188), (tx + (-30 if left else 30), 235)], fill=GOLD if i == 1 else (255, 255, 255, 60)); blit(c.fr, im, 0, yy, c.alpha(cl(g * 2)))
                text_in_box(c, f"{a}  {b}", (x0 + x1) // 2, yy + 100, .35 + i * 1.1, 44, 660, color=INK if i == 1 else WHITE, lh=1.25)
        elif name == "용띠":    # 계단
            im, d = lay(700)
            for i, (a, b) in enumerate(s):
                g = e_out(cl((tt - (.3 + i * .8)) / .5)); h = int((280 + i * 120) * g); x0 = 100 + i * 290
                d.rounded_rectangle((x0, 640 - h, x0 + 270, 640), 24, fill=GOLD if i == 2 else (255, 255, 255, 50), outline=GOLD, width=4)
            blit(c.fr, im, 0, 640, 1.0)
            for i, (a, b) in enumerate(s):
                h = 280 + i * 120; x0 = 100 + i * 290; ytop = 640 + 640 - h
                group_in_box(c, [(a, 52, GOLD if i != 2 else INK, 1.2), (b, 44, WHITE if i != 2 else INK, 1.25)], x0 + 135, (ytop + 1280) / 2, .6 + i * .8, 236, gap=14)
        else:                   # 뱀띠: 색 막대 목록
            for i, (a, b) in enumerate(s):
                yy = 650 + i * 190; g = e_out(cl((tt - (.3 + i * .7)) / .4))
                if g > 0:
                    im, d = lay(150); d.rounded_rectangle((90, 20, 108, 130), 9, fill=CORAL if i == 0 else (GOLD if i == 1 else (127, 214, 200, 255))); blit(c.fr, im, (1 - g) * 120, yy, c.alpha(g))
                text(c, f"{a}  {b}", yy + 14, .35 + i * .7, 48, maxw=720, cx=CX + 70, lh=1.25, stagger=0)
    return f
def S_cta2(name):
    def f(c):
        if name == "원숭이띠":    # ⑤ 숫자 반복
            text(c, "내 행운의 숫자, 5와 10은 어떤가요?", 505, .1, 48, maxw=840, stagger=0); text(c, "5 · 10 · 5 · 10", 660, .5, 150, color=GOLD, maxw=900, stagger=0); pill(c, 1.6, 930); prof(c, 1110, 2.2)
        elif name == "개띠":      # ② 댓글 질문 크게
            y = text(c, "올해 다시 읽어 볼\n약속은 무엇인가요?", 520, .1, 100, color=GOLD, maxw=840, lh=1.25); pill(c, 1.5, y + 50); prof(c, y + 220, 2.1)
        elif name == "용띠":      # ④ 한 줄 정리 + 팔로우
            text(c, "댓글로 올해 쌓을 것을 알려 주세요", 500, .1, 48, maxw=840, stagger=0); y = text(c, "단단하게\n쌓는 해", 620, .6, 92, color=GOLD, maxw=840, lh=1.25); pill(c, 1.4, y + 50); prof(c, y + 220, 2.0)
        else:                     # 뱀띠 ① 팔로우 카드(정월 없이)
            y = text(c, "올해 시작하고 끝낼 일은\n무엇인가요?", 540, .1, 64, maxw=840, lh=1.25); pill(c, 1.0, y + 70); prof(c, y + 250, 1.8)
    return f
_W, _C, _K, _T = S_why, S_cal, S_work, S_cta
def S_why(name): return S_why2(name) if name in NEW4 else _W(name)
def S_cal(name): return S_cal2(name) if name in NEW4 else _C(name)
def S_work(name): return S_work2(name) if name in NEW4 else _K(name)
def S_cta(name): return S_cta2(name) if name in NEW4 else _T(name)


# ───────── 장면 8개 일반 틀 (원숭이띠 10/7·용띠 10/8 대표 지적 -> R27~R32). 모든 글은 kbreak(뜻 단위 줄바꿈), 박스 안 글은 box_text(정중앙·넘치면 멈춤), 간격은 높이를 더해 직접 계산한다
class Lint(Exception): pass
def kbreak(s_, size, maxw, path=BLACK):
    """뜻 단위 줄바꿈(R27): 띄어쓰기(조사는 낱말에 붙어 있음)에서만 끊고, 마지막 줄 3글자 이하 금지, 줄 길이 균형(가장 짧은 줄 >= 가장 긴 줄의 60%)"""
    fnt = font(path, size); sp = fnt.getlength(" "); out = []
    for para in s_.split("\n"):
        w0 = para.split(" "); w = []; k0 = 0
        while k0 < len(w0):   # 붙여 쓰는 말: '~ㄹ 수 있어요'·'~ㄴ 것'은 한 덩어리로(중간에서 끊지 않는다)
            tok = w0[k0]
            if k0 + 1 < len(w0) and w0[k0 + 1] in ("수", "것"):
                tok += " " + w0[k0 + 1]; k0 += 1
                if k0 + 1 < len(w0) and w0[k0 + 1][:1] in ("있", "없"): tok += " " + w0[k0 + 1]; k0 += 1
            w.append(tok); k0 += 1
        n = len(w); Wd = [fnt.getlength(x) for x in w]
        if max(Wd) > maxw: raise Lint(f"낱말이 줄 너비보다 넓음: {para!r}")
        def wd(i, j): return sum(Wd[i:j]) + sp * (j - i - 1)
        L = 0; i = 0
        while i < n:
            j = i + 1
            while j < n and wd(i, j + 1) <= maxw: j += 1
            L += 1; i = j
        best = None; best_r = -1
        for LL in range(L, L + 3):
            tgt = wd(0, n) / LL if LL > 1 else 0; INF = 1e18; dp = [[INF] * (n + 1) for _ in range(LL + 1)]; pv = [[0] * (n + 1) for _ in range(LL + 1)]; dp[0][0] = 0
            for k in range(1, LL + 1):
                for j in range(1, n + 1):
                    for i in range(k - 1, j):
                        x = wd(i, j)
                        if x > maxw: continue
                        last = (k == LL and j == n); cost = (x - tgt) ** 2
                        if last and LL > 1 and len(" ".join(w[i:j])) <= 3: cost += 1e12
                        if dp[k - 1][i] + cost < dp[k][j]: dp[k][j] = dp[k - 1][i] + cost; pv[k][j] = i
            if dp[LL][n] >= INF: continue
            idx = [n]; j = n
            for k in range(LL, 0, -1): j = pv[k][j]; idx.append(j)
            idx = idx[::-1]; lines = [" ".join(w[idx[k]:idx[k + 1]]) for k in range(LL)]
            ws = [fnt.getlength(l) for l in lines]; ok = (len(lines) == 1) or (min(ws) >= .6 * max(ws) and len(lines[-1]) > 3)
            rr_ = (min(ws) / max(ws)) if len(lines) > 1 else 1
            if best is None or ok or rr_ > best_r: best, best_r = lines, rr_
            if ok: break
        out += best
    return out
def tw(lines, size, path=BLACK): fnt = font(path, size); return max(fnt.getlength(l) for l in lines)
def th_(s_, size, maxw=820, lh=1.3): return len(kbreak(s_, size, maxw)) * int(size * lh)
def tblock(c, s_, y, t0, size, maxw=820, color=WHITE, cx=CX, lh=1.3, stagger=0):
    lines = kbreak(s_, size, maxw); text(c, "\n".join(lines), y, t0, size, color=color, maxw=maxw + 80, cx=cx, lh=lh, stagger=stagger); return y + len(lines) * int(size * lh)
def box_text(c, s_, box, t0, size=48, color=WHITE, lh=1.3, padx=36, pady=28, minsize=44):
    """R28: 박스 안 글은 정중앙, 안쪽 여백 밖으로 나가면 만들기를 멈춘다"""
    x0, y0, x1, y1 = box; iw = x1 - x0 - 2 * padx; ih = y1 - y0 - 2 * pady; sz = size
    while True:
        lines = kbreak(s_, sz, iw); H = len(lines) * int(sz * lh)
        if tw(lines, sz) <= iw and H <= ih: break
        if sz <= minsize: raise Lint(f"박스 넘침(R28): {s_!r} 상자 {box} 글 {tw(lines, sz):.0f}x{H} > 안쪽 {iw}x{ih}")
        sz -= 2
    text(c, "\n".join(lines), (y0 + y1) / 2 - H / 2, t0, sz, color=color, maxw=iw + 80, cx=(x0 + x1) / 2, lh=lh, stagger=0)
def stack_top(heights, gaps):
    tot = sum(heights) + sum(gaps); y0 = 910 - tot / 2
    if y0 < 470 or y0 + tot > 1350: raise Lint(f"묶음이 범위를 벗어남(R21): 위 {y0:.0f} 아래 {y0 + tot:.0f}")
    return y0, tot
GG, GT = 60, 40     # 그림↔글 60px 이상, 글 덩어리 사이 40px 이상(R29)
Hg = 340            # 도형 층 높이(도형은 이 안에서 잘리지 않게)
CFG = {
 "원숭이띠": dict(hook="2027년에 원숭이띠에게\n무거운 일이 맡겨지는 건\n인정받는다는 뜻", years="1980·1992·2004·2016년생", shape="ring", hj="申", l1="불(丁)에 다듬어지는 쇠(申)", l2="무거운 일은 나를 단단하게 만드는 일이에요", nums=("5", "10"), lucky="5와 10은 흙의 숫자예요.\n흙이 쇠를 받쳐 줘요", cta="q", q="올해 가장 무겁게 맡은 책임은 무엇인가요?"),
 "용띠": dict(hook="2027년 용띠는\n크게 벌기보다 단단하게\n쌓는 게 맞는 해", years="1976·1988·2000·2012년생", shape="stack2", hj="辰", l1="같은 흙끼리 만나요", l2="흙은 쌓고 다지는 글자라\n기반을 다지기 좋아요", nums=("2", "7"), lucky="2와 7은 불의 숫자예요.\n불이 흙을 북돋아 줘요", cta="line", cm="댓글로 올해 쌓을 것을 알려 주세요", big="단단하게 쌓는 해"),
}

CFG.update({
 "개띠": dict(hook="2027년 개띠는\n말로 한 약속을\n한 번 더 확인하는 해", years="1982·1994·2006·2018년생", shape="pair2", l1="서로 조율이 필요한 사이", l2="맞춰 가면 약속이 단단해져요", nums=("2", "7"), lucky="2와 7은 불의 숫자예요.\n불이 흙을 북돋아 줘요", cta="big", q="올해 다시 읽어 볼 약속은\n무엇인가요?"),
 "뱀띠": dict(hook="2027년 뱀띠는\n의욕이 넘칠수록\n속도를 줄이는 해", years="1977·1989·2001·2013년생", shape="row3", l1="여름의 불로 함께 모여요", l2="의욕이 커지니 속도 조절이 필요해요", nums=("3", "8"), lucky="3과 8은 나무의 숫자예요.\n나무가 불을 키워 줘요", cta="q", q="올해 시작하고 끝낼 일은\n무엇인가요?"),
 "말띠": dict(hook="2027년 말띠는\n내년에 좋은 짝을\n만날 수 있는 해", years="1978·1990·2002·2014년생", shape="overlap", l1="겹치는 곳이 짝이에요", l2="午와 未는 짝이 되는 글자(육합)", nums=("3", "8"), lucky="3과 8은 나무의 숫자예요.\n나무가 불을 키워 줘요", cta="face", face="v3_ponytail", q="내년에 만나고 싶은 짝은\n어떤 사람인가요?"),
 "양띠": dict(hook="2027년 양띠는\n내 띠가 돌아와\n제자리 같아도 괜찮은 해", years="1979·1991·2003·2015년생", shape="eq", l1="내 띠가 돌아와요(본명년)", l2="2027년 丁未, 새로 시작하는 해예요", nums=("2", "7"), lucky="2와 7은 불의 숫자예요.\n불이 흙을 북돋아 줘요", cta="line", cm="댓글로 올해 정리할 것을 알려 주세요", big="정리부터 하면\n다시 서는 해"),
 "닭띠": dict(hook="2027년 닭띠는\n꼼꼼함이 드디어\n인정받는 해", years="1981·1993·2005·2017년생", shape="arrowjw", l1="불에 다듬어지는 보석", l2="꼼꼼함이 빛나는 해예요", nums=("5", "10"), lucky="5와 10은 흙의 숫자예요.\n흙이 쇠를 받쳐 줘요", cta="big", q="올해 가장\n인정받고 싶은 건\n무엇인가요?"),
 "돼지띠": dict(hook="2027년 돼지띠는\n사람을 통해\n돈이 들어오는 해", years="1983·1995·2007·2019년생", shape="tri", l1="세 글자가 한 팀(삼합)", l2="사람을 통해 돈과 기회가 들어와요", nums=("4", "9"), lucky="4와 9는 쇠의 숫자예요.\n쇠가 물을 키워 줘요", cta="face", face="v4_glasses", q="올해 도움 받고 싶은 일은\n무엇인가요?"),
 "쥐띠": dict(hook="2027년 쥐띠는\n돈은 들어오는데\n마음이 상하기 쉬운 해", years="1972·1984·1996·2008년생", shape="cross", l1="서로 서운하게 만드는 사이(해)", l2="子와 未는 해이면서 원진이에요", nums=("4", "9"), lucky="4와 9는 쇠의 숫자예요.\n쇠가 물을 키워 줘요", cta="q", q="서운한 마음을 마지막으로\n말한 건 언제인가요?"),
})

# ───────── 띠 릴스 기획서(10/8): 띠마다 장면 문구·캡션·트렌디 표현·연결 글을 한곳에 정한다. 영상과 기획서 화면이 같은 자료(CFG)를 쓴다
PLAN = {
 "원숭이띠": dict(rid="zodiac-21", date="10/22 낮", blog="n09 원숭이띠 운세", tags="#원숭이띠운세 #2027년운세 #정미년 #띠별운세 #사주", sub=None,
    lead="무거운 일이 맡겨지는 해, 책임이 인정으로 돌아오는 때가 언제인지 정리했어요."),
 "개띠": dict(rid="zodiac-25", date="10/24 낮", blog="n65 개띠 운세", tags="#개띠운세 #2027년운세 #정미년 #띠별운세 #사주", sub=None,
    lead="말로 한 약속을 한 번 더 확인하는 해, 언제 확인하면 좋은지 정리했어요."),
 "용띠": dict(rid="zodiac-11", date="10/29 낮", blog="n66 용띠 운세", tags="#용띠운세 #2027년운세 #정미년 #무지출챌린지 #사주", sub="무지출 챌린지처럼, 새는 곳부터 막는 해예요",
    lead="무지출 챌린지처럼 새는 곳부터 막고 쌓는 해, 언제 시작하면 좋은지 정리했어요."),
 "뱀띠": dict(rid="zodiac-13", date="10/31 낮", blog="n67 뱀띠 운세", tags="#뱀띠운세 #2027년운세 #정미년 #띠별운세 #사주", sub=None,
    lead="의욕이 넘칠수록 속도를 줄이는 해, 언제 힘을 쓰고 언제 쉬면 좋은지 정리했어요."),
 "말띠": dict(rid="zodiac-17", date="11/5 낮", blog="n59 말띠 운세", tags="#말띠운세 #2027년운세 #정미년 #띠별운세 #사주", sub=None,
    lead="내년에 좋은 짝을 만날 수 있는 해, 언제 마음을 열면 좋은지 정리했어요."),
 "양띠": dict(rid="zodiac-19", date="11/7 낮", blog="n04 양띠 운세", tags="#양띠운세 #2027년운세 #정미년 #갓생 #사주", sub="갓생은 정리부터, 비우고 나서 다시 서는 해예요",
    lead="갓생은 정리부터, 내 띠가 돌아오는 해에 언제 비우고 언제 세우면 좋은지 정리했어요."),
 "닭띠": dict(rid="zodiac-23", date="11/12 낮", blog="n68 닭띠 운세", tags="#닭띠운세 #2027년운세 #정미년 #띠별운세 #사주", sub=None,
    lead="꼼꼼함이 인정받는 해, 언제 실력을 보여 주면 좋은지 정리했어요."),
 "돼지띠": dict(rid="zodiac-27", date="11/13 저녁", blog="n49 돼지띠 운세", tags="#돼지띠운세 #2027년운세 #정미년 #띠별운세 #사주", sub=None,
    lead="사람을 통해 돈이 들어오는 해, 언제 사람을 만나면 좋은지 정리했어요."),
 "쥐띠": dict(rid="zodiac-03", date="11/14 낮", blog="n69 쥐띠 운세", tags="#쥐띠운세 #2027년운세 #정미년 #띠별운세 #사주", sub=None,
    lead="돈은 들어오는데 마음이 상하기 쉬운 해, 언제 조심하면 좋은지 정리했어요."),
}
# 문장 장면(3번): '~는 건 ~라는 뜻' 형식(대표 원숭이띠 지정)
CFG["개띠"]["hook"] = "2027년에 개띠에게\\n약속이 자꾸 엇갈리는 건\\n한 번 더 확인하라는 뜻"
CFG["용띠"]["hook"] = "2027년에 용띠가\\n크게 벌기보다 쌓게 되는 건\\n기반을 다지라는 뜻"
CFG["뱀띠"]["hook"] = "2027년에 뱀띠가\\n의욕이 넘치는 건\\n속도를 조절하라는 뜻"
CFG["말띠"]["hook"] = "2027년에 말띠에게\\n좋은 짝이 보이는 건\\n서로 끌리는 짝의 해라는 뜻"
CFG["양띠"]["hook"] = "2027년에 양띠가\\n제자리 같은 건\\n내 띠가 돌아와 다시 세우는 중이라는 뜻"
CFG["닭띠"]["hook"] = "2027년에 닭띠의\\n꼼꼼함이 드러나는 건\\n인정받는다는 뜻"
CFG["돼지띠"]["hook"] = "2027년에 돼지띠에게\\n돈이 사람을 통해 오는 건\\n연결의 해라는 뜻"
CFG["쥐띠"]["hook"] = "2027년에 쥐띠가\\n돈은 들어오는데 마음이 상하기 쉬운 건\\n오해를 줄이라는 뜻"
# 단정을 줄인 문구(R20·표현가이드 10번): '분명해요' 같은 확신 표현을 쓰지 않는다
OVER = {"쥐띠": {"money": ("돈이 들어올 기회가 보이는 해예요.", "가까운 사람과 돈이 섞이면 마음이 먼저 상해요.")}}
SUB = {n: p["sub"] for n, p in PLAN.items() if p["sub"]}
def two(sent): a = sent.split(". "); return (a[0] + ("." if not a[0].endswith(".") else ""), (a[1] if len(a) > 1 else ""))
def G_kw(name):
    t = T[name]; sub = SUB.get(name)
    def f(c):
        parts = [(f"2027 {name}", 58), (t["one"], 118)] + ([(sub, 44)] if sub else [])
        hs = [th_(a, b, 820, 1.25) for a, b in parts]; y0, tot = stack_top(hs, [GT] * (len(parts) - 1))
        y = tblock(c, parts[0][0], y0, .05, 58, color=GOLD, lh=1.25); y = tblock(c, parts[1][0], y + GT, .5, 118, lh=1.25)
        if sub: tblock(c, sub, y + GT, 1.2, 44, color=DIM, lh=1.25)
    return f
def G_years(name):
    cf = CFG[name]; ys = cf["years"].replace("년생", "").split("·"); big = f"{ys[0]}·{ys[1]}\n{ys[2]}·{ys[3]}년생"
    def f(c):
        h1 = th_(f"{name} 출생연도", 50, 820, 1.25); h2 = th_(big, 104, 820, 1.25); y0, tot = stack_top([h1, h2], [GT])
        y = tblock(c, f"{name} 출생연도", y0, .05, 50, color=GOLD, lh=1.25); tblock(c, big, y + GT, .3, 104, lh=1.25)
    return f
def G_hook(name):
    cf = CFG[name]
    def f(c):
        h = th_(cf["hook"], 74, 820, 1.3); y0, tot = stack_top([h], []); tblock(c, cf["hook"], y0, .1, 74, lh=1.3, stagger=.3)
    return f
def G_why(name):
    cf = CFG[name]
    def f(c):
        tt = c.t; ht = th_("왜 그럴까", 88, 820, 1.25); h1 = th_(cf["l1"], 58, 820, 1.25); h2 = th_(cf["l2"], 46, 800, 1.35)
        y0, tot = stack_top([ht, Hg, h1, h2], [GG, GG, GT]); y = tblock(c, "왜 그럴까", y0, .05, 88, lh=1.25)
        im, d = lay(Hg); cy = Hg // 2; g = lambda t0: e_back(cl((tt - t0) / .45))
        if cf["shape"] == "ring":
            r = 80 * min(g(.4), 1.05); pulse = 1 + .04 * math.sin(tt * 5)
            for k, w_ in enumerate((46, 30, 16)):
                rr_ = (r + 24 + k * 20) * pulse; d.ellipse((CX - rr_, cy - rr_, CX + rr_, cy + rr_), outline=(CORAL[0], CORAL[1], CORAL[2], 200 - k * 55), width=w_ // 4 + 2)
            circ(d, CX, cy, int(r), cf["hj"], GOLD, fg=(30, 24, 40, 255), fs=100)
        elif cf["shape"] == "stack2":   # 辰 위, 未 아래 같은 흙
            a, b = g(.4), g(1.0); circ(d, CX, 74, int(66 * min(a, 1.05)), "辰", (206, 168, 84, 120), GOLD, fs=66); circ(d, CX, Hg - 74, int(66 * min(b, 1.05)), "未", (206, 168, 84, 120), GOLD, fs=66)
            ln = e_out(cl((tt - 1.4) / .5)); d.line([(CX, 146), (CX, 146 + 48 * ln)], fill=GOLD, width=8)
        elif cf["shape"] == "pair2":    # 戌 ⇄ 未 서로 조율
            a, b = g(.4), g(.9); circ(d, CX - 240, cy, int(100 * min(a, 1.05)), "戌", (255, 255, 255, 30), GOLD, fs=96); circ(d, CX + 240, cy, int(100 * min(b, 1.05)), "未", (255, 255, 255, 30), GOLD, fs=96)
            ar = e_out(cl((tt - 1.2) / .5))
            if ar > 0: arrow(d, CX - 110, CX - 110 + 220 * ar, cy - 36, GOLD); arrow(d, CX + 110, CX + 110 - 220 * ar, cy + 36, CORAL)
        elif cf["shape"] == "row3":     # 巳 午 未 여름의 불
            for k, (x, hj) in enumerate(((CX - 290, "巳"), (CX, "午"), (CX + 290, "未"))):
                gg = g(.3 + k * .45)
                if gg > 0: circ(d, x, cy, int(100 * min(gg, 1.05)), hj, CORAL if hj == "午" else (255, 255, 255, 30), CORAL, fs=96)
            if tt > 1.3: d.rounded_rectangle((CX - 190, cy - 8, CX - 100, cy + 8), 8, fill=(255, 138, 115, 255)); d.rounded_rectangle((CX + 100, cy - 8, CX + 190, cy + 8), 8, fill=(255, 138, 115, 255))
        elif cf["shape"] == "overlap":  # 午 未 겹침
            L1 = Image.new("RGBA", (1080, Hg), (0, 0, 0, 0)); L2 = Image.new("RGBA", (1080, Hg), (0, 0, 0, 0)); d1 = ImageDraw.Draw(L1); d2 = ImageDraw.Draw(L2)
            a, b = g(.4), g(.9); r1 = int(130 * min(a, 1.05)); r2 = int(130 * min(b, 1.05))
            d1.ellipse((CX - 95 - r1, cy - r1, CX - 95 + r1, cy + r1), fill=(232, 193, 90, 90), outline=GOLD, width=6); d2.ellipse((CX + 95 - r2, cy - r2, CX + 95 + r2, cy + r2), fill=(244, 140, 4, 90), outline=(244, 140, 4, 255), width=6)
            im = Image.alpha_composite(L1, L2); d = ImageDraw.Draw(im)
            if a > .6: d.text((CX - 185, cy), "午", font=hj_font(104), fill=(255, 255, 255, 255), anchor="mm")
            if b > .6: d.text((CX + 185, cy), "未", font=hj_font(104), fill=(255, 255, 255, 255), anchor="mm")
        elif cf["shape"] == "eq":       # 未 = 未 본명년
            for k, x in enumerate((CX - 210, CX + 210)):
                gg = g(.4 + k * .5)
                if gg > 0: circ(d, x, cy, int(110 * min(gg, 1.05)), "未", (255, 255, 255, 30), GOLD, fs=104)
            ge = e_out(cl((tt - 1.1) / .4)); d.text((CX, cy - 2), "=", font=font(BLACK, 110), fill=(255, 255, 255, int(255 * ge)), anchor="mm")
        elif cf["shape"] == "arrowjw":  # 丁 → 酉
            g1, g2 = g(.4), g(1.2); circ(d, CX - 230, cy, int(105 * min(g1, 1.05)), "丁", CORAL, fg=(255, 255, 255, 255), fs=100) if g1 > 0 else None
            ar = e_out(cl((tt - .8) / .4)); arrow(d, CX - 100, CX - 100 + 200 * ar, cy, (255, 255, 255, 255)) if ar > 0 else None
            circ(d, CX + 230, cy, int(105 * min(g2, 1.05)), "酉", GOLD, fg=(30, 24, 40, 255), fs=100) if g2 > 0 else None
        elif cf["shape"] == "tri":      # 亥 卯 未 삼합
            pts = [(CX, 60, "亥"), (CX - 200, Hg - 70, "卯"), (CX + 200, Hg - 70, "未")]; prog = e_out(cl((tt - 1.3) / 1.2))
            for k, (a_, b_) in enumerate([(0, 1), (1, 2), (2, 0)]):
                sg = cl(prog * 3 - k)
                if sg > 0: d.line([(pts[a_][0], pts[a_][1]), (pts[a_][0] + (pts[b_][0] - pts[a_][0]) * sg, pts[a_][1] + (pts[b_][1] - pts[a_][1]) * sg)], fill=GOLD, width=7)
            for k, (x, yy, hj) in enumerate(pts):
                gg = g(.3 + k * .35)
                if gg > 0: circ(d, x, yy, int(58 * min(gg, 1.08)), hj, GOLD if hj == "未" else (255, 255, 255, 40), GOLD, fg=(30, 24, 40, 255) if hj == "未" else (255, 255, 255, 255), fs=58)
        else:                           # cross: 子 ✕ 未 서로 서운하게
            circ(d, CX - 230, cy, int(105 * min(g(.4), 1.05)), "子", (255, 255, 255, 30), GOLD, fs=100)
            x2 = e_out(cl((tt - .8) / .4)); a2 = int(255 * x2); d.line([(CX - 42, cy - 42), (CX + 42, cy + 42)], fill=(CORAL[0], CORAL[1], CORAL[2], a2), width=14); d.line([(CX + 42, cy - 42), (CX - 42, cy + 42)], fill=(CORAL[0], CORAL[1], CORAL[2], a2), width=14)
            gg = g(1.1)
            if gg > 0: circ(d, CX + 230, cy, int(105 * min(gg, 1.05)), "未", (255, 255, 255, 30), CORAL, fs=100)
        y = y + GG; blit(c.fr, im, 0, y, 1.0); y += Hg + GG
        y = tblock(c, cf["l1"], y, 1.6, 58, color=GOLD, lh=1.25); tblock(c, cf["l2"], y + GT, 2.1, 46, lh=1.35, maxw=800)
    return f
def G_cal(name):
    t = T[name]; good, save = t["good"], t["save"]
    def f(c):
        tt = c.t; im, d = lay(760); R = 290; cx_, cy_ = CX, 380
        up = lambda t0: e_out(cl((tt - t0) / .35)); ug, us = up(2.0), up(3.5)
        def lerp(a, b, u): return tuple(int(a[i] + (b[i] - a[i]) * u) for i in range(4))
        for i, m in enumerate(MONTHS):
            g = e_back(cl((tt - (.2 + i * .12)) / .35))
            if g <= 0: continue
            ang = -math.pi / 2 + i * math.pi / 6; x = cx_ + R * math.cos(ang); yy = cy_ + R * math.sin(ang); r = 50 * min(g, 1.05); fs_ = 44
            if m in good and ug > 0: r = 50 * (1 + .18 * ug); d.ellipse((x - r, yy - r, x + r, yy + r), fill=lerp((255, 255, 255, 26), GOLD, ug), outline=lerp((255, 255, 255, 190), GOLD, ug), width=5); col = lerp((255, 255, 255, 255), (30, 24, 40, 255), ug); fs_ = int(44 * (1 + .12 * ug))
            elif m in save and us > 0: r = 50 * (1 + .18 * us); d.ellipse((x - r, yy - r, x + r, yy + r), fill=(255, 255, 255, 26), outline=lerp((255, 255, 255, 190), CORAL, us), width=int(5 + 3 * us)); col = lerp((255, 255, 255, 255), CORAL, us); fs_ = int(44 * (1 + .12 * us))
            else: d.ellipse((x - r, yy - r, x + r, yy + r), fill=(255, 255, 255, 26), outline=(255, 255, 255, 190), width=5); col = (255, 255, 255, 255)
            d.text((x, yy - 2), ML(m), font=font(BLACK, fs_), fill=col, anchor="mm")
        d.text((cx_, cy_ - 52), "힘 쓸 달", font=font(BLACK, int(70 * (1 + .12 * ug))), fill=lerp((255, 255, 255, 255), GOLD, ug), anchor="mm")
        d.text((cx_, cy_ + 52), "아낄 달", font=font(BLACK, int(70 * (1 + .12 * us))), fill=lerp((255, 255, 255, 255), CORAL, us), anchor="mm")
        stack_top([760], []); blit(c.fr, im, 0, 910 - 380, 1.0)   # 그림 층 760px, 가운데 y 380이 y 910에 오게
    return f
def G_one(name, key, label):
    t = T[name]; l1, l2 = OVER.get(name, {}).get(key) or two(t[key])
    def f(c):
        h1 = th_(l1, 62, 820, 1.3); h2 = th_(l2, 50, 820, 1.3) if l2 else 0
        y0, tot = stack_top([280, h1] + ([h2] if l2 else []), [GG] + ([GT] if l2 else []))
        im, d = lay(280); g = e_back(cl((c.t - .1) / .45)); r = int(140 * min(g, 1.05))
        if r > 0: d.ellipse((CX - r, 140 - r, CX + r, 140 + r), fill=GOLD); d.text((CX, 136), label, font=font(BLACK, 110 if len(label) < 3 else 90), fill=(30, 24, 40, 255), anchor="mm")
        blit(c.fr, im, 0, y0, 1.0); y = tblock(c, l1, y0 + 280 + GG, .5, 62, lh=1.3)
        if l2: tblock(c, l2, y + GT, 1.1, 50, color=DIM, lh=1.3)
    return f
def G_lucky(name):
    cf = CFG[name]
    def f(c):
        ht = th_("행운의 숫자", 62, 820, 1.25); hl = th_(cf["lucky"], 52, 800, 1.35); y0, tot = stack_top([ht, 300, hl], [GG, GG]); y = tblock(c, "행운의 숫자", y0, .1, 62, color=GOLD, lh=1.25)
        im, d = lay(300)
        for x, n_, tg in ((CX - 190, cf["nums"][0], .3), (CX + 190, cf["nums"][1], .8)):
            g = e_back(cl((c.t - tg) / .45)); r = int(150 * min(g, 1.05))
            if r > 0: d.ellipse((x - r, 150 - r, x + r, 150 + r), fill=GOLD); d.text((x, 146), n_, font=font(BLACK, 150 if len(n_) == 1 else 130), fill=(30, 24, 40, 255), anchor="mm")
        blit(c.fr, im, 0, y + GG, 1.0); tblock(c, cf["lucky"], y + GG + 300 + GG, 1.5, 52, lh=1.35, maxw=800)
    return f
def G_cta(name):
    cf = CFG[name]
    def f(c):
        prof_t = "프로필 링크에서 생년월일 입력하고\n내 첫글자와 타고난 기운 알아보기"; hp = 140; hf = th_(prof_t, 44, 840, 1.4)
        if cf["cta"] == "q":
            hq = th_(cf["q"], 64, 840, 1.25); y0, tot = stack_top([hq, hp, hf], [GG, GT]); y = tblock(c, cf["q"], y0, .1, 64, lh=1.25); pill(c, 1.0, y + GG); tblock(c, prof_t, y + GG + hp + GT, 1.8, 44, color=DIM, lh=1.4, maxw=840)
        elif cf["cta"] == "big":
            hq = th_(cf["q"], 96, 840, 1.25); y0, tot = stack_top([hq, hp, hf], [GG, GT]); y = tblock(c, cf["q"], y0, .1, 96, color=GOLD, lh=1.25); pill(c, 1.5, y + GG); tblock(c, prof_t, y + GG + hp + GT, 2.1, 44, color=DIM, lh=1.4, maxw=840)
        elif cf["cta"] == "face":   # 정월이 나오는 마무리: 질문 -> 정월 -> 알약 -> 프로필 링크 (위치를 고정해 검산)
            hq = th_(cf["q"], 52, 840, 1.25); y = 487; tblock(c, cf["q"], y, .1, 52, lh=1.25); character(c, cf["face"], t0=.4, width=470, bottom=1042); pill(c, 1.2, 1057); tblock(c, prof_t, 1217, 1.9, 44, color=DIM, lh=1.4, maxw=840)
        else:
            hc = th_(cf["cm"], 48, 840, 1.25); hb = th_(cf["big"], 92, 840, 1.25); y0, tot = stack_top([hc, hb, hp, hf], [GT, GG, GT]); y = tblock(c, cf["cm"], y0, .1, 48, lh=1.25); y = tblock(c, cf["big"], y + GT, .6, 92, color=GOLD, lh=1.25); pill(c, 1.4, y + GG); tblock(c, prof_t, y + GG + hp + GT, 2.0, 44, color=DIM, lh=1.4, maxw=840)
    return f
GEN = tuple(CFG)
def zodiac_lint(names=None):
    """R27~R29 자동 검사: 장면마다 끝 상태를 그려 묶음의 위·아래 끝과 가운데를 재고(R21), 박스·줄바꿈·잘림 위반은 그리는 중에 Lint 예외로 잡는다"""
    import numpy as np; probs = []
    for n in (names or GEN):
        for i, (d_, fn) in enumerate(scenes_of(n)):
            try:
                fr = Image.new("RGB", (_CM.W, _CM.H), (0, 0, 0)); _CM.DY = 0; fn(Ctx(fr, d_ * .95, d_)); a = np.asarray(fr).astype("int32").sum(axis=2); ys = np.where((a > 45).sum(axis=1) > 2)[0]; lo, hi = int(ys.min()), int(ys.max()); mid = (lo + hi) / 2
                if lo < 470 or hi > 1350 or abs(mid - 910) > 15: probs.append(f"{n} 장면{i + 1}: 위 {lo} 아래 {hi} 가운데 {mid:.0f} (R21 범위 470~1350, 910±15)")
            except Lint as e: probs.append(f"{n} 장면{i + 1}: {e}")
    return probs
CTA_DUR = {"q": 3.8, "big": 4.1, "face": 3.9, "line": 4.0}
def scenes_of(name):
    """대표 10/8 지정 순서: 1 키워드 / 2 출생연도 / 3 문장 / 4 왜 그럴까 / 5 힘 쓸 달·아낄 달 / 6 돈 / 7 일 / 8 사람 / 9 행운의 숫자 / 10 마무리. 길이는 R13(문장 2초·낱말 1초 이상): 마지막 글이 나온 뒤 2초 이상 남게"""
    return [(2.6, G_kw(name)), (2.4, G_years(name)), (2.8, G_hook(name)), (4.3, G_why(name)), (5.0, G_cal(name)), (3.2, G_one(name, "money", "돈")), (3.2, G_one(name, "work", "일")), (3.2, G_one(name, "people", "사람")), (3.6, G_lucky(name)), (CTA_DUR[CFG[name]["cta"]], G_cta(name))]
def build_generic(name, outdir):
    probs = zodiac_lint([name])
    if probs: raise Lint("레이아웃 검사에서 멈춤: " + " / ".join(probs))
    SC2 = scenes_of(name); p, dur = render(name, SC2, outdir); mi = MP.choose("data", f"zodiac-{name}"); MP.mux(p, [x for x, _ in SC2], mi, 700 + len(name))
    still(SC2, 0, 2.4, os.path.join(outdir, name + "_cover.jpg")); print("완료", name, round(dur, 1), "초 · 장면", len(SC2), "· 음악", mi["style"], mi["bpm"]); return p

def build(name, outdir):
    if name in GEN: return build_generic(name, outdir)
    SC = [(2.8, S_hook(name)), (4.2, S_why(name)), (5.4, S_cal(name)), (5.2, S_work(name)), (4.4, S_cta(name))]
    if name in ("말띠", "돼지띠"): pass
    SC2 = [(d, autofit(fn, d)) if (i < 4 or name not in ("말띠", "돼지띠")) else (d, fn) for i, (d, fn) in enumerate(SC)]   # 정월이 아래에 붙는 마무리(말띠·돼지띠)만 자동 맞춤에서 뺀다
    p, dur = render(name, SC2, outdir); mi = MP.choose("data", f"zodiac-{name}"); MP.mux(p, [x for x, _ in SC2], mi, 700 + len(name))
    still(SC2, 0, 2.6, os.path.join(outdir, name + "_cover.jpg"))
    print("완료", name, round(dur, 1), "초 · 음악", mi["style"], mi["bpm"]); return p
if __name__ == "__main__":
    out = os.path.join(ROOT, "2026-motion", "zodiac"); names = sys.argv[1:] or ["말띠", "양띠", "닭띠", "돼지띠", "쥐띠"]
    for n in names: build(n, out)
