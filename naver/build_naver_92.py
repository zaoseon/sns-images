"""네이버 n92: 2027년 토끼띠 운세 새 글 (CT 11/4 19:40 → ① 최우선, 대표 11/4 19:28 재발행 일정 '새 글로 다시 쓰기' n08 → n92, 11/21 18:00 자리).
- 왜: 노출 안 되는 옛 글 n08(2027년 토끼띠 운세, 사람이 모이는 해 월별·재물·연애운 총정리)을 새 글로. n08은 건드리지 않는다(K-147·K-178).
- 검색어: data/keywords/kw_volume.json posts.n92(11/7 20:12) — 토끼띠운세 47,100 · 토끼띠 26,510 · 2027년토끼띠운세 710.
- 다르게 쓴 것(K-151): n08의 한 줄 요약 줄·12달 나열·삼재 설명·수비학·여섯 운명학·호감의 상호성·나이(세) 표기 대신,
  해 글자 두 개가 나무(토끼)에게 주는 것(丁 불 = 솜씨·표현, 未 흙 = 돈) + 삼합 亥卯未를 세 기둥으로 세우고,
  '솜씨를 값으로 바꾸는 세 단계(모으기·보여 주기·값 붙이기)', 움직일 때 세 번(7·11월 한 팀, 10월 짝, 8·9월 쉬어 감),
  태어난 해별 하늘 글자(癸·乙·丁·己·辛)가 丁에게서 받는 것. 예시 장면 = 1999년 2월 4일 오후 2시생(호랑이띠) · 오후 4시생(토끼띠), 입춘 15:57.
  심리 = 이케아 효과(Norton, Mochon & Ariely 2012, 종이접기 실험). 삼재 날짜는 n81이 맡아 연결글로만. 띠 글 꼬리 '힘 쓸 달·아낄 달 총정리' 안 씀(CT 11/4 21:05).
  그림 유형 triad·route·monthgrid·vbar(n90 fork·sides·bignum, n91 twopanel·compare·exp와 다름). 연결글 → n81(발행·노출 '예' 1위, 11/8 측정).
- 계산: 해 간지·띠 관계·하늘 글자 관계는 assert, 힘 쓸 달은 사이트 tools/tti_extra.json(n80·n08과 같은 값), 절기·입춘·연주는 engine/engine.py.
- 출처 2개(K-162, 11/8 확인): Norton, Mochon & Ariely (2012) Journal of Consumer Psychology 22(3) 453–460, DOI 10.1016/j.jcps.2011.08.002
  (하버드 DASH 원문: 실험 1B 종이접기 106명, 접은 사람 자기 작품 0.23달러 · 다른 사람이 같은 작품 0.05달러 · 전문가 작품 0.27달러, 실험 1A 이케아 상자 0.78 대 0.48달러 = 63%) · 한국천문연구원 음양력 변환(입춘·절기 시각).
- 날짜: CT가 정한다. pages.json dt 는 자리값, dt_tbd 로 표시.
사용: SITE=<zaoseon-site> python3 naver/build_naver_92.py"""
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
       '<tr><td style="padding:12px 10px;text-align:center;border:1px solid #d0d0d0"><b>1·2월생이라 내 띠가 헷갈린다면</b></td></tr>'
       '<tr><td style="padding:12px 10px;text-align:center;border:1px solid #d0d0d0"><span style="color:#9a9a9a">[ 1999 . 02 . 04 ]</span></td></tr>'
       '<tr><td style="padding:12px 10px;text-align:center;border:1px solid #d0d0d0"><b><a href="https://zaoseon.com/?utm_source=naver&amp;utm_medium=mid#free">내 태어난 날 글자 보기 →</a></b></td></tr>'
       '</tbody></table>' + BL)
CTA = ('<p><a href="https://zaoseon.com/?utm_source=naver&utm_medium=cta#free"><img src="' + RAW +
       'naver_cta5_1%EC%B4%88%EB%AC%B4%EB%A3%8C%ED%92%80%EC%9D%B4.jpg" alt="자오선 무료 1초 풀이 안내 배너"></a></p>')
PID, KEY, PAL = "n92", "92", "k_neon_s"   # 나무 판 묶음(EL_SET 나무), n85·n88 y_olive_s · n87·n89 dg_gold_s · n90 g_ivory_s 와 다른 판

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
assert role("나무", "불") == "솜씨·표현" and role("나무", "흙") == "손에 쥐는 돈"      # 토끼(卯 나무)에게 丁 불·未 흙
R, Y = BR.index("卯"), BR.index("未")
assert {BR.index("亥"), R, Y} == {11, 3, 7}                                             # 삼합 亥卯未
LIUHE = {0: 1, 2: 11, 3: 10, 4: 9, 5: 8, 6: 7}; LIUHE.update({v: k for k, v in list(LIUHE.items())})
WONJIN = {0: 7, 1: 6, 2: 9, 3: 8, 4: 11, 5: 10}; WONJIN.update({v: k for k, v in list(WONJIN.items())})
assert LIUHE[R] == BR.index("戌") and WONJIN[R] == BR.index("申") and (R + 6) % 12 == BR.index("酉")
MB = {m: BR[m % 12] for m in range(1, 13)}                                               # 2월 寅 … 12월 子, 1월 丑
assert MB[7] == "未" and MB[10] == "戌" and MB[11] == "亥" and MB[8] == "申" and MB[9] == "酉"
YRS = [1951 + 12 * k for k in range(7)]; assert all(BR[(y - 4) % 12] == "卯" for y in YRS)
STEM = {y: GAN[(y - 4) % 10] for y in (1963, 1975, 1987, 1999, 2011)}
assert STEM == {1963: "癸", 1975: "乙", 1987: "丁", 1999: "己", 2011: "辛"}
ROLE_Y = {y: role(GEL[s], "불") for y, s in STEM.items()}
assert ROLE_Y == {1963: "손에 쥐는 돈", 1975: "솜씨·표현", 1987: "같은 편", 1999: "문서·도움", 2011: "책임·규칙"}
EX = json.load(open(os.path.join(SITE, "tools", "tti_extra.json"), encoding="utf-8"))
assert EX["rabbit"]["good"] == ["7월", "10월", "11월"] and EX["rabbit"]["care"] == ["8월", "9월"]
sys.path.insert(0, os.path.join(SITE, "engine")); import engine as E
T27 = dict((n, t) for n, _, t in E.get_solar_terms_kst(2027))
for n, (mo, dd) in {"입춘": (2, 4), "소서": (7, 7), "입추": (8, 8), "백로": (9, 8), "한로": (10, 8), "입동": (11, 8)}.items():
    assert (T27[n].month, T27[n].day) == (mo, dd), (n, T27[n])
assert (T27["입춘"].hour, T27["입춘"].minute) == (10, 46)
L99 = dict((n, t) for n, _, t in E.get_solar_terms_kst(1999))["입춘"]; assert (L99.month, L99.day, L99.hour, L99.minute) == (2, 4, 15, 57)
assert E.compute_saju(D.datetime(1999, 2, 4, 14, 0))["팔자"]["년주"] == "戊寅"   # 오후 2시생 = 호랑이띠
assert E.compute_saju(D.datetime(1999, 2, 4, 16, 0))["팔자"]["년주"] == "己卯"   # 오후 4시생 = 토끼띠
print("해 간지·삼합·육합·원진·충·하늘 글자·힘 쓸 달·절기·입춘·연주 다시 확인")

# ───────── 본문 (n08 문장을 옮기지 않았다)
head = ["<b>2027년 토끼띠 운세는 해의 불(丁)로 솜씨를 꺼내고, 해의 흙(未)에서 그 값을 받는 해예요.</b>",
        "나무인 토끼에게 불은 내 안에서 나가는 말과 손재주, 흙은 손에 쥐는 돈이에요. 여기에 토끼(卯)와 양(未)은 돼지(亥)와 한 팀(삼합)이라, 혼자 만든 것보다 함께 만든 것이 더 멀리 가요.",
        "<b>움직일 때는 세 번이에요. 7월과 11월에는 한 팀이 모이고, 10월에는 짝이 오고, 8월·9월에는 쉬어 가요.</b>",
        "2027년은 토끼띠 삼재가 끝나는 해(날삼재)이기도 해요. 삼재가 끝나는 날짜는 따로 정리해 두어서, 이 글에서는 솜씨와 값, 움직일 때만 볼게요. 2026년 11월 8일 기준으로 정리한 내용이에요."]
toc_q = ["2027년 토끼띠 운세, 해 글자 두 개가 무엇을 줄까요?", "토끼띠는 몇 년생이고, 2월 4일생은 어떻게 볼까요?",
         "솜씨를 값으로 바꾸려면 무엇부터 할까요?", "왜 7월·10월·11월에 움직이고 8월·9월에 쉴까요?",
         "태어난 해마다 먼저 챙길 것은 무엇일까요?", "내가 만든 것은 왜 더 비싸 보일까요?", "토끼띠가 자주 묻는 질문"]
sec1 = P("<b>나무가 불을 피우고 흙에 뿌리를 내리듯, 토끼띠에게 2027년은 꺼내고 받는 해예요.</b>",
         "띠마다 기운이 하나씩 있어요. 토끼(卯)는 봄의 나무예요.",
         "사주에서는 내가 낳는 기운을 솜씨와 표현(식상), 내가 이기는 기운을 돈(재성)으로 봐요. 나무는 불을 낳고 흙을 이기니, 해의 丁 불은 솜씨, 해의 未 흙은 돈이 돼요.",
         "그래서 2027년 토끼띠는 말, 글, 손재주처럼 내 안에 있던 것이 먼저 밖으로 나가고, 그 뒤에 값이 따라오는 순서예요.") + "[[F]]" + \
       P("하나 더 있어요. 해의 주인 양(未)은 돼지(亥)·토끼(卯)와 한 팀(삼합 亥卯未)이에요. 세 글자가 모이면 나무의 힘이 커져요.",
         "토끼띠에게는 내 편이 늘어나는 해라는 뜻이에요. 혼자 붙잡고 있던 일을 같이 할 사람에게 보여 주면 속도가 붙어요.")
sec2 = P("<b>토끼띠는 1951·1963·1975·1987·1999·2011·2023년생이에요.</b>",
         "다만 사주에서 해는 1월 1일이 아니라 입춘에 바뀌어요. 그래서 1월생과 2월 초에 태어난 사람은 앞 해 띠일 수 있어요.") + \
       P("🔎 1999년 2월 4일에 태어난 두 사람을 떠올려 볼게요. 그해 입춘은 2월 4일 오후 3시 57분이었어요.",
         "오후 2시에 태어난 사람은 입춘 전이라 1998년 무인년, 호랑이띠예요. 오후 4시에 태어난 사람은 입춘 뒤라 1999년 기묘년, 토끼띠예요.",
         "같은 날 두 시간 차이로 띠가 갈려요. 2월 3일에서 5일 사이에 태어났다면 '나 몇 시쯤 태어났어?' 하고 가족에게 한 줄 물어보세요.") + MID
sec3 = P("<b>솜씨가 값이 되려면, 먼저 보이게 하고 그다음 값을 붙여요.</b>",
         "해의 불이 솜씨를 꺼내 주는 해라, 하고 싶은 말과 만들고 싶은 것이 많아져요. 그런데 꺼내기만 하고 값을 정하지 않으면 바쁜데 남는 것이 적은 해가 되기 쉬워요.",
         "그래서 순서를 셋으로 나눠 보면 좋아요.") + "[[R]]" + \
       P("<b>모으기</b>: 지난 1년 동안 만든 것 가운데 남에게 보여 줄 만한 것 세 개를 한 폴더에 모아요. 보고서, 사진, 짧은 글 무엇이든 괜찮아요.",
         "<b>보여 주기</b>: 그 세 개를 같이 일할 만한 사람 한 명에게 먼저 보여 줘요. 한 팀이 모이는 해라 이 한 사람이 다음 사람을 데려오기 쉬워요.",
         "<b>값 붙이기</b>: 부탁을 받으면 '기본은 이만큼부터예요'라고 내가 먼저 숫자를 꺼내요. 값을 상대에게 맡기면 솜씨가 싸게 매겨지기 쉬워요.") + \
       P("회사에 다닌다면 값은 돈만이 아니에요. 올해 낸 결과를 '몇 건, 몇 %'처럼 숫자로 적어 두면, 연말 평가 때 그 숫자가 내 솜씨의 값이 돼요.")
sec4 = P("<b>토끼띠가 2027년에 힘 쓸 달은 7월·10월·11월, 아낄 달은 8월·9월이에요.</b>",
         "사주의 달은 1일이 아니라 절기로 바뀌어요. 달마다 그달을 맡은 띠 글자가 있어서, 그 글자와 토끼의 사이로 달을 골라요.") + "[[M]]" + \
       P("⭐ 7월 7일 소서부터는 양(未)의 달이에요. 해와 같은 글자가 달에 한 번 더 들어와 한 팀의 힘이 커져요. 같이 할 일을 먼저 꺼내기 좋아요.",
         "⭐ 10월 8일 한로부터는 개(戌)의 달이에요. 토끼와 개는 짝을 이루는 사이(육합)라, 계약이나 동업처럼 둘이 손잡는 일에 힘이 실려요.",
         "⭐ 11월 8일 입동부터는 돼지(亥)의 달이에요. 해의 양, 달의 돼지, 내 띠 토끼까지 세 글자가 다 모여요. 7월에 꺼낸 일을 마무리하기 좋아요.") + \
       P("⚠️ 8월 8일 입추부터는 원숭이(申)의 달이에요. 토끼와 원숭이는 서운함이 쌓이기 쉬운 사이(원진)라, 같이 일하는 사람과 말이 엇갈리기 쉬워요.",
         "⚠️ 9월 8일 백로부터는 닭(酉)의 달이에요. 토끼와 닭은 정면으로 마주 보는 사이(충)라, 이사·이직처럼 큰 결정은 10월로 한 달 미뤄 보세요.",
         "아낄 달은 나쁜 달이 아니라 속도를 줄이는 달이에요. 8월에는 일정 사이에 빈 날을 하루씩 넣어 두세요.")
sec5 = P("<b>같은 토끼띠라도 태어난 해의 하늘 글자가 달라서, 해의 丁에게서 받는 것이 조금씩 달라요.</b>",
         "🌿 <b>1963년생(계묘)</b>: 하늘 글자가 물이라 해의 불이 손에 쥐는 돈이에요. 들어온 돈은 한 달쯤 두고 쓸 곳을 정해 보세요.",
         "🌿 <b>1975년생(을묘)</b>: 하늘 글자도 나무라 해의 불이 솜씨예요. 이 글의 세 단계가 가장 잘 맞는 해예요.",
         "🌿 <b>1987년생(정묘)</b>: 하늘 글자가 해와 같은 丁이라 같은 편이 늘어요. 같이 할 사람이 많아지는 만큼 나눠 내는 돈도 늘어요.",
         "🌿 <b>1999년생(기묘)</b>: 하늘 글자가 흙이라 해의 불이 문서와 도움이에요. 자격증, 계약서처럼 종이로 남는 일을 챙겨 보세요.",
         "🌿 <b>2011년생(신묘)</b>: 하늘 글자가 쇠라 해의 불이 책임이에요. 학교나 모임에서 맡는 역할이 늘 수 있어요.")
sec6 = P("🧠 <b>내가 만든 것은 남이 보는 것보다 비싸 보이기 쉬워요. 심리학에서는 이것을 이케아 효과라고 해요.</b>",
         "노튼, 모촌, 애리얼리 연구진은 2012년, 사람들에게 종이접기를 직접 접게 한 뒤 그 작품에 얼마를 낼지 물었어요.",
         "접은 사람은 자기 작품에 평균 23센트를 불렀어요. 같은 작품에 다른 사람들이 부른 값은 5센트였어요. 전문가가 접은 작품에는 27센트를 불렀어요.") + "[[B]]" + \
       P("같은 연구의 이케아 상자 실험에서도, 상자를 직접 조립한 사람은 조립된 상자를 받은 사람보다 63% 더 높은 값을 불렀어요.",
         "내가 만든 것을 아끼는 마음은 자연스러워요. 그 마음이 있어서 끝까지 만들어요.",
         "다만 값을 정할 때는 그 마음이 눈을 가리기 쉬워요. 솜씨가 값이 되는 해일수록, 값을 붙이기 전에 남의 눈을 한 번 빌려 보세요.",
         '📚 <b>출처 1</b>: <a href="https://doi.org/10.1016/j.jcps.2011.08.002">Norton, Mochon &amp; Ariely (2012), The IKEA effect: When labor leads to love, Journal of Consumer Psychology 22(3)</a>',
         '📚 <b>출처 2</b>: <a href="https://astro.kasi.re.kr/life/pageView/5">한국천문연구원 천문우주지식정보, 음양력 변환</a>') + \
       P("🌱 <b>마음 코치 정월의 질문</b>", "2027년에 꺼내고 싶은 내 솜씨는<br>무엇인가요?",
         "🔸 그 솜씨를 가장 먼저 보여 주고 싶은 한 사람은<br>누구인가요?") + \
       P("✔️ <b>2027년 토끼띠가 해 볼 것</b>",
         "1. 지난 1년 동안 만든 것 세 개를 한 폴더에 모아 두세요.",
         "2. 7월 7일 전에, 같이 할 만한 사람 한 명에게 그 폴더를 보여 주세요.",
         "3. 값을 붙이기 전에 믿는 사람 한 명에게 '이거 얼마면 살 것 같아?'라고 물어보세요.")
sec7 = P("<b>Q. 날삼재라는데 이사나 이직을 해도 되나요?</b>",
         "A. 날삼재는 삼재가 나가는 마지막 해라 겁낼 해는 아니에요. 이 글의 달로 보면 큰 결정은 충이 드는 9월보다 짝이 오는 10월 뒤가 편해요. 삼재가 끝나는 날짜는 아래 글에 따로 정리했어요.") + \
       P("<b>Q. 같은 토끼띠인데 왜 사람마다 다르게 느껴질까요?</b>",
         "A. 띠는 태어난 해 글자 하나만 본 거예요. 태어난 날의 글자(일간)까지 보면, 같은 토끼띠라도 해의 불이 솜씨인 사람과 돈인 사람으로 갈려요.") + \
       P("<b>Q. 2027년 토끼띠 운세는 언제부터 적용돼요?</b>",
         "A. 사주에서 해는 입춘에 바뀌어요. 2027년 입춘은 2월 4일 오전 10시 46분이에요. 그 전 1월까지는 2026년 병오년 기운으로 봐요.")
tail = P("여러분은 2027년에 어떤 솜씨를 꺼내고 싶나요?", "꺼내고 싶은 것 하나를 태어난 해와 함께 댓글로 남겨 주세요.") + \
       '<p><b>👇 토끼띠 삼재가 정확히 언제 끝나는지 보고 싶다면, 2027 삼재띠 언제 끝날까, 돼지띠 토끼띠 양띠 날삼재 날짜</b></p>'
secs = [sec1, sec2, sec3, sec4, sec5, sec6, sec7]

def _have(n): return os.path.exists(os.path.join(HERE, "img", n))
def build():
    for d_ in ("wide", "m1280", "master"): os.makedirs(os.path.join(HERE, "img", d_), exist_ok=True)
    c = V.Ctx(PAL); made = []
    a4 = f"wide/naver_z{KEY}_a4.jpg"
    if not _have(a4):
        V.render(PID + "_new", {"d": "N", "el": "나무", "kick": "2027년 토끼띠 운세", "hook": ["솜씨를 꺼내고", "값을 받는 해"], "sub": "언제 움직일까",
                                "items": ["7월", "10월", "11월"]}, os.path.join(HERE, "img", a4), PAL)
    made.append(a4)
    nm = {"F": f"naver_z{KEY}_t3.jpg", "R": f"naver_z{KEY}_r3.jpg", "M": f"naver_z{KEY}_m3.jpg", "B": f"naver_z{KEY}_v3.jpg"}
    if not _have(nm["F"]):
        DGC.triad(nm["F"], c, "해 글자 두 개가 토끼띠에게 주는 것",
                  [("丁 불", "솜씨·표현. 말과 손재주가 밖으로 나가요"), ("未 흙", "돈. 꺼낸 솜씨에 값이 붙어요"), ("亥卯未", "한 팀. 돼지·양과 손잡아 나무가 커져요")],
                  1, "꺼내고, 값을 받고, 함께 키우는 해", "해 간지 丁未 · 오행으로 계산")
    if not _have(nm["R"]):
        DGB.route(nm["R"], c, "솜씨를 값으로 바꾸는 세 단계", [("모으기", "만든 것 세 개를 한 폴더에"), ("보여 주기", "같이 할 사람 한 명에게"), ("값 붙이기", "내가 먼저 숫자를 꺼내기")])
    if not _have(nm["M"]):
        tag = {7: ("한 팀", "up"), 10: ("짝", "up"), 11: ("한 팀", "up"), 8: ("원진", "dn"), 9: ("충", "dn")}
        DG.monthgrid(nm["M"], c, "2027년 토끼띠의 달", [(m, *tag.get(m, ("", None))) for m in list(range(2, 13)) + [1]])
    if not _have(nm["B"]):
        DGC.vbar(nm["B"], c, "내가 접은 종이접기에 부른 값", [("내 작품, 내가", 23, True), ("내 작품, 남이", 5, False), ("전문가 작품, 남이", 27, False)],
                 30, "내가 만든 것은 남이 매긴 값보다 네 배 넘게 비싸 보였어요", "Norton, Mochon & Ariely (2012) 실험 1B · 단위 센트(100센트 = 1달러)", fmt="{:.0f}센트", step=10)
    import fullbleed as FBL
    plan_p = os.path.join(HERE, "fullbleed_plan.json"); plan = json.load(open(plan_p, encoding="utf-8")) if os.path.exists(plan_p) else {}
    rows = []
    for pos, k in enumerate("FRMB", 1):
        f = nm[k][:-4] + "f.jpg"
        if not _have(f):
            r, why = FBL.convert(nm[k], [os.path.join(HERE, "img"), os.path.join(HERE, "img", "m1280")])
            if not r: print("fullbleed 건너뜀", nm[k], why); made.append(nm[k]); continue
        rows.append({"pos": pos, "old": nm[k], "new": f}); made.append(nm[k]); nm[k] = f
        reg_ = json.load(open(DG.REG, encoding="utf-8")); reg_[f] = reg_[rows[-1]["old"]]; json.dump(dict(sorted(reg_.items())), open(DG.REG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    plan[PID] = rows; json.dump(plan, open(plan_p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    made += [v for v in nm.values() if v not in made]
    alt = {"F": "해 글자 두 개가 토끼띠에게 주는 것 그림. 丁 불은 솜씨와 표현, 未 흙은 돈, 돼지·토끼·양 삼합은 한 팀",
           "R": "솜씨를 값으로 바꾸는 세 단계 그림. 만든 것 세 개 모으기, 같이 할 사람 한 명에게 보여 주기, 내가 먼저 값 꺼내기",
           "M": "2027년 토끼띠의 달 그림. 힘 쓸 달 7월 한 팀·10월 짝·11월 한 팀, 아낄 달 8월 원진·9월 충",
           "B": "이케아 효과 종이접기 실험 그림. 접은 사람이 자기 작품에 23센트, 다른 사람이 같은 작품에 5센트, 전문가 작품에 27센트를 불렀어요"}
    body = P(*head) + P("<b>📌 토끼띠의 2027년을 읽는 길</b>", *[f"{i + 1}. {q}" for i, q in enumerate(toc_q)])
    for i, (q, s) in enumerate(zip(toc_q, secs)):
        for k in "FRMB": s = s.replace(f"[[{k}]]", IMG(nm[k], alt[k]))
        body += H(f"{i + 1}. {q}") + s
    body += tail + CTA
    import copy_rules as CR
    for w in ("재미로", "상담", "—", "안녕하세요, 자오선의 정월이에요", "결론부터 말씀드릴게요", "생년월일만 넣으면 1초", "한 줄 요약", "이 글의 순서", "수비학으로 겹쳐 보면",
              "총정리", "사람이 모이는 해", "호감의 상호성") + tuple(CR.금지어):
        assert w not in re.sub(r"<[^>]+>", " ", body), w
    for f in made:   # 사이트 사본(K-069)
        dst = os.path.join(SITE, "public", "naver", "img", f); os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy(os.path.join(HERE, "img", f), dst)
    return body, a4, made

TITLE = "2027년 토끼띠 운세, 솜씨가 값이 되는 해 언제 움직일까"
TAGS = ["2027년토끼띠운세", "토끼띠운세", "토끼띠", "2027토끼띠운세", "87년생토끼띠운세", "정미년", "삼합", "날삼재", "이케아효과", "자오선"]
REL = {"id": "n81", "title": "2027 삼재띠 언제 끝날까, 돼지띠 토끼띠 양띠 날삼재 날짜",
       "phrase": "토끼띠 삼재가 정확히 언제 끝나는지 보고 싶다면, 2027 삼재띠 언제 끝날까, 돼지띠 토끼띠 양띠 날삼재 날짜",
       "url": "https://blog.naver.com/zaoseon/224462303163"}
KW_VOL = json.load(open(os.path.join(SITE, "data", "keywords", "kw_volume.json"), encoding="utf-8"))["posts"]["n92"]["씨앗"]
INTENT = {"keywords": ["토끼띠운세", "2027년토끼띠운세", "토끼띠"],
          "keyword_src": "kw-volume 작업(data/keywords/kw_volume.json posts.n92, 11/7 20:12) 월 검색량 · n08 조회 순위(재발행 일정 '새 글로 다시 쓰기')",
          "intent": "알고 싶다", "intent_note": "2027년 토끼띠에게 어떤 해인지 해 글자로 바로 알고, 몇 년생인지·1·2월생 띠·언제 움직이고 쉴지·무엇을 해 볼지까지 보기",
          "first3": "2027년 토끼띠 운세는 해의 불(丁)로 솜씨를 꺼내고, 해의 흙(未)에서 그 값을 받는 해예요.",
          "answer_keys": ["토끼띠 운세", "솜씨와 값", "7월·10월·11월"],
          "order": toc_q[:6], "images": ["해 글자 두 개가 토끼에게 주는 것(triad, 오행 계산)", "솜씨를 값으로 바꾸는 세 단계(route)", "2027 토끼띠의 달(monthgrid, 절기·띠 관계)", "이케아 효과 종이접기 실험(vbar)"],
          "related": "n81", "cta": PID, "experience": [], "applied": True,
          "differs_from_n08": "제목·도입(정의 + 움직일 때 세 번 직답)·소제목 순서·한 줄 요약 줄·12달 나열·삼재 설명·수비학·여섯 운명학·호감의 상호성 대신 해 글자 세 기둥(丁 솜씨·未 돈·亥卯未 한 팀)·솜씨를 값으로 바꾸는 세 단계·움직일 때 세 번(7·11 한 팀, 10 짝, 8·9 쉬어 감)·태어난 해 하늘 글자별 丁의 몫·예시 장면(1999.2.4 오후 2시 호랑이띠 / 오후 4시 토끼띠, 입춘 15:57)·그림 유형(triad·route·monthgrid·vbar)·심리 개념(이케아 효과, Norton 외 2012)·출처·연결글(→ n81, 삼재 날짜는 그 글로)"}

if __name__ == "__main__":
    body, a4, made = build()
    reg = json.load(open(MP.REG, encoding="utf-8"))
    assert PID not in reg or not reg[PID].get("done"), "이미 예약 끝난 글"
    reg[PID] = dict(dt="2027-02-04T08:00:00", dt_tbd="CT가 정함(재발행 일정 11/21 18:00 자리). 이 날짜는 자리값", title=TITLE, tags=TAGS, body=body,
                    cover=a4, related=REL, thumbs=None, cid=None, clips=None, category="2027 운세", done=False, kw_vol=KW_VOL,
                    k131="n92 11/8(K-151 새 글)", source="build_naver_92.py (n08 주제 새 글, n08 그대로)")
    json.dump(reg, open(MP.REG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    ic = json.load(open(os.path.join(HERE, "intent_cards.json"), encoding="utf-8")); ic["cards"][PID] = INTENT
    json.dump(ic, open(os.path.join(HERE, "intent_cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    v = reg[PID]
    MP.write_page(PID, D.datetime.fromisoformat(v["dt"]), v["title"], v["tags"], v["body"], None, v["cover"], v["related"], v["category"])
    MP.write_index()
    import k151_check as K
    print(PID, len(TITLE), "자 제목 · 본문 글자", len(re.sub(r"<[^>]+>|&nbsp;", "", body)), "· 사진", made, "· K 검사", K.check(PID, v))
