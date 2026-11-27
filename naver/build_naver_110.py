"""네이버 n110: 압박감에 강한 사람 새 글 (CT 11/4 재발행 일정 '새 글로 다시 쓰기' n24 → n110, 진행표 docs/네이버_누락글_진행표_2026-11-18.md 열일곱째 줄, 일정표 11/30 08:00 자리).
- 왜: 노출 안 되는 옛 글 n24(압박이 오면 오히려 강해지는 사람, 위기에 강한 마음)를 새 글로. n24는 건드리지 않는다(K-147·K-178).
- 검색어: n110 씨앗(멘탈강한사람·스트레스에강한사람·위기에강한사람·압박감·회복탄력성) 11/27 12:0x 요청, kw-volume 결과로 kw_vol 채움.
- 새 원칙(CLAUDE.md 0~1-3): 첫 줄은 장면, 정의는 첫 200자 안, 면책·출처 줄·설문지 코너·이모지 머리·목차 줄 없음, 링크는 말 속 낱말에.
- 다르게 쓴 것(K-151): n24의 한 줄 요약·세 풀이(경금·임수·양자리·사수자리·수비학 1·5)·'나는 몇 개나 겹칠까'·여키스-도슨·스틸(2007) 대신
  브룩스 2014 실험(Alison Wood Brooks, Journal of Experimental Psychology: General 143(3) 1144-1158, APA 공개 PDF 원문 확인:
  1실험 대학생 113명 노래방 정확도 '설렌다' 80.52% · 아무 말 안 함 69.27% · '불안하다' 52.98% / 2실험 140명 발표, '설렌다'가 '침착하다'보다 더 설득력·자신감 있게 평가),
  사주 = 편관(나를 몰아붙이는 글자)과 식신(손으로 다듬는 글자), 예시 둘(1995.3.9 오후 2시 己 일간 乙 편관·辛 식신 / 1995.9.15 밤 8시 己 일간 乙 편관 두 자리·甲 정관, 천간 식신 없음, engine assert).
  그림 compare(실험)·compare(사주)·checklist. 표 1개(순간 | 몸이 보내는 신호 | 이렇게 말해요). 연결글 → n45(노출 '예').
- 날짜: CT가 정한다. pages.json dt 는 자리값, dt_tbd 로 표시.
사용: SITE=<zaoseon-site> python3 naver/build_naver_110.py"""
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
       '<tr><td style="padding:12px 10px;text-align:center;border:1px solid #d0d0d0"><b>내 여덟 글자에 편관과 식신이 있는지 궁금하다면</b></td></tr>'
       '<tr><td style="padding:12px 10px;text-align:center;border:1px solid #d0d0d0"><span style="color:#9a9a9a">[ 1995 . 03 . 09 ]</span></td></tr>'
       '<tr><td style="padding:12px 10px;text-align:center;border:1px solid #d0d0d0"><b><a href="https://zaoseon.com/?utm_source=naver&amp;utm_medium=mid#free">내 태어난 날 글자 보기 →</a></b></td></tr>'
       '</tbody></table>' + BL)
CTA = ('<p><a href="https://zaoseon.com/?utm_source=naver&utm_medium=cta#free"><img src="' + RAW +
       'naver_cta5_1%EC%B4%88%EB%AC%B4%EB%A3%8C%ED%92%80%EC%9D%B4.jpg" alt="자오선 무료 1초 풀이 안내 배너"></a></p>')
PID, KEY, PAL = "n110", "110", "y_black_d"   # 예시 일간 己 = 흙 판 묶음(EL_SET 흙, y_gray_s 는 compare 칠한 칸 글자와 바탕이 같은 색이라 안 씀). n109 p_purple_s · n108 k_neon_s · n107 p_red_s · n101 y_black_s 와 다른 판

# ───────── 계산값과 검산
import datetime as D
sys.path.insert(0, os.path.join(SITE, "engine"))
import engine as E
A = E.compute_saju(D.datetime(1995, 3, 9, 14))["팔자"]
assert A == {"년주": "乙亥", "월주": "己卯", "일주": "己亥", "시주": "辛未"}, A
assert [E.ten_god("己", A[k][0]) for k in ("년주", "월주", "시주")] == ["편관", "비견", "식신"]
assert E.compute_saju(D.datetime(1995, 3, 9, 14, 50))["팔자"] == A                 # 같은 未시 안
B = E.compute_saju(D.datetime(1995, 9, 15, 20))["팔자"]
assert B == {"년주": "乙亥", "월주": "乙酉", "일주": "己酉", "시주": "甲戌"}, B
assert [E.ten_god("己", B[k][0]) for k in ("년주", "월주", "시주")] == ["편관", "편관", "정관"]
assert E.compute_saju(D.datetime(1995, 9, 15, 20, 50))["팔자"] == B                # 같은 戌시 안
assert E.ten_god("辛", "乙") == "편재" and E.ten_god("己", "辛") == "식신"            # 辛(쇠)이 乙(나무)을 자른다 = 식신이 편관을 다듬는 자리
# 실험값(논문 원문): 1실험 113명 · 설렌다 80.52 · 말 없음 69.27 · 불안하다 52.98 / 2실험 140명
print("예시 A 己亥 일간 · 乙 편관·辛 식신 / 예시 B 己酉 일간 · 乙 편관 두 자리·甲 정관 · 80.52/52.98 확인")

# ───────── 본문 (n24 문장을 옮기지 않았다)
PDF = "https://www.apa.org/pubs/journals/releases/xge-a0035325.pdf"      # Brooks 2014 원문 PDF(APA)
PR = "https://www.apa.org/news/press/releases/2013/12/performance-anxiety"   # APA 보도자료(같은 실험)
N58 = "https://blog.naver.com/zaoseon/224468727235"   # 십성 뜻 한눈에(노출 '예')
head = ["<b>발표 5분 전, 손끝은 차갑고 심장 소리가 귀까지 올라와요. 속으로 '진정하자, 진정하자'를 몇 번째 외우는 중이죠.</b>",
        "그런데 진정하려 할수록 더 떨려요. 압박감에 강한 사람은 덜 떨리는 사람이 아니에요. 똑같이 뛰는 심장을 '이제 시작이구나' 하는 신호로 읽는 사람이에요.",
        "노래방 기계로 잰 실험에서는 부르기 직전 한마디만 바꿨는데, 정확도가 53%에서 80%로 갈렸어요."]
toc_q = ["압박감에 왜 몸부터 떨릴까요?", "'진정하자'와 '설렌다', 어느 쪽이 나을까요?", "순간마다 뭐라고 말하면 될까요?",
         "사주로 보면 압박에 강한 사람은 누구일까요?", "다음 압박이 오면 무엇부터 할까요?", "자주 묻는 질문"]
sec1 = P("<b>몸이 중요한 순간을 앞두고 힘을 끌어올리는 중이라서요.</b>",
         "심장이 빨라지고 손에 땀이 나는 건 고장이 아니에요. 피를 빨리 돌려서 바로 움직일 수 있게 준비하는 거예요.",
         "재밌는 건 설렐 때도 몸은 거의 똑같이 반응한다는 거예요. 첫 데이트 직전에도 심장은 뛰잖아요. 다른 건 그걸 뭐라고 부르느냐예요.")
sec2 = P("<b>'설렌다' 쪽이에요. 이미 뛰는 심장을 멈추게 하는 것보다, 뛰는 김에 쓰는 게 쉽거든요.</b>",
         f"하버드 경영대학원의 브룩스 교수는 대학생 113명에게 노래방 게임으로 노래를 부르게 했어요. 부르기 직전 한 그룹은 '나 불안해', 한 그룹은 '<a href=\"{PDF}\">나 설레</a>'라고 소리 내어 말하게 했고, 한 그룹은 아무 말도 안 했고요.") + "[[S]]" + \
       P("게임 기계가 매긴 노래 정확도는 '설렌다'고 말한 쪽이 평균 80%, 아무 말 안 한 쪽이 69%, '불안하다'고 말한 쪽이 53%였어요. 한마디가 30점 가까운 차이를 만든 거예요.",
         f"같은 연구에서 140명에게 남 앞에서 발표를 시켰을 때도, '나 설레'라고 말하고 시작한 사람이 '나 침착해'라고 말한 사람보다 <a href=\"{PR}\">더 설득력 있고 자신 있게</a> 보였다는 평가를 받았어요.")
TD = 'style="padding:10px;border:1px solid #d0d0d0'
TABLE = ('<table style="width:100%;border-collapse:collapse"><tbody>'
         f'<tr><td {TD};text-align:center"><b>순간</b></td><td {TD};text-align:center"><b>몸이 보내는 신호</b></td><td {TD};text-align:center"><b>이렇게 말해요</b></td></tr>'
         + "".join(f'<tr><td {TD}">{a}</td><td {TD}">{b}</td><td {TD}">{c}</td></tr>' for a, b, c in [
             ("발표 직전", "심장이 빨라져요", "'설렌다, 이제 내 차례다'"),
             ("면접 대기실", "손에 땀이 나요", "'몸이 준비하는 중이네'"),
             ("마감 전날 밤", "잠이 안 와요", "'오늘 밤 한 장만 끝내자'"),
             ("어려운 통화 전", "목소리가 떨려요", "'첫 문장만 말하면 된다'")])
         + '</tbody></table>' + BL)
sec3 = P("<b>몸 신호를 부정하지 말고, 이름만 바꿔 불러 주세요.</b>") + TABLE + \
       P("속으로만 말고 작게라도 소리 내어 말해 주세요. 실험에서도 입 밖으로 말하게 했거든요.",
         "'괜찮아, 안 떨려'처럼 몸과 반대되는 말은 잘 안 먹혀요. 몸은 이미 뛰고 있으니까요. 떨리는 건 인정하고, 그 떨림이 어디로 갈지만 정해 주는 거예요.")
sec4 = P(f"<b>사주에서는 나를 몰아붙이는 글자를 <a href=\"{N58}\">편관</a>이라고 하는데, 이걸 손으로 다듬는 식신이 같이 있으면 압박이 일이 돼요.</b>",
         "마감, 시험, 윗사람 눈치처럼 등을 떠미는 힘이 편관이에요. 식신은 손을 움직여 뭔가를 만들어 내는 글자고요. 둘이 같이 있으면 압박이 왔을 때 걱정보다 손이 먼저 나가요.") + "[[C]]" + \
       P("🔎 1995년 3월 9일 오후 2시생은 乙亥·己卯·己亥·辛未예요. 기(己) 일간 기준으로 해 자리엔 편관 乙, 시 자리엔 식신 辛이 보여요. 辛이 乙을 자르는 모양이라, 마감이 몰려도 '일단 하나 끝내자'로 바뀌기 쉬워요.",
         "1995년 9월 15일 밤 8시생은 乙亥·乙酉·己酉·甲戌로, 같은 기(己) 일간인데 편관 乙이 두 자리, 정관 甲까지 겉으로 나와 있어요. 다듬어 줄 식신은 겉에 없고요. 압박이 한꺼번에 몰리면 손보다 몸이 먼저 굳기 쉬워요.",
         "그래서 두 번째 사람일수록 위에서 말한 한마디가 더 쓸모 있어요. 다듬는 글자가 겉에 없으면, 말로 그 자리를 채워 주면 되니까요.") + MID
sec5 = P("<b>떨림이 오는 순간, 세 가지만 순서대로 해 보세요.</b>") + "[[K]]" + \
       P("처음엔 어색해요. 그래도 '설렌다'로 시작한 날이 쌓이면, 다음엔 심장이 뛰는 순간 그 말이 먼저 떠올라요.",
         "압박감에 강한 사람은 그렇게 만들어지는 거예요. 타고난 글자가 어떻든, 떨림에 붙이는 이름은 오늘부터 내가 고를 수 있어요.")
sec6 = P("<b>Q. 떨림이 너무 심할 때도 효과가 있어요?</b>",
         "A. 말 한마디로 떨림이 없어지지는 않아요. 숨을 길게 내쉬며 어깨를 한 번 내리고, 그다음에 말해 보세요.") + \
       P("<b>Q. '진정해'라는 말은 왜 잘 안 통해요?</b>",
         "A. 이미 빨라진 심장한테 당장 멈추라는 말이라서요. 몸과 말이 엇갈리면 '나 왜 이렇게 떨지' 하는 생각만 커져요.")
tail = P("여러분은 떨릴 때 속으로 뭐라고 말하는 편인가요? '진정하자' 쪽인가요, '해 보자' 쪽인가요?", "댓글에 그 한마디만 남겨 주세요.") + \
       '<p><b>👇 압박이 끝나고 나서 무기력이 몰려온다면, 무기력, 퇴근 후 아무것도 하기 싫은 이유와 방전 3가지</b></p>'
secs = [sec1, sec2, sec3, sec4, sec5, sec6]

def _have(n): return os.path.exists(os.path.join(HERE, "img", n))
def build():
    for d_ in ("wide", "m1280", "master"): os.makedirs(os.path.join(HERE, "img", d_), exist_ok=True)
    c = V.Ctx(PAL); made = []
    a4 = f"wide/naver_z{KEY}_a1.jpg"   # 표지 항목은 한글만(한자는 글꼴에 없어 네모)
    if not _have(a4):
        V.render(PID + "_new", {"d": "N", "el": "흙", "kick": "압박감에 강한 사람", "hook": ["떨릴 때", "'설렌다' 한마디"], "sub": "노래방 실험과 사주 편관",
                                "items": ["80%·53%", "113명", "편관·식신"]}, os.path.join(HERE, "img", a4), PAL)
    made.append(a4)
    nm = {"S": f"naver_z{KEY}_t1.jpg", "C": f"naver_z{KEY}_t2.jpg", "K": f"naver_z{KEY}_k1.jpg"}
    if not _have(nm["S"]):
        DGC.compare(nm["S"], c, "부르기 직전 한마디만 바꿨을 때", ("'나 불안해'", "'나 설레'"),
                    [("누가", "대학생 113명 중", "대학생 113명 중"), ("한 일", "노래방 게임", "노래방 게임"),
                     ("정확도 평균", "53%", "80%"), ("아무 말 안 한 쪽", "69%", "69%")],
                    "브룩스 2014 실험 · 한마디로 30점 가까이", hi=1)
    if not _have(nm["C"]):
        DGC.compare(nm["C"], c, "압박이 일이 되는 사주, 몸이 굳는 사주", ("일이 되는 사람", "몸이 굳는 사람"),
                    [("예시", "1995.3.9 오후 2시", "1995.9.15 밤 8시"), ("일간", "기 일간", "기 일간"),
                     ("몰아붙이는 글자", "편관 을목 하나", "편관 을목 둘 + 정관"), ("다듬는 글자", "식신 신금 있음", "겉에 없음"),
                     ("압박이 오면", "손이 먼저 나가요", "몸이 먼저 굳어요")],
                    "만세력 계산값 · 편관은 나를 몰아붙이는 글자, 식신은 손으로 다듬는 글자", hi=0)
    if not _have(nm["K"]):
        DGB.checklist(nm["K"], c, "떨림이 올 때, 순서대로 세 가지", [("숨 길게 한 번", "내쉬면서 어깨 내리기"),
                                                       ("'나 설레' 소리 내기", "작게라도 입 밖으로"),
                                                       ("첫 동작 하나만", "첫 문장, 첫 줄, 첫 장")], note="떨림은 그대로, 이름만 바꿔요")
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
    alt = {"S": "노래방 실험 비교 표. 부르기 전에 '나 불안해'라고 말한 쪽은 정확도 53%, '나 설레'라고 말한 쪽은 80%였어요",
           "C": "압박이 일이 되는 사주와 몸이 굳는 사주 비교 표. 1995년 3월 9일생은 편관과 식신이 같이 있고, 1995년 9월 15일생은 편관이 두 자리예요",
           "K": "떨림이 올 때 할 세 가지 칸. 숨 길게 한 번, '나 설레' 소리 내기, 첫 동작 하나만이에요"}
    body = P(*head)   # 목차 줄은 넣지 않는다(n106~n109 와 같게)
    for i, (q, s) in enumerate(zip(toc_q, secs)):
        for k in "SCK": s = s.replace(f"[[{k}]]", IMG(nm[k], alt[k]))
        body += H(f"{i + 1}. {q}") + s
    body += tail + CTA
    import copy_rules as CR
    for w in ("재미로", "상담", "—", "안녕하세요, 자오선의 정월이에요", "결론부터", "핵심부터", "생년월일만 넣으면 1초", "한 줄 요약", "이 글의 순서", "수비학",
              "공통점", "몇 개나", "겹칠까", "세 풀이", "경금", "임수", "양자리", "사수자리", "여키스", "지연 행동", "연료",
              "총정리", "기운", "흐름", "편이에요", "상대 쪽", "📚", "해 볼 것", "가상", "예시 장면", "반드시", "무조건") + tuple(CR.금지어):
        assert w not in re.sub(r"<[^>]+>", " ", body), w
    for f in made:   # 사이트 사본(K-069)
        dst = os.path.join(SITE, "public", "naver", "img", f); os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy(os.path.join(HERE, "img", f), dst)
    return body, a4, made

TITLE = "압박감에 강한 이유, 떨릴 때 한마디로 갈린 80% 대 53%"
TAGS = ["압박감", "멘탈강한사람", "스트레스에강한사람", "위기에강한사람", "발표긴장", "면접긴장", "편관", "식신", "십성", "자오선"]
REL = {"id": "n45", "title": "무기력, 퇴근 후 아무것도 하기 싫은 이유와 방전 3가지",
       "phrase": "압박이 끝나고 나서 무기력이 몰려온다면, 무기력, 퇴근 후 아무것도 하기 싫은 이유와 방전 3가지",
       "url": "https://blog.naver.com/zaoseon/224474813836"}
KW_VOL = (json.load(open(os.path.join(SITE, "data", "keywords", "kw_volume.json"), encoding="utf-8"))["posts"].get(PID) or {}).get("씨앗") or {}
INTENT = {"keywords": ["압박감", "멘탈강한사람", "스트레스에강한사람", "위기에강한사람"],
          "keyword_src": "n110 씨앗 요청(11/27 12:0x) · kw-volume 결과로 채움",
          "intent": "방법을 알고 싶다", "intent_note": "압박이 오면 왜 떨리는지, 떨릴 때 뭐라고 하면 나은지, 사주로 압박에 강한 사람, 다음에 할 일",
          "first3": "발표 5분 전, 손끝은 차갑고 심장 소리가 귀까지 올라와요. 압박감에 강한 사람은 똑같이 뛰는 심장을 '이제 시작이구나' 하는 신호로 읽는 사람이에요.",
          "answer_keys": ["떨림은 몸이 힘을 끌어올리는 준비, 설렘과 몸 신호가 같음", "'나 설레' 80% · 말 없음 69% · '나 불안해' 53%(113명)", "순간별 한마디 표", "편관 + 식신이면 압박이 일이 됨"],
          "community_q": [], "order": toc_q, "images": ["노래방 실험 불안 대 설렘(compare)", "편관·식신 사주 비교(compare)", "떨릴 때 세 가지(checklist)"],
          "related": "n45", "cta": PID, "experience": [], "applied": True}

if __name__ == "__main__":
    body, a4, made = build()
    reg = json.load(open(MP.REG, encoding="utf-8"))
    assert PID not in reg or not reg[PID].get("done"), "이미 예약 끝난 글"
    reg[PID] = dict(dt="2027-02-16T08:00:00", dt_tbd="CT가 정함(재발행 일정 'n24 다시 쓰기' 11/30 08:00 자리, 진행표 11/18). 이 날짜는 자리값", title=TITLE, tags=TAGS, body=body,
                    cover=a4, related=REL, thumbs=None, cid=None, clips=None, category="마음 읽기", done=False, kw_vol=KW_VOL,
                    k131="n110 11/27(K-151 새 글, n24 다시 쓰기)", source="build_naver_110.py (n24 → n110 새 글)")
    json.dump(reg, open(MP.REG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    ic = json.load(open(os.path.join(HERE, "intent_cards.json"), encoding="utf-8")); ic["cards"][PID] = INTENT
    json.dump(ic, open(os.path.join(HERE, "intent_cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    v = reg[PID]
    MP.write_page(PID, D.datetime.fromisoformat(v["dt"]), v["title"], v["tags"], v["body"], None, v["cover"], v["related"], v["category"])
    MP.write_index()
    import k151_check as K
    print(PID, len(TITLE), "자 제목 · 본문 글자", len(re.sub(r"<[^>]+>|&nbsp;", "", body)), "· 사진", made, "· K 검사", K.check(PID, v))
