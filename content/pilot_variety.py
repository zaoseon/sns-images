"""양산형 방지 시범 3편(10/7 대표 '시범안 확인'): ① 데이터(두 원이 겹치는 넓이=실제 비율) ② 비교(좌우 패널) ③ 오행(나무가 자란다).
새 규칙을 처음부터: R21 본문 y 475 이상 · R19 정월 얼굴 40% 이하(①②는 얼굴 없음) · 영상마다 다른 글 효과·마무리 · R04 x 50~900 · R06 글자 44px 이상 · R18 가운데.
사용: python3 content/pilot_variety.py A|B|C  -> 2026-pilot/<이름>.mp4"""
import sys, os, math, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "..")); sys.path.insert(0, os.path.join(ROOT, "pipeline"))
from clip_motion import *
from PIL import ImageChops
import clip_motion as _M, fonts_kit as _FK, music_plan as MP
CORAL = (255, 138, 115, 255); TEAL = (127, 214, 200, 255); BLUE = (92, 120, 255, 255); PINK = (255, 92, 157, 255)
MID = 907   # 상단 문구 아래(395)와 하단 주소 위(1425)의 가운데 910에 맞춘 값(실제 글 범위를 재서 보정, 10/7 대표 '아래로 쏠림')
AUDIT = False   # 배치 검사 때 장식(워터마크 막)을 끈다
# ---------- 글 효과(영상마다 다르게 쓴다, R19) ----------
def _lines(s, size, color, maxw, lh, path=BLACK): return line_layers(s, size, color, path, maxw, lh)
def fx_slide(c, s, y, t0, size, color=WHITE, maxw=820, lh=1.3, dirn=-1, cx=CX):
    ls, step = _lines(s, eff_size(s, size, maxw, BLACK), color, maxw, lh)
    for i, L in enumerate(ls):
        p = e_out((c.t - t0 - i * .14) / .5); blit(c.fr, L, cx - L.width / 2 + (1 - p) * dirn * 280, y + i * step - 20, c.alpha(cl(p * 1.5)))
    return y + len(ls) * step
def fx_wipe(c, s, y, t0, size, color=WHITE, maxw=820, lh=1.3, cx=CX):
    ls, step = _lines(s, eff_size(s, size, maxw, BLACK), color, maxw, lh)
    for i, L in enumerate(ls):
        p = e_out((c.t - t0 - i * .3) / .6); w = int(L.width * cl(p))
        if w > 2: blit(c.fr, L.crop((0, 0, w, L.height)), cx - L.width / 2, y + i * step - 20, c.alpha(1))
    return y + len(ls) * step
def fx_zoom(c, s, y, t0, size, color=WHITE, maxw=820, lh=1.3, cx=CX):
    ls, step = _lines(s, eff_size(s, size, maxw, BLACK), color, maxw, lh)
    for i, L in enumerate(ls):
        p = e_out((c.t - t0 - i * .12) / .5); k = 1.45 - .45 * p; im = L.resize((max(1, int(L.width * k)), max(1, int(L.height * k))), Image.LANCZOS)
        blit(c.fr, im, cx - im.width / 2, y + i * step - 20 + (L.height - im.height) / 2, c.alpha(cl(p * 1.6)))
    return y + len(ls) * step
def fx_count(c, to, y, t0, size, color=GOLD, suffix="", dur=1.1, cx=CX):
    p = e_out(cl((c.t - t0) / dur)); n = int(round(to * p)); s = f"{n}{suffix}"; L = line_layers(s, size, color, BLACK, 900, 1.2)[0][0]
    a = c.alpha(cl((c.t - t0) / .25)); blit(c.fr, L, cx - L.width / 2, y - 20, a); return y + int(size * 1.2)

def rich_lines(segs_lines, size, lh=1.3):
    """줄마다 (글, 색) 조각으로 된 글을 한 줄 층으로 만든다. 강조 낱말만 다른 색을 쓸 때."""
    f = font(BLACK, size); layers = []
    for segs in segs_lines:
        w = sum(f.getlength(tx) for tx, _ in segs); L = Image.new("RGBA", (int(w) + 16, int(size * 1.3)), (0, 0, 0, 0)); d = ImageDraw.Draw(L); x = 8
        for tx, col in segs: d.text((x, size * .65), tx, font=f, fill=col, anchor="lm"); x += f.getlength(tx)
        layers.append(L)
    return layers, int(size * lh)
def fx_slide_rich(c, segs_lines, y, t0, size, dirn=-1, lh=1.3, cx=CX):
    ls, step = rich_lines(segs_lines, size, lh)
    for i, L in enumerate(ls):
        p = e_out((c.t - t0 - i * .14) / .5); blit(c.fr, L, cx - L.width / 2 + (1 - p) * dirn * 280, y + i * step - 20, c.alpha(cl(p * 1.5)))
    return y + len(ls) * step
def lay(h=1000, off=0): im = Image.new("RGBA", (1080, h), (0, 0, 0, 0)); return im, ImageDraw.Draw(im)
# ---------- ① 데이터: 두 원이 겹치는 넓이 = 실제 비율 ----------
def overlap_d(r, f):
    lo, hi = 0.0, 2.0 * r
    for _ in range(60):
        d = (lo + hi) / 2; x = d / (2 * r); area = (2 * r * r * math.acos(x) - (d / 2) * math.sqrt(max(0, 4 * r * r - d * d))) / (math.pi * r * r)
        if area > f: lo = d
        else: hi = d
    return (lo + hi) / 2
R_V = 170; D_V = overlap_d(R_V, 0.135); VY = 985
def venn_layer(state, k=1.0):
    """state 'same': 겹침(금색) 강조 / 'diff': 바깥(산호색) 강조."""
    im = Image.new("RGBA", (1080, 620), (0, 0, 0, 0)); oy = VY - 310; cxL = CX - D_V / 2 * k - (1 - k) * 260; cxR = CX + D_V / 2 * k + (1 - k) * 260
    mL = Image.new("L", im.size, 0); mR = Image.new("L", im.size, 0); ImageDraw.Draw(mL).ellipse((cxL - R_V, 310 - R_V, cxL + R_V, 310 + R_V), fill=255); ImageDraw.Draw(mR).ellipse((cxR - R_V, 310 - R_V, cxR + R_V, 310 + R_V), fill=255)
    lens = ImageChops.multiply(mL, mR); only = ImageChops.subtract(ImageChops.lighter(mL, mR), lens)
    base = (255, 255, 255, 40); im.paste(Image.new("RGBA", im.size, base), (0, 0), ImageChops.lighter(mL, mR))
    if state == "same": im.paste(Image.new("RGBA", im.size, GOLD), (0, 0), lens)
    else: im.paste(Image.new("RGBA", im.size, CORAL), (0, 0), only); im.paste(Image.new("RGBA", im.size, (255, 255, 255, 70)), (0, 0), lens)
    d = ImageDraw.Draw(im)
    for (x, nm) in ((cxL, "사주"), (cxR, "별자리")): d.text((x, 310), nm, font=font(BLACK, 56), fill=(255, 255, 255, 235), anchor="mm")   # 각 원의 한가운데(10/7 대표)
    return im, oy, (cxL + cxR) / 2
def A1(c):
    H = text_h("사주와 별자리,\n같은 말을 할까요?", 104, 820, 1.3) + 36 + text_h("무작위 3,000명을 계산했어요", 56, 820, 1.4); y0 = MID - H / 2
    y = fx_wipe(c, "사주와 별자리,\n같은 말을 할까요?", y0, .1, 104, lh=1.3); fx_slide(c, "무작위 3,000명을 계산했어요", y + 36, 1.1, 56, DIM, dirn=1)
def A2(c):
    fx_slide(c, "100명 중", 490, .05, 64, DIM, dirn=-1); fx_count(c, 14, 565, .3, 190, GOLD, "명", 1.2)
    p = e_out(cl((c.t - .1) / .9)); im, oy, mx = venn_layer("same", p); blit(c.fr, im, 0, oy, c.alpha(cl(p * 1.5)))
    g = e_out(cl((c.t - 1.7) / .5))
    if g > 0:
        L = Image.new("RGBA", (6, 84), (224, 184, 102, int(255 * g))); blit(c.fr, L, mx - 3, VY + 120, 1.0)
        fx_wipe(c, "사주와 별자리가\n같은 방향을 가리켰어요", 1215, 1.9, 52, lh=1.3)
def A3(c):
    p = 1.0; im, oy, mx = venn_layer("diff", 1.0); blit(c.fr, im, 0, oy, 1.0)
    fx_slide(c, "나머지는", 490, .05, 64, DIM, dirn=-1); fx_count(c, 86, 565, .3, 190, CORAL, "명", 1.2)
    fx_wipe(c, "서로 다른 방향을 가리켰어요\n이게 보통이에요", 1215, 1.6, 52, lh=1.3)
def A4(c):
    fx_zoom(c, "별자리마다 크게 달라요", 490, .05, 68, maxw=840)
    rows = [("염소자리", 23.0, GOLD), ("황소자리", 22.7, GOLD), ("천칭자리", 5.6, CORAL)]; im, d = lay(900); f52 = font(BLACK, 52); f56 = font(BLACK, 56)
    for i, (nm, v, col) in enumerate(rows):
        y = 680 + i * 190 - 480; t0 = .5 + i * .5; g = e_out(cl((c.t - t0) / .7)); a = int(255 * cl(g * 1.5))
        d.text((70, y), nm, font=f52, fill=(255, 255, 255, a), anchor="lm"); w = 640 * (v / 23.0) * g
        d.rounded_rectangle((70, y + 36, 70 + max(10, w), y + 100), radius=32, fill=(col[0], col[1], col[2], a)); d.text((70 + max(10, w) + 20, y + 68), f"{v * g:.1f}%", font=f56, fill=(255, 255, 255, a), anchor="lm")
    blit(c.fr, im, 0, 480, 1.0); fx_slide(c, "무작위 3,000명을 계산했어요", 1295, 2.4, 44, DIM, dirn=1)
def A5(c):
    H = text_h("다르다고\n틀린 게 아니에요", 100, 820, 1.3) + 40 + text_h("같은 말은 타고난 결이에요.\n다른 말은 내가 고를 수 있는 곳이에요.", 52, 840, 1.4); y0 = MID - H / 2
    y = fx_zoom(c, "다르다고\n틀린 게 아니에요", y0, .1, 100, GOLD); fx_slide(c, "같은 말은 타고난 결이에요.\n다른 말은 내가 고를 수 있는 곳이에요.", y + 40, 1.0, 52, DIM, maxw=840, lh=1.4, dirn=1)
def A6(c):
    H = text_h("나는 어느 쪽일까요?", 100, 820, 1.3) + 48 + int(72 * 1.3); y0 = MID - H / 2
    y = fx_slide(c, "나는 어느 쪽일까요?", y0, .1, 100, dirn=-1); fx_slide(c, "댓글로 알려 주세요", y + 48, .6, 72, GOLD, dirn=1)
def color_row(items, size, gap=34):
    """색이 다른 조각을 한 줄로 이어 붙인 층과 각 조각의 가운데 x를 돌려준다."""
    ls = [line_layers(t, size, col, BLACK, 900, 1.2)[0][0] for t, col in items]; W_ = sum(L.width for L in ls) + gap * (len(ls) - 1); H_ = max(L.height for L in ls)
    im = Image.new("RGBA", (W_, H_), (0, 0, 0, 0)); x = 0; centers = []
    for L in ls: im.alpha_composite(L, (x, 0)); centers.append(x + L.width / 2); x += L.width + gap
    return im, centers
def A7(c):
    """마무리 ⑤: 숫자 반복(14=같은 말 금색, 86=다른 말 산호색) + 팔로우"""
    t0 = .1; Htot = int(190 * 1.2) + 14 + int(60 * 1.3) + 56 + int(60 * 1.3) + 36 + int(46 * 1.4) * 2 + 40 + 124; y = MID - 30 - Htot / 2
    nums, nc = color_row((("14", GOLD), (":", (255, 255, 255, 255)), ("86", CORAL)), 190)
    p = e_out((c.t - t0) / .5); k = 1.45 - .45 * p; L = nums.resize((max(1, int(nums.width * k)), max(1, int(nums.height * k))), Image.LANCZOS)
    blit(c.fr, L, CX - L.width / 2, y - 20 + (nums.height - L.height) / 2, c.alpha(cl(p * 1.6))); x0 = CX - nums.width / 2
    q = e_out((c.t - t0 - .4) / .5); ly = y + int(190 * 1.2) + 14 - 20 + (1 - q) * 40
    for tx, col, cxn in (("같은 말", GOLD, nc[0]), ("다른 말", CORAL, nc[2])):
        Lt = line_layers(tx, 60, col, BLACK, 600, 1.2)[0][0]; blit(c.fr, Lt, x0 + cxn - Lt.width / 2, ly, c.alpha(cl(q * 1.5)))
    y = y + int(190 * 1.2) + 14 + int(60 * 1.3)
    y = fx_slide(c, "팔로우하고 더 많은 이야기 나눠요", y + 56, t0 + 1.0, 60, maxw=830, dirn=1)
    y = fx_slide(c, "프로필 링크에서 생년월일 입력하고\n내 첫글자와 타고난 기운 알아보기", y + 36, t0 + 1.5, 46, DIM, maxw=840, lh=1.4, dirn=-1)
    fnt = font(BLACK, 58); pl = "＋ 팔로우"; pw = int(fnt.getlength(pl)) + 100; im = Image.new("RGBA", (pw + 20, 140), (0, 0, 0, 0)); d = ImageDraw.Draw(im); d.rounded_rectangle((10, 10, 10 + pw, 130), radius=60, fill=GOLD); d.text((10 + pw / 2, 71), pl, font=fnt, fill=INK, anchor="mm")
    q2 = e_back((c.t - t0 - 2.1) / .45); pulse = 1 + .03 * math.sin(c.t * 6); L2 = im.resize((int(im.width * pulse), int(im.height * pulse))); blit(c.fr, L2, CX - L2.width / 2, y + 40 + (1 - e_out(q2)) * 40, c.alpha(cl(q2 * 2)))
SC_A = [(2.8, A1), (5.0, A2), (3.6, A3), (4.2, A4), (3.4, A5), (2.2, A6), (3.4, A7)]
SETS = {"A": ("vs14_venn", SC_A, "data")}

# ---------- ② 비교: 좌우 패널이 만나고 갈라진다 ----------
PW, PH, PY = 330, 420, 612
def panels(c, gap_px, tint_same=0.0, t0=.0):
    """gap_px: 두 패널 사이 간격(음수면 겹침). tint_same: 겹침 영역 금색 강도."""
    im, d = lay(800); oy = 0; T0 = PY - 480
    xl = CX - PW - gap_px / 2 if gap_px >= 0 else CX - PW + (-gap_px) / 2
    xr = CX + gap_px / 2 if gap_px >= 0 else CX - (-gap_px) / 2
    d.rounded_rectangle((xl, T0, xl + PW, T0 + PH), radius=40, fill=(255, 92, 157, 215)); d.rounded_rectangle((xr, T0, xr + PW, T0 + PH), radius=40, fill=(92, 120, 255, 215))
    if gap_px < 0 and tint_same > 0:
        x0 = xr; x1 = xl + PW; d.rectangle((x0, T0, x1, T0 + PH), fill=(224, 184, 102, int(235 * tint_same)))
    d.text((xl + PW / 2 - (0 if gap_px >= 0 else 40), T0 + 90), "사주", font=font(BLACK, 72), fill=(255, 255, 255, 255), anchor="mm"); d.text((xl + PW / 2 - (0 if gap_px >= 0 else 40), T0 + 175), "(동양)", font=font(BLACK, 46), fill=(255, 255, 255, 230), anchor="mm")
    d.text((xr + PW / 2 + (0 if gap_px >= 0 else 40), T0 + 90), "별자리", font=font(BLACK, 72), fill=(255, 255, 255, 255), anchor="mm"); d.text((xr + PW / 2 + (0 if gap_px >= 0 else 40), T0 + 175), "(서양)", font=font(BLACK, 46), fill=(255, 255, 255, 230), anchor="mm")
    blit(c.fr, im, 0, 480, 1.0)
def B1(c):
    H = text_h("사주와 별자리가\n다른 말을 할 때", 100, 820, 1.3) + 36 + text_h("어느 쪽 말을 들어야 할까요?", 56, 820, 1.4); y0 = MID - H / 2
    y = fx_slide(c, "사주와 별자리가\n다른 말을 할 때", y0, .1, 100, dirn=-1); fx_slide(c, "어느 쪽 말을 들어야 할까요?", y + 36, 1.0, 56, DIM, dirn=1)
def B2(c):
    p = e_out(cl((c.t - .2) / 1.6)); gap = 150 - 280 * p   # 150 → -130 : 두 패널이 만나 겹친다
    fx_wipe(c, "같은 답이 나오면", 490, .05, 60, DIM); panels(c, gap, tint_same=cl((c.t - 1.4) / .6))
    g = e_out(cl((c.t - 1.9) / .5))
    if g > 0: fx_zoom(c, "타고난 결", PY + PH + 50, 2.0, 96, GOLD)
def B3(c):
    p = e_out(cl((c.t - .2) / 1.4)); gap = -130 + 280 * p   # 겹침 → 간격 150 : 갈라진다
    fx_wipe(c, "답이 갈리면", 490, .05, 60, DIM); panels(c, gap, tint_same=0.0)
    g = e_out(cl((c.t - 1.5) / .5)); by = PY + PH + 45
    if g > 0:
        im, d = lay(200); a = int(255 * g); d.rounded_rectangle((CX - 190 + (1 - g) * 40, 10, CX + 190 - (1 - g) * 40, 110), radius=50, outline=(224, 184, 102, a), width=6, fill=(11, 16, 32, int(215 * g))); d.text((CX, 60), "내가 고를 곳", font=font(BLACK, 58), fill=(224, 184, 102, a), anchor="mm"); blit(c.fr, im, 0, by - 10, 1.0)
    fx_slide(c, "풀이끼리 답이 갈리는 곳은\n내가 선택해서 바꿀 수 있어요", by + 100 + 45, 2.0, 46, DIM, maxw=840, lh=1.4, dirn=1)
SIX = ["사주", "별자리", "수비학", "자미두수", "당사주", "하락이수"]
def B4(c):
    fx_zoom(c, "여섯 가지를 겹쳐서", 490, .05, 72, maxw=840)
    im, d = lay(900); cols = [PINK, BLUE, TEAL, GOLD, CORAL, (170, 140, 255, 255)]; f52 = font(BLACK, 52)
    st = e_out(cl((c.t - 2.0) / .9)); vis = 1 - e_out(cl((c.t - 2.6) / .5))      # 2.0초부터 가운데로 모이고 사라진다
    for i, nm in enumerate(SIX):
        t0 = .4 + i * .2; p = e_out(cl((c.t - t0) / .5)); cx_ = 190 + (i % 3) * 270; cy_ = 700 - 480 + (i // 3) * 150; tx = CX; ty = 850 - 480
        x = cx_ + (tx - cx_) * st; y = cy_ + (ty - cy_) * st; sc = 1 - .45 * st; al = int(235 * cl(p * 1.4) * vis)
        if al > 3: d.rounded_rectangle((x - 120 * sc, y - 55 * sc, x + 120 * sc, y + 55 * sc), radius=int(30 * sc), fill=cols[i][:3] + (al,)); d.text((x, y + 2), nm, font=font(BLACK, max(20, int(52 * sc))), fill=(30, 20, 40, int(255 * cl(p * 1.4) * vis)), anchor="mm")
    blit(c.fr, im, 0, 480, 1.0)
    k = e_out(cl((c.t - 2.7) / .7))
    if k > 0:                                                                       # 자오선 로고타입: 子午線 + 자오선 + 한 줄
        im2, d2 = lay(900); al = int(255 * k); cy0 = 830 - 480; d2.ellipse((CX - 280, cy0 - 280, CX + 280, cy0 + 280), outline=GOLD[:3] + (int(120 * k),), width=6, fill=(11, 16, 32, int(150 * k)))
        d2.text((CX, cy0 - 62), "子午線", font=font(_FK.P["serif"], int(170 * (.8 + .2 * k))), fill=GOLD[:3] + (al,), anchor="mm"); d2.text((CX, cy0 + 100), "자오선", font=font(BLACK, 96), fill=(255, 255, 255, al), anchor="mm"); d2.text((CX, cy0 + 200), "여섯 운명학 교차분석", font=font(BLACK, 46), fill=(214, 218, 228, int(al * .9)), anchor="mm")
        blit(c.fr, im2, 0, 480, 1.0)
    fx_wipe(c, "같은 답과 다른 답을 나눠 봐요", 1215, 2.9, 52, GOLD, maxw=840)
def B5(c):
    H = text_h("같은 답은 결,\n다른 답은 선택", 108, 820, 1.3) + 40 + text_h("모순처럼 보여도\n그 사이에 내가 서 있어요", 54, 820, 1.4); y0 = MID - H / 2
    y = fx_wipe(c, "같은 답은 결,\n다른 답은 선택", y0, .1, 108, GOLD); fx_slide(c, "모순처럼 보여도\n그 사이에 내가 서 있어요", y + 40, 1.1, 54, DIM, dirn=1)
def B6(c):
    """마무리 ②: 댓글 질문 크게 + 팔로우 한 줄 + 프로필 링크 한 줄 + 하단 선택(동양? 서양?)"""
    Htot = text_h("어느 쪽을\n더 믿으세요?", 118, 830, 1.25) + 44 + int(60 * 1.3) + 26 + int(46 * 1.4) * 2 + 48 + 110; y = MID - 24 - Htot / 2
    y = fx_zoom(c, "어느 쪽을\n더 믿으세요?", y, .1, 118, GOLD); y = fx_slide(c, "댓글로 알려 주시고 팔로우해 주세요", y + 44, 1.0, 60, maxw=840, dirn=-1)
    y = fx_slide(c, "프로필 링크에서 생년월일 입력하고\n내 첫글자와 타고난 기운 알아보기", y + 26, 1.5, 46, DIM, maxw=840, lh=1.4, dirn=1)
    im, d = lay(140); f = font(BLACK, 64)
    for k, (nm, col) in enumerate((("동양?", (255, 92, 157, 255)), ("서양?", (92, 120, 255, 255)))):
        q = e_back(cl((c.t - 2.1 - k * .25) / .45)); w = 300 * min(q, 1.0)
        if q <= 0: continue
        x0 = CX - 320 + k * 340; d.rounded_rectangle((x0 + 150 - w / 2, 10, x0 + 150 + w / 2, 120), radius=55, fill=col); d.text((x0 + 150, 66), nm, font=f, fill=(255, 255, 255, int(255 * cl(q))), anchor="mm")
    blit(c.fr, im, 0, y + 48, 1.0)
SC_B = [(2.8, B1), (4.6, B2), (4.4, B3), (4.4, B4), (3.4, B5), (4.2, B6)]
SETS["B"] = ("vs_split", SC_B, "fun")

# ---------- ③ 오행: 큰 나무(갑목)가 자란다 ----------
def watermark(c, hanja, t0=.0, alpha=.13, size=720):
    """일간 한자를 배경 차트 가운데(x 470, y 800)에 워터마크처럼 깐다(10/7 대표). 일간 설명 장면의 맨 먼저 그려 글·그림 뒤로 간다."""
    if AUDIT: return
    k = e_out(cl((c.t - t0) / .7)); im = Image.new("RGBA", (900, 900), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse((50, 50, 850, 850), fill=(9, 13, 30, int(150 * k)))   # 차트 위에서 한자가 묻히지 않도록 뒤에 어두운 막을 깐다
    d.text((450, 440), hanja, font=font(_FK.P["serif"], size), fill=(GOLD[0], GOLD[1], GOLD[2], int(255 * .05 * k)), anchor="mm", stroke_width=5, stroke_fill=(GOLD[0], GOLD[1], GOLD[2], int(255 * .26 * k))); blit(c.fr, im, CX - 450, 910 - 450, 1.0)   # 윤곽선 위주의 은은한 워터마크
GROUND = 1320   # 땅 선(절대 y)
LEAF = [(84, 170, 110), (70, 150, 100), (110, 190, 120), (96, 178, 104)]
def tree_layer(g, sway=0.0, coins=0.0, roots=0.0, t=0.0, wind=0.0):
    """g: 자란 정도 0~1, sway: 흔들림(-1~1), coins: 잎이 금화로 바뀌는 정도, roots: 뿌리 길이 0~1."""
    im, d = lay(1000); base = GROUND - 480; cx = CX; H = max(10, 290 * g)
    gl = Image.new("RGBA", (1080, 40), (0, 0, 0, 0)); ImageDraw.Draw(gl).rounded_rectangle((160, 14, 790, 22), radius=4, fill=(255, 255, 255, 70)); im.alpha_composite(gl, (0, base - 14))
    if roots > 0:
        for ang, ln in ((-38, 36), (-14, 44), (12, 42), (36, 34)):
            a = math.radians(ang); L = ln * roots; d.line([(cx, base + 6), (cx + math.sin(a) * L * .55, base + 6 + math.cos(a) * L * .55), (cx + math.sin(a) * L, base + 6 + math.cos(a) * L)], fill=(224, 184, 102, 255), width=9, joint="curve")
    def tx(h): return cx + sway * (h / H) ** 2 * 70
    L_, R_ = [], []
    for k in range(11):
        h = H * k / 10; w = 30 * (1 - k / 10) + 11; L_.append((tx(h) - w, base - h)); R_.append((tx(h) + w, base - h))
    d.polygon(L_ + R_[::-1], fill=(120, 84, 56, 255)); d.line([(tx(H * k / 10) - 4, base - H * k / 10) for k in range(11)], fill=(150, 108, 72, 255), width=6)
    tips = []
    for f, ang, ln in ((.42, -52, 150), (.52, 50, 160), (.66, -40, 130), (.74, 42, 135), (.88, -24, 100), (.9, 26, 100)):
        if g < f * .9: continue
        gg = cl((g - f * .9) / .25) * g; h = H * f; x0, y0 = tx(h), base - h; a = math.radians(ang + sway * 18); x1 = x0 + math.sin(a) * ln * gg; y1 = y0 - math.cos(a) * ln * gg
        d.line([(x0, y0), (x1, y1)], fill=(120, 84, 56, 255), width=int(14 * (1 - f * .5))); tips.append((x1, y1, 40 + 12 * gg))
    tips.append((tx(H), base - H - 24 * g, 70 * g + 16))
    for n, (x, y, r) in enumerate(tips):
        for j in range(6):
            ox = math.cos(j * 1.3 + n) * r * .55; oy = math.sin(j * 1.9 + n) * r * .45; rr_ = r * (.55 + .12 * ((j + n) % 3)); col = LEAF[(j + n) % 4]
            if coins > 0:
                k = cl(coins * 1.4 - j * .12); col = tuple(int(col[i] + ((246, 196, 64)[i] - col[i]) * k) for i in range(3))
            d.ellipse((x + ox - rr_, y + oy - rr_, x + ox + rr_, y + oy + rr_), fill=col + (235,))
            if coins > .3: d.ellipse((x + ox - rr_ * .62, y + oy - rr_ * .62, x + ox + rr_ * .62, y + oy + rr_ * .62), outline=(176, 120, 24, int(230 * coins)), width=5)
    if wind > 0:
        for k in range(5):
            xx = (-200 + ((t * 700 + k * 260) % 1400)); yy = base - 40 - k * 80
            d.line([(xx, yy), (xx + 170, yy - 10)], fill=(255, 255, 255, int(110 * wind)), width=5)
    return im
def C1(c):
    H = text_h("곧게 뻗어\n굽히기 싫은 사람", 100, 820, 1.3); y = fx_zoom(c, "곧게 뻗어\n굽히기 싫은 사람", 515, .1, 100, GOLD); fx_wipe(c, "태어난 날 첫 글자가 갑(甲)이라면", y + 36, 1.0, 52, DIM, maxw=840)
    blit(c.fr, tree_layer(.32 * e_out(cl(c.t / 2.4))), 0, 480, 1.0)
def C2(c):
    watermark(c, "甲")
    y = fx_slide(c, "우뚝 서서\n앞장서는 타입", 490, .05, 80, GOLD, dirn=-1); fx_wipe(c, "큰 나무 같은 기운이라, 한번 정한 방향으로\n곧게 자라려는 힘이 강해요", y + 16, 1.0, 44, DIM, maxw=840, lh=1.4)
    blit(c.fr, tree_layer(.32 + .68 * e_out(cl((c.t - .2) / 2.8))), 0, 480, 1.0)
def C3(c):
    watermark(c, "甲")
    y = fx_zoom(c, "책임지는\n사랑을 해요", 490, .05, 80); fx_slide(c, "표현은 서툴러도 한번 정하면 결을 오래 지켜요.\n마음은 말로 한 번씩 꺼내 주세요", y + 16, 1.0, 44, DIM, maxw=840, lh=1.4, dirn=1)
    blit(c.fr, tree_layer(1.0, sway=.06 * math.sin(c.t * 2), roots=e_out(cl((c.t - .4) / 1.4))), 0, 480, 1.0)
def C4(c):
    watermark(c, "甲")
    y = fx_wipe(c, "성장에 쓰는\n투자형", 490, .05, 80, GOLD); fx_slide(c, "배우고 키우는 일에 기꺼이 써요.\n큰 지출 전엔 회수 시기를 적어 보세요", y + 16, 1.0, 44, DIM, maxw=840, lh=1.4, dirn=-1)
    blit(c.fr, tree_layer(1.0, sway=.05 * math.sin(c.t * 2), roots=1.0, coins=e_out(cl((c.t - .6) / 2.4))), 0, 480, 1.0)
def C5(c):
    watermark(c, "甲")
    y = fx_slide(c, "곧음은 무기,\n휘는 법도 알아요", 490, .05, 80, dirn=1); fx_zoom(c, "센 바람엔 가지도 흔들려야\n부러지지 않아요", y + 16, 1.0, 44, GOLD, maxw=840, lh=1.4)
    amp = e_out(cl(c.t / 1.0)); blit(c.fr, tree_layer(1.0, sway=amp * (.55 * math.sin(c.t * 2.6)), roots=1.0, coins=.0, t=c.t, wind=amp), 0, 480, 1.0)
def C6(c):
    """마무리 ③: 정월(이 장면에만 등장) + 질문 + 팔로우 알약"""
    y = fx_slide_rich(c, [[("주변에 ", WHITE), ("갑목", GOLD), (" 같은", WHITE)], [("사람이 있나요?", WHITE)]], 490, .1, 84, dirn=-1); y = fx_slide(c, "댓글로 알려 주시고 팔로우해 주세요", y + 22, .8, 54, maxw=840, dirn=1)
    y = fx_slide(c, "프로필 링크에서 생년월일 입력하고\n내 첫글자와 타고난 기운 알아보기", y + 16, 1.2, 44, DIM, maxw=840, lh=1.4, dirn=-1)
    fnt = font(BLACK, 54); pl = "＋ 팔로우"; pw = int(fnt.getlength(pl)) + 90; im = Image.new("RGBA", (pw + 20, 120), (0, 0, 0, 0)); d = ImageDraw.Draw(im); d.rounded_rectangle((10, 10, 10 + pw, 110), radius=50, fill=GOLD); d.text((10 + pw / 2, 61), pl, font=fnt, fill=INK, anchor="mm")
    q = e_back((c.t - 1.6) / .45); pulse = 1 + .03 * math.sin(c.t * 6); L = im.resize((int(im.width * pulse), int(im.height * pulse))); blit(c.fr, L, CX - L.width / 2, y + 24 + (1 - e_out(q)) * 40, c.alpha(cl(q * 2)))
    character(c, "v5_halfup_v2", t0=.5, width=430)
SC_C = [(3.0, C1), (5.0, C2), (4.4, C3), (4.2, C4), (4.8, C5), (3.6, C6)]
SETS["C"] = ("gab_tree", SC_C, "love")

def build(key):
    name, sc, mood = SETS[key]; out = os.path.join(ROOT, "2026-pilot"); p, d = render(name, sc, out); mi = MP.choose(mood, "pilot-" + name); MP.mux(p, [x for x, _ in sc], mi, 400 + ord(key))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", "1.0", "-i", p, "-frames:v", "1", os.path.join(out, name + "_thumb.png")], check=True); print("완료", name, round(d, 1), "초 · 음악", mi["style"], mi["bpm"])
if __name__ == "__main__":
    build(sys.argv[1])
