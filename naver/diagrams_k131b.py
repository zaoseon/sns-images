"""네이버 본문 도식 2판 (K-131 B2 다시, 대표 10/17 17:42 "새 틀 다섯을 색만 바꿔 돌려 썼다 — 글마다 그 글에만 있는 내용으로").
B2 16편(심리·관계 공통점)은 첫 판에서 세 원 겹침·겹친 개수 계단·고리·저울을 글마다 돌려 써서 다시 틀이 됐다.
여기 함수는 글의 '해 볼 것'·'왜'·심리학 단락에 적힌 장면·순서·시간·행동을 그대로 모양으로 옮긴다(지어낸 수치 없음).
모양: ladder(시간 순서 사다리) · twopanel(두 장면 견주기) · strip(장면 네 칸) · iceberg(겉과 속) · counter(칸 채우기) ·
checklist(체크표) · chat(말풍선) · route(길과 정거장) · battery(충전 막대) · spotlight(비추는 장면) · ruler(10점 눈금) ·
cycle5(오행 상생·상극) · split(큰 일 쪼개기) · timer(5분 타이머) · fork(갈림길) · curve(설렘 곡선) · relay(역할 나누기) · pick(동그라미 하나).
선 굵기는 diagrams_k131 의 LW·BOX·AH(K-133) 한 곳을 쓴다. 같은 모양은 한 배치에 두 번까지(k131_check)."""
import math
import diagrams_k131 as DG
from diagrams_k131 import K, Cv, L, RT, XB, SB, LW, LW2, BOX, AH, _dot, _dash, _arrow, _exitbox, _ebh, _done
import body_v3 as B

W = RT - L - 20          # 쓸 폭
X0 = L + 10

def _lines(t, font, size, w): return DG._bl(Cv(10, (0, 0, 0)), t, font, size, w)

def _para(cv, x, y, t, font, size, col, w, anchor="mm", lh=None):
    """줄 나눔 글 덩어리. anchor 'mm' = (x, y)가 덩어리 가운데, 'lt' = 왼쪽 위. 높이를 돌려준다."""
    ls = _lines(t, font, size, w); lh = lh or int(size * 1.36); h = lh * len(ls)
    yy = (y - h / 2 + lh / 2) if anchor == "mm" else (y + lh / 2)
    for ln in ls:
        cv.text(x if anchor == "mm" else x, yy, ln, font, size, col, "mm" if anchor == "mm" else "lm"); yy += lh
    return h

def _ph(t, font, size, w, lh=None): return (lh or int(size * 1.36)) * len(_lines(t, font, size, w))

def _soft(c): return c.card if not c.dark else c.line

def _tri(cv, pts, col): cv.d.polygon([(x * K.S, y * K.S) for x, y in pts], fill=col)

# 1. 시간 순서 사다리 ------------------------------------------------------------
def ladder(name, c, head, steps, note=""):
    """steps = [(시간 꼬리표, 할 일)] 위에서 아래로. 왼쪽 알약 = 시간, 굵은 세로줄 + 점, 오른쪽 = 할 일."""
    top = 160; pw = 250; tx = X0 + pw + 90; tw = RT - 10 - tx
    hs = [max(110, _ph(t, SB, 44, tw) + 40) for _, t in steps]
    H = int(top + sum(hs) + 30 * (len(steps) - 1) + (110 if note else 40)); cv = Cv(H, c.bg); B._head(cv, c, head)
    lx = X0 + pw + 40; ys = []; y = top
    for h in hs: ys.append(y + h / 2); y += h + 30
    cv.line(lx, ys[0], lx, ys[-1], c.fg, LW)
    for k, ((tag, t), cy, h) in enumerate(zip(steps, ys, hs)):
        cv.rr([X0, cy - 38, X0 + pw, cy + 38], 38, fill=c.acc if k in (0, len(steps) - 1) else _soft(c))
        cv.text(X0 + pw / 2, cy, tag, XB, cv.fit(tag, XB, 44, pw - 30, 42), c.pillfg if k in (0, len(steps) - 1) else c.fg, "mm")
        _dot(cv, lx, cy, 18, fill=c.fg)
        _para(cv, tx, cy - _ph(t, SB, 44, tw) / 2, t, SB, 44, c.fg, tw, "lt")
    if note: cv.text(X0, H - 60, note, SB, cv.fit(note, SB, 42, W, 42), c.gray, "lm")
    _done(cv, c, name, "ladder")

# 2. 두 장면 견주기 ---------------------------------------------------------------
def twopanel(name, c, head, left, right, concept, exit_text, verb="이렇게 풀어요: "):
    """left/right = (제목, 설명, 원 크기 0~1). 같은 마음이 두 장면에서 얼마나 커지는지 원 크기로."""
    top = 160; gap = 30; pw = (W - gap) / 2; ph = 520
    H = int(top + ph + 70 + 40 + _ebh(verb + exit_text, c) + 50); cv = Cv(H, c.bg); B._head(cv, c, head)
    for k, (t, sub, r) in enumerate((left, right)):
        x = X0 + k * (pw + gap); cv.rr([x, top, x + pw, top + ph], 34, fill=_soft(c))
        cv.text(x + pw / 2, top + 60, t, XB, cv.fit(t, XB, 48, pw - 40, 42), c.fg, "mm")
        R = 40 + 100 * r; cy = top + 265
        _dot(cv, x + pw / 2, cy, R, fill=c.acc if k == 0 else None, outline=None if k == 0 else c.fg, w=0 if k == 0 else LW)
        _para(cv, x + pw / 2, top + 440, sub, SB, 42, c.fg, pw - 50)
    _arrow(cv, c, (X0 + pw - 30, top + 265), (X0 + pw + gap + 30, top + 265), c.fg)
    cv.text((L + RT) / 2, top + ph + 45, concept, SB, 42, c.gray, "mm")
    _exitbox(cv, c, top + ph + 90, verb + exit_text)
    _done(cv, c, name, "twopanel")

# 3. 장면 네 칸(ㄹ자 순서) ---------------------------------------------------------
def strip(name, c, head, frames, note=""):
    """frames = 글 4개. 1 → 2 / 4 ← 3 (ㄹ자). 칸마다 큰 번호."""
    top = 160; gap = 90; fw = (W - gap) / 2; tw = fw - 60
    rh = [max(_ph(frames[0], SB, 44, tw), _ph(frames[1], SB, 44, tw)), max(_ph(frames[2], SB, 44, tw), _ph(frames[3], SB, 44, tw))]
    fh = [h + 150 for h in rh]
    H = int(top + fh[0] + gap + fh[1] + (110 if note else 40)); cv = Cv(H, c.bg); B._head(cv, c, head)
    pos = [(0, 0), (1, 0), (1, 1), (0, 1)]
    boxes = []
    for k, (col, row) in enumerate(pos):
        x = X0 + col * (fw + gap); y = top + (0 if row == 0 else fh[0] + gap); h = fh[row]
        last = k == 3
        cv.rr([x, y, x + fw, y + h], 34, fill=c.acc if last else _soft(c))
        _dot(cv, x + 56, y + 56, 34, fill=c.fg if not last else c.pillfg)
        cv.text(x + 56, y + 56, str(k + 1), XB, 44, c.bg if not last else c.acc, "mm")
        _para(cv, x + 30, y + 110, frames[k], SB, 44, c.pillfg if last else c.fg, tw, "lt")
        boxes.append((x, y, h))
    (x1, y1, h1), (x2, y2, h2), (x3, y3, h3), (x4, y4, h4) = boxes
    _arrow(cv, c, (x1 + fw + 12, y1 + h1 / 2), (x2 - 12, y2 + h2 / 2), c.fg)
    _arrow(cv, c, (x2 + fw / 2, y2 + h2 + 12), (x3 + fw / 2, y3 - 12), c.fg)
    _arrow(cv, c, (x3 - 12, y3 + h3 / 2), (x4 + fw + 12, y4 + h4 / 2), c.fg)
    if note: cv.text(X0, H - 60, note, SB, cv.fit(note, SB, 42, W, 42), c.gray, "lm")
    _done(cv, c, name, "strip")

# 4. 겉과 속 ------------------------------------------------------------------------
def iceberg(name, c, head, above, below, concept, exit_text, verb="이렇게 풀어요: "):
    """above = 겉으로 보이는 말(한 줄), below = 물밑에 남는 마음 [글...]. 물 위 작은 봉우리, 물 아래 큰 덩어리."""
    top = 170; cx = (L + RT) / 2; wl = top + 230; bh = 70 + 74 * len(below) + 40
    H = int(wl + bh + 60 + 40 + _ebh(verb + exit_text, c) + 50); cv = Cv(H, c.bg); B._head(cv, c, head)
    _tri(cv, [(cx, top + 40), (cx + 230, wl), (cx - 230, wl)], _soft(c))
    cv.text(cx, wl - 70, above, XB, cv.fit(above, XB, 46, 380, 42), c.fg, "mm")
    cv.text(X0, top + 40, "겉", XB, 52, c.gray, "lm")
    cv.line(X0, wl, RT - 10, wl, c.fg, LW)
    _tri(cv, [(cx - 230, wl + 6), (cx + 230, wl + 6), (cx + 420, wl + bh), (cx - 420, wl + bh)], c.acc)
    cv.text(X0, wl + 60, "속", XB, 52, c.gray, "lm")
    y = wl + 80
    for t in below: cv.text(cx, y, t, XB, cv.fit(t, XB, 44, 640, 42), c.pillfg, "mm"); y += 74
    cv.text(RT - 10, wl + bh + 35, concept, SB, 42, c.gray, "rm")
    _exitbox(cv, c, wl + bh + 80, verb + exit_text)
    _done(cv, c, name, "iceberg")

# 5. 칸 채우기 -------------------------------------------------------------------------
def counter(name, c, head, slots, result, note=""):
    """slots = [(큰 글, 작은 글)] 차례로 채워지는 칸, result = 칸이 다 차면 하는 일."""
    top = 170; n = len(slots); gap = 26; sw = (W - gap * (n - 1)) / n
    sh = 150 + max(_ph(s, SB, 42, sw - 40) for _, s in slots)
    rh = _ph(result, XB, 46, W - 120) + 70
    H = int(top + sh + 150 + rh + (110 if note else 50)); cv = Cv(H, c.bg); B._head(cv, c, head)
    for k, (t, s) in enumerate(slots):
        x = X0 + k * (sw + gap); on = True
        cv.rr([x, top, x + sw, top + sh], 30, fill=_soft(c), outline=c.fg, w=BOX)
        cv.text(x + sw / 2, top + 64, t, XB, cv.fit(t, XB, 52, sw - 30, 42), c.fg, "mm")
        _para(cv, x + sw / 2, top + 110 + (sh - 110) / 2 - 10, s, SB, 42, c.gray if not c.dark else c.fg, sw - 40)
    _arrow(cv, c, ((L + RT) / 2, top + sh + 20), ((L + RT) / 2, top + sh + 120), c.fg)
    y = top + sh + 140; cv.rr([X0, y, RT - 10, y + rh], 34, fill=c.acc)
    _para(cv, (L + RT) / 2, y + rh / 2, result, XB, 46, c.pillfg, W - 120)
    if note: cv.text(X0, H - 60, note, SB, cv.fit(note, SB, 42, W, 42), c.gray, "lm")
    _done(cv, c, name, "counter")

# 6. 체크표 -------------------------------------------------------------------------------
def checklist(name, c, head, items, note=""):
    """items = [(굵은 할 일, 작은 설명 or '')] 빈 네모 = 독자가 채울 칸."""
    top = 160; tx = X0 + 130; tw = RT - 10 - tx - 20
    hs = [max(120, _ph(t, XB, 46, tw) + (_ph(s, SB, 42, tw) + 10 if s else 0) + 50) for t, s in items]
    H = int(top + sum(hs) + 20 * len(items) + (100 if note else 30)); cv = Cv(H, c.bg); B._head(cv, c, head)
    y = top
    for (t, s), h in zip(items, hs):
        cv.rr([X0, y, RT - 10, y + h], 30, fill=_soft(c))
        cv.rr([X0 + 34, y + 32, X0 + 94, y + 92], 12, outline=c.fg, w=BOX)
        hh = _para(cv, tx, y + 26, t, XB, 46, c.fg, tw, "lt")
        if s: _para(cv, tx, y + 26 + hh + 6, s, SB, 42, c.gray, tw, "lt")
        y += h + 20
    if note: cv.text(X0, H - 55, note, SB, cv.fit(note, SB, 42, W, 42), c.gray, "lm")
    _done(cv, c, name, "checklist")

# 7. 말풍선 ---------------------------------------------------------------------------------
def chat(name, c, head, msgs, who=("상대", "나"), note=""):
    """msgs = [('me'|'you', 글)]. 나 = 오른쪽 진한 풍선, 상대 = 왼쪽 옅은 풍선. 글은 그 글 본문의 예문 그대로."""
    top = 170; bw = 680
    hs = [_ph(t, SB, 46, bw - 70) + 56 for _, t in msgs]
    H = int(top + 60 + sum(hs) + 40 * len(msgs) + (100 if note else 30)); cv = Cv(H, c.bg); B._head(cv, c, head)
    if any(s == "you" for s, _ in msgs): cv.text(X0 + 10, top + 10, who[0], SB, 42, c.gray, "lm")
    cv.text(RT - 20, top + 10, who[1], SB, 42, c.gray, "rm")
    y = top + 60
    for (s, t), h in zip(msgs, hs):
        tw_ = min(bw, max(cv.tw(ln, SB, 46) for ln in _lines(t, SB, 46, bw - 70)) + 70)
        if s == "me":
            x1 = RT - 10; x0 = x1 - tw_; cv.rr([x0, y, x1, y + h], 40, fill=c.acc); _tri(cv, [(x1 - 50, y + h - 4), (x1 + 4, y + h + 26), (x1 - 10, y + h - 40)], c.acc)
            col = c.pillfg
        else:
            x0 = X0; x1 = x0 + tw_; cv.rr([x0, y, x1, y + h], 40, fill=_soft(c), outline=c.fg, w=BOX)
            col = c.fg
        _para(cv, x0 + 35, y + 28, t, SB, 46, col, bw - 70, "lt"); y += h + 40
    if note: cv.text(X0, H - 55, note, SB, cv.fit(note, SB, 42, W, 42), c.gray, "lm")
    _done(cv, c, name, "chat")

# 8. 길과 정거장 ---------------------------------------------------------------------------------
def route(name, c, head, stops):
    """stops = [(정거장 이름, 할 일)] 왼쪽에서 오른쪽으로 물결 길 위."""
    top = 170; n = len(stops); cw = W / n; ys = [top + 120 + (0 if k % 2 == 0 else 90) for k in range(n)]
    xs = [X0 + cw * (k + .5) for k in range(n)]
    th = max(_ph(t, SB, 42, cw - 24) for _, t in stops)
    H = int(max(ys) + 90 + th + 60); cv = Cv(H, c.bg); B._head(cv, c, head)
    pts = []
    for k in range(n - 1):
        for j in range(21):
            u = j / 20; x = xs[k] + (xs[k + 1] - xs[k]) * u; y = ys[k] + (ys[k + 1] - ys[k]) * (1 - math.cos(math.pi * u)) / 2
            pts.append((x, y))
    for a, b in zip(pts, pts[1:]): cv.line(*a, *b, c.fg, LW + 2)
    for a in pts[::4]: _dot(cv, *a, (LW + 2) / 2, fill=c.fg)
    for k, ((t, s), x, y) in enumerate(zip(stops, xs, ys)):
        _dot(cv, x, y, 34, fill=c.acc if k in (0, n - 1) else c.bg, outline=None if k in (0, n - 1) else c.fg, w=0 if k in (0, n - 1) else BOX)
        cv.text(x, y - 74, t, XB, cv.fit(t, XB, 46, cw - 16, 42), c.fg, "mm")
        hh = _ph(s, SB, 42, cw - 24); _para(cv, x, max(ys) + 70 + hh / 2, s, SB, 42, c.fg, cw - 24)
    _done(cv, c, name, "route")

# 9. 충전 막대 ---------------------------------------------------------------------------------
def battery(name, c, head, cells, concept="", exit_text="", verb="이렇게 채워요: "):
    """cells = [(위 글, 채움 0~1, 아래 글)] 나란히. 숫자는 쓰지 않는다(얼마나 찼는지 모양만)."""
    top = 170; n = len(cells); gap = 60; cw = (W - gap * (n - 1)) / n; bw, bh = min(260, cw - 80), 380
    th = max(_ph(t, SB, 42, cw - 20) for _, _, t in cells)
    H = int(top + 70 + bh + 50 + th + (60 if concept else 20) + (40 + _ebh(verb + exit_text, c) if exit_text else 0) + 50); cv = Cv(H, c.bg); B._head(cv, c, head)
    for k, (t, f, s) in enumerate(cells):
        cx = X0 + k * (cw + gap) + cw / 2; y0 = top + 70
        cv.text(cx, top + 20, t, XB, cv.fit(t, XB, 48, cw - 20, 42), c.fg, "mm")
        cv.rr([cx - 50, y0 - 26, cx + 50, y0 + 4], 8, fill=c.fg)
        cv.rr([cx - bw / 2, y0, cx + bw / 2, y0 + bh], 34, outline=c.fg, w=BOX + 2)
        inner = bh - 36; fh = inner * f
        cv.rr([cx - bw / 2 + 18, y0 + 18 + inner - fh, cx + bw / 2 - 18, y0 + bh - 18], 20, fill=c.acc)
        _para(cv, cx, y0 + bh + 40 + _ph(s, SB, 42, cw - 20) / 2, s, SB, 42, c.fg, cw - 20)
        if k < n - 1: _arrow(cv, c, (cx + bw / 2 + 20, y0 + bh / 2), (cx + cw + gap - bw / 2 - 20, y0 + bh / 2), c.fg)
    y = top + 70 + bh + 50 + th
    if concept: cv.text(RT - 10, y + 30, concept, SB, 42, c.gray, "rm"); y += 60
    if exit_text: _exitbox(cv, c, y + 20, verb + exit_text)
    _done(cv, c, name, "battery")

# 10. 비추는 장면 ---------------------------------------------------------------------------------
def spotlight(name, c, head, src, lit, dark, concept, exit_text, verb="이렇게 넓혀요: "):
    """src = 빛을 내는 생각(왼쪽 원), lit = 빛 안 장면 글, dark = 빛 밖 장면 글. 빛줄기 안 칸만 칠한다."""
    top = 170; cy = top + 300; sx = X0 + 140
    H = int(cy + 330 + 60 + 40 + _ebh(verb + exit_text, c) + 50); cv = Cv(H, c.bg); B._head(cv, c, head)
    bx = X0 + 380; bw = RT - 10 - bx
    _tri(cv, [(sx + 100, cy - 40), (sx + 100, cy + 40), (RT - 10, cy + 150), (RT - 10, cy - 150)], _soft(c))
    _dot(cv, sx, cy, 130, fill=c.acc); _para(cv, sx, cy, src, XB, 44, c.pillfg, 200)
    rows = [(t, True) for t in lit] + [(t, False) for t in dark]
    # 빛 안 칸: 가운데 세로로, 빛 밖 칸: 위·아래 가장자리
    ins = [cy - 75, cy + 15][:len(lit)] if len(lit) <= 2 else [cy - 110, cy - 20, cy + 70]
    outs = [top + 30, cy + 220][:len(dark)]
    for t, y in zip(lit, ins):
        cv.rr([bx + 40, y - 6, RT - 40, y + 70], 30, fill=c.acc); cv.text((bx + RT) / 2, y + 32, t, XB, cv.fit(t, XB, 44, bw - 110, 42), c.pillfg, "mm")
    for t, y in zip(dark, outs):
        x0, x1, y0, y1 = bx + 40, RT - 40, y, y + 76
        for (a, b) in (((x0, y0), (x1, y0)), ((x1, y0), (x1, y1)), ((x1, y1), (x0, y1)), ((x0, y1), (x0, y0))): _dash(cv, *a, *b, c.gray, LW2, 18, 14)
        cv.text((bx + RT) / 2, y + 38, t, SB, cv.fit(t, SB, 44, bw - 110, 42), c.gray, "mm")
    cv.text(RT - 10, cy + 330, concept, SB, 42, c.gray, "rm")
    _exitbox(cv, c, cy + 380, verb + exit_text)
    _done(cv, c, name, "spotlight")

# 11. 10점 눈금 ---------------------------------------------------------------------------------
def ruler(name, c, head, mine, theirs, concept, exit_text, verb="이렇게 맞춰요: "):
    """0~10 눈금. mine = 내가 드러냈다고 믿는 곳(10 끝), theirs = 상대가 아는 곳(물음표, 자리는 비워 둠)."""
    top = 170; y = top + 300; x0, x1 = X0 + 40, RT - 50
    H = int(y + 230 + 40 + _ebh(verb + exit_text, c) + 50); cv = Cv(H, c.bg); B._head(cv, c, head)
    cv.line(x0, y, x1, y, c.fg, LW + 2)
    for k in range(11):
        x = x0 + (x1 - x0) * k / 10; cv.line(x, y - (30 if k % 5 == 0 else 18), x, y + (30 if k % 5 == 0 else 18), c.fg, LW)
        if k in (0, 5, 10): cv.text(x, y + 70, str(k), XB, 46, c.fg, "mm")
    xm = x1; cv.rr([xm - 340, top + 30, xm + 30, top + 130], 40, fill=c.acc); cv.text(xm - 155, top + 80, mine, XB, cv.fit(mine, XB, 44, 340, 42), c.pillfg, "mm")
    _arrow(cv, c, (xm - 20, top + 140), (xm, y - 40), c.fg)
    xq = x0 + (x1 - x0) * .35; _dot(cv, xq, y - 140, 56, outline=c.fg, w=BOX); cv.text(xq, y - 140, "?", XB, 64, c.fg, "mm")
    cv.text(xq + 80, y - 140, theirs, SB, cv.fit(theirs, SB, 44, 420, 42), c.fg, "lm")
    _dash(cv, xq, y - 80, xq, y - 36, c.fg, LW, 12, 10)
    cv.text(RT - 10, y + 150, concept, SB, 42, c.gray, "rm")
    _exitbox(cv, c, y + 200, verb + exit_text)
    _done(cv, c, name, "ruler")

# 12. 오행 상생·상극 ---------------------------------------------------------------------------------
def cycle5(name, c, head, note=""):
    """나무→불→흙→쇠→물→나무(키워 줌, 바깥 실선) · 나무→흙→물→불→쇠→나무(누름, 안쪽 점선). 그 글 2절의 표 그대로."""
    E = [("나무", "갑·을"), ("불", "병·정"), ("흙", "무·기"), ("쇠", "경·신"), ("물", "임·계")]
    top = 160; R = 300; r = 92; cx = (L + RT) / 2; cy = top + 40 + R + r
    H = int(cy + R + r + 60 + 160 + (80 if note else 0)); cv = Cv(H, c.bg); B._head(cv, c, head)
    P = [(cx + R * math.sin(2 * math.pi * k / 5), cy - R * math.cos(2 * math.pi * k / 5)) for k in range(5)]
    def edge(a, b, gap):
        ux, uy = b[0] - a[0], b[1] - a[1]; n = math.hypot(ux, uy); ux, uy = ux / n, uy / n
        return (a[0] + ux * gap, a[1] + uy * gap), (b[0] - ux * gap, b[1] - uy * gap)
    for k in range(5):   # 누름: 두 칸 건너
        a, b = edge(P[k], P[(k + 2) % 5], r + 16); _dash(cv, *a, b[0] - (b[0] - a[0]) * .06, b[1] - (b[1] - a[1]) * .06, c.gray, LW2, 22, 16)
        _arrow(cv, c, (b[0] - (b[0] - a[0]) * .08, b[1] - (b[1] - a[1]) * .08), b, c.gray, LW2)
    for k in range(5):   # 키워 줌: 이웃
        a, b = edge(P[k], P[(k + 1) % 5], r + 14); _arrow(cv, c, a, b, c.acc if c.dark else c.fg, LW + 2)
    for (t, s), (x, y) in zip(E, P):
        _dot(cv, x, y, r, fill=c.acc); cv.text(x, y - 20, t, XB, 48, c.pillfg, "mm"); cv.text(x, y + 30, s, SB, 42, c.pillfg, "mm")
    y = cy + R + r + 70
    DG._legend(cv, c, y, [(lambda x, y: _arrow(cv, c, (x - 34, y), (x + 22, y), c.acc if c.dark else c.fg, LW + 2), "키워 줘요(편안한 사이)")])
    DG._legend(cv, c, y + 80, [(lambda x, y: _dash(cv, x - 34, y, x + 22, y, c.gray, LW2, 22, 16), "누르는 관계(조율이 필요한 사이)")])
    if note: cv.text(X0, y + 160, note, SB, cv.fit(note, SB, 42, W, 42), c.gray, "lm")
    _done(cv, c, name, "cycle5")

# 13. 큰 일 쪼개기 ---------------------------------------------------------------------------------
def split(name, c, head, big, parts, rest, note=""):
    """big = 큰 일 한 줄 막대, parts = 작은 마감 글들(같은 폭으로 나눔), rest = 다 끝난 뒤 쉬는 칸."""
    top = 170; bh = 110; rw = 230; gx = X0; gw = W - rw - 30
    H = int(top + bh + 130 + bh + 80 + 70 + (80 if note else 30)); cv = Cv(H, c.bg); B._head(cv, c, head)
    cv.rr([gx, top, gx + gw, top + bh], 40, outline=c.fg, w=BOX, fill=_soft(c))
    cv.text(gx + gw / 2, top + bh / 2, big, XB, cv.fit(big, XB, 48, gw - 60, 42), c.fg, "mm")
    y = top + bh + 130; n = len(parts); pw = (gw - 20 * (n - 1)) / n
    for k, t in enumerate(parts):
        x = gx + k * (pw + 20); cv.rr([x, y, x + pw, y + bh], 40, fill=c.acc)
        cv.text(x + pw / 2, y + bh / 2, t, XB, cv.fit(t, XB, 46, pw - 30, 42), c.pillfg, "mm")
        cv.line(x + pw - 6, y - 70, x + pw - 6, y, c.fg, LW); _tri(cv, [(x + pw - 6, y - 70), (x + pw - 6, y - 30), (x + pw - 60, y - 50)], c.fg)
        _arrow(cv, c, (x + pw / 2, top + bh + 14), (x + pw / 2, y - 14), c.gray, LW2)
    x = gx + gw + 30; cv.rr([x, y, x + rw, y + bh], 40, outline=c.fg, w=BOX)
    cv.text(x + rw / 2, y + bh / 2, rest, XB, cv.fit(rest, XB, 44, rw - 30, 42), c.fg, "mm")
    cv.text(gx, y + bh + 60, "깃발 = 날짜를 붙인 작은 마감", SB, 42, c.gray, "lm")
    if note: cv.text(X0, H - 55, note, SB, cv.fit(note, SB, 42, W, 42), c.gray, "lm")
    _done(cv, c, name, "split")

# 14. 5분 타이머 ---------------------------------------------------------------------------------
def timer(name, c, head, minutes, center, side, concept, exit_text, verb="이렇게 시작해요: "):
    """시계판 + minutes 만큼 칠한 부채꼴. side = 오른쪽에 쓰는 흐름 글 [..] (그 글 심리학 단락의 말)."""
    top = 170; R = 230; cx = X0 + R + 20; cy = top + 40 + R
    sw = RT - 10 - (cx + R + 60)
    H = int(cy + R + 70 + 40 + _ebh(verb + exit_text, c) + 50); cv = Cv(H, c.bg); B._head(cv, c, head)
    _dot(cv, cx, cy, R, fill=_soft(c), outline=c.fg, w=BOX + 2)
    a1 = minutes / 60 * 360
    cv.d.pieslice([(cx - R + 18) * K.S, (cy - R + 18) * K.S, (cx + R - 18) * K.S, (cy + R - 18) * K.S], -90, -90 + a1, fill=c.acc)
    for k in range(12):
        ang = math.radians(30 * k); x0, y0 = cx + (R - 46) * math.sin(ang), cy - (R - 46) * math.cos(ang); x1, y1 = cx + (R - 14) * math.sin(ang), cy - (R - 14) * math.cos(ang)
        cv.line(x0, y0, x1, y1, c.fg, LW)
    _dot(cv, cx, cy, 86, fill=c.fg); cv.text(cx, cy, center, XB, 52, c.bg, "mm")
    sx = cx + R + 60; y = top + 60
    for k, t in enumerate(side):
        h = _ph(t, SB, 44, sw); _para(cv, sx, y, t, SB, 44, c.fg if k == len(side) - 1 else c.gray, sw, "lt"); y += h
        if k < len(side) - 1: _arrow(cv, c, (sx + 30, y + 6), (sx + 30, y + 64), c.gray, LW2); y += 76
    cv.text(RT - 10, cy + R + 35, concept, SB, 42, c.gray, "rm")
    _exitbox(cv, c, cy + R + 80, verb + exit_text)
    _done(cv, c, name, "timer")

# 15. 갈림길 ---------------------------------------------------------------------------------
def fork(name, c, head, root, branches, note=""):
    """root 한 칸에서 아래 가지 2~3개로 굵은 선."""
    top = 170; n = len(branches); gap = 26; bw = (W - gap * (n - 1)) / n
    rh = _ph(root, XB, 46, W - 200) + 60; bh = max(_ph(t, XB, 46, bw - 40) for t in branches) + 60
    H = int(top + rh + 150 + bh + (110 if note else 40)); cv = Cv(H, c.bg); B._head(cv, c, head)
    cx = (L + RT) / 2; cv.rr([X0 + 60, top, RT - 70, top + rh], 40, fill=c.acc); _para(cv, cx, top + rh / 2, root, XB, 46, c.pillfg, W - 200)
    yb = top + rh + 150; ym = top + rh + 70
    cv.line(cx, top + rh, cx, ym, c.fg, LW + 2)
    xs = [X0 + k * (bw + gap) + bw / 2 for k in range(n)]
    cv.line(xs[0], ym, xs[-1], ym, c.fg, LW + 2)
    for x, t in zip(xs, branches):
        _arrow(cv, c, (x, ym), (x, yb - 8), c.fg, LW + 2)
        cv.rr([x - bw / 2, yb, x + bw / 2, yb + bh], 34, fill=_soft(c), outline=c.fg, w=BOX); _para(cv, x, yb + bh / 2, t, XB, 46, c.fg, bw - 40)
    if note: cv.text(X0, H - 55, note, SB, cv.fit(note, SB, 42, W, 42), c.gray, "lm")
    _done(cv, c, name, "fork")

# 16. 설렘 곡선 ---------------------------------------------------------------------------------
def curve(name, c, head, labels, keep, concept, exit_text, x_labels=("시작", "익숙해질 무렵"), verb="이렇게 되살려요: "):
    """그대로 두면 빨리 올랐다 옅어지는 선(회색 점선) vs 고마운 점을 말로 전하면 다시 오르는 선(진한 실선, 점선에서 갈라짐). 높이 숫자는 없음.
    labels = (오를 때, 익숙해질 때, 옅어질 때) 그 글 심리학 단락의 말. keep = 진한 선 이름."""
    top = 170; gx0, gx1 = X0 + 20, RT - 30; gy0, gy1 = top + 110, top + 520
    H = int(gy1 + 90 + 170 + 40 + 60 + _ebh(verb + exit_text, c) + 50); cv = Cv(H, c.bg); B._head(cv, c, head)
    cv.line(gx0, gy1, gx1, gy1, c.fg, LW); cv.line(gx0, gy0 - 30, gx0, gy1, c.fg, LW)
    X = lambda u: gx0 + (gx1 - gx0) * u; Y = lambda v: gy1 - (gy1 - gy0) * v
    f = lambda u: (math.sin(u / .18 * math.pi / 2)) if u < .18 else math.exp(-(u - .18) * 3.4) * .92 + .08
    sm = lambda t: 0 if t <= 0 else 1 if t >= 1 else t * t * (3 - 2 * t)
    g = lambda u: f(u) + sm((u - .42) / .2) * (.42 + .07 * math.sin(2 * math.pi * (u - .42) / .19))
    pts = [(X(u / 100), Y(f(u / 100))) for u in range(101)]
    for k in range(0, 100, 2): cv.line(*pts[k], *pts[k + 1], c.gray, LW2)
    q = [(X(u / 100), Y(g(u / 100))) for u in range(42, 101)]
    for a, b in zip(q, q[1:]): cv.line(*a, *b, c.acc if c.dark else c.fg, LW + 2)
    cv.text(X(.18) + 34, Y(1) - 6, labels[0], XB, 44, c.fg, "lm")
    cv.text(gx0, gy1 + 45, x_labels[0], SB, 42, c.fg, "lm"); cv.text(gx1, gy1 + 45, x_labels[1], SB, 42, c.fg, "rm")
    ly = gy1 + 130   # 선 이름은 그래프 밖 범례로(선과 글이 겹치지 않게)
    DG._legend(cv, c, ly, [(lambda x, y: _dash(cv, x - 34, y, x + 22, y, c.gray, LW2, 9, 9), "그대로 두면: " + labels[1] + " → " + labels[2])])
    DG._legend(cv, c, ly + 76, [(lambda x, y: cv.line(x - 34, y, x + 22, y, c.acc if c.dark else c.fg, LW + 2), keep)])
    cv.text(RT - 10, ly + 150, concept, SB, 42, c.gray, "rm")
    _exitbox(cv, c, ly + 200, verb + exit_text)
    _done(cv, c, name, "curve")

# 17. 역할 나누기(두 줄 막대) ---------------------------------------------------------------------------------
def relay(name, c, head, lanes, ticks, note=""):
    """lanes = [(사람, [(글, 시작, 끝, 'acc'|'out')])] 시간 축 0~1. ticks = [(위치, 글)]. 바통처럼 앞 칸이 끝나는 곳에서 다음 칸."""
    top = 170; lab = 230; gx = X0 + lab; gw = RT - 10 - gx; lh = 150
    X = lambda v: gx + gw * v
    H = int(top + 70 + lh * len(lanes) + (110 if note else 40)); cv = Cv(H, c.bg); B._head(cv, c, head)
    for v, t in ticks:
        _dash(cv, X(v), top + 60, X(v), top + 70 + lh * len(lanes), c.gray, LW2, 14, 12)
        cv.text(X(v) + (12 if v < 1 else -12), top + 30, t, XB, 42, c.fg, "lm" if v < 1 else "rm")
    for i, (who, bars) in enumerate(lanes):
        y = top + 70 + i * lh + 25; cv.text(X0 + 4, y + 50, who, XB, cv.fit(who, XB, 46, lab - 20, 42), c.fg, "lm")
        for t, s, e, st in bars:
            box = [X(s) + 6, y, X(e) - 6, y + 100]
            if st == "acc": cv.rr(box, 50, fill=c.acc); col = c.pillfg
            else: cv.rr(box, 50, fill=_soft(c), outline=c.fg, w=BOX); col = c.fg
            cv.text((box[0] + box[2]) / 2, y + 50, t, XB, cv.fit(t, XB, 44, box[2] - box[0] - 40, 42), col, "mm")
    if note: cv.text(X0, H - 55, note, SB, cv.fit(note, SB, 42, W, 42), c.gray, "lm")
    _done(cv, c, name, "relay")

# 18. 동그라미 하나 ---------------------------------------------------------------------------------
def pick(name, c, head, others, chosen, concept, exit_text, verb="이렇게 골라요: "):
    """others = 흐린 칸 글들, chosen = 굵은 동그라미를 친 칸 하나(가운데 줄)."""
    top = 186; n = len(others) + 1; rh = 104; gap = 36
    H = int(top + n * (rh + gap) + 50 + 40 + _ebh(verb + exit_text, c) + 50); cv = Cv(H, c.bg); B._head(cv, c, head)
    items = others[:len(others) // 2] + [chosen] + others[len(others) // 2:]
    y = top
    for t in items:
        on = t is chosen
        if on:
            cv.rr([X0 + 40, y, RT - 50, y + rh], 52, fill=c.acc); cv.text((L + RT) / 2, y + rh / 2, t, XB, cv.fit(t, XB, 48, W - 160, 42), c.pillfg, "mm")
            cv.rr([X0 + 18, y - 16, RT - 28, y + rh + 16], (rh + 32) / 2, outline=c.fg, w=LW)
        else:
            cv.rr([X0 + 110, y + 10, RT - 120, y + rh - 10], 40, fill=_soft(c)); cv.text((L + RT) / 2, y + rh / 2, t, SB, cv.fit(t, SB, 44, W - 300, 42), c.gray, "mm")
        y += rh + gap
    cv.text(RT - 10, y + 20, concept, SB, 42, c.gray, "rm")
    _exitbox(cv, c, y + 70, verb + exit_text)
    _done(cv, c, name, "pick")
