"""네이버 본문 서식 변환 (10/4 대표 요청): 원고 본문을 네이버에 붙였을 때 바로 이 모양이 되게 한다.
 - 전체 가운데 정렬, 본문 16px, 소제목 19px(굵게)
 - 한 문장을 짧은 줄로 끊는다(폰에서도 한 줄이 한글 약 22자를 넘지 않게). 끊는 자리는 쉼표·연결 어미·주어 다음을 먼저 고른다
 - 글자 내용은 바꾸지 않는다(띄어쓰기와 줄바꿈만). test_format_body.py가 글자 보존을 확인한다
복사해 붙일 때 네이버가 글자 크기·정렬을 그대로 받는지는 네이버 쪽 동작이라, 처음 한 편으로 확인한다."""
import html as H, re

BODY_PX, TITLE_PX = 16, 19
BODY_LIMIT, TITLE_LIMIT = 22.0, 16.5          # 한 줄 최대 너비(한글 1자 = 1.0). 폰 네이버 앱은 16px 기준 약 20~22자

def cw(c):
    o = ord(c)
    if c in "\ufe0f\u200d": return 0
    if c == " ": return .32
    if c in ".,;:!?": return .34
    if c in "·()[]'\"“”‘’": return .4
    if c in "/~-+=": return .5
    if c.isdigit(): return .58
    if c.isascii() and c.isalpha(): return .62
    if 0x1F000 <= o <= 0x1FAFF or 0x2600 <= o <= 0x27BF or 0x2B00 <= o <= 0x2BFF: return 1.2
    return 1.0
def width(plain): return sum(cw(c) for c in plain)

TAG = re.compile(r"(<[^>]+>)")
def plain_of(h): return H.unescape(TAG.sub("", h))

def tokenize(inner):
    toks = []; cur = ""; bold = False; bs = False
    def flush():
        nonlocal cur
        if cur:
            toks.append({"h": cur, "p": plain_of(cur), "bs": bs, "be": bold}); cur = ""
    for part in TAG.split(inner):
        if not part: continue
        if part.startswith("<"):
            if not cur: bs = bold
            low = part.lower()
            if low == "<b>": bold = True
            elif low == "</b>": bold = False
            cur += part; continue
        for ch in part:
            if ch == " ": flush()
            else:
                if not cur: bs = bold
                cur += ch
    flush(); return toks

ADNOM = r"(하는|되는|있는|없는|같은|좋은|쉬운|어려운|많은|높은|낮은|깊은|가까운|다른|큰|작은|아픈|힘든|먼|젊은|바쁜|이런|그런)$"
def bpen(tok, k=0):                              # 이 낱말(k번째) 뒤에서 끊을 때 얼마나 어색한가(작을수록 좋음)
    q = tok["p"].rstrip()
    if q.endswith((",", "，")): return 0
    q = q.rstrip(".!?)")
    if re.search(r"(은|는)$", q) and len(q) >= 2 and k <= 3 and not re.search(ADNOM, q): return .5      # 주어·화제 뒤
    if re.search(r"(면서|으면|이면|라면|다면|는데|한데|지만|라서|니까|해서|어서|아서|서도|이며|으며|으니|하며|함께|만큼|동안|마다|무렵|뒤에)$", q) or (re.search(r"(면|고|며)$", q) and len(q) >= 3): return 1.5
    if re.search(r"(이|가|도|만|께서)$", q) and len(q) >= 3: return 3
    if re.search(r"(와|과|에서|에게|에는|보다|처럼|까지|부터|으로|에|를|을)$", q): return 5
    return 9

def _inside(toks):                               # k번째 낱말 뒤가 괄호 안이면 True(괄호 안에서는 끊지 않는다)
    out = []; d = 0
    for t in toks:
        d += t["p"].count("(") - t["p"].count(")"); out.append(d > 0)
    return out

def _dp(toks, i0, j0, limit):
    """toks[i0..j0]를 limit 안의 줄로 나눈다(줄 너비가 고르고 끊는 자리가 자연스럽게)."""
    n = j0 - i0 + 1; ws = [width(t["p"]) for t in toks[i0:j0 + 1]]; ins = _inside(toks)
    def W(i, j): return sum(ws[i:j + 1]) + .32 * (j - i)
    if W(0, n - 1) <= limit: return [(i0, j0)]
    INF = 1e9; best = [INF] * (n + 1); back = [0] * (n + 1); best[0] = 0; ideal = limit - 4
    for j in range(1, n + 1):
        for i in range(j - 1, -1, -1):
            w = W(i, j - 1)
            if w > limit and i != j - 1: break
            last = j == n
            c = 6 + (0 if last else 3 * bpen(toks[i0 + j - 1], i0 + j - 1) + (300 if ins[i0 + j - 1] else 0)) + ((0.12 * (ideal - w) ** 2) if not last else (0.12 * max(0, 9 - w) ** 2 + (15 if w < 5 else 0)))
            if w > limit: c += 50
            if best[i] + c < best[j]: best[j] = best[i] + c; back[j] = i
    out = []; j = n
    while j > 0: i = back[j]; out.append((i0 + i, i0 + j - 1)); j = i
    return out[::-1]

def wrap(inner, limit, slack=0.0):
    toks = tokenize(inner); n = len(toks)
    if n == 0: return [inner]
    ws = [width(t["p"]) for t in toks]
    def W(i, j): return sum(ws[i:j + 1]) + .32 * (j - i)
    LIM = (limit if limit < 18 else 20.4) + slack   # 본문은 한 줄 20.4(한글 약 20자). 제목(19px)은 더 짧게
    if W(0, n - 1) <= LIM: return [_line(toks, 0, n - 1)]
    chunks = []; s0 = 0                              # 1) 쉼표·연결 어미·주어 뒤에서 낱덩이로 자른다
    ins = _inside(toks)
    for k in range(n - 1):
        if bpen(toks[k], k) <= 1.5 and not ins[k]: chunks.append((s0, k)); s0 = k + 1
    chunks.append((s0, n - 1))
    lines = []; cur = chunks[0]                      # 2) 덩이를 한 줄 안에 들어가는 만큼 합친다
    for ch in chunks[1:]:
        if W(cur[0], ch[1]) <= LIM: cur = (cur[0], ch[1])
        else: lines.append(cur); cur = ch
    lines.append(cur)
    out = []
    for (i, j) in lines:                             # 3) 한 덩이가 너무 길면 고르게 나눈다
        out += _dp(toks, i, j, LIM) if W(i, j) > LIM else [(i, j)]
    if len(out) > 1 and W(*out[-1]) < 7:                                      # 끝줄에 두세 글자만 남으면 한 줄 너비를 조금 늘려 다시
        if slack == 0.0:
            alt = wrap(inner, limit, 1.3)
            if len(alt) < len(out) or _tail(alt) >= 7: return alt
        out = _dp(toks, 0, n - 1, LIM)
    return [_line(toks, i, j) for i, j in out]

def _tail(lines):
    return width(plain_of(lines[-1]))
def _line(toks, i, j):
    h = " ".join(t["h"] for t in toks[i:j + 1])
    if toks[i]["bs"]: h = "<b>" + h
    if toks[j]["be"]: h += "</b>"
    return h

def P(inner, px=BODY_PX): return f'<p style="text-align:center"><span style="font-size:{px}px">{inner}</span></p>'
def BLANK(): return P("&nbsp;")
SUM = re.compile(r"^([^\s<]{1,4}\s*<b>[^<]{1,12}</b>):\s*(.+)$")

def format_body(body):
    paras = re.findall(r"<p>(.*?)</p>", body, re.S); out = []; k = 0; after_conc = False
    while k < len(paras):
        inner = paras[k].strip(); pl = plain_of(inner).replace("\xa0", " ").strip()
        if inner == "&nbsp;" or not pl and "<img" not in inner:
            out.append(BLANK()); k += 1; continue
        if "<img" in inner or "<a " in inner:
            out.append(f'<p style="text-align:center">{inner}</p>'); k += 1; continue
        if after_conc and SUM.match(inner):                          # 결론 요약 블록: 이름 줄 + 내용 줄
            items = []
            while k < len(paras) and SUM.match(paras[k].strip()):
                m = SUM.match(paras[k].strip()); items.append((m.group(1), m.group(2))); k += 1
            for n, (lab, val) in enumerate(items):
                out.append(P(lab)); out.append(P("<br>".join(wrap(val, BODY_LIMIT))))
                if n < len(items) - 1: out.append(BLANK())
            after_conc = False; continue
        m = re.fullmatch(r"<b>(.*)</b>", inner)
        if m and "<b>" not in m.group(1):                            # 굵은 글씨만 있는 줄 = 제목류
            t = m.group(1); big = bool(re.match(r"^\d+\.\s", plain_of(t))) or bool(re.match(r"^[^\w\s가-힣]", plain_of(t)))
            if re.match(r"^Q\.", plain_of(t)): big = False
            px = TITLE_PX if big else BODY_PX; lines = wrap("<b>" + t + "</b>", TITLE_LIMIT if big else BODY_LIMIT)
            out.append(P("<br>".join(lines), px)); k += 1; continue
        after_conc = "결론부터" in pl
        out.append(P("<br>".join(wrap(inner, BODY_LIMIT)))); k += 1
    return "".join(out)
