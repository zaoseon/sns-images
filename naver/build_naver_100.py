"""네이버 n100: 역마살 뜻·혼자 여행 새 글 (CT 11/4 19:40 재발행 일정 '새 글로 다시 쓰기' n21 → n100, 진행표 docs/네이버_누락글_진행표_2026-11-18.md 일곱째 줄).
- 왜: 노출 안 되는 옛 글 n21(혼자 여행을 좋아하는 사람의 공통점, 역마 사주와 별자리·숫자)을 새 글로. n21은 건드리지 않는다(K-147·K-178).
- 검색어: n100 묶음(혼자여행·역마살·혼자여행좋아하는사람·역마살뜻·혼행) 11/19 19:45 ① 요청 — 결과가 오면 KW_VOL 이 채워진다.
- 다르게 쓴 것(K-151): n21의 첫 질문·'핵심부터'·한 줄 요약·세 풀이(壬일간·사수/물병자리·수비학 5·7)·'몇 개나 겹칠까'·드 메스트르·여섯 운명학·심리적 분리(Sonnentag & Fritz 2007) 대신
  역마살 뜻 정의 직답, 띠·일지 두 기준, 예시 1994년 9월 3일 오후 2시생(甲戌·壬申·壬辰·丁未, 개띠 → 역마 申이 월지에 있음, engine assert),
  2027년 띠 묶음별 역마 달 네 칸(寅·巳·申·亥 달의 절기 날짜 engine assert), 2027 해 지지 未(亥卯未 → 역마 巳),
  심리 = 혼자 있는 15분 실험(Nguyen, Ryan & Deci 2018, PSPB — 네 실험, 들뜬 기분은 좋든 나쁘든 가라앉고, 스스로 고른 혼자일 때 차분함이 늘고 외로움은 덜 늘었다).
  그림 유형 exp·quad·checklist. 연결글 → n79(도화살 뜻, 노출 '예').
- 출처 2개(K-162, 11/19 원문 확인): Nguyen, Ryan & Deci, Solitude as an approach to affective self-regulation, PSPB, DOI 10.1177/0146167217733073 (selfdeterminationtheory.org PDF 본문: 실험 4개,
  1~3은 15분 혼자, 메타분석 들뜬 좋은 기분 r=−.33·들뜬 나쁜 기분 r=−.30·차분함 r=.20·외로움·슬픔 r=.14, 고르기·자율성이 외로움 증가를 줄임) · 한국천문연구원 음양력 변환(절기 시각).
- 날짜: CT가 정한다. pages.json dt 는 자리값, dt_tbd 로 표시.
사용: SITE=<zaoseon-site> python3 naver/build_naver_100.py"""
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
       '<tr><td style="padding:12px 10px;text-align:center;border:1px solid #d0d0d0"><b>내 여덟 글자에 역마 글자가 있는지 궁금하다면</b></td></tr>'
       '<tr><td style="padding:12px 10px;text-align:center;border:1px solid #d0d0d0"><span style="color:#9a9a9a">[ 1994 . 09 . 03 ]</span></td></tr>'
       '<tr><td style="padding:12px 10px;text-align:center;border:1px solid #d0d0d0"><b><a href="https://zaoseon.com/?utm_source=naver&amp;utm_medium=mid#free">내 태어난 날 글자 보기 →</a></b></td></tr>'
       '</tbody></table>' + BL)
CTA = ('<p><a href="https://zaoseon.com/?utm_source=naver&utm_medium=cta#free"><img src="' + RAW +
       'naver_cta5_1%EC%B4%88%EB%AC%B4%EB%A3%8C%ED%92%80%EC%9D%B4.jpg" alt="자오선 무료 1초 풀이 안내 배너"></a></p>')
PID, KEY, PAL = "n100", "100", "dg_gold_s"   # 역마 申 = 쇠 판 묶음(EL_SET 쇠). n99 m_soft_s · n98 k_white_s · n97 m_young_s · n96 y_pink_s 와 다른 판

# ───────── 계산값과 검산
import datetime as D
sys.path.insert(0, os.path.join(SITE, "engine"))
import engine as E
YM = {"申子辰": "寅", "寅午戌": "申", "巳酉丑": "亥", "亥卯未": "巳"}   # 역마: 삼합 첫 글자와 충하는 자리(통용 기준)
def yeokma(zhi): return next(v for k, v in YM.items() if zhi in k)
X = D.datetime(1994, 9, 3, 14, 0)
PX = E.compute_saju(X)["팔자"]
assert PX == {"년주": "甲戌", "월주": "壬申", "일주": "壬辰", "시주": "丁未"}, PX
assert E.compute_saju(D.datetime(1994, 9, 3, 14, 50))["팔자"] == PX           # 같은 未시 안
assert yeokma(PX["년주"][1]) == "申" and "申" in PX["월주"]                      # 개띠 → 申, 월지에 있음
assert yeokma(PX["일주"][1]) == "寅" and not any("寅" in p for p in PX.values())  # 일지 辰 → 寅, 없음
assert yeokma("未") == "巳"                                                       # 2027 해 지지 未 → 巳
T = dict((n, t) for n, _, t in E.get_solar_terms_kst(2027))
MON = {"寅": ("입춘", "경칩"), "巳": ("입하", "망종"), "申": ("입추", "백로"), "亥": ("입동", "대설")}
SPAN = {}
for z, (a, b) in MON.items():
    s_, e_ = T[a], T[b]; mid = s_ + (e_ - s_) / 2
    assert E.compute_saju(mid.replace(tzinfo=None))["팔자"]["월주"][1] == z, z
    SPAN[z] = (s_.month, s_.day, (e_ - D.timedelta(days=1)).month, (e_ - D.timedelta(days=1)).day)
assert SPAN == {"寅": (2, 4, 3, 5), "巳": (5, 6, 6, 5), "申": (8, 8, 9, 7), "亥": (11, 8, 12, 6)}, SPAN
assert E.compute_saju(D.datetime(2027, 3, 1, 12))["팔자"]["년주"] == "丁未"
print("예시 팔자·역마 申(년지 기준)·寅 없음·2027 역마 달 네 칸·해 지지 未 → 巳 확인")
def sp(z): a, b, c_, d_ = SPAN[z]; return f"{a}월 {b}일~{c_}월 {d_}일"

# ───────── 본문 (n21 문장을 옮기지 않았다)
head = ["<b>역마살은 사주에서 이동과 바뀜을 부르는 글자예요. 띠(또는 태어난 날 아래 글자)로 정해지는 寅·申·巳·亥 넷 가운데 하나가 여덟 글자에 있으면 역마가 있다고 봐요.</b>",
        "옛날 역참의 말처럼 늘 오가는 기운이라, 혼자 떠나는 여행이나 출장, 이사가 잦은 사람에게서 자주 보여요.",
        "<b>심리학 실험에서는 혼자 15분만 있어도 들뜬 기분이 가라앉았고, 스스로 고른 혼자일 때 더 차분해졌어요.</b>",
        "이 글은 역마살 찾는 법, 예시 한 명, 혼자 있는 시간 실험, 2027년 띠별로 역마가 들어오는 달까지 다뤄요."]
toc_q = ["역마살은 어떻게 찾을까요?", "1994년 9월 3일 오후 2시생은 어떻게 읽을까요?", "혼자 있으면 마음은 어떻게 달라질까요?",
         "2027년 역마가 들어오는 달은 언제일까요?", "혼자 떠나기 전에 무엇을 챙길까요?", "자주 묻는 질문"]
sec1 = P("<b>역마는 내 띠가 속한 묶음으로 찾아요. 묶음마다 역마 글자가 하나씩 정해져 있어요.</b>",
         "🔹 원숭이·쥐·용띠(申子辰) → 호랑이 글자 寅",
         "🔹 호랑이·말·개띠(寅午戌) → 원숭이 글자 申",
         "🔹 뱀·닭·소띠(巳酉丑) → 돼지 글자 亥",
         "🔹 돼지·토끼·양띠(亥卯未) → 뱀 글자 巳") + \
       P("띠 대신 태어난 날 아래 글자(일지)로 같은 표를 한 번 더 보기도 해요. 띠 기준은 바깥으로 드러나는 이동, 일지 기준은 내 생활 속 움직임으로 봐요.",
         "찾은 글자가 여덟 글자 가운데 아래 글자 넷(년·월·일·시) 중 하나에 있으면 역마가 있다고 봐요. 살이라는 이름이 붙었지만 나쁜 뜻이 아니라, 머물기보다 움직일 때 힘이 나는 기운이에요.") + MID
sec2 = P("🔎 <b>1994년 9월 3일 오후 2시에 태어난 사람을 예로 들어 볼게요.</b>",
         "여덟 글자는 甲戌·壬申·壬辰·丁未예요. 개띠(戌)라서 역마 글자는 申이고, 태어난 달 아래 글자가 바로 申이에요. 띠 기준 역마가 있는 사주예요.",
         "태어난 날 아래 글자는 辰이라 일지 기준 역마는 寅인데, 여덟 글자에 寅은 없어요.") + \
       P("그래서 이 사람은 바깥 일로 오가는 이동은 많지만, 생활 자체를 자주 옮기는 쪽은 아니라고 읽어요. 출장이나 여행은 즐기되 돌아올 집은 단단히 두는 사람이에요.",
         "일간도 壬, 큰 강물이에요. 흐르는 물이 역마를 만나 '움직일 때 숨이 트이는' 기운이 더 또렷해져요.",
         '📚 <b>출처 2</b>: <a href="https://astro.kasi.re.kr/life/pageView/5">한국천문연구원 천문우주지식정보, 음양력 변환(절기 시각)</a>')
sec3 = P("🧠 <b>혼자 떠나고 싶은 마음은 심리학에서도 실험으로 다뤘어요.</b>",
         "심리학자 응우옌·라이언·데시는 대학생들을 15분 동안 아무것도 하지 않고 혼자 앉아 있게 했어요. 같은 방식의 실험을 네 번 했어요.",
         "혼자 있고 나면 신나는 기분도, 화나는 기분도 함께 가라앉았어요. 대신 차분하고 느긋한 기분은 조금 늘었어요.") + "[[B]]" + \
       P("눈여겨볼 점은 '고르느냐'예요. 스스로 고른 혼자일 때는 차분함이 더 늘고 외로움은 덜 늘었어요. 억지로 혼자가 된 사람은 오히려 외로움과 슬픔이 커졌어요.",
         "혼자 여행이 충전이 되는 건 떠나는 걸 내가 골랐을 때예요. 그러니 혼자 떠나고 싶은 마음이 들면, 피하는 게 아니라 고르는 거라고 나에게 먼저 말해 주세요.",
         '📚 <b>출처 1</b>: <a href="https://doi.org/10.1177/0146167217733073">Nguyen, Ryan &amp; Deci (2018), Solitude as an approach to affective self-regulation, Personality and Social Psychology Bulletin</a>')
sec4 = P("<b>2027년에는 띠 묶음마다 역마 글자의 달이 한 번씩 와요. 그달에는 떠날 일이 생기거나 떠나고 싶은 마음이 커지기 쉬워요.</b>") + "[[K]]" + \
       P(f"🔹 원숭이·쥐·용띠: 寅 달, {sp('寅')}",
         f"🔹 돼지·토끼·양띠: 巳 달, {sp('巳')}",
         f"🔹 호랑이·말·개띠: 申 달, {sp('申')}",
         f"🔹 뱀·닭·소띠: 亥 달, {sp('亥')}") + \
       P(f"2027년은 해 아래 글자가 未(양)예요. 未가 속한 돼지·토끼·양 묶음의 역마가 巳라서, 巳 달({sp('巳')})은 여러 사람에게 움직임이 많은 달로 봐요.",
         f"예시의 개띠는 申 달({sp('申')})에 역마 글자가 한 번 더 들어와요. 오래 미뤄 둔 혼자 여행을 이때 잡으면 좋은 사람이에요.")
sec5 = P("<b>역마가 있어도 떠나는 방식은 내가 정할 수 있어요.</b>") + \
       P("🌱 <b>마음 코치 정월의 질문</b>", "요즘 떠나고 싶은 마음은<br>무엇에서 멀어지고 싶어서인가요?",
         "🔸 혼자 가면 가장 먼저<br>하고 싶은 일은 무엇인가요?") + "[[C]]" + \
       P("✔️ <b>혼자 떠나기 전 세 가지</b>",
         "1. 떠나는 이유를 한 줄로 적어 보세요. 예: '조용히 걷고 싶어서'. 고른 혼자라는 걸 스스로 알면 더 쉬어져요.",
         "2. 가까운 사람에게 일정과 돌아오는 날을 미리 알려 두세요. 연락이 끊겨 서운해지는 일이 줄어들 거예요.",
         "3. 돌아온 날 저녁에 한 사람과 짧게 여행 이야기를 나눠 보세요. 혼자의 시간이 관계로 다시 이어져요.")
sec6 = P("<b>Q. 역마살이 있으면 한곳에 오래 못 사나요?</b>",
         "A. 아니에요. 움직일 때 힘이 나는 기운일 뿐, 꼭 이사를 자주 해야 한다는 뜻은 아니에요. 여행, 출장, 새 공부처럼 바깥으로 나가는 일로도 충분히 채워져요.") + \
       P("<b>Q. 역마가 없는데도 혼자 여행이 좋아요.</b>",
         "A. 그럴 수 있어요. 역마는 기질의 한 면이고, 혼자 있는 시간이 필요한 이유는 사람마다 달라요. 위 실험처럼 내가 골라서 혼자가 될 때 쉬어진다면 그걸로 충분해요.") + \
       P("<b>Q. 역마 달에는 꼭 떠나야 하나요?</b>",
         "A. 꼭 그렇지는 않아요. 그달에 떠날 일이 잡히기 쉽고 마음도 들뜨기 쉬워서, 미리 일정을 정해 두면 들뜬 마음을 쓸 곳이 생긴다는 정도로 읽어 주세요.")
tail = P("여러분의 띠는 2027년 몇 월에 역마가 들어오나요?", "위 표에서 찾아보고 그달에 가고 싶은 곳 하나만 댓글에 적어 주세요.") + \
       '<p><b>👇 역마와 함께 자주 묻는 도화살이 무엇이고 2027년 언제 피는지 보고 싶다면, 도화살 뜻과 2027년 도화 달, 도화가 있으면 인기가 많을까</b></p>'
secs = [sec1, sec2, sec3, sec4, sec5, sec6]

def _have(n): return os.path.exists(os.path.join(HERE, "img", n))
def build():
    for d_ in ("wide", "m1280", "master"): os.makedirs(os.path.join(HERE, "img", d_), exist_ok=True)
    c = V.Ctx(PAL); made = []
    a4 = f"wide/naver_z{KEY}_a5.jpg"   # 표지 항목은 한글만(한자는 글꼴에 없어 네모, 11/18 n96 a4)
    if not _have(a4):
        V.render(PID + "_new", {"d": "N", "el": "쇠", "kick": "역마살 뜻", "hook": ["혼자 떠나고 싶은", "사주가 있어요"], "sub": "2027년 띠별 역마 달까지 봐요",
                                "items": ["인", "신", "사·해"]}, os.path.join(HERE, "img", a4), PAL)
    made.append(a4)
    nm = {"B": f"naver_z{KEY}_e5.jpg", "K": f"naver_z{KEY}_q3.jpg", "C": f"naver_z{KEY}_h3.jpg"}
    if not _have(nm["B"]):
        DGC.exp(nm["B"], c, "혼자 15분, 기분은 어떻게", "응우옌·라이언·데시 · 2018",
                [("혼자 앉기", "15분 동안 아무것도 하지 않고 혼자 있었어요"), ("고른 혼자", "혼자 있기를 스스로 고르게 했어요")],
                "들뜬 기분은 좋든 나쁘든 가라앉았고, 스스로 고른 혼자일 때 차분함이 늘고 외로움은 덜 늘었어요",
                "Nguyen·Ryan·Deci (2018), Personality and Social Psychology Bulletin", tag="실험")
    if not _have(nm["K"]):
        DGC.quad(nm["K"], c, "2027년 띠별 역마 달", [(sp('寅'), "원숭이·쥐·용띠, 호랑이 달"), (sp('巳'), "돼지·토끼·양띠, 뱀 달"),
                                                (sp('申'), "호랑이·말·개띠, 원숭이 달"), (sp('亥'), "뱀·닭·소띠, 돼지 달")],
                 1, "절기 시각: 한국천문연구원", note="2027년 해 글자 양의 역마가 뱀이라 5~6월은 여럿이 움직여요")
    if not _have(nm["C"]):
        DGB.checklist(nm["C"], c, "혼자 떠나기 전 세 칸", [("떠나는 이유 한 줄", "고른 혼자라는 걸 알기"), ("일정과 돌아오는 날", "가까운 사람에게 미리"),
                                                     ("돌아온 날 저녁", "한 사람과 여행 이야기")])
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
    alt = {"B": "혼자 15분 실험 그림. 15분 혼자 있으면 들뜬 기분은 좋든 나쁘든 가라앉았고, 스스로 고른 혼자일 때 차분함이 늘고 외로움은 덜 늘었어요",
           "K": f"2027년 띠별 역마 달 그림. 원숭이·쥐·용띠 {sp('寅')}, 돼지·토끼·양띠 {sp('巳')}, 호랑이·말·개띠 {sp('申')}, 뱀·닭·소띠 {sp('亥')}",
           "C": "혼자 떠나기 전 세 칸 체크 그림. 떠나는 이유 한 줄, 일정과 돌아오는 날 알리기, 돌아온 날 저녁 여행 이야기"}
    body = P(*head) + P("<b>📌 역마와 혼자 여행을 읽는 순서</b>", *[f"{i + 1}. {q}" for i, q in enumerate(toc_q)])
    for i, (q, s) in enumerate(zip(toc_q, secs)):
        for k in "BKC": s = s.replace(f"[[{k}]]", IMG(nm[k], alt[k]))
        body += H(f"{i + 1}. {q}") + s
    body += tail + CTA
    import copy_rules as CR
    for w in ("재미로", "상담", "—", "안녕하세요, 자오선의 정월이에요", "결론부터 말씀드릴게요", "핵심부터", "한 줄로 먼저", "생년월일만 넣으면 1초", "한 줄 요약", "이 글의 순서", "수비학",
              "공통점", "몇 개나 겹칠까", "여섯 운명학", "메스트르", "심리적 분리", "사수자리", "물병자리", "총정리", "솜씨", "값을 매", "내게", "도망") + tuple(CR.금지어):
        assert w not in re.sub(r"<[^>]+>", " ", body), w
    for f in made:   # 사이트 사본(K-069)
        dst = os.path.join(SITE, "public", "naver", "img", f); os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy(os.path.join(HERE, "img", f), dst)
    return body, a4, made

TITLE = "역마살 뜻, 혼자 여행이 좋은 사주와 2027년 떠나기 좋은 달"
TAGS = ["역마살", "역마살뜻", "혼자여행", "혼자여행좋아하는사람", "혼행", "역마", "2027운세", "사주보는법", "혼자있는시간", "자오선"]
REL = {"id": "n79", "title": "도화살 뜻과 2027년 도화 달, 도화가 있으면 인기가 많을까",
       "phrase": "역마와 함께 자주 묻는 도화살이 무엇이고 2027년 언제 피는지 보고 싶다면, 도화살 뜻과 2027년 도화 달, 도화가 있으면 인기가 많을까",
       "url": "https://blog.naver.com/zaoseon/224467820880"}
KW_VOL = (json.load(open(os.path.join(SITE, "data", "keywords", "kw_volume.json"), encoding="utf-8"))["posts"].get(PID) or {}).get("씨앗") or {}
INTENT = {"keywords": ["역마살", "역마살뜻", "혼자여행"],
          "keyword_src": "n21 재발행 일정 '새 글로 다시 쓰기'(진행표 11/18 일곱째 줄) · 월 검색량은 kw-volume n100 요청(11/19 19:45)",
          "intent": "뜻을 알고 싶다", "intent_note": "역마살이 무엇이고 내 사주에 있는지 찾는 법, 혼자 떠나고 싶은 마음이 괜찮은지, 2027년 언제 움직이면 좋은지",
          "first3": "역마살은 사주에서 이동과 바뀜을 부르는 글자예요. 띠로 정해지는 寅·申·巳·亥 가운데 하나가 여덟 글자에 있으면 역마가 있다고 봐요. 혼자 15분만 있어도 들뜬 기분이 가라앉고, 스스로 고른 혼자일 때 더 차분해졌어요.",
          "answer_keys": ["역마 = 이동과 바뀜의 글자", "띠 묶음별 寅·申·巳·亥", "고른 혼자일 때 차분함 늘고 외로움 덜 늘어남", "2027 띠별 역마 달"],
          "community_q": [], "order": toc_q, "images": ["혼자 15분 실험(exp)", "2027 띠별 역마 달(quad)", "혼자 떠나기 전 세 칸(checklist)"],
          "related": "n79", "cta": PID, "experience": [], "applied": True,
          "differs_from_n21": "제목(공통점 → 역마살 뜻·2027 떠나기 좋은 달)·도입(정의 직답)·소제목 순서·세 풀이(壬·사수/물병·수비학 5·7)·'몇 개나 겹칠까'·드 메스트르·여섯 운명학·심리적 분리(Sonnentag 2007) 대신 띠·일지 두 기준·예시 1994.9.3 오후 2시(甲戌·壬申·壬辰·丁未, 엔진 assert)·혼자 15분 실험(Nguyen 외 2018)·2027 띠별 역마 달(절기 assert)·그림 유형(exp·quad·checklist)·연결글(→ n79)"}

if __name__ == "__main__":
    body, a4, made = build()
    reg = json.load(open(MP.REG, encoding="utf-8"))
    assert PID not in reg or not reg[PID].get("done"), "이미 예약 끝난 글"
    reg[PID] = dict(dt="2027-02-08T18:00:00", dt_tbd="CT가 정함(재발행 일정 'n21 다시 쓰기' 자리, 진행표 11/18). 이 날짜는 자리값", title=TITLE, tags=TAGS, body=body,
                    cover=a4, related=REL, thumbs=None, cid=None, clips=None, category="운명학 사전", done=False, kw_vol=KW_VOL,
                    k131="n100 11/19(K-151 새 글)", source="build_naver_100.py (n21 주제 새 글, n21 그대로)")
    json.dump(reg, open(MP.REG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    ic = json.load(open(os.path.join(HERE, "intent_cards.json"), encoding="utf-8")); ic["cards"][PID] = INTENT
    json.dump(ic, open(os.path.join(HERE, "intent_cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    v = reg[PID]
    MP.write_page(PID, D.datetime.fromisoformat(v["dt"]), v["title"], v["tags"], v["body"], None, v["cover"], v["related"], v["category"])
    MP.write_index()
    import k151_check as K
    print(PID, len(TITLE), "자 제목 · 본문 글자", len(re.sub(r"<[^>]+>|&nbsp;", "", body)), "· 사진", made, "· K 검사", K.check(PID, v))
