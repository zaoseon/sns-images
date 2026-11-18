"""네이버 n94: 2026년 12월 손없는날 새 글 (콘텐츠 계획 11/21~12/13, 대표 11/14 20:38 '진행해' — 11/23 칸 '2026년 12월 손없는날, 대설 뒤 이사 날짜').
- 번호: n93 은 재발행 일정의 'n23 다시 쓰기' 자리로 비워 둔다(to-content 11/8 알림과 맞춤). 이 글은 n94.
- 검색어: data/keywords/kw_volume.json posts.plan_손없는날 — 12월손없는날 10,360 · 12월이사손없는날 1,640 · 손없는날 84,500(연관 상위).
- 다르게 쓴 것(K-151): 미발행 n60(11월 손없는날)의 인사·'결론부터'·한 줄 요약 줄·여섯 운명학 단락·기준점 효과 대신
  주말 손 방향 표(12월 주말 8일 중 손없는날은 27일 하루), 대설(12/7 11:52)·동지(12/22 05:50)와 손없는날이 겹치는 첫 주, 연말 계약 만료·전입신고 14일,
  심리 = 계획 오류(Buehler, Griffin & Ross 1994). 그림 유형 calendar·compass·checklist·vbar.
- 계산: 음력은 korean_lunar_calendar(KASI 기반, engine/engine.py 와 같은 것), 절기·월주는 engine/engine.py — 모두 assert.
- 출처 2개(K-162, 11/17 확인): Buehler, Griffin & Ross (1994) JPSP 67(3) 366–381, DOI 10.1037/0022-3514.67.3.366
  (연구 1: 졸업 논문 학생 37명, 예상 평균 33.9일 · 최선 27.4일 · 최악 48.6일 · 실제 55.5일 · 예상 안에 끝낸 학생 약 30%, 위키백과 'Planning fallacy' 인용 정보로 확인) · 한국천문연구원 음양력 변환.
- 날짜: CT가 정한다. pages.json dt 는 자리값, dt_tbd 로 표시. 계획 표는 11/23.
- 11/18 19:5x ① 고침(대표 11/18 18:07 "손없는 날이 꼭 이사에만 해당되냐", to-content 11/18 18:1x): 제목·첫 3줄·목차·끝 질문을 이사 밖 용도까지 넓히고
  2절 뒤에 '이사 말고 결혼·개업·계약에도 쓸까요?' 절을 더함. 이사 절(3·4·5)은 그대로. 용도 순서는 검색량 순(kw_volume son_uses_1118:
  손없는날결혼 300 · 개업 15 · 계약·입주·인테리어 각 10). 커뮤니티 질문(11/18 지식iN '이사 택일 앱마다 다르게 표기될 수 있나요')은 FAQ 한 줄로.
사용: SITE=<zaoseon-site> python3 naver/build_naver_94.py"""
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
       '<tr><td style="padding:12px 10px;text-align:center;border:1px solid #d0d0d0"><b>이사 날짜 말고, 내 12월 흐름이 궁금하다면</b></td></tr>'
       '<tr><td style="padding:12px 10px;text-align:center;border:1px solid #d0d0d0"><span style="color:#9a9a9a">[ 1990 . 12 . 07 ]</span></td></tr>'
       '<tr><td style="padding:12px 10px;text-align:center;border:1px solid #d0d0d0"><b><a href="https://zaoseon.com/?utm_source=naver&amp;utm_medium=mid#free">내 태어난 날 글자 보기 →</a></b></td></tr>'
       '</tbody></table>' + BL)
CTA = ('<p><a href="https://zaoseon.com/?utm_source=naver&utm_medium=cta#free"><img src="' + RAW +
       'naver_cta5_1%EC%B4%88%EB%AC%B4%EB%A3%8C%ED%92%80%EC%9D%B4.jpg" alt="자오선 무료 1초 풀이 안내 배너"></a></p>')
PID, KEY, PAL = "n94", "94", "p_purple_s"   # 12월 = 자(子) 물 → 물 판 묶음(EL_SET 물), n92 k_neon_s · n91 p_red_s 와 다른 판

# ───────── 계산값과 검산
import datetime as D
from korean_lunar_calendar import KoreanLunarCalendar
LC = KoreanLunarCalendar(); WD = "월화수목금토일"
def lunar(y, m, d): LC.setSolarDate(y, m, d); return LC.lunarMonth, LC.lunarDay
DIR = {1: "동", 2: "동", 3: "남", 4: "남", 5: "서", 6: "서", 7: "북", 8: "북", 9: "없음", 0: "없음"}
SON = [d for d in range(1, 32) if lunar(2026, 12, d)[1] % 10 in (9, 0)]
assert SON == [7, 8, 17, 18, 27, 28], SON
assert [WD[D.date(2026, 12, d).weekday()] for d in SON] == list("월화목금일월")
assert [lunar(2026, 12, d) for d in SON] == [(10, 29), (10, 30), (11, 9), (11, 10), (11, 19), (11, 20)]
WEEKEND = [d for d in range(1, 32) if D.date(2026, 12, d).weekday() >= 5]
assert WEEKEND == [5, 6, 12, 13, 19, 20, 26, 27]
WDIR = {d: DIR[lunar(2026, 12, d)[1] % 10] for d in WEEKEND}
assert WDIR == {5: "북", 6: "북", 12: "남", 13: "서", 19: "동", 20: "동", 26: "북", 27: "없음"}, WDIR
assert lunar(2026, 12, 25) == (11, 17) and DIR[7] == "북"                                  # 성탄절 25일(금)은 북쪽
JAN = [d for d in range(1, 32) if lunar(2027, 1, d)[1] % 10 in (9, 0)]
assert JAN == [6, 7, 16, 17, 26, 27] and [WD[D.date(2027, 1, d).weekday()] for d in JAN] == list("수목토일화수")
sys.path.insert(0, os.path.join(SITE, "engine")); import engine as E
T26 = dict((n, t) for n, _, t in E.get_solar_terms_kst(2026))
assert (T26["대설"].month, T26["대설"].day, T26["대설"].hour, T26["대설"].minute) == (12, 7, 11, 52)
DJ = E._find_term_time(2026, 270) + D.timedelta(hours=9)                                    # 동지(태양 황경 270도), KST
assert (DJ.month, DJ.day, DJ.hour, DJ.minute) == (12, 22, 5, 50)
assert E.compute_saju(D.datetime(2026, 12, 7, 9, 0))["팔자"]["월주"] == "己亥"              # 대설 전 오전은 아직 돼지 달
assert E.compute_saju(D.datetime(2026, 12, 7, 14, 0))["팔자"]["월주"] == "庚子"             # 대설 뒤 쥐 달
print("12월 손없는날·주말 방향·1월 손없는날·대설·동지·월주 다시 확인")

# ───────── 본문
head = ["<b>2026년 12월 손없는날은 7일(월), 8일(화), 17일(목), 18일(금), 27일(일), 28일(월)로 모두 여섯 번이에요.</b>",
        "손없는날은 이사뿐 아니라 결혼, 개업, 계약, 입주, 집 고치는 날을 고를 때도 같이 봐요. 그래서 날짜는 하나지만 쓰임은 여러 가지예요.",
        "주말에 걸린 손없는날은 27일 일요일 하루뿐이에요. 토요일을 생각했다면 손이 있는 방향을 먼저 보면 돼요.",
        "<b>첫 손없는날 7일은 절기 대설과 같은 날이고, 동지는 22일 새벽이에요.</b>",
        "이 글의 날짜는 2026년 11월 17일에 음력 변환으로 하나씩 다시 셌어요."]
toc_q = ["2026년 12월 손없는날은 언제일까요?", "손없는날은 왜 음력 9일과 10일일까요?", "이사 말고 결혼·개업·계약에도 쓸까요?", "주말에 이사한다면 손은 어느 쪽에 있을까요?",
         "대설과 동지 사이, 12월 이사에서 챙길 날은?", "이사 준비는 왜 늘 예상보다 길어질까요?", "12월 손없는날 자주 묻는 질문"]
sec1 = P("<b>12월 손없는날은 첫 주 월·화, 셋째 주 목·금, 마지막 주 일·월이에요.</b>",
         "📅 7일(월): 음력 10월 29일 · 8일(화): 음력 10월 30일",
         "📅 17일(목): 음력 11월 9일 · 18일(금): 음력 11월 10일",
         "📅 27일(일): 음력 11월 19일 · 28일(월): 음력 11월 20일") + "[[K]]" + \
       P("평일 손없는날이 다섯 번이라, 휴가를 하루 낼 수 있다면 고를 날이 넓어져요.",
         "연말에 계약이 끝나는 집이라면 27일(일)과 28일(월)이 가장 가까운 손없는날이에요.")
sec2 = P("<b>손은 날마다 방향을 옮겨 다니며 일을 막는다고 여긴 기운이에요. 음력 끝자리가 9와 0인 날에는 어느 쪽에도 없다고 봤어요.</b>",
         "그래서 음력으로 9일·10일·19일·20일·29일·30일을 이사, 개업, 혼례에 편한 날로 꼽았어요.",
         "양력 달력에서는 이 날이 달마다 다른 자리에 와요. 12월에는 음력 10월 끝과 11월 초·중순이 겹쳐서 7일과 8일이 이어 붙었어요.",
         "음력 10월이 30일까지 있는 큰달이라, 8일(음력 10월 30일)도 손없는날에 들어가요.")
sec2b = P("<b>네, 예부터 손없는날은 이사보다 넓게 썼어요. 혼례, 가게 문 여는 날, 집을 고치거나 들어가는 날도 이 날에서 골랐어요.</b>",
          "다만 쓰임마다 먼저 볼 것이 달라요. 손없는날은 후보를 좁히는 데 쓰고, 마지막은 일정이 정해요.") + \
        P("💍 <b>결혼</b>: 12월 주말 손없는날은 27일(일) 하나예요. 예식장은 몇 달 전에 차니, 27일이 안 되면 토요일 중 방향이 맞는 날을 후보로 둬요.",
          "🏪 <b>개업</b>: 평일 손없는날이 다섯 번(7·8·17·18·28일)이라 고르기 쉬워요. 문 여는 날보다 앞서 사업자 등록과 간판 설치 날을 맞춰 두세요.",
          "📝 <b>계약·잔금</b>: 계약서 쓰는 날과 잔금 치르는 날이 다르면, 손없는날은 잔금일에 맞춰 보세요. 보통 잔금 치르는 날에 짐이 실제로 옮겨 가요.",
          "🔨 <b>입주·집 고치기</b>: 공사를 시작하는 날을 손없는날로 잡는 풀이가 있어요. 12월 공사라면 7·8일에 시작해 17·18일 전에 끝내는 식으로 짜 볼 수 있어요.")
sec3 = P("<b>12월 주말 여덟 날 가운데 손없는날은 27일 하나예요. 나머지 토·일은 손이 있는 방향만 피하면 된다고 보는 풀이가 많아요.</b>",
         "방향은 음력 날짜의 끝자리로 정해요. 1·2는 동쪽, 3·4는 남쪽, 5·6은 서쪽, 7·8은 북쪽이에요.") + "[[G]]" + \
       P("🧭 북쪽: 5일(토), 6일(일), 26일(토)",
         "🧭 동쪽: 19일(토), 20일(일)",
         "🧭 남쪽: 12일(토) · 서쪽: 13일(일)",
         "🧭 손 없음: 27일(일)") + \
       P("방향은 지금 사는 집에서 새집을 바라본 쪽이에요. 지도 앱에 두 주소를 넣고 새집이 어느 쪽에 있는지 먼저 보세요.",
         "예를 들어 새집이 남쪽이면 12일(토)만 피하면 돼요. 나머지 주말에는 남쪽에 손이 없어요.") + MID
sec4 = P("<b>12월 7일은 손없는날이면서 절기 대설이에요. 오전 11시 52분부터 사주의 달이 쥐(子)의 달로 바뀌어요.</b>",
         "동지는 22일 오전 5시 50분이에요. 밤이 가장 긴 날이라 예부터 팥죽을 쑤어 나눠 먹었어요.",
         "동지는 손없는날이 아니에요. 22일은 음력 11월 14일이라 손이 남쪽에 있어요.") + \
       P("연말 이사는 날짜보다 서류가 먼저 막히기 쉬워요. 잔금일, 이삿짐, 전입신고를 한 줄에 놓고 보면 빠뜨리는 칸이 줄어요.") + "[[C]]" + \
       P("전입신고는 이사한 날부터 14일 안에 해야 해요(주민등록법). 전세라면 같은 날 확정일자도 받아 두세요.",
         "12월 31일 전후로 계약이 끝나는 집이 몰려서, 27일·28일 이삿짐 예약은 일찍 차요. 업체 두 곳에 같은 날 견적을 물어 두면 비교가 쉬워요.")
sec5 = P("🧠 <b>이사 준비가 늘 생각보다 오래 걸리는 데에는 이름이 있어요. 심리학에서는 계획 오류라고 해요.</b>",
         "뷸러, 그리핀, 로스 연구진은 1994년, 졸업 논문을 쓰는 대학생 37명에게 논문을 끝내는 데 며칠이 걸릴지 물었어요.",
         "학생들의 예상은 평균 33.9일이었어요. 모든 일이 가장 잘 풀릴 때는 27.4일, 가장 안 풀릴 때도 48.6일이라고 했어요.",
         "실제로는 평균 55.5일이 걸렸어요. 가장 나쁜 경우로 잡은 날보다도 길었고, 예상 안에 끝낸 학생은 열 명 중 셋쯤이었어요.") + "[[B]]" + \
       P("일이 잘 풀리는 장면만 떠올리고, 지난번에 걸린 시간은 잘 꺼내 보지 않기 때문이에요.",
         "그래서 이사 준비는 지난 이사 때 실제로 걸린 날을 기준으로 잡는 편이 정확해요. 기억이 안 나면 처음 생각한 날에 절반을 더해 보세요.",
         '📚 <b>출처 1</b>: <a href="https://doi.org/10.1037/0022-3514.67.3.366">Buehler, Griffin &amp; Ross (1994), Exploring the planning fallacy, Journal of Personality and Social Psychology 67(3)</a>',
         '📚 <b>출처 2</b>: <a href="https://astro.kasi.re.kr/life/pageView/5">한국천문연구원 천문우주지식정보, 음양력 변환</a>') + \
       P("🌱 <b>마음 코치 정월의 질문</b>", "올해가 가기 전에<br>새집에서 가장 먼저 하고 싶은 일은 무엇인가요?",
         "🔸 지난 이사에서 가장 오래 걸렸던 일은<br>무엇이었나요?") + \
       P("✔️ <b>12월 이사를 앞두고 해 볼 것</b>",
         "1. 지도 앱으로 지금 집에서 새집이 어느 쪽인지 먼저 보세요.",
         "2. 손없는날 하나와 방향이 맞는 주말 하나, 후보 두 날을 정해 두세요.",
         "3. 지난 이사 때 걸린 날을 떠올려, 준비 시작일을 그만큼 앞당겨 적어 두세요.")
sec6 = P("<b>Q. 12월 주말에 손없는날은 며칠인가요?</b>",
         "A. 27일 일요일 하루예요. 토요일은 손없는날이 없어서, 토요일에 옮긴다면 방향을 보고 골라요.") + \
       P("<b>Q. 크리스마스(25일)에 이사해도 될까요?</b>",
         "A. 25일은 음력 11월 17일이라 손이 북쪽에 있어요. 새집이 북쪽이 아니면 방향으로는 걸리지 않아요. 다만 공휴일이라 업체 일정부터 물어보세요.") + \
       P("<b>Q. 2027년 1월 손없는날도 알려 주세요.</b>",
         "A. 2027년 1월 손없는날은 6일(수), 7일(목), 16일(토), 17일(일), 26일(화), 27일(수)이에요. 주말 손없는날이 16일·17일 이틀 있어요.") + \
       P("<b>Q. 손없는날이면 무엇이든 잘되는 날인가요?</b>",
         "A. 손이 없다는 뜻이지 일이 저절로 풀린다는 뜻은 아니에요. 잔금일과 입주일이 맞는지가 먼저예요.") + \
       P("<b>Q. 앱마다 손없는날이 다르게 나와요. 왜 그럴까요?</b>",
         "A. 손없는날은 음력 날짜 끝자리(9·0)로 정해서 어느 앱이든 같아야 해요. 다르게 보이면 길일을 고르는 다른 방법(황도·흑도 같은 택일법)을 같이 적은 경우일 수 있어요. 이 글은 음력 끝자리 하나만 썼어요.")
tail = P("여러분은 12월에 이사나 결혼, 개업을 앞두고 있나요?", "고른 날짜나 아직 고민 중인 두 날을 댓글에 적어 주세요.") + \
       '<p><b>👇 2027년 이사를 앞두고 삼재가 마음에 걸린다면, 2027 삼재띠 언제 끝날까, 돼지띠 토끼띠 양띠 날삼재 날짜</b></p>'
secs = [sec1, sec2, sec2b, sec3, sec4, sec5, sec6]

def _have(n): return os.path.exists(os.path.join(HERE, "img", n))
def build():
    for d_ in ("wide", "m1280", "master"): os.makedirs(os.path.join(HERE, "img", d_), exist_ok=True)
    c = V.Ctx(PAL); made = []
    a4 = f"wide/naver_z{KEY}_a4.jpg"
    if not _have(a4):
        V.render(PID + "_new", {"d": "N", "el": "물", "kick": "2026년 12월 손없는날", "hook": ["주말은", "27일 하루"], "sub": "토요일은 방향으로",
                                "items": ["7·8일", "17·18일", "27·28일"]}, os.path.join(HERE, "img", a4), PAL)
    made.append(a4)
    nm = {"K": f"naver_z{KEY}_k3.jpg", "G": f"naver_z{KEY}_g3.jpg", "C": f"naver_z{KEY}_c3.jpg", "B": f"naver_z{KEY}_v3.jpg"}
    if not _have(nm["K"]):
        DG.calendar(nm["K"], c, "2026년 12월 손없는날", [(2026, 12, set(SON))], note="색 칸은 손없는날(7일은 대설과 같은 날), 테두리는 동지 22일", ring={12: {22}})
    if not _have(nm["G"]):
        DG.compass(nm["G"], c, "12월 주말, 손이 있는 쪽", {"북": "5·6·26일", "동": "19·20일", "남": "12일(토)", "서": "13일(일)"},
                   ("27일(일)", "손 없음"), "방향은 지금 집에서 새집을 바라본 쪽이에요")
    if not _have(nm["C"]):
        DGB.checklist(nm["C"], c, "12월 이사 세 칸", [("잔금일과 입주일 맞추기", "계약서 두 장의 날짜를 나란히"),
                                                   ("이삿짐 업체 두 곳에 같은 날 견적", "27·28일은 일찍 차요"),
                                                   ("이사한 날부터 14일 안에 전입신고", "전세라면 확정일자도 같은 날")])
    if not _have(nm["B"]):
        DGC.vbar(nm["B"], c, "졸업 논문, 며칠 걸릴까", [("가장 잘 풀릴 때", 27.4, False), ("평균 예상", 33.9, False), ("가장 안 풀릴 때", 48.6, False), ("실제", 55.5, True)],
                 60, "실제 걸린 날은 가장 나쁜 예상보다도 길었어요", "Buehler, Griffin & Ross (1994) 연구 1 · 대학생 37명", fmt="{:.1f}일", step=10)
    import fullbleed as FBL
    plan_p = os.path.join(HERE, "fullbleed_plan.json"); plan = json.load(open(plan_p, encoding="utf-8")) if os.path.exists(plan_p) else {}
    rows = []
    for pos, k in enumerate("KGCB", 1):
        f = nm[k][:-4] + "f.jpg"
        if not _have(f):
            r, why = FBL.convert(nm[k], [os.path.join(HERE, "img"), os.path.join(HERE, "img", "m1280")])
            if not r: print("fullbleed 건너뜀", nm[k], why); made.append(nm[k]); continue
        rows.append({"pos": pos, "old": nm[k], "new": f}); made.append(nm[k]); nm[k] = f
        reg_ = json.load(open(DG.REG, encoding="utf-8")); reg_[f] = reg_[rows[-1]["old"]]; json.dump(dict(sorted(reg_.items())), open(DG.REG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    plan[PID] = rows; json.dump(plan, open(plan_p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    made += [v for v in nm.values() if v not in made]
    alt = {"K": "2026년 12월 달력 그림. 손없는날 7일, 8일, 17일, 18일, 27일, 28일에 색, 동지 22일에 테두리",
           "G": "12월 주말 손 방향 그림. 북쪽 5일·6일·26일, 동쪽 19일·20일, 남쪽 12일, 서쪽 13일, 27일은 손 없음",
           "C": "12월 이사 세 칸 체크 그림. 잔금일과 입주일 맞추기, 업체 두 곳 견적, 14일 안에 전입신고",
           "B": "계획 오류 연구 그림. 졸업 논문 예상 최선 27.4일, 평균 33.9일, 최악 48.6일, 실제 55.5일"}
    body = P(*head) + P("<b>📌 12월 손없는날을 고르는 길</b>", *[f"{i + 1}. {q}" for i, q in enumerate(toc_q)])
    for i, (q, s) in enumerate(zip(toc_q, secs)):
        for k in "KGCB": s = s.replace(f"[[{k}]]", IMG(nm[k], alt[k]))
        body += H(f"{i + 1}. {q}") + s
    body += tail + CTA
    import copy_rules as CR
    for w in ("재미로", "상담", "—", "안녕하세요, 자오선의 정월이에요", "결론부터 말씀드릴게요", "생년월일만 넣으면 1초", "한 줄 요약", "이 글의 순서", "수비학으로 겹쳐 보면",
              "총정리", "여섯 운명학으로 넓혀 보면", "기준점 효과", "힘 쓸 달", "아낄 달") + tuple(CR.금지어):
        assert w not in re.sub(r"<[^>]+>", " ", body), w
    for f in made:   # 사이트 사본(K-069)
        dst = os.path.join(SITE, "public", "naver", "img", f); os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy(os.path.join(HERE, "img", f), dst)
    return body, a4, made

TITLE = "2026년 12월 손없는날, 이사·결혼·개업 날짜 한눈에"
TAGS = ["12월손없는날", "2026년12월손없는날", "손없는날", "12월이사손없는날", "손없는날결혼", "손없는날개업", "이사날짜", "1월손없는날", "대설", "자오선"]
REL = {"id": "n81", "title": "2027 삼재띠 언제 끝날까, 돼지띠 토끼띠 양띠 날삼재 날짜",
       "phrase": "2027년 이사를 앞두고 삼재가 마음에 걸린다면, 2027 삼재띠 언제 끝날까, 돼지띠 토끼띠 양띠 날삼재 날짜",
       "url": "https://blog.naver.com/zaoseon/224462303163"}
_KV = json.load(open(os.path.join(SITE, "data", "keywords", "kw_volume.json"), encoding="utf-8"))["posts"]["plan_손없는날"]
_KU = json.load(open(os.path.join(SITE, "data", "keywords", "kw_volume.json"), encoding="utf-8"))["posts"]["son_uses_1118"]["씨앗"]
KW_VOL = {"손없는날결혼": _KU["손없는날결혼"], "손없는날개업": _KU["손없는날개업"], "12월손없는날": _KV["씨앗"]["12월손없는날"], "12월이사손없는날": _KV["씨앗"]["12월이사손없는날"], "손없는날": _KV["연관상위"]["손없는날"], "1월손없는날": _KV["씨앗"]["1월손없는날"]}
INTENT = {"keywords": ["12월손없는날", "손없는날", "12월이사손없는날", "손없는날결혼"],
          "keyword_src": "kw-volume 작업(data/keywords/kw_volume.json posts.plan_손없는날·son_uses_1118, 11/18) 월 검색량 · 콘텐츠 계획 11/21~12/13 3절 · 커뮤니티 질문 data/kcos_community/zaoseon/2026-11-18.json",
          "intent": "날짜를 찾는다", "intent_note": "12월 손없는날 날짜·요일을 바로 보고, 이사 말고 결혼·개업·계약·입주에도 쓰는지, 주말이면 방향으로 고르는 법, 연말 서류(전입신고), 1월 날짜까지. 11/18 대표 지적으로 용도를 넓힘(검색자 대부분이 '이사'를 안 붙임: 12월손없는날 10,330 vs 12월이사손없는날 1,820)",
          "first3": "2026년 12월 손없는날은 7일(월), 8일(화), 17일(목), 18일(금), 27일(일), 28일(월)로 모두 여섯 번이에요.",
          "answer_keys": ["12월 손없는날 6일", "이사·결혼·개업·계약·입주 모두", "주말은 27일 하나", "토요일은 방향"],
          "community_q": ["이사 택일 황흑도법이 사주 앱마다 다르게 표기될 수 있나요(지식iN, 11/18 수집)"],
          "order": toc_q, "images": ["12월 달력(calendar, 음력 변환)", "주말 손 방향(compass)", "12월 이사 세 칸(checklist)", "계획 오류 연구(vbar)"],
          "related": "n81", "cta": PID, "experience": [], "applied": True,
          "differs_from_n60": "미발행 n60(11월)의 인사·'결론부터'·한 줄 요약 줄·여섯 운명학 단락·기준점 효과 대신 주말 손 방향 표·대설/동지·전입신고 14일·1월 날짜·계획 오류(Buehler 외 1994)·그림 유형(calendar·compass·checklist·vbar)"}

if __name__ == "__main__":
    body, a4, made = build()
    reg = json.load(open(MP.REG, encoding="utf-8"))
    assert PID not in reg or not reg[PID].get("done"), "이미 예약 끝난 글"
    reg[PID] = dict(dt="2027-02-05T08:00:00", dt_tbd="CT가 정함(콘텐츠 계획 11/23 칸). 이 날짜는 자리값", title=TITLE, tags=TAGS, body=body,
                    cover=a4, related=REL, thumbs=None, cid=None, clips=None, category="절기 이야기", done=False, kw_vol=KW_VOL,
                    k131="n94 11/17(K-151 새 글)", source="build_naver_94.py (콘텐츠 계획 새 글)")
    json.dump(reg, open(MP.REG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    ic = json.load(open(os.path.join(HERE, "intent_cards.json"), encoding="utf-8")); ic["cards"][PID] = INTENT
    json.dump(ic, open(os.path.join(HERE, "intent_cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    v = reg[PID]
    MP.write_page(PID, D.datetime.fromisoformat(v["dt"]), v["title"], v["tags"], v["body"], None, v["cover"], v["related"], v["category"])
    MP.write_index()
    import k151_check as K
    print(PID, len(TITLE), "자 제목 · 본문 글자", len(re.sub(r"<[^>]+>|&nbsp;", "", body)), "· 사진", made, "· K 검사", K.check(PID, v))
