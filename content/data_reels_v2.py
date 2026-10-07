"""데이터 릴스 9편 새 구성(10/7, 대표 '제안대로'): 영상마다 다른 그림(형태)·글 효과·마무리. 숫자는 확인된 값만 쓴다(계산 자료 3,000명 README).
확정 규칙 적용: 상단 문구 아래 475↑ · 묶음 가운데 910 · 맨 아래 주소와 50px↑ · 뒤 차트 브랜드 차트 · 줄바꿈 뜻 단위 · 값마다 색 하나.
사용: python3 content/data_reels_v2.py <키>  -> 2026-reels-v2/<키>.mp4"""
import sys, os, math, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "..")); sys.path.insert(0, os.path.join(ROOT, "pipeline")); sys.path.insert(0, HERE)
from pilot_variety import *
import music_plan as MP
import fonts_kit as _FK
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
def v_tiles12(c, t0, focus=(), cy=928, a=1.0, avg=None, done=False):
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
        if count is not None: fx_count(c, count[0], 556, .25, 108, bigcol, count[1], 1.1)
        else: eff(e_title, c, big, 568 if small else 510, .25, 88 if len(big) < 12 else 76, bigcol, maxw=840, lh=1.2)
        vis(c); eff(e_cap + ("-" if e_cap == "slide" else ""), c, caption, 1235, 1.6, 48, DIM, maxw=840, lh=1.4)
    return f
def hook_scene(title, sub, vis, e="zoom", ty=490):
    def f(c):
        H = text_h(title, 100, 820, 1.3); y = eff(e, c, title, ty, .1, 100, WHITE, maxw=820, lh=1.3); eff("slide", c, sub, y + 24, 1.0, 54, DIM, maxw=820, lh=1.4); vis(c)
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

# ---------------- 그림 부품 2 ----------------
def v_dots100(c, t0, hollow=17, focus="hollow", cy=910, a=1.0, done=False):
    """100명 = 점 100개. 속이 빈 점이 hollow개(아래쪽부터), focus: 'hollow' 또는 'filled' 강조."""
    im, d = lay(900); R_, gap = 17, 46; x0 = CX - 4.5 * gap; y0 = cy - 4.5 * gap - 480
    for i in range(100):
        r_, k = divmod(i, 10); is_h = i >= 100 - hollow; g = 1.0 if done else e_back(cl((c.t - t0 - i * .012) / .3))
        if g <= 0: continue
        dim = (focus == "hollow" and not is_h) or (focus == "filled" and is_h); al = int(255 * cl(g) * a * (.28 if dim else 1)); x = x0 + k * gap; y = y0 + r_ * gap
        if is_h: d.ellipse((x - R_, y - R_, x + R_, y + R_), outline=CORAL[:3] + (al,), width=6)
        else: d.ellipse((x - R_, y - R_, x + R_, y + R_), fill=GOLD[:3] + (al,))
    blit(c.fr, im, 0, 480, 1.0)
def v_tiles39(c, t0, hot=7, cy=910, a=1.0, done=False):
    """명궁 모양 39가지 = 작은 칸 39개, 하나만 강조."""
    im, d = lay(900); cols, rows = 13, 3; cw, ch, gap = 46, 62, 12; x0 = CX - (cols * cw + (cols - 1) * gap) / 2; y0 = cy - (rows * ch + (rows - 1) * gap) / 2 - 480
    for i in range(39):
        r_, k = divmod(i, cols); g = 1.0 if done else e_back(cl((c.t - t0 - i * .03) / .3)); al = int(255 * cl(g) * a)
        if g <= 0: continue
        x = x0 + k * (cw + gap); y = y0 + r_ * (ch + gap); hot_ = (i == hot)
        d.rounded_rectangle((x, y, x + cw, y + ch), radius=12, fill=(GOLD[:3] + (al,)) if hot_ else (96, 110, 160, int(al * .75)))
    blit(c.fr, im, 0, 480, 1.0)
def v_axis(c, t0, focus=0, cy=950, a=1.0, done=False, labels=True):
    """가로 축 0~12%: 7~9.3% 띠, 천복성 9.3%, 천수성 7.2%, 고르게 나누면 8.3%."""
    im, d = lay(900); X0, X1 = 110, 830; sc = (X1 - X0) / 12.0; y = cy - 480; f44 = font(BLACK, 44); f50 = font(BLACK, 50); g = 1.0 if done else e_out(cl((c.t - t0) / .8)); al = int(255 * cl(g * 1.5) * a)
    d.rounded_rectangle((X0, y - 5, X1, y + 5), radius=5, fill=(255, 255, 255, int(al * .5)))
    for v in (0, 4, 8, 12): d.text((X0 + v * sc, y + 62), f"{v}%", font=f44, fill=(255, 255, 255, int(al * .8)), anchor="mm"); d.line([(X0 + v * sc, y - 14), (X0 + v * sc, y + 14)], fill=(255, 255, 255, int(al * .6)), width=4)
    band = e_out(cl((c.t - t0 - (1.4 if focus == 3 else .2)) / .7)) if focus in (0, 3) else 0.0; hot = 1.0 if focus in (0, 3) else .0
    if done: band = 1.0
    d.rounded_rectangle((X0 + 7.0 * sc, y - 46, X0 + (7.0 + 2.3 * band) * sc, y + 46), radius=18, fill=(TEAL[0], TEAL[1], TEAL[2], int(150 * a)))
    for v, col, lab, up, fc in ((9.3, GOLD, "천복성 9.3%", True, 1), (7.2, CORAL, "천수성 7.2%", False, 2)):
        gg = 1.0 if done else e_back(cl((c.t - t0 - .5 - fc * .3) / .4)); ax = int(255 * cl(gg) * a * (1 if focus in (0, fc) else .3)); xx = X0 + v * sc; r = 24 * min(gg, 1.1)
        d.ellipse((xx - r, y - r, xx + r, y + r), fill=col[:3] + (ax,), outline=(255, 255, 255, ax), width=4)
        if labels and focus in (fc, 0): d.text((xx, y + (-110 if up else 130)), lab, font=f50, fill=col[:3] + (ax,), anchor="mm")
    if labels and focus in (3, 0):
        xx = X0 + 8.33 * sc
        for yy in range(int(y - 190), int(y - 60), 24): d.line([(xx, yy), (xx, yy + 12)], fill=(255, 255, 255, int(al)), width=4)
        d.text((xx, y - 215), "고르게 나누면 8.3%", font=f44, fill=(255, 255, 255, int(al)), anchor="mm")
    blit(c.fr, im, 0, 480, 1.0)
def v_segbar(c, t0, parts, focus=None, cy=910, a=1.0, done=False):
    """가로로 쌓은 막대: parts=[(값, 색, 글)]. focus: 강조할 조각 번호."""
    im, d = lay(900); X0, W_ = 110, 720; y = cy - 480 - 30; H_ = 110; tot = sum(v for v, _, _ in parts); g = 1.0 if done else e_out(cl((c.t - t0) / .9)); f = font(BLACK, 54); x = X0
    for i, (v, col, lab) in enumerate(parts):
        w = W_ * v / tot * g; dim = focus is not None and focus != i; al = int(255 * a * (.3 if dim else 1)); d.rounded_rectangle((x, y - H_ / 2, x + max(4, w - 6), y + H_ / 2), radius=28, fill=col[:3] + (al,))
        if g > .85 and lab: d.text((x + (w - 6) / 2, y + H_ / 2 + 52), lab, font=f, fill=col[:3] + (al,), anchor="mm")   # 라벨은 막대 아래(좁은 조각에서도 안 잘림)
        x += w
    blit(c.fr, im, 0, 480, 1.0)
def v_hexagram(c, t0, lines, change=(), cy=910, a=1.0, done=False, size=1.0):
    """육효: lines는 아래부터 6개(1=양, 0=음). 동전을 던질 때마다 한 줄씩 쌓인다. change: 바뀌는 효 번호(0~5)."""
    im, d = lay(900); W_ = int(360 * size); H_ = int(30 * size); gap = int(30 * size); y0 = cy - (6 * H_ + 5 * gap) / 2 - 480 + (6 * H_ + 5 * gap) - H_
    for i, ln in enumerate(lines):
        g = 1.0 if done else e_out(cl((c.t - t0 - i * .35) / .4)); al = int(255 * cl(g * 1.4) * a); y = y0 - i * (H_ + gap); ch_ = i in change; col = (CORAL[:3] + (al,)) if ch_ else (GOLD[:3] + (al,))
        if ch_ and g > .9 and not done: col = (CORAL[:3] + (int(al * (.65 + .35 * math.sin(c.t * 9))),))
        if ln: d.rounded_rectangle((CX - W_ / 2, y, CX + W_ / 2, y + H_), radius=H_ // 2, fill=col)
        else:
            sw = int((W_ - int(60 * size)) / 2); d.rounded_rectangle((CX - W_ / 2, y, CX - W_ / 2 + sw, y + H_), radius=H_ // 2, fill=col); d.rounded_rectangle((CX + W_ / 2 - sw, y, CX + W_ / 2, y + H_), radius=H_ // 2, fill=col)
    blit(c.fr, im, 0, 480, 1.0)
def v_grid60(c, t0, lit=(), lit_col=None, cy=930, a=1.0, done=False, pulse=False):
    """하락이수 60괘 = 칸 60개(12열x5줄). lit: {번호: (한자, 색)}."""
    im, d = lay(900); cols, rows = 12, 5; cw, ch, gap = 58, 66, 6; x0 = CX - (cols * cw + (cols - 1) * gap) / 2; y0 = cy - (rows * ch + (rows - 1) * gap) / 2 - 480; fs = font(_FK.P["serif"], 46)
    for i in range(60):
        r_, k = divmod(i, cols); g = 1.0 if done else e_back(cl((c.t - t0 - i * .018) / .3))
        if g <= 0: continue
        al = int(255 * cl(g) * a); x = x0 + k * (cw + gap); y = y0 + r_ * (ch + gap)
        if i in lit: hj, col = lit[i]; d.rounded_rectangle((x - 4, y - 4, x + cw + 4, y + ch + 4), radius=14, fill=col[:3] + (al,)); d.text((x + cw / 2, y + ch / 2 - 2), hj, font=fs, fill=(24, 20, 36, al), anchor="mm")
        else:
            gl = (.9 + .1 * math.sin(c.t * 5 + i)) if pulse else 1; d.rounded_rectangle((x, y, x + cw, y + ch), radius=10, fill=(96, 110, 160, int(al * .6 * gl)))
    blit(c.fr, im, 0, 480, 1.0)
SIXN = ["사주", "별자리", "수비학", "자미두수", "당사주", "하락이수"]
def v_six(c, t0, colors, cy=880, a=1.0, done=False, mark=None):
    """여섯 운명학 = 점 6개(3x2). 같은 색 = 같은 방향을 가리킨다. mark: 점 둘을 잇는 선 (i, j, 글)."""
    im, d = lay(900); R_ = 75; f40 = font(BLACK, 40); pos = [(CX - 230 + (i % 3) * 230, cy - 105 + (i // 3) * 210 - 480) for i in range(6)]
    if mark:
        i, j, lab = mark; g = e_out(cl((c.t - t0 - 1.6) / .5)) * a
        if g > 0: d.line([pos[i], pos[j]], fill=(255, 255, 255, int(255 * g)), width=8); d.text(((pos[i][0] + pos[j][0]) / 2 + 60, (pos[i][1] + pos[j][1]) / 2 - 8), lab, font=font(BLACK, 46), fill=(255, 255, 255, int(255 * g)), anchor="mm", stroke_width=4, stroke_fill=(10, 14, 32, int(255 * g)))
    for i in range(6):
        g = 1.0 if done else e_back(cl((c.t - t0 - i * .13) / .4)); x, y = pos[i]; r = R_ * min(g, 1.08); al = int(255 * cl(g) * a); col = colors[i]
        d.ellipse((x - r, y - r, x + r, y + r), fill=col[:3] + (al,), outline=(255, 255, 255, al), width=4); d.text((x, y), SIXN[i], font=f40, fill=(24, 20, 36, al) if col in (GOLD, TEAL, CORAL) else (255, 255, 255, al), anchor="mm")
    blit(c.fr, im, 0, 480, 1.0)
def legend(c, t0, y=1120): fx_slide(c, "같은 색 = 같은 방향", y, t0, 44, DIM, dirn=1)

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
def reel_ziwei():
    d, _ = D["ziwei"]; V = lambda hol, foc: (lambda c: v_dots100(c, .3, hol, foc, cy=965))
    return [(2.8, hook_scene(d["coverTitle"], d["coverSub"], lambda c: v_dots100(c, .6, 17, "hollow", cy=1100, a=.6, done=True), "zoom")),
            (4.2, stat_scene("100명 중", "", CORAL, "명궁에 큰 별이 없어요.\n맞은편 별을 빌려 읽어요", V(17, "hollow"), "wipe", "slide", count=(17, "명"))),
            (4.2, stat_scene("나머지는", "", GOLD, "명궁에 큰 별이 앉아요.\n별 하나나 두 별의 조합이에요", V(17, "filled"), "slide", "wipe", count=(83, "명"))),
            (4.2, stat_scene("명궁 모양은 39가지", "가장 흔한 별도 5%", WHITE, "같은 명궁은 드물어요", lambda c: v_tiles39(c, .3), "zoom", "slide")),
            (3.4, adv_scene(d["advice"][0], d["advice"][1], "wipe")), (2.2, cq_scene(d["ctaQ"], "프로필 링크 > 감정서에서 확인")), (3.4, end_card(d))]
def reel_dang():
    d, _ = D["dang"]; V = lambda foc: (lambda c: v_axis(c, .3, foc, cy=950))
    return [(2.8, hook_scene(d["coverTitle"], d["coverSub"], lambda c: v_axis(c, .6, 0, cy=1180, a=.6, done=True, labels=False), "slide", ty=540)),
            (4.2, stat_scene("가장 자주 나온 별", "천복성 9.3%", GOLD, "가장 자주 나온 별이에요", V(1), "zoom", "wipe")),
            (4.2, stat_scene("가장 드물게 나온 별", "천수성 7.2%", CORAL, "가장 드물게 나온 별이에요", V(2), "wipe", "slide")),
            (4.2, stat_scene("열두 별이 고르게", "7~9% 사이", TEAL, "열두 별이 7~9% 사이에 모여 있어요", V(3), "slide", "wipe")),
            (3.4, adv_scene(d["advice"][0], d["advice"][1], "zoom")), (2.2, cq_scene(d["ctaQ"], "프로필 링크 > 감정서에서 확인")), (3.4, end_choice("내 중심별은\n흔할까요?", "흔한 별?", "드문 별?"))]
HEX = [1, 0, 1, 1, 0, 0]
def reel_liuyao():
    d, _ = D["liuyao"]; V = lambda foc, parts: (lambda c: v_segbar(c, .3, parts, foc))
    P1 = [(82, CORAL, "바뀜 82"), (18, GOLD, "그대로 18")]; P2 = [(66, TEAL, "한두 개 66"), (34, (96, 110, 160, 255), "")]
    return [(2.8, hook_scene(d["coverTitle"], d["coverSub"], lambda c: v_hexagram(c, .6, HEX, (1, 4), cy=1150, size=.8), "wipe", ty=525)),
            (4.2, stat_scene("100번 중", "", CORAL, "바뀌는 효(동효)가\n하나 이상 나와요", V(0, P1), "slide", "slide", count=(82, "번"))),
            (4.2, stat_scene("100번 중", "", GOLD, "하나도 안 바뀌고\n본괘 그대로예요", V(1, P1), "wipe", "wipe", count=(18, "번"))),
            (4.2, stat_scene("100번 중", "", TEAL, "바뀌는 효가 한두 개예요.\n두 괘로 읽어요", V(None, P2), "zoom", "slide", count=(66, "번"))),
            (3.4, adv_scene(d["advice"][0], d["advice"][1], "slide")), (2.2, cq_scene(d["ctaQ"], "프로필 링크 > 정월에게 묻다")), (3.4, end_numbers("82", "18", CORAL, GOLD, "바뀜", "그대로"))]
def reel_harak():
    d, _ = D["harak"]; G1 = {14: ("坤", GOLD)}; G2 = {14: ("坤", GOLD), 33: ("剝", CORAL)}
    return [(2.8, hook_scene(d["coverTitle"], d["coverSub"], lambda c: v_grid60(c, .6, {}, cy=1100, a=.6, done=True), "zoom")),
            (4.2, stat_scene("가장 자주 나온 괘", "곤괘(坤) 6.2%", GOLD, "고르게 나뉘면 1.7%예요", lambda c: v_grid60(c, .3, G1), "wipe", "slide")),
            (4.2, stat_scene("곤괘 다음으로 흔했어요", "박괘(剝) 4.3%", CORAL, "곤괘 다음으로 흔했어요", lambda c: v_grid60(c, .2, G2, done=True), "slide", "wipe")),
            (4.2, stat_scene("3,000명에게서 나온", "괘 모양 60가지", WHITE, "한 가지도 빠짐없이 나왔어요", lambda c: v_grid60(c, .3, {}, pulse=True), "zoom", "slide")),
            (3.4, adv_scene(d["advice"][0], d["advice"][1], "wipe")), (2.2, cq_scene(d["ctaQ"], "프로필 링크 > 감정서에서 확인")), (3.4, end_char([[("내 ", WHITE), ("하락이수 괘", GOLD), ("는", WHITE)], [("무엇일까요?", WHITE)]], "v7_hanbok"))]
def reel_alone():
    d, _ = D["alone"]; A = [GOLD, CORAL, CORAL, TEAL, TEAL, TEAL]; B = [GOLD, CORAL, GOLD, TEAL, TEAL, CORAL]; C = [GOLD, CORAL, TEAL, TEAL, TEAL, GOLD]
    sx = lambda cols, mk=None: (lambda c: (v_six(c, .3, cols, cy=940, mark=mk), legend(c, 1.4, 1140)))
    return [(2.8, hook_scene(d["coverTitle"], d["coverSub"], lambda c: v_six(c, .6, A, cy=1090, a=.6, done=True), "wipe")),
            (4.2, stat_scene("100명 중", "", CORAL, "사주와 같은 방향을 가리킨\n운명학이 하나도 없어요", sx(A), "zoom", "slide", count=(37, "명"))),
            (4.2, stat_scene("나머지는", "", GOLD, "다른 운명학 중 하나 이상은\n사주와 같은 방향이에요", sx(B), "slide", "wipe", count=(63, "명"))),
            (4.2, stat_scene("가장 닮은 짝은", "하락이수", TEAL, "사주와 24%가 같은 방향이었어요", sx(C, (0, 5, "24%")), "wipe", "slide")),
            (3.4, adv_scene(d["advice"][0], d["advice"][1], "zoom")), (2.2, cq_scene(d["ctaQ"])), (3.4, end_recap("혼자 다른 사람\n100명 중 37명", "slide"))]
def reel_four():
    d, _ = D["four"]; A = [GOLD, GOLD, GOLD, GOLD, CORAL, TEAL]; B = [GOLD, TEAL, GOLD, TEAL, GOLD, TEAL]; Z = [GOLD, CORAL, TEAL, BLUE, PINK, (170, 140, 255, 255)]
    sx = lambda cols: (lambda c: (v_six(c, .3, cols, cy=940), legend(c, 1.4, 1140)))
    return [(2.8, hook_scene(d["coverTitle"], d["coverSub"], lambda c: v_six(c, .6, B, cy=1090, a=.6, done=True), "zoom")),
            (4.2, stat_scene("100명 중", "", GOLD, "여섯 중 넷 이상이\n같은 방향을 가리켜요", sx(A), "wipe", "slide", count=(5, "명"))),
            (4.2, stat_scene("100명 중", "", TEAL, "가장 많이 모인 방향이\n둘뿐이에요", sx(B), "slide", "wipe", count=(61, "명"))),
            (4.2, stat_scene("여섯 모두 같은 사람", "0명", CORAL, "3,000명 중 한 명도 없었어요", sx(Z), "zoom", "slide")),
            (3.4, adv_scene(d["advice"][0], d["advice"][1], "slide")), (2.2, cq_scene(d["ctaQ"])), (3.4, end_char([[("내 ", WHITE), ("지도", GOLD), ("는 몇 개가", WHITE)], [("같을까요?", WHITE)]], "v11_mug"))]
REELS.update({"ziwei": (reel_ziwei, "data"), "dang": (reel_dang, "data"), "liuyao": (reel_liuyao, "data"), "harak": (reel_harak, "data"), "alone": (reel_alone, "data"), "four": (reel_four, "data")})

def build(key):
    fn, mood = REELS[key]; sc = fn(); out = os.path.join(ROOT, "2026-reels-v2"); p, dur = render(key, sc, out); mi = MP.choose(mood, "v2-" + key); MP.mux(p, [x for x, _ in sc], mi, 500 + len(key))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", "1.0", "-i", p, "-frames:v", "1", os.path.join(out, key + "_thumb.png")], check=True); print("완료", key, round(dur, 1), "초 · 음악", mi["style"], mi["bpm"])
if __name__ == "__main__":
    build(sys.argv[1])
