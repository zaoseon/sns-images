"""네이버 n97: 별자리 운세 보는 법 새 글 (CT 11/4 19:40 재발행 일정 '새 글로 다시 쓰기' n51 → n97, 진행표 docs/네이버_누락글_진행표_2026-11-18.md 넷째 줄).
- 왜: 검색에 다른 우리 글만 잡히는 옛 글 n51(별자리 운세 제대로 보는 법, 내 별자리 원소와 12별자리 생일 한눈에)을 새 글로. n51은 건드리지 않는다(K-147·K-178).
- 검색어: 별자리운세 871,700(kw_volume 기존 묶음). n97 묶음(별자리운세·내별자리·별자리원소·12별자리날짜·별자리생일)은 11/19 ① 요청 — 결과가 오면 KW_VOL 이 채워진다.
- 다르게 쓴 것(K-151): n51의 인사·'결론부터'·한 줄 요약·원소 4무리·양태 3가지·2027 느린 별·확증 편향(Nickerson)·포러 실험·여섯 운명학 대신
  경계 시각이 해마다 몇 시간씩 바뀌는 이유(태양 황경 30° 넘는 시각, swisseph 계산 assert), 2026·2027 경계 시각 표, 별자리 경계 = 24절기 중기(춘분·곡우…),
  같은 10월 23일생도 해마다 별자리가 다른 예, 읽는 순서(태양 → 달 약 2.5일 → 상승 약 2시간). 심리 대신 조사 숫자 = Pew 2025(미국 성인 9,593명, 28%가 한 해 한 번 이상 별자리·운세를 봄).
  그림 유형 bignum·compare·ladder. 연결글 → n82(노출 '예').
- 출처 2개(K-162, 11/19 원문 확인): Pew Research Center (2025.5.21) 3 in 10 Americans consult astrology, tarot cards or fortune tellers — 2024.10.21~27, 9,593명, 별자리·운세 28% ·
  한국천문연구원 천문우주지식정보 음양력 변환(절기 시각).
- 날짜: CT가 정한다. pages.json dt 는 자리값, dt_tbd 로 표시.
사용: SITE=<zaoseon-site> python3 naver/build_naver_97.py"""
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
       '<tr><td style="padding:12px 10px;text-align:center;border:1px solid #d0d0d0"><b>경계 날짜에 태어났다면 시각까지 넣어 보세요</b></td></tr>'
       '<tr><td style="padding:12px 10px;text-align:center;border:1px solid #d0d0d0"><span style="color:#9a9a9a">[ 1996 . 10 . 23 ]</span></td></tr>'
       '<tr><td style="padding:12px 10px;text-align:center;border:1px solid #d0d0d0"><b><a href="https://zaoseon.com/?utm_source=naver&amp;utm_medium=mid#free">내 별자리와 띠 같이 보기 →</a></b></td></tr>'
       '</tbody></table>' + BL)
CTA = ('<p><a href="https://zaoseon.com/?utm_source=naver&utm_medium=cta#free"><img src="' + RAW +
       'naver_cta5_1%EC%B4%88%EB%AC%B4%EB%A3%8C%ED%92%80%EC%9D%B4.jpg" alt="자오선 무료 1초 풀이 안내 배너"></a></p>')
PID, KEY, PAL = "n97", "97", "m_young_s"   # 별 = 하늘·물 판 묶음(EL_SET 물). n96 y_pink_s · n95 y_olive_s · n94 p_purple_s · n93 y_black_d 와 다른 판

# ───────── 계산값과 검산 (태양 황경 30°마다 넘는 시각, 한국 시각)
import datetime as D
import swisseph as swe
def _lon(dt):
    return swe.calc_ut(swe.julday(dt.year, dt.month, dt.day, dt.hour + dt.minute / 60 + dt.second / 3600), swe.SUN)[0][0]
def ingress(deg, start):
    f = lambda t: ((_lon(t) - deg + 180) % 360) - 180
    t = start
    while f(t) < 0: t += D.timedelta(hours=6)
    a, b = t - D.timedelta(hours=6), t
    for _ in range(40):
        m = a + (b - a) / 2
        if f(m) < 0: a = m
        else: b = m
    return b + D.timedelta(hours=9)
SIGNS = ["양자리", "황소자리", "쌍둥이자리", "게자리", "사자자리", "처녀자리", "천칭자리", "전갈자리", "사수자리", "염소자리", "물병자리", "물고기자리"]
JQ = ["춘분", "곡우", "소만", "하지", "대서", "처서", "추분", "상강", "소설", "동지", "대한", "우수"]   # 태양 황경 0°,30°… = 24절기 중기
MON = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 1, 2]
IN = {y: {s: ingress(i * 30, D.datetime(y, MON[i], 10)) for i, s in enumerate(SIGNS)} for y in (2026, 2027)}
hm = lambda t: f"{t.month}월 {t.day}일 {t.hour}시 {t.minute}분"
assert hm(IN[2026]["전갈자리"]) == "10월 23일 18시 37분" and hm(IN[2027]["전갈자리"]) == "10월 24일 0시 32분"
assert hm(IN[2026]["양자리"]) == "3월 20일 23시 45분" and hm(IN[2027]["양자리"]) == "3월 21일 5시 24분"
assert hm(IN[2026]["사수자리"]) == "11월 22일 16시 23분" and hm(IN[2026]["염소자리"]) == "12월 22일 5시 50분"
# 이 해의 차이: 같은 경계가 2026→2027 약 5시간 40분~6시간 늦어진다(1년 ≈ 365.24일)
gaps = [(IN[2027][s] - IN[2026][s]).total_seconds() / 3600 - 365 * 24 for s in SIGNS]
assert all(5.4 < g < 6.1 for g in gaps), gaps
# 절기 중기와 같은 순간: engine 의 절기 표는 節만 있으니 swisseph 로 직접 — 동지 = 태양 황경 270°
assert IN[2026]["염소자리"].strftime("%m%d%H%M") == "12220550"
print("2026·2027 별자리 경계 24개 계산 · 10/23 경계 · 해마다 약 6시간 늦어짐 확인")
ROWS27 = [(s, JQ[i], IN[2027][s]) for i, s in enumerate(SIGNS)]

# ───────── 본문 (n51 문장을 옮기지 않았다)
head = ["<b>별자리 운세는 태어난 순간 태양이 지나던 하늘 칸으로 한 해와 한 달의 흐름을 읽는 풀이예요.</b>",
        "그래서 별자리 운세를 제대로 보려면 먼저 내 칸이 맞는지부터 봐야 해요. 12별자리 날짜는 해마다 몇 시간씩 바뀌어서, 경계 날짜에 태어난 사람은 흔히 보는 표와 다를 수 있어요.",
        "<b>같은 10월 23일생이라도 2026년에는 오후 6시 37분부터 전갈자리, 2027년에는 하루 종일 천칭자리예요.</b>",
        "이 글은 별자리 날짜가 바뀌는 이유, 2027년 12별자리 경계 시각, 운세를 읽는 순서까지 다뤄요."]
toc_q = ["별자리 운세는 무엇을 보고 읽을까요?", "12별자리 날짜는 왜 해마다 바뀔까요?", "별자리 경계와 절기는 같은 날일까요?",
         "별자리 운세는 어떤 순서로 읽을까요?", "운세를 읽고 나서 무엇을 해 볼까요?", "자주 묻는 질문"]
sec1 = P("🌌 <b>하늘에서 태양이 1년 동안 지나가는 길을 30도씩 12칸으로 나눈 것이 12별자리예요.</b>",
         "태어난 순간 태양이 어느 칸에 있었는지가 내 태양 별자리예요. 보통 '내 별자리'라고 말하는 것이 이거예요.",
         "별자리 운세를 챙겨 보는 사람은 생각보다 많아요. 미국 퓨 리서치 센터가 2024년 10월 성인 9,593명에게 물었더니, 28%가 한 해에 한 번 이상 별자리나 운세를 본다고 답했어요.") + "[[B]]" + \
       P("그만큼 많이 보는데도, 내 칸이 맞는지 확인하는 사람은 드물어요. 대부분 생일 표 한 장만 보고 정하거든요.",
         '📚 <b>출처 1</b>: <a href="https://www.pewresearch.org/religion/2025/05/21/3-in-10-americans-consult-astrology-tarot-cards-or-fortune-tellers/">Pew Research Center (2025), 3 in 10 Americans consult astrology, tarot cards or fortune tellers</a>')
sec2 = P("<b>12별자리 날짜가 해마다 바뀌는 건 1년이 딱 365일이 아니기 때문이에요.</b>",
         "태양이 하늘 길을 한 바퀴 도는 데는 약 365일 6시간이 걸려요. 그래서 같은 경계도 이듬해에는 6시간쯤 늦게 오고, 4년마다 윤일이 끼면서 다시 당겨져요.",
         f"예를 들어 전갈자리가 시작되는 순간은 2026년 {hm(IN[2026]['전갈자리'])}, 2027년 {hm(IN[2027]['전갈자리'])}이에요.") + "[[K]]" + \
       P("표에 '10월 23일부터 전갈자리'라고만 적혀 있으면, 2027년 10월 23일생은 전갈자리로 잘못 알기 쉬워요. 실제로는 그날 하루 종일 천칭자리예요.",
         "경계 날짜 앞뒤 하루에 태어났다면 태어난 시각까지 넣어서 확인해야 해요.") + MID
sec3 = P("<b>네, 같은 날이에요. 12별자리 경계는 24절기 가운데 12개 중기와 같은 순간이에요.</b>",
         "춘분은 태양이 하늘 길 0도에 오는 순간이고, 이때 양자리가 시작돼요. 그 뒤로 30도마다 절기 하나와 별자리 하나가 같이 바뀌어요.",
         "🗓️ <b>2027년 별자리가 시작되는 시각</b>(한국 시각)",
         *[f"{s} · {j} · {hm(t)}" for s, j, t in ROWS27[10:] + ROWS27[:10]]) + \
       P("그래서 사주에서 쓰는 절기 달력과 별자리 날짜는 같은 하늘을 다른 이름으로 부르는 셈이에요. 올해 11월 22일 소설에는 사수자리가, 12월 22일 동지에는 염소자리가 시작돼요.",
         '📚 <b>출처 2</b>: <a href="https://astro.kasi.re.kr/life/pageView/5">한국천문연구원 천문우주지식정보, 음양력 변환(절기 시각)</a>')
sec4 = P("<b>별자리 운세는 태양, 달, 상승 별자리 순서로 넓혀 가며 읽어요.</b>",
         "☀️ 태양 별자리는 생일만 있으면 나와요. 한 해 운세나 이번 달 운세는 보통 이 칸을 기준으로 써요.",
         "🌙 달은 한 칸을 2~3일이면 지나가요. 그래서 달 별자리는 태어난 날과 대략의 시각이 있어야 정확해요.",
         "⬆️ 상승 별자리는 태어난 순간 동쪽 지평선에 걸린 칸이에요. 평균 2시간쯤마다 바뀌어서 태어난 시각과 장소가 모두 필요해요.") + "[[C]]" + \
       P("곳마다 별자리 운세가 조금씩 다른 건 어느 칸을 기준으로 썼는지가 달라서예요. 태양 칸으로 쓴 글과 상승 칸으로 쓴 글은 같은 사람에게도 다른 말을 해요.")
sec5 = P("<b>운세 문장은 결과보다 질문으로 읽으면 쓸모가 커요.</b>",
         "'이번 달은 관계가 바빠진다'는 문장을 봤다면, 정말 바빠질지 맞히기보다 내가 지금 누구와의 관계에 마음을 쓰고 있는지 떠올려 보는 거예요.") + \
       P("🌱 <b>마음 코치 정월의 질문</b>", "이번 달 운세에서 눈에 걸린 문장 하나는<br>무엇이었나요?",
         "🔸 그 문장이 눈에 걸린 건<br>요즘 어떤 일 때문일까요?") + \
       P("✔️ <b>별자리 운세 볼 때 해 볼 것</b>",
         "1. 생일이 경계 날짜 앞뒤 하루라면, 태어난 해의 경계 시각을 찾아 내 칸이 맞는지 먼저 확인해 보세요.",
         "2. 운세를 읽을 때 태양 칸 기준인지, 상승 칸 기준인지 글 첫머리에서 확인해 보세요.",
         "3. 눈에 걸린 문장 하나를 이번 주에 해 볼 행동 하나로 바꿔 적어 보세요.")
sec6 = P("<b>Q. 별자리 운세 표마다 날짜가 하루씩 다른 건 왜인가요?</b>",
         "A. 경계 시각이 해마다 바뀌는데, 표는 여러 해를 하나로 묶어 '무렵' 날짜를 적기 때문이에요. 경계에서 하루 안쪽이라면 내가 태어난 해의 시각으로 봐야 해요.") + \
       P("<b>Q. 한국 시각으로 봐야 하나요?</b>",
         "A. 네. 경계 시각은 세계 어디서나 같은 순간이지만, 시계로 적으면 나라마다 날짜가 달라질 수 있어요. 한국에서 태어났다면 한국 시각 표로 보세요. 이 글의 시각은 모두 한국 시각이에요.") + \
       P("<b>Q. 별자리와 띠는 무엇이 다른가요?</b>",
         "A. 별자리는 태양이 지나는 칸이라 한 해 안에서 12번 바뀌고, 띠는 태어난 해로 정해져 12년마다 돌아와요. 띠는 설날이 아니라 입춘(2027년 2월 4일 오전 10시 46분)부터 바뀌어요.")
tail = P("여러분의 생일은 경계 날짜 근처인가요?", "내 별자리를 확인하고 댓글에 별자리 이름만 남겨 주세요.") + \
       '<p><b>👇 내 별자리가 물고기자리라면, 물고기자리 2027 운세, 해왕성 토성 떠난 해 달라지는 3가지</b></p>'
secs = [sec1, sec2, sec3, sec4, sec5, sec6]

def _have(n): return os.path.exists(os.path.join(HERE, "img", n))
def build():
    for d_ in ("wide", "m1280", "master"): os.makedirs(os.path.join(HERE, "img", d_), exist_ok=True)
    c = V.Ctx(PAL); made = []
    a4 = f"wide/naver_z{KEY}_a5.jpg"   # 표지 항목은 한글만(한자·기호는 글꼴에 없어 네모, 11/18 n96 a4)
    if not _have(a4):
        V.render(PID + "_new", {"d": "N", "el": "물", "kick": "별자리 운세 보는 법", "hook": ["내 별자리 날짜", "해마다 바뀌어요"], "sub": "2027년 12별자리 경계 시각까지",
                                "items": ["태양", "달", "상승"]}, os.path.join(HERE, "img", a4), PAL)
    made.append(a4)
    nm = {"B": f"naver_z{KEY}_n3.jpg", "K": f"naver_z{KEY}_v4.jpg", "C": f"naver_z{KEY}_s4.jpg"}
    if not _have(nm["B"]):
        DGC.bignum(nm["B"], c, "별자리·운세를 한 해 한 번 이상 봐요", "28%", "미국 성인 9,593명 가운데",
                   [("누가", "퓨 리서치 센터, 2024년 10월 조사"), ("물음", "별자리나 운세를 얼마나 자주 보나요"), ("결과", "열 명 중 세 명꼴이 한 해 한 번 이상")],
                   "Pew Research Center (2025)")
    if not _have(nm["K"]):
        DGC.compare(nm["K"], c, "전갈자리가 시작되는 순간", ("2026년", "2027년"),
                    [("시작", "10월 23일 오후 6시 37분", "10월 24일 0시 32분"), ("23일 아침생", "천칭자리", "천칭자리"),
                     ("23일 밤생", "전갈자리", "천칭자리")], "태양 황경 210도 · 한국 시각 · 한국천문연구원 절기(상강)와 같은 순간", hi=1)
    if not _have(nm["C"]):
        DGB.ladder(nm["C"], c, "별자리 운세를 읽는 세 칸", [("태양", "생일만 있으면 나와요"), ("달", "2~3일마다 바뀌어요"), ("상승", "평균 2시간마다 바뀌어요")], "태양에서 상승으로 갈수록 태어난 시각이 더 필요해요")
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
    alt = {"B": "조사 숫자 그림. 미국 성인 9,593명 가운데 28%가 한 해 한 번 이상 별자리나 운세를 본다고 답했어요",
           "K": "전갈자리가 시작되는 순간 비교 그림. 2026년은 10월 23일 오후 6시 37분, 2027년은 10월 24일 0시 32분이라 2027년 10월 23일생은 하루 종일 천칭자리",
           "C": "별자리 운세를 읽는 세 칸 그림. 태양은 생일만, 달은 2~3일마다 바뀌어 날과 시각, 상승은 평균 2시간마다 바뀌어 시각과 장소가 필요해요"}
    body = P(*head) + P("<b>📌 별자리 운세를 읽는 순서</b>", *[f"{i + 1}. {q}" for i, q in enumerate(toc_q)])
    for i, (q, s) in enumerate(zip(toc_q, secs)):
        for k in "BKC": s = s.replace(f"[[{k}]]", IMG(nm[k], alt[k]))
        body += H(f"{i + 1}. {q}") + s
    body += tail + CTA
    import copy_rules as CR
    for w in ("재미로", "상담", "—", "안녕하세요, 자오선의 정월이에요", "결론부터 말씀드릴게요", "한 줄로 먼저", "생년월일만 넣으면 1초", "한 줄 요약", "이 글의 순서", "수비학",
              "원소", "양태", "확증", "포러", "여섯 운명학", "총정리", "힘 쓸 달", "아낄 달", "솜씨", "값을 매", "내게") + tuple(CR.금지어):
        assert w not in re.sub(r"<[^>]+>", " ", body), w
    for f in made:   # 사이트 사본(K-069)
        dst = os.path.join(SITE, "public", "naver", "img", f); os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy(os.path.join(HERE, "img", f), dst)
    return body, a4, made

TITLE = "별자리 운세 보는 법, 12별자리 날짜가 해마다 바뀌는 이유"
TAGS = ["별자리운세", "별자리날짜", "12별자리", "별자리경계", "내별자리", "태양별자리", "상승별자리", "절기", "별자리생일", "자오선"]
REL = {"id": "n82", "title": "물고기자리 2027 운세, 해왕성 토성 떠난 해 달라지는 3가지",
       "phrase": "내 별자리가 물고기자리라면, 물고기자리 2027 운세, 해왕성 토성 떠난 해 달라지는 3가지",
       "url": "https://blog.naver.com/zaoseon/224465940267"}
_KV = json.load(open(os.path.join(SITE, "data", "keywords", "kw_volume.json"), encoding="utf-8"))
KW_VOL = (_KV["posts"].get("n97") or {}).get("씨앗") or {}
INTENT = {"keywords": ["별자리운세", "12별자리날짜", "내별자리"],
          "keyword_src": "별자리운세 871,700(kw_volume 기존 묶음) · n51 재발행 일정 '새 글로 다시 쓰기'(진행표 11/18 넷째 줄) · n97 묶음 11/19 요청",
          "intent": "방법을 알고 싶다", "intent_note": "별자리 운세를 볼 때 내 별자리가 맞는지(경계 날짜·시각), 어떤 칸으로 읽는지, 2027 경계 시각을 바로",
          "first3": "별자리 운세는 태어난 순간 태양이 지나던 하늘 칸으로 흐름을 읽는 풀이예요. 12별자리 날짜는 해마다 몇 시간씩 바뀌어요. 같은 10월 23일생도 2026년과 2027년 별자리가 달라요.",
          "answer_keys": ["태양 별자리 = 태양이 지나던 30도 칸", "경계는 해마다 약 6시간 늦어짐", "경계 = 24절기 중기"],
          "community_q": [], "order": toc_q, "images": ["조사 숫자(bignum, Pew 2025)", "전갈자리 시작 2026·2027 비교(compare, swisseph 계산)", "읽는 세 칸(ladder)"],
          "related": "n82", "cta": PID, "experience": [], "applied": True,
          "differs_from_n51": "제목(원소와 생일 한눈에 → 날짜가 해마다 바뀌는 이유)·도입(정의 + 10/23 경계 예)·소제목 순서·원소 4무리·양태 3가지·2027 느린 별·확증 편향·포러 실험·여섯 운명학 대신 경계 시각 계산(swisseph assert)·2027 경계 시각 12줄·절기 중기와 같은 순간·읽는 순서(태양·달·상승)·Pew 2025 조사·그림 유형(bignum·compare·ladder)·연결글(→ n82)"}

if __name__ == "__main__":
    body, a4, made = build()
    reg = json.load(open(MP.REG, encoding="utf-8"))
    assert PID not in reg or not reg[PID].get("done"), "이미 예약 끝난 글"
    reg[PID] = dict(dt="2027-02-07T08:00:00", dt_tbd="CT가 정함(재발행 일정 'n51 다시 쓰기' 자리, 진행표 11/18). 이 날짜는 자리값", title=TITLE, tags=TAGS, body=body,
                    cover=a4, related=REL, thumbs=None, cid=None, clips=None, category="운명학 사전", done=False, kw_vol=KW_VOL,
                    k131="n97 11/19(K-151 새 글)", source="build_naver_97.py (n51 주제 새 글, n51 그대로)")
    json.dump(reg, open(MP.REG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    ic = json.load(open(os.path.join(HERE, "intent_cards.json"), encoding="utf-8")); ic["cards"][PID] = INTENT
    json.dump(ic, open(os.path.join(HERE, "intent_cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    v = reg[PID]
    MP.write_page(PID, D.datetime.fromisoformat(v["dt"]), v["title"], v["tags"], v["body"], None, v["cover"], v["related"], v["category"])
    MP.write_index()
    import k151_check as K
    print(PID, len(TITLE), "자 제목 · 본문 글자", len(re.sub(r"<[^>]+>|&nbsp;", "", body)), "· 사진", made, "· K 검사", K.check(PID, v))
