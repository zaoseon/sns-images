"""릴스 14편(세 지도 3 · 갑/을 2 · 데이터 9)을 새 영상 엔진 장면으로 다시 구성(10/7). 옛 방식(카드 1장을 화면 가운데에 붙임)은 상단 문구·글자 크기·빈 곳 규칙과 맞지 않아 9:16 장면으로 새로 만든다.
구성: 표지 → 핵심 3장 → 조언 → 댓글 질문 → 팔로우·홈페이지(R11). 문장은 기존 카드 정의(carousel 틀)에 있는 말만 쓴다.
사용: python3 pipeline/rebuild_reels.py  (resume 지원)"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "..")); sys.path.insert(0, os.path.join(ROOT, "pipeline")); sys.path.insert(0, HERE)
from clip_motion import *
MID = 910   # 안전 영역(상단 문구 아래 415 ~ 하단 고정 위 1405)의 세로 가운데
FACE_OK = lambda n: os.path.exists(os.path.join(ROOT, "characters", "cut", n + ".png"))
def face_of(d): n = d.get("face", "v1_lowbun"); return n if FACE_OK(n) else "v1_lowbun"
def S_hook(d):
    def f(c):
        chip(c, d.get("kicker") or "정월의 사주·별자리·숫자", 250, .05)
        y = text(c, d["coverTitle"], 410, .25, 104, maxw=820, lh=1.3, stagger=.26)
        text(c, d["coverSub"], y + 16, .9, 56, color=DIM, maxw=820)
        character(c, face_of(d), t0=.2, width=700)
    return f
def S_stat(title, body, n):
    def f(c):
        chip(c, f"{n} / 3", 250, .05)
        H = text_h(title, 124, 820, 1.25) + 56 + text_h(body, 72, 820, 1.4); y0 = MID - H / 2     # 글 묶음을 안전 영역 가운데로(R18·여백 규칙)
        y = text(c, title, y0, .15, 124, color=GOLD, maxw=820, lh=1.25)
        text(c, body, y + 56, .7, 72, color=WHITE, maxw=820, lh=1.4)
    return f
def S_advice(d):
    def f(c):
        chip(c, "조언", 250, .05)
        y = text(c, d["advice"][0], 420, .2, 100, maxw=820, lh=1.3)
        text(c, d["advice"][1], y + 30, .8, 56, color=DIM, maxw=820, lh=1.4)
        character(c, face_of(d), t0=.4, width=520)
    return f
def S_ctaA(d, hint=None):
    def f(c):
        H = text_h(d["ctaQ"], 108, 820, 1.3) + 48 + int(72 * 1.3) + (40 + int(54 * 1.3) if hint else 0); y0 = MID - H / 2
        y = text(c, d["ctaQ"], y0, .1, 108, maxw=820, lh=1.3)
        y = text(c, "댓글로 알려 주세요", y + 48, .7, 72, color=GOLD)
        if hint: text(c, hint, y + 40, 1.0, 54, color=DIM, maxw=820)
    return f
def S_ctaB(c):
    """팔로우 + 홈페이지 유입(R11). 카드 높이=글 높이+같은 위아래 여백(R18)."""
    t0 = .1; l1, l2, l3 = ("프로필 링크에서", 52), ("생년월일 입력하고", 76), ("내 첫글자와 타고난 기운 알아보기", 48)
    hs = [int(s * 1.2) for _, s in (l1, l2, l3)]; gap = 12; pad = 56; inner = sum(hs) + 2 * gap; w = 860; h = inner + 2 * pad
    Htot = int(100 * 1.3) + 4 + int(74 * 1.3) + 44 + h + 36 + 120; y_start = MID - Htot / 2                     # 큰 문구 + 카드 + 버튼 묶음 전체를 안전 영역 가운데로
    y = text(c, "팔로우하고", y_start, t0, 100); y = text(c, "더 많은 이야기 나눠요", y + 4, t0 + .35, 74, color=GOLD, maxw=820); top = y + 44
    card = rr(w, h, (26, 33, 54, 235), GOLD, r=44, ow=3); p = e_back((c.t - t0 - .7) / .5); blit(c.fr, card, CX - w / 2 - 4, top - 4 + (1 - e_out(p)) * 50, c.alpha(cl(p * 2)))
    yy = top + pad
    for (tx, sz), hh, col, tt in zip((l1, l2, l3), hs, (GOLD, WHITE, WHITE), (t0 + 1.0, t0 + 1.3, t0 + 1.6)): text(c, tx, yy, tt, sz, color=col, maxw=w - 60, lh=1.2); yy += hh + gap
    fnt = font(BLACK, 58); pl = "＋ 팔로우"; pw = int(fnt.getlength(pl)) + 100; im = Image.new("RGBA", (pw + 20, 140), (0, 0, 0, 0)); d = ImageDraw.Draw(im); d.rounded_rectangle((10, 10, 10 + pw, 130), radius=60, fill=GOLD); d.text((10 + pw / 2, 71), pl, font=fnt, fill=INK, anchor="mm")
    q = e_back((c.t - t0 - 1.9) / .45); pulse = 1 + .03 * math.sin(c.t * 6); L = im.resize((int(im.width * pulse), int(im.height * pulse))); blit(c.fr, L, CX - L.width / 2, top + h + 36 + (1 - e_out(q)) * 40, c.alpha(cl(q * 2)))
def scenes(d, hint=None):
    rows = [d["personality"], d["love"], d["money"]]
    return [(2.6, S_hook(d))] + [(2.7, S_stat(t, b, i + 1)) for i, (t, b) in enumerate(rows)] + [(3.0, S_advice(d)), (2.2, S_ctaA(d, hint)), (3.2, S_ctaB)]
def all_defs():
    """14편의 정의를 모은다. gapeul은 모듈 import 때 렌더가 돌므로 쓰지 않고 정의를 옮겨 쓴다."""
    out = {}
    import new_tri_reels as N, data_reels as DR
    for k, (d, ov) in N.defs.items(): out[("2026-w42reel-new/ig", k)] = (d, None)
    for k, (d, ov) in DR.defs.items(): out[("2026-w42reel-data/ig", k)] = (d, DR.HINT.get(k))
    import carousel_sets as CS
    g = dict(CS.SPARE["갑"]); g["advice"] = ["곧음은 무기,\n휘는 법도 알아요", "센 바람엔 가지도 흔들려야\n부러지지 않아요.\n한 번쯤은 먼저 끄덕여 보세요."]
    e = dict(CS.SPARE["을"]); e["advice"] = ["유연함은 무기,\n내 마음도 챙겨요", "맞추는 건 강점이지만 늘 내가 맞추면 지쳐요.\n하고 싶은 말 하나는 꼭 꺼내 보세요."]
    out[("2026-w42car-gapeul-reel/ig", "gab")] = (g, None); out[("2026-w42car-gapeul-reel/ig", "eul")] = (e, None)
    return out
