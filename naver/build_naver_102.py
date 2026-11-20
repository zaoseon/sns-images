"""네이버 n102: 좋아하는 티가 안 나는 이유 새 글 (CT 11/4 19:40 재발행 일정 '새 글로 다시 쓰기' n26 → n102, 진행표 docs/네이버_누락글_진행표_2026-11-18.md 아홉째 줄).
- 왜: 노출 안 되는 옛 글 n26(좋아해도 티가 하나도 안 나는 사람의 공통점, 사주·별자리·숫자)을 새 글로. n26은 건드리지 않는다(K-147·K-178). n26은 클립이 걸려 옛 글 비공개 카드에서 빠진다(진행표).
- 검색어: 첫 묶음(좋아하는사람앞에서 10·무심한척 10·호감표현 25·좋아하는티 15·호감신호 85)이 모두 월 100 아래라(K-162) 둘째 묶음으로 바꿈: 짝사랑 5,370·식신 3,760·호감 2,550·식상 530(kw_volume 11/20).
- 다르게 쓴 것(K-151): n26의 첫 장면·'결론부터'·한 줄 요약·세 풀이(戊·癸 일간·염소/물병자리·수비학 4·7)·'몇 개나 겹칠까'·시라노·투명성 착각(Gilovich 외 1998) 대신
  표현을 맡는 글자 식상(식신·상관) 직답, 일간별 식상 오행 다섯 줄, 예시 1993.12.10 오전 8시생(癸酉·甲子·乙丑·庚辰, 乙 일간인데 불 글자가 지장간까지 하나도 없음, engine assert),
  2027 丁 = 乙 식신·甲 상관(ten_god assert), 巳·午 달 5/6~7/6(절기 assert), 심리 = 호감 격차(Boothby, Cooney, Sandstrom & Clark 2018, 5분 대화 실제 5.82 vs 짐작 5.17).
  그림 유형 ladder·vbar·chat. 연결글 → n91(첫눈에 반하는 이유, 11/20 노출 '예' 1위).
- 출처 2개(K-162, 11/20 원문 확인): Boothby, Cooney, Sandstrom & Clark (2018), The liking gap in conversations, Psychological Science 29(11) 1742-1756, DOI 10.1177/0956797618783714
  (와튼 교수진 페이지 PDF 본문: 연구 다섯, 연구 1a 낯선 두 사람 36명 약 5분 대화, 7점 척도 실제 호감 5.82·짐작 5.17, 연구 3 대화 2~45분에도 격차 유지, APS 보도자료: 기숙사 룸메이트 격차가 몇 달 이어짐)
  · 한국천문연구원 음양력 변환(절기 시각).
- 날짜: CT가 정한다. pages.json dt 는 자리값, dt_tbd 로 표시.
사용: SITE=<zaoseon-site> python3 naver/build_naver_102.py"""
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
       '<tr><td style="padding:12px 10px;text-align:center;border:1px solid #d0d0d0"><b>내 여덟 글자에 표현 글자가 있는지 궁금하다면</b></td></tr>'
       '<tr><td style="padding:12px 10px;text-align:center;border:1px solid #d0d0d0"><span style="color:#9a9a9a">[ 1993 . 12 . 10 ]</span></td></tr>'
       '<tr><td style="padding:12px 10px;text-align:center;border:1px solid #d0d0d0"><b><a href="https://zaoseon.com/?utm_source=naver&amp;utm_medium=mid#free">내 태어난 날 글자 보기 →</a></b></td></tr>'
       '</tbody></table>' + BL)
CTA = ('<p><a href="https://zaoseon.com/?utm_source=naver&utm_medium=cta#free"><img src="' + RAW +
       'naver_cta5_1%EC%B4%88%EB%AC%B4%EB%A3%8C%ED%92%80%EC%9D%B4.jpg" alt="자오선 무료 1초 풀이 안내 배너"></a></p>')
PID, KEY, PAL = "n102", "102", "g_ivory_s"   # 예시 일간 乙 = 나무 판 묶음(EL_SET 나무). n101 y_black_s · n100 dg_gold_s 와 다른 판

# ───────── 계산값과 검산
import datetime as D
sys.path.insert(0, os.path.join(SITE, "engine"))
import engine as E
HIDDEN = {"子": "壬癸", "丑": "癸辛己", "寅": "戊丙甲", "卯": "甲乙", "辰": "乙癸戊", "巳": "戊庚丙", "午": "丙己丁", "未": "丁乙己",
          "申": "戊壬庚", "酉": "庚辛", "戌": "辛丁戊", "亥": "戊甲壬"}   # 지장간(통용 기준)
X = D.datetime(1993, 12, 10, 8, 0)
PX = E.compute_saju(X)["팔자"]
assert PX == {"년주": "癸酉", "월주": "甲子", "일주": "乙丑", "시주": "庚辰"}, PX
assert E.compute_saju(D.datetime(1993, 12, 10, 8, 40))["팔자"] == PX            # 같은 辰시 안
allc = "".join(PX.values()) + "".join(HIDDEN[p[1]] for p in PX.values())
assert not set("丙丁巳午") & set(allc)                                          # 乙의 표현 글자(불)가 지장간까지 없음
assert sum(ch in "壬癸子" for ch in allc) >= 5                                   # 물(인성) 많음: 癸·子·丑 속 癸·辰 속 癸·子 속 壬癸
assert E.ten_god("乙", "庚") == "정관" and E.ten_god("乙", "癸") == "편인"
assert E.ten_god("乙", "丁") == "식신" and E.ten_god("甲", "丁") == "상관"
assert E.compute_saju(D.datetime(2027, 3, 1, 12))["팔자"]["년주"] == "丁未"
T = dict((n, t) for n, _, t in E.get_solar_terms_kst(2027))
a_, b_ = T["입하"], T["소서"] - D.timedelta(days=1)
assert (a_.month, a_.day, b_.month, b_.day) == (5, 6, 7, 6), (a_, b_)
for d_ in (D.datetime(2027, 5, 20, 12), D.datetime(2027, 6, 20, 12)): assert E.compute_saju(d_)["팔자"]["월주"][1] in "巳午"
print("예시 乙丑 일간 · 불 글자 지장간까지 없음 · 2027 丁 = 乙 식신·甲 상관 · 巳午 달 5/6~7/6 확인")

# ───────── 본문 (n26 문장을 옮기지 않았다)
head = ["<b>짝사랑하는 마음이 티가 안 나는 건 마음이 작아서가 아니라, 마음을 겉으로 꺼내는 길이 좁아서예요. 사주에서는 이 길을 맡는 글자를 식상이라고 불러요.</b>",
        "식상은 내 일간이 낳는 오행이에요. 편하게 나오는 쪽을 식신, 또렷하게 나오는 쪽을 상관이라고 해요. 여덟 글자에 식상이 적으면 마음이 커져도 말과 표정으로 늦게 나와요.",
        "<b>심리학의 5분 대화 실험에서는 상대가 나를 좋아한 만큼보다 내가 짐작한 호감이 늘 낮았어요. 7점 만점에 실제 5.82, 짐작 5.17이었어요.</b>",
        "이 글은 표현 글자 찾는 법, 예시 한 명, 호감 격차 실험, 2027년 표현 글자가 들어오는 사람, 말 한 줄로 바꿔 보는 법까지 다뤄요."]
toc_q = ["짝사랑할 때 마음을 꺼내는 글자는 무엇일까요?", "1993년 12월 10일 오전 8시생은 어떻게 읽을까요?", "상대는 정말 내 마음을 모를까요?",
         "2027년 표현 글자가 들어오는 사람은 누구일까요?", "좋아하는 마음을 말 한 줄로 바꾸려면", "자주 묻는 질문"]
sec1 = P("<b>식상은 일간마다 정해져 있어요. 내 일간이 키워 주는 오행이 곧 표현 글자예요.</b>") + "[[L]]" + \
       P("식신은 편하게 흘러나오는 표현, 상관은 날이 서고 또렷한 표현으로 봐요. 둘 중 하나라도 여덟 글자에 있으면 마음이 겉으로 나올 길이 있는 거예요.",
         "글자 겉에 없어도 아래 글자 속에 숨은 글자(지장간)로 있으면 천천히 나와요. 겉에도 속에도 없으면 마음이 생겨도 한참 안에 머무는 편이에요.") + MID
sec2 = P("🔎 <b>1993년 12월 10일 오전 8시에 태어난 사람을 예로 들어 볼게요.</b>",
         "여덟 글자는 癸酉·甲子·乙丑·庚辰, 일간은 을(乙) 나무예요. 을의 표현 글자는 불(병·정·사·오)인데, 이 사주에는 불이 겉에도 속에도 하나도 없어요.",
         "대신 물이 많아요. 癸와 子가 겉에 있고, 丑과 辰 속에도 癸가 숨어 있어요. 물은 을에게 생각하고 받아들이는 글자라, 마음이 생기면 말보다 생각이 먼저 길어져요.") + \
       P("시간 기둥의 庚은 을에게 정관, 스스로를 단정하게 다잡는 글자예요. 좋아하는 사람 앞에서 더 반듯해지고 더 조용해지는 모양이 여기서 나와요.",
         "이런 사람은 마음이 없는 게 아니라 확인이 끝난 뒤에야 꺼내요. 상대 쪽에서는 그 사이가 '관심 없음'으로 보이기 쉬워요.",
         '📚 <b>출처 2</b>: <a href="https://astro.kasi.re.kr/life/pageView/5">한국천문연구원 천문우주지식정보, 음양력 변환(절기 시각)</a>')
sec3 = P("🧠 <b>티가 안 날까 봐 걱정되는 마음, 심리학에서는 반대쪽 결과가 나왔어요.</b>",
         "심리학자 부스비·쿠니·샌드스트롬·클라크는 처음 만난 두 사람에게 5분쯤 이야기를 나누게 했어요. 그리고 '상대가 얼마나 좋았는지'와 '상대가 나를 얼마나 좋아했을 것 같은지'를 따로 물었어요.") + "[[B]]" + \
       P("상대가 실제로 나를 좋아한 점수는 7점 만점에 5.82였는데, 내가 짐작한 점수는 5.17이었어요. 사람들은 상대의 호감을 늘 낮춰 짐작했어요. 연구진은 이것을 '호감 격차'라고 불렀어요.",
         "대화를 길게 해도, 실제 모임에서 해도 격차는 그대로였고, 기숙사 룸메이트 사이에서는 몇 달 동안 이어졌어요. 대화 중에 나에 대한 걱정에 마음을 쓰느라 상대가 보낸 신호를 놓치기 때문이에요.",
         "그러니 티가 안 나서 걱정이라면, 상대도 같은 걱정을 하고 있을 가능성이 커요. 내가 받은 호감은 생각보다 크고, 내가 보낸 신호도 생각보다 덜 보여요.",
         '📚 <b>출처 1</b>: <a href="https://doi.org/10.1177/0956797618783714">Boothby, Cooney, Sandstrom &amp; Clark (2018), The liking gap in conversations: Do people like us more than we think? Psychological Science</a>')
sec4 = P("<b>2027년은 해의 첫 글자가 丁(불)이에요. 丁은 을(乙) 일간에게 식신, 갑(甲) 일간에게 상관이라, 나무 일간에게는 표현 글자가 들어오는 해예요.</b>",
         "예시의 을 일간처럼 여덟 글자에 불이 없던 사람은 2027년에 말이 먼저 나오는 경험을 하기 쉬워요. 미뤄 둔 고백이나 오래 아낀 한마디를 꺼내기 좋은 해로 봐요.",
         "특히 巳·午 달, 2027년 5월 6일부터 7월 6일 무렵은 불이 가장 강한 때라 표현이 한 번 더 또렷해져요.") + \
       P("다른 일간에게도 丁은 저마다 뜻이 있어요. 병·정 일간에게는 같은 기운이 와서 자기 색이 짙어지고, 무·기 일간에게는 나를 받쳐 주는 글자가 와요. 내 일간에서 丁이 무엇인지 먼저 찾아보세요.")
sec5 = P("<b>표현 글자가 적어도 말은 연습으로 늘어요. 길게 쓸 필요 없이 한 줄이면 충분해요.</b>") + "[[C]]" + \
       P("🌱 <b>마음 코치 정월의 질문</b>", "좋아하는 사람이 내 마음을<br>10점 중 몇 점쯤 알 것 같나요?",
         "🔸 그 점수를 1점 올릴<br>한 줄은 무엇일까요?") + \
       P("✔️ <b>이번 주에 해 볼 세 가지</b>",
         "1. 행동으로 챙긴 일에 이유 한 줄을 붙여 보세요. 예: '네가 좋아할 것 같아서 샀어.'",
         "2. 대화가 끝나면 상대가 웃었던 순간 하나를 떠올려 적어 보세요. 놓친 신호를 다시 보는 연습이에요.",
         "3. 마음이 커진 날, 그날 안에 짧은 연락 하나를 먼저 보내 보세요. 확인이 끝나길 기다리지 않아도 돼요.")
sec6 = P("<b>Q. 식상이 없으면 연애를 못 하나요?</b>",
         "A. 아니에요. 표현이 늦을 뿐 마음의 깊이와는 상관없어요. 오히려 한 번 꺼낸 말이 무겁고 오래가는 사람이 많아요.") + \
       P("<b>Q. 상대가 티를 안 내면 나를 안 좋아하는 건가요?</b>",
         "A. 꼭 그렇지는 않아요. 위 실험처럼 사람들은 상대의 호감을 낮춰 짐작하는 버릇이 있어요. 짐작보다 상대의 행동이 꾸준한지를 보는 편이 정확해요.") + \
       P("<b>Q. 태어난 시간을 모르면 식상을 못 보나요?</b>",
         "A. 일간과 년·월·일 글자만으로도 대부분 보여요. 시간 기둥에만 식상이 있는 경우도 있으니, 시간을 알면 한 번 더 확인해 보세요.")
tail = P("짝사랑하는 사람이 내 마음을 몇 점쯤 안다고 생각하나요?", "10점 중 숫자 하나만 댓글에 남겨 주세요. 다음 주에 다시 적어 보면 달라져 있을 거예요.") + \
       '<p><b>👇 첫눈에 끌리는 사주와 천천히 끌리는 사주를 더 보고 싶다면, 첫눈에 반하는 이유, 끌림이 빠른 사주와 느린 사주 신호 4가지</b></p>'
secs = [sec1, sec2, sec3, sec4, sec5, sec6]

def _have(n): return os.path.exists(os.path.join(HERE, "img", n))
def build():
    for d_ in ("wide", "m1280", "master"): os.makedirs(os.path.join(HERE, "img", d_), exist_ok=True)
    c = V.Ctx(PAL); made = []
    a4 = f"wide/naver_z{KEY}_a5.jpg"   # 표지 항목은 한글만(한자는 글꼴에 없어 네모, 11/18 n96 a4)
    if not _have(a4):
        V.render(PID + "_new", {"d": "N", "el": "나무", "kick": "짝사랑 티가 안 나는 이유", "hook": ["마음은 큰데", "말이 늦게 나와요"], "sub": "5분 대화 실험과 사주 표현 글자",
                                "items": ["식신", "상관", "2027"]}, os.path.join(HERE, "img", a4), PAL)
    made.append(a4)
    nm = {"L": f"naver_z{KEY}_l3.jpg", "B": f"naver_z{KEY}_v3.jpg", "C": f"naver_z{KEY}_c3.jpg"}
    if not _have(nm["L"]):
        DGB.ladder(nm["L"], c, "내 일간의 표현 글자", [("갑·을", "불이 표현 글자예요(병·정, 뱀·말)"), ("병·정", "흙이 표현 글자예요(무·기, 용·개·소·양)"),
                                                  ("무·기", "쇠가 표현 글자예요(경·신, 원숭이·닭)"), ("경·신", "물이 표현 글자예요(임·계, 돼지·쥐)"),
                                                  ("임·계", "나무가 표현 글자예요(갑·을, 호랑이·토끼)")], note="내 일간이 키워 주는 오행 = 식신·상관")
    if not _have(nm["B"]):
        DGC.vbar(nm["B"], c, "5분 대화 뒤, 상대의 호감", [("실제 호감", 5.82, True), ("내가 짐작한 호감", 5.17, False)], 7,
                 "사람들은 상대가 나를 좋아한 만큼을 늘 낮춰 짐작했어요", "Boothby 외 (2018), Psychological Science · 7점 척도, 연구 1a")
    if not _have(nm["C"]):
        DGB.chat(nm["C"], c, "행동에 한 줄만 붙여 보기", [("me", "커피 사 왔어"), ("me", "네가 좋아할 것 같아서 샀어"), ("you", "헐 고마워, 기억하고 있었네")],
                 note="첫 줄은 행동, 둘째 줄이 마음이에요")
    import fullbleed as FBL
    plan_p = os.path.join(HERE, "fullbleed_plan.json"); plan = json.load(open(plan_p, encoding="utf-8")) if os.path.exists(plan_p) else {}
    rows = []
    for pos, k in enumerate("LBC", 1):
        f = nm[k][:-4] + "f.jpg"
        if not _have(f):
            r, why = FBL.convert(nm[k], [os.path.join(HERE, "img"), os.path.join(HERE, "img", "m1280")])
            if not r: print("fullbleed 건너뜀", nm[k], why); made.append(nm[k]); continue
        rows.append({"pos": pos, "old": nm[k], "new": f}); made.append(nm[k]); nm[k] = f
        reg_ = json.load(open(DG.REG, encoding="utf-8")); reg_[f] = reg_[rows[-1]["old"]]; json.dump(dict(sorted(reg_.items())), open(DG.REG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    plan[PID] = rows; json.dump(plan, open(plan_p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    made += [v for v in nm.values() if v not in made]
    alt = {"L": "일간별 표현 글자 그림. 갑·을은 불, 병·정은 흙, 무·기는 쇠, 경·신은 물, 임·계는 나무가 표현 글자예요",
           "B": "5분 대화 실험 막대 그림. 상대가 실제로 나를 좋아한 점수 5.82, 내가 짐작한 점수 5.17(7점 만점)",
           "C": "말풍선 그림. 커피 사 왔어 다음에 네가 좋아할 것 같아서 샀어를 붙이니 상대가 고마워라고 답해요"}
    body = P(*head) + P("<b>📌 짝사랑 티가 안 나는 마음을 읽는 순서</b>", *[f"{i + 1}. {q}" for i, q in enumerate(toc_q)])
    for i, (q, s) in enumerate(zip(toc_q, secs)):
        for k in "LBC": s = s.replace(f"[[{k}]]", IMG(nm[k], alt[k]))
        body += H(f"{i + 1}. {q}") + s
    body += tail + CTA
    import copy_rules as CR
    for w in ("재미로", "상담", "—", "안녕하세요, 자오선의 정월이에요", "결론부터", "핵심부터", "생년월일만 넣으면 1초", "한 줄 요약", "이 글의 순서", "수비학",
              "공통점", "몇 개나", "겹칠까", "세 풀이", "여섯 운명학", "시라노", "로스탕", "투명성 착각", "길로비치", "염소자리", "물병자리", "무토", "계수", "무심한 척",
              "총정리", "솜씨", "값을 매", "내게") + tuple(CR.금지어):
        assert w not in re.sub(r"<[^>]+>", " ", body), w
    for f in made:   # 사이트 사본(K-069)
        dst = os.path.join(SITE, "public", "naver", "img", f); os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy(os.path.join(HERE, "img", f), dst)
    return body, a4, made

TITLE = "짝사랑 티가 안 나는 이유, 5분 대화 실험과 사주 표현 글자"
TAGS = ["짝사랑", "좋아하는티", "호감표현", "호감신호", "호감", "식상", "식신", "연애심리", "호감격차", "자오선"]
REL = {"id": "n91", "title": "첫눈에 반하는 이유, 끌림이 빠른 사주와 느린 사주 신호 4가지",
       "phrase": "첫눈에 끌리는 사주와 천천히 끌리는 사주를 더 보고 싶다면, 첫눈에 반하는 이유, 끌림이 빠른 사주와 느린 사주 신호 4가지",
       "url": "https://blog.naver.com/zaoseon/224480158127"}
KW_VOL = (json.load(open(os.path.join(SITE, "data", "keywords", "kw_volume.json"), encoding="utf-8"))["posts"].get(PID) or {}).get("씨앗") or {}
INTENT = {"keywords": ["짝사랑", "식신", "호감"],
          "keyword_src": "n26 재발행 일정 '새 글로 다시 쓰기'(진행표 11/18 아홉째 줄) · 월 검색량 kw-volume n102 11/20(첫 묶음 좋아하는사람앞에서·무심한척·호감표현·좋아하는티·호감신호 모두 100 아래 → 짝사랑 5,370·식신 3,760·호감 2,550 으로 바꿈)",
          "intent": "이유를 알고 싶다", "intent_note": "좋아하는데 왜 티가 안 나는지, 상대가 정말 모르는지, 어떻게 표현을 늘리는지",
          "first3": "짝사랑하는 마음이 티가 안 나는 건 마음을 겉으로 꺼내는 길이 좁아서예요. 사주에서는 이 길을 맡는 글자를 식상이라고 불러요. 5분 대화 실험에서 상대의 실제 호감은 5.82, 내가 짐작한 호감은 5.17이었어요.",
          "answer_keys": ["표현 글자 = 식상(식신·상관)", "일간별 식상 오행", "호감 격차: 상대 호감을 낮춰 짐작", "2027 丁 = 나무 일간 표현의 해"],
          "community_q": [], "order": toc_q, "images": ["일간별 표현 글자(ladder)", "5분 대화 호감 격차(vbar)", "행동에 한 줄 붙이기(chat)"],
          "related": "n91", "cta": PID, "experience": [], "applied": True,
          "differs_from_n26": "제목(좋아해도 티가 안 나는 사람의 공통점 → 짝사랑 티가 안 나는 이유·5분 대화 실험)·도입(정의 직답)·소제목 순서·세 풀이(戊·癸·염소/물병·수비학 4·7)·'몇 개나 겹칠까'·시라노·투명성 착각(Gilovich 1998) 대신 식상 표·예시 1993.12.10 오전 8시(癸酉·甲子·乙丑·庚辰, 불 지장간까지 없음, 엔진 assert)·호감 격차(Boothby 외 2018)·2027 丁 = 乙 식신·甲 상관·巳午 달(절기 assert)·그림 유형(ladder·vbar·chat)·연결글(→ n91)"}

if __name__ == "__main__":
    body, a4, made = build()
    reg = json.load(open(MP.REG, encoding="utf-8"))
    assert PID not in reg or not reg[PID].get("done"), "이미 예약 끝난 글"
    reg[PID] = dict(dt="2027-02-10T18:00:00", dt_tbd="CT가 정함(재발행 일정 'n26 다시 쓰기' 자리, 진행표 11/18). 이 날짜는 자리값", title=TITLE, tags=TAGS, body=body,
                    cover=a4, related=REL, thumbs=None, cid=None, clips=None, category="관계 읽기", done=False, kw_vol=KW_VOL,
                    k131="n102 11/20(K-151 새 글)", source="build_naver_102.py (n26 주제 새 글, n26 그대로)")
    json.dump(reg, open(MP.REG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    ic = json.load(open(os.path.join(HERE, "intent_cards.json"), encoding="utf-8")); ic["cards"][PID] = INTENT
    json.dump(ic, open(os.path.join(HERE, "intent_cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    v = reg[PID]
    MP.write_page(PID, D.datetime.fromisoformat(v["dt"]), v["title"], v["tags"], v["body"], None, v["cover"], v["related"], v["category"])
    MP.write_index()
    import k151_check as K
    print(PID, len(TITLE), "자 제목 · 본문 글자", len(re.sub(r"<[^>]+>|&nbsp;", "", body)), "· 사진", made, "· K 검사", K.check(PID, v))
