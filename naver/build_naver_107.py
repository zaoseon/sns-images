"""네이버 n107: 2026년 동지 새 글 (CT 11/21 새 글 1편 시험 — 계획 표 12/12 '2026 동지' 칸, 주제 은행 6번).
- 왜: 검색량 동지 67,600 · 동짓날 9,200 · 2026동지 3,270 · 동지팥죽 2,030(kw_volume plan_동지). 자오선 글 중 동지를 다룬 글은 없고(n94 는 12월 손없는날에서 동지 22일을 한 줄 언급),
  주제 은행은 '날짜·시각 정보형, 운세는 끝에 짧게'(동지운세 10)로 정함. 그래서 날짜·시각 → 애동지·중동지·노동지 → 팥죽 → 사주에서 동지(子월) → 겨울 마음 순서.
- 출처 2개(K-162, 11/21 확인): 한국민속대백과사전 '동지'(E0016784: 24절기 22번째·황경 270°·밤이 가장 긴 날·아세/작은 설·애동지/중동지/노동지·애동지엔 팥죽을 쑤지 않음·팥은 양색이라 음귀를 쫓음)
  · Rosenthal et al. (1984) Archives of General Psychiatry 41(1) 72-80, DOI 10.1001/archpsyc.1984.01790120076010 (초록: 29명 · 예비 시험 11명, Europe PMC 에서 확인).
  백과사전 본문에 '팥시루떡 대체'·'새알심 나이 수'는 없어서 글에 쓰지 않았다.
- 계산(engine·ephem assert): 동지 시각 = 태양 황경 270°(engine 의 절기 찾기), 서울 낮 길이 = ephem 해 뜨고 짐(고도 0, 대기굴절 포함), 음력 = korean_lunar_calendar, 사주 달 = engine.
- 날짜: CT가 정한다. pages.json dt 는 자리값, dt_tbd 로 표시.
사용: SITE=<zaoseon-site> python3 naver/build_naver_107.py"""
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
       '<tr><td style="padding:12px 10px;text-align:center;border:1px solid #d0d0d0"><b>동지 말고 내 사주 여덟 글자가 궁금하다면</b></td></tr>'
       '<tr><td style="padding:12px 10px;text-align:center;border:1px solid #d0d0d0"><span style="color:#9a9a9a">[ 1996 . 12 . 21 ]</span></td></tr>'
       '<tr><td style="padding:12px 10px;text-align:center;border:1px solid #d0d0d0"><b><a href="https://zaoseon.com/?utm_source=naver&amp;utm_medium=mid#free">내 태어난 날 글자 보기 →</a></b></td></tr>'
       '</tbody></table>' + BL)
CTA = ('<p><a href="https://zaoseon.com/?utm_source=naver&utm_medium=cta#free"><img src="' + RAW +
       'naver_cta5_1%EC%B4%88%EB%AC%B4%EB%A3%8C%ED%92%80%EC%9D%B4.jpg" alt="자오선 무료 1초 풀이 안내 배너"></a></p>')
PID, KEY, PAL = "n107", "107", "p_red_s"   # 팥의 붉은색 → 붉은 판. 최근 n105 p_black_s · n104 m_young_s · n103 k_neon_s · n102 g_ivory_s 와 다른 판

# ───────── 계산값과 검산
import datetime as D, ephem
sys.path.insert(0, os.path.join(SITE, "engine")); import engine as E
from korean_lunar_calendar import KoreanLunarCalendar as KLC
KST = E.KST
def kst_of(t):
    return (t if hasattr(t, "astimezone") else E.ephem.Date(t).datetime().replace(tzinfo=D.timezone.utc)).astimezone(KST)
def dongji(y): return kst_of(E._find_term_time(y, 270.0))      # 태양 황경 270° = 동지
def lunar(dt):
    c = KLC(); c.setSolarDate(dt.year, dt.month, dt.day); assert not c.isIntercalation; return c.lunarYear, c.lunarMonth, c.lunarDay
def kind(day): return "애동지" if day <= 10 else ("중동지" if day <= 20 else "노동지")   # 흔히 쓰는 구분: 음력 11월 초순·중순·하순
DJ = {y: dongji(y) for y in range(2025, 2030)}
D26 = DJ[2026]
assert (D26.month, D26.day, D26.hour, D26.minute) == (12, 22, 5, 50), D26
assert D26.weekday() == 1                                                    # 화요일
assert lunar(D26)[1:] == (11, 14) and kind(14) == "중동지"
ROW = []
for y, (mo, da, hh, mm, kd) in {2025: (12, 22, 0, 3, "애동지"), 2026: (12, 22, 5, 50, "중동지"), 2027: (12, 22, 11, 42, "노동지"),
                                2028: (12, 21, 17, 19, "애동지"), 2029: (12, 21, 23, 14, "중동지")}.items():
    t = DJ[y]; assert (t.month, t.day, t.hour, t.minute) == (mo, da, hh, mm), (y, t)
    lm, ld = lunar(t)[1:]; assert lm == 11 and kind(ld) == kd, (y, lm, ld)
    ROW.append((f"{y}년", f"{mo}월 {da}일 {hh}시 {mm:02d}분", f"음력 11월 {ld}일 · {kd}"))
# 대설·소한(사주 子월의 처음과 끝)
T26 = dict((n, t) for n, _, t in E.get_solar_terms_kst(2026)); T27 = dict((n, t) for n, _, t in E.get_solar_terms_kst(2027))
DS, SH = T26["대설"], T27["소한"]
assert (DS.month, DS.day, DS.hour, DS.minute) == (12, 7, 11, 52) and (SH.month, SH.day, SH.hour, SH.minute) == (1, 5, 23, 9)
# 서울 낮 길이(해 뜨고 짐, 표준: 윗가장자리·대기굴절 포함)
def daylen(y, m, d):
    o = ephem.Observer(); o.lat, o.lon, o.elevation, o.pressure, o.horizon = "37.5665", "126.9780", 38, 1010, "0"
    o.date = ephem.Date(f"{y}/{m}/{d} 03:00:00"); s = ephem.Sun(); r, st = o.previous_rising(s), o.next_setting(s)
    kr = lambda x: ephem.Date(x).datetime() + D.timedelta(hours=9)
    return kr(r), kr(st), round((ephem.Date(st) - ephem.Date(r)) * 24 * 60)
RS, SS, LEN_D = daylen(2026, 12, 22); _, _, LEN_C = daylen(2026, 3, 20); _, _, LEN_H = daylen(2026, 6, 21)
assert (RS.strftime("%H:%M"), SS.strftime("%H:%M")) == ("07:43", "17:17") and (LEN_D, LEN_C, LEN_H) == (575, 728, 886), (RS, SS, LEN_D, LEN_C, LEN_H)   # 9시간 35분 근사, 12시간 8분, 14시간 46분
assert LEN_D // 60 == 9 and LEN_D % 60 == 35 and LEN_H // 60 == 14 and LEN_H % 60 == 46 and (LEN_H - LEN_D) == 311      # 하지가 5시간 11분 더 길다
# 사주 예시: 1996.12.21 오전 10시 (그해 동지는 같은 날 23:05)
EX = E.compute_saju(D.datetime(1996, 12, 21, 10))["팔자"]
assert (EX["년주"], EX["월주"], EX["일주"], EX["시주"]) == ("丙子", "庚子", "壬辰", "乙巳"), EX
d96 = dongji(1996); assert (d96.month, d96.day, d96.hour, d96.minute) == (12, 21, 23, 5)
assert E.compute_saju(D.datetime(1996, 12, 21, 23, 30))["팔자"]["월주"] == "庚子"                                          # 동지 시각 뒤에 태어나도 같은 달
T96 = dict((n, t) for n, _, t in E.get_solar_terms_kst(1996)); assert (T96["대설"].month, T96["대설"].day) == (12, 7)
# 해마다 12/21~22
assert all(DJ[y].day in (21, 22) for y in DJ)
print("동지 2026", D26.strftime("%m-%d %H:%M"), "· 음력 11/14 중동지 · 대설", DS.strftime("%m-%d %H:%M"), "· 소한", SH.strftime("%Y-%m-%d %H:%M"),
      "· 서울 낮", RS.strftime("%H:%M"), SS.strftime("%H:%M"), LEN_D, "분 · 예시", EX)

# ───────── 본문 (11/21 다시 쓰기: 출처·검증 범위 문장은 본문에서 빼고 링크만 말 속에 건다)
ENC = "https://encykorea.aks.ac.kr/Article/E0016784"
ROS = "https://doi.org/10.1001/archpsyc.1984.01790120076010"
head = ["<b>12월 22일 오전 5시 50분, 올해 동지는 팥죽 쑤는 중동지예요.</b>",
        f"음력 11월 14일에 들어서 애동지도 노동지도 아니거든요. 애동지에는 팥죽을 쑤지 않는다는 <a href=\"{ENC}\">옛 풍속</a>이 있는데, 올해는 그런 걱정 없이 새알심까지 넣어 끓여도 돼요.",
        "동지는 일 년 중 밤이 가장 길고 낮이 가장 짧은 날이에요. 그런데 그 긴 밤에 왜 하필 팥죽을 먹을까요? 하나씩 풀어 볼게요."]
toc_q = ["동지는 어떤 날일까요?", "2026년 동지는 언제일까요?", "애동지·중동지·노동지는 뭐가 다를까요?", "동지에는 왜 팥죽을 먹을까요?",
         "사주에서 동지는 어느 자리에 놓일까요?", "해가 짧은 겨울, 마음은 어떻게 달라질까요?"]
sec1 = P("<b>일 년 중 밤이 가장 길고 낮이 가장 짧은 날이에요. 24절기 가운데 스물두 번째 절기이고, 태양이 황경 270도에 닿는 때예요.</b>",
         f"서울에서 올해 동지의 해는 {RS:%H시 %M분}에 떠서 {SS:%H시 %M분}에 져요. 낮이 고작 {LEN_D // 60}시간 {LEN_D % 60}분인데, 하지 무렵 낮이 {LEN_H // 60}시간 {LEN_H % 60}분쯤이니 {(LEN_H - LEN_D) // 60}시간 {(LEN_H - LEN_D) % 60}분이나 짧은 거예요.") + "[[V]]" + \
       P(f"그래도 동지가 지나면 낮이 하루씩 길어져요. 그래서 옛사람들은 동지를 <a href=\"{ENC}\">작은 설</a>이라 부르며 설 다음가는 날로 챙겼어요.")
sec2 = P("<b>2026년 12월 22일 화요일 오전 5시 50분이에요.</b>",
         "동지는 날짜가 아니라 시각으로 정해져요. 태양이 황경 270도에 닿는 순간이 5시 50분이니까 그 순간이 든 22일이 동짓날이에요.") + "[[C]]" + \
       P("해마다 12월 21일이나 22일에 들어오는데, 시각이 자정 근처면 달력 날짜가 하루 달라져요. 2025년은 22일 0시 3분, 2028년은 21일 17시 19분, 2029년은 21일 23시 14분이에요.")
sec3 = P("<b>동지가 음력 11월 며칠에 드느냐의 차이예요. 1~10일이면 애동지, 11~20일이면 중동지, 21일부터는 노동지예요.</b>",
         "올해는 음력 11월 14일이라 중동지예요. 2027년은 11월 25일이라 노동지고, 2028년은 11월 6일이라 애동지예요. 팥죽은 올해와 내년엔 마음 편히 쑤고, 2028년에만 애동지 풍속을 떠올려 보세요.") + "[[T]]"
sec4 = P("<b>팥이 붉은 양의 색이라서 어둡고 음한 귀신을 쫓는다고 믿었기 때문이에요.</b>",
         "밤이 가장 길어 어둠이 제일 깊은 날에, 제일 붉은 음식을 끓여 식구끼리 나눠 먹은 거예요. 죽에 넣는 새알심은 단자를 새알만 하게 빚어서 붙은 이름이고요.",
         "'동지팥죽을 먹어야 진짜 한 살 더 먹는다'는 말도 전해지는데, 동지가 작은 설이라 불린 까닭과 이어지는 말이에요.")
sec5 = P("<b>동지는 사주의 달을 바꾸는 날이 아니에요. 子월 한가운데에 놓인 날이에요.</b>",
         "사주의 달은 24절기 중 열두 절로 나누는데, 동지는 그 사이에 낀 절기라 달이 바뀌지 않아요. 2026년 子월은 12월 7일 11시 52분 대설에 시작해서 2027년 1월 5일 23시 09분 소한 전까지이고, 동지 22일은 그 안에 쏙 들어와요.") + \
       P("🔎 예를 들어 1996년 12월 21일 오전 10시에 태어난 사람이 있어요. 그해 동지는 같은 날 밤 11시 5분이라 동지가 되기 열세 시간쯤 앞서 태어났는데도, 사주는 丙子년 庚子월 壬辰일 乙巳시예요. 달 글자는 대설에 시작한 子 그대로예요.",
         "밤 11시 30분에 태어난 사람도 똑같이 庚子월이에요. 동지 시각 앞뒤로 달이 갈리지 않거든요.") + MID
sec6 = P("<b>겨울에 해가 짧아지면 기분이 가라앉는 사람이 실제로 있어요.</b>",
         f"1984년 미국 연구팀이 <a href=\"{ROS}\">겨울마다 되풀이되는 우울</a>을 겪는 환자 29명을 정리했는데, 잠이 늘고 많이 먹고 탄수화물이 당기는 모습이 많았어요. 밝은 빛으로 낮 시간을 늘려 본 11명에게서는 우울이 덜어지는 모습이 보였고요.") + \
       P("그러니 겨울에 유독 무겁다면 의지가 약해서만은 아니에요. 동지는 그 어둠이 가장 깊은 날이면서 다음 날부터 해가 길어지는 첫날이기도 하니까, 올해는 해 있는 시간에 10분만 밖에 나가 보세요. 마음이 2주 넘게 계속 가라앉으면 전문가와 꼭 이야기해 보시고요.") + \
       P("🌱 <b>마음 코치 정월의 질문</b>", "올겨울,<br>해가 있는 시간에 나는 어디에 있나요?",
         "올해는 12월 22일 낮에 10분만 밖에서 해를 쬐어 보세요.")
tail = P("여러분은 올해 동지에 팥죽을 직접 쑤실 건가요, 사 드실 건가요?", "댓글에 '직접'이나 '사 먹기' 한 마디만 남겨 주세요.") + \
       '<p><b>👇 입동 전에 태어나면 사주의 달이 어떻게 달라지는지 궁금하다면, 입동 뜻과 2026년 입동 날짜, 입동 전에 태어나면 사주의 달이 달라요</b></p>'
secs = [sec1, sec2, sec3, sec4, sec5, sec6]

def _have(n): return os.path.exists(os.path.join(HERE, "img", n))
def build():
    for d_ in ("wide", "m1280", "master"): os.makedirs(os.path.join(HERE, "img", d_), exist_ok=True)
    c = V.Ctx(PAL); made = []
    a4 = f"wide/naver_z{KEY}_a1.jpg"
    if not _have(a4):
        V.render(PID + "_new", {"d": "N", "el": "물", "kick": "2026년 동지", "hook": ["12월 22일", "오전 5시 50분"], "sub": "중동지 팥죽 풍속과 사주 달",
                                "items": ["날짜", "구분", "팥죽"]}, os.path.join(HERE, "img", a4), PAL)
    made.append(a4)
    nm = {"V": f"naver_z{KEY}_v1.jpg", "C": f"naver_z{KEY}_c1.jpg", "T": f"naver_z{KEY}_t1.jpg"}
    if not _have(nm["V"]):
        DGC.vbar(nm["V"], c, "서울 낮 길이, 동지는 얼마나 짧을까", [("동지 12/22", round(LEN_D / 60, 1), True), ("춘분 3/20", round(LEN_C / 60, 1), False), ("하지 6/21", round(LEN_H / 60, 1), False)],
                 16, f"동지 낮은 하지보다 {(LEN_H - LEN_D) // 60}시간 {(LEN_H - LEN_D) % 60}분 짧아요", "2026년 서울 해 뜨고 짐 계산값(시간)", fmt="{:.1f}", step=4)
    if not _have(nm["C"]):
        DG.calendar(nm["C"], c, "2026년 12월 동지", [(2026, 12, {22})], note="색 칸은 동지 22일 오전 5시 50분, 테두리는 대설 7일", ring={12: {7}})
    if not _have(nm["T"]):
        DGC.compare(nm["T"], c, "2025~2029년 동지 날짜와 구분", ("동지 시각", "음력과 구분"), ROW,
                    "음력 11월 1~10일 애동지 · 11~20일 중동지 · 21일부터 노동지", hi=1)
    import fullbleed as FBL
    plan_p = os.path.join(HERE, "fullbleed_plan.json"); plan = json.load(open(plan_p, encoding="utf-8")) if os.path.exists(plan_p) else {}
    rows = []
    for pos, k in enumerate("VCT", 1):
        f = nm[k][:-4] + "f.jpg"
        if not _have(f):
            r, why = FBL.convert(nm[k], [os.path.join(HERE, "img"), os.path.join(HERE, "img", "m1280")])
            if not r: print("fullbleed 건너뜀", nm[k], why); made.append(nm[k]); continue
        rows.append({"pos": pos, "old": nm[k], "new": f}); made.append(nm[k]); nm[k] = f
        reg_ = json.load(open(DG.REG, encoding="utf-8")); reg_[f] = reg_[rows[-1]["old"]]; json.dump(dict(sorted(reg_.items())), open(DG.REG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    plan[PID] = rows; json.dump(plan, open(plan_p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    made += [v for v in nm.values() if v not in made]
    alt = {"V": f"2026년 서울 낮 길이 막대 그림. 동지 {LEN_D // 60}시간 {LEN_D % 60}분, 춘분 {LEN_C // 60}시간 {LEN_C % 60}분, 하지 {LEN_H // 60}시간 {LEN_H % 60}분이에요",
           "C": "2026년 12월 달력 그림. 동지는 22일 오전 5시 50분, 대설은 7일이에요",
           "T": "2025년부터 2029년까지 동지 날짜와 시각, 음력 날짜, 애동지·중동지·노동지 구분 표예요"}
    body = P(*head)
    for i, (q, s) in enumerate(zip(toc_q, secs)):
        for k in "VCT": s = s.replace(f"[[{k}]]", IMG(nm[k], alt[k]))
        body += H(f"{i + 1}. {q}") + s
    body += tail + CTA
    import copy_rules as CR
    for w in ("재미로", "상담", "—", "안녕하세요, 자오선의 정월이에요", "결론부터 말씀드릴게요", "생년월일만 넣으면 1초", "한 줄 요약", "이 글의 순서", "수비학",
              "총정리", "기운", "흐름", "편이에요", "누르", "누른", "결") + tuple(CR.금지어):
        assert w not in re.sub(r"<[^>]+>", " ", body), w
    for f in made:   # 사이트 사본(K-069)
        dst = os.path.join(SITE, "public", "naver", "img", f); os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy(os.path.join(HERE, "img", f), dst)
    return body, a4, made

TITLE = "2026년 동지 날짜와 시각, 애동지 중동지 노동지 구분"
TAGS = ["동지", "2026동지", "동짓날", "동지팥죽", "애동지", "중동지", "동지시각", "대설", "사주월", "자오선"]
REL = {"id": "n63", "title": "입동 뜻과 2026년 입동 날짜, 입동 전에 태어나면 사주의 달이 달라요",
       "phrase": "입동 전에 태어나면 사주의 달이 어떻게 달라지는지 궁금하다면, 입동 뜻과 2026년 입동 날짜, 입동 전에 태어나면 사주의 달이 달라요",
       "url": "https://blog.naver.com/zaoseon/224447866334"}
KW_VOL = (json.load(open(os.path.join(SITE, "data", "keywords", "kw_volume.json"), encoding="utf-8"))["posts"].get("plan_동지") or {}).get("씨앗") or {}
assert KW_VOL.get("동지", 0) >= 100, KW_VOL
INTENT = {"keywords": ["동지", "2026동지", "동짓날", "동지팥죽"],
          "keyword_src": "kw-volume plan_동지 씨앗(동지 67,600·동짓날 9,200·2026동지 3,270·동지팥죽 2,030·동지운세 10) · 주제 은행 6번(data/topics/topic_bank.md)",
          "intent": "날짜·시각을 알고 싶다", "intent_note": "2026년 동지가 언제(날짜·시각)인지, 애동지·중동지·노동지 중 무엇인지, 팥죽을 먹는 까닭, 사주와는 어떻게 이어지는지",
          "first3": "12월 22일 오전 5시 50분, 올해 동지는 팥죽 쑤는 중동지예요. 음력 11월 14일에 들어서 애동지도 노동지도 아니거든요. 동지는 일 년 중 밤이 가장 길고 낮이 가장 짧은 날이에요.",
          "answer_keys": ["동지 12/22 05:50", "음력 11/14 중동지", "팥은 붉은 양색, 음귀를 쫓음(백과)", "사주 달은 대설에 시작하는 子월, 동지는 중기"],
          "community_q": [], "order": toc_q, "images": ["서울 낮 길이 동지·춘분·하지(vbar)", "2026년 12월 달력(calendar)", "2025~2029 동지 날짜·구분(compare)"],
          "related": "n63", "cta": PID, "experience": [], "applied": True}

if __name__ == "__main__":
    body, a4, made = build()
    reg = json.load(open(MP.REG, encoding="utf-8"))
    assert PID not in reg or not reg[PID].get("done"), "이미 예약 끝난 글"
    reg[PID] = dict(dt="2026-12-12T08:00:00", dt_tbd="CT가 정함(계획 표 12/12 '2026 동지' 칸 자리값). 대기표에는 넣지 않음", title=TITLE, tags=TAGS, body=body,
                    cover=a4, related=REL, thumbs=None, cid=None, clips=None, category="절기 이야기", done=False, kw_vol=KW_VOL,
                    k131="n107 11/21(K-151 새 글, 시험)", source="build_naver_107.py (새 글 1편 시험, 동지)")
    json.dump(reg, open(MP.REG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    ic = json.load(open(os.path.join(HERE, "intent_cards.json"), encoding="utf-8")); ic["cards"][PID] = INTENT
    json.dump(ic, open(os.path.join(HERE, "intent_cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    v = reg[PID]
    MP.write_page(PID, D.datetime.fromisoformat(v["dt"]), v["title"], v["tags"], v["body"], None, v["cover"], v["related"], v["category"])
    MP.write_index()
    import k151_check as K
    print(PID, len(TITLE), "자 제목 · 본문 글자", len(re.sub(r"<[^>]+>|&nbsp;", "", body)), "· 사진", made, "· K 검사", K.check(PID, v))
