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
        s.h = h; s.bg = bg; s.img = Image.new("RGB", (BW * S, h * S), bg); s.d = ImageDraw.Draw(s.img)
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
        s.img.paste(col, (BW * S - int(side * .62), s.h * S - int(side * .55)), a)
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
        os.makedirs(MASTER, exist_ok=True); os.makedirs(DELIV, exist_ok=True)
        s.img.save(os.path.join(MASTER, name), quality=95, subsampling=0, optimize=True)
        d = s.img.resize((BW, s.h), Image.LANCZOS)
        d.save(os.path.join(DELIV, name), quality=93, subsampling=0, optimize=True); d.save(os.path.join(IMG, name), quality=93, subsampling=0, optimize=True)

def _pid(path):
    m = re.search(r"naver_z(\d+)_", os.path.basename(path)); return f"n{int(m.group(1))}" if m else None
def _skip(path): return ONLY is not None and _pid(path) not in ONLY

def _theme():   # naver2.theme(el)이 R에 넣어 둔 색을 읽는다
    return R.INK, R.GOLD, R.PAPER, R.LINE

def head_block(cv, head, acc, fg):
    cv.text(64, 54, head, TITLE, cv.fit(head, TITLE, 72, 800, 56), fg)
    cv.text(BW - 64, 64, "子午線 자오선", SER, 40, acc, "ra")

def rows(path, head, items, note=""):
    """items: [(라벨, 큰 글, 작은 글, 색 'gold'|'red'|None)] - 한 줄에 칸 하나, 줄 수만큼 이미지가 길어진다."""
    if _skip(path): return
    bg, acc, fg, line = _theme(); RED = (176, 56, 46)
    items = [tuple(i) + (None,) * (4 - len(i)) for i in items]
    n = len(items); has_small = any(it[2] for it in items); RH = 132 if has_small else 108; GAP = 12; top = 170
    H = top + n * RH + (n - 1) * GAP + (110 if note else 60)
    cv = Cv(H, bg); cv.watermark(acc); head_block(cv, head, acc, fg)
    LW = min(300, max(cv.tw(it[0], TITLE, 54) for it in items) + 36)
    for i, (lab, big, small, col) in enumerate(items):
        y = top + i * (RH + GAP); c = RED if col == "red" else acc
        cv.rr([64, y, BW - 64, y + RH], 28, fill=WHITE, outline=(c if col else line), w=(4 if col else 3))
        cv.text(96, y + RH / 2, lab, TITLE, cv.fit(lab, TITLE, 54, LW - 20, 44), c, "lm")
        x0 = 96 + LW + 16; mw = BW - 64 - 28 - x0
        if small:
            cv.text(x0, y + 66, big, BODY, cv.fit(big, BODY, 58, mw, 46), fg, "ls")
            cv.text(x0, y + 114, small, BODY, cv.fit(small, BODY, 42, mw, 36), DIM, "ls")
        else:
            cv.text(x0, y + RH / 2, big, BODY, cv.fit(big, BODY, 58, mw, 46), fg, "lm")
    if note: cv.text(64, H - 60, note, BODY, cv.fit(note, BODY, 44, BW - 128, 36), acc, "lm")
    cv.save(os.path.basename(path))

def table(path, head, cols, rows_, widths):
    if _skip(path): return
    bg, acc, fg, line = _theme(); n = len(rows_); RH = 112; top = 170; hh = 78
    H = top + hh + n * RH + 60; cv = Cv(H, bg); cv.watermark(acc); head_block(cv, head, acc, fg)
    avail = BW - 128; tot = float(sum(widths)); ws = [w * avail / tot for w in widths]
    x = 64
    for c, w in zip(cols, ws): cv.text(x + 12, top + hh / 2, c, BODY, 44, acc, "lm"); x += w
    cv.line(64, top + hh, BW - 64, top + hh, acc, 4)
    for r in range(n):
        y = top + hh + r * RH; x = 64
        for i, (c, w) in enumerate(zip(rows_[r], ws)):
            path_ = TITLE if i == 0 else BODY; size = 54 if i == 0 else 52; mw = w - 28
            col = acc if i == 0 else fg
            if cv.tw(c, path_, size) <= mw: cv.text(x + 12, y + RH / 2, c, path_, size, col, "lm")
            else:
                sz = 44; ls = cv.wrap(c, path_, sz, mw)[:2]
                if len(ls) > 2 or any(cv.tw(l, path_, sz) > mw for l in ls): WARN.append(("표 넘침", c, mw))
                for k, l in enumerate(ls): cv.text(x + 12, y + RH / 2 + (k - (len(ls) - 1) / 2) * 52, l, path_, sz, col, "lm")
            x += w
        cv.line(64, y + RH, BW - 64, y + RH, line, 3)
    cv.save(os.path.basename(path))

# ---- 정월 얼굴이 있는 카드(한눈에 보기·점수 카드): thumb_sq 색·얼굴 그대로 ----
def _ctx(pid):
    import thumb_sq as TQ, add_extra_images as AX
    c, face = AX.cfg(pid); return TQ, c, face

def intro(pid, summary, maps, path, label="세 풀이"):
    if _skip(path): return
    TQ, c, face = _ctx(pid); H = 640; cv = Cv(H, c.bg); cv.watermark(c.acc, .06)
    cv.rr([32, 32, BW - 32, H - 32], 52, fill=c.card, outline=c.line, w=5)
    R_ = 132; TQ.badge(cv.img, cv.d, face, c, int((78 + R_) * S), int(318 * S), int(R_ * S))
    X0 = 372; mw = BW - 72 - X0
    lab = "한눈에 보기"; lw = cv.tw(lab, TITLE, 44) + 64
    cv.rr([X0, 64, X0 + lw, 136], 36, fill=c.acc); cv.text(X0 + 32, 100, lab, TITLE, 44, c.pillfg, "lm")
    plain = lambda t: re.sub(r"\([^)]*[\u4e00-\u9fff][^)]*\)", "", t)
    for size in range(76, 51, -2):
        ls = cv.wrap(summary, TITLE, size, mw); lh = int(size * 1.3)
        ml = cv.wrap(label + "  " + plain(maps), BODY, 42, mw)[:2]
        end = 168 + len(ls) * lh + 40 + len(ml) * 54
        if len(ls) <= 3 and end <= H - 150 and (len(ls) < 3 or size <= 66): break
    y = 168
    for l in ls: cv.text(X0, y, l, TITLE, size, c.fg); y += lh
    cv.line(X0, y + 14, X0 + 150, y + 14, c.acc, 10)
    yy = y + 44
    for l in ml: cv.text(X0, yy, l, BODY, 42, c.acc); yy += 54
    cv.text(X0, H - 74, "子午線 자오선", SER, 40, c.acc, "lm"); cv.text(BW - 72, H - 74, "AI로 생성한 가상의 캐릭터입니다", BODY, 30, c.gray, "rm")
    cv.save(os.path.basename(path))

def bars(pid, title, rows_, path):
    if _skip(path): return
    TQ, c, face = _ctx(pid); n = len(rows_); RH = 138; top = 168; H = top + n * RH + (n - 1) * 12 + 72
    cv = Cv(H, c.bg); cv.watermark(c.acc, .06); cv.rr([32, 32, BW - 32, H - 32], 52, fill=c.card, outline=c.line, w=5)
    tw_ = cv.tw(title, TITLE, 46) + 64; cv.rr([72, 64, 72 + tw_, 140], 38, fill=c.acc); cv.text(72 + 32, 102, title, TITLE, 46, c.pillfg, "lm")
    cv.text(BW - 72, 100, "子午線 자오선", SER, 38, c.acc, "rm")
    for i, (lab, txt) in enumerate(rows_):
        y = top + i * (RH + 12)
        cv.rr([72, y, BW - 72, y + RH], 30, fill=c.bg, outline=c.line, w=3)
        cv.rr([88, y + 14, 88 + 232, y + RH - 14], 24, fill=c.acc)
        if cv.tw(lab, TITLE, 52) <= 208: cv.text(88 + 116, y + RH / 2, lab, TITLE, 52, c.pillfg, "mm")
        else:   # 긴 라벨은 두 줄로(알약 안 가운데)
            ll = cv.wrap(lab, TITLE, 42, 208)[:2]
            if len(ll) > 2 or any(cv.tw(l, TITLE, 42) > 214 for l in ll): WARN.append(("라벨 넘침", lab))
            for k, l in enumerate(ll): cv.text(88 + 116, y + RH / 2 + (k - (len(ll) - 1) / 2) * 50, l, TITLE, 42, c.pillfg, "mm")
        mw = BW - 72 - 350 - 28; size = 46; ls = cv.wrap(txt, BODY, size, mw)
        while len(ls) > 2 and size > 40: size -= 2; ls = cv.wrap(txt, BODY, size, mw)
        if len(ls) > 2: WARN.append(("점수 줄 3줄", txt)); ls = ls[:2]
        lh = int(size * 1.3)
        for k, l in enumerate(ls): cv.text(350, y + RH / 2 + (k - (len(ls) - 1) / 2) * lh, l, BODY, size, c.fg, "lm")
    cv.save(os.path.basename(path))
