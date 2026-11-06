"""네이버 n88: 점성술과 사주 차이 새 글 (CT 11/4 19:40 → ① 최우선, 대표 11/4 19:28 재발행 일정 '새 글로 다시 쓰기' n11 → n88, 11/19 08:00 자리).
- 왜: 노출 안 되는 옛 글 n11(여섯 가지 운명학을 겹쳐 읽는 자오선)을 새 글로. n11은 건드리지 않는다(K-147·K-178).
- 검색어: data/keywords/kw_volume.json posts.n88(kw-volume 11/6 11:55) — 점성술 3,430 · 사주종류 340 · 사주점성술 25.
  11/5 첫 요청(운세종류 70·운명학 25)은 100 미만이라 11/6 넓혀 다시 받음. n11의 '자오선 소개' 대신 검색되는 말(점성술·사주 차이)로 쓴다.
- 다르게 쓴 것(K-151): n11의 여섯 체계 나열·이름 뜻·회사 소개 대신, 예시 한 명(양력 1997.4.26 오전 10시 30분, 서울)을
  사주(丁丑 甲辰 戊戌 丁巳, 흙 4·불 3·나무 1·쇠 0·물 0)와 점성술(행성 7개: 흙 4·불 2·공기 1·물 0, 태양 황소·달 사수·상승 게)로
  같이 세어 '재료·같게 말하는 곳·다르게 말하는 곳' 세 가지로 읽는 글. 심리 개념(통제 소재 Rotter 1966 → 군중의 지혜 Galton 1907),
  그림 유형(versus·dumbbell·triad, n11은 소개 그림·표·순서), 연결글(n01 → n82 발행·노출 '예'). 소제목 틀(한 줄 요약·이 글의 순서·생년월일만 넣으면 1초) 안 씀.
- 계산: engine/engine.py compute_saju · engine/astro.py compute_astrology(스위스 천체력). 아래 assert.
- 출처 2개(K-162, 11/6 확인): Galton (1907) Vox populi, Nature 75, 450–451(DOI 10.1038/075450a0, 787장·중앙값 1,207파운드·실제 1,198파운드는
  Wallis 2014 arXiv 1410.3989로 확인) · Astrodienst 스위스 천체력 안내(astro.com/swisseph, 검색 결과로 주소 확인).
- 날짜: CT가 정한다. pages.json dt 는 자리값, dt_tbd 로 표시.
사용: SITE=<zaoseon-site> python3 naver/build_naver_88.py"""
import os, sys, json, re, html, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "pipeline"))
os.chdir(HERE)
import cover_v3 as V, make_page as MP, diagrams_k131 as DG, diagrams_k131c as DGC
SITE = os.environ.get("SITE", "/home/claude/zaoseon-site")
RAW = "https://raw.githubusercontent.com/zaoseon/sns-images/main/naver/img/"
BL = "<p>&nbsp;</p>"
def P(*ls): return "".join(f"<p>{l}</p>" for l in ls) + BL
def IMG(name, alt): return f'<p><img src="{RAW}{name}" alt="{html.escape(alt, quote=True)}"></p>' + BL
def H(t): return f"<p><b>{t}</b></p>"
MID = ('<table style="width:100%;max-width:440px;margin:0 auto;border-collapse:collapse"><tbody>'
       '<tr><td style="padding:12px 10px;text-align:center;border:1px solid #d0d0d0"><b>생일을 넣으면 내 여덟 글자가 바로</b></td></tr>'
       '<tr><td style="padding:12px 10px;text-align:center;border:1px solid #d0d0d0"><span style="color:#9a9a9a">[ 1997 . 04 . 26 ]</span></td></tr>'
       '<tr><td style="padding:12px 10px;text-align:center;border:1px solid #d0d0d0"><b><a href="https://zaoseon.com/?utm_source=naver&amp;utm_medium=mid#free">내 태어난 날 글자 보기 →</a></b></td></tr>'
       '</tbody></table>' + BL)
CTA = ('<p><a href="https://zaoseon.com/?utm_source=naver&utm_medium=cta#free"><img src="' + RAW +
       'naver_cta5_1%EC%B4%88%EB%AC%B4%EB%A3%8C%ED%92%80%EC%9D%B4.jpg" alt="자오선 무료 1초 풀이 안내 배너"></a></p>')
PID, KEY, PAL = "n88", "88", "y_black_s"   # 예시의 흙 = 흙 판 묶음(EL_SET 흙), n85 y_olive_s·n81 y_olive 와 다른 판

# ───────── 계산값과 검산 (engine/engine.py · engine/astro.py)
import datetime as D
sys.path.insert(0, os.path.join(SITE, "engine")); import engine as E, astro as A
EX = D.datetime(1997, 4, 26, 10, 30)                       # 예시: 양력 1997년 4월 26일 오전 10시 30분, 서울
R = E.compute_saju(EX)
assert R["팔자"] == {"년주": "丁丑", "월주": "甲辰", "일주": "戊戌", "시주": "丁巳"}
assert R["일간"] == "戊" and R["일간_오행"] == "土"
assert R["오행분포"] == {"木": 1, "火": 3, "土": 4, "金": 0, "水": 0}
eight = "".join(R["팔자"][k] for k in ("년주", "월주", "일주", "시주"))
ohg = lambda ch: E.GAN_OHENG.get(ch, E.JI_OHENG.get(ch))
assert [c for c in eight if ohg(c) == "土"] == list("丑辰戊戌")
assert [c for c in eight if ohg(c) == "火"] == list("丁丁巳")
AS = A.compute_astrology(EX)                               # 서울 위경도 기본값
assert (AS["태양궁"], AS["달별자리"], AS["상승궁"]) == ("황소자리", "사수자리", "게자리")
assert AS["원소분포"] == {"불": 2, "흙": 4, "공기": 1, "물": 0}
pl = AS["행성배치"]
assert [k for k, v in pl.items() if v["원소"] == "흙"] == ["태양", "수성", "금성", "화성"]
assert [k for k, v in pl.items() if v["원소"] == "불"] == ["달", "토성"] and pl["목성"]["별자리"] == "물병자리"
assert pl["화성"]["별자리"] == "처녀자리" and all(pl[k]["별자리"] == "황소자리" for k in ("태양", "수성", "금성"))
PCT = {"흙": (round(4 / 8 * 100), round(4 / 7 * 100)), "불": (round(3 / 8 * 100), round(2 / 7 * 100)), "물": (0, 0)}
assert PCT == {"흙": (50, 57), "불": (38, 29), "물": (0, 0)}
print("여덟 글자·행성 일곱 개 엔진으로 다시 확인")

# ───────── 본문 (n11 문장을 옮기지 않았다)
head = ["<b>점성술과 사주는 같은 생일을 서로 다른 재료로 읽는 방식이에요.</b>",
        "사주는 절기 달력으로 태어난 해·달·날·시를 여덟 글자로 바꾸고, 점성술은 태어난 순간 하늘에 있던 행성의 자리를 읽어요.",
        "<b>재료가 다르니 말이 다를 때도 있지만, 같은 사람을 두고 똑같은 말을 하는 곳도 꽤 나와요.</b>",
        "오늘은 한 사람의 생일을 두 방식으로 같이 세어서, 같은 말과 다른 말을 나눠 볼게요. 2026년 11월 6일 기준으로 정리한 내용이에요."]
toc_q = ["점성술과 사주 차이, 무엇을 재료로 읽을까요?", "같은 생일 하나를 두 방식으로 세면 어떻게 나올까요?",
         "두 방식이 똑같이 말하는 곳은 어디일까요?", "말이 갈리는 곳은 틀린 걸까요, 고를 수 있는 걸까요?",
         "왜 한 방식보다 겹쳐 읽는 쪽이 덜 치우칠까요?", "자주 묻는 질문"]
sec1 = P("<b>사주는 달력의 글자를, 점성술은 하늘의 자리를 재료로 써요.</b>",
         "사주는 한 해를 스물네 절기로 나눈 달력 위에서 태어난 해·달·날·시를 기둥 넷, 글자 여덟 개로 바꿔요. 그 글자를 나무·불·흙·쇠·물 다섯 기운으로 세어 읽어요.",
         "점성술은 태어난 순간 태양·달·수성·금성·화성·목성·토성이 열두 별자리 가운데 어디에 있었는지를 봐요. 그 자리를 불·흙·공기·물 네 원소로 묶어 읽어요.") + "[[L]]" + \
       P("한 가지 더 달라요. 점성술은 <b>태어난 곳</b>도 넣어요.",
         "같은 시각이라도 서울과 부산은 동쪽 지평선에 걸린 별자리가 조금 달라서, 첫인상을 뜻하는 상승궁이 바뀔 수 있어요. 사주는 태어난 곳보다 시각을 더 따져요.")
sec2 = P("🔎 <b>예시 한 명을 정해 볼게요. 양력 1997년 4월 26일 오전 10시 30분, 서울에서 태어난 사람이에요.</b>",
         "사주로 세면 여덟 글자는 해 丁丑, 달 甲辰, 날 戊戌, 시 丁巳예요. 나를 뜻하는 날 기둥 위 글자(일간)는 戊, 큰 산 같은 흙이에요.",
         "다섯 기운은 흙 4, 불 3, 나무 1, 쇠 0, 물 0이에요. 丑·辰·戊·戌이 흙이고 丁·丁·巳가 불이에요.") + \
       P("점성술로 세면 태양·수성·금성이 황소자리, 화성이 처녀자리라 흙이 넷이에요.",
         "달은 사수자리, 토성은 양자리라 불이 둘, 목성이 물병자리라 공기가 하나예요. 물은 0이에요.",
         "태양 별자리는 황소자리, 서울에서 태어났다면 상승궁은 게자리로 나와요.") + MID
sec3 = P("<b>흙이 가장 많고 물이 0이라는 말은 두 방식이 똑같이 해요.</b>",
         "사주는 여덟 글자 가운데 흙이 넷이라 절반, 점성술은 행성 일곱 개 가운데 흙이 넷이라 절반이 조금 넘어요.",
         "물은 두 방식 모두 0이에요. 불도 사주 셋, 점성술 둘로 둘째 자리예요.") + "[[V]]" + \
       P("두 방식이 같은 말을 하는 곳은 오래 따라다닌 성향이라고 봐요.",
         "이 사람이라면 천천히 쌓고, 한번 정한 건 오래 지키는 쪽이에요. 급하게 정하라는 말에 '하루만 생각해 볼게'라고 답하는 장면이 자주 나올 거예요.",
         "이건 바꿔야 할 단점이 아니라 내가 가장 잘 쓰는 도구라고 보면 돼요.")
sec4 = P("<b>갈리는 곳은 틀린 곳이 아니라, 상황에 따라 내가 고를 수 있는 곳이에요.</b>",
         "사주는 흙이 가득해 단단한데, 점성술의 달은 사수자리예요. 달은 속마음을 뜻해서, 겉으로는 차분해도 속으로는 멀리 떠나 보고 싶은 마음이 있다고 읽어요.",
         "사주는 물이 0인데 상승궁은 물 원소인 게자리예요. 처음 만난 사람에게는 오히려 다정하고 잘 챙기는 사람으로 보일 수 있어요.") + "[[C]]" + \
       P("그래서 같은 사람에게 두 장면이 다 나와요.",
         "평소엔 계획대로 가다가도, 마음이 답답한 주에는 '이번 주말에 혼자 바다 보고 올게'라고 말하는 사람이요.",
         "어느 쪽이 진짜 나인지 고르지 않아도 돼요. 지금 상황에 어느 얼굴을 꺼낼지는 내가 정할 수 있어요.")
sec5 = P("🧠 <b>한 사람의 눈은 치우치지만, 여러 눈을 겹치면 치우침이 덜해져요.</b>",
         "통계학자 골턴은 1906년 영국의 한 가축 시장에서 황소 한 마리 무게를 맞히는 대회 표 787장을 모았어요.",
         "한 사람 한 사람의 짐작은 크게 빗나간 것도 많았는데, 가운데 값은 1,207파운드였어요. 실제 무게 1,198파운드와 1%도 차이가 나지 않았어요.",
         "각자의 치우침이 서로 다른 쪽으로 빗나가서, 겹쳐 놓으면 서로를 덜어 준 거예요.",
         "운명학은 무게를 재는 저울이 아니에요. 다만 한 방식만 보면 그 방식의 시선으로만 나를 보게 되는 건 비슷해요.",
         "그래서 저는 같은 말은 오래 가는 성향으로, 다른 말은 고를 수 있는 곳으로 나눠서 읽어요.",
         '📚 <b>출처 1</b>: <a href="https://doi.org/10.1038/075450a0">Galton (1907), Vox Populi, Nature 75, p.450</a>',
         '📚 <b>출처 2</b>: <a href="https://www.astro.com/swisseph/swisseph.htm">Astrodienst, Swiss Ephemeris 행성 위치 계산 안내</a>') + \
       P("🌱 <b>마음 코치 정월의 질문</b>", "두 방식이 똑같이 말한 내 성향은<br>요즘 어디에서 가장 잘 쓰이고 있나요?",
         "🔸 말이 갈린 곳이 있다면<br>이번 주에 어느 얼굴을 꺼내 보고 싶나요?") + \
       P("✔️ <b>이번 주에 겹쳐 세어 볼 것</b>",
         "1. 만세력에서 내 여덟 글자를 다섯 기운으로 세고, 가장 많은 것과 0개인 것을 적어 두세요.",
         "2. 출생 차트에서 행성 일곱 개의 별자리를 네 원소로 묶어 세어 보세요.",
         "3. 두 결과에서 같은 말 하나, 다른 말 하나를 한 줄씩 적어 보세요.")
sec6 = P("<b>Q. 태양 별자리만 알아도 비교할 수 있나요?</b>",
         "A. 태양 하나는 행성 일곱 개 가운데 하나라서 한쪽 말만 듣는 셈이에요. 예시도 태양은 황소자리 흙이지만, 달은 사수자리 불이었어요. 태어난 시각을 넣어 달과 상승궁까지 보면 비교가 훨씬 또렷해져요.") + \
       P("<b>Q. 사주의 흙과 점성술의 흙은 같은 뜻인가요?</b>",
         "A. 이름은 같아도 묶는 방식이 달라요. 사주의 흙은 계절과 계절 사이를 잇는 기운이고, 점성술의 흙은 황소·처녀·염소자리를 묶은 원소예요. 둘 다 '지키고 쌓는 쪽'으로 읽는 일이 많아서 겹쳐 보기 좋아요.") + \
       P("<b>Q. 태어난 시를 모르면요?</b>",
         "A. 사주는 시 기둥을 뺀 여섯 글자로, 점성술은 달과 상승궁을 뺀 나머지로 볼 수 있어요. 다만 달은 하루에 반 별자리쯤 움직여서, 시각을 모르면 달 별자리가 갈릴 수 있어요.") + \
       P("<b>Q. 자오선은 두 가지만 겹치나요?</b>",
         "A. 사주와 점성술에 자미두수·당사주·하락이수·수비학까지 여섯 가지를 같은 생일로 세어 겹쳐요. 이 글은 그중 가장 많이 찾는 두 가지로 보여 드렸어요.")
tail = P("여러분은 두 방식이 똑같이 말한 기운이 있었나요?", "흙, 불, 물 같은 기운 이름 하나만 댓글로 남겨 주세요.") + \
       '<p><b>👇 물고기자리 한 별자리를 2027년 하늘로 끝까지 읽어 본 예가 궁금하다면, 물고기자리 2027 운세, 해왕성 토성 떠난 해 달라지는 3가지</b></p>'
secs = [sec1, sec2, sec3, sec4, sec5, sec6]

def _have(n): return os.path.exists(os.path.join(HERE, "img", n))
def build():
    for d_ in ("wide", "m1280", "master"): os.makedirs(os.path.join(HERE, "img", d_), exist_ok=True)
    c = V.Ctx(PAL); made = []
    a4 = f"wide/naver_z{KEY}_a4.jpg"
    if not _have(a4):
        V.render(PID + "_new", {"d": "N", "el": "흙", "kick": "점성술과 사주", "hook": ["같은 생일", "두 방식으로"], "sub": "예시 한 명으로 겹쳐 읽기",
                                "items": ["재료", "같은 말", "다른 말"]}, os.path.join(HERE, "img", a4), PAL)
    made.append(a4)
    nm = {"L": f"naver_z{KEY}_w8.jpg", "V": f"naver_z{KEY}_d7.jpg", "C": f"naver_z{KEY}_t7.jpg"}
    if not _have(nm["L"]):
        DGC.versus(nm["L"], c, "같은 생일, 다른 재료", "사주와 점성술",
                   ("사주", "태어난 해·달·날·시를 여덟 글자로 바꿔요.", "다섯 기운 개수로 읽어요."),
                   ("점성술", "태어난 순간 행성 일곱 개와 태어난 곳을 봐요.", "열두 별자리, 네 원소로 읽어요."),
                   "재료가 달라도 같은 사람을 그려요", "자오선 정리")
    if not _have(nm["V"]):
        DGC.dumbbell(nm["V"], c, "두 방식이 같게 말한 곳", [("흙", 50, 57), ("불", 38, 29), ("물", 0, 0)], ("사주 여덟 글자 중", "점성술 행성 일곱 개 중"),
                     "흙이 가장 많고 물은 0, 두 방식이 같은 말을 해요", "예시 1997.4.26 오전 10시 30분 서울 · 자오선 계산")
    if not _have(nm["C"]):
        DGC.triad(nm["C"], c, "겹쳐 읽으면 나오는 세 가지", [("재료", "달력의 글자와 하늘의 자리"), ("같은 말", "오래 따라다닌 성향"),
                                                       ("다른 말", "상황에 따라 내가 고를 수 있는 곳")], 2,
                  "달 사수자리·상승 게자리는 흙 사주와 다른 얼굴이에요", "예시 1997.4.26 오전 10시 30분 서울 · 자오선 계산")
    import fullbleed as FBL
    plan_p = os.path.join(HERE, "fullbleed_plan.json"); plan = json.load(open(plan_p, encoding="utf-8")) if os.path.exists(plan_p) else {}
    rows = []
    for pos, k in enumerate("LVC", 1):
        f = nm[k][:-4] + "f.jpg"
        if not _have(f):
            r, why = FBL.convert(nm[k], [os.path.join(HERE, "img"), os.path.join(HERE, "img", "m1280")]); assert r, (nm[k], why)
        rows.append({"pos": pos, "old": nm[k], "new": f}); made.append(nm[k]); nm[k] = f
        reg_ = json.load(open(DG.REG, encoding="utf-8")); reg_[f] = reg_[rows[-1]["old"]]; json.dump(dict(sorted(reg_.items())), open(DG.REG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    plan[PID] = rows; json.dump(plan, open(plan_p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    made += list(nm.values())
    alt = {"L": "같은 생일 다른 재료 그림. 사주는 절기 달력 위의 해·달·날·시를 여덟 글자로 바꿔 다섯 기운으로 읽고, 점성술은 태어난 순간 행성 일곱 개의 자리와 태어난 곳을 열두 별자리 네 원소로 읽어요",
           "V": "두 방식이 같게 말한 곳 그림. 1997년 4월 26일 오전 10시 30분 서울생은 흙이 사주 50%, 점성술 57%로 가장 많고 불은 38%와 29%, 물은 둘 다 0%",
           "C": "겹쳐 읽으면 나오는 세 가지 그림. 재료는 달력의 글자와 하늘의 자리, 같은 말은 오래 따라다닌 성향, 다른 말은 내가 고를 수 있는 곳"}
    body = P(*head) + P("<b>📌 같이 세어 볼 순서</b>", *[f"{i + 1}. {q}" for i, q in enumerate(toc_q)])
    for i, (q, s) in enumerate(zip(toc_q, secs)):
        for k in "LVC": s = s.replace(f"[[{k}]]", IMG(nm[k], alt[k]))
        body += H(f"{i + 1}. {q}") + s
    body += tail + CTA
    import copy_rules as CR
    for w in ("재미로", "상담", "—", "안녕하세요, 자오선의 정월이에요", "결론부터 말씀드릴게요", "생년월일만 넣으면 1초", "한 줄 요약", "이 글의 순서") + tuple(CR.금지어):
        assert w not in re.sub(r"<[^>]+>", " ", body), w
    for f in made:   # 사이트 사본(K-069)
        dst = os.path.join(SITE, "public", "naver", "img", f); os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy(os.path.join(HERE, "img", f), dst)
    return body, a4, made

TITLE = "점성술과 사주 차이, 같은 생일로 겹쳐 읽으면 보이는 3가지"
TAGS = ["점성술", "사주", "사주종류", "점성술사주", "별자리", "출생차트", "오행", "4원소", "운명학", "자오선"]
REL = {"id": "n82", "title": "물고기자리 2027 운세, 해왕성 토성 떠난 해 달라지는 3가지",
       "phrase": "물고기자리 한 별자리를 2027년 하늘로 끝까지 읽어 본 예가 궁금하다면, 물고기자리 2027 운세, 해왕성 토성 떠난 해 달라지는 3가지",
       "url": "https://blog.naver.com/zaoseon/224465940267"}
KW_VOL = json.load(open(os.path.join(SITE, "data", "keywords", "kw_volume.json"), encoding="utf-8"))["posts"]["n88"]["씨앗"]
INTENT = {"keywords": ["점성술", "사주 종류", "사주 점성술"],
          "keyword_src": "kw-volume 작업(data/keywords/kw_volume.json posts.n88, 11/6 다시 받음) 월 검색량 · n11 조회 순위(재발행 일정 '새 글로 다시 쓰기')",
          "intent": "알고 싶다", "intent_note": "사주와 점성술이 무엇을 재료로 읽고 어디가 같고 다른지, 한 사람 예시로 두 방식을 나란히 세어 보기",
          "first3": "점성술과 사주는 같은 생일을 서로 다른 재료로 읽는 방식이에요.",
          "answer_keys": ["점성술", "사주", "재료"],
          "order": toc_q[:5], "images": ["재료 맞대기(versus)", "두 방식 기운 비율(dumbbell, 엔진 계산)", "겹쳐 읽는 세 가지(triad)"],
          "related": "n82", "cta": PID, "experience": [], "applied": True,
          "differs_from_n11": "제목·도입(정의 + 재료 차이 직답)·소제목 순서·여섯 체계 나열과 이름 뜻·회사 소개 대신 예시 한 명(1997.4.26 오전 10시 30분 서울, 丁丑 甲辰 戊戌 丁巳 · 황소·사수·게)을 두 방식으로 끝까지 세기·같은 말(흙 4, 물 0)과 다른 말(달 사수·상승 게)·그림 유형(versus·dumbbell·triad)·심리 개념(통제 소재 → 군중의 지혜, Galton 1907)·출처·연결글(n01 → n82)"}

if __name__ == "__main__":
    body, a4, made = build()
    reg = json.load(open(MP.REG, encoding="utf-8"))
    assert PID not in reg or not reg[PID].get("done"), "이미 예약 끝난 글"
    reg[PID] = dict(dt="2027-02-02T08:00:00", dt_tbd="CT가 정함(재발행 일정 11/19 08:00 자리). 이 날짜는 자리값", title=TITLE, tags=TAGS, body=body,
                    cover=a4, related=REL, thumbs=None, cid=None, clips=None, category="운명학 사전", done=False, kw_vol=KW_VOL,
                    k131="n88 11/6(K-151 새 글)", source="build_naver_88.py (n11 주제 새 글, n11 그대로)")
    json.dump(reg, open(MP.REG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    ic = json.load(open(os.path.join(HERE, "intent_cards.json"), encoding="utf-8")); ic["cards"][PID] = INTENT
    json.dump(ic, open(os.path.join(HERE, "intent_cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    v = reg[PID]
    MP.write_page(PID, D.datetime.fromisoformat(v["dt"]), v["title"], v["tags"], v["body"], None, v["cover"], v["related"], v["category"])
    MP.write_index()
    import k151_check as K
    print(PID, len(TITLE), "자 제목 · 본문 글자", len(re.sub(r"<[^>]+>|&nbsp;", "", body)), "· 사진", made, "· K 검사", K.check(PID, v))
