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
                text(c, f"{a}  {b}", yy + 6, .35 + i * .7, 52, maxw=700, cx=CX + 100, lh=1.25, stagger=0)
        elif name == "양띠":  # 카드 뒤집기
            for i, (a, b) in enumerate(s):
                yy = 640 + i * 230; p = cl((tt - (.3 + i * 1.3)) / .55); w = int(780 * abs(math.cos((1 - e_out(p)) * math.pi / 2)))
                im = Image.new("RGBA", (1080, 200), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
                if p < .5: d.rounded_rectangle((CX - w // 2, 10, CX + w // 2, 190), 30, fill=(255, 255, 255, 28), outline=(255, 255, 255, 120), width=4)
                else: d.rounded_rectangle((CX - w // 2, 10, CX + w // 2, 190), 30, fill=GOLD if i == 0 else (255, 255, 255, 40), outline=GOLD, width=4)
                blit(c.fr, im, 0, yy, 1.0)
                if p > .85: text(c, f"{a}  {b}", yy + 48, 0, 46, color=INK if i == 0 else WHITE, maxw=700, stagger=0, lh=1.2)
        elif name == "닭띠":  # 좌우 비교
            g = e_back(cl((tt - .3) / .5)); im, d = lay(520)
            d.rounded_rectangle((70, 20, 520, 500), 30, fill=GOLD); d.rounded_rectangle((560, 20, 1010, 500), 30, outline=CORAL, width=7); blit(c.fr, im, 0, 620, c.alpha(cl(g * 2)))
            text(c, "좋은 신호", 650, .5, 52, color=INK, maxw=400, cx=295, stagger=0)
            text(c, f"{s[0][1]}\n{s[1][1]}", 740, .9, 44, color=INK, maxw=390, cx=295, lh=1.35, stagger=.3)
            text(c, "조심", 650, 1.6, 52, color=CORAL, maxw=400, cx=785, stagger=0)
            text(c, s[2][1], 740, 2.0, 44, maxw=390, cx=785, lh=1.35, stagger=0)
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
def build(name, outdir):
    SC = [(2.8, S_hook(name)), (4.2, S_why(name)), (5.4, S_cal(name)), (5.2, S_work(name)), (4.4, S_cta(name))]
    if name in ("말띠", "돼지띠"): pass
    SC2 = [(d, autofit(fn, d)) if (i < 4 or name not in ("말띠", "돼지띠")) else (d, fn) for i, (d, fn) in enumerate(SC)]   # 정월이 아래에 붙는 마무리(말띠·돼지띠)만 자동 맞춤에서 뺀다
    p, dur = render(name, SC2, outdir); mi = MP.choose("data", f"zodiac-{name}"); MP.mux(p, [x for x, _ in SC2], mi, 700 + len(name))
    still(SC2, 0, 2.6, os.path.join(outdir, name + "_cover.jpg"))
    print("완료", name, round(dur, 1), "초 · 음악", mi["style"], mi["bpm"]); return p
if __name__ == "__main__":
    out = os.path.join(ROOT, "2026-motion", "zodiac"); names = sys.argv[1:] or ["말띠", "양띠", "닭띠", "돼지띠", "쥐띠"]
    for n in names: build(n, out)
