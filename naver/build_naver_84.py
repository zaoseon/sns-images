"""네이버 n84: 연애운 2027 새 글 (CT 11/4 08:25 → ① 최우선, 대표 11/4 07:48 "지금 노출 안되는 글들도 조회수 높은 것들 순서로 수정 후 신규발행").
- 왜: 노출 안 되는 옛 글 n10(2027년 연애운 좋은 띠 TOP5)을 새 글로. n10은 건드리지 않는다(K-147·K-178).
- 대표 검색어: CT 11/4 19:10 실측(data/keywords/kw_volume.json) '연애운' 월 10,580 → 제목 맨 앞. 보조 '띠별 연애운'(25).
- 다르게 쓴 것(K-151): n10은 육합·삼합 순위 TOP5 + 짝 글자의 달. 이 글은 순위 없이 '도화(桃花)가 피는 달' 네 무리(인오술→묘, 사유축→오, 신자진→유, 해묘미→자)
  + 2027 절기 시작 시각 + 심리 개념(아론 1997 가까워지는 36가지 질문) + 그림 유형(route·exp·ladder).
- 계산: 절기 = zaoseon-site engine.get_solar_terms_kst(2027·2028). 한국천문연구원 2027 달력자료(11/4 확인: 입춘 10:46·경칩 4:40·망종 6:26·백로 5:28·대설 17:38)와 분 단위로 맞음.
  달 간지 = 오호둔(丁년 寅월 壬寅) 셈 + engine.month_pillar, 띠 = engine.year_pillar. 아래 assert 로 다시 잰다.
- 출처 2개(K-162, 11/4 확인): Aron 외 (1997) PSPB 23(4) 363-377 DOI 10.1177/0146167297234003 · 한국천문연구원 2027 달력자료.
- 날짜: CT가 정한다. pages.json dt 는 자리값, dt_tbd 로 표시. queue.json 에는 넣지 않는다(naver_queue_add.py 로 CT가).
사용: SITE=<zaoseon-site> python3 naver/build_naver_84.py"""
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
MID = MID.replace("[ 1993 . 03 . 03 ]", "[ 1996 . 09 . 08 ]")
PID, KEY, PAL = "n84", "84", "m_soft_s"   # 연애 글 → 불 판 묶음 가운데 부드러운 판(n83 p_red_s 와 다르게)

# ───────── 계산값과 검산 (엔진 · 한국 시각, 분 반올림)
import datetime as D
sys.path.insert(0, os.path.join(SITE, "engine")); import engine as EN
KST = D.timezone(D.timedelta(hours=9))
T26, T27, T28 = (EN.get_solar_terms_kst(y) for y in (2026, 2027, 2028))
TT27 = {n: t for n, _, t in T27}; TT28 = {n: t for n, _, t in T28}
def rm(t): return (t + D.timedelta(seconds=30)).replace(second=0, microsecond=0)
def kt(t):
    t = rm(t); h = t.hour; ap = "새벽" if h < 6 else "오전" if h < 12 else "오후" if h < 18 else "밤"; h12 = h if h <= 12 else h - 12
    return f"{t.month}월 {t.day}일 {ap} {h12}시 {t.minute}분"
# 한국천문연구원 2027 달력자료(11/4 확인)와 같은지
assert kt(TT27["입춘"]) == "2월 4일 오전 10시 46분" and kt(TT27["경칩"]) == "3월 6일 새벽 4시 40분"
assert kt(TT27["망종"]) == "6월 6일 오전 6시 26분" and kt(TT27["백로"]) == "9월 8일 새벽 5시 28분" and kt(TT27["대설"]) == "12월 7일 오후 5시 38분"
ZJ = "子丑寅卯辰巳午未申酉戌亥"; GAN = "甲乙丙丁戊己庚辛壬癸"
NM = dict(zip(ZJ, "쥐 소 호랑이 토끼 용 뱀 말 양 원숭이 닭 개 돼지".split()))
TAO = {"寅午戌": "卯", "巳酉丑": "午", "申子辰": "酉", "亥卯未": "子"}          # 도화: 세 띠 무리 → 도화 글자
ORDER = ["寅午戌", "巳酉丑", "申子辰", "亥卯未"]
START = {"卯": ("경칩", TT27["경칩"], TT27["청명"]), "午": ("망종", TT27["망종"], TT27["소서"]),
         "酉": ("백로", TT27["백로"], TT27["한로"]), "子": ("대설", TT27["대설"], TT28["소한"])}
def ty(y, m=6, d=1):
    p = EN.year_pillar(D.datetime(y, m, d, 12, tzinfo=KST), EN.get_solar_terms_kst(y), EN.get_solar_terms_kst(y - 1)); return EN._ganji_str(p)
assert ty(2027) == "丁未" and ty(1990) == "庚午" and ty(1996) == "丙子" and ty(1999, 1, 25) == "戊寅"
MONTH_GZ = {}
for z in TAO.values():   # 오호둔: 丁년 寅월 천간 = 壬, 한 달에 한 칸씩
    k = (ZJ.index(z) - ZJ.index("寅")) % 12; MONTH_GZ[z] = GAN[(GAN.index("壬") + k) % 10] + z
assert MONTH_GZ == {"卯": "癸卯", "午": "丙午", "酉": "己酉", "子": "壬子"}
# 엔진 월주로도 한 번 더(달 가운데 날)
TL = sorted([x for T in (T26, T27, T28) for x in T], key=lambda x: x[2])
for z, (_, a, _) in START.items():
    g = EN.month_pillar(a + D.timedelta(days=10), "丁", TL); g = g if isinstance(g, str) else EN._ganji_str(g)
    assert g == MONTH_GZ[z], (z, g)
def grp(z): return [g for g in TAO if z in g][0]
assert TAO[grp("午")] == "卯" and TAO[grp("子")] == "酉" and TAO[grp("寅")] == "卯"   # 1990 말띠 3월 · 1996 쥐띠 9월 · 1999.1.25 호랑이띠 3월
def names(g): return "·".join(NM[x] for x in g)
def span(z):
    a, s, e = START[z]; s = rm(s); e = rm(e) - D.timedelta(days=1)
    return f"{s.month}월 {s.day}일 {a}부터 " + ("2028년 " if e.year == 2028 else "") + f"{e.month}월 {e.day}일까지"
assert span("子") == "12월 7일 대설부터 2028년 1월 5일까지", span("子")
assert span("卯") == "3월 6일 경칩부터 4월 4일까지", span("卯")
print("절기·간지·띠 엔진으로 다시 확인")

# ───────── 본문 (n10 문장을 옮기지 않았다)
head = ["<b>연애운은 그해와 그달의 글자가 내 띠와 만나는 모양으로 읽는 인연의 흐름이에요.</b>",
        "2027년 연애운은 띠마다 도화(桃花)가 피는 달이 달라요. 호랑이·말·개띠는 3월, 뱀·닭·소띠는 6월, 원숭이·쥐·용띠는 9월, 돼지·토끼·양띠는 12월이에요.",
        "<b>올해는 누군가를 만날 수 있을까 달력부터 넘겨 보게 된다면, 내 띠의 달 하나만 먼저 찾아 가세요.</b>",
        "2026년 11월 4일 기준으로 정리한 내용이에요."]
toc_q = ["연애운에서 말하는 도화는 무엇일까요?", "2027 연애운, 내 띠의 도화 달은 언제일까요?", "도화 달에 가까워지는 대화는 어떻게 할까요?",
         "띠 말고 무엇을 더 보면 좋을까요?", "자주 묻는 질문"]
EMO = {"寅午戌": "🐯🐴🐶", "巳酉丑": "🐍🐔🐮", "申子辰": "🐵🐭🐲", "亥卯未": "🐷🐰🐑"}
sec1 = P("<b>도화는 복숭아꽃이라는 뜻이에요.</b>", "사주에서는 사람의 눈길이 모이고 마음이 끌리는 기운을 도화라고 불러요.",
         "띠마다 도화가 되는 글자가 정해져 있어요. 열두 띠는 세 띠씩 네 무리로 묶여요.") + \
       P(*[f"{EMO[g]} <b>{names(g)}띠</b>: {NM[TAO[g]]}({TAO[g]}) 글자가 도화" for g in ORDER]) + \
       P("그 글자가 들어오는 달이 내 도화 달이에요.", "좋고 나쁨을 가르는 말이 아니라, 내가 사람들 눈에 잘 띄는 때라는 뜻으로 읽어요.") + MID
sec2 = P("<b>사주의 달은 양력 1일이 아니라 절기에서 바뀌어요.</b>", "그래서 도화 달도 절기가 드는 날부터 세요.") + \
       P(*[f"🌸 <b>{names(g)}띠</b>: {span(TAO[g])}, {MONTH_GZ[TAO[g]]} 달" for g in ORDER]) + "[[R]]" + \
       P("📆 예를 들어 1990년생 말띠는 3월, 1996년생 쥐띠는 9월이 도화 달이에요.",
         "같은 해에 태어난 사람은 띠가 같아서 도화 달도 같아요.") + \
       P("절기 시각은 한국천문연구원 2027년 달력자료와 같아요.", "흐름을 읽는 이야기이고, 그 달에 꼭 누군가를 만난다는 뜻은 아니에요.")
sec3 = P("🧠 <b>사람이 눈에 띄는 달이라도, 가까워지는 건 대화의 깊이에서 시작돼요.</b>",
         "심리학자 아론 연구팀은 처음 만난 두 사람에게 45분 동안 점점 깊어지는 질문 36개를 번갈아 묻게 했어요.") + "[[E]]" + \
       P("가벼운 잡담만 나눈 짝보다, 질문을 나눈 짝이 서로를 더 가깝게 느꼈어요.",
         "처음부터 깊은 말을 꺼낸 게 아니라, 가벼운 질문에서 조금씩 내려간 것이 열쇠였어요.",
         '📚 <b>출처 1</b>: <a href="https://doi.org/10.1177/0146167297234003">Aron, Melinat, Aron, Vallone &amp; Bator (1997), Personality and Social Psychology Bulletin</a>',
         '📚 <b>출처 2</b>: <a href="https://astro.kasi.re.kr/kor/life/post/calendarData?year=2027">한국천문연구원 천문우주지식정보, 2027년 달력자료(절기 시각)</a>') + \
       P("아래는 질문을 세 단계로 내려가는 예시예요.") + "[[Q]]" + \
       P("🌱 <b>마음 코치 정월의 질문</b>", "요즘 누군가에게 가장 깊게 물어본 질문은<br>무엇이었나요?",
         "🔸 다음에 만나면 '요즘 어때'보다<br>'올해 제일 고마웠던 일이 뭐야'로 시작한다면요?") + \
       P("✔️ <b>이번 주에 해 볼 것 하나</b>: 2027년 달력이 생기면<br>내 도화 달 첫날 칸에 '물어보고 싶은 질문 하나'를<br>미리 적어 두세요.")
sec4 = P("<b>띠는 태어난 해의 글자라, 같은 해 사람은 모두 같은 달을 받아요.</b>",
         "사주에서는 태어난 날의 글자(일지)로도 도화를 봐요. 날의 글자까지 보면 같은 띠라도 달이 하나 더 생기거나 겹쳐요.") + \
       P("💞 2027년의 띠는 양(未)이에요. 양과 짝을 이루는 말띠, 한 팀으로 묶이는 토끼띠·돼지띠는 한 해 내내 사람 사이 일이 잘 풀리는 쪽으로 읽어요.",
         "그래서 말띠는 3월 도화 달과 짝의 해가 겹치는 한 해예요.") + \
       P("별자리·수비학·자미두수처럼 다른 운명학을 겹쳐 보면, 같은 달을 가리키는 곳과 갈리는 곳이 보여요.")
sec5 = P("<b>Q. 도화가 있으면 바람기가 있다는 뜻인가요?</b>", "A. 아니에요.",
         "예전에는 도화살이라고 겁을 주는 말로 썼지만, 지금은 사람을 끄는 매력과 눈길로 읽어요. 그 눈길을 어디에 쓰는지가 더 중요해요.") + \
       P("<b>Q. 도화 달에 꼭 연애를 시작해야 하나요?</b>", "A. 꼭 그렇지 않아요.",
         "새 사람을 만나는 일만이 아니라, 오래 알던 사람과 한 걸음 가까워지는 일도 도화 달의 모양이에요.") + \
       P("<b>Q. 1월이나 2월 초에 태어났다면요?</b>", "A. 입춘 전에 태어났다면 앞 해의 띠로 봐요.",
         "예를 들어 1999년 1월 25일생은 토끼띠가 아니라 호랑이띠라서, 도화 달이 3월이에요.") + \
       P("<b>Q. 띠별 연애운은 해마다 같은 달인가요?</b>", "A. 도화가 되는 글자는 띠마다 늘 같아요.",
         "다만 그 글자의 달이 시작하는 날짜와 시각은 해마다 조금씩 달라서, 그해 절기를 다시 봐야 해요.")
tail = P("여러분의 도화 달은 몇 월이었나요?", "띠와 달만 댓글로 남겨 주세요.") + \
       '<p><b>👇 연애 말고 한 해 전체 흐름이 궁금하다면, 2027 띠별 운세, 정미년 12띠 힘 쓸 달과 아낄 달 한눈에</b></p>'
secs = [sec1, sec2, sec3, sec4, sec5]

def _have(n): return os.path.exists(os.path.join(HERE, "img", n))
def build():
    for d_ in ("wide", "m1280", "master"): os.makedirs(os.path.join(HERE, "img", d_), exist_ok=True)
    c = V.Ctx(PAL); made = []
    a4 = f"wide/naver_z{KEY}_a4.jpg"
    if not _have(a4):
        V.render(PID + "_new", {"d": "N", "el": "불", "kick": "2027 연애운", "hook": ["내 띠 도화 달", "언제일까"], "sub": "12띠를 네 무리로",
                                "items": ["3월", "6월", "9월 · 12월"]}, os.path.join(HERE, "img", a4), PAL)
    made.append(a4)
    nm = {"R": f"naver_z{KEY}_r7.jpg", "E": f"naver_z{KEY}_e6.jpg", "Q": f"naver_z{KEY}_l6.jpg"}
    if not _have(nm["R"]):
        DGB.route(nm["R"], c, "2027 도화 달 네 번",
                  [(f"{rm(START[TAO[g]][1]).month}월 {rm(START[TAO[g]][1]).day}일", " ".join(NM[x] for x in g) + "띠") for g in ORDER])
    if not _have(nm["E"]):
        DGC.exp(nm["E"], c, "가까워지는 36가지 질문", "아론 연구팀 · 1997",
                [("만남", "처음 만난 두 사람이 짝을 지어요"), ("45분", "점점 깊어지는 질문 36개를 번갈아 물어요"),
                 ("견주기", "가벼운 잡담만 나눈 짝과 견줘요")],
                "질문을 나눈 짝이 서로를 더 가깝게 느꼈어요", "Aron 외 (1997), PSPB")
    if not _have(nm["Q"]):
        DGB.ladder(nm["Q"], c, "질문 세 단계로 내려가기", [
            ("가볍게", "요즘 제일 자주 듣는 노래는 뭐야?"), ("조금 더", "올해 제일 고마웠던 일은 뭐였어?"),
            ("깊게", "내년에 꼭 해 보고 싶은 일 하나는?")], "예시 질문이에요. 내 말로 바꿔 써 보세요")
    import fullbleed as FBL
    plan_p = os.path.join(HERE, "fullbleed_plan.json"); plan = json.load(open(plan_p, encoding="utf-8")) if os.path.exists(plan_p) else {}
    rows = []
    for pos, k in enumerate("REQ", 1):
        f = nm[k][:-4] + "f.jpg"
        if not _have(f):
            r, why = FBL.convert(nm[k], [os.path.join(HERE, "img"), os.path.join(HERE, "img", "m1280")]); assert r, (nm[k], why)
        rows.append({"pos": pos, "old": nm[k], "new": f}); made.append(nm[k]); nm[k] = f
        reg_ = json.load(open(DG.REG, encoding="utf-8")); reg_[f] = reg_[rows[-1]["old"]]; json.dump(dict(sorted(reg_.items())), open(DG.REG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    plan[PID] = rows; json.dump(plan, open(plan_p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    made += list(nm.values())
    alt = {"R": "2027 도화 달 네 번 그림. 3월 6일 경칩 호랑이·말·개띠, 6월 6일 망종 뱀·닭·소띠, 9월 8일 백로 원숭이·쥐·용띠, 12월 7일 대설 돼지·토끼·양띠",
           "E": "아론 연구팀 1997 실험 그림. 처음 만난 두 사람이 45분 동안 점점 깊어지는 질문 36개를 나누자 잡담만 나눈 짝보다 더 가깝게 느꼈어요",
           "Q": "질문 세 단계 예시 그림. 가볍게 요즘 듣는 노래, 조금 더 올해 고마웠던 일, 깊게 내년에 해 보고 싶은 일"}
    body = P(*head) + P("<b>📌 이 글의 순서</b>", *[f"{i + 1}. {q}" for i, q in enumerate(toc_q)])
    for i, (q, s) in enumerate(zip(toc_q, secs)):
        for k in "REQ": s = s.replace(f"[[{k}]]", IMG(nm[k], alt[k]))
        body += H(f"{i + 1}. {q}") + s
    body += tail + CTA
    import copy_rules as CR
    for w in ("재미로", "상담", "—", "안녕하세요, 자오선의 정월이에요", "결론부터 말씀드릴게요") + tuple(CR.금지어):
        assert w not in re.sub(r"<[^>]+>", " ", body), w
    for f in made:   # 사이트 사본(K-069)
        dst = os.path.join(SITE, "public", "naver", "img", f); os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy(os.path.join(HERE, "img", f), dst)
    return body, a4, made

TITLE = "연애운 2027, 12띠 도화가 피는 달 언제인지 한눈에"
TAGS = ["연애운", "2027연애운", "띠별연애운", "도화살", "도화", "2027운세", "정미년", "인연운", "36가지질문", "자오선"]
REL = {"id": "n80", "title": "2027 띠별 운세, 정미년 12띠 힘 쓸 달과 아낄 달 한눈에",
       "phrase": "연애 말고 한 해 전체 흐름이 궁금하다면, 2027 띠별 운세, 정미년 12띠 힘 쓸 달과 아낄 달 한눈에",
       "url": "https://blog.naver.com/zaoseon/224461125363"}
KW_VOL = {"연애운": 10580, "띠별연애운": 25, "2027년연애운": 25}
INTENT = {"keywords": ["연애운", "2027 연애운", "띠별 연애운", "도화 달", "도화살"],
          "keyword_src": "CT 11/4 19:10 월 검색량 실측(data/keywords/kw_volume.json posts.n84): 연애운 10,580 · 띠별연애운 25 · 2027년연애운 25. n10 조회 순위(노출 안 되는 옛 글 3번째)",
          "intent": "알고 싶다", "intent_note": "2027년에 내 띠의 인연이 들어오는 달이 언제인지 날짜로 확인",
          "first3": "연애운은 그해와 그달의 글자가 내 띠와 만나는 모양으로 읽는 인연의 흐름이에요. 2027년에는 호랑이·말·개띠 3월, 뱀·닭·소띠 6월, 원숭이·쥐·용띠 9월, 돼지·토끼·양띠 12월이 도화 달이에요.",
          "answer_keys": ["연애운", "도화"],
          "order": toc_q[:4], "images": ["2027 도화 달 네 번(route)", "가까워지는 36가지 질문(exp, Aron 외 1997)", "질문 세 단계(ladder)"],
          "related": "n80", "cta": PID, "experience": [], "applied": True,
          "differs_from_n10": "제목·도입(정의 + 네 무리 직답)·소제목 순서·순위 없음(n10은 TOP5)·기준(육합 짝 달 → 도화 달)·예시(1990 말띠·1996 쥐띠·1999.1.25 호랑이띠)·그림 유형(route·exp·ladder)·심리 개념(Aron 1997)·출처·연결글(n80)"}

if __name__ == "__main__":
    body, a4, made = build()
    reg = json.load(open(MP.REG, encoding="utf-8"))
    assert PID not in reg or not reg[PID].get("done"), "이미 예약 끝난 글"
    reg[PID] = dict(dt="2027-01-31T08:00:00", dt_tbd="CT가 정함(서브 배너 링크 고침 확인 뒤 하루 2편 08:00·18:00). 이 날짜는 자리값", title=TITLE, tags=TAGS, body=body,
                    cover=a4, related=REL, thumbs=None, cid=None, clips=None, category="관계 읽기", done=False, kw_vol=KW_VOL,
                    k131="n84 11/4(K-151 새 글)", source="build_naver_84.py (n10 주제 새 글, n10 그대로)")
    json.dump(reg, open(MP.REG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    ic = json.load(open(os.path.join(HERE, "intent_cards.json"), encoding="utf-8")); ic["cards"][PID] = INTENT
    json.dump(ic, open(os.path.join(HERE, "intent_cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    v = reg[PID]
    MP.write_page(PID, D.datetime.fromisoformat(v["dt"]), v["title"], v["tags"], v["body"], None, v["cover"], v["related"], v["category"])
    MP.write_index()
    import k151_check as K
    print(PID, len(TITLE), "자 제목 · 본문 글자", len(re.sub(r"<[^>]+>|&nbsp;", "", body)), "· 사진", made, "· K 검사", K.check(PID, v))
