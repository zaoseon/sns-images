"""네이버 n101: 사주 궁합 보는 법 새 글 (CT 11/4 19:40 재발행 일정 '새 글로 다시 쓰기' n28 → n101, 진행표 docs/네이버_누락글_진행표_2026-11-18.md 여덟째 줄).
- 왜: 노출 안 되는 옛 글 n28(동양과 서양이 말하는 잘 맞는 사이, 사주 상생·별자리 원소·수비학)을 새 글로. n28은 건드리지 않는다(K-147·K-178).
- 검색어: n101 묶음(사주궁합·사주궁합보는법·궁합보는법·천간합·일간궁합) 11/20 11:45 ① 요청. 지난 측정 사주궁합 7,850·궁합 8,270(kw_volume 다른 묶음).
- 다르게 쓴 것(K-151): n28의 첫 질문·'한 줄로 정리'·세 풀이(오행 상생·별자리 네 원소·수비학 세 무리)·'몇 개나 맞을까'·가상 두 사람(갑목·쌍둥이·3)·여섯 운명학·확증 편향(Nickerson 1998) 대신
  사주 궁합 정의 직답, 일간 오행(키움·누름) → 일간이 합이 되는 다섯 쌍(甲己·乙庚·丙辛·丁壬·戊癸, 다섯 쌍 모두 오행으로는 누르는 사이라는 점),
  예시 두 사람 1996.3.8 낮 12시(丙子·辛卯·甲辰·庚午)와 1994.7.22 낮 12시(甲戌·辛未·己酉·庚午) — 일간 甲己 합, 일지 辰酉 육합(engine assert),
  2027 해 글자 丁 → 壬 일간과 합(engine assert), 심리 = 실제 닮음과 닮았다고 느끼는 마음(Montoya, Horton & Kirchner 2008 메타분석, 313개 연구·460개 효과크기).
  그림 유형 cycle5·compare·bignum. 연결글 → n72(띠 궁합 제대로 보는 법, 11/20 노출 '예' 1위). 띠 삼합·원진(n72)과 띠 궁합표(n83)는 다루지 않는다.
- 출처 2개(K-162, 11/20 원문 확인): Montoya, Horton & Kirchner (2008), Is actual similarity necessary for attraction? JSPR 25(6) 889-922, DOI 10.1177/0265407508096700
  (Murdoch 대학 연구 포털 초록: 313개 연구 460개 효과크기, 실제 닮음 r=.47·느낀 닮음 r=.39, 만나지 않은·짧게 만난 사이에서는 실제 닮음이 중요, 이미 이어진 사이에서는 실제 닮음 효과가 뚜렷하지 않고 느낀 닮음은 끌림을 예측)
  · 한국천문연구원 음양력 변환(절기 시각).
- 날짜: CT가 정한다. pages.json dt 는 자리값, dt_tbd 로 표시.
사용: SITE=<zaoseon-site> python3 naver/build_naver_101.py"""
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
       '<tr><td style="padding:12px 10px;text-align:center;border:1px solid #d0d0d0"><b>두 사람의 태어난 날 첫 글자가 궁금하다면</b></td></tr>'
       '<tr><td style="padding:12px 10px;text-align:center;border:1px solid #d0d0d0"><span style="color:#9a9a9a">[ 1996 . 03 . 08 ]</span></td></tr>'
       '<tr><td style="padding:12px 10px;text-align:center;border:1px solid #d0d0d0"><b><a href="https://zaoseon.com/?utm_source=naver&amp;utm_medium=mid#free">내 태어난 날 글자 보기 →</a></b></td></tr>'
       '</tbody></table>' + BL)
CTA = ('<p><a href="https://zaoseon.com/?utm_source=naver&utm_medium=cta#free"><img src="' + RAW +
       'naver_cta5_1%EC%B4%88%EB%AC%B4%EB%A3%8C%ED%92%80%EC%9D%B4.jpg" alt="자오선 무료 1초 풀이 안내 배너"></a></p>')
PID, KEY, PAL = "n101", "101", "y_black_s"   # 甲己 합 = 흙 → 흙 판 묶음(EL_SET 흙). n100 dg_gold_s · n99 m_soft_s · n98 k_white_s 와 다른 판

# ───────── 계산값과 검산
import datetime as D
sys.path.insert(0, os.path.join(SITE, "engine"))
import engine as E
EL = {"甲": "나무", "乙": "나무", "丙": "불", "丁": "불", "戊": "흙", "己": "흙", "庚": "쇠", "辛": "쇠", "壬": "물", "癸": "물"}
GROW = {"나무": "불", "불": "흙", "흙": "쇠", "쇠": "물", "물": "나무"}          # 키워 줌
PRESS = {"나무": "흙", "흙": "물", "물": "불", "불": "쇠", "쇠": "나무"}         # 누름
HAP = [("甲", "己", "흙"), ("乙", "庚", "쇠"), ("丙", "辛", "물"), ("丁", "壬", "나무"), ("戊", "癸", "불")]   # 천간합(통용 기준)
for a, b, _ in HAP: assert PRESS[EL[a]] == EL[b] or PRESS[EL[b]] == EL[a], (a, b)   # 다섯 쌍 모두 한쪽이 다른 쪽을 누름(양 글자가 음 글자를)
A = E.compute_saju(D.datetime(1996, 3, 8, 12, 0))["팔자"]
B = E.compute_saju(D.datetime(1994, 7, 22, 12, 0))["팔자"]
assert A == {"년주": "丙子", "월주": "辛卯", "일주": "甲辰", "시주": "庚午"}, A
assert B == {"년주": "甲戌", "월주": "辛未", "일주": "己酉", "시주": "庚午"}, B
assert E.compute_saju(D.datetime(1996, 3, 8, 12, 50))["팔자"] == A and E.compute_saju(D.datetime(1994, 7, 22, 12, 50))["팔자"] == B   # 같은 午시 안
assert (A["일주"][0], B["일주"][0]) == ("甲", "己")                            # 일간 합
LIU = [set("子丑"), set("寅亥"), set("卯戌"), set("辰酉"), set("巳申"), set("午未")]
assert set(A["일주"][1] + B["일주"][1]) in LIU                                 # 일지 辰酉 육합
assert E.compute_saju(D.datetime(2027, 3, 1, 12))["팔자"]["년주"] == "丁未"     # 2027 해 글자 丁 → 壬과 합
assert E.ten_god("甲", "己") == "정재" and E.ten_god("己", "甲") == "정관"
print("합 다섯 쌍 = 이기는 사이 · 예시 두 사람 甲辰·己酉(일간 합, 일지 辰酉) · 2027 丁未 확인")

# ───────── 본문 (n28 문장을 옮기지 않았다)
head = ["<b>사주 궁합은 두 사람의 태어난 날 첫 글자(일간)끼리 어떤 사이인지 보는 거예요. 서로 키워 주는지, 이기는지, 만나서 새 오행 하나로 묶이는 '합'인지를 먼저 봐요.</b>",
        "일간이 합이 되는 짝은 다섯 쌍뿐이에요. 갑·기(甲己), 을·경(乙庚), 병·신(丙辛), 정·임(丁壬), 무·계(戊癸)예요.",
        "<b>심리학에서 313개 연구를 모아 보니, 오래 만난 사이에서는 실제로 닮았는지보다 '우리는 닮았다'고 느끼는 마음이 끌림과 더 이어졌어요.</b>",
        "이 글은 사주 궁합을 읽는 순서, 합이 되는 다섯 쌍, 예시 두 사람, 닮음에 관한 연구, 두 사람이 해 볼 것까지 다뤄요."]
toc_q = ["사주 궁합은 무엇부터 볼까요?", "일간이 합이 되는 5쌍은 무엇일까요?", "1996년 3월 8일생과 1994년 7월 22일생은 어떻게 읽을까요?",
         "닮은 사람끼리 더 잘 맞을까요?", "궁합을 보고 나서 둘이 해 볼 것", "자주 묻는 질문"]
toc_s = ["사주 궁합 보는 순서", "일간이 합이 되는 다섯 쌍", "1996년 3월 8일생과 1994년 7월 22일생 예시", "닮음과 끌림", "둘이 해 볼 것", "묻고 답하기"]   # 11/21 ① 목차 짧은 이름(RP-01)
sec1 = P("<b>사주 궁합은 일간 오행 두 개를 나란히 놓는 데서 시작해요.</b>",
         "갑·을은 나무, 병·정은 불, 무·기는 흙, 경·신은 쇠, 임·계는 물이에요.",
         "나무는 불을, 불은 흙을, 흙은 쇠를, 쇠는 물을, 물은 나무를 키워 줘요. 한쪽이 다른 쪽을 키우면 기대기 편한 사이로 봐요.") + "[[Y]]" + \
       P("거꾸로 나무는 흙을, 흙은 물을, 물은 불을, 불은 쇠를, 쇠는 나무를 이겨요. 이기는 사이도 나쁜 짝은 아니에요. 한 사람이 끌고 한 사람이 받치는 모양이에요.",
         "같은 오행끼리는 편하지만 둘 다 같은 일에 치우치기 쉬워요. 그래서 오행 다음에 '합'이 있는지를 한 번 더 봐요.") + MID
sec2 = P("<b>합은 두 글자가 만나 새 오행 하나로 묶이는 걸 말해요. 일간끼리 합이 되면 서로 자꾸 눈이 가는 사이로 봐요.</b>") + "[[S]]" + \
       P("눈여겨볼 점이 있어요. 다섯 쌍 모두 오행으로만 보면 한쪽이 다른 쪽을 이기는 사이예요. 갑(나무)은 기(흙)를, 경(쇠)은 을(나무)을, 무(흙)는 계(물)를 이겨요.",
         "이기는 사이인데 만나면 하나로 묶이는 것, 그래서 합이 된 짝은 다르면서도 떨어지기 어려운 사이로 봐요.",
         "합은 나쁜 쪽이 없는 게 아니에요. 묶이는 힘이 큰 만큼 한 사람이 자기 색을 잃기 쉬우니, 각자 혼자 쓰는 시간을 정해 두는 게 좋아요.") + \
       P("2027년은 해의 첫 글자가 丁(불)이에요. 丁과 합이 되는 글자가 壬이라, 둘 중 한 사람이 임(壬) 일간이면 2027년에는 둘 사이에 새로 묶이는 일(함께 사는 일, 같이 하는 일)이 생기기 쉬운 해로 봐요.")
sec3 = P("🔎 <b>1996년 3월 8일 낮 12시생 A와 1994년 7월 22일 낮 12시생 B를 예로 들어 볼게요.</b>",
         "A의 여덟 글자는 丙子·辛卯·甲辰·庚午, 일간은 갑(甲) 나무예요. B는 甲戌·辛未·己酉·庚午, 일간은 기(己) 흙이에요.",
         "두 사람의 일간이 갑·기, 합으로 묶이는 사이예요. 오행으로는 A의 나무가 B의 흙을 이기는 사이라, A가 먼저 정하고 B가 받쳐 주는 그림이 자주 나와요.") + \
       P("태어난 날 아래 글자(일지)도 봐요. A는 辰, B는 酉인데 辰과 酉도 서로 합이 되는 짝(육합)이에요. 겉으로 끌리는 데다 생활 습관도 잘 맞아요.",
         "이런 짝은 다툼이 적은 대신, B가 '늘 맞춰 준다'고 느끼는 날이 쌓이기 쉬워요. 고를 일 하나는 B가 정하게 번갈아 맡기면 균형이 잡혀요.",
         '📚 <b>출처 2</b>: <a href="https://astro.kasi.re.kr/life/pageView/5">한국천문연구원 천문우주지식정보, 음양력 변환(절기 시각)</a>')
sec4 = P("🧠 <b>닮은 사람끼리 끌린다는 말은 심리학에서 오래 다룬 주제예요.</b>",
         "심리학자 몬토야·호턴·커치너는 실험실과 실제 관계를 다룬 313개 연구, 460개 결과를 한데 모아 다시 셈했어요(2008).") + "[[N]]" + \
       P("처음 만났거나 짧게 만난 사이에서는 실제로 성격이나 생각이 닮은 사람에게 더 끌렸어요.",
         "그런데 이미 이어진 관계에서는 실제로 닮았는지가 끌림과 뚜렷하게 이어지지 않았어요. 대신 '우리는 닮았다'고 느끼는 마음은 어느 단계에서나 끌림과 이어졌어요.",
         "사주 궁합도 같은 자리에 놓고 보면 좋아요. 합이 없다고 끝난 사이가 아니에요. 오래 갈수록 중요한 건 둘이 같은 쪽을 보고 있다고 느끼는 순간이에요.",
         '📚 <b>출처 1</b>: <a href="https://doi.org/10.1177/0265407508096700">Montoya, Horton &amp; Kirchner (2008), Is actual similarity necessary for attraction? A meta-analysis of actual and perceived similarity, Journal of Social and Personal Relationships</a>')
sec5 = P("<b>궁합은 맞고 안 맞고를 가르는 표가 아니라, 어디서 맞춰 갈지 알려 주는 지도예요.</b>") + \
       P("🌱 <b>마음 코치 정월의 질문</b>", "우리 둘이 닮았다고 느낀<br>가장 최근의 순간은 언제였나요?",
         "🔸 서로 다르다고 느낀 일 하나는<br>어떻게 나눠 맡으면 좋을까요?") + \
       P("✔️ <b>둘이 해 볼 세 가지</b>",
         "1. 두 사람의 일간을 나란히 적고, 키워 주는지·이기는지·합인지 표시해 보세요.",
         "2. 이기는 사이라면 이번 주에 정할 일 하나를 받치는 쪽이 정하게 맡겨 보세요.",
         "3. 이번 주 안에 '이건 우리 둘이 똑같다' 싶은 것 하나를 서로에게 말해 보세요. 닮았다고 느끼는 순간이 쌓여요.")
sec6 = P("<b>Q. 일간이 합이 아니면 궁합이 나쁜 건가요?</b>",
         "A. 아니에요. 합이 되는 짝은 다섯 쌍뿐이라 대부분의 짝은 합이 없어요. 키워 주는 사이, 같은 오행 사이도 충분히 잘 지내요.") + \
       P("<b>Q. 띠 궁합과 사주 궁합은 무엇이 다른가요?</b>",
         "A. 띠 궁합은 태어난 해 아래 글자로 보고, 사주 궁합은 태어난 날 글자까지 봐요. 같은 해에 태어나도 일간이 다르면 사주 궁합은 달라져요.") + \
       P("<b>Q. 태어난 시간을 몰라도 볼 수 있나요?</b>",
         "A. 일간과 일지는 태어난 날만 알면 나와서 위 순서대로 볼 수 있어요. 시간까지 알면 여덟 글자 전체로 더 넓게 읽어요.")
tail = P("두 분의 일간은 키워 주는 사이인가요, 이기는 사이인가요, 합으로 묶이는 사이인가요?", "위 순서대로 찾아보고 댓글에 '키움·이김·합' 중 하나만 남겨 주세요.") + \
       '<p><b>👇 두 사람의 띠 궁합도 같이 보고 싶다면, 띠 궁합 제대로 보는 법, 삼합·육합·원진으로 보는 띠별 궁합</b></p>'
secs = [sec1, sec2, sec3, sec4, sec5, sec6]

def _have(n): return os.path.exists(os.path.join(HERE, "img", n))
def build():
    for d_ in ("wide", "m1280", "master"): os.makedirs(os.path.join(HERE, "img", d_), exist_ok=True)
    c = V.Ctx(PAL); made = []
    a4 = f"wide/naver_z{KEY}_a6.jpg"   # 11/21 ① a5→a6: 표지 훅 '누르는'→'이기는'(문체 규격 v1 ABS-05). a5 는 그대로 둔다   # 표지 항목은 한글만(한자는 글꼴에 없어 네모, 11/18 n96 a4)
    if not _have(a4):
        V.render(PID + "_new", {"d": "N", "el": "흙", "kick": "사주 궁합 보는 법", "hook": ["이기는 사이인데", "합이 되는 짝"], "sub": "일간 합 다섯 쌍과 두 사람 예시",
                                "items": ["갑·기", "을·경", "병·신"]}, os.path.join(HERE, "img", a4), PAL)
    made.append(a4)
    nm = {"Y": f"naver_z{KEY}_y4.jpg", "S": f"naver_z{KEY}_s4.jpg", "N": f"naver_z{KEY}_n3.jpg"}
    if not _have(nm["Y"]):
        DGB.cycle5(nm["Y"], c, "일간 오행, 키워 주는지 이기는지", note="두 사람의 일간 오행을 이 바퀴에서 찾아 보세요", press="이기는 관계(맞춰 갈 게 많은 사이)")
    if not _have(nm["S"]):
        DGC.compare(nm["S"], c, "일간이 합이 되는 다섯 쌍", ("오행으로 보면", "합으로 보면"),
                    [("갑·기", "나무가 흙을 이겨요", "묶이면 흙"), ("을·경", "쇠가 나무를 이겨요", "묶이면 쇠"), ("병·신", "불이 쇠를 이겨요", "묶이면 물"),
                     ("정·임", "물이 불을 이겨요", "묶이면 나무"), ("무·계", "흙이 물을 이겨요", "묶이면 불")], "천간합 통용 기준", hi=1)
    if not _have(nm["N"]):
        DGC.bignum(nm["N"], c, "닮아서 끌릴까, 닮았다고 느껴서 끌릴까", "313", "개 연구를 모아 다시 셈했어요",
                   [("처음 만남", "실제로 닮은 사람에게 더 끌렸어요"), ("오래 만남", "실제로 닮았는지는 뚜렷한 차이가 없었어요"),
                    ("느낀 닮음", "닮았다고 느끼는 마음은 어느 단계에서나 끌림과 이어졌어요")],
                   "Montoya·Horton·Kirchner (2008), Journal of Social and Personal Relationships")
    import fullbleed as FBL
    plan_p = os.path.join(HERE, "fullbleed_plan.json"); plan = json.load(open(plan_p, encoding="utf-8")) if os.path.exists(plan_p) else {}
    rows = []
    for pos, k in enumerate("YSN", 1):
        f = nm[k][:-4] + "f.jpg"
        if not _have(f):
            r, why = FBL.convert(nm[k], [os.path.join(HERE, "img"), os.path.join(HERE, "img", "m1280")])
            if not r: print("fullbleed 건너뜀", nm[k], why); made.append(nm[k]); continue
        rows.append({"pos": pos, "old": nm[k], "new": f}); made.append(nm[k]); nm[k] = f
        reg_ = json.load(open(DG.REG, encoding="utf-8")); reg_[f] = reg_[rows[-1]["old"]]; json.dump(dict(sorted(reg_.items())), open(DG.REG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    plan[PID] = rows; json.dump(plan, open(plan_p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    made += [v for v in nm.values() if v not in made]
    alt = {"Y": "일간 오행 바퀴 그림. 나무는 불을, 불은 흙을, 흙은 쇠를, 쇠는 물을, 물은 나무를 키워 주고, 두 칸 건너는 이기는 관계예요",
           "S": "일간이 합이 되는 다섯 쌍 그림. 갑·기는 묶이면 흙, 을·경은 쇠, 병·신은 물, 정·임은 나무, 무·계는 불이 되고, 다섯 쌍 모두 오행으로는 이기는 사이예요",
           "N": "313개 연구를 모은 닮음 연구 그림. 처음 만난 사이에서는 실제로 닮은 사람에게 더 끌렸고, 오래 만난 사이에서는 닮았다고 느끼는 마음이 끌림과 이어졌어요"}
    body = P(*head) + P("<b>📌 사주 궁합을 읽는 순서</b>", *[f"{i + 1}. {q}" for i, q in enumerate(toc_s)])
    for i, (q, s) in enumerate(zip(toc_q, secs)):
        for k in "YSN": s = s.replace(f"[[{k}]]", IMG(nm[k], alt[k]))
        body += H(f"{i + 1}. {q}") + s
    body += tail + CTA
    import copy_rules as CR
    for w in ("재미로", "상담", "—", "안녕하세요, 자오선의 정월이에요", "결론부터 말씀드릴게요", "핵심부터", "한 줄로 정리", "생년월일만 넣으면 1초", "한 줄 요약", "이 글의 순서", "수비학",
              "공통점", "몇 개나", "여섯 운명학", "확증 편향", "엠페도클레스", "추연", "원소", "쌍둥이자리", "사수자리", "총정리", "솜씨", "값을 매", "내게", "찰떡") + tuple(CR.금지어):
        assert w not in re.sub(r"<[^>]+>", " ", body), w
    for f in made:   # 사이트 사본(K-069)
        dst = os.path.join(SITE, "public", "naver", "img", f); os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy(os.path.join(HERE, "img", f), dst)
    return body, a4, made

TITLE = "사주 궁합 보는 법, 일간이 합이 되는 5쌍과 두 사람 예시"
TAGS = ["사주궁합", "사주궁합보는법", "궁합보는법", "궁합", "일간궁합", "천간합", "오행궁합", "연애궁합", "닮은사람", "자오선"]
REL = {"id": "n72", "title": "띠 궁합 제대로 보는 법, 삼합·육합·원진으로 보는 띠별 궁합",
       "phrase": "두 사람의 띠 궁합도 같이 보고 싶다면, 띠 궁합 제대로 보는 법, 삼합·육합·원진으로 보는 띠별 궁합",
       "url": "https://blog.naver.com/zaoseon/224447869316"}
KW_VOL = (json.load(open(os.path.join(SITE, "data", "keywords", "kw_volume.json"), encoding="utf-8"))["posts"].get(PID) or {}).get("씨앗") or {}
INTENT = {"keywords": ["사주궁합", "사주궁합보는법", "궁합보는법"],
          "keyword_src": "n28 재발행 일정 '새 글로 다시 쓰기'(진행표 11/18 여덟째 줄) · 월 검색량은 kw-volume n101 요청(11/20 11:45), 지난 측정 사주궁합 7,850",
          "intent": "방법을 알고 싶다", "intent_note": "사주 궁합을 무엇부터 보는지, 일간 합이 무엇인지, 합이 없으면 나쁜지, 닮은 사람끼리 잘 맞는지",
          "first3": "사주 궁합은 두 사람의 일간끼리 키워 주는지, 이기는지, 합인지 보는 거예요. 일간이 합이 되는 짝은 다섯 쌍뿐이에요. 오래 만난 사이에서는 실제로 닮았는지보다 닮았다고 느끼는 마음이 끌림과 더 이어졌어요.",
          "answer_keys": ["사주 궁합 = 일간끼리의 관계", "키움·이김·합 세 가지", "합 다섯 쌍은 모두 오행으로는 이기는 사이", "느낀 닮음이 오래 만난 사이에서 더 중요"],
          "community_q": [], "order": toc_q, "images": ["일간 오행 바퀴(cycle5)", "합 다섯 쌍(compare)", "닮음 연구 313(bignum)"],
          "related": "n72", "cta": PID, "experience": [], "applied": True,
          "differs_from_n28": "제목(동양과 서양이 말하는 잘 맞는 사이 → 사주 궁합 보는 법·합 5쌍)·도입(정의 직답)·소제목 순서·세 풀이(오행·별자리 원소·수비학)·'몇 개나 맞을까'·가상 두 사람·여섯 운명학·확증 편향(Nickerson 1998) 대신 일간 오행 → 합 다섯 쌍(모두 이기는 사이)·예시 1996.3.8/1994.7.22(甲辰·己酉, 일간 합·일지 육합, 엔진 assert)·2027 丁壬·닮음 메타분석(Montoya 외 2008)·그림 유형(cycle5·compare·bignum)·연결글(→ n72)"}

if __name__ == "__main__":
    body, a4, made = build()
    reg = json.load(open(MP.REG, encoding="utf-8"))
    assert PID not in reg or not reg[PID].get("done"), "이미 예약 끝난 글"
    reg[PID] = dict(dt="2027-02-09T18:00:00", dt_tbd="CT가 정함(재발행 일정 'n28 다시 쓰기' 자리, 진행표 11/18). 이 날짜는 자리값", title=TITLE, tags=TAGS, body=body,
                    cover=a4, related=REL, thumbs=None, cid=None, clips=None, category="관계 읽기", done=False, kw_vol=KW_VOL,
                    k131="n101 11/20(K-151 새 글)", source="build_naver_101.py (n28 주제 새 글, n28 그대로)")
    json.dump(reg, open(MP.REG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    ic = json.load(open(os.path.join(HERE, "intent_cards.json"), encoding="utf-8")); ic["cards"][PID] = INTENT
    json.dump(ic, open(os.path.join(HERE, "intent_cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    v = reg[PID]
    MP.write_page(PID, D.datetime.fromisoformat(v["dt"]), v["title"], v["tags"], v["body"], None, v["cover"], v["related"], v["category"])
    MP.write_index()
    import k151_check as K
    print(PID, len(TITLE), "자 제목 · 본문 글자", len(re.sub(r"<[^>]+>|&nbsp;", "", body)), "· 사진", made, "· K 검사", K.check(PID, v))
