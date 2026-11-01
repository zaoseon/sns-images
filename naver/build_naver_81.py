"""네이버 n81: 2027 삼재띠 새 글 (CT 11/1 17:20 → ①, 대표 11/1 17:08 "n02로 해 보려고 한다, 같이 바로 진행").
- 왜: n80(n01 주제 새 글)이 11/1 15:16 발행 뒤 바로 검색에 나왔다. 두 번째 시험으로 조회 2위 n02(2027년 삼재띠 총정리)를 새 글로 쓴다.
- 지킨 것: n02는 건드리지 않는다(K-147). 복사하지 않는다(K-151): 제목·도입·소제목 순서·띠별 문장·예시(1996년 1월생)·그림 유형(바퀴·연표 대신 이어달리기·체크리스트·실험)·
  심리 개념(부정성 편향 대신 못 끝낸 목표와 계획 세우기)·연결글(n01 대신 n80)을 모두 새로 썼다. 같은 것은 계산값뿐이다(삼재 묶음·세 해·띠별 달·색은 tti_extra.json).
- n73(날삼재 이사·결혼, 11/3 예약 원고)과 겹치지 않게: 이 글은 '누가·언제부터 언제까지·띠별 한 줄' 허브다. 이사·결혼은 소제목 하나로만 짧게.
- 입춘 시각: zaoseon-site engine/engine.py get_solar_terms_kst(y) 11/1 실행 값 = 1996-02-04 22:07 · 2025-02-03 23:10 · 2027-02-04 10:46 · 2028-02-04 16:31 (아래 TERMS, 사이트 엔진이 있으면 다시 잰다).
- 심리 근거: Masicampo & Baumeister (2011), JPSP, DOI 10.1037/a0024192 (zaoseon-site docs/심리근거카드_마음_임상대조_H09-H16.md 에 있는 카드).
사용: SITE=<zaoseon-site> python3 naver/build_naver_81.py   (pages.json 에 n81을 넣고 사이트 원고 페이지 n81.html·목록만 다시 쓴다. render_all 은 부르지 않는다)"""
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
       '<tr><td style="padding:12px 10px;text-align:center;border:1px solid #d0d0d0"><b>생년월일만 넣으면 1초</b></td></tr>'
       '<tr><td style="padding:12px 10px;text-align:center;border:1px solid #d0d0d0"><span style="color:#9a9a9a">[ 1990 . 03 . 15 ]</span></td></tr>'
       '<tr><td style="padding:12px 10px;text-align:center;border:1px solid #d0d0d0"><b><a href="https://zaoseon.com/?utm_source=naver&amp;utm_medium=mid#free">내 태어난 날 글자 보기 →</a></b></td></tr>'
       '</tbody></table>' + BL)
CTA = ('<p><a href="https://zaoseon.com/?utm_source=naver&utm_medium=cta#free"><img src="' + RAW +
       'naver_cta5_1%EC%B4%88%EB%AC%B4%EB%A3%8C%ED%92%80%EC%9D%B4.jpg" alt="자오선 무료 1초 풀이 안내 배너"></a></p>')
PID, KEY, PAL = "n81", "81", "y_olive"   # 미(未)=흙 → 올리브 판(n02와 다른 판)

# ───────── 계산값과 검산
BR = "子丑寅卯辰巳午未申酉戌亥"; GAN = "甲乙丙丁戊己庚辛壬癸"
def gz(y): return GAN[(y - 4) % 10] + BR[(y - 4) % 12]
assert [gz(y) for y in (2025, 2026, 2027, 2028, 2029, 2030)] == ["乙巳", "丙午", "丁未", "戊申", "己酉", "庚戌"]
assert [gz(y) for y in (2037, 2038, 2039)] == ["丁巳", "戊午", "己未"]
GROUPS = ["亥卯未", "寅午戌", "巳酉丑", "申子辰"]           # 삼합 묶음. 첫 글자(생지)와 마주 보는(충) 글자의 해부터 3년
def start(g): return (BR.index(g[0]) + 6) % 12
def first_year(g, after=2024):
    y = after + 1
    while BR[(y - 4) % 12] != BR[start(g)]: y += 1
    return y
assert [first_year(g) for g in GROUPS] == [2025, 2028, 2031, 2034]
assert first_year("亥卯未", 2027) == 2037
assert BR.index("亥") == 11 and BR.index("巳") == 5                # 시계판: 돼지 11시, 뱀 5시(맞은편)
# 입춘(engine.get_solar_terms_kst, 11/1 실행 값). 사이트 엔진이 돌면 다시 잰다.
TERMS = {1996: "02-04 22:07", 2025: "02-03 23:10", 2027: "02-04 10:46", 2028: "02-04 16:31"}
try:
    sys.path.insert(0, os.path.join(SITE, "engine")); import engine as EN
    for y, s in TERMS.items():
        t = [x for x in EN.get_solar_terms_kst(y) if x[0] == "입춘"][0][2]
        assert t.strftime("%m-%d %H:%M") == s, (y, t)
    print("입춘 시각 엔진으로 다시 확인")
except ImportError:
    print("엔진 없음: 11/1 실행 값으로 씀")
EX = json.load(open(os.path.join(SITE, "tools", "tti_extra.json"), encoding="utf-8"))
SLUG = ["rat", "ox", "tiger", "rabbit", "dragon", "snake", "horse", "sheep", "monkey", "rooster", "dog", "pig"]
def yrs(i, n=5): return ", ".join([str(y) for y in range(1960, 2027) if (y - 4) % 12 == i][-n:])
assert yrs(11) == "1971, 1983, 1995, 2007, 2019" and yrs(7) == "1967, 1979, 1991, 2003, 2015"
assert yrs(3, 6) == "1963, 1975, 1987, 1999, 2011, 2023"
assert gz(1995) == "乙亥" and gz(1996) == "丙子"                  # 1996년 1월 25일생 = 입춘(2/4 22:07) 전 → 을해년 돼지띠
GOOD = {s: EX[s]["good"] for s in SLUG}; CARE = {s: EX[s]["care"] for s in SLUG}
# 오행: 卯=나무, 未=흙, 亥=물, 丁=불. 나무→불(내 힘이 나감), 불→흙(나를 채워 줌), 물이 불을 이김(재물)
EL = dict(zip(BR, "물 흙 나무 나무 흙 불 불 흙 쇠 쇠 흙 물".split()))
assert (EL["卯"], EL["未"], EL["亥"]) == ("나무", "흙", "물")

# ───────── 세 띠 새 문장(n02 문장을 옮기지 않았다). 해 볼 것의 달은 그 띠의 힘 쓸 달 안에서만 고른다(아래 assert).
Z = [  # (번호, 이름, 해들, 한 줄, 왜, 해 볼 달, 해 볼 것)
 (11, "돼지띠", yrs(11), "들어오는 사람을 고르는 해",
  "돼지(亥)는 2027년의 양(未)과 한 팀으로 묶여요(삼합). 마지막 해에도 소개와 모임이 이어지기 쉬워요. 다 이어 가기보다 남길 인연을 고를수록 2028년이 가벼워요.",
  "3월", "올해 이어 갈 모임 하나만 남기고 나머지는 쉬어 가기"),
 (3, "토끼띠", yrs(3, 6), "일정이 몰리는 만큼 덜어 내는 해",
  "토끼(卯)는 나무 기운이고, 2027년의 불(丁)을 키우는 쪽이에요. 힘이 밖으로 나가는 해라 맡는 일이 늘기 쉬워요. 하반기에 지치지 않게 미리 덜어 두는 게 열쇠예요.",
  "10월", "하반기 달력에서 빼도 되는 약속 하나 지우기"),
 (7, "양띠", yrs(7), "내 해와 마지막 해가 겹치는 해",
  "2027년은 양(未)의 해라 양띠에게는 띠가 돌아온 해(본명년)예요. 해의 불(丁)이 양띠의 흙을 데워 주는 모양이라, 새로 늘리기보다 배우고 채우는 일에 힘이 실려요.",
  "6월", "배우고 싶던 것 하나에 등록하기"),
]
for i, n, _, _, _, m, _ in Z: assert m in GOOD[SLUG[i]], (n, m)

# ───────── 본문
head = ["<b>2027년 삼재띠는 돼지띠·토끼띠·양띠예요.</b>",
        "세 띠 모두 2025년에 들어온 삼재의 마지막 해, 날삼재를 맞아요.",
        "<b>이 삼재는 2028년 2월 4일 오후 4시 31분 입춘에 끝나고, 그때부터 호랑이띠·말띠·개띠의 삼재가 시작돼요.</b>",
        "연말에 가족끼리 내년 이야기를 하다 보면 '우리 집에 삼재 든 사람 있나?'부터 묻게 되죠. 누가, 언제부터 언제까지인지 날짜로 정리했어요.",
        "2026년 11월 1일 기준으로 정리한 내용이에요."]
toc_q = ["우리 집에 2027 삼재띠가 있을까요?", "삼재는 정확히 언제 시작해서 언제 끝날까요?", "같은 날삼재라도 띠마다 무엇이 다를까요?",
         "이사나 결혼을 앞두고 있다면요?", "못 끝낸 일이 자꾸 떠오른다면?", "자주 묻는 질문"]

sec1 = P("<b>태어난 해로 바로 찾아보세요.</b>") + \
       P("🐷 돼지띠: " + yrs(11) + "년생", "🐰 토끼띠: " + yrs(3, 6) + "년생", "🐑 양띠: " + yrs(7) + "년생") + \
       P("🔢 <b>1월이나 2월 초에 태어났다면</b>", "띠는 1월 1일이 아니라 입춘에 바뀌어요.",
         "1996년 1월 25일생은 그해 입춘(2월 4일 밤 10시 7분)보다 앞이라 쥐띠가 아니라 1995년 을해(乙亥)년 돼지띠예요.",
         "그래서 2월 3~5일생은 태어난 시간까지 같이 봐야 띠가 정해져요.") + MID
sec2 = P("<b>삼재는 세 해, 입춘에서 입춘까지예요.</b>") + \
       P("🌱 <b>들삼재</b>: 2025년 을사(乙巳)년, 2월 3일 밤 11시 10분 입춘부터", "🌿 <b>눌삼재</b>: 2026년 병오(丙午)년",
         "🍂 <b>날삼재</b>: 2027년 정미(丁未)년, 2월 4일 오전 10시 46분 입춘부터", "🚪 <b>끝</b>: 2028년 2월 4일 오후 4시 31분 입춘") + \
       P("🕰️ <b>시계판으로 찾는 법</b>", "열두 띠를 시계판에 놓으면 쥐가 12시, 돼지가 11시, 뱀이 5시 자리예요.",
         "돼지·토끼·양은 한 묶음(삼합)이고, 묶음의 맨 앞 띠인 돼지의 맞은편이 뱀이에요.",
         "그래서 뱀의 해 2025년부터 말·양의 해까지 세 해가 이 묶음의 삼재예요.") + \
       P("아래 그림처럼 묶음마다 세 해씩 이어달리기를 해요.", "칠한 칸이 지금 날삼재를 맞는 묶음이에요.") + "[[L]]"
sec3 = P("세 띠가 같은 날삼재여도, 2027년의 정미(丁未)와 만나는 모양은 달라요.", "내 띠만 찾아 읽으셔도 돼요.")
for i, n, ys, one, why, m, todo in Z:
    x = EX[SLUG[i]]
    sec3 += P(f"<b>{n} ({ys}년생)</b>", f"<b>{one}</b>", why)
    sec3 += P(f"📅 힘 쓸 달 {' · '.join(GOOD[SLUG[i]])}", f"아낄 달 {' · '.join(CARE[SLUG[i]])}",
              f"🍀 {x['color']} · 숫자 {x['num']} · {x['dir']}", f"✔️ {m}에 해 볼 것: {todo}")
sec4 = P("<b>삼재라는 이유만으로 큰일을 미룰 까닭은 없어요.</b>", "날삼재는 옛말로 '나가는 해'라, 막는 해보다 마무리를 챙기는 해로 읽어요.",
         "날짜보다 잔금일·만기일·식장 계약 같은 조건을 먼저 맞춰 보세요.")
sec5 = P("🧠 <b>심리학으로 읽으면</b>", "삼재 마지막 해에는 '그때 시작만 해 둔 일'이 자꾸 떠오르기 쉬워요.",
         "못 끝낸 일은 다른 일을 하는 중에도 머릿속에 끼어든다고 해요.",
         "마시캄포와 바우마이스터(2011)는 그 일을 <b>언제, 어떻게 할지 계획만 적어도</b> 생각이 덜 끼어든다는 것을 실험으로 보였어요.",
         '📚 <b>출처</b>: <a href="https://doi.org/10.1037/a0024192">Masicampo &amp; Baumeister (2011), Journal of Personality and Social Psychology</a>') + "[[E]]" + \
       P("끝내는 것까지 한 번에 하지 않아도 돼요.", "다음 첫 동작과 날짜만 붙여 두면, 그 일은 머릿속이 아니라 달력에서 기다려요.") + "[[K]]" + \
       P("🌱 <b>마음 코치 정월의 질문</b>", "세 해를 지나오는 동안<br>마음 한쪽에 남은 일이 있을 거예요.",
         "🔸 요즘 자꾸 떠오르는 못 끝낸 일은<br>무엇인가요?", "🔸 그 일의 다음 첫 동작을<br>한 줄로 적는다면요?") + \
       P("✔️ <b>이번 주에 해 볼 것 하나</b>: 떠오르는 일 하나에<br>다음 첫 동작과 날짜를 붙여<br>달력에 적어 두세요.")
sec6 = P("<b>Q. 2028년 삼재띠는 누구예요?</b>", "A. 호랑이띠·말띠·개띠예요.",
         "2028년 무신(戊申)년이 들삼재, 2029년 기유(己酉)년이 눌삼재, 2030년 경술(庚戌)년이 날삼재예요.") + \
       P("<b>Q. 돼지·토끼·양띠의 다음 삼재는 언제예요?</b>", "A. 12년 뒤인 2037년 정사(丁巳)년부터 2039년 기미(己未)년까지예요.") + \
       P("<b>Q. 날삼재가 세 해 중 가장 가벼운가요?</b>", "A. 정해진 무게는 없어요.",
         "같은 띠라도 태어난 달·날·시간의 여덟 글자가 달라서, 삼재를 지나는 모양도 사람마다 달라요.") + \
       P("<b>Q. 부적이나 풀이를 꼭 해야 하나요?</b>", "A. 꼭 필요한 건 아니에요.", "마음이 놓이는 방법을 고르면 되고, 큰돈을 요구하는 곳은 한 번 더 생각해 보세요.")
tail = P("여러분 집에는 2027 삼재띠가 몇 명인가요?", "댓글로 띠를 남겨 주시면 그 띠의 힘 쓸 달을 같이 찾아 드릴게요.") + \
       '<p><b>👇 띠마다 힘 쓸 달을 한 장으로 보고 싶다면, 2027 띠별 운세, 정미년 12띠 힘 쓸 달과 아낄 달 한눈에</b></p>'
secs = [sec1, sec2, sec3, sec4, sec5, sec6]

def _have(n): return os.path.exists(os.path.join(HERE, "img", n))
def build():
    for d_ in ("wide", "m1280", "master"): os.makedirs(os.path.join(HERE, "img", d_), exist_ok=True)
    c = V.Ctx(PAL); made = []
    a4 = f"wide/naver_z{KEY}_a4.jpg"
    if not _have(a4):
        V.render(PID + "_new", {"d": "N", "el": "흙", "kick": "2027 삼재띠", "hook": ["삼재 끝나는 날", "2028년 2월 4일"], "sub": "돼지띠 · 토끼띠 · 양띠",
                                "items": ["누가", "언제까지", "띠별 한 줄"]}, os.path.join(HERE, "img", a4), PAL)
    made.append(a4)
    nm = {"L": f"naver_z{KEY}_l7.jpg", "E": f"naver_z{KEY}_e6.jpg", "K": f"naver_z{KEY}_h6.jpg"}
    if not _have(nm["L"]):
        DGB.relay(nm["L"], c, "삼재 이어달리기", [
            ("亥卯未", [("돼지·토끼·양", 0, 1 / 3, "acc")]), ("寅午戌", [("호랑이·말·개", 1 / 3, 2 / 3, "out")]),
            ("巳酉丑", [("뱀·닭·소", 2 / 3, 1, "out")])],
            [(0, "2025"), (1 / 3, "2028"), (2 / 3, "2031"), (1, "2033")], "다음은 원숭이·쥐·용띠 2034~2036")
    if not _have(nm["E"]):
        DGC.exp(nm["E"], c, "못 끝낸 일, 계획만 적어도", "마시캄포·바우마이스터 · 2011",
                [("1", "못 끝낸 일 하나를 떠올려요"), ("2", "한쪽만 언제·어떻게 할지 계획을 적어요"), ("3", "모두 다른 과제를 해요")],
                "계획을 적은 쪽은 그 일이 덜 끼어들었어요", "Masicampo & Baumeister (2011), JPSP")
    if not _have(nm["K"]):
        DGB.checklist(nm["K"], c, "날삼재 매듭 세 칸", [("자꾸 떠오르는 못 끝낸 일 적기", "한 줄에 하나씩"),
                      ("일마다 다음 첫 동작 붙이기", "'서류 봉투 열기'처럼 작게"), ("그 동작을 할 날짜 적기", "2028년 2월 4일 입춘 전으로")], "빈 칸은 직접 채워 보세요")
    import fullbleed as FBL
    plan_p = os.path.join(HERE, "fullbleed_plan.json"); plan = json.load(open(plan_p, encoding="utf-8")) if os.path.exists(plan_p) else {}
    rows = []
    for pos, k in enumerate("LEK", 1):
        f = nm[k][:-4] + "f.jpg"
        if not _have(f):
            r, why = FBL.convert(nm[k], [os.path.join(HERE, "img"), os.path.join(HERE, "img", "m1280")]); assert r, (nm[k], why)
        rows.append({"pos": pos, "old": nm[k], "new": f}); made.append(nm[k]); nm[k] = f
        reg_ = json.load(open(DG.REG, encoding="utf-8")); reg_[f] = reg_[rows[-1]["old"]]; json.dump(dict(sorted(reg_.items())), open(DG.REG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    plan[PID] = rows; json.dump(plan, open(plan_p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    made += list(nm.values())
    alt = {"L": "삼재 묶음이 세 해씩 이어지는 그림. 돼지·토끼·양띠 2025~2027, 호랑이·말·개띠 2028~2030, 뱀·닭·소띠 2031~2033, 다음은 원숭이·쥐·용띠 2034~2036",
           "E": "못 끝낸 일을 떠올린 뒤 한쪽만 언제 어떻게 할지 계획을 적게 하자, 계획을 적은 쪽은 다른 과제를 하는 동안 그 일이 덜 떠올랐다는 마시캄포·바우마이스터 2011 실험 그림",
           "K": "날삼재 매듭 체크리스트: 자꾸 떠오르는 못 끝낸 일 적기, 일마다 다음 첫 동작 붙이기, 2028년 2월 4일 입춘 전으로 날짜 적기"}
    body = P(*head) + P("<b>📌 이 글의 순서</b>", *[f"{i + 1}. {q}" for i, q in enumerate(toc_q)])
    for i, (q, s) in enumerate(zip(toc_q, secs)):
        for k in "LEK": s = s.replace(f"[[{k}]]", IMG(nm[k], alt[k]))
        body += H(f"{i + 1}. {q}") + s
    body += tail + CTA
    for w in ("재미로", "상담", "—", "안녕하세요, 자오선의 정월이에요", "결론부터 말씀드릴게요", "반드시", "무조건", "엔진", "손해"):
        assert w not in body, w
    for f in made:   # 사이트 사본(K-069)
        dst = os.path.join(SITE, "public", "naver", "img", f); os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy(os.path.join(HERE, "img", f), dst)
    return body, a4, made

TITLE = "2027 삼재띠 돼지띠 토끼띠 양띠, 날삼재 끝나는 날과 2028 삼재"
TAGS = ["2027삼재띠", "삼재띠", "2027삼재", "날삼재", "삼재끝나는날", "돼지띠삼재", "토끼띠삼재", "양띠삼재", "2028삼재띠", "자오선"]
REL = {"id": "n80", "title": "2027 띠별 운세, 정미년 12띠 힘 쓸 달과 아낄 달 한눈에",
       "phrase": "띠마다 힘 쓸 달을 한 장으로 보고 싶다면, 2027 띠별 운세, 정미년 12띠 힘 쓸 달과 아낄 달 한눈에",
       "url": "https://blog.naver.com/zaoseon/224461125363"}
INTENT = {"keywords": ["2027 삼재띠", "2027년 삼재", "날삼재", "삼재 끝나는 날", "2028 삼재띠"],
          "keyword_src": "n02 태그·유입(조회 2위, 10/3~10/31 조회 162) · n02 태그(2027년삼재띠·날삼재·2028삼재띠) · 자동완성 자료 없음(발행 7일 뒤 유입 검색어로 고친다)",
          "intent": "알고 싶다", "intent_note": "우리 집에 삼재띠가 있는지, 언제 끝나는지 날짜로 확인",
          "first3": "2027년 삼재띠는 돼지띠·토끼띠·양띠예요. 셋 다 날삼재(마지막 해)이고, 2028년 2월 4일 오후 4시 31분 입춘에 끝나며 그때부터 호랑이띠·말띠·개띠 삼재가 시작돼요.",
          "answer_keys": ["삼재띠", "돼지띠·토끼띠·양띠"],
          "order": toc_q[:5], "images": ["네 삼재 묶음 이어달리기(relay)", "계획 세우기 실험(exp, Masicampo & Baumeister 2011)", "날삼재 매듭 체크리스트(checklist)"],
          "related": "n80", "cta": PID, "experience": [], "applied": True,
          "differs_from_n02": "제목·도입(끝나는 날짜 직답)·소제목 순서·띠별 문장·예시(1996년 1월생)·계산법 설명(시계판)·그림 유형(바퀴·연표 → 이어달리기·실험·체크리스트)·심리 개념(부정성 편향 → 못 끝낸 목표와 계획)·연결글(n01 → n80)",
          "vs_n73": "n73(이사·결혼 판단)은 소제목 4 하나로만 짧게, 오해 목록·정서 예측 오류는 넣지 않음"}

if __name__ == "__main__":
    body, a4, made = build()
    reg = json.load(open(MP.REG, encoding="utf-8"))
    assert PID not in reg or not reg[PID].get("done"), "이미 예약 끝난 글"
    reg[PID] = dict(dt="2026-11-02T18:00:00", title=TITLE, tags=TAGS, body=body, cover=a4, related=REL, thumbs=None, cid=None, clips=None,
                    category="2027 신년운세", done=False, k131="n81 11/1(K-151 새 글)", source="build_naver_81.py (n02 주제 새 글, n02 그대로)")
    json.dump(reg, open(MP.REG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    ic = json.load(open(os.path.join(HERE, "intent_cards.json"), encoding="utf-8")); ic["cards"][PID] = INTENT
    json.dump(ic, open(os.path.join(HERE, "intent_cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    v = reg[PID]; import datetime as D
    MP.write_page(PID, D.datetime.fromisoformat(v["dt"]), v["title"], v["tags"], v["body"], None, v["cover"], v["related"], v["category"])
    MP.write_index()
    print(PID, len(TITLE), "자 제목 · 본문 글자", len(re.sub(r"<[^>]+>|&nbsp;", "", body)), "· 사진", made)
