"""채널별 템플릿 엔진(10/6 대표 제안): 내용만 넣으면 채널 안전영역 안에 글자·요소가 자동으로 배치되고, 안전영역 밖(UI에 가려지는 곳)에는 배경만 깔린다.
흐름: 채널 지오메트리(channel_specs) → 내용 칸(slot)에 글자 맞춤(fit) → 요소 좌표 계산 → 안전영역 검증 → HTML 한 장 → 그림.
- 글자는 칸 크기에 맞춰 가장 큰 글자로 줄바꿈(단어 중간 안 끊음). 최소 크기(본문 44px)보다 작아져야 하면 '넘침'으로 표시해 만들기를 막는다.
- 모든 요소의 좌표를 만들기 전에 계산하므로, 안전영역을 넘는 요소는 만들어지지 않는다(검증 통과가 만들기 조건).
사용: python3 pipeline/template_engine.py  -> 2026-motion/tpl/ (시제품: 같은 내용 3종 × 릴스·캐러셀)"""
import os, sys, asyncio, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from PIL import Image, ImageFont
import fonts_kit as K, brand_frame as BF
R = os.path.abspath(os.path.join(HERE, ".."))
AS = os.path.join(R, "assets", "brand_bg")
GOLD = "#e7c88d"; PINK = "#ff5c9d"; BLUE = "#4560f0"
# 채널 지오메트리: W,H · 안전영역 · 위 고정줄 아래 y · 아래 고정줄 위 y · 제목 글꼴 · brand_frame 종류
CHAN = {"reel": dict(W=1080, H=1920, safe=(50, 330, 900, 1470), head_bottom=385, foot_top=1425, title="gm_bold", kind="reel", stacked=False, gap=25, min_body=44),
        "carousel": dict(W=1080, H=1440, safe=(55, 55, 1025, 1385), head_bottom=108, foot_top=1350, title="pl_blk", kind="card", stacked=False, gap=22, min_body=44)}
def content_box(ch):
    c = CHAN[ch]; s = c["safe"]; return (s[0], c["head_bottom"] + c["gap"], s[2], c["foot_top"] - c["gap"])
_F = {}
def font(path, size):
    k = (path, size)
    if k not in _F: _F[k] = ImageFont.truetype(path, size)
    return _F[k]
def _greedy(words, fnt, maxw):
    line = ""; out = []
    for w in words:
        t = (line + " " + w).strip()
        if line and fnt.getlength(t) > maxw: out.append(line); line = w
        else: line = t
    out.append(line); return out
def _balanced(words, fnt, n):
    """같은 줄 수(n)에서 가장 긴 줄이 가장 짧아지게 나눈다(한 단어만 덜렁 남는 줄바꿈을 막는다)."""
    import itertools
    best = None
    for cuts in itertools.combinations(range(1, len(words)), n - 1):
        parts = []; prev = 0
        for c in list(cuts) + [len(words)]: parts.append(" ".join(words[prev:c])); prev = c
        ws = [fnt.getlength(x) for x in parts]; key = (max(ws), sum(w * w for w in ws))
        if best is None or key < best[0]: best = (key, parts)
    return best[1] if best else [" ".join(words)]
def wrap(text, fnt, maxw):
    """명시한 줄바꿈(\n)은 그대로 지키고, 한 줄에 안 들어가는 문장만 균형 있게 나눈다. 단어 중간은 끊지 않는다."""
    out = []
    for para in text.split("\n"):
        words = para.split(" "); g = _greedy(words, fnt, maxw)
        out += _balanced(words, fnt, len(g)) if len(g) > 1 and len(words) <= 14 else g
    return out
def fit(text, path, box_w, box_h, max_size, min_size, lh=1.25):
    """칸(box_w x box_h)에 들어가는 가장 큰 글자 크기와 줄. 못 들어가면 overflow=True."""
    for size in range(max_size, min_size - 1, -2):
        f = font(path, size); lines = wrap(text, f, box_w); w = max(f.getlength(l) for l in lines); h = len(lines) * size * lh
        if w <= box_w and h <= box_h: return dict(size=size, lines=lines, w=w, h=h, overflow=False, lh=lh)
    f = font(path, min_size); lines = wrap(text, f, box_w); return dict(size=min_size, lines=lines, w=max(f.getlength(l) for l in lines), h=len(lines) * min_size * lh, overflow=True, lh=lh)
def fit_line(text, path, wmax, hmax, max_size, min_size):
    """한 줄 라벨: 줄바꿈 없이 칸 폭 안에 들어가는 가장 큰 글자."""
    for size in range(max_size, min_size - 1, -2):
        f = font(path, size); w = f.getlength(text)
        if w <= wmax and size * 1.1 <= hmax: return dict(size=size, lines=[text], w=w, h=size * 1.1, overflow=False)
    f = font(path, min_size); return dict(size=min_size, lines=[text], w=f.getlength(text), h=min_size * 1.1, overflow=True)
class Page:
    def __init__(self, ch): self.ch = ch; self.c = CHAN[ch]; self.els = []; self.html = []; self.cb = content_box(ch); self.problems = []
    def title_path(self): return K.P[self.c["title"]]
    def body_path(self): return K.P["pr_xb"]
    def add(self, name, rect, html, text=False):
        self.els.append((name, rect)); self.html.append(html)
        s = self.c["safe"]
        if rect[0] < s[0] - 1 or rect[2] > s[2] + 1 or rect[1] < s[1] - 1 or rect[3] > s[3] + 1: self.problems.append(f"{name} 안전영역 밖 {tuple(round(v) for v in rect)}")
    def check_center(self, name, box, children, tol=8):
        """박스 안 글 묶음의 위·아래, 왼쪽·오른쪽 안쪽 여백이 같은지 본다(R18). 어긋나면 만들기를 막는다."""
        ux0 = min(c[0] for c in children); uy0 = min(c[1] for c in children); ux1 = max(c[2] for c in children); uy1 = max(c[3] for c in children)
        t, b, l, r = uy0 - box[1], box[3] - uy1, ux0 - box[0], box[2] - ux1
        if abs(t - b) > tol: self.problems.append(f"{name} 안 글이 세로로 치우침(위 {t:.0f}px · 아래 {b:.0f}px)")
        if abs(l - r) > tol: self.problems.append(f"{name} 안 글이 가로로 치우침(왼쪽 {l:.0f}px · 오른쪽 {r:.0f}px)")
    def text(self, name, txt, role, cx, top, box_w, box_h, max_size, min_size, color="#fff", lh=1.25, align="center", weight=900):
        path = self.title_path() if role == "title" else self.body_path(); r = fit(txt, path, box_w, box_h, max_size, min_size, lh)
        if r["overflow"]: self.problems.append(f"{name} 글자가 칸에 안 들어감(최소 {min_size}px에서도 넘침)")
        fam = K.D if role == "title" else K.B; x0 = cx - r["w"] / 2 if align == "center" else cx
        html = f'<div style="position:absolute;left:{cx - box_w / 2 if align == "center" else cx:.0f}px;top:{top:.0f}px;width:{box_w:.0f}px;text-align:{align};font-family:{fam};font-weight:{weight};font-size:{r["size"]}px;line-height:{lh};color:{color};white-space:pre-line">' + "\n".join(r["lines"]) + '</div>'
        self.add(name, (x0, top, x0 + r["w"], top + r["h"]), html); return r
def bg_html(ch):
    c = CHAN[ch]; W, H = c["W"], c["H"]
    src = os.path.join(AS, "derived", "bg_cosmos.jpg")
    if ch == "reel": img = f'<img style="position:absolute;left:0;top:0;width:{W}px;height:{H}px" src="file://{src}">'
    else: img = f'<img style="position:absolute;left:0;top:{-(1920 - H) // 2}px;width:1080px;height:1920px" src="file://{src}">'
    chart = f'<img style="position:absolute;left:{(W - 1100) // 2}px;top:{(H - 1100) // 2}px;width:1100px;height:1100px;opacity:.38" src="file://{os.path.join(AS, "chart.png")}">'
    sm = ""
    if ch == "reel": sm = f'<img style="position:absolute;left:60px;top:60px;width:270px;mix-blend-mode:screen;-webkit-mask-image:radial-gradient(circle,#000 52%,transparent 74%)" src="file://{os.path.join(AS, "derived", "sun.png")}"><img style="position:absolute;left:760px;top:20px;width:230px;mix-blend-mode:screen;-webkit-mask-image:radial-gradient(circle,#000 52%,transparent 74%)" src="file://{os.path.join(AS, "derived", "moon.png")}">'
    return img + chart + sm + '<div style="position:absolute;left:0;top:0;width:100%;height:100%;background:radial-gradient(ellipse 62% 40% at 50% 52%,rgba(4,8,26,.55),transparent 78%)"></div>'
# ---------------- 템플릿 3종 ----------------
def t_hook(ch, title, left, right, mid):
    p = Page(ch); x0, y0, x1, y1 = p.cb; cw, chh = x1 - x0, y1 - y0; cx = (x0 + x1) / 2
    tr = p.text("제목", title, "title", cx, y0, cw, chh * 0.40, 112, 72, lh=1.2)
    top = y0 + tr["h"] + 24; avail = y1 - top; D = min(avail, cw / 1.62); gap = D * .62; gx0 = cx - (gap + D) / 2; cy = top + (avail - D) / 2
    p.add("원 묶음", (gx0, cy, gx0 + gap + D, cy + D), f'<div style="position:absolute;left:0;top:0;width:{p.c["W"]}px;height:{p.c["H"]}px;isolation:isolate"><div style="position:absolute;left:{gx0:.0f}px;top:{cy:.0f}px;width:{D:.0f}px;height:{D:.0f}px;border-radius:50%;background:{PINK};mix-blend-mode:multiply"></div><div style="position:absolute;left:{gx0 + gap:.0f}px;top:{cy:.0f}px;width:{D:.0f}px;height:{D:.0f}px;border-radius:50%;background:{BLUE};mix-blend-mode:multiply"></div></div>')
    mid_y = cy + D / 2; ex = D * .62
    for name, txt, ccx, wmax, mx in (("왼쪽 글자", left, gx0 + ex / 2, ex * .86, 120), ("오른쪽 글자", right, gx0 + gap + D - ex / 2, ex * .86, 96), ("가운데 글자", mid, gx0 + gap + (D - gap) / 2 if False else gx0 + D - (D - gap) / 2, (D - gap) * .8, 64)):
        r = fit_line(txt, p.title_path(), wmax, D * .3, mx, 40); t = mid_y - r["h"] / 2
        if r["overflow"]: p.problems.append(f"{name} 글자가 칸에 안 들어감")
        p.add(name, (ccx - r["w"] / 2, t, ccx + r["w"] / 2, t + r["h"]), f'<div style="position:absolute;left:{ccx - wmax / 2:.0f}px;top:{t:.0f}px;width:{wmax:.0f}px;text-align:center;font-family:{K.D};font-weight:900;font-size:{r["size"]}px;line-height:1.1;color:#fff;white-space:nowrap">{r["lines"][0]}</div>')
    return p
def t_ranking(ch, title, rows, unit="%"):
    """제목은 의미 단위로 줄바꿈(명시한 \n 우선)·가운데 정렬. 제목과 그래프 사이 간격은 하단 여백을 남기도록 함께 계산한다(10/6 대표 지정)."""
    p = Page(ch); x0, y0, x1, y1 = p.cb; cw = x1 - x0; cx = (x0 + x1) / 2; chh = y1 - y0
    tr = p.text("제목", title, "title", cx, y0, cw, 170, 58, 44, lh=1.2)
    bottom_margin = max(40, chh * .04); gap = max(30, chh * .035)            # 그래프 아래 여백과 제목-그래프 간격을 함께 확보
    top = y0 + tr["h"] + gap; area = y1 - bottom_margin - top; n = len(rows); pitch = area / n; bh = pitch * .88; mx = max(v for _, v in rows)
    fs = int(min(56, bh * .8)) // 2 * 2
    if fs < p.c["min_body"]: p.problems.append(f"막대 글자가 {fs}px로 최소 {p.c['min_body']}px보다 작음")
    for i, (nm, v) in enumerate(rows):
        w = cw * (.30 + .70 * v / mx); t = top + i * pitch; col = "linear-gradient(90deg,#c9a24a,#e7c88d)" if i == 0 else "linear-gradient(90deg,#6a3fc8,#ff5c9d)"; tc = "#17102b" if i == 0 else "#fff"
        p.add(f"막대 {nm}", (x0, t, x0 + w, t + bh), f'<div style="position:absolute;left:{x0:.0f}px;top:{t:.0f}px;width:{w:.0f}px;height:{bh:.0f}px;border-radius:0 {bh / 2:.0f}px {bh / 2:.0f}px 0;background:{col};font-family:{K.D};font-weight:900;font-size:{fs}px;line-height:{bh:.0f}px;color:{tc}"><span style="position:absolute;left:24px">{nm}</span><span style="position:absolute;right:24px">{v:.1f}{unit}</span></div>')
    return p

def cta_vertical(ch, hs, pad=60, gaps=None):
    """마무리 장면의 세로 배치: 카드 높이 = 안쪽 글 높이 + 위아래 같은 여백(글이 카드 가운데), 전체 묶음도 내용 영역 가운데(10/6 대표: 카드 안 글이 위로 치우침).
    hs: dict a,b,ia,ib,ic,btn = 각 줄 높이."""
    g = dict(a_b=8, b_card=36, ia_ib=14, ib_ic=12, card_btn=40); g.update(gaps or {})
    x0, y0, x1, y1 = content_box(ch); chh = y1 - y0
    inner = hs["ia"] + g["ia_ib"] + hs["ib"] + g["ib_ic"] + hs["ic"]; card_h = inner + 2 * pad
    stack = hs["a"] + g["a_b"] + hs["b"] + g["b_card"] + card_h + g["card_btn"] + hs["btn"]; top = y0 + (chh - stack) / 2; T = {}
    T["a"] = top; T["b"] = T["a"] + hs["a"] + g["a_b"]; T["card"] = T["b"] + hs["b"] + g["b_card"]; T["card_h"] = card_h
    T["ia"] = T["card"] + pad; T["ib"] = T["ia"] + hs["ia"] + g["ia_ib"]; T["ic"] = T["ib"] + hs["ib"] + g["ib_ic"]; T["btn"] = T["card"] + card_h + g["card_btn"]; T["end"] = T["btn"] + hs["btn"]; T["pad"] = pad
    return T

def t_cta(ch, big, accent, card_top, card_mid, btn):
    p = Page(ch); x0, y0, x1, y1 = p.cb; cw = x1 - x0; cx = (x0 + x1) / 2; chh = y1 - y0; u = chh / 990.0
    tp = p.title_path(); cxl, cxr = x0 + cw * .03, x1 - cw * .03; iw = cxr - cxl - 60
    fa = fit(big, tp, cw, 150 * u, 100, 64, 1.15); fb = fit(accent, tp, cw, 120 * u, 84, 56, 1.15)
    fia = fit(card_top, tp, iw, 80 * u, 54, 44, 1.2); fib = fit(card_mid[0], tp, iw, 120 * u, 78, 52, 1.2); fic = fit(card_mid[1], tp, iw, 90 * u, 56, 44, 1.25)
    for nm, f in (("큰 문구", fa), ("강조 문구", fb), ("카드 첫줄", fia), ("카드 가운데", fib), ("카드 끝줄", fic)):
        if f["overflow"]: p.problems.append(f"{nm} 글자가 칸에 안 들어감")
    bh = min(104 * u, 110); T = cta_vertical(ch, dict(a=fa["h"], b=fb["h"], ia=fia["h"], ib=fib["h"], ic=fic["h"], btn=bh), pad=60 * u)
    def line(name, f, top, color="#fff", w=None):
        w = w or cw; html = f'<div style="position:absolute;left:{cx - w / 2:.0f}px;top:{top:.0f}px;width:{w:.0f}px;text-align:center;font-family:{K.D};font-weight:900;font-size:{f["size"]}px;line-height:{f["lh"]};color:{color};white-space:pre-line">' + "\n".join(f["lines"]) + "</div>"
        p.add(name, (cx - f["w"] / 2, top, cx + f["w"] / 2, top + f["h"]), html)
    line("큰 문구", fa, T["a"]); line("강조 문구", fb, T["b"], GOLD)
    p.add("카드", (cxl, T["card"], cxr, T["card"] + T["card_h"]), f'<div style="position:absolute;left:{cxl:.0f}px;top:{T["card"]:.0f}px;width:{cxr - cxl:.0f}px;height:{T["card_h"]:.0f}px;border:3px solid {GOLD};border-radius:44px;background:linear-gradient(145deg,rgba(28,40,92,.9),rgba(9,14,44,.9));box-shadow:0 0 46px rgba(231,200,141,.25)"></div>')
    line("카드 첫줄", fia, T["ia"], GOLD, iw); line("카드 가운데", fib, T["ib"], "#fff", iw); line("카드 끝줄", fic, T["ic"], "#fff", iw)
    p.check_center("카드", (cxl, T["card"], cxr, T["card"] + T["card_h"]), [e[1] for e in p.els if e[0] in ("카드 첫줄", "카드 가운데", "카드 끝줄")])
    bw = min(cw * .56, 520); by = T["btn"]
    p.add("버튼", (cx - bw / 2, by, cx + bw / 2, by + bh), f'<div style="position:absolute;left:{cx - bw / 2:.0f}px;top:{by:.0f}px;width:{bw:.0f}px;height:{bh:.0f}px;border-radius:{bh / 2:.0f}px;background:{GOLD};color:#17102b;text-align:center;font-family:{K.D};font-weight:900;font-size:58px;line-height:{bh:.0f}px">{btn}</div>')
    return p
SIX = ["안정", "표현", "유연", "생성", "결단", "소통"]
def explain_layout(ch, texts=("사주와 별자리는 각자 내 마음의 방향을 하나씩 짚어요", "둘이 같은 방향을 짚으면 '같은\u00a0말'이에요", "방향이 다르면 '다른\u00a0말'이에요. 내가 고를 곳이에요")):
    """정월 설명 틀의 모든 좌표(10/6 대표 지정): ① 말풍선 글은 의미 단위 줄바꿈·가운데 정렬, 정월 배지 글자는 중앙 ② 여섯 방향은 3x2로 가운데 정렬(크기는 전체 배치에 맞춤) ③ 설명글(사주가 짚은 방향 등)은 작게 ④ 가운데 기준은 캔버스 가운데."""
    c = CHAN[ch]; x0, y0, x1, y1 = content_box(ch); W = c["W"]; cx = W / 2; chh = y1 - y0; u = chh / 990.0; half = min(cx - x0, x1 - cx); L = dict(cx=cx, u=u, half=half)
    rowA = 300 * u; D = 270 * u; L["avatar"] = (x0 + 10, y0 + 6 * u, D)
    bl = x0 + 10 + D + 30; bw = x1 - bl - 12; bh = rowA - 14 * u; bt = y0 + 10 * u; L["bubble"] = (bl, bt, bw, bh)
    path = K.P["pr_xb"]; pad_x, pad_y = 36 * u, 30 * u; fits = [fit(t, path, bw - 2 * pad_x, bh - 2 * pad_y, 58, 44, 1.32) for t in texts]
    fs = min(f["size"] for f in fits); lines = []
    for t in texts:
        r = fit(t, path, bw - 2 * pad_x, bh - 2 * pad_y, fs, fs, 1.32); lines.append(r["lines"])      # 같은 글자 크기로 줄바꿈
    L["bubble_fs"] = fs; L["bubble_lines"] = lines; L["bubble_overflow"] = any(f["overflow"] for f in fits)
    L["badge"] = (bl + 30 * u, bt - 27 * u, 54 * u)                                                      # 왼쪽, 위, 높이 (너비는 글자 폭 + 여백, 글자는 중앙)
    y = y0 + rowA; ban_top = y + 40 * u; ban_fs = int(72 * u) // 2 * 2; L["banner"] = (ban_top, ban_fs); y = ban_top + 82 * u
    td = 112 * u; tok_top = y + 14 * u; L["tok"] = (tok_top, td); y = tok_top + td
    lab_top = y + 14 * u; lab_fs = int(46 * u) // 2 * 2; L["label"] = (lab_top, lab_fs); y = lab_top + 56 * u
    gap = 14 * u; cwid = min(240 * u * (1 if ch == "reel" else 1.15), (2 * half - 2 * gap) / 3); chh_ = 88 * u; top = y + 8 * u; xs = cx - (3 * cwid + 2 * gap) / 2
    L["chips"] = [(xs + (i % 3) * (cwid + gap), top + (i // 3) * (chh_ + 10 * u), cwid, chh_) for i in range(6)]; L["chip_fs"] = int(50 * u) // 2 * 2
    y = top + 2 * chh_ + 10 * u; leg_fs = int(36 * u) // 2 * 2; L["legend"] = (y + 26 * u, 46 * u, leg_fs); L["end"] = y + 26 * u + 92 * u; L["tok_c0"] = L["chips"][0][0] + cwid / 2; L["tok_c1"] = L["chips"][1][0] + cwid / 2
    return L
def t_explain(ch, state, texts=None):
    """state: 'same'(두 토큰이 같은 방향) | 'diff'(다른 방향). 정월 설명 장면의 한 컷."""
    p = Page(ch); L = explain_layout(ch) if texts is None else explain_layout(ch, texts); u = L["u"]; cx = L["cx"]; ax, ay, D = L["avatar"]; bl, bt, bw, bh = L["bubble"]
    if L["bubble_overflow"]: p.problems.append("말풍선 글자가 칸에 안 들어감")
    i = 1 if state == "same" else 2; lines = L["bubble_lines"][i]
    p.add("아바타", (ax, ay, ax + D, ay + D), f'<div style="position:absolute;left:{ax:.0f}px;top:{ay:.0f}px;width:{D:.0f}px;height:{D:.0f}px;border-radius:50%;overflow:hidden;border:{6 * u:.0f}px solid {GOLD};background:radial-gradient(circle at 50% 35%,#27346f,#0b1235);box-shadow:0 0 44px rgba(231,200,141,.35)"><img style="position:absolute;left:{-D * .158:.0f}px;top:{D * .03:.0f}px;width:{D * 1.333:.0f}px" src="file://{os.path.join(AS, "derived", "jw_gesture.png")}"></div>')
    hl = "방향" if False else None
    def mark(l): return l.replace("'같은\u00a0말'", f"<b style='color:{GOLD};font-family:{K.D}'>'같은&nbsp;말'</b>").replace("'다른\u00a0말'", f"<b style='color:{GOLD};font-family:{K.D}'>'다른&nbsp;말'</b>")
    txt = "<br>".join(mark(l) for l in lines); th = len(lines) * L["bubble_fs"] * 1.32; tw = max(font(K.P["pr_xb"], L["bubble_fs"]).getlength(l) for l in lines)
    p.add("말풍선", (bl, bt, bl + bw, bt + bh), f'<div style="position:absolute;left:{bl:.0f}px;top:{bt:.0f}px;width:{bw:.0f}px;height:{bh:.0f}px;box-sizing:border-box;background:linear-gradient(145deg,rgba(28,40,92,.95),rgba(9,14,44,.95));border:3px solid {GOLD};border-radius:{42 * u:.0f}px;box-shadow:0 0 46px rgba(231,200,141,.28)"></div>')
    p.add("말풍선 글", (bl + bw / 2 - tw / 2, bt + bh / 2 - th / 2, bl + bw / 2 + tw / 2, bt + bh / 2 + th / 2), f'<div style="position:absolute;left:{bl:.0f}px;top:{bt:.0f}px;width:{bw:.0f}px;height:{bh:.0f}px;display:flex;align-items:center;justify-content:center;text-align:center;font-family:{K.B};font-weight:800;font-size:{L["bubble_fs"]}px;line-height:1.32;color:#fff"><div style="text-align:center">{txt}</div></div>')
    bx, by, bhh = L["badge"]; bwid = font(K.P["gm_bold"], int(38 * u)).getlength("정월") + 56 * u
    p.add("정월 배지", (bx, by, bx + bwid, by + bhh), f'<div style="position:absolute;left:{bx:.0f}px;top:{by:.0f}px;width:{bwid:.0f}px;height:{bhh:.0f}px;border-radius:{bhh:.0f}px;background:{GOLD};color:#17102b;display:flex;align-items:center;justify-content:center;font-family:{K.D};font-weight:900;font-size:{int(38 * u)}px;line-height:1">정월</div>')
    p.add("꼬리", (bl - 30, bt + bh / 2 - 26, bl, bt + bh / 2 + 26), f'<div style="position:absolute;left:{bl - 30:.0f}px;top:{bt + bh / 2 - 26:.0f}px;width:0;height:0;border:26px solid transparent;border-right:34px solid {GOLD};border-left:0"></div><div style="position:absolute;left:{bl - 26:.0f}px;top:{bt + bh / 2 - 21:.0f}px;width:0;height:0;border:21px solid transparent;border-right:29px solid #151f55;border-left:0"></div>')
    btop, bfs = L["banner"]; bt_txt = "같은 말 = 타고난 결" if state == "same" else "다른 말 = 내가 고를 곳"; r = fit_line(bt_txt, p.title_path(), 2 * L["half"], bfs * 1.2, bfs, 40)
    p.add("배너", (cx - r["w"] / 2, btop, cx + r["w"] / 2, btop + r["h"]), f'<div style="position:absolute;left:0;top:{btop:.0f}px;width:{p.c["W"]}px;text-align:center;font-family:{K.D};font-weight:900;font-size:{r["size"]}px;line-height:1.1;color:{GOLD};white-space:nowrap">{bt_txt}</div>')
    ttop, td = L["tok"]; c0, c1 = L["tok_c0"], L["tok_c1"]; off = td * .28
    pk = c0 - td / 2 - off + (off if state == "diff" else 0); bk = (c0 - td / 2 + off) if state == "same" else (c1 - td / 2)
    p.add("토큰 묶음", (min(pk, bk), ttop, max(pk, bk) + td, ttop + td), f'<div style="position:absolute;left:0;top:0;width:{p.c["W"]}px;height:{p.c["H"]}px;isolation:isolate"><div style="position:absolute;left:{pk:.0f}px;top:{ttop:.0f}px;width:{td:.0f}px;height:{td:.0f}px;border-radius:50%;background:{PINK};mix-blend-mode:multiply"></div><div style="position:absolute;left:{bk:.0f}px;top:{ttop:.0f}px;width:{td:.0f}px;height:{td:.0f}px;border-radius:50%;background:{BLUE};mix-blend-mode:multiply"></div></div>')
    ltop, lfs = L["label"]; lr = fit_line("자오선이 나눈 여섯 방향", p.title_path(), 2 * L["half"], lfs * 1.2, lfs, 36)
    p.add("여섯 방향 제목", (cx - lr["w"] / 2, ltop, cx + lr["w"] / 2, ltop + lr["h"]), f'<div style="position:absolute;left:0;top:{ltop:.0f}px;width:{p.c["W"]}px;text-align:center;font-family:{K.D};font-weight:900;font-size:{lr["size"]}px;line-height:1.1;color:{GOLD};white-space:nowrap">자오선이 나눈 여섯 방향</div>')
    for k, (cxx, cyy, cww, chh_) in enumerate(L["chips"]):
        on = (state == "same" and k == 0) or (state == "diff" and k in (0, 1)); bgc = ("rgba(122,79,208,.75)" if state == "same" else ("rgba(255,92,157,.55)" if k == 0 else "rgba(69,96,240,.6)")) if on else "rgba(255,255,255,.1)"
        p.add(f"칩 {SIX[k]}", (cxx, cyy, cxx + cww, cyy + chh_), f'<div style="position:absolute;left:{cxx:.0f}px;top:{cyy:.0f}px;width:{cww:.0f}px;height:{chh_:.0f}px;box-sizing:border-box;border-radius:{26 * u:.0f}px;border:4px solid rgba(231,200,141,.65);background:{bgc};color:#fff;display:flex;align-items:center;justify-content:center;font-family:{K.D};font-weight:900;font-size:{L["chip_fs"]}px">{SIX[k]}</div>')
    gtop, gh, gfs = L["legend"]
    for j, (col, tx) in enumerate(((PINK, "사주가 짚은 방향"), (BLUE, "별자리가 짚은 방향"))):
        w = font(K.P["gm_bold"], gfs).getlength(tx) + gfs + 14; y0_ = gtop + j * gh
        p.add(f"설명글 {j + 1}", (cx - w / 2, y0_, cx + w / 2, y0_ + gh), f'<div style="position:absolute;left:0;top:{y0_:.0f}px;width:{p.c["W"]}px;text-align:center;font-family:{K.D};font-weight:900;font-size:{gfs}px;line-height:{gh:.0f}px;color:rgba(255,255,255,.88);white-space:nowrap"><span style="display:inline-block;width:{gfs * .8:.0f}px;height:{gfs * .8:.0f}px;border-radius:50%;background:{col};vertical-align:-2px;margin-right:14px"></span>{tx}</div>')
    p.ai = True; return p

def render_html(p):
    c = p.c; ai = getattr(p, 'ai', False)
    head = f'<!doctype html><meta charset=utf-8><style>{K.css("gm" if p.ch == "reel" else "pl")}{BF.css()}html,body{{margin:0;width:{c["W"]}px;height:{c["H"]}px;overflow:hidden;background:#050a1c;position:relative;word-break:keep-all;line-break:strict}}</style><body>'
    return head + bg_html(p.ch) + "".join(p.html) + BF.html(c["kind"], ai=ai, stacked=c["stacked"]) + "<script>document.title='ok'</script>"
async def render(pages):
    from playwright.async_api import async_playwright
    out = {}
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        for name, p in pages.items():
            c = p.c; pg = await b.new_page(viewport={"width": c["W"], "height": c["H"]}); open("/tmp/tpl.html", "w", encoding="utf-8").write(render_html(p)); await pg.goto("file:///tmp/tpl.html"); await pg.wait_for_function("document.title=='ok'"); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(300)
            path = os.path.join(R, "2026-motion", "tpl", name + ".png"); os.makedirs(os.path.dirname(path), exist_ok=True); await pg.screenshot(path=path); out[name] = path; await pg.close()
        await b.close()
    return out
RANK = [("염소", 23.0), ("황소", 22.7), ("처녀", 18.1), ("사자", 16.3), ("물병", 14.1), ("사수", 13.4), ("쌍둥이", 12.9), ("게", 12.6), ("양", 9.9), ("전갈", 7.3), ("물고기", 6.1), ("천칭", 5.6)]
if __name__ == "__main__":
    pages = {}
    for ch in ("reel", "carousel"):
        pages[f"{ch}_hook"] = t_hook(ch, "내 별자리,\n사주랑 같은 말\n할까?", "사주", "별자리", "같은 말")
        pages[f"{ch}_ranking"] = t_ranking(ch, "사주와 같은 말을 하는\n별자리 순위", RANK)
        pages[f"{ch}_cta"] = t_cta(ch, "팔로우하고", "더 많은 이야기 나눠요", "프로필 링크에서", ("생년월일 입력하고", "내 첫글자와 타고난 기운 알아보기"), "＋ 팔로우")
    for ch in ("reel", "carousel"):
        pages[f"{ch}_explain_same"] = t_explain(ch, "same"); pages[f"{ch}_explain_diff"] = t_explain(ch, "diff")
    bad = {k: p.problems for k, p in pages.items() if p.problems}
    for k, p in pages.items(): print(k, "요소", len(p.els), "문제", len(p.problems), p.problems[:3])
    json.dump({k: [(n, [round(v) for v in r]) for n, r in p.els] for k, p in pages.items()}, open("/tmp/tpl_rects.json", "w", encoding="utf-8"), ensure_ascii=False)
    if bad: print("검증 실패 — 만들지 않음"); sys.exit(1)
    outs = asyncio.run(render(pages)); print(list(outs))
    from PIL import ImageDraw
    import page_overlay as PO
    for name, path in outs.items():
        im = Image.open(path).convert("RGB")
        if name.startswith("reel"): PO.draw(im, "릴스 · " + name.split("_")[1], []).save(path.replace(".png", "_check.jpg"), quality=90)
        else:
            W, H = im.size; can = Image.new("RGB", (W, H + 300), (11, 16, 32)); can.paste(im, (0, 0)); ov = Image.new("RGBA", (W, H + 300), (0, 0, 0, 0)); d = ImageDraw.Draw(ov); TEAL = (127, 214, 200, 255)
            a, b, c, e = CHAN["carousel"]["safe"]
            for (x0, y0, x1, y1) in ((a, b, c, b), (c, b, c, e), (c, e, a, e), (a, e, a, b)):
                n = int(max(abs(x1 - x0), abs(y1 - y0)) // 24)
                for i in range(0, n, 2): d.line([(x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n), (x0 + (x1 - x0) * (i + 1) / n, y0 + (y1 - y0) * (i + 1) / n)], fill=TEAL, width=6)
            for y in range(100, H, 100): d.line([(0, y), (W, y)], fill=(255, 255, 255, 36), width=1); f = font(K.P["pr_xb"], 26); d.rectangle((2, y - 16, 56, y + 16), fill=(0, 0, 0, 150)); d.text((8, y - 14), str(y), font=f, fill=(255, 235, 120, 255))
            f34 = font(K.P["pr_xb"], 34); d.text((40, H + 24), "초록 점선 = 캐러셀(3:4) 안전 영역 x 55~1025 · y 55~1385", font=f34, fill=(255, 255, 255, 255)); d.text((40, H + 78), "프로필 격자도 3:4라 그림 전체가 그대로 보여요", font=f34, fill=(255, 255, 255, 255))
            d.text((40, H + 132), "자홍 상자(안전 영역을 넘는 요소) = 0개", font=f34, fill=(255, 120, 220, 255)); d.text((40, H + 200), "모든 요소의 좌표를 만들기 전에 계산해 검증해요", font=f34, fill=(231, 200, 141, 255))
            Image.alpha_composite(can.convert("RGBA"), ov).convert("RGB").save(path.replace(".png", "_check.jpg"), quality=90)
