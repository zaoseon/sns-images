"""모션그래픽 견본 M2 '100명 점 격자 + 숫자 카운트업'(10/5 대표: 모션그래픽도 기획에 넣는다).
데이터는 content/cross_data/README.md의 실제 값: 한 축에 모인 체계 수 2개 61.0% / 3개 32.2% / 4개 이상 5.3%(나머지 약 1.5%는 흩어짐). 100명 기준 반올림.
사용: python3 pipeline/motion_dots.py -> 2026-motion/dots_cross.mp4"""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import pick_reel as PK, clip_motion as M
from PIL import Image, ImageDraw
CX = M.CX; BOLD = PK.BOLD
GOLDC = (231, 200, 141); TEAL = (127, 214, 200); CORAL = (255, 138, 115); GRAY = (120, 124, 140)
GROUPS = [("둘", 61, GOLDC), ("셋", 32, TEAL), ("넷 이상", 5, CORAL), ("흩어짐", 2, GRAY)]
def layer_text(txt, size, color, path=BOLD):
    f = M.font(path, size); w = int(f.getlength(txt)) + 24; im = Image.new("RGBA", (w, int(size * 1.4)), (0, 0, 0, 0)); ImageDraw.Draw(im).text((12, 4), txt, font=f, fill=color + (255,)); return im
def dot_layer(col, r=30, glow=False):
    s = r * 2 + (40 if glow else 4); im = Image.new("RGBA", (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    if glow:
        for k, a in ((18, 40), (12, 70), (6, 110)): d.ellipse((s / 2 - r - k, s / 2 - r - k, s / 2 + r + k, s / 2 + r + k), fill=col + (a,))
    d.ellipse((s / 2 - r, s / 2 - r, s / 2 + r, s / 2 + r), fill=col + (255,)); return im
def build():
    def s1(c):
        M.chip(c, "정월의 숫자 퀴즈", 345, .05)
        y = PK.title(c, "나랑 같은 말을 하는\n*운명학*, 몇 개일까요?", 445, .2, 104)
        PK.small(c, "먼저 답을 골라 보세요", y + 10, .9, 48, PK.GOLDA); M.character(c, "v2_straight", t0=.3, width=730, bottom=1455, dx=-60)
    def s2(c):
        PK.title(c, "여섯 운명학 중\n한 곳에 모인 수는?", 420, .05, 96)
        for i, (lab, col) in enumerate((("둘", GOLDC), ("셋", TEAL), ("넷 이상", CORAL))):
            cy = 860 + i * 190; t0 = .35 + i * .18; p = M.e_back((c.t - t0) / .45)
            if p > 0.02:
                pill = M.rr(760, 150, col + (255,), None, r=75); M.pop(c, pill, CX, cy, t0, a=1.0)
                M.text(c, f"{i+1}   {lab}", cy - 52, t0 + .1, 70, color=(20, 20, 30, 255), path=BOLD, maxw=700, stagger=0)
        PK.small(c, "고른 번호를 댓글로 남겨 주세요", 1400, 1.4, 44, PK.GOLDA)
    def s3(c):
        M.text(c, "100명 중", 345, .05, 72, color=(255, 255, 255, 255), path=BOLD, maxw=800, stagger=0)
        x0, y0, cell = CX - 390 + 39, 640, 76; idx = 0; starts = [.3, 2.0, 3.4, 4.3]; durs = [1.5, 1.2, .8, .4]; cur = None; shown = {}
        for gi, (lab, n, col) in enumerate(GROUPS):
            for k in range(n):
                t0 = starts[gi] + durs[gi] * k / n; p = M.e_back((c.t - t0) / .28)
                r, cc = divmod(idx, 10); idx += 1
                if p > .02:
                    s = max(.02, min(p, 1.15)); L = dot_layer(col, int(30 * s) if s != 1 else 30, glow=(gi == 2 and c.t > 4.9)); M.blit(c.fr, L, x0 + cc * cell - L.width / 2, y0 + r * cell - L.height / 2, c.alpha(M.cl(p * 2)))
            if c.t >= starts[gi]: cur = gi; shown[gi] = int(round(n * M.cl((c.t - starts[gi]) / durs[gi])))
        if cur is not None:
            lab, n, col = GROUPS[cur]; v = shown[cur]
            L = layer_text(f"{lab} {v}명" if lab != "흩어짐" else f"{lab} {v}명", 96 if cur != 2 else 108, col); M.blit(c.fr, L, CX - L.width / 2, 452, c.alpha(1))
        lx = 90
        for gi in range(4):
            if c.t >= starts[gi] + durs[gi]:
                lab, n, col = GROUPS[gi]; d = dot_layer(col, 16); M.blit(c.fr, d, lx, 1402, c.alpha(1)); T = layer_text(f"{lab} {n}", 44, (255, 255, 255)); M.blit(c.fr, T, lx + 40, 1396, c.alpha(1)); lx += 40 + T.width + 20
    def s4(c):
        PK.title(c, "넷 이상이 같은 말은\n100명 중 5명뿐", 430, .1, 100, color=PK.GOLDA); PK.small(c, "대부분은 둘이나 셋만 만나요\n나머지는 내가 고를 수 있는 곳이에요", 800, .8, 46, (255, 255, 255))
        PK.title(c, "떠오르는 사람에게\n보내 보세요", 1080, 1.5, 78); PK.small(c, "내 운명학은 프로필 링크에서 1초", 1330, 2.0, 44, (255, 255, 255))
    return [(3.2, s1), (3.6, s2), (6.2, s3), (3.4, s4)]
if __name__ == "__main__":
    sc = build(); bad = PK.check_frames(sc); print("안전 영역 검사:", "통과" if not bad else bad[:3])
    if bad and "--force" not in sys.argv: sys.exit(1)
    out, secs = M.render("dots_cross", sc, os.path.join(HERE, "..", "2026-motion")); PK.music(out, sc, 77); print(out, secs, "초")
