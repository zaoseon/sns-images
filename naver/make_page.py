"""네이버 원고 복사용 페이지 만들기 (zaoseon-site public/naver/). 9/30 대표 요청 반영:
- 순서: 제목 → 본문 전체 복사(+본문) → CTA 배너 링크 → 태그(하나씩 복사) → 예약 발행일(24시 표기 "21시 00분")
- 본문 줄바꿈: 문장마다 한 줄, 문단 사이 빈 줄 한 칸, 소제목 앞 빈 줄
- 발행(예약) 끝난 글은 목록과 파일에서 뺀다 (pages.json 의 done)
사용: from make_page import page_from_html, write_index
"""
import re, sys, urllib.parse, html, json, os, datetime as D
import format_body as FB
import format_v2 as V2

def saved_urls():
    """앱에서 저장한 글 주소(+발행 기록)를 사이트 저장소 data/naver_urls.json에서 읽는다(30분마다 앱 자료 갱신 때 같이 갱신). {글 id: 주소}"""
    try:
        u = json.load(open(f"{SITE}/data/naver_urls.json", encoding="utf-8")); items = u.get("items", u) if isinstance(u, dict) else u
        return {x["id"]: x["url"] for x in items if isinstance(x, dict) and x.get("url")}
    except Exception: return {}

_CONTENT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "content")
_RAW = "https://raw.githubusercontent.com/zaoseon/sns-images/main/clips_reel/"
def _jload(name, default):
    try: return json.load(open(os.path.join(_CONTENT, name), encoding="utf-8"))
    except Exception: return default
def app_clips_for(pid, title, clips):
    """(10/14 D-241 · 앱 요청 mv7q2y49) 지금 블로그 '내 클립'에서 고를 수 있는 클립 = 블로그 앱으로 올린 클립(content/blog_app_clips.json).
    일간 클립은 이 글의 clips 목록에 있을 때, 주제 클립은 제목 낱말이 맞거나 그 클립이 나온 글일 때. [(이름, 덧붙임)]"""
    ba = _jload("blog_app_clips.json", {}); out = []
    for c in ba.get("clips", []):
        if c.get("match") == "ilgan" and c["label"] in (clips or []): out.append((c["label"], ""))
    for c in ba.get("clips", []):
        if c.get("match") != "keywords": continue
        if c.get("from_post") == pid: out.append((c["label"], "이 글에서 만든 클립이에요"))
        elif any(k in (title or "") for k in c.get("keywords", [])): out.append((c["label"], c.get("note", "")))
    return out
def new_clips_for(pid):
    """이 글 릴스를 클립용으로 바꾼 것(content/clips_from_reels.json 의 blog 짝). 이미 블로그 앱으로 올린 것(same_as)은 뺀다."""
    done = {c.get("same_as") for c in _jload("blog_app_clips.json", {}).get("clips", [])}
    out = []
    for c in _jload("clips_from_reels.json", {}).get("clips", []):
        if c.get("blog") != pid or c["id"] in done: continue
        try:
            import subprocess; mp4 = os.path.join(_CONTENT, "..", "clips_reel", c["id"] + ".mp4")
            dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", mp4]))
        except Exception: dur = None
        out.append({"id": c["id"], "name": re.sub(r"\s*\n\s*", " ", c["hook"]).replace("*", ""), "date": D.date.fromisoformat(c["upload"]).strftime("%-m/%-d"), "dur": dur})
    return out
def clip_box_html(pid, title, clips):
    """3-1 칸: (가) 지금 '내 클립'에서 고를 수 있는 것 (나) 새로 올릴 클립(블로그 앱으로 올린 뒤 글 수정해서 넣기). 둘 다 없으면 칸을 안 만든다."""
    have, new = app_clips_for(pid, title, clips), new_clips_for(pid)
    if not (have or new): return ""
    ba = _jload("blog_app_clips.json", {}); n = len(ba.get("clips", []))
    V = '<p class="val" style="font-size:20px;font-weight:700;margin:6px 0">'; S = ' <span style="font-size:16px;font-weight:400;color:#8a6d3b">· '
    h = ('<div class="box"><p class="lab">3-1. 본문에 클립 넣기 (글쓰기 화면 위쪽 \'클립\' 버튼 → 내 클립)</p>'
         f'<p class="hint">자리: 결론 요약 박스와 이미지 아래, \'이 글의 순서\' 위. <b>지금 블로그 \'내 클립\'에서 고를 수 있는 것</b>(블로그 앱으로 올린 {n}개: {html.escape(ba.get("summary", ""))}) '
         + ('중 이 글에 맞는 것:</p>' if have else '중에는 이 글에 맞는 것이 없어요.</p>'))
    i = 0
    for name, note in have:
        i += 1; h += f'{V}{i}. {html.escape(name, quote=False)}' + (f'{S}{html.escape(note, quote=False)}</span>' if note else '') + '</p>'
    if new:
        h += ('<p class="hint"><b>새로 올릴 클립(이 글 릴스를 클립용으로 바꾼 것)</b>: 영상을 폰에 저장한 뒤 <b>네이버 블로그 앱</b> → 글쓰기 대신 클립 만들기로 올리세요. '
              '클립 앱·클립 홈에서 올리면 블로그 \'내 클립\'에 안 보여요. 올린 다음 이 글을 수정해서 위 자리에 넣으면 돼요. 설명 글은 아래 버튼으로 받아 붙여 넣으세요.</p>')
        for c in new:
            i += 1; meta = f'올릴 날 {c["date"]}' + (f' · {c["dur"]:.1f}초' if c["dur"] else '') + ' · 소리 없음'
            h += (f'{V}{i}. {html.escape(c["name"], quote=False)}{S}{meta}</span></p>'
                  f'<a href="{_RAW}{c["id"]}.mp4" target="_blank" rel="noopener"><button>클립 영상 열기(저장)</button></a> '
                  f'<a href="{_RAW}desc/{c["id"]}.txt" target="_blank" rel="noopener"><button>설명 글 열기</button></a>')
    note = ba.get("page_notes", {}).get(pid)
    if note: h += f'<p class="hint">{html.escape(note, quote=False)}</p>'
    return h + '</div>'
SITE = os.environ.get("SITE", "/home/claude/zaoseon-site")
CTA_BASE = "https://zaoseon.com/?utm_source=naver&utm_medium=cta"
CTA_LINK = CTA_BASE + "#free"
CAT_LIST = ["2027 신년운세", "띠별 운세", "주간 기운", "절기 이야기", "태어난 날(일주) 이야기", "운명학 입문", "자오선 소식"]
CATS = {"n01": "2027 신년운세", "n02": "띠별 운세", "n03": "띠별 운세", "n04": "띠별 운세", "n05": "띠별 운세", "n06": "띠별 운세", "n07": "태어난 날(일주) 이야기",
        "n08": "띠별 운세", "n09": "띠별 운세", "n10": "띠별 운세", "n11": "자오선 소식", "n12": "절기 이야기", "n13": "운명학 입문", "n14": "2027 신년운세", "n15": "운명학 입문",
        "s10": "절기 이야기", **{f"n{i}": "태어난 날(일주) 이야기" for i in range(16, 26)}}   # 새 글은 add(..., category=) 로 지정하거나 여기에 추가
W = "월화수목금토일"
def when_text(dt):  # dt: datetime
    return f"{dt.year}년 {dt.month}월 {dt.day}일 ({W[dt.weekday()]}) {dt.hour}시 {dt.minute:02d}분"
SENT = re.compile(r'(?<=[가-힣\)"\'’”][.?!])\s+(?=\S)')
def blocks_from_html(body):
    """기존 원고 HTML(<p>..<br>..</p>, 소제목 span 22px) → 블록 목록"""
    out = []
    for m in re.finditer(r'<p>(.*?)</p>', body, re.S):
        inner = m.group(1).strip()
        if inner in ("&nbsp;", ""): continue
        if 'font-size:22px' in inner:
            out.append(("h", re.sub(r'<[^>]+>', '', inner))); continue
        if inner.startswith("<img"):
            out.append(("img", inner)); continue
        lines = []
        for part in re.split(r'<br\s*/?>', inner):
            # 문장마다 줄을 나누되 굵게 표시는 유지
            for s in SENT.split(part.strip()):
                if s.strip(): lines.append(s.strip())
        out.append(("p", lines))
    return out
def body_html(blocks):
    h, first = [], True
    for kind, v in blocks:
        if kind == "h":
            h.append('<p>&nbsp;</p>'); h.append(f'<p><b>{v}</b></p>')
        elif kind == "img":
            if "naver_cta" in v: v = f'<a href="{CTA_LINK}">{v}</a>'  # 붙여 넣을 때 링크가 같이 가는지 시험(9/30)
            h.append(f'<p>{v}</p>')
        else:
            if not first and h and not h[-1].startswith('<p><b>'): h.append('<p>&nbsp;</p>')
            h += [f'<p>{l}</p>' for l in v]
        first = False
    return "".join(h)
CSS = '''body{margin:0;background:#f4f1ea;color:#222;font:19px/1.7 -apple-system,"Apple SD Gothic Neo","Noto Sans KR",sans-serif}
.wrap{max-width:820px;margin:0 auto;padding:20px 16px 80px}.box{background:#fff;border:1px solid #ddd;border-radius:12px;padding:14px 16px;margin:0 0 12px}
.lab{font-size:16px;color:#8a6d3b;font-weight:700;margin:0 0 6px}.val{margin:0;white-space:pre-wrap;word-break:break-all;font-size:24px;font-weight:700;line-height:1.45}#t{font-size:28px}
button{font:inherit;font-size:18px;font-weight:700;border:0;border-radius:12px;padding:12px 20px;background:#c4a062;color:#111;cursor:pointer;margin-top:8px}
button.big{width:100%;padding:18px;font-size:20px}.ok{background:#7fb07a}
#body{font-size:16px;background:#fff;border:2px dashed #c4a062;border-radius:12px;padding:18px;margin-top:10px}#body p{margin:0}#body img{max-width:100%;height:auto}
.hint{font-size:16px;color:#666}.tags{display:flex;flex-wrap:wrap;gap:8px;margin-top:6px}
.tag{background:#f4efe4;color:#222;border:1px solid #c4a062;border-radius:999px;padding:10px 16px;font-size:17px;font-weight:600;margin:0}.tag.ok{background:#7fb07a;border-color:#7fb07a;color:#111}.tag.ok::after{content:" ✓"}'''
JS = '''function cp(id,b){navigator.clipboard.writeText(document.getElementById(id).innerText).then(function(){b.textContent="복사됨";b.className="ok"})}
function cpt(b){navigator.clipboard.writeText(b.dataset.t).then(function(){b.className="tag ok"})}
function cpb(b){var el=document.getElementById("body");var h=el.innerHTML,t=el.innerText;function done(){b.textContent="본문 복사됨 · 네이버 본문에 붙여 넣으세요";b.className="big ok"}
 function sel(){var r=document.createRange();r.selectNodeContents(el);var s=getSelection();s.removeAllRanges();s.addRange(r);document.execCommand("copy");done()}
 if(window.ClipboardItem){navigator.clipboard.write([new ClipboardItem({"text/html":new Blob([h],{type:"text/html"}),"text/plain":new Blob([t],{type:"text/plain"})})]).then(done,sel)}else sel()}'''
_CM = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "category_map.json"), encoding="utf-8"))
def new_cat(pid, cat):
    """10/12 메뉴 개편: 글 번호별 지정 → 옛 이름 바꾸기 순서로 새 메뉴 이름을 준다."""
    if pid in _CM["by_id"]: return _CM["by_id"][pid]
    return _CM["rename"].get(cat, cat) if cat else cat

_PSY = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "psy_map.json"), encoding="utf-8"))
def apply_psy(pid, title, tags, body):
    """10/12 심리 키워드 반영: psy_map.json에 있는 글이면 제목·태그를 바꾸고 '이번에 해 볼 것' 앞에 '심리학으로 읽으면' 단락을 넣는다(두 번 넣지 않음)."""
    m = _PSY.get(pid)
    if not m: return title, tags, body
    tags = _brand_tag((m.get("tags_front", []) + [t for t in tags if t not in m.get("tags_front", [])])[:10])   # 10/12: 앞 태그가 늘어도 '자오선'은 남긴다
    if "심리학으로 읽으면" not in body:
        blk = '<p>&nbsp;</p><p>🧠 <b>심리학으로 읽으면</b></p>' + "".join(f"<p>{l}</p>" for l in m["block"])
        mm = re.search(r'<p>&nbsp;</p><p><b>\d+\. 이번에 해 볼 것</b></p>', body)
        body = body[:mm.start()] + blk + body[mm.start():] if mm else body
    return m.get("title", title), tags, body

def _brand_tag(tags):
    """10/12: 태그 10개 안에 '자오선'이 꼭 있게 한다(정본: 블로그 태그는 '자오선'만 고정). 없으면 맨 뒤 태그를 '자오선'으로 바꾼다."""
    tags = list(tags)[:10]
    if "자오선" not in tags: tags = (tags[:9] + ["자오선"]) if len(tags) >= 10 else tags + ["자오선"]
    return tags

_AUXSTART = re.compile(r"^(싶|있|않|못|수$|줄$|보|주$|주고|지$|것$|거$)")
def _mbreak(text, limit=17.6):
    """코칭 블록 문장을 모바일 의미 단위 줄로 직접 끊는다(<br>로 이은 문자열). format_body의 DP를 쓰되 '하고 | 싶은'·'할 | 수 있는'처럼
    보조 낱말 앞에서는 끊지 않는다. 문장마다 줄을 새로 시작한다."""
    out = []
    for sent in re.split(r"(?<=[.!?])\s+", text.strip()):
        toks = FB.tokenize(sent)
        if not toks: continue
        if FB.width(sent) <= limit: out.append(sent); continue
        orig = FB.bpen
        def bp(tok, k, _t=toks, _o=orig):
            v = _o(tok, k)
            if k + 1 < len(_t) and _AUXSTART.match(_t[k + 1]["p"].strip()): v += 12
            return v
        FB.bpen = bp
        try: spans = FB._dp(toks, 0, len(toks) - 1, limit)
        finally: FB.bpen = orig
        out.append("<br>".join(FB._line(toks, i, j) for i, j in spans))
    return "<br>".join(out)

def apply_coaching(pid, title, tags, body):
    """10/12 대표: 아직 안 올린 원고마다 '마음 코치 정월의 질문' 블록(질문 2~3개 + 이번 주에 해 볼 것 하나)을 'N. 자주 묻는 질문' 앞에 넣고,
    제목 40자·말투 고침(coaching_data.py)을 적용한다. 두 번 넣지 않는다(이미 '이번 주에 해 볼 것 하나'가 있으면 그대로)."""
    try: import coaching_data as CD
    except Exception: return title, _brand_tag(tags), body
    for old, new in CD.REPLACE.get(pid, []):
        if old in body: body = body.replace(old, new)   # 이미 고쳐진 원고면 건너뜀
    if pid in CD.COACH and "이번 주에 해 볼 것 하나" not in body:
        lead, qs, do = CD.COACH[pid]
        blk = ('<p>&nbsp;</p><p>🌱 <b>마음 코치 정월의 질문</b></p>' + f'<p>{_mbreak(lead)}</p>' + "".join(f'<p>{_mbreak("🔸 " + q)}</p>' for q in qs)
               + f'<p>&nbsp;</p><p>✔️ <b>이번 주에 해 볼 것 하나</b>: {_mbreak(do, 16.8)}</p>')
        ms = list(re.finditer(r'<p>&nbsp;</p><p><b>\d+\. (?:자주|궁금)[^<]*</b></p>', body))
        if not ms: raise ValueError(f"{pid}: FAQ 소제목을 못 찾아 코칭 블록을 넣을 자리가 없어요")
        body = body[:ms[-1].start()] + blk + body[ms[-1].start():]
    return CD.TITLES.get(pid, title), _brand_tag(tags), body

_CARDS = None
def _cards():
    """zaoseon-site data/naver_related_cards.json: 발행 글에 지금 달린 링크 카드(서브 노트북 card_list.mjs가 공개 글을 읽어 만든다).
    {"items": {"n20": [{"url": "...", "title": "..."}, ...]}}"""
    global _CARDS
    if _CARDS is None:
        try: _CARDS = json.load(open(f"{SITE}/data/naver_related_cards.json", encoding="utf-8")).get("items", {})
        except Exception: _CARDS = {}
    return _CARDS
try: _PLANNED = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "planned_cards.json"), encoding="utf-8")).get("items", {})
except Exception: _PLANNED = {}
def _nu(u): return re.sub(r"[?#].*$", "", (u or "").strip()).rstrip("/").replace("m.blog.naver.com", "blog.naver.com")
def related_cards(pid, body, ru):
    """10/16 서브 노트북 보고: 발행 글 수정은 본문을 통째로 바꾸므로, 원고에 카드 자리가 모자라면 이미 달린 카드가 사라진다(n12·n13).
    지금 달린 카드마다 원고에 <!--LINKCARD--> 자리를 둔다. 기본 연결글(ru) 카드는 그 제목 줄 바로 뒤, 나머지는 '👇 안내 + 제목 링크 줄' 다음.
    발행 키트(get_post.mjs)는 자리마다 바로 앞 제목 줄의 주소로 카드를 넣는다."""
    cards = list(_cards().get(pid) or [])
    # 10/17 옛 발행글 4편(n01·n02·n03·s10): 새로 쓴 원고에 더할 카드(지금 공개 글엔 아직 없음, naver/planned_cards.json). 수정 발행 뒤 card_list.mjs 가 실제 카드로 적는다
    for c_ in _PLANNED.get(pid, []):
        if _nu(c_.get("url")) not in {_nu(x.get("url")) for x in cards}: cards.append(c_)
    if not cards or "<!--LINKCARD-->" in body: return body
    import html as _h
    try: titles = {_nu(x.get("url")): x.get("title", "") for x in json.load(open(f"{SITE}/data/naver_urls.json", encoding="utf-8"))["items"] if x.get("url")}
    except Exception: titles = {}
    nru = _nu(ru); extra = []; at = None
    for c in cards:
        u = _nu(c.get("url"))
        if not u: continue
        if u == nru and at is None:
            m = re.search(r'<p[^>]*>(?:(?!</p>).)*href="' + re.escape(_h.escape(ru, quote=True)) + r'"(?:(?!</p>).)*</p>', body, re.S) or \
                re.search(r'<p[^>]*>(?:(?!</p>).)*href="' + re.escape(ru) + r'"(?:(?!</p>).)*</p>', body, re.S)
            if m: body = body[:m.end()] + "<!--LINKCARD-->" + body[m.end():]; at = m.end() + len("<!--LINKCARD-->"); continue
        extra.append((c.get("url").strip(), (c.get("title") or titles.get(u) or "").strip(), c.get("kind") or "글"))
    if extra:
        blk = ""
        for u, t, kind in extra:   # 클립 카드(kind=클립)는 블로그 글이 아니다: 그 주소 그대로 카드 자리만(서브 노트북 10/16)
            t = t.split(", ")[0].strip() or ("자오선 클립" if kind == "클립" else "함께 볼 글")
            if kind == "클립":   # 클립 제목 칸은 설명 전체가 들어 있다 → 앞 몇 낱말(한 줄)만 + ' 클립'
                w_, out_ = t.split(), ""
                for x_ in w_:
                    if len(out_) + len(x_) > 11: break
                    out_ = (out_ + " " + x_).strip()
                t = (out_ or t[:11]) + " 클립"
            lead = "👇 영상으로도 볼 수 있어요." if kind == "클립" else "👇 이 글도 같이 읽어 보세요."
            # 10/17 대표: 유도 문구 한 줄만, 글 제목 줄은 쓰지 않는다(카드에 제목이 나온다). 주소는 유도 문구 줄의 링크로(키트가 이 주소로 카드를 만든다)
            blk += FB.BLANK() + FB.P('<a href="' + _h.escape(u, quote=True) + '">' + lead + "</a>") + "<!--LINKCARD-->"
        if at is None:   # 기본 연결글 카드가 없으면 CTA 배너 앞(없으면 끝)
            m = re.search(r'<p[^>]*>(?:(?!</p>).)*naver_cta\d', body, re.S); at = m.start() if m else len(body)
        body = body[:at] + blk + body[at:]
    return body

def cta_last(body):
    """CTA 배너 문단 뒤에 링크 카드 자리가 있으면 배너를 본문 맨 끝으로 옮긴다(맞은 꼴: … 카드 > CTA)."""
    m = re.search(r'<p[^>]*>(?:(?!</p>).)*naver_cta\d(?:(?!</p>).)*</p>', body, re.S)
    if not m or "<!--LINKCARD-->" not in body[m.end():]: return body
    return body[:m.start()] + body[m.end():] + m.group(0)

def _own(pid, name):
    """10/18 대표: 글마다 주제에 맞는 CTA 배너. naver/cta_banner10.py 가 그린 naver_cta12_<글번호>_<판>.jpg 가 있으면 그것을 쓴다."""
    try: ver = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "cta_copy.json"), encoding="utf-8"))["posts"].get(pid, {}).get("ver", 12)
    except Exception: ver = 12
    own = name.replace("naver_cta9_", f"naver_cta{ver}_{pid}_")
    return own if os.path.exists(os.path.join(IMG_DIR, own)) else name

def cta_pick(pid, cover, body):
    """10/17 15:05 대표 "색 다른 5세트를 만들어 놓고 원고 내부 이미지 톤에 맞게 바꿔서 적용".
    본문 이미지(없으면 표지)의 평균 색을 재서, 5세트(naver/cta_banner6.SET) 중 바탕색이 가장 가까운 판의 배너 이름을 돌려준다.
    pages.json 글에 "cta_pal" 이 있으면 그것을 쓴다(손으로 고를 때)."""
    import json as _j
    from PIL import Image as _I
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import cta_banner6 as _C
    reg = load(); want = (reg.get(pid) or {}).get("cta_pal")
    if want in _C.SET: return _own(pid, _C.set_name(want))
    pals = {k: {"bg": _C.roles(k)["bg"]} for k in _C.SET}   # 9판: 대표 자료의 실제 색(역할)에서 바탕색
    hx = lambda h: tuple(int(h.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4))
    files = [m for m in re.findall(r"naver/img/(?:m\d+/)?([^\"'?]+\.(?:jpg|png))", body) if "naver_cta" not in m][:6]
    if cover: files.append(cover)
    cols = []
    for f in files:
        f = urllib.parse.unquote(f); fp = os.path.join(IMG_DIR, f)
        if os.path.exists(fp):
            try: cols.append(_I.open(fp).convert("RGB").resize((1, 1), _I.BOX).getpixel((0, 0)))
            except Exception: pass
    if not cols: return _own(pid, _C.set_name(_C.SET[0]))
    avg = tuple(sum(c[i] for c in cols) / len(cols) for i in range(3))
    best = min(_C.SET, key=lambda k: sum((a - b) ** 2 for a, b in zip(avg, hx(pals[k]["bg"]))))
    return _own(pid, _C.set_name(best))

def write_page(pid, dt, title, tags, body, nxt=None, cover=None, related=None, category=None, thumbs=None, cid=None, clips=None, reserve=None, v2=True):
    if cover:   # 10/16: 원고 페이지는 대표 이미지를 사이트 사본(/naver/img/...)에서 읽는다 — 새 표지(_a3)를 만들고 사본을 안 둬서 안 보였다
        import shutil; dst = f"{SITE}/public/naver/img/{cover}"; src = os.path.join(IMG_DIR, cover)
        if os.path.exists(src) and not os.path.exists(dst): os.makedirs(os.path.dirname(dst), exist_ok=True); shutil.copy(src, dst)
    global CTA_LINK
    CTA_LINK = CTA_BASE + "&utm_campaign=" + pid + "#free"   # 10/18 대표: 글별 사이트 방문 재기(GoatCounter). 보이는 글은 그대로
    tags = tags[:10]  # 9/30: 태그 10개까지(예약 시간 줄이기)
    body = re.sub(r"naver_cta[2-8]_[^\"'<>\s]+?\.jpg", cta_pick(pid, cover, body), body)   # 10/17 15:05 대표: 색 5세트 중 본문 이미지 톤에 맞는 배너(cta_pick). 옛 파일은 발행 글이 쓰므로 그대로 둔다   # 10/17 14:58 대표 "배너가 그냥 봐도 크다" → 6판 1280x240(글줄 옆 단추, naver/cta_banner6.py). 옛 파일은 발행 글이 쓰므로 그대로 둔다
    body = re.sub(r"<p>\s*(?:&nbsp;\s*)?이 글은 재미로[^<]*</p>", "", body)   # 10/17 K-128 대표: '재미로' 면책 문장은 넣지 않는다. 발행글은 다른 이유로 고칠 때 같이 뺀다(지금 서브 노트북 수정 발행 중)   # 10/17 대표: 1280x400 배너(naver/cta_banner.py, 제목 57px·부제 50px 이상). 옛 cta4(10/4 2/3 크기)는 폰에서 글자 8px라 바꿈. 옛 파일은 발행 글이 쓰므로 그대로 둔다
    _mids = []   # 10/16 K-017 글 중간 입력칸 모양 상자(<table>): 서식 단계들이 <p>만 다루므로 자리표로 비켜 두었다가 끝에 되돌린다
    body = re.sub(r"<table\b.*?</table>", lambda m_: (_mids.append(m_.group(0)), f"<p>MIDBOX{len(_mids) - 1}</p>")[1], body, flags=re.S)
    body = FB.format_body(body)   # 10/4: 가운데 정렬 · 본문 16px · 제목 19px · 짧은 줄바꿈(네이버에 붙이면 바로 이 모양)
    if v2: body = V2.apply(body)   # 10/5 서식 2판(대표 요청 6가지): 인사말 줄 나눔·요약 박스·순서 위치·구분선·항목 빈 줄·작은 이미지. 10/5 대표 확인 뒤 기본으로 켬(v2=False를 주면 옛 서식)
    chips = "".join(f'<button class="tag" data-t="{html.escape(t)}" onclick="cpt(this)">{html.escape(t)}</button>' for t in tags)
    nav = f'<a href="/naver/{nxt}.html"><button class="big">다음 원고 →</button></a>' if nxt else '<a href="/naver/"><button class="big">목록으로 (마지막 원고)</button></a>'
    cover_box = (f'<div class="box"><p class="lab">2. 대표 이미지: 먼저 저장 → 네이버 글쓰기 맨 위에 사진으로 올리기(처음 올린 사진이 대표가 돼요) → 그다음 아래 본문 복사</p>'
                 f'<img src="/naver/img/{cover}?v=b4" style="width:100%;border-radius:8px" alt=""><a href="/naver/img/{cover}?v=b4" download="{os.path.basename(cover)}"><button>대표 이미지 저장</button></a></div>') if cover else ""
    _ru = (saved_urls().get((related or {}).get("id")) or (related or {}).get("url") or "") if related else ""   # 앱에 저장된 주소가 우선, 없으면 발행 기록의 주소
    if v2 and _ru: body = V2.link_guide(body, _ru)   # 본문의 연결 글 제목 줄에 링크(복사하면 같이 감)
    body = FB.fit_mobile(body)   # 10/15 대표 폰 캡처: 실제 한 줄 폭(본문 약 15.7자·소제목 약 13.4자)을 넘는 줄을 다시 나눈다
    body = re.sub(r"<p[^>]*>(?:<span[^>]*>)?MIDBOX(\d+)(?:</span>)?</p>", lambda m_: _mids[int(m_.group(1))] + "<p>&nbsp;</p>", body)
    body = related_cards(pid, body, _ru)   # 10/16 발행 글에 달린 링크 카드 수만큼 원고에도(카드를 잃지 않게)
    body = cta_last(body)   # 10/17 서브 노트북 점검: CTA 배너는 링크 카드 뒤, 본문 맨 끝(원본은 naver/tail_order.py 로 고침, 여기는 안전장치)
    if related and (related.get("url") or related.get("title") or _ru):
        _u = _ru
        rel_box = (f'<div class="box"><p class="lab">4. 함께 볼 글(내부 링크): 글 주소가 앱에 저장돼 있으면 본문 맨 아래 👇 유도 문구 줄에 링크가 자동으로 걸려요. 글 제목 줄은 쓰지 않아요. 링크 카드는 유도 문구 다음 줄에 주소를 붙여 넣고 엔터 → 카드가 생기면 주소 줄은 지워요</p>'
                   f'<p class="val" style="font-size:20px;font-weight:700" id="rt">{html.escape(related.get("title") or "")}</p><button onclick="cp(\'rt\',this)">글 제목 복사</button>'
                   + (f'<p class="val" id="rl" style="margin-top:10px">{html.escape(_u)}</p><button onclick="cp(\'rl\',this)">글 주소 복사</button>' if _u else
                      '<p class="hint">주소는 네이버 블로그 글 관리에서 이 제목의 글 → 공유 → URL 복사. 상황판 원고 카드에 발행 주소를 적어 두면 다음부터 여기에 자동으로 나와요.</p>')
                   + f'<p class="hint">유도 문구(본문에 이미 들어 있음): {html.escape(related["phrase"])}</p></div>')
    else: rel_box = ""
    reserve_box = ("" if not reserve else '<div class="box" style="background:#fff8e6;border-color:#e6d3a0"><p class="lab">📅 예약은 이때부터 걸어요</p>'
                   f'<p class="val" style="font-size:21px;font-weight:700">{html.escape(reserve["hard"])} 이후</p>'
                   '<p class="hint">함께 볼 글이 그때 발행돼 주소가 생겨요. 예약만 걸려 있는 글은 주소가 없어서 링크로 걸 수 없어요.</p>'
                   + (f'<p class="hint">본문에 클립까지 넣으려면 {html.escape(reserve["soft"])} 이후에 걸어요(그 전이면 클립은 건너뛰어도 돼요). 마감: 발행 시각 전까지.</p>' if reserve.get("needsClip") else '') + '</div>')
    clip_box = clip_box_html(pid, title, clips)   # 10/14 D-241: 블로그 앱으로 올린 클립 + 릴스 클립(blog 짝) 기준
    cat_box = (f'<div class="box"><p class="lab">6. 카테고리: 글쓰기 화면 오른쪽 카테고리에서 이 이름을 고르세요</p><p class="val" style="font-size:22px;font-weight:700">{html.escape(category)}</p></div>') if category else '<div class="box"><p class="lab">6. 카테고리</p><p class="val">미정 - 알려 주세요</p></div>'
    thumb_box = (f'<div class="box"><p class="lab">2-1. 대표 이미지 안에 넣을 문구 후보 (제목을 그대로 반복하지 말고, 클릭할 이유를 한 줄로)</p>'
                 + "".join(f'<p class="val" style="font-size:22px;font-weight:700;margin:6px 0">{i+1}. {html.escape(t)}</p>' for i, t in enumerate(thumbs)) + '</div>') if thumbs else ""
    cid_box = (f'<div class="box"><p class="lab">콘텐츠 ID (클립·측정에서 이 글을 가리키는 이름)</p><p class="val" style="font-size:20px;font-weight:700">{html.escape(cid)}</p></div>') if cid else ""
    check_box = ('<div class="box"><p class="lab">9. 올리기 전 확인 (SOP 체크리스트)</p><ul style="font-size:19px;line-height:1.8;margin:6px 0 0;padding-left:22px">'
                 '<li>한 가지 질문만 다뤘나요?</li><li>첫 150자 안에 결론이 있나요?</li><li>제목에 검색어와 얻는 것이 보이나요?</li>'
                 '<li>대표 이미지 문구가 제목과 다른 말인가요?</li><li>태그가 글 내용과 맞고 "인기·추천·일상" 같은 말이 없나요?</li>'
                 '<li>맨 아래에 다음 행동(배너·함께 볼 글)이 하나로 보이나요?</li><li>클립 칸이 있는 글이면 클립을 넣었나요? 함께 볼 글 링크 카드가 붙었나요?</li></ul></div>')
    page = f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>네이버 원고 · {html.escape(title)}</title><style>{CSS}</style><link rel="stylesheet" href="/naver/m.css?v=3"></head><body><div class="wrap">
<p class="hint"><a href="/naver/">← 네이버 원고 목록</a></p>
{reserve_box}
<div class="box"><p class="lab">1. 제목</p><p class="val" id="t">{html.escape(title)}</p><button onclick="cp('t',this)">제목 복사</button></div>
{cover_box}
{thumb_box}
<div class="box"><p class="lab">3. 본문 (이미지 포함) - 대표 이미지를 먼저 올린 뒤 그 아래에 붙여 넣으세요</p><button class="big" onclick="cpb(this)">본문 전체 복사</button><p class="hint">버튼이 안 되면 아래 점선 상자 안을 처음부터 끝까지 드래그해서 복사하세요.</p><div id="body">{body}</div></div>
{clip_box}
{rel_box}
<div class="box"><p class="lab">5. CTA 배너 링크: 맨 아래 배너 이미지를 누르고 링크 버튼으로 걸기</p><p class="val" id="c">{html.escape(CTA_LINK)}</p><button onclick="cp('c',this)">링크 복사</button></div>
{cat_box}
<div class="box"><p class="lab">7. 태그 {len(tags)}개 · 하나씩 눌러 복사 → 태그 칸에 붙여 넣고 엔터</p><div class="tags">{chips}</div></div>
<div class="box"><p class="lab">8. 예약 발행일</p><p class="val" style="font-size:20px;font-weight:700">{when_text(dt)}</p></div>
{cid_box}
{check_box}
{nav}</div><script>{JS}</script><script src="/naver/m.js?v=1" defer></script></body></html>'''
    open(f"{SITE}/public/naver/{pid}.html", "w").write(page)
REG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pages.json")
def load(): return json.load(open(REG)) if os.path.exists(REG) else {}
IMG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img")
PUB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "published.json")  # 발행된 네이버 글 주소 {"id": {"title","url","date"}}
def add(pid, dt, title, tags, body_blocks, related=None, category=None, thumbs=None, cid=None, clips=None):
    """related = {"id": 발행된 글 id, "phrase": 클릭 유도 문구}. 유도 문구는 본문 끝(CTA 배너 앞)에 넣는다"""
    """첫 이미지(대표 이미지)는 본문 복사에서 빼고 따로 내려받게 한다(9/30: 붙여 넣은 이미지는 대표로 못 고름)"""
    reg = load(); cover = None
    for i, (k, v) in enumerate(body_blocks):
        if k == "img" and "naver_cta" not in v:
            m = re.search(r'alt="([^"]+)"', v) or re.search(r'/([^/"?]+\.jpg)', v)
            cover = html.unescape(m.group(1)); body_blocks = body_blocks[:i] + body_blocks[i+1:]; break
    if cover:
        import shutil; os.makedirs(f"{SITE}/public/naver/img", exist_ok=True)
        shutil.copy(os.path.join(IMG_DIR, cover), f"{SITE}/public/naver/img/{cover}")
    ctas = [b for b in body_blocks if b[0] == "img" and "naver_cta" in b[1]]   # 10/1: CTA 배너는 항상 맨 마지막
    body_blocks = [b for b in body_blocks if not (b[0] == "img" and "naver_cta" in b[1])]
    rel = None
    if related:
        pub = json.load(open(PUB)) if os.path.exists(PUB) else {}
        rel = {"id": related["id"], "title": related.get("title") or pub.get(related["id"], {}).get("title", ""), "phrase": related["phrase"], "url": pub.get(related["id"], {}).get("url", "")}
        body_blocks = body_blocks + [("p", ["<b>👇 " + related["phrase"] + "</b>"])]   # 유도 문구는 굵게
    body_blocks = body_blocks + ctas
    title, tags, _b = apply_psy(pid, title, tags, body_html(body_blocks))
    title, tags, _b = apply_coaching(pid, title, tags, _b)   # 10/12 코칭 블록·제목 40자·말투 고침
    reg[pid] = {"dt": dt.isoformat(), "title": title, "tags": tags[:10], "body": _b, "cover": cover, "related": rel, "thumbs": thumbs, "cid": cid, "clips": clips, "category": new_cat(pid, category or CATS.get(pid)), "done": False}
    json.dump(reg, open(REG, "w"), ensure_ascii=False, indent=1); render_all()
def urls_guard():
    """원고를 다시 만들기 전에 글 주소 목록(zaoseon-site data/naver_urls.json)이 비지 않았는지 잰다.
    10/17 10:18 앱 동기화가 34개를 2개로 지웠다 — 그대로 만들면 발행 글 원고의 연결글 주소 칸이 비고,
    키트는 그 글을 조용히 건너뛰어 아무도 모르게 된다(서브 노트북 10/17). 발행된 글(published.json status=published)의
    80% 밑이면 멈춘다. 일부러 넘기려면 ZS_URLS_OK=1."""
    if os.environ.get("ZS_URLS_OK") == "1": return
    try: pub = sum(1 for v in json.load(open(PUB, encoding="utf-8")).values() if v.get("status") == "published")
    except Exception: return
    n = len(saved_urls())
    if pub and n < pub * 0.8:
        raise SystemExit(f"[원고 멈춤] 글 주소 목록이 {n}개뿐이에요(발행 글 {pub}편). data/naver_urls.json 이 동기화로 지워졌을 수 있어요. "
                         f"앞 판(git log -- data/naver_urls.json)에서 되살린 뒤 다시 만드세요. 일부러 넘기려면 ZS_URLS_OK=1.")

def render_all():
    """목록에 남은 글을 발행일 순으로 다시 그린다(다음 원고 버튼 연결)"""
    urls_guard()
    reg = load(); live = sorted((v["dt"], k) for k, v in reg.items() if not v.get("done") and "body" in v)
    for i, (dt, k) in enumerate(live):
        v = reg[k]; nxt = live[i+1][1] if i+1 < len(live) else None
        write_page(k, D.datetime.fromisoformat(dt), v["title"], v["tags"], v["body"], nxt, v.get("cover"), v.get("related"), new_cat(k, v.get("category") or CATS.get(k)), v.get("thumbs"), v.get("cid"), v.get("clips"), v.get("reserve"))
    # 10/16 대표: 이미 발행·예약한 글도 AI 브리핑 기준·새 이미지로 고쳐서 서브 노트북 키트가 네이버에서 수정한다 → 고친 원고 페이지도 만든다(목록은 fix.html 따로)
    for dt, k in sorted((v["dt"], k) for k, v in reg.items() if v.get("done") and "body" in v):
        v = reg[k]
        write_page(k, D.datetime.fromisoformat(dt), v["title"], v["tags"], v["body"], None, v.get("cover"), v.get("related"), new_cat(k, v.get("category") or CATS.get(k)), v.get("thumbs"), v.get("cid"), v.get("clips"), v.get("reserve"))
    write_index(); write_fix_index()
def done(pid):
    """대표가 예약을 마친 글: 목록과 파일에서 뺀다"""
    reg = load(); reg.setdefault(pid, {})["done"] = True; json.dump(reg, open(REG, "w"), ensure_ascii=False, indent=1)
    p = f"{SITE}/public/naver/{pid}.html"
    if os.path.exists(p): os.remove(p)
    render_all()
def write_index():
    reg = load(); items = sorted((v["dt"], k, v["title"]) for k, v in reg.items() if not v.get("done"))
    rows = "".join(f'<div class="box"><p class="lab">{when_text(D.datetime.fromisoformat(dt))}</p><p class="val"><a href="/naver/{k}.html">{html.escape(t)}</a></p></div>' for dt, k, t in items) \
        or '<div class="box"><p class="val">지금 올릴 원고가 없어요. 예약을 마친 글은 목록에서 빠져요.</p></div>'
    open(f"{SITE}/public/naver/index.html", "w").write(f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>네이버 원고 목록</title><style>{CSS}</style><link rel="stylesheet" href="/naver/m.css?v=3"></head><body><div class="wrap"><h1>네이버 블로그 원고</h1><p class="hint">예약 발행일 순서예요. <a href="/naver/fix.html">이미 올린 글 · 고친 원고 보기 →</a></p>{rows}</div></body></html>')

def write_fix_index():
    """이미 네이버에 발행·예약한 글의 고친 원고 목록(10/16). 주소가 있는 글(발행)과 예약 글을 함께 보여 준다."""
    reg = load()
    try: urls = {x["id"]: x["url"] for x in json.load(open(f"{SITE}/data/naver_urls.json", encoding="utf-8"))["items"] if x.get("url")}
    except Exception: urls = {}
    items = sorted((v["dt"], k, v["title"]) for k, v in reg.items() if "body" in v and (v.get("done") or k in urls))
    rows = "".join(f'<div class="box"><p class="lab">{"발행됨" if k in urls else "예약됨"} · {when_text(D.datetime.fromisoformat(dt))}</p><p class="val"><a href="/naver/{k}.html">{html.escape(t)}</a></p></div>' for dt, k, t in items)
    open(f"{SITE}/public/naver/fix.html", "w").write(f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>고친 원고(발행·예약 글)</title><style>{CSS}</style><link rel="stylesheet" href="/naver/m.css?v=3"></head><body><div class="wrap"><h1>이미 올린 글 · 고친 원고</h1><p class="hint">이미 네이버에 발행·예약한 글을 AI 브리핑 기준과 새 이미지로 고친 원고예요. 서브 노트북 키트가 네이버에서 이 내용으로 수정해요. <a href="/naver/">올릴 원고 목록으로</a></p>{rows}</div></body></html>')

def alert_text(pids):
    """원고를 목록에 올린 뒤 캘린더 알림 설명문. ①이 Google Calendar create_event로 만든다(9/30 대표 요청)."""
    reg = load(); rows = []
    for k in sorted(pids, key=lambda k: reg[k]["dt"]):
        rows.append(f'- {when_text(D.datetime.fromisoformat(reg[k]["dt"]))} · {reg[k]["title"]}\n  https://zaoseon.com/naver/{k}.html')
    return ("새 네이버 원고가 목록에 올라왔어요. 각 페이지의 예약 발행일로 예약해 주세요.\n"
            "끝나면 대화창에 \"예약 완료\"라고만 말해 주세요. 목록과 상황판을 정리해요.\n\n"
            "원고 목록: https://zaoseon.com/naver/\n\n" + "\n".join(rows))
