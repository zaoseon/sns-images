"""네이버 n93: 서운함 참다가 터지는 이유 새 글 (CT 11/4 19:40 재발행 일정 '새 글로 다시 쓰기' n23 → n93, 진행표 docs/네이버_누락글_진행표_2026-11-18.md 첫 줄, CT 11/18 11:3x).
- 왜: 노출 안 되는 옛 글 n23(서운한 걸 참다가 한 번에 터지는 사람의 공통점)을 새 글로. n23은 건드리지 않는다(K-147·K-178).
- 검색어: data/keywords/kw_volume.json posts.n93 — 서운함 240 · 서운한감정 25 · 감정폭발 25 · 서운함표현 15 · 참다가터지는성격 10.
- 다르게 쓴 것(K-151): n23의 인사·'먼저 결론'·한 줄 요약 줄·세 풀이(정화/황소·전갈/수비학 6)·'몇 개 겹칠까'·여섯 운명학 단락·투명성 착각·두드리기 실험·고트먼 대신
  천간(겉)·지지(속) 두 층과 창고 글자 辰·戌·丑·未(지장간), 창고를 여는 충(辰戌·丑未)과 2026년 12월 날짜,
  예시 = 1995년 1월 10일 낮 12시생(甲戌·丁丑·辛丑·甲午, 표현의 글자 癸가 丑 두 곳에만 숨음).
  심리 = 표현 억제(Butler 외 2003 짝 대화 실험 · Srivastava 외 2009 대학 신입생 278명). 그림 유형 iceberg·quad·exp·checklist. 연결글 → n58(발행·노출 '예').
- 계산: 팔자는 zaoseon-site engine/engine.py, 지장간은 engine/appx.JJG, 십성은 ny_facts.tg, 충은 ny_facts.CHUNG — 모두 assert.
- 출처 2개(K-162, 11/18 확인): Butler, Egloff, Wilhelm, Smith, Erickson & Gross (2003) Emotion 3(1) 48–67, DOI 10.1037/1528-3542.3.1.48
  (애리조나 대학 서지·초록: 처음 만난 여성 둘이 속상한 주제로 대화, 한쪽이 표정을 감추면 대화가 끊기고 상대의 혈압이 더 오름) ·
  Srivastava, Tamir, McGonigal, John & Gross (2009) JPSP 96(4) 883–897, DOI 10.1037/a0014755 (PMC4141473: 278명, 자기 보고·주간 기록·친구 보고 모두 지지·가까움·만족이 낮음).
- 날짜: CT가 정한다. pages.json dt 는 자리값, dt_tbd 로 표시.
사용: SITE=<zaoseon-site> python3 naver/build_naver_93.py"""
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
       '<tr><td style="padding:12px 10px;text-align:center;border:1px solid #d0d0d0"><b>내 날 아래 글자가 창고 글자인지 궁금하다면</b></td></tr>'
       '<tr><td style="padding:12px 10px;text-align:center;border:1px solid #d0d0d0"><span style="color:#9a9a9a">[ 1995 . 01 . 10 ]</span></td></tr>'
       '<tr><td style="padding:12px 10px;text-align:center;border:1px solid #d0d0d0"><b><a href="https://zaoseon.com/?utm_source=naver&amp;utm_medium=mid#free">내 태어난 날 글자 보기 →</a></b></td></tr>'
       '</tbody></table>' + BL)
CTA = ('<p><a href="https://zaoseon.com/?utm_source=naver&utm_medium=cta#free"><img src="' + RAW +
       'naver_cta5_1%EC%B4%88%EB%AC%B4%EB%A3%8C%ED%92%80%EC%9D%B4.jpg" alt="자오선 무료 1초 풀이 안내 배너"></a></p>')
PID, KEY, PAL = "n93", "93", "y_black_d"   # 창고 글자 = 흙 → 흙 판 묶음(EL_SET 흙). y_gray_s 는 pillfg=acc 라 칠한 칸 글자가 안 보여 뺌(11/18 눈 확인). n94 p_purple_s · n92 k_neon_s · n88 y_black_s · n85 y_olive_s 와 다른 판

# ───────── 계산값과 검산
import datetime as D
sys.path.insert(0, os.path.join(SITE, "engine"))
import engine as E, ny_facts as F
from appx import JJG
X = D.datetime(1995, 1, 10, 12, 0)
PX = E.compute_saju(X)["팔자"]
assert PX == {"년주": "甲戌", "월주": "丁丑", "일주": "辛丑", "시주": "甲午"}, PX
assert E.compute_saju(D.datetime(1995, 1, 10, 11, 40))["팔자"] == PX
dm = PX["일주"][0]; assert dm == "辛"
SIK = ("식신", "상관")
stems = [PX[k][0] for k in ("년주", "월주", "시주")]
assert not [g for g in stems if F.tg(dm, g) in SIK]                       # 겉(천간)에는 표현의 글자 없음
assert [F.tg(dm, g) for g in stems] == ["정재", "편관", "정재"]
hid = {k: [g for g in JJG[v[1]] if F.tg(dm, g) in SIK] for k, v in PX.items()}
assert hid == {"년주": [], "월주": ["癸"], "일주": ["癸"], "시주": []}, hid   # 속(지장간)에만 癸 두 개
assert JJG["丑"] == "癸辛己" and JJG["辰"] == "乙癸戊" and JJG["戌"] == "辛丁戊" and JJG["未"] == "丁乙己"
assert sum(PX[k][1] in "辰戌丑未" for k in PX) == 3                          # 창고 글자 셋(戌·丑·丑)
assert frozenset("丑未") in F.CHUNG and frozenset("辰戌") in F.CHUNG
assert not any(frozenset((a[1], b[1])) in F.CHUNG for a in PX.values() for b in PX.values() if a != b)   # 원국 안에서는 부딪힘 없음
DEC = {}
for d in range(1, 32): DEC.setdefault(E.compute_saju(D.datetime(2026, 12, d, 12))["팔자"]["일주"][1], []).append(d)
assert DEC["辰"] == [8, 20] and DEC["戌"] == [2, 14, 26] and DEC["丑"] == [5, 17, 29] and DEC["未"] == [11, 23], DEC
assert E.compute_saju(D.datetime(2026, 12, 11, 12))["팔자"]["일주"] == "己未" and E.compute_saju(D.datetime(2026, 12, 23, 12))["팔자"]["일주"] == "辛未"
def dd(b): return "·".join(str(x) for x in DEC[b]) + "일"
print("예시 팔자·지장간·창고 글자·12월 부딪히는 날 다시 확인", {b: DEC[b] for b in "辰戌丑未"})

# ───────── 본문 (n23 문장을 옮기지 않았다)
head = ["<b>서운함을 참다가 한 번에 터지는 이유는 쌓아 둔 말이 한꺼번에 열리는 때가 따로 있기 때문이에요.</b>",
        "사주에서는 이것을 두 층으로 봐요. 위 칸 천간은 겉으로 드러나는 나, 아래 칸 지지는 속에 담아 두는 나예요.",
        "<b>아래 칸 가운데 辰·戌·丑·未 네 글자는 창고 글자예요. 안에 글자 세 개씩을 품고 있어서, 이 글자가 많으면 말을 바로 꺼내기보다 쌓아 두기 쉬워요.</b>",
        "창고는 마주 보는 글자와 부딪히는 날 열려요. 이 글은 내 창고 글자를 찾는 법, 2026년 12월에 창고가 열리기 쉬운 날, 터지기 전에 작게 꺼내는 법까지 다뤄요."]
toc_q = ["서운함을 참다가 터지는 이유, 사주에서는 어디를 볼까요?", "창고 글자 辰·戌·丑·未는 무엇을 담아 둘까요?",
         "1995년 1월 10일 낮 12시생은 왜 말이 늦을까요?", "쌓인 서운함은 언제 한꺼번에 나올까요?",
         "참으면 관계가 지켜질까요?", "터지기 전에 무엇을 해 보면 좋을까요?", "자주 묻는 질문"]
sec1 = P("<b>서운함이 쌓이는 사람은 겉으로 하는 말과 속에 남는 말이 달라요.</b>",
         "입으로는 '괜찮아'라고 하는데, 속에서는 '그때 그 말이 서운했어'가 그대로 남아 있어요.",
         "사주 여덟 글자도 위 칸 넷과 아래 칸 넷으로 나뉘어요. 위 칸 천간은 남에게 보이는 얼굴이고, 아래 칸 지지는 그 밑에 깔린 마음이에요.") + "[[I]]" + \
       P("느낀 것을 말로 꺼내는 글자는 십성으로 식상(식신·상관)이에요. 식상이 위 칸에 있으면 서운한 마음을 그 자리에서 말하기 쉬워요.",
         "식상이 아래 칸 속에만 숨어 있으면 마음은 있는데 말이 늦게 나와요. 늦게 나온 말은 그동안 쌓인 만큼 커져서 나와요.")
sec2 = P("<b>창고 글자는 지나간 계절의 기운을 모아 두는 글자예요.</b>",
         "辰은 물을, 戌은 불을, 丑은 쇠를, 未는 나무를 담아 두는 창고라고 봐요. 그래서 네 글자 모두 안에 글자 세 개씩을 품고 있어요.",
         "예를 들어 丑 안에는 癸·辛·己, 戌 안에는 辛·丁·戊가 들어 있어요. 겉은 조용한 흙인데 속은 여러 마음이 겹쳐 있는 셈이에요.") + \
       P("그래서 창고 글자가 2개 이상이면 담아 두는 양이 커요. 서운한 일이 있어도 '이 정도는 넘어가자' 하고 창고에 넣어 두는 편이에요.",
         "창고 글자가 태어난 날 아래 칸(일지)에 있으면, 특히 가족이나 연인처럼 가까운 사람에게 받은 서운함을 오래 쌓아 두기 쉬워요.",
         "창고가 크다는 것은 참을성이 크다는 뜻이기도 해요. 다만 꺼내는 날을 내가 정하지 않으면, 창고가 열리는 날이 대신 정해요.")
sec3 = P("🔎 <b>1995년 1월 10일 낮 12시에 태어난 사람을 예로 들어 볼게요.</b>",
         "여덟 글자는 甲戌·丁丑·辛丑·甲午예요. 입춘 전이라 해 기둥은 1994년의 甲戌, 띠는 개띠예요.",
         "날의 주인(일간)은 辛, 다듬은 보석 같은 쇠예요. 辛에게 말을 꺼내는 글자 식상은 물(壬·癸)이에요.") + \
       P("위 칸을 보면 甲·丁·甲이라 물이 하나도 없어요. 甲은 돈의 글자, 丁은 선을 지키는 글자라 겉으로는 해야 할 일과 지킬 선이 먼저 보여요.",
         "아래 칸에는 戌·丑·丑·午가 있고, 창고 글자가 셋이에요. 말을 꺼내는 癸는 달과 날 아래의 丑 두 곳 속에만 숨어 있어요.",
         "그래서 이 사람은 서운한 일이 생기면 그날은 웃고 넘기기 쉬워요. 집에 와서 혼자 곱씹다가 몇 주 뒤에 '사실 그때' 하고 꺼내요. 듣는 사람은 갑자기 터졌다고 느끼지만, 본인에게는 몇 주를 쌓은 말이에요.") + MID
sec4 = P("<b>창고는 마주 보는 창고 글자와 부딪힐 때 열려요.</b>",
         "辰과 戌, 丑과 未가 서로 마주 보고 부딪히는 글자예요. 내 일지가 丑인데 未가 들어오는 날이면 丑 창고 문이 흔들려요. 이때 쌓아 둔 말이 한꺼번에 나오기 쉬워요.",
         "위의 1995년 1월 10일생은 일지가 丑이라 未일이 그런 날이에요. 2026년 12월에는 11일과 23일이에요.") + "[[Q]]" + \
       P(f"내 일지가 辰이면 戌일인 12월 {dd('戌')}, 戌이면 辰일인 {dd('辰')}, 丑이면 未일인 {dd('未')}, 未면 丑일인 {dd('丑')}이에요.",
         "이날이 꼭 다툼이 나는 날이라는 뜻은 아니에요. 쌓인 말이 올라오기 쉬운 날이라, 그 전에 작게 꺼내 두면 창고가 열려도 나올 것이 적어요.",
         "내 일지는 무료 풀이에 생일만 넣으면 '태어난 날' 아래 칸에서 바로 보여요.")
sec5 = P("🧠 <b>참으면 관계가 지켜질 것 같지만, 연구에서는 오히려 거리가 생겼어요.</b>",
         "스탠퍼드 대학의 버틀러·그로스 연구진은 처음 만난 여성 두 명씩 짝을 지어 속상한 주제로 이야기하게 했어요. 그리고 한 사람에게만 '느끼는 것을 얼굴에 드러내지 말라'고 부탁했어요.",
         "그러자 대화가 자꾸 끊겼어요. 감추지 않은 짝과 견주어 앞에 앉은 상대의 혈압이 더 올랐고, 두 사람 사이의 친밀감도 덜 생겼어요.") + "[[B]]" + \
       P("그로스가 함께한 스리바스타바 연구진은 대학 신입생 278명을 첫 학기 동안 따라가 봤어요. 감정을 감추는 학생일수록 새 친구에게 받는 지지와 가까움, 관계 만족이 낮았어요. 본인이 적은 기록뿐 아니라 친구들이 본 모습에서도 같았어요.",
         "말하지 않은 서운함은 상대에게 보이지 않아요. 상대는 이유를 모른 채 어색함만 느끼고, 나는 혼자 쌓아요.",
         '📚 <b>출처 1</b>: <a href="https://doi.org/10.1037/1528-3542.3.1.48">Butler, Egloff, Wilhelm, Smith, Erickson &amp; Gross (2003), The social consequences of expressive suppression, Emotion 3(1)</a>',
         '📚 <b>출처 2</b>: <a href="https://pmc.ncbi.nlm.nih.gov/articles/PMC4141473/">Srivastava, Tamir, McGonigal, John &amp; Gross (2009), The social costs of emotional suppression, Journal of Personality and Social Psychology 96(4)</a>')
sec6 = P("<b>창고가 큰 사람은 참는 힘을 버리기보다, 꺼내는 날을 내가 정하면 돼요.</b>",
         "서운함이 들어올 때마다 다 말할 필요는 없어요. 다만 창고에 넣기 전에 한 번 이름을 붙여 두면, 나중에 꺼낼 때 지난 일까지 한꺼번에 딸려 나오지 않아요.") + \
       P("🌱 <b>마음 코치 정월의 질문</b>", "요즘 '괜찮아'라고 넘긴 일 가운데<br>아직 마음에 남아 있는 것은 무엇인가요?",
         "🔸 그 일을 한 문장으로 말한다면<br>누구에게, 어떤 말로 꺼내고 싶나요?") + "[[C]]" + \
       P("✔️ <b>터지기 전에 해 볼 것</b>",
         "1. 서운한 일이 생긴 날, 휴대폰 메모에 '무슨 일·내 마음' 두 칸만 적어 두세요.",
         "2. 메모가 두 개가 되기 전에 '그때 그 말이 조금 서운했어'처럼 한 문장으로 꺼내 보세요. 지난 일은 붙이지 않아요.",
         "3. 내 창고가 열리기 쉬운 날이 다가오면 그 전날 메모를 한 번 읽고, 남은 것이 있으면 먼저 말해 두세요.")
sec7 = P("<b>Q. 창고 글자가 없으면 서운함이 안 쌓이나요?</b>",
         "A. 아니에요. 창고 글자는 담아 두는 양을 보는 것이지, 서운함을 느끼는지를 정하지 않아요. 창고가 없어도 말을 꺼내는 글자가 속에만 있으면 쌓일 수 있어요.") + \
       P("<b>Q. 서운함을 말하면 속 좁은 사람처럼 보일까 봐 걱정돼요.</b>",
         "A. 작을 때 한 문장으로 말하면 오히려 가볍게 들려요. 몇 주를 쌓았다가 꺼내야 커 보여요. 위 연구에서도 감춘 쪽이 관계에서 거리를 더 느꼈어요.") + \
       P("<b>Q. 태어난 시를 모르면 어떻게 보나요?</b>",
         "A. 시 기둥에도 창고 글자가 올 수 있어서 개수가 하나쯤 달라질 수 있어요. 해·달·날 여섯 글자만으로 먼저 보고, 일지(날 아래 글자)부터 확인해 보세요.")
tail = P("여러분은 서운함을 바로 말하는 쪽인가요, 창고에 넣어 두는 쪽인가요?", "바로 말하면 '바로', 쌓아 두면 '창고'라고 댓글에 적어 주세요.") + \
       '<p><b>👇 말을 꺼내는 글자 식상이 십성 열 가지 가운데 어디인지 보고 싶다면, 십성 뜻 한눈에, 10가지 이름과 내 일간으로 찾는 표</b></p>'
secs = [sec1, sec2, sec3, sec4, sec5, sec6, sec7]

def _have(n): return os.path.exists(os.path.join(HERE, "img", n))
def build():
    for d_ in ("wide", "m1280", "master"): os.makedirs(os.path.join(HERE, "img", d_), exist_ok=True)
    c = V.Ctx(PAL); made = []
    a4 = f"wide/naver_z{KEY}_a4.jpg"
    if not _have(a4):
        V.render(PID + "_new", {"d": "N", "el": "흙", "kick": "서운함 참다가 터지는 이유", "hook": ["쌓아 둔 말이", "열리는 날"], "sub": "사주 창고 글자 4개로 봐요",
                                "items": ["진·술", "축·미", "12월 날짜"]}, os.path.join(HERE, "img", a4), PAL)
    made.append(a4)
    nm = {"I": f"naver_z{KEY}_i3.jpg", "Q": f"naver_z{KEY}_q3.jpg", "B": f"naver_z{KEY}_e3.jpg", "C": f"naver_z{KEY}_h3.jpg"}
    if not _have(nm["I"]):
        DGB.iceberg(nm["I"], c, "겉으로 하는 말, 속에 쌓이는 말", "괜찮아",
                    ["그때 그 말이 서운했어", "나도 많이 바빴는데", "왜 늘 내가 먼저 챙길까"],
                    "위 칸 천간은 겉, 아래 칸 지지는 속", "속에 쌓인 말을 작을 때 한 문장씩 꺼내기")
    if not _have(nm["Q"]):
        DGC.quad(nm["Q"], c, "12월, 내 창고가 열리는 날", [
            ("辰 · 물의 창고", f"戌일에 열려요. 12월 {dd('戌')}"), ("戌 · 불의 창고", f"辰일에 열려요. 12월 {dd('辰')}"),
            ("丑 · 쇠의 창고", f"未일에 열려요. 12월 {dd('未')}"), ("未 · 나무의 창고", f"丑일에 열려요. 12월 {dd('丑')}")],
            2, "자오선 계산 · 2026년 12월 일진", note="일지는 태어난 날 기둥의 아래 글자예요")
    if not _have(nm["B"]):
        DGC.exp(nm["B"], c, "속상한 이야기를 하며 표정을 감추면", "버틀러·그로스 연구진 · 2003",
                [("누가", "처음 만난 여성 두 명씩 짝을 지었어요"), ("무엇을", "속상한 주제로 대화하며 한 사람만 표정을 감췄어요"),
                 ("결과", "대화가 자꾸 끊기고, 앞에 앉은 상대의 혈압이 더 올랐어요")],
                "감출수록 두 사람 사이의 친밀감이 덜 생겼어요", "Butler 외 (2003), Emotion")
    if not _have(nm["C"]):
        DGB.checklist(nm["C"], c, "터지기 전에 꺼내는 세 칸", [("서운한 날 메모 두 칸", "무슨 일 · 내 마음"),
                                                       ("메모 두 개 전에 한 문장", "지난 일은 붙이지 않아요"),
                                                       ("창고가 열리는 날 전날", "메모를 읽고 남은 것 먼저")])
    import fullbleed as FBL
    plan_p = os.path.join(HERE, "fullbleed_plan.json"); plan = json.load(open(plan_p, encoding="utf-8")) if os.path.exists(plan_p) else {}
    rows = []
    for pos, k in enumerate("IQBC", 1):
        f = nm[k][:-4] + "f.jpg"
        if not _have(f):
            r, why = FBL.convert(nm[k], [os.path.join(HERE, "img"), os.path.join(HERE, "img", "m1280")])
            if not r: print("fullbleed 건너뜀", nm[k], why); made.append(nm[k]); continue
        rows.append({"pos": pos, "old": nm[k], "new": f}); made.append(nm[k]); nm[k] = f
        reg_ = json.load(open(DG.REG, encoding="utf-8")); reg_[f] = reg_[rows[-1]["old"]]; json.dump(dict(sorted(reg_.items())), open(DG.REG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    plan[PID] = rows; json.dump(plan, open(plan_p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    made += [v for v in nm.values() if v not in made]
    alt = {"I": "겉으로 하는 말과 속에 쌓이는 말 그림. 겉은 괜찮아, 속은 그때 그 말이 서운했어 같은 말이 쌓여 있어요",
           "Q": f"창고 글자 네 개와 2026년 12월에 열리는 날 그림. 辰은 {dd('戌')}, 戌은 {dd('辰')}, 丑은 {dd('未')}, 未는 {dd('丑')}",
           "B": "버틀러·그로스 연구진 2003년 실험 그림. 처음 만난 두 사람이 대화하며 한 사람이 표정을 감추면 대화가 끊기고 상대의 혈압이 더 올랐어요",
           "C": "터지기 전에 꺼내는 세 칸 체크 그림. 서운한 날 메모 두 칸, 메모 두 개 전에 한 문장, 창고가 열리는 날 전날 메모 읽기"}
    body = P(*head) + P("<b>📌 쌓인 서운함을 읽는 순서</b>", *[f"{i + 1}. {q}" for i, q in enumerate(toc_q)])
    for i, (q, s) in enumerate(zip(toc_q, secs)):
        for k in "IQBC": s = s.replace(f"[[{k}]]", IMG(nm[k], alt[k]))
        body += H(f"{i + 1}. {q}") + s
    body += tail + CTA
    import copy_rules as CR
    for w in ("재미로", "상담", "—", "안녕하세요, 자오선의 정월이에요", "결론부터 말씀드릴게요", "먼저 결론을", "생년월일만 넣으면 1초", "한 줄 요약", "이 글의 순서", "수비학",
              "사람의 공통점", "몇 개나 겹칠까", "투명성 착각", "고트먼", "여섯 운명학", "총정리", "힘 쓸 달", "아낄 달", "솜씨", "값을 매") + tuple(CR.금지어):
        assert w not in re.sub(r"<[^>]+>", " ", body), w
    for f in made:   # 사이트 사본(K-069)
        dst = os.path.join(SITE, "public", "naver", "img", f); os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy(os.path.join(HERE, "img", f), dst)
    return body, a4, made

TITLE = "서운함 참다가 터지는 이유, 사주 창고 글자 4개가 열리는 날"
TAGS = ["서운함", "서운한감정", "감정폭발", "서운함표현", "참다가터지는성격", "창고글자", "지장간", "표현억제", "관계심리", "자오선"]
REL = {"id": "n58", "title": "십성 뜻 한눈에, 10가지 이름과 내 일간으로 찾는 표",
       "phrase": "말을 꺼내는 글자 식상이 십성 열 가지 가운데 어디인지 보고 싶다면, 십성 뜻 한눈에, 10가지 이름과 내 일간으로 찾는 표",
       "url": "https://blog.naver.com/zaoseon/224468727235"}
KW_VOL = json.load(open(os.path.join(SITE, "data", "keywords", "kw_volume.json"), encoding="utf-8"))["posts"]["n93"]["씨앗"]
INTENT = {"keywords": ["서운함", "감정폭발", "참다가터지는성격"],
          "keyword_src": "kw-volume 작업(data/keywords/kw_volume.json posts.n93) 월 검색량 · n23 조회 순위(재발행 일정 '새 글로 다시 쓰기', 진행표 11/18 첫 줄)",
          "intent": "이유를 알고 싶다", "intent_note": "왜 서운함을 참다가 한 번에 터지는지 바로 알고, 내 글자로 확인하는 법과 터지기 전에 꺼내는 법까지 보기",
          "first3": "서운함을 참다가 한 번에 터지는 이유는 쌓아 둔 말이 한꺼번에 열리는 때가 따로 있기 때문이에요.",
          "answer_keys": ["서운함이 터지는 이유", "창고 글자 辰·戌·丑·未", "12월 열리는 날"],
          "order": toc_q[:6], "images": ["겉과 속(iceberg)", "창고 글자 넷과 12월 날짜(quad, 엔진 계산)", "표현 억제 실험(exp)", "터지기 전 세 칸(checklist)"],
          "related": "n58", "cta": PID, "experience": [], "applied": True,
          "differs_from_n23": "제목·도입(이유 직답 + 두 층)·소제목 순서·정화/황소·전갈/수비학 6 세 풀이와 '몇 개 겹칠까' 대신 천간·지지 두 층과 창고 글자(지장간)·충으로 열리는 날(2026년 12월)·예시 장면(1995.1.10 낮 12시 甲戌·丁丑·辛丑·甲午)·그림 유형(iceberg·quad·exp·checklist)·심리 개념(투명성 착각·두드리기·고트먼 → 표현 억제, Butler 외 2003·Srivastava 외 2009)·출처 2개·연결글(→ n58)·여섯 운명학 단락·면책 문장 뺌"}

if __name__ == "__main__":
    body, a4, made = build()
    reg = json.load(open(MP.REG, encoding="utf-8"))
    assert PID not in reg or not reg[PID].get("done"), "이미 예약 끝난 글"
    reg[PID] = dict(dt="2027-02-04T18:00:00", dt_tbd="CT가 정함(재발행 일정 'n23 다시 쓰기' 자리, 진행표 11/18). 이 날짜는 자리값", title=TITLE, tags=TAGS, body=body,
                    cover=a4, related=REL, thumbs=None, cid=None, clips=None, category="관계 읽기", done=False, kw_vol=KW_VOL,
                    k131="n93 11/18(K-151 새 글)", source="build_naver_93.py (n23 주제 새 글, n23 그대로)")
    json.dump(reg, open(MP.REG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    ic = json.load(open(os.path.join(HERE, "intent_cards.json"), encoding="utf-8")); ic["cards"][PID] = INTENT
    json.dump(ic, open(os.path.join(HERE, "intent_cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    v = reg[PID]
    MP.write_page(PID, D.datetime.fromisoformat(v["dt"]), v["title"], v["tags"], v["body"], None, v["cover"], v["related"], v["category"])
    MP.write_index()
    import k151_check as K
    print(PID, len(TITLE), "자 제목 · 본문 글자", len(re.sub(r"<[^>]+>|&nbsp;", "", body)), "· 사진", made, "· K 검사", K.check(PID, v))
