"""네이버 n95: 2027년 소띠 운세 새 글 (CT 11/4 19:40 재발행 일정 '새 글로 다시 쓰기' n06 → n95, 진행표 docs/네이버_누락글_진행표_2026-11-18.md 둘째 줄, CT 11/18 11:3x).
- 왜: 노출 안 되는 옛 글 n06(2027년 소띠 운세, 양띠와 충 드는 해 이사·이직 월별 총정리)을 새 글로. n06은 건드리지 않는다(K-147·K-178).
- 검색어: data/keywords/kw_volume.json — posts.n83 연관상위 소띠운세 45,000 · posts.plan_띠 2027소띠운세 80. (posts.n95 씨앗은 아직 없음 → 발행 7일 뒤 검색어로 고침, K-143)
- 다르게 쓴 것(K-151): n06의 인사·'결론부터'·한 줄 요약 줄·행운 색/숫자/방향·12달 나열·수비학·여섯 운명학·현상 유지 편향 대신
  丑未 충을 '창고 글자끼리 부딪혀 묵은 창고가 열린다'로 풀고(지장간 癸辛己·丁乙己), 해의 丁 불 = 소(흙)에게 문서·도움,
  움직일 때 다섯 번(5·9·12월 / 6·7월, 절기 날짜), 태어난 해별 하늘 글자(辛·癸·乙·丁·己)가 丁에게서 받는 것, 예시 = 1997년 1월 20일생(쥐띠)·2월 10일생(소띠).
  심리 = 새 출발 효과(Dai, Milkman & Riis 2014). 그림 유형 fork·ladder·vbar. 연결글 → n83(발행·노출 '예'). 띠 글 꼬리 '힘 쓸 달·아낄 달 총정리' 안 씀.
- 계산: 해 간지·띠 관계·하늘 글자 관계는 assert, 좋은 달·조심할 달은 사이트 tools/tti_extra.json(n80·n06과 같은 값), 절기·입춘·연주는 engine/engine.py, 지장간은 engine/appx.JJG.
- 출처 2개(K-162, 11/18 확인): Dai, Milkman & Riis (2014) Management Science, DOI 10.1287/mnsc.2014.1901
  (와튼 원문 PDF: 구글 'diet' 검색 새 주 +14.4% · 새 달 +3.7% · 새해 +82.1%, 헬스장 방문 새 주 +33.4%) · 한국천문연구원 음양력 변환(입춘·절기 시각).
- 날짜: CT가 정한다. pages.json dt 는 자리값, dt_tbd 로 표시.
사용: SITE=<zaoseon-site> python3 naver/build_naver_95.py"""
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
       '<tr><td style="padding:12px 10px;text-align:center;border:1px solid #d0d0d0"><b>1월생이라 내 띠가 헷갈린다면</b></td></tr>'
       '<tr><td style="padding:12px 10px;text-align:center;border:1px solid #d0d0d0"><span style="color:#9a9a9a">[ 1997 . 01 . 20 ]</span></td></tr>'
       '<tr><td style="padding:12px 10px;text-align:center;border:1px solid #d0d0d0"><b><a href="https://zaoseon.com/?utm_source=naver&amp;utm_medium=mid#free">내 태어난 날 글자 보기 →</a></b></td></tr>'
       '</tbody></table>' + BL)
CTA = ('<p><a href="https://zaoseon.com/?utm_source=naver&utm_medium=cta#free"><img src="' + RAW +
       'naver_cta5_1%EC%B4%88%EB%AC%B4%EB%A3%8C%ED%92%80%EC%9D%B4.jpg" alt="자오선 무료 1초 풀이 안내 배너"></a></p>')
PID, KEY, PAL = "n95", "95", "y_olive_s"   # 소(丑)·양(未) = 흙 → 흙 판 묶음(EL_SET 흙), n93 y_black_d · n94 p_purple_s · n88 y_black_s 와 다른 판

# ───────── 계산값과 검산
import datetime as D
BR = "子丑寅卯辰巳午未申酉戌亥"; GAN = "甲乙丙丁戊己庚辛壬癸"
assert GAN[(2027 - 4) % 10] + BR[(2027 - 4) % 12] == "丁未"
GEL = dict(zip(GAN, "나무 나무 불 불 흙 흙 쇠 쇠 물 물".split()))
GEUK = {"물": "불", "불": "쇠", "쇠": "나무", "나무": "흙", "흙": "물"}
SAENG = {"물": "나무", "나무": "불", "불": "흙", "흙": "쇠", "쇠": "물"}
def role(me, it):
    if it == me: return "같은 편"
    if GEUK[me] == it: return "손에 쥐는 돈"
    if SAENG[me] == it: return "솜씨·표현"
    if GEUK[it] == me: return "책임·규칙"
    assert SAENG[it] == me; return "문서·도움"
assert role("흙", "불") == "문서·도움" and role("흙", "흙") == "같은 편"                 # 소(丑 흙)에게 丁 불·未 흙
O, Y = BR.index("丑"), BR.index("未"); assert (O + 6) % 12 == Y                          # 丑未 충(마주 봄)
LIUHE = {0: 1, 2: 11, 3: 10, 4: 9, 5: 8, 6: 7}; LIUHE.update({v: k for k, v in list(LIUHE.items())})
WONJIN = {0: 7, 1: 6, 2: 9, 3: 8, 4: 11, 5: 10}; WONJIN.update({v: k for k, v in list(WONJIN.items())})
assert LIUHE[O] == BR.index("子") and WONJIN[O] == BR.index("午") and {BR.index("巳"), BR.index("酉"), O} == {5, 9, 1}   # 육합 子丑 · 원진 丑午 · 삼합 巳酉丑
MB = {m: BR[m % 12] for m in range(1, 13)}                                               # 2월 寅 … 12월 子, 1월 丑
assert MB[5] == "巳" and MB[6] == "午" and MB[7] == "未" and MB[9] == "酉" and MB[12] == "子"
sys.path.insert(0, os.path.join(SITE, "engine")); import engine as E
from appx import JJG
assert JJG["丑"] == "癸辛己" and JJG["未"] == "丁乙己"
YRS = [1949 + 12 * k for k in range(7)]; assert all(BR[(y - 4) % 12] == "丑" for y in YRS)
STEM = {y: GAN[(y - 4) % 10] for y in (1961, 1973, 1985, 1997, 2009)}
assert STEM == {1961: "辛", 1973: "癸", 1985: "乙", 1997: "丁", 2009: "己"}
for y, s in STEM.items(): assert E.compute_saju(D.datetime(y, 6, 1, 12))["팔자"]["년주"] == s + "丑"
ROLE_Y = {y: role(GEL[s], "불") for y, s in STEM.items()}
assert ROLE_Y == {1961: "책임·규칙", 1973: "손에 쥐는 돈", 1985: "솜씨·표현", 1997: "같은 편", 2009: "문서·도움"}
EX = json.load(open(os.path.join(SITE, "tools", "tti_extra.json"), encoding="utf-8"))
assert EX["ox"]["good"] == ["5월", "9월", "12월"] and EX["ox"]["care"] == ["6월", "7월"]
T27 = dict((n, t) for n, _, t in E.get_solar_terms_kst(2027))
for n, (mo, dd) in {"입춘": (2, 4), "입하": (5, 6), "망종": (6, 6), "소서": (7, 7), "백로": (9, 8), "대설": (12, 7)}.items():
    assert (T27[n].month, T27[n].day) == (mo, dd), (n, T27[n])
assert (T27["입춘"].hour, T27["입춘"].minute) == (10, 46)
T28 = dict((n, t) for n, _, t in E.get_solar_terms_kst(2028)); assert (T28["소한"].month, T28["소한"].day) == (1, 6)
L97 = dict((n, t) for n, _, t in E.get_solar_terms_kst(1997))["입춘"]; assert (L97.month, L97.day, L97.hour) == (2, 4, 4)
assert E.compute_saju(D.datetime(1997, 1, 20, 12))["팔자"]["년주"] == "丙子"     # 1월 20일생 = 쥐띠
assert E.compute_saju(D.datetime(1997, 2, 10, 12))["팔자"]["년주"] == "丁丑"     # 2월 10일생 = 소띠
print("해 간지·충·육합·원진·삼합·지장간·하늘 글자·좋은 달·절기·입춘·연주 다시 확인")

# ───────── 본문 (n06 문장을 옮기지 않았다)
head = ["<b>2027년 소띠 운세는 해의 양(未)이 소(丑)와 마주 보고 부딪혀, 오래 묵혀 둔 일이 움직이는 해예요.</b>",
        "소와 양은 둘 다 흙이지만 소는 겨울 흙, 양은 여름 흙이에요. 사주에서는 마주 보는 두 글자가 만나는 것을 충(沖)이라고 하고, 소와 양처럼 창고 글자끼리 부딪히면 닫혀 있던 창고가 열린다고 봐요.",
        "<b>움직이기 좋은 때는 5월·9월·12월, 쉬어 갈 때는 6월·7월이에요.</b>",
        "해의 다른 글자 丁 불은 흙인 소에게 문서와 도움의 글자예요. 그래서 2027년 소띠는 미뤄 둔 서류와 자리를 꺼내 정리하고, 도와줄 사람의 손을 잡는 순서가 편해요. 2026년 11월 18일 기준으로 정리한 내용이에요."]
toc_q = ["2027년 소띠 운세, 양과 부딪히면 무엇이 열릴까요?", "소띠는 몇 년생이고, 1월생은 어떻게 볼까요?",
         "묵은 창고가 열리면 무엇부터 꺼낼까요?", "왜 5월·9월·12월에 움직이고 6월·7월에 쉴까요?",
         "태어난 해마다 해의 불에게서 받는 것은 무엇일까요?", "새해가 되면 왜 다시 시작하고 싶어질까요?", "소띠가 자주 묻는 질문"]
sec1 = P("<b>소(丑)와 양(未)은 둘 다 속에 글자 세 개를 품은 창고 글자예요.</b>",
         "소 안에는 癸·辛·己(물·쇠·흙), 양 안에는 丁·乙·己(불·나무·흙)가 들어 있어요. 평소에는 겉의 흙에 덮여 잘 보이지 않아요.",
         "두 창고가 정면으로 부딪히면 속에 있던 글자들이 밖으로 나와요. 그래서 2027년 소띠에게는 몇 년째 '언젠가'로 미뤄 둔 일이 다시 눈앞에 올라오기 쉬워요.") + "[[F]]" + \
       P("충이라는 말 때문에 겁먹을 필요는 없어요. 움직임이 커지는 해라는 뜻이라, 미뤄 둔 이사나 이직, 정리하고 싶던 일이 있다면 꺼낼 기회가 돼요.",
         "다만 흔들림이 큰 만큼 한꺼번에 여러 개를 바꾸면 지치기 쉬워요. 올해 바꿀 것은 하나나 둘로 정해 두면 좋아요.")
sec2 = P("<b>소띠는 1949·1961·1973·1985·1997·2009·2021년생이에요.</b>",
         "다만 사주에서 해는 1월 1일이 아니라 입춘에 바뀌어요. 그래서 1월생과 2월 초에 태어난 사람은 앞 해 띠일 수 있어요.") + \
       P("🔎 1997년 1월 20일에 태어난 사람을 떠올려 볼게요. 그해 입춘은 2월 4일 새벽 4시쯤이었어요.",
         "1월 20일은 입춘 전이라 해 기둥이 1996년의 丙子, 띠는 쥐띠예요. 같은 1997년생이라도 2월 10일생은 입춘 뒤라 丁丑, 소띠예요.",
         "주민등록상 1997년생인데 친구들과 띠 이야기가 엇갈렸다면, 태어난 날이 입춘 전인지 먼저 확인해 보세요.") + MID
sec3 = P("<b>창고가 열리는 해에는 꺼낼 것 하나, 비울 것 하나, 물어볼 사람 하나를 정해 두면 좋아요.</b>",
         "흔들림이 오기 전에 내가 먼저 고르면, 올라오는 일에 끌려다니지 않고 고른 일부터 처리할 수 있어요.") + \
       P("<b>꺼낼 것</b>: 몇 년째 미뤄 둔 일 하나를 적어요. 이사, 부서 이동 신청, 자격증 시험처럼 '언젠가 해야지' 했던 것이에요.",
         "<b>비울 것</b>: 창고 자리만 차지하는 것을 하나 정리해요. 안 쓰는 정기 구독, 몇 년째 열지 않은 짐 상자, 끝난 모임의 단체 대화방 같은 것이에요.",
         "<b>물어볼 사람</b>: 해의 丁 불은 소에게 문서와 도움이에요. 계약서, 추천서, 자격처럼 종이로 남는 일에 힘이 실려요. 꺼낸 일을 먼저 해 본 사람 한 명에게 '처음에 뭐부터 했어?' 하고 물어보세요.") + \
       P("셋을 한 장에 적어 냉장고나 모니터 옆에 붙여 두면, 6월·7월처럼 흔들리는 달에도 무엇을 붙잡을지 헷갈리지 않아요.")
sec4 = P("<b>소띠가 2027년에 움직이기 좋은 달은 5월·9월·12월, 쉬어 갈 달은 6월·7월이에요.</b>",
         "사주의 달은 1일이 아니라 절기로 바뀌어요. 달마다 그달을 맡은 띠 글자가 있어서, 그 글자와 소의 사이로 달을 골라요.") + "[[M]]" + \
       P("⭐ 5월 6일 입하부터는 뱀(巳)의 달이에요. 뱀·닭·소는 한 팀(삼합)이라, 꺼낸 일을 같이 할 사람이나 새 자리 이야기가 들어오기 쉬워요.",
         "⭐ 9월 8일 백로부터는 닭(酉)의 달이에요. 한 팀의 마지막 글자가 들어와, 5월에 시작한 일이 결과로 보이기 쉬워요.",
         "⭐ 12월 7일 대설부터는 쥐(子)의 달이에요. 쥐와 소는 짝을 이루는 사이(육합)라, 한 해를 정리하고 다음 약속을 잡기 좋아요.") + \
       P("⚠️ 6월 6일 망종부터는 말(午)의 달이에요. 말과 소는 서운함이 쌓이기 쉬운 사이(원진)라, 같이 일하는 사람과 말이 엇갈리기 쉬워요.",
         "⚠️ 7월 7일 소서부터는 양(未)의 달이에요. 해의 글자가 달에 한 번 더 들어와 부딪힘이 가장 크게 느껴져요. 큰 계약 서명은 한 달쯤 미뤄 9월 백로 뒤로 잡아 보세요.",
         "쉬어 갈 달은 나쁜 달이 아니라 속도를 줄이는 달이에요. 6월과 7월에는 일정 사이에 빈 날을 하루씩 넣어 두세요.",
         "2028년 1월 6일 소한부터는 소(丑)의 달, 내 띠의 달이에요. 1년 동안 꺼낸 것을 한 장에 적어 보며 다음 해를 준비해 보세요.")
sec5 = P("<b>같은 소띠라도 태어난 해의 하늘 글자가 달라서, 해의 丁에게서 받는 것이 조금씩 달라요.</b>",
         "🐂 <b>1961년생(신축)</b>: 하늘 글자가 쇠라 해의 불이 책임이에요. 맡는 역할이 늘 수 있어요. 받을 일과 넘길 일을 먼저 나눠 보세요.",
         "🐂 <b>1973년생(계축)</b>: 하늘 글자가 물이라 해의 불이 손에 쥐는 돈이에요. 들어오고 나가는 돈이 함께 커지기 쉬워서, 큰 지출은 두 번 나눠 정해 보세요.",
         "🐂 <b>1985년생(을축)</b>: 하늘 글자가 나무라 해의 불이 말과 표현이에요. 회의나 모임에서 내 생각을 먼저 꺼내기 좋은 해예요.",
         "🐂 <b>1997년생(정축)</b>: 하늘 글자가 해와 같은 丁이라 같은 편이 늘어요. 같이 하자는 사람이 많아지는 만큼, 오래 갈 사람을 골라 보세요.",
         "🐂 <b>2009년생(기축)</b>: 하늘 글자가 흙이라 해의 불이 문서와 도움이에요. 시험이나 자격처럼 종이로 남는 일에 힘을 실어 보세요.")
sec6 = P("🧠 <b>새해나 새 달처럼 달력에 금이 그어지는 때, 사람은 다시 시작하고 싶어져요. 심리학에서는 이것을 새 출발 효과라고 해요.</b>",
         "와튼 스쿨의 다이, 밀크먼, 리스 연구진은 2014년, 사람들이 언제 '다이어트'를 검색하는지 구글 검색 기록으로 살펴봤어요.",
         "평소와 견주어 새 주가 시작될 때는 14.4%, 새 달에는 3.7%, 새해가 시작될 때는 82.1% 더 많이 찾았어요.") + "[[B]]" + \
       P("같은 연구에서 대학 헬스장에 가는 비율도 새 주의 첫날에 33.4% 높았어요.",
         "지난 일과 나 사이에 금이 그어지면 '이제부터는 다르게'라는 마음이 쉽게 생겨요.",
         "소띠에게 2027년은 해 글자가 대신 그어 주는 금 같은 해예요. 입춘이나 5월 입하처럼 금이 그어지는 날에 꺼낼 것 하나를 시작해 보세요.",
         '📚 <b>출처 1</b>: <a href="https://doi.org/10.1287/mnsc.2014.1901">Dai, Milkman &amp; Riis (2014), The fresh start effect: Temporal landmarks motivate aspirational behavior, Management Science</a>',
         '📚 <b>출처 2</b>: <a href="https://astro.kasi.re.kr/life/pageView/5">한국천문연구원 천문우주지식정보, 음양력 변환</a>') + \
       P("🌱 <b>마음 코치 정월의 질문</b>", "몇 년째 '언젠가'로 미뤄 둔 일은<br>무엇인가요?",
         "🔸 그 일을 2027년에 꺼낸다면<br>어느 달에 첫발을 떼고 싶나요?") + \
       P("✔️ <b>2027년 소띠가 해 볼 것</b>",
         "1. 꺼낼 것·비울 것·물어볼 사람을 한 장에 적어 두세요.",
         "2. 5월 6일 입하 전에, 꺼낼 일을 먼저 해 본 사람 한 명에게 연락해 보세요.",
         "3. 6월과 7월 달력에는 아무 약속 없는 날을 하루씩 미리 표시해 두세요.")
sec7 = P("<b>Q. 충이 드는 해에는 이사하면 안 되나요?</b>",
         "A. 아니에요. 움직임이 큰 해라 미뤄 둔 이사를 꺼내기에 오히려 맞아요. 이 글의 달로 보면 6월·7월보다 5월이나 9월 뒤가 편해요.") + \
       P("<b>Q. 가족이나 동료가 양띠면 사이가 나빠지나요?</b>",
         "A. 띠는 태어난 해 글자 하나만 본 거예요. 양띠와 함께라면 결정을 서두르기 전에 언제까지 정하면 되는지 먼저 물어보며 속도를 한 번 맞춰 보세요.") + \
       P("<b>Q. 2027년 소띠 운세는 언제부터 적용되나요?</b>",
         "A. 사주에서 해는 입춘에 바뀌어요. 2027년 입춘은 2월 4일 오전 10시 46분이에요. 그 전 1월까지는 2026년 병오년 기운으로 봐요.")
tail = P("여러분이 2027년에 꺼내고 싶은 일은 무엇인가요?", "꺼낼 일 하나를 태어난 해와 함께 댓글에 적어 주세요.") + \
       '<p><b>👇 소띠의 띠 궁합을 번호로 바로 찾고 싶다면, 띠 궁합표 한눈에, 12띠 짝과 부딪히는 띠 번호로 찾는 법</b></p>'
secs = [sec1, sec2, sec3, sec4, sec5, sec6, sec7]

def _have(n): return os.path.exists(os.path.join(HERE, "img", n))
def build():
    for d_ in ("wide", "m1280", "master"): os.makedirs(os.path.join(HERE, "img", d_), exist_ok=True)
    c = V.Ctx(PAL); made = []
    a4 = f"wide/naver_z{KEY}_a4.jpg"
    if not _have(a4):
        V.render(PID + "_new", {"d": "N", "el": "흙", "kick": "2027년 소띠 운세", "hook": ["묵은 창고가", "열리는 해"], "sub": "언제 움직이면 좋을까",
                                "items": ["5월", "9월", "12월"]}, os.path.join(HERE, "img", a4), PAL)
    made.append(a4)
    nm = {"F": f"naver_z{KEY}_f3.jpg", "M": f"naver_z{KEY}_l3.jpg", "B": f"naver_z{KEY}_v3.jpg"}
    if not _have(nm["F"]):
        DGB.fork(nm["F"], c, "2027 정미년이 소띠에게 주는 것", "해 글자 丁未 · 내 띠 丑",
                 ["丁 불 · 문서와 도움", "未 흙 · 마주 선 흙", "丑未 충 · 창고가 열림"], "흔들림이 큰 해라 바꿀 것은 하나나 둘로")
    if not _have(nm["M"]):
        DGB.ladder(nm["M"], c, "2027년 소띠의 달 다섯", [
            ("5월 6일", "입하 · 뱀의 달, 한 팀이 모여요"), ("6월 6일", "망종 · 말의 달, 말이 엇갈리기 쉬워요"),
            ("7월 7일", "소서 · 양의 달, 부딪힘이 가장 커요"), ("9월 8일", "백로 · 닭의 달, 결과가 보여요"),
            ("12월 7일", "대설 · 쥐의 달, 짝이 와요")], "절기 날짜 한국천문연구원 · 띠 관계 자오선 계산")
    if not _have(nm["B"]):
        DGC.vbar(nm["B"], c, "'다이어트' 검색이 늘어난 때", [("새 주", 14.4, False), ("새 달", 3.7, False), ("새해", 82.1, True)],
                 90, "새해가 시작될 때는 평소보다 82.1% 더 찾았어요", "Dai, Milkman & Riis (2014) 연구 1 · 평소 날과 견준 증가", fmt="{:.1f}%", step=20)
    import fullbleed as FBL
    plan_p = os.path.join(HERE, "fullbleed_plan.json"); plan = json.load(open(plan_p, encoding="utf-8")) if os.path.exists(plan_p) else {}
    rows = []
    for pos, k in enumerate("FMB", 1):
        f = nm[k][:-4] + "f.jpg"
        if not _have(f):
            r, why = FBL.convert(nm[k], [os.path.join(HERE, "img"), os.path.join(HERE, "img", "m1280")])
            if not r: print("fullbleed 건너뜀", nm[k], why); made.append(nm[k]); continue
        rows.append({"pos": pos, "old": nm[k], "new": f}); made.append(nm[k]); nm[k] = f
        reg_ = json.load(open(DG.REG, encoding="utf-8")); reg_[f] = reg_[rows[-1]["old"]]; json.dump(dict(sorted(reg_.items())), open(DG.REG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    plan[PID] = rows; json.dump(plan, open(plan_p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    made += [v for v in nm.values() if v not in made]
    alt = {"F": "2027 정미년이 소띠에게 주는 것 그림. 丁 불은 문서와 도움, 未 흙은 마주 보는 같은 흙, 丑未 충은 묵은 창고가 열리는 것",
           "M": "2027년 소띠의 달 다섯 그림. 5월 6일 뱀의 달, 6월 6일 말의 달, 7월 7일 양의 달, 9월 8일 닭의 달, 12월 7일 쥐의 달",
           "B": "새 출발 효과 연구 그림. 다이어트 검색이 새 주 14.4%, 새 달 3.7%, 새해 82.1% 늘었어요"}
    body = P(*head) + P("<b>📌 2027년 소띠가 읽을 순서</b>", *[f"{i + 1}. {q}" for i, q in enumerate(toc_q)])
    for i, (q, s) in enumerate(zip(toc_q, secs)):
        for k in "FMB": s = s.replace(f"[[{k}]]", IMG(nm[k], alt[k]))
        body += H(f"{i + 1}. {q}") + s
    body += tail + CTA
    import copy_rules as CR
    for w in ("재미로", "상담", "—", "안녕하세요, 자오선의 정월이에요", "결론부터 말씀드릴게요", "생년월일만 넣으면 1초", "한 줄 요약", "이 글의 순서", "수비학",
              "여섯 운명학", "현상 유지", "총정리", "힘 쓸 달", "아낄 달", "솜씨", "값을 매", "행운") + tuple(CR.금지어):
        assert w not in re.sub(r"<[^>]+>", " ", body), w
    for f in made:   # 사이트 사본(K-069)
        dst = os.path.join(SITE, "public", "naver", "img", f); os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy(os.path.join(HERE, "img", f), dst)
    return body, a4, made

TITLE = "2027년 소띠 운세, 양띠와 부딪히는 해 언제 움직이면 좋을까"
TAGS = ["2027년소띠운세", "소띠운세", "2027소띠운세", "소띠", "정미년", "축미충", "소띠이사", "새출발효과", "띠별운세", "자오선"]
REL = {"id": "n83", "title": "띠 궁합표 한눈에, 12띠 짝과 부딪히는 띠 번호로 찾는 법",
       "phrase": "소띠의 띠 궁합을 번호로 바로 찾고 싶다면, 띠 궁합표 한눈에, 12띠 짝과 부딪히는 띠 번호로 찾는 법",
       "url": "https://blog.naver.com/zaoseon/224465980874"}
_KV = json.load(open(os.path.join(SITE, "data", "keywords", "kw_volume.json"), encoding="utf-8"))["posts"]
KW_VOL = {"소띠운세": _KV["n83"]["연관상위"]["소띠운세"], "2027소띠운세": _KV["plan_띠"]["씨앗"]["2027소띠운세"]}
INTENT = {"keywords": ["2027년소띠운세", "소띠운세", "2027소띠운세"],
          "keyword_src": "kw-volume 작업(data/keywords/kw_volume.json posts.n83 연관상위·posts.plan_띠) 월 검색량 · n06 조회 순위(재발행 일정 '새 글로 다시 쓰기', 진행표 11/18 둘째 줄) · 2027년소띠운세 씨앗은 아직 없음",
          "intent": "알고 싶다", "intent_note": "2027년 소띠에게 어떤 해인지(양띠와 충), 언제 움직이고 언제 쉬면 좋은지, 내 출생 연도와 1월생 띠까지 바로 보기",
          "first3": "2027년 소띠 운세는 해의 양(未)이 소(丑)와 마주 보고 부딪혀, 오래 묵혀 둔 일이 움직이는 해예요.",
          "answer_keys": ["양띠와 충", "움직일 달 5·9·12월", "쉬어 갈 달 6·7월"],
          "order": toc_q[:6], "images": ["해 글자가 주는 것(fork)", "소띠의 달 다섯(ladder, 절기 날짜)", "새 출발 효과(vbar)"],
          "related": "n83", "cta": PID, "experience": [], "applied": True,
          "differs_from_n06": "제목·도입(정의 + 창고가 열리는 충)·소제목 순서·한 줄 요약/행운 색·숫자·방향·12달 나열·수비학 2·여섯 운명학·현상 유지 편향 대신 창고 글자 충(지장간)·꺼낼 것/비울 것/물어볼 사람·움직일 때 다섯 번(절기 날짜)·태어난 해별 하늘 글자·예시(1997.1.20 쥐띠·2.10 소띠)·그림 유형(fork·ladder·vbar)·심리 개념(새 출발 효과, Dai 외 2014)·출처 2개·연결글(→ n83)"}

if __name__ == "__main__":
    body, a4, made = build()
    reg = json.load(open(MP.REG, encoding="utf-8"))
    assert PID not in reg or not reg[PID].get("done"), "이미 예약 끝난 글"
    reg[PID] = dict(dt="2027-02-05T18:00:00", dt_tbd="CT가 정함(재발행 일정 'n06 다시 쓰기' 자리, 진행표 11/18). 이 날짜는 자리값", title=TITLE, tags=TAGS, body=body,
                    cover=a4, related=REL, thumbs=None, cid=None, clips=None, category="2027 운세", done=False, kw_vol=KW_VOL,
                    k131="n95 11/18(K-151 새 글)", source="build_naver_95.py (n06 주제 새 글, n06 그대로)")
    json.dump(reg, open(MP.REG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    ic = json.load(open(os.path.join(HERE, "intent_cards.json"), encoding="utf-8")); ic["cards"][PID] = INTENT
    json.dump(ic, open(os.path.join(HERE, "intent_cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    v = reg[PID]
    MP.write_page(PID, D.datetime.fromisoformat(v["dt"]), v["title"], v["tags"], v["body"], None, v["cover"], v["related"], v["category"])
    MP.write_index()
    import k151_check as K
    print(PID, len(TITLE), "자 제목 · 본문 글자", len(re.sub(r"<[^>]+>|&nbsp;", "", body)), "· 사진", made, "· K 검사", K.check(PID, v))
