"""네이버 n99: 사주로 보는 연애 스타일 새 글 (CT 11/4 19:40 재발행 일정 '새 글로 다시 쓰기' n07 → n99, 진행표 docs/네이버_누락글_진행표_2026-11-18.md 여섯째 줄).
- 왜: 노출이 '다른 글'인 옛 글 n07(태어난 날로 보는 연애 스타일 10가지)을 새 글로. n07은 건드리지 않는다(K-147·K-178).
- 검색어: n99 묶음(연애스타일·사주연애스타일·일간연애·연애성향·일간별성격) 11/19 19:45 ① 요청 — 결과가 오면 KW_VOL 이 채워진다.
- 다르게 쓴 것(K-151): n07의 인사·한 줄 요약·일간 열 칸 나열(갑목 지켜 주는 연애…)·별자리 원소 비교·오행 상생 궁합 다섯 줄·여섯 운명학·애착 유형 대신
  심리학 연애 스타일 여섯 가지(Lee → Hendrick & Hendrick 1986, 42문항·807명·567명), 일간 오행 다섯 갈래 × 음양(먼저 다가가는 쪽/맞춰 가는 쪽),
  2027 丁未의 丁이 일간별로 무슨 십성인지(엔진 ten_god assert), 예시 1995년 6월 12일 오후 3시생(乙亥·壬午·甲戌·壬申, 일간 甲, engine assert).
  애착 유형은 n39가 이미 다뤄서 쓰지 않았다. 그림 유형 bignum·ladder·checklist. 연결글 → n58(십성 뜻, 노출 '예').
- 출처(K-162, 11/19 원문 확인): Hendrick & Hendrick (1986) JPSP 50(2) 392–402, DOI 10.1037/0022-3514.50.2.392 (초록: Lee의 여섯 연애 스타일, 문항 42개(스타일마다 7개),
  1차 807명 요인분석에서 여섯 척도가 뚜렷이 나옴, 2차 567명에서 다시 확인). 성별 차이 방향은 초록에서 확인 못 해서 쓰지 않았다.
- 날짜: CT가 정한다. pages.json dt 는 자리값, dt_tbd 로 표시.
사용: SITE=<zaoseon-site> python3 naver/build_naver_99.py"""
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
       '<tr><td style="padding:12px 10px;text-align:center;border:1px solid #d0d0d0"><b>내 일간이 다섯 갈래 중 어디인지 궁금하다면</b></td></tr>'
       '<tr><td style="padding:12px 10px;text-align:center;border:1px solid #d0d0d0"><span style="color:#9a9a9a">[ 1995 . 06 . 12 ]</span></td></tr>'
       '<tr><td style="padding:12px 10px;text-align:center;border:1px solid #d0d0d0"><b><a href="https://zaoseon.com/?utm_source=naver&amp;utm_medium=mid#free">내 태어난 날 글자 보기 →</a></b></td></tr>'
       '</tbody></table>' + BL)
CTA = ('<p><a href="https://zaoseon.com/?utm_source=naver&utm_medium=cta#free"><img src="' + RAW +
       'naver_cta5_1%EC%B4%88%EB%AC%B4%EB%A3%8C%ED%92%80%EC%9D%B4.jpg" alt="자오선 무료 1초 풀이 안내 배너"></a></p>')
PID, KEY, PAL = "n99", "99", "m_soft_s"   # 연애 = 불 판 묶음(EL_SET 불). n98 k_white_s · n97 m_young_s · n96 y_pink_s · n91 p_red_s 와 다른 판

# ───────── 계산값과 검산
import datetime as D
sys.path.insert(0, os.path.join(SITE, "engine"))
import engine as E
X = D.datetime(1995, 6, 12, 15, 0)
PX = E.compute_saju(X)["팔자"]
assert PX == {"년주": "乙亥", "월주": "壬午", "일주": "甲戌", "시주": "壬申"}, PX
assert E.compute_saju(D.datetime(1995, 6, 12, 16, 20))["팔자"] == PX           # 같은 申시 안
assert E.compute_saju(D.datetime(2027, 3, 1, 12))["팔자"]["년주"] == "丁未"
TG = {g: E.ten_god(g, "丁") for g in "甲乙丙丁戊己庚辛壬癸"}
assert TG == {"甲": "상관", "乙": "식신", "丙": "겁재", "丁": "비견", "戊": "정인", "己": "편인", "庚": "정관", "辛": "편관", "壬": "정재", "癸": "편재"}, TG
print("예시 팔자·일간 甲·2027 丁未·일간별 丁 십성 확인")

# ───────── 본문 (n07 문장을 옮기지 않았다)
head = ["<b>연애 스타일은 마음을 주는 방식과 다가가는 방향이에요. 사주에서는 태어난 날 위 글자(일간)의 오행으로 방식을, 음양으로 먼저 다가가는지 맞춰 가는지를 읽어요.</b>",
        "그래서 갈래는 열 개처럼 보여도 실제로는 다섯 오행에 두 방향이 붙은 구조예요.",
        "<b>심리학도 연애 스타일을 한 칸으로 나누지 않아요. 여섯 가지 점수를 함께 재고, 그 조합으로 사람을 읽어요.</b>",
        "이 글은 연애 스타일 여섯 가지 연구, 일간 다섯 갈래 읽는 법, 예시 한 명, 2027년에 일간마다 달라지는 연애 흐름까지 다뤄요."]
toc_q = ["심리학에서는 연애 스타일을 어떻게 나눌까요?", "사주로 연애 스타일은 어떻게 볼까요?", "다섯 갈래는 각각 어떻게 다를까요?",
         "1995년 6월 12일 오후 3시생은 어떻게 읽을까요?", "2027년에는 일간마다 연애가 어떻게 달라질까요?", "자주 묻는 질문"]
sec1 = P("🧠 <b>심리학에서는 연애 스타일을 여섯 가지로 나눠 재요.</b>",
         "캐나다 사회학자 존 리가 사랑하는 방식을 여섯 가지로 나눴고, 미국 심리학자 클라이드 헨드릭과 수전 헨드릭이 1986년 이것을 42문항 척도로 만들었어요.",
         "807명에게 물어 여섯 가지가 뚜렷하게 갈리는 것을 확인했고, 567명에게 다시 물어 같은 결과를 얻었어요.") + "[[B]]" + \
       P("눈여겨볼 점은 사람마다 여섯 점수를 모두 가진다는 거예요. 한 사람 안에 설레는 마음도, 친구 같은 마음도 다른 크기로 함께 있어요. 그래서 '나는 이 유형'으로 끝내기보다 어느 쪽이 큰지를 보는 게 더 맞아요.",
         '📚 <b>출처 1</b>: <a href="https://doi.org/10.1037/0022-3514.50.2.392">Hendrick &amp; Hendrick (1986), A theory and method of love, Journal of Personality and Social Psychology 50(2)</a>')
sec2 = P("<b>사주에서는 일간 하나에 두 가지를 읽어요. 오행과 음양이에요.</b>",
         "일간은 태어난 날의 위 글자예요. 열 글자가 날마다 차례로 돌아서, 같은 해에 태어나도 일간은 사람마다 달라요.",
         "🔹 <b>오행</b>(나무·불·흙·쇠·물)은 마음을 주는 방식이에요. 키워 주는지, 드러내는지, 지켜 주는지 같은 거예요.",
         "🔹 <b>음양</b>은 움직이는 방향이에요. 양 일간(甲·丙·戊·庚·壬)은 먼저 다가가는 쪽, 음 일간(乙·丁·己·辛·癸)은 상대에 맞춰 천천히 가는 쪽으로 봐요.") + \
       P("그러니까 연애 스타일은 '다섯 갈래 중 어디 + 먼저 가는지 맞춰 가는지' 두 칸으로 읽으면 돼요. 일간을 모르면 아래 칸에 생년월일을 넣어 바로 볼 수 있어요.") + MID
sec3 = P("<b>다섯 갈래를 마음 주는 방식으로 나누면 이래요.</b>") + "[[K]]" + \
       P("🌳 <b>나무(甲·乙)</b>: 상대가 자라는 걸 보며 기뻐해요. 응원하고 키워 주는 연애예요.",
         "🔥 <b>불(丙·丁)</b>: 좋으면 드러내요. 표현과 분위기로 마음을 전하는 연애예요.",
         "⛰️ <b>흙(戊·己)</b>: 곁을 지켜요. 말보다 늘 그 자리에 있어 주는 것으로 마음을 보여 줘요.",
         "⚔️ <b>쇠(庚·辛)</b>: 분명한 게 좋아요. 약속과 기준을 지키는 것이 곧 마음이에요.",
         "🌊 <b>물(壬·癸)</b>: 스며들어요. 상대의 기분을 먼저 읽고 맞춰 흐르는 연애예요.") + \
       P("같은 나무라도 甲(양)은 먼저 손을 내밀며 키워 주고, 乙(음)은 상대 곁에서 맞춰 자라며 키워 줘요. 방향만 다르고 마음을 주는 방식은 같아요.")
sec4 = P("🔎 <b>1995년 6월 12일 오후 3시에 태어난 사람을 예로 들어 볼게요.</b>",
         "여덟 글자는 乙亥·壬午·甲戌·壬申이에요. 일간은 甲, 곧게 자라는 큰 나무이고 양이에요.",
         "그래서 이 사람은 먼저 다가가서 상대를 키워 주는 연애로 봐요. 상대가 하고 싶은 일을 먼저 묻고, 그 일이 잘되도록 돕는 데서 마음을 느끼는 사람이에요.") + \
       P("주변 글자도 같이 보면 더 또렷해져요. 여덟 글자에 물(壬 둘·亥)이 셋이에요. 물은 나무를 키우는 기운이라, 이 사람은 받는 마음에도 익숙한 편으로 봐요.",
         "주는 연애와 받는 연애가 둘 다 있는 사람이라, 한쪽만 하다 지칠 때 '나도 이게 필요해'라고 한 번 말해 보세요.",
         '📚 <b>출처 2</b>: <a href="https://astro.kasi.re.kr/life/pageView/5">한국천문연구원 천문우주지식정보, 음양력 변환(절기 시각)</a>')
sec5 = P("<b>2027년 정미년의 위 글자는 丁(촛불)이에요. 이 丁이 내 일간에게 무슨 역할인지에 따라 연애 흐름이 달라져요.</b>",
         "🌳 <b>나무 일간</b>: 丁은 나를 드러내는 글자(식신·상관)예요. 마음을 말과 행동으로 꺼내기 좋은 해예요.",
         "🔥 <b>불 일간</b>: 丁은 나와 같은 편(비견·겁재)이에요. 친구 같은 사이가 가까워지기 쉽고, 같은 사람을 두고 마음이 겹칠 수도 있어요.",
         "⛰️ <b>흙 일간</b>: 丁은 나를 돌봐 주는 글자(정인·편인)예요. 챙김을 받는 일이 늘어나는 해예요. 받는 걸 어색해하지 않는 연습이 필요해요.",
         "⚔️ <b>쇠 일간</b>: 丁은 나를 다듬는 글자(정관·편관)예요. 가볍게 만나기보다 약속과 책임이 붙는 관계로 기울기 쉬워요.",
         "🌊 <b>물 일간</b>: 丁은 내가 다루는 글자(정재·편재)예요. 새 사람을 만나는 일이 늘어나는 해로 봐요.") + \
       P("예시의 甲 일간에게 丁은 상관이에요. 원래 먼저 다가가는 사람이 2027년엔 표현까지 커지는 해라, 마음을 전할 때 상대의 속도를 한 번 살피면 좋아요.") + \
       P("🌱 <b>마음 코치 정월의 질문</b>", "연애에서 내가 가장 자주 하는<br>행동은 무엇인가요?",
         "🔸 그 행동은 키워 주기, 드러내기, 지켜 주기,<br>분명히 하기, 맞춰 주기 중 어디에 가까운가요?") + "[[C]]" + \
       P("✔️ <b>이번 주에 해 볼 것</b>",
         "1. 내 일간의 갈래와 방향을 한 줄로 적어 보세요. 예: '나무, 먼저 다가가는 쪽'.",
         "2. 상대에게 '나는 이럴 때 마음이 전해졌다고 느껴'라고 한 문장만 말해 보세요.",
         "3. 상대가 마음을 주는 방식 하나를 찾아 '고마워'라고 짚어 주세요. 방식이 달라도 마음은 같을 수 있어요.")
sec6 = P("<b>Q. 일간이 같으면 연애 스타일도 똑같나요?</b>",
         "A. 아니에요. 일간은 바탕이고, 나머지 일곱 글자와 지금 겪는 일이 함께 작용해요. 같은 일간끼리도 어느 쪽 점수가 큰지는 달라요.") + \
       P("<b>Q. 연인과 갈래가 다르면 안 맞는 건가요?</b>",
         "A. 다르다는 건 마음을 주는 방식이 다르다는 뜻이에요. 서로의 방식을 말로 알려 주면 오히려 서로 채워 주는 사이가 될 수 있어요.") + \
       P("<b>Q. 음 일간은 고백을 못 하나요?</b>",
         "A. 그렇지 않아요. 음 일간은 상대의 마음을 먼저 살핀 뒤에 움직이는 쪽이라, 다가가는 때가 조금 늦을 뿐이에요. 타이밍을 잡으면 오히려 더 단단하게 다가가요.")
tail = P("여러분의 일간은 다섯 갈래 중 어디인가요?", "무료 풀이에서 확인하고 갈래 이름 하나만 댓글에 적어 주세요.") + \
       '<p><b>👇 2027년 丁이 내 일간에게 무슨 이름인지 십성 열 가지로 더 보고 싶다면, 십성 뜻 한눈에, 10가지 이름과 내 일간으로 찾는 표</b></p>'
secs = [sec1, sec2, sec3, sec4, sec5, sec6]

def _have(n): return os.path.exists(os.path.join(HERE, "img", n))
def build():
    for d_ in ("wide", "m1280", "master"): os.makedirs(os.path.join(HERE, "img", d_), exist_ok=True)
    c = V.Ctx(PAL); made = []
    a4 = f"wide/naver_z{KEY}_a5.jpg"   # 표지 항목은 한글만(한자는 글꼴에 없어 네모, 11/18 n96 a4)
    if not _have(a4):
        V.render(PID + "_new", {"d": "N", "el": "불", "kick": "사주로 보는 연애 스타일", "hook": ["다섯 갈래와", "두 방향"], "sub": "일간 오행과 음양으로 읽어요",
                                "items": ["먼저 가요", "맞춰 가요", "2027"]}, os.path.join(HERE, "img", a4), PAL)
    made.append(a4)
    nm = {"B": f"naver_z{KEY}_b5.jpg", "K": f"naver_z{KEY}_l3.jpg", "C": f"naver_z{KEY}_h3.jpg"}
    if not _have(nm["B"]):
        DGC.bignum(nm["B"], c, "연애 스타일 여섯 가지", "6", "한 사람이 여섯 점수를 모두 가져요",
                   [("설렘", "첫눈에 끌리는 사랑"), ("놀이", "가볍게 즐기는 사랑"), ("우정", "친구처럼 쌓이는 사랑"),
                    ("조건", "따져 보고 고르는 사랑"), ("몰두", "불안하게 매달리는 사랑"), ("헌신", "주는 것이 기쁜 사랑")],
                   "Hendrick & Hendrick (1986), 42문항 · 807명과 567명")
    if not _have(nm["K"]):
        DGB.ladder(nm["K"], c, "일간 다섯 갈래, 마음 주는 방식", [("나무", "키워 주는 연애"), ("불", "드러내는 연애"), ("흙", "지켜 주는 연애"),
                                                         ("쇠", "분명히 하는 연애"), ("물", "맞춰 흐르는 연애")],
                   "양 일간은 먼저 다가가고, 음 일간은 맞춰 가요")
    if not _have(nm["C"]):
        DGB.checklist(nm["C"], c, "이번 주 세 칸", [("내 갈래 한 줄", "예: 나무, 먼저 가는 쪽"), ("한 문장 말하기", "이럴 때 마음이 전해져"),
                                               ("상대 방식 짚기", "방식이 달라도 고마워")])
    import fullbleed as FBL
    plan_p = os.path.join(HERE, "fullbleed_plan.json"); plan = json.load(open(plan_p, encoding="utf-8")) if os.path.exists(plan_p) else {}
    rows = []
    for pos, k in enumerate("BKC", 1):
        f = nm[k][:-4] + "f.jpg"
        if not _have(f):
            r, why = FBL.convert(nm[k], [os.path.join(HERE, "img"), os.path.join(HERE, "img", "m1280")])
            if not r: print("fullbleed 건너뜀", nm[k], why); made.append(nm[k]); continue
        rows.append({"pos": pos, "old": nm[k], "new": f}); made.append(nm[k]); nm[k] = f
        reg_ = json.load(open(DG.REG, encoding="utf-8")); reg_[f] = reg_[rows[-1]["old"]]; json.dump(dict(sorted(reg_.items())), open(DG.REG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    plan[PID] = rows; json.dump(plan, open(plan_p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    made += [v for v in nm.values() if v not in made]
    alt = {"B": "연애 스타일 여섯 가지 그림. 설렘, 놀이, 우정, 조건, 몰두, 헌신, 한 사람이 여섯 점수를 모두 가져요",
           "K": "일간 다섯 갈래 그림. 나무는 키워 주는 연애, 불은 드러내는 연애, 흙은 지켜 주는 연애, 쇠는 분명히 하는 연애, 물은 맞춰 흐르는 연애",
           "C": "이번 주 세 칸 체크 그림. 내 갈래 한 줄, 한 문장 말하기, 상대 방식 짚기"}
    body = P(*head) + P("<b>📌 내 연애 스타일을 읽는 순서</b>", *[f"{i + 1}. {q}" for i, q in enumerate(toc_q)])
    for i, (q, s) in enumerate(zip(toc_q, secs)):
        for k in "BKC": s = s.replace(f"[[{k}]]", IMG(nm[k], alt[k]))
        body += H(f"{i + 1}. {q}") + s
    body += tail + CTA
    import copy_rules as CR
    for w in ("재미로", "상담", "—", "안녕하세요, 자오선의 정월이에요", "결론부터 말씀드릴게요", "한 줄로 먼저", "생년월일만 넣으면 1초", "한 줄 요약", "이 글의 순서", "수비학",
              "공통점", "몇 개나 겹칠까", "여섯 운명학", "애착", "별자리", "지켜 주는 연애예요. 표현은", "총정리", "솜씨", "값을 매", "내게", "궁합") + tuple(CR.금지어):
        assert w not in re.sub(r"<[^>]+>", " ", body), w
    for f in made:   # 사이트 사본(K-069)
        dst = os.path.join(SITE, "public", "naver", "img", f); os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy(os.path.join(HERE, "img", f), dst)
    return body, a4, made

TITLE = "연애 스타일 사주로 보는 법, 일간 다섯 갈래와 2027년 흐름"
TAGS = ["연애스타일", "사주연애스타일", "일간연애", "연애성향", "일간별성격", "일간", "2027연애운", "사주보는법", "관계심리", "자오선"]
REL = {"id": "n58", "title": "십성 뜻 한눈에, 10가지 이름과 내 일간으로 찾는 표",
       "phrase": "2027년 丁이 내 일간에게 무슨 이름인지 십성 열 가지로 더 보고 싶다면, 십성 뜻 한눈에, 10가지 이름과 내 일간으로 찾는 표",
       "url": "https://blog.naver.com/zaoseon/224468727235"}
KW_VOL = (json.load(open(os.path.join(SITE, "data", "keywords", "kw_volume.json"), encoding="utf-8"))["posts"].get(PID) or {}).get("씨앗") or {}
INTENT = {"keywords": ["연애스타일", "사주연애스타일", "일간연애"],
          "keyword_src": "n07 재발행 일정 '새 글로 다시 쓰기'(진행표 11/18 여섯째 줄) · 월 검색량은 kw-volume n99 요청(11/19 19:45)",
          "intent": "방법을 알고 싶다", "intent_note": "사주로 내 연애 스타일을 어떻게 읽는지, 열 가지 나열 말고 읽는 틀(오행·음양)과 예시 한 명, 2027년 흐름까지",
          "first3": "연애 스타일은 마음을 주는 방식과 다가가는 방향이에요. 사주에서는 일간의 오행으로 방식을, 음양으로 먼저 다가가는지 맞춰 가는지를 읽어요. 갈래는 다섯 오행에 두 방향이에요. 심리학도 여섯 점수의 조합으로 연애 스타일을 읽어요.",
          "answer_keys": ["일간 오행 = 마음 주는 방식", "음양 = 먼저 다가감/맞춰 감", "심리학 연애 스타일 6가지, 한 사람이 모두 가짐"],
          "community_q": [], "order": toc_q, "images": ["연애 스타일 여섯 가지(bignum)", "일간 다섯 갈래(ladder)", "이번 주 세 칸(checklist)"],
          "related": "n58", "cta": PID, "experience": [], "applied": True,
          "differs_from_n07": "제목(연애 스타일 10가지 → 사주로 보는 법·다섯 갈래·2027)·도입(정의 직답)·소제목 순서·일간 열 칸 나열·별자리 원소·오행 상생 궁합·여섯 운명학·애착 유형 대신 연애 스타일 여섯 가지 연구(Hendrick 1986)·오행 × 음양 두 칸 읽기·예시 1995.6.12 오후 3시(乙亥·壬午·甲戌·壬申, 엔진 assert)·2027 丁의 일간별 십성(엔진 assert)·그림 유형(bignum·ladder·checklist)·연결글(→ n58)"}

if __name__ == "__main__":
    body, a4, made = build()
    reg = json.load(open(MP.REG, encoding="utf-8"))
    assert PID not in reg or not reg[PID].get("done"), "이미 예약 끝난 글"
    reg[PID] = dict(dt="2027-02-08T08:00:00", dt_tbd="CT가 정함(재발행 일정 'n07 다시 쓰기' 자리, 진행표 11/18). 이 날짜는 자리값", title=TITLE, tags=TAGS, body=body,
                    cover=a4, related=REL, thumbs=None, cid=None, clips=None, category="관계 읽기", done=False, kw_vol=KW_VOL,
                    k131="n99 11/19(K-151 새 글)", source="build_naver_99.py (n07 주제 새 글, n07 그대로)")
    json.dump(reg, open(MP.REG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    ic = json.load(open(os.path.join(HERE, "intent_cards.json"), encoding="utf-8")); ic["cards"][PID] = INTENT
    json.dump(ic, open(os.path.join(HERE, "intent_cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    v = reg[PID]
    MP.write_page(PID, D.datetime.fromisoformat(v["dt"]), v["title"], v["tags"], v["body"], None, v["cover"], v["related"], v["category"])
    MP.write_index()
    import k151_check as K
    print(PID, len(TITLE), "자 제목 · 본문 글자", len(re.sub(r"<[^>]+>|&nbsp;", "", body)), "· 사진", made, "· K 검사", K.check(PID, v))
