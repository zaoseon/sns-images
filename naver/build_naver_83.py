"""네이버 n83: 띠 궁합표 새 글 (CT 11/4 08:25 → ① 최우선, 대표 11/4 07:48 "지금 노출 안되는 글들도 조회수 높은 것들 순서로 수정 후 신규발행").
- 왜: 노출 안 되는 옛 글 조회 2위 n03(띠별 궁합표 총정리)을 새 글로 쓴다.
- 지킨 것: n03은 건드리지 않는다(K-147). 복사하지 않는다(K-151): 제목·도입·소제목 순서(쌍 목록 → 내 띠 한 줄 표)·찾는 법(시계 → 띠 번호 더하기·빼기)·
  예시(1991년 1월 20일생)·그림 유형(quad·fork·compare)·심리 개념(실제로 닮음 vs 닮았다고 느낌)·연결글(n01 → 발행된 n80)을 새로 썼다. 같은 것은 띠 관계 계산값뿐이다.
- 띠 관계: 육합·충·삼합은 번호 규칙으로 계산하고 정해진 목록과 assert, 원진은 목록. 입춘 1991 = engine.get_solar_terms_kst(1991) 2/4 17:08.
- 출처 2개(K-162, 11/4 웹 확인): Montoya, Horton & Kirchner (2008) JSPR 25(6) 889-922 DOI 10.1177/0265407508096700(머독대 연구 목록에서 확인) ·
  한국천문연구원 천문우주지식정보 2027 월력요항(n04에서 쓴 주소).
- 날짜: CT가 정한다. pages.json dt 는 자리값(2027-01-31 18:00)이고 dt_tbd 로 표시.
사용: SITE=<zaoseon-site> python3 naver/build_naver_83.py"""
import os, sys, json, re, html, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "pipeline"))
os.chdir(HERE)
import cover_v3 as V, make_page as MP, diagrams_k131 as DG, diagrams_k131b as DGB, diagrams_k131c as DGC
SITE = os.environ.get("SITE", "/home/claude/zaoseon-site")
RAW = "https://raw.githubusercontent.com/zaoseon/sns-images/main/naver/img/"
BL = "<p>&nbsp;</p>"
def P(*ls): return "".join(f"<p>{l}</p>" for l in ls) + BL
def IMG(name, alt): return f'<p><img src="{RAW}{name}" alt="{html.escape(alt, quote=True)}"></p>' + BL
def H(t): return f"<p><b>{t}</b></p>"
MID = ('<table style="width:100%;max-width:440px;margin:0 auto;border-collapse:collapse"><tbody>'
       '<tr><td style="padding:12px 10px;text-align:center;border:1px solid #d0d0d0"><b>두 사람 생년월일로 1초</b></td></tr>'
       '<tr><td style="padding:12px 10px;text-align:center;border:1px solid #d0d0d0"><span style="color:#9a9a9a">[ 1991 . 01 . 20 ]</span></td></tr>'
       '<tr><td style="padding:12px 10px;text-align:center;border:1px solid #d0d0d0"><b><a href="https://zaoseon.com/?utm_source=naver&amp;utm_medium=mid#free">내 태어난 날 글자 보기 →</a></b></td></tr>'
       '</tbody></table>' + BL)
CTA = ('<p><a href="https://zaoseon.com/?utm_source=naver&utm_medium=cta#free"><img src="' + RAW +
       'naver_cta5_1%EC%B4%88%EB%AC%B4%EB%A3%8C%ED%92%80%EC%9D%B4.jpg" alt="자오선 무료 1초 풀이 안내 배너"></a></p>')
PID, KEY, PAL = "n83", "83", "p_red_s"   # 관계 글 → 페일 핑크 판(y_pink_s 는 바둑판 칸이 K-138 대비 1.5로 막힘)

# ───────── 띠 관계 계산과 검산 (번호 1=쥐 … 12=돼지)
NM = ["쥐", "소", "호랑이", "토끼", "용", "뱀", "말", "양", "원숭이", "닭", "개", "돼지"]
HJ = "子丑寅卯辰巳午未申酉戌亥"
EMO = ["🐭", "🐮", "🐯", "🐰", "🐲", "🐍", "🐴", "🐑", "🐵", "🐔", "🐶", "🐷"]
def no(i): return i + 1
def pair(i): return [j for j in range(12) if j != i and (no(i) + no(j)) % 12 == 3][0]          # 두 번호 더해 3 또는 15 = 짝(육합)
def team(i): return [j for j in range(12) if j != i and (i - j) % 4 == 0]                      # 네 칸씩 = 한 팀(삼합)
def opp(i): return (i + 6) % 12                                                                # 여섯 칸 = 마주 봄(충)
WJ = {0: 7, 7: 0, 1: 6, 6: 1, 2: 9, 9: 2, 3: 8, 8: 3, 4: 11, 11: 4, 5: 10, 10: 5}               # 원진: 子未 丑午 寅酉 卯申 辰亥 巳戌
assert {frozenset((HJ[i], HJ[pair(i)])) for i in range(12)} == {frozenset(x) for x in ("子丑", "寅亥", "卯戌", "辰酉", "巳申", "午未")}
assert {frozenset(HJ[k] for k in [i] + team(i)) for i in range(12)} == {frozenset(x) for x in ("申子辰", "亥卯未", "寅午戌", "巳酉丑")}
assert {frozenset((HJ[i], HJ[opp(i)])) for i in range(12)} == {frozenset(x) for x in ("子午", "丑未", "寅申", "卯酉", "辰戌", "巳亥")}
assert all(WJ[WJ[i]] == i for i in WJ) and {frozenset((HJ[i], HJ[j])) for i, j in WJ.items()} == {frozenset(x) for x in ("子未", "丑午", "寅酉", "卯申", "辰亥", "巳戌")}
for i in range(12): assert len({pair(i), opp(i), WJ[i], *team(i)}) == 5, NM[i]                    # 네 관계가 겹치지 않음
assert (pair(0), team(0), opp(0), WJ[0]) == (1, [4, 8], 6, 7)                                      # 쥐: 짝 소 · 한 팀 용·원숭이 · 마주 봄 말 · 서운함 양
# 2027 정미(未=양, 번호 8)
Y = 7; assert (NM[pair(Y)], [NM[j] for j in team(Y)], NM[opp(Y)], NM[WJ[Y]]) == ("말", ["토끼", "돼지"], "소", "쥐")
# 입춘 1991(engine 11/4 실행 값): 2월 4일 17:08 → 1991년 1월 20일생은 1990 경오(庚午)년 말띠
BR = HJ; GAN = "甲乙丙丁戊己庚辛壬癸"
def gz(y): return GAN[(y - 4) % 10] + BR[(y - 4) % 12]
assert gz(1990) == "庚午" and gz(1991) == "辛未"
try:
    sys.path.insert(0, os.path.join(SITE, "engine")); import engine as EN
    t = [x for x in EN.get_solar_terms_kst(1991) if x[0] == "입춘"][0][2]; assert t.strftime("%m-%d %H:%M") == "02-04 17:08", t
    print("입춘 1991 엔진으로 다시 확인")
except ImportError:
    print("엔진 없음: 11/4 실행 값으로 씀")

def row(i):
    return (f"{EMO[i]} <b>{NM[i]}띠</b>: 짝 {NM[pair(i)]} · 한 팀 {'·'.join(NM[j] for j in team(i))} · "
            f"마주 봄 {NM[opp(i)]} · 서운함 {NM[WJ[i]]}")

# ───────── 본문 (n03 문장을 옮기지 않았다)
head = ["<b>띠 궁합표는 열두 띠가 서로 어떤 자리에 있는지 한 장에 모은 표예요.</b>",
        "내 띠 줄 하나만 보면 짝(육합), 한 팀(삼합), 마주 보는 띠(충), 서운함이 쌓이기 쉬운 띠(원진)가 바로 나와요.",
        "<b>예를 들어 쥐띠는 짝이 소띠, 한 팀이 용띠·원숭이띠, 마주 보는 띠가 말띠예요.</b>",
        "명절에 가족끼리 '우리 둘은 띠가 안 맞는대' 하는 말이 나오면 이 표부터 같이 펴 보세요.",
        "2026년 11월 4일 기준으로 정리한 내용이에요."]
toc_q = ["12띠 궁합표, 내 띠 줄은 어디일까요?", "짝·한 팀·마주 보는 띠는 어떻게 정해질까요?", "1월생이라면 띠부터 다시 봐야 하는 이유는?",
         "띠 궁합이 안 맞으면 정말 안 맞을까요?", "2027년 정미년에 궁합이 움직이는 띠는?", "자주 묻는 질문"]

sec1 = P("<b>내 띠를 찾아 그 줄만 읽으셔도 돼요.</b>") + P(*[row(i) for i in range(12)]) + \
       P("아래 그림은 한 팀(삼합)으로 묶이는 네 무리예요.", "칠한 칸이 2027년 양의 해와 같은 팀이에요.") + "[[M]]" + MID
sec2 = P("<b>띠마다 번호를 붙이면 외우지 않아도 찾을 수 있어요.</b>", "쥐 1, 소 2, 호랑이 3 … 돼지 12까지 순서대로 번호를 매겨요.") + \
       P("❤️ <b>짝(육합)</b>: 두 번호를 더해 3이나 15가 되는 띠", "쥐 1 + 소 2 = 3, 말 7 + 양 8 = 15처럼요.") + \
       P("🤝 <b>한 팀(삼합)</b>: 번호가 4씩 차이 나는 세 띠", "토끼 4, 양 8, 돼지 12가 한 팀이에요.") + \
       P("🔥 <b>마주 봄(충)</b>: 번호가 6 차이 나는 띠", "호랑이 3과 원숭이 9처럼 열두 띠 원에서 정면으로 마주 앉아요.") + \
       P("💧 <b>서운함(원진)</b>은 번호 규칙이 없어 여섯 쌍을 그대로 봐요.",
         "쥐·양, 소·말, 호랑이·닭, 토끼·원숭이, 용·돼지, 뱀·개예요.") + "[[F]]"
sec3 = P("<b>띠는 1월 1일이 아니라 입춘에 바뀌어요.</b>", "그래서 1월생과 2월 초생은 띠 궁합표를 보기 전에 내 띠부터 확인해야 해요.") + \
       P("📆 1991년 입춘은 2월 4일 오후 5시 8분이었어요.", "1991년 1월 20일생은 입춘 전이라 양띠가 아니라 1990년 경오(庚午)년 말띠예요.",
         "양띠로 알고 궁합표를 보면 짝(말)과 서운함(쥐)이 통째로 바뀌어요.") + \
       P("입춘 날짜와 시각은 해마다 달라요. 한국천문연구원 월력요항에서 그해 입춘을 확인할 수 있어요.",
         '📚 <b>출처 1</b>: <a href="https://astro.kasi.re.kr/kor/life/post/calendarData?year=2027">한국천문연구원 천문우주지식정보, 2027 월력요항</a>')
sec4 = P("🧠 <b>띠 궁합은 시작점이고, 결론은 아니에요.</b>",
         "심리학자 몬토야 연구팀은 '닮을수록 끌린다'는 연구 수백 건을 모아 다시 분석했어요.") + "[[C]]" + \
       P("처음 만나는 사이에서는 실제로 닮은 점도 끌림과 이어졌어요.",
         "그런데 이미 만나고 있는 사이에서는 실제로 닮았는지보다 <b>'우리는 잘 맞는다'고 느끼는지</b>가 끌림과 더 이어졌어요.",
         '📚 <b>출처 2</b>: <a href="https://doi.org/10.1177/0265407508096700">Montoya, Horton &amp; Kirchner (2008), Journal of Social and Personal Relationships</a>') + \
       P("마주 보는 띠라도 서로 맞는 점을 자주 말해 주는 사이라면 느끼는 궁합은 달라질 수 있어요.") + \
       P("🌱 <b>마음 코치 정월의 질문</b>", "🔸 띠가 안 맞는다는 그 사람과<br>잘 맞았던 순간 하나를 떠올리면요?",
         "🔸 그 순간을 오늘 한 문장으로<br>그 사람에게 말해 준다면요?") + \
       P("✔️ <b>이번 주에 해 볼 것 하나</b>: 자주 부딪히는 사람에게<br>'이건 우리 잘 맞더라' 한 가지를<br>말로 건네 보세요.")
sec5 = P("<b>2027년은 양(未)의 해라, 양과 이어진 띠의 궁합이 먼저 움직여요.</b>") + \
       P(f"❤️ 짝: {NM[pair(Y)]}띠, 손잡는 일이 잘 풀리기 쉬워요.", f"🤝 한 팀: {'띠·'.join(NM[j] for j in team(Y))}띠, 사람을 통해 일이 들어와요.",
         f"🔥 마주 봄: {NM[opp(Y)]}띠, 자리가 움직이기 쉬운 해예요.", f"💧 서운함: {NM[WJ[Y]]}띠, 말은 글로 한 번 더 남겨 두세요.") + \
       P("띠별로 힘 쓸 달과 아낄 달은 아래 연결 글에 한 장으로 모아 두었어요.")
sec6 = P("<b>Q. 띠 궁합에서 가장 좋은 짝은 무엇인가요?</b>", "A. 짝(육합)과 한 팀(삼합)을 편한 사이로 봐요.",
         "짝은 둘이 마주 앉아 맞춰 가는 사이, 한 팀은 셋이 모여 같은 쪽을 보는 사이예요.") + \
       P("<b>Q. 마주 보는 띠(충)와 결혼해도 되나요?</b>", "A. 피해야 할 까닭은 없어요.",
         "속도와 방식이 달라 부딪히기 쉬운 만큼, 역할을 나누면 서로 없는 것을 채워 주는 사이로 읽어요.") + \
       P("<b>Q. 원진은 왜 서운함이라고 하나요?</b>", "A. 겉으로 큰 다툼은 적은데 작은 서운함이 쌓이기 쉬운 사이로 봐서예요.",
         "그때그때 짧게 말하는 것만으로도 많이 가벼워져요.") + \
       P("<b>Q. 띠 말고 더 자세한 궁합은요?</b>", "A. 두 사람의 태어난 날 첫 글자(일간)와 여덟 글자를 함께 겹쳐 봐요.",
         "같은 띠 부부라도 태어난 날이 달라서 궁합이 다르게 나와요.")
tail = P("여러분 집에서 가장 자주 부딪히는 두 띠는 무엇인가요?", "표에서 찾은 관계를 댓글로 들려주세요.") + \
       '<p><b>👇 우리 둘의 띠가 2027년에 어떤 해를 맞는지 궁금하다면, 2027 띠별 운세, 정미년 12띠 힘 쓸 달과 아낄 달 한눈에</b></p>'
secs = [sec1, sec2, sec3, sec4, sec5, sec6]

def _have(n): return os.path.exists(os.path.join(HERE, "img", n))
def build():
    for d_ in ("wide", "m1280", "master"): os.makedirs(os.path.join(HERE, "img", d_), exist_ok=True)
    c = V.Ctx(PAL); made = []
    a4 = f"wide/naver_z{KEY}_a4.jpg"
    if not _have(a4):
        V.render(PID + "_new", {"d": "N", "el": "불", "kick": "12띠 궁합표", "hook": ["내 띠 줄만 보면", "짝이 보여요"], "sub": "번호로 찾는 법",
                                "items": ["짝", "한 팀", "마주 봄"]}, os.path.join(HERE, "img", a4), PAL)
    made.append(a4)
    nm = {"M": f"naver_z{KEY}_d6.jpg", "F": f"naver_z{KEY}_k6.jpg", "C": f"naver_z{KEY}_c6.jpg"}
    if not _have(nm["M"]):
        TM = [(8, 0, 4), (11, 3, 7), (2, 6, 10), (5, 9, 1)]          # 원숭이·쥐·용 / 돼지·토끼·양 / 호랑이·말·개 / 뱀·닭·소
        for g in TM: assert sorted(team(g[0]) + [g[0]]) == sorted(g)
        DGC.quad(nm["M"], c, "한 팀으로 묶이는 네 무리", [("·".join(NM[k] for k in g), "번호 " + " · ".join(str(no(k)) for k in g)) for g in TM], 1,
                 "띠 관계 계산 · 삼합", "칠한 칸은 2027년 양(未)의 해와 같은 팀이에요")
    if not _have(nm["F"]):
        DGB.fork(nm["F"], c, "띠 번호로 궁합 찾기", "쥐 1 소 2 호랑이 3 … 돼지 12",
                 ["더해서 3이나 15 = 짝", "4씩 차이 = 한 팀", "6 차이 = 마주 봄"], "원진 여섯 쌍은 번호 규칙 없이 그대로 봐요")
    if not _have(nm["C"]):
        DGC.compare(nm["C"], c, "닮아서 끌릴까, 닮았다고 느껴서 끌릴까", ("실제로 닮은 점", "닮았다고 느끼는 점"),
                    [("첫 만남", "끌림과 이어져요", "끌림과 이어져요"), ("만나는 중", "끌림과 거의 상관없어요", "여전히 끌림과 이어져요")],
                    "Montoya 외 (2008), JSPR", hi=1)
    import fullbleed as FBL
    plan_p = os.path.join(HERE, "fullbleed_plan.json"); plan = json.load(open(plan_p, encoding="utf-8")) if os.path.exists(plan_p) else {}
    rows = []
    for pos, k in enumerate("MFC", 1):
        f = nm[k][:-4] + "f.jpg"
        if not _have(f):
            r, why = FBL.convert(nm[k], [os.path.join(HERE, "img"), os.path.join(HERE, "img", "m1280")]); assert r, (nm[k], why)
        rows.append({"pos": pos, "old": nm[k], "new": f}); made.append(nm[k]); nm[k] = f
        reg_ = json.load(open(DG.REG, encoding="utf-8")); reg_[f] = reg_[rows[-1]["old"]]; json.dump(dict(sorted(reg_.items())), open(DG.REG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    plan[PID] = rows; json.dump(plan, open(plan_p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    made += list(nm.values())
    alt = {"M": "한 팀으로 묶이는 네 무리 그림. 원숭이·쥐·용, 돼지·토끼·양, 호랑이·말·개, 뱀·닭·소. 돼지·토끼·양이 2027년 양의 해와 같은 팀",
           "F": "띠에 1부터 12까지 번호를 붙여, 더해서 3이나 15면 짝, 4씩 차이면 한 팀, 6 차이면 마주 보는 띠로 찾는 방법 그림",
           "C": "처음 만난 사이에서는 실제로 닮은 점과 닮았다고 느끼는 점 모두 끌림과 이어지고, 이미 만나는 사이에서는 닮았다고 느끼는 점만 끌림과 이어진다는 몬토야 연구팀 2008 비교표"}
    body = P(*head) + P("<b>📌 이 글의 순서</b>", *[f"{i + 1}. {q}" for i, q in enumerate(toc_q)])
    for i, (q, s) in enumerate(zip(toc_q, secs)):
        for k in "MFC": s = s.replace(f"[[{k}]]", IMG(nm[k], alt[k]))
        body += H(f"{i + 1}. {q}") + s
    body += tail + CTA
    import copy_rules as CR
    for w in ("재미로", "상담", "—", "안녕하세요, 자오선의 정월이에요", "결론부터 말씀드릴게요") + tuple(CR.금지어):
        assert w not in re.sub(r"<[^>]+>", " ", body), w
    for f in made:   # 사이트 사본(K-069)
        dst = os.path.join(SITE, "public", "naver", "img", f); os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy(os.path.join(HERE, "img", f), dst)
    return body, a4, made

TITLE = "띠 궁합표 한눈에, 12띠 짝과 부딪히는 띠 번호로 찾는 법"
TAGS = ["띠궁합표", "띠궁합", "띠별궁합", "12띠궁합", "잘맞는띠", "육합", "삼합", "원진", "2027궁합", "자오선"]
REL = {"id": "n80", "title": "2027 띠별 운세, 정미년 12띠 힘 쓸 달과 아낄 달 한눈에",
       "phrase": "우리 둘의 띠가 2027년에 어떤 해를 맞는지 궁금하다면, 2027 띠별 운세, 정미년 12띠 힘 쓸 달과 아낄 달 한눈에",
       "url": "https://blog.naver.com/zaoseon/224461125363"}
INTENT = {"keywords": ["띠 궁합표", "띠 궁합", "띠별 궁합", "잘 맞는 띠", "12띠 궁합"],
          "keyword_src": "n03 조회 순위(11/4 CT·서브 '노출 안 되는 옛 글 조회수 순' 2위) · n03 태그(띠별궁합·띠궁합표·띠궁합) · 자동완성·월 검색량 자료 없음(발행 7일 뒤 유입 검색어로 고친다)",
          "intent": "알고 싶다", "intent_note": "내 띠와 상대 띠가 짝인지, 부딪히는 사이인지 표에서 바로 찾기",
          "first3": "띠 궁합표는 열두 띠가 서로 어떤 자리에 있는지 한 장에 모은 표예요. 내 띠 줄 하나만 보면 짝(육합)·한 팀(삼합)·마주 보는 띠(충)·서운함(원진)이 나와요. 쥐띠는 짝이 소띠, 한 팀이 용띠·원숭이띠예요.",
          "answer_keys": ["궁합표", "짝(육합)"],
          "order": toc_q[:5], "images": ["한 팀 네 무리(quad)", "띠 번호로 찾는 법(fork)", "실제 닮음 vs 느끼는 닮음(compare, Montoya 외 2008)"],
          "related": "n80", "cta": PID, "experience": [], "applied": True,
          "differs_from_n03": "제목·도입(정의 + 쥐띠 예시 직답)·소제목 순서(쌍 목록 → 내 띠 한 줄 표)·찾는 법(시계 → 번호 더하기·빼기)·예시(1991년 1월 20일생 입춘)·그림 유형(quad·fork·compare)·심리 개념(닮음 연구)·출처 2개·연결글(n01 → n80)"}

if __name__ == "__main__":
    body, a4, made = build()
    reg = json.load(open(MP.REG, encoding="utf-8"))
    assert PID not in reg or not reg[PID].get("done"), "이미 예약 끝난 글"
    reg[PID] = dict(dt="2027-01-31T18:00:00", dt_tbd="CT가 정함(서브 배너 링크 고침 확인 뒤 하루 2편 08:00·18:00). 이 날짜는 자리값", title=TITLE, tags=TAGS, body=body,
                    cover=a4, related=REL, thumbs=None, cid=None, clips=None, category="관계 읽기", done=False,
                    k131="n83 11/4(K-151 새 글)", source="build_naver_83.py (n03 주제 새 글, n03 그대로)")
    json.dump(reg, open(MP.REG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    ic = json.load(open(os.path.join(HERE, "intent_cards.json"), encoding="utf-8")); ic["cards"][PID] = INTENT
    json.dump(ic, open(os.path.join(HERE, "intent_cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    v = reg[PID]; import datetime as D
    MP.write_page(PID, D.datetime.fromisoformat(v["dt"]), v["title"], v["tags"], v["body"], None, v["cover"], v["related"], v["category"])
    MP.write_index()
    import k151_check as K
    print(PID, len(TITLE), "자 제목 · 본문 글자", len(re.sub(r"<[^>]+>|&nbsp;", "", body)), "· 사진", made, "· K 검사", K.check(PID, v))
