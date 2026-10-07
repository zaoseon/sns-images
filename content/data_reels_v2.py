"""데이터 릴스 9편 새 구성(10/7, 대표 '제안대로'): 영상마다 다른 그림(형태)·글 효과·마무리. 숫자는 확인된 값만 쓴다(계산 자료 3,000명 README).
확정 규칙 적용: 상단 문구 아래 475↑ · 묶음 가운데 910 · 맨 아래 주소와 50px↑ · 뒤 차트 브랜드 차트 · 줄바꿈 뜻 단위 · 값마다 색 하나.
사용: python3 content/data_reels_v2.py <키>  -> 2026-reels-v2/<키>.mp4"""
import sys, os, math, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "..")); sys.path.insert(0, os.path.join(ROOT, "pipeline")); sys.path.insert(0, HERE)
from pilot_variety import *
import music_plan as MP
import reels_engine as RE
PAL = [GOLD, CORAL, TEAL, BLUE, PINK, (170, 140, 255, 255)]
FX = {"wipe": fx_wipe, "slide": fx_slide, "zoom": fx_zoom}
def eff(name, c, s, y, t0, size, color=WHITE, **kw):
    """name: wipe | zoom | slide | slide-(왼쪽에서) — 글 효과를 영상마다 돌려 쓴다."""
    base = name.rstrip("-"); f = FX[base]
    if base == "slide": kw["dirn"] = -1 if name.endswith("-") else 1
    return f(c, s, y, t0, size, color, **kw)
def sc_text_block(c, lines, y, t0, size, color, e, maxw=840, lh=1.4): return eff(e, c, lines, y, t0, size, color, maxw=maxw, lh=lh)
# ---------------- 그림 부품 ----------------
STARS = [("염소", 23.0), ("황소", 22.7), ("처녀", 18.1), ("사자", 16.3), ("물병", 14.1), ("사수", 13.4), ("쌍둥이", 12.9), ("게", 12.6), ("양", 9.9), ("전갈", 7.3), ("물고기", 6.1), ("천칭", 5.6)]
def heat(v, k0=5.0, k1=23.5): k = cl((v - k0) / (k1 - k0)); return tuple(int(a + (b - a) * k) for a, b in zip((52, 62, 100), (231, 200, 141)))
def v_tiles12(c, t0, focus=(), cy=910, a=1.0, avg=None, done=False):
    im, d = lay(900); fn = font(BLACK, 46); fv = font(BLACK, 40); cw, ch, gx, gy = 190, 128, 22, 20; x0 = CX - (4 * cw + 3 * gx) / 2; y0 = cy - (3 * ch + 2 * gy) / 2 - 480
    for i, (nm, v) in enumerate(STARS):
        r, k = divmod(i, 4); x = x0 + k * (cw + gx); y = y0 + r * (ch + gy); g = (1.0 if done else e_back(cl((c.t - t0 - i * .09) / .35))) * a
        if g <= 0: continue
        dim = focus and nm not in focus; al = int(255 * cl(g) * (.3 if dim else 1)); col = heat(v)
        d.rounded_rectangle((x, y, x + cw, y + ch), radius=24, fill=col + (al,), outline=(255, 255, 255, int(al * .9)) if (focus and not dim) else None, width=5)
        ink = (24, 20, 36, al) if v > 14 else (255, 255, 255, al)
        d.text((x + cw / 2, y + 44), nm, font=fn, fill=ink, anchor="mm"); d.text((x + cw / 2, y + 92), f"{v:.1f}%", font=fv, fill=ink, anchor="mm")
    blit(c.fr, im, 0, 480, 1.0)
def v_pairbars(c, t0, focus=0, cy=910, a=1.0, done=False):
    im, d = lay(900); X0 = 110; sc = 25.0; fl = font(BLACK, 46); fv = font(BLACK, 50); y1 = cy - 150 - 480; y2 = cy + 20 - 480
    for k, (nm, v, col, y) in enumerate((("사주 + 하락이수", 24.4, GOLD, y1), ("수비학 + 자미두수", 13.1, CORAL, y2))):
        g = 1.0 if done else e_out(cl((c.t - t0 - k * .4) / .7)); dim = focus and focus != k + 1; al = int(255 * cl(g * 1.5) * a * (.3 if dim else 1))   # 길이(g)와 투명도(a)를 분리
        d.text((X0, y - 8), nm, font=fl, fill=(255, 255, 255, al), anchor="lm"); w = v * sc * g; d.rounded_rectangle((X0, y + 30, X0 + max(12, w), y + 100), radius=35, fill=col[:3] + (al,)); d.text((X0 + max(12, w) + 18, y + 65), f"{v * g:.1f}%", font=fv, fill=(255, 255, 255, al), anchor="lm")
    q = e_out(cl((c.t - t0 - .9) / .6)) * a; xb = X0 + 16.7 * sc; al = int(255 * q * (1 if focus in (0, 3) else .45))
    for yy in range(int(y1 - 20), int(y2 + 130), 26): d.line([(xb, yy), (xb, yy + 14)], fill=(255, 255, 255, al), width=4)
    d.text((xb, y2 + 150), "우연이면 약 17%", font=font(BLACK, 44), fill=(255, 255, 255, al), anchor="mm")
    blit(c.fr, im, 0, 480, 1.0)
# ---------------- 틀 ----------------
def stat_scene(small, big, bigcol, caption, vis, e_title="wipe", e_cap="slide", count=None):
    def f(c):
        if small: fx_slide(c, small, 486, .05, 50, DIM, dirn=-1)
        if count is not None: fx_count(c, count[0], 568, .25, 132, bigcol, count[1], 1.1)
        else: eff(e_title, c, big, 568 if small else 510, .25, 88 if len(big) < 12 else 76, bigcol, maxw=840, lh=1.2)
        vis(c); eff(e_cap + ("-" if e_cap == "slide" else ""), c, caption, 1225, 1.6, 48, DIM, maxw=840, lh=1.4)
    return f
def hook_scene(title, sub, vis, e="zoom"):
    def f(c):
        H = text_h(title, 100, 820, 1.3); y = eff(e, c, title, 490, .1, 100, WHITE, maxw=820, lh=1.3); eff("slide", c, sub, y + 24, 1.0, 54, DIM, maxw=820, lh=1.4); vis(c)
    return f
def adv_scene(t1, t2, e="wipe"):
    def f(c):
        H = text_h(t1, 100, 820, 1.3) + 40 + text_h(t2, 52, 840, 1.4); y0 = MID - H / 2; y = eff(e, c, t1, y0, .1, 100, GOLD, maxw=820, lh=1.3); fx_slide(c, t2, y + 40, 1.0, 52, DIM, maxw=840, lh=1.4, dirn=1)
    return f
def cq_scene(q, hint=None):
    def f(c):
        H = text_h(q, 100, 820, 1.3) + 48 + int(72 * 1.3) + (40 + int(50 * 1.3) if hint else 0); y0 = MID - H / 2; y = fx_slide(c, q, y0, .1, 100, dirn=-1); y = fx_slide(c, "댓글로 알려 주세요", y + 48, .6, 72, GOLD, dirn=1)
        if hint: fx_slide(c, hint, y + 40, 1.0, 50, DIM, maxw=840, dirn=-1)
    return f
def pill(c, label, y, t_in, col=GOLD):
    fnt = font(BLACK, 58); pw = int(fnt.getlength(label)) + 100; im = Image.new("RGBA", (pw + 20, 140), (0, 0, 0, 0)); d = ImageDraw.Draw(im); d.rounded_rectangle((10, 10, 10 + pw, 130), radius=60, fill=col); d.text((10 + pw / 2, 71), label, font=fnt, fill=INK, anchor="mm")
    q = e_back((c.t - t_in) / .45); pulse = 1 + .03 * math.sin(c.t * 6); L = im.resize((int(im.width * pulse), int(im.height * pulse))); blit(c.fr, L, CX - L.width / 2, y + (1 - e_out(q)) * 40, c.alpha(cl(q * 2)))
def end_recap(line, e="zoom"):
    """마무리 ④ 한 줄 정리+팔로우"""
    def f(c):
        Htot = text_h(line, 96, 820, 1.25) + 30 + int(60 * 1.3) + 56 + int(46 * 1.4) * 2 + 40 + 140; y = MID - 6 - Htot / 2
        y = eff(e, c, line, y, .1, 96, GOLD, maxw=820, lh=1.25); y = fx_slide(c, "팔로우하고 더 많은 이야기 나눠요", y + 30, .7, 60, maxw=830, dirn=1)
        y = fx_slide(c, "프로필 링크에서 생년월일 입력하고\n내 첫글자와 타고난 기운 알아보기", y + 56, 1.2, 46, DIM, maxw=840, lh=1.4, dirn=-1); pill(c, "＋ 팔로우", y + 40, 1.9)
    return f
def end_char(segs, face):
    """마무리 ③ 정월+알약 (정월은 이 장면에만)"""
    def f(c):
        y = fx_slide_rich(c, segs, 490, .1, 84, dirn=-1); y = fx_slide(c, "댓글로 알려 주시고 팔로우해 주세요", y + 22, .8, 54, maxw=840, dirn=1)
        y = fx_slide(c, "프로필 링크에서 생년월일 입력하고\n내 첫글자와 타고난 기운 알아보기", y + 16, 1.2, 44, DIM, maxw=840, lh=1.4, dirn=-1); pill(c, "＋ 팔로우", y + 24, 1.6); character(c, face, t0=.5, width=430)
    return f
def end_numbers(a, b, ca, cb, la, lb):
    """마무리 ⑤ 숫자 반복(값마다 색 하나)+팔로우"""
    def f(c):
        t0 = .1; Htot = int(190 * 1.2) + 14 + int(60 * 1.3) + 56 + int(60 * 1.3) + 36 + int(46 * 1.4) * 2 + 40 + 124; y = MID - 30 - Htot / 2
        nums, nc = color_row(((a, ca), (":", (255, 255, 255, 255)), (b, cb)), 190); p = e_out((c.t - t0) / .5); k = 1.45 - .45 * p; L = nums.resize((max(1, int(nums.width * k)), max(1, int(nums.height * k))), Image.LANCZOS)
        blit(c.fr, L, CX - L.width / 2, y - 20 + (nums.height - L.height) / 2, c.alpha(cl(p * 1.6))); x0 = CX - nums.width / 2; q = e_out((c.t - t0 - .4) / .5); ly = y + int(190 * 1.2) + 14 - 20 + (1 - q) * 40
        for tx, col, cxn in ((la, ca, nc[0]), (lb, cb, nc[2])): Lt = line_layers(tx, 60, col, BLACK, 600, 1.2)[0][0]; blit(c.fr, Lt, x0 + cxn - Lt.width / 2, ly, c.alpha(cl(q * 1.5)))
        y = y + int(190 * 1.2) + 14 + int(60 * 1.3); y = fx_slide(c, "팔로우하고 더 많은 이야기 나눠요", y + 56, t0 + 1.0, 60, maxw=830, dirn=1)
        y = fx_slide(c, "프로필 링크에서 생년월일 입력하고\n내 첫글자와 타고난 기운 알아보기", y + 36, t0 + 1.5, 46, DIM, maxw=840, lh=1.4, dirn=-1); pill(c, "＋ 팔로우", y + 40, t0 + 2.1)
    return f
def end_card(d_def):
    """마무리 ① 팔로우 카드(릴스 변환기의 카드 장면)"""
    return RE.S_ctaB
def end_choice(q, a_lab, b_lab):
    """마무리 ② 질문 크게 + 선택 알약"""
    def f(c):
        Htot = text_h(q, 112, 830, 1.25) + 44 + int(60 * 1.3) + 26 + int(46 * 1.4) * 2 + 48 + 110; y = MID - 24 - Htot / 2
        y = fx_zoom(c, q, y, .1, 112, GOLD, maxw=830, lh=1.25); y = fx_slide(c, "댓글로 알려 주시고 팔로우해 주세요", y + 44, 1.0, 60, maxw=840, dirn=-1)
        y = fx_slide(c, "프로필 링크에서 생년월일 입력하고\n내 첫글자와 타고난 기운 알아보기", y + 26, 1.5, 46, DIM, maxw=840, lh=1.4, dirn=1); im, d = lay(140); f64 = font(BLACK, 64)
        for k, (nm, col) in enumerate(((a_lab, PINK), (b_lab, BLUE))):
            qq = e_back(cl((c.t - 2.1 - k * .25) / .45)); w = 300 * min(qq, 1.0)
            if qq <= 0: continue
            x0 = CX - 320 + k * 340; d.rounded_rectangle((x0 + 150 - w / 2, 10, x0 + 150 + w / 2, 120), radius=55, fill=col); d.text((x0 + 150, 66), nm, font=f64, fill=(255, 255, 255, int(255 * cl(qq))), anchor="mm")
        blit(c.fr, im, 0, y + 48, 1.0)
    return f
# ---------------- 릴스 정의 ----------------
D = {k: (d, h) for (dd, k), (d, h) in RE.all_defs().items() if "data" in dd}
def lines(d, nm): return d[nm][1]
def reel_pair():
    d, _ = D["pair"]; V = lambda foc: (lambda c: v_pairbars(c, .4, foc))
    return [(2.8, hook_scene(d["coverTitle"], d["coverSub"], lambda c: v_pairbars(c, .8, 0, cy=1100, a=.6, done=True), "zoom")),
            (4.2, stat_scene("가장 닮은 짝", "사주 + 하락이수 24%", GOLD, "같은 방향을 가장 자주 가리킨 짝이에요", V(1), "wipe", "slide")),
            (4.2, stat_scene("가장 먼 짝", "수비학 + 자미두수 13%", CORAL, "가장 드물게 같았던 짝이에요", V(2), "slide", "wipe")),
            (4.2, stat_scene("기준선", "우연이라면 약 17%", WHITE, "여섯 방향 중 하나를 찍어도 그만큼 나와요", V(3), "zoom", "slide")),
            (3.4, adv_scene(d["advice"][0], d["advice"][1], "zoom")), (2.2, cq_scene(d["ctaQ"])), (3.4, end_recap("가장 닮은 짝 24%,\n가장 먼 짝 13%", "wipe"))]
def reel_star():
    d, _ = D["star"]; V = lambda foc: (lambda c: v_tiles12(c, .3, foc))
    return [(2.8, hook_scene(d["coverTitle"], d["coverSub"], lambda c: v_tiles12(c, .8, (), cy=1100, a=.6, done=True), "wipe")),
            (4.2, stat_scene("가장 자주", "염소·황소자리 23%", GOLD, "사주와 같은 방향을 가장 자주 가리켰어요", V(("염소", "황소")), "zoom", "slide")),
            (4.2, stat_scene("가장 드물게", "천칭자리 5.6%", CORAL, "물고기·전갈자리도 6~7%예요", V(("천칭", "물고기", "전갈")), "slide", "wipe")),
            (4.2, stat_scene("별자리마다 크게 달라요", "전체 평균 13.5%", WHITE, "태양 별자리 기준이에요", V(()), "wipe", "slide")),
            (3.4, adv_scene(d["advice"][0], d["advice"][1], "slide")), (2.2, cq_scene(d["ctaQ"])), (3.4, end_char([[("내 ", WHITE), ("별자리", GOLD), ("는", WHITE)], [("어디쯤일까요?", WHITE)]], "v3_ponytail"))]
REELS = {"pair": (reel_pair, "data"), "star": (reel_star, "data")}
def build(key):
    fn, mood = REELS[key]; sc = fn(); out = os.path.join(ROOT, "2026-reels-v2"); p, dur = render(key, sc, out); mi = MP.choose(mood, "v2-" + key); MP.mux(p, [x for x, _ in sc], mi, 500 + len(key))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", "1.0", "-i", p, "-frames:v", "1", os.path.join(out, key + "_thumb.png")], check=True); print("완료", key, round(dur, 1), "초 · 음악", mi["style"], mi["bpm"])
if __name__ == "__main__":
    build(sys.argv[1])
