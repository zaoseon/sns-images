"""네이버 n105: 당사주 보는 법 새 글 (CT 11/4 19:40 재발행 일정 '새 글로 다시 쓰기' n61 → n105, 진행표 docs/네이버_누락글_진행표_2026-11-18.md 열둘째 줄).
- 왜: 검색에 '다른 글'만 잡히는 옛 글 n61(당사주 뜻과 보는 법, 띠로 내 초년 별 바로 찾기)을 새 글로. n61은 건드리지 않는다(K-147·K-178).
- 검색어: n105 묶음(당사주·당사주보는법·당사주풀이·무료당사주·당사주뜻) 11/21 11:45 ① 요청 → kw-volume 12:07 예약에서 잼.
- 다르게 쓴 것(K-151): n61의 첫 질문·인사·한 줄 요약·열두 별 뜻 목록·띠별 초년 별 열둘·네 칸 달리기 비유·갑인년 7월 26일 예시·자미두수·하락이수·부정성 편향 대신
  당사주 정의 직답, 네 별을 세는 순서(해 → 달 → 날 → 시, 한 칸씩 이어 셈), 양력 1991.2.10 오전 10시생 예시(설날 2.15 전이라 음력 1990.12.26 말띠,
  사주 해 글자는 입춘 뒤라 辛未 양띠 — engine·음력 변환 assert), 설날 기준과 입춘 기준으로 셌을 때 네 별 비교, 12시 순서 표,
  심리 = 역사의 끝 착각(Quoidbach·Gilbert·Wilson 2013, 1만 9천 명 넘게·18~68세, 초록 확인). 그림 유형 route·compare·checklist. 연결글 → n78(사주 시간표).
- 출처 2개(K-162, 11/21 확인): 한국민족문화대백과사전 '당사주'(E0013895, 천귀성을 12지의 자에 붙여 차례로, 초년·중년·말년·평생 네 단계, 생월은 생년 자리에서
  정월·2월 차례로, 생일은 하루·이틀, 생시는 자시·축시 차례로 셈) · Quoidbach, Gilbert & Wilson (2013) Science 339(6115) 96-98, DOI 10.1126/science.1229294.
  백과사전 본문에 '음력'이라는 말은 없다 → 본문은 '흔히 음력으로 센다'로만 쓴다.
- 날짜: CT가 정한다. pages.json dt 는 자리값, dt_tbd 로 표시.
사용: SITE=<zaoseon-site> python3 naver/build_naver_105.py"""
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
       '<tr><td style="padding:12px 10px;text-align:center;border:1px solid #d0d0d0"><b>당사주 말고 내 사주 여덟 글자가 궁금하다면</b></td></tr>'
       '<tr><td style="padding:12px 10px;text-align:center;border:1px solid #d0d0d0"><span style="color:#9a9a9a">[ 1991 . 02 . 10 ]</span></td></tr>'
       '<tr><td style="padding:12px 10px;text-align:center;border:1px solid #d0d0d0"><b><a href="https://zaoseon.com/?utm_source=naver&amp;utm_medium=mid#free">내 태어난 날 글자 보기 →</a></b></td></tr>'
       '</tbody></table>' + BL)
CTA = ('<p><a href="https://zaoseon.com/?utm_source=naver&utm_medium=cta#free"><img src="' + RAW +
       'naver_cta5_1%EC%B4%88%EB%AC%B4%EB%A3%8C%ED%92%80%EC%9D%B4.jpg" alt="자오선 무료 1초 풀이 안내 배너"></a></p>')
PID, KEY, PAL = "n105", "105", "p_black_s"   # 예시 말띠(午 = 불) → 불 판 묶음. n104 m_young_s · n103 k_neon_s · n102 g_ivory_s 와 다른 판

# ───────── 계산값과 검산
import datetime as D
sys.path.insert(0, os.path.join(SITE, "engine")); import engine as E
from korean_lunar_calendar import KoreanLunarCalendar as KLC
JI = "子丑寅卯辰巳午未申酉戌亥"
STAR = ["천귀성", "천액성", "천권성", "천파성", "천간성", "천문성", "천복성", "천역성", "천고성", "천인성", "천예성", "천수성"]
SIJI = ["자", "축", "인", "묘", "진", "사", "오", "미", "신", "유", "술", "해"]
def dang(year_ji, m, d, si):   # 백과사전 순서: 해 자리 → 생월 수만큼(정월이 해 자리) → 생일 수만큼(하루가 달 자리) → 생시(자시가 날 자리)
    y = JI.index(year_ji); mo = (y + m - 1) % 12; da = (mo + d - 1) % 12; ho = (da + si) % 12
    return [STAR[y], STAR[mo], STAR[da], STAR[ho]]
assert dang("寅", 7, 26, 6) == ["천권성", "천고성", "천인성", "천파성"]          # n61 예시(갑인년 7월 26일 오시)와 같은 셈인지 확인
c = KLC(); c.setSolarDate(1991, 2, 10); assert (c.lunarYear, c.lunarMonth, c.lunarDay, c.isIntercalation) == (1990, 12, 26, False), c.LunarIsoFormat()
c2 = KLC(); assert c2.setLunarDate(1991, 1, 1, False) and c2.SolarIsoFormat() == "1991-02-15"     # 1991년 설날
S = E.compute_saju(D.datetime(1991, 2, 10, 10))["팔자"]
assert S["년주"] == "辛未" and S["시주"][1] == "巳", S                               # 사주 해는 입춘(2/4) 뒤라 辛未(양띠), 오전 10시 = 사시
T91 = dict((n, t) for n, _, t in E.get_solar_terms_kst(1991)); assert (T91["입춘"].month, T91["입춘"].day) == (2, 4)
GOOD = dang("午", 12, 26, 5); BAD = dang("未", 12, 26, 5)                            # 사시 = 여섯째 시(자시에서 다섯 칸)
assert GOOD == ["천복성", "천문성", "천복성", "천수성"], GOOD
assert BAD == ["천역성", "천복성", "천역성", "천귀성"], BAD
print("당사주 셈(n61 예시 일치) · 1991.2.10 → 음력 1990.12.26 · 설날 2/15 · 사주 해 辛未 · 네 별", GOOD, "대 입춘 기준", BAD)

# ───────── 본문 (n61 문장을 옮기지 않았다)
head = ["<b>당사주는 별 네 개로 한평생을 읽는 옛 점법이에요. 열두 별을 열두 띠 자리에 하나씩 붙여 두고, 태어난 해·달·날·시를 차례로 세어 넷을 찾아요.</b>",
        "네 별은 앞에서부터 초년, 중년, 말년, 평생의 별이에요. 셈은 해 자리에서 시작해 한 칸씩 이어 가요.",
        "<b>헷갈리는 사람은 1월과 2월 초에 태어난 사람이에요. 당사주의 띠는 설날로, 사주의 띠는 입춘으로 바뀌어서 같은 사람인데 띠가 다르게 나올 수 있어요.</b>",
        "이 글은 네 별을 세는 순서, 1991년 2월 10일생 예시, 띠를 잘못 잡았을 때 달라지는 별, 앞날을 읽는 마음까지 다뤄요."]
toc_q = ["당사주는 무엇을 세는 걸까요?", "네 별은 어떤 순서로 셀까요?", "1991년 2월 10일 오전 10시생은 어떻게 셀까요?",
         "설날 전에 태어났다면 띠를 어떻게 잡을까요?", "말년 별을 보고 앞날을 정해도 될까요?", "자주 묻는 질문"]
TOC_S = ["당사주가 세는 것", "네 별 세는 순서", "1991년 2월 10일생 예시", "설날 전 1·2월생의 띠", "말년 별과 앞날", "묻고 답하기"]
sec1 = P("<b>당사주는 사람이 태어난 해·달·날·시에 따라 하늘의 열두 별 가운데 넷을 골라 읽어요.</b>",
         "한국민족문화대백과사전은 당사주를 천귀성을 12지의 자(子)에 붙이고 나머지 별을 차례로 늘어놓아 세는 점법으로 적고 있어요.",
         "열두 별은 자리 순서대로 천귀성, 천액성, 천권성, 천파성, 천간성, 천문성, 천복성, 천역성, 천고성, 천인성, 천예성, 천수성이에요.") + \
       P("사주가 여덟 글자를 놓고 글자끼리의 사이를 읽는다면, 당사주는 별 넷의 이름을 읽어요. 그래서 처음 보는 사람도 손가락으로 셀 수 있어요.",
         "📚 <b>출처 1</b>: <a href=\"https://encykorea.aks.ac.kr/Article/E0013895\">한국민족문화대백과사전, 당사주</a>")
sec2 = P("<b>네 별은 따로 찾지 않고, 앞 별의 자리에서 이어서 세요.</b>",
         "1. 해: 태어난 해의 띠 자리 별이 초년 별이에요. 쥐띠는 자 자리라 천귀성이에요.",
         "2. 달: 초년 별 자리를 정월로 두고, 태어난 달까지 한 칸씩 세어요. 닿은 별이 중년 별이에요.",
         "3. 날: 중년 별 자리를 하루로 두고, 태어난 날까지 세어요. 닿은 별이 말년 별이에요.",
         "4. 시: 말년 별 자리를 자시로 두고 축시, 인시 차례로 태어난 시까지 세어요. 닿은 별이 평생 별이에요.") + "[[R]]" + \
       P("시는 두 시간씩 열둘로 나눠요. 밤 11시~새벽 1시가 자시, 새벽 1~3시가 축시이고, 오전 9~11시는 여섯째인 사시예요.",
         "당사주는 달을 정월, 2월로 세기 때문에 흔히 음력 생일로 셈해요. 양력 생일이라면 음력으로 먼저 바꿔 두세요.")
sec3 = P("🔎 <b>양력 1991년 2월 10일 오전 10시에 태어난 사람을 예로 세어 볼게요.</b>",
         "1991년 설날은 양력 2월 15일이에요. 2월 10일은 설날 닷새 전이라, 음력으로는 1990년 12월 26일이에요.",
         "1990년은 경오년, 말띠예요. 말(오) 자리의 별인 천복성이 초년 별이에요.") + \
       P("달은 12월이라 오 자리에서 열한 칸을 더 세어 사 자리, 천문성이 중년 별이에요.",
         "날은 26일이라 사 자리에서 스물다섯 칸을 더 세어 오 자리, 천복성이 말년 별이에요.",
         "시는 오전 10시, 사시라 오 자리에서 다섯 칸을 더 세어 해 자리, 천수성이 평생 별이에요.",
         "이 사람의 네 별은 천복성, 천문성, 천복성, 천수성이에요.") + MID
sec4 = P("<b>같은 사람의 띠가 당사주에서는 말띠, 사주에서는 양띠로 나와요.</b>",
         "사주는 해가 입춘에 바뀌어요. 1991년 입춘은 2월 4일이라, 2월 10일생의 사주 해 글자는 신미(辛未), 양띠예요.",
         "당사주는 음력 해를 따르니 설날 전인 2월 10일생은 아직 1990년 말띠예요.") + "[[C]]" + \
       P("양띠로 잘못 잡고 세면 네 별이 천역성, 천복성, 천역성, 천귀성으로 바뀌어요. 첫 칸이 하나 밀리니 네 별이 모두 달라져요.",
         "양력 1월이나 2월 초에 태어났다면, 그해 설날 날짜부터 확인해 보세요. 설날 전이면 앞 해의 띠로 세요.")
sec5 = P("<b>말년 별 하나로 앞날을 정해 두기보다, 지금부터 바꿀 수 있는 몫을 남겨 두세요.</b>",
         "🧠 심리학자 쿼이드백·길버트·윌슨은 18세부터 68세까지 1만 9천 명 넘는 사람에게 지난 10년과 앞으로 10년을 물었어요(2013).",
         "나이와 상관없이 사람들은 지난 10년 동안 많이 바뀌었다고 답하면서, 앞으로 10년은 별로 안 바뀔 거라고 내다봤어요.",
         "연구진은 이것을 '역사의 끝 착각'이라고 불렀어요. 지금의 내가 끝까지 갈 거라고 여기는 마음이에요.") + \
       P("당사주의 말년 별도 같은 자리에 놓고 보면 좋아요. 지금 내 모습이 그대로 이어진다고 보면 별 이름이 정해진 답처럼 들려요.",
         "10년 전의 나를 떠올려 보면, 앞으로 10년도 그만큼 바뀔 수 있다는 걸 알 수 있어요.",
         "📚 <b>출처 2</b>: <a href=\"https://doi.org/10.1126/science.1229294\">Quoidbach, Gilbert &amp; Wilson (2013), The end of history illusion, Science</a>") + "[[L]]" + \
       P("🌱 <b>마음 코치 정월의 질문</b>", "10년 전의 나와 지금의 나는<br>무엇이 가장 달라졌나요?",
         "🔸 10년 뒤의 나는<br>무엇이 달라져 있으면 좋을까요?",
         "먼저 내 양력 생일을 음력으로 바꿔서 설날 전인지 확인하고, 위 순서대로 네 별을 세어 10년 전과 달라진 점과 함께 종이에 적어 보세요.")
sec6 = P("<b>Q. 당사주와 사주는 무엇이 다른가요?</b>",
         "A. 사주는 입춘과 절기로 해와 달을 나눠 여덟 글자를 세우고, 당사주는 흔히 음력 날짜로 별 네 개를 세요. 그래서 1·2월생은 띠부터 다르게 나올 수 있어요.") + \
       P("<b>Q. 태어난 시를 모르면 어떻게 하나요?</b>",
         "A. 초년·중년·말년 별 셋은 날짜만 알면 나와요. 평생 별만 비워 두고, 시를 알게 되면 그때 이어서 세면 돼요.") + \
       P("<b>Q. 남자와 여자는 세는 방향이 다른가요?</b>",
         "A. 곳에 따라 여자는 거꾸로 세는 방식도 써요. 백과사전에 적힌 방식은 남녀 구분 없이 차례로 세는 방식이라, 이 글도 그 순서로 셌어요.")
tail = P("여러분은 설날 전에 태어났나요, 뒤에 태어났나요?", "댓글에 '설날 전'이나 '설날 뒤' 한 마디만 남겨 주세요.") + \
       '<p><b>👇 사주에서 내가 태어난 시가 무슨 시인지 헷갈린다면, 사주 시간표, 오후 3시 52분은 무슨 시일까</b></p>'
secs = [sec1, sec2, sec3, sec4, sec5, sec6]

def _have(n): return os.path.exists(os.path.join(HERE, "img", n))
def build():
    for d_ in ("wide", "m1280", "master"): os.makedirs(os.path.join(HERE, "img", d_), exist_ok=True)
    c = V.Ctx(PAL); made = []
    a4 = f"wide/naver_z{KEY}_a5.jpg"   # 표지 항목은 한글만(11/18 n96 a4)
    if not _have(a4):
        V.render(PID + "_new", {"d": "N", "el": "불", "kick": "당사주 보는 법", "hook": ["설날 전에 태어났다면", "띠부터 다시 세요"], "sub": "네 별 세는 순서와 예시 한 명",
                                "items": ["초년", "중년", "말년"]}, os.path.join(HERE, "img", a4), PAL)
    made.append(a4)
    nm = {"R": f"naver_z{KEY}_r3.jpg", "C": f"naver_z{KEY}_c3.jpg", "L": f"naver_z{KEY}_k3.jpg"}
    if not _have(nm["R"]):
        DGB.route(nm["R"], c, "당사주 네 별 세는 순서", [("해 · 초년", "띠 자리 별"), ("달 · 중년", "정월부터 생월까지"), ("날 · 말년", "하루부터 생일까지"), ("시 · 평생", "자시부터 생시까지")])
    if not _have(nm["C"]):
        DGC.compare(nm["C"], c, "양력 1991년 2월 10일 오전 10시생", ("설날 기준 말띠", "입춘 기준 양띠"),
                    [("초년", GOOD[0], BAD[0]), ("중년", GOOD[1], BAD[1]), ("말년", GOOD[2], BAD[2]), ("평생", GOOD[3], BAD[3])],
                    "당사주는 음력 해 · 1991년 설날 2월 15일 · 입춘 2월 4일", hi=0)
    if not _have(nm["L"]):
        DGB.checklist(nm["L"], c, "당사주 세기 전 네 가지", [("음력 생일", "양력이면 음력으로 바꿔요"), ("설날 전인지", "전이면 앞 해의 띠"),
                                                       ("태어난 시", "두 시간씩 열두 시"), ("10년 전의 나", "앞날도 그만큼 바뀌어요")])
    import fullbleed as FBL
    plan_p = os.path.join(HERE, "fullbleed_plan.json"); plan = json.load(open(plan_p, encoding="utf-8")) if os.path.exists(plan_p) else {}
    rows = []
    for pos, k in enumerate("RCL", 1):
        f = nm[k][:-4] + "f.jpg"
        if not _have(f):
            r, why = FBL.convert(nm[k], [os.path.join(HERE, "img"), os.path.join(HERE, "img", "m1280")])
            if not r: print("fullbleed 건너뜀", nm[k], why); made.append(nm[k]); continue
        rows.append({"pos": pos, "old": nm[k], "new": f}); made.append(nm[k]); nm[k] = f
        reg_ = json.load(open(DG.REG, encoding="utf-8")); reg_[f] = reg_[rows[-1]["old"]]; json.dump(dict(sorted(reg_.items())), open(DG.REG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    plan[PID] = rows; json.dump(plan, open(plan_p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    made += [v for v in nm.values() if v not in made]
    alt = {"R": "당사주 네 별을 세는 순서 그림. 해는 띠 자리 별이 초년, 달은 정월부터 생월까지 세어 중년, 날은 하루부터 생일까지 세어 말년, 시는 자시부터 생시까지 세어 평생 별이에요",
           "C": "양력 1991년 2월 10일 오전 10시생을 설날 기준 말띠와 입춘 기준 양띠로 셌을 때 네 별을 견준 그림. 말띠는 천복성·천문성·천복성·천수성, 양띠는 천역성·천복성·천역성·천귀성이에요",
           "L": "당사주를 세기 전 확인할 네 가지 그림. 음력 생일, 설날 전인지, 태어난 시, 10년 전의 나"}
    body = P(*head) + P("<b>📌 당사주를 세는 순서</b>", *[f"{i + 1}. {q}" for i, q in enumerate(TOC_S)])
    for i, (q, s) in enumerate(zip(toc_q, secs)):
        for k in "RCL": s = s.replace(f"[[{k}]]", IMG(nm[k], alt[k]))
        body += H(f"{i + 1}. {q}") + s
    body += tail + CTA
    import copy_rules as CR
    for w in ("재미로", "상담", "—", "안녕하세요, 자오선의 정월이에요", "결론부터 말씀드릴게요", "생년월일만 넣으면 1초", "한 줄 요약", "이 글의 순서", "수비학",
              "자미두수", "하락이수", "부정성 편향", "바우마이스터", "갑인년", "달리기", "총정리", "솜씨", "값을 매", "기운", "흐름", "편이에요") + tuple(CR.금지어):
        assert w not in re.sub(r"<[^>]+>", " ", body), w
    for f in made:   # 사이트 사본(K-069)
        dst = os.path.join(SITE, "public", "naver", "img", f); os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy(os.path.join(HERE, "img", f), dst)
    return body, a4, made

TITLE = "당사주 보는 법, 음력 생일로 네 별 세는 순서와 1월생 예시"
TAGS = ["당사주", "당사주보는법", "당사주풀이", "무료당사주", "당사주뜻", "초년운", "말년운", "음력생일", "설날띠", "자오선"]
REL = {"id": "n78", "title": "사주 시간표, 오후 3시 52분은 무슨 시일까",
       "phrase": "사주에서 내가 태어난 시가 무슨 시인지 헷갈린다면, 사주 시간표, 오후 3시 52분은 무슨 시일까",
       "url": "https://blog.naver.com/zaoseon/224469680434"}
KW_VOL = (json.load(open(os.path.join(SITE, "data", "keywords", "kw_volume.json"), encoding="utf-8"))["posts"].get(PID) or {}).get("씨앗") or {}
INTENT = {"keywords": ["당사주", "당사주보는법", "당사주풀이"],
          "keyword_src": "n61 재발행 일정 '새 글로 다시 쓰기'(진행표 11/18 열둘째 줄) · 월 검색량은 kw-volume n105 요청(11/21 11:45)",
          "intent": "방법을 알고 싶다", "intent_note": "당사주 네 별을 어떤 순서로 세는지, 내 띠를 무엇으로 잡는지(설날·입춘), 예시 한 명으로 직접 세어 보기",
          "first3": "당사주는 열두 별을 띠 자리에 붙이고 태어난 해·달·날·시를 차례로 세어 별 넷을 찾는 점법이에요. 네 별은 초년·중년·말년·평생이에요. 1·2월생은 설날 기준 띠와 입춘 기준 띠가 달라 별이 모두 바뀔 수 있어요.",
          "answer_keys": ["당사주 = 열두 별 중 넷", "해→달→날→시 이어 세기", "당사주 띠는 설날, 사주 띠는 입춘", "앞날은 생각보다 많이 바뀜(역사의 끝 착각)"],
          "community_q": [], "order": toc_q, "images": ["네 별 세는 순서(route)", "설날 기준 대 입춘 기준(compare)", "세기 전 네 가지(checklist)"],
          "related": "n78", "cta": PID, "experience": [], "applied": True,
          "differs_from_n61": "제목(당사주 뜻과 보는 법·띠로 초년 별 → 네 별 세는 순서·1월생 예시)·도입(인사·한 줄 요약 → 정의 직답)·소제목 순서·열두 별 뜻 목록·띠별 초년 별 열둘·네 칸 달리기·갑인년 예시·자미두수·하락이수·부정성 편향(Baumeister 2001) 대신 세는 순서·1991.2.10 예시(음력 변환·사주 해 assert)·설날 대 입춘 비교·역사의 끝 착각(Quoidbach 외 2013)·그림 유형(route·compare·checklist)·연결글(→ n78)"}

if __name__ == "__main__":
    body, a4, made = build()
    reg = json.load(open(MP.REG, encoding="utf-8"))
    assert PID not in reg or not reg[PID].get("done"), "이미 예약 끝난 글"
    reg[PID] = dict(dt="2027-02-12T08:00:00", dt_tbd="CT가 정함(재발행 일정 'n61 다시 쓰기' 자리, 진행표 11/18). 이 날짜는 자리값", title=TITLE, tags=TAGS, body=body,
                    cover=a4, related=REL, thumbs=None, cid=None, clips=None, category="운명학 사전", done=False, kw_vol=KW_VOL,
                    k131="n105 11/21(K-151 새 글)", source="build_naver_105.py (n61 주제 새 글, n61 그대로)")
    json.dump(reg, open(MP.REG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    ic = json.load(open(os.path.join(HERE, "intent_cards.json"), encoding="utf-8")); ic["cards"][PID] = INTENT
    json.dump(ic, open(os.path.join(HERE, "intent_cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    v = reg[PID]
    MP.write_page(PID, D.datetime.fromisoformat(v["dt"]), v["title"], v["tags"], v["body"], None, v["cover"], v["related"], v["category"])
    MP.write_index()
    import k151_check as K
    print(PID, len(TITLE), "자 제목 · 본문 글자", len(re.sub(r"<[^>]+>|&nbsp;", "", body)), "· 사진", made, "· K 검사", K.check(PID, v))
