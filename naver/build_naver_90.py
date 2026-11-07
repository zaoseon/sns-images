"""네이버 n90: 2027년 재물운 좋은 띠 새 글 (CT 11/4 19:40 → ① 최우선, 대표 11/4 19:28 재발행 일정 '새 글로 다시 쓰기' n05 → n90, 11/20 18:00 자리).
- 왜: 노출 안 되는 옛 글 n05(2027년 돈 들어오는 띠 TOP3)를 새 글로. n05는 건드리지 않는다(K-147·K-178).
- 검색어: data/keywords/kw_volume.json posts.n90 — 2027년재물운 110(11/6 20:03). 11/7 씨앗을 넓혀 다시 요청(재물운·2027년띠별운세).
- 다르게 쓴 것(K-151): n05의 순위(TOP3 돼지·쥐·말)·한 줄 요약·수비학·여섯 운명학·심적 회계 대신,
  해 글자 두 개(丁 불·未 흙)가 띠 기운에 무엇이 되는지로 '돈이 들어오는 세 갈래'를 세운다(丁이 돈: 쥐·돼지 / 未가 돈: 호랑이·토끼 / 未와 손잡는 띠: 돼지·토끼·말).
  예시 장면 = 1996년 2월 4일생 둘(저녁 8시 乙亥 돼지띠 · 밤 10시 30분 丙子 쥐띠, 입춘 22:07). 심리 = Thaler & Benartzi 2004 SMarT(오를 월급 미리 나누기).
  그림 유형 fork·sides·bignum(n05는 순위 목록). 연결글 s 없음 → n80(발행·노출 '예'). 소제목 틀(한 줄 요약·이 글의 순서·생년월일만 넣으면 1초·수비학으로 겹쳐 보면) 안 씀.
- 계산: 해 간지·띠 관계는 n80과 같은 식으로 assert, 힘 쓸 달은 사이트 tools/tti_extra.json(n80과 같은 값), 입춘 시각과 연주는 engine/engine.py.
- 출처 2개(K-162, 11/7 확인): Thaler & Benartzi (2004) Journal of Political Economy 112(S1) S164–S187, DOI 10.1086/380085
  (EconPapers 서지·초록으로 확인: 78% 가입, 80%가 네 번째 인상까지 유지, 40개월 동안 평균 저축 비율 3.5%→13.6%) · 한국천문연구원 음양력 변환(입춘 시각).
- 날짜: CT가 정한다. pages.json dt 는 자리값, dt_tbd 로 표시.
사용: SITE=<zaoseon-site> python3 naver/build_naver_90.py"""
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
       '<tr><td style="padding:12px 10px;text-align:center;border:1px solid #d0d0d0"><b>띠 말고 내 돈 기운이 궁금하다면</b></td></tr>'
       '<tr><td style="padding:12px 10px;text-align:center;border:1px solid #d0d0d0"><span style="color:#9a9a9a">[ 1996 . 02 . 04 ]</span></td></tr>'
       '<tr><td style="padding:12px 10px;text-align:center;border:1px solid #d0d0d0"><b><a href="https://zaoseon.com/?utm_source=naver&amp;utm_medium=mid#free">내 태어난 날 글자 보기 →</a></b></td></tr>'
       '</tbody></table>' + BL)
CTA = ('<p><a href="https://zaoseon.com/?utm_source=naver&utm_medium=cta#free"><img src="' + RAW +
       'naver_cta5_1%EC%B4%88%EB%AC%B4%EB%A3%8C%ED%92%80%EC%9D%B4.jpg" alt="자오선 무료 1초 풀이 안내 배너"></a></p>')
PID, KEY, PAL = "n90", "90", "g_ivory_s"   # 나무 띠에게 흙이 돈 = 나무 판 묶음(EL_SET 나무), n89 k_white_s·n88 y_black_s 와 다른 판

# ───────── 계산값과 검산
import datetime as D
BR = "子丑寅卯辰巳午未申酉戌亥"; GAN = "甲乙丙丁戊己庚辛壬癸"
assert GAN[(2027 - 4) % 10] + BR[(2027 - 4) % 12] == "丁未"
EL = dict(zip(BR, "물 흙 나무 나무 흙 불 불 흙 쇠 쇠 흙 물".split()))
GEUK = {"물": "불", "불": "쇠", "쇠": "나무", "나무": "흙", "흙": "물"}     # 내가 이기는 기운 = 재물
SAENG = {"물": "나무", "나무": "불", "불": "흙", "흙": "쇠", "쇠": "물"}    # 내가 낳는 기운 = 솜씨·표현
def role(me, it):
    if it == me: return "같은 편"
    if GEUK[me] == it: return "손에 쥐는 돈"
    if SAENG[me] == it: return "솜씨·표현"
    if GEUK[it] == me: return "책임·규칙"
    assert SAENG[it] == me; return "문서·도움"
ROLE = {e: (role(e, "불"), role(e, "흙")) for e in ("물", "나무", "불", "흙", "쇠")}
assert ROLE == {"물": ("손에 쥐는 돈", "책임·규칙"), "나무": ("솜씨·표현", "손에 쥐는 돈"), "불": ("같은 편", "솜씨·표현"),
                "흙": ("문서·도움", "같은 편"), "쇠": ("책임·규칙", "문서·도움")}
assert [b for b in BR if EL[b] == "물"] == ["子", "亥"] and [b for b in BR if EL[b] == "나무"] == ["寅", "卯"]
Y = BR.index("未")
LIUHE = {0: 1, 2: 11, 3: 10, 4: 9, 5: 8, 6: 7}; LIUHE.update({v: k for k, v in list(LIUHE.items())})
assert LIUHE[Y] == BR.index("午")                                    # 육합: 말띠
assert {BR.index("亥"), BR.index("卯"), Y} == {11, 3, 7}             # 삼합 亥卯未: 돼지·토끼
assert (Y + 6) % 12 == BR.index("丑")                                # 충: 소띠
WONJIN = {0: 7, 1: 6, 2: 9, 3: 8, 4: 11, 5: 10}; WONJIN.update({v: k for k, v in list(WONJIN.items())})
assert WONJIN[Y] == BR.index("子")                                   # 원진: 쥐띠
def yrs(i): return "·".join(str(1972 + i + 12 * k) for k in range(4))
assert yrs(11) == "1983·1995·2007·2019" and yrs(0) == "1972·1984·1996·2008" and yrs(2) == "1974·1986·1998·2010" and yrs(3) == "1975·1987·1999·2011" and yrs(6) == "1978·1990·2002·2014"
EX = json.load(open(os.path.join(SITE, "tools", "tti_extra.json"), encoding="utf-8"))
assert EX["rat"]["good"][:2] == ["4월", "8월"] and EX["pig"]["good"] == ["2월", "3월", "7월"]
assert EX["tiger"]["good"] == ["6월", "10월", "11월"] and EX["rabbit"]["good"] == ["7월", "10월", "11월"] and EX["horse"]["good"] == ["2월", "7월", "10월"]
assert EX["ox"]["care"] == ["6월", "7월"] and EX["dog"]["care"] == ["4월", "5월"]
sys.path.insert(0, os.path.join(SITE, "engine")); import engine as E
LC = dict((n, t) for n, _, t in E.get_solar_terms_kst(1996))["입춘"]; assert (LC.month, LC.day, LC.hour, LC.minute) == (2, 4, 22, 7)
L27 = dict((n, t) for n, _, t in E.get_solar_terms_kst(2027))["입춘"]; assert (L27.month, L27.day, L27.hour, L27.minute) == (2, 4, 10, 46)
assert E.compute_saju(D.datetime(1996, 2, 4, 20, 0))["팔자"]["년주"] == "乙亥"    # 저녁 8시생 = 돼지띠
assert E.compute_saju(D.datetime(1996, 2, 4, 22, 30))["팔자"]["년주"] == "丙子"   # 밤 10시 30분생 = 쥐띠
assert E.compute_saju(D.datetime(2027, 2, 4, 9, 0))["팔자"]["년주"] == "丙午" and E.compute_saju(D.datetime(2027, 2, 4, 12, 0))["팔자"]["년주"] == "丁未"
print("해 간지·띠 관계·힘 쓸 달·입춘 시각·연주 다시 확인")

# ───────── 본문 (n05 문장을 옮기지 않았다)
head = ["<b>2027년 재물운 좋은 띠는 해의 두 글자 丁(불)과 未(흙) 가운데 하나를 내 돈으로 쓰는 띠예요.</b>",
        "불이 돈이 되는 띠는 쥐띠·돼지띠, 흙이 돈이 되는 띠는 호랑이띠·토끼띠예요. 여기에 양(未)과 손잡는 돼지띠·토끼띠·말띠는 사람을 통해 돈이 들어와요.",
        "<b>그래서 2027년 돈 길은 세 갈래예요. 해의 불, 해의 흙, 손잡는 사람이에요. 돼지띠와 토끼띠는 두 갈래에 함께 들어가요.</b>",
        "나머지 띠도 돈이 막히는 해는 아니에요. 해 글자가 내 띠에 다른 일을 맡길 뿐이라, 그 일을 알면 돈을 지키는 법도 보여요. 2026년 11월 7일 기준으로 정리한 내용이에요."]
toc_q = ["2027년 재물운 좋은 띠는 무엇으로 가를까요?", "해의 불이 돈이 되는 쥐띠와 돼지띠, 무엇이 다를까요?",
         "호랑이띠와 토끼띠는 왜 솜씨가 돈이 될까요?", "사람이 돈을 데려오는 띠는 누구일까요?",
         "나머지 띠는 2027년 돈을 어떻게 지킬까요?", "오를 월급을 미리 나눠 두면 무엇이 달라질까요?", "자주 묻는 질문"]
sec1 = P("<b>내 띠 기운이 해 글자를 이기면, 그 글자가 내 손에 쥐는 돈이 돼요.</b>",
         "띠마다 기운이 하나씩 있어요. 쥐·돼지는 물, 호랑이·토끼는 나무, 뱀·말은 불, 소·용·양·개는 흙, 원숭이·닭은 쇠예요.",
         "사주에서는 내가 이기는 기운을 재물로 봐요. 물은 불을 끄고, 나무는 흙에 뿌리를 내리니 물에게는 불이, 나무에게는 흙이 돈이에요.",
         "2027년 정미년은 하늘 글자가 丁 불, 땅 글자가 未 흙이에요. 글자가 두 개라 돈이 되는 띠도 두 무리로 나뉘어요.") + "[[F]]" + \
       P("여기에 하나를 더 봐요. 해의 주인인 양(未)과 한 팀을 이루는 띠는, 내 기운과 상관없이 사람과 제안이 따라와요.",
         "이렇게 세 갈래로 보면, 순위 한 줄보다 내 띠가 어느 길로 돈을 만나는지가 먼저 보여요.")
sec2 = P("🔎 <b>같은 날 태어나도 시각이 다르면 띠가 달라질 수 있어요.</b>",
         "1996년 2월 4일생 두 사람을 떠올려 볼게요. 그해 입춘은 2월 4일 밤 10시 7분이었어요.",
         "저녁 8시에 태어난 사람은 입춘 전이라 1995년 을해년, 돼지띠예요. 밤 10시 30분에 태어난 사람은 입춘 뒤라 1996년 병자년, 쥐띠예요.") + \
       P("둘 다 물의 띠라 2027년 해의 불은 둘 모두에게 돈이에요. 다만 돈이 들어오는 모양은 달라요.",
         "돼지(亥)는 양(未)과 한 팀(삼합)이라 소개와 연결로 돈이 들어오기 쉬워요. 1983·1995·2007·2019년생이에요. 힘 쓸 달은 2월·3월·7월이에요.",
         "쥐(子)는 양(未)과 서로 서운함이 쌓이기 쉬운 사이(원진)예요. 돈 기회는 분명한데, 가까운 사람과 돈이 섞이면 마음이 먼저 다쳐요. 1972·1984·1996·2008년생이고 힘 쓸 달은 4월·8월이에요.") + \
       P("물의 띠에게 해의 흙은 나를 누르는 기운이라 책임도 같이 따라와요. 돈과 일이 함께 늘어나는 해로 보면 돼요.",
         "쥐띠라면 친구와 나눠 낼 돈, 빌려준 돈은 '이번 달 25일까지 보내 줄 수 있어?'처럼 날짜를 넣어 문자로 남겨 두세요.") + MID
sec3 = P("<b>나무의 띠에게 해의 불은 솜씨, 해의 흙은 돈이에요.</b>",
         "나무는 불을 키우고, 불은 흙을 데워요. 그래서 호랑이띠·토끼띠에게 2027년은 내가 만든 결과물이 돈으로 이어지는 모양이에요.",
         "말솜씨, 손재주, 쌓아 둔 기술처럼 내 안에서 나가는 것이 먼저 움직이고, 그 뒤에 돈이 따라와요.") + \
       P("호랑이(寅)띠는 1974·1986·1998·2010년생이에요. 힘 쓸 달은 6월·10월·11월이에요. 보여 줄 결과물 하나에 값을 먼저 정해 두면 좋아요.",
         "토끼(卯)띠는 1975·1987·1999·2011년생이에요. 토끼는 돼지·양과 한 팀(삼합)이기도 해서, 혼자 버는 돈보다 함께 만드는 돈이 커요. 힘 쓸 달은 7월·10월·11월이에요.",
         "다만 솜씨를 많이 꺼내는 해라 지치기 쉬워요. 견적을 낼 때 '수정은 두 번까지예요'처럼 일의 끝을 같이 적어 두세요.")
sec4 = P("<b>양(未)과 손잡는 띠는 돈보다 사람이 먼저 와요.</b>",
         "열두 띠에는 서로 한 팀이 되는 사이(삼합)와 짝을 이루는 사이(육합)가 있어요. 양과 한 팀은 돼지·토끼, 양과 짝은 말이에요.",
         "이 띠들은 2027년에 소개, 동업, 좋은 조건의 제안처럼 사람을 거쳐 돈이 들어오는 일이 많아요.") + \
       P("말(午)띠는 1978·1990·2002·2014년생이에요. 말은 불이라 해의 흙이 솜씨가 되고, 양과 짝까지 이루니 둘이 손잡는 일에 힘이 실려요. 힘 쓸 달은 2월·7월·10월이에요.",
         "사람을 거쳐 오는 돈은 말로 정하고 끝나기 쉬워요. 제안을 받으면 '조건을 메일로 한 번 정리해 주실 수 있을까요?'라고 물어 두세요.")
sec5 = P("<b>나머지 띠는 해 글자가 돈 대신 다른 일을 맡겨요.</b>",
         "뱀띠·말띠에게 해의 불은 같은 편이에요. 같이 쓰는 사람이 늘어나는 모양이라 모임비, 경조사비처럼 나눠 내는 돈이 커지기 쉬워요.",
         "소·용·양·개띠에게 해의 불은 문서와 도움이에요. 자격증, 계약, 집 문서처럼 종이로 남는 일이 돈을 지켜 줘요. 대신 해의 흙은 같은 편이라 함께 쓰는 돈도 늘어요.",
         "원숭이띠·닭띠에게 해의 불은 책임이에요. 일이 무거워지는 만큼 평가가 따라오니, 맡은 일의 성과를 숫자로 적어 두면 연봉 이야기 때 힘이 돼요.") + "[[S]]" + \
       P("⚠️ 소(丑)띠는 양과 정면으로 마주 보는 자리(충)라 이사·이직처럼 큰돈이 움직이는 일이 생기기 쉬워요. 아낄 달 6월·7월에는 큰 결제를 한 번 미뤄 보세요.",
         "⚠️ 개(戌)띠는 소·양과 함께 조율이 필요한 세 글자(형)에 들어가요. 보증이나 명의를 빌려주는 일은 아낄 달 4월·5월이 아니어도 한 번 더 생각해 보세요.",
         "조심할 곳을 아는 건 돈이 안 들어온다는 뜻이 아니에요. 어디로 새는지 먼저 알면 막을 수 있다는 뜻이에요.")
sec6 = P("🧠 <b>오를 월급의 일부를 미리 저축으로 정해 두면, 쓰는 돈을 줄이는 아픔 없이 모으는 돈이 늘어요.</b>",
         "행동경제학자 세일러와 베나치는 2004년, 월급이 오를 때마다 오른 몫의 일부를 저축으로 옮기겠다고 미리 약속하게 하는 방법(Save More Tomorrow)을 한 회사에서 시험했어요.",
         "제안받은 사람의 78%가 가입했고, 80%는 네 번째 월급 인상 때까지 계속했어요. 40개월 동안 평균 저축 비율은 3.5%에서 13.6%로 올랐어요.") + "[[B]]" + \
       P("지금 쓰는 돈을 줄이라고 하면 손해처럼 느껴져요. 아직 받지 않은 돈을 미리 나누면 그 아픔이 훨씬 작아요.",
         "띠별 힘 쓸 달도 같은 방식으로 쓰면 좋아요. 돈이 들어올 달을 알면, 들어오기 전에 어디로 보낼지 먼저 정해 둘 수 있어요.",
         '📚 <b>출처 1</b>: <a href="https://doi.org/10.1086/380085">Thaler &amp; Benartzi (2004), Save More Tomorrow: Using Behavioral Economics to Increase Employee Saving, Journal of Political Economy 112(S1)</a>',
         '📚 <b>출처 2</b>: <a href="https://astro.kasi.re.kr/life/pageView/5">한국천문연구원 천문우주지식정보, 음양력 변환</a>') + \
       P("🌱 <b>마음 코치 정월의 질문</b>", "2027년에 돈이 들어온다면<br>가장 먼저 어디로 보내고 싶나요?",
         "🔸 그 돈이 들어오기 전에<br>오늘 미리 정해 둘 수 있는 것은 무엇일까요?") + \
       P("✔️ <b>2027년 돈 길을 준비하며 해 볼 것</b>",
         "1. 내 띠가 세 갈래 가운데 어디에 드는지 확인하고, 힘 쓸 달을 달력에 적어 두세요.",
         "2. 다음에 월급이나 수입이 오르면, 오른 몫의 절반이 적금으로 가도록 자동이체 날짜를 지금 정해 두세요.",
         "3. 사람을 거쳐 오는 돈과 나눠 내는 돈은 금액과 날짜를 문자나 메일로 남겨 두세요.")
sec7 = P("<b>Q. 띠가 세 갈래에 없으면 2027년 돈이 안 들어오나요?</b>",
         "A. 아니에요. 띠는 태어난 해 글자 하나만 본 거예요. 돈의 흐름은 태어난 날의 글자(일간)까지 봐야 내 몫이 보여요. 띠는 큰 방향을 잡는 첫 칸으로 써 주세요.") + \
       P("<b>Q. 2027년 돈의 해는 언제부터 시작돼요?</b>",
         "A. 사주에서 해는 입춘에 바뀌어요. 2027년 입춘은 2월 4일 오전 10시 46분이에요. 그 전, 1월에 들어오는 연말 보너스는 아직 2026년 병오년 기운으로 봐요.") + \
       P("<b>Q. 1월이나 2월 초에 태어났으면 무슨 띠로 봐요?</b>",
         "A. 태어난 해의 입춘보다 먼저 태어났으면 앞 해 띠예요. 위의 1996년 2월 4일생처럼 같은 날이어도 시각에 따라 갈려요. 헷갈리면 태어난 날을 넣어 해 글자를 직접 확인해 보세요.")
tail = P("여러분의 띠는 세 갈래 가운데 어디에 들었나요?", "불, 흙, 손잡는 사람 가운데 하나를 띠와 함께 댓글로 남겨 주세요.") + \
       '<p><b>👇 띠별 운세에서 내 띠의 힘 쓸 달과 아낄 달까지 보고 싶다면, 2027 띠별 운세, 정미년 12띠 힘 쓸 달과 아낄 달 한눈에</b></p>'
secs = [sec1, sec2, sec3, sec4, sec5, sec6, sec7]

def _have(n): return os.path.exists(os.path.join(HERE, "img", n))
def build():
    for d_ in ("wide", "m1280", "master"): os.makedirs(os.path.join(HERE, "img", d_), exist_ok=True)
    c = V.Ctx(PAL); made = []
    a4 = f"wide/naver_z{KEY}_a4.jpg"
    if not _have(a4):
        V.render(PID + "_new", {"d": "N", "el": "나무", "kick": "2027년 재물운", "hook": ["해 글자 두 개로", "찾는 돈 길"], "sub": "내 띠는 어느 갈래일까",
                                "items": ["쥐·돼지", "호랑이·토끼", "말"]}, os.path.join(HERE, "img", a4), PAL)
    made.append(a4)
    nm = {"F": f"naver_z{KEY}_k9.jpg", "S": f"naver_z{KEY}_s8.jpg", "B": f"naver_z{KEY}_b7.jpg"}
    if not _have(nm["F"]):
        DGB.fork(nm["F"], c, "2027년 돈이 들어오는 세 갈래", "2027년 해 글자, 불과 흙",
                 ["불이 돈|쥐·돼지", "흙이 돈|호랑이·토끼", "손잡는 띠|돼지·토끼·말"], "돼지띠·토끼띠는 두 갈래에 함께 들어가요")
    if not _have(nm["S"]):
        DG.sides(nm["S"], c, "해 글자 두 개가 내 띠에 주는 것", "해의 불", "해의 흙",
                 [(e, ROLE[e][0], ROLE[e][1]) for e in ("물", "나무", "불", "흙", "쇠")], "가운데 칸은 내 띠의 기운이에요")
    if not _have(nm["B"]):
        DGC.bignum(nm["B"], c, "오를 월급을 미리 나눠 두면", "3.5% → 13.6%", "40개월 뒤 평균 저축 비율",
                   [("가입", "제안받은 사람 가운데 78%가 가입했어요"), ("유지", "80%가 네 번째 월급 인상 때까지 계속했어요"),
                    ("방법", "월급이 오를 때마다 오른 몫의 일부를 저축으로 먼저 옮겼어요")], "Thaler & Benartzi (2004)")
    import fullbleed as FBL
    plan_p = os.path.join(HERE, "fullbleed_plan.json"); plan = json.load(open(plan_p, encoding="utf-8")) if os.path.exists(plan_p) else {}
    rows = []
    for pos, k in enumerate("FSB", 1):
        f = nm[k][:-4] + "f.jpg"
        if not _have(f):
            r, why = FBL.convert(nm[k], [os.path.join(HERE, "img"), os.path.join(HERE, "img", "m1280")])
            if not r: print("fullbleed 건너뜀", nm[k], why); made.append(nm[k]); continue
        rows.append({"pos": pos, "old": nm[k], "new": f}); made.append(nm[k]); nm[k] = f
        reg_ = json.load(open(DG.REG, encoding="utf-8")); reg_[f] = reg_[rows[-1]["old"]]; json.dump(dict(sorted(reg_.items())), open(DG.REG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    plan[PID] = rows; json.dump(plan, open(plan_p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    made += [v for v in nm.values() if v not in made]
    alt = {"F": "2027년 돈이 들어오는 세 갈래 그림. 해 글자 丁 불이 돈인 쥐띠·돼지띠, 未 흙이 돈인 호랑이띠·토끼띠, 양과 손잡는 돼지띠·토끼띠·말띠",
           "S": "해 글자 두 개가 띠 기운에 주는 것 표. 물은 불이 돈·흙이 책임, 나무는 불이 솜씨·흙이 돈, 불은 불이 같은 편·흙이 솜씨, 흙은 불이 문서·흙이 같은 편, 쇠는 불이 책임·흙이 문서",
           "B": "세일러와 베나치 2004년 연구 그림. 오를 월급의 일부를 미리 저축으로 정하게 하자 78%가 가입하고 80%가 계속했으며 40개월 뒤 평균 저축 비율이 3.5%에서 13.6%로 올랐어요"}
    body = P(*head) + P("<b>📌 내 띠의 돈 길을 찾는 순서</b>", *[f"{i + 1}. {q}" for i, q in enumerate(toc_q)])
    for i, (q, s) in enumerate(zip(toc_q, secs)):
        for k in "FSB": s = s.replace(f"[[{k}]]", IMG(nm[k], alt[k]))
        body += H(f"{i + 1}. {q}") + s
    body += tail + CTA
    import copy_rules as CR
    for w in ("재미로", "상담", "—", "안녕하세요, 자오선의 정월이에요", "결론부터 말씀드릴게요", "생년월일만 넣으면 1초", "한 줄 요약", "이 글의 순서", "수비학으로 겹쳐 보면", "TOP3") + tuple(CR.금지어):
        assert w not in re.sub(r"<[^>]+>", " ", body), w
    for f in made:   # 사이트 사본(K-069)
        dst = os.path.join(SITE, "public", "naver", "img", f); os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy(os.path.join(HERE, "img", f), dst)
    return body, a4, made

TITLE = "2027년 재물운 좋은 띠, 해 글자로 보는 돈 길 3가지"
TAGS = ["2027년재물운", "재물운좋은띠", "재물운", "2027재물운", "띠별재물운", "돈들어오는띠", "정미년", "2027년운세", "저축", "자오선"]
REL = {"id": "n80", "title": "2027 띠별 운세, 정미년 12띠 힘 쓸 달과 아낄 달 한눈에",
       "phrase": "띠별 운세에서 내 띠의 힘 쓸 달과 아낄 달까지 보고 싶다면, 2027 띠별 운세, 정미년 12띠 힘 쓸 달과 아낄 달 한눈에",
       "url": "https://blog.naver.com/zaoseon/224461125363"}
KW_VOL = json.load(open(os.path.join(SITE, "data", "keywords", "kw_volume.json"), encoding="utf-8"))["posts"]["n90"]["씨앗"]
INTENT = {"keywords": ["2027년재물운", "재물운좋은띠", "재물운"],
          "keyword_src": "kw-volume 작업(data/keywords/kw_volume.json posts.n90) 월 검색량 · n05 조회 순위(재발행 일정 '새 글로 다시 쓰기')",
          "intent": "알고 싶다", "intent_note": "2027년에 돈이 들어오는 띠가 어디인지, 왜 그런지를 해 글자 두 개(丁 불·未 흙)와 띠 관계로 바로 찾고, 내 띠가 할 일까지 보기",
          "first3": "2027년 재물운 좋은 띠는 해의 두 글자 丁(불)과 未(흙) 가운데 하나를 내 돈으로 쓰는 띠예요.",
          "answer_keys": ["재물운", "쥐띠·돼지띠", "호랑이띠·토끼띠"],
          "order": toc_q[:6], "images": ["돈 길 세 갈래(fork)", "해 글자 두 개가 띠 기운에 주는 것(sides, 오행 계산)", "오를 월급 미리 나누기 연구(bignum)"],
          "related": "n80", "cta": PID, "experience": [], "applied": True,
          "differs_from_n05": "제목·도입(정의 + 세 갈래 직답)·소제목 순서·순위 TOP3 대신 해 글자 두 개로 세 갈래(丁이 돈 쥐·돼지 / 未가 돈 호랑이·토끼 / 未와 합 돼지·토끼·말)·예시 장면(1996.2.4 저녁 8시 돼지띠 · 밤 10시 30분 쥐띠, 입춘 22:07)·나머지 띠는 해 글자가 맡기는 일·그림 유형(fork·sides·bignum)·심리 개념(심적 회계 → Save More Tomorrow, Thaler & Benartzi 2004)·출처·연결글(→ n80)·수비학·여섯 운명학 단락 뺌"}

if __name__ == "__main__":
    body, a4, made = build()
    reg = json.load(open(MP.REG, encoding="utf-8"))
    assert PID not in reg or not reg[PID].get("done"), "이미 예약 끝난 글"
    reg[PID] = dict(dt="2027-02-03T08:00:00", dt_tbd="CT가 정함(재발행 일정 11/20 18:00 자리). 이 날짜는 자리값", title=TITLE, tags=TAGS, body=body,
                    cover=a4, related=REL, thumbs=None, cid=None, clips=None, category="2027 운세", done=False, kw_vol=KW_VOL,
                    k131="n90 11/7(K-151 새 글)", source="build_naver_90.py (n05 주제 새 글, n05 그대로)")
    json.dump(reg, open(MP.REG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    ic = json.load(open(os.path.join(HERE, "intent_cards.json"), encoding="utf-8")); ic["cards"][PID] = INTENT
    json.dump(ic, open(os.path.join(HERE, "intent_cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    v = reg[PID]
    MP.write_page(PID, D.datetime.fromisoformat(v["dt"]), v["title"], v["tags"], v["body"], None, v["cover"], v["related"], v["category"])
    MP.write_index()
    import k151_check as K
    print(PID, len(TITLE), "자 제목 · 본문 글자", len(re.sub(r"<[^>]+>|&nbsp;", "", body)), "· 사진", made, "· K 검사", K.check(PID, v))
