"""네이버 n86: 자미두수 명반 새 글 (CT 11/4 19:40 → ① 최우선, 대표 11/4 19:28 재발행 일정 '새 글로 다시 쓰기' n57 → n86, 11/17 08:00 자리).
- 왜: 노출 안 되는 옛 글 n57(자미두수 명반 보는 법, 내 명궁 찾는 표와 12궁·주성 14개)을 새 글로. n57은 건드리지 않는다(K-147·K-178).
- 검색어: tools/seo/kw_volume_request.json n86 → kw-volume 작업(data/keywords/kw_volume.json posts.n86) 값. 아래 KW_VOL.
- 다르게 쓴 것(K-151): 12궁·주성 14개 나열 대신 '명궁 한 칸 직접 세기' 3단계 + 실제 예시 한 명(엔진 계산) + 태어난 시 찾는 장면
  + 심리 개념(고정 마음가짐 → 대표 강점 새 방식으로 쓰기, Seligman 외 2005) + 그림 유형(quad·counter·exp, n57은 triad·compare).
  소제목 틀(한 줄 요약·이 글의 순서·생년월일만 넣으면 1초)을 쓰지 않는다(CT 11/4 21:05).
- 계산: engine/ziwei.py(오픈소스 iztro 대조 검증본) + korean_lunar_calendar. 아래 assert.
- 출처 2개(K-162, 11/5 확인): Seligman, Steen, Park & Peterson (2005) American Psychologist 60(5) 410-421 DOI 10.1037/0003-066X.60.5.410
  · 한국천문연구원 음양력 변환(n75에서 확인한 주소).
- 날짜: CT가 정한다. pages.json dt 는 자리값, dt_tbd 로 표시.
사용: SITE=<zaoseon-site> python3 naver/build_naver_86.py"""
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
       '<tr><td style="padding:12px 10px;text-align:center;border:1px solid #d0d0d0"><b>양력 생일을 넣으면 음력과 내 글자가 함께</b></td></tr>'
       '<tr><td style="padding:12px 10px;text-align:center;border:1px solid #d0d0d0"><span style="color:#9a9a9a">[ 1992 . 06 . 20 ]</span></td></tr>'
       '<tr><td style="padding:12px 10px;text-align:center;border:1px solid #d0d0d0"><b><a href="https://zaoseon.com/?utm_source=naver&amp;utm_medium=mid#free">내 태어난 날 글자 보기 →</a></b></td></tr>'
       '</tbody></table>' + BL)
CTA = ('<p><a href="https://zaoseon.com/?utm_source=naver&utm_medium=cta#free"><img src="' + RAW +
       'naver_cta5_1%EC%B4%88%EB%AC%B4%EB%A3%8C%ED%92%80%EC%9D%B4.jpg" alt="자오선 무료 1초 풀이 안내 배너"></a></p>')
PID, KEY, PAL = "n86", "86", "m_young_s"   # 자미(紫微)=보랏빛 별 → 물 판 묶음(EL_SET 물), n82 p_purple_s 와 다른 판

# ───────── 계산값과 검산 (engine/ziwei.py)
import datetime as D
sys.path.insert(0, os.path.join(SITE, "engine")); import ziwei as Z
JI = Z.JI
EX = D.datetime(1992, 6, 20, 14, 20)                       # 예시: 양력 1992년 6월 20일 오후 2시 20분
ly, lm, ld = Z._lunar(EX); si = Z._si_index(EX.hour); R = Z.compute_ziwei(EX)
assert (ly, lm, ld) == (1992, 5, 20)                         # 음력 5월 20일
assert si == 7 and JI[si] == "未"                            # 미시(오후 1시~3시)
assert Z._si_index((EX - D.timedelta(minutes=30)).hour) == 7 # 30분 당겨 보는 방식(오후 1시 50분)으로도 미시
zi_cell = (2 + (lm - 1)) % 12; assert JI[zi_cell] == "午"    # 자시 기준 칸: 1월 寅부터 한 칸씩 → 5월 午
assert [JI[(zi_cell - k) % 12] for k in range(1, 8)] == list("巳辰卯寅丑子亥")
assert R["명궁_지지"] == "亥" and R["명궁_주성들"] == ["太陰"] and R["신궁_지지"] == "丑"
assert JI[(Z.JI.index("亥") - 4) % 12] == "未" and R["재백궁_주성"] == "(주성 없음)"   # 재백궁은 명궁에서 거꾸로 네 칸
assert R["관록궁_주성"] == "太陽·天梁"
assert "섬세" in Z.STAR_MEANING["太陰"]
assert [JI[(2 + m - 1) % 12] for m in range(1, 13)] == list("寅卯辰巳午未申酉戌亥子丑")
# 아침(묘·진·사시) 저녁(유·술·해시)처럼 시진 여섯 개 범위만 알 때 명궁 후보는 여섯 칸으로 줄어든다(시진마다 다른 칸).
assert len({Z._ming_gong(lm, s) for s in range(6)}) == 6
assert Z._lunar(D.datetime(1991, 3, 10))[1] == 1 and Z._lunar(D.datetime(1992, 3, 10))[1] == 2   # 같은 양력 날, 다른 음력 달
EMPTY = D.datetime(1989, 3, 10, 16, 10); RE = Z.compute_ziwei(EMPTY)   # 명궁이 빈 예: 차성
assert RE["명궁_주성들"] == [] and RE["명궁_지지"] == "未" and RE["명궁_차성"] == ["太陽", "太陰"]
print("명궁·별 엔진으로 다시 확인")

# ───────── 본문 (n57 문장을 옮기지 않았다)
head = ["<b>자미두수 명반은 음력 생일과 태어난 시로 열두 칸에 별 14개를 놓은 표예요.</b>",
        "그 열두 칸 가운데 제일 먼저 찾는 칸이 명궁(命宮)이에요. 음력으로 태어난 달과 태어난 시만 알면 손가락으로 셀 수 있어요.",
        "<b>앱마다 명반 그림이 달라 어디부터 봐야 할지 몰랐다면, 오늘은 내 명궁 한 칸만 직접 찾아 보세요.</b>",
        "2026년 11월 5일 기준으로 정리한 내용이에요."]
toc_q = ["자미두수 명반의 열두 칸은 어떻게 생겼을까요?", "명궁은 음력 생월과 태어난 시로 어떻게 셀까요?",
         "태어난 시를 모르면, 엄마한테 물어봐야 할까요?", "명궁 별을 읽은 다음엔 무엇을 해 볼까요?", "자주 묻는 질문"]
sec1 = P("<b>명반은 열두 글자 칸이 시계처럼 둘러선 판이에요.</b>",
         "칸마다 子·丑·寅 같은 땅의 글자가 하나씩 붙어 있고, 이 자리는 누구 명반이든 같아요.",
         "사람마다 달라지는 건 두 가지예요. 어느 칸이 명궁이 되는지, 그리고 별 14개가 어느 칸에 앉는지예요.",
         "명궁을 찾으면 나머지 궁 이름은 명궁에서 거꾸로 한 칸씩 형제궁, 부처궁, 자녀궁, 재백궁 순서로 붙어요.") + \
       P("처음부터 열두 칸을 다 읽지 않아도 돼요. 아래 네 칸만 먼저 보면 명반이 어떤 이야기를 하는지 잡혀요.") + "[[Q]]"
sec2 = P("<b>명궁 찾기는 세 단계면 끝나요.</b>",
         "1️⃣ <b>음력 생월 찾기</b>: 양력 생일을 음력으로 바꿔요. 자미두수는 음력 달이 기준이에요.",
         "2️⃣ <b>자시 기준 칸 찾기</b>: 음력 1월은 寅 칸이고, 달이 하나 늘 때마다 한 칸씩 앞으로 가요. 그래서 5월은 午, 11월은 子, 12월은 丑이에요.",
         "3️⃣ <b>태어난 시만큼 거꾸로 세기</b>: 태어난 시가 자시(밤 11시~새벽 1시)에서 몇 시진 늦는지 세고, 그 수만큼 거꾸로 가면 명궁이에요.") + \
       P("🔎 <b>한 사람으로 직접 세어 볼게요.</b>",
         "양력 1992년 6월 20일 오후 2시 20분에 태어났다면 음력으로는 5월 20일, 시는 미(未)시(오후 1시~3시)예요.",
         "음력 5월이니 자시 기준 칸은 午예요. 미시는 자시에서 일곱 시진 늦으니 午에서 거꾸로 일곱 칸을 세요.",
         "巳, 辰, 卯, 寅, 丑, 子, 亥. 이 사람의 자미두수 명궁은 亥 칸이고, 그 칸에 앉은 별은 태음(太陰)이에요.") + "[[K]]" + MID
sec3 = P("<b>네, 한 번은 물어볼 만해요. 자미두수 명궁은 시가 한 칸만 달라도 옮겨 가요.</b>",
         "시진 열두 개마다 명궁이 다른 칸이라, 시를 모르면 명궁을 하나로 정할 수 없어요.",
         "기억이 흐릿한 건 흔한 일이에요. 오래된 일이니까요.") + \
       P("📄 출생증명서나 산모수첩, 육아수첩에 시와 분까지 적혀 있는 경우가 많아요.",
         "💬 물어볼 때는 이렇게 짧게 보내면 돼요. \"엄마, 나 아침에 태어났어, 밤에 태어났어?\"",
         "아침이었는지 저녁이었는지만 알아도 후보 칸이 열두 개에서 여섯 개로 줄어요.") + \
       P("시 경계에서 30분쯤 앞뒤로 태어났다면 앱마다 명궁이 한 칸 다를 수 있어요. 한국 시각을 그대로 쓰는지, 해의 실제 시각에 맞춰 30분쯤 당겨 보는지가 앱마다 달라서예요.",
         "예시의 오후 2시 20분은 30분을 당겨도 미시라 어느 쪽으로 봐도 명궁이 같아요.")
sec4 = P("🧠 <b>명궁 별 설명은 '나는 원래 이래'보다 '이번 주에 써 볼 힘'으로 읽는 편이 좋아요.</b>",
         "셀리그먼 연구팀은 온라인 참가자들을 여섯 가지 연습에 나눠 맡겼어요. 그중 한 무리는 자기 대표 강점 하나를 한 주 동안 날마다 새로운 방식으로 써 봤어요.") + "[[E]]" + \
       P("그 무리는 연습이 끝나고 6개월 뒤까지 행복감이 더 높고 우울감이 더 낮았어요.",
         "명궁 별도 같은 방식으로 쓸 수 있어요. 예시의 태음(太陰)은 섬세하게 살피고 안을 들여다보는 별로 봐요.",
         '📚 <b>출처 1</b>: <a href="https://doi.org/10.1037/0003-066X.60.5.410">Seligman, Steen, Park &amp; Peterson (2005), Positive Psychology Progress, American Psychologist</a>',
         '📚 <b>출처 2</b>: <a href="https://astro.kasi.re.kr/life/pageView/5">한국천문연구원 천문우주지식정보, 음양력 변환</a>') + \
       P("🌱 <b>마음 코치 정월의 질문</b>", "내 명궁 별 설명 가운데<br>요즘 내가 실제로 쓰고 있는 말은 무엇인가요?",
         "🔸 아직 안 써 본 말이 있다면<br>이번 주 어디에서 한 번 꺼내 볼 수 있을까요?") + \
       P("✔️ <b>이번 주에 해 볼 것</b>",
         "1. 출생증명서나 산모수첩에서 태어난 시를 찾아 두세요.",
         "2. 한국천문연구원 음양력 변환에서 음력 생월을 확인해 보세요.",
         "3. 명궁 별 설명 한 줄을 골라 이번 주 할 일 하나에 붙여 써 보세요. 태음이라면 '회의 메모를 한 번 더 살피기'처럼요.")
sec5 = P("<b>Q. 명궁 칸에 별이 하나도 없으면요?</b>", "A. 맞은편 칸인 천이궁의 별을 빌려 읽어요. 이걸 차성(借星)이라고 해요.",
         "예를 들어 양력 1989년 3월 10일 오후 4시 10분생은 명궁 未 칸이 비어 있어서, 맞은편 丑 칸의 태양·태음을 빌려 읽어요.") + \
       P("<b>Q. 양력 생일로 바로 세우면 안 되나요?</b>", "A. 안 돼요. 같은 양력 3월 10일이라도 1991년생은 음력 1월, 1992년생은 음력 2월이라 명궁 칸도 서로 달라요.",
         "윤달에 태어났다면 15일까지는 그 달로, 16일부터는 다음 달로 보는 방식을 흔히 써요.") + \
       P("<b>Q. 자미두수와 사주는 무엇이 다른가요?</b>", "A. 같은 생년월일시를 넣어도 사주는 글자 여덟 개를, 자미두수는 열두 칸 지도와 별을 읽어요.",
         "그래서 사주는 기운의 많고 적음을, 자미두수는 삶의 어느 칸에 무게가 실렸는지를 먼저 보여 줘요.") + \
       P("<b>Q. 신궁은 언제 보나요?</b>", "A. 명궁을 읽은 다음이에요. 신궁은 같은 생월과 시로 반대 방향으로 세는 칸이에요.",
         "예시의 1992년 6월 20일 오후 2시 20분생은 신궁이 丑 칸이에요.")
tail = P("여러분의 명궁은 열두 글자 가운데 어느 칸이었나요?", "글자 하나만 댓글로 남겨 주세요.") + \
       '<p><b>👇 명반 다음으로 2027년 한 해 흐름이 궁금하다면, 2027 띠별 운세, 정미년 12띠 힘 쓸 달과 아낄 달 한눈에</b></p>'
secs = [sec1, sec2, sec3, sec4, sec5]

def _have(n): return os.path.exists(os.path.join(HERE, "img", n))
def build():
    for d_ in ("wide", "m1280", "master"): os.makedirs(os.path.join(HERE, "img", d_), exist_ok=True)
    c = V.Ctx(PAL); made = []
    a4 = f"wide/naver_z{KEY}_a4.jpg"
    if not _have(a4):
        V.render(PID + "_new", {"d": "N", "el": "물", "kick": "자미두수 명반", "hook": ["내 명궁 한 칸", "3단계로 세기"], "sub": "음력 생월과 태어난 시",
                                "items": ["음력 달", "자시 칸", "거꾸로 세기"]}, os.path.join(HERE, "img", a4), PAL)
    made.append(a4)
    nm = {"Q": f"naver_z{KEY}_q7.jpg", "K": f"naver_z{KEY}_k7.jpg", "E": f"naver_z{KEY}_e7.jpg"}
    if not _have(nm["Q"]):
        DGC.quad(nm["Q"], c, "명반에서 먼저 볼 네 칸", [("명궁", "나의 바탕, 제일 먼저 찾는 칸"), ("재백궁", "돈을 모으고 쓰는 방식"),
                                                   ("관록궁", "일하는 모습과 자리"), ("부처궁", "가장 가까운 사람과의 사이")], 0,
                 "자미두수 궁 순서", "궁 이름은 명궁에서 거꾸로 한 칸씩 붙어요")
    if not _have(nm["K"]):
        DGB.counter(nm["K"], c, "명궁 세기, 예시 한 명", [("음력 5월", "양력 1992.6.20 오후 2시 20분"), ("午 칸", "1월 寅부터 한 칸씩 앞으로"),
                                                    ("일곱 칸", "미시는 자시보다 일곱 시진 늦어요")],
                    "午에서 거꾸로 일곱 칸 → 명궁은 亥, 별은 태음", "자오선 계산 · 음력 한국천문연구원 기준")
    if not _have(nm["E"]):
        DGC.exp(nm["E"], c, "타고난 강점, 새 방식으로 써 보기", "셀리그먼 연구팀 · 2005",
                [("나누기", "온라인 참가자를 여섯 가지 연습에 나눠요"), ("한 주", "대표 강점 하나를 날마다 새로운 방식으로 써요"),
                 ("다시 재기", "1주, 1달, 3달, 6달 뒤 행복감과 우울감을 재요")],
                "새 방식으로 강점을 쓴 무리는 6개월 뒤에도 더 행복했어요", "Seligman, Steen, Park & Peterson (2005)")
    import fullbleed as FBL
    plan_p = os.path.join(HERE, "fullbleed_plan.json"); plan = json.load(open(plan_p, encoding="utf-8")) if os.path.exists(plan_p) else {}
    rows = []
    for pos, k in enumerate("QKE", 1):
        f = nm[k][:-4] + "f.jpg"
        if not _have(f):
            r, why = FBL.convert(nm[k], [os.path.join(HERE, "img"), os.path.join(HERE, "img", "m1280")]); assert r, (nm[k], why)
        rows.append({"pos": pos, "old": nm[k], "new": f}); made.append(nm[k]); nm[k] = f
        reg_ = json.load(open(DG.REG, encoding="utf-8")); reg_[f] = reg_[rows[-1]["old"]]; json.dump(dict(sorted(reg_.items())), open(DG.REG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    plan[PID] = rows; json.dump(plan, open(plan_p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    made += list(nm.values())
    alt = {"Q": "자미두수 명반에서 먼저 볼 네 칸 그림. 명궁은 나의 바탕, 재백궁은 돈을 모으고 쓰는 방식, 관록궁은 일하는 모습, 부처궁은 가장 가까운 사람과의 사이",
           "K": "명궁 세기 예시 그림. 양력 1992년 6월 20일 오후 2시 20분생은 음력 5월, 자시 기준 칸은 午, 미시는 일곱 시진 늦어 거꾸로 일곱 칸 세면 명궁은 亥 칸이고 별은 태음",
           "E": "셀리그먼 연구팀 2005 실험 그림. 대표 강점 하나를 한 주 동안 날마다 새로운 방식으로 쓴 사람들은 6개월 뒤에도 행복감이 더 높았어요"}
    body = P(*head) + P("<b>📌 오늘 볼 차례</b>", *[f"{i + 1}. {q}" for i, q in enumerate(toc_q)])
    for i, (q, s) in enumerate(zip(toc_q, secs)):
        for k in "QKE": s = s.replace(f"[[{k}]]", IMG(nm[k], alt[k]))
        body += H(f"{i + 1}. {q}") + s
    body += tail + CTA
    import copy_rules as CR
    for w in ("재미로", "상담", "—", "안녕하세요, 자오선의 정월이에요", "결론부터 말씀드릴게요", "생년월일만 넣으면 1초", "한 줄 요약", "이 글의 순서") + tuple(CR.금지어):
        assert w not in re.sub(r"<[^>]+>", " ", body), w
    for f in made:   # 사이트 사본(K-069)
        dst = os.path.join(SITE, "public", "naver", "img", f); os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy(os.path.join(HERE, "img", f), dst)
    return body, a4, made

TITLE = "자미두수 명반 보는 법, 음력 생월과 시로 명궁 찾는 3단계"
TAGS = ["자미두수", "자미두수명반", "자미두수보는법", "명궁", "명궁찾기", "명반보는법", "자미두수명궁", "신궁", "차성", "자오선"]
REL = {"id": "n80", "title": "2027 띠별 운세, 정미년 12띠 힘 쓸 달과 아낄 달 한눈에",
       "phrase": "명반 다음으로 2027년 한 해 흐름이 궁금하다면, 2027 띠별 운세, 정미년 12띠 힘 쓸 달과 아낄 달 한눈에",
       "url": "https://blog.naver.com/zaoseon/224461125363"}
KW_VOL = json.load(open(os.path.join(SITE, "data", "keywords", "kw_volume.json"), encoding="utf-8"))["posts"]["n86"]["씨앗"]
INTENT = {"keywords": ["자미두수", "자미두수 명반", "자미두수 보는 법", "명궁", "명반 보는 법"],
          "keyword_src": "kw-volume 작업(data/keywords/kw_volume.json posts.n86) 월 검색량 · n57 조회 순위(재발행 일정 '새 글로 다시 쓰기' 첫째)",
          "intent": "해 보고 싶다", "intent_note": "자미두수 명반에서 내 명궁이 어느 칸인지 직접 찾는 순서와, 태어난 시를 모를 때 어떻게 하는지",
          "first3": "자미두수 명반은 음력 생일과 태어난 시로 열두 칸에 별 14개를 놓은 표예요. 그 열두 칸 가운데 제일 먼저 찾는 칸이 명궁(命宮)이에요.",
          "answer_keys": ["자미두수", "명반", "명궁"],
          "order": toc_q[:4], "images": ["먼저 볼 네 칸(quad)", "명궁 세기 예시(counter, 엔진 계산)", "대표 강점 새 방식 실험(exp, Seligman 외 2005)"],
          "related": "n80", "cta": PID, "experience": [], "applied": True,
          "differs_from_n57": "제목·도입(정의 + 명궁 직답)·소제목 순서·12궁/주성 14개 나열 대신 명궁 세기 3단계와 예시 한 명(1992.6.20 오후 2시 20분, 명궁 亥 태음)·태어난 시 찾는 장면·차성 예시(1989.3.10)·그림 유형(quad·counter·exp)·심리 개념(고정 마음가짐 → 대표 강점 새 방식, Seligman 2005)·출처·연결글(n11 → n80)"}

if __name__ == "__main__":
    body, a4, made = build()
    reg = json.load(open(MP.REG, encoding="utf-8"))
    assert PID not in reg or not reg[PID].get("done"), "이미 예약 끝난 글"
    reg[PID] = dict(dt="2027-02-01T08:00:00", dt_tbd="CT가 정함(재발행 일정 11/17 08:00 자리, 서브 배너 링크 고침 확인 뒤). 이 날짜는 자리값", title=TITLE, tags=TAGS, body=body,
                    cover=a4, related=REL, thumbs=None, cid=None, clips=None, category="운명학 사전", done=False, kw_vol=KW_VOL,
                    k131="n86 11/5(K-151 새 글)", source="build_naver_86.py (n57 주제 새 글, n57 그대로)")
    json.dump(reg, open(MP.REG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    ic = json.load(open(os.path.join(HERE, "intent_cards.json"), encoding="utf-8")); ic["cards"][PID] = INTENT
    json.dump(ic, open(os.path.join(HERE, "intent_cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    v = reg[PID]
    MP.write_page(PID, D.datetime.fromisoformat(v["dt"]), v["title"], v["tags"], v["body"], None, v["cover"], v["related"], v["category"])
    MP.write_index()
    import k151_check as K
    print(PID, len(TITLE), "자 제목 · 본문 글자", len(re.sub(r"<[^>]+>|&nbsp;", "", body)), "· 사진", made, "· K 검사", K.check(PID, v))
