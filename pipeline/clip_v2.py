"""네이버 클립 v2 (10/15 대표: 같은 틀 반복=양산형 저품질로 보일 수 있어 하루 1개로 합쳐 새로 만든다).
원칙
- 고정 첫 장면·고정 끝 장면을 쓰지 않는다. 첫 장면이 곧 그 글의 실제 내용(찾는 표·계산·연구·장면)이고 썸네일은 그 장면 그대로다.
- 클립마다 장면 모양(표·노트·고르기·그래프·연대표·말풍선·일정표·영수증·배터리·가면…)과 색이 다르다. 정월 얼굴을 쓰지 않는다(AI 표시 불필요).
- 설명 글은 클립마다 새로 쓴다. 고정 문장·고정 태그 자리 없음. 주소 없음(블로그 스티커가 연결).
- 규격: 1080x1920, 30fps, H.264, 소리 없음. 글자는 네이버 클립 화면이 가리지 않는 x 70~880, y 190~1440 안.
데이터: content/clips_v2.json  사용: python3 pipeline/clip_v2.py [id ...] (없으면 전부)  /  --audit (문구·반복 검사만)
결과: clips_v2/<id>.mp4, <id>_thumb.jpg, <id>_check.jpg(장면별 한 장씩), desc/<id>.txt"""
import os, sys, re, json, subprocess, tempfile, shutil
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, ".."))
SPEC = os.path.join(ROOT, "content", "clips_v2.json"); OUT = os.path.join(ROOT, "clips_v2")
W, H = 1080, 1920; L, R, T, B = 70, 880, 190, 1440; CX = (L + R) // 2
NOTO = {"black": ("/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc", 1), "bold": ("/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc", 1),
        "med": ("/usr/share/fonts/opentype/noto/NotoSansCJK-Medium.ttc", 1), "reg": ("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc", 1),
        "serif": ("/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc", 1)}
FD = os.path.join(HERE, "fonts")
LATIN = {"gmarket": os.path.join(FD, "GmarketSansBold.ttf"), "paper": os.path.join(FD, "Paperlogy-8ExtraBold.ttf"), "pre": os.path.join(FD, "PRETENDARD-BLACK.OTF"), "preb": os.path.join(FD, "PRETENDARD-BOLD.OTF")}
HANJA = re.compile(r"[㐀-鿿]")
_fc = {}
def font(kind, size, text=""):
    """제목 글꼴(kind)이 한자를 못 그리면 Noto CJK로 바꾼다."""
    if kind in LATIN and HANJA.search(text or ""): kind = "black"
    k = (kind, size)
    if k not in _fc:
        if kind in NOTO: p, i = NOTO[kind]; _fc[k] = ImageFont.truetype(p, size, index=i)
        else: _fc[k] = ImageFont.truetype(LATIN[kind], size)
    return _fc[k]
def hexc(s, a=None):
    s = s.lstrip("#"); c = tuple(int(s[i:i + 2], 16) for i in (0, 2, 4)); return c + ((a,) if a is not None else ())

class Pal:
    def __init__(self, p): self.__dict__.update({k: (hexc(v) if isinstance(v, str) and v.startswith("#") else v) for k, v in p.items()})

def canvas(P):
    im = Image.new("RGB", (W, H), P.bg1); d = ImageDraw.Draw(im)
    for y in range(H):   # 위→아래 두 색
        t = y / H; c = tuple(int(P.bg1[i] + (P.bg2[i] - P.bg1[i]) * t) for i in range(3)); d.line((0, y, W, y), fill=c)
    return im

def lines_of(text, fnt, maxw):
    """*강조* 유지, 사용자가 넣은 줄바꿈 우선, 넘치면 띄어쓰기에서 나눈다. [[(글자, 강조)], ...]"""
    out = []
    for para in text.split("\n"):
        chars, hl = [], False
        for ch in para:
            if ch == "*": hl = not hl; continue
            chars.append((ch, hl))
        words, cur = [], []
        for c in chars:
            if c[0] == " ":
                if cur: words.append(cur); cur = []
            else: cur.append(c)
        if cur: words.append(cur)
        line = []
        for wd in words:
            cand = line + ([(" ", False)] if line else []) + wd
            if line and fnt.getlength("".join(c[0] for c in cand)) > maxw: out.append(line); line = list(wd)
            else: line = cand
        out.append(line)
    return out
def text(d, s, x, y, size, color, kind="bold", align="center", maxw=None, lh=1.3, hl=None, P=None):
    """글을 그리고 아래 끝 y를 돌려준다. align center면 x는 가운데."""
    maxw = maxw or (R - L); f = font(kind, size, s); hl = hl or (P.acc if P else color); y0 = y
    ls = lines_of(s, f, maxw)
    for ln in ls:
        wt = f.getlength("".join(c[0] for c in ln)); xx = x - wt / 2 if align == "center" else x
        for ch, h in ln:
            d.text((xx, y), ch, font=f, fill=hl if h else color); xx += f.getlength(ch)
        y += int(size * lh)
    text.last_lines = len(ls); return y
def text_h(s, size, kind="bold", maxw=None, lh=1.3):
    return len(lines_of(s, font(kind, size, s), maxw or (R - L))) * int(size * lh)
def rrect(d, box, r, fill=None, outline=None, width=3): d.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=width)
def mark(d, P):   # 작은 이름표 한 곳(아래 왼쪽). 클립마다 같은 큰 틀이 아니라 작은 표시만 남긴다
    d.text((L, B - 34), "자오선 · " + P.tag, font=font("med", 28), fill=P.dim)
OFF = [0]   # 두 번 그리기: 첫 번째로 내용 높이를 재고, 두 번째에 안전영역 가운데로 내린다
def head(d, P, sc, y=None):
    y = (T + 30 if y is None else y) + OFF[0]
    if sc.get("kicker"):
        f = font("bold", 34, sc["kicker"]); w = f.getlength(sc["kicker"]) + 44
        rrect(d, (CX - w / 2, y, CX + w / 2, y + 58), 29, fill=P.chip); d.text((CX - (w - 44) / 2, y + 8), sc["kicker"], font=f, fill=P.chipfg); y += 90
    if sc.get("title"): y = text(d, sc["title"], CX, y, sc.get("tsize", 76), P.fg, P.tfont, P=P, lh=1.25) + 34
    return y

# ───── 장면 종류: 각 함수는 단계별 이미지 목록을 돌려준다(뒤 단계일수록 요소가 하나씩 더 보임) ─────
def s_table(P, sc):
    out = []; rows = sc["rows"]
    for k in range(len(rows) + 1):
        im = canvas(P); d = ImageDraw.Draw(im); y = head(d, P, sc); y += 10
        for i, r in enumerate(rows[:k]):
            rrect(d, (L, y, R, y + 150), 22, fill=P.card)
            d.text((L + 36, y + 50), r[0], font=font("bold", 42, r[0]), fill=P.cardfg)
            f = font("serif", 96); d.text((R - 210, y + 14), r[1], font=f, fill=P.acc)
            d.text((R - 92, y + 58), r[2], font=font("med", 34), fill=P.dim)
            y += 168
        if k == len(rows) and sc.get("foot"): text(d, sc["foot"], CX, y + 24, 40, P.fg2, "med", P=P)
        mark(d, P); out.append(im)
    return out
def s_statement(P, sc):
    out = []
    for k in (1, 2) if sc.get("small") else (1,):
        im = canvas(P); d = ImageDraw.Draw(im)
        if sc.get("kicker"): head(d, P, {"kicker": sc["kicker"]})
        big, sm = sc["big"], sc.get("small", "")
        hb = text_h(big, sc.get("bsize", 70), P.tfont); hs = text_h(sm, 44, "med") if sm else 0
        y = 820 - (hb + (60 + hs if sm else 0)) // 2
        y = text(d, big, CX, y, sc.get("bsize", 70), P.fg, P.tfont, P=P, lh=1.32)
        if k == 2:
            d.line((CX - 60, y + 28, CX + 60, y + 28), fill=P.acc, width=4); text(d, sm, CX, y + 60, 44, P.fg2, "med", P=P, lh=1.45)
        mark(d, P); out.append(im)
    return out
def s_list(P, sc):
    """번호·표시가 있는 줄 목록(해 볼 것, 세 풀이)."""
    out = []; it = sc["items"]
    for k in range(1, len(it) + 1):
        im = canvas(P); d = ImageDraw.Draw(im); y = head(d, P, sc) + 10
        for i, row in enumerate(it[:k]):
            lab, main = row[0], row[1]; sub = row[2] if len(row) > 2 else ""
            hh = 70 + text_h(main, 46, "bold", maxw=R - L - 200) + (text_h(sub, 36, "med", maxw=R - L - 200) + 6 if sub else 0)
            rrect(d, (L, y, R, y + hh), 24, fill=P.card)
            f = font("black", 40, lab); d.text((L + 30, y + 30), lab, font=f, fill=P.acc)
            yy = text(d, main, L + 170, y + 30, 46, P.cardfg, "bold", align="left", maxw=R - L - 200, P=P)
            if sub: text(d, sub, L + 170, yy + 4, 36, P.carddim, "med", align="left", maxw=R - L - 200, P=P)
            y += hh + 22
        mark(d, P); out.append(im)
    return out
def s_choice(P, sc):
    """셋 중 고르기: 세로 카드 세 장, 알파벳 표시."""
    out = []; cs = sc["cards"]
    for k in range(1, len(cs) + 1):
        im = canvas(P); d = ImageDraw.Draw(im); y = head(d, P, sc) + 6
        for i, c in enumerate(cs[:k]):
            hh = 64 + text_h(c[0], 50, P.tfont, maxw=R - L - 170) + text_h(c[1], 36, "med", maxw=R - L - 170)
            rrect(d, (L, y, R, y + hh), 30, outline=P.acc, width=4, fill=P.card)
            d.ellipse((L + 30, y + 30, L + 110, y + 110), fill=P.acc); f = font("black", 46); ch = "ABC"[i]
            d.text((L + 70 - f.getlength(ch) / 2, y + 38), ch, font=f, fill=P.bg1)
            yy = text(d, c[0], L + 140, y + 30, 50, P.cardfg, P.tfont, align="left", maxw=R - L - 170, P=P)
            text(d, c[1], L + 140, yy + 2, 36, P.carddim, "med", align="left", maxw=R - L - 170, P=P)
            y += hh + 26
        if k == len(cs) and sc.get("foot"): text(d, sc["foot"], CX, y + 14, 42, P.fg2, "med", P=P)
        mark(d, P); out.append(im)
    return out
def s_notebook(P, sc):
    """줄 노트에 걱정을 적고, 하나에만 동그라미."""
    out = []; it = sc["items"]
    for k in range(1, len(it) + 2):
        im = canvas(P); d = ImageDraw.Draw(im); y = head(d, P, sc)
        x0, x1, y0 = L + 10, R - 10, y + 10; y1 = y0 + 120 * len(it) + 80
        d.rectangle((x0, y0, x1, y1), fill=P.card); d.line((x0 + 90, y0, x0 + 90, y1), fill=(220, 120, 120), width=3)
        for j in range(len(it) + 1): d.line((x0, y0 + 60 + j * 120, x1, y0 + 60 + j * 120), fill=(190, 205, 230), width=2)
        for j, s in enumerate(it[:min(k, len(it))]):
            d.text((x0 + 120, y0 + 60 + j * 120 - 62), s, font=font("med", 46, s), fill=P.cardfg)
        if k == len(it) + 1:
            j = sc["circle"]; f = font("med", 46, it[j]); w = f.getlength(it[j])
            d.ellipse((x0 + 96, y0 + 60 + j * 120 - 84, x0 + 144 + w, y0 + 60 + j * 120 + 6), outline=P.acc, width=6)
            text(d, sc["foot"], CX, y1 + 50, 44, P.fg, "bold", P=P)
        mark(d, P); out.append(im)
    return out
def s_quote(P, sc):
    """연구 한 줄: 개념 이름(크게) + 누가·언제 + 풀이."""
    out = []
    for k in (1, 2):
        im = canvas(P); d = ImageDraw.Draw(im); y = head(d, P, {"kicker": sc.get("kicker")})
        y = 560 + OFF[0]
        d.text((L, y - 120), "“", font=font("serif", 200), fill=P.acc)
        y = text(d, sc["concept"], L + 20, y + 40, 84, P.fg, P.tfont, align="left", P=P)
        y = text(d, sc["who"], L + 20, y + 10, 38, P.dim, "med", align="left", P=P)
        if k == 2:
            d.line((L + 20, y + 30, L + 220, y + 30), fill=P.acc, width=5)
            text(d, sc["body"], L + 20, y + 70, 48, P.fg2, "bold", align="left", maxw=R - L - 40, P=P, lh=1.45)
        mark(d, P); out.append(im)
    return out
def s_three(P, sc):
    """세 풀이 한 장: 동양·서양·숫자(또는 두 풀이) 칸."""
    out = []; it = sc["items"]
    for k in range(1, len(it) + 1):
        im = canvas(P); d = ImageDraw.Draw(im); y = head(d, P, sc) + 10
        cw = (R - L - 20 * (len(it) - 1)) / len(it)
        for i, (lab, main, sub) in enumerate(it[:k]):
            x = L + i * (cw + 20); rrect(d, (x, y, x + cw, y + 520), 26, fill=P.card)
            text(d, lab, x + cw / 2, y + 34, 34, P.acc, "bold", maxw=cw - 30, P=P)
            yy = text(d, main, x + cw / 2, y + 120, 54, P.cardfg, "black", maxw=cw - 30, P=P, lh=1.2)
            text(d, sub, x + cw / 2, yy + 20, 32, P.carddim, "med", maxw=cw - 40, P=P, lh=1.4)
        if k == len(it) and sc.get("foot"): text(d, sc["foot"], CX, y + 580, 42, P.fg, "bold", P=P)
        mark(d, P); out.append(im)
    return out
def s_progress(P, sc):
    """시작→끝 선 위에 힘이 빠지는 구간 세 곳."""
    out = []; pts = sc["points"]
    for k in range(0, len(pts) + 1):
        im = canvas(P); d = ImageDraw.Draw(im); y = head(d, P, sc)
        gy = y + 330; d.line((L + 20, gy, R - 20, gy), fill=P.dim, width=6)
        d.text((L + 10, gy + 24), "시작", font=font("bold", 36), fill=P.fg2); d.text((R - 70, gy + 24), "끝", font=font("bold", 36), fill=P.fg2)
        import math
        prev = None
        for i in range(0, 101):   # 힘 곡선: 처음 높고 가운데 꺼짐, 끝에서 다시 흔들림
            t = i / 100; v = 0.85 - 0.55 * math.sin(math.pi * t) * 0.9 + 0.12 * math.sin(6 * t)
            p = (L + 20 + t * (R - L - 40), gy - 40 - v * 230)
            if prev: d.line((prev, p), fill=P.acc, width=7)
            prev = p
        for i, (x, lab, tip) in enumerate(pts[:k]):
            px = L + 20 + x * (R - L - 40); d.ellipse((px - 18, gy - 18, px + 18, gy + 18), fill=P.acc)
            text(d, lab, px, gy + 80, 40, P.fg, "black", maxw=300, P=P)
            text(d, tip, px, gy + 140, 32, P.fg2, "med", maxw=250, P=P, lh=1.35)
        if k == len(pts) and sc.get("foot"): text(d, sc["foot"], CX, gy + 420, 48, P.fg, P.tfont, P=P)
        mark(d, P); out.append(im)
    return out
def s_boxes(P, sc):
    """네 칸(당사주): 2x2."""
    im = canvas(P); d = ImageDraw.Draw(im); y = head(d, P, sc) + 10; bw = (R - L - 30) / 2
    for i, (lab, sub) in enumerate(sc["boxes"]):
        x = L + (i % 2) * (bw + 30); yy = y + (i // 2) * 250
        rrect(d, (x, yy, x + bw, yy + 220), 24, fill=P.card if i != sc.get("hi", -1) else P.acc)
        text(d, lab, x + bw / 2, yy + 46, 60, P.cardfg if i != sc.get("hi", -1) else P.bg1, "black", maxw=bw - 20, P=P)
        text(d, sub, x + bw / 2, yy + 136, 34, P.carddim if i != sc.get("hi", -1) else P.bg1, "med", maxw=bw - 20, P=P)
    if sc.get("foot"): text(d, sc["foot"], CX, y + 540, 42, P.fg, "bold", P=P, lh=1.4)
    mark(d, P); return [im]
def s_timeline(P, sc):
    out = []; ev = sc["events"]
    for k in range(1, len(ev) + 1):
        im = canvas(P); d = ImageDraw.Draw(im); y = head(d, P, sc) + 20; x = L + 70
        d.line((x, y, x, y + 200 * len(ev) - 80), fill=P.dim, width=5)
        for i, (date, name, sub, hi) in enumerate(ev[:k]):
            yy = y + i * 200; r = 30 if hi else 20
            d.ellipse((x - r, yy - r + 30, x + r, yy + r + 30), fill=P.acc if hi else P.fg2)
            d.text((x + 60, yy), date, font=font("bold", 36), fill=P.dim)
            d.text((x + 230, yy - 12), name, font=font("black", 60 if hi else 52, name), fill=P.acc if hi else P.fg)
            text(d, sub, x + 230, yy + 66, 34, P.fg2, "med", align="left", maxw=R - x - 240, P=P)
        mark(d, P); out.append(im)
    return out
def s_phone(P, sc):
    out = []
    for k in (1, 2):
        im = canvas(P); d = ImageDraw.Draw(im); y = head(d, P, sc)
        px0, px1 = L + 90, R - 90; rrect(d, (px0, y, px1, y + 620), 50, fill=P.card, outline=P.dim, width=4)
        rrect(d, (px0 + 60, y + 110, px1 - 140, y + 230), 36, fill=P.chip)
        text(d, sc["msg"], px0 + 100, y + 140, 42, P.chipfg, "med", align="left", maxw=px1 - px0 - 240, P=P)
        d.text((px1 - 260, y + 250), sc["read"], font=font("med", 32), fill=P.carddim)
        for i in range(3): d.ellipse((px0 + 80 + i * 44, y + 360, px0 + 108 + i * 44, y + 388), fill=P.dim)
        if k == 2: text(d, sc["foot"], CX, y + 680, 46, P.fg, "bold", P=P, lh=1.4)
        mark(d, P); out.append(im)
    return out
def s_chat(P, sc):
    out = []; msgs = sc["msgs"]
    for k in range(1, len(msgs) + 1):
        im = canvas(P); d = ImageDraw.Draw(im); y = head(d, P, sc) + 20
        for who, s in msgs[:k]:
            f = font("med", 44, s); w = min(f.getlength(s) + 70, R - L - 120)
            hh = text_h(s, 44, "med", maxw=w - 70) + 50
            if who == "me": x0 = R - w; rrect(d, (x0, y, R, y + hh), 34, fill=P.acc); text(d, s, x0 + 35, y + 22, 44, P.bg1, "med", align="left", maxw=w - 70, P=P)
            elif who == "think": text(d, s, R - 10 - font("med", 38, s).getlength(s), y + 10, 38, P.dim, "med", align="left", P=P); hh = 70
            else: rrect(d, (L, y, L + w, y + hh), 34, fill=P.card); text(d, s, L + 35, y + 22, 44, P.cardfg, "med", align="left", maxw=w - 70, P=P)
            y += hh + 30
        mark(d, P); out.append(im)
    return out
def s_schedule(P, sc):
    out = []; bl = sc["blocks"]; nhi = sum(1 for b in bl if b[2])
    for k in (0, 1):
        im = canvas(P); d = ImageDraw.Draw(im); y = head(d, P, sc) + 6
        for tm, s, hi in bl:
            if hi and not k: continue
            hh = 110 if not hi else 96
            rrect(d, (L + 150, y, R, y + hh), 20, fill=P.acc if hi else P.card)
            d.text((L, y + 34), tm, font=font("bold", 36), fill=P.dim)
            d.text((L + 190, y + (28 if not hi else 22)), s, font=font("bold", 44, s), fill=P.bg1 if hi else P.cardfg)
            y += hh + 18
        if k: text(d, sc["foot"], CX, y + 30, 44, P.fg, "bold", P=P)
        mark(d, P); out.append(im)
    return out
def s_receipt(P, sc):
    out = []; rows = sc["rows"]
    for k in range(1, len(rows) + 2):
        im = canvas(P); d = ImageDraw.Draw(im); y = head(d, P, sc)
        x0, x1 = L + 50, R - 50; y1 = y + 170 + 110 * len(rows) + 260
        d.rectangle((x0, y, x1, y1), fill=P.card)
        for i in range(0, int(x1 - x0), 30): d.polygon([(x0 + i, y1), (x0 + i + 15, y1 + 18), (x0 + i + 30, y1)], fill=P.card)
        d.text((x0 + 40, y + 40), sc["head"], font=font("bold", 40, sc["head"]), fill=P.cardfg)
        d.line((x0 + 30, y + 120, x1 - 30, y + 120), fill=P.carddim, width=2)
        for i, (a, b) in enumerate(rows[:min(k, len(rows))]):
            yy = y + 150 + i * 110; d.text((x0 + 40, yy), a, font=font("med", 40, a), fill=P.cardfg)
            fb = font("black", 44, b); d.text((x1 - 40 - fb.getlength(b), yy - 2), b, font=fb, fill=P.acc)
        if k == len(rows) + 1:
            yy = y + 160 + len(rows) * 110; d.line((x0 + 30, yy, x1 - 30, yy), fill=P.carddim, width=2)
            text(d, sc["total"], CX, yy + 40, 46, P.cardfg, "black", maxw=x1 - x0 - 80, P=P)
        mark(d, P); out.append(im)
    return out
def s_battery(P, sc):
    out = []; bs = sc["bats"]
    for k in range(1, len(bs) + 1):
        im = canvas(P); d = ImageDraw.Draw(im); y = head(d, P, sc) + 30; cw = (R - L - 60) / 3
        for i, (el, lvl, s) in enumerate(bs[:k]):
            x = L + i * (cw + 30); bx0, bx1 = x + 40, x + cw - 40
            rrect(d, (bx0 + 50, y, bx1 - 50, y + 30), 8, fill=P.dim); rrect(d, (bx0, y + 26, bx1, y + 470), 30, outline=P.fg, width=8)
            fh = int(424 * lvl); d.rounded_rectangle((bx0 + 20, y + 450 - fh, bx1 - 20, y + 450), radius=16, fill=P.acc if lvl > .2 else (220, 90, 80))
            text(d, el, x + cw / 2, y + 510, 56, P.fg, "black", maxw=cw, P=P)
            text(d, s, x + cw / 2, y + 590, 36, P.fg2, "med", maxw=cw - 10, P=P)
        if k == len(bs) and sc.get("foot"): text(d, sc["foot"], CX, y + 720, 44, P.fg, "bold", P=P)
        mark(d, P); out.append(im)
    return out
def s_jars(P, sc):
    out = []
    for k in (1, 2, 3):
        im = canvas(P); d = ImageDraw.Draw(im); y = head(d, P, sc) + 10
        for gi, (n, lab) in enumerate(sc["groups"]):
            if k < gi + 1: continue
            gy = y + gi * 300; d.text((L, gy), lab, font=font("black", 46, lab), fill=P.fg)
            cols = 12 if n > 6 else 6; sz = 52 if n > 6 else 96
            for j in range(n):
                cx = L + 20 + (j % cols) * (sz + (14 if n > 6 else 34)); cy = gy + 80 + (j // cols) * (sz + 20)
                rrect(d, (cx, cy + sz * .18, cx + sz, cy + sz), int(sz * .2), fill=P.jar[j % len(P.jar)])
                d.rectangle((cx + sz * .15, cy, cx + sz * .85, cy + sz * .2), fill=P.dim)
        if k == 3: yy = text(d, sc["foot"], CX, y + 560, 46, P.fg, "bold", P=P, lh=1.4); text(d, sc["src"], CX, yy + 16, 32, P.dim, "med", P=P)
        mark(d, P); out.append(im)
    return out
def s_rewrite(P, sc):
    out = []
    for k in (1, 2):
        im = canvas(P); d = ImageDraw.Draw(im); y = head(d, P, sc) + 40
        rrect(d, (L, y, R, y + 200), 26, fill=P.card); f = font("bold", 56, sc["before"]); w = f.getlength(sc["before"])
        d.text((CX - w / 2, y + 66), sc["before"], font=f, fill=P.carddim)
        if k == 2:
            d.line((CX - w / 2 - 10, y + 100, CX + w / 2 + 10, y + 100), fill=(220, 90, 80), width=7)
            d.polygon([(CX - 30, y + 240), (CX + 30, y + 240), (CX, y + 290)], fill=P.acc)
            rrect(d, (L, y + 320, R, y + 600), 26, outline=P.acc, width=5, fill=P.card)
            text(d, sc["after"], CX, y + 380, 56, P.cardfg, "black", P=P)
            text(d, sc["foot"], CX, y + 680, 42, P.fg2, "med", P=P, lh=1.4)
        mark(d, P); out.append(im)
    return out
def s_masks(P, sc):
    out = []; ms = sc["masks"]
    for k in range(1, len(ms) + 1):
        im = canvas(P); d = ImageDraw.Draw(im); y = head(d, P, sc) + 20
        for i, (name, sub) in enumerate(ms[:k]):
            yy = y + i * 300; mx = L + 20
            d.ellipse((mx, yy, mx + 200, yy + 240), fill=P.card)
            for ex in (mx + 45, mx + 115): d.ellipse((ex, yy + 80, ex + 42, yy + 112), fill=P.bg1)
            arc = [(mx + 50, yy + 140, mx + 150, yy + 200, 20, 160), (mx + 60, yy + 165, mx + 140, yy + 170, 0, 0), (mx + 50, yy + 150, mx + 150, yy + 210, 200, 340)][i % 3]
            if arc[4] == arc[5]: d.line((arc[0], arc[1], arc[2], arc[3]), fill=P.bg1, width=8)
            else: d.arc(arc[:4], arc[4], arc[5], fill=P.bg1, width=8)
            yy2 = text(d, name, mx + 250, yy + 50, 50, P.fg, "black", align="left", maxw=R - mx - 260, P=P)
            text(d, sub, mx + 250, yy2 + 6, 36, P.fg2, "med", align="left", maxw=R - mx - 260, P=P)
        mark(d, P); out.append(im)
    return out
def s_roles(P, sc):
    out = []; rs = sc["roles"]
    for k in range(1, len(rs) + 1):
        im = canvas(P); d = ImageDraw.Draw(im); y = head(d, P, sc) + 20; cw = (R - L - 40) / 3
        for i, (el, han, role, tip) in enumerate(rs[:k]):
            x = L + i * (cw + 20); col = hexc(P.elc[i])
            d.ellipse((x + cw / 2 - 110, y, x + cw / 2 + 110, y + 220), fill=col)
            f = font("serif", 110); d.text((x + cw / 2 - f.getlength(han) / 2, y + 30), han, font=f, fill=(255, 255, 255))
            text(d, el, x + cw / 2, y + 250, 44, P.fg, "black", maxw=cw, P=P)
            text(d, role, x + cw / 2, y + 320, 40, P.acc, "bold", maxw=cw, P=P)
            text(d, tip, x + cw / 2, y + 400, 34, P.fg2, "med", maxw=cw - 10, P=P, lh=1.4)
        if k == len(rs) and sc.get("foot"): text(d, sc["foot"], CX, y + 660, 44, P.fg, "bold", P=P)
        mark(d, P); out.append(im)
    return out
KIND = {"table": s_table, "statement": s_statement, "list": s_list, "choice": s_choice, "notebook": s_notebook, "quote": s_quote, "three": s_three,
        "progress": s_progress, "boxes": s_boxes, "timeline": s_timeline, "phone": s_phone, "chat": s_chat, "schedule": s_schedule,
        "receipt": s_receipt, "battery": s_battery, "jars": s_jars, "rewrite": s_rewrite, "masks": s_masks, "roles": s_roles}

def run(cmd): subprocess.run(cmd, check=True)
ENC = ["-c:v", "libx264", "-crf", "20", "-preset", "medium", "-pix_fmt", "yuv420p", "-r", "30", "-an"]
def render(c):
    P = Pal(c["pal"]); tmp = tempfile.mkdtemp(); segs = []; firsts = []; finals = []
    for si, sc in enumerate(c["scenes"]):
        OFF[0] = 0; steps = KIND[sc["kind"]](P, sc)
        if sc["kind"] != "statement":
            import numpy as np
            a = np.asarray(steps[-1].convert("L"), dtype=int); b = np.asarray(canvas(P).convert("L"), dtype=int)
            rows = np.where(np.abs(a - b)[:B - 50].max(axis=1) > 24)[0]
            if len(rows):
                top, bot = rows.min(), rows.max(); dy = int(((T + 10) + (B - 60)) / 2 - (top + bot) / 2)
                dy = max(0, min(dy, (B - 60) - bot))
                if dy > 20: OFF[0] = dy; steps = KIND[sc["kind"]](P, sc); OFF[0] = 0
        hold = sc.get("hold", 2.6); step = sc.get("step", 0.9)
        for j, im in enumerate(steps):
            p = os.path.join(tmp, f"s{si}_{j}.png"); im.save(p); dur = hold if j == len(steps) - 1 else step
            fi = 0.25 if j == 0 else 0.12
            o = os.path.join(tmp, f"s{si}_{j}.mp4"); segs.append(o)
            run(["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-framerate", "30", "-t", f"{dur}", "-i", p, "-vf", f"fade=t=in:st=0:d={fi},format=yuv420p"] + ENC + [o])
        finals.append(steps[-1])
    lst = os.path.join(tmp, "l.txt"); open(lst, "w").write("".join(f"file '{s}'\n" for s in segs))
    os.makedirs(os.path.join(OUT, "desc"), exist_ok=True); outp = os.path.join(OUT, c["id"] + ".mp4")
    run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", "-movflags", "+faststart", outp])
    finals[0].convert("RGB").save(os.path.join(OUT, c["id"] + "_thumb.jpg"), quality=90)   # 썸네일 = 첫 장면 완성본(영상 속 실제 화면)
    sh = Image.new("RGB", (270 * len(finals), 480))
    for i, im in enumerate(finals):
        t = im.resize((270, 480)); dd = ImageDraw.Draw(t); dd.rectangle((L / 4, T / 4, R / 4, B / 4), outline=(255, 60, 60)); sh.paste(t, (270 * i, 0))
    sh.save(os.path.join(OUT, c["id"] + "_check.jpg"), quality=88)
    open(os.path.join(OUT, "desc", c["id"] + ".txt"), "w", encoding="utf-8").write(c["desc"] + "\n\n" + " ".join("#" + t for t in c["tags"]) + "\n")
    shutil.rmtree(tmp)
    j = json.loads(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,width,height:format=duration", "-of", "json", outp]))
    return float(j["format"]["duration"]), [s for s in j["streams"] if s["codec_type"] == "audio"]

def render_reel(c):
    """릴스 본문만(끝의 팔로우·프로필 장면은 자르고 masks로 인스타 전용 글을 가림). 첫·끝 고정 장면 없음. 썸네일 = 본문 속 thumb_at 초 화면."""
    sys.path.insert(0, HERE); import clip_from_reel as CF
    sp = json.load(open(os.path.join(ROOT, "content", "clips_from_reels.json"), encoding="utf-8")); src = next(x for x in sp["clips"] if x["id"] == c["from"])
    tmp = tempfile.mkdtemp(); os.makedirs(os.path.join(OUT, "desc"), exist_ok=True); outp = os.path.join(OUT, c["id"] + ".mp4")
    b = os.path.join(tmp, "b.mp4"); CF.body_seg(src, sp, b, tmp)
    # 인스타 릴스 화면을 80%로 줄여 네이버 클립 버튼·글이 가리지 않는 자리(x 70~880, y 190~1440)에 둔다. 빈 곳은 같은 영상을 흐리게 깐다
    fc = "[0:v]split[a][b];[a]scale=1080:1920,boxblur=30:2,eq=brightness=-0.18[bg];[b]scale=864:1536[fg];[bg][fg]overlay=40:150,format=yuv420p"
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", b, "-filter_complex", fc] + ENC + ["-movflags", "+faststart", outp])
    th = os.path.join(OUT, c["id"] + "_thumb.jpg"); run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(c["thumb_at"]), "-i", outp, "-frames:v", "1", "-q:v", "3", th])
    j = json.loads(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type:format=duration", "-of", "json", outp])); dur = float(j["format"]["duration"])
    sh = Image.new("RGB", (270 * 5, 480))
    for i, t in enumerate([0.3, dur * .25, dur * .5, dur * .75, dur - 0.3]):
        p = os.path.join(tmp, f"f{i}.png"); run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{t:.2f}", "-i", outp, "-frames:v", "1", "-vf", "scale=270:480", p])
        im = Image.open(p).convert("RGB"); ImageDraw.Draw(im).rectangle((L / 4, T / 4, R / 4, B / 4), outline=(255, 60, 60)); sh.paste(im, (270 * i, 0))
    sh.save(os.path.join(OUT, c["id"] + "_check.jpg"), quality=88)
    open(os.path.join(OUT, "desc", c["id"] + ".txt"), "w", encoding="utf-8").write(c["desc"] + "\n\n" + " ".join("#" + t for t in c["tags"]) + "\n")
    shutil.rmtree(tmp); return dur, [s for s in j["streams"] if s["codec_type"] == "audio"]

FORBID = ["상" + "담", "치료", "적중", "반드시", "무조건", "결이", "타고난 결", "겹으로", "zaoseon.com", "http"]
def norm(s): return re.sub(r"[\s\W]+", "", s)
def audit(sp):
    """문구 검사 + 같은 틀 반복 검사(클립끼리 비교). 빈 목록이면 통과."""
    sys.path.insert(0, HERE); import natural_audit as N
    bad = []; cl = sp["clips"]
    for c in cl:
        dsc = c["desc"]
        if len(dsc) > 300: bad.append((c["id"], f"설명 {len(dsc)}자 > 300"))
        if not 3 <= len(c["tags"]) <= 5 or len(set(c["tags"])) != len(c["tags"]): bad.append((c["id"], "태그 3~5개, 겹침 없이"))
        for w in FORBID:
            if w in dsc or any(w in json.dumps(s, ensure_ascii=False) for s in c.get("scenes", [])): bad.append((c["id"], f"금지 표현 '{w}'"))
        if not re.search(r"마음|관계", dsc): bad.append((c["id"], "마음·관계 한 줄 없음(브랜드 규칙)"))
        for ln in dsc.split("\n"):
            if len(ln) > 120: bad.append((c["id"], f"설명 한 줄이 너무 김({len(ln)}자)"))
        texts = [(c["id"] + ":desc", dsc)] + [(c["id"] + f":s{i}", re.sub(r"\*", "", json.dumps(s, ensure_ascii=False))) for i, s in enumerate(c.get("scenes", []))]
        for h in N.scan(texts[:1]): bad.append((c["id"], f"natural_audit {h[0]} | {h[2]}"))
    # 같은 틀 반복: 설명 첫 문장·끝 문장, 태그 묶음, 첫 장면 종류, 바로 옆 날 색
    def first(c): return norm(c["desc"].split("\n")[0])[:18]
    def last(c): return norm([l for l in c["desc"].split("\n") if l.strip()][-1])[:18]
    for f, name in ((first, "설명 첫 줄"), (last, "설명 끝 줄")):
        seen = {}
        for c in cl:
            k = f(c)
            if k in seen: bad.append((c["id"], f"{name}이 {seen[k]}와 같음"))
            seen.setdefault(k, c["id"])
    lines = {}
    for c in cl:
        for ln in set(l.strip() for l in c["desc"].split("\n") if len(l.strip()) > 12):
            lines.setdefault(norm(ln), []).append(c["id"])
    for k, ids in lines.items():
        if len(ids) > 1: bad.append((ids[1], f"같은 문장이 {len(ids)}개 클립에: {ids}"))
    tg = {}
    for c in cl: tg.setdefault(tuple(sorted(c["tags"])), []).append(c["id"])
    for k, ids in tg.items():
        if len(ids) > 1: bad.append((ids[1], f"태그 묶음이 같음: {ids}"))
    pos = {}
    for c in cl:
        for i, t in enumerate(c["tags"]): pos.setdefault((i, t), []).append(c["id"])
    for (i, t), ids in pos.items():
        if len(ids) > len(cl) // 2: bad.append(("-", f"태그 '{t}'가 {i + 1}번째 자리에 {len(ids)}/{len(cl)}개(고정 자리)"))
    ks = [(c["scenes"][0]["kind"] if c.get("scenes") else "reel") for c in sorted(cl, key=lambda c: c["upload"])]
    for a, b, c in zip(ks, ks[1:], sorted(cl, key=lambda c: c["upload"])[1:]):
        if a == b: bad.append((c["id"], f"바로 앞 날과 첫 장면 모양이 같음({a})"))
    from collections import Counter
    for k, n in Counter(ks).items():
        if n > 2: bad.append(("-", f"첫 장면 모양 '{k}'가 {n}번(2번까지)"))
    ups = [c["upload"] for c in cl]
    if len(set(ups)) != len(ups): bad.append(("-", "올리는 날 중복(하루 1개)"))
    return bad
def thumb_sim(ids):
    """썸네일끼리 작게 줄인 흑백 차이(0~255). 낮을수록 비슷함."""
    import numpy as np
    ims = {i: np.asarray(Image.open(os.path.join(OUT, i + "_thumb.jpg")).convert("L").resize((27, 48)), dtype=float) for i in ids if os.path.exists(os.path.join(OUT, i + "_thumb.jpg"))}
    ks = list(ims); res = []
    for a in range(len(ks)):
        for b in range(a + 1, len(ks)): res.append((abs(ims[ks[a]] - ims[ks[b]]).mean(), ks[a], ks[b]))
    return sorted(res)[:5]
def main(a):
    sp = json.load(open(SPEC, encoding="utf-8")); bad = audit(sp)
    if bad: print("검사 걸림", len(bad)); [print("  ", b) for b in bad]
    if "--audit" in a: sys.exit(1 if bad else 0)
    if bad: sys.exit(1)
    ids = [x for x in a if not x.startswith("--")] or [c["id"] for c in sp["clips"]]
    for c in sp["clips"]:
        if c["id"] in ids:
            d, au = (render_reel(c) if c.get("kind") == "reel" else render(c)); print(f"{c['id']}: {d:.1f}초", "소리 있음!" if au else "OK")
    print("썸네일 가장 비슷한 짝(값이 작을수록 비슷):", [(round(s, 1), x, y) for s, x, y in thumb_sim([c["id"] for c in sp["clips"]])])
if __name__ == "__main__": main(sys.argv[1:])
