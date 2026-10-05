"""format_v2(서식 2판) 시험 (10/5). pages.json의 아직 올리지 않은 원고 전부에 적용해서 규칙이 지켜지는지, 글자가 빠지거나 늘지 않았는지 본다."""
import json, re, collections, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import format_body as FB, format_v2 as V2
bad = 0
def ok(c, m):
    global bad
    print(("OK   " if c else "FAIL ") + m)
    if not c: bad += 1
pg = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "pages.json"), encoding="utf-8"))
prep = lambda b: b.replace("naver_cta2_", "naver_cta4_").replace("naver_cta3_", "naver_cta4_")
text = lambda h: re.sub(r"\s+", "", re.sub(r"<[^>]+>", "", h).replace("&nbsp;", ""))
EL = re.compile(r"<table.*?</table>|<hr[^>]*>|<p[^>]*>.*?</p>", re.S)
posts = {k: v for k, v in pg.items() if not v.get("done") and "body" in v}
res = {}
for k, v in posts.items():
    base = FB.format_body(prep(v["body"])); new = V2.apply(base); res[k] = (base, new, [V2.HR if e.startswith("<hr") else e for e in EL.findall(new)])
ok(len(posts) > 0, f"시험 대상 원고 {len(posts)}편")
lost = []
for k, (base, new, _) in res.items():
    a, b = collections.Counter(text(base)), collections.Counter(text(new)); add = b - a; allow = collections.Counter("안녕하세요,자오선의")
    if (a - b) or any(add[c] > allow[c] for c in add): lost.append(k)
ok(not lost, "글자 보존: 빠지거나 늘어난 글자 없음(짧은 인사말을 전체 인사말로 바꾼 것만 허용)" + (f" {lost[:5]}" if lost else ""))
ok(all(re.sub(r"<[^>]+>", "", n).count(V2.GREET) == 1 for _, n, _ in res.values()), "인사말(안녕하세요, 자오선의 정월이에요.)이 모든 글에 정확히 한 번")
def around_greeting(els):
    i = next(i for i, e in enumerate(els) if e != V2.HR and V2.pl(e) == V2.GREET)
    return i > 0 and V2.blank(els[i - 1]) and i + 1 < len(els) and V2.blank(els[i + 1])
ok(all(around_greeting(e) for _, _, e in res.values()), "인사말 앞뒤가 빈 줄")
ok(all(n.count("<table") == 1 for _, n, _ in res.values()), "요약 박스(1칸 표)가 모든 글에 한 개")
ok(all(re.search(r"한 줄 요약", re.search(r"<table.*?</table>", n, re.S).group(0)) for _, n, _ in res.values()), "박스 안에 한 줄 요약이 들어 있음")
def order_ok(els):
    h = next((i for i, e in enumerate(els) if e != V2.HR and V2.pl(e).startswith("📌 이 글의 순서")), None)
    if h is None: return True
    box = next(i for i, e in enumerate(els) if e.startswith("<table")); fh = next((i for i, e in enumerate(els) if V2.numhead(e)), len(els))
    im = next((i for i in range(box + 1, fh) if V2.isimg(els[i]) and not V2.iscta(els[i])), None)
    # 요약 박스 뒤에 첫 번호 제목보다 앞서는 이미지가 있으면 순서는 그 이미지 뒤, 없으면 박스 뒤
    pos_img = next((i for i in range(box + 1, fh) if V2.isimg(els[i]) and not V2.iscta(els[i])), None)
    return h > box and (pos_img is None or h > pos_img)
ok(all(order_ok(e) for _, _, e in res.values()), "📌 이 글의 순서는 요약 이미지 다음(그런 이미지가 없으면 요약 박스 다음)")
def hr_ok(els):
    heads = [i for i, e in enumerate(els) if V2.numhead(e)]
    return all(i > 0 and els[i - 1] == V2.HR for i in heads) and all(i + 1 < len(els) and V2.blank(els[i + 1]) for i in heads)
ok(all(hr_ok(e) for _, _, e in res.values()), "번호 제목마다 앞에 구분선, 뒤에 빈 줄 한 칸")
def pre_guide(els):
    g = [i for i, e in enumerate(els) if e != V2.HR and V2.pl(e).startswith("👇")]
    return all(els[i - 1] == V2.HR for i in g)
ok(all(pre_guide(e) for _, _, e in res.values()), "👇 유도 문구 앞에 구분선")
def pre_order(els):
    h = [i for i, e in enumerate(els) if e != V2.HR and V2.pl(e).startswith("📌 이 글의 순서")]
    return all(els[i - 1] == V2.HR for i in h)
ok(all(pre_order(e) for _, _, e in res.values()), "📌 이 글의 순서 앞에 구분선 한 개")
ok(all(not (els[i] == V2.HR and els[i + 1] == V2.HR) for _, _, els in res.values() for i in range(len(els) - 1)), "구분선이 연달아 나오지 않음")
ok(all(not (V2.blank(els[i]) and V2.blank(els[i + 1])) for _, _, els in res.values() for i in range(len(els) - 1)), "빈 줄이 두 칸 이상 이어지지 않음")

def box_inner(n): return re.search(r"<table.*?</table>", n, re.S).group(0)
ok(all("background:#ffffff" in box_inner(n) and "border:1px solid #cfcfcf" in box_inner(n) and 'width="%d"' % V2.IMG_W in box_inner(n) for _, n, _ in res.values()), f"박스: 흰 바탕 + 회색 윤곽선 + 이미지 폭({V2.IMG_W}px)")
ok(all("#fbf7ee" not in n and "#c4a062" not in n for _, n, _ in res.values()), "박스·구분선에 베이지 배경·금색이 없음")
def box_gaps(n):
    ps = re.findall(r"<p[^>]*>.*?</p>", box_inner(n), re.S)
    return all(V2.blank(ps[i - 1]) for i, p in enumerate(ps) if i and not V2.blank(p) and V2.emoji0(V2.pl(p)) and not V2.big(p))
ok(all(box_gaps(n) for _, n, _ in res.values()), "박스 안 한 줄 요약 / 세 풀이 / 해 볼 것 사이가 한 줄씩 띄워짐")
hrs = [t for _, n, _ in res.values() for t in re.findall(r"<hr[^>]*>", n)]
ok(hrs and all(V2.LINE_GRAY in t and 'width="%d"' % V2.LINE_W in t for t in hrs), f"구분선 {len(hrs)}개는 모두 회색({V2.LINE_GRAY}), 가운데, 폭 {V2.LINE_W}px(이미지보다 짧게)")
ok(all(re.search(r"<b>👇", p) for _, n, _ in res.values() for p in re.findall(r"<p[^>]*>(?:(?!</p>).)*👇(?:(?!</p>).)*</p>", n, re.S)), "👇 유도 문구 줄은 모두 굵게")
ok(all(len(re.findall(r"<p[^>]*>(?:(?!</p>).)*👇(?:(?!</p>).)*</p>", n, re.S)) >= 1 for _, n, _ in res.values() if "👇" in n), "👇 유도 문구가 있는 글 확인")
ok(all(not (V2.isimg(els[i]) and V2.blank(els[i + 1])) for _, _, els in res.values() for i in range(len(els) - 1)), "이미지 바로 다음에 빈 줄이 없음")
ok(all(not (els[i] == V2.HR and V2.blank(els[i + 1])) and not (V2.blank(els[i]) and els[i + 1] == V2.HR) for _, _, els in res.values() for i in range(len(els) - 1)), "구분선 앞뒤에 빈 줄이 없음")
imgs = [t for _, n, _ in res.values() for t in re.findall(r"<img[^>]*>", n)]
small = [t for t in imgs if "naver_cta" not in t]; cta = [t for t in imgs if "naver_cta" in t]
ok(all(f"/{V2.SMALL_DIR}/" in t and f'width="{V2.IMG_W}"' in t for t in small), f"본문 이미지 {len(small)}개는 모두 작은 판 주소와 width {V2.IMG_W}")
ok(all(f"/{V2.CTA_DIR}/" in t and 'width="%d"' % V2.LINE_W in t for t in cta), f"CTA 배너 {len(cta)}개는 링크 카드와 같은 폭({V2.LINE_W}px) 작은 판")
miss = []
for t in small + cta:
    m = re.search(r"/naver/img/(?:%s|%s)/([^\"?]+)" % (V2.SMALL_DIR, V2.CTA_DIR), t); n = __import__("urllib.parse", fromlist=["x"]).unquote(m.group(1))
    if not os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), "img", (V2.CTA_DIR if "naver_cta" in n else V2.SMALL_DIR), n)): miss.append(n)
ok(not miss, "작은 판 이미지 파일이 모두 있음" + (f" 없음: {miss[:3]}" if miss else ""))
body = res[next(iter(res))][1]
lk = V2.link_guide(body, "https://blog.naver.com/zaoseon/1234?a=1&b=2")
ok(lk.count('<a href="https://blog.naver.com/zaoseon/1234?a=1&amp;b=2">') == 1 and re.sub(r"<[^>]+>", "", lk) == re.sub(r"<[^>]+>", "", body), "연결 글 링크: 👇 아래 제목 줄에 한 번, 글자는 그대로, 주소의 &는 &amp;로")
ok(V2.link_guide(lk, "https://x.com/y") == lk and V2.link_guide(body, "") == body, "이미 링크가 있거나 주소가 없으면 바꾸지 않음")
print("모두 통과" if not bad else f"실패 {bad}"); sys.exit(1 if bad else 0)
