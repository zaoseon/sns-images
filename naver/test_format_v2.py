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
EL = re.compile(r"<table.*?</table>|<hr>|<p[^>]*>.*?</p>", re.S)
posts = {k: v for k, v in pg.items() if not v.get("done") and "body" in v}
res = {}
for k, v in posts.items():
    base = FB.format_body(prep(v["body"])); new = V2.apply(base); res[k] = (base, new, EL.findall(new))
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
ok(all(not (els[i] == V2.HR and els[i + 1] == V2.HR) for _, _, els in res.values() for i in range(len(els) - 1)), "구분선이 연달아 나오지 않음")
ok(all(not (V2.blank(els[i]) and V2.blank(els[i + 1])) for _, _, els in res.values() for i in range(len(els) - 1)), "빈 줄이 두 칸 이상 이어지지 않음")
imgs = [t for _, n, _ in res.values() for t in re.findall(r"<img[^>]*>", n)]
small = [t for t in imgs if "naver_cta" not in t]; cta = [t for t in imgs if "naver_cta" in t]
ok(all(f"/{V2.SMALL_DIR}/" in t and f'width="{V2.IMG_W}"' in t for t in small), f"본문 이미지 {len(small)}개는 모두 작은 판 주소와 width {V2.IMG_W}")
ok(all(f"/{V2.SMALL_DIR}/" not in t for t in cta), f"CTA 배너 {len(cta)}개는 그대로(문서 너비)")
miss = []
for t in small:
    m = re.search(r"/naver/img/%s/([^\"?]+)" % V2.SMALL_DIR, t); n = __import__("urllib.parse", fromlist=["x"]).unquote(m.group(1))
    if not os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), "img", V2.SMALL_DIR, n)): miss.append(n)
ok(not miss, "작은 판 이미지 파일이 모두 있음" + (f" 없음: {miss[:3]}" if miss else ""))
print("모두 통과" if not bad else f"실패 {bad}"); sys.exit(1 if bad else 0)
