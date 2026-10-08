"""네이버 본문 서식 2판 (10/5 대표 요청 6가지). format_body.format_body()가 만든 본문 위에 얹는다(기존 변환기는 그대로).
 1) 첫 문단 / 인사말(안녕하세요, 자오선의 정월이에요.) / 간단 설명+결론 안내를 빈 줄로 나눈다
 2) 한 줄 요약·세 풀이·해 볼 것 같은 요약 줄을 네모 박스(1칸 표, 이미지 폭·흰 바탕·회색 윤곽선) 안에 넣고 항목 사이를 한 줄 띄운다
 3) '📌 이 글의 순서'를 요약 이미지(한눈에 보기) 다음으로 옮긴다
 4) 구분선(<hr>, 회색·이미지 폭): 이 글의 순서 앞과 뒤, 번호 제목 사이, 마무리와 👇 유도 문구 사이
 5) 번호 제목 다음 한 줄 띄우기, 항목(🔹·1위·1.)마다 한 줄 띄우기
 6) 본문 이미지는 가로 IMG_W px 작은 판(img/m640/)을, CTA 배너도 같은 IMG_W px 작은 판(img/m640/)을 쓴다 → 네이버에 붙이면 문서 너비로 커지지 않는다
 7) 구분선·이미지 바로 뒤에는 빈 줄을 두지 않는다. 구분선은 LINE_W px 가운데 회색
글자는 더하지 않는다. 단 '정월이에요.'만 있던 인사말은 전체 인사말로 바꾼다. test_format_v2.py가 글자 보존을 확인한다.
복사해 붙일 때 네이버가 표·구분선·이미지 크기를 어떻게 받는지는 네이버 쪽 동작이라, 처음 한 편으로 확인한다."""
import re
import format_body as FB

IMG_W = 640
SMALL_DIR = "m1280"   # 10/8: 납품판 폴더. 파일은 가로 1280(imgkit이 2560 원본을 줄여 만듦)이고 HTML width는 아래 IMG_W(640)로 둔다. 편집기에서 크게 붙으면 DELIV_W를 960으로
DELIV_W = 1280
LINE_W = 480       # 구분선 폭(px, 이미지보다 짧게 가운데)
CTA_W = IMG_W      # CTA 배너는 본문 이미지와 같은 폭(640px). 네이버 에디터가 붙인 이미지 폭을 화면 폭에 비례해 줄이므로, 이미지 640px ≈ 링크 카드 폭(10/5 대표: 480px 배너가 카드보다 작게 나옴)
GREET = "안녕하세요, 자오선의 정월이에요."
HR = "<hr>"
PTAG = re.compile(r"<p[^>]*>.*?</p>|<hr>", re.S)
LINE_GRAY = "#c8c8c8"
BOX_OPEN = f'<table width="{IMG_W}" align="center" style="width:{IMG_W}px;max-width:100%;border-collapse:collapse"><tbody><tr><td style="border:1px solid #cfcfcf;background:#ffffff;padding:16px 12px;text-align:center">'
BOX_CLOSE = "</td></tr></tbody></table>"
HR_HTML = f'<hr width="{LINE_W}" align="center" style="width:{LINE_W}px;max-width:100%;border:0;border-top:1px solid {LINE_GRAY};margin:0 auto">'   # 구분선: 회색, 가운데, 이미지보다 짧게(앞뒤 빈 줄 없음)
ITEM = re.compile(r"^(🔹|🔸|▪️|▫️|•|[①-⑩]|\d+위|\d+\)|\d+\.\s)")
NUMHEAD = re.compile(r"^\d+\.\s")

def pl(p): return FB.plain_of(p).replace("\xa0", " ").strip()
def blank(p): return p != HR and pl(p) == "" and "<img" not in p
def isimg(p): return "<img" in p
def iscta(p): return "naver_cta" in p
def big(p): return "font-size:19px" in p
def numhead(p): return p != HR and big(p) and bool(NUMHEAD.match(pl(p)))
def emoji0(t): return bool(t) and ord(t[0]) > 0x2000 and not t[0].isalnum()
def first_text(p): return pl(p)

def _split_greeting(paras):
    """인사말을 따로 한 문단으로: 앞 문장과 한 문단이면 쪼개고, '정월이에요.'만 있으면 전체 인사말로."""
    out = []; done = False
    for p in paras:
        t = pl(p)
        if not done and p != HR and not p.startswith("<table") and "정월이에요" in t and len(t) < 90 and not isimg(p):
            done = True
            segs = re.split(r"<br\s*/?>", re.search(r"<span[^>]*>(.*)</span>", p, re.S).group(1))
            gi = next((i for i, s in enumerate(segs) if "안녕하세요" in FB.plain_of(s) or "정월이에요" in FB.plain_of(s)), None)
            if gi is None: out.append(p); continue
            before, line = segs[:gi], segs[gi]
            if "안녕하세요" in line and line.index("안녕하세요") > 0:       # 앞 문장과 같은 줄이면 '안녕하세요' 앞에서 자른다
                k = line.index("안녕하세요"); before = before + [line[:k].strip()]; line = line[k:]
            before = [b for b in before if FB.plain_of(b).strip()]
            if before: out.append(FB.P("<br>".join(before)))
            g = "<br>".join([line] + segs[gi + 1:])
            out.append(FB.P(GREET if FB.plain_of(g).strip() == "정월이에요." else g)); continue
        out.append(p)
    return out

def _blank_around(paras, idx_pred):
    """idx_pred가 True인 문단 앞뒤에 빈 줄이 정확히 한 칸씩 있게."""
    out = []
    for i, p in enumerate(paras):
        if p != HR and idx_pred(p):
            if out and not blank(out[-1]) and out[-1] != HR: out.append(FB.BLANK())
            out.append(p)
            if i + 1 < len(paras) and not blank(paras[i + 1]) and paras[i + 1] != HR: out.append(FB.BLANK())
        else: out.append(p)
    return out

def _is_greeting(p): return p != HR and pl(p) == GREET

def _dedupe_blanks(paras):
    out = []
    for p in paras:
        if blank(p) and out and (blank(out[-1]) or out[-1] == HR): continue
        if p == HR:
            while out and blank(out[-1]): out.pop()
        out.append(p)
    # HR 바로 뒤의 빈 줄은 뺀다(구분선에 자체 여백이 있다)
    res = []
    for i, p in enumerate(out):
        if blank(p) and res and res[-1] == HR: continue
        res.append(p)
    return res

def _tighten_intro(paras):
    """인사말 뒤 '간단 설명 → 결론 안내'는 한 묶음: 둘 사이의 빈 줄을 뺀다."""
    gi = next((i for i, p in enumerate(paras) if _is_greeting(p)), None)
    if gi is None: return paras
    for i, p in enumerate(paras):
        if i > gi and p != HR and ("결론부터" in pl(p) or "한 줄로 정리" in pl(p)):
            if i >= 2 and blank(paras[i - 1]) and not blank(paras[i - 2]) and paras[i - 2] != HR and i - 2 > gi and not isimg(paras[i - 2]):
                return paras[:i - 1] + paras[i:]
            break
    return paras

def _summary_range(paras):
    """'한 줄 요약' 줄부터 요약 항목이 이어지는 끝까지 [s, e]. 없으면 None."""
    s = next((i for i, p in enumerate(paras) if p != HR and re.match(r"^\S{1,4}\s*한 줄 요약", pl(p)) and not big(p)), None)
    if s is None: return None
    e = s; n = len(paras)
    while e + 1 < n:
        q = paras[e + 1]; t = pl(q)
        if q == HR or isimg(q) or big(q) or t.startswith("📌"): break
        if blank(q):
            j = e + 2
            while j < n and paras[j] != HR and blank(paras[j]): j += 1
            if j < n and paras[j] != HR and not isimg(paras[j]) and not big(paras[j]) and emoji0(pl(paras[j])) and not pl(paras[j]).startswith("📌"):
                e = j - 1; continue
            break
        e += 1
    while e > s and blank(paras[e]): e -= 1
    return s, e

def _rewrap_box_p(p):
    m = re.fullmatch(r"(<p[^>]*><span[^>]*>)(.*)(</span></p>)", p, re.S)
    if not m or "<img" in m.group(2) or FB.plain_of(m.group(2)).strip() in ("", "\xa0"): return p
    joined = " ".join(x.strip() for x in re.split(r"<br\s*/?>", m.group(2)))
    if FB.width(FB.plain_of(joined)) <= FB.BOX_LIMIT and "<br" not in m.group(2): return p
    return m.group(1) + "<br>".join(FB.box_lines(joined)) + m.group(3)

def _box_summary(paras):
    r = _summary_range(paras)
    if not r: return paras
    s, e = r; inner = []
    for p in paras[s:e + 1]:
        if p != HR and not blank(p) and emoji0(pl(p)) and not big(p) and inner and not blank(inner[-1]): inner.append(FB.BLANK())   # 한 줄 요약 / 세 풀이 / 해 볼 것을 한 줄씩 띄운다
        inner.append(_rewrap_box_p(p) if not blank(p) and not big(p) else p)
    while inner and blank(inner[-1]): inner.pop()
    return paras[:s] + [BOX_OPEN + "".join(inner) + BOX_CLOSE] + paras[e + 1:]

def _order_block(paras):
    h = next((i for i, p in enumerate(paras) if p != HR and pl(p).startswith("📌 이 글의 순서")), None)
    if h is None: return None
    e = h
    while e + 1 < len(paras) and paras[e + 1] != HR and NUMHEAD.match(pl(paras[e + 1])) and not big(paras[e + 1]) and not blank(paras[e + 1]): e += 1
    return h, e

def _move_order(paras):
    """📌 이 글의 순서를, 요약 박스 뒤에 오는 첫 이미지(한눈에 보기) 다음으로. 그런 이미지가 첫 번호 제목보다 앞에 없으면 그대로."""
    ob = _order_block(paras)
    if not ob: return paras
    h, e = ob; block = paras[h:e + 1]
    box = next((i for i, p in enumerate(paras) if p.startswith("<table")), None)
    first_head = next((i for i, p in enumerate(paras) if numhead(p)), len(paras))
    start = box if box is not None else h
    im = next((i for i in range(start + 1, first_head) if isimg(paras[i]) and not iscta(paras[i])), None)
    if im is None or im < h: return paras
    rest = paras[:h] + paras[e + 1:]
    im2 = im - (e - h + 1)
    return rest[:im2 + 1] + [FB.BLANK()] + block + [FB.BLANK()] + rest[im2 + 1:]

def _dividers(paras):
    out = []
    ob = _order_block(paras)
    after_order = (ob[1] if ob else None)
    heads = [i for i, p in enumerate(paras) if numhead(p)]
    for i, p in enumerate(paras):
        if p != HR and ((i in heads) or (after_order is not None and False)):
            out.append(HR)
        if p != HR and ((pl(p).startswith("👇") and not ENGAGE.search(pl(p))) or pl(p).startswith("📌 이 글의 순서")):   # 함께 볼 글 안내(👇) 앞, 이 글의 순서 앞. 댓글·공유 유도 문구의 👇 앞에는 두지 않는다
            out.append(HR)
        out.append(p)
    return out

def _bold_guide(paras):
    """마무리 유도 문구(👇 줄)를 굵게. 기존 변환기가 굵은 표시를 지우므로 여기서 다시 입힌다. 바로 아래 연결 글 제목 줄은 그대로."""
    out = []
    for p in paras:
        if p != HR and not p.startswith("<table") and pl(p).startswith("👇") and "<b>" not in p:
            p = re.sub(r"(<span[^>]*>)(.*)(</span>)", r"\1<b>\2</b>\3", p, count=1, flags=re.S)
        out.append(p)
    return out

ENGAGE = re.compile(r"댓글(?:로|에)[^.!?]{0,30}(?:남겨|알려)|이 글을 공유해 주세요")
def _engage_emoji(paras):
    """댓글·공유를 청하는 유도 문구 문단 맨 앞에 👇를 붙인다(10/5 대표 요청). 첫 줄에 자리가 없으면(폰 한 줄 22자 넘음) 이모지만 윗줄에 둔다. 이미 이모지·번호로 시작하는 줄은 건드리지 않는다."""
    out = []
    for p in paras:
        if p != HR and not p.startswith("<table") and "<img" not in p and "<a " not in p:
            t = pl(p).strip()
            if ENGAGE.search(t) and len(t) < 160 and not re.match(r"^(👇|📌|✔|🔹|🔸|\d+\.|Q\.|A\.|[\U0001F300-\U0001FAFF])", t):
                m = re.match(r"(<p[^>]*><span[^>]*>)(.*)(</span></p>)$", p, re.S)
                if m:
                    lines = m.group(2).split("<br>")
                    if FB.width(FB.plain_of(lines[0])) + 2.0 <= 18.0: lines[0] = "👇 " + lines[0]
                    else: lines.insert(0, "👇")
                    p = m.group(1) + "<br>".join(lines) + m.group(3)
        out.append(p)
    return out

def _after_heading_blank(paras):
    out = []
    for i, p in enumerate(paras):
        out.append(p)
        if numhead(p) and i + 1 < len(paras) and not blank(paras[i + 1]) and paras[i + 1] != HR and not isimg(paras[i + 1]): out.append(FB.BLANK())
    return out

def _is_item(p):
    if p == HR or p.startswith("<table") or big(p) or isimg(p): return False
    t = pl(p)
    if not t or t.startswith(("📌", "👇")): return False
    return bool(ITEM.match(t) or t.startswith("Q.") or emoji0(t))

def _items_blank(paras):
    """🔹·1위·1.·Q.·이모지로 시작하는 항목(💼 일, 🌌 별자리, 띠 묶음 등)은 항목마다 한 줄 띄운다. 이 글의 순서 목록과 요약 박스 안은 그대로."""
    out = []; in_order = False
    for p in paras:
        t = pl(p) if p != HR and not p.startswith("<table") else ""
        if t.startswith("📌 이 글의 순서"): in_order = True
        elif in_order and not (NUMHEAD.match(t) and not big(p)): in_order = False
        if not in_order and _is_item(p):
            if out and not blank(out[-1]) and out[-1] != HR and not isimg(out[-1]) and not big(out[-1]) and not out[-1].startswith("<table"): out.append(FB.BLANK())
        out.append(p)
    return out

def _blank_after_box(paras):
    out = []
    for i, p in enumerate(paras):
        out.append(p)
        if p.startswith("<table") and i + 1 < len(paras) and not blank(paras[i + 1]) and paras[i + 1] != HR: out.append(FB.BLANK())
    return out

def _no_blank_after_image(paras):
    """이미지 바로 다음에는 빈 줄을 두지 않는다(네이버가 이미지 설명칸 때문에 자동으로 간격을 만든다 - 대표 10/5)."""
    out = []
    for p in paras:
        if blank(p) and out and out[-1] != HR and isimg(out[-1]): continue
        out.append(p)
    return out

def _small_images(body):
    def sub(m):
        tag = m.group(0)
        if f"/{SMALL_DIR}/" in tag: return tag
        tag = re.sub(r'(/naver/img/)([^"/?]+)', r"\1" + SMALL_DIR + r"/\2", tag)    # 본문 이미지와 CTA 배너 모두 같은 폭(640px) 작은 판
        if "width=" not in tag: tag = tag.replace("<img ", f'<img width="{IMG_W}" ', 1)
        return tag
    return re.sub(r"<img[^>]*>", sub, body)

def link_guide(body, url):
    """👇 유도 문구 바로 아래 제목 줄에 연결 글 주소로 링크를 건다(이미 걸려 있으면 그대로). 주소는 앱에 저장된 값(data/naver_urls.json)."""
    if not url: return body
    import html as _h
    ms = list(re.finditer(r"<p[^>]*>.*?</p>", body, re.S)); g = max((i for i, m in enumerate(ms) if "👇" in FB.plain_of(m.group(0))), default=None)   # 함께 볼 글 안내는 본문 끝(CTA 앞)의 마지막 👇 줄. 앞쪽 댓글·공유 유도 문구의 👇와 헷갈리지 않게
    if g is None: return body
    for m in ms[g + 1:]:
        t = FB.plain_of(m.group(0)).replace("\xa0", " ").strip()
        if not t: continue
        if "<img" in m.group(0) or "<a " in m.group(0): return body
        new = re.sub(r"(<span[^>]*>)(.*)(</span>)", lambda k: k.group(1) + '<a href="' + _h.escape(url, quote=True) + '">' + k.group(2) + "</a>" + k.group(3), m.group(0), count=1, flags=re.S)
        return body[:m.start()] + new + body[m.end():]
    return body


# ---- 10/8 대표 캡처 반영: 문단 사이 줄띄움·도입부 간격·이미지 앞뒤 ----
def _nlines(p):
    m = re.search(r"<span[^>]*>(.*)</span>", p, re.S)
    return len([x for x in re.split(r"<br\s*/?>", m.group(1)) if FB.plain_of(x).strip()]) if m else 1
def _wholebold(p): return p != HR and not p.startswith("<table") and bool(re.fullmatch(r'<p[^>]*><span[^>]*><b>.*</b></span></p>', p, re.S)) and p.count("<b>") == 1
def _is_q(p): return pl(p).startswith("Q.")
def _is_sublabel(p):
    """🧭 사주 - 무토·경금일생 처럼 이모지로 시작하는 한 줄 작은 제목(굵은 글씨, ' - ' 포함)."""
    t = pl(p) if p != HR and not p.startswith("<table") else ""
    return bool(t) and emoji0(t) and " - " in t and "<b>" in p and _nlines(p) == 1 and not big(p)
def _plainp(p): return p != HR and not p.startswith("<table") and not blank(p) and not isimg(p) and not big(p) and "<a " not in p
def _conclusion_idx(paras):
    return next((i for i, p in enumerate(paras) if p != HR and not p.startswith("<table") and ("결론부터" in pl(p) or "한 줄로 정리" in pl(p) or "한 줄 정리" in pl(p))), None)

def _intro_gaps(paras):
    """도입 문단들·정월 인사·설명 문단·결론 안내 문장을 모두 한 줄씩 띄운다(10/8 대표: 도입 문단 이후 한 줄 띄고 정월 인사, 한 줄 띄고 문단, 한 줄 띄고 결론 안내)."""
    ci = _conclusion_idx(paras)
    if ci is None: return paras
    out = []
    for i, p in enumerate(paras):
        if out and i <= ci and _plainp(p) and _plainp(out[-1]): out.append(FB.BLANK())
        out.append(p)
    return out

def _paragraph_gaps(paras):
    """문단과 문단 사이 한 줄 띄움(10/8 대표 캡처). 한 문단 = 짧은 문장 묶음(합쳐서 4줄까지). 굵은 한 줄(핵심 문장)은 따로 한 문단.
    항목(🔹·1.·이모지 제목:)과 그 설명 줄, Q.와 A. 줄, 이 글의 순서 목록은 한 덩어리로 둔다."""
    out = []; cnt = 0; chain = False; ci = _conclusion_idx(paras); in_order = False
    for i, p in enumerate(paras):
        t = pl(p) if p != HR and not p.startswith("<table") else ""
        if t.startswith("📌 이 글의 순서"): in_order = True
        elif in_order and not (NUMHEAD.match(t) and not big(p) and t): in_order = False
        if out and not blank(out[-1]) and out[-1] != HR and not out[-1].startswith("<table") and not isimg(out[-1]) and _plainp(p) or (out and _is_q(p) and False):
            prev = out[-1]
            if in_order: pass
            elif pl(prev).startswith("👇"): pass                                          # 👇 유도 문구와 바로 아래 연결 글 제목은 붙여 둔다
            elif chain and not _is_item(p) and not _wholebold(p): pass                       # 항목·Q&A의 설명 줄은 붙여 둔다
            elif _wholebold(prev) and not _is_q(prev) and not _wholebold(p) and chain is False: out.append(FB.BLANK()); cnt = 0
            elif _wholebold(p) or _wholebold(prev): out.append(FB.BLANK()); cnt = 0
            elif _is_item(p): pass                                                           # 항목 앞 빈 줄은 _items_blank가 담당
            elif cnt + _nlines(p) <= 4: pass                                                 # 짧은 문장끼리는 한 문단
            else: out.append(FB.BLANK()); cnt = 0
        if blank(p) or p == HR or p.startswith("<table") or isimg(p) or big(p): cnt = 0; chain = False
        else:
            cnt = (cnt + _nlines(p)) if out and not blank(out[-1]) else _nlines(p)
            chain = bool(_is_item(p) or _is_q(p) or (chain and _plainp(p) and not _wholebold(p)))
        out.append(p)
    return out

def _no_blank_before_image(paras):
    """이미지 앞뒤로는 줄띄움 없이(10/8 대표): 번호 제목 바로 아래 이미지, 상자·본문 뒤 이미지 앞의 빈 줄을 뺀다."""
    out = []
    for p in paras:
        if isimg(p) and out and blank(out[-1]): out.pop()
        out.append(p)
    return out


def _sublabel_blank(paras):
    """작은 제목(굵은 한 줄, 이모지·번호로 시작, Q. 제외) 다음에는 한 줄 띄운다. 바로 이미지·구분선이 오면 띄우지 않는다(10/8 대표)."""
    out = []
    for i, p in enumerate(paras):
        out.append(p)
        order_head = p != HR and not p.startswith("<table") and pl(p).startswith("📌 이 글의 순서")
        if (order_head or ((_wholebold(p) or _is_sublabel(p)) and not big(p))) and not _is_q(p) and not (p != HR and not p.startswith("<table") and pl(p).startswith("👇")) and i + 1 < len(paras):
            q = paras[i + 1]
            if _plainp(q) and not _wholebold(q): out.append(FB.BLANK())
    return out

def apply(body):
    paras = PTAG.findall(body)
    paras = _split_greeting(paras)
    paras = _blank_around(paras, _is_greeting)
    paras = _intro_gaps(paras)
    paras = _box_summary(paras)
    paras = _blank_after_box(paras)
    paras = _move_order(paras)
    paras = _items_blank(paras)
    paras = _bold_guide(paras)
    paras = _engage_emoji(paras)
    paras = _dividers(paras)
    paras = _after_heading_blank(paras)
    paras = _paragraph_gaps(paras)
    paras = _sublabel_blank(paras)
    paras = _dedupe_blanks(paras)
    paras = _no_blank_after_image(paras)
    paras = _no_blank_before_image(paras)
    return _small_images("".join(paras).replace(HR, HR_HTML))
