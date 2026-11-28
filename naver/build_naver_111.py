"""네이버 n111: 혼자 일할 때 더 잘하는 사람 새 글 (CT 11/4 재발행 일정 '새 글로 다시 쓰기' n29 → n111, 진행표 docs/네이버_누락글_진행표_2026-11-18.md 열여덟째 줄, 일정표 11/30 18:00 자리).
- 왜: 노출 안 되는 옛 글 n29(혼자 일할 때 더 잘하는 사람, 몰입형 일 스타일 풀이)를 새 글로. n29는 건드리지 않는다(K-147·K-178).
- 검색어: n111 씨앗(혼자일하는직업·혼자일하는게편한사람·몰입·집중력·혼자있고싶을때) 11/28 11:5x 요청, kw-volume 결과로 kw_vol 채움.
- 새 원칙(CLAUDE.md 0~1-3): 첫 줄은 장면, 정의는 첫 200자 안, 면책·출처 줄·설문지 코너·이모지 머리·목차 줄 없음, 링크는 말 속 낱말에.
- 다르게 쓴 것(K-151): n29의 한 줄 요약·세 풀이(신금·계수·처녀·전갈·수비학 4·7)·'몇 개나 겹칠까'·칙센트미하이·투명성 착각·속담 대신
  번스타인·터반 2018 열린 사무실 실험(Phil. Trans. R. Soc. B 373:20170239, PMC 원문 확인:
  1실험 52명 마주 보는 대화 72% 줄고 메일 56%·메신저 67% 늘어 / 2실험 100명 마주 보는 대화 67~71% 줄어, 1실험 경영진이 성과 지표 하락을 연구팀에 전함),
  사주 = 인성(정인·편인, 받아들여 정리하는 글자)과 겁재(나란히 견주는 글자), 예시 같은 날 두 시(1996.7.20 오전 10시 戊 일간 편인 丙·정인 丁 / 오후 2시 편인 丙·겁재 己, engine assert).
  그림 compare(실험)·compare(사주)·checklist. 표 1개(상황 | 이렇게 말해요 | 지켜지는 것). 연결글 → n42(노출 '예').
- 날짜: CT가 정한다. pages.json dt 는 자리값, dt_tbd 로 표시.
사용: SITE=<zaoseon-site> python3 naver/build_naver_111.py"""
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
       '<tr><td style="padding:12px 10px;text-align:center;border:1px solid #d0d0d0"><b>내 여덟 글자에 인성이 몇 개인지 궁금하다면</b></td></tr>'
       '<tr><td style="padding:12px 10px;text-align:center;border:1px solid #d0d0d0"><span style="color:#9a9a9a">[ 1996 . 07 . 20 ]</span></td></tr>'
       '<tr><td style="padding:12px 10px;text-align:center;border:1px solid #d0d0d0"><b><a href="https://zaoseon.com/?utm_source=naver&amp;utm_medium=mid#free">내 태어난 날 글자 보기 →</a></b></td></tr>'
       '</tbody></table>' + BL)
CTA = ('<p><a href="https://zaoseon.com/?utm_source=naver&utm_medium=cta#free"><img src="' + RAW +
       'naver_cta5_1%EC%B4%88%EB%AC%B4%EB%A3%8C%ED%92%80%EC%9D%B4.jpg" alt="자오선 무료 1초 풀이 안내 배너"></a></p>')
PID, KEY, PAL = "n111", "111", "y_olive_s"   # 예시 일간 戊 = 흙 판 묶음(EL_SET 흙). n110 y_black_d · n109 p_purple_s · n108 k_neon_s · n107 p_red_s · n101 y_black_s 와 다른 판

# ───────── 계산값과 검산
import datetime as D
sys.path.insert(0, os.path.join(SITE, "engine"))
import engine as E
A = E.compute_saju(D.datetime(1996, 7, 20, 10))["팔자"]
assert A == {"년주": "丙子", "월주": "乙未", "일주": "戊午", "시주": "丁巳"}, A
assert [E.ten_god("戊", A[k][0]) for k in ("년주", "월주", "시주")] == ["편인", "정관", "정인"]
assert E.compute_saju(D.datetime(1996, 7, 20, 10, 50))["팔자"] == A                 # 같은 巳시 안
B = E.compute_saju(D.datetime(1996, 7, 20, 14))["팔자"]
assert B == {"년주": "丙子", "월주": "乙未", "일주": "戊午", "시주": "己未"}, B
assert [E.ten_god("戊", B[k][0]) for k in ("년주", "월주", "시주")] == ["편인", "정관", "겁재"]
assert E.compute_saju(D.datetime(1996, 7, 20, 14, 50))["팔자"] == B                # 같은 未시 안
# 실험값(논문 원문 PMC6030579): 1실험 52명 · 마주 보는 대화 72% 줄어 · 메일 56% · 메신저 67% 늘어 / 2실험 100명 · 67~71% 줄어
print("예시 A 戊午 일간 · 편인 丙·정인 丁 / 예시 B 같은 날 오후 2시 · 편인 丙·겁재 己 · 72/56/67 확인")

# ───────── 본문 (n29 문장을 옮기지 않았다)
PMC = "https://pmc.ncbi.nlm.nih.gov/articles/PMC6030579/"          # Bernstein & Turban 2018 원문(PMC)
DOI = "https://doi.org/10.1098/rstb.2017.0239"                    # 같은 논문 학술지 주소
KASI = "https://astro.kasi.re.kr/life/pageView/5"                 # 한국천문연구원 음양력 변환
N58 = "https://blog.naver.com/zaoseon/224468727235"   # 십성 뜻 한눈에(노출 '예')
head = ["<b>'다 같이 모여서 정리해 보죠.' 회의실에선 한마디도 못 했는데, 자리로 돌아오니 30분 만에 정리안이 나와요.</b>",
        "혼자 일할 때 더 잘하는 사람은 사람을 피하는 사람이 아니에요. 생각을 끝까지 이어 붙인 다음에 말해야 제 실력이 나오는 사람이에요.",
        "벽을 없애고 다 같이 앉게 한 회사에선, 오히려 마주 보고 나눈 대화가 72% 줄었어요."]
toc_q = ["혼자 일할 때 왜 더 잘될까요?", "벽을 없애면 대화가 늘까요?", "혼자 일하는 시간은 어떻게 지킬까요?",
         "사주로 보면 누가 혼자일 때 힘이 날까요?", "혼자 일하는 사람은 협업을 어떻게 할까요?", "자주 묻는 질문"]
sec1 = P("<b>생각을 처음부터 끝까지 끊기지 않고 이어 붙일 시간이 생겨서요.</b>",
         "기획안 세 줄째를 쓰는데 옆에서 '잠깐 이것 좀요' 하면, 다시 첫 줄부터 읽어야 해요. 끊긴 자리를 찾는 데만 한참 걸리죠.",
         "회의에선 말이 막히는데 메일로는 또박또박 잘 쓰는 사람, 주변에 한 명쯤 있죠. 말이 느린 게 아니에요. 정리가 끝나기 전에 말을 꺼내야 해서 막히는 거예요.")
sec2 = P("<b>반대였어요. 서로 다 보이는 자리에선 사람들이 말을 아끼고 메일로 옮겨 갔어요.</b>",
         f"하버드 경영대학원의 번스타인 교수 팀은 벽과 칸막이를 없앤 회사 두 곳에서 직원들에게 대화를 재는 배지를 달게 했어요. 첫 회사 52명은 사무실을 <a href=\"{PMC}\">열린 구조로 바꾼 뒤</a> 마주 보고 나눈 대화 시간이 72% 줄었어요.") + "[[S]]" + \
       P("대신 서로 보낸 메일은 56%, 메신저 대화는 67% 늘었어요. 두 번째 회사 100명에게서도 마주 보는 대화가 67~71% 줄었고요.",
         f"첫 회사 경영진은 <a href=\"{DOI}\">사내 성과 지표가 떨어졌다는 말</a>도 연구팀에 전했어요. 다 보이는 자리에선 누구나 조금씩 숨는 거예요.")
TD = 'style="padding:10px;border:1px solid #d0d0d0'
TABLE = ('<table style="width:100%;border-collapse:collapse"><tbody>'
         f'<tr><td {TD};text-align:center"><b>상황</b></td><td {TD};text-align:center"><b>이렇게 말해요</b></td><td {TD};text-align:center"><b>지켜지는 것</b></td></tr>'
         + "".join(f'<tr><td {TD}">{a}</td><td {TD}">{b}</td><td {TD}">{c}</td></tr>' for a, b, c in [
             ("회의 직전", "'안건 먼저 받아 볼 수 있을까요?'", "생각 정리할 30분"),
             ("메신저가 계속 올 때", "'2시까지 집중하고 바로 답할게요'", "끊기지 않는 두 시간"),
             ("갑자기 의견을 물을 때", "'정리해서 오늘 안에 보낼게요'", "급한 말 대신 다듬은 글"),
             ("옆자리 수다가 길 때", "'저 이거 마감이라 잠깐 들어갈게요'", "사이도 시간도 그대로")])
         + '</tbody></table>' + BL)
sec3 = P("<b>시간을 먼저 막아 두고, 막은 이유를 한 줄로 알려 주세요.</b>") + TABLE + \
       P("달력에 '집중'이라고 두 시간을 칠해 두면, 회의 잡는 사람도 그 시간을 피해 가요.",
         "말 없이 사라지면 '혼자 다 한다'는 오해가 생겨요. 언제 돌아오는지 한 줄만 붙여도 그 오해가 줄어요.")
sec4 = P(f"<b>사주에서 생각을 받아들이고 정리하는 글자를 <a href=\"{N58}\">인성</a>이라고 해요. 이 글자가 겉에 둘 있으면 혼자 정리하는 시간에 힘이 나요.</b>",
         "배우고, 곱씹고, 머릿속에서 순서를 맞추는 글자라서 끊기지 않는 시간이 있어야 제 몫을 해요.") + "[[C]]" + \
       P("🔎 1996년 7월 20일 오전 10시생은 丙子·乙未·戊午·丁巳예요. 무(戊) 일간 기준으로 해 자리에 편인 丙, 시 자리에 정인 丁이 보여요. 인성이 둘이라, 혼자 정리해 온 말에 힘이 실려요.",
         "같은 날 오후 2시생은 丙子·乙未·戊午·己未로, 시 자리가 겁재 己로 바뀌어요. 겁재는 나와 나란히 서서 견주는 글자예요. 이 사람은 옆 사람 속도를 보면서 일할 때 손이 더 빨라져요.",
         f"같은 날 태어나도 시 하나로 일하는 방식이 갈려요. 태어난 시까지 넣으면 <a href=\"{KASI}\">음력·절기</a>를 맞춘 여덟 글자에 여섯 운명학을 겹쳐, 일하는 자리를 보는 자미두수 관록궁(일 영역)까지 같이 읽어요.") + MID
sec5 = P("<b>혼자 끝낸 정리 한 장을 들고 가면 돼요.</b>") + "[[K]]" + \
       P("빈손으로 회의에 들어가면 남의 말에 끌려가요. 반쯤 된 정리라도 있으면, 그 위에서 이야기가 시작돼요.",
         "혼자 일하는 힘은 숨는 힘이 아니에요. 혼자 다듬은 걸 꺼내 놓는 순간 협업이 오히려 빨라져요.")
sec6 = P("<b>Q. 혼자 일하는 게 편하면 사회성이 부족한 건가요?</b>",
         "A. 아니에요. 말할 준비를 혼자 끝내는 방식일 뿐이에요. 준비가 되면 회의에서도 말이 잘 나와요.") + \
       P("<b>Q. 재택처럼 완전히 혼자 일하면 더 좋을까요?</b>",
         "A. 혼자 일하는 시간과 나누는 시간을 둘 다 정해 두세요. 혼자만 길어지면 중간 상황을 나눌 때를 놓쳐요.")
tail = P("여러분은 어떤 순간에 일이 제일 잘 풀리나요? 혼자 문 닫고 있을 때인가요, 옆에 누가 있을 때인가요?", "댓글에 한 줄만 남겨 주세요.") + \
       '<p><b>👇 사람 많은 자리에서 유독 예민해진다면, 예민한 사람이 쉽게 피곤한 이유, 감각이 큰 사람의 마음</b></p>'
secs = [sec1, sec2, sec3, sec4, sec5, sec6]

def _have(n): return os.path.exists(os.path.join(HERE, "img", n))
def build():
    for d_ in ("wide", "m1280", "master"): os.makedirs(os.path.join(HERE, "img", d_), exist_ok=True)
    c = V.Ctx(PAL); made = []
    a4 = f"wide/naver_z{KEY}_a1.jpg"   # 표지 항목은 한글만(한자는 글꼴에 없어 네모)
    if not _have(a4):
        V.render(PID + "_new", {"d": "N", "el": "흙", "kick": "혼자 일할 때 더 잘하는 사람", "hook": ["벽을 없애자", "대화가 72% 뚝"], "sub": "열린 사무실 실험과 사주 인성",
                                "items": ["72%", "52명", "편인·정인"]}, os.path.join(HERE, "img", a4), PAL)
    made.append(a4)
    nm = {"S": f"naver_z{KEY}_t1.jpg", "C": f"naver_z{KEY}_t2.jpg", "K": f"naver_z{KEY}_k1.jpg"}
    if not _have(nm["S"]):
        DGC.compare(nm["S"], c, "벽을 없앤 뒤 바뀐 것", ("벽 있던 때", "벽 없앤 뒤"),
                    [("누가", "첫 회사 52명", "같은 52명"), ("마주 보는 대화", "기준", "72% 줄어요"),
                     ("서로 보낸 메일", "기준", "56% 늘어요"), ("메신저 대화", "기준", "67% 늘어요")],
                    "번스타인·터반 2018 · 두 번째 회사 100명도 67~71% 줄어요", hi=1)
    if not _have(nm["C"]):
        DGC.compare(nm["C"], c, "같은 날 태어나도 시 하나로 갈려요", ("혼자일 때 힘 나요", "옆에 있으면 빨라요"),
                    [("예시", "1996.7.20 오전 10시", "1996.7.20 오후 2시"), ("일간", "무 일간", "무 일간"),
                     ("시 자리", "정인 정화", "겁재 기토"), ("인성", "편인 + 정인 둘", "편인 하나"),
                     ("잘 되는 때", "혼자 정리한 뒤", "옆 사람과 견줄 때")],
                    "만세력 계산값 · 인성은 받아들여 정리하는 글자, 겁재는 나란히 견주는 글자", hi=0)
    if not _have(nm["K"]):
        DGB.checklist(nm["K"], c, "혼자 일하는 사람의 협업 세 단계", [("혼자 30분", "안건 받아 생각 정리"),
                                                       ("정리 한 장", "반쯤 된 것도 괜찮아요"),
                                                       ("중간에 한 줄", "'여기까지 했어요' 나누기")], note="혼자 다듬고, 꺼내 놓기")
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
    alt = {"S": "열린 사무실 실험 비교 표. 벽을 없앤 뒤 52명이 마주 보고 나눈 대화는 72% 줄고, 메일은 56%, 메신저는 67% 늘었어요",
           "C": "같은 날 다른 시에 태어난 두 사주 비교 표. 1996년 7월 20일 오전 10시생은 인성이 둘, 오후 2시생은 시 자리가 겁재예요",
           "K": "혼자 일하는 사람의 협업 세 단계 칸. 혼자 30분 정리, 정리 한 장, 중간에 한 줄 나누기예요"}
    body = P(*head)   # 목차 줄은 넣지 않는다(n106~n110 과 같게)
    for i, (q, s) in enumerate(zip(toc_q, secs)):
        for k in "SCK": s = s.replace(f"[[{k}]]", IMG(nm[k], alt[k]))
        body += H(f"{i + 1}. {q}") + s
    body += tail + CTA
    import copy_rules as CR
    for w in ("재미로", "상담", "—", "안녕하세요, 자오선의 정월이에요", "결론부터", "핵심부터", "생년월일만 넣으면 1초", "한 줄 요약", "이 글의 순서", "수비학",
              "공통점", "몇 개나", "겹칠까", "세 풀이", "신금", "계수", "처녀자리", "전갈자리", "칙센트미하이", "투명성", "백지장",
              "총정리", "기운", "흐름", "편이에요", "상대 쪽", "📚", "해 볼 것", "가상", "예시 장면", "반드시", "무조건", "지도") + tuple(CR.금지어):
        assert w not in re.sub(r"<[^>]+>", " ", body), w
    for f in made:   # 사이트 사본(K-069)
        dst = os.path.join(SITE, "public", "naver", "img", f); os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy(os.path.join(HERE, "img", f), dst)
    return body, a4, made

TITLE = "혼자 일할 때 더 잘하는 이유, 대화 72% 줄어든 사무실 실험"
TAGS = ["혼자일할때", "혼자일하는게편한사람", "집중력", "몰입", "회의", "열린사무실", "인성", "편인", "십성", "자오선"]
REL = {"id": "n42", "title": "예민한 사람이 쉽게 피곤한 이유, 감각이 큰 사람의 마음",
       "phrase": "사람 많은 자리에서 유독 예민해진다면, 예민한 사람이 쉽게 피곤한 이유, 감각이 큰 사람의 마음",
       "url": "https://blog.naver.com/zaoseon/224447837285"}
KW_VOL = (json.load(open(os.path.join(SITE, "data", "keywords", "kw_volume.json"), encoding="utf-8"))["posts"].get(PID) or {}).get("씨앗") or {}
INTENT = {"keywords": ["혼자일하는게편한사람", "집중력", "몰입", "혼자일하는직업"],
          "keyword_src": "n111 씨앗 요청(11/28 11:5x) · kw-volume 결과로 채움",
          "intent": "이유를 알고 싶다", "intent_note": "혼자 일할 때 왜 더 잘되는지, 다 같이 앉으면 정말 협업이 늘어나는지, 혼자 일하는 시간 지키는 말, 사주로 보는 인성, 협업하는 법",
          "first3": "회의실에선 한마디도 못 했는데 자리로 돌아오니 30분 만에 정리안이 나와요. 혼자 일할 때 더 잘하는 사람은 생각을 끝까지 이어 붙인 다음에 말해야 제 실력이 나오는 사람이에요.",
          "answer_keys": ["끊기지 않는 시간이 생겨서", "벽 없앤 사무실 52명 마주 보는 대화 72% 줄고 메일 56% 늘어", "시간 지키는 한마디 표", "인성 둘이면 혼자 정리한 뒤 힘이 남"],
          "community_q": [], "order": toc_q,
          "images": ["열린 사무실 실험 전후(compare)", "같은 날 두 시 사주 비교(compare)", "협업 세 단계(checklist)"],
          "related": "n42", "cta": PID, "experience": [], "applied": True}

if __name__ == "__main__":
    body, a4, made = build()
    reg = json.load(open(MP.REG, encoding="utf-8"))
    assert PID not in reg or not reg[PID].get("done"), "이미 예약 끝난 글"
    reg[PID] = dict(dt="2027-02-16T18:00:00", dt_tbd="CT가 정함(재발행 일정 'n29 다시 쓰기' 11/30 18:00 자리, 진행표 11/18). 이 날짜는 자리값", title=TITLE, tags=TAGS, body=body,
                    cover=a4, related=REL, thumbs=None, cid=None, clips=None, category="마음 읽기", done=False, kw_vol=KW_VOL,
                    k131="n111 11/28(K-151 새 글, n29 다시 쓰기)", source="build_naver_111.py (n29 → n111 새 글)")
    json.dump(reg, open(MP.REG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    ic = json.load(open(os.path.join(HERE, "intent_cards.json"), encoding="utf-8")); ic["cards"][PID] = INTENT
    json.dump(ic, open(os.path.join(HERE, "intent_cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    v = reg[PID]
    MP.write_page(PID, D.datetime.fromisoformat(v["dt"]), v["title"], v["tags"], v["body"], None, v["cover"], v["related"], v["category"])
    MP.write_index()
    import k151_check as K
    print(PID, len(TITLE), "자 제목 · 본문 글자", len(re.sub(r"<[^>]+>|&nbsp;", "", body)), "· 사진", made, "· K 검사", K.check(PID, v))
