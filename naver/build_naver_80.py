"""네이버 n80: 2027 띠별 운세 새 글 (CT 10/29 13:55 → ①, 대표 10/29 13:36 "빨리 해보자", 16:33 "내일 오전·오후 한 편씩").
- 왜: n01(9/29, 첫 글, 유입 1위)이 지금 검색에 안 나온다. 10/24 이후 새 글은 하루 안에 색인된다(서브 10/29 10:50). 그래서 같은 주제를 새 글로 쓴다.
- 지킨 것: n01은 건드리지 않는다(K-147). 복사하지 않는다(K-151): 제목·도입·소제목 순서·띠별 문장·예시·그림 종류·심리 개념·연결글을 모두 새로 썼다.
  같은 것은 계산값뿐이다(띠 관계·힘 쓸 달·아낄 달·행운 색·숫자·방향·입춘 시각). 값은 사이트 tools/tti_extra.json(= /2027/ 띠 페이지·n01과 같은 값)에서 읽고 아래 assert 로 다시 잰다.
- 새 글 틀(K-151·R70·N17): 고정 첫 인사·'결론부터' 문장 없음 · 첫 200자에 '띠별 운세' 직답 · 제목 40자 안 · 태그 10개, 마지막 '자오선'.
- 의도 카드(K-143) 먼저: intent_cards.json n80. 연결글은 발행 글만(K-155): n14(10/2 발행).
- 그림(K-131·K-135): 도식 3장, 서로 다른 유형(months·route·twopanel), 옛 틀 0장. 표지는 정월 없는 판. 새 이름만(K-025).
- 입춘 시각: zaoseon-site engine/engine.py get_solar_terms_kst(2027) = 2월 4일 10:46(10/29 실행으로 확인).
- 심리 근거: body_v4 카드 M15(실행 의도, Gollwitzer 1999, American Psychologist, Crossref 확인 10/14).
사용: SITE=<zaoseon-site> python3 naver/build_naver_80.py   (pages.json 에 n80을 넣고 사이트 원고 페이지 n80.html·목록만 다시 쓴다. render_all 은 부르지 않는다)"""
import os, sys, json, re, html, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "pipeline"))
os.chdir(HERE)
import cover_v3 as V, make_page as MP, diagrams_k131 as DG, diagrams_k131b as DGB
SITE = os.environ.get("SITE", "/home/claude/zaoseon-site")
RAW = "https://raw.githubusercontent.com/zaoseon/sns-images/main/naver/img/"
BL = "<p>&nbsp;</p>"
def P(*ls): return "".join(f"<p>{l}</p>" for l in ls) + BL
def IMG(name, alt): return f'<p><img src="{RAW}{name}" alt="{html.escape(alt, quote=True)}"></p>' + BL
def H(t): return f"<p><b>{t}</b></p>"
MID = ('<table style="width:100%;max-width:440px;margin:0 auto;border-collapse:collapse"><tbody>'
       '<tr><td style="padding:12px 10px;text-align:center;border:1px solid #d0d0d0"><b>생년월일만 넣으면 1초</b></td></tr>'
       '<tr><td style="padding:12px 10px;text-align:center;border:1px solid #d0d0d0"><span style="color:#9a9a9a">[ 1990 . 03 . 15 ]</span></td></tr>'
       '<tr><td style="padding:12px 10px;text-align:center;border:1px solid #d0d0d0"><b><a href="https://zaoseon.com/?utm_source=naver&amp;utm_medium=mid#free">내 태어난 날 글자 보기 →</a></b></td></tr>'
       '</tbody></table>' + BL)
CTA = ('<p><a href="https://zaoseon.com/?utm_source=naver&utm_medium=cta#free"><img src="' + RAW +
       'naver_cta5_1%EC%B4%88%EB%AC%B4%EB%A3%8C%ED%92%80%EC%9D%B4.jpg" alt="자오선 무료 1초 풀이 안내 배너"></a></p>')
PID, KEY, PAL = "n80", "80", "p_red"   # 정(丁)=불 → 핑크&레드 판(n01은 y_pink_s)

# ───────── 계산값과 검산
BR = "子丑寅卯辰巳午未申酉戌亥"; GAN = "甲乙丙丁戊己庚辛壬癸"
assert GAN[(2027 - 4) % 10] + BR[(2027 - 4) % 12] == "丁未"
assert GAN[(2026 - 4) % 10] + BR[(2026 - 4) % 12] == "丙午"     # 입춘 전 2027년 1월생 = 병오년 말띠
EX = json.load(open(os.path.join(SITE, "tools", "tti_extra.json"), encoding="utf-8"))
SLUG = ["rat", "ox", "tiger", "rabbit", "dragon", "snake", "horse", "sheep", "monkey", "rooster", "dog", "pig"]
NAME = ["쥐띠", "소띠", "호랑이띠", "토끼띠", "용띠", "뱀띠", "말띠", "양띠", "원숭이띠", "닭띠", "개띠", "돼지띠"]
EL = dict(zip(BR, "물 흙 나무 나무 흙 불 불 흙 쇠 쇠 흙 물".split()))
SAENG = {"물": "쇠", "나무": "물", "불": "나무", "흙": "불", "쇠": "흙"}          # 나를 살려 주는 기운
COLOR = {"쇠": "흰색 · 금색", "물": "검정 · 남색", "나무": "초록 · 청록", "불": "빨강 · 주황", "흙": "노랑 · 베이지"}
NUM = {"물": "1, 6", "불": "2, 7", "나무": "3, 8", "쇠": "4, 9", "흙": "5, 10"}
DIR = {"물": "북쪽", "불": "남쪽", "나무": "동쪽", "쇠": "서쪽", "흙": "가운데(집 안)"}
for i, b in enumerate(BR):   # 행운 색·숫자·방향 = 내 띠 기운을 살려 주는 기운의 색·수·방향(값은 tti_extra 그대로인지 잰다)
    e = SAENG[EL[b]]; x = EX[SLUG[i]]
    assert (x["color"], x["num"], x["dir"]) == (COLOR[e], NUM[e], DIR[e]), (b, x)
Y = BR.index("未")
LIUHE = {0: 1, 2: 11, 3: 10, 4: 9, 5: 8, 6: 7}; LIUHE.update({v: k for k, v in list(LIUHE.items())})
assert LIUHE[Y] == BR.index("午")                                    # 육합: 말띠
assert {BR.index("亥"), BR.index("卯"), Y} == {11, 3, 7}             # 삼합 亥卯未: 돼지·토끼
assert (Y + 6) % 12 == BR.index("丑")                                # 충: 소띠
WONJIN = {0: 7, 1: 6, 2: 9, 3: 8, 4: 11, 5: 10}; WONJIN.update({v: k for k, v in list(WONJIN.items())})
assert WONJIN[Y] == BR.index("子")                                   # 원진: 쥐띠
assert {BR.index(x) for x in "丑戌未"} == {1, 10, 7}                 # 삼형: 개띠·소띠·양띠
def yrs(i): return ", ".join(str(1972 + i + 12 * k) for k in range(4))
assert yrs(11) == "1983, 1995, 2007, 2019" and yrs(0) == "1972, 1984, 1996, 2008"
GOOD = {s: EX[s]["good"] for s in SLUG}; CARE = {s: EX[s]["care"] for s in SLUG}
def mon(lst): return {13 if "이듬해" in x else int(re.sub(r"\D", "", x)) for x in lst}

# ───────── 띠별 새 문장(n01 문장을 옮기지 않았다). 해 볼 것의 달은 그 띠의 힘 쓸 달 안에서만 고른다(아래 assert).
Z = [  # 한 줄, 왜 그런가, 써 볼 달, 해 볼 것
 ("말이 엇갈리기 쉬운 대신 돈 기회는 열리는 해", "쥐(子)와 양(未)은 서로 서운함이 쌓이는 사이(원진)로 읽어요. 물인 쥐띠에게 해의 불(丁)은 손에 쥐는 재물이에요.", "4월", "미뤄 둔 돈 이야기를 말 대신 글로 정리해 보내기"),
 ("머물던 자리가 움직이는 해", "소(丑)는 양(未)과 열두 띠 원에서 정면으로 마주 보는 자리(충)예요. 그래서 이사·이직·부서 이동처럼 자리가 바뀌는 일이 많아요.", "5월", "옮기고 싶은 자리 하나를 정해 알아보기 시작하기"),
 ("가진 실력을 밖에 꺼내 보이는 해", "나무(寅)는 불(丁)을 키우는 쪽이에요. 내 힘이 바깥으로 나가니 말과 결과물이 눈에 띄지만, 그만큼 쉽게 지쳐요.", "6월", "보여 줄 결과물 하나에 마감 날짜 붙이기"),
 ("같이할 사람이 늘어나는 해", "토끼(卯)는 돼지(亥)·양(未)과 한 팀으로 묶이는 사이(삼합)예요. 혼자 할 때보다 사람을 통해 일이 풀려요.", "7월", "함께하고 싶은 사람에게 먼저 연락하기"),
 ("쌓아 둔 것이 단단해지는 해", "용(辰)과 양(未)은 같은 흙이고, 해의 불(丁)이 그 흙을 데워요. 크게 벌이기보다 기반을 다질 때 힘이 실려요.", "8월", "매달 같은 날 저축을 옮기는 날 정하기"),
 ("추진력이 커지는 만큼 쉬는 날도 챙길 해", "뱀(巳)은 해의 정미(丁未)와 함께 여름 불 기운으로 모여요. 의욕이 커지는 만큼 과열을 조심할 해예요.", "8월", "일정표에 쉬는 날을 먼저 적어 두기"),
 ("좋은 짝과 손잡는 해", "말(午)과 양(未)은 서로 짝을 이루는 사이(육합)예요. 연애·동업·계약처럼 둘이 손잡는 일에 힘이 실려요.", "2월", "함께할 사람과 첫 약속 날짜 정하기"),
 ("나를 점검하고 다시 세우는 해", "2027년은 양(未)의 해라 내 띠가 돌아온 해(본명년)예요. 새 판보다 지금 가진 것을 고쳐 세우기 좋아요.", "3월", "정리할 것 세 가지를 적고 하나씩 끝내기"),
 ("책임이 늘고 인정도 따라오는 해", "쇠(申)는 불(丁)에 다듬어지는 쪽이에요. 무거운 일이 들어오지만, 지나고 나면 쓸모 있는 실력이 돼요.", "4월", "맡은 일 하나를 골라 끝까지 마무리하기"),
 ("꼼꼼함이 실력으로 보이는 해", "닭(酉)도 쇠라서 불(丁)에 다듬어져요. 원숭이띠보다 섬세한 쪽이라 품질과 마무리로 인정받기 좋아요.", "5월", "내 작업을 한 장으로 기록해 남기기"),
 ("약속과 서류를 다시 보는 해", "개(戌)는 소(丑)·양(未)과 함께 서로 조율이 필요한 세 글자(형)에 들어가요. 정해 둔 규칙과 계약을 다시 살필 일이 생겨요.", "2월", "올해 맺은 계약서를 한 번 다시 읽기"),
 ("사람을 통해 기회가 들어오는 해", "돼지(亥)는 토끼(卯)·양(未)과 한 팀(삼합)이에요. 또 물인 돼지띠에게 해의 불(丁)은 재물이라, 소개가 수입으로 이어지기 쉬워요.", "3월", "소개받을 자리 하나를 먼저 만들기"),
]
for i, z in enumerate(Z): assert z[2] in GOOD[SLUG[i]], (NAME[i], z[2])

# ───────── 본문
head = ["<b>2027년 띠별 운세</b>를 내 띠부터 바로 찾을 수 있게 정리했어요.",
        "<b>정미년(丁未年)에 손잡는 일이 잘 풀리는 띠는 말띠·토끼띠·돼지띠, 자리가 크게 바뀌는 띠는 소띠·양띠·개띠예요.</b>",
        "나머지 여섯 띠는 해의 불(丁)과 내 띠 기운이 만나는 모양으로 읽어요. 쥐띠는 재물, 호랑이띠는 표현, 용띠는 다지기, 뱀띠는 속도, 원숭이띠·닭띠는 책임이 열쇠예요.",
        "새해 달력을 받으면 가족 띠부터 찾아보게 되죠. 이 글은 띠마다 힘 쓸 달과 아낄 달까지 한 번에 보이게 묶었어요.",
        "2026년 10월 29일 기준으로 정리한 내용이에요."]
toc_q = ["내 띠는 2027년에 어떤 해일까요?", "손잡는 띠와 자리가 바뀌는 띠는 왜 갈릴까요?", "띠별로 언제 힘을 쓰면 좋을까요?",
         "1월이나 2월 초에 태어났다면 무슨 띠일까요?", "달력에 적어 두면 왜 덜 미룰까요?", "자주 묻는 질문"]

sec1 = P(*[f"{NAME[i]}: {Z[i][0]}" for i in range(12)]) + \
       P("아래 그림은 열두 띠의 힘 쓸 달과 아낄 달을 한 장에 모은 거예요.", "칠한 동그라미가 힘 쓸 달, 빈 동그라미가 아낄 달이에요.") + "[[M]]" + MID
sec2 = P("<b>열두 띠를 시계처럼 둥글게 놓고, 양(未)과 어떤 자리에 있는지로 갈려요.</b>") + \
       P("🤝 <b>손잡는 쪽</b>", "말(午)은 양과 짝을 이루는 자리(육합)예요.", "돼지(亥)·토끼(卯)는 양과 셋이 모여 나무 기운이 되는 한 팀(삼합)이에요.") + \
       P("🔄 <b>자리가 바뀌는 쪽</b>", "소(丑)는 양과 정면으로 마주 보는 자리(충)예요.", "개(戌)는 소·양과 서로 조율이 필요한 세 글자(형)로 묶여요.", "양띠는 자기 띠가 돌아온 해라 같은 무리에 넣어 읽어요.") + \
       P("자리가 바뀐다는 건 나쁜 일이 온다는 뜻이 아니에요.", "<b>멈춰 있던 것이 움직이기 쉬운 해라는 뜻이에요.</b>") + \
       P("🔢 <b>2027년이 왜 정미년인지</b>", "2027에서 4를 빼면 2023이에요.", "10으로 나눈 나머지 3은 갑·을·병·정의 넷째 글자 정(丁)이에요.",
         "12로 나눈 나머지 7은 자·축·인·묘·진·사·오·미의 여덟째 글자 미(未)예요.", "미(未)는 열두 띠로 양이라 2027년은 양띠 해예요.") + \
       P("🌌 <b>별자리로 보면</b>", "2027년에는 토성과 해왕성이 한 해 내내 양자리에 머물러요.", "목성은 7월 27일 사자자리에서 처녀자리로 옮겨 가요.",
         "띠가 그해의 기운이라면, 별자리는 그해 하늘이 움직이는 순서예요. 둘을 같이 적어 두면 한 해가 덜 흐릿해요.")
sec3 = P("내 띠만 찾아 읽으셔도 돼요.", "띠마다 힘 쓸 달 가운데 한 달을 골라 해 볼 일을 하나씩 붙였어요.")
for i in range(12):
    x = EX[SLUG[i]]
    sec3 += P(f"<b>{NAME[i]} ({yrs(i)}년생)</b>", f"<b>{Z[i][0]}</b>", Z[i][1])
    sec3 += P(f"📅 힘 쓸 달 {' · '.join(GOOD[SLUG[i]])}", f"아낄 달 {' · '.join(CARE[SLUG[i]])}",
              f"🍀 {x['color']} · 숫자 {x['num']} · {x['dir']}", f"✔️ {Z[i][2]}에 해 볼 것: {Z[i][3]}")
sec4 = P("<b>입춘 전이면 앞 해의 띠예요.</b>", "사주에서 띠는 1월 1일이 아니라 입춘에 바뀌어요.") + "[[R]]" + \
       P("🔢 <b>예를 들어 볼게요</b>", "2027년 1월 20일에 태어난 아기는 아직 입춘 전이라 병오(丙午)년, 말띠예요.",
         "2027년 2월 4일 오전 10시 46분 입춘이 지나야 정미년 양띠가 돼요.", "입춘 시각은 해마다 달라서, 2월 3~5일생은 태어난 시간까지 같이 봐야 해요.")
sec5 = P("🧠 <b>심리학으로 읽으면</b>", "'올해는 꼭 해야지'라는 마음만으로는 첫발이 잘 안 떨어져요.",
         "언제, 어디서, 무엇을 할지 미리 정해 두는 계획을 심리학에서는 <b>'실행 의도'</b>라고 해요.",
         "'4월 첫 월요일 아침, 출근하면 바로 그 일을 연다'처럼 때와 행동을 붙여 두면 미루는 일이 줄어든다고 봐요.",
         '📚 <b>출처</b>: <a href="https://doi.org/10.1037/0003-066X.54.7.493">Gollwitzer (1999), American Psychologist</a>') + "[[T]]" + \
       P("그래서 힘 쓸 달은 '좋은 달'로 알고만 있기보다, 그달 첫 주에 할 일 하나를 날짜와 같이 적어 두는 게 좋아요.") + \
       P("🌱 <b>마음 코치 정월의 질문</b>", "새해 운세는 읽는 순간보다<br>달력에 옮기는 순간이 더 중요해요.",
         "🔸 2027년 힘 쓸 달에 꼭 시작하고 싶은<br>한 가지는 무엇인가요?", "🔸 아낄 달에 미뤄 두고 싶은<br>큰 결정은 무엇인가요?") + \
       P("✔️ <b>이번 주에 해 볼 것 하나</b>: 내 띠의 힘 쓸 달 하나를 골라<br>그달 첫 주에 할 일을 날짜와 같이<br>달력에 적어 두세요.")
sec6 = P("<b>Q. 기운이 잘 맞는 띠가 아니면 2027년이 나쁜가요?</b>", "A. 아니에요.", "띠는 태어난 해 한 글자만 본 거예요.",
         "태어난 달·날·시간까지 여덟 글자를 같이 봐야 해서, 같은 띠라도 한 해가 달라요.") + \
       P("<b>Q. 행운의 색과 숫자는 어떻게 정해요?</b>", "A. 내 띠의 기운을 살려 주는 기운에서 가져와요.",
         "예를 들어 물인 쥐띠·돼지띠는 물을 살리는 쇠의 색(흰색·금색)과 쇠의 수(4, 9)예요.") + \
       P("<b>Q. 가족 띠는 어떻게 같이 보면 좋아요?</b>", "A. 위 그림에서 가족끼리 칠한 동그라미가 겹치는 달을 찾아보세요.",
         "그달을 가족 여행이나 큰 계획을 같이 정하는 달로 잡으면 이야기를 꺼내기 쉬워요.") + \
       P("<b>Q. 내 날의 기운은 어디서 볼 수 있나요?</b>", "A. 자오선 사이트에 생년월일만 넣으면 태어난 날의 기운과 2027년 한 줄을 무료로 볼 수 있어요.")
tail = P("여러분 띠의 힘 쓸 달은 몇 월이었나요?", "댓글로 띠와 달을 남겨 주시면 그달에 해 볼 일을 같이 골라 드릴게요.") + \
       '<p><b>👇 같은 띠라도 한 해가 다른 이유가 궁금하다면, 2027년 운세 사주·점성술·수비학·자미두수로 겹쳐 본 정미년 한 해 흐름</b></p>'
secs = [sec1, sec2, sec3, sec4, sec5, sec6]

def _have(n): return os.path.exists(os.path.join(HERE, "img", n))
def build():
    for d_ in ("wide", "m1280", "master"): os.makedirs(os.path.join(HERE, "img", d_), exist_ok=True)
    c = V.Ctx(PAL); made = []
    a4 = f"wide/naver_z{KEY}_a4.jpg"
    if not _have(a4):
        V.render(PID + "_new", {"d": "N", "el": "불", "kick": "2027 띠별 운세", "hook": ["내 띠 힘 쓸 달", "한 장에"], "sub": "정미년 12띠 달력",
                                "items": ["힘 쓸 달", "아낄 달", "1월생 띠"]}, os.path.join(HERE, "img", a4), PAL)
    made.append(a4)
    mrows = [(NAME[i].replace("띠", ""), mon(GOOD[s]), mon(CARE[s])) for i, s in enumerate(SLUG)]
    nm = {"M": f"naver_z{KEY}_m6.jpg", "R": f"naver_z{KEY}_r6.jpg", "T": f"naver_z{KEY}_t6.jpg"}
    if not _have(nm["M"]): DG.months(nm["M"], c, "2027년 내 띠 달력", mrows)
    if not _have(nm["R"]): DGB.route(nm["R"], c, "1월생은 무슨 띠일까", [("1월 1일", "입춘 전까지는 병오년 말띠"), ("2월 4일 10:46", "입춘, 이때부터 정미년"), ("입춘 뒤", "양띠로 읽어요")])
    if not _have(nm["T"]): DGB.twopanel(nm["T"], c, "마음만 먹을 때와 날짜를 붙일 때", ("언젠가 해야지", "때가 없어서 오늘도 미뤄져요", .35),
                                        ("4월 첫 월요일 아침", "때가 오면 바로 할 일이 떠올라요", .85), "실행 의도(Gollwitzer, 1999)", "힘 쓸 달 첫 주에 할 일 하나를 날짜와 같이 적어요")
    # K-137 꽉 찬 폭: 좌우 흰 여백을 잘라 새 이름(…f.jpg)으로. fullbleed.main 은 계획 파일을 이 글로만 덮어써서 convert 를 직접 부르고 계획은 합친다
    import fullbleed as FBL
    plan_p = os.path.join(HERE, "fullbleed_plan.json"); plan = json.load(open(plan_p, encoding="utf-8")) if os.path.exists(plan_p) else {}
    rows = []
    for pos, k in enumerate("MRT", 1):
        f = nm[k][:-4] + "f.jpg"
        if not _have(f):
            r, why = FBL.convert(nm[k], [os.path.join(HERE, "img"), os.path.join(HERE, "img", "m1280")]); assert r, (nm[k], why)
        rows.append({"pos": pos, "old": nm[k], "new": f}); made.append(nm[k]); nm[k] = f
        reg_ = json.load(open(DG.REG, encoding="utf-8")); reg_[f] = reg_[rows[-1]["old"]]; json.dump(dict(sorted(reg_.items())), open(DG.REG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    plan[PID] = rows; json.dump(plan, open(plan_p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    made += list(nm.values())
    alt = {"M": "2027년 12띠별 힘 쓸 달과 아낄 달을 열두 달 칸에 동그라미로 표시한 달력 그림",
           "R": "2027년 1월 1일부터 입춘 전까지는 병오년 말띠, 2월 4일 오전 10시 46분 입춘부터 정미년이라 그 뒤 태어나면 양띠라는 길 그림",
           "T": "언젠가 해야지 하고 마음만 먹을 때보다 4월 첫 월요일 아침처럼 때를 붙일 때 할 일이 더 잘 떠오른다는 실행 의도 비교 그림"}
    body = P(*head) + P("<b>📌 이 글의 순서</b>", *[f"{i + 1}. {q}" for i, q in enumerate(toc_q)])
    for i, (q, s) in enumerate(zip(toc_q, secs)):
        for k in "MRT": s = s.replace(f"[[{k}]]", IMG(nm[k], alt[k]))
        body += H(f"{i + 1}. {q}") + s
    body += tail + CTA
    for w in ("재미로", "상담", "—", "안녕하세요, 자오선의 정월이에요", "결론부터 말씀드릴게요", "반드시", "무조건", "엔진", "손해"):
        assert w not in body, w
    for f in made:   # 사이트 사본(K-069)
        dst = os.path.join(SITE, "public", "naver", "img", f); os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy(os.path.join(HERE, "img", f), dst)
    return body, a4, made

TITLE = "2027 띠별 운세, 정미년 12띠 힘 쓸 달과 아낄 달 한눈에"
TAGS = ["2027띠별운세", "2027년띠별운세", "띠별운세", "정미년운세", "2027대박띠", "2027년운세", "정미년", "힘쓸달", "2027행운의색", "자오선"]
REL = {"id": "n14", "title": "2027년 운세 사주·점성술·수비학·자미두수로 겹쳐 본 정미년 한 해 흐름",
       "phrase": "같은 띠라도 한 해가 다른 이유가 궁금하다면, 2027년 운세 사주·점성술·수비학·자미두수로 겹쳐 본 정미년 한 해 흐름",
       "url": "https://blog.naver.com/zaoseon/224428452763"}
INTENT = {"keywords": ["2027 띠별 운세", "정미년 대박띠", "2027년 띠별운세", "2027 운세 좋은 띠", "정미년 운세"],
          "keyword_src": "n01 유입 검색어 9/29~10/5(data/analytics/naver_blog_inflow_2026-09-29_10-05.json: 정미년·2027년 대박띠·띠별 운세) · 태그 조사 tag_research.json(2027신년운세 월 1,010·2027년띠별운세 180) · 자동완성 자료 없음",
          "intent": "알고 싶다", "intent_note": "내 띠 결과 바로 찾기",
          "first3": "2027년 띠별 운세: 손잡는 일이 잘 풀리는 띠는 말띠·토끼띠·돼지띠, 자리가 크게 바뀌는 띠는 소띠·양띠·개띠예요. 나머지 여섯 띠는 열쇠 한 단어씩.",
          "answer_keys": ["띠별 운세", "말띠·토끼띠·돼지띠"],
          "order": toc_q[:5], "images": ["12띠 힘 쓸 달·아낄 달 달력(months)", "입춘 경계 길 그림(route)", "실행 의도 비교(twopanel, Gollwitzer 1999)"],
          "related": "n14", "cta": PID, "experience": [], "applied": True,
          "differs_from_n01": "제목·도입·소제목 순서·띠별 문장·예시(2027년 1월생 아기)·그림 유형(관계도·표 대신 길 그림·비교)·심리 개념(확증 편향 → 실행 의도)·연결글(n02 → n14)"}

if __name__ == "__main__":
    body, a4, made = build()
    reg = json.load(open(MP.REG, encoding="utf-8"))
    assert PID not in reg or not reg[PID].get("done"), "이미 예약 끝난 글"
    reg[PID] = dict(dt="2026-10-30T11:00:00", title=TITLE, tags=TAGS, body=body, cover=a4, related=REL, thumbs=None, cid=None, clips=None,
                    category="2027 신년운세", done=False, k131="n80 10/29(K-151 새 글)", source="build_naver_80.py (n01 주제 새 글, n01 그대로)")
    json.dump(reg, open(MP.REG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    ic = json.load(open(os.path.join(HERE, "intent_cards.json"), encoding="utf-8")); ic["cards"][PID] = INTENT
    json.dump(ic, open(os.path.join(HERE, "intent_cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    v = reg[PID]; import datetime as D
    MP.write_page(PID, D.datetime.fromisoformat(v["dt"]), v["title"], v["tags"], v["body"], None, v["cover"], v["related"], v["category"])
    MP.write_index()
    print(PID, len(TITLE), "자 제목 · 본문 글자", len(re.sub(r"<[^>]+>|&nbsp;", "", body)), "· 사진", made)
