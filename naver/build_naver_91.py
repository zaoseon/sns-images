"""네이버 n91: 첫눈에 반하는 이유 새 글 (CT 11/4 19:40 → ① 최우선, 대표 11/4 19:28 재발행 일정 '새 글로 다시 쓰기' n22 → n91, 11/21 08:00 자리).
- 왜: 노출 안 되는 옛 글 n22(첫눈에 반하는 사람의 공통점)를 새 글로. n22는 건드리지 않는다(K-147·K-178).
- 검색어: data/keywords/kw_volume.json posts.n91 — 11/7 첫 씨앗(첫눈에반한사람 55·도화살 19,190)에서 도화살은 n79(도화살 뜻, 11/10)·n84(도화 피는 달)가
  이미 맡아 겹침을 피하고, 11/7 19:50 넓혀 다시 받음 → 첫인상 1,580 · 첫눈에반하다 470 · 금사빠테스트 15.
- 다르게 쓴 것(K-151): n22의 한 줄 요약·세 풀이(병화·양/사자자리·수비학 3/5)·몇 개 겹칠까·로미오·여섯 운명학·확증 편향 대신,
  사주 여덟 글자에서 끌림이 빠른 신호 둘(도화 글자·식상 2개 이상)과 느린 신호 둘(인성 2개 이상·관성 2개 이상)을 세고,
  예시 장면 = 1996년 4월 21일 같은 날 태어난 두 사람(오전 8시 丙辰시 · 저녁 6시 辛酉시)이 시 기둥 하나로 갈리는 것.
  심리 = Zsok 외 2017(첫눈에 반함은 강한 첫 끌림, 겉모습 끌림이 가장 크게 가름). 제목에 사주·별자리·숫자 나열 안 함(CT 11/4 21:05).
  그림 유형 twopanel·compare·exp. 연결글 → n77(발행·노출 '예'). 소제목 틀(한 줄 요약·이 글의 순서·생년월일만 넣으면 1초·수비학으로 겹쳐 보면) 안 씀.
- 계산: 팔자는 zaoseon-site engine/engine.py, 신호 판정은 engine/dapjang_love.signals(정월의 답장 5번 '금사빠일까 자만추일까'와 같은 기준), 모두 assert.
- 출처 2개(K-162, 11/7 확인): Zsok, Haucke, De Wit & Barelds (2017) Personal Relationships 24(4) 869–885, DOI 10.1111/pere.12218
  (흐로닝언 대학 서지·초록: 열정·친밀·헌신이 높지 않았고 겉모습 끌림이 크게 가름) · 영국심리학회 Research Digest 요약(396명, 32명이 49번, 서로 동시에 반한 경우 없음).
- 날짜: CT가 정한다. pages.json dt 는 자리값, dt_tbd 로 표시.
사용: SITE=<zaoseon-site> python3 naver/build_naver_91.py"""
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
       '<tr><td style="padding:12px 10px;text-align:center;border:1px solid #d0d0d0"><b>내 끌림 속도가 궁금하다면</b></td></tr>'
       '<tr><td style="padding:12px 10px;text-align:center;border:1px solid #d0d0d0"><span style="color:#9a9a9a">[ 1996 . 04 . 21 ]</span></td></tr>'
       '<tr><td style="padding:12px 10px;text-align:center;border:1px solid #d0d0d0"><b><a href="https://zaoseon.com/?utm_source=naver&amp;utm_medium=mid#free">내 태어난 날 글자 보기 →</a></b></td></tr>'
       '</tbody></table>' + BL)
CTA = ('<p><a href="https://zaoseon.com/?utm_source=naver&utm_medium=cta#free"><img src="' + RAW +
       'naver_cta5_1%EC%B4%88%EB%AC%B4%EB%A3%8C%ED%92%80%EC%9D%B4.jpg" alt="자오선 무료 1초 풀이 안내 배너"></a></p>')
PID, KEY, PAL = "n91", "91", "p_red_s"   # 불 판 묶음(끌림), n90 g_ivory_s·n89 k_white_s·n88 y_black_s 와 다른 판

# ───────── 계산값과 검산
import datetime as D
sys.path.insert(0, os.path.join(SITE, "engine"))
import engine as E, dapjang as DJ, dapjang_love as LV, ny_facts as F
A, B = D.datetime(1996, 4, 21, 8, 0), D.datetime(1996, 4, 21, 18, 0)
PA, PB = E.compute_saju(A)["팔자"], E.compute_saju(B)["팔자"]
assert PA == {"년주": "丙子", "월주": "壬辰", "일주": "戊子", "시주": "丙辰"}, PA
assert PB == {"년주": "丙子", "월주": "壬辰", "일주": "戊子", "시주": "辛酉"}, PB
for h, m in ((7, 40), (8, 20)): assert E.compute_saju(D.datetime(1996, 4, 21, h, m))["팔자"]["시주"] == "丙辰"
for h, m in ((17, 40), (18, 20)): assert E.compute_saju(D.datetime(1996, 4, 21, h, m))["팔자"]["시주"] == "辛酉"
assert LV.DOHWA["子"] == "酉" and LV.DOHWA["午"] == "卯" and LV.DOHWA["卯"] == "子" and LV.DOHWA["酉"] == "午"
assert set(LV.DOHWA.values()) == set("子午卯酉")
def cnt(Pz, grp):
    dm = Pz["일주"][0]
    return sum((DJ.GROUP.get(F.tg(dm, v[0])) == grp if k != "일주" else 0) + (DJ.GROUP.get(F.tg(dm, F.ZMAIN[v[1]])) == grp) for k, v in Pz.items())
assert (cnt(PA, "식상"), cnt(PA, "인성"), cnt(PA, "관성")) == (0, 2, 0)
assert (cnt(PB, "식상"), cnt(PB, "인성"), cnt(PB, "관성")) == (2, 1, 0)
assert F.tg("戊", "丙") == "편인" and F.tg("戊", "辛") == "상관" and F.tg("戊", F.ZMAIN["酉"]) == "상관"
def saju_sig(b):
    sig, _ = LV.signals(DJ.facts(b, "가", "여")); return sorted(k for s, w, sy, k, src, _t in sig if sy == "사주명리")
assert saju_sig(A) == ["인성_많음"] and saju_sig(B) == ["도화", "식상_많음"]
print("두 사람 팔자·도화·식상·인성 개수·신호 판정 다시 확인")

# ───────── 본문 (n22 문장을 옮기지 않았다)
head = ["<b>첫눈에 반하는 이유는 타고난 끌림의 속도와 그날 눈에 들어온 첫인상이 한꺼번에 겹치기 때문이에요.</b>",
        "사주 여덟 글자에서는 끌림의 속도를 네 가지 신호로 봐요. 빠른 쪽은 사람을 당기는 도화 글자와 마음을 바로 꺼내는 표현의 글자(식상)예요.",
        "<b>느린 쪽은 나를 먼저 지키는 글자(인성)와 선을 지키는 글자(관성)예요. 둘 중 어느 쪽이 많은지가 첫눈에 반하는 사람과 천천히 스며드는 사람을 갈라요.</b>",
        "다만 연구에서는 첫눈에 반한 순간이 사랑보다 강한 첫 끌림에 가까웠어요. 그래서 이 글은 끌림을 알아보는 법과, 그 끌림을 오래 갈 마음으로 확인하는 법까지 같이 다뤄요."]
toc_q = ["첫눈에 반하는 이유, 사주에서는 무엇으로 볼까요?", "같은 날 태어나도 끌림의 속도가 다를 수 있을까요?",
         "빠른 신호 도화와 식상은 무엇이 다를까요?", "천천히 스며드는 사람은 어떤 글자가 많을까요?",
         "첫눈에 반한 마음은 사랑일까요, 강한 첫인상일까요?", "첫눈에 반한 다음 무엇을 해 보면 좋을까요?", "자주 묻는 질문"]
sec1 = P("<b>끌림이 빠른 사람은 마음이 움직이는 순간과 겉으로 꺼내는 순간 사이가 짧아요.</b>",
         "사주에서는 이 간격을 글자로 봐요. 도화(子·午·卯·酉 가운데 내 띠와 일지에 맞는 글자)는 눈길이 머무는 힘, 식상은 느낀 것을 말과 표정으로 바로 꺼내는 힘이에요.",
         "반대로 인성은 들어온 마음을 한 번 품고 생각하는 힘, 관성은 지켜야 할 선을 먼저 떠올리는 힘이에요.") + "[[F]]" + \
       P("빠른 신호가 많으면 첫 만남에서 이미 마음이 기울고, 느린 신호가 많으면 세 번째, 네 번째 만남에서야 마음이 보여요.",
         "어느 쪽이 더 좋다는 뜻은 아니에요. 속도가 다를 뿐이라, 내 속도를 알면 상대의 속도도 덜 서운하게 기다릴 수 있어요.")
sec2 = P("🔎 <b>1996년 4월 21일에 태어난 두 사람을 떠올려 볼게요.</b>",
         "한 사람은 오전 8시, 한 사람은 저녁 6시에 태어났어요. 해·달·날 기둥은 丙子·壬辰·戊子로 똑같고, 시 기둥만 丙辰과 辛酉로 달라요.",
         "날의 주인(일간)은 둘 다 戊, 큰 산 같은 흙이에요.") + "[[S]]" + \
       P("저녁 6시생은 시 기둥에 酉가 들어와요. 쥐(子)띠에 일지도 子라 도화 글자가 酉예요. 게다가 辛과 酉는 戊에게 표현의 글자라 식상이 2개가 돼요.",
         "오전 8시생은 시 기둥이 丙辰이라 도화가 없고, 해와 시의 丙 두 개가 戊를 품어 주는 인성이 돼요.",
         "같은 날 태어나도 저녁 6시생은 소개팅 첫 만남에 마음이 기울기 쉽고, 오전 8시생은 '한 번 더 보고 싶다'는 마음이 세 번째 만남쯤에야 오기 쉬워요. 시 기둥 하나가 첫인상을 받아들이는 속도를 바꾼 거예요.") + MID
sec3 = P("<b>도화는 끌리게 하는 힘, 식상은 끌린 마음을 꺼내는 힘이에요.</b>",
         "도화가 있으면 나도 모르게 눈에 띄고, 나 역시 첫인상에 쉽게 마음이 가요. 끌림이 들어오는 쪽이에요.",
         "식상이 2개 이상이면 좋으면 좋다고 바로 말하고, 연락도 먼저 하는 편이에요. 끌림이 나가는 쪽이에요.") + \
       P("둘이 함께 있으면 첫눈에 반하고 그 마음을 그날 바로 보여 주기 쉬워요. 위의 저녁 6시생이 그래요.",
         "도화만 있으면 마음은 기울어도 말은 아끼고, 식상만 있으면 끌림보다 대화가 먼저 불붙어요. 그래서 하나만 있을 때는 '빠른 편' 정도로 봐요.",
         "도화가 무엇인지, 2027년에 언제 들어오는지는 따로 길게 다뤄서 이 글에서는 끌림의 속도만 봐요.")
sec4 = P("<b>천천히 스며드는 사람은 인성이나 관성이 2개 이상인 경우가 많아요.</b>",
         "인성이 많으면 마음이 와도 바로 꺼내지 않고 한동안 품어 둬요. '이 사람이 정말 괜찮은 사람일까'를 먼저 생각해요.",
         "관성이 많으면 좋아도 지켜야 할 선과 순서를 먼저 떠올려요. 연락 간격, 만나는 요일처럼 정해 둔 틀 안에서 마음이 자라요.") + \
       P("이런 사람은 첫눈에 반하는 일은 드물어도, 한 번 마음이 정해지면 잘 흔들리지 않아요.",
         "빠른 사람과 만나면 서로 답답하거나 부담스러울 수 있어요. 이때 '나는 좀 천천히 마음이 생기는 편이야'라고 한 줄 먼저 말해 두면, 상대가 내 느린 답장을 거절로 읽지 않아요.")
sec5 = P("🧠 <b>첫눈에 반하는 마음은 깊은 사랑이라기보다, 강한 첫 끌림에 우리가 붙인 이름에 가까워요.</b>",
         "네덜란드 흐로닝언 대학의 졸크 연구진은 2017년, 온라인 조사와 실험실, 세 번의 만남 행사에서 396명이 처음 본 사람에게 느낀 마음을 바로 그 자리에서 쟀어요.",
         "32명이 모두 49번 '첫눈에 반했다'고 답했어요. 그 순간의 열정·친밀감·헌신은 높지 않았고, 첫눈에 반했는지를 가장 크게 가른 것은 상대의 겉모습에 끌린 정도였어요.") + "[[B]]" + \
       P("만남 행사에서는 첫눈에 반한 경우가 서로 동시에 일어난 적이 한 번도 없었어요.",
         "그러니 첫눈에 반했다면 그 마음은 진짜예요. 다만 그 마음이 사랑인지는 상대를 알아 가며 나중에 정해져요.",
         '📚 <b>출처 1</b>: <a href="https://doi.org/10.1111/pere.12218">Zsok, Haucke, De Wit &amp; Barelds (2017), What kind of love is love at first sight? An empirical investigation, Personal Relationships 24(4)</a>',
         '📚 <b>출처 2</b>: <a href="https://www.bps.org.uk/research-digest/sorry-romantics-new-findings-suggest-love-first-sight-really-lust-first-sight">영국심리학회 Research Digest, 첫눈에 반함 연구 요약</a>')
sec6 = P("<b>첫눈에 반한 다음에는 끌림과 확인을 나눠서 가요.</b>",
         "빠른 신호가 많은 사람일수록 첫 만남의 설렘이 다음 판단까지 끌고 가기 쉬워요. 끌림은 그대로 두고, 확인할 것을 따로 정해 두면 마음이 덜 다쳐요.") + \
       P("🌱 <b>마음 코치 정월의 질문</b>", "처음 그 사람에게 끌린 것은<br>얼굴이었나요, 말투였나요, 분위기였나요?",
         "🔸 그 사람과 두 번째로 만난다면<br>무엇을 꼭 확인해 보고 싶나요?") + \
       P("✔️ <b>첫눈에 반한 다음 해 볼 것</b>",
         "1. 첫 만남이 끝나면 휴대폰 메모에 '끌린 것 하나, 아직 모르는 것 하나'를 적어 두세요.",
         "2. 두 번째 만남에서는 아직 모르는 것 하나를 '쉬는 날엔 보통 뭐 해요?'처럼 가볍게 물어보세요.",
         "3. 마음이 앞설 때는 답장을 보내기 전에 10분만 두고, 그 사이 내 하루 일정을 먼저 정해 두세요.")
sec7 = P("<b>Q. 도화도 식상도 없으면 첫눈에 반하지 않나요?</b>",
         "A. 아니에요. 사주 글자는 끌림의 속도를 보는 것이지, 반할 수 있는지를 정하지 않아요. 느린 신호가 많은 사람도 마음에 드는 사람 앞에서는 빨라져요.") + \
       P("<b>Q. 금사빠는 오래 못 가나요?</b>",
         "A. 빨리 빠지는 것과 빨리 식는 것은 달라요. 끌림이 빠른 사람도 확인하는 시간을 따로 두면 오래 가요. 위의 '끌린 것 하나, 아직 모르는 것 하나'가 그 시간이에요.") + \
       P("<b>Q. 태어난 시를 모르면 어떻게 봐요?</b>",
         "A. 위 두 사람처럼 시 기둥 하나로 도화와 식상이 갈릴 수 있어요. 시를 모르면 해·달·날 여섯 글자만으로 보고, 시를 알게 되면 다시 세어 보세요.")
tail = P("여러분은 첫눈에 반하는 쪽인가요, 천천히 스며드는 쪽인가요?", "빠른 쪽이면 '첫눈', 느린 쪽이면 '스며듦'이라고 댓글로 남겨 주세요.") + \
       '<p><b>👇 2027년 연애운에서 좋은 짝이 오는 달까지 보고 싶다면, 2027년 연애운, 좋은 짝 만나는 사주 신호와 도화 달</b></p>'
secs = [sec1, sec2, sec3, sec4, sec5, sec6, sec7]

def _have(n): return os.path.exists(os.path.join(HERE, "img", n))
def build():
    for d_ in ("wide", "m1280", "master"): os.makedirs(os.path.join(HERE, "img", d_), exist_ok=True)
    c = V.Ctx(PAL); made = []
    a4 = f"wide/naver_z{KEY}_a4.jpg"
    if not _have(a4):
        V.render(PID + "_new", {"d": "N", "el": "불", "kick": "첫눈에 반하는 이유", "hook": ["끌림이 빠른 사람", "느린 사람"], "sub": "사주 여덟 글자로 보는 속도",
                                "items": ["도화", "식상", "인성·관성"]}, os.path.join(HERE, "img", a4), PAL)
    made.append(a4)
    nm = {"F": f"naver_z{KEY}_w8.jpg", "S": f"naver_z{KEY}_c7.jpg", "B": f"naver_z{KEY}_e9.jpg"}
    if not _have(nm["F"]):
        DGB.twopanel(nm["F"], c, "끌림의 속도를 가르는 신호 넷",
                     ("빠른 신호", "도화 글자, 표현의 글자 식상 2개 이상", 0.55), ("느린 신호", "품는 글자 인성, 선을 지키는 관성 2개 이상", 0.2),
                     "원이 클수록 첫 만남에 마음이 먼저 움직여요", "빠른 쪽은 확인을 한 번 더, 느린 쪽은 표현을 한 번 먼저")
    if not _have(nm["S"]):
        DGC.compare(nm["S"], c, "1996년 4월 21일, 시만 다른 두 사람", ("오전 8시생", "저녁 6시생"),
                    [("시 기둥", "丙辰", "辛酉"), ("도화", "없음", "酉 있음"), ("식상", "0개", "2개"), ("인성", "2개", "1개"), ("끌림", "천천히 스며들어요", "빨리 기울어요")],
                    "자오선 계산 · 해·달·날 기둥은 丙子·壬辰·戊子로 같아요", hi=1)
    if not _have(nm["B"]):
        DGC.exp(nm["B"], c, "첫눈에 반한 순간을 그 자리에서 쟀더니", "졸크 연구진 · 2017",
                [("누가", "396명, 온라인 조사·실험실·만남 행사 세 번"), ("무엇을", "처음 본 사람에게 느낀 열정·친밀감·헌신과 끌림을 그 자리에서 물었어요"),
                 ("결과", "32명이 모두 49번 첫눈에 반했다고 답했어요")],
                "가장 크게 가른 것은 겉모습 끌림이었어요. 깊은 사랑보다 강한 첫 끌림에 가까웠어요", "Zsok 외 (2017), Personal Relationships")
    import fullbleed as FBL
    plan_p = os.path.join(HERE, "fullbleed_plan.json"); plan = json.load(open(plan_p, encoding="utf-8")) if os.path.exists(plan_p) else {}
    rows = []
    for pos, k in enumerate("FSB", 1):
        f = nm[k][:-4] + "f.jpg"
        if not _have(f):
            r, why = FBL.convert(nm[k], [os.path.join(HERE, "img"), os.path.join(HERE, "img", "m1280")])
            if not r: print("fullbleed 건너뜀", nm[k], why); made.append(nm[k]); continue
        rows.append({"pos": pos, "old": nm[k], "new": f}); made.append(nm[k]); nm[k] = f
        reg_ = json.load(open(DG.REG, encoding="utf-8")); reg_[f] = reg_[rows[-1]["old"]]; json.dump(dict(sorted(reg_.items())), open(DG.REG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    plan[PID] = rows; json.dump(plan, open(plan_p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    made += [v for v in nm.values() if v not in made]
    alt = {"F": "첫눈에 반하는 속도를 가르는 사주 신호 그림. 빠른 신호는 도화 글자와 식상 2개 이상, 느린 신호는 인성과 관성 2개 이상",
           "S": "1996년 4월 21일에 태어난 두 사람 비교 표. 오전 8시생은 시 기둥 丙辰·도화 없음·식상 0개·인성 2개, 저녁 6시생은 시 기둥 辛酉·도화 酉·식상 2개·인성 1개",
           "B": "졸크 연구진 2017년 연구 그림. 396명 가운데 32명이 모두 49번 첫눈에 반했다고 답했고, 겉모습 끌림이 가장 크게 갈랐어요"}
    body = P(*head) + P("<b>📌 내 끌림의 속도를 읽는 순서</b>", *[f"{i + 1}. {q}" for i, q in enumerate(toc_q)])
    for i, (q, s) in enumerate(zip(toc_q, secs)):
        for k in "FSB": s = s.replace(f"[[{k}]]", IMG(nm[k], alt[k]))
        body += H(f"{i + 1}. {q}") + s
    body += tail + CTA
    import copy_rules as CR
    for w in ("재미로", "상담", "—", "안녕하세요, 자오선의 정월이에요", "결론부터 말씀드릴게요", "생년월일만 넣으면 1초", "한 줄 요약", "이 글의 순서", "수비학으로 겹쳐 보면",
              "사람의 공통점", "바람기", "로미오") + tuple(CR.금지어):
        assert w not in re.sub(r"<[^>]+>", " ", body), w
    for f in made:   # 사이트 사본(K-069)
        dst = os.path.join(SITE, "public", "naver", "img", f); os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy(os.path.join(HERE, "img", f), dst)
    return body, a4, made

TITLE = "첫눈에 반하는 이유, 끌림이 빠른 사주와 느린 사주 신호 4가지"
TAGS = ["첫눈에반하는이유", "첫눈에반하다", "첫인상", "금사빠", "금사빠테스트", "끌림", "사주연애", "식상", "연애심리", "자오선"]
REL = {"id": "n77", "title": "2027년 연애운, 좋은 짝 만나는 사주 신호와 도화 달",
       "phrase": "2027년 연애운에서 좋은 짝이 오는 달까지 보고 싶다면, 2027년 연애운, 좋은 짝 만나는 사주 신호와 도화 달",
       "url": "https://blog.naver.com/zaoseon/224465035043"}
KW_VOL = json.load(open(os.path.join(SITE, "data", "keywords", "kw_volume.json"), encoding="utf-8"))["posts"]["n91"]["씨앗"]
INTENT = {"keywords": ["첫눈에반하다", "첫인상", "금사빠"],
          "keyword_src": "kw-volume 작업(data/keywords/kw_volume.json posts.n91, 11/7 20:03) 월 검색량 · n22 조회 순위(재발행 일정 '새 글로 다시 쓰기') · 도화살은 n79·n84가 맡아 뺌",
          "intent": "알고 싶다", "intent_note": "나는 왜 첫눈에 반하는지, 끌림이 빠른 사람과 느린 사람을 무엇으로 가르는지 바로 알고, 반한 다음 무엇을 해 볼지까지 보기",
          "first3": "첫눈에 반하는 이유는 타고난 끌림의 속도와 그날 눈에 들어온 첫인상이 한꺼번에 겹치기 때문이에요.",
          "answer_keys": ["첫눈에 반하는 이유", "도화·식상", "인성·관성"],
          "order": toc_q[:6], "images": ["빠른 신호와 느린 신호(twopanel)", "같은 날 시만 다른 두 사람(compare, 엔진 계산)", "첫눈에 반함 연구(exp)"],
          "related": "n77", "cta": PID, "experience": [], "applied": True,
          "differs_from_n22": "제목·도입(정의 + 네 신호 직답)·소제목 순서·병화/양·사자자리/수비학 3·5 세 풀이와 '몇 개 겹칠까' 대신 사주 신호 넷(도화·식상 / 인성·관성)·예시 장면(1996.4.21 오전 8시 丙辰 · 저녁 6시 辛酉)·그림 유형(twopanel·compare·exp)·심리 개념(확증 편향 → 첫눈에 반함은 강한 첫 끌림, Zsok 외 2017)·출처 2개·연결글(→ n77)·여섯 운명학·로미오 단락 뺌"}

if __name__ == "__main__":
    body, a4, made = build()
    reg = json.load(open(MP.REG, encoding="utf-8"))
    assert PID not in reg or not reg[PID].get("done"), "이미 예약 끝난 글"
    reg[PID] = dict(dt="2027-02-03T18:00:00", dt_tbd="CT가 정함(재발행 일정 11/21 08:00 자리). 이 날짜는 자리값", title=TITLE, tags=TAGS, body=body,
                    cover=a4, related=REL, thumbs=None, cid=None, clips=None, category="관계 읽기", done=False, kw_vol=KW_VOL,
                    k131="n91 11/7(K-151 새 글)", source="build_naver_91.py (n22 주제 새 글, n22 그대로)")
    json.dump(reg, open(MP.REG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    ic = json.load(open(os.path.join(HERE, "intent_cards.json"), encoding="utf-8")); ic["cards"][PID] = INTENT
    json.dump(ic, open(os.path.join(HERE, "intent_cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    v = reg[PID]
    MP.write_page(PID, D.datetime.fromisoformat(v["dt"]), v["title"], v["tags"], v["body"], None, v["cover"], v["related"], v["category"])
    MP.write_index()
    import k151_check as K
    print(PID, len(TITLE), "자 제목 · 본문 글자", len(re.sub(r"<[^>]+>|&nbsp;", "", body)), "· 사진", made, "· K 검사", K.check(PID, v))
