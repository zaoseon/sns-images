"""네이버 본문 서식 변환 (10/4 대표 요청): 원고 본문을 네이버에 붙였을 때 바로 이 모양이 되게 한다.
 - 전체 가운데 정렬, 본문 16px, 소제목 19px(굵게)
 - 한 문장을 짧은 줄로 끊는다(폰에서도 한 줄이 한글 약 22자를 넘지 않게). 끊는 자리는 쉼표·연결 어미·주어 다음을 먼저 고른다
 - 글자 내용은 바꾸지 않는다(띄어쓰기와 줄바꿈만). test_format_body.py가 글자 보존을 확인한다
복사해 붙일 때 네이버가 글자 크기·정렬을 그대로 받는지는 네이버 쪽 동작이라, 처음 한 편으로 확인한다."""
import html as H, re

BODY_PX, TITLE_PX = 16, 19
BODY_LIMIT, TITLE_LIMIT = 22.0, 16.8          # 한 줄 최대 너비(한글 1자 = 1.0). 폰 네이버 앱은 16px 기준 약 20~22자

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
    if re.fullmatch(r"(\d+|[QA]|[①-⑩])\.?\)?", q) or re.fullmatch(r"\d+\)", q): return 100          # "1." "Q." "A." "①" 같은 번호 표시 뒤는 끊지 않는다
    q = q.rstrip(".!?)")
    if re.fullmatch(r"[^\w가-힣]{1,4}|\d+\.|[QA]\.", q): return 100                    # 🔹·🧭·1.·Q. 같은 표시 낱말 뒤는 끊지 않는다
    if re.fullmatch(r"(오전|오후)|\d+시", q): return 30                                        # 10/8: 시각은 끊지 않는다("오후 3시 / 29분")
    if len(q) == 1 and q in "몇안못더잘꼭또큰한두세네그이저새각첫온모든": return 40       # 10/8 대표: 한 글자 낱말(몇·안·못·더)을 줄 끝에 홀로 두지 않는다("몇 / 개인지")
    if re.search(r"(와|과|의)$", q) and len(q) >= 2: return 14      # 10/8: "산과 / 비", "별자리와 / 사주로"처럼 뒤 낱말과 한 덩어리인 말을 줄 끝에 두지 않는다
    if re.search(r"(은|는)$", q) and len(q) >= 2 and k <= 2 and not re.search(ADNOM, q): return .5      # 주어·화제 뒤
    if re.search(r"(면서|으면|이면|라면|다면|는데|한데|지만|라서|니까|해서|어서|아서|서도|이며|으며|으니|하며|함께|만큼|동안|마다|무렵|뒤에)$", q) or (re.search(r"(면|고|며)$", q) and len(q) >= 3): return 1.5
    if re.search(r"(이|가|도|만|께서)$", q) and len(q) >= 3: return 2.5
    if not re.search(r"[가-힣]", q): return 2.0                                   # zaoseon.com 같은 로마자·숫자 낱말
    if q in ("중", "뒤", "때", "후", "전", "사이"): return 1.0                       # "세 지도 중 / 몇 개가"처럼 짧은 때·범위 낱말 뒤
    if re.search(r"(을|를)$", q) and len(q) >= 3: return 1.0                 # 10/8 대표 캡처: "운명학을 / 겹쳐 읽어요", "숫자를 / 한 자리가"처럼 목적어 뒤에서 끊는다
    if re.search(r"(에서|에게|에는|보다|처럼|까지|부터|으로|에)$", q): return 2.0
    if re.search(r"[\'\"”’]$", q) and len(q) >= 3: return 0.5               # 따옴표를 닫은 뒤
    if re.search(r"(야|해|라|서)$", q) and len(q) >= 2 and k >= 1 and not re.search(r"(에서|에게서)$", q): return 0.8 # "끝나야 | 입을", "위해 | 결론부터" 같은 연결 어미 뒤
    return 9


AUXG = ("않고", "있고", "없고", "싶고", "같고", "보고", "두고", "주고")
CONNS = r"(면서|으면|이면|라면|다면|는데|한데|지만|라서|니까|해서|어서|아서|서도|이며|으며|으니|하며|보다|다가|도록|거나|든지)$"
def _major(tok, k):
    """큰 덩어리 끝인가: 쉼표, 연결 어미(~이라·~하고·~끝나야·~위해·~풀기보다), 따옴표 닫음. 10/8 대표 캡처의 줄바꿈이 이 자리에서 끊긴다."""
    q = tok["p"].rstrip()
    if q.endswith((",", "，")): return True
    if re.search(r"\)(은|는)$", q): return True                                 # 전갈자리(10/23~11/21)는 | 깊이 담아…
    q = q.rstrip(".!?)")
    if re.search(r"[^'\"‘“][’”'\"][^'\"’”]{0,3}$", q): return True                    # 따옴표를 닫음(뒤에 조사 붙어도)
    if q in AUXG or len(q) < 2 or k < 1: return False                       # 문장 맨 앞 낱말("하지만")은 덩어리 끝이 아니다
    if re.search(r"(에서|에게서|에서는)$", q): return False
    if re.search(CONNS, q): return True
    if re.search(r"(면|고|며)$", q): return True
    if re.search(r"(야|해|라|서)$", q): return True                              # "끝나야 | 입을", "위해 | 결론부터", "산이라 | 움직이지"
    return False
def _listunit(tok):
    """'사주·별자리·숫자'처럼 조사 없이 가운뎃점으로 나열한 낱말: 한 줄로 따로 둔다."""
    q = tok["p"].strip(); return q.count("·") >= 2 and not re.search(r"[은는이가을를의과와도만로에]$", q)

def _inside(toks):                               # k번째 낱말 뒤가 괄호·따옴표 안이면 True(그 안에서는 끊지 않는다)
    out = []; d = 0; q = False
    for t in toks:
        p = t["p"]; d += p.count("(") - p.count(")")
        if re.match(r"^['\"‘“]", p) and not re.search(r"['\"’”][^'\"’”]{0,4}$", p[1:]): q = True        # 따옴표를 열고 같은 낱말 안에서 닫지 않음
        elif q and re.search(r"['\"’”][^'\"’”]{0,4}$", p): q = False                                      # 닫는 따옴표(뒤에 조사 붙어도)
        out.append(d > 0 or q)
    return out

def _dp(toks, i0, j0, limit, force=False, tailpen=True):
    """toks[i0..j0]를 limit 안의 줄로 나눈다(줄 너비가 고르고 끊는 자리가 자연스럽게)."""
    n = j0 - i0 + 1; ws = [width(t["p"]) for t in toks[i0:j0 + 1]]; ins = _inside(toks)
    def W(i, j): return sum(ws[i:j + 1]) + .32 * (j - i)
    if W(0, n - 1) <= limit and not force: return [(i0, j0)]
    INF = 1e9; best = [INF] * (n + 1); back = [0] * (n + 1); best[0] = 0; ideal = limit - 4
    for j in range(1, n + 1):
        for i in range(j - 1, -1, -1):
            w = W(i, j - 1)
            if w > limit and i != j - 1: break
            last = j == n
            c = 6 + (0 if last else 3 * bpen(toks[i0 + j - 1], i0 + j - 1) + (300 if ins[i0 + j - 1] else 0)) + ((0.12 * (ideal - w) ** 2) if not last else ((0.12 * max(0, 9 - w) ** 2 + (45 if w < 5 else 0)) if tailpen else 0))
            if w > limit: c += 50
            if force and i == 0 and j == n and n > 1: c += 1000
            if best[i] + c < best[j]: best[j] = best[i] + c; back[j] = i
    out = []; j = n
    while j > 0: i = back[j]; out.append((i0 + i, i0 + j - 1)); j = i
    return out[::-1]

import json as _json, os as _os
try: OVERRIDES = {k: v for k, v in _json.load(open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "line_overrides.json"), encoding="utf-8")).items() if not k.startswith("_")}
except Exception: OVERRIDES = {}

def wrap(inner, limit, slack=0.0, soft=None):
    if "<" not in inner and OVERRIDES.get(inner.strip()): return list(OVERRIDES[inner.strip()])      # 사람이 직접 끊은 문장
    toks = tokenize(inner); n = len(toks)
    if n == 0: return [inner]
    ws = [width(t["p"]) for t in toks]
    def W(i, j): return sum(ws[i:j + 1]) + .32 * (j - i)
    LIM = (limit if limit < 18 else 18.0) + slack   # 본문은 한 줄 19.8(한글 약 19자, 폰 폭 여유). 제목(19px)은 16.8(10/8 대표: 모바일 줄 길이 정리)
    SING = min(soft, LIM) if soft else LIM          # soft가 있으면 이 너비를 넘는 문장은 두 줄 이상으로 나눈다
    if W(0, n - 1) <= SING: return [_line(toks, 0, n - 1)]
    chunks = []; s0 = 0                              # 1) 쉼표·연결 어미·주어 뒤에서 낱덩이로 자른다
    ins = _inside(toks)
    for k in range(n - 1):
        if (_major(toks[k], k) or _listunit(toks[k]) or _listunit(toks[k + 1])) and not ins[k]: chunks.append((s0, k)); s0 = k + 1
    chunks.append((s0, n - 1))
    lines = []; cur = chunks[0]                      # 2) 덩이를 한 줄 안에 들어가는 만큼 합친다
    for ch in chunks[1:]:
        if W(cur[0], ch[1]) <= SING and not (ch[0] == ch[1] and _listunit(toks[ch[0]])) and not (cur[0] == cur[1] and _listunit(toks[cur[0]])): cur = (cur[0], ch[1])
        else: lines.append(cur); cur = ch
    lines.append(cur)
    out = []
    for (i, j) in lines:                             # 3) 한 덩이가 너무 길면 고르게 나눈다
        out += _dp(toks, i, j, LIM, tailpen=(j == n - 1)) if W(i, j) > LIM else [(i, j)]   # 끝 덩이가 아니면 끝줄 짧음 벌점을 빼고, 아래에서 다음 덩이와 합친다
    merged = [out[0]]                                # 4) 나눈 조각의 끝줄이 다음 덩이와 한 줄에 들어가면 합친다("아니라 + 정리하는 시간이에요.")
    for (i, j) in out[1:]:
        a, b = merged[-1]
        if b - a + 1 <= 2 and W(a, j) <= SING and not _listunit(toks[a]) and not _listunit(toks[j]): merged[-1] = (a, j)
        else: merged.append((i, j))
    out = merged
    if soft and len(out) == 1 and W(0, n - 1) > SING: out = _dp(toks, 0, n - 1, LIM, True)
    if len(out) > 1 and W(*out[-1]) < 4.5:                                      # 끝줄에 두세 글자만 남으면 한 줄 너비를 조금 늘려 다시
        out = _dp(toks, 0, n - 1, LIM)             # 10/8: 한 줄 폭을 늘리지 않고(대표 폰 기준 18.0) 전체를 다시 고르게 나눈다
    if len(out) == 2:                                # 10/10 대표: 두 줄이면 두 줄의 길이가 비슷하게(쉼표 뒤 끊기는 그대로 둔다). 짧은 줄이 긴 줄의 55% 아래이면 줄 폭 차이가 가장 작은 자리(와·과·의·한 글자 낱말·꾸밈말 뒤는 제외)로 다시 끊는다
        (a, b), (c, d) = out; w1, w2 = W(a, b), W(c, d)
        if not toks[b]["p"].rstrip().endswith((",", "，", "을", "를", "중")) and min(w1, w2) / max(w1, w2) < .55:
            ins2 = _inside(toks); best_k, best_c = None, None
            for k in range(a, d):
                if ins2[k] or W(a, k) > LIM or W(k + 1, d) > LIM: continue
                pk = bpen(toks[k], k)
                if pk >= 10: continue
                if pk >= 9 and not re.search(r"(은|는|이|가|을|를|에|로|도|만|서|고|며|면|게|지|요|다|네|데|까|쯤|라)$|\d+(일|분|시|월|년|번|개|명)$|^(모두|함께|먼저|다시|바로|이미|항상|자주|가끔|아직|특히|보통|그래서|하지만|그리고|또는|그런데|가장|많이|조금|훨씬|서로|오히려|조금씩|천천히|빨리)$", toks[k]["p"].rstrip(".!?")): continue     # 낱말 덩어리(태양|별자리, 시간|단위)는 쪼개지 않는다
                c2 = abs(W(a, k) - W(k + 1, d)) + .6 * pk
                if best_c is None or c2 < best_c: best_k, best_c = k, c2
            if best_k is not None and best_k != b and abs(W(a, best_k) - W(best_k + 1, d)) + 2 < abs(w1 - w2): out = [(a, best_k), (best_k + 1, d)]
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
SUM = re.compile(r"^([^\s<]{1,4}\s*<b>[^<]{1,12}</b>):\s*(.+)$")                 # 이모지 + <b>이름</b>: 내용
LAB = re.compile(r"^([^\s<]{1,4}\s*<b>([^<]{1,14})</b>):\s*(.+)$")

BOX_LIMIT = 13.5      # 10/8 대표 캡처: 요약 상자 안 줄은 폭 13 안팎
def box_lines(val):
    """요약 상자 안 줄바꿈: 쉼표로 나열한 항목(산(戊)과 쇠(庚), 전갈·염소자리, 숫자 4와 7)은 한 줄에 하나, 그 밖은 폭 13.5로 의미 단위."""
    out = []
    for piece in re.split(r"<br\s*/?>", val):
        for piece in re.split(r"(?<=[.!?])\s+", piece.strip()):               # 문장마다 따로(앞 문장 뒤에 쉼표 나열이 붙어 한 줄이 길어지는 것 방지, 10/9)
            piece = piece.strip()
            if not piece: continue
            items = [x.strip() for x in re.split(r"(?<=,)\s+", piece) if x.strip()]
            if piece.count(",") >= 2 and len(plain_of(piece)) < 60 and all(width(plain_of(x)) <= BOX_LIMIT for x in items): out += items      # 항목이 모두 한 줄에 들어갈 때만 한 줄에 하나씩(마지막 항목이 길면 의미 단위로 감는다)
            else: out += sent_lines(piece, BOX_LIMIT)
    return out

def sent_lines(inner, limit=BODY_LIMIT, soft=None):
    """문장마다 새 줄에서 시작하고, 긴 문장은 짧은 줄로 끊는다(문장 안 <br>도 줄 시작으로 본다)."""
    out = []
    for piece in re.split(r"<br\s*/?>", inner):
        toks = tokenize(piece.strip()); cur = []
        for k, t in enumerate(toks):
            cur.append(t["h"])
            if re.search(r"[.!?]$", t["p"].rstrip("”\"')")) and not re.fullmatch(r"(\d+|[QA])\.", t["p"]) and k < len(toks) - 1:
                out += wrap(_join(toks, k - len(cur) + 1, k), limit, 0.0, soft); cur = []
        if cur: out += wrap(_join(toks, len(toks) - len(cur), len(toks) - 1), limit, 0.0, soft)
    return out
def _join(toks, i, j): return _line(toks, i, j)

def _prep(paras):
    """문단 순서 손질: 인사말이 '첫 문장 → 주제 문장 → 인사말' 순서이면 '첫 문장 → 인사말 → 주제 문장'으로(대표 정리본 기준)."""
    if len(paras) >= 3 and plain_of(paras[2]).strip() == "안녕하세요, 자오선의 정월이에요." and plain_of(paras[0]).strip().endswith("?"):
        paras = [paras[0], paras[2], paras[1]] + paras[3:]
    return paras

def _next_nonblank(paras, k):
    while k < len(paras) and paras[k].strip() == "&nbsp;": k += 1
    return k

def format_body(body):
    paras = _prep(re.findall(r"<p>(.*?)</p>", body, re.S)); out = []; k = 0; after_conc = False; in_order = False
    while k < len(paras):
        inner = paras[k].strip(); pl = plain_of(inner).replace("\xa0", " ").strip()
        if inner == "&nbsp;" or not pl and "<img" not in inner:
            out.append(BLANK()); k += 1; continue
        if "<img" in inner or "<a " in inner:
            out.append(f'<p style="text-align:center">{inner}</p>'); k += 1; continue
        if after_conc and SUM.match(inner):                          # 결론 요약 블록: 이름 줄 + 내용 줄(이름 뒤 ':' 없이), 항목 사이 빈 줄
            items = []
            def _cont(kk):     # 항목 바로 뒤 일반 문단(빈 줄·다른 항목·제목·이미지 아님)은 같은 항목의 내용
                return kk < len(paras) and paras[kk].strip() != "&nbsp;" and not SUM.match(paras[kk].strip()) and "<img" not in paras[kk] and "<a " not in paras[kk] and not re.fullmatch(r"<b>.*</b>", paras[kk].strip()) and not plain_of(paras[kk]).strip().startswith(("📌", "👇"))
            while k < len(paras):
                kk = _next_nonblank(paras, k)
                if kk < len(paras) and SUM.match(paras[kk].strip()):
                    m = SUM.match(paras[kk].strip()); val = m.group(2); k = kk + 1
                    while _cont(k): val += "<br>" + paras[k].strip(); k += 1
                    items.append((m.group(1), val))
                else: break
            for n, (lab, val) in enumerate(items):
                out.append(P(lab)); out.append(P("<br>".join(box_lines(val))))
                if n < len(items) - 1: out.append(BLANK())
            after_conc = False; continue
        m = LAB.match(inner)
        if m and len(plain_of(m.group(3)).strip()) >= 4:   # 10/8: 이름 줄을 따로(':' 유지), 내용은 다음 줄부터
            out.append(P(m.group(1) + ":")); out.append(P("<br>".join(sent_lines(m.group(3), BODY_LIMIT, 17.0)))); k += 1; continue
        if pl.startswith("👇"):                                       # 함께 볼 글 안내: '👇 유도 문구' 줄 + 연결 글 제목 줄(제목은 첫 쉼표 앞까지, 카드에 전체 제목이 나온다)
            t = pl[1:].strip(); mm = re.match(r"^(.+?[.!?])\s+(.+)$", t)
            if mm: tea, ttl = mm.group(1), mm.group(2)
            else:
                mm = re.match(r"^(.+?),\s*(.+)$", t); tea, ttl = (mm.group(1) + "?", mm.group(2)) if mm else (t, "")
            ttl = ttl.split(", ")[0].strip()
            out.append(P("<br>".join(wrap("👇 " + tea, BODY_LIMIT, 0.0, 17.0))))   # 10/5 대표 지적: 긴 유도 문구·제목 줄이 폰에서 아무 데서나 꺾였다 → 일반 문장처럼 짧은 줄로 나눈다
            if ttl: out.append(P("<br>".join(wrap(ttl, BODY_LIMIT, 0.0, 17.0))))
            k += 1; continue
        m = re.fullmatch(r"<b>(.*)</b>", inner)
        if m and "<b>" not in m.group(1):                            # 굵은 글씨만 있는 줄 = 제목류
            t = m.group(1); big = bool(re.match(r"^\d+\.\s", plain_of(t))) or bool(re.match(r"^[^\w\s가-힣]", plain_of(t)))
            if re.match(r"^Q\.", plain_of(t)): big = False
            px = TITLE_PX if big else BODY_PX; lines = wrap("<b>" + t + "</b>", TITLE_LIMIT if big else BODY_LIMIT)
            out.append(P("<br>".join(lines), px)); k += 1; continue
        after_conc = "결론부터" in pl
        if pl.startswith("📌"): in_order = True
        elif in_order and re.match(r"^\d+\.\s", pl):                  # 이 글의 순서 목록 줄은 한 줄로 둔다(대표 캡처: "4. 같은 말을 하는 곳, 다른 말을 하는 곳"이 한 줄) - 폭 20.5까지
            out.append(P("<br>".join(wrap(inner, BODY_LIMIT, 2.5)))); k += 1; continue
        else: in_order = False
        out.append(P("<br>".join(sent_lines(inner)))); k += 1
    return "".join(out)
