"""모션그래픽 견본 M2 '100명 점 격자 + 숫자 카운트업'(10/5 대표: 모션그래픽도 기획에 넣는다).
데이터는 content/cross_data/README.md의 실제 값: 한 축에 모인 체계 수 2개 61.0% / 3개 32.2% / 4개 이상 5.3%(나머지 약 1.5%는 흩어짐). 100명 기준 반올림.
사용: python3 pipeline/motion_dots.py -> 2026-motion/dots_cross.mp4"""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import pick_reel as PK, clip_motion as M, music_plan as MP, face_plan as FP
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
FI = FP.pick("data", "motion-dots"); FACE = FI["face"] + ("_flip" if FI["flip"] else ""); DX = -70 if FI["flip"] else 70
def build():
    def s1(c):
        M.chip(c, "정월의 숫자 퀴즈", 345, .05)
        y = PK.title(c, "나랑 같은 말을 하는\n*운명학*, 몇 개일까요?", 430, .2, 92, lh=1.5)
        PK.small(c, "먼저 답을 골라 보세요", y + 40, .9, 54, PK.GOLDA); M.character(c, FACE, t0=.3, width=760, bottom=1460, dx=DX)
    def s2(c):
        PK.title(c, "여섯 운명학 중\n한 곳에 모인 수는?", 400, .05, 92, lh=1.5)
        for i, (lab, col) in enumerate((("둘", GOLDC), ("셋", TEAL), ("넷 이상", CORAL))):
            cy = 820 + i * 195; t0 = .35 + i * .18; p = M.e_back((c.t - t0) / .45)
            if p > 0.02:
                pill = M.rr(800, 170, col + (255,), None, r=85); M.pop(c, pill, CX, cy, t0, a=1.0)
                M.text(c, f"{i+1}   {lab}", cy - 60, t0 + .1, 82, color=(20, 20, 30, 255), path=BOLD, maxw=700, stagger=0)
        PK.small(c, "고른 번호를 댓글로 남겨 주세요", 1322, 1.4, 52, PK.GOLDA)
    def s3(c):
        M.text(c, "100명 중", 345, .05, 84, color=(255, 255, 255, 255), path=BOLD, maxw=800, stagger=0)
        x0, y0, cell = CX - 310 + 31, 748, 62; idx = 0; starts = [.3, 2.0, 3.4, 4.3]; durs = [1.5, 1.2, .8, .4]; cur = None; shown = {}
        for gi, (lab, n, col) in enumerate(GROUPS):
            for k in range(n):
                t0 = starts[gi] + durs[gi] * k / n; p = M.e_back((c.t - t0) / .28)
                r, cc = divmod(idx, 10); idx += 1
                if p > .02:
                    s = max(.02, min(p, 1.15)); L = dot_layer(col, int(30 * s) if s != 1 else 30, glow=(gi == 2 and c.t > 4.9)); M.blit(c.fr, L, x0 + cc * cell - L.width / 2, y0 + r * cell - L.height / 2, c.alpha(M.cl(p * 2)))
            if c.t >= starts[gi]: cur = gi; shown[gi] = int(round(n * M.cl((c.t - starts[gi]) / durs[gi])))
        if cur is not None:
            lab, n, col = GROUPS[cur]; v = shown[cur]
            L = layer_text(f"{lab} {v}명", 124 if cur != 2 else 138, col); M.blit(c.fr, L, CX - L.width / 2, 545, c.alpha(1))
        lx = 90
        for gi in range(4):
            if c.t >= starts[gi] + durs[gi]:
                lab, n, col = GROUPS[gi]; d = dot_layer(col, 16); M.blit(c.fr, d, lx, 1366, c.alpha(1)); T = layer_text(f"{lab} {n}", 48, (255, 255, 255), path=PK.PR); M.blit(c.fr, T, lx + 40, 1346, c.alpha(1)); lx += 40 + T.width + 20
    def s4(c):
        PK.title(c, "넷 이상이 같은 말은\n100명 중 5명뿐", 400, .1, 96, color=PK.GOLDA, lh=1.5); PK.small(c, "대부분은 둘이나 셋만 만나요\n나머지는 내가 고를 수 있는 곳이에요", 820, .8, 54, (255, 255, 255))
        PK.title(c, "떠오르는 사람에게\n보내 보세요", 1090, 1.5, 80, lh=1.5)
    return [(3.2, s1), (3.6, s2), (6.2, s3), (3.4, s4)]
if __name__ == "__main__":
    sc = build(); bad = PK.check_frames(sc); print("안전 영역 검사:", "통과" if not bad else bad[:3])
    if bad and "--force" not in sys.argv: sys.exit(1)
    out, secs = M.render("dots_cross", sc, os.path.join(HERE, "..", "2026-motion")); mi = MP.choose("data", "motion-dots"); MP.mux(out, [d for d, _ in sc], mi, 77); print("음악:", mi["style"], mi["bpm"], mi["key"], "| 얼굴:", FACE); print(out, secs, "초")
