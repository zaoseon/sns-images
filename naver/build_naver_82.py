"""네이버 n82: 물고기자리 2027 운세 새 글 (CT 11/4 08:25 → ① 최우선, 대표 11/4 07:48 "지금 노출 안되는 글들도 조회수 높은 것들 순서로 수정 후 신규발행").
- 왜: n80·n81(옛 글 주제 새 글)이 발행 뒤 바로 검색에 나왔다. 노출 안 되는 옛 글 가운데 조회 1위 n48(물고기자리 성격과 2027년 운세)을 새 글로 쓴다.
- 지킨 것: n48은 건드리지 않는다(K-147). 복사하지 않는다(K-151): 제목·도입·소제목 순서·예시(1993년 2월 25일·3월 3일생)·
  그림 유형(timeline3·versus·checklist)·심리 개념(반추 대신 공감과 연민)·연결글(n01 대신 발행된 n80)을 새로 썼다. 같은 것은 계산값뿐이다.
- 하늘 계산: pyswisseph(Swiss Ephemeris) 11/4 실행 값, 한국 시각. 아래 assert 로 다시 잰다(pyswisseph 없으면 적어 둔 값으로 씀).
- 사주 일진: zaoseon-site engine.day_pillar (1993-02-25 丁丑, 1993-03-03 癸未).
- 출처 2개(K-162, 11/4 웹에서 확인한 주소): Singer & Klimecki (2014) Current Biology 24(18) R875-R878 DOI 10.1016/j.cub.2014.06.054(pure.mpg.de 확인) ·
  Klimecki, Leiberg, Ricard & Singer (2014) Social Cognitive and Affective Neuroscience DOI 10.1093/scan/nst060.
- 날짜: CT가 정한다(서브가 배너 링크 고침을 확인한 날부터 하루 2편 08:00·18:00, 확인 전 queue.json 안 넣음). pages.json dt 는 자리값(2027-01-31)이고 dt_tbd 로 표시.
사용: SITE=<zaoseon-site> python3 naver/build_naver_82.py"""
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
PID, KEY, PAL = "n82", "82", "p_purple_s"   # 물고기자리=물 → 물 판 묶음(EL_SET 물) 가운데 보라 판

# ───────── 계산값과 검산 (Swiss Ephemeris, 한국 시각)
SKY = {"해왕성 떠남": "2026-01-27 02:40", "토성 떠남": "2026-02-14 09:11", "해 물고기 2026": "2026-02-19 00:51", "해 양 2026": "2026-03-20 23:45",
       "해 물고기 2027": "2027-02-19 06:33", "해 양 2027": "2027-03-21 05:24", "수성 역행": "2027-02-10 02:59", "수성 순행": "2027-03-03 22:11",
       "초승달": "2027-03-08 18:07", "목성 처녀": "2027-07-26 13:49", "목성 천칭": "2028-08-24 14:08", "토성 황소": "2028-04-13 12:40"}
try:
    import swisseph as swe, datetime as D
    SIG = "양 황소 쌍둥이 게 사자 처녀 천칭 전갈 사수 염소 물병 물고기".split()
    def _jd(s): t = D.datetime.fromisoformat(s) - D.timedelta(hours=9); return swe.julday(t.year, t.month, t.day, t.hour + t.minute / 60)
    def _sg(p, s, dm=0): return SIG[int(swe.calc_ut(_jd(s) + dm, p)[0][0] // 30)]
    m = 2 / 1440   # 2분 앞뒤
    for k, p, a, b in (("해왕성 떠남", swe.NEPTUNE, "물고기", "양"), ("토성 떠남", swe.SATURN, "물고기", "양"), ("해 물고기 2027", swe.SUN, "물병", "물고기"),
                       ("해 양 2027", swe.SUN, "물고기", "양"), ("목성 처녀", swe.JUPITER, "사자", "처녀"), ("토성 황소", swe.SATURN, "양", "황소")):
        assert _sg(p, SKY[k], -m) == a and _sg(p, SKY[k], m) == b, k
    for s in ("2027-01-01 00:00", "2027-06-30 00:00", "2027-12-31 23:00"):          # 2027 한 해 내내 해왕성·토성은 양자리
        assert _sg(swe.NEPTUNE, s) == "양" and _sg(swe.SATURN, s) == "양", s
    assert swe.calc_ut(_jd(SKY["수성 역행"]) + 0.1, swe.MERCURY)[0][3] < 0 < swe.calc_ut(_jd(SKY["수성 역행"]) - 0.1, swe.MERCURY)[0][3]
    assert _sg(swe.MERCURY, SKY["수성 역행"]) == "물고기"
    assert swe.calc_ut(_jd(SKY["수성 순행"]) + 0.1, swe.MERCURY)[0][3] > 0 > swe.calc_ut(_jd(SKY["수성 순행"]) - 0.1, swe.MERCURY)[0][3]
    e = lambda s: (swe.calc_ut(_jd(s), swe.MOON)[0][0] - swe.calc_ut(_jd(s), swe.SUN)[0][0]) % 360
    assert e(SKY["초승달"]) < 0.5 or e(SKY["초승달"]) > 359.5; assert _sg(swe.MOON, SKY["초승달"]) == "물고기"
    for s in ("1993-02-25 12:00", "1993-03-03 12:00"): assert _sg(swe.SUN, s) == "물고기", s
    print("하늘 계산 Swiss Ephemeris 로 다시 확인")
except ImportError:
    print("pyswisseph 없음: 11/4 실행 값으로 씀")
GZ = {"1993-02-25": "丁丑", "1993-03-03": "癸未"}
try:
    sys.path.insert(0, os.path.join(SITE, "engine")); import engine as EN, datetime as D
    for d_, g in GZ.items(): assert EN._ganji_str(EN.day_pillar(D.date.fromisoformat(d_))) == g, d_
    print("일진 엔진으로 다시 확인")
except ImportError:
    print("엔진 없음: 11/4 실행 값으로 씀")
def kt(k, fmt):
    import datetime as D; t = D.datetime.fromisoformat(SKY[k]); h = t.hour
    ap = "새벽" if h < 6 else "오전" if h < 12 else "오후" if h < 18 else "밤"; h12 = h if h <= 12 else h - 12
    return fmt.format(m=t.month, d=t.day, ap=ap, h=h12, mi=t.minute, y=t.year)
assert kt("해 물고기 2027", "{m}월 {d}일 {ap} {h}시 {mi}분") == "2월 19일 오전 6시 33분"
assert kt("해 양 2027", "{m}월 {d}일 {ap} {h}시 {mi}분") == "3월 21일 새벽 5시 24분"

# ───────── 본문 (n48 문장을 옮기지 않았다)
head = ["<b>물고기자리는 2월 19일 무렵부터 3월 20일 무렵까지 태어난 별자리예요.</b>",
        "2027년 물고기자리 운세는 세 가지가 달라져요. 오래 머문 해왕성과 토성이 떠난 뒤 처음 맞는 한 해, 생일 무렵 수성 역행, 7월 26일 맞은편 별자리로 옮기는 목성이에요.",
        "<b>내 일보다 남의 기분이 먼저 보여서 하루가 금방 지나간다면, 이 글에서 2027년 달력에 적어 둘 날짜부터 챙겨 가세요.</b>",
        "2026년 11월 4일 기준으로 정리한 내용이에요."]
toc_q = ["물고기자리는 몇 월 며칠생일까요?", "2027 물고기자리 운세, 무엇이 달라질까요?", "남의 마음을 잘 읽는 사람은 왜 쉽게 지칠까요?",
         "같은 물고기자리라도 사주로 보면 왜 다를까요?", "2027년 달력에 적어 둘 날은 언제일까요?", "자주 묻는 질문"]

sec1 = P("<b>해가 물고기자리를 지나는 동안 태어나면 물고기자리예요.</b>", "그래서 해마다 시작과 끝 시각이 조금씩 달라요.") + \
       P("📅 2026년: " + kt("해 물고기 2026", "{m}월 {d}일 {ap} {h}시 {mi}분") + " ~ " + kt("해 양 2026", "{m}월 {d}일 {ap} {h}시 {mi}분"),
         "📅 2027년: " + kt("해 물고기 2027", "{m}월 {d}일 {ap} {h}시 {mi}분") + " ~ " + kt("해 양 2027", "{m}월 {d}일 {ap} {h}시 {mi}분")) + \
       P("🔢 <b>3월 20일생은 해마다 다를 수 있어요</b>", "2026년 3월 20일에는 밤 11시 45분부터 양자리였어요.",
         "2027년 3월 20일생은 하루 종일 물고기자리예요. 경계 날짜에 태어났다면 태어난 시각까지 같이 보세요.") + MID
sec2 = P("<b>하나, 두 별이 떠난 뒤 처음 맞는 한 해예요.</b>",
         "해왕성은 2012년부터 약 14년, 토성은 2023년부터 약 3년 동안 물고기자리에 머물다 2026년 1월과 2월에 양자리로 옮겼어요.",
         "2027년에는 두 별이 한 해 내내 양자리에 있어요. 오래 안고 있던 숙제를 내려놓고, 하고 싶은 일을 내 말로 정하기 좋은 해로 읽어요.") + \
       P("<b>둘, 생일 무렵에 수성 역행이 있어요.</b>",
         "수성은 2월 10일 새벽 물고기자리에서 거꾸로 가기 시작해 3월 3일 밤에 다시 앞으로 가요.",
         "점성술에서는 이때 말과 약속이 엇갈리기 쉽다고 봐요. 새 계약보다 보낸 글을 한 번 더 읽는 쪽에 힘을 쓰세요.") + \
       P("<b>셋, 7월 26일 목성이 맞은편 처녀자리로 와요.</b>",
         "처녀자리는 물고기자리의 정반대 별자리라, 나와 마주 앉는 사람(짝·동업자)의 자리로 읽어요.",
         "목성은 2028년 8월 24일까지 처녀자리에 머물러요. 혼자 끌어안던 일을 함께 나눌 사람이 눈에 들어오기 쉬운 때예요.") + \
       P("아래 그림은 물고기자리를 지나간 별과 2027년 일정을 한 줄로 이은 거예요.") + "[[L]]" + \
       P("별의 움직임으로 흐름을 읽는 이야기이고, 일이 정해져 있다는 뜻은 아니에요.")
sec3 = P("🧠 <b>물고기자리는 남의 마음을 내 일처럼 느끼는 별자리로 자주 그려져요.</b>",
         "그런데 남의 아픔을 그대로 같이 느끼기만 하면 내가 먼저 지쳐요.",
         "신경과학자 싱어와 클리메키는 '같이 아파하는 공감'과 '따뜻하게 바라보며 잘되길 바라는 연민'을 나눠서 봤어요.") + "[[E]]" + \
       P("연구팀이 사람들에게 공감만 연습하게 하자, 남의 괴로운 장면을 볼 때 내 괴로움도 커졌어요.",
         "연민 연습을 더하자 좋은 마음이 늘고 괴로움은 줄었어요.",
         '📚 <b>출처 1</b>: <a href="https://doi.org/10.1093/scan/nst060">Klimecki, Leiberg, Ricard &amp; Singer (2014), Social Cognitive and Affective Neuroscience</a>',
         '📚 <b>출처 2</b>: <a href="https://doi.org/10.1016/j.cub.2014.06.054">Singer &amp; Klimecki (2014), Empathy and compassion, Current Biology</a>') + \
       P("🌱 <b>마음 코치 정월의 질문</b>", "요즘 누구의 기분을<br>내 것처럼 들고 다니고 있나요?",
         "🔸 그 사람에게 '같이 힘들어'보다<br>'네가 괜찮아지면 좋겠어'라고 말한다면요?")
sec4 = P("<b>별자리는 태어난 날의 하늘, 사주는 태어난 날의 글자예요.</b>",
         "같은 물고기자리여도 사주에서 나를 가리키는 첫 글자(일간)는 날마다 바뀌어요.") + \
       P("📆 1993년 2월 25일생: 일간 정(丁), 촛불", "📆 1993년 3월 3일생: 일간 계(癸), 빗물",
         "엿새 차이로 같은 물고기자리인데, 한 사람은 불, 한 사람은 물의 글자예요.") + \
       P("🔥 <b>정(丁) 일간 물고기자리</b>", "마음은 깊은데 겉으로는 환하게 웃어서, 지친 걸 주변이 늦게 알아요. 힘든 날은 '오늘은 여기까지'를 먼저 말해 보세요.") + \
       P("💧 <b>계(癸) 일간 물고기자리</b>", "물에 물이 겹쳐 남의 기분이 더 깊이 스며요. 하루에 한 번, 아무 연락에도 답하지 않는 20분을 정해 두세요.") + \
       P("자미두수·당사주·하락이수처럼 태어난 시간까지 쓰는 풀이를 더하면 그림이 더 또렷해져요.")
sec5 = P("<b>세 날짜만 달력에 적어 두면 돼요.</b>") + "[[K]]" + \
       P("✔️ <b>이번 주에 해 볼 것 하나</b>: 2027년 달력이 생기면<br>3월 8일 칸에 '올해 하고 싶은 일 한 줄'이라고<br>미리 적어 두세요.",
         "3월 8일 저녁 6시 7분은 물고기자리에서 초승달이 뜨는 때예요.")
sec6 = P("<b>Q. 물고기자리 2027년 운세는 좋은 편인가요?</b>", "A. 좋고 나쁨보다 '짐을 내려놓는 해'에 가까워요.",
         "오래 머문 두 별이 떠났고, 7월 말부터는 곁의 사람과 나누는 일에 힘이 실려요.") + \
       P("<b>Q. 물고기자리 수호성은 무엇인가요?</b>", "A. 전통 점성술은 목성, 현대 점성술은 해왕성으로 봐요.",
         "그래서 2027년 7월 목성이 맞은편으로 오는 일을 물고기자리에게 특히 크게 읽는 유파도 있어요.") + \
       P("<b>Q. 수성 역행 때 계약을 하면 안 되나요?</b>", "A. 꼭 피할 까닭은 없어요.", "날짜보다 조건을 한 번 더 읽고, 말로 한 약속은 글로 남기는 쪽을 권해요.") + \
       P("<b>Q. 물고기자리와 잘 맞는 별자리는요?</b>", "A. 같은 물 원소인 게자리·전갈자리가 편하다고 봐요.",
         "맞은편 처녀자리는 서로 없는 것을 채워 주는 짝으로 읽어요.")
tail = P("여러분은 정(丁)의 물고기자리에 가까우세요, 계(癸)의 물고기자리에 가까우세요?", "생일과 함께 댓글로 들려주세요.") + \
       '<p><b>👇 별자리 말고 띠로 보는 2027년이 궁금하다면, 2027 띠별 운세, 정미년 12띠 힘 쓸 달과 아낄 달 한눈에</b></p>'
secs = [sec1, sec2, sec3, sec4, sec5, sec6]

def _have(n): return os.path.exists(os.path.join(HERE, "img", n))
def build():
    for d_ in ("wide", "m1280", "master"): os.makedirs(os.path.join(HERE, "img", d_), exist_ok=True)
    c = V.Ctx(PAL); made = []
    a4 = f"wide/naver_z{KEY}_a4.jpg"
    if not _have(a4):
        V.render(PID + "_new", {"d": "N", "el": "물", "kick": "물고기자리 운세", "hook": ["2027 물고기자리", "달라지는 3가지"], "sub": "2월 19일 ~ 3월 21일생",
                                "items": ["두 별 떠남", "수성 역행", "목성 맞은편"]}, os.path.join(HERE, "img", a4), PAL)
    made.append(a4)
    nm = {"L": f"naver_z{KEY}_t6.jpg", "E": f"naver_z{KEY}_v6.jpg", "K": f"naver_z{KEY}_h6.jpg"}
    if not _have(nm["L"]):
        DGC.timeline3(nm["L"], c, "물고기자리 하늘 일정", [
            ("2026.1", "해왕성 떠남", "14년 머문 해왕성이 양자리로"), ("2026.2", "토성 떠남", "3년 머문 토성도 양자리로"),
            ("2027.2", "생일철 수성 역행", "2월 10일 시작, 3월 3일 밤 끝"), ("2027.7", "목성 처녀자리로", "7월 26일, 맞은편 별자리에 와요")],
            "2027년은 두 별 없이 맞는 첫 한 해", "Swiss Ephemeris 계산 · 한국 시각")
    if not _have(nm["E"]):
        DGC.versus(nm["E"], c, "같이 아파하기 vs 따뜻하게 바라보기", "싱어·클리메키 연구팀 · 2014",
                   ("공감 연습", "남의 아픔을 그대로 같이 느끼는 연습을 했어요", "괴로운 마음이 커졌어요"),
                   ("연민 연습", "따뜻하게 바라보는 연습을 더했어요", "괴로움이 줄었어요"),
                   "같이 아파하기보다 따뜻하게 바라보기", "Klimecki 외 (2014), SCAN")
    if not _have(nm["K"]):
        DGB.checklist(nm["K"], c, "2027 물고기자리 달력 세 칸", [
            ("2월 10일 ~ 3월 3일", "보낸 약속·계약서 한 번 더 읽기"), ("3월 8일 초승달", "올해 하고 싶은 일 한 줄 적기"),
            ("7월 26일 뒤", "함께 나눌 사람 한 명에게 먼저 연락")], "빈 칸은 직접 채워 보세요")
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
    alt = {"L": "물고기자리 하늘 일정 그림. 2026년 1월 해왕성, 2월 토성이 양자리로 떠나고, 2027년 2월 10일부터 3월 3일까지 수성 역행, 7월 26일 목성이 처녀자리로 옮겨요",
           "E": "공감 연습만 한 사람은 괴로운 마음이 커지고, 연민 연습을 더한 사람은 좋은 마음이 늘고 괴로움이 줄었다는 싱어·클리메키 연구팀 2014 비교 그림",
           "K": "2027 물고기자리 달력 세 칸 체크리스트: 2월 10일부터 3월 3일 약속 다시 읽기, 3월 8일 초승달에 하고 싶은 일 적기, 7월 26일 뒤 함께 나눌 사람에게 연락"}
    body = P(*head) + P("<b>📌 이 글의 순서</b>", *[f"{i + 1}. {q}" for i, q in enumerate(toc_q)])
    for i, (q, s) in enumerate(zip(toc_q, secs)):
        for k in "LEK": s = s.replace(f"[[{k}]]", IMG(nm[k], alt[k]))
        body += H(f"{i + 1}. {q}") + s
    body += tail + CTA
    import copy_rules as CR
    for w in ("재미로", "상담", "—", "안녕하세요, 자오선의 정월이에요", "결론부터 말씀드릴게요") + tuple(CR.금지어):
        assert w not in re.sub(r"<[^>]+>", " ", body), w
    for f in made:   # 사이트 사본(K-069)
        dst = os.path.join(SITE, "public", "naver", "img", f); os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy(os.path.join(HERE, "img", f), dst)
    return body, a4, made

TITLE = "물고기자리 2027 운세, 해왕성 토성 떠난 해 달라지는 3가지"
TAGS = ["물고기자리", "물고기자리운세", "2027물고기자리", "물고기자리성격", "별자리운세", "2027별자리운세", "목성처녀자리", "수성역행", "공감피로", "자오선"]
REL = {"id": "n80", "title": "2027 띠별 운세, 정미년 12띠 힘 쓸 달과 아낄 달 한눈에",
       "phrase": "별자리 말고 띠로 보는 2027년이 궁금하다면, 2027 띠별 운세, 정미년 12띠 힘 쓸 달과 아낄 달 한눈에",
       "url": "https://blog.naver.com/zaoseon/224461125363"}
INTENT = {"keywords": ["물고기자리 2027 운세", "물고기자리 운세", "물고기자리 날짜", "물고기자리 성격", "2027 별자리 운세"],
          "keyword_src": "n48 조회 순위(11/4 CT·서브 '노출 안 되는 옛 글 조회수 순' 1위) · n48 태그(물고기자리·물고기자리운세·물고기자리성격) · 자동완성·월 검색량 자료 없음(발행 7일 뒤 유입 검색어로 고친다)",
          "intent": "알고 싶다", "intent_note": "내 생일이 물고기자리인지, 2027년에 무엇이 달라지는지 날짜로 확인",
          "first3": "물고기자리는 2월 19일 무렵부터 3월 20일 무렵까지 태어난 별자리예요. 2027년에는 해왕성·토성이 떠난 첫 한 해, 생일 무렵 수성 역행, 7월 26일 목성의 맞은편 이동이 달라져요.",
          "answer_keys": ["물고기자리", "2월 19일"],
          "order": toc_q[:5], "images": ["물고기자리 하늘 일정(timeline3)", "공감 vs 연민 연습(versus, Klimecki 외 2014)", "2027 달력 세 칸(checklist)"],
          "related": "n80", "cta": PID, "experience": [], "applied": True,
          "differs_from_n48": "제목·도입(날짜 직답 + 달라지는 3가지)·소제목 순서·예시(1993년 2월 25일·3월 3일생, 정·계 일간)·그림 유형(timeline3·versus·checklist)·심리 개념(반추 → 공감과 연민)·출처(Nolen-Hoeksema → Singer·Klimecki 2개)·연결글(n01 → n80)"}

if __name__ == "__main__":
    body, a4, made = build()
    reg = json.load(open(MP.REG, encoding="utf-8"))
    assert PID not in reg or not reg[PID].get("done"), "이미 예약 끝난 글"
    reg[PID] = dict(dt="2027-01-31T08:00:00", dt_tbd="CT가 정함(서브 배너 링크 고침 확인 뒤 하루 2편 08:00·18:00). 이 날짜는 자리값", title=TITLE, tags=TAGS, body=body,
                    cover=a4, related=REL, thumbs=None, cid=None, clips=None, category="2027 신년운세", done=False,
                    k131="n82 11/4(K-151 새 글)", source="build_naver_82.py (n48 주제 새 글, n48 그대로)")
    json.dump(reg, open(MP.REG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    ic = json.load(open(os.path.join(HERE, "intent_cards.json"), encoding="utf-8")); ic["cards"][PID] = INTENT
    json.dump(ic, open(os.path.join(HERE, "intent_cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    v = reg[PID]; import datetime as D
    MP.write_page(PID, D.datetime.fromisoformat(v["dt"]), v["title"], v["tags"], v["body"], None, v["cover"], v["related"], v["category"])
    MP.write_index()
    import k151_check as K
    print(PID, len(TITLE), "자 제목 · 본문 글자", len(re.sub(r"<[^>]+>|&nbsp;", "", body)), "· 사진", made, "· K 검사", K.check(PID, v))
