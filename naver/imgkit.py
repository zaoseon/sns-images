"""네이버 본문 이미지 공통 제작 도구 (10/8 대표: 이미지가 저화질이고 글씨가 작다. 폰트·줄간격·배경 규칙을 정해 전부 적용).
기준 문서: zaoseon-site docs/네이버_본문이미지_제작가이드_2026-10-08.md

핵심 규칙
- 모든 좌표는 가로 1280 기준 값이고, 실제로는 2배(2560)로 그려서 `master/`에 둔다(클립·영상용 원본). 블로그에 쓰는 납품판은 1280으로 줄여
  `m1280/`(그리고 옛 위치 `img/`)에 둔다. 처음부터 큰 판을 줄이므로 흐려지지 않는다(예전: 960~1080 판을 1280으로 키운 뒤 640으로 줄임).
- 글자 크기는 높이가 아니라 가로폭 기준이다: 폰 화면(가로 약 360~412)에서 보이는 크기가 14px 이상이어야 하므로 납품판 1280에서
  본문 작은 글 42px 이상, 본문 큰 글 52px 이상, 라벨·제목 54px 이상(제목 72). 줄 수가 많으면 글자를 줄이지 않고 이미지 높이를 늘린다.
- 글꼴: 제목·라벨 Paperlogy ExtraBold, 본문 Pretendard ExtraBold(굵기 800), 한자가 든 줄만 명조. 줄간격 1.35(두 줄 이상 문장).
- 배경: 오행 색 바탕 + 황도 차트 소재 7%(오른쪽 아래, 잘려 나가게). 순검정·글자만 있는 판 금지. 글자색은 어두운 잉크, 보조 글은 (96,90,84).
- 로고 子午線 자오선은 오른쪽 위, 정월 얼굴이 있는 판은 AI 표시를 오른쪽 아래(연회색). 박스 안 글은 세로 가운데.
"""
import os, sys, re
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "pipeline"))
import render as R
from PIL import Image, ImageDraw
S = 2                       # 그리는 배율(master = 1280 x S)
BW = 1280                   # 납품 가로
CW = 1100                   # 내용 폭: 가로 1280 이미지 안에 좌우 흰 여백 90씩. 네이버 PC 편집기는 HTML width를 무시하고 이미지를 화면 폭으로 붙이므로(10/8 확인),
OX = (BW - CW) // 2         #   이미지 안에 여백을 둬서 붙였을 때 내용이 640/740(링크 카드 폭, 약 86%)으로 보이게 한다. 파일은 1280 그대로라 선명하다.
FD = os.path.join(HERE, "..", "pipeline", "fonts") + "/"
TITLE = FD + "Paperlogy-8ExtraBold.ttf"; BODY = FD + "PRETENDARD-EXTRABOLD.OTF"; SER = R.SER
DIM = (96, 90, 84); WHITE = (255, 255, 255)
IMG = os.path.join(HERE, "img"); MASTER = os.path.join(IMG, "master"); DELIV = os.path.join(IMG, "m1280")
CHART = os.path.join(HERE, "..", "assets", "brand_bg", "chart.png")
ONLY = None                 # 다시 만들 글 번호 집합(예: {'n20','n26'}); None이면 전부
WARN = []

def F(path, size): return R.F(path, int(round(size * S)))
def HF(t, path, size):
    f = F(path, size); return R.HF(t, f)

class Cv:
    def __init__(s, h, bg):
        s.h = h; s.bg = bg; s.img = Image.new("RGB", (BW * S, h * S), WHITE); s.d = ImageDraw.Draw(s.img)
        s.d.rounded_rectangle([OX * S, 0, (OX + CW) * S - 1, h * S - 1], 44 * S, fill=bg)
    def tw(s, t, path, size): return s.d.textlength(t, font=HF(t, path, size)) / S
    def text(s, x, y, t, path, size, fill, anchor="la"): s.d.text((x * S, y * S), t, font=HF(t, path, size), fill=fill, anchor=anchor)
    def rr(s, box, r, fill=None, outline=None, w=0):
        s.d.rounded_rectangle([v * S for v in box], r * S, fill=fill, outline=outline, width=int(round(w * S)))
    def line(s, x0, y0, x1, y1, fill, w=2): s.d.line([(x0 * S, y0 * S), (x1 * S, y1 * S)], fill=fill, width=int(round(w * S)))
    def watermark(s, tint, alpha=0.07):
        try: ch = Image.open(CHART).convert("RGBA")
        except Exception: return
        side = int(s.h * 1.5 * S); ch = ch.resize((side, side), Image.LANCZOS)
        a = ch.split()[3].point(lambda v: int(v * alpha)); col = Image.new("RGB", ch.size, tint)
        s.img.paste(col, ((OX + CW) * S - int(side * .62), s.h * S - int(side * .55)), a)
    def fit(s, t, path, size, maxw, lo):
        while size > lo and s.tw(t, path, size) > maxw: size -= 2
        if s.tw(t, path, size) > maxw: WARN.append(("넘침", t, size, maxw))
        return size
    def wrap(s, t, path, size, maxw):
        words = t.split(" "); lines = []; cur = ""
        for w in words:
            tr = (cur + " " + w).strip()
            if s.tw(tr, path, size) <= maxw or not cur: cur = tr
            else: lines.append(cur); cur = w
        if cur: lines.append(cur)
        return lines
    def save(s, name):
        s.d.rectangle([0, 0, OX * S - 1, s.h * S], fill=WHITE); s.d.rectangle([(OX + CW) * S, 0, BW * S, s.h * S], fill=WHITE)   # 워터마크가 여백으로 번지지 않게 마지막에 다시 흰색
        os.makedirs(MASTER, exist_ok=True); os.makedirs(DELIV, exist_ok=True)
        s.img.save(os.path.join(MASTER, name), quality=95, subsampling=0, optimize=True)
        d = s.img.resize((BW, s.h), Image.LANCZOS)
        d.save(os.path.join(DELIV, name), quality=93, subsampling=0, optimize=True); d.save(os.path.join(IMG, name), quality=93, subsampling=0, optimize=True)


CONN = re.compile(r"(,|고|며|서|면|는데|지만|니까|다가|도록|라서|아서|어서|으며|으면|거나|든지)$")
BIND = re.compile(r"(와|과|의)$")          # 다음 말과 한 덩어리(산과|비, 해의|달): 줄 끝에 두지 않는다
ONE = re.compile(r"^[가-힣]$")             # 한 글자 낱말(안·못·더·큰): 줄 끝에 홀로 두지 않는다
def balanced(cv, text, path, size, maxw, units=None):
    """의미 단위로, 줄 폭이 고르게 되도록 줄을 나눈다. 줄 수는 꼭 필요한 만큼(가장 적게). units: 쪼개지 말 덩어리 목록(없으면 띄어쓰기)."""
    toks = units if units else text.split(" ")
    n = len(toks); wd = [cv.tw(t, path, size) for t in toks]; sp = cv.tw(" ", path, size)
    def lw(i, j): return sum(wd[i:j]) + sp * (j - i - 1)
    total = lw(0, n)
    if total <= maxw: return [" ".join(toks)]
    k = 2
    while True:
        # k줄로 나누는 모든 방법 중 비용이 가장 작은 것(토큰 수가 작아 전수 계산)
        best = [None, 1e9]
        def go(i, left, cuts):
            if left == 1:
                cs = cuts + [n]
                ws = [lw(a, b) for a, b in zip([0] + cs[:-1], cs)]
                if max(ws) > maxw: return
                mean = sum(ws) / len(ws); cost = sum((w - mean) ** 2 for w in ws) / (maxw ** 2) * 4
                for a, b in zip([0] + cs[:-1], cs[:-1]):    # 줄 끝(b)에서 끊을 때의 벌점
                    last = toks[b - 1]; core = re.sub(r"[,.!?·]", "", last)
                    if CONN.search(last): cost -= 0.35
                    if BIND.search(core) and len(core) >= 2: cost += 1.2
                    if ONE.match(core): cost += 1.5
                if ws[-1] < 3.2 * size and len(toks[cs[-2]:]) == 1: cost += 1.5    # 끝줄에 짧은 낱말 하나만 남음
                if cost < best[1]: best[:] = [cs[:-1], cost]
                return
            for j in range(i + 1, n - left + 2):
                if lw(i, j) > maxw: break
                go(j, left - 1, cuts + [j])
        go(0, k, [])
        if best[0] is not None: break
        k += 1
        if k > n: return [" ".join(toks)]
    cs = [0] + best[0] + [n]
    return [" ".join(toks[a:b]) for a, b in zip(cs[:-1], cs[1:])]

def _pid(path):
    m = re.search(r"naver_z(\d+)_", os.path.basename(path)); return f"n{int(m.group(1))}" if m else None
def _skip(path): return ONLY is not None and _pid(path) not in ONLY

def _theme():   # naver2.theme(el)이 R에 넣어 둔 색을 읽는다
    return R.INK, R.GOLD, R.PAPER, R.LINE

L = OX + 40; RT = OX + CW - 40          # 내용 안쪽 왼쪽·오른쪽
def head_block(cv, head, acc, fg):
    bw = cv.tw("子午線 자오선", SER, 34) + 24
    cv.text(L, 54, head, TITLE, cv.fit(head, TITLE, 72, RT - L - bw, 52), fg)
    cv.text(RT, 66, "子午線 자오선", SER, 34, acc, "ra")

def rows(path, head, items, note=""):
    """items: [(라벨, 큰 글, 작은 글, 색 'gold'|'red'|None)]. 칸이 한 줄에 다 들어가면 한 줄(라벨 | 큰 글 작은 글), 아니면 두 줄."""
    if _skip(path): return
    bg, acc, fg, line = _theme(); RED = (176, 56, 46)
    items = [tuple(i) + (None,) * (4 - len(i)) for i in items]
    n = len(items); inner = RT - L; top = 168; GAP = 12
    tmp = Cv(100, bg)
    LW = min(250, max(tmp.tw(it[0], TITLE, 50) for it in items) + 30)
    def one(it):   # 한 줄에 들어가는가(큰 글 54, 작은 글 40 그대로)
        need = 32 + LW + 14 + tmp.tw(it[1], BODY, 54) + ((28 + tmp.tw(it[2], BODY, 40)) if it[2] else 0) + 32
        return need <= inner
    single = all(one(it) for it in items)
    RH = 104 if single else (132 if any(it[2] for it in items) else 108)
    H = top + n * RH + (n - 1) * GAP + (110 if note else 60)
    cv = Cv(H, bg); cv.watermark(acc); head_block(cv, head, acc, fg)
    for i, (lab, big, small, col) in enumerate(items):
        y = top + i * (RH + GAP); c = RED if col == "red" else acc
        cv.rr([L, y, RT, y + RH], 28, fill=WHITE, outline=(c if col else line), w=(4 if col else 3))
        cv.text(L + 32, y + RH / 2, lab, TITLE, cv.fit(lab, TITLE, 50, LW - 16, 42), c, "lm")
        x0 = L + 32 + LW + 14; mw = RT - 32 - x0
        if single:
            sb = cv.fit(big, BODY, 54, mw - ((28 + cv.tw(small, BODY, 40)) if small else 0), 46)
            cv.text(x0, y + RH / 2 + 19, big, BODY, sb, fg, "ls")
            if small: cv.text(x0 + cv.tw(big, BODY, sb) + 28, y + RH / 2 + 19, small, BODY, 40, DIM, "ls")
        elif small:
            cv.text(x0, y + 66, big, BODY, cv.fit(big, BODY, 56, mw, 44), fg, "ls")
            cv.text(x0, y + 114, small, BODY, cv.fit(small, BODY, 42, mw, 36), DIM, "ls")
        else:
            cv.text(x0, y + RH / 2, big, BODY, cv.fit(big, BODY, 56, mw, 44), fg, "lm")
    if note: cv.text(L, H - 60, note, BODY, cv.fit(note, BODY, 44, RT - L, 36), acc, "lm")
    cv.save(os.path.basename(path))

def table(path, head, cols, rows_, widths):
    if _skip(path): return
    bg, acc, fg, line = _theme(); n = len(rows_); RH = 112; top = 168; hh = 78
    H = top + hh + n * RH + 60; cv = Cv(H, bg); cv.watermark(acc); head_block(cv, head, acc, fg)
    avail = RT - L; tot = float(sum(widths)); ws = [w * avail / tot for w in widths]; x = L
    for c, w in zip(cols, ws): cv.text(x + 10, top + hh / 2, c, BODY, 44, acc, "lm"); x += w
    cv.line(L, top + hh, RT, top + hh, acc, 4)
    for r in range(n):
        y = top + hh + r * RH; x = L
        for i, (c, w) in enumerate(zip(rows_[r], ws)):
            path_ = TITLE if i == 0 else BODY; size = 54 if i == 0 else 50; mw = w - 24; col = acc if i == 0 else fg
            if cv.tw(c, path_, size) <= mw: cv.text(x + 10, y + RH / 2, c, path_, size, col, "lm")
            else:
                ls = balanced(cv, c, path_, 44, mw)
                if len(ls) > 2 or any(cv.tw(l, path_, 44) > mw + 2 for l in ls): WARN.append(("표 넘침", c, mw))
                for k, l in enumerate(ls[:2]): cv.text(x + 10, y + RH / 2 + (k - (len(ls[:2]) - 1) / 2) * 52, l, path_, 44, col, "lm")
            x += w
        cv.line(L, y + RH, RT, y + RH, line, 3)
    cv.save(os.path.basename(path))

# ---- 정월 얼굴이 있는 카드(한눈에 보기·점수 카드): thumb_sq 색·얼굴 그대로 ----
def _ctx(pid):
    import thumb_sq as TQ, add_extra_images as AX
    c, face = AX.cfg(pid); return TQ, c, face

def _maps_lines(cv, label, maps, size, maxw):
    plain = re.sub(r"\([^)]*[\u4e00-\u9fff][^)]*\)", "", maps)
    items = [t.strip() for t in plain.split(",") if t.strip()]
    units = [(label + "  " if k == 0 else "") + it + ("," if k < len(items) - 1 else "") for k, it in enumerate(items)]
    ls = balanced(cv, "", BODY, size, maxw, units=units)
    out = []
    for l in ls:                                  # 덩어리 하나가 너무 길면 띄어쓰기 단위로 다시 나눈다
        out += balanced(cv, l, BODY, size, maxw) if cv.tw(l, BODY, size) > maxw else [l]
    return out

def intro(pid, summary, maps, path, label="세 풀이"):
    if _skip(path): return
    TQ, c, face = _ctx(pid); R_ = 120
    PL, PR = OX + 28, OX + CW - 28                              # 흰 카드 왼쪽·오른쪽
    X0 = PL + 40 + 2 * R_ + 56; mw = PR - 44 - X0
    tmp = Cv(100, c.bg); lab = "한눈에 보기"; lw = tmp.tw(lab, TITLE, 44) + 64
    for size in range(72, 47, -2):
        ls = balanced(tmp, summary, TITLE, size, mw); lh = int(size * 1.3)
        ml = _maps_lines(tmp, label, maps, 40, mw)
        if len(ls) <= 3 and len(ml) <= 2: break
    block = 72 + 30 + len(ls) * lh + 46 + len(ml) * 52           # 알약 + 간격 + 요약 + 선 + 보조 줄
    H = max(600, 64 + block + 56 + 84)                            # 위 64, 아래 56 + 바닥 줄 84
    cv = Cv(H, c.bg); cv.watermark(c.acc, .06)
    cv.rr([PL, 28, PR, H - 28], 52, fill=c.card, outline=c.line, w=5)
    avail_top, avail_bot = 28, H - 28 - 84                         # 바닥 줄 위까지가 글·얼굴 영역
    y0 = avail_top + (avail_bot - avail_top - block) / 2          # 세로 가운데
    cy = (avail_top + avail_bot) / 2
    TQ.badge(cv.img, cv.d, face, c, int((PL + 40 + R_) * S), int(cy * S), int(R_ * S))
    cv.rr([X0, y0, X0 + lw, y0 + 72], 36, fill=c.acc); cv.text(X0 + 32, y0 + 36, lab, TITLE, 44, c.pillfg, "lm")
    y = y0 + 72 + 30
    for l in ls: cv.text(X0, y, l, TITLE, size, c.fg); y += lh
    cv.line(X0, y + 14, X0 + 150, y + 14, c.acc, 10); yy = y + 46
    for l in ml: cv.text(X0, yy, l, BODY, 40, c.acc); yy += 52
    cv.text(PL + 44, H - 28 - 44, "子午線 자오선", SER, 38, c.acc, "lm"); cv.text(PR - 44, H - 28 - 44, "AI로 생성한 가상의 캐릭터입니다", BODY, 30, c.gray, "rm")
    cv.save(os.path.basename(path))

def bars(pid, title, rows_, path):
    if _skip(path): return
    TQ, c, face = _ctx(pid); n = len(rows_); PL, PR = OX + 28, OX + CW - 28
    mw = PR - 44 - 30 - (PL + 44 + 14 + 224 + 28); tmp = Cv(100, c.bg)
    RH = 138; top = 160; H = top + n * RH + (n - 1) * 12 + 72
    cv = Cv(H, c.bg); cv.watermark(c.acc, .06); cv.rr([PL, 28, PR, H - 28], 52, fill=c.card, outline=c.line, w=5)
    tw_ = cv.tw(title, TITLE, 44) + 60; cv.rr([PL + 44, 56, PL + 44 + tw_, 130], 37, fill=c.acc); cv.text(PL + 44 + 30, 93, title, TITLE, 44, c.pillfg, "lm")
    cv.text(PR - 44, 93, "子午線 자오선", SER, 34, c.acc, "rm")
    for i, (lab, txt) in enumerate(rows_):
        y = top + i * (RH + 12)
        cv.rr([PL + 44, y, PR - 44, y + RH], 30, fill=c.bg, outline=c.line, w=3)
        px0 = PL + 44 + 14; cv.rr([px0, y + 14, px0 + 224, y + RH - 14], 24, fill=c.acc)
        if cv.tw(lab, TITLE, 50) <= 200: cv.text(px0 + 112, y + RH / 2, lab, TITLE, 50, c.pillfg, "mm")
        else:
            ll = balanced(cv, lab, TITLE, 40, 204)[:2]
            if len(ll) > 2 or any(cv.tw(l, TITLE, 40) > 206 for l in ll): WARN.append(("라벨 넘침", lab))
            for k, l in enumerate(ll): cv.text(px0 + 112, y + RH / 2 + (k - (len(ll) - 1) / 2) * 48, l, TITLE, 40, c.pillfg, "mm")
        size = 44; ls = balanced(cv, txt, BODY, size, mw)
        while len(ls) > 2 and size > 38: size -= 2; ls = balanced(cv, txt, BODY, size, mw)
        if len(ls) > 2: WARN.append(("점수 줄 3줄", txt)); ls = ls[:2]
        lh = int(size * 1.32)
        for k, l in enumerate(ls): cv.text(px0 + 224 + 28, y + RH / 2 + (k - (len(ls) - 1) / 2) * lh, l, BODY, size, c.fg, "lm")
    cv.save(os.path.basename(path))
