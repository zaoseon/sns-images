"""네이버 n87: 사주 보는 법 새 글 (CT 11/4 19:40 → ① 최우선, 대표 11/4 19:28 재발행 일정 '새 글로 다시 쓰기' n47 → n87, 11/18 08:00 자리).
- 왜: 노출 안 되는 옛 글 n47(사주 보는 법 처음이라면, 일간·절기·태어난 시간)을 새 글로. n47은 건드리지 않는다(K-147·K-178).
- 검색어: data/keywords/kw_volume.json posts.n87(kw-volume 11/5) — 사주보는법 2,190 · 사주일간 2,050 · 일간 1,710 · 사주팔자보는법 210.
- 다르게 쓴 것(K-151): n47의 '세 가지(일간·절기·시간)' 설명과 열 글자 비유 나열 대신, 예시 한 명(1994.9.13 오전 8시 40분)의
  여덟 글자를 네 단계(일간 → 달 글자 계절 → 오행 개수 → 많은 것·0개 한 줄)로 끝까지 세는 글. 절기 경계 예시(1996.11.7 입동),
  심리 개념(자기효능감 Bandura 1977 → 풀이된 예시 효과 Sweller & Cooper 1985), 그림 유형(ladder·compare·vbar, n47은 quad·timeline3),
  연결글(n14 → n75 발행·노출 '예'). 소제목 틀(한 줄 요약·이 글의 순서·생년월일만 넣으면 1초·해 볼 것)을 쓰지 않는다(CT 11/4 21:05).
  앱마다 시주가 다른 이유는 n75가 다루므로 이 글은 짧게만 말하고 연결글로 보낸다(글끼리 겹침 줄이기).
- 계산: engine/engine.py compute_saju·get_solar_terms_kst. 아래 assert.
- 출처 2개(K-162, 11/5 확인): Sweller & Cooper (1985) Cognition and Instruction 2(1) 59-89 DOI 10.1207/s1532690xci0201_3(위키백과 Worked-example effect 인용 정보로 확인)
  · 한국천문연구원 음양력 변환(n75·n86에서 확인한 주소).
- 날짜: CT가 정한다. pages.json dt 는 자리값, dt_tbd 로 표시.
사용: SITE=<zaoseon-site> python3 naver/build_naver_87.py"""
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
       '<tr><td style="padding:12px 10px;text-align:center;border:1px solid #d0d0d0"><b>생일을 넣으면 여덟 글자와 일간이 바로</b></td></tr>'
       '<tr><td style="padding:12px 10px;text-align:center;border:1px solid #d0d0d0"><span style="color:#9a9a9a">[ 1994 . 09 . 13 ]</span></td></tr>'
       '<tr><td style="padding:12px 10px;text-align:center;border:1px solid #d0d0d0"><b><a href="https://zaoseon.com/?utm_source=naver&amp;utm_medium=mid#free">내 일간 찾아 보기 →</a></b></td></tr>'
       '</tbody></table>' + BL)
CTA = ('<p><a href="https://zaoseon.com/?utm_source=naver&utm_medium=cta#free"><img src="' + RAW +
       'naver_cta5_1%EC%B4%88%EB%AC%B4%EB%A3%8C%ED%92%80%EC%9D%B4.jpg" alt="자오선 무료 1초 풀이 안내 배너"></a></p>')
PID, KEY, PAL = "n87", "87", "dg_gold_s"   # 사주 첫걸음 = 나무 판 묶음(EL_SET 나무), n86 m_young_s·n85·n84와 다른 판

# ───────── 계산값과 검산 (engine/engine.py)
import datetime as D
sys.path.insert(0, os.path.join(SITE, "engine")); import engine as E
EX = D.datetime(1994, 9, 13, 8, 40)                          # 예시: 양력 1994년 9월 13일 오전 8시 40분
R = E.compute_saju(EX)
assert R["팔자"] == {"년주": "甲戌", "월주": "癸酉", "일주": "壬寅", "시주": "甲辰"}
assert R["일간"] == "壬" and R["일간_오행"] == "水"
assert R["오행분포"] == {"木": 3, "火": 0, "土": 2, "金": 1, "水": 2}
eight = "".join(R["팔자"][k] for k in ("년주", "월주", "일주", "시주"))
assert [c for c in eight if E.GAN_OHENG.get(c, E.JI_OHENG.get(c)) == "木"] == list("甲寅甲")
assert [c for c in eight if E.JI_OHENG.get(c) == "土" and c in E.JI_OHENG] == list("戌辰")
assert [c for c in eight if E.GAN_OHENG.get(c, E.JI_OHENG.get(c)) == "水"] == list("癸壬")
T94 = {n: t for n, _, t in E.get_solar_terms_kst(1994)}
assert T94["백로"] < D.datetime(1994, 9, 13, 8, 40, tzinfo=T94["백로"].tzinfo) < T94["한로"]   # 酉 달 = 백로~한로 전
T96 = {n: t for n, _, t in E.get_solar_terms_kst(1996)}
assert (T96["입동"].month, T96["입동"].day, T96["입동"].hour, T96["입동"].minute) == (11, 7, 12, 26)
assert E.compute_saju(D.datetime(1996, 11, 7, 7, 30))["팔자"]["월주"] == "戊戌"
assert E.compute_saju(D.datetime(1996, 11, 7, 18, 30))["팔자"]["월주"] == "己亥"
assert E.compute_saju(D.datetime(1996, 11, 7, 7, 30))["팔자"]["일주"] == E.compute_saju(D.datetime(1996, 11, 7, 18, 30))["팔자"]["일주"] == "戊申"
assert E.compute_saju(D.datetime(1994, 9, 13, 23, 30))["팔자"]["일주"] == "癸卯"                        # 밤 11시부터 다음 날(자오선 기준)
assert E.compute_saju(D.datetime(1994, 9, 13, 23, 30), ja_si_next_day=False)["팔자"]["일주"] == "壬寅"  # 자정부터 새 날로 보면 그대로
print("여덟 글자·절기 엔진으로 다시 확인")

# ───────── 본문 (n47 문장을 옮기지 않았다)
head = ["<b>사주 보는 법은 여덟 글자 가운데 일간 하나를 먼저 찾고, 계절과 오행 개수 순서로 넓혀 가는 거예요.</b>",
        "만세력에 생일을 넣으면 한자 여덟 개가 네 줄로 나와요. 처음엔 여덟 개를 한꺼번에 읽지 않아도 돼요.",
        "<b>오늘은 한 사람의 여덟 글자를 처음부터 끝까지 같이 세어 볼게요. 따라 세고 나면 내 사주도 같은 순서로 볼 수 있어요.</b>",
        "2026년 11월 5일 기준으로 정리한 내용이에요."]
toc_q = ["만세력 화면에서 여덟 글자는 어디에 있을까요?", "사주 보는 법 첫 단계, 나를 뜻하는 글자는 어느 칸일까요?",
         "태어난 달 글자로 어떤 계절에 태어났는지 볼 수 있을까요?", "오행 개수를 세면 무엇이 보일까요?",
         "처음 배울 때 예시부터 따라 하면 왜 덜 헷갈릴까요?", "자주 묻는 질문"]
sec1 = P("<b>여덟 글자는 네 기둥에 두 글자씩 놓여 있어요.</b>",
         "태어난 해, 달, 날, 시가 기둥 하나씩이고, 기둥마다 위 글자(천간) 하나와 아래 글자(지지) 하나가 있어요.",
         "만세력 앱은 대부분 오른쪽부터 해, 달, 날, 시 순서로 세워요. 그래서 왼쪽 끝이 시 기둥이에요.") + \
       P("🔎 <b>예시 한 명을 정해 볼게요.</b>",
         "양력 1994년 9월 13일 오전 8시 40분에 태어난 사람이에요.",
         "이 사람의 여덟 글자는 해 甲戌, 달 癸酉, 날 壬寅, 시 甲辰이에요.",
         "아래 네 단계를 이 여덟 글자 하나로 끝까지 따라가 볼게요.") + "[[L]]"
sec2 = P("<b>날 기둥의 위 글자예요. 이 글자를 일간(日干)이라고 하고, 사주에서 '나'를 뜻하는 글자로 봐요.</b>",
         "예시의 날 기둥은 壬寅이니 일간은 壬(임)이에요. 임은 물 기운이고, 넓게 흐르는 강물에 자주 비유해요.",
         "해 기둥과 시 기둥에도 甲이 있지만, 이건 내가 아니라 내 둘레의 기운으로 봐요. 처음 읽을 때 가장 많이 헷갈리는 곳이에요.") + \
       P("일간은 열 가지뿐이라 한 줄이면 찾아요.",
         "나무는 甲·乙, 불은 丙·丁, 흙은 戊·己, 쇠는 庚·辛, 물은 壬·癸예요.") + MID
sec3 = P("<b>네, 달 기둥 아래 글자가 태어난 계절을 알려 줘요.</b>",
         "예시의 달 기둥 아래 글자는 酉(유)예요. 酉 달은 백로부터 한로 전까지라 가을 한가운데예요.",
         "강물인 壬이 서늘한 가을에 태어난 셈이에요. 같은 壬이라도 여름생인지 겨울생인지에 따라 풀이가 다르게 나와요.") + \
       P("⚠️ <b>달 글자는 1일이 아니라 절기 시각에 바뀌어요.</b>",
         "1996년 11월 7일은 낮 12시 26분이 입동이었어요. 같은 날 오전 7시 30분생은 달 기둥이 戊戌, 저녁 6시 30분생은 己亥예요.",
         "날 기둥은 둘 다 戊申이라 일간은 같지만, 한 사람은 늦가을생이고 한 사람은 초겨울생이 돼요.",
         "생일이 절기 날짜와 겹친다면 태어난 시각까지 꼭 넣어 보세요.") + "[[C]]"
sec4 = P("<b>여덟 글자를 다섯 기운으로 나눠 세면, 많이 쓰는 기운과 덜 쓰는 기운이 보여요.</b>",
         "예시를 세어 볼게요. 甲·寅·甲은 나무, 戌·辰은 흙, 酉는 쇠, 癸·壬은 물이에요.",
         "모으면 나무 3, 흙 2, 물 2, 쇠 1, 불 0이에요.") + "[[V]]" + \
       P("불이 0이라고 열정이 없다는 뜻은 아니에요. 지금까지 덜 꺼내 쓴 쪽이라고 읽으면 돼요.",
         "나무가 셋으로 가장 많으니, 일간 壬의 물이 나무 쪽으로 흘러가는 모양이에요.",
         "물이 나무를 키우는 사이라서, 하고 싶은 말이나 만들고 싶은 것으로 힘이 잘 나가는 편이라고 봐요.")
sec5 = P("🧠 <b>처음 배울 때는 규칙 설명보다 다 풀린 예시 하나가 빨라요.</b>",
         "교육심리학자 스웰러와 쿠퍼는 1985년, 대수 문제를 배우는 학생들을 두 무리로 나눴어요.",
         "한 무리는 문제를 직접 풀었고, 다른 무리는 풀이가 다 적힌 예시를 따라 읽었어요.",
         "예시를 따라 읽은 무리가 비슷한 문제를 더 빨리, 덜 틀리게 풀었어요.",
         "새로 배울 때는 머릿속 여유가 작아서, 길을 찾느라 쓰는 힘을 예시가 덜어 주기 때문이에요.",
         "그래서 이 글도 규칙보다 한 사람의 여덟 글자를 먼저 끝까지 셌어요.",
         '📚 <b>출처 1</b>: <a href="https://doi.org/10.1207/s1532690xci0201_3">Sweller &amp; Cooper (1985), The Use of Worked Examples as a Substitute for Problem Solving in Learning Algebra, Cognition and Instruction</a>',
         '📚 <b>출처 2</b>: <a href="https://astro.kasi.re.kr/life/pageView/5">한국천문연구원 천문우주지식정보, 음양력 변환</a>') + \
       P("🌱 <b>마음 코치 정월의 질문</b>", "내 여덟 글자에서 가장 많은 기운은<br>요즘 어디에 가장 많이 쓰이고 있나요?",
         "🔸 0개인 기운이 있다면<br>이번 주에 아주 작게 꺼내 볼 자리는 어디일까요?") + \
       P("✔️ <b>이번 주에 따라 세어 볼 것</b>",
         "1. 만세력에서 내 날 기둥 위 글자, 일간 하나를 찾아 적어 두세요.",
         "2. 달 기둥 아래 글자로 내가 어느 계절에 태어났는지 적어 보세요.",
         "3. 여덟 글자를 다섯 기운으로 나눠 세고, 가장 많은 것과 0개인 것을 한 줄로 적어 두세요.")
sec6 = P("<b>Q. 밤 11시 넘어 태어났는데 앱마다 일간이 달라요.</b>",
         "A. 밤 11시부터 새 날로 보는 방식과 자정부터 새 날로 보는 방식이 있어서예요.",
         "예시와 같은 날 밤 11시 30분생이라면, 밤 11시부터 새 날로 볼 때 날 기둥이 癸卯라 일간이 癸예요. 자정부터 보면 壬寅 그대로예요.",
         "자오선은 밤 11시부터 다음 날로 봐요.") + \
       P("<b>Q. 태어난 시를 모르면요?</b>",
         "A. 시 기둥을 뺀 여섯 글자로도 1단계와 2단계는 그대로 할 수 있어요. 일간과 달 기둥은 시가 없어도 나와요.",
         "다만 생일이 절기 날이라면 달 기둥이 시각에 따라 갈릴 수 있으니, 출생증명서나 산모수첩을 한 번 찾아보세요.") + \
       P("<b>Q. 음력 생일만 알아요.</b>",
         "A. 한국천문연구원 음양력 변환에서 양력으로 바꾼 뒤 넣어 보세요. 사주의 달 글자는 음력 달이 아니라 절기로 정해져요.") + \
       P("<b>Q. 오행이 고르게 있어야 좋은 사주인가요?</b>",
         "A. 고르면 꺼내 쓸 도구가 여럿이고, 한쪽이 많으면 그 도구를 깊게 쓰는 편이에요. 어느 쪽이 낫다기보다 쓰는 방법이 달라요.")
tail = P("여러분 여덟 글자에서 0개인 기운은 무엇이었나요?", "나무, 불, 흙, 쇠, 물 가운데 하나만 댓글로 남겨 주세요.") + \
       '<p><b>👇 만세력 화면 세 곳과 앱마다 시주가 다른 이유가 궁금하다면, 만세력 보는 법 3곳, 일간·오행과 앱마다 시주가 다른 이유</b></p>'
secs = [sec1, sec2, sec3, sec4, sec5, sec6]

def _have(n): return os.path.exists(os.path.join(HERE, "img", n))
def build():
    for d_ in ("wide", "m1280", "master"): os.makedirs(os.path.join(HERE, "img", d_), exist_ok=True)
    c = V.Ctx(PAL); made = []
    a4 = f"wide/naver_z{KEY}_a4.jpg"
    if not _have(a4):
        V.render(PID + "_new", {"d": "N", "el": "나무", "kick": "사주 보는 법", "hook": ["여덟 글자", "4단계로 읽기"], "sub": "예시 한 명으로 끝까지",
                                "items": ["일간", "계절", "오행 개수"]}, os.path.join(HERE, "img", a4), PAL)
    made.append(a4)
    nm = {"L": f"naver_z{KEY}_l7.jpg", "C": f"naver_z{KEY}_c7.jpg", "V": f"naver_z{KEY}_v7.jpg"}
    if not _have(nm["L"]):
        DGB.ladder(nm["L"], c, "사주 읽는 네 단계", [("1단계", "날 기둥 위 글자, 일간 찾기"), ("2단계", "달 기둥 아래 글자로 계절 보기"),
                                                ("3단계", "여덟 글자를 다섯 기운으로 세기"), ("4단계", "가장 많은 기운과 0개인 기운 한 줄로 적기")],
                   "예시 1994.9.13 오전 8시 40분 · 자오선 계산")
    if not _have(nm["C"]):
        DGC.compare(nm["C"], c, "같은 날, 다른 달 기둥", ("오전 7시 30분생", "저녁 6시 30분생"),
                    [("달 기둥", "戊戌", "己亥"), ("계절", "늦가을, 흙의 달", "초겨울, 물의 달"), ("날 기둥", "戊申", "戊申")],
                    "1996년 11월 7일 입동 낮 12시 26분 · 자오선 계산", 1)
    if not _have(nm["V"]):
        DGC.vbar(nm["V"], c, "예시 여덟 글자, 오행 개수", [("나무", 3, True), ("불", 0, False), ("흙", 2, False), ("쇠", 1, False), ("물", 2, False)],
                 3, "나무 3이 가장 많고, 불 0은 덜 꺼내 쓴 기운이에요", "1994.9.13 오전 8시 40분 · 자오선 계산", fmt="{:.0f}")
    import fullbleed as FBL
    plan_p = os.path.join(HERE, "fullbleed_plan.json"); plan = json.load(open(plan_p, encoding="utf-8")) if os.path.exists(plan_p) else {}
    rows = []
    for pos, k in enumerate("LCV", 1):
        f = nm[k][:-4] + "f.jpg"
        if not _have(f):
            r, why = FBL.convert(nm[k], [os.path.join(HERE, "img"), os.path.join(HERE, "img", "m1280")]); assert r, (nm[k], why)
        rows.append({"pos": pos, "old": nm[k], "new": f}); made.append(nm[k]); nm[k] = f
        reg_ = json.load(open(DG.REG, encoding="utf-8")); reg_[f] = reg_[rows[-1]["old"]]; json.dump(dict(sorted(reg_.items())), open(DG.REG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    plan[PID] = rows; json.dump(plan, open(plan_p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    made += list(nm.values())
    alt = {"L": "사주 읽는 네 단계 그림. 1단계 날 기둥 위 글자 일간 찾기, 2단계 달 기둥 아래 글자로 계절 보기, 3단계 여덟 글자를 다섯 기운으로 세기, 4단계 가장 많은 기운과 0개인 기운 적기",
           "C": "같은 날 다른 달 기둥 그림. 1996년 11월 7일 입동 낮 12시 26분 전 오전 7시 30분생은 달 기둥 戊戌 늦가을, 뒤 저녁 6시 30분생은 己亥 초겨울, 날 기둥은 둘 다 戊申",
           "V": "예시 여덟 글자 오행 개수 막대그림. 1994년 9월 13일 오전 8시 40분생은 나무 3, 불 0, 흙 2, 쇠 1, 물 2"}
    body = P(*head) + P("<b>📌 따라 읽을 순서</b>", *[f"{i + 1}. {q}" for i, q in enumerate(toc_q)])
    for i, (q, s) in enumerate(zip(toc_q, secs)):
        for k in "LCV": s = s.replace(f"[[{k}]]", IMG(nm[k], alt[k]))
        body += H(f"{i + 1}. {q}") + s
    body += tail + CTA
    import copy_rules as CR
    for w in ("재미로", "상담", "—", "안녕하세요, 자오선의 정월이에요", "결론부터 말씀드릴게요", "생년월일만 넣으면 1초", "한 줄 요약", "이 글의 순서") + tuple(CR.금지어):
        assert w not in re.sub(r"<[^>]+>", " ", body), w
    for f in made:   # 사이트 사본(K-069)
        dst = os.path.join(SITE, "public", "naver", "img", f); os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy(os.path.join(HERE, "img", f), dst)
    return body, a4, made

TITLE = "사주 보는 법, 만세력 여덟 글자를 예시 한 명으로 읽는 4단계"
TAGS = ["사주보는법", "사주", "사주일간", "일간", "사주팔자보는법", "만세력", "오행", "절기", "사주공부", "자오선"]
REL = {"id": "n75", "title": "만세력 보는 법 3곳, 일간·오행과 앱마다 시주가 다른 이유",
       "phrase": "만세력 화면 세 곳과 앱마다 시주가 다른 이유가 궁금하다면, 만세력 보는 법 3곳, 일간·오행과 앱마다 시주가 다른 이유",
       "url": "https://blog.naver.com/zaoseon/224463601442"}
KW_VOL = json.load(open(os.path.join(SITE, "data", "keywords", "kw_volume.json"), encoding="utf-8"))["posts"]["n87"]["씨앗"]
INTENT = {"keywords": ["사주 보는 법", "사주 일간", "일간", "사주팔자 보는 법"],
          "keyword_src": "kw-volume 작업(data/keywords/kw_volume.json posts.n87) 월 검색량 · n47 조회 순위(재발행 일정 '새 글로 다시 쓰기')",
          "intent": "해 보고 싶다", "intent_note": "만세력에 나온 여덟 글자를 처음 읽을 때 어디부터 어떤 순서로 보는지, 한 사람 예시로 끝까지 따라 하기",
          "first3": "사주 보는 법은 여덟 글자 가운데 일간 하나를 먼저 찾고, 계절과 오행 개수 순서로 넓혀 가는 거예요.",
          "answer_keys": ["사주 보는 법", "일간", "오행"],
          "order": toc_q[:5], "images": ["네 단계(ladder)", "같은 날 다른 달 기둥(compare, 엔진 절기 계산)", "예시 오행 개수(vbar, 엔진 계산)"],
          "related": "n75", "cta": PID, "experience": [], "applied": True,
          "differs_from_n47": "제목·도입(정의 + 순서 직답)·소제목 순서·세 가지 설명과 열 글자 비유 나열 대신 예시 한 명(1994.9.13 오전 8시 40분, 甲戌 癸酉 壬寅 甲辰)을 네 단계로 끝까지 세기·절기 경계 예시(1996.11.7 입동)·밤 11시 일간 차이 예시·그림 유형(ladder·compare·vbar)·심리 개념(자기효능감 → 풀이된 예시 효과, Sweller & Cooper 1985)·출처·연결글(n14 → n75)"}

if __name__ == "__main__":
    body, a4, made = build()
    reg = json.load(open(MP.REG, encoding="utf-8"))
    assert PID not in reg or not reg[PID].get("done"), "이미 예약 끝난 글"
    reg[PID] = dict(dt="2027-02-01T18:00:00", dt_tbd="CT가 정함(재발행 일정 11/18 08:00 자리, 서브 배너 링크 고침 확인 뒤). 이 날짜는 자리값", title=TITLE, tags=TAGS, body=body,
                    cover=a4, related=REL, thumbs=None, cid=None, clips=None, category="운명학 사전", done=False, kw_vol=KW_VOL,
                    k131="n87 11/5(K-151 새 글)", source="build_naver_87.py (n47 주제 새 글, n47 그대로)")
    json.dump(reg, open(MP.REG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    ic = json.load(open(os.path.join(HERE, "intent_cards.json"), encoding="utf-8")); ic["cards"][PID] = INTENT
    json.dump(ic, open(os.path.join(HERE, "intent_cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    v = reg[PID]
    MP.write_page(PID, D.datetime.fromisoformat(v["dt"]), v["title"], v["tags"], v["body"], None, v["cover"], v["related"], v["category"])
    MP.write_index()
    import k151_check as K
    print(PID, len(TITLE), "자 제목 · 본문 글자", len(re.sub(r"<[^>]+>|&nbsp;", "", body)), "· 사진", made, "· K 검사", K.check(PID, v))
