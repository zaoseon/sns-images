"""네이버 n108: 오늘의 운세 새 글 (CT 11/4 재발행 일정 '새 글로 다시 쓰기' n50 → n108, 진행표 docs/네이버_누락글_진행표_2026-11-18.md 열넷째 줄).
- 왜: 노출 안 되는 옛 글 n50(오늘의 운세, 일진과 내 일간 쉽게 읽는 법)을 새 글로. n50은 건드리지 않는다(K-147·K-178).
- 검색어: kw-volume n108 씨앗(오늘의운세·오늘운세·일진·일진보는법·오늘일진, 11/23 11:5x 요청).
- 새 원칙(CLAUDE.md 0~1-3): 첫 줄은 장면(ZS-01), 정의는 첫 200자 안, 모순 하나(믿자니 앱마다 다르고 안 보자니 손이 감) → 잡을 것/놓을 것,
  면책·출처 줄·설문지 코너·이모지 머리·목차 줄 없음, 링크는 말 속 낱말에.
- 다르게 쓴 것(K-151): n50의 결론 먼저·한 줄 요약·다섯 관계 목록·병화 10/19~25 예시·수비학·통제소재 대신
  앱마다 다른 이유 3가지(띠 대 일간 · 밤 11시 자시 경계 · 입춘), 밤 11시 30분생 예시(1996.3.19 → 乙 / 丙, engine ja_si_next_day assert),
  갑 일간 예시(1997.4.22 오전 9시 丁丑·甲辰·甲午·己巳)의 2026년 12월 7~15일 일진(engine assert),
  일진 = 한국민족문화대백과사전 E0047325(60갑자를 그날그날에 붙임, 원문 확인) · 심리 = 실행 의도(Gollwitzer & Sheeran 2006, Advances in Experimental Social Psychology 38:69-119, 94개 독립 검증 d=.65, KOPS 초록 원문 확인).
  그림 compare·route·checklist. 표 1개(기준 | 이렇게 보면 | 달라지는 사람). 연결글 → n75(노출 '예').
- 날짜: CT가 정한다. pages.json dt 는 자리값, dt_tbd 로 표시.
사용: SITE=<zaoseon-site> python3 naver/build_naver_108.py"""
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
       '<tr><td style="padding:12px 10px;text-align:center;border:1px solid #d0d0d0"><b>내 일간이 무엇인지 궁금하다면</b></td></tr>'
       '<tr><td style="padding:12px 10px;text-align:center;border:1px solid #d0d0d0"><span style="color:#9a9a9a">[ 1997 . 04 . 22 ]</span></td></tr>'
       '<tr><td style="padding:12px 10px;text-align:center;border:1px solid #d0d0d0"><b><a href="https://zaoseon.com/?utm_source=naver&amp;utm_medium=mid#free">내 태어난 날 글자 보기 →</a></b></td></tr>'
       '</tbody></table>' + BL)
CTA = ('<p><a href="https://zaoseon.com/?utm_source=naver&utm_medium=cta#free"><img src="' + RAW +
       'naver_cta5_1%EC%B4%88%EB%AC%B4%EB%A3%8C%ED%92%80%EC%9D%B4.jpg" alt="자오선 무료 1초 풀이 안내 배너"></a></p>')
PID, KEY, PAL = "n108", "108", "k_neon_s"   # 예시 일간 甲 = 나무 판 묶음(y_olive_s 는 checklist 회색 글 대비 1.1~1.3 막음). n107 p_red_s · n106 m_soft_s · n105 p_black_s 와 다른 판

# ───────── 계산값과 검산
import datetime as D
sys.path.insert(0, os.path.join(SITE, "engine"))
import engine as E
WEEK = {7: "乙卯", 8: "丙辰", 9: "丁巳", 10: "戊午", 11: "己未", 12: "庚申", 13: "辛酉", 14: "壬戌", 15: "癸亥"}
for d_, g_ in WEEK.items(): assert E._ganji_str(E.day_pillar(D.date(2026, 12, d_))) == g_, (d_, g_)
A = E.compute_saju(D.datetime(1997, 4, 22, 9))["팔자"]
assert A == {"년주": "丁丑", "월주": "甲辰", "일주": "甲午", "시주": "己巳"}, A
TG = {d_: E.ten_god("甲", g_[0]) for d_, g_ in WEEK.items()}
assert TG == {7: "겁재", 8: "식신", 9: "상관", 10: "편재", 11: "정재", 12: "편관", 13: "정관", 14: "편인", 15: "정인"}, TG
N1 = E.compute_saju(D.datetime(1996, 3, 19, 23, 30))["팔자"]["일주"]                       # 밤 11시부터 다음 날
N0 = E.compute_saju(D.datetime(1996, 3, 19, 23, 30), ja_si_next_day=False)["팔자"]["일주"]  # 자정에 날 바꿈
assert (N0, N1) == ("乙卯", "丙辰"), (N0, N1)
assert E.ten_god("乙", "戊") == "정재" and E.ten_god("丙", "戊") == "식신"
print("12/7~15 일진 · 갑 일간 십성 · 밤 11시 30분생 乙/丙 확인")

# ───────── 본문 (n50 문장을 옮기지 않았다)
ENC = "https://encykorea.aks.ac.kr/Article/E0047325"   # 한국민족문화대백과사전 일진(日辰)
KOPS = "https://kops.uni-konstanz.de/entities/publication/2e749bfb-8533-437c-8203-7e788c910c5f"
head = ["<b>출근길에 운세 앱 두 개를 열었더니, 하나는 '귀인 만나는 날', 하나는 '말조심할 날'이래요.</b>",
        "믿자니 앱마다 말이 다르고, 안 보자니 아침마다 손이 가죠. 오늘의 운세는 그날 날짜에 붙는 두 글자인 일진과, 내가 태어난 날의 하늘 글자인 일간이 어떤 사이인지 보는 풀이예요. 앱마다 다르게 나오는 건 대개 '내 글자'를 어디서 가져오느냐가 달라서고요.",
        "이 기준 하나만 잡으면 앱을 몇 개씩 돌려 볼 일이 없어져요."]
toc_q = ["오늘의 운세는 왜 앱마다 다르게 나올까요?", "오늘 일진은 어떻게 찾을까요?", "내 일간과 일진은 어떻게 맞춰 볼까요?",
         "운세가 나쁘게 나온 날엔 어떻게 쓸까요?", "자주 묻는 질문"]
TD = 'style="padding:10px;border:1px solid #d0d0d0'
TABLE = ('<table style="width:100%;border-collapse:collapse"><tbody>'
         f'<tr><td {TD};text-align:center"><b>기준</b></td><td {TD};text-align:center"><b>이렇게 보면</b></td><td {TD};text-align:center"><b>달라지는 사람</b></td></tr>'
         + "".join(f'<tr><td {TD}">{a}</td><td {TD}">{b}</td><td {TD}">{c}</td></tr>' for a, b, c in [
             ("띠", "같은 해에 태어나면 모두 같은 글", "같은 띠라도 생일마다 하루가 달라요"),
             ("태어난 날", "생일마다 다른 글", "밤 11시~자정생은 날 글자가 바뀌어요"),
             ("해가 바뀌는 날", "입춘(2월 4일 무렵)부터 새해", "1월~2월 초생은 앞 해 띠로 봐요")])
         + '</tbody></table>' + BL)
sec1 = P("<b>띠로 보느냐 태어난 날로 보느냐, 그리고 밤 11시를 어느 날로 치느냐가 달라서예요.</b>",
         "띠 운세는 같은 해에 태어난 사람 모두에게 같은 글이 나가요. 1997년생 소띠라면 그해 태어난 사람 전부가 같은 하루를 받는 셈이죠. 태어난 날 글자로 보는 운세는 같은 소띠라도 생일마다 달라지고요.") + TABLE + \
       P("셋 중에 제일 많이 헷갈리는 게 밤 11시예요. 옛 시간으로 밤 11시부터 새벽 1시까지가 자시(子時)라서, 밤 11시부터 다음 날로 치는 곳과 자정에 날을 바꾸는 곳이 나뉘거든요.") + "[[C]]" + \
       P("1996년 3월 19일 밤 11시 30분에 태어났다면 자정 기준으론 을(乙) 일간, 밤 11시 기준으론 병(丙) 일간이에요. 나무와 불, 아예 다른 사람이 돼 버려요. 이 시간대에 태어났다면 앱 설명에서 '자시' 기준부터 찾아보세요.")
sec2 = P("<b>날마다 글자 짝 60개가 차례로 하나씩 붙고, 60일이 지나면 처음으로 돌아와요.</b>",
         f"이렇게 그날그날에 붙는 글자 짝을 <a href=\"{ENC}\">일진</a>이라고 불러요. 2026년 12월 7일 월요일은 을묘(乙卯)일, 8일은 병진(丙辰)일, 9일은 정사(丁巳)일이에요. 앞 글자인 하늘 글자가 하루에 한 칸씩 갑·을·병·정… 열 개를 돌죠.",
         "오늘의 운세를 직접 읽을 땐 이 앞 글자 하나만 봐도 충분해요. 뒤 글자인 땅 글자까지 겹쳐 보는 건 그다음 일이에요.") + MID
sec3 = P("<b>그날 앞 글자가 나와 같은 오행인지, 나를 채우는지, 내가 키우는지, 내가 다루는지, 나를 다잡는지만 보면 돼요.</b>",
         "1997년 4월 22일 오전 9시생은 丁丑·甲辰·甲午·己巳로, 갑(甲) 일간이에요. 쭉 뻗은 큰 나무 같은 사람이죠. 이 사람의 12월 둘째 주를 그대로 읽어 볼게요.") + "[[R]]" + \
       P("7일 乙은 같은 나무라 내 방식이 또렷해지는 날, 8·9일 丙·丁은 나무가 불을 키우는 날이라 말하고 내놓기 좋은 날이에요.",
         "10·11일 戊·己 흙은 나무가 뿌리로 붙잡는 땅이라 돈과 일을 정리하기 좋고, 12·13일 庚·辛 쇠는 나무를 다듬는 도끼라 약속과 규칙에 묶이기 쉬워요. 14일 壬부터는 물이 나무를 채워 주는 이틀이라, 쉬고 배우기에 딱이고요.")
sec4 = P("<b>'조심하세요'라는 말을 '이럴 땐 이렇게 한다' 한 줄로 바꿔 두면 돼요.</b>",
         f"심리학자 골비처와 시런이 <a href=\"{KOPS}\">94개의 검증</a>을 모아 봤더니, '만약 ~하면 ~한다'처럼 상황과 행동을 미리 짝지어 둔 사람이 목표를 더 잘 이뤘어요. 효과 크기가 0.65로, 심리학에서 중간보다 큰 쪽이에요.",
         "갑 일간이 12일 경신(庚申)일 운세에서 '말조심'을 봤다면 이렇게 적어 두는 거예요. '회의에서 반대 의견이 나오면, 바로 답하지 말고 메모부터 한다.' 겁나던 문장이 오늘 할 행동 하나로 바뀌어요.") + "[[K]]" + \
       P("잡을 건 내 일간 하나, 놓을 건 앱 여러 개 돌려 보기예요. 내일 아침엔 일진 앞 글자만 보고, 할 일 한 줄을 정해서 나가 보세요.")
sec5 = P("<b>Q. 띠 운세는 틀린 건가요?</b>",
         "A. 틀린 게 아니라 넓게 본 거예요. 같은 해 태어난 사람들의 한 해를 볼 땐 띠가, 내 오늘 하루를 볼 땐 일간이 더 가까워요.") + \
       P("<b>Q. 태어난 시간을 모르면 못 보나요?</b>",
         "A. 일간은 날짜만 있으면 나와요. 밤 11시 무렵에 태어난 게 아니라면 시간 없이도 오늘의 운세는 읽을 수 있어요.")
tail = P("여러분은 아침에 운세 앱을 몇 개나 열어 보세요?", "댓글에 '하나'나 '여러 개' 한 마디만 남겨 주세요.") + \
       '<p><b>👇 내 일간을 만세력에서 직접 찾는 법이 궁금하다면, 만세력 보는 법 3곳, 일간·오행과 앱마다 시주가 다른 이유</b></p>'
secs = [sec1, sec2, sec3, sec4, sec5]

def _have(n): return os.path.exists(os.path.join(HERE, "img", n))
def build():
    for d_ in ("wide", "m1280", "master"): os.makedirs(os.path.join(HERE, "img", d_), exist_ok=True)
    c = V.Ctx(PAL); made = []
    a4 = f"wide/naver_z{KEY}_a1.jpg"   # 표지 항목은 한글만(한자는 글꼴에 없어 네모)
    if not _have(a4):
        V.render(PID + "_new", {"d": "N", "el": "나무", "kick": "오늘의 운세", "hook": ["운세 앱마다", "말이 다른 이유"], "sub": "일진과 내 일간으로 읽기",
                                "items": ["띠", "밤 11시", "일간"]}, os.path.join(HERE, "img", a4), PAL)
    made.append(a4)
    nm = {"C": f"naver_z{KEY}_t1.jpg", "R": f"naver_z{KEY}_r1.jpg", "K": f"naver_z{KEY}_k1.jpg"}
    if not _have(nm["C"]):
        DGC.compare(nm["C"], c, "밤 11시 30분생, 앱마다 다른 일간", ("자정에 날 바꿈", "밤 11시에 날 바꿈"),
                    [("태어난 때", "1996.3.19 밤 11시 30분", "1996.3.19 밤 11시 30분"), ("치는 날", "3월 19일", "3월 20일"),
                     ("일간", "을 일간 · 나무", "병 일간 · 불"), ("12월 10일 무오일", "내가 다루는 날", "내가 내놓는 날")],
                    "만세력 계산값 · 밤 11시~새벽 1시가 자시예요", hi=1)
    if not _have(nm["R"]):
        DGB.route(nm["R"], c, "갑 일간의 12월 둘째 주", [("7일 을", "내 방식대로"), ("8·9일 병·정", "말하고 내놓기"),
                                                   ("10·11일 무·기", "돈과 일 정리"), ("12·13일 경·신", "약속에 묶임"), ("14·15일 임·계", "쉬고 배우기")])
    if not _have(nm["K"]):
        DGB.checklist(nm["K"], c, "운세 본 아침, 한 줄 만들기", [("오늘 일진 앞 글자 보기", "12월 12일이면 경(쇠)"), ("내 일간과 사이 찾기", "갑 일간에겐 나무를 다듬는 날"),
                                                        ("'~하면 ~한다' 한 줄 적기", "반대 의견이 나오면 메모부터")], note="상황과 행동을 미리 짝지어 두는 거예요")
    import fullbleed as FBL
    plan_p = os.path.join(HERE, "fullbleed_plan.json"); plan = json.load(open(plan_p, encoding="utf-8")) if os.path.exists(plan_p) else {}
    rows = []
    for pos, k in enumerate("CRK", 1):
        f = nm[k][:-4] + "f.jpg"
        if not _have(f):
            r, why = FBL.convert(nm[k], [os.path.join(HERE, "img"), os.path.join(HERE, "img", "m1280")])
            if not r: print("fullbleed 건너뜀", nm[k], why); made.append(nm[k]); continue
        rows.append({"pos": pos, "old": nm[k], "new": f}); made.append(nm[k]); nm[k] = f
        reg_ = json.load(open(DG.REG, encoding="utf-8")); reg_[f] = reg_[rows[-1]["old"]]; json.dump(dict(sorted(reg_.items())), open(DG.REG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    plan[PID] = rows; json.dump(plan, open(plan_p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    made += [v for v in nm.values() if v not in made]
    alt = {"C": "밤 11시 30분생 비교 표. 자정에 날을 바꾸면 을 일간, 밤 11시에 날을 바꾸면 병 일간이에요",
           "R": "갑 일간의 12월 7일부터 15일까지 길 그림. 같은 나무, 불을 키움, 흙을 붙잡음, 쇠가 다듬음, 물이 채움 순서예요",
           "K": "운세 본 아침 한 줄 만들기 칸. 일진 앞 글자 보기, 내 일간과 사이 찾기, 하면 한다 한 줄 적기예요"}
    body = P(*head)   # 목차 줄은 넣지 않는다(n106·n107 과 같게)
    for i, (q, s) in enumerate(zip(toc_q, secs)):
        for k in "CRK": s = s.replace(f"[[{k}]]", IMG(nm[k], alt[k]))
        body += H(f"{i + 1}. {q}") + s
    body += tail + CTA
    import copy_rules as CR
    for w in ("재미로", "상담", "—", "안녕하세요, 자오선의 정월이에요", "결론부터", "핵심부터", "생년월일만 넣으면 1초", "한 줄 요약", "이 글의 순서", "수비학",
              "통제소재", "병화 일간", "다섯 가지", "누르", "총정리", "기운", "흐름", "편이에요", "상대 쪽", "📚", "해 볼 것", "가상", "예시 장면") + tuple(CR.금지어):
        assert w not in re.sub(r"<[^>]+>", " ", body), w
    for f in made:   # 사이트 사본(K-069)
        dst = os.path.join(SITE, "public", "naver", "img", f); os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy(os.path.join(HERE, "img", f), dst)
    return body, a4, made

TITLE = "오늘의 운세 앱마다 다른 이유 3가지, 일진으로 내 하루 읽기"
TAGS = ["오늘의운세", "오늘운세", "일진", "일진보는법", "오늘일진", "일간", "만세력", "띠운세", "자시", "자오선"]
REL = {"id": "n75", "title": "만세력 보는 법 3곳, 일간·오행과 앱마다 시주가 다른 이유",
       "phrase": "내 일간을 만세력에서 직접 찾는 법이 궁금하다면, 만세력 보는 법 3곳, 일간·오행과 앱마다 시주가 다른 이유",
       "url": "https://blog.naver.com/zaoseon/224463601442"}
KW_VOL = (json.load(open(os.path.join(SITE, "data", "keywords", "kw_volume.json"), encoding="utf-8"))["posts"].get(PID) or {}).get("씨앗") or {}
INTENT = {"keywords": ["오늘의운세", "오늘운세", "일진", "일진보는법"],
          "keyword_src": "kw-volume n108 씨앗(오늘의운세·오늘운세·일진·일진보는법·오늘일진, 11/23 요청)",
          "intent": "원리를 알고 싶다", "intent_note": "운세 앱마다 결과가 다른 까닭, 일진 찾는 법, 내 일간과 맞춰 읽는 법, 나쁜 운세를 쓰는 법",
          "first3": "출근길에 운세 앱 두 개를 열었더니, 하나는 '귀인 만나는 날', 하나는 '말조심할 날'이래요. 오늘의 운세는 그날 날짜에 붙는 두 글자인 일진과, 내가 태어난 날의 하늘 글자인 일간이 어떤 사이인지 보는 풀이예요.",
          "answer_keys": ["띠 대 일간 · 밤 11시 경계 · 입춘", "일진은 60일마다 돌아옴", "앞 글자 하나로 다섯 사이", "'~하면 ~한다' 한 줄(94개 검증 d=.65)"],
          "community_q": [], "order": toc_q, "images": ["밤 11시 30분생 일간 비교(compare)", "갑 일간 12월 둘째 주(route)", "운세 본 아침 한 줄(checklist)"],
          "related": "n75", "cta": PID, "experience": [], "applied": True}

if __name__ == "__main__":
    body, a4, made = build()
    reg = json.load(open(MP.REG, encoding="utf-8"))
    assert PID not in reg or not reg[PID].get("done"), "이미 예약 끝난 글"
    reg[PID] = dict(dt="2027-02-14T08:00:00", dt_tbd="CT가 정함(재발행 일정 'n50 다시 쓰기' 자리, 진행표 11/18). 이 날짜는 자리값", title=TITLE, tags=TAGS, body=body,
                    cover=a4, related=REL, thumbs=None, cid=None, clips=None, category="운명학 사전", done=False, kw_vol=KW_VOL,
                    k131="n108 11/23(K-151 새 글, n50 다시 쓰기)", source="build_naver_108.py (n50 → n108 새 글)")
    json.dump(reg, open(MP.REG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    ic = json.load(open(os.path.join(HERE, "intent_cards.json"), encoding="utf-8")); ic["cards"][PID] = INTENT
    json.dump(ic, open(os.path.join(HERE, "intent_cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    v = reg[PID]
    MP.write_page(PID, D.datetime.fromisoformat(v["dt"]), v["title"], v["tags"], v["body"], None, v["cover"], v["related"], v["category"])
    MP.write_index()
    import k151_check as K
    print(PID, len(TITLE), "자 제목 · 본문 글자", len(re.sub(r"<[^>]+>|&nbsp;", "", body)), "· 사진", made, "· K 검사", K.check(PID, v))
