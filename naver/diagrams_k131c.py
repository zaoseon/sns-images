"""네이버 본문 그림 3판 (K-131 B2 · K-135, 대표 10/17 18:16 운영앱 요청 mvc6m8lr
"이건 계속 돌려쓰기 하는 거잖아. 인포그래픽, 차트, 관련된 유명한 이미지나 그림, 하다못해 그 이론을 얘기한 심리학자나
거기에 관련된 고전이라든지 영화나 드라마 등 할 게 얼마나 많은데... 가능한 건 바꾸고 앞으로 원고도 이런 걸 반영하라고 제발").
2판(diagrams_k131b)은 글의 '해 볼 것'을 상자·화살표·저울·배터리로 옮긴 것이라 다시 같은 묶음이 됐다. 3판은 '그림 거리'를 먼저 고른다:
 (가) 진짜 숫자로 그린 차트 — 논문·책에 나온 값만(vbar·dumbbell·line·bignum·heat·rings·span·axis)
 (나) 공유 저작물 명화 — 이 실행 환경은 위키미디어 접속이 막혀(403) 이번 판에는 없음. 넣을 땐 작가 사후 70년 지난 것만, 출처 표기
 (다) 이론을 말한 학자·실험 카드 — 이름·연도·실험 한 줄·우리 글과의 연결(exp·person·timeline·equation·triad·quad·compare·triangle). 인물 사진 없음
 (라) 고전·우화·신화·속담 — 제목과 장면을 우리 말로 설명만(story·book·scene·proverb·quote·versus). 스틸컷·포스터·현대 대사 인용 없음
모양 22가지, 한 배치 안 같은 모양 2번까지, 상자+화살표 모양(ARROWY)은 배치 전체 4장까지 — k131_check 가 잰다.
선 굵기는 diagrams_k131 LW·BOX·AH(K-133). 글자 42px 이상. 장식 아이콘·그라데이션 없음(K-041·K-042)."""
import math
import diagrams_k131 as DG
from diagrams_k131 import K, Cv, L, RT, XB, SB, LW, LW2, BOX, AH, _dot, _dash, _arrow, _done
from diagrams_k131b import _para, _ph, _soft, _tri
import body_v3 as B

W = RT - L - 20
X0 = L + 10
CX = (L + RT) / 2
SER = K.SER
# 3판 모양 → (가)~(라) 갈래. k131_check 가 3판 글은 두 장 모두 여기 있는 모양인지, 상자+화살표가 배치에 4장 이하인지 잰다.
KIND = {"vbar": "가", "dumbbell": "가", "line3": "가", "bignum": "가", "heat": "가", "rings": "가", "span": "가", "axis": "가",
        "exp": "다", "person": "다", "timeline3": "다", "equation": "다", "triad": "다", "quad": "다", "compare": "다", "triangle": "다",
        "story": "라", "book": "라", "scene": "라", "proverb": "라", "quote": "라", "versus": "라"}
ARROWY = {"exp", "timeline3"}


def _lum(col):
    f = lambda v: (v / 255) / 12.92 if v <= 10 else (((v / 255) + .055) / 1.055) ** 2.4
    r, g, b = (f(v) for v in col[:3]); return .2126 * r + .7152 * g + .0722 * b


def _cr(a, b):
    la, lb = sorted((_lum(a), _lum(b)), reverse=True); return (la + .05) / (lb + .05)


def _ink(c):
    """강조색 글자: 판·옅은 판 둘 다에서 대비 3 이상이면 강조색, 아니면 글자색(분홍 판처럼 강조색이 흰색일 때)."""
    return c.acc if min(_cr(c.acc, c.bg), _cr(c.acc, _soft(c))) >= 3 else c.fg


def _hf(c): return c.acc if _cr(c.acc, _soft(c)) >= 1.6 else c.fg      # 칠한 칸 바탕(강조색이 옅은 판과 안 갈리면 글자색)


def _ht(c): return c.pillfg if _cr(c.acc, _soft(c)) >= 1.6 else c.bg


def _sh(t): return _ph(t, SB, 42, W, 54) + 60


def _src(cv, c, y, t):
    """그림 맨 아래 출처(작은 글자 금지 → 42px, 회색). 길면 줄을 나눈다. y 는 무시하고 판 맨 아래에 맞춘다."""
    _para(cv, X0, cv.h - _sh(t) + 14, t, SB, 42, c.gray, W, "lt", 54)


def _pill(cv, c, x, y, t, fill=None, fg=None, size=42):
    w = cv.tw(t, XB, size) + 56
    cv.rr([x, y - 34, x + w, y + 34], 34, fill=fill or c.acc); cv.text(x + w / 2, y, t, XB, size, fg or c.pillfg, "mm")
    return w


def _H(top, *parts): return int(top + sum(parts))


# (다) 1. 실험 카드 --------------------------------------------------------------------
def exp(name, c, head, who, steps, finding, src):
    """who = '웨그너 연구진 · 1987', steps = [(꼬리표, 글)] 실험 순서(위→아래), finding = 결과 한두 줄."""
    top = 150; tw = W - 210
    hs = [max(100, _ph(t, SB, 44, tw) + 36) for _, t in steps]; fh = _ph(finding, XB, 46, W - 100) + 70
    H = _H(top, 90, sum(hs), 46 * (len(steps) - 1), 60, fh, 50 + _sh(src)); cv = Cv(H, c.bg); B._head(cv, c, head)
    w = _pill(cv, c, X0, top + 40, "실험", fill=c.fg, fg=c.bg); cv.text(X0 + w + 24, top + 40, who, XB, cv.fit(who, XB, 46, W - w - 30, 42), c.fg, "lm")
    y = top + 100
    for k, ((tag, t), h) in enumerate(zip(steps, hs)):
        cv.rr([X0, y, RT - 10, y + h], 28, fill=_soft(c))
        cv.text(X0 + 90, y + h / 2, tag, XB, cv.fit(tag, XB, 44, 150, 42), _ink(c), "mm")
        _para(cv, X0 + 190, y + h / 2 - _ph(t, SB, 44, tw) / 2, t, SB, 44, c.fg, tw, "lt")
        y += h
        if k < len(steps) - 1: _arrow(cv, c, (CX, y + 4), (CX, y + 44), c.fg); y += 46
    y += 30; cv.rr([X0, y, RT - 10, y + fh], 34, fill=c.acc)
    _para(cv, CX, y + fh / 2, finding, XB, 46, c.pillfg, W - 100)
    _src(cv, c, H - 55, src); _done(cv, c, name, "exp")


# (라) 2. 우화·신화 세 장면 --------------------------------------------------------------
def story(name, c, head, origin, beats, lesson, src):
    """origin = '그리스 신화', beats = 장면 글 3개(위→아래), lesson = 우리 글과 이어지는 한 줄. 화살표 없이 왼쪽 큰 번호(一 二 三)와 세로 줄."""
    top = 150; tw = W - 170
    hs = [_ph(t, SB, 46, tw) + 60 for t in beats]; lh = _ph(lesson, XB, 46, W - 100) + 70
    H = _H(top, 100, sum(hs), 40, lh, 50 + _sh(src)); cv = Cv(H, c.bg); B._head(cv, c, head)
    _pill(cv, c, X0, top + 40, origin)
    y = top + 100; cv.line(X0 + 120, y + 20, X0 + 120, y + sum(hs) - 20, _ink(c), LW2)
    for k, (t, h) in enumerate(zip(beats, hs)):
        cv.text(X0 + 50, y + h / 2, "一二三"[k], SER, 76, _ink(c), "mm")
        _para(cv, X0 + 160, y + h / 2 - _ph(t, SB, 46, tw) / 2, t, SB, 46, c.fg, tw, "lt"); y += h
    y += 40; cv.rr([X0, y, RT - 10, y + lh], 34, fill=c.acc)
    _para(cv, CX, y + lh / 2, lesson, XB, 46, c.pillfg, W - 100)
    _src(cv, c, H - 55, src); _done(cv, c, name, "story")


# (다) 3. 두 갈래 비교표 ------------------------------------------------------------------
def compare(name, c, head, cols, rows, src, hi=1):
    """cols = (왼 제목, 오른 제목), rows = [(줄 이름, 왼, 오른)]. hi = 칠할 쪽(0/1)."""
    top = 150; lab = 200; cw = (W - lab - 20) / 2
    rhs = [max(_ph(a, SB, 42, cw - 40), _ph(b, SB, 42, cw - 40)) + 50 for _, a, b in rows]
    H = _H(top, 110, sum(rhs), 50 + _sh(src)); cv = Cv(H, c.bg); B._head(cv, c, head)
    xs = [X0 + lab + 20, X0 + lab + 20 + cw]
    cv.rr([xs[hi], top, xs[hi] + cw, top + 110 + sum(rhs)], 30, fill=_hf(c))
    for k, t in enumerate(cols):
        cv.text(xs[k] + cw / 2, top + 55, t, XB, cv.fit(t, XB, 48, cw - 30, 42), _ht(c) if k == hi else c.fg, "mm")
    y = top + 110
    for (r, a, b), h in zip(rows, rhs):
        cv.line(X0, y, RT - 10, y, c.line if not c.dark else c.gray, DG.GRID)
        _para(cv, X0 + lab / 2, y + h / 2, r, XB, 42, c.fg, lab - 10)
        for k, t in enumerate((a, b)): _para(cv, xs[k] + cw / 2, y + h / 2, t, SB, 42, _ht(c) if k == hi else c.fg, cw - 40)
        y += h
    _src(cv, c, H - 55, src); _done(cv, c, name, "compare")


# (라) 4. 고전 책 -------------------------------------------------------------------------
def book(name, c, head, title, by, quote, gloss, src):
    """왼쪽 책등(세로 제목), 오른쪽 큰 인용(옮긴 말) + 풀이."""
    top = 150; bx = 230; tx = X0 + bx + 60; tw = RT - 10 - tx
    qh = _ph(quote, SER, 54, tw, 78); gh = _ph(gloss, SB, 44, tw)
    bh = max(560, 120 + qh + 90 + gh + 40)
    H = _H(top, 30, bh, 50 + _sh(src)); cv = Cv(H, c.bg); B._head(cv, c, head)
    y0 = top + 30; cv.rr([X0, y0, X0 + bx, y0 + bh], 18, fill=c.acc)
    cv.line(X0 + 34, y0, X0 + 34, y0 + bh, c.pillfg, LW2)
    ch = list(title.replace(" ", "")); step = min(78, (bh - 160) / max(1, len(ch)))
    for k, t in enumerate(ch): cv.text(X0 + bx / 2 + 14, y0 + 70 + k * step, t, XB, 56, c.pillfg, "mm")
    cv.text(tx - 10, y0 + 40, "“", SER, 120, _ink(c), "lt")
    _para(cv, tx, y0 + 120, quote, SER, 54, c.fg, tw, "lt", 78)
    cv.text(tx, y0 + 120 + qh + 30, "— " + by, XB, cv.fit("— " + by, XB, 44, tw, 42), _ink(c), "lm")
    _para(cv, tx, y0 + 120 + qh + 90, gloss, SB, 44, c.fg, tw, "lt")
    _src(cv, c, H - 55, src); _done(cv, c, name, "book")


# (가) 5. 큰 숫자 ---------------------------------------------------------------------------
def bignum(name, c, head, num, cap, rows, src):
    """num = '5 : 1', cap = 숫자 바로 아래 한 줄, rows = [(꼬리표, 글)] 숫자의 뜻."""
    top = 150; rh = [_ph(t, SB, 44, W - 260) + 40 for _, t in rows]
    H = _H(top, 360, 90, sum(rh), 50 + _sh(src)); cv = Cv(H, c.bg); B._head(cv, c, head)
    cv.text(CX, top + 180, num, XB, cv.fit(num, XB, 230, W, 120), _ink(c), "mm")
    cv.text(CX, top + 340, cap, XB, cv.fit(cap, XB, 48, W, 42), c.fg, "mm")
    y = top + 420
    for (tag, t), h in zip(rows, rh):
        cv.line(X0, y, RT - 10, y, c.line if not c.dark else c.gray, DG.GRID)
        cv.text(X0 + 10, y + h / 2, tag, XB, cv.fit(tag, XB, 44, 220, 42), _ink(c), "lm")
        _para(cv, X0 + 250, y + h / 2 - _ph(t, SB, 44, W - 260) / 2, t, SB, 44, c.fg, W - 260, "lt"); y += h
    _src(cv, c, H - 55, src); _done(cv, c, name, "bignum")


# (라) 6. 속담 --------------------------------------------------------------------------------
def proverb(name, c, head, where, saying, meaning, link, src):
    top = 150; sh = _ph(saying, SER, 76, W - 80, 104); mh = _ph(meaning, SB, 44, W - 60); lh = _ph(link, XB, 46, W - 100) + 70
    H = _H(top, 90, sh + 120, 30, mh, 50, lh, 50 + _sh(src)); cv = Cv(H, c.bg); B._head(cv, c, head)
    _pill(cv, c, X0, top + 40, where)
    y = top + 100; cv.rr([X0, y, RT - 10, y + sh + 120], 34, fill=_soft(c))
    cv.line(X0 + 40, y + 40, X0 + 40, y + sh + 80, c.acc, 16)
    _para(cv, CX + 20, y + 60 + sh / 2, saying, SER, 76, c.fg, W - 140, "mm", 104)
    y += sh + 150; _para(cv, X0 + 10, y, meaning, SB, 44, c.fg, W - 60, "lt"); y += mh + 50
    cv.rr([X0, y, RT - 10, y + lh], 34, fill=c.acc); _para(cv, CX, y + lh / 2, link, XB, 46, c.pillfg, W - 100)
    _src(cv, c, H - 55, src); _done(cv, c, name, "proverb")


# (가) 7. 선 그래프(함수 곡선) ------------------------------------------------------------------
def line3(name, c, head, f, xr, yr, xl, yl, marks, note, src, ref=None):
    """f(x) 곡선을 굵게. marks = [(x, 글, 위/아래)] 곡선 위 점. ref = 견줄 점선 함수(없으면 생략). 축 글은 42px."""
    top = 150; gx0, gx1 = X0 + 90, RT - 40; gy0, gy1 = top + 60, top + 640
    nh = _ph(note, XB, 46, W - 100) + 70 if note else 0
    H = _H(top, 640, 110, nh, 40 if note else 0, 40 + _sh(src)); cv = Cv(H, c.bg); B._head(cv, c, head)
    X = lambda x: gx0 + (x - xr[0]) / (xr[1] - xr[0]) * (gx1 - gx0)
    Y = lambda y: gy1 - (y - yr[0]) / (yr[1] - yr[0]) * (gy1 - gy0)
    zx = X(0) if xr[0] < 0 < xr[1] else gx0; zy = Y(0) if yr[0] < 0 < yr[1] else gy1
    cv.line(gx0, zy, gx1, zy, c.gray, BOX); cv.line(zx, gy0, zx, gy1, c.gray, BOX)
    cv.text(gx1, zy + 50, xl, SB, 42, c.gray, "rm"); cv.text(zx + 20, gy0 - 10, yl, SB, 42, c.gray, "lm")
    def plot(fn, col, w, dash=False):
        pts = [(X(xr[0] + (xr[1] - xr[0]) * i / 200), Y(fn(xr[0] + (xr[1] - xr[0]) * i / 200))) for i in range(201)]
        pts = [(x, min(max(y, gy0), gy1)) for x, y in pts]
        for a, b in zip(pts, pts[1:]):
            if dash: continue
            cv.line(*a, *b, col, w)
        if dash:
            for i in range(0, 200, 6): cv.line(*pts[i], *pts[min(i + 3, 200)], col, w)
    if ref: plot(ref, c.gray, LW2, True)
    plot(f, c.acc, LW + 4)
    for x, t, up in marks:
        px, py = X(x), Y(f(x)); _dot(cv, px, py, 20, fill=c.fg)
        tw_ = cv.tw(t, XB, 44) + 40; bx = min(max(px - tw_ / 2, X0), RT - 10 - tw_); by = py - 90 if up else py + 50
        cv.rr([bx, by, bx + tw_, by + 64], 32, fill=c.fg); cv.text(bx + tw_ / 2, by + 32, t, XB, 44, c.bg, "mm")
    y = gy1 + 110
    if note: cv.rr([X0, y, RT - 10, y + nh], 34, fill=c.acc); _para(cv, CX, y + nh / 2, note, XB, 46, c.pillfg, W - 100)
    _src(cv, c, H - 55, src); _done(cv, c, name, "line3")


# (다) 8. 연도 흐름 ------------------------------------------------------------------------------
def timeline3(name, c, head, events, note, src):
    """events = [(연도 글, 이름, 한 줄)] 왼쪽 세로줄에 점, 점 사이 화살표. 마지막이 우리 글."""
    top = 150; tw = W - 300
    hs = [max(120, _ph(t, SB, 42, tw) + 90) for _, _, t in events]; nh = _ph(note, XB, 46, W - 100) + 70 if note else 0
    H = _H(top, 40, sum(hs), 40, nh, 50 + _sh(src)); cv = Cv(H, c.bg); B._head(cv, c, head)
    lx = X0 + 250; y = top + 40; ys = []
    for h in hs: ys.append(y + 40); y += h
    for a, b in zip(ys, ys[1:]): _arrow(cv, c, (lx, a + 26), (lx, b - 26), c.fg)
    for (yr, nm, t), cy, h in zip(events, ys, hs):
        cv.text(lx - 40, cy, yr, XB, cv.fit(yr, XB, 52, 220, 42), _ink(c), "rm")
        _dot(cv, lx, cy, 20, fill=c.acc)
        cv.text(lx + 50, cy, nm, XB, cv.fit(nm, XB, 46, RT - 10 - lx - 50, 42), c.fg, "lm")
        _para(cv, lx + 50, cy + 36, t, SB, 42, c.gray if not c.dark else c.fg, RT - 10 - lx - 50, "lt")
    y = top + 40 + sum(hs) + 20
    if note: cv.rr([X0, y, RT - 10, y + nh], 34, fill=c.acc); _para(cv, CX, y + nh / 2, note, XB, 46, c.pillfg, W - 100)
    _src(cv, c, H - 55, src); _done(cv, c, name, "timeline3")


# (다) 9. 네 칸(2x2) ------------------------------------------------------------------------------
def quad(name, c, head, items, hi, src, note=""):
    """items = [(제목, 설명)] 4개, hi = 칠할 칸 번호."""
    top = 150; gap = 24; qw = (W - gap) / 2
    qh = 120 + max(_ph(t, SB, 42, qw - 50) for _, t in items); nh = _ph(note, SB, 44, W) + 30 if note else 0
    H = _H(top, 30, 2 * qh + gap, 40, nh, 40 + _sh(src)); cv = Cv(H, c.bg); B._head(cv, c, head)
    for k, (t, s) in enumerate(items):
        x = X0 + (k % 2) * (qw + gap); y = top + 30 + (k // 2) * (qh + gap); on = k == hi
        cv.rr([x, y, x + qw, y + qh], 34, fill=_hf(c) if on else _soft(c))
        cv.text(x + 30, y + 60, t, XB, cv.fit(t, XB, 50, qw - 60, 42), _ht(c) if on else c.fg, "lm")
        _para(cv, x + 30, y + 110, s, SB, 42, _ht(c) if on else c.fg, qw - 50, "lt")
    if note: _para(cv, X0, top + 30 + 2 * qh + gap + 40, note, SB, 44, c.fg, W, "lt")
    _src(cv, c, H - 55, src); _done(cv, c, name, "quad")


# (가) 10. 날 수 칸 ---------------------------------------------------------------------------------
def span(name, c, head, n, per_row, label, side, src):
    """n 일을 한 칸씩(per_row 칸 한 줄). label = 칸 아래 한 줄, side = [(꼬리표, 글)]."""
    top = 150; gap = 12; cs = (W - gap * (per_row - 1)) / per_row; rows = math.ceil(n / per_row)
    sh = [_ph(t, SB, 44, W - 230) + 36 for _, t in side]
    H = _H(top, 40, rows * (cs + gap), 100, sum(sh), 40 + _sh(src)); cv = Cv(H, c.bg); B._head(cv, c, head)
    for i in range(n):
        x = X0 + (i % per_row) * (cs + gap); y = top + 40 + (i // per_row) * (cs + gap)
        cv.rr([x, y, x + cs, y + cs], 12, fill=c.acc)
        if i in (0, n - 1): cv.text(x + cs / 2, y + cs / 2, str(i + 1), XB, 42, c.pillfg, "mm")
    y = top + 40 + rows * (cs + gap) + 40
    cv.text(X0, y, label, XB, cv.fit(label, XB, 48, W, 42), c.fg, "lm"); y += 60
    for (tag, t), h in zip(side, sh):
        cv.text(X0, y + h / 2, tag, XB, cv.fit(tag, XB, 44, 200, 42), _ink(c), "lm")
        _para(cv, X0 + 220, y + h / 2 - _ph(t, SB, 44, W - 230) / 2, t, SB, 44, c.fg, W - 230, "lt"); y += h
    _src(cv, c, H - 55, src); _done(cv, c, name, "span")


# (라) 11. 장면(대본 꼴) -----------------------------------------------------------------------------
def scene(name, c, head, work, by, acts, link, src):
    """acts = [(장면 꼬리표, 우리 말 장면 설명)] 대본처럼 왼쪽 꼬리표. 대사 인용 없이 설명만."""
    top = 150; tw = W - 240
    hs = [_ph(t, SB, 44, tw) + 50 for _, t in acts]; lh = _ph(link, XB, 46, W - 100) + 70
    H = _H(top, 175, sum(hs), 40, lh, 50 + _sh(src)); cv = Cv(H, c.bg); B._head(cv, c, head)
    cv.text(X0, top + 50, work, SER, cv.fit(work, SER, 62, W - 20, 44), c.fg, "lm")
    cv.text(X0, top + 118, by, SB, 42, c.gray, "lm")
    y = top + 175; cv.line(X0, y - 18, RT - 10, y - 18, c.fg, LW2)
    for (tag, t), h in zip(acts, hs):
        cv.text(X0, y + 40, tag, XB, cv.fit(tag, XB, 44, 210, 42), _ink(c), "lm")
        _para(cv, X0 + 230, y + 18, t, SB, 44, c.fg, tw, "lt"); y += h
    y += 20; cv.rr([X0, y, RT - 10, y + lh], 34, fill=c.acc); _para(cv, CX, y + lh / 2, link, XB, 46, c.pillfg, W - 100)
    _src(cv, c, H - 55, src); _done(cv, c, name, "scene")


# (가) 12. 짐작과 실제(점 두 개) -----------------------------------------------------------------------
def dumbbell(name, c, head, rows, labs, note, src, unit="%"):
    """rows = [(줄 이름, 짐작 값, 실제 값)] 0~100. labs = (짐작 이름, 실제 이름)."""
    top = 150; gx0, gx1 = X0 + 40, RT - 60; rh = 270; nh = _ph(note, XB, 46, W - 100) + 70
    H = _H(top, 110, rh * len(rows), 70, nh, 50 + _sh(src)); cv = Cv(H, c.bg); B._head(cv, c, head)
    X = lambda v: gx0 + v / 100 * (gx1 - gx0)
    x = X0
    for k, t in enumerate(labs):
        if k == 0: _dot(cv, x + 24, top + 50, 22, outline=c.fg, w=BOX)
        else: _dot(cv, x + 24, top + 50, 24, fill=c.acc)
        cv.text(x + 64, top + 50, t, SB, 42, c.fg, "lm"); x += 64 + cv.tw(t, SB, 42) + 60
    y = top + 110
    for r, a, b in rows:
        cv.text(X0, y + 30, r, XB, cv.fit(r, XB, 44, W, 42), c.fg, "lm")
        cy = y + 170; cv.line(gx0, cy, gx1, cy, c.line if not c.dark else c.gray, DG.GRID)
        cv.line(X(b), cy, X(a), cy, c.fg, LW + 4)
        _dot(cv, X(a), cy, 30, fill=c.bg, outline=c.fg, w=BOX); _dot(cv, X(b), cy, 32, fill=c.acc)
        for v, up in ((a, True), (b, False)):
            t = f"{v:g}{unit}"; cv.text(X(v), cy - 64 if up else cy + 66, t, XB, 48, c.fg, "mm")
        y += rh
    y += 30; cv.rr([X0, y, RT - 10, y + nh], 34, fill=c.acc); _para(cv, CX, y + nh / 2, note, XB, 46, c.pillfg, W - 100)
    _src(cv, c, H - 55, src); _done(cv, c, name, "dumbbell")


# (다) 13. 세 기둥 ---------------------------------------------------------------------------------------
def triad(name, c, head, items, hi, link, src):
    """items = [(이름, 설명)] 3개 세로 기둥, hi = 칠할 기둥."""
    top = 150; gap = 24; cw = (W - 2 * gap) / 3
    ch = 190 + max(_ph(t, SB, 42, cw - 40) for _, t in items); lh = _ph(link, XB, 46, W - 100) + 70
    H = _H(top, 30, ch, 50, lh, 50 + _sh(src)); cv = Cv(H, c.bg); B._head(cv, c, head)
    for k, (t, s) in enumerate(items):
        x = X0 + k * (cw + gap); y = top + 30; on = k == hi
        cv.rr([x, y, x + cw, y + ch], 30, fill=_hf(c) if on else _soft(c))
        cv.text(x + cw / 2, y + 60, str(k + 1), XB, 64, _ht(c) if on else (_ink(c)), "mm")
        cv.text(x + cw / 2, y + 140, t, XB, cv.fit(t, XB, 48, cw - 30, 42), _ht(c) if on else c.fg, "mm")
        _para(cv, x + cw / 2, y + 190 + (ch - 190) / 2 - 10, s, SB, 42, _ht(c) if on else c.fg, cw - 40)
    y = top + 30 + ch + 50; cv.rr([X0, y, RT - 10, y + lh], 34, fill=c.fg)
    _para(cv, CX, y + lh / 2, link, XB, 46, c.bg, W - 100)
    _src(cv, c, H - 55, src); _done(cv, c, name, "triad")


# (라) 14. 두 쪽 맞대기(우화) ---------------------------------------------------------------------------
def versus(name, c, head, origin, left, right, link, src):
    """left/right = (누구, 한 일, 결과). 왼쪽 옅은 판, 오른쪽 강조 판. 가운데 세로줄."""
    top = 150; pw = (W - 30) / 2
    ph = 150 + max(_ph(a + " " + b, SB, 44, pw - 60) for _, a, b in (left, right)) + 60
    lh = _ph(link, XB, 46, W - 100) + 70
    H = _H(top, 100, ph, 50, lh, 50 + _sh(src)); cv = Cv(H, c.bg); B._head(cv, c, head)
    _pill(cv, c, X0, top + 40, origin, fill=c.fg, fg=c.bg)
    for k, (who, did, res) in enumerate((left, right)):
        x = X0 + k * (pw + 30); y = top + 100; on = k == 1
        cv.rr([x, y, x + pw, y + ph], 34, fill=_hf(c) if on else _soft(c))
        cv.text(x + pw / 2, y + 70, who, XB, cv.fit(who, XB, 60, pw - 40, 44), _ht(c) if on else c.fg, "mm")
        h1 = _para(cv, x + 30, y + 140, did, SB, 44, _ht(c) if on else c.fg, pw - 60, "lt")
        _para(cv, x + 30, y + 160 + h1, res, XB, 44, _ht(c) if on else c.fg, pw - 60, "lt")
    y = top + 100 + ph + 50; cv.rr([X0, y, RT - 10, y + lh], 34, fill=_soft(c), outline=c.fg, w=BOX)
    _para(cv, CX, y + lh / 2, link, XB, 46, c.fg, W - 100)
    _src(cv, c, H - 55, src); _done(cv, c, name, "versus")


# (가) 15. 짝 표(히트맵) -----------------------------------------------------------------------------------
def heat(name, c, head, labels, M, legend, note, src):
    """labels = 줄·칸 이름(같은 순서), M[i][j] = 0 옅음 / 1 중간 / 2 진함. legend = {값: 글}."""
    n = len(labels); top = 150; lab = 190; cs = (W - lab) / n
    nh = _ph(note, SB, 44, W) + 30
    H = _H(top, 80, cs * n, 120, nh, 40 + _sh(src)); cv = Cv(H, c.bg); B._head(cv, c, head)
    gx = X0 + lab; gy = top + 80
    import cover_v3 as V
    shade = {0: _soft(c), 1: V.mix(c.acc, c.bg, .5), 2: c.acc}
    for j, t in enumerate(labels): cv.text(gx + (j + .5) * cs, top + 40, t, XB, cv.fit(t, XB, 46, cs - 10, 42), c.fg, "mm")
    for i, t in enumerate(labels):
        cv.text(X0, gy + (i + .5) * cs, t, XB, cv.fit(t, XB, 46, lab - 20, 42), c.fg, "lm")
        for j in range(n):
            v = M[i][j]; x = gx + j * cs; y = gy + i * cs
            cv.rr([x + 6, y + 6, x + cs - 6, y + cs - 6], 18, fill=shade[v])
            if v == 2: cv.text(x + cs / 2, y + cs / 2, "●", XB, 44, c.pillfg, "mm")
    y = gy + n * cs + 60; x = X0
    for v in (2, 1, 0):
        if v not in legend: continue
        cv.rr([x, y - 26, x + 52, y + 26], 12, fill=shade[v]); cv.text(x + 70, y, legend[v], SB, 42, c.fg, "lm"); x += 110 + cv.tw(legend[v], SB, 42)
    _para(cv, X0, y + 60, note, SB, 44, c.fg, W, "lt")
    _src(cv, c, H - 55, src); _done(cv, c, name, "heat")


# (가) 16. 두 축 지도(몰입 통로) ------------------------------------------------------------------------------
def axis(name, c, head, xl, yl, band, zones, note, src):
    """x축 = 실력, y축 = 도전. 대각선 띠(band 글) + zones = [(x 0~1, y 0~1, 글)]."""
    top = 150; s = 640; gx0 = X0 + 120; gy0 = top + 40; gx1 = gx0 + s; gy1 = gy0 + s
    nh = _ph(note, XB, 46, W - 100) + 70
    H = _H(top, 40, s, 120, nh, 50 + _sh(src)); cv = Cv(H, c.bg); B._head(cv, c, head)
    _tri(cv, [(gx0, gy1), (gx0 + 140, gy1), (gx1, gy0 + 140), (gx1, gy0), (gx1 - 140, gy0), (gx0, gy1 - 140)], c.acc)
    cv.line(gx0, gy0, gx0, gy1, c.fg, BOX); cv.line(gx0, gy1, gx1, gy1, c.fg, BOX)
    cv.text(gx1, gy1 + 50, xl, XB, 44, c.fg, "rm")
    for k, ch in enumerate(yl): cv.text(gx0 - 60, gy0 + 40 + k * 52, ch, XB, 44, c.fg, "mm")
    cx_, cy_ = (gx0 + gx1) / 2, (gy0 + gy1) / 2
    cv.text(cx_, cy_, band, XB, 54, c.pillfg, "mm")
    for zx, zy, t in zones:
        cv.text(gx0 + zx * s, gy1 - zy * s, t, XB, 46, c.fg, "mm")
    cv.text(gx1 + 30, gy0 + 40, "도전과 실력이", SB, 42, c.gray, "lm"); cv.text(gx1 + 30, gy0 + 96, "같이 오를 때", SB, 42, c.gray, "lm")
    y = gy1 + 100; cv.rr([X0, y, RT - 10, y + nh], 34, fill=c.fg); _para(cv, CX, y + nh / 2, note, XB, 46, c.bg, W - 100)
    _src(cv, c, H - 55, src); _done(cv, c, name, "axis")


# (다) 17. 학자 카드 -----------------------------------------------------------------------------------------
def person(name, c, head, ko, en, when, rows, link, src):
    """사진 없이 이름 첫 글자 원 + 이름·연도 + [(꼬리표, 글)] + 우리 글과 이어지는 한 줄."""
    top = 150; rh = [_ph(t, SB, 44, W - 230) + 40 for _, t in rows]; lh = _ph(link, XB, 46, W - 100) + 70
    H = _H(top, 260, sum(rh), 40, lh, 50 + _sh(src)); cv = Cv(H, c.bg); B._head(cv, c, head)
    _dot(cv, X0 + 100, top + 120, 100, fill=c.acc); cv.text(X0 + 100, top + 120, ko[0], XB, 96, c.pillfg, "mm")
    cv.text(X0 + 240, top + 80, ko, XB, cv.fit(ko, XB, 60, W - 240, 44), c.fg, "lm")
    cv.text(X0 + 240, top + 140, en, SB, cv.fit(en, SB, 44, W - 240, 42), c.gray, "lm")
    cv.text(X0 + 240, top + 192, when, XB, cv.fit(when, XB, 44, W - 240, 42), _ink(c), "lm")
    y = top + 260
    for (tag, t), h in zip(rows, rh):
        cv.line(X0, y, RT - 10, y, c.line if not c.dark else c.gray, DG.GRID)
        cv.text(X0 + 10, y + h / 2, tag, XB, cv.fit(tag, XB, 44, 200, 42), c.fg, "lm")
        _para(cv, X0 + 220, y + h / 2 - _ph(t, SB, 44, W - 230) / 2, t, SB, 44, c.fg, W - 230, "lt"); y += h
    y += 40; cv.rr([X0, y, RT - 10, y + lh], 34, fill=c.acc); _para(cv, CX, y + lh / 2, link, XB, 46, c.pillfg, W - 100)
    _src(cv, c, H - 55, src); _done(cv, c, name, "person")


# (다) 18. 식(분수) ----------------------------------------------------------------------------------------------
def equation(name, c, head, lhs, num, den, rows, src):
    """lhs = 왼쪽 말, num/den = 분자·분모 낱말 목록. rows = [(낱말, 뜻)]."""
    top = 150; rh = [_ph(t, SB, 44, W - 260) + 36 for _, t in rows]
    H = _H(top, 380, sum(rh), 50 + _sh(src)); cv = Cv(H, c.bg); B._head(cv, c, head)
    cv.rr([X0, top + 30, RT - 10, top + 330], 34, fill=_soft(c))
    lw = cv.tw(lhs + " =", XB, 56); cv.text(X0 + 40, top + 180, lhs + " =", XB, 56, c.fg, "lm")
    fx0 = X0 + 80 + lw; fx1 = RT - 50; fcx = (fx0 + fx1) / 2
    nt = " × ".join(num); dt = " × ".join(den)
    cv.text(fcx, top + 115, nt, XB, cv.fit(nt, XB, 54, fx1 - fx0, 42), c.fg, "mm")
    cv.line(fx0, top + 180, fx1, top + 180, c.fg, LW)
    cv.text(fcx, top + 245, dt, XB, cv.fit(dt, XB, 54, fx1 - fx0, 42), _ink(c), "mm")
    y = top + 370
    for (tag, t), h in zip(rows, rh):
        cv.text(X0 + 10, y + h / 2, tag, XB, cv.fit(tag, XB, 46, 230, 42), _ink(c), "lm")
        _para(cv, X0 + 250, y + h / 2 - _ph(t, SB, 44, W - 260) / 2, t, SB, 44, c.fg, W - 260, "lt"); y += h
    _src(cv, c, H - 55, src); _done(cv, c, name, "equation")


# (가) 19. 세로 막대 -------------------------------------------------------------------------------------------------
def vbar(name, c, head, bars, vmax, note, src, fmt="{:.2f}", groups=()):
    """bars = [(이름, 값, 칠할지)] 0~vmax 막대. 값은 논문 값 그대로. groups = [(묶음 이름, 첫 막대, 끝 막대)] 막대 이름 아래 한 줄."""
    top = 150; gy0 = top + 110; gy1 = gy0 + 520; n = len(bars); gap = 60; bw = (W - 60 - gap * (n - 1)) / n
    nh = _ph(note, XB, 46, W - 100) + 70; gh = 90 if groups else 0
    H = _H(top, 110, 520, 130, gh, nh, 50 + _sh(src)); cv = Cv(H, c.bg); B._head(cv, c, head)
    for t, a, b in groups:
        xa = X0 + 60 + a * (bw + gap); xb = X0 + 60 + b * (bw + gap) + bw
        cv.line(xa, gy1 + 100, xb, gy1 + 100, c.fg, LW2); cv.text((xa + xb) / 2, gy1 + 150, t, XB, cv.fit(t, XB, 46, xb - xa, 42), c.fg, "mm")
    for v in range(0, int(vmax) + 1):
        y = gy1 - v / vmax * (gy1 - gy0); cv.line(X0 + 50, y, RT - 10, y, c.line if not c.dark else c.gray, DG.GRID)
        cv.text(X0 + 30, y, str(v), SB, 42, c.gray, "rm")
    for k, (t, v, on) in enumerate(bars):
        x = X0 + 60 + k * (bw + gap); y = gy1 - v / vmax * (gy1 - gy0)
        cv.rr([x, y, x + bw, gy1], 16, fill=_hf(c) if on else _soft(c), outline=None if on else c.fg, w=0 if on else BOX)
        cv.text(x + bw / 2, y - 40, fmt.format(v), XB, 52, c.fg, "mm")
        cv.text(x + bw / 2, gy1 + 50, t, XB, cv.fit(t, XB, 44, bw + gap - 10, 42), c.fg, "mm")
    y = gy1 + 110 + gh; cv.rr([X0, y, RT - 10, y + nh], 34, fill=c.acc); _para(cv, CX, y + nh / 2, note, XB, 46, c.pillfg, W - 100)
    _src(cv, c, H - 55, src); _done(cv, c, name, "vbar")


# (다) 20. 세모(세 꼭짓점) ------------------------------------------------------------------------------------------
def triangle(name, c, head, verts, fade, center, note, src):
    """verts = [(이름, 짧은 뜻)] 위·왼아래·오른아래. fade = 점선으로 그릴 꼭짓점(먼저 옅어지는 것)."""
    top = 150; cy0 = top + 200; cy1 = top + 640; hw = 340
    P = [(CX, cy0), (CX - hw, cy1), (CX + hw, cy1)]; nh = _ph(note, XB, 46, W - 100) + 70
    H = _H(top, 640, 170, nh, 50 + _sh(src)); cv = Cv(H, c.bg); B._head(cv, c, head)
    for i in range(3):
        a, b = P[i], P[(i + 1) % 3]
        if fade in (i, (i + 1) % 3): _dash(cv, *a, *b, c.gray, LW, 30, 22)
        else: cv.line(*a, *b, c.fg, LW)
    cv.text(CX, (cy0 + 2 * cy1) / 3, center, XB, cv.fit(center, XB, 48, hw, 42), c.fg, "mm")
    for i, ((t, s), (x, y)) in enumerate(zip(verts, P)):
        on = i != fade
        _dot(cv, x, y, 34, fill=_hf(c) if on else c.bg, outline=None if on else c.gray, w=0 if on else BOX)
        tx = x if i == 0 else (max(x, X0 + 160) if i == 1 else min(x, RT - 170))
        ty, sy = (y - 150, y - 92) if i == 0 else (y + 80, y + 134)
        cv.text(tx, ty, t, XB, 50, c.fg if on else c.gray, "mm")
        cv.text(tx, sy, s, SB, 42, c.fg if on else c.gray, "mm")
    y = cy1 + 170; cv.rr([X0, y, RT - 10, y + nh], 34, fill=c.acc); _para(cv, CX, y + nh / 2, note, XB, 46, c.pillfg, W - 100)
    _src(cv, c, H - 55, src); _done(cv, c, name, "triangle")


# (가) 21. 겹 동그라미 ----------------------------------------------------------------------------------------------
def rings(name, c, head, layers, hi, note, src):
    """layers = [(사람 수 글, 뜻)] 안→밖. hi = 칠할 겹(안쪽 몇 겹까지)."""
    top = 150; R = 280; cy = top + 60 + R; nh = _ph(note, XB, 46, W - 100) + 70
    n = len(layers); H = _H(top, 60, 2 * R, 60, nh, 50 + _sh(src)); cv = Cv(H, c.bg); B._head(cv, c, head)
    cxr = X0 + R + 10
    for k in range(n - 1, -1, -1):
        r = R * (k + 1) / n; on = k < hi
        _dot(cv, cxr, cy, r, fill=_hf(c) if on else _soft(c), outline=c.fg if not on else None, w=0 if on else BOX)
    for k, (t, s) in enumerate(layers):
        r = R * (k + .5) / n if k else 0
        cv.text(cxr, cy - r if k else cy, t, XB, 44, _ht(c) if k < hi else c.fg, "mm")
    tx = cxr + R + 50; y = cy - R + 40
    for k, (t, s) in enumerate(layers):
        cv.text(tx, y, t, XB, 44, _ink(c), "lm"); _para(cv, tx, y + 26, s, SB, 42, c.fg, RT - 10 - tx, "lt")
        y += 2 * R / n
    y = cy + R + 60; cv.rr([X0, y, RT - 10, y + nh], 34, fill=c.fg); _para(cv, CX, y + nh / 2, note, XB, 46, c.bg, W - 100)
    _src(cv, c, H - 55, src); _done(cv, c, name, "rings")


# (라) 22. 인용과 세 자리 -----------------------------------------------------------------------------------------------
def quote(name, c, head, quote_txt, by, seats, link, src):
    """quote_txt = 옮긴 말(우리 말), seats = [(숫자, 뜻)] 자리 셋을 굵은 사각으로(내용 그림, 장식 아님)."""
    top = 150; qh = _ph(quote_txt, SER, 54, W - 60, 78); lh = _ph(link, XB, 46, W - 100) + 70
    H = _H(top, 60, qh, 80, 330, 50, lh, 50 + _sh(src)); cv = Cv(H, c.bg); B._head(cv, c, head)
    cv.text(X0, top + 60, "“", SER, 120, _ink(c), "lt")
    _para(cv, X0 + 70, top + 80, quote_txt, SER, 54, c.fg, W - 80, "lt", 78)
    cv.text(RT - 10, top + 100 + qh, by, SB, cv.fit(by, SB, 42, W, 42), c.gray, "rm")
    y = top + 160 + qh; gap = 30; sw = (W - 2 * gap) / 3
    for k, (n_, t) in enumerate(seats):
        x = X0 + k * (sw + gap)
        for j in range(n_):
            bx = x + sw / 2 - (n_ * 70 + (n_ - 1) * 20) / 2 + j * 90
            cv.rr([bx, y + 20, bx + 70, y + 110], 10, fill=c.acc if k == 0 else _soft(c), outline=c.fg, w=BOX)
            cv.line(bx + 10, y + 110, bx + 10, y + 160, c.fg, LW); cv.line(bx + 60, y + 110, bx + 60, y + 160, c.fg, LW)
        cv.text(x + sw / 2, y + 220, f"의자 {n_}개", XB, 46, c.fg, "mm")
        cv.text(x + sw / 2, y + 285, t, SB, cv.fit(t, SB, 44, sw, 42), c.fg, "mm")
    y += 380; cv.rr([X0, y, RT - 10, y + lh], 34, fill=c.acc); _para(cv, CX, y + lh / 2, link, XB, 46, c.pillfg, W - 100)
    _src(cv, c, H - 55, src); _done(cv, c, name, "quote")
