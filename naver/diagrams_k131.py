"""네이버 본문 도식·인포그래픽 (K-131, 대표 10/17 15:25 "내부 이미지도 탬플릿처럼 쓰지 말고 도식화·인포그래픽 넣어라").
옛 5틀(i 결론·b 배지 목록·s 흐름·q 질문·c 해 볼 것)은 '색 판 위 글자 목록'이라 그림이 아니다. 여기 함수는 글 안의 실제 값(띠 관계 표·
손없는날 음력 계산·삼재 연도·힘 쓸 달)만으로 모양을 그린다. 지어낸 수치 없음. 그림 속 핵심은 본문 글에도 있다(N8).
유형(K-131 계획서 1~6): months(열두 달 칸) · wheel(12띠 관계도) · matrix(12x12 교차표) · calendar(달력) · compass(계산 과정 도식) · timeline(연도 흐름)
판·글꼴은 body_v3 와 같다(그 글 표지와 같은 두 색 판 = K-044, 글자 42px 이상, 장식 아이콘·그라데이션 없음 = K-041·K-042, 색 셋 = K-043).
만든 파일은 diagrams.json 에 {파일: 유형}으로 적는다 → k131_check.py 가 글마다 도식 2장 이상·옛 틀 2장 이하를 잰다.
파일은 새 이름만(K-025, imgkit.guard_overwrite)."""
import os, sys, json, math, calendar as CAL
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "pipeline"))
import imgkit as K
from imgkit import Cv, L, RT
import body_v3 as B
XB, SB = B.XB, B.SB
REG = os.path.join(HERE, "diagrams.json")
ZJ = "쥐 소 호랑이 토끼 용 뱀 말 양 원숭이 닭 개 돼지".split()

def _reg(name, typ):
    d = json.load(open(REG, encoding="utf-8")) if os.path.exists(REG) else {}
    d[name] = typ; json.dump(dict(sorted(d.items())), open(REG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

def _done(cv, c, name, typ):
    B._save(cv, name)
    if not B.PREVIEW: _reg(name, typ)

def _dot(cv, x, y, r, fill=None, outline=None, w=0):
    cv.d.ellipse([(x - r) * K.S, (y - r) * K.S, (x + r) * K.S, (y + r) * K.S], fill=fill, outline=outline, width=int(round(w * K.S)))

def _dash(cv, x0, y0, x1, y1, col, w, on, off):
    n = math.hypot(x1 - x0, y1 - y0); ux, uy = (x1 - x0) / n, (y1 - y0) / n; t = 0
    while t < n:
        e = min(n, t + on); cv.line(x0 + ux * t, y0 + uy * t, x0 + ux * e, y0 + uy * e, col, w); t = e + off

def _legend(cv, c, y, items):
    """items = [(그리기 함수(x, y), 글)] 한 줄에 왼쪽부터."""
    x = L + 10
    for draw, t in items:
        draw(x + 26, y); cv.text(x + 64, y, t, SB, 42, c.fg, "lm"); x += 64 + cv.tw(t, SB, 42) + 48

# 1. 열두 달 칸 --------------------------------------------------------------
def months(name, c, head, rows, next_jan=True, up_label="힘을 쓸 달", dn_label="아낄 달"):
    """rows = [(띠 이름, 힘 쓸 달 집합, 아낄 달 집합)]. 달 13 = 이듬해 1월. dn_label=None 이면 둘째 표시는 범례에서 뺀다(그 글에 없는 값)."""
    ncol = 13 if next_jan else 12; lab = 200; top = 150; hh = 66; rh = 80
    gx = L + 10 + lab; cw = (RT - 10 - gx) / ncol
    H = top + hh + rh * len(rows) + 190; cv = Cv(H, c.bg); B._head(cv, c, head)
    if next_jan:   # 이듬해 1월 칸은 바탕을 한 톤 다르게
        x = gx + 12 * cw; cv.rr([x + 2, top, x + cw - 2, top + hh + rh * len(rows)], 18, fill=c.card if c.dark else c.line)
    for m in range(ncol):
        cv.text(gx + (m + .5) * cw, top + hh / 2, str(m % 12 + 1), XB, 42, c.fg, "mm")
    for i, (t, up, dn) in enumerate(rows):
        y = top + hh + i * rh; cy = y + rh / 2
        cv.line(L + 10, y, RT - 10, y, c.line, 2)
        cv.text(L + 14, cy, t, XB, cv.fit(t, XB, 44, lab - 20, 42), c.fg, "lm")
        for m in range(1, ncol + 1):
            x = gx + (m - .5) * cw
            if m in up: _dot(cv, x, cy, 23, fill=c.acc)
            elif m in dn: _dot(cv, x, cy, 20, outline=c.fg, w=6)
            else: _dot(cv, x, cy, 5, fill=c.gray)
    y = top + hh + rh * len(rows) + 70
    _legend(cv, c, y, [(lambda x, y: _dot(cv, x, y, 23, fill=c.acc), up_label)] + ([(lambda x, y: _dot(cv, x, y, 20, outline=c.fg, w=6), dn_label)] if dn_label else []))
    if next_jan: cv.text(RT - 10, y + 70, "맨 오른쪽 칸은 이듬해 1월이에요", SB, 42, c.gray, "rm")
    _done(cv, c, name, "months")

# 2. 12띠 관계도 -------------------------------------------------------------
STY = {"pair": lambda cv, c, a, b: None,
       "solid": lambda cv, c, a, b: cv.line(*a, *b, c.acc, 9),
       "thin": lambda cv, c, a, b: cv.line(*a, *b, c.gray, 5),
       "dash": lambda cv, c, a, b: _dash(cv, *a, *b, c.fg, 7, 26, 18),
       "dot": lambda cv, c, a, b: _dash(cv, *a, *b, c.gray, 7, 8, 14),
       "thick": lambda cv, c, a, b: cv.line(*a, *b, c.acc, 18)}   # 마주 이어진 짝(육합, 이웃하지 않은 두 띠)
def wheel(name, c, head, edges, hi=(), legend=(), note="", focus=None):
    """edges = [(띠 번호, 띠 번호, 'solid'|'thin'|'dash'|'dot')], hi = 칠할 띠 번호. 쥐가 맨 위, 시계 방향(지지 순서)."""
    R, r = 330, 74; top = 150; cx = (L + RT) / 2; cy = top + 20 + R + r
    H = int(cy + R + r + 50 + 80 * len(legend) + (80 if note else 0) + 20); cv = Cv(H, c.bg); B._head(cv, c, head)
    pos = [(cx + R * math.sin(math.radians(30 * i)), cy - R * math.cos(math.radians(30 * i))) for i in range(12)]
    def trim(a, b):
        n = math.hypot(b[0] - a[0], b[1] - a[1]); ux, uy = (b[0] - a[0]) / n, (b[1] - a[1]) / n
        return (a[0] + ux * (r + 8), a[1] + uy * (r + 8)), (b[0] - ux * (r + 8), b[1] - uy * (r + 8))
    for i, j, s in edges:   # 이웃한 두 띠의 짝(육합)은 선이 너무 짧아서 두 원을 굵은 띠로 잇는다
        if s == "pair": cv.line(*pos[i], *pos[j], c.acc, 2 * r * .55)
    for order in ("thin", "dot", "dash", "solid", "thick"):
        for i, j, s in edges:
            if s == order: STY[s](cv, c, *trim(pos[i], pos[j]))
    for i, (x, y) in enumerate(pos):
        on = i in hi
        _dot(cv, x, y, r, fill=c.acc if on else c.bg, outline=None if on else c.fg, w=0 if on else 4)
        if i == focus: _dot(cv, x, y, r + 2, outline=c.fg, w=10)
        cv.text(x, y, ZJ[i], XB, 44 if len(ZJ[i]) < 3 else 42, c.pillfg if on else c.fg, "mm")
    y = cy + R + r + 60
    for kind, t in legend:
        x = L + 10
        if kind == "hi": _dot(cv, x + 34, y, 26, fill=c.acc)
        elif kind == "pair": cv.line(x, y, x + 70, y, c.acc, 30)
        else: STY[kind](cv, c, (x, y), (x + 70, y))
        cv.text(x + 100, y, t, SB, cv.fit(t, SB, 42, RT - L - 120, 42), c.fg, "lm"); y += 80
    if note: cv.text(L + 10, y, note, SB, cv.fit(note, SB, 42, RT - L - 20, 42), c.gray, "lm")
    _done(cv, c, name, "wheel")

def edges_of(i):
    """띠 i 와 육합·삼합·충·원진 (n03 _gung 과 같은 표)."""
    hap = {0: 1, 2: 11, 3: 10, 4: 9, 5: 8, 6: 7}; hap.update({v: k for k, v in list(hap.items())})
    won = {0: 7, 1: 6, 2: 9, 3: 8, 4: 11, 5: 10}; won.update({v: k for k, v in list(won.items())})
    return hap[i], [(i + 4) % 12, (i + 8) % 12], (i + 6) % 12, won[i]

# 3. 12x12 교차표 ------------------------------------------------------------
def matrix(name, c, head):
    lab = 150; top = 150; hh = 70; n = 12; gx = L + 10 + lab; cw = (RT - 10 - gx) / n; rh = 70
    H = top + hh + rh * n + 220; cv = Cv(H, c.bg); B._head(cv, c, head)
    for j in range(n): cv.text(gx + (j + .5) * cw, top + hh / 2, ZJ[j][0], XB, 42, c.fg, "mm")
    def mk(kind, x, y):
        if kind == "hap": _dot(cv, x, y, 22, fill=c.acc)
        elif kind == "tri": _dot(cv, x, y, 19, outline=c.acc, w=7)
        elif kind == "chung": cv.line(x - 17, y - 17, x + 17, y + 17, c.fg, 7); cv.line(x - 17, y + 17, x + 17, y - 17, c.fg, 7)
        elif kind == "won": cv.line(x - 20, y, x + 20, y, c.gray, 8)
    for i in range(n):
        y = top + hh + i * rh; cy = y + rh / 2; cv.line(L + 10, y, RT - 10, y, c.line, 2)
        cv.text(L + 14, cy, ZJ[i], XB, 42, c.fg, "lm")
        h, tri, ch, wo = edges_of(i)
        for j in range(n):
            x = gx + (j + .5) * cw
            if i == j: cv.rr([x - cw / 2 + 6, y + 6, x + cw / 2 - 6, y + rh - 6], 12, fill=c.line); continue
            kind = "hap" if j == h else "tri" if j in tri else "chung" if j == ch else "won" if j == wo else None
            if kind: mk(kind, x, cy)
    y = top + hh + rh * n + 70
    _legend(cv, c, y, [(lambda x, y: mk("hap", x, y), "짝(육합)"), (lambda x, y: mk("tri", x, y), "한 팀(삼합)")])
    _legend(cv, c, y + 80, [(lambda x, y: mk("chung", x, y), "부딪힘(충)"), (lambda x, y: mk("won", x, y), "서운함(원진)")])
    _done(cv, c, name, "matrix")

# 4. 달력 ---------------------------------------------------------------------
def calendar(name, c, head, months_, note="", ring=None):
    """months_ = [(년, 월, 칠할 날 집합)] 한 장에 두 달까지 나란히. ring = {월: 테두리만 칠 날 집합}(절기 같은 기준일)."""
    gap = 40; pw = (RT - L - 20 - gap * (len(months_) - 1)) / len(months_); cw = pw / 7; rh = 76; top = 150
    H = top + 70 + 66 + rh * 6 + (110 if note else 50); cv = Cv(H, c.bg); B._head(cv, c, head)
    for k, (yy, mm, hot) in enumerate(months_):
        x0 = L + 10 + k * (pw + gap)
        cv.text(x0 + 6, top + 36, f"{mm}월", XB, 54, c.fg, "lm")
        for d, w in enumerate("일월화수목금토"): cv.text(x0 + (d + .5) * cw, top + 70 + 33, w, SB, 42, c.gray, "mm")
        weeks = CAL.Calendar(firstweekday=6).monthdayscalendar(yy, mm)
        for r_, wk in enumerate(weeks):
            for d, day in enumerate(wk):
                if not day: continue
                x = x0 + (d + .5) * cw; y = top + 70 + 66 + (r_ + .5) * rh
                if day in hot: _dot(cv, x, y, 32, fill=c.acc)
                elif day in (ring or {}).get(mm, ()): _dot(cv, x, y, 32, outline=c.fg, w=5)
                cv.text(x, y, str(day), XB, 42, c.pillfg if day in hot else c.fg, "mm")
    if note: cv.text(L + 10, H - 60, note, SB, cv.fit(note, SB, 42, RT - L - 20, 42), c.gray, "lm")
    _done(cv, c, name, "calendar")

# 5. 계산 과정 도식(방위) --------------------------------------------------------
def compass(name, c, head, arms, center, example):
    """arms = {'북': '끝자리 7·8', '동': …}. 가운데 = 손 없는 날. example = 계산 예 한 줄."""
    top = 150; cx = (L + RT) / 2; cy = top + 400; D = 290; bw, bh = 330, 150
    H = cy + D + bh / 2 + 150; cv = Cv(int(H), c.bg); B._head(cv, c, head)
    at = {"북": (0, -1), "동": (1, 0), "남": (0, 1), "서": (-1, 0)}
    for k, (dx, dy) in at.items():
        x, y = cx + dx * (D + (90 if dx else 0)), cy + dy * D
        cv.line(cx + dx * 120, cy + dy * 120, x - dx * bw / 2, y - dy * bh / 2, c.line, 6)
        cv.rr([x - bw / 2, y - bh / 2, x + bw / 2, y + bh / 2], 30, fill=c.card)
        cv.text(x, y - 30, f"{k}쪽", XB, 52, c.fg, "mm"); cv.text(x, y + 34, arms[k], SB, 42, c.gray, "mm")
    _dot(cv, cx, cy, 120, fill=c.acc)
    cv.text(cx, cy - 28, center[0], XB, 52, c.pillfg, "mm"); cv.text(cx, cy + 32, center[1], SB, 42, c.pillfg, "mm")
    cv.text(L + 10, H - 70, example, SB, cv.fit(example, SB, 42, RT - L - 20, 42), c.fg, "lm")
    _done(cv, c, name, "compass")

# 6. 연도 흐름 -----------------------------------------------------------------
def timeline(name, c, head, y0, groups, mark=None):
    """groups = [(이름, 시작 해)] 3년 띠(들·눌·날). mark = 칠할 해(세로 띠)."""
    lab = 290; top = 150; hh = 70; rh = 112; n = 12; gx = L + 10 + lab; cw = (RT - 10 - gx) / n
    H = top + hh + rh * len(groups) + (130 if mark else 40); cv = Cv(H, c.bg); B._head(cv, c, head)
    if mark: x = gx + (mark - y0) * cw; cv.rr([x + 2, top + hh - 6, x + cw - 2, top + hh + rh * len(groups) + 6], 16, fill=c.card if c.dark else c.line)
    for k in range(0, n, 3): cv.text(gx + k * cw + 4, top + hh / 2, str(y0 + k), XB, 42, c.fg, "lm")
    for i, (t, s) in enumerate(groups):
        y = top + hh + i * rh; cy = y + rh / 2; cv.line(L + 10, y, RT - 10, y, c.line, 2)
        cv.text(L + 14, cy, t, XB, cv.fit(t, XB, 44, lab - 20, 42), c.fg, "lm")
        x = gx + (s - y0) * cw
        cv.rr([x + 4, cy - 36, x + 3 * cw - 4, cy + 36], 36, fill=c.acc)
        for k, w in enumerate("들눌날"): cv.text(x + (k + .5) * cw, cy, w, XB, 42, c.pillfg, "mm")
    if mark: cv.text(RT - 10, H - 60, f"칠한 세로 칸이 {mark}년이에요", SB, 42, c.gray, "rm")
    _done(cv, c, name, "timeline")

# 7. 한 띠의 열두 달 칸(사주 해: 2월 입춘 ~ 이듬해 1월) -----------------------------------
def monthgrid(name, c, head, cells, note="마지막 칸은 이듬해 1월이에요"):
    """cells = [(월 숫자, 꼬리표 or '', 'up'|'dn'|None)] 12칸(2월부터). 칸 안: 'N월' · 그달의 띠 · 꼬리표(그 글에 적힌 관계만).
    up = 칠한 칸(힘을 쓸 달), dn = 굵은 테두리(아낄 달). 그달의 띠 = 월 지지(2월 寅 … 12월 子, 1월 丑)."""
    cols, gap, ch = 4, 16, 210; top = 150; cw = (RT - L - 20 - gap * (cols - 1)) / cols; rows_ = math.ceil(len(cells) / cols)
    H = int(top + rows_ * (ch + gap) + 170); cv = Cv(H, c.bg); B._head(cv, c, head)
    for k, (m, tag, st) in enumerate(cells):
        x = L + 10 + (k % cols) * (cw + gap); y = top + (k // cols) * (ch + gap)
        if st == "up": cv.rr([x, y, x + cw, y + ch], 26, fill=c.acc); fg = sub = c.pillfg
        elif st == "dn": cv.rr([x, y, x + cw, y + ch], 26, fill=c.card if c.dark else c.bg, outline=c.fg, w=6); fg, sub = c.fg, c.fg
        else: cv.rr([x, y, x + cw, y + ch], 26, fill=c.card); fg, sub = c.fg, c.gray
        cv.text(x + 24, y + 58, f"{m}월", XB, 54, fg, "lm")
        cv.text(x + 24, y + 122, ZJ[m % 12] + " 달", SB, cv.fit(ZJ[m % 12] + " 달", SB, 42, cw - 40, 42), sub, "lm")
        if tag: cv.text(x + 24, y + 172, tag, XB, cv.fit(tag, XB, 42, cw - 40, 42), fg, "lm")
    y = top + rows_ * (ch + gap) + 50
    _legend(cv, c, y, [(lambda x, y: cv.rr([x - 26, y - 26, x + 26, y + 26], 10, fill=c.acc), "힘을 쓸 달"),
                       (lambda x, y: cv.rr([x - 26, y - 26, x + 26, y + 26], 10, outline=c.fg, w=6), "아낄 달")])
    if note: cv.text(L + 10, y + 80, note, SB, cv.fit(note, SB, 42, RT - L - 20, 42), c.gray, "lm")
    _done(cv, c, name, "monthgrid")

# 8. 여섯 운명학 교차표 ---------------------------------------------------------
def cross(name, c, head, cols, rows, note=""):
    """cols = 이 글의 주제(짧게), rows = [(체계, [표시...])] 표시 '●' 같은 방향 · '○' 서로 갈림 · '–' 이 주제는 말하지 않음(계산 안 함)."""
    lab = 240; top = 150; hh = 80; rh = 96; gx = L + 10 + lab; cw = (RT - 10 - gx) / len(cols)
    H = int(top + hh + rh * len(rows) + 200 + (80 if note else 0)); cv = Cv(H, c.bg); B._head(cv, c, head)
    def mk(t, x, y):
        if t == "●": _dot(cv, x, y, 24, fill=c.acc)
        elif t == "○": _dot(cv, x, y, 21, outline=c.fg, w=7)
        else: cv.line(x - 16, y, x + 16, y, c.gray, 6)
    for j, t in enumerate(cols): cv.text(gx + (j + .5) * cw, top + hh / 2, t, XB, cv.fit(t, XB, 44, cw - 16, 42), c.fg, "mm")
    for i, (sysname, marks) in enumerate(rows):
        y = top + hh + i * rh; cy = y + rh / 2; cv.line(L + 10, y, RT - 10, y, c.line, 2)
        quiet = all(m_ not in "●○" for m_ in marks)
        cv.text(L + 14, cy, sysname, XB, cv.fit(sysname, XB, 46, lab - 20, 42), c.gray if quiet else c.fg, "lm")
        for j, m_ in enumerate(marks): mk(m_, gx + (j + .5) * cw, cy)
    y = top + hh + rh * len(rows) + 70
    _legend(cv, c, y, [(lambda x, y: mk("●", x, y), "같은 방향"), (lambda x, y: mk("○", x, y), "서로 갈림"), (lambda x, y: mk("–", x, y), "말하지 않음")])
    if note: cv.text(L + 10, y + 90, note, SB, cv.fit(note, SB, 42, RT - L - 20, 42), c.gray, "lm")
    _done(cv, c, name, "cross")

# 9. 시기 띠그래프(한 해 흐름·절기와 사주 달) -------------------------------------------
def band(name, c, head, axis, ticks, rows, marks=()):
    """axis = (시작, 끝) 숫자 축. ticks = [(위치, 글)]. rows = [(글, 시작, 끝, 'acc'|'out'|'soft')]. marks = [(위치, 글)] 세로 점선 + 아래 설명."""
    lab_top = 150; th = 70; rh = 120; gx = L + 10; gw = RT - L - 20; a0, a1 = axis
    X = lambda v: gx + (v - a0) / (a1 - a0) * gw
    H = int(lab_top + th + rh * len(rows) + 40 + 80 * len(marks) + 40); cv = Cv(H, c.bg); B._head(cv, c, head)
    for v, t in ticks:
        cv.line(X(v), lab_top + th - 10, X(v), lab_top + th + rh * len(rows), c.line, 2); cv.text(X(v) + 8, lab_top + th / 2, t, XB, 42, c.fg, "lm")
    yb = lab_top + th + rh * len(rows) + 10
    order = sorted(range(len(marks)), key=lambda k: -marks[k][0])   # 오른쪽 표시가 위 줄: 왼쪽 표시의 설명 글이 다른 점선을 가로지르지 않게
    yk = {k: yb + 40 + 80 * r for r, k in enumerate(order)}
    for k, (v, t) in enumerate(marks): _dash(cv, X(v), lab_top + th, X(v), yk[k], c.fg, 5, 14, 10)   # 점선을 먼저, 막대가 위에
    for i, (t, s, e, st) in enumerate(rows):
        y = lab_top + th + i * rh + 20; box = [X(s) + 3, y, X(e) - 3, y + rh - 40]
        if st == "acc": cv.rr(box, 40, fill=c.acc); fg = c.pillfg
        elif st == "out": cv.rr(box, 40, fill=c.card if c.dark else c.bg, outline=c.fg, w=6); fg = c.fg
        else: cv.rr(box, 40, fill=c.card if not c.dark else c.line); fg = c.fg
        cv.text((box[0] + box[2]) / 2, y + (rh - 40) / 2, t, XB, cv.fit(t, XB, 46, box[2] - box[0] - 30, 42), fg, "mm")
    for k, (v, t) in enumerate(marks):
        _dot(cv, X(v), yk[k], 12, fill=c.fg)
        right = X(v) + 30 + cv.tw(t, SB, 42) <= RT
        cv.text(X(v) + (26 if right else -26), yk[k], t, SB, 42, c.fg, "lm" if right else "rm")
    _done(cv, c, name, "band")
