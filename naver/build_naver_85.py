"""네이버 n85: 2027년 운세 새 글 (CT 11/4 08:25 → ① 최우선, 대표 11/4 07:48 "지금 노출 안되는 글들도 조회수 높은 것들 순서로 수정 후 신규발행").
- 왜: 노출 안 되는 옛 글 n14(2027년 운세 사주·점성술·수비학·자미두수로 겹쳐 본 정미년)를 새 글로. n14는 건드리지 않는다(K-147·K-178).
- 대표 검색어: CT 11/4 19:10 실측 '2027년 운세' 월 6,200 → 제목 맨 앞. 보조 '정미년 운세'(1,800)·'신년운세'(5,670).
- 다르게 쓴 것(K-151): 여섯 운명학 겹쳐 보기 대신 정미년 뜻 + 흐름이 바뀌는 날짜 5가지 + 심리 개념(실행 의도 → 새 출발 효과) + 그림 유형(triad·ladder·twopanel).
- 계산: 입춘 = engine(한국천문연구원 2027 달력자료와 분 단위로 같음), 설날 2/7 = 한국천문연구원(11/4 확인)·삭 2/7 00:56,
  수성 역행·목성·개기일식 = pyswisseph 11/4 값, 아래 assert. (n82 초승달 18:07·수성 시각과 다름 → to-content [알림])
- 출처 2개(K-162, 11/4 확인): Dai, Milkman & Riis (2014) Management Science 60(10) 2563-2582 DOI 10.1287/mnsc.2014.1901 · 한국천문연구원 2027 달력자료.
- 날짜: CT가 정한다. pages.json dt 는 자리값, dt_tbd 로 표시.
사용: SITE=<zaoseon-site> python3 naver/build_naver_85.py"""
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
       '<tr><td style="padding:12px 10px;text-align:center;border:1px solid #d0d0d0"><span style="color:#9a9a9a">[ 1993 . 03 . 03 ]</span></td></tr>'
       '<tr><td style="padding:12px 10px;text-align:center;border:1px solid #d0d0d0"><b><a href="https://zaoseon.com/?utm_source=naver&amp;utm_medium=mid#free">내 태어난 날 글자 보기 →</a></b></td></tr>'
       '</tbody></table>' + BL)
CTA = ('<p><a href="https://zaoseon.com/?utm_source=naver&utm_medium=cta#free"><img src="' + RAW +
       'naver_cta5_1%EC%B4%88%EB%AC%B4%EB%A3%8C%ED%92%80%EC%9D%B4.jpg" alt="자오선 무료 1초 풀이 안내 배너"></a></p>')
MID = MID.replace("[ 1993 . 03 . 03 ]", "[ 1999 . 01 . 25 ]")
PID, KEY, PAL = "n85", "85", "y_olive_s"   # 정미 = 불 위의 흙 → 흙 판 묶음 가운데 올리브 판

# ───────── 계산값과 검산 (엔진·Swiss Ephemeris · 한국 시각, 분 반올림)
import datetime as D
sys.path.insert(0, os.path.join(SITE, "engine")); import engine as EN
KST = D.timezone(D.timedelta(hours=9))
TT27 = {n: t for n, _, t in EN.get_solar_terms_kst(2027)}; TT28 = {n: t for n, _, t in EN.get_solar_terms_kst(2028)}
def rm(t): return (t + D.timedelta(seconds=30)).replace(second=0, microsecond=0)
def kt(t):
    t = rm(t); h = t.hour; ap = "새벽" if h < 6 else "오전" if h < 12 else "오후" if h < 18 else "밤"; h12 = h if h <= 12 else h - 12
    return f"{t.month}월 {t.day}일 {ap} {h12}시 {t.minute}분"
assert kt(TT27["입춘"]) == "2월 4일 오전 10시 46분"            # 한국천문연구원 2027 달력자료(11/4 확인)
assert kt(TT28["입춘"]) == "2월 4일 오후 4시 31분"             # n81 과 같은 값
def ty(y, m=6, d=1):
    p = EN.year_pillar(D.datetime(y, m, d, 12, tzinfo=KST), EN.get_solar_terms_kst(y), EN.get_solar_terms_kst(y - 1)); return EN._ganji_str(p)
assert ty(2027) == "丁未" and ty(1967) == "丁未" and ty(2027, 2, 3) == "丙午" and ty(1999, 1, 25) == "戊寅"
GAN = "甲乙丙丁戊己庚辛壬癸"; ZJ = "子丑寅卯辰巳午未申酉戌亥"
assert [n for n in range(60) if n % 10 == GAN.index("丁") and n % 12 == ZJ.index("未")] == [43]   # 60갑자 44번째
# 하늘 값: Swiss Ephemeris 11/4 실행 값(한국 시각). 설날 = 2027년 첫 음력 초하루(삭 2/7 00:56), 한국천문연구원 '2월 7일(일)'과 같음.
SKY = {"삭": "2027-02-07 00:56", "수성1": "2027-02-10 02:36", "수성1끝": "2027-03-03 21:32", "수성2": "2027-06-11 03:15", "수성2끝": "2027-07-05 04:39",
       "수성3": "2027-10-07 23:37", "수성3끝": "2027-10-28 23:10", "목성 처녀": "2027-07-26 13:49", "목성 천칭": "2028-08-24 14:08", "일식": "2027-08-02 19:06"}
try:
    import swisseph as swe
    SIG = "양 황소 쌍둥이 게 사자 처녀 천칭 전갈 사수 염소 물병 물고기".split()
    def _jd(s): t = D.datetime.fromisoformat(s) - D.timedelta(hours=9); return swe.julday(t.year, t.month, t.day, t.hour + t.minute / 60)
    m = 3 / 1440
    el = lambda j: (swe.calc_ut(j, swe.MOON)[0][0] - swe.calc_ut(j, swe.SUN)[0][0]) % 360
    assert el(_jd(SKY["삭"]) - m) > 359 and el(_jd(SKY["삭"]) + m) < 1, "삭"
    sp = lambda s, d: swe.calc_ut(_jd(s) + d, swe.MERCURY)[0][3]
    for k in ("수성1", "수성2", "수성3"): assert sp(SKY[k], -m) > 0 > sp(SKY[k], m), k
    for k in ("수성1끝", "수성2끝", "수성3끝"): assert sp(SKY[k], -m) < 0 < sp(SKY[k], m), k
    jp = lambda s, d: SIG[int(swe.calc_ut(_jd(s) + d, swe.JUPITER)[0][0] // 30)]
    assert jp(SKY["목성 처녀"], -m) == "사자" and jp(SKY["목성 처녀"], m) == "처녀"
    assert jp(SKY["목성 천칭"], -m) == "처녀" and jp(SKY["목성 천칭"], m) == "천칭"
    r = swe.sol_eclipse_when_glob(_jd("2027-07-01 00:00"), swe.FLG_SWIEPH, 0)
    assert abs(r[1][0] - _jd(SKY["일식"])) < 3 / 1440 and r[0] & swe.ECL_TOTAL, "일식"
    print("하늘 계산 Swiss Ephemeris 로 다시 확인")
except ImportError:
    print("pyswisseph 없음: 11/4 실행 값으로 씀")
def sd(k, end=False):
    t = D.datetime.fromisoformat(SKY[k]); return f"{t.month}월 {t.day}일"
print("입춘·간지 엔진으로 다시 확인")

# ───────── 본문 (n14 문장을 옮기지 않았다)
head = ["<b>2027년 운세는 정미년(丁未年) 한 해의 흐름을 읽는 풀이예요.</b>",
        "정(丁)은 촛불 같은 불, 미(未)는 여름 끝의 흙인 양이라 '붉은 양의 해'라고 불러요. 정미년은 " + kt(TT27["입춘"]) + " 입춘에 시작해 2028년 " + kt(TT28["입춘"]) + " 입춘 전까지예요.",
        "<b>새해 계획을 1월 1일에 세웠다가 흐지부지된 적이 있다면, 이 글에서 다시 시작할 날짜 하나를 골라 가세요.</b>",
        "2026년 11월 4일 기준으로 정리한 내용이에요."]
toc_q = ["정미년은 어떤 해일까요?", "2027년 운세가 바뀌는 날짜 5가지는 언제일까요?", "새해 결심은 왜 1월 1일이 아니어도 될까요?",
         "내 띠로 보면 2027년 운세는 어떻게 다를까요?", "자주 묻는 질문"]
sec1 = P("<b>정미(丁未)는 60갑자의 44번째 짝이에요.</b>", "60년에 한 번 돌아와서, 바로 앞 정미년은 1967년이었어요.") + "[[T]]" + \
       P("🔥 <b>정(丁)</b>: 밤을 밝히는 작은 불이에요. 크게 타오르기보다 오래 비추는 불이에요.",
         "🟫 <b>미(未)</b>: 여름 끝의 마른 흙이고, 띠로는 양이에요.",
         "작은 불이 마른 흙을 천천히 데우는 모양이라, 새로 크게 벌이기보다 가진 것을 익히는 해로 읽어요.") + MID
sec2 = P("<b>2027년은 날짜 다섯 개만 달력에 적어 두면 흐름이 보여요.</b>") + \
       P("1️⃣ <b>" + kt(TT27["입춘"]) + " 입춘</b>: 정미년이 시작돼요. 사주와 띠는 이날부터 바뀌어요.",
         "2️⃣ <b>2월 7일 설날</b>: 음력 정월 초하루예요. 띠는 설날이 아니라 입춘으로 나눠요.",
         "3️⃣ <b>수성 역행 세 번</b>: " + sd("수성1") + "~" + sd("수성1끝") + ", " + sd("수성2") + "~" + sd("수성2끝") + ", " + sd("수성3") + " 밤~" + sd("수성3끝") + ". 점성술에서는 약속과 연락을 한 번 더 확인하는 때로 봐요.",
         "4️⃣ <b>" + kt(D.datetime.fromisoformat(SKY["목성 처녀"])) + " 목성이 처녀자리로</b>: 2028년 8월 24일까지 머물러요. 넓히던 일을 정리하고 다듬는 쪽으로 무게가 옮겨 가요.",
         "5️⃣ <b>8월 2일 개기일식</b>: 스페인·북아프리카·중동을 지나는 일식이에요. 점성술에서는 한 해의 큰 매듭으로 읽어요.") + "[[L]]" + \
       P("입춘·설날은 한국천문연구원 2027년 달력자료, 별의 날짜는 Swiss Ephemeris로 계산한 한국 시각이에요.",
         "별의 움직임으로 흐름을 읽는 이야기이고, 일이 정해져 있다는 뜻은 아니에요.")
sec3 = P("🧠 <b>사람은 '새로 시작하는 날'이 있을 때 결심을 더 잘 꺼내요.</b>",
         "다이·밀크먼·리스 연구팀은 새해, 새달, 새 주, 생일 같은 시간의 이정표 바로 뒤에 다이어트 검색, 운동 시설 방문, 목표 약속이 늘어난다는 걸 찾았어요.") + "[[F]]" + \
       P("연구팀은 이걸 '새 출발 효과'라고 불렀어요. 지난 실수를 앞 칸에 두고, 새 칸에서 다시 시작하는 마음이 생긴다는 거예요.",
         "그래서 1월 1일을 놓쳐도 괜찮아요. 2027년에는 입춘과 설날이 사흘 사이에 두 번 와요.",
         '📚 <b>출처 1</b>: <a href="https://doi.org/10.1287/mnsc.2014.1901">Dai, Milkman &amp; Riis (2014), The Fresh Start Effect, Management Science</a>',
         '📚 <b>출처 2</b>: <a href="https://astro.kasi.re.kr/kor/life/post/calendarData?year=2027">한국천문연구원 천문우주지식정보, 2027년 달력자료(입춘·설날)</a>') + \
       P("🌱 <b>마음 코치 정월의 질문</b>", "올해 시작했다가 멈춘 일 가운데<br>다시 꺼내고 싶은 하나는 무엇인가요?",
         "🔸 그 일을 '1월 1일'이 아니라<br>'2월 4일 입춘'에 다시 시작한다면요?") + \
       P("✔️ <b>이번 주에 해 볼 것 하나</b>: 2027년 달력이 생기면<br>2월 4일 칸에 '다시 시작할 일 한 줄'을<br>미리 적어 두세요.")
sec4 = P("<b>같은 정미년이라도 내 띠가 해의 양(未)과 어떤 사이인지에 따라 읽는 법이 달라요.</b>",
         "🤝 말띠는 양과 짝을 이루고, 토끼띠·돼지띠는 양과 한 팀으로 묶여요. 손잡는 일이 잘 풀리는 쪽이에요.",
         "🔄 소띠는 양과 마주 보고, 양띠는 같은 글자가 겹치고, 개띠는 양과 부딪히는 사이라 자리가 크게 바뀌는 쪽이에요.",
         "나머지 여섯 띠는 해의 불(丁)과 내 띠 기운이 만나는 모양으로 읽어요.") + \
       P("띠마다 힘 쓸 달과 아낄 달은 아래 연결글에 한 장으로 모아 두었어요.")
sec5 = P("<b>Q. 2027년은 무슨 띠의 해인가요?</b>", "A. 양띠의 해예요.",
         "정(丁)이 붉은색을 뜻하는 불이라 '붉은 양의 해'라고 불러요.") + \
       P("<b>Q. 1월에 태어난 사람은 2027년 운세를 무슨 띠로 보나요?</b>", "A. 입춘 전에 태어났다면 앞 해의 띠로 봐요.",
         "예를 들어 1999년 1월 25일생은 토끼띠가 아니라 호랑이띠예요. 2027년 2월 3일에 태어나는 아기도 말띠예요.") + \
       P("<b>Q. 정미년은 좋은 해인가요?</b>", "A. 좋고 나쁨보다 '익히는 해'에 가까워요.",
         "상반기에는 시작한 일을 알리고, 7월 말 목성이 옮긴 뒤에는 정리와 점검에 힘을 쓰면 흐름과 맞아요.") + \
       P("<b>Q. 신년운세는 언제 보는 게 맞나요?</b>", "A. 사주로 보면 입춘 뒤가 새해예요.",
         "양력 1월 1일, 설날, 입춘 가운데 마음이 새로 시작되는 날을 하나 골라 그날 보셔도 좋아요.")
tail = P("여러분은 2027년 다섯 날짜 가운데 어느 날을 출발선으로 고르시겠어요?", "번호 하나만 댓글로 남겨 주세요.") + \
       '<p><b>👇 내 띠의 2027년이 궁금하다면, 2027 띠별 운세, 정미년 12띠 힘 쓸 달과 아낄 달 한눈에</b></p>'
secs = [sec1, sec2, sec3, sec4, sec5]

def _have(n): return os.path.exists(os.path.join(HERE, "img", n))
def build():
    for d_ in ("wide", "m1280", "master"): os.makedirs(os.path.join(HERE, "img", d_), exist_ok=True)
    c = V.Ctx(PAL); made = []
    a4 = f"wide/naver_z{KEY}_a4.jpg"
    if not _have(a4):
        V.render(PID + "_new", {"d": "N", "el": "흙", "kick": "2027년 운세", "hook": ["정미년 한 해", "바뀌는 날 5개"], "sub": "붉은 양의 해",
                                "items": ["입춘", "목성 이동", "개기일식"]}, os.path.join(HERE, "img", a4), PAL)
    made.append(a4)
    nm = {"T": f"naver_z{KEY}_t7.jpg", "L": f"naver_z{KEY}_l7.jpg", "F": f"naver_z{KEY}_w7.jpg"}
    if not _have(nm["T"]):
        DGC.triad(nm["T"], c, "정미년 세 가지 뜻", [("정 丁", "밤을 밝히는 작은 불"), ("미 未", "여름 끝 마른 흙, 띠로는 양"),
                                                  ("60년 만", "앞은 1967년, 다음은 2087년")], 0,
                  "작은 불이 흙을 데우는 해: 벌이기보다 익히기", "60갑자 44번째 · 엔진 계산")
    if not _have(nm["L"]):
        DGB.ladder(nm["L"], c, "2027년 바뀌는 날 다섯", [
            ("2월 4일", "입춘: 정미년 시작, 띠가 바뀌어요"), ("2월 7일", "설날: 음력 정월 초하루"),
            ("수성 역행", "2월 · 6월 · 10월, 약속 다시 읽기"), ("7월 26일", "목성 처녀자리로: 넓히기에서 다듬기로"),
            ("8월 2일", "개기일식: 한 해의 큰 매듭")], "입춘·설날 한국천문연구원 · 별 Swiss Ephemeris")
    if not _have(nm["F"]):
        DGB.twopanel(nm["F"], c, "결심이 잘 나오는 날", ("평범한 날", "어제와 같은 하루", 0.35), ("새로 시작하는 날", "새해 · 새달 · 생일 · 입춘", 1.0),
                     "새 출발 효과 · Dai, Milkman & Riis (2014)", "놓친 결심은 입춘에 다시 꺼내기", verb="이렇게 써요: ")
    import fullbleed as FBL
    plan_p = os.path.join(HERE, "fullbleed_plan.json"); plan = json.load(open(plan_p, encoding="utf-8")) if os.path.exists(plan_p) else {}
    rows = []
    for pos, k in enumerate("TLF", 1):
        f = nm[k][:-4] + "f.jpg"
        if not _have(f):
            r, why = FBL.convert(nm[k], [os.path.join(HERE, "img"), os.path.join(HERE, "img", "m1280")]); assert r, (nm[k], why)
        rows.append({"pos": pos, "old": nm[k], "new": f}); made.append(nm[k]); nm[k] = f
        reg_ = json.load(open(DG.REG, encoding="utf-8")); reg_[f] = reg_[rows[-1]["old"]]; json.dump(dict(sorted(reg_.items())), open(DG.REG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    plan[PID] = rows; json.dump(plan, open(plan_p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    made += list(nm.values())
    alt = {"T": "정미년 세 가지 뜻 그림. 정은 밤을 밝히는 작은 불, 미는 여름 끝 마른 흙이자 양띠, 60년 만에 돌아와 앞은 1967년 다음은 2087년",
           "L": "2027년 바뀌는 날 다섯 그림. 2월 4일 입춘, 2월 7일 설날, 2월·6월·10월 수성 역행, 7월 26일 목성 처녀자리 이동, 8월 2일 개기일식",
           "F": "새 출발 효과 그림. 평범한 날보다 새해·새달·생일·입춘처럼 새로 시작하는 날에 결심이 더 커져요. 다이·밀크먼·리스 2014"}
    body = P(*head) + P("<b>📌 이 글의 순서</b>", *[f"{i + 1}. {q}" for i, q in enumerate(toc_q)])
    for i, (q, s) in enumerate(zip(toc_q, secs)):
        for k in "TLF": s = s.replace(f"[[{k}]]", IMG(nm[k], alt[k]))
        body += H(f"{i + 1}. {q}") + s
    body += tail + CTA
    import copy_rules as CR
    for w in ("재미로", "상담", "—", "안녕하세요, 자오선의 정월이에요", "결론부터 말씀드릴게요") + tuple(CR.금지어):
        assert w not in re.sub(r"<[^>]+>", " ", body), w
    for f in made:   # 사이트 사본(K-069)
        dst = os.path.join(SITE, "public", "naver", "img", f); os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy(os.path.join(HERE, "img", f), dst)
    return body, a4, made

TITLE = "2027년 운세 한눈에, 정미년 뜻과 흐름 바뀌는 날짜 5가지"
TAGS = ["2027년운세", "2027운세", "정미년운세", "신년운세", "2027년신년운세", "정미년", "붉은양의해", "2027입춘", "새출발효과", "자오선"]
REL = {"id": "n80", "title": "2027 띠별 운세, 정미년 12띠 힘 쓸 달과 아낄 달 한눈에",
       "phrase": "내 띠의 2027년이 궁금하다면, 2027 띠별 운세, 정미년 12띠 힘 쓸 달과 아낄 달 한눈에",
       "url": "https://blog.naver.com/zaoseon/224461125363"}
KW_VOL = {"2027년운세": 6200, "신년운세": 5670, "2027운세": 2300, "2027년신년운세": 2180, "정미년운세": 1800}
INTENT = {"keywords": ["2027년 운세", "정미년 운세", "신년운세", "2027 운세", "정미년 뜻"],
          "keyword_src": "CT 11/4 19:10 월 검색량 실측(data/keywords/kw_volume.json posts.n85): 2027년운세 6,200 · 신년운세 5,670 · 2027운세 2,300 · 2027년신년운세 2,180 · 정미년운세 1,800. n14 조회 순위(노출 안 되는 옛 글 4번째)",
          "intent": "알고 싶다", "intent_note": "2027년이 어떤 해인지(정미년 뜻)와 언제부터 언제까지인지, 흐름이 바뀌는 날짜를 확인",
          "first3": "2027년 운세는 정미년(丁未年) 한 해의 흐름을 읽는 풀이예요. 정미년은 2027년 2월 4일 오전 10시 46분 입춘에 시작해 2028년 2월 4일 오후 4시 31분 입춘 전까지예요.",
          "answer_keys": ["2027년 운세", "정미년"],
          "order": toc_q[:4], "images": ["정미년 세 가지 뜻(triad)", "2027년 바뀌는 날 다섯(ladder)", "새 출발 효과(twopanel, Dai 외 2014)"],
          "related": "n80", "cta": PID, "experience": [], "applied": True,
          "differs_from_n14": "제목·도입(정의 + 시작·끝 시각 직답)·소제목 순서·여섯 운명학 겹쳐 보기 대신 날짜 다섯·예시(1967 정미년, 1999.1.25 호랑이띠)·그림 유형(triad·ladder·twopanel)·심리 개념(실행 의도 → 새 출발 효과)·출처·연결글(n80)"}

if __name__ == "__main__":
    body, a4, made = build()
    reg = json.load(open(MP.REG, encoding="utf-8"))
    assert PID not in reg or not reg[PID].get("done"), "이미 예약 끝난 글"
    reg[PID] = dict(dt="2027-01-31T18:00:00", dt_tbd="CT가 정함(서브 배너 링크 고침 확인 뒤 하루 2편 08:00·18:00). 이 날짜는 자리값", title=TITLE, tags=TAGS, body=body,
                    cover=a4, related=REL, thumbs=None, cid=None, clips=None, category="2027 운세", done=False, kw_vol=KW_VOL,
                    k131="n85 11/4(K-151 새 글)", source="build_naver_85.py (n14 주제 새 글, n14 그대로)")
    json.dump(reg, open(MP.REG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    ic = json.load(open(os.path.join(HERE, "intent_cards.json"), encoding="utf-8")); ic["cards"][PID] = INTENT
    json.dump(ic, open(os.path.join(HERE, "intent_cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    v = reg[PID]
    MP.write_page(PID, D.datetime.fromisoformat(v["dt"]), v["title"], v["tags"], v["body"], None, v["cover"], v["related"], v["category"])
    MP.write_index()
    import k151_check as K
    print(PID, len(TITLE), "자 제목 · 본문 글자", len(re.sub(r"<[^>]+>|&nbsp;", "", body)), "· 사진", made, "· K 검사", K.check(PID, v))
