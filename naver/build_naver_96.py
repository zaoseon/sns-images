"""네이버 n96: 헤어진 사람이 다시 생각나는 이유(재회) 새 글 (CT 11/4 19:40 재발행 일정 '새 글로 다시 쓰기' n17 → n96, 진행표 docs/네이버_누락글_진행표_2026-11-18.md 셋째 줄).
- 왜: 노출 안 되는 옛 글 n17(헤어진 뒤 다시 연락하는 사람의 공통점, 사주·별자리·숫자로 읽는 이별 후 마음)을 새 글로. n17은 건드리지 않는다(K-147·K-178).
- 주제 근거: 커뮤니티 수집 11/18(data/kcos_community/zaoseon/2026-11-18.json) '재회 가능성 사주' 관련 제목 30/87, 지식iN 17건 — 이번 묶음에서 실제 질문이 가장 많음(topic_bank 11/18 3번).
- 검색어: 월 검색량 아직 없음 → tools/seo/kw_volume_request.json 에 n96 묶음(재회·재회운·헤어진연인연락·이별후연락·재회가능성) 요청(11/18 ①). 결과가 오면 KW_VOL 이 채워진다.
- 다르게 쓴 것(K-151): n17의 인사·'한 줄로 먼저'·한 줄 요약·丁/癸 일간·물 별자리·수비학 2·6·'몇 개 겹칠까'·오르페우스·여섯 운명학·흰곰 효과·24시간 기다리기 대신
  연인 자리 = 일지(배우자 자리), 2027 丁未의 未와 일지 관계(午 육합 · 亥·卯 반합 · 丑 충 · 子 원진 · 戌 형, ny_facts.ji_rel assert),
  2026년 12월 子월(대설 12/7 11:52부터)과의 관계, 예시 1995년 3월 16일 오전 9시생(乙亥·己卯·丙午·癸巳).
  심리 = 관계 되돌림(relationship churning, Halpern-Meekin 외 2013 — 17~24세 792명 중 약 45%가 헤어졌다 다시 만남). 그림 유형 fork·bignum·checklist. 연결글 → n83.
- 출처 2개(K-162, 11/18 PMC 원문 확인): Halpern-Meekin, Manning, Giordano & Longmore (2013) Journal of Adolescent Research 28(2) 166–188, DOI 10.1177/0743558412464524
  (TARS 4차 2006년 면접, 17~24세 데이트·동거 중 792명, 본문 'approximately 45 percent ... experience a relationship reconciliation') · 한국천문연구원 음양력 변환(절기 시각).
- 날짜: CT가 정한다. pages.json dt 는 자리값, dt_tbd 로 표시. 콘텐츠 계획 12/8 '재회운' 칸과 주제가 겹치므로 그 칸에 쓸지 CT가 정한다.
사용: SITE=<zaoseon-site> python3 naver/build_naver_96.py"""
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
       '<tr><td style="padding:12px 10px;text-align:center;border:1px solid #d0d0d0"><b>내 연인 자리(날 아래 글자)가 궁금하다면</b></td></tr>'
       '<tr><td style="padding:12px 10px;text-align:center;border:1px solid #d0d0d0"><span style="color:#9a9a9a">[ 1995 . 03 . 16 ]</span></td></tr>'
       '<tr><td style="padding:12px 10px;text-align:center;border:1px solid #d0d0d0"><b><a href="https://zaoseon.com/?utm_source=naver&amp;utm_medium=mid#free">내 태어난 날 글자 보기 →</a></b></td></tr>'
       '</tbody></table>' + BL)
CTA = ('<p><a href="https://zaoseon.com/?utm_source=naver&utm_medium=cta#free"><img src="' + RAW +
       'naver_cta5_1%EC%B4%88%EB%AC%B4%EB%A3%8C%ED%92%80%EC%9D%B4.jpg" alt="자오선 무료 1초 풀이 안내 배너"></a></p>')
PID, KEY, PAL = "n96", "96", "y_pink_s"   # 연인 자리·2027 丁(불) → 불 판 묶음(EL_SET 불). n95 y_olive_s · n94 p_purple_s · n93 y_black_d · n91 p_red_s 와 다른 판

# ───────── 계산값과 검산
import datetime as D
sys.path.insert(0, os.path.join(SITE, "engine"))
import engine as E, ny_facts as F
Y27 = E.compute_saju(D.datetime(2027, 3, 1, 12))["팔자"]["년주"]; assert Y27 == "丁未", Y27
assert E.compute_saju(D.datetime(2027, 2, 4, 9))["팔자"]["년주"] == "丙午"       # 입춘(2/4 10:46) 전은 아직 2026년 기운
REL27 = {z: F.ji_rel(z, "未") for z in F.Z}
assert REL27["午"] == ["午未 육합"] and REL27["亥"] == ["亥未 반합(木)"] and REL27["卯"] == ["卯未 반합(木)"]
assert REL27["丑"] == ["丑未 충", "丑未 형"] and REL27["子"] == ["子未 원진", "子未 해"] and REL27["戌"] == ["戌未 형"]
QUIET = [z for z in F.Z if not REL27[z]]; assert set(QUIET) == set("寅辰巳申酉未"), QUIET
REL12 = {z: F.ji_rel(z, "子") for z in "午丑未"}
assert REL12 == {"午": ["午子 충"], "丑": ["丑子 육합"], "未": ["未子 원진", "未子 해"]}, REL12
T26 = dict((n, t) for n, _, t in E.get_solar_terms_kst(2026))
assert (T26["대설"].month, T26["대설"].day, T26["대설"].hour, T26["대설"].minute) == (12, 7, 11, 52)
assert E.compute_saju(D.datetime(2026, 12, 7, 14, 0))["팔자"]["월주"] == "庚子"
X = D.datetime(1995, 3, 16, 9, 0)
PX = E.compute_saju(X)["팔자"]
assert PX == {"년주": "乙亥", "월주": "己卯", "일주": "丙午", "시주": "癸巳"}, PX
assert E.compute_saju(D.datetime(1995, 3, 16, 9, 40))["팔자"] == PX
assert F.ji_rel("午", "未") == ["午未 육합"] and F.ji_rel("午", "子") == ["午子 충"]
print("2027 丁未·일지 관계 12개·12월 子월·대설·예시 팔자 다시 확인")

# ───────── 본문 (n17 문장을 옮기지 않았다)
head = ["<b>재회운은 헤어진 사람이 다시 생각나고 다시 이어질 기회가 오는 때를 보는 풀이예요. 사주에서는 연인 자리가 움직이는 해와 달로 봐요.</b>",
        "헤어진 사람이 다시 생각나는 건 드문 일이 아니에요. 17~24세 792명을 조사한 연구에서 약 45%가 헤어졌다 다시 만난 적이 있었어요.",
        "<b>연인 자리는 태어난 날 기둥의 아래 글자, 일지예요. 2027년 정미년에는 일지가 午·亥·卯인 사람은 연인 자리가 손잡는 해, 丑인 사람은 부딪히는 해예요.</b>",
        "이 글은 내 연인 자리를 찾는 법, 2027년과 올해 12월에 움직이는 글자, 다시 연락하기 전에 볼 것까지 다뤄요."]
toc_q = ["헤어진 사람이 다시 생각나는 건 이상한 걸까요?", "사주에서 연인 자리는 어디일까요?", "2027년 재회운, 연인 자리가 움직이는 글자는?",
         "1995년 3월 16일 오전 9시생의 재회운은 어떻게 읽을까요?", "다시 연락하기 전에 무엇을 볼까요?", "자주 묻는 질문"]
sec1 = P("🧠 <b>헤어졌다 다시 만나는 일은 생각보다 흔해요. 심리학에서는 이것을 관계 되돌림이라고 불러요.</b>",
         "미국 볼링그린 주립대 연구진은 톨레도에서 자란 청년 792명을 2006년에 면접했어요. 나이는 17~24세, 지금 사귀거나 함께 사는 사람이 있는 이들이었어요.",
         "그 사람과 헤어졌다가 다시 만난 적이 있는지 물었더니, 약 45%가 그렇다고 답했어요.") + "[[B]]" + \
       P("그러니 끝난 사람이 다시 떠오르는 건 마음이 약해서가 아니에요. 함께한 시간이 길수록 생활 곳곳에 그 사람이 남아 있어서, 비슷한 장면을 만나면 기억이 먼저 올라와요.",
         "중요한 건 떠오르는 마음 자체보다, 그 마음이 올라올 때 무엇을 하느냐예요.",
         '📚 <b>출처 1</b>: <a href="https://doi.org/10.1177/0743558412464524">Halpern-Meekin, Manning, Giordano &amp; Longmore (2013), Relationship churning in emerging adulthood, Journal of Adolescent Research 28(2)</a>')
sec2 = P("<b>사주 여덟 글자 가운데 태어난 날 기둥의 아래 글자(일지)를 연인·배우자 자리로 봐요.</b>",
         "날 기둥 위 글자(일간)가 나 자신이라면, 바로 아래 글자는 내 옆에 앉는 사람의 자리예요. 그래서 일지에 무엇이 오는지, 그 해에 어떤 글자가 일지를 건드리는지를 같이 봐요.",
         "일지는 무료 풀이에 생일만 넣으면 '태어난 날' 칸 아래에서 바로 보여요. 태어난 시를 몰라도 일지는 나와요.")
sec3 = P("<b>2027년 재회운은 해의 아래 글자 未로 봐요. 내 일지가 未와 어떤 사이인지 보면 돼요.</b>",
         "🤝 <b>午·亥·卯</b>: 未와 손잡는 글자예요(午는 육합, 亥·卯는 한 팀). 연인 자리가 끌려 나오는 해라, 지난 인연이 다시 생각나거나 새 인연이 들어오기 쉽다고 봐요.",
         "⚡ <b>丑</b>: 未와 마주 보고 부딪히는 글자예요. 연인 자리가 흔들리는 해라, 미뤄 둔 관계를 정리하거나 결정하는 일이 생기기 쉬워요.",
         "🌀 <b>子·戌</b>: 子는 未와 원진, 戌은 형으로 걸려요. 큰 사건보다 작은 서운함이 오래 남는 쪽으로 봐요.") + "[[K]]" + \
       P("寅·辰·巳·申·酉·未는 2027년 해의 글자와 따로 얽히지 않아요. 연인 자리가 크게 움직이는 해는 아니라고 봐요.",
         "다만 해의 글자는 1년 내내 같은 무게로 오지 않아요. 입춘인 2027년 2월 4일 오전 10시 46분부터 정미년으로 세요.") + MID
sec4 = P("🔎 <b>1995년 3월 16일 오전 9시에 태어난 사람을 예로 들어 볼게요.</b>",
         "여덟 글자는 乙亥·己卯·丙午·癸巳예요. 날의 주인(일간)은 丙, 한낮의 해 같은 불이고, 연인 자리(일지)는 午예요.",
         "2027년 해의 글자 未는 午와 육합이에요. 이 사람에게 2027년은 연인 자리가 끌려 나오는 해예요. 헤어진 사람이 문득 떠오르거나, 연락하고 싶은 마음이 커지는 때로 볼 수 있어요.") + \
       P("그런데 올해 12월은 반대예요. 12월 7일 오전 11시 52분 대설부터 쥐(子)의 달이 시작되는데, 子는 午와 마주 보고 부딪히는 글자예요.",
         "그래서 이 사람은 12월에 마음이 먼저 흔들리고, 해가 바뀐 뒤에 그 마음을 붙잡고 싶어질 수 있어요. 12월에 보내고 싶은 연락이 있다면 한 달쯤 묵혀 두고, 그 뒤에도 같은 마음인지 보는 편이 좋아요.")
sec5 = P("<b>다시 연락할지 정하는 기준은 사주보다 헤어진 이유에 있어요.</b>",
         "연인 자리가 손잡는 해라도 헤어진 이유가 그대로면 같은 자리에서 다시 멈추기 쉬워요. 반대로 부딪히는 해라도 이유가 풀렸다면 이야기를 다시 꺼낼 수 있어요.") + \
       P("🌱 <b>마음 코치 정월의 질문</b>", "그 사람과 헤어진 이유를 한 문장으로 쓴다면<br>무엇이라고 쓰게 되나요?",
         "🔸 그 이유는 지금<br>얼마나 달라졌나요?") + "[[C]]" + \
       P("✔️ <b>다시 연락하기 전에 해 볼 것</b>",
         "1. 헤어진 이유를 한 문장으로 적고, 그 옆에 '지금도 그대로인가'를 예·아니오로 적어 보세요.",
         "2. 그 사람이 떠오른 때를 일주일 동안 적어 보세요. 늦은 밤이나 힘든 날에만 떠오른다면 그 사람보다 그날의 마음일 수 있어요.",
         "3. 보낸다면 한 가지만 담은 짧은 문장으로 보내 보세요. 사과면 사과, 안부면 안부 하나만 담아 보세요.")
sec6 = P("<b>Q. 재회운이 있는 해면 다시 만나게 되나요?</b>",
         "A. 아니에요. 다시 생각나거나 연락하고 싶은 마음이 커지는 때로 볼 뿐, 상대의 마음이나 결과를 정하지 않아요.") + \
       P("<b>Q. 내 일지가 丑이면 2027년엔 연락하지 않는 게 좋을까요?</b>",
         "A. 부딪히는 해는 관계를 정리하거나 결정하는 일이 생기기 쉬운 때예요. 연락을 막는 해가 아니라, 미뤄 둔 답을 내는 해로 보면 돼요. 마침 올해 12월은 子의 달이라 丑과 손잡는 달이에요.") + \
       P("<b>Q. 상대의 일지도 봐야 하나요?</b>",
         "A. 두 사람의 일지가 서로 손잡는지, 부딪히는지도 봐요. 띠 궁합과 같은 방식으로 읽어서, 아래 연결 글의 번호표로 먼저 확인해 볼 수 있어요.",
         '📚 <b>출처 2</b>: <a href="https://astro.kasi.re.kr/life/pageView/5">한국천문연구원 천문우주지식정보, 음양력 변환(절기 시각)</a>')
tail = P("여러분의 날 아래 글자(일지)는 무엇인가요?", "무료 풀이에서 확인하고 글자 하나만 댓글에 적어 주세요.") + \
       '<p><b>👇 두 사람의 띠 궁합을 번호로 먼저 보고 싶다면, 띠 궁합표 한눈에, 12띠 짝과 부딪히는 띠 번호로 찾는 법</b></p>'
secs = [sec1, sec2, sec3, sec4, sec5, sec6]

def _have(n): return os.path.exists(os.path.join(HERE, "img", n))
def build():
    for d_ in ("wide", "m1280", "master"): os.makedirs(os.path.join(HERE, "img", d_), exist_ok=True)
    c = V.Ctx(PAL); made = []
    a4 = f"wide/naver_z{KEY}_a5.jpg"   # a4 는 항목 칸 한자가 글꼴에 없어 네모로 나옴(11/18 눈 확인) → 한글 읽기로 a5
    if not _have(a4):
        V.render(PID + "_new", {"d": "N", "el": "불", "kick": "헤어진 사람이 생각나는 이유", "hook": ["연인 자리가", "움직이는 해"], "sub": "2027년 내 날 아래 글자로 봐요",
                                "items": ["오·해·묘", "축", "자·술"]}, os.path.join(HERE, "img", a4), PAL)
    made.append(a4)
    nm = {"K": f"naver_z{KEY}_k3.jpg", "B": f"naver_z{KEY}_n3.jpg", "C": f"naver_z{KEY}_h3.jpg"}
    if not _have(nm["K"]):
        DGB.fork(nm["K"], c, "2027년, 내 연인 자리는?", "해의 아래 글자 未", ["午·亥·卯 손잡는 해", "丑 부딪히는 해", "子·戌 서운함이 남는 해"],
                 note="연인 자리 = 태어난 날 기둥의 아래 글자(일지)")
    if not _have(nm["B"]):
        DGC.bignum(nm["B"], c, "헤어졌다 다시 만난 적 있나요", "약 45%", "17~24세 792명 가운데",
                   [("누가", "미국 톨레도 청년 792명, 2006년 면접"), ("물음", "지금 연인과 헤어졌다 다시 만난 적이 있나요"), ("결과", "절반 가까이가 그렇다고 답했어요")],
                   "Halpern-Meekin 외 (2013), Journal of Adolescent Research")
    if not _have(nm["C"]):
        DGB.checklist(nm["C"], c, "다시 연락하기 전 세 칸", [("헤어진 이유 한 문장", "지금도 그대로인가 예·아니오"),
                                                     ("떠오른 때 일주일 적기", "늦은 밤에만 떠오르나요"),
                                                     ("보낸다면 한 가지만", "사과면 사과, 안부면 안부")])
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
    alt = {"K": "2027년 연인 자리 그림. 해의 아래 글자 未에서 세 갈래, 午·亥·卯는 손잡는 해, 丑은 부딪히는 해, 子·戌은 서운함이 남는 해",
           "B": "관계 되돌림 연구 그림. 17~24세 792명 가운데 약 45%가 헤어졌다 다시 만난 적이 있다고 답했어요",
           "C": "다시 연락하기 전 세 칸 체크 그림. 헤어진 이유 한 문장, 떠오른 때 일주일 적기, 보낸다면 한 가지만"}
    body = P(*head) + P("<b>📌 헤어진 사람이 생각날 때 읽는 순서</b>", *[f"{i + 1}. {q}" for i, q in enumerate(toc_q)])
    for i, (q, s) in enumerate(zip(toc_q, secs)):
        for k in "BKC": s = s.replace(f"[[{k}]]", IMG(nm[k], alt[k]))
        body += H(f"{i + 1}. {q}") + s
    body += tail + CTA
    import copy_rules as CR
    for w in ("재미로", "상담", "—", "안녕하세요, 자오선의 정월이에요", "결론부터 말씀드릴게요", "한 줄로 먼저", "생년월일만 넣으면 1초", "한 줄 요약", "이 글의 순서", "수비학",
              "사람의 공통점", "몇 개나 겹칠까", "흰곰", "오르페우스", "여섯 운명학", "총정리", "힘 쓸 달", "아낄 달", "솜씨", "값을 매", "24시간", "내게") + tuple(CR.금지어):
        assert w not in re.sub(r"<[^>]+>", " ", body), w
    for f in made:   # 사이트 사본(K-069)
        dst = os.path.join(SITE, "public", "naver", "img", f); os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy(os.path.join(HERE, "img", f), dst)
    return body, a4, made

TITLE = "재회운 2027, 헤어진 사람이 다시 생각나는 이유와 연인 자리"
TAGS = ["재회", "재회운", "헤어진연인", "이별후연락", "헤어진사람생각", "일지", "배우자자리", "2027연애운", "관계심리", "자오선"]
REL = {"id": "n83", "title": "띠 궁합표 한눈에, 12띠 짝과 부딪히는 띠 번호로 찾는 법",
       "phrase": "두 사람의 띠 궁합을 번호로 먼저 보고 싶다면, 띠 궁합표 한눈에, 12띠 짝과 부딪히는 띠 번호로 찾는 법",
       "url": "https://blog.naver.com/zaoseon/224465980874"}
KW_VOL = (json.load(open(os.path.join(SITE, "data", "keywords", "kw_volume.json"), encoding="utf-8"))["posts"].get("n96") or {}).get("씨앗") or {}
INTENT = {"keywords": ["재회", "재회운", "헤어진연인연락"],
          "keyword_src": "커뮤니티 수집 11/18(재회 관련 제목 30/87, 지식iN 17) · n17 재발행 일정 '새 글로 다시 쓰기'(진행표 11/18 셋째 줄) · 월 검색량은 kw-volume n96 요청 중(11/18)",
          "intent": "이유를 알고 싶다", "intent_note": "헤어진 사람이 왜 다시 생각나는지, 그게 이상한 일인지 바로 알고, 내 연인 자리(일지)로 2027년·12월에 움직이는 때와 연락 전에 볼 것까지",
          "first3": "헤어진 사람이 다시 생각나고 연락하고 싶어지는 건 드문 일이 아니에요. 17~24세 792명을 조사한 연구에서 절반 가까이가 헤어졌다 다시 만난 적이 있었어요.",
          "answer_keys": ["드문 일이 아님(약 45%)", "연인 자리 = 일지", "2027 午·亥·卯 손잡음, 丑 부딪힘"],
          "community_q": ["재회가능성 알고싶습니다(카페, 11/18 수집)", "남친과 헤어졌는데 재회를 해야하는지 고민이에요(카페, 11/18 수집)"],
          "order": toc_q, "images": ["관계 되돌림 연구(bignum)", "2027 연인 자리 세 갈래(fork, 엔진 계산)", "연락 전 세 칸(checklist)"],
          "related": "n83", "cta": PID, "experience": [], "applied": True,
          "differs_from_n17": "제목(공통점 → 이유)·도입(연구 숫자 직답 + 일지)·소제목 순서·丁/癸 일간·물 별자리·수비학 2·6·'몇 개 겹칠까'·오르페우스·여섯 운명학·흰곰 효과(Wegner 1987)·24시간 기다리기 대신 일지(연인 자리)와 2027 未·12월 子월 관계(엔진 assert)·예시 1995.3.16 오전 9시(乙亥·己卯·丙午·癸巳)·관계 되돌림(Halpern-Meekin 외 2013)·그림 유형(bignum·fork·checklist)·연결글(→ n83)"}

if __name__ == "__main__":
    body, a4, made = build()
    reg = json.load(open(MP.REG, encoding="utf-8"))
    assert PID not in reg or not reg[PID].get("done"), "이미 예약 끝난 글"
    reg[PID] = dict(dt="2027-02-06T08:00:00", dt_tbd="CT가 정함(재발행 일정 'n17 다시 쓰기' 자리, 진행표 11/18 · 콘텐츠 계획 12/8 재회운 칸과 겹침). 이 날짜는 자리값", title=TITLE, tags=TAGS, body=body,
                    cover=a4, related=REL, thumbs=None, cid=None, clips=None, category="관계 읽기", done=False, kw_vol=KW_VOL,
                    k131="n96 11/18(K-151 새 글)", source="build_naver_96.py (n17 주제 새 글, n17 그대로)")
    json.dump(reg, open(MP.REG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    ic = json.load(open(os.path.join(HERE, "intent_cards.json"), encoding="utf-8")); ic["cards"][PID] = INTENT
    json.dump(ic, open(os.path.join(HERE, "intent_cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    v = reg[PID]
    MP.write_page(PID, D.datetime.fromisoformat(v["dt"]), v["title"], v["tags"], v["body"], None, v["cover"], v["related"], v["category"])
    MP.write_index()
    import k151_check as K
    print(PID, len(TITLE), "자 제목 · 본문 글자", len(re.sub(r"<[^>]+>|&nbsp;", "", body)), "· 사진", made, "· K 검사", K.check(PID, v))
