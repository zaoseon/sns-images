"""네이버 n98: 눈물이 많은 사람 새 글 (CT 11/4 19:40 재발행 일정 '새 글로 다시 쓰기' n16 → n98, 진행표 docs/네이버_누락글_진행표_2026-11-18.md 다섯째 줄).
- 왜: 노출 안 되는 옛 글 n16(눈물이 많은 사람의 공통점, 사주·별자리·숫자로 보는 감정이입이 큰 사람)을 새 글로. n16은 건드리지 않는다(K-147·K-178).
- 검색어: n98 묶음(눈물이많은사람·눈물많은성격·감정이입·공감능력·잘우는사람) 11/19 ① 요청 — 결과가 오면 KW_VOL 이 채워진다.
- 다르게 쓴 것(K-151): n16의 인사·한 줄 요약·癸/乙 일간·게자리/물고기자리·수비학 2·6·'몇 개나 겹칠까'·아리스토텔레스 카타르시스·여섯 운명학·표현 억제(Gross & John 2003)·물 한 잔과 산책 대신
  감각 처리 민감성(Aron & Aron 1997, 7개 연구·27문항 척도), 울고 나면 편해지는지(Gračanin·Bylsma·Vingerhoets 2014 — 35개국 회상 조사에서는 대부분 나아졌다고 기억, 날마다 적은 기록에서는 약 30%),
  사주 여덟 글자 속 물 글자(壬·癸·亥·子) 개수, 예시 1993년 11월 24일 오전 10시생(癸酉·癸亥·己酉·己巳, 물 3개, engine assert), 2026년 12월 子월(대설 12/7 11:52)·2027 丁未.
  그림 유형 exp·counter·checklist. 연결글 → n87(노출 '예'). n93(표현 억제·Butler 2003)과도 심리 출처가 겹치지 않게 했다.
- 출처 2개(K-162, 11/19 원문 확인): Aron & Aron (1997) JPSP 73(2) 345–368, DOI 10.1037/0022-3514.73.2.345 (PubMed 9248053 초록: 7개 연구, 27문항 HSP 척도, 내향성·정서성과 일부만 겹침) ·
  Gračanin, Bylsma & Vingerhoets (2014) Frontiers in Psychology 5:502, DOI 10.3389/fpsyg.2014.00502 (PMC4035568 본문: Bylsma 외 2008 35개국 대부분 나아졌다고 회상 · Bylsma 외 2011 일기 연구 울음의 약 30%만 기분 나아짐).
  'HSP 15~20%' 같은 숫자는 원문 초록에서 확인 못 해서 쓰지 않았다.
- 날짜: CT가 정한다. pages.json dt 는 자리값, dt_tbd 로 표시.
사용: SITE=<zaoseon-site> python3 naver/build_naver_98.py"""
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
       '<tr><td style="padding:12px 10px;text-align:center;border:1px solid #d0d0d0"><b>내 여덟 글자에 물 글자가 몇 개인지 궁금하다면</b></td></tr>'
       '<tr><td style="padding:12px 10px;text-align:center;border:1px solid #d0d0d0"><span style="color:#9a9a9a">[ 1993 . 11 . 24 ]</span></td></tr>'
       '<tr><td style="padding:12px 10px;text-align:center;border:1px solid #d0d0d0"><b><a href="https://zaoseon.com/?utm_source=naver&amp;utm_medium=mid#free">내 태어난 날 글자 보기 →</a></b></td></tr>'
       '</tbody></table>' + BL)
CTA = ('<p><a href="https://zaoseon.com/?utm_source=naver&utm_medium=cta#free"><img src="' + RAW +
       'naver_cta5_1%EC%B4%88%EB%AC%B4%EB%A3%8C%ED%92%80%EC%9D%B4.jpg" alt="자오선 무료 1초 풀이 안내 배너"></a></p>')
PID, KEY, PAL = "n98", "98", "k_white_s"   # 눈물 = 물 판 묶음(EL_SET 물). n97 m_young_s · n96 y_pink_s · n95 y_olive_s · n94 p_purple_s 와 다른 판

# ───────── 계산값과 검산
import datetime as D
sys.path.insert(0, os.path.join(SITE, "engine"))
import engine as E
WATER = set("壬癸亥子")
X = D.datetime(1993, 11, 24, 10, 0)
PX = E.compute_saju(X)["팔자"]
assert PX == {"년주": "癸酉", "월주": "癸亥", "일주": "己酉", "시주": "己巳"}, PX
assert E.compute_saju(D.datetime(1993, 11, 24, 10, 50))["팔자"] == PX           # 같은 巳시 안
NW = sum(ch in WATER for ch in "".join(PX.values())); assert NW == 3, NW
T26 = dict((n, t) for n, _, t in E.get_solar_terms_kst(2026))
assert (T26["대설"].month, T26["대설"].day, T26["대설"].hour, T26["대설"].minute) == (12, 7, 11, 52)
assert E.compute_saju(D.datetime(2026, 12, 7, 14, 0))["팔자"]["월주"] == "庚子"
assert E.compute_saju(D.datetime(2027, 3, 1, 12))["팔자"]["년주"] == "丁未"
assert E.ten_god("己", "丁") == "편인", E.ten_god("己", "丁")
print("예시 팔자·물 글자 3개·12월 子월·2027 丁未·己에게 丁=편인 확인")

# ───────── 본문 (n16 문장을 옮기지 않았다)
head = ["<b>눈물이 많은 사람은 장면과 남의 마음이 크게 들어와 감정이 먼저 차오르는 사람이에요. 약해서라기보다 들어온 것을 깊게 받아들이는 기질에 가까워요.</b>",
        "그런데 울고 나면 정말 편해질까요? 35개국 사람들은 대부분 울고 나서 나아졌다고 기억했지만, 울 때마다 바로 적게 한 기록에서는 열 번 중 세 번꼴이었어요.",
        "<b>사주에서는 여덟 글자 가운데 물 글자(壬·癸·亥·子)가 3개 이상이면 마음에 물이 많은 사람으로 봐요.</b>",
        "이 글은 눈물이 많은 이유, 울음이 마음을 달래는지, 내 사주의 물 글자 세는 법, 울고 난 뒤에 해 볼 것까지 다뤄요."]
toc_q = ["눈물이 많은 사람은 왜 먼저 울까요?", "울고 나면 정말 편해질까요?", "사주에서는 눈물이 많은 사람을 어떻게 볼까요?",
         "1993년 11월 24일 오전 10시생은 어떻게 읽을까요?", "눈물이 많을 때 무엇을 해 볼까요?", "자주 묻는 질문"]
sec1 = P("🧠 <b>심리학에서는 들어온 자극을 남보다 깊게 처리하는 기질을 '감각 처리 민감성'이라고 불러요.</b>",
         "미국 심리학자 일레인 아론과 아서 아론은 1997년 7개 연구를 묶어 이 기질을 27문항 척도로 쟀어요.",
         "결과는 이 기질이 내향성이나 감정 기복과 일부만 겹친다는 것이었어요. 조용한 성격이라서, 감정이 들쭉날쭉해서 예민한 게 아니라 따로 있는 기질이라는 뜻이에요.") + \
       P("드라마 한 장면, 친구의 짧은 한숨에도 눈물이 먼저 나는 사람은 그 장면을 더 오래, 더 깊게 곱씹는 쪽일 수 있어요. 그래서 남보다 빨리 차오르고, 그만큼 빨리 지치기도 해요.",
         '📚 <b>출처 1</b>: <a href="https://doi.org/10.1037/0022-3514.73.2.345">Aron &amp; Aron (1997), Sensory-processing sensitivity and its relation to introversion and emotionality, Journal of Personality and Social Psychology 73(2)</a>')
sec2 = P("<b>울고 나면 편해지는 때도 있고, 아닌 때도 있어요. 연구 방법에 따라 답이 달랐어요.</b>",
         "네덜란드 틸뷔르흐대 연구진이 그동안의 울음 연구를 모아 정리했어요(2014). 35개국 사람들에게 지난 울음을 떠올려 물었을 때는 대부분 울고 나서 나아졌다고 답했어요.",
         "그런데 울 때마다 바로 기록하게 한 일기 연구에서는, 울음 뒤에 기분이 나아진 건 약 30%였어요.") + "[[B]]" + \
       P("기억 속 울음은 개운한 장면으로 남기 쉽지만, 그날그날의 울음은 그렇지 않을 때도 많다는 뜻이에요. 그러니 울고 나서도 마음이 그대로라면 내가 잘못 운 게 아니에요. 울음 다음에 무엇을 하느냐를 따로 챙기면 돼요.",
         '📚 <b>출처 2</b>: <a href="https://doi.org/10.3389/fpsyg.2014.00502">Gračanin, Bylsma &amp; Vingerhoets (2014), Is crying a self-soothing behavior?, Frontiers in Psychology 5</a>')
sec3 = P("<b>사주에서는 여덟 글자 가운데 물 글자가 몇 개인지로 마음의 물을 봐요.</b>",
         "물 글자는 넷이에요. 위 글자 壬(큰 물)·癸(빗물), 아래 글자 亥(돼지)·子(쥐)예요. 물은 스며들고 고이는 성질이라, 감정과 생각이 깊이 흐르는 기운으로 봐요.") + "[[K]]" + \
       P("🔹 <b>3개 이상</b>: 마음에 물이 많은 사주로 봐요. 남의 감정이 쉽게 스며들고, 한 번 고인 마음이 오래 남아요.",
         "🔹 <b>1~2개</b>: 물이 알맞게 흐르는 쪽이에요. 평소엔 덤덤하다가 마음이 쌓인 날 한꺼번에 나오기도 해요.",
         "🔹 <b>0개</b>: 물이 드러나지 않는 사주예요. 눈물이 없다기보다 감정을 말이나 행동으로 먼저 풀어요.",
         "일간(태어난 날 위 글자)이 무엇이든 물 글자는 똑같이 세요. 다만 이건 타고난 기질을 보는 것이고, 눈물의 양을 정하지는 않아요.") + MID
sec4 = P("🔎 <b>1993년 11월 24일 오전 10시에 태어난 사람을 예로 들어 볼게요.</b>",
         "여덟 글자는 癸酉·癸亥·己酉·己巳예요. 날의 주인(일간)은 己, 씨앗을 품는 밭 흙이에요. 여기에 癸가 둘, 亥가 하나라 물 글자가 3개예요.",
         "밭에 물이 넉넉하게 스민 모양이라, 남의 마음이 쉽게 스며들고 그 마음을 오래 품는 사람으로 봐요.") + \
       P("올해 12월은 물이 하나 더 들어와요. 12월 7일 오전 11시 52분 대설부터 쥐(子)의 달이 시작되는데, 子도 물 글자예요. 이 사람에게 12월은 작은 장면에도 눈물이 차오르기 쉬운 달로 봐요.",
         "2027년 정미년은 조금 달라요. 丁은 밭 흙을 데워 주는 불이고(己에게 편인), 未는 물을 막아 주는 둑 같은 흙이에요. 마음의 물이 넘치기보다 데워지고 고이는 해라, 쌓인 감정을 말로 꺼내 보기 좋은 해로 볼 수 있어요.")
sec5 = P("<b>눈물을 줄이려 애쓰기보다, 울고 난 뒤를 챙겨 보세요.</b>",
         "눈물이 많은 건 고칠 일이 아니에요. 다만 많이 받아들이는 만큼 쉬는 칸도 커야 해요.") + \
       P("🌱 <b>마음 코치 정월의 질문</b>", "최근에 눈물이 난 장면은<br>무엇이었나요?",
         "🔸 그 장면에서 내 마음을 건드린 건<br>누구의 어떤 말이었나요?") + "[[C]]" + \
       P("✔️ <b>울고 난 뒤 해 볼 것</b>",
         "1. 운 날은 달력에 점 하나와 장면을 두 단어로 적어 보세요. 예: '퇴근길, 엄마 전화'.",
         "2. 울고 30분쯤 지나 마음이 0에서 10 중 몇인지 적어 보세요. 나아진 날과 아닌 날을 모아 보면, 나를 달래 주는 게 무엇인지 보여요.",
         "3. 다 울고 나서 이야기를 들어 줄 사람 한 명을 미리 정해 두세요. 꼭 해결해 주지 않아도 들어만 주는 사람이면 돼요.")
sec6 = P("<b>Q. 눈물이 많은 건 고쳐야 하나요?</b>",
         "A. 아니에요. 들어온 것을 깊게 받아들이는 기질이라 고칠 대상이 아니에요. 다만 지치기 쉬우니 쉬는 시간을 일정에 먼저 넣어 두면 좋아요.") + \
       P("<b>Q. 일하다가 눈물이 날 것 같으면 어떻게 하나요?</b>",
         "A. 자리에서 잠깐 일어나 물을 마시거나 손을 씻으면 장면에서 한 발 떨어질 수 있어요. 눈물이 났다면 '잠깐만요' 한마디면 충분해요. 설명은 마음이 가라앉은 뒤에 해도 돼요.") + \
       P("<b>Q. 물 글자가 하나도 없는데 눈물이 많아요.</b>",
         "A. 그럴 수 있어요. 물 글자는 기질의 한 면일 뿐이고, 지금 겪는 일과 몸 상태가 눈물에 더 크게 작용해요. 사주는 나를 돌아보는 데 쓰고, 지금의 나를 먼저 믿어 주세요.")
tail = P("여러분의 여덟 글자에는 물 글자가 몇 개 있나요?", "무료 풀이에서 확인하고 숫자 하나만 댓글에 적어 주세요.") + \
       '<p><b>👇 내 사주 여덟 글자를 처음부터 읽어 보고 싶다면, 사주 보는 법, 만세력 여덟 글자를 예시 한 명으로 읽는 4단계</b></p>'
secs = [sec1, sec2, sec3, sec4, sec5, sec6]

def _have(n): return os.path.exists(os.path.join(HERE, "img", n))
def build():
    for d_ in ("wide", "m1280", "master"): os.makedirs(os.path.join(HERE, "img", d_), exist_ok=True)
    c = V.Ctx(PAL); made = []
    a4 = f"wide/naver_z{KEY}_a5.jpg"   # 표지 항목은 한글만(한자는 글꼴에 없어 네모, 11/18 n96 a4)
    if not _have(a4):
        V.render(PID + "_new", {"d": "N", "el": "물", "kick": "눈물이 많은 사람", "hook": ["울고 나면", "정말 편해질까"], "sub": "35개국 연구와 사주 물 글자로 봐요",
                                "items": ["임", "계", "해·자"]}, os.path.join(HERE, "img", a4), PAL)
    made.append(a4)
    nm = {"B": f"naver_z{KEY}_e5.jpg", "K": f"naver_z{KEY}_c3.jpg", "C": f"naver_z{KEY}_h3.jpg"}
    if not _have(nm["B"]):
        DGC.exp(nm["B"], c, "울고 나면 편해질까", "틸뷔르흐대 연구진 · 2014",
                [("돌아보며", "35개국 사람들에게 지난 울음을 떠올려 물었어요"), ("그날그날", "울 때마다 바로 기분을 적게 했어요")],
                "떠올릴 때는 대부분 나아졌다고 했지만, 바로 적은 기록에서는 약 30%만 나아졌어요",
                "Gračanin·Bylsma·Vingerhoets (2014), Frontiers in Psychology", tag="연구 정리")
    if not _have(nm["K"]):
        DGB.counter(nm["K"], c, "여덟 글자 속 물 글자 세기", [("壬", "큰 물"), ("癸", "빗물"), ("亥", "돼지"), ("子", "쥐")],
                    "3개 이상이면 마음에 물이 많은 사주로 봐요", "일간이 무엇이든 넷을 똑같이 세요")
    if not _have(nm["C"]):
        DGB.checklist(nm["C"], c, "울고 난 뒤 세 칸", [("달력에 점 하나", "장면을 두 단어로"), ("30분 뒤 마음 점수", "0에서 10 중 몇"),
                                                  ("들어 줄 사람 한 명", "해결 말고 들어만 주는 사람")])
    import fullbleed as FBL
    plan_p = os.path.join(HERE, "fullbleed_plan.json"); plan = json.load(open(plan_p, encoding="utf-8")) if os.path.exists(plan_p) else {}
    rows = []
    for pos, k in enumerate("BKC", 1):
        f = nm[k][:-4] + "f.jpg"
        if not _have(f):
            r, why = FBL.convert(nm[k], [os.path.join(HERE, "img"), os.path.join(HERE, "img", "m1280")])
            if not r: print("fullbleed 건너뜀", nm[k], why); made.append(nm[k]); continue
        rows.append({"pos": pos, "old": nm[k], "new": f}); made.append(nm[k]); nm[k] = f
        reg_ = json.load(open(DG.REG, encoding="utf-8")); reg_[f] = reg_[rows[-1]["old"]]; json.dump(dict(sorted(reg_.items())), open(DG.REG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    plan[PID] = rows; json.dump(plan, open(plan_p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    made += [v for v in nm.values() if v not in made]
    alt = {"B": "울음 연구 정리 그림. 35개국 사람들은 떠올릴 때 대부분 울고 나서 나아졌다고 했지만, 울 때마다 바로 적은 기록에서는 약 30%만 나아졌어요",
           "K": "여덟 글자 속 물 글자 세기 그림. 壬 큰 물, 癸 빗물, 亥 돼지, 子 쥐, 3개 이상이면 마음에 물이 많은 사주로 봐요",
           "C": "울고 난 뒤 세 칸 체크 그림. 달력에 점 하나, 30분 뒤 마음 점수, 들어 줄 사람 한 명"}
    body = P(*head) + P("<b>📌 눈물이 많은 나를 읽는 순서</b>", *[f"{i + 1}. {q}" for i, q in enumerate(toc_q)])
    for i, (q, s) in enumerate(zip(toc_q, secs)):
        for k in "BKC": s = s.replace(f"[[{k}]]", IMG(nm[k], alt[k]))
        body += H(f"{i + 1}. {q}") + s
    body += tail + CTA
    import copy_rules as CR
    for w in ("재미로", "상담", "—", "안녕하세요, 자오선의 정월이에요", "결론부터 말씀드릴게요", "한 줄로 먼저", "생년월일만 넣으면 1초", "한 줄 요약", "이 글의 순서", "수비학",
              "공통점", "몇 개나 겹칠까", "카타르시스", "아리스토텔레스", "여섯 운명학", "표현 억제", "게자리", "물고기자리", "산책", "총정리", "솜씨", "값을 매", "내게") + tuple(CR.금지어):
        assert w not in re.sub(r"<[^>]+>", " ", body), w
    for f in made:   # 사이트 사본(K-069)
        dst = os.path.join(SITE, "public", "naver", "img", f); os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy(os.path.join(HERE, "img", f), dst)
    return body, a4, made

TITLE = "눈물이 많은 사람, 울고 나면 편해질까요 35개국 연구와 사주"
TAGS = ["눈물이많은사람", "눈물많은성격", "감정이입", "공감능력", "잘우는사람", "예민한사람", "사주물기운", "감정조절", "관계심리", "자오선"]
REL = {"id": "n87", "title": "사주 보는 법, 만세력 여덟 글자를 예시 한 명으로 읽는 4단계",
       "phrase": "내 사주 여덟 글자를 처음부터 읽어 보고 싶다면, 사주 보는 법, 만세력 여덟 글자를 예시 한 명으로 읽는 4단계",
       "url": "https://blog.naver.com/zaoseon/224476055740"}
KW_VOL = (json.load(open(os.path.join(SITE, "data", "keywords", "kw_volume.json"), encoding="utf-8"))["posts"].get("n98") or {}).get("씨앗") or {}
INTENT = {"keywords": ["눈물이많은사람", "눈물많은성격", "감정이입"],
          "keyword_src": "n16 재발행 일정 '새 글로 다시 쓰기'(진행표 11/18 다섯째 줄) · 월 검색량은 kw-volume n98 요청 중(11/19)",
          "intent": "이유를 알고 싶다", "intent_note": "눈물이 왜 많은지, 그게 약한 건지, 울고 나면 정말 편해지는지 바로 알고, 내 사주의 물 글자와 울고 난 뒤 할 일까지",
          "first3": "눈물이 많은 사람은 장면과 남의 마음이 크게 들어와 감정이 먼저 차오르는 사람이에요. 울고 나면 편해진다는 기억과 달리, 바로 적은 기록에서는 열 번 중 세 번꼴이었어요. 사주에서는 물 글자 3개 이상을 마음에 물이 많은 사람으로 봐요.",
          "answer_keys": ["약함이 아니라 깊게 받아들이는 기질", "울음 뒤 나아짐 회상 대부분 vs 기록 약 30%", "물 글자 壬·癸·亥·子 3개 이상"],
          "community_q": [], "order": toc_q, "images": ["울음 연구 정리(exp)", "물 글자 세기(counter)", "울고 난 뒤 세 칸(checklist)"],
          "related": "n87", "cta": PID, "experience": [], "applied": True,
          "differs_from_n16": "제목(공통점 → 울고 나면 편해질까)·도입(정의 + 연구 숫자)·소제목 순서·癸/乙 일간·게자리/물고기자리·수비학 2·6·'몇 개나 겹칠까'·카타르시스·여섯 운명학·표현 억제(Gross & John 2003) 대신 감각 처리 민감성(Aron 1997)·울음 연구 정리(Gračanin 외 2014)·물 글자 개수·예시 1993.11.24 오전 10시(癸酉·癸亥·己酉·己巳, 엔진 assert)·12월 子월·2027 丁未·그림 유형(exp·counter·checklist)·연결글(→ n87)"}

if __name__ == "__main__":
    body, a4, made = build()
    reg = json.load(open(MP.REG, encoding="utf-8"))
    assert PID not in reg or not reg[PID].get("done"), "이미 예약 끝난 글"
    reg[PID] = dict(dt="2027-02-07T18:00:00", dt_tbd="CT가 정함(재발행 일정 'n16 다시 쓰기' 자리, 진행표 11/18). 이 날짜는 자리값", title=TITLE, tags=TAGS, body=body,
                    cover=a4, related=REL, thumbs=None, cid=None, clips=None, category="마음 읽기", done=False, kw_vol=KW_VOL,
                    k131="n98 11/19(K-151 새 글)", source="build_naver_98.py (n16 주제 새 글, n16 그대로)")
    json.dump(reg, open(MP.REG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    ic = json.load(open(os.path.join(HERE, "intent_cards.json"), encoding="utf-8")); ic["cards"][PID] = INTENT
    json.dump(ic, open(os.path.join(HERE, "intent_cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    v = reg[PID]
    MP.write_page(PID, D.datetime.fromisoformat(v["dt"]), v["title"], v["tags"], v["body"], None, v["cover"], v["related"], v["category"])
    MP.write_index()
    import k151_check as K
    print(PID, len(TITLE), "자 제목 · 본문 글자", len(re.sub(r"<[^>]+>|&nbsp;", "", body)), "· 사진", made, "· K 검사", K.check(PID, v))
