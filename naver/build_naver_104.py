"""네이버 n104: 생년월일 운세·음력 생일 새 글 (CT 11/4 19:40 재발행 일정 '새 글로 다시 쓰기' n13 → n104, 진행표 docs/네이버_누락글_진행표_2026-11-18.md 열한째 줄).
- 왜: 검색에 '다른 글'만 잡히는 옛 글 n13(같은 생년월일을 여섯 가지 운명학으로 읽으면?)을 새 글로. n13은 건드리지 않는다(K-147·K-178).
- 주제를 고른 이유: n13의 '여섯 운명학 겹쳐 읽기'는 n88(점성술과 사주 차이)·n85 가, '같은 날 다른 시간'은 n75(앱마다 시주가 다른 이유)·n78(사주 시간표)이 이미 다룬다.
  겹치지 않는 '같은 생년월일'의 질문 = 음력 생일을 어떻게 넣는가(음력 숫자를 양력 칸에 넣는 실수·윤달생). 사이트 무료 풀이 칸도 양력만 받는다('음력 생일이면 양력으로 바꿔 넣어 주세요').
- 검색어: data/keywords/kw_volume.json — 생년월일운세 23,850(posts.n73·n84 등 연관상위). 음력 관련 검색어는 아직 안 잼 → kw_volume_request 에 n104 묶음, 발행 7일 뒤 검색어로 고침(K-143).
- 다르게 쓴 것(K-151): n13의 첫 질문·인사·한 줄 요약·여섯 풀이 소개·가상 인물 1990.5.15·자미두수 탐랑성·하락이수 귀매괘·점성술 차트·수비학 대신
  생년월일 운세 정의 직답, 사주 달은 절기로 정해져 계산은 양력으로 한다는 점, 음력 1993.3.15 오전 10시 → 양력 4.6(癸酉·丙辰·丁巳·乙巳) 대
  같은 숫자를 양력 칸에 넣은 3.15(癸酉·乙卯·乙未·辛巳), 윤3월 15일 → 5.6(丁巳 달), 윤달 해 목록(1987~2025, 19년에 7번 assert), 음력 3월 15일의 양력 날짜 2025~2028,
  같은 생년월일 하루 약 651명(2024 출생 23만 8,300명 ÷ 366일). 그림 유형 compare·route·checklist. 연결글 → n87(사주 보는 법 만세력 4단계, 11/20 노출 '예').
- 출처 2개(K-162, 11/20 확인): 한국천문연구원 음양력 변환(엔진이 쓰는 korean_lunar_calendar 가 KASI 자료 기반) ·
  통계청 2024년 출생·사망통계(잠정) 출생아 23만 8,300명(뉴시스 2025.2.26 보도 본문 확인, 8월 확정 보도 본문도 23만 8,300명).
- 날짜: CT가 정한다. pages.json dt 는 자리값, dt_tbd 로 표시.
사용: SITE=<zaoseon-site> python3 naver/build_naver_104.py"""
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
       '<tr><td style="padding:12px 10px;text-align:center;border:1px solid #d0d0d0"><b>음력 생일을 양력으로 바꿨다면</b></td></tr>'
       '<tr><td style="padding:12px 10px;text-align:center;border:1px solid #d0d0d0"><span style="color:#9a9a9a">[ 1993 . 04 . 06 ]</span></td></tr>'
       '<tr><td style="padding:12px 10px;text-align:center;border:1px solid #d0d0d0"><b><a href="https://zaoseon.com/?utm_source=naver&amp;utm_medium=mid#free">내 태어난 날 글자 보기 →</a></b></td></tr>'
       '</tbody></table>' + BL)
CTA = ('<p><a href="https://zaoseon.com/?utm_source=naver&utm_medium=cta#free"><img src="' + RAW +
       'naver_cta5_1%EC%B4%88%EB%AC%B4%EB%A3%8C%ED%92%80%EC%9D%B4.jpg" alt="자오선 무료 1초 풀이 안내 배너"></a></p>')
PID, KEY, PAL = "n104", "104", "m_young_s"   # 달(음력) = 물 판 묶음(EL_SET 물). n103 k_neon_s · n102 g_ivory_s · n101 y_black_s 와 다른 판

# ───────── 계산값과 검산
import datetime as D
sys.path.insert(0, os.path.join(SITE, "engine")); import engine as E
from korean_lunar_calendar import KoreanLunarCalendar as KLC
def L2S(y, m, d, leap=False):
    c = KLC(); assert c.setLunarDate(y, m, d, leap), (y, m, d, leap); return D.date.fromisoformat(c.SolarIsoFormat())
def has_leap(y): return [m for m in range(1, 13) if KLC().setLunarDate(y, m, 1, True)]
assert L2S(1993, 3, 15) == D.date(1993, 4, 6) and L2S(1993, 3, 15, True) == D.date(1993, 5, 6)
RIGHT = E.compute_saju(D.datetime(1993, 4, 6, 10))["팔자"]; WRONG = E.compute_saju(D.datetime(1993, 3, 15, 10))["팔자"]
LEAP = E.compute_saju(D.datetime(1993, 5, 6, 10))["팔자"]
assert RIGHT == {"년주": "癸酉", "월주": "丙辰", "일주": "丁巳", "시주": "乙巳"}, RIGHT
assert WRONG == {"년주": "癸酉", "월주": "乙卯", "일주": "乙未", "시주": "辛巳"}, WRONG
assert LEAP["월주"] == "丁巳" and LEAP["일주"] == "丁亥", LEAP
T93 = dict((n, t) for n, _, t in E.get_solar_terms_kst(1993))
assert (T93["입하"].month, T93["입하"].day, T93["입하"].hour) == (5, 5, 21) and (T93["청명"].month, T93["청명"].day) == (4, 5)
LEAPS = {y: has_leap(y)[0] for y in range(1985, 2031) if has_leap(y)}
assert LEAPS == {1987: 6, 1990: 5, 1993: 3, 1995: 8, 1998: 5, 2001: 4, 2004: 2, 2006: 7, 2009: 5, 2012: 3, 2014: 9, 2017: 5, 2020: 4, 2023: 2, 2025: 6, 2028: 5}, LEAPS
assert len([y for y in LEAPS if 1987 <= y <= 2005]) == 7                               # 19년에 일곱 번
assert (L2S(2027, 1, 1) - L2S(2026, 1, 1)).days == 355 and (L2S(2024, 1, 1) - L2S(2023, 1, 1)).days == 384   # 윤달 없는 해·있는 해
BDAY = {y: L2S(y, 3, 15) for y in (2025, 2026, 2027, 2028)}
assert BDAY == {2025: D.date(2025, 4, 12), 2026: D.date(2026, 5, 1), 2027: D.date(2027, 4, 21), 2028: D.date(2028, 4, 9)}, BDAY
BIRTHS_2024 = 238300; assert round(BIRTHS_2024 / 366) == 651                            # 2024 윤년 366일
assert E.ten_god("丁", "乙") == "편인"
print("음력→양력·잘못 넣은 사주·윤3월·입하·윤달 해 16개·음력 해 길이·음력 생일 4년·하루 출생 다시 확인")

# ───────── 본문 (n13 문장을 옮기지 않았다)
_ly = [f"{y} 윤{m}월" for y, m in LEAPS.items() if y <= 2025]; LY1, LY2 = " · ".join(_ly[:8]), " · ".join(_ly[8:])
head = ["<b>생년월일 운세는 태어난 해·달·날·시간을 여덟 글자(사주)로 바꿔 읽는 거예요. 음력 생일을 양력으로 바르게 바꿔 넣으면 사주는 똑같이 나와요.</b>",
        "문제는 음력 숫자를 양력 칸에 그대로 넣을 때예요. 그러면 다른 날에 태어난 사람의 사주가 나와요.",
        "<b>음력 1993년 3월 15일생을 양력 3월 15일로 넣으면, 태어난 날 글자가 丁巳에서 乙未로 바뀌어요.</b>",
        "윤달에 태어났다면 '윤달'까지 표시해야 해요. 1993년에는 3월이 두 번 있어서, 3월 15일과 윤3월 15일은 양력으로 꼭 한 달 차이가 나요."]
toc_q = ["생년월일 운세는 음력과 양력 중 무엇으로 볼까요?", "음력 숫자를 양력 칸에 넣으면 무엇이 바뀔까요?", "윤달에 태어났다면 어떻게 넣을까요?",
         "음력 생일은 왜 해마다 양력 날짜가 바뀔까요?", "생년월일을 넣기 전에 확인할 네 가지", "자주 묻는 질문"]
sec1 = P("<b>사주 계산은 양력 날짜로 해요. 사주의 해와 달이 음력 1일이 아니라 절기로 바뀌기 때문이에요.</b>",
         "절기는 해가 하늘에서 지나는 길을 스물넷으로 나눈 날이에요. 입춘은 해마다 양력 2월 4일 무렵, 입하는 5월 5일 무렵처럼 양력 날짜가 거의 같아요.",
         "음력 1일은 달 모양으로 정해서 해마다 양력과 열흘 넘게 어긋나요. 그래서 만세력은 음력 날짜를 받아도 먼저 양력으로 바꾼 뒤에 셈해요.") + \
       P("자오선 무료 풀이 칸도 양력 날짜를 받아요. 음력 생일이라면 한국천문연구원 음양력 변환에서 양력 날짜를 먼저 찾은 뒤 넣어 주세요.",
         "바꾸는 데 1분이면 되고, 한 번 찾은 양력 날짜는 휴대폰 메모에 적어 두면 다음에도 그대로 써요.")
sec2 = P("🔎 <b>음력 1993년 3월 15일 오전 10시에 태어난 사람을 예로 들어 볼게요.</b>",
         "음력 3월 15일을 양력으로 바꾸면 1993년 4월 6일이에요. 여덟 글자는 癸酉·丙辰·丁巳·乙巳, 태어난 날의 첫 글자(일간)는 정(丁) 불이에요.") + "[[C]]" + \
       P("같은 숫자를 양력 칸에 그대로 넣으면 1993년 3월 15일이 돼요. 실제보다 22일 앞선 날이라 여덟 글자가 癸酉·乙卯·乙未·辛巳로 나와요.",
         "해 글자 癸酉만 같고, 달 글자도 날 글자도 시간 글자도 달라요. 일간이 불에서 나무로 바뀌니, 성격 풀이부터 좋은 달까지 다른 사람 이야기를 읽게 돼요.",
         "풀이를 읽는데 하나도 안 맞는다는 느낌이 들면, 음력 숫자를 양력 칸에 넣지 않았는지 먼저 확인해 보세요.") + MID
sec3 = P("<b>음력 열두 달은 354~355일이라 양력 365일보다 열흘쯤 짧아요. 이 차이를 맞추려고 2~3년에 한 번 같은 달을 한 번 더 넣는데, 이 달이 윤달이에요.</b>",
         "1987년부터 2025년 사이 윤달이 있던 해는 아래와 같아요.", LY1, LY2, "1987년부터 2005년까지 19년 동안 일곱 번 들어갔어요.") + \
       P("1993년생이라면 음력 3월이 두 번이에요. 3월 15일은 양력 4월 6일, 윤3월 15일은 양력 5월 6일이에요.",
         "5월 6일은 그해 입하(5월 5일 밤 9시쯤) 뒤라, 달 글자가 丙辰이 아니라 丁巳가 돼요. 날 글자도 丁巳에서 丁亥로 달라져요.",
         "윤달생인데 변환할 때 '윤달' 칸을 빼먹으면 한 달 앞선 날로 바뀌어요. 부모님께 생일을 여쭐 때 '윤달이었는지'도 같이 물어보세요.")
sec4 = P("<b>음력 생일은 매년 같은 음력 날짜라서, 양력 달력에서는 해마다 날짜가 바뀌어요.</b>",
         "음력 3월 15일생이라면 양력으로 2025년 4월 12일, 2026년 5월 1일, 2027년 4월 21일, 2028년 4월 9일이 생일이에요. 같은 생일이 3주 넘게 오가요.") + "[[R]]" + \
       P("생일 축하는 음력으로 해도 괜찮아요. 다만 사주는 태어난 해의 양력 날짜 하나로 정해져요. 올해 음력 생일의 양력 날짜를 넣으면 다른 날의 사주가 나와요.",
         "가족 생일을 음력으로 챙긴다면, 연초에 올해의 양력 날짜를 달력에 한 번에 적어 두면 편해요.")
sec5 = P("<b>생년월일 운세를 보기 전에 네 가지만 확인하면 엉뚱한 사주를 읽을 일이 줄어요.</b>") + "[[L]]" + \
       P("📚 <b>출처 1</b>: <a href=\"https://astro.kasi.re.kr/life/pageView/5\">한국천문연구원 천문우주지식정보, 음양력 변환</a>",
         "📚 <b>출처 2</b>: <a href=\"https://www.newsis.com/view/NISX20250226_0003079235\">통계청 2024년 출생통계(잠정), 뉴시스 2025년 2월 26일 보도</a>") + \
       P("🌱 <b>마음 코치 정월의 질문</b>", "내 생일이 음력인지 양력인지<br>마지막으로 확인한 건 언제였나요?",
         "🔸 가족 중에 음력 생일을 챙기는 사람이 있다면<br>올해 양력 날짜는 언제인가요?") + \
       P("✔️ <b>오늘 해 볼 것</b>",
         "1. 부모님께 내 생일이 음력인지, 윤달이었는지 문자로 여쭤 보세요.",
         "2. 음력이라면 한국천문연구원 음양력 변환에서 양력 날짜를 찾아 메모에 적어 두세요.",
         "3. 찾은 양력 날짜로 내 태어난 날 글자를 한 번 확인해 보세요.")
sec6 = P("<b>Q. 주민등록번호 생일이 음력이면 어떻게 하나요?</b>",
         "A. 출생 신고 때 음력 생일로 적은 경우가 있어요. 그 숫자가 음력이라면 양력으로 바꿔서 넣어야 해요. 확실하지 않다면 부모님이나 출생 기록으로 먼저 확인해 보세요.") + \
       P("<b>Q. 같은 생년월일이면 사주도 같나요?</b>",
         "A. 2024년에 태어난 아기는 23만 8,300명, 하루에 약 651명이에요. 같은 날 태어나면 해·달·날 여섯 글자는 같고, 태어난 시간에 따라 마지막 두 글자가 달라져요.") + \
       P("<b>Q. 밤 11시 넘어 태어났으면 날짜를 바꿔야 하나요?</b>",
         "A. 사주에서는 밤 11시부터를 다음 날로 봐요. 음력을 양력으로 바꾼 뒤, 밤 11시~자정 사이라면 무료 풀이 칸의 '밤 11시~자정 사이에 태어났어요' 칸에 표시해 주세요.")
tail = P("여러분의 생일은 음력인가요, 양력인가요?", "댓글에 '음력'이나 '양력' 한 단어만 남겨 주세요. 윤달생이라면 '윤달'도 함께요.") + \
       '<p><b>👇 사주 여덟 글자를 처음부터 차례대로 읽고 싶다면, 사주 보는 법, 만세력 여덟 글자를 예시 한 명으로 읽는 4단계</b></p>'
TOC_S = ["음력과 양력, 무엇으로 셈하나", "음력 숫자를 양력 칸에 넣은 예시", "윤달생이 넣는 법", "해마다 바뀌는 음력 생일", "넣기 전 네 칸", "묻고 답하기"]
secs = [sec1, sec2, sec3, sec4, sec5, sec6]

def _have(n): return os.path.exists(os.path.join(HERE, "img", n))
def build():
    for d_ in ("wide", "m1280", "master"): os.makedirs(os.path.join(HERE, "img", d_), exist_ok=True)
    c = V.Ctx(PAL); made = []
    a4 = f"wide/naver_z{KEY}_a5.jpg"   # 표지 항목은 한글만(11/18 n96 a4)
    if not _have(a4):
        V.render(PID + "_new", {"d": "N", "el": "물", "kick": "생년월일 운세", "hook": ["음력 생일을", "양력 칸에 넣으면"], "sub": "윤달생은 어떻게 넣을까",
                                "items": ["음력", "양력", "윤달"]}, os.path.join(HERE, "img", a4), PAL)
    made.append(a4)
    nm = {"C": f"naver_z{KEY}_c3.jpg", "R": f"naver_z{KEY}_r3.jpg", "L": f"naver_z{KEY}_k3.jpg"}
    if not _have(nm["C"]):
        DGC.compare(nm["C"], c, "음력 1993년 3월 15일 오전 10시생", ("양력으로 바꿔 넣음", "숫자 그대로 양력 칸에"),
                    [("넣은 날짜", "1993년 4월 6일", "1993년 3월 15일"), ("해 글자", "계유", "계유"), ("달 글자", "병진", "을묘"),
                     ("날 글자", "정사", "을미"), ("일간", "정 · 불", "을 · 나무")], "음양력 변환 한국천문연구원 · 여덟 글자 자오선 계산", hi=0)
    if not _have(nm["R"]):
        DGB.route(nm["R"], c, "음력 3월 15일생의 양력 생일", [("2025년", "4월 12일"), ("2026년", "5월 1일"), ("2027년", "4월 21일"), ("2028년", "4월 9일")])
    if not _have(nm["L"]):
        DGB.checklist(nm["L"], c, "생년월일 넣기 전 네 칸", [("내 생일이 음력인지 양력인지", "부모님이나 출생 기록으로"), ("윤달이었는지", "변환할 때 '윤달' 칸 표시"),
                                                          ("태어난 시간", "모르면 날짜까지만 넣어요"), ("밤 11시 넘었는지", "넘었다면 다음 날로")])
    import fullbleed as FBL
    plan_p = os.path.join(HERE, "fullbleed_plan.json"); plan = json.load(open(plan_p, encoding="utf-8")) if os.path.exists(plan_p) else {}
    rows = []
    for pos, k in enumerate("CRL", 1):
        f = nm[k][:-4] + "f.jpg"
        if not _have(f):
            r, why = FBL.convert(nm[k], [os.path.join(HERE, "img"), os.path.join(HERE, "img", "m1280")])
            if not r: print("fullbleed 건너뜀", nm[k], why); made.append(nm[k]); continue
        rows.append({"pos": pos, "old": nm[k], "new": f}); made.append(nm[k]); nm[k] = f
        reg_ = json.load(open(DG.REG, encoding="utf-8")); reg_[f] = reg_[rows[-1]["old"]]; json.dump(dict(sorted(reg_.items())), open(DG.REG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    plan[PID] = rows; json.dump(plan, open(plan_p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    made += [v for v in nm.values() if v not in made]
    alt = {"C": "음력 1993년 3월 15일생을 양력으로 바꿔 넣은 사주와 숫자 그대로 양력 칸에 넣은 사주를 견준 그림. 해 글자 계유만 같고 달·날 글자와 일간이 달라요",
           "R": "음력 3월 15일생의 양력 생일 그림. 2025년 4월 12일, 2026년 5월 1일, 2027년 4월 21일, 2028년 4월 9일로 해마다 바뀌어요",
           "L": "생년월일을 넣기 전 확인할 네 칸 그림. 음력인지 양력인지, 윤달이었는지, 태어난 시간, 밤 11시가 넘었는지"}
    body = P(*head) + P("<b>📌 생년월일 운세를 보기 전 읽을 순서</b>", *[f"{i + 1}. {q}" for i, q in enumerate(TOC_S)])
    for i, (q, s) in enumerate(zip(toc_q, secs)):
        for k in "CRL": s = s.replace(f"[[{k}]]", IMG(nm[k], alt[k]))
        body += H(f"{i + 1}. {q}") + s
    body += tail + CTA
    import copy_rules as CR
    for w in ("재미로", "상담", "—", "안녕하세요, 자오선의 정월이에요", "결론부터 말씀드릴게요", "생년월일만 넣으면 1초", "한 줄 요약", "이 글의 순서", "수비학",
              "여섯 가지 운명학", "자미두수", "하락이수", "탐랑", "귀매", "점성술", "가상의", "1990년 5월 15일", "총정리", "솜씨", "값을 매", "기운", "흐름", "편이에요") + tuple(CR.금지어):
        assert w not in re.sub(r"<[^>]+>", " ", body), w
    for f in made:   # 사이트 사본(K-069)
        dst = os.path.join(SITE, "public", "naver", "img", f); os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy(os.path.join(HERE, "img", f), dst)
    return body, a4, made

TITLE = "생년월일 운세, 음력 생일 넣는 법과 윤달생이 확인할 1가지"
TAGS = ["생년월일운세", "음력생일", "음력양력변환", "윤달생", "사주음력", "같은생년월일", "만세력", "사주보는법", "사주", "자오선"]
REL = {"id": "n87", "title": "사주 보는 법, 만세력 여덟 글자를 예시 한 명으로 읽는 4단계",
       "phrase": "사주 여덟 글자를 처음부터 차례대로 읽고 싶다면, 사주 보는 법, 만세력 여덟 글자를 예시 한 명으로 읽는 4단계",
       "url": "https://blog.naver.com/zaoseon/224476055740"}
_KV = json.load(open(os.path.join(SITE, "data", "keywords", "kw_volume.json"), encoding="utf-8"))["posts"]
KW_VOL = {"생년월일운세": _KV["n73"]["연관상위"]["생년월일운세"]}
KW_VOL.update((_KV.get(PID) or {}).get("씨앗") or {})
INTENT = {"keywords": ["생년월일운세", "음력생일", "음력양력변환"],
          "keyword_src": "kw-volume 작업(data/keywords/kw_volume.json posts.n73 연관상위 생년월일운세 23,850) · n13 재발행 일정 '새 글로 다시 쓰기'(진행표 11/18 열한째 줄) · 음력 검색어는 n104 묶음으로 요청(11/20 19:45)",
          "intent": "방법을 알고 싶다", "intent_note": "음력 생일로 운세를 볼 때 무엇을 넣어야 하는지, 음력 숫자를 양력 칸에 넣으면 왜 틀리는지, 윤달생은 어떻게 넣는지",
          "first3": "생년월일 운세는 태어난 날을 여덟 글자로 바꿔 읽는 거예요. 음력 생일을 양력으로 바르게 바꾸면 사주는 같고, 음력 숫자를 양력 칸에 넣으면 다른 사람의 사주가 나와요.",
          "answer_keys": ["사주 계산은 양력(절기)", "음력 숫자를 양력 칸에 넣으면 일간까지 바뀜", "윤달은 '윤달' 표시", "음력 생일의 양력 날짜는 해마다 바뀜"],
          "community_q": [], "order": toc_q, "images": ["바르게 넣음 대 숫자 그대로(compare)", "음력 생일의 양력 날짜 4년(route)", "넣기 전 네 칸(checklist)"],
          "related": "n87", "cta": PID, "experience": [], "applied": True,
          "differs_from_n13": "제목(여섯 가지 운명학 교차 분석 → 생년월일 운세 음력 생일 넣는 법·윤달생이 확인할 1가지)·도입(첫 질문·한 줄 요약·인사 → 정의 직답)·소제목 순서·여섯 풀이 소개·가상 인물 1990.5.15·자미두수·하락이수·점성술·수비학 대신 절기와 양력 계산·음력 1993.3.15 바르게/잘못 넣은 사주(engine assert)·윤달 해 목록·음력 생일 양력 날짜 4년·하루 출생 651명(통계청)·그림 유형(compare·route·checklist)·연결글(→ n87)"}

if __name__ == "__main__":
    body, a4, made = build()
    reg = json.load(open(MP.REG, encoding="utf-8"))
    assert PID not in reg or not reg[PID].get("done"), "이미 예약 끝난 글"
    reg[PID] = dict(dt="2027-02-11T18:00:00", dt_tbd="CT가 정함(재발행 일정 'n13 다시 쓰기' 자리, 진행표 11/18). 이 날짜는 자리값", title=TITLE, tags=TAGS, body=body,
                    cover=a4, related=REL, thumbs=None, cid=None, clips=None, category="운명학 사전", done=False, kw_vol=KW_VOL,
                    k131="n104 11/20(K-151 새 글)", source="build_naver_104.py (n13 주제 새 글, n13 그대로)")
    json.dump(reg, open(MP.REG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    ic = json.load(open(os.path.join(HERE, "intent_cards.json"), encoding="utf-8")); ic["cards"][PID] = INTENT
    json.dump(ic, open(os.path.join(HERE, "intent_cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    v = reg[PID]
    MP.write_page(PID, D.datetime.fromisoformat(v["dt"]), v["title"], v["tags"], v["body"], None, v["cover"], v["related"], v["category"])
    MP.write_index()
    import k151_check as K
    print(PID, len(TITLE), "자 제목 · 본문 글자", len(re.sub(r"<[^>]+>|&nbsp;", "", body)), "· 사진", made, "· K 검사", K.check(PID, v))
