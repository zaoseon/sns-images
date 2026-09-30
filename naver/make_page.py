"""네이버 원고 복사용 페이지 만들기 (zaoseon-site public/naver/). 9/30 대표 요청 반영:
- 순서: 제목 → 본문 전체 복사(+본문) → CTA 배너 링크 → 태그(하나씩 복사) → 예약 발행일(24시 표기 "21시 00분")
- 본문 줄바꿈: 문장마다 한 줄, 문단 사이 빈 줄 한 칸, 소제목 앞 빈 줄
- 발행(예약) 끝난 글은 목록과 파일에서 뺀다 (pages.json 의 done)
사용: from make_page import page_from_html, write_index
"""
import re, html, json, os, datetime as D
SITE = os.environ.get("SITE", "/home/claude/zaoseon-site")
CTA_LINK = "https://zaoseon.com/?utm_source=naver&utm_medium=cta#free"
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
def write_page(pid, dt, title, tags, body):
    chips = "".join(f'<button class="tag" data-t="{html.escape(t)}" onclick="cpt(this)">{html.escape(t)}</button>' for t in tags)
    page = f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>네이버 원고 · {html.escape(title)}</title><style>{CSS}</style></head><body><div class="wrap">
<p class="hint"><a href="/naver/">← 네이버 원고 목록</a></p>
<div class="box"><p class="lab">1. 제목</p><p class="val" id="t">{html.escape(title)}</p><button onclick="cp('t',this)">제목 복사</button></div>
<div class="box"><p class="lab">2. 본문 (이미지 포함)</p><button class="big" onclick="cpb(this)">본문 전체 복사</button><p class="hint">버튼이 안 되면 아래 점선 상자 안을 처음부터 끝까지 드래그해서 복사하세요.</p><div id="body">{body}</div></div>
<div class="box"><p class="lab">3. CTA 배너 링크: 맨 아래 배너 이미지를 누르고 링크 버튼으로 걸기</p><p class="val" id="c">{html.escape(CTA_LINK)}</p><button onclick="cp('c',this)">링크 복사</button></div>
<div class="box"><p class="lab">4. 태그 {len(tags)}개 · 하나씩 눌러 복사 → 태그 칸에 붙여 넣고 엔터</p><div class="tags">{chips}</div></div>
<div class="box"><p class="lab">5. 예약 발행일</p><p class="val" style="font-size:20px;font-weight:700">{when_text(dt)}</p></div>
</div><script>{JS}</script></body></html>'''
    open(f"{SITE}/public/naver/{pid}.html", "w").write(page)
REG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pages.json")
def load(): return json.load(open(REG)) if os.path.exists(REG) else {}
def add(pid, dt, title, tags, body_blocks):
    reg = load(); write_page(pid, dt, title, tags, body_html(body_blocks))
    reg[pid] = {"dt": dt.isoformat(), "title": title, "done": False}; json.dump(reg, open(REG, "w"), ensure_ascii=False, indent=1); write_index()
def done(pid):
    """대표가 예약을 마친 글: 목록과 파일에서 뺀다"""
    reg = load(); reg.setdefault(pid, {})["done"] = True; json.dump(reg, open(REG, "w"), ensure_ascii=False, indent=1)
    p = f"{SITE}/public/naver/{pid}.html"
    if os.path.exists(p): os.remove(p)
    write_index()
def write_index():
    reg = load(); items = sorted((v["dt"], k, v["title"]) for k, v in reg.items() if not v.get("done"))
    rows = "".join(f'<div class="box"><p class="lab">{when_text(D.datetime.fromisoformat(dt))}</p><p class="val"><a href="/naver/{k}.html">{html.escape(t)}</a></p></div>' for dt, k, t in items) \
        or '<div class="box"><p class="val">지금 올릴 원고가 없어요. 예약을 마친 글은 목록에서 빠져요.</p></div>'
    open(f"{SITE}/public/naver/index.html", "w").write(f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>네이버 원고 목록</title><style>{CSS}</style></head><body><div class="wrap"><h1>네이버 블로그 원고</h1><p class="hint">예약 발행일 순서예요.</p>{rows}</div></body></html>')
