"""2027 정미년 하늘 일정 영상 '수성이 거꾸로 가는 날, 딱 세 번'(10/7, 대표 승인: C안 · 중심 문구 = 수성 역행 3번이 불의 삼합 달에 있다 · 해석은 정월의 한마디).
데이터: 자오선 엔진(스위스 에페메리스·절기 계산)을 NASA 일식 일정과 외부 천문 달력으로 대조했다. 모든 날짜는 한국시간.
 수성 역행 2/10~3/3 · 6/11~7/4 · 10/8~10/28 / 일식 2/7(금환)·8/2(개기) / 사주 월 경계(절입): 寅월 2/4~3/5 · 午월 6/6~7/6 · 戌월 10/8~11/7
형태: 세로 12개월 노선도(막대가 자람) → 삼각형 도식(寅·午·戌) → 정월의 한마디 → 댓글 질문 → 한 줄 정리+팔로우.
사용: python3 content/clips_motion_2027.py -> 2026-motion/sky_2027.mp4"""
import sys, os, math, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "..")); sys.path.insert(0, os.path.join(ROOT, "pipeline"))
from clip_motion import *
import fonts_kit as _FK, music_plan as MP
CORAL = (255, 138, 115, 255); TEAL = (127, 214, 200, 255)
DAYS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
RETRO = [((2, 10), (3, 3)), ((6, 11), (7, 4)), ((10, 8), (10, 28))]       # 수성 역행(한국시간)
ECL = [(2, 7), (8, 2)]                                                       # 일식
def lay(h=900): im = Image.new("RGBA", (1080, h), (0, 0, 0, 0)); return im, ImageDraw.Draw(im)
def S_hook(c):
    H = text_h("2027년", 140, 820, 1.2) + text_h("수성이 거꾸로 가는 날", 92, 820, 1.25) + text_h("딱 세 번이에요", 124, 820, 1.2) + 40 + text_h("날짜로 알려 드려요", 56, 820, 1.4); y0 = 910 - H / 2
    y = text(c, "2027년", y0, .1, 140, color=GOLD, maxw=820, lh=1.2); y = text(c, "수성이 거꾸로 가는 날", y, .5, 92, maxw=820, lh=1.25); y = text(c, "딱 세 번이에요", y, 1.0, 124, color=GOLD, maxw=820, lh=1.2); text(c, "날짜로 알려 드려요", y + 40, 1.6, 56, color=DIM, maxw=820)
def S_map(c):
    t = c.t; TOP = 500; RH = 68; X0, X1 = 190, 880; W = X1 - X0
    text(c, "2027 수성 역행 · 일식", 415, .05, 56, maxw=840, stagger=0)
    im, d = lay(1000); f44 = font(BLACK, 44); f40 = font(BLACK, 40)
    def fx(m, day, end=False): return X0 + W * ((day if end else day - 1) / DAYS[m - 1])
    for i in range(12):
        p = e_out(cl((t - (.2 + i * .09)) / .3)); a = int(255 * p); y = (TOP - 480) + i * RH + RH // 2
        hot = (i + 1) in (2, 3, 6, 7, 10)
        d.text((70, y), f"{i + 1}월", font=f44, fill=(GOLD[0], GOLD[1], GOLD[2], a) if hot else (235, 238, 246, int(a * .78)), anchor="lm")
        d.rounded_rectangle((X0, y - 3, X1, y + 3), radius=3, fill=(255, 255, 255, int(a * .22)))
    segs = [(2, 10, 28, "2/10 시작", .0, 2.0), (3, 1, 3, "3/3 끝", .0, 2.0), (6, 11, 30, "6/11 시작", .0, 3.0), (7, 1, 4, "7/4 끝", .0, 3.0), (10, 8, 28, "10/8~10/28", .0, 4.0)]
    for (m, a0, a1, lab, _, ts) in segs:
        g = e_out(cl((t - ts - (.45 if m in (3, 7) else 0)) / .5))
        if g <= 0: continue
        y = (TOP - 480) + (m - 1) * RH + RH // 2; x0 = fx(m, a0); x1 = x0 + (fx(m, a1, True) - x0) * g
        d.rounded_rectangle((x0, y - 25, max(x0 + 8, x1), y + 25), radius=25, fill=CORAL)
        if m in (3, 7):
            d.text((x1 + 14, y), lab, font=f40, fill=(255, 255, 255, int(255 * g)), anchor="lm")
        elif g > .85: d.text((x0 + 16, y), lab, font=f40, fill=(26, 20, 30, 255), anchor="lm")
    for k, (m, day) in enumerate(ECL):
        g = e_back(cl((t - (1.7 + k * 1.7)) / .4))
        if g <= 0: continue
        y = (TOP - 480) + (m - 1) * RH + RH // 2; x = fx(m, day) + 4; r = 24 * min(g, 1.1)
        d.ellipse((x - r, y - r, x + r, y + r), fill=(12, 12, 20, 255), outline=GOLD, width=5)
    lg = e_out(cl((t - 4.4) / .4)); yL = (TOP - 480) + 12 * RH + 24
    d.rounded_rectangle((70, yL - 14, 118, yL + 14), radius=14, fill=(CORAL[0], CORAL[1], CORAL[2], int(255 * lg))); d.text((132, yL), "수성 역행", font=f44, fill=(255, 255, 255, int(255 * lg)), anchor="lm")
    d.ellipse((430, yL - 17, 464, yL + 17), fill=(12, 12, 20, int(255 * lg)), outline=(GOLD[0], GOLD[1], GOLD[2], int(255 * lg)), width=4); d.text((478, yL), "일식", font=f44, fill=(255, 255, 255, int(255 * lg)), anchor="lm")
    blit(c.fr, im, 0, 480, 1.0)
def S_trine(c):
    t = c.t; y0 = text(c, "세 번 모두", 415, .05, 84, maxw=840, stagger=0)
    text(c, "사주에서 '불의 삼합' 달이에요", y0 - 6, .45, 60, color=DIM, maxw=840, stagger=0)
    pts = [(CX, 760, "午", "6월"), (CX - 270, 1170, "寅", "2월"), (CX + 270, 1170, "戌", "10월")]
    im, d = lay(1000); R = 108; fh = font(_FK.P["serif"], 118); fm = font(BLACK, 58)
    prog = e_out(cl((t - 1.4) / 1.4)); order = [(0, 1), (1, 2), (2, 0)]
    for k, (a, b) in enumerate(order):
        seg = cl(prog * 3 - k)
        if seg <= 0: continue
        xa, ya = pts[a][0], pts[a][1] - 480; xb, yb = pts[b][0], pts[b][1] - 480
        d.line([(xa, ya), (xa + (xb - xa) * seg, ya + (yb - ya) * seg)], fill=(GOLD[0], GOLD[1], GOLD[2], 255), width=8)
    for k, (x, y, hj, mo) in enumerate(pts):
        g = e_back(cl((t - (.5 + k * .35)) / .45))
        if g <= 0: continue
        r = R * min(g, 1.08); yy = y - 480
        d.ellipse((x - r, yy - r, x + r, yy + r), fill=(CORAL[0], CORAL[1], CORAL[2], 255), outline=(255, 235, 200, 255), width=5)
        d.text((x, yy - 4), hj, font=fh, fill=(40, 20, 28, 255), anchor="mm"); d.text((x, yy + R + 56), mo, font=fm, fill=(255, 255, 255, int(255 * cl(g))), anchor="mm")
    blit(c.fr, im, 0, 480, 1.0)
    cen = e_out(cl((t - 2.9) / .5))
    if cen > 0: text(c, "수성 역행", 950, 2.9, 70, color=GOLD, maxw=600, stagger=0)
def S_hanmadi(c):
    body = "불의 해에 불의 달마다\n수성이 돌아와요.\n말과 약속은 한 번 더\n확인해 보세요."; note = "재미로 보는 풀이예요"
    bw = 840; pad = 40; hb = text_h(body, 62, bw - 2 * pad, 1.36); H = pad + 66 + 12 + hb + 18 + int(44 * 1.3) + pad; top = 418
    p = e_back((c.t - .1) / .5); card = rr(bw, H, (26, 33, 54, 238), GOLD, r=44, ow=3); blit(c.fr, card, CX - bw / 2 - 4, top - 4 + (1 - e_out(p)) * 40, c.alpha(cl(p * 2)))
    text(c, "정월의 한마디", top + pad, .5, 54, color=GOLD, maxw=bw - 2 * pad, stagger=0); y = top + pad + 66 + 12
    text(c, body, y, .9, 62, maxw=bw - 2 * pad, lh=1.36, stagger=.3); text(c, note, y + hb + 18, 2.2, 44, color=DIM, maxw=bw - 2 * pad, stagger=0)
    character(c, "v6_winter", t0=.3, width=600)
def S_ctaA(c):
    H = text_h("어느 달이 가장\n궁금하세요?", 104, 820, 1.3) + 48 + int(72 * 1.3); y0 = 910 - H / 2
    y = text(c, "어느 달이 가장\n궁금하세요?", y0, .1, 104, maxw=820, lh=1.3); text(c, "댓글로 알려 주세요", y + 48, .7, 72, color=GOLD)
def S_ctaB(c):
    t0 = .1; Htot = int(96 * 1.3) + 30 + int(60 * 1.3) + 56 + int(52 * 1.4) * 2 + 40 + 124; y = 910 - Htot / 2
    y = text(c, "수성 역행 세 번,\n불의 삼합 달", y, t0, 96, color=GOLD, maxw=820, lh=1.25)
    y = text(c, "팔로우하고 더 많은 이야기 나눠요", y + 30, t0 + .6, 60, maxw=830, lh=1.3)
    y = text(c, "내 일간 12개월은 프로필 링크에서\n생년월일 입력하고 확인해 보세요", y + 56, t0 + 1.2, 52, color=DIM, maxw=830, lh=1.4)
    fnt = font(BLACK, 58); pl = "＋ 팔로우"; pw = int(fnt.getlength(pl)) + 100; im = Image.new("RGBA", (pw + 20, 140), (0, 0, 0, 0)); d = ImageDraw.Draw(im); d.rounded_rectangle((10, 10, 10 + pw, 130), radius=60, fill=GOLD); d.text((10 + pw / 2, 71), pl, font=fnt, fill=INK, anchor="mm")
    q = e_back((c.t - t0 - 1.9) / .45); pulse = 1 + .03 * math.sin(c.t * 6); L = im.resize((int(im.width * pulse), int(im.height * pulse))); blit(c.fr, L, CX - L.width / 2, y + 40 + (1 - e_out(q)) * 40, c.alpha(cl(q * 2)))
SC = [(2.8, S_hook), (5.6, S_map), (4.4, S_trine), (4.4, S_hanmadi), (2.2, S_ctaA), (3.2, S_ctaB)]
if __name__ == "__main__":
    out = os.path.join(ROOT, "2026-motion"); p, d = render("sky_2027", SC, out); mi = MP.choose("data", "sky-2027"); MP.mux(p, [x for x, _ in SC], mi, 321)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", "1.0", "-i", p, "-frames:v", "1", os.path.join(out, "sky_2027_thumb.png")], check=True); print("완료", round(d, 1), "초 · 음악", mi["style"], mi["bpm"])
