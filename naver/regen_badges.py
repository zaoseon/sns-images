"""10/4 대표 지적(원 안에 캐릭터가 제대로 안 들어감 · 자오선 로고가 카드 선에 붙음 · 글씨가 작음) 뒤 이미지를 다시 그린다.
원인: thumb_sq.head_circle 이 머리 폭을 원의 0.72로 맞춰 턱이 원 아래에 잘렸다(0.58로 줄임). add_intro_image 카드는 로고가 아래 선에 붙고 글이 작았다.
다시 그리는 것: (1) 정사각 대표 이미지 naver_zNN_a.jpg (n26~n63) (2) 목록용 sq_*.jpg (이미 있는 것) (3) 한눈에 보기 카드 naver_zNN_i.jpg (n26~n63) (4) 위 둘의 가로 판 img/wide/*.
n47~n63 의 구도·얼굴·원소색은 build_naver_47_52/53_63.py 의 art(...) 호출에서 읽는다(빌드는 돌리지 않음 - pages.json·본문은 건드리지 않고 이미지 파일만 바꾼다).
사용: python3 naver/regen_badges.py        (끝나면 zaoseon-site public/naver/img 와 public/naver/img/wide 에 같은 이름으로 복사해야 원고 페이지·앱에서 보인다)"""
import ast, os, re, sys, json, statistics
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import thumb_sq as TQ, add_intro_image as AI
IMG = os.path.join(HERE, "img"); WIDE = os.path.join(IMG, "wide"); os.makedirs(WIDE, exist_ok=True)

def load_47_63():
    ents = {}
    for fn in ("build_naver_47_52.py", "build_naver_53_63.py"):
        tree = ast.parse(open(os.path.join(HERE, fn), encoding="utf-8").read())
        for n in ast.walk(tree):
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "art" and len(n.args) >= 7:
                g = dict(vars(TQ)); ev = lambda i: eval(compile(ast.Expression(n.args[i]), "x", "eval"), g)
                no, face, el, dark, tcfg = ev(0), ev(3), ev(4), ev(5), ev(6)
                t = dict(tcfg); t.update(el=el, face=face); TQ.T[f"n{no}"] = t; ents[no] = dark
    return ents

def edge_color(im):
    w, h = im.size; px = []
    for x in (2, w // 2, w - 3):
        for y in (2, h - 3): px.append(im.getpixel((x, y)))
    for y in (h // 2,): px += [im.getpixel((2, y)), im.getpixel((w - 3, y))]
    return tuple(int(statistics.median(p[i] for p in px)) for i in range(3))
def wide(src, name):                                   # make_wide_covers.py 와 같은 방식(가운데 720x720, 양옆은 가장자리 색)
    im = Image.open(src).convert("RGB"); can = Image.new("RGB", (1200, 720), edge_color(im))
    can.paste(im.resize((720, 720), Image.LANCZOS), (240, 0)); can.save(os.path.join(WIDE, name), quality=95)

def summary_maps(b):
    m1 = re.search(r"<b>한 줄 요약</b>:\s*(.*?)</p>", b)
    m2 = re.search(r"<b>(세 지도|두 지도)</b>:\s*(.*?)</p>", b) or re.search(r"<b>(세 가지|달력|세 지도|두 지도|[^<]{2,6})</b>:\s*(.*?)</p>", b[b.find("한 줄 요약") + 10:])
    summ = re.sub(r"<[^>]+>", " ", m1.group(1)).split("  ")[0].strip(); summ = re.sub(r"\s+", " ", summ)
    return summ, re.sub(r"<[^>]+>", "", m2.group(2)), m2.group(1)

def main():
    dark47 = load_47_63(); reg = json.load(open(os.path.join(HERE, "pages.json"), encoding="utf-8")); n_a = n_i = n_sq = 0
    for no in range(26, 64):
        pid = f"n{no}"; pre = f"naver_z{no}"
        TQ.render(pid, os.path.join(IMG, f"{pre}_a.jpg"), dark=dark47.get(no)); n_a += 1
        wide(os.path.join(IMG, f"{pre}_a.jpg"), f"{pre}_a.jpg")
        if os.path.exists(os.path.join(IMG, f"{pre}_i.jpg")):
            summ, maps, label = summary_maps(reg[pid]["body"]); AI.cfg = None
            AI.render(pid, summ, maps, os.path.join(IMG, f"{pre}_i.jpg"), label=label); n_i += 1
    for f in sorted(os.listdir(IMG)):
        m = re.fullmatch(r"sq_(.+)\.jpg", f)
        if m and m.group(1) in TQ.T:
            TQ.render(m.group(1), os.path.join(IMG, f), dark=False); wide(os.path.join(IMG, f), f); n_sq += 1
    print("정사각 대표", n_a, "· 한눈에 보기 카드", n_i, "· 목록용 sq", n_sq)
if __name__ == "__main__": main()
