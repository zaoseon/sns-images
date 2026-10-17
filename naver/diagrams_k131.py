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

# 10. 세 풀이 겹침(벤 그림) — '나는 몇 개나 겹칠까' 글 ----------------------------------------
def venn(name, c, head, sets, center, note=""):
    """sets = [(체계, 해당 글자)] 셋(사주·별자리·수비학). center = 셋 다 겹칠 때 그 글이 말하는 한 줄."""
    top = 150; R_ = 200; cx = (L + RT) / 2; cy = top + 150 + R_ + 100; d = 140
    C = [(cx - d, cy - d * .55), (cx + d, cy - d * .55), (cx, cy + d * .75)]
    lines = K.balanced(Cv(10, c.bg), center, XB, 46, RT - L - 40)
    H = int(cy + d * .75 + R_ + 150 + 66 * len(lines) + (70 if note else 0) + 40); cv = Cv(H, c.bg); B._head(cv, c, head)
    for (x, y) in C: _dot(cv, x, y, R_, outline=c.fg, w=6)
    # 이름은 원 바깥(왼쪽 위·오른쪽 위·아래)에 두어 선과 겹치지 않게
    spots = [(L + 10, C[0][1] - R_ - 40, "l"), (RT - 10, C[1][1] - R_ - 40, "r"), (cx, C[2][1] + R_ + 40, "m")]
    for (tx, ty, al), (t, sub) in zip(spots, sets):
        if al == "m": cv.text(tx, ty, t + "  " + sub, XB, 46, c.fg, "mm"); continue
        cv.text(tx, ty - 40, t, XB, 50, c.fg, al + "m"); cv.text(tx, ty + 14, sub, SB, 42, c.gray, al + "m")
    gx, gy = cx, cy - d * .12
    _dot(cv, gx, gy, 46, fill=c.acc); cv.text(gx, gy, "3", XB, 52, c.pillfg, "mm")
    y = cy + d * .75 + R_ + 130
    for ln in lines: cv.text(cx, y, ln, XB, 46, c.fg, "mm"); y += 66
    if note: cv.text(cx, y + 10, note, SB, cv.fit(note, SB, 42, RT - L - 20, 42), c.gray, "mm")
    _done(cv, c, name, "venn")

# 11. 겹친 개수 계단 -------------------------------------------------------------
def steps(name, c, head, levels):
    """levels = [(개수, 그 글의 풀이 한 줄)] 3개부터. 막대 길이 = 개수/3, 풀이는 막대 아래 줄."""
    top = 150; gx = L + 10; gw = RT - L - 20; cv0 = Cv(10, c.bg)
    blocks = [(n, K.balanced(cv0, t, SB, 42, gw - 20)) for n, t in levels]
    H = int(top + sum(76 + 46 + 58 * len(ls) + 30 for _, ls in blocks) + 40); cv = Cv(H, c.bg); B._head(cv, c, head)
    y = top
    for n, ls in blocks:
        w = max(150, gw * n / 3) if n else 150
        cv.rr([gx, y, gx + w, y + 76], 38, fill=c.acc if n == 3 else (c.card if not c.dark else c.line), outline=None if n == 3 else c.fg, w=0 if n == 3 else 4)
        cv.text(gx + 30, y + 38, f"{n}개", XB, 46, c.pillfg if n == 3 else c.fg, "lm")
        for k in range(3):
            if k < n: _dot(cv, gx + w - 40 - 46 * k, y + 38, 13, fill=c.pillfg if n == 3 else c.fg)
        yy = y + 76 + 46
        for ln in ls: cv.text(gx + 4, yy, ln, SB, 42, c.fg if n == 3 else c.gray, "lm"); yy += 58
        y = yy + 30
    _done(cv, c, name, "steps")

def _arrow(cv, c, a, b, col, w=7, head=26):
    cv.line(*a, *b, col, w); ang = math.atan2(b[1] - a[1], b[0] - a[0])
    for s_ in (2.6, -2.6):
        cv.line(b[0], b[1], b[0] + head * math.cos(ang + s_), b[1] + head * math.sin(ang + s_), col, w)

def _exitbox(cv, c, y, text):
    ls = K.balanced(cv, text, XB, 44, RT - L - 120); h = 60 + 62 * len(ls)
    cv.rr([L + 10, y, RT - 10, y + h], 34, fill=c.acc)
    yy = y + 30 + 31
    for ln in ls: cv.text((L + RT) / 2, yy, ln, XB, 44, c.pillfg, "mm"); yy += 62
    return y + h

def _ebh(text, c): return 60 + 62 * len(K.balanced(Cv(10, c.bg), text, XB, 44, RT - L - 120))

def _nodebox(cv, c, x, y, t, w=420):
    ls = K.balanced(cv, t, SB, 42, w - 50); h = 40 + 56 * len(ls)
    cv.rr([x - w / 2, y - h / 2, x + w / 2, y + h / 2], 30, fill=c.card if not c.dark else c.line)
    yy = y - h / 2 + 20 + 28
    for ln in ls: cv.text(x, yy, ln, SB, 42, c.fg, "mm"); yy += 56
    return h

# 12. 되풀이 고리(심리 개념) ---------------------------------------------------------
def loop(name, c, head, nodes, concept, exit_text):
    """nodes = 고리를 도는 마음 2~4개(그 글 심리학 단락의 말). concept = 개념 이름. exit_text = 고리를 끊는 행동(글의 제안)."""
    top = 150; cx = (L + RT) / 2; R_ = 280 if len(nodes) > 2 else 0; cy = top + 360
    H = int(cy + 360 + 60 + _ebh("이렇게 끊어요: " + exit_text, c) + 50); cv = Cv(H, c.bg); B._head(cv, c, head)
    if len(nodes) == 2:
        P_ = [(cx, cy - 190), (cx, cy + 190)]
        _arrow(cv, c, (cx + 250, cy - 110), (cx + 250, cy + 110), c.fg); _arrow(cv, c, (cx - 250, cy + 110), (cx - 250, cy - 110), c.fg)
        cv.text(cx, cy, concept, XB, 48, c.acc if not c.dark else c.fg, "mm")
    else:
        P_ = [(cx + R_ * 1.3 * math.sin(2 * math.pi * k / len(nodes)), cy - R_ * math.cos(2 * math.pi * k / len(nodes))) for k in range(len(nodes))]
        for k in range(len(nodes)):
            a, b = P_[k], P_[(k + 1) % len(nodes)]; mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
            ux, uy = (b[0] - a[0]), (b[1] - a[1]); n_ = math.hypot(ux, uy); ux, uy = ux / n_, uy / n_
            ox, oy = (mx - cx) * .18, (my - cy) * .18   # 화살표를 고리 바깥쪽으로 조금 밀어 상자와 안 겹치게
            _arrow(cv, c, (mx + ox - ux * 45, my + oy - uy * 45), (mx + ox + ux * 45, my + oy + uy * 45), c.fg)
        _dot(cv, cx, cy, 120, fill=c.acc); cv.text(cx, cy, concept, XB, cv.fit(concept, XB, 44, 210, 42), c.pillfg, "mm")
    for (x, y), t in zip(P_, nodes): _nodebox(cv, c, x, y, t, 440 if len(nodes) == 2 else 340)
    _exitbox(cv, c, cy + 360 + 40, "이렇게 끊어요: " + exit_text)
    _done(cv, c, name, "loop")

# 13. 쌓였다 터지는 탑(심리 개념) -------------------------------------------------------
def stack(name, c, head, layers, burst, concept, exit_text):
    """layers = 아래부터 쌓이는 마음, burst = 맨 위에서 터지는 모양 한 줄."""
    top = 160; cx = (L + RT) / 2; bh = 100; n = len(layers)
    H = int(top + 130 + bh * n + 20 * n + 110 + 40 + _ebh("이렇게 풀어요: " + exit_text, c) + 50); cv = Cv(H, c.bg); B._head(cv, c, head)
    y0 = top + 130 + (bh + 20) * n
    for k, t in enumerate(layers):
        w = 760 - 90 * k; y = y0 - (bh + 20) * (k + 1)
        cv.rr([cx - w / 2, y, cx + w / 2, y + bh], 24, fill=c.card if not c.dark else c.line, outline=c.fg, w=3)
        cv.text(cx, y + bh / 2, t, SB, cv.fit(t, SB, 44, w - 40, 42), c.fg, "mm")
    yt = y0 - (bh + 20) * n - 20
    for k in range(-2, 3): _arrow(cv, c, (cx + k * 70, yt), (cx + k * 110, yt - 70), c.acc, 7, 20)
    cv.text(cx, top + 10, burst, XB, 50, c.fg, "mm")
    cv.text(RT - 10, y0 + 40, concept, SB, 42, c.gray, "rm")
    _exitbox(cv, c, y0 + 90, "이렇게 풀어요: " + exit_text)
    _done(cv, c, name, "stack")

# 14. 저울(심리 개념) ------------------------------------------------------------------
def scale(name, c, head, heavy, light, concept, exit_text):
    """heavy = 무겁게 느끼는 쪽(왼쪽, 내려감), light = 가볍게 보는 쪽."""
    top = 150; cx = (L + RT) / 2; py = top + 170; arm = 330; tilt = 0.22
    H = int(py + 520 + 40 + _ebh("이렇게 맞춰요: " + exit_text, c) + 50); cv = Cv(H, c.bg); B._head(cv, c, head)
    lx, ly = cx - arm * math.cos(tilt), py + arm * math.sin(tilt); rx, ry = cx + arm * math.cos(tilt), py - arm * math.sin(tilt)
    cv.line(cx, py, cx, py + 440, c.fg, 10); cv.rr([cx - 120, py + 430, cx + 120, py + 460], 14, fill=c.fg)
    cv.line(lx, ly, rx, ry, c.fg, 10); _dot(cv, cx, py, 18, fill=c.fg)
    for (x, y), t, f in (((lx, ly), heavy, True), ((rx, ry), light, False)):
        cv.line(x, y, x, y + 120, c.fg, 4)
        h = _nodebox(cv, c, x, y + 120 + 70, t, 330) if not f else None
        if f:
            ls = K.balanced(cv, t, XB, 44, 330); hh = 40 + 60 * len(ls)
            cv.rr([x - 190, y + 120, x + 190, y + 120 + hh], 30, fill=c.acc); yy = y + 120 + 20 + 30
            for ln in ls: cv.text(x, yy, ln, XB, 44, c.pillfg, "mm"); yy += 60
    cv.text(cx, py + 500, concept, SB, 42, c.gray, "mm")
    _exitbox(cv, c, py + 540, "이렇게 맞춰요: " + exit_text)
    _done(cv, c, name, "scale")

# 15. 두 쪽 견주기(결정 속도처럼 두 갈래 글) ---------------------------------------------------
def sides(name, c, head, left, right, rows, note=""):
    """left/right = 두 쪽 이름, rows = [(체계, 왼쪽 글, 오른쪽 글)]. 가운데 세로 축에 체계, 양쪽에 알약."""
    top = 150; cx = (L + RT) / 2; rh = 150; pw = 330
    H = int(top + 110 + rh * len(rows) + (90 if note else 30)); cv = Cv(H, c.bg); B._head(cv, c, head)
    cv.text(cx - 260, top + 40, left, XB, 50, c.fg, "mm"); cv.text(cx + 260, top + 40, right, XB, 50, c.fg, "mm")
    cv.line(cx, top + 90, cx, top + 100 + rh * len(rows), c.line, 4)
    for i, (sy, a, b) in enumerate(rows):
        y = top + 110 + i * rh + rh / 2
        cv.rr([cx - 70, y - 34, cx + 70, y + 34], 34, fill=c.fg); cv.text(cx, y, sy, XB, cv.fit(sy, XB, 42, 120, 42) if cv.tw(sy, XB, 42) <= 120 else 42, c.bg, "mm")
        cv.rr([cx - 100 - pw, y - 44, cx - 100, y + 44], 44, fill=c.acc); cv.text(cx - 100 - pw / 2, y, a, XB, cv.fit(a, XB, 44, pw - 40, 42), c.pillfg, "mm")
        cv.rr([cx + 100, y - 44, cx + 100 + pw, y + 44], 44, outline=c.fg, w=5, fill=c.bg); cv.text(cx + 100 + pw / 2, y, b, XB, cv.fit(b, XB, 44, pw - 40, 42), c.fg, "mm")
    if note: cv.text(cx, H - 50, note, SB, cv.fit(note, SB, 42, RT - L - 20, 42), c.gray, "mm")
    _done(cv, c, name, "sides")
