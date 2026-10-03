"""네이버 원고 복사용 페이지 만들기 (zaoseon-site public/naver/). 9/30 대표 요청 반영:
- 순서: 제목 → 본문 전체 복사(+본문) → CTA 배너 링크 → 태그(하나씩 복사) → 예약 발행일(24시 표기 "21시 00분")
- 본문 줄바꿈: 문장마다 한 줄, 문단 사이 빈 줄 한 칸, 소제목 앞 빈 줄
- 발행(예약) 끝난 글은 목록과 파일에서 뺀다 (pages.json 의 done)
사용: from make_page import page_from_html, write_index
"""
import re, html, json, os, datetime as D
SITE = os.environ.get("SITE", "/home/claude/zaoseon-site")
CTA_LINK = "https://zaoseon.com/?utm_source=naver&utm_medium=cta#free"
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
CSS = '''body{margin:0;background:#f4f1ea;color:#222;font:16px/1.7 -apple-system,"Apple SD Gothic Neo","Noto Sans KR",sans-serif}
.wrap{max-width:720px;margin:0 auto;padding:20px 16px 80px}.box{background:#fff;border:1px solid #ddd;border-radius:12px;padding:14px 16px;margin:0 0 12px}
.lab{font-size:13px;color:#8a6d3b;font-weight:700;margin:0 0 4px}.val{margin:0;white-space:pre-wrap;word-break:break-all}
button{font:inherit;font-weight:700;border:0;border-radius:10px;padding:10px 16px;background:#c4a062;color:#111;cursor:pointer;margin-top:8px}
button.big{width:100%;padding:16px;font-size:18px}.ok{background:#7fb07a}
#body{background:#fff;border:2px dashed #c4a062;border-radius:12px;padding:18px;margin-top:10px}#body p{margin:0}#body img{max-width:100%;height:auto}
.hint{font-size:14px;color:#666}.tags{display:flex;flex-wrap:wrap;gap:8px;margin-top:6px}
.tag{background:#f4efe4;color:#222;border:1px solid #c4a062;border-radius:999px;padding:8px 14px;font-weight:600;margin:0}.tag.ok{background:#7fb07a;border-color:#7fb07a;color:#111}.tag.ok::after{content:" ✓"}'''
JS = '''function cp(id,b){navigator.clipboard.writeText(document.getElementById(id).innerText).then(function(){b.textContent="복사됨";b.className="ok"})}
function cpt(b){navigator.clipboard.writeText(b.dataset.t).then(function(){b.className="tag ok"})}
function cpb(b){var el=document.getElementById("body");var h=el.innerHTML,t=el.innerText;function done(){b.textContent="본문 복사됨 · 네이버 본문에 붙여 넣으세요";b.className="big ok"}
 function sel(){var r=document.createRange();r.selectNodeContents(el);var s=getSelection();s.removeAllRanges();s.addRange(r);document.execCommand("copy");done()}
 if(window.ClipboardItem){navigator.clipboard.write([new ClipboardItem({"text/html":new Blob([h],{type:"text/html"}),"text/plain":new Blob([t],{type:"text/plain"})})]).then(done,sel)}else sel()}'''
def write_page(pid, dt, title, tags, body, nxt=None, cover=None, related=None, category=None, thumbs=None, cid=None, clips=None, reserve=None):
    tags = tags[:10]  # 9/30: 태그 10개까지(예약 시간 줄이기)
    chips = "".join(f'<button class="tag" data-t="{html.escape(t)}" onclick="cpt(this)">{html.escape(t)}</button>' for t in tags)
    nav = f'<a href="/naver/{nxt}.html"><button class="big">다음 원고 →</button></a>' if nxt else '<a href="/naver/"><button class="big">목록으로 (마지막 원고)</button></a>'
    cover_box = (f'<div class="box"><p class="lab">2. 대표 이미지: 먼저 저장 → 네이버 글쓰기 맨 위에 사진으로 올리기(처음 올린 사진이 대표가 돼요) → 그다음 아래 본문 복사</p>'
                 f'<img src="/naver/img/{cover}?v=sq" style="width:100%;border-radius:8px" alt=""><a href="/naver/img/{cover}" download="{cover}"><button>대표 이미지 저장</button></a></div>') if cover else ""
    if related and (related.get("url") or related.get("title")):
        _u = related.get("url") or ""
        rel_box = (f'<div class="box"><p class="lab">4. 함께 볼 글(내부 링크): 본문 맨 아래 유도 문구 다음 줄에 이 글의 주소를 붙여 넣고 엔터 → 링크 카드</p>'
                   f'<p class="val" style="font-size:20px;font-weight:700" id="rt">{html.escape(related.get("title") or "")}</p><button onclick="cp(\'rt\',this)">글 제목 복사</button>'
                   + (f'<p class="val" id="rl" style="margin-top:10px">{html.escape(_u)}</p><button onclick="cp(\'rl\',this)">글 주소 복사</button>' if _u else
                      '<p class="hint">주소는 네이버 블로그 글 관리에서 이 제목의 글 → 공유 → URL 복사. 상황판 원고 카드에 발행 주소를 적어 두면 다음부터 여기에 자동으로 나와요.</p>')
                   + f'<p class="hint">유도 문구(본문에 이미 들어 있음): {html.escape(related["phrase"])}</p></div>')
    else: rel_box = ""
    reserve_box = ("" if not reserve else '<div class="box" style="background:#fff8e6;border-color:#e6d3a0"><p class="lab">📅 예약은 이때부터 걸어요</p>'
                   f'<p class="val" style="font-size:21px;font-weight:700">{html.escape(reserve["hard"])} 이후</p>'
                   '<p class="hint">함께 볼 글이 그때 발행돼 주소가 생겨요. 예약만 걸려 있는 글은 주소가 없어서 링크로 걸 수 없어요.</p>'
                   + (f'<p class="hint">본문에 클립까지 넣으려면 {html.escape(reserve["soft"])} 이후에 걸어요(그 전이면 클립은 건너뛰어도 돼요). 마감: 발행 시각 전까지.</p>' if reserve.get("needsClip") else '') + '</div>')
    clip_box = ("" if not clips else '<div class="box"><p class="lab">3-1. 본문에 클립 넣기 (글쓰기 화면 위쪽 \'클립\' 버튼 → 내 클립)</p><p class="hint">자리: 본문 맨 위 결론 요약 바로 아래, \'이 글의 순서\' 위. 이미 올라가 있는 클립이에요.</p>'
                + "".join(f'<p class="val" style="font-size:20px;font-weight:700;margin:6px 0">{i+1}. {html.escape(c)}</p>' for i, c in enumerate(clips)) + '</div>')
    cat_box = (f'<div class="box"><p class="lab">6. 카테고리: 글쓰기 화면 오른쪽 카테고리에서 이 이름을 고르세요</p><p class="val" style="font-size:22px;font-weight:700">{html.escape(category)}</p></div>') if category else '<div class="box"><p class="lab">6. 카테고리</p><p class="val">미정 - 알려 주세요</p></div>'
    thumb_box = (f'<div class="box"><p class="lab">2-1. 대표 이미지 안에 넣을 문구 후보 (제목을 그대로 반복하지 말고, 클릭할 이유를 한 줄로)</p>'
                 + "".join(f'<p class="val" style="font-size:22px;font-weight:700;margin:6px 0">{i+1}. {html.escape(t)}</p>' for i, t in enumerate(thumbs)) + '</div>') if thumbs else ""
    cid_box = (f'<div class="box"><p class="lab">콘텐츠 ID (클립·측정에서 이 글을 가리키는 이름)</p><p class="val" style="font-size:20px;font-weight:700">{html.escape(cid)}</p></div>') if cid else ""
    check_box = ('<div class="box"><p class="lab">9. 올리기 전 확인 (SOP 체크리스트)</p><ul style="font-size:19px;line-height:1.8;margin:6px 0 0;padding-left:22px">'
                 '<li>한 가지 질문만 다뤘나요?</li><li>첫 150자 안에 결론이 있나요?</li><li>제목에 검색어와 얻는 것이 보이나요?</li>'
                 '<li>대표 이미지 문구가 제목과 다른 말인가요?</li><li>태그가 글 내용과 맞고 "인기·추천·일상" 같은 말이 없나요?</li>'
                 '<li>맨 아래에 다음 행동(배너·함께 볼 글)이 하나로 보이나요?</li><li>클립 칸이 있는 글이면 클립을 넣었나요? 함께 볼 글 링크 카드가 붙었나요?</li></ul></div>')
    page = f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>네이버 원고 · {html.escape(title)}</title><style>{CSS}</style></head><body><div class="wrap">
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
{nav}</div><script>{JS}</script></body></html>'''
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
    reg[pid] = {"dt": dt.isoformat(), "title": title, "tags": tags[:10], "body": body_html(body_blocks), "cover": cover, "related": rel, "thumbs": thumbs, "cid": cid, "clips": clips, "category": category or CATS.get(pid), "done": False}
    json.dump(reg, open(REG, "w"), ensure_ascii=False, indent=1); render_all()
def render_all():
    """목록에 남은 글을 발행일 순으로 다시 그린다(다음 원고 버튼 연결)"""
    reg = load(); live = sorted((v["dt"], k) for k, v in reg.items() if not v.get("done") and "body" in v)
    for i, (dt, k) in enumerate(live):
        v = reg[k]; nxt = live[i+1][1] if i+1 < len(live) else None
        write_page(k, D.datetime.fromisoformat(dt), v["title"], v["tags"], v["body"], nxt, v.get("cover"), v.get("related"), v.get("category") or CATS.get(k), v.get("thumbs"), v.get("cid"), v.get("clips"), v.get("reserve"))
    write_index()
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
    open(f"{SITE}/public/naver/index.html", "w").write(f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>네이버 원고 목록</title><style>{CSS}</style></head><body><div class="wrap"><h1>네이버 블로그 원고</h1><p class="hint">예약 발행일 순서예요.</p>{rows}</div></body></html>')

def alert_text(pids):
    """원고를 목록에 올린 뒤 캘린더 알림 설명문. ①이 Google Calendar create_event로 만든다(9/30 대표 요청)."""
    reg = load(); rows = []
    for k in sorted(pids, key=lambda k: reg[k]["dt"]):
        rows.append(f'- {when_text(D.datetime.fromisoformat(reg[k]["dt"]))} · {reg[k]["title"]}\n  https://zaoseon.com/naver/{k}.html')
    return ("새 네이버 원고가 목록에 올라왔어요. 각 페이지의 예약 발행일로 예약해 주세요.\n"
            "끝나면 대화창에 \"예약 완료\"라고만 말해 주세요. 목록과 상황판을 정리해요.\n\n"
            "원고 목록: https://zaoseon.com/naver/\n\n" + "\n".join(rows))
