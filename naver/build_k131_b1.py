"""K-131 B1(발행 글 · 띠·시기 7편) 본문 도식 다시 그리기 (① 자동 10/17, 계획 zaoseon-site docs/네이버_본문이미지_다시그리기_계획_2026-10-17.md).
글마다 도식 2종(diagrams_k131), 그림 속 값은 그 글 본문에 적힌 값만 쓴다(띠 관계·힘 쓸 달·손없는날·절기 시각).
pages.json 본문에서 옛 설명 그림 몇 장을 도식으로 바꾸거나 소제목 아래에 넣는다. 옛 5틀은 글마다 2장 이하(n64 b4·c4 뺌).
이웃한 발행일 글의 첫 도식이 같지 않게: n02 wheel → n14 cross → n03 matrix → n08 monthgrid → n05 wheel → n10 months → n06 wheel → n12 calendar → n64 monthgrid.
사용: python3 naver/build_k131_b1.py            (그림 + pages.json 본문 고침)
      PREVIEW=폴더 python3 naver/build_k131_b1.py   (그림만 시안 폴더에, pages.json 안 고침)"""
import os, sys, re, json, html
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import body_v3 as B, diagrams_k131 as DG
RAW = "https://raw.githubusercontent.com/zaoseon/sns-images/main/naver/img/"
BL = "<p>&nbsp;</p>"
PG = os.path.join(HERE, "pages.json")
TAG = "B1 10/17"

def IMG(name, alt): return f'<p><img src="{RAW}{name}" alt="{html.escape(alt, quote=True)}"></p>' + BL

def have(n): return os.path.exists(os.path.join(HERE, "img", n))

def replace_img(body, part, new):
    pat = re.compile(r'<p><img[^>]*src="[^"]*' + re.escape(part) + r'[^"]*"[^>]*></p>(?:<p>&nbsp;</p>)?')
    body, k = pat.subn(lambda m: new, body); assert k == 1, (part, k); return body

def after_head(body, num, new):
    m = re.search(r'<p><b>' + str(num) + r'\. [^<]*</b></p>', body); assert m, num
    return body[:m.end()] + new + body[m.end():]

def before_head(body, num, new):
    m = re.search(r'<p><b>' + str(num) + r'\. [^<]*</b></p>', body); assert m, num
    k = body.rfind(BL, 0, m.start()); k = k if k >= 0 and k + len(BL) == m.start() else m.start()
    return body[:k] + new + body[k:]

def drop_line(body, text):
    body, k = re.subn(r'<p>' + re.escape(text) + r'</p>', "", body); assert k == 1, (text, k); return body

def months_grid(spec):   # spec = {월: (꼬리표, 상태)} → 2월~1월 12칸
    return [(m, *spec.get(m, ("", None))) for m in list(range(2, 13)) + [1]]

def plan():
    P = {}
    # n14 2027년 여섯 운명학으로 겹쳐 본 한 해 흐름
    P["n14"] = dict(key="14", diag={
        "X": (lambda n, c: DG.cross(n, c, "여섯 운명학이 2027년에 하는 말", ["불의 해", "하반기 실속", "말"],
              [("사주", "●●–"), ("점성술", "●●○"), ("수비학", "–––"), ("자미두수", "––○"), ("당사주", "–––"), ("하락이수", "–––")],
              note="당사주·하락이수는 사람마다 달라 이 글에선 뺐어요"),
              "2027년을 사주·점성술·수비학·자미두수·당사주·하락이수로 겹쳐 본 교차표: 불의 해와 하반기 실속은 사주와 점성술이 같은 방향, 말은 점성술과 자미두수가 서로 갈려요"),
        "N": (lambda n, c: DG.band(n, c, "2027년 한 해를 쓰는 순서", (1, 13), [(m, str(m)) for m in range(1, 13)],
              [("시작하고 알리기", 1, 7.52, "acc"), ("정리하고 점검하기", 7.84, 13, "out"), ("함께 갈 사람 한 명 (숫자 2)", 1, 13, "soft")],
              [(7.84, "7월 27일 무렵 목성이 처녀자리로")]),
              "2027년 1월부터 7월 중순까지는 시작하고 알리기, 7월 27일 무렵 목성이 처녀자리로 옮긴 뒤 12월까지는 정리하고 점검하기, 한 해 내내 함께 갈 사람 한 명을 표시한 띠그래프")},
        ops=[("rep", "naver_x13_", "X"), ("after", 5, "N")])
    # n08 2027년 토끼띠
    P["n08"] = dict(key="08", diag={
        "G": (lambda n, c: DG.monthgrid(n, c, "2027년 토끼띠 열두 달", months_grid({
              2: ("닮은 기운", None), 3: ("내 달", None), 4: ("어긋남", None), 6: ("틀어짐", None), 7: ("한 팀", "up"), 8: ("서운함", "dn"),
              9: ("부딪힘", "dn"), 10: ("짝", "up"), 11: ("세 띠 모임", "up"), 12: ("날카로움", None), 1: ("차분", None)})),
              "2027년 토끼띠 열두 달 칸: 힘을 쓸 달은 7월·10월·11월, 아낄 달은 8월·9월, 칸마다 그달의 띠와 토끼띠의 사이를 적은 그림"),
        "W": (lambda n, c: DG.wheel(n, c, "토끼(卯)와 잘 맞는 띠·조심할 띠", [(3, 11, "solid"), (3, 7, "solid"), (11, 7, "solid"), (3, 10, "thick"), (3, 9, "dash"), (3, 8, "dot"), (3, 0, "dot"), (3, 6, "dot")],
              hi={11, 7, 10}, focus=3, legend=[("solid", "한 팀(삼합): 돼지띠·양띠"), ("thick", "짝(육합): 개띠"), ("dash", "정면으로 마주 봄(충): 닭띠"), ("dot", "말을 천천히(원진·형·파): 원숭이·쥐·말띠")]),
              "토끼띠와 12띠의 관계도: 돼지띠·양띠는 한 팀, 개띠는 짝, 닭띠는 정면으로 마주 보고, 원숭이띠·쥐띠·말띠는 말을 천천히 하면 좋은 띠")},
        ops=[("rep", "naver_r02_", "G"), ("after", 6, "W")])
    # n05 2027년 돈 들어오는 띠 TOP3
    P["n05"] = dict(key="05", diag={
        "W": (lambda n, c: DG.wheel(n, c, "양(未)의 해, 돈이 들어오는 띠", [(7, 6, "pair"), (7, 11, "solid"), (7, 0, "dot")], hi={11, 0, 6}, focus=7,
              legend=[("hi", "돈 들어오는 띠 TOP3: 돼지띠·쥐띠·말띠"), ("pair", "양과 짝(육합): 말띠"), ("solid", "양과 한 팀(삼합): 돼지띠"), ("dot", "양과 서운하기 쉬운 사이(원진): 쥐띠")],
              note="쥐띠·돼지띠는 물의 띠라 해의 불이 재물이에요"),
              "2027년 양의 해와 돈 들어오는 띠 TOP3 관계도: 말띠는 양과 짝, 돼지띠는 한 팀, 쥐띠는 물의 띠라 불이 재물이지만 양과 서운하기 쉬운 사이"),
        "M": (lambda n, c: DG.months(n, c, "TOP3 띠가 힘을 쓸 달", [("돼지띠", {2, 3, 7}, set()), ("쥐띠", {4, 8}, set()), ("말띠", {2, 7, 10}, set())], next_jan=False, dn_label=None),
              "2027년 재물운 TOP3 띠가 힘을 쓸 달: 돼지띠 2·3·7월, 쥐띠 4·8월, 말띠 2·7·10월")},
        ops=[("after", 1, "W"), ("rep", "naver_m02_", "M")])
    # n10 2027년 연애운 TOP5
    P["n10"] = dict(key="10", diag={
        "M": (lambda n, c: DG.months(n, c, "TOP5 띠의 인연의 달", [("말띠", {7}, {2, 10}), ("토끼띠", {10}, {11}), ("돼지띠", {2}, {3, 7}), ("호랑이띠", {11}, {6, 10}), ("뱀띠", {8}, {9, 13})],
              up_label="인연의 달", dn_label="힘이 실리는 달"),
              "2027년 연애운 TOP5 띠의 인연의 달: 말띠 7월, 토끼띠 10월, 돼지띠 2월, 호랑이띠 11월, 뱀띠 8월과 힘이 실리는 달을 열두 달 칸에 표시한 그림"),
        "W": (lambda n, c: DG.wheel(n, c, "짝(육합)이 되는 띠 여섯 쌍", [(0, 1, "pair"), (6, 7, "pair"), (2, 11, "thick"), (3, 10, "thick"), (4, 9, "thick"), (5, 8, "thick")],
              legend=[("pair", "이웃한 짝: 쥐·소, 말·양"), ("thick", "마주 이어진 짝: 호랑이·돼지, 토끼·개, 용·닭, 뱀·원숭이")],
              note="내 띠와 짝이 되는 띠의 달이 내 인연의 달이에요"),
              "12띠의 짝(육합) 여섯 쌍 관계도: 쥐와 소, 말과 양, 호랑이와 돼지, 토끼와 개, 용과 닭, 뱀과 원숭이. 짝이 되는 띠의 달이 인연의 달")},
        ops=[("rep", "naver_l12_", "M"), ("rep", "naver_l13_", "L13W"), ("drop", "재미로 읽어 주세요.")])
    # n06 2027년 소띠
    P["n06"] = dict(key="06", diag={
        "W": (lambda n, c: DG.wheel(n, c, "소(丑)와 양(未)이 마주 보는 해", [(1, 0, "pair"), (1, 5, "solid"), (1, 9, "solid"), (5, 9, "solid"), (1, 7, "dash"), (1, 6, "dot")], hi={0, 5, 9}, focus=1,
              legend=[("pair", "짝(육합): 쥐띠"), ("solid", "한 팀(삼합): 뱀띠·닭띠"), ("dash", "정면으로 마주 봄(충): 양띠"), ("dot", "서운하기 쉬운 사이(원진): 말띠")]),
              "소띠와 12띠의 관계도: 쥐띠는 짝, 뱀띠·닭띠는 한 팀, 2027년의 양띠는 정면으로 마주 보고, 말띠는 서운하기 쉬운 사이"),
        "G": (lambda n, c: DG.monthgrid(n, c, "2027년 소띠 열두 달", months_grid({
              2: ("방향 잡기", None), 3: ("사람 모임", None), 4: ("일이 커짐", None), 5: ("한 팀", "up"), 6: ("서운함", "dn"), 7: ("부딪힘", "dn"),
              8: ("결실 시작", None), 9: ("한 팀", "up"), 10: ("서류 점검", None), 11: ("소개", None), 12: ("짝", "up"), 1: ("내 띠의 달", None)})),
              "2027년 소띠 열두 달 칸: 힘을 쓸 달은 5월·9월·12월, 아낄 달은 6월·7월, 칸마다 그달에 할 일을 적은 그림")},
        ops=[("after", 1, "W"), ("rep", "naver_o02_", "G")])
    # n12 2026년 상강·손없는날
    P["n12"] = dict(key="12", diag={
        "K": (lambda n, c: DG.calendar(n, c, "상강 앞뒤 손없는날", [(2026, 10, {19, 20, 29, 30}), (2026, 11, {8, 17, 18})], ring={10: {23}, 11: {7}},
              note="색 칸은 손없는날, 테두리는 상강(10/23)과 입동(11/7)이에요"),
              "2026년 10월·11월 달력: 손없는날 10월 19·20·29·30일, 11월 8·17·18일에 색을 칠하고 상강 10월 23일·입동 11월 7일에 테두리를 친 그림"),
        "N": (lambda n, c: DG.band(n, c, "상강 앞뒤 절기와 사주 달", (0, 70), [(0, "10월"), (31, "11월"), (61, "12월")],
              [("개의 달 (한로~입동)", 7.6, 37.8, "acc"), ("돼지의 달 (입동~대설)", 37.8, 67.5, "out")],
              [(18, "중양절 10/19"), (22.8, "상강 10/23 · 전갈자리 시작"), (37.8, "입동 11/7")]),
              "10월 8일 한로부터 11월 7일 입동 전까지 개의 달, 입동부터 12월 7일 대설 전까지 돼지의 달, 그 사이 중양절 10월 19일과 상강 10월 23일을 표시한 띠그래프")},
        ops=[("rep", "naver_s12_", "K"), ("after", 5, "N"), ("drop", "띠 하나만 본 한 줄 풀이이니 재미로 읽어 주세요.", "띠 하나만 본 한 줄 풀이예요.")])
    # n64 2027년 호랑이띠
    P["n64"] = dict(key="64", diag={
        "G": (lambda n, c: DG.monthgrid(n, c, "2027년 호랑이띠 열두 달", months_grid({
              6: ("한 팀", "up"), 10: ("한 팀", "up"), 11: ("짝", "up"), 8: ("부딪힘", "dn"), 9: ("서운함", "dn")})),
              "2027년 호랑이띠 열두 달 칸: 힘을 쓸 달은 6월·10월·11월, 아낄 달은 8월·9월을 칠한 그림"),
        "W": (lambda n, c: DG.wheel(n, c, "호랑이(寅)와 달마다 만나는 띠", [(2, 6, "solid"), (2, 10, "solid"), (2, 11, "thick"), (2, 8, "dash"), (2, 9, "dot")], hi={6, 10, 11}, focus=2,
              legend=[("solid", "함께 모이는 글자(반합): 말·개"), ("thick", "짝(육합): 돼지, 파도 겹쳐요"), ("dash", "정면으로 부딪힘(충): 원숭이"), ("dot", "서운함이 쌓이는 사이(원진): 닭")]),
              "호랑이띠와 2027년 달마다 만나는 띠의 관계도: 말·개는 함께 모이고, 돼지는 짝이면서 파가 겹치고, 원숭이는 정면으로 부딪히고, 닭은 서운함이 쌓이는 사이")},
        ops=[("rep", "naver_z64_b4", ""), ("rep", "naver_z64_c4", ""), ("after", 3, "G"), ("before", 4, "W")])
    return P

def run(only=None):
    P = plan(); pages = json.load(open(PG, encoding="utf-8")); made = []
    for pid, sp in P.items():
        if only and pid not in only: continue
        c = B.pal_of(pid); names = {}
        for k, (fn, alt) in sp["diag"].items():
            n = f"naver_z{sp['key']}_{k.lower()}5.jpg"
            if B.PREVIEW or not have(n): fn(n, c)
            names[k] = (n, alt); made.append(n)
        if B.PREVIEW: continue
        body = pages[pid]["body"]
        for op in sp["ops"]:
            if op[0] == "rep":
                if op[2] == "L13W":   # 표(인연의 달 날짜)는 두고 바로 아래에 관계도
                    m = re.search(r'<p><img[^>]*src="[^"]*' + re.escape(op[1]) + r'[^"]*"[^>]*></p>(?:<p>&nbsp;</p>)?', body)
                    body = body[:m.end()] + IMG(*names["W"]) + body[m.end():]
                else: body = replace_img(body, op[1], IMG(*names[op[2]]) if op[2] else "")
            elif op[0] == "after": body = after_head(body, op[1], IMG(*names[op[2]]))
            elif op[0] == "before": body = before_head(body, op[1], IMG(*names[op[2]]))
            elif op[0] == "drop":
                if len(op) == 3: body, k = re.subn(r'<p>' + re.escape(op[1]) + r'</p>', f"<p>{op[2]}</p>", body); assert k == 1, op
                else: body = drop_line(body, op[1])
        pages[pid]["body"] = body; pages[pid]["k131"] = TAG
    if not B.PREVIEW:
        open(PG, "w", encoding="utf-8").write(json.dumps(pages, ensure_ascii=False, indent=1) + "\n")
    return made

def thick(only=None):
    """K-133(대표 10/17 17:42 선·화살표 굵게): 같은 도식을 굵은 선(diagrams_k131 LW·BOX·AH)으로 새 이름 *6.jpg 에 다시 그리고
    원고 본문의 *5.jpg 주소를 *6.jpg 로 바꾼다. 옛 *5.jpg 는 지우지 않는다(K-025·네이버 사진 보존 규칙)."""
    P = plan(); pages = json.load(open(PG, encoding="utf-8")); made = []
    for pid, sp in P.items():
        if only and pid not in only: continue
        c = B.pal_of(pid); body = pages[pid]["body"]
        for k, (fn, alt) in sp["diag"].items():
            o, n = f"naver_z{sp['key']}_{k.lower()}5.jpg", f"naver_z{sp['key']}_{k.lower()}6.jpg"
            if B.PREVIEW or not have(n): fn(n, c)
            made.append(n)
            if not B.PREVIEW: assert body.count(o) == 1, (pid, o); body = body.replace(o, n)
        if not B.PREVIEW: pages[pid]["body"] = body; pages[pid]["k131"] = TAG + " · K-133 굵은 선"
    if not B.PREVIEW:
        open(PG, "w", encoding="utf-8").write(json.dumps(pages, ensure_ascii=False, indent=1) + "\n")
    return made

if __name__ == "__main__":
    if sys.argv[1:2] == ["--thick"]: print(thick({a for a in sys.argv[2:]} or None))
    else: print(run({a for a in sys.argv[1:]} or None))
