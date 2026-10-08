"""2027 띠 릴스 5편 새 틀 제작(10/7 대표 승인: 옛 v3 방식(명조·검은 바탕·작은 글씨) -> 새 틀로 같은 칸 덮어쓰기). 구성 그림: https://claude.ai/artifact/CSAxkf1JuXZNMQJssNi5MS
편마다 달력 장면·돈 일 사람 장면·마무리를 다르게(R19). 데이터는 build_2026-w42.py의 T(기존 띠 글과 같은 값)만 쓴다. 정월은 말띠·돼지띠 마무리에만(R03).
장면: 표지(훅) -> 왜 그럴까 -> 힘 쓸 달·아낄 달 -> 돈·일·사람 -> 마무리. 사용: python3 content/clips_motion_zodiac.py [이름 ...] -> 2026-motion/zodiac/<이름>.mp4 + _cover.jpg"""
import sys, os, math, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "..")); sys.path.insert(0, os.path.join(ROOT, "pipeline"))
from clip_motion import *
import fonts_kit as _FK, music_plan as MP
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


# ───────── 원숭이띠 재구성 (10/7 대표 지적): 장면 8개 - 표지(키워드·출생연도·문장) / 왜 그럴까 / 힘 쓸 달·아낄 달 / 돈 / 일 / 사람 / 행운의 숫자 / 마무리
MK = T["원숭이띠"]
def M_cover(c):
    t = MK; hook = "2027년에 원숭이띠에게\n무거운 일이 맡겨지는 건\n인정받는다는 뜻"
    H = 62 + 12 + 118 + 24 + 52 + 34 + text_h(hook, 54, 820, 1.3); y0 = 910 - H / 2
    y = text(c, "2027 원숭이띠", y0, .05, 58, color=GOLD, maxw=820, stagger=0)
    y = text(c, "책임과 인정", y + 6, .3, 118, maxw=820, stagger=0)
    y = text(c, "1980·1992·2004·2016년생", y + 20, 1.0, 50, color=DIM, maxw=820, stagger=0)
    text(c, hook, y + 36, 1.6, 54, maxw=820, lh=1.3, stagger=.25)
def M_why(c):
    tt = c.t; y = title(c, "왜 그럴까"); im, d = lay(520); Y0 = 540
    r = 125 * min(e_back(cl((tt - .4) / .45)), 1.05); pulse = 1 + .045 * math.sin(tt * 5)
    for k, w_ in enumerate((46, 30, 16)):
        rr_ = (r + 30 + k * 26) * pulse; d.ellipse((CX - rr_, 250 - rr_, CX + rr_, 250 + rr_), outline=(CORAL[0], CORAL[1], CORAL[2], 200 - k * 55), width=w_ // 4 + 2)
    circ(d, CX, 250, int(r), "申", GOLD, fg=(30, 24, 40, 255), fs=140); blit(c.fr, im, 0, Y0, 1.0)
    text(c, "불(丁)에 다듬어지는 쇠(申)", 1080, 1.5, 58, color=GOLD, maxw=840, stagger=0)
    text(c, "무거운 일은 나를 단단하게 만드는 일이에요", 1170, 2.0, 46, maxw=800, lh=1.35, stagger=0)
def M_cal(c):
    tt = c.t; good, save = MK["good"], MK["save"]; im, d = lay(900); Y0 = 460; R = 300; cx_, cy_ = CX, 450; fm = font(BLACK, 44)
    up = lambda t0: e_out(cl((tt - t0) / .35))
    ug, us = up(2.7), up(4.4)                      # 힘 쓸 달 / 아낄 달 글자가 색이 바뀌는 순서
    def lerp(a, b, u): return tuple(int(a[i] + (b[i] - a[i]) * u) for i in range(4))
    for i, m in enumerate(MONTHS):
        g = e_back(cl((tt - (.2 + i * .12)) / .35))
        if g <= 0: continue
        ang = -math.pi / 2 + i * math.pi / 6; x = cx_ + R * math.cos(ang); yy = cy_ + R * math.sin(ang); r = 50 * min(g, 1.05)
        if m in good and ug > 0: r = 50 * (1 + .18 * ug); d.ellipse((x - r, yy - r, x + r, yy + r), fill=lerp((255, 255, 255, 26), GOLD, ug), outline=lerp((255, 255, 255, 190), GOLD, ug), width=5); col = lerp((255, 255, 255, 255), (30, 24, 40, 255), ug)
        elif m in save and us > 0: r = 50 * (1 + .18 * us); d.ellipse((x - r, yy - r, x + r, yy + r), fill=(255, 255, 255, 26), outline=lerp((255, 255, 255, 190), CORAL, us), width=int(5 + 3 * us)); col = lerp((255, 255, 255, 255), CORAL, us)
        else: d.ellipse((x - r, yy - r, x + r, yy + r), fill=(255, 255, 255, 26), outline=(255, 255, 255, 190), width=5); col = (255, 255, 255, 255)
        d.text((x, yy - 2), ML(m), font=font(BLACK, int(44 * r / 50) if r > 50 else 44), fill=col, anchor="mm")
    g_sz = int(70 * (1 + .12 * ug)); s_sz = int(70 * (1 + .12 * us))
    d.text((cx_, cy_ - 52), "힘 쓸 달", font=font(BLACK, g_sz), fill=lerp((255, 255, 255, 255), GOLD, ug), anchor="mm")
    d.text((cx_, cy_ + 52), "아낄 달", font=font(BLACK, s_sz), fill=lerp((255, 255, 255, 255), CORAL, us), anchor="mm")
    blit(c.fr, im, 0, Y0, 1.0)
def M_one(key, label, line1, line2):
    def f(c):
        im, d = lay(320); g = e_back(cl((c.t - .1) / .45)); r = int(140 * min(g, 1.05))
        if r > 0: d.ellipse((CX - r, 160 - r, CX + r, 160 + r), fill=GOLD); d.text((CX, 156), label, font=font(BLACK, 110), fill=(30, 24, 40, 255), anchor="mm")
        blit(c.fr, im, 0, 520, 1.0); y = text(c, line1, 880, .5, 62, maxw=820, lh=1.3, stagger=0); text(c, line2, y + 24, 1.1, 50, color=DIM, maxw=820, lh=1.3, stagger=0)
    return f
def M_lucky(c):
    im, d = lay(360); a = e_back(cl((c.t - .3) / .45)); b = e_back(cl((c.t - .8) / .45))
    d.text((CX, 40), "행운의 숫자", font=font(BLACK, 62), fill=GOLD, anchor="mm")
    for x, n_, g in ((CX - 190, "5", a), (CX + 190, "10", b)):
        r = int(150 * min(g, 1.05))
        if r > 0: d.ellipse((x - r, 210 - r, x + r, 210 + r), fill=GOLD); d.text((x, 206), n_, font=font(BLACK, 150 if len(n_) == 1 else 130), fill=(30, 24, 40, 255), anchor="mm")
    blit(c.fr, im, 0, 520, 1.0); text(c, "5와 10은 흙의 숫자예요. 흙이 쇠를 받쳐 줘요", 960, 1.5, 52, maxw=800, lh=1.35, stagger=0)
def M_cta(c):
    y = text(c, "올해 가장 무겁게 맡은\n책임은 무엇인가요?", 540, .1, 64, maxw=840, lh=1.25); pill(c, 1.0, y + 70); prof(c, y + 250, 1.8)
def build_monkey(outdir):
    name = "원숭이띠"; SC = [(2.6, M_cover), (3.2, M_why), (5.2, M_cal), (2.4, M_one("돈", "돈", MK["money"].split(". ")[0] + ".", MK["money"].split(". ")[1])), (2.4, M_one("일", "일", MK["work"].split(". ")[0] + ".", MK["work"].split(". ")[1])), (2.4, M_one("사람", "사람", MK["people"].split(". ")[0] + ".", MK["people"].split(". ")[1])), (3.0, M_lucky), (3.6, M_cta)]
    SC2 = [(d, autofit(fn, d)) for d, fn in SC]
    p, dur = render(name, SC2, outdir); mi = MP.choose("data", f"zodiac-{name}"); MP.mux(p, [x for x, _ in SC2], mi, 700 + len(name))
    still(SC2, 0, 2.4, os.path.join(outdir, name + "_cover.jpg")); print("완료", name, round(dur, 1), "초 · 장면", len(SC2), "· 음악", mi["style"], mi["bpm"]); return p

def build(name, outdir):
    if name == "원숭이띠": return build_monkey(outdir)
    SC = [(2.8, S_hook(name)), (4.2, S_why(name)), (5.4, S_cal(name)), (5.2, S_work(name)), (4.4, S_cta(name))]
    if name in ("말띠", "돼지띠"): pass
    SC2 = [(d, autofit(fn, d)) if (i < 4 or name not in ("말띠", "돼지띠")) else (d, fn) for i, (d, fn) in enumerate(SC)]   # 정월이 아래에 붙는 마무리(말띠·돼지띠)만 자동 맞춤에서 뺀다
    p, dur = render(name, SC2, outdir); mi = MP.choose("data", f"zodiac-{name}"); MP.mux(p, [x for x, _ in SC2], mi, 700 + len(name))
    still(SC2, 0, 2.6, os.path.join(outdir, name + "_cover.jpg"))
    print("완료", name, round(dur, 1), "초 · 음악", mi["style"], mi["bpm"]); return p
if __name__ == "__main__":
    out = os.path.join(ROOT, "2026-motion", "zodiac"); names = sys.argv[1:] or ["말띠", "양띠", "닭띠", "돼지띠", "쥐띠"]
    for n in names: build(n, out)
