"""네이버 n89: 육효점 보는 법 새 글 (CT 11/4 19:40 → ① 최우선, 대표 11/4 19:28 재발행 일정 '새 글로 다시 쓰기' n15 → n89, 11/20 08:00 자리).
- 왜: 노출 안 되는 옛 글 n15(육효란? 주역에 오행을 더한 점괘 읽는 법, 정월에게 묻다)를 새 글로. n15는 건드리지 않는다(K-147·K-178).
- 검색어: data/keywords/kw_volume.json posts.n89(kw-volume 11/6 12:06) — 주역점 670 · 육효점 650 · 육효 520 (주역점보는법·육효풀이 10).
- 겹침 피하기: 동전 세 개로 괘 이름 찾기는 발행 글 n56(주역 64괘 조견표, 검색 노출 '예')이, 질문 한 줄로 줄이기는 n44가 이미 다뤘다.
  그래서 이 글은 '괘를 세운 다음 무엇을 읽나'(세효·응효 → 용신 → 월건·일진 → 움직이는 줄)만 예시 한 괘로 끝까지 간다. 연결글 n56.
- 다르게 쓴 것(K-151): n15의 상품 소개·시연용 화풍정(火風鼎)·사주와 차이·손실 회피 대신, 이직 질문 하나(2026.11.6 오전 9시 30분)에
  동전 여섯 번(6·7·7·8·8·8) → 지풍승(地風升) → 지천태(地天泰), 세효 4효 丑 흙 · 응효 1효 · 용신 관귀 3효 酉 쇠 · 월건 戊戌 · 일진 甲申 · 공망 午未.
  심리 개념(손실 회피 Kahneman 1979 → 실행 의도 Gollwitzer & Sheeran 2006), 그림 유형(quad·compare·exp), 연결글(s10 → n56).
  소제목 틀(한 줄 요약·이 글의 순서·생년월일만 넣으면 1초) 안 씀.
- 계산: zaoseon-site engine/liuyao.py chart · engine/liuyao_judge.py judge('직장'). 아래 assert.
- 출처 2개(K-162, 11/6 확인): Gollwitzer & Sheeran (2006) Advances in Experimental Social Psychology 38, 69–119(DOI 10.1016/S0065-2601(06)38002-1,
  콘스탄츠 대학 연구실 서지 기록으로 확인, 94개 시험·효과 크기 d=0.65는 2차 정리 글로 확인) · 중국철학서전자화계획 周易 升 괘사(ctext.org/book-of-changes/sheng, 열어 '升:元亨,用見大人,勿恤,南征吉' 확인).
- 날짜: CT가 정한다. pages.json dt 는 자리값, dt_tbd 로 표시.
사용: SITE=<zaoseon-site> python3 naver/build_naver_89.py"""
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
       '<tr><td style="padding:12px 10px;text-align:center;border:1px solid #d0d0d0"><b>괘 말고 타고난 기운도 궁금하다면</b></td></tr>'
       '<tr><td style="padding:12px 10px;text-align:center;border:1px solid #d0d0d0"><span style="color:#9a9a9a">[ 1993 . 08 . 21 ]</span></td></tr>'
       '<tr><td style="padding:12px 10px;text-align:center;border:1px solid #d0d0d0"><b><a href="https://zaoseon.com/?utm_source=naver&amp;utm_medium=mid#free">내 태어난 날 글자 보기 →</a></b></td></tr>'
       '</tbody></table>' + BL)
CTA = ('<p><a href="https://zaoseon.com/?utm_source=naver&utm_medium=cta#free"><img src="' + RAW +
       'naver_cta5_1%EC%B4%88%EB%AC%B4%EB%A3%8C%ED%92%80%EC%9D%B4.jpg" alt="자오선 무료 1초 풀이 안내 배너"></a></p>')
PID, KEY, PAL = "n89", "89", "k_white_s"   # 예시의 용신 酉 = 쇠 판 묶음(EL_SET 쇠), n88 y_black_s·n87 dg_gold_s 와 다른 판

# ───────── 계산값과 검산 (engine/liuyao.py · engine/liuyao_judge.py)
import datetime as D
sys.path.insert(0, os.path.join(SITE, "engine")); import liuyao as L, liuyao_judge as J
ASK = D.datetime(2026, 11, 6, 9, 30)                       # 질문한 때: 2026년 11월 6일 오전 9시 30분(입동 하루 전)
LINES = [6, 7, 7, 8, 8, 8]                                 # 아래 줄부터: 뒤뒤뒤 · 앞뒤뒤 · 앞뒤뒤 · 앞앞뒤 · 앞앞뒤 · 앞앞뒤 (앞 3, 뒤 2)
COINS = ["뒤·뒤·뒤", "앞·뒤·뒤", "앞·뒤·뒤", "앞·앞·뒤", "앞·앞·뒤", "앞·앞·뒤"]
for s, v in zip(COINS, LINES): assert sum(3 if x == "앞" else 2 for x in s.split("·")) == v
C = L.chart(LINES, ASK)
assert C["base"]["full"] == "地風升" and C["base"]["ko"] == "지풍승" and (C["base"]["upper"], C["base"]["lower"]) == ("坤", "巽")
assert C["changed"]["full"] == "地天泰" and C["changed"]["ko"] == "지천태" and C["changed"]["lower"] == "乾"
assert C["base"]["palace"] == "震" and C["day"] == "甲申" and C["month"] == "戊戌" and tuple(C["kong"]) == ("午", "未")
RW = {r["pos"]: r for r in C["rows"]}
assert RW[4]["shi"] and RW[4]["gz"] == "癸丑" and RW[4]["liuqin"] == "처재" and RW[4]["el"] == "土"
assert RW[1]["ying"] and RW[1]["moving"] and RW[1]["gz"] == "辛丑" and RW[1]["change"]["gz"] == "甲子" and RW[1]["change"]["el"] == "水"
assert [r["pos"] for r in C["rows"] if r["moving"]] == [1]
assert [r["pos"] for r in C["rows"] if r["liuqin"] == "관귀"] == [3, 6] and RW[3]["gz"] == "辛酉" and RW[3]["el"] == "金" and RW[3]["wx"] == "상"
assert not RW[3]["kong"] and not RW[3]["yuepo"] and not RW[3]["richong"]
JD = J.judge(C, "직장")
assert JD["yong"] == "관귀" and JD["yong_line"] == 3 and JD["verdict"] == "좋음" and not JD["hidden"]
rs = " ".join(JD["reasons"])
for w in ("이달의 기운이 도와줘요", "오늘 기운이 뒤에서 받쳐 줘요", "원신", "독발", "반음"): assert w in rs, w
assert JD["timing"][0].startswith("卯월(양력 3월경)")
print("괘·세응·용신·월건·일진·움직이는 줄 엔진으로 다시 확인")

# ───────── 본문 (n15 문장을 옮기지 않았다)
head = ["<b>육효점은 주역 괘 여섯 줄에 내 자리와 질문의 자리를 정하고 그날 기운으로 힘을 재는 점이에요.</b>",
        "동전을 던져 괘 이름을 찾는 데서 멈추면 주역점이고, 줄마다 흙·쇠·물 같은 기운과 '나·상대·일' 자리를 얹으면 육효점이 돼요.",
        "<b>괘를 세운 다음에는 네 군데만 차례로 보면 돼요. 내 자리, 질문이 찾는 자리, 그날의 기운, 움직이는 줄이에요.</b>",
        "오늘은 이직 질문 하나로 괘 하나를 세워서, 그 네 군데를 끝까지 읽어 볼게요. 2026년 11월 6일 기준으로 정리한 내용이에요."]
toc_q = ["육효점은 괘를 세운 다음 무엇을 볼까요?", "이직 질문 하나로 괘를 세우면 어떻게 나올까요?",
         "여섯 줄 가운데 내 자리와 질문의 자리는 어디일까요?", "그날의 기운과 움직이는 줄은 무엇을 더할까요?",
         "질문을 또렷하게 적으면 왜 읽기 쉬워질까요?", "자주 묻는 질문"]
sec1 = P("<b>괘 이름은 출발점이고, 답은 줄마다 붙인 자리에서 나와요.</b>",
         "육효점에서는 여섯 줄 하나하나에 십이지 글자 하나와 다섯 기운 하나를 붙여요. 그리고 그 기운이 괘의 바탕 기운과 어떤 사이인지로 이름을 붙여요. 돈과 재물(처재), 일과 직장(관귀), 문서와 집(부모), 결과와 아랫사람(자손), 경쟁하는 사람(형제)이에요.",
         "괘를 세운 다음 먼저 보는 곳은 네 군데예요.") + "[[Q]]" + \
       P("이 네 곳만 순서대로 보면, 괘 이름의 뜻을 몰라도 질문에 대한 흐름을 한 줄로 말할 수 있어요.")
sec2 = P("🔎 <b>예시 질문은 '이번 달 들어온 이직 제안, 내년 봄 안에 옮기면 어떨까요?'예요.</b>",
         "2026년 11월 6일 오전 9시 30분에 동전 세 개를 여섯 번 던졌다고 해 볼게요. 앞면은 3, 뒷면은 2로 세요.",
         "아래 줄부터 뒤·뒤·뒤(6), 앞·뒤·뒤(7), 앞·뒤·뒤(7), 앞·앞·뒤(8), 앞·앞·뒤(8), 앞·앞·뒤(8)가 나왔어요.",
         "7은 이어진 줄, 8은 끊어진 줄이에요. 6은 끊어진 줄인데 이어진 줄로 바뀌는 '움직이는 줄'이에요.") + \
       P("아래 세 줄은 바람(巽), 위 세 줄은 땅(坤)이라 본괘는 지풍승(地風升)이에요. 땅 밑의 나무가 올라오는 모습이라 '오른다'는 뜻이에요.",
         "맨 아래 줄이 움직여 아래 괘가 하늘(乾)로 바뀌니, 바뀐 괘는 지천태(地天泰)예요. 하늘과 땅이 통하는 괘예요.",
         "『주역』은 승괘에 '크게 통하니 걱정하지 말라'는 말을 붙여 두었어요.") + "[[C]]" + MID
sec3 = P("<b>나는 '세효', 상대는 '응효', 질문이 찾는 것은 '용신'이라는 줄이에요.</b>",
         "지풍승에서 내 자리(세효)는 아래에서 넷째 줄, 丑 흙이에요. 상대 자리(응효)는 맨 아래 첫째 줄이에요. 이 질문에서 상대는 제안을 한 회사예요.",
         "그런데 움직이는 줄이 바로 이 첫째 줄이에요. 회사 쪽이 먼저 움직이는 모습이라, 제안이 지나가는 말이 아니라고 읽어요.") + \
       P("이직 질문은 일과 직장을 뜻하는 관귀 줄을 봐요. 이 괘에는 관귀가 셋째 줄과 맨 위 줄 두 곳에 있어요.",
         "둘 다 酉 쇠예요. 그중 셋째 줄이 안쪽 괘에 있어 지금 내 가까이에 있는 일이라, 셋째 줄을 중심으로 봐요.",
         "질문마다 보는 줄이 달라요. 돈 질문이면 처재, 계약이나 집 질문이면 부모 줄을 먼저 찾아요.")
sec4 = P("<b>질문한 달과 날의 기운이 용신을 돕는지 누르는지를 재요.</b>",
         "11월 6일은 입동 하루 전이라 이달의 기운은 아직 戊戌, 흙이에요. 흙은 쇠를 낳아서 酉 쇠를 힘 있게 해 줘요.",
         "그날의 기운(일진)은 甲申이에요. 申도 쇠라서 같은 편이 뒤에서 받쳐 주는 모습이에요.",
         "그날 비어 있는 글자(공망)는 午와 未예요. 셋째 줄 酉는 여기에 걸리지 않아 힘이 빠지지 않아요.") + \
       P("움직이는 줄은 하나뿐인데, 그 줄 丑 흙이 酉 쇠를 낳는 기운이에요. 돕는 쪽이 혼자 움직이니 힘이 더 실린다고 읽어요.",
         "그래서 이 괘는 이직 쪽으로 흐름이 열려 있어요. 다만 괘가 바뀌며 서로 부딪히는 모양이라, 한 번 정한 조건이 다시 바뀌기 쉬워요.",
         "이럴 때 할 일은 하나예요. 연봉과 입사 날짜를 말로만 듣지 말고 '조건을 메일로 한 번 더 받을 수 있을까요?'라고 물어 두세요.",
         "때로는 흔들리던 일이 자리를 잡는 卯월, 양력 3월 무렵을 봐요. 질문에 붙인 '내년 봄'과 맞는 때예요.")
sec5 = P("🧠 <b>목표만 적는 것보다 '언제·어디서·어떻게'까지 적으면 해내는 비율이 높아져요.</b>",
         "심리학자 골비처와 시런은 2006년, 이렇게 '언제·어디서 하겠다'를 미리 정하는 방법을 시험한 연구 94개를 모아 다시 셌어요.",
         "그 결과 계획을 붙인 쪽이 목표만 정한 쪽보다 목표를 이룬 정도가 뚜렷하게 높았어요. 효과 크기는 0.65로 중간을 넘는 크기였어요.") + "[[E]]" + \
       P("육효점에서 질문에 기한과 사건을 붙이라고 하는 것도 같은 이유예요.",
         "'이직할까?'는 볼 줄도, 볼 때도 정해지지 않아요. '이 제안, 내년 봄 안에 옮기면?'이라고 적으면 관귀 줄과 봄이라는 때가 같이 정해져요.",
         "그래서 저는 괘보다 질문 한 줄을 먼저 다듬어요.",
         '📚 <b>출처 1</b>: <a href="https://doi.org/10.1016/S0065-2601(06)38002-1">Gollwitzer &amp; Sheeran (2006), Implementation intentions and goal achievement, Advances in Experimental Social Psychology 38</a>',
         '📚 <b>출처 2</b>: <a href="https://ctext.org/book-of-changes/sheng">중국철학서전자화계획, 周易 升(승괘) 원문</a>') + \
       P("🌱 <b>마음 코치 정월의 질문</b>", "요즘 마음에 걸린 일을<br>사건 하나, 기한 하나로 적으면 어떤 문장이 되나요?",
         "🔸 그 질문에서 내가 찾는 것은<br>돈일까요, 일일까요, 문서일까요?") + \
       P("✔️ <b>괘를 세운 날 해 볼 것</b>",
         "1. 질문을 '무엇을, 언제까지'가 들어간 한 줄로 적어 두세요.",
         "2. 괘를 세우면 내 자리(세효)와 질문이 찾는 줄(용신)에 동그라미를 쳐 두세요.",
         "3. 그날의 기운과 움직이는 줄이 용신을 돕는지, 누르는지만 한 줄로 적어 보세요.")
sec6 = P("<b>Q. 육효점과 주역점은 다른 건가요?</b>",
         "A. 괘를 세우는 방법은 같아요. 주역점은 괘 이름과 괘에 붙은 말을 읽고, 육효점은 그 위에 줄마다 기운과 자리를 얹어 질문 하나를 더 좁게 읽어요.") + \
       P("<b>Q. 움직이는 줄이 하나도 없으면요?</b>",
         "A. 바뀐 괘 없이 본괘 하나만 봐요. 이때는 그날과 그달의 기운이 용신을 돕는지가 더 중요해져요. 일이 크게 바뀌기보다 지금 흐름대로 간다고 봐요.") + \
       P("<b>Q. 용신이 괘에 없으면요?</b>",
         "A. 괘가 속한 바탕 괘에서 숨어 있는 줄(복신)을 찾아 읽어요. 찾는 것이 아직 겉으로 드러나지 않았다는 뜻이라, 서두르기보다 때를 기다려 보라고 읽는 일이 많아요.") + \
       P("<b>Q. 같은 질문을 다시 던져도 되나요?</b>",
         "A. 한 질문에는 한 괘만 읽어요. 마음에 드는 답이 나올 때까지 던지면 어느 괘를 믿을지 흐려져요. 상황이 크게 바뀌었을 때 질문을 새로 적어 다시 세워요.")
tail = P("여러분은 요즘 어떤 질문으로 괘를 세워 보고 싶나요?", "돈, 일, 문서, 사람 가운데 하나만 댓글로 남겨 주세요.") + \
       '<p><b>👇 주역 64괘에서 동전으로 내 괘 이름부터 찾고 싶다면, 주역 64괘 조견표, 동전 3개로 내 괘 찾는 법 (8괘 한 장)</b></p>'
secs = [sec1, sec2, sec3, sec4, sec5, sec6]

def _have(n): return os.path.exists(os.path.join(HERE, "img", n))
def build():
    for d_ in ("wide", "m1280", "master"): os.makedirs(os.path.join(HERE, "img", d_), exist_ok=True)
    c = V.Ctx(PAL); made = []
    a4 = f"wide/naver_z{KEY}_a4.jpg"
    if not _have(a4):
        V.render(PID + "_new", {"d": "N", "el": "쇠", "kick": "육효점 보는 법", "hook": ["괘를 세운 다음", "네 곳만 보기"], "sub": "이직 질문 하나로 끝까지",
                                "items": ["내 자리", "질문의 자리", "그날 기운"]}, os.path.join(HERE, "img", a4), PAL)
    made.append(a4)
    nm = {"Q": f"naver_z{KEY}_q7.jpg", "C": f"naver_z{KEY}_c7.jpg", "E": f"naver_z{KEY}_e7.jpg"}
    if not _have(nm["Q"]):
        DGC.quad(nm["Q"], c, "괘를 세운 뒤 보는 네 곳", [("세효", "나의 자리, 내 마음과 준비"), ("응효", "상대의 자리, 사람이나 회사"),
                                                    ("용신", "질문이 찾는 것, 돈·일·문서"), ("움직이는 줄", "바뀌는 쪽, 일이 흘러갈 곳")], 2,
                 "자오선 정리", "용신은 질문마다 달라요")
    if not _have(nm["C"]):
        DGC.compare(nm["C"], c, "예시 괘, 맨 아래 줄 하나가 바뀌면", ("본괘 지풍승", "바뀐 괘 지천태"),
                    [("위 괘", "땅(坤)", "땅(坤)"), ("아래 괘", "바람(巽)", "하늘(乾)"), ("첫째 줄", "끊어진 줄, 丑 흙", "이어진 줄, 子 물"), ("읽는 뜻", "오른다", "통한다")],
                    "예시 2026.11.6 오전 9시 30분 · 자오선 계산", hi=1)
    if not _have(nm["E"]):
        DGC.exp(nm["E"], c, "언제·어디서까지 적으면", "골비처·시런 · 2006",
                [("모으기", "'언제·어디서 하겠다'를 미리 정하는 방법을 시험한 연구 94개를 모았어요."),
                 ("나누기", "목표만 정한 쪽과, 계획까지 붙인 쪽을 나란히 비교했어요."),
                 ("세기", "목표를 얼마나 이뤘는지 연구마다 같은 잣대로 다시 셌어요.")],
                "계획을 붙인 쪽이 뚜렷하게 더 해냈어요. 효과 크기 0.65", "Gollwitzer & Sheeran (2006)")
    import fullbleed as FBL
    plan_p = os.path.join(HERE, "fullbleed_plan.json"); plan = json.load(open(plan_p, encoding="utf-8")) if os.path.exists(plan_p) else {}
    rows = []
    for pos, k in enumerate("QCE", 1):
        f = nm[k][:-4] + "f.jpg"
        if not _have(f):
            r, why = FBL.convert(nm[k], [os.path.join(HERE, "img"), os.path.join(HERE, "img", "m1280")]); assert r, (nm[k], why)
        rows.append({"pos": pos, "old": nm[k], "new": f}); made.append(nm[k]); nm[k] = f
        reg_ = json.load(open(DG.REG, encoding="utf-8")); reg_[f] = reg_[rows[-1]["old"]]; json.dump(dict(sorted(reg_.items())), open(DG.REG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    plan[PID] = rows; json.dump(plan, open(plan_p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    made += list(nm.values())
    alt = {"Q": "괘를 세운 뒤 보는 네 곳 그림. 세효는 나의 자리, 응효는 상대의 자리, 용신은 질문이 찾는 것(돈·일·문서), 움직이는 줄은 일이 흘러갈 쪽",
           "C": "예시 괘 그림. 본괘 지풍승은 위 땅 아래 바람, 맨 아래 끊어진 줄 丑 흙이 이어진 줄 子 물로 바뀌어 아래가 하늘이 되면 지천태",
           "E": "골비처와 시런 2006년 연구 그림. 계획 세우기 연구 94개를 모아 목표만 정한 쪽과 언제·어디서까지 정한 쪽을 비교하니 계획을 붙인 쪽이 더 해냈고 효과 크기는 0.65"}
    body = P(*head) + P("<b>📌 괘 하나를 끝까지 읽는 순서</b>", *[f"{i + 1}. {q}" for i, q in enumerate(toc_q)])
    for i, (q, s) in enumerate(zip(toc_q, secs)):
        for k in "QCE": s = s.replace(f"[[{k}]]", IMG(nm[k], alt[k]))
        body += H(f"{i + 1}. {q}") + s
    body += tail + CTA
    import copy_rules as CR
    for w in ("재미로", "상담", "—", "안녕하세요, 자오선의 정월이에요", "결론부터 말씀드릴게요", "생년월일만 넣으면 1초", "한 줄 요약", "이 글의 순서") + tuple(CR.금지어):
        assert w not in re.sub(r"<[^>]+>", " ", body), w
    for f in made:   # 사이트 사본(K-069)
        dst = os.path.join(SITE, "public", "naver", "img", f); os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy(os.path.join(HERE, "img", f), dst)
    return body, a4, made

TITLE = "육효점 보는 법, 괘를 세운 뒤 내 자리부터 읽는 4단계"
TAGS = ["육효점", "육효", "주역점", "육효보는법", "주역", "괘", "동전점", "이직운", "운명학", "자오선"]
REL = {"id": "n56", "title": "주역 64괘 조견표, 동전 3개로 내 괘 찾는 법 (8괘 한 장)",
       "phrase": "주역 64괘에서 동전으로 내 괘 이름부터 찾고 싶다면, 주역 64괘 조견표, 동전 3개로 내 괘 찾는 법 (8괘 한 장)",
       "url": "https://blog.naver.com/zaoseon/224447834229"}
KW_VOL = json.load(open(os.path.join(SITE, "data", "keywords", "kw_volume.json"), encoding="utf-8"))["posts"]["n89"]["씨앗"]
INTENT = {"keywords": ["육효점", "주역점", "육효"],
          "keyword_src": "kw-volume 작업(data/keywords/kw_volume.json posts.n89, 11/6 12:06) 월 검색량 · n15 조회 순위(재발행 일정 '새 글로 다시 쓰기')",
          "intent": "알고 싶다", "intent_note": "괘를 세운 다음 무엇을 어떤 순서로 읽는지, 이직 질문 한 괘로 세효·용신·월건 일진·움직이는 줄까지 끝까지 따라가 보기",
          "first3": "육효점은 주역 괘 여섯 줄에 내 자리와 질문의 자리를 정하고 그날 기운으로 힘을 재는 점이에요.",
          "answer_keys": ["육효점", "주역점", "괘"],
          "order": toc_q[:5], "images": ["괘 뒤에 보는 네 곳(quad)", "본괘·바뀐 괘 맞대기(compare, 엔진 계산)", "실행 의도 연구(exp)"],
          "related": "n56", "cta": PID, "experience": [], "applied": True,
          "differs_from_n15": "제목·도입(정의 + 네 곳 직답)·소제목 순서·상품 소개와 시연용 화풍정 대신 이직 질문 한 괘(2026.11.6 오전 9시 30분, 6·7·7·8·8·8 → 지풍승→지천태)로 세효·응효·용신(관귀 酉)·월건 戊戌·일진 甲申·공망·움직이는 줄까지 끝까지 읽기·그림 유형(quad·compare·exp)·심리 개념(손실 회피 → 실행 의도, Gollwitzer & Sheeran 2006)·출처·연결글(s10 → n56)"}

if __name__ == "__main__":
    body, a4, made = build()
    reg = json.load(open(MP.REG, encoding="utf-8"))
    assert PID not in reg or not reg[PID].get("done"), "이미 예약 끝난 글"
    reg[PID] = dict(dt="2027-02-02T18:00:00", dt_tbd="CT가 정함(재발행 일정 11/20 08:00 자리). 이 날짜는 자리값", title=TITLE, tags=TAGS, body=body,
                    cover=a4, related=REL, thumbs=None, cid=None, clips=None, category="운명학 사전", done=False, kw_vol=KW_VOL,
                    k131="n89 11/6(K-151 새 글)", source="build_naver_89.py (n15 주제 새 글, n15 그대로)")
    json.dump(reg, open(MP.REG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    ic = json.load(open(os.path.join(HERE, "intent_cards.json"), encoding="utf-8")); ic["cards"][PID] = INTENT
    json.dump(ic, open(os.path.join(HERE, "intent_cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    v = reg[PID]
    MP.write_page(PID, D.datetime.fromisoformat(v["dt"]), v["title"], v["tags"], v["body"], None, v["cover"], v["related"], v["category"])
    MP.write_index()
    import k151_check as K
    print(PID, len(TITLE), "자 제목 · 본문 글자", len(re.sub(r"<[^>]+>|&nbsp;", "", body)), "· 사진", made, "· K 검사", K.check(PID, v))
