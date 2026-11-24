"""네이버 n109: 통장 쪼개기 새 글 (CT 11/4 재발행 일정 '새 글로 다시 쓰기' n18 → n109, 진행표 docs/네이버_누락글_진행표_2026-11-18.md 열다섯째 줄).
- 왜: 노출 안 되는 옛 글 n18(돈이 모이는 사람의 공통점, 사주와 별자리가 똑같이 흙을 가리켜요)을 새 글로. n18은 건드리지 않는다(K-147·K-178).
- 검색어: kw_volume 기존 값 통장쪼개기 660 · 돈관리 240(plan_블프 11월 측정). n109 씨앗(통장쪼개기·돈모으는법·돈관리·월급관리·돈이모이는사람)은 11/24 11:5x 요청.
- 새 원칙(CLAUDE.md 0~1-3): 첫 줄은 장면(ZS-01), 정의는 첫 200자 안, 모순 하나(아끼려 애쓰는데 한 통장에서 다 꺼내 씀) → 잡을 것/놓을 것,
  면책·출처 줄·설문지 코너·이모지 머리·목차 줄 없음, 링크는 말 속 낱말에.
- 다르게 쓴 것(K-151): n18의 한 줄 요약·세 풀이(무토·기토·흙의 별자리·수비학 4·8)·'나는 몇 개나 겹칠까' 대신
  봉투 나누기 실험(Soman & Cheema 2011, Journal of Marketing Research 48 특별호 S14-S22: 인도 건설 현장 146가구 14주,
  봉투 하나 평균 241루피 대 둘로 나눔 414루피, 아이 사진 있음 350 대 없음 304, 목표 금액 40·80루피 차이는 의미 없음 — 러셀세이지재단 공개 PDF 원문 확인),
  사주 = 재성(정재)과 비견·겁재, 예시 둘(1997.7.19 오전 8시 壬 일간 정재 丁 두 자리 / 1998.2.26 밤 8시 甲 일간 비견 甲 두 자리 + 편재 戊 하나, engine assert).
  일간 정재 짝 열 개 ten_god assert. 그림 compare(실험)·compare(사주)·checklist. 표 1개(통장 | 넣는 돈 | 규칙). 연결글 → n43(노출 '예').
- 날짜: CT가 정한다. pages.json dt 는 자리값, dt_tbd 로 표시.
사용: SITE=<zaoseon-site> python3 naver/build_naver_109.py"""
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
       '<tr><td style="padding:12px 10px;text-align:center;border:1px solid #d0d0d0"><b>내 여덟 글자에 정재가 있는지 궁금하다면</b></td></tr>'
       '<tr><td style="padding:12px 10px;text-align:center;border:1px solid #d0d0d0"><span style="color:#9a9a9a">[ 1997 . 07 . 19 ]</span></td></tr>'
       '<tr><td style="padding:12px 10px;text-align:center;border:1px solid #d0d0d0"><b><a href="https://zaoseon.com/?utm_source=naver&amp;utm_medium=mid#free">내 태어난 날 글자 보기 →</a></b></td></tr>'
       '</tbody></table>' + BL)
CTA = ('<p><a href="https://zaoseon.com/?utm_source=naver&utm_medium=cta#free"><img src="' + RAW +
       'naver_cta5_1%EC%B4%88%EB%AC%B4%EB%A3%8C%ED%92%80%EC%9D%B4.jpg" alt="자오선 무료 1초 풀이 안내 배너"></a></p>')
PID, KEY, PAL = "n109", "109", "p_purple_s"   # 예시 일간 壬 = 물 판 묶음(g_ivory_s 는 checklist 글 대비 1.2~1.35 막음). n108 k_neon_s · n107 p_red_s · n106 m_soft_s · n105 p_black_s 와 다른 판

# ───────── 계산값과 검산
import datetime as D
sys.path.insert(0, os.path.join(SITE, "engine"))
import engine as E
JJ = {"甲": "己", "乙": "戊", "丙": "辛", "丁": "庚", "戊": "癸", "己": "壬", "庚": "乙", "辛": "甲", "壬": "丁", "癸": "丙"}
for a_, b_ in JJ.items(): assert E.ten_god(a_, b_) == "정재", (a_, b_)
A = E.compute_saju(D.datetime(1997, 7, 19, 8))["팔자"]
assert A == {"년주": "丁丑", "월주": "丁未", "일주": "壬戌", "시주": "甲辰"}, A
assert [E.ten_god("壬", A[k][0]) for k in ("년주", "월주")] == ["정재", "정재"]
assert E.compute_saju(D.datetime(1997, 7, 19, 8, 50))["팔자"] == A                 # 같은 辰시 안
B = E.compute_saju(D.datetime(1998, 2, 26, 20))["팔자"]
assert B == {"년주": "戊寅", "월주": "甲寅", "일주": "甲辰", "시주": "甲戌"}, B
assert [E.ten_god("甲", B[k][0]) for k in ("년주", "월주", "시주")] == ["편재", "비견", "비견"]
assert E.compute_saju(D.datetime(1998, 2, 26, 20, 50))["팔자"] == B                # 같은 戌시 안
# 실험값(논문 원문): 봉투 하나 241 · 둘 414 루피, 14주, 146가구
assert round(414 / 241, 1) == 1.7
print("예시 A 壬戌 일간 · 丁 정재 두 자리 / 예시 B 甲辰 일간 · 甲 비견 두 자리·戊 편재 하나 · 정재 짝 열 개 · 414/241=1.7 확인")

# ───────── 본문 (n18 문장을 옮기지 않았다)
JMR = "https://www.russellsage.org/sites/default/files/u137/jmr-C-s014-s021-online.pdf"   # Soman & Cheema 2011 원문 PDF
ROT = "https://rotman.utoronto.ca/Connect/Rotman-MAG/IdeaExchange/Dilip-Soman"   # 소먼 교수 해설(같은 실험, 원문 확인)
N58 = "https://blog.naver.com/zaoseon/224468727235"   # 십성 뜻 한눈에(노출 '예')
head = ["<b>월급 들어온 지 열흘, 통장 앱 열기가 무서워요. 딱히 산 것도 없는데 잔고가 반으로 줄어 있어요.</b>",
        "아끼자니 숨이 막히고, 그냥 두자니 다음 달도 똑같을 게 뻔하죠. 통장 쪼개기는 월급을 쓸 돈, 나갈 돈, 모을 돈으로 통장부터 나눠 담는 방법이에요. 돈이 모이는 사람은 덜 쓰는 사람이라기보다 쓰기 전에 먼저 나눠 두는 사람이고요.",
        "같은 돈을 봉투 하나에 넣느냐 둘로 나누느냐만 바꾼 실험에서도, 모인 돈이 1.7배 차이 났어요."]
toc_q = ["아끼는데도 왜 돈이 안 모일까요?", "통장을 나누면 정말 더 모일까요?", "통장 쪼개기는 몇 개로 나눌까요?",
         "사주로 보면 모으는 사람과 새는 사람은 누구일까요?", "이번 월급날엔 무엇부터 할까요?", "자주 묻는 질문"]
sec1 = P("<b>한 통장에 다 들어 있으면 남은 돈이 전부 '써도 되는 돈'으로 보이니까요.</b>",
         "잔고가 한 덩어리로 보이면 커피 한 잔, 택시 한 번이 다 '이 정도는 괜찮지'가 돼요. 카드값 빠지는 날에야 그게 다음 달 몫이었다는 걸 알게 되고요.",
         "덜 쓰려고 애쓰는 마음과 한 통장에서 다 꺼내 쓰는 습관이 같이 있으니, 아무리 참아도 남는 게 없는 거예요. 잡을 건 의지가 아니라 돈이 놓이는 자리예요.")
sec2 = P("<b>네, 나눠 담기만 해도 손이 덜 가요.</b>",
         f"토론토대 소먼 교수와 버지니아대 치마 교수는 인도의 한 건설 현장에서 일당을 받는 146가구와 <a href=\"{JMR}\">14주 동안 실험</a>을 했어요. 매주 모을 돈을 떼어 봉인한 봉투에 넣어 줬는데, 절반은 봉투 하나에, 나머지 절반은 같은 돈을 <a href=\"{ROT}\">봉투 두 개에 나눠</a> 담았어요.") + "[[S]]" + \
       P("14주 뒤 봉투 하나였던 집은 평균 241루피, 둘로 나눈 집은 414루피를 모았어요. 급해서 하나를 뜯더라도 다른 하나는 남았거든요.",
         "봉투에 아이 사진을 붙인 집은 더 모았어요. 모으는 이유가 눈에 보이면 꺼내기 전에 한 번 더 멈추게 되는 거죠.")
TD = 'style="padding:10px;border:1px solid #d0d0d0'
TABLE = ('<table style="width:100%;border-collapse:collapse"><tbody>'
         f'<tr><td {TD};text-align:center"><b>통장</b></td><td {TD};text-align:center"><b>넣는 돈</b></td><td {TD};text-align:center"><b>규칙</b></td></tr>'
         + "".join(f'<tr><td {TD}">{a}</td><td {TD}">{b}</td><td {TD}">{c}</td></tr>' for a, b, c in [
             ("월급 통장", "월급·부수입", "들어온 날 다른 통장으로 보내고 비워 둬요"),
             ("고정비 통장", "월세·통신비·보험·구독", "자동이체를 전부 여기로 모아요"),
             ("생활비 통장", "한 달 쓸 돈", "체크카드는 이 통장에만 연결해요"),
             ("모으는 통장", "저축·비상금", "통장 이름에 모으는 이유를 적어요")])
         + '</tbody></table>' + BL)
sec3 = P("<b>처음엔 네 개면 충분해요. 들어오는 곳, 빠져나가는 곳, 쓰는 곳, 모으는 곳이요.</b>") + TABLE + \
       P("모으는 통장 이름을 '내년 이사 보증금'처럼 바꿔 두면, 아이 사진 붙인 봉투와 같은 일을 해요.",
         "통장을 열 개씩 만들 필요는 없어요. 옮기는 일 자체가 귀찮아지면 석 달을 못 가니까요.")
sec4 = P(f"<b>사주에서는 내가 다루는 돈을 재성이라고 하는데, 꼬박꼬박 쌓이는 돈은 <a href=\"{N58}\">정재</a>로 봐요.</b>",
         "정재가 또렷하면 정해 둔 돈을 정해 둔 자리에 두는 일이 편해요. 나와 같은 글자인 비견·겁재가 많으면 돈이 사람을 따라 나가기 쉽고요. 모임, 한턱, 경조사가 유난히 잦은 사람이 여기 많아요.") + "[[C]]" + \
       P("🔎 1997년 7월 19일 오전 8시생은 丁丑·丁未·壬戌·甲辰이에요. 임(壬) 일간에게 정재인 丁이 두 자리라, 월급날 정해 둔 만큼 옮기는 걸 잘해요.",
         "1998년 2월 26일 밤 8시생은 戊寅·甲寅·甲辰·甲戌로, 갑(甲) 일간 옆에 같은 甲이 두 자리 더 있고 돈 글자 戊는 하나예요. 버는 힘은 있는데 사람 만나는 자리에서 돈이 새기 쉬워요.",
         "모으는 사람은 모으는 통장 하나면 되고, 새는 사람은 '사람 통장'을 하나 더 두면 돼요. 모임·선물·경조사 돈을 거기서만 꺼내면 생활비가 덜 흔들려요.") + MID
sec5 = P("<b>월급이 들어온 날, 쓰기 전에 옮기는 것 하나만 정하면 돼요.</b>") + "[[K]]" + \
       P("금액은 작아도 괜찮아요. 같은 실험에서 모을 돈을 크게 잡았느냐는 차이가 거의 없었고, 나눠 담았느냐가 훨씬 큰 차이를 냈어요.",
         "이번 월급날엔 '얼마 모을까'보다 '어디로 먼저 보낼까'부터 정해 두세요. 그 한 번이 다음 달 잔고를 바꿔요.")
sec6 = P("<b>Q. 통장 쪼개기, 몇 개가 적당해요?</b>",
         "A. 서너 개면 돼요. 늘릴수록 옮기는 일이 귀찮아져서 오래 못 가요.") + \
       P("<b>Q. 비상금은 어디에 둬요?</b>",
         "A. 체크카드가 연결되지 않은 통장이 좋아요. 꺼내려면 한 번 옮겨야 하니까, 그 사이에 정말 급한 일인지 한 번 더 보게 돼요.")
tail = P("여러분은 월급날 통장부터 나누는 쪽인가요, 일단 두고 보는 쪽인가요?", "댓글에 '나눔'이나 '그냥' 한 마디만 남겨 주세요.") + \
       '<p><b>👇 돈 쓰고 나서 후회하는 소비심리가 궁금하다면, 소비심리 뜻, 돈 쓰고 후회하는 3가지 모양 사주와 별자리로</b></p>'
secs = [sec1, sec2, sec3, sec4, sec5, sec6]

def _have(n): return os.path.exists(os.path.join(HERE, "img", n))
def build():
    for d_ in ("wide", "m1280", "master"): os.makedirs(os.path.join(HERE, "img", d_), exist_ok=True)
    c = V.Ctx(PAL); made = []
    a4 = f"wide/naver_z{KEY}_a1.jpg"   # 표지 항목은 한글만(한자는 글꼴에 없어 네모)
    if not _have(a4):
        V.render(PID + "_new", {"d": "N", "el": "물", "kick": "통장 쪼개기", "hook": ["아끼는데도", "돈이 안 모이는 이유"], "sub": "봉투 실험과 사주 정재",
                                "items": ["통장 4개", "1.7배", "정재"]}, os.path.join(HERE, "img", a4), PAL)
    made.append(a4)
    nm = {"S": f"naver_z{KEY}_t1.jpg", "C": f"naver_z{KEY}_t2.jpg", "K": f"naver_z{KEY}_k1.jpg"}
    if not _have(nm["S"]):
        DGC.compare(nm["S"], c, "같은 돈, 봉투만 나눴을 때", ("봉투 하나", "봉투 둘"),
                    [("누가", "건설 현장 146가구", "건설 현장 146가구"), ("기간", "14주", "14주"),
                     ("모은 돈 평균", "241루피", "414루피"), ("급할 때", "봉투째 다 뜯어요", "하나는 남아요")],
                    "소먼·치마 2011 실험 · 나누기만 해도 1.7배", hi=1)
    if not _have(nm["C"]):
        DGC.compare(nm["C"], c, "모으는 사주, 새는 사주", ("모으는 사람", "새는 사람"),
                    [("예시", "1997.7.19 오전 8시", "1998.2.26 밤 8시"), ("일간", "임 일간", "갑 일간"),
                     ("눈에 띄는 글자", "정재 정화가 두 자리", "같은 갑목이 두 자리"), ("돈이 가는 곳", "정해 둔 자리", "모임·한턱·경조사"),
                     ("더할 통장", "모으는 통장 하나", "사람 통장 하나 더")],
                    "만세력 계산값 · 정재는 꼬박꼬박 쌓이는 돈, 비견·겁재는 나와 같은 글자", hi=0)
    if not _have(nm["K"]):
        DGB.checklist(nm["K"], c, "월급날, 쓰기 전에 할 세 가지", [("다음 날 자동이체 걸기", "고정비·모으는 통장으로 먼저"),
                                                       ("체크카드는 생활비 통장에만", "월급 통장엔 카드 안 붙이기"),
                                                       ("모으는 통장 이름 바꾸기", "'내년 이사 보증금'처럼 이유로")], note="쓰기 전에 먼저 나눠 두는 거예요")
    import fullbleed as FBL
    plan_p = os.path.join(HERE, "fullbleed_plan.json"); plan = json.load(open(plan_p, encoding="utf-8")) if os.path.exists(plan_p) else {}
    rows = []
    for pos, k in enumerate("SCK", 1):
        f = nm[k][:-4] + "f.jpg"
        if not _have(f):
            r, why = FBL.convert(nm[k], [os.path.join(HERE, "img"), os.path.join(HERE, "img", "m1280")])
            if not r: print("fullbleed 건너뜀", nm[k], why); made.append(nm[k]); continue
        rows.append({"pos": pos, "old": nm[k], "new": f}); made.append(nm[k]); nm[k] = f
        reg_ = json.load(open(DG.REG, encoding="utf-8")); reg_[f] = reg_[rows[-1]["old"]]; json.dump(dict(sorted(reg_.items())), open(DG.REG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    plan[PID] = rows; json.dump(plan, open(plan_p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    made += [v for v in nm.values() if v not in made]
    alt = {"S": "봉투 실험 비교 표. 같은 돈을 봉투 하나에 넣은 집은 14주에 241루피, 둘로 나눈 집은 414루피를 모았어요",
           "C": "모으는 사주와 새는 사주 비교 표. 1997년 7월 19일생은 정재가 두 자리, 1998년 2월 26일생은 같은 갑목이 두 자리예요",
           "K": "월급날 쓰기 전에 할 세 가지 칸. 자동이체 걸기, 체크카드는 생활비 통장에만, 모으는 통장 이름 바꾸기예요"}
    body = P(*head)   # 목차 줄은 넣지 않는다(n106~n108 과 같게)
    for i, (q, s) in enumerate(zip(toc_q, secs)):
        for k in "SCK": s = s.replace(f"[[{k}]]", IMG(nm[k], alt[k]))
        body += H(f"{i + 1}. {q}") + s
    body += tail + CTA
    import copy_rules as CR
    for w in ("재미로", "상담", "—", "안녕하세요, 자오선의 정월이에요", "결론부터", "핵심부터", "생년월일만 넣으면 1초", "한 줄 요약", "이 글의 순서", "수비학",
              "공통점", "몇 개나", "겹칠까", "세 풀이", "무토", "기토", "황소자리", "처녀자리", "염소자리", "흙의 별자리", "손실회피",
              "총정리", "기운", "흐름", "편이에요", "상대 쪽", "📚", "해 볼 것", "가상", "예시 장면", "반드시", "무조건") + tuple(CR.금지어):
        assert w not in re.sub(r"<[^>]+>", " ", body), w
    for f in made:   # 사이트 사본(K-069)
        dst = os.path.join(SITE, "public", "naver", "img", f); os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy(os.path.join(HERE, "img", f), dst)
    return body, a4, made

TITLE = "통장 쪼개기, 아껴도 돈이 안 모이는 이유와 봉투 실험 1.7배"
TAGS = ["통장쪼개기", "돈모으는법", "돈관리", "월급관리", "돈이모이는사람", "비상금통장", "자동이체", "정재", "재성", "자오선"]
REL = {"id": "n43", "title": "소비심리 뜻, 돈 쓰고 후회하는 3가지 모양 사주와 별자리로",
       "phrase": "돈 쓰고 나서 후회하는 소비심리가 궁금하다면, 소비심리 뜻, 돈 쓰고 후회하는 3가지 모양 사주와 별자리로",
       "url": "https://blog.naver.com/zaoseon/224482710487"}
KW_VOL = (json.load(open(os.path.join(SITE, "data", "keywords", "kw_volume.json"), encoding="utf-8"))["posts"].get(PID) or {}).get("씨앗") or {}
INTENT = {"keywords": ["통장쪼개기", "돈모으는법", "돈관리", "월급관리"],
          "keyword_src": "kw_volume 기존 측정 통장쪼개기 660·돈관리 240(plan_블프) + n109 씨앗 요청(11/24)",
          "intent": "방법을 알고 싶다", "intent_note": "아껴도 돈이 안 모이는 까닭, 통장을 나누면 정말 더 모이는지, 몇 개로 나누는지, 월급날 먼저 할 일",
          "first3": "월급 들어온 지 열흘, 통장 앱 열기가 무서워요. 통장 쪼개기는 월급을 쓸 돈, 나갈 돈, 모을 돈으로 통장부터 나눠 담는 방법이에요.",
          "answer_keys": ["한 통장이면 다 '써도 되는 돈'으로 보임", "봉투 둘로 나누면 241 → 414루피(146가구 14주)", "월급·고정비·생활비·모으는 통장 넷", "정재는 꼬박꼬박, 비견·겁재 많으면 사람 통장"],
          "community_q": [], "order": toc_q, "images": ["봉투 하나 대 둘 실험(compare)", "모으는·새는 사주 비교(compare)", "월급날 세 가지(checklist)"],
          "related": "n43", "cta": PID, "experience": [], "applied": True}

if __name__ == "__main__":
    body, a4, made = build()
    reg = json.load(open(MP.REG, encoding="utf-8"))
    assert PID not in reg or not reg[PID].get("done"), "이미 예약 끝난 글"
    reg[PID] = dict(dt="2027-02-15T08:00:00", dt_tbd="CT가 정함(재발행 일정 'n18 다시 쓰기' 자리, 진행표 11/18). 이 날짜는 자리값", title=TITLE, tags=TAGS, body=body,
                    cover=a4, related=REL, thumbs=None, cid=None, clips=None, category="마음 읽기", done=False, kw_vol=KW_VOL,
                    k131="n109 11/24(K-151 새 글, n18 다시 쓰기)", source="build_naver_109.py (n18 → n109 새 글)")
    json.dump(reg, open(MP.REG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    ic = json.load(open(os.path.join(HERE, "intent_cards.json"), encoding="utf-8")); ic["cards"][PID] = INTENT
    json.dump(ic, open(os.path.join(HERE, "intent_cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    v = reg[PID]
    MP.write_page(PID, D.datetime.fromisoformat(v["dt"]), v["title"], v["tags"], v["body"], None, v["cover"], v["related"], v["category"])
    MP.write_index()
    import k151_check as K
    print(PID, len(TITLE), "자 제목 · 본문 글자", len(re.sub(r"<[^>]+>|&nbsp;", "", body)), "· 사진", made, "· K 검사", K.check(PID, v))
