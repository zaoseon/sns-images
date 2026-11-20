"""네이버 n103: 2027년 호랑이띠 운세 새 글 (CT 11/4 19:40 재발행 일정 '새 글로 다시 쓰기' n64 → n103, 진행표 docs/네이버_누락글_진행표_2026-11-18.md 열째 줄).
- 왜: 검색에 '다른 글'만 잡히는 옛 글 n64(2027년 호랑이띠 운세, 나를 보여 주는 해 힘 쓸 달과 아낄 달)를 새 글로. n64는 건드리지 않는다(K-147·K-178).
- 검색어: data/keywords/kw_volume.json — posts.plan_삼재 연관상위 호랑이띠운세 16,480 · posts.plan_띠 2027호랑이띠운세 60. (posts.n103 씨앗은 없음 → 발행 7일 뒤 검색어로 고침, K-143)
- 다르게 쓴 것(K-151): n64의 첫 질문·인사·'결론부터'·한 줄 요약·달력 줄·수비학(2+0+2+7)·스포트라이트 효과·분야별 나열·'힘 쓸 달·아낄 달' 대신
  '2028년 삼재가 시작되기 전 마지막 한 해'(寅午戌 → 申酉戌 해, 2028 戊申 들삼재·2029 己酉 눌삼재·2030 庚戌 날삼재·2031 입춘 끝, engine assert),
  끝내 둘 일 세 가지(끝낼 일·모을 사람·보여 줄 것), 달 다섯(6·10·11 / 8·9, tti_extra tiger 와 같은 값, 절기 날짜 assert), 예시 2010.2.3생(소띠)·2.5생(호랑이띠),
  심리 = 실행 의도 '만약 ~하면 ~한다'(Gollwitzer & Sheeran 2006 메타분석). 그림 유형 route·monthgrid·twopanel. 연결글 → n81(2027 삼재띠 언제 끝날까, 11/20 노출 '예').
- 출처 2개(K-162, 11/20 확인): Gollwitzer & Sheeran (2006), Implementation intentions and goal achievement: A meta-analysis of effects and processes,
  Advances in Experimental Social Psychology 38, 69-119, DOI 10.1016/S0065-2601(06)38002-1 (콘스탄츠 대학 연구실 서지 확인. 94개 연구·8,000명 넘게·d=0.65 는
  같은 연구실 Parks-Stamm & Gollwitzer 2009 장(章) 본문에서 확인 — 원 논문 PDF 는 그림 파일이라 글자를 못 읽음) · 한국천문연구원 음양력 변환(절기 시각).
- 날짜: CT가 정한다. pages.json dt 는 자리값, dt_tbd 로 표시.
사용: SITE=<zaoseon-site> python3 naver/build_naver_103.py"""
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
       '<tr><td style="padding:12px 10px;text-align:center;border:1px solid #d0d0d0"><b>2월 초에 태어나 내 띠가 헷갈린다면</b></td></tr>'
       '<tr><td style="padding:12px 10px;text-align:center;border:1px solid #d0d0d0"><span style="color:#9a9a9a">[ 2010 . 02 . 03 ]</span></td></tr>'
       '<tr><td style="padding:12px 10px;text-align:center;border:1px solid #d0d0d0"><b><a href="https://zaoseon.com/?utm_source=naver&amp;utm_medium=mid#free">내 태어난 날 글자 보기 →</a></b></td></tr>'
       '</tbody></table>' + BL)
CTA = ('<p><a href="https://zaoseon.com/?utm_source=naver&utm_medium=cta#free"><img src="' + RAW +
       'naver_cta5_1%EC%B4%88%EB%AC%B4%EB%A3%8C%ED%92%80%EC%9D%B4.jpg" alt="자오선 무료 1초 풀이 안내 배너"></a></p>')
PID, KEY, PAL = "n103", "103", "k_neon_s"   # 호랑이(寅) = 나무 → 나무 판 묶음(EL_SET 나무). n102 g_ivory_s · n100 dg_gold_s · n95 y_olive_s 와 다른 판

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
    if SAENG[me] == it: return "말과 표현"
    if GEUK[it] == me: return "책임"
    assert SAENG[it] == me; return "문서와 도움"
assert role("나무", "불") == "말과 표현" and role("나무", "흙") == "손에 쥐는 돈"      # 호랑이(寅 나무)에게 丁 불·未 흙
T_ = BR.index("寅")
SAMHAP = {BR.index("寅"), BR.index("午"), BR.index("戌")}
assert (T_ + 6) % 12 == BR.index("申")                                                   # 寅申 충
LIUHE = {0: 1, 2: 11, 3: 10, 4: 9, 5: 8, 6: 7}; LIUHE.update({v: k for k, v in list(LIUHE.items())})
WONJIN = {0: 7, 1: 6, 2: 9, 3: 8, 4: 11, 5: 10}; WONJIN.update({v: k for k, v in list(WONJIN.items())})
assert LIUHE[T_] == BR.index("亥") and WONJIN[T_] == BR.index("酉")                       # 육합 寅亥 · 원진 寅酉
SAMJAE = {frozenset(SAMHAP): "申酉戌"}                                                    # 寅午戌 생 → 申酉戌 해 삼재(통용 셈법)
sys.path.insert(0, os.path.join(SITE, "engine")); import engine as E
YZ = {y: E.compute_saju(D.datetime(y, 6, 1, 12))["팔자"]["년주"] for y in (2027, 2028, 2029, 2030, 2031)}
assert YZ == {2027: "丁未", 2028: "戊申", 2029: "己酉", 2030: "庚戌", 2031: "辛亥"}, YZ
assert "".join(YZ[y][1] for y in (2028, 2029, 2030)) == SAMJAE[frozenset(SAMHAP)]
YRS = [1950 + 12 * k for k in range(7)]; assert all(BR[(y - 4) % 12] == "寅" for y in YRS)
STEM = {y: GAN[(y - 4) % 10] for y in (1962, 1974, 1986, 1998, 2010)}
assert STEM == {1962: "壬", 1974: "甲", 1986: "丙", 1998: "戊", 2010: "庚"}
for y, s in STEM.items(): assert E.compute_saju(D.datetime(y, 6, 1, 12))["팔자"]["년주"] == s + "寅"
ROLE_Y = {y: role(GEL[s], "불") for y, s in STEM.items()}
assert ROLE_Y == {1962: "손에 쥐는 돈", 1974: "말과 표현", 1986: "같은 편", 1998: "문서와 도움", 2010: "책임"}, ROLE_Y
EX = json.load(open(os.path.join(SITE, "tools", "tti_extra.json"), encoding="utf-8"))
assert EX["tiger"]["good"] == ["6월", "10월", "11월"] and EX["tiger"]["care"] == ["8월", "9월"]
MB = {m: BR[m % 12] for m in range(1, 13)}
assert BR.index(MB[6]) in SAMHAP and BR.index(MB[10]) in SAMHAP and LIUHE[T_] == BR.index(MB[11])
assert MB[8] == "申" and BR.index(MB[9]) == WONJIN[T_]
T27 = dict((n, t) for n, _, t in E.get_solar_terms_kst(2027))
for n, (mo, dd) in {"입춘": (2, 4), "망종": (6, 6), "입추": (8, 8), "백로": (9, 8), "한로": (10, 8), "입동": (11, 8)}.items():
    assert (T27[n].month, T27[n].day) == (mo, dd), (n, T27[n])
assert (T27["입춘"].hour, T27["입춘"].minute) == (10, 46)
T28 = dict((n, t) for n, _, t in E.get_solar_terms_kst(2028))["입춘"]; assert (T28.month, T28.day, T28.hour) == (2, 4, 16)
T31 = dict((n, t) for n, _, t in E.get_solar_terms_kst(2031))["입춘"]; assert (T31.month, T31.day) == (2, 4)
L10 = dict((n, t) for n, _, t in E.get_solar_terms_kst(2010))["입춘"]; assert (L10.month, L10.day, L10.hour, L10.minute) == (2, 4, 7, 47)
assert E.compute_saju(D.datetime(2010, 2, 3, 12))["팔자"]["년주"] == "己丑"     # 2월 3일생 = 소띠
assert E.compute_saju(D.datetime(2010, 2, 5, 12))["팔자"]["년주"] == "庚寅"     # 2월 5일생 = 호랑이띠
print("해 간지·삼재 셋 해·충·육합·원진·삼합·하늘 글자·좋은 달·절기·입춘·연주 다시 확인")

# ───────── 본문 (n64 문장을 옮기지 않았다)
head = ["<b>2027년 호랑이띠 운세는 2028년 삼재가 시작되기 전 마지막 한 해예요. 새 일을 크게 벌이기보다 하던 일을 끝내고, 같이 갈 사람을 모아 두기 좋은 해예요.</b>",
        "호랑이띠(寅)는 2028년 무신년에 들삼재가 시작돼요. 2027년 해의 첫 글자 丁(불)은 나무인 호랑이가 키워 주는 글자라, 만든 것을 사람들 앞에 내놓기 좋은 해예요.",
        "<b>움직이기 좋은 달은 6월·10월·11월, 속도를 줄일 달은 8월·9월이에요.</b>",
        "절기 날짜는 한국천문연구원 음양력 자료와 같은 방법으로 셈했고, 2026년 11월 20일에 정리했어요."]
toc_q = ["2027년 호랑이띠 운세, 삼재 앞 해라는 건 무슨 뜻일까요?", "호랑이띠는 몇 년생이고, 2월 초에 태어나면 어떻게 볼까요?",
         "왜 6월·10월·11월에 움직이고 8월·9월에 쉴까요?", "삼재 전에 끝내 둘 일 세 가지", "계획을 '만약 ~하면'으로 적으면 왜 더 잘 지킬까요?",
         "호랑이띠가 자주 묻는 질문"]
sec1 = P("<b>삼재는 태어난 해의 띠 묶음으로 세요. 호랑이·말·개띠는 원숭이·닭·개의 해, 3년 동안을 삼재로 봐요.</b>",
         "2028년 무신년(원숭이)이 들삼재, 2029년 기유년(닭)이 눌삼재, 2030년 경술년(개)이 날삼재예요. 2031년 2월 4일 입춘에 신해년이 되면서 끝나요.") + "[[R]]" + \
       P("그래서 2027년은 삼재가 아니에요. 3년 동안 이사·이직·창업 같은 큰 결정을 한꺼번에 몰지 말라는 오래된 셈법이라, 그 전 해에 미뤄 둔 일을 끝내 두면 마음이 가벼워요.",
         "해의 두 글자도 같이 봐요. 丁(불)은 나무가 키워 주는 글자라 말하고 보여 주는 일이 잘 풀려요. 未(흙)는 나무가 거두는 글자라 돈을 받고 쓰는 일이 늘어요.",
         "말할 일과 돈 쓸 일이 같이 많아지는 해라, 들어오는 돈과 나가는 돈을 달마다 한 줄씩 적어 두면 2028년 준비가 쉬워요.")
sec2 = P("<b>호랑이띠는 1950·1962·1974·1986·1998·2010·2022년생이에요.</b>",
         "사주에서 해는 1월 1일이 아니라 입춘에 바뀌어요. 1월생과 2월 초에 태어난 사람은 앞 해 띠일 수 있어요.") + \
       P("🔎 2010년 2월 3일에 태어난 사람을 예로 들어 볼게요. 그해 입춘은 2월 4일 오전 7시 47분이었어요.",
         "2월 3일은 입춘 전이라 해 기둥이 2009년의 己丑, 띠는 소띠예요. 같은 2010년생이라도 2월 5일생은 庚寅, 호랑이띠예요.",
         "학교에서는 2010년생 호랑이띠로 불렸는데 사주를 보니 소띠로 나왔다면, 입춘 시각 때문이에요.") + MID
sec3 = P("<b>사주의 달은 1일이 아니라 절기로 바뀌어요. 달마다 그달을 맡은 띠 글자가 있어서, 그 글자와 호랑이가 어떤 사이인지로 달을 골라요.</b>") + "[[M]]" + \
       P("⭐ 6월 6일 망종부터는 말(午)의 달이에요. 호랑이·말·개는 한 묶음(삼합)이라, 같이 일할 사람이나 소개가 들어오기 쉬워요.",
         "⭐ 10월 8일 한로부터는 개(戌)의 달이에요. 묶음의 마지막 글자가 와서, 6월에 시작한 일이 결과로 보이기 쉬워요.",
         "⭐ 11월 8일 입동부터는 돼지(亥)의 달이에요. 호랑이와 돼지는 짝을 이루는 사이(육합)라 계약이나 약속을 잡기 좋아요. 조건은 문자나 메일로 한 번 더 남겨 두세요.") + \
       P("⚠️ 8월 8일 입추부터는 원숭이(申)의 달이에요. 호랑이와 마주 보고 부딪히는 글자(충)이고, 2028년 해의 글자이기도 해요. 삼재를 한 달 먼저 겪어 보는 달이라, 큰 계약은 10월 한로 뒤로 미뤄 보세요.",
         "⚠️ 9월 8일 백로부터는 닭(酉)의 달이에요. 호랑이와 닭은 서운함이 쌓이기 쉬운 사이(원진)라, 같이 일하는 사람과 말이 어긋나기 쉬워요. 중요한 이야기는 만나서 말하고 메일로 한 번 정리해 두세요.",
         "쉬어 갈 달은 나쁜 달이 아니라 속도를 줄이는 달이에요. 8월과 9월 달력에는 약속 없는 날을 하루씩 먼저 표시해 두세요.")
sec4 = P("<b>삼재 3년 앞에 끝내 둘 일은 세 가지예요. 끝낼 일 하나, 모을 사람 두세 명, 보여 줄 것 하나예요.</b>") + \
       P("<b>끝낼 일</b>: 3년 넘게 미뤄 둔 일 하나를 2027년 안에 끝내요. 이사 날짜 정하기, 자격증 마지막 시험, 대출 갈아타기처럼 날짜가 있는 일이 좋아요.",
         "<b>모을 사람</b>: 6월과 10월, 묶음의 달에 같이 일할 사람 두세 명에게 먼저 연락해요. 삼재 3년 동안 '이건 같이 하자'고 부를 사람이에요.",
         "<b>보여 줄 것</b>: 해의 丁은 호랑이가 키워 주는 글자라, 만든 것을 내놓을 때 반응이 와요. 발표 자료, 작업 모음 파일, 블로그 글처럼 남에게 보여 줄 결과물 하나를 정해 두세요.") + \
       P("셋을 종이 한 장에 적어 2027년 달력 첫 장에 붙여 두면, 8월·9월처럼 속도를 줄이는 달에도 무엇부터 할지 바로 보여요.")
sec5 = P("🧠 <b>계획을 '만약 ○○하면, △△한다'로 적으면 지키는 비율이 올라가요. 심리학에서는 이것을 실행 의도라고 불러요.</b>",
         "심리학자 골비처와 시런은 2006년, 실행 의도를 다룬 94개 연구를 한데 모아 다시 셈했어요. 참여한 사람은 8,000명이 넘었어요.") + "[[T]]" + \
       P("목표만 적은 사람보다 '언제, 어디서, 무엇을'까지 정한 사람이 목표를 더 많이 이뤘어요. 연구진은 이 차이를 중간보다 큰 효과(d=0.65)로 셈했어요.",
         "무엇을 할지 미리 정해 두면, 그 상황이 왔을 때 다시 고민하지 않고 바로 움직이게 돼요.",
         "호랑이띠라면 이렇게 적어 볼 수 있어요. '만약 8월에 이사 이야기가 나오면, 날짜는 10월 한로 뒤로 잡는다.' '만약 6월에 같이 하자는 연락이 오면, 그 주 안에 만나서 할 일을 나눈다.'",
         '📚 <b>출처 1</b>: <a href="https://doi.org/10.1016/S0065-2601(06)38002-1">Gollwitzer &amp; Sheeran (2006), Implementation intentions and goal achievement: A meta-analysis of effects and processes, Advances in Experimental Social Psychology</a>',
         '📚 <b>출처 2</b>: <a href="https://astro.kasi.re.kr/life/pageView/5">한국천문연구원 천문우주지식정보, 음양력 변환</a>') + \
       P("🌱 <b>마음 코치 정월의 질문</b>", "2028년이 오기 전에 꼭 끝내고 싶은 일은<br>무엇인가요?",
         "🔸 그 일을 같이 끝낼 사람을 한 명 고른다면<br>누구에게 먼저 연락하고 싶나요?") + \
       P("✔️ <b>2027년 호랑이띠가 해 볼 것</b>",
         "1. 끝낼 일·모을 사람·보여 줄 것을 종이 한 장에 적어 두세요.",
         "2. 그 아래 '만약 ○○하면, △△한다' 문장을 두 줄 적어 보세요.",
         "3. 6월 6일 망종 전에, 같이 일할 사람 한 명에게 먼저 연락해 보세요.")
sec6 = P("<b>Q. 삼재 앞 해에 이사나 이직을 해도 되나요?</b>",
         "A. 2027년은 삼재가 아니라서 미뤄 둔 이사나 이직을 하기에 오히려 맞는 해예요. 이 글의 달로 보면 8월·9월보다 6월이나 10월·11월이 편해요.") + \
       P("<b>Q. 1986년생과 1998년생은 다르게 보나요?</b>",
         "A. 태어난 해의 첫 글자가 달라서, 2027년의 丁에게서 받는 것이 달라요. 1986년생(병인)은 丁과 같은 불이라 같이 하자는 사람이 늘어요. 1998년생(무인)은 흙이라 丁이 문서·도움 글자예요. 계약서나 추천서 일이 늘어요. 1974년생(갑인)은 말과 표현, 1962년생(임인)은 손에 쥐는 돈, 1950·2010년생(경인)은 맡을 일이 늘어요.") + \
       P("<b>Q. 2027년 호랑이띠 운세는 언제부터 적용되나요?</b>",
         "A. 사주에서 해는 입춘에 바뀌어요. 2027년 입춘은 2월 4일 오전 10시 46분이에요. 그 전 1월까지는 2026년 병오년으로 봐요.")
tail = P("여러분이 2028년 전에 끝내고 싶은 일은 무엇인가요?", "끝낼 일 하나를 태어난 해와 함께 댓글에 적어 주세요.") + \
       '<p><b>👇 2027 삼재띠가 언제 끝나는지도 같이 보고 싶다면, 2027 삼재띠 언제 끝날까, 돼지띠 토끼띠 양띠 날삼재 날짜</b></p>'
TOC_S = ["삼재 앞 해의 뜻", "호랑이띠 나이와 2월 초생", "움직일 달과 쉬어 갈 달", "삼재 전에 끝내 둘 일", "만약 ~하면 계획", "자주 묻는 질문"]
secs = [sec1, sec2, sec3, sec4, sec5, sec6]

def _have(n): return os.path.exists(os.path.join(HERE, "img", n))
def build():
    for d_ in ("wide", "m1280", "master"): os.makedirs(os.path.join(HERE, "img", d_), exist_ok=True)
    c = V.Ctx(PAL); made = []
    a4 = f"wide/naver_z{KEY}_a5.jpg"   # 표지 항목은 한글만(11/18 n96 a4)
    if not _have(a4):
        V.render(PID + "_new", {"d": "N", "el": "나무", "kick": "2027년 호랑이띠 운세", "hook": ["삼재 들기 전", "끝내 둘 일"], "sub": "움직일 달과 쉬어 갈 달",
                                "items": ["6월", "10월", "11월"]}, os.path.join(HERE, "img", a4), PAL)
    made.append(a4)
    nm = {"R": f"naver_z{KEY}_r3.jpg", "M": f"naver_z{KEY}_g3.jpg", "T": f"naver_z{KEY}_t3.jpg"}
    if not _have(nm["R"]):
        DGB.route(nm["R"], c, "호랑이띠 삼재까지 남은 길", [("2027 정미", "끝내 두는 해"), ("2028 무신", "들삼재"), ("2029 기유", "눌삼재"),
                                                       ("2030 경술", "날삼재"), ("2031 입춘", "삼재 끝")])
    if not _have(nm["M"]):
        tag = {6: ("묶음의 달", "up"), 10: ("묶음의 달", "up"), 11: ("짝의 달", "up"), 8: ("부딪히는 달", "dn"), 9: ("서운한 달", "dn")}
        DG.monthgrid(nm["M"], c, "2027년 호랑이띠의 달", [(m, *tag.get(m, ("", None))) for m in list(range(2, 13)) + [1]])
    if not _have(nm["T"]):
        DGB.twopanel(nm["T"], c, "목표만 적을 때와 '만약'까지 적을 때", ("목표만", "올해 꼭 이사하기", 0.25), ("만약 ~하면", "8월에 이야기가 나오면 10월 뒤로 날짜 잡기", 0.6),
                     "94개 연구, 8,000명 넘게 참여 (Gollwitzer & Sheeran 2006)", "상황 하나, 할 일 하나", verb="이렇게 적어요: ")
    import fullbleed as FBL
    plan_p = os.path.join(HERE, "fullbleed_plan.json"); plan = json.load(open(plan_p, encoding="utf-8")) if os.path.exists(plan_p) else {}
    rows = []
    for pos, k in enumerate("RMT", 1):
        f = nm[k][:-4] + "f.jpg"
        if not _have(f):
            r, why = FBL.convert(nm[k], [os.path.join(HERE, "img"), os.path.join(HERE, "img", "m1280")])
            if not r: print("fullbleed 건너뜀", nm[k], why); made.append(nm[k]); continue
        rows.append({"pos": pos, "old": nm[k], "new": f}); made.append(nm[k]); nm[k] = f
        reg_ = json.load(open(DG.REG, encoding="utf-8")); reg_[f] = reg_[rows[-1]["old"]]; json.dump(dict(sorted(reg_.items())), open(DG.REG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    plan[PID] = rows; json.dump(plan, open(plan_p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    made += [v for v in nm.values() if v not in made]
    alt = {"R": "호랑이띠 삼재까지 남은 길 그림. 2027 정미년은 삼재 앞 해, 2028 무신년 들삼재, 2029 기유년 눌삼재, 2030 경술년 날삼재, 2031년 입춘에 끝나요",
           "M": "2027년 호랑이띠의 달 그림. 6월·10월은 묶음의 달, 11월은 짝의 달로 칠했고, 8월은 부딪히는 달, 9월은 서운한 달로 테두리를 그었어요",
           "T": "실행 의도 연구 그림. 목표만 적을 때보다 '만약 ~하면 ~한다'로 상황과 할 일을 같이 적을 때 목표를 더 많이 이뤘어요"}
    body = P(*head) + P("<b>📌 2027년 호랑이띠가 읽을 순서</b>", *[f"{i + 1}. {q}" for i, q in enumerate(TOC_S)])
    for i, (q, s) in enumerate(zip(toc_q, secs)):
        for k in "RMT": s = s.replace(f"[[{k}]]", IMG(nm[k], alt[k]))
        body += H(f"{i + 1}. {q}") + s
    body += tail + CTA
    import copy_rules as CR
    for w in ("재미로", "상담", "—", "안녕하세요, 자오선의 정월이에요", "결론부터 말씀드릴게요", "생년월일만 넣으면 1초", "한 줄 요약", "이 글의 순서", "수비학",
              "스포트라이트", "나를 보여 주는 해", "분야별", "총정리", "힘 쓸 달", "아낄 달", "솜씨", "값을 매", "행운", "기운", "흐름", "편이에요") + tuple(CR.금지어):
        assert w not in re.sub(r"<[^>]+>", " ", body), w
    for f in made:   # 사이트 사본(K-069)
        dst = os.path.join(SITE, "public", "naver", "img", f); os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy(os.path.join(HERE, "img", f), dst)
    return body, a4, made

TITLE = "2027년 호랑이띠 운세, 삼재 들기 전 한 해 언제 움직일까"
TAGS = ["2027년호랑이띠운세", "호랑이띠운세", "2027호랑이띠운세", "호랑이띠", "호랑이띠삼재", "정미년", "들삼재", "실행의도", "띠별운세", "자오선"]
REL = {"id": "n81", "title": "2027 삼재띠 언제 끝날까, 돼지띠 토끼띠 양띠 날삼재 날짜",
       "phrase": "2027 삼재띠가 언제 끝나는지도 같이 보고 싶다면, 2027 삼재띠 언제 끝날까, 돼지띠 토끼띠 양띠 날삼재 날짜",
       "url": "https://blog.naver.com/zaoseon/224462303163"}
_KV = json.load(open(os.path.join(SITE, "data", "keywords", "kw_volume.json"), encoding="utf-8"))["posts"]
KW_VOL = {"호랑이띠운세": _KV["plan_삼재"]["연관상위"]["호랑이띠운세"], "2027호랑이띠운세": _KV["plan_띠"]["씨앗"]["2027호랑이띠운세"]}
INTENT = {"keywords": ["2027년호랑이띠운세", "호랑이띠운세", "2027호랑이띠운세"],
          "keyword_src": "kw-volume 작업(data/keywords/kw_volume.json posts.plan_삼재 연관상위·posts.plan_띠) 월 검색량 · n64 재발행 일정 '새 글로 다시 쓰기'(진행표 11/18 열째 줄) · 2027년호랑이띠운세 씨앗은 아직 없음",
          "intent": "알고 싶다", "intent_note": "2027년 호랑이띠에게 어떤 해인지(2028 삼재 앞 해), 언제 움직이고 언제 쉬면 좋은지, 내 출생 연도와 2월 초생 띠까지 바로 보기",
          "first3": "2027년 호랑이띠 운세는 2028년 삼재가 시작되기 전 마지막 한 해예요. 움직이기 좋은 달은 6월·10월·11월, 속도를 줄일 달은 8월·9월이에요.",
          "answer_keys": ["2028 들삼재 앞 해", "움직일 달 6·10·11월", "쉬어 갈 달 8·9월", "끝내 둘 일 세 가지"],
          "community_q": [], "order": toc_q, "images": ["삼재까지 남은 길(route)", "호랑이띠의 달(monthgrid, 절기 날짜)", "실행 의도(twopanel)"],
          "related": "n81", "cta": PID, "experience": [], "applied": True,
          "differs_from_n64": "제목(나를 보여 주는 해·힘 쓸 달과 아낄 달 → 삼재 들기 전 한 해 언제 움직일까)·도입(인사·결론부터·한 줄 요약 → 정의 직답)·소제목 순서·수비학(2+0+2+7)·스포트라이트 효과·분야별 나열 대신 삼재 셋 해(2028 들·2029 눌·2030 날, 2031 입춘 끝, engine assert)·끝내 둘 일 세 가지·예시 2010.2.3/2.5·실행 의도(Gollwitzer & Sheeran 2006)·그림 유형(route·monthgrid·twopanel)·연결글(→ n81)"}

if __name__ == "__main__":
    body, a4, made = build()
    reg = json.load(open(MP.REG, encoding="utf-8"))
    assert PID not in reg or not reg[PID].get("done"), "이미 예약 끝난 글"
    reg[PID] = dict(dt="2027-02-10T18:00:00", dt_tbd="CT가 정함(재발행 일정 'n64 다시 쓰기' 자리, 진행표 11/18). 이 날짜는 자리값", title=TITLE, tags=TAGS, body=body,
                    cover=a4, related=REL, thumbs=None, cid=None, clips=None, category="2027 운세", done=False, kw_vol=KW_VOL,
                    k131="n103 11/20(K-151 새 글)", source="build_naver_103.py (n64 주제 새 글, n64 그대로)")
    json.dump(reg, open(MP.REG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    ic = json.load(open(os.path.join(HERE, "intent_cards.json"), encoding="utf-8")); ic["cards"][PID] = INTENT
    json.dump(ic, open(os.path.join(HERE, "intent_cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    v = reg[PID]
    MP.write_page(PID, D.datetime.fromisoformat(v["dt"]), v["title"], v["tags"], v["body"], None, v["cover"], v["related"], v["category"])
    MP.write_index()
    import k151_check as K
    print(PID, len(TITLE), "자 제목 · 본문 글자", len(re.sub(r"<[^>]+>|&nbsp;", "", body)), "· 사진", made, "· K 검사", K.check(PID, v))
