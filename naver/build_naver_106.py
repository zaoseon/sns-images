"""네이버 n106: 사과하는 법 새 글 (CT 11/4 19:40 재발행 일정 '새 글로 다시 쓰기' n19 → n106, 진행표 docs/네이버_누락글_진행표_2026-11-18.md 열셋째 줄).
- 왜: 노출 안 되는 옛 글 n19(싸우면 먼저 사과하는 사람의 공통점, 사주·별자리·숫자)를 새 글로. n19는 건드리지 않는다(K-147·K-178).
- 검색어(kw_volume n106, 11/21 19:54): 사과하는법 310 · 화해하는법 45 · 연인싸움 25 · 먼저사과하는사람 15 · 먼저사과 10. 월 100 이상은 '사과하는법' 하나라 제목 첫 낱말로.
- 새 원칙(CLAUDE.md 0~1-3, 11/21): 첫 줄은 사연 장면(ZS-01), 정의는 첫 200자 안, 본문은 모순 하나 → 잡을 것/놓을 것, 면책·출처 줄·설문지 코너·이모지 머리 없음, 링크는 말 속 낱말에.
- 다르게 쓴 것(K-151): n19의 '결론 먼저'·한 줄 요약·세 풀이(乙·己 일간·천칭/물고기자리·수비학 2·6)·'몇 개나 겹칠까'·논어·표현 억제 대신
  사과 여섯 요소 실험(Lewicki·Polin·Lount, Negotiation and Conflict Management Research 2016년 5월호, 두 실험 755명 = 성인 333명 + 대학생 422명:
  책임 인정 1위 · 바로잡을 약속 2위 · 후회 표현·잘못 설명·다시 안 하겠다는 다짐 공동 3위 · 용서 요청 꼴찌 · 요소가 많을수록 효과적, 오하이오주립대 보도자료 2016-04-12 원문 확인),
  사주 = 정관(나를 다잡는 글자)과 비견·겁재, 예시 둘(1995.8.3 오전 10시 丙 일간 정관 癸 두 자리 / 1996.9.27 낮 12시 丁 일간 둘레 불 글자, engine assert).
  일간 정관 짝 열 개 ten_god assert. 그림 유형 ladder·compare·chat. 표 1개(먼저 사과할 신호 | 기다려도 될 신호). 연결글 → n91.
- 날짜: CT가 정한다. pages.json dt 는 자리값, dt_tbd 로 표시.
사용: SITE=<zaoseon-site> python3 naver/build_naver_106.py"""
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
       '<tr><td style="padding:12px 10px;text-align:center;border:1px solid #d0d0d0"><b>내 여덟 글자에 정관이 있는지 궁금하다면</b></td></tr>'
       '<tr><td style="padding:12px 10px;text-align:center;border:1px solid #d0d0d0"><span style="color:#9a9a9a">[ 1995 . 08 . 03 ]</span></td></tr>'
       '<tr><td style="padding:12px 10px;text-align:center;border:1px solid #d0d0d0"><b><a href="https://zaoseon.com/?utm_source=naver&amp;utm_medium=mid#free">내 태어난 날 글자 보기 →</a></b></td></tr>'
       '</tbody></table>' + BL)
CTA = ('<p><a href="https://zaoseon.com/?utm_source=naver&utm_medium=cta#free"><img src="' + RAW +
       'naver_cta5_1%EC%B4%88%EB%AC%B4%EB%A3%8C%ED%92%80%EC%9D%B4.jpg" alt="자오선 무료 1초 풀이 안내 배너"></a></p>')
PID, KEY, PAL = "n106", "106", "m_soft_s"   # 예시 두 사람 일간 丙·丁 = 불 판 묶음. n107 p_red_s · n105 p_black_s · n104 m_young_s 와 다른 판

# ───────── 계산값과 검산
import datetime as D
sys.path.insert(0, os.path.join(SITE, "engine"))
import engine as E
JG = {"甲": "辛", "乙": "庚", "丙": "癸", "丁": "壬", "戊": "乙", "己": "甲", "庚": "丁", "辛": "丙", "壬": "己", "癸": "戊"}
for a_, b_ in JG.items(): assert E.ten_god(a_, b_) == "정관", (a_, b_)
A = E.compute_saju(D.datetime(1995, 8, 3, 10))["팔자"]
assert A == {"년주": "乙亥", "월주": "癸未", "일주": "丙寅", "시주": "癸巳"}, A
assert [E.ten_god("丙", A[k][0]) for k in ("월주", "시주")] == ["정관", "정관"]
assert E.compute_saju(D.datetime(1995, 8, 3, 10, 50))["팔자"] == A                 # 같은 巳시 안
B = E.compute_saju(D.datetime(1996, 9, 27, 12))["팔자"]
assert B == {"년주": "丙子", "월주": "丁酉", "일주": "丁卯", "시주": "丙午"}, B
assert [E.ten_god("丁", B[k][0]) for k in ("년주", "월주", "시주")] == ["겁재", "비견", "겁재"]
assert not any(E.ten_god("丁", B[k][0]) in ("정관", "편관") for k in B if k != "일주")
print("예시 A 丙寅 일간 · 癸 정관 두 자리 / 예시 B 丁卯 일간 · 丙丁 겁재·비견 세 자리 · 정관 짝 열 개 확인")

# ───────── 본문 (n19 문장을 옮기지 않았다)
OSU = "https://news.osu.edu/the-6-elements-of-an-effective-apology-according-to-science/"
EKU = "https://encompass.eku.edu/fs_research/92"   # 논문 목록 쪽(An Exploration of the Structure of Effective Apologies)
head = ["<b>싸우고 이틀째, 카톡 창에 '미안해'를 썼다 지웠다 하다가 결국 또 내가 먼저 보내요.</b>",
        "보내고 나면 잠깐 후련한데, 그날 밤엔 이상하게 더 서운하죠. 사과하는 법의 핵심은 '미안해' 한 마디가 아니라 '내가 이걸 잘못했어'를 먼저 말하는 거예요. 그래야 싸움이 끝난 뒤에 내 이야기를 꺼낼 자리도 생겨요.",
        "755명에게 사과문을 읽혀 본 실험에서도 마음이 풀린 사과엔 이 한 줄이 꼭 있었어요."]
toc_q = ["먼저 사과했는데 왜 더 서운할까요?", "잘 받아들여지는 사과는 무엇이 다를까요?", "먼저 사과할 때와 기다릴 때는 어떻게 가를까요?",
         "사주로 보면 사과가 빠른 사람과 느린 사람은 누구일까요?", "사과하는 카톡은 어떻게 보낼까요?", "자주 묻는 질문"]
sec1 = P("<b>싸움은 사과로 끝냈는데, 내가 왜 서운했는지는 한 번도 말하지 못했으니까요.</b>",
         "'미안해'를 먼저 보내면 상대는 다 풀린 줄 알아요. 나는 싸움을 끝내고 싶었던 거지, 내 서운함까지 없던 일로 하려던 건 아닌데요.",
         "관계는 지키고 싶고, 내 마음도 알아줬으면 좋겠고. 이 두 마음이 같이 있는데 사과 한 마디로 앞의 것만 챙기니까, 다음 싸움에서도 또 내가 먼저 숙이게 되는 거예요.")
sec2 = P("<b>'내 잘못이야'라고 책임을 인정하는 말이 들어 있느냐가 가장 컸어요.</b>",
         f"미국 오하이오주립대 르위키 교수 연구팀은 <a href=\"{OSU}\">두 번의 실험</a>에서 성인 333명과 대학생 422명에게 여러 사과문을 보여 주고, 얼마나 마음이 움직이는지 물었어요. 사과에 들어가는 말은 <a href=\"{EKU}\">여섯 가지</a>로 나눴고요.") + "[[L]]" + \
       P("1위는 책임 인정, 2위는 '이렇게 바로잡을게'라는 약속이었어요. 미안한 마음, 무엇이 잘못됐는지 설명, 다시 안 그러겠다는 다짐은 나란히 3위였고요.",
         "꼴찌는 뜻밖에도 '용서해 줘'였어요. 마음이 급할수록 제일 먼저 튀어나오는 말이 가장 덜 통한 거예요.")
TABLE = ('<table style="width:100%;border-collapse:collapse"><tbody>'
         '<tr><td style="padding:10px;border:1px solid #d0d0d0;text-align:center"><b>먼저 사과할 신호</b></td><td style="padding:10px;border:1px solid #d0d0d0;text-align:center"><b>기다려도 될 신호</b></td></tr>'
         + "".join(f'<tr><td style="padding:10px;border:1px solid #d0d0d0">{a}</td><td style="padding:10px;border:1px solid #d0d0d0">{b}</td></tr>' for a, b in [
             ("내가 한 말이나 행동이 분명히 있어요", "무엇이 잘못인지 서로 다르게 기억해요"),
             ("하루가 지나도 그 장면이 떠올라 미안해요", "사과하면 내 서운함이 묻힐 것 같아요"),
             ("상대가 할 말을 다 했어요", "상대가 아직 화가 올라 있어요"),
             ("다음에 바꿀 행동이 떠올라요", "'그냥 빨리 끝내고 싶어서'가 이유의 전부예요")])
         + '</tbody></table>' + BL)
sec3 = P("<b>내 잘못이 분명하면 먼저 하고, 잘못이 반반이면 내 몫만큼만 사과하면 돼요.</b>",
         "왼쪽 칸에 둘 이상 걸리면 오늘 보내도 괜찮아요. 오른쪽 칸이 더 많다면 아직 사과할 때가 아니에요.") + TABLE + \
       P("오른쪽에 걸린 날엔 사과 대신 '이 얘기 내일 다시 하고 싶어' 한 줄로 시간을 버는 게 나아요.")
sec4 = P("<b>사주에서는 나를 다잡는 글자인 정관이 사과의 속도와 이어져요.</b>",
         "정관이 또렷하면 싸운 뒤에도 '내가 뭘 잘못했지'부터 따져서 사과가 빨라요. 나와 같은 글자인 비견·겁재가 많으면 '나도 할 말 있어'가 먼저 올라와서 사과가 늦고요.") + "[[C]]" + \
       P("🔎 1995년 8월 3일 오전 10시생은 乙亥·癸未·丙寅·癸巳예요. 병(丙) 일간에게 정관인 癸가 두 자리나 있어서, 싸움이 식기도 전에 사과문부터 쓰는 사람이에요.",
         "1996년 9월 27일 낮 12시생은 丙子·丁酉·丁卯·丙午로, 정(丁) 일간 둘레가 같은 불 글자로 꽉 차 있어요. 사과는 느리지만 한 번 하면 속엣말까지 다 꺼내요.",
         "누가 맞고 틀린 건 없어요. 빠른 사람은 책임 한 줄 뒤에 내 서운함 한 줄을 붙이고, 느린 사람은 '용서해 줘' 대신 책임 한 줄부터 꺼내면 돼요.") + MID
sec5 = P("<b>책임 한 줄, 바로잡을 약속 한 줄, 그리고 내 서운함 한 줄이면 충분해요.</b>") + "[[H]]" + \
       P("'어제 약속 시간 말없이 바꾼 거, 내가 잘못했어. 다음엔 바뀌면 바로 말할게.' 여기까지가 상대를 위한 두 줄이에요.",
         "마지막 한 줄은 나를 위한 거예요. '근데 나도 그날 기다리면서 좀 서운했어.' 사과를 다 하고 나서 꺼내면 같은 말도 따지는 말로 들리지 않아요.",
         "오늘 밤 보낼 카톡이 있다면 '용서해 줘'는 지우고, 그 자리에 '내가 이걸 잘못했어'를 넣어 보세요.")
sec6 = P("<b>Q. 먼저 사과하면 지는 건가요?</b>",
         "A. 아니에요. 누가 먼저 했느냐보다 무엇을 인정했느냐가 오래 남아요.") + \
       P("<b>Q. 상대가 사과를 안 받아 주면 어떡하죠?</b>",
         "A. 답을 조르는 카톡을 한 번 더 보내기보다, 하루쯤 두고 약속한 행동을 먼저 보여 주는 게 더 빨라요.")
tail = P("싸우면 여러분은 먼저 사과하는 쪽인가요, 기다리는 쪽인가요?", "댓글에 '먼저'나 '기다림' 한 마디만 남겨 주세요.") + \
       '<p><b>👇 첫눈에 끌리는 사주와 천천히 끌리는 사주가 궁금하다면, 첫눈에 반하는 이유, 끌림이 빠른 사주와 느린 사주 신호 4가지</b></p>'
secs = [sec1, sec2, sec3, sec4, sec5, sec6]

def _have(n): return os.path.exists(os.path.join(HERE, "img", n))
def build():
    for d_ in ("wide", "m1280", "master"): os.makedirs(os.path.join(HERE, "img", d_), exist_ok=True)
    c = V.Ctx(PAL); made = []
    a4 = f"wide/naver_z{KEY}_a1.jpg"   # 표지 항목은 한글만(한자는 글꼴에 없어 네모, 11/18 n96 a4)
    if not _have(a4):
        V.render(PID + "_new", {"d": "N", "el": "불", "kick": "사과하는 법", "hook": ["먼저 사과했는데", "왜 더 서운할까"], "sub": "755명 실험과 사주 정관",
                                "items": ["책임", "약속", "정관"]}, os.path.join(HERE, "img", a4), PAL)
    made.append(a4)
    nm = {"L": f"naver_z{KEY}_l1.jpg", "C": f"naver_z{KEY}_t1.jpg", "H": f"naver_z{KEY}_c1.jpg"}
    if not _have(nm["L"]):
        DGB.ladder(nm["L"], c, "잘 받아들여지는 사과 순위", [("1위", "책임 인정: '내가 이걸 잘못했어'"), ("2위", "바로잡을 약속: '다음엔 바로 말할게'"),
                                                      ("공동 3위", "미안한 마음 · 잘못 설명 · 다시 안 하겠다는 다짐"), ("꼴찌", "용서 요청: '용서해 줘'")],
                   note="두 실험 755명 · 여러 가지를 담을수록 잘 받아들여져요")
    if not _have(nm["C"]):
        DGC.compare(nm["C"], c, "사과가 빠른 사주, 느린 사주", ("빠른 사람", "느린 사람"),
                    [("예시", "1995.8.3 오전 10시", "1996.9.27 낮 12시"), ("일간", "병 일간", "정 일간"),
                     ("눈에 띄는 글자", "정관 계수가 두 자리", "같은 불 글자가 세 자리"), ("싸운 뒤", "'내가 뭘 잘못했지'", "'나도 할 말 있어'"),
                     ("붙일 한 줄", "내 서운함 한 줄", "책임 한 줄부터")],
                    "만세력 계산값 · 정관은 나를 다잡는 글자, 비견·겁재는 나와 같은 글자", hi=0)
    if not _have(nm["H"]):
        DGB.chat(nm["H"], c, "사과 세 줄로 보내 보기", [("me", "어제 약속 시간 말없이 바꾼 거, 내가 잘못했어"), ("me", "다음엔 바뀌면 바로 말할게"),
                                                  ("you", "알았어, 말해 줘서 고마워"), ("me", "근데 나도 그날 기다리면서 좀 서운했어")],
                 note="책임 → 약속 → 내 마음 순서예요")
    import fullbleed as FBL
    plan_p = os.path.join(HERE, "fullbleed_plan.json"); plan = json.load(open(plan_p, encoding="utf-8")) if os.path.exists(plan_p) else {}
    rows = []
    for pos, k in enumerate("LCH", 1):
        f = nm[k][:-4] + "f.jpg"
        if not _have(f):
            r, why = FBL.convert(nm[k], [os.path.join(HERE, "img"), os.path.join(HERE, "img", "m1280")])
            if not r: print("fullbleed 건너뜀", nm[k], why); made.append(nm[k]); continue
        rows.append({"pos": pos, "old": nm[k], "new": f}); made.append(nm[k]); nm[k] = f
        reg_ = json.load(open(DG.REG, encoding="utf-8")); reg_[f] = reg_[rows[-1]["old"]]; json.dump(dict(sorted(reg_.items())), open(DG.REG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    plan[PID] = rows; json.dump(plan, open(plan_p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    made += [v for v in nm.values() if v not in made]
    alt = {"L": "잘 받아들여지는 사과 순위 그림. 1위 책임 인정, 2위 바로잡을 약속, 공동 3위 미안한 마음·잘못 설명·다짐, 꼴찌 용서 요청이에요",
           "C": "사과가 빠른 사주와 느린 사주 비교 표. 1995년 8월 3일생은 정관이 두 자리, 1996년 9월 27일생은 같은 불 글자가 세 자리예요",
           "H": "말풍선 그림. 내가 잘못했어, 다음엔 바로 말할게, 근데 나도 서운했어 순서로 보낸 사과 카톡이에요"}
    body = P(*head)   # 목차 줄은 넣지 않는다(n107 과 같게, 분량 1,900~2,200자)
    for i, (q, s) in enumerate(zip(toc_q, secs)):
        for k in "LCH": s = s.replace(f"[[{k}]]", IMG(nm[k], alt[k]))
        body += H(f"{i + 1}. {q}") + s
    body += tail + CTA
    import copy_rules as CR
    for w in ("재미로", "상담", "—", "안녕하세요, 자오선의 정월이에요", "결론부터", "핵심부터", "생년월일만 넣으면 1초", "한 줄 요약", "이 글의 순서", "수비학",
              "공통점", "몇 개나", "겹칠까", "세 풀이", "여섯 운명학", "논어", "표현 억제", "천칭자리", "물고기자리", "을목", "기토", "평화주의자",
              "총정리", "기운", "흐름", "편이에요", "상대 쪽", "📚", "해 볼 것", "가상", "예시 장면") + tuple(CR.금지어):
        assert w not in re.sub(r"<[^>]+>", " ", body), w
    for f in made:   # 사이트 사본(K-069)
        dst = os.path.join(SITE, "public", "naver", "img", f); os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy(os.path.join(HERE, "img", f), dst)
    return body, a4, made

TITLE = "사과하는 법, 먼저 사과해도 서운한 이유와 755명 실험"
TAGS = ["사과하는법", "먼저사과", "먼저사과하는사람", "화해하는법", "연인싸움", "사과", "연애심리", "정관", "싸운뒤연락", "자오선"]
REL = {"id": "n91", "title": "첫눈에 반하는 이유, 끌림이 빠른 사주와 느린 사주 신호 4가지",
       "phrase": "첫눈에 끌리는 사주와 천천히 끌리는 사주가 궁금하다면, 첫눈에 반하는 이유, 끌림이 빠른 사주와 느린 사주 신호 4가지",
       "url": "https://blog.naver.com/zaoseon/224480158127"}
KW_VOL = (json.load(open(os.path.join(SITE, "data", "keywords", "kw_volume.json"), encoding="utf-8"))["posts"].get(PID) or {}).get("씨앗") or {}
assert KW_VOL.get("사과하는법", 0) >= 100, KW_VOL
INTENT = {"keywords": ["사과하는법", "화해하는법", "먼저사과", "연인싸움"],
          "keyword_src": "kw-volume n106 씨앗(사과하는법 310·화해하는법 45·연인싸움 25·먼저사과하는사람 15·먼저사과 10, 11/21 19:54)",
          "intent": "방법을 알고 싶다", "intent_note": "싸운 뒤 어떻게 사과해야 받아들여지는지, 먼저 사과했는데 서운한 까닭, 먼저 할 때와 기다릴 때, 보낼 문장",
          "first3": "싸우고 이틀째, 카톡 창에 '미안해'를 썼다 지웠다 하다가 결국 또 내가 먼저 보내요. 사과하는 법의 핵심은 '미안해' 한 마디가 아니라 '내가 이걸 잘못했어'를 먼저 말하는 거예요.",
          "answer_keys": ["책임 인정 1위·바로잡을 약속 2위·용서 요청 꼴찌(755명)", "잘못이 반반이면 내 몫만", "정관이 또렷하면 사과가 빠름", "책임·약속·내 서운함 세 줄"],
          "community_q": [], "order": toc_q, "images": ["사과 여섯 요소 순위(ladder)", "사과가 빠른·느린 사주 비교(compare)", "사과 세 줄 카톡(chat)"],
          "related": "n91", "cta": PID, "experience": [], "applied": True}

if __name__ == "__main__":
    body, a4, made = build()
    reg = json.load(open(MP.REG, encoding="utf-8"))
    assert PID not in reg or not reg[PID].get("done"), "이미 예약 끝난 글"
    reg[PID] = dict(dt="2027-02-13T08:00:00", dt_tbd="CT가 정함(재발행 일정 'n19 다시 쓰기' 11/28 자리, 진행표 11/18). 이 날짜는 자리값", title=TITLE, tags=TAGS, body=body,
                    cover=a4, related=REL, thumbs=None, cid=None, clips=None, category="관계 읽기", done=False, kw_vol=KW_VOL,
                    k131="n106 11/22(K-151 새 글, n19 다시 쓰기)", source="build_naver_106.py (n19 → n106 새 글)")
    json.dump(reg, open(MP.REG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    ic = json.load(open(os.path.join(HERE, "intent_cards.json"), encoding="utf-8")); ic["cards"][PID] = INTENT
    json.dump(ic, open(os.path.join(HERE, "intent_cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    v = reg[PID]
    MP.write_page(PID, D.datetime.fromisoformat(v["dt"]), v["title"], v["tags"], v["body"], None, v["cover"], v["related"], v["category"])
    MP.write_index()
    import k151_check as K
    print(PID, len(TITLE), "자 제목 · 본문 글자", len(re.sub(r"<[^>]+>|&nbsp;", "", body)), "· 사진", made, "· K 검사", K.check(PID, v))
