"""K-131 B3(발행 글 · 운명학 사전 7편, F4) 본문 그림 · K-135 그림 거리 · K-137 여백 없는 판 (① 자동 실행 10/19 11:45, 배치표 zaoseon-site data/naver_redraw_plan.json B3).
B2 3판(build_k131_b2v3.py, 대표 승인 10/17 19:34)과 같은 방식으로 글마다 두 장(*8.jpg):
  R(e8) = 심리학 단락 자리: 그 단락이 말한 개념의 실험·학자 카드. 앞 줄 '이 마음이 흘러가는 모양을 그려 보면 이래요.'를 그 연구를 말하는 한두 문장으로 바꾼다
  C(g8) = 그 글 본문의 계산 값·조견 값으로 그린 차트·표(지어낸 수치 없음). n15만 『주역』 계사전 책 카드
옛 틀은 글마다 2장 이하(옛 c4 '해 볼 것' 그림 뺌, n51은 b4 원소 배지 목록을 원소 네 칸 그림으로 바꿈).
본문의 다른 사진은 이미 발행 글에 들어간 여백 없는 판(fullbleed_plan.json new, n11은 K-138로 고친 5f)으로 원고 이름도 맞춘다.
K-128: 이 글들 끝의 '이 글은 재미로…' 줄을 뺀다(다시 발행할 때 같이).
새 이름만(*8.jpg·*8f.jpg). sparse 환경이라 imgkit.guard_overwrite 가 원격 파일을 못 보므로 git ls-tree 로 이름 겹침을 먼저 잰다.
사용: PREVIEW=폴더 python3 naver/build_k131_b3.py (그림만) · python3 naver/build_k131_b3.py [글 번호…] (그림 + 여백 없는 판 + pages.json)"""
import os, sys, re, json, html, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import body_v3 as B, diagrams_k131c as D3
import build_k131_b1 as B1, build_k131_b2v2 as V2, cover_v3 as CV
PAL_OVR = {"n15": "v_emerald", "n48": "v_navy", "n57": "y_gray", "n11": "y_gray"}   # 표지 판 v_royal(#0A46B3)은 K-067 쓰지 않는 파랑 → 진한 초록·네이비 판, 흰 판은 B2처럼 옅은 회색 판
PG = os.path.join(HERE, "pages.json")
TAG = "B3 10/19(K-135)"
LEAD = "<p>이 마음이 흘러가는 모양을 그려 보면 이래요.</p>"
FUN = re.compile(r"<p>이 글은 재미로, 그리고 나를 돌아보는 계기로 읽어 주세요\.</p>")


def P_(t): return "".join(f"<p>{html.escape(x, quote=False)}</p>" for x in t.split("\n"))


def plan():
    P = {}
    # n13 같은 생년월일 여섯 풀이 — 오행 막대(본문 값) + 확증 편향 질문 고르기 실험
    P["n13"] = dict(key="13",
        C=(4, lambda n, c: D3.vbar(n, c, "예시 인물의 다섯 기운", [("쇠", 3, True), ("불", 2, False), ("흙", 2, False), ("물", 1, False), ("나무", 0, True)], 3,
            "시작을 뜻하는 나무가 0이에요.|그래서 시작은 의식해서 만들어요", "출처: 자오선 계산 · 가상 예시 1990년 5월 15일 오후 2시 30분생", fmt="{:.0f}"),
           "예시 인물의 여덟 글자를 다섯 기운으로 센 막대그래프: 쇠 3, 불 2, 흙 2, 물 1, 나무 0. 시작을 뜻하는 나무가 하나도 없어요",
           "예시 인물의 여덟 글자를 다섯 기운으로 세어 보면 이래요.\n쇠가 가장 많고, 시작을 뜻하는 나무는 하나도 없어요."),
        R=(lambda n, c: D3.exp(n, c, "외향적인 사람인지 알아보세요", "스나이더·스완 · 1978",
            [("부탁", "처음 만난 사람이 '외향적인 사람인지' 알아보게 했어요"), ("방법", "준비된 질문 목록에서 물어볼 질문을 고르게 했어요"),
             ("모습", "많은 사람이 '파티를 띄우려면 뭘 하세요?'처럼 외향적이라는 답이 나오기 쉬운 질문을 골랐어요")],
            "묻는 방식이 답을 미리 정해요.|풀이도 맞는 장면만 찾기 쉬워요", "출처: Snyder & Swann (1978), J. Personality and Social Psychology"),
           "스나이더와 스완(1978) 실험 카드: 상대가 외향적인지 알아보라고 하자 많은 사람이 외향적이라는 답이 나오기 쉬운 질문만 골랐다는 실험",
           "심리학자 스나이더와 스완(1978)은 사람들에게 처음 만난 상대가 외향적인지 알아보게 했어요.\n많은 사람이 '파티를 띄우려면 뭘 하세요?'처럼 이미 짐작에 맞는 답이 나올 질문만 골랐어요."))
    # n15 육효 — 계사전 책 카드 + 소유 효과(손실 회피) 큰 숫자
    P["n15"] = dict(key="15",
        C=(1, lambda n, c: D3.book(n, c, "괘가 바뀌는 이유", "주역", "『주역』 계사전",
            "궁하면 변하고, 변하면 통하고, 통하면 오래간다", "막힌 때가 곧 바뀔 때라는 뜻이에요. 육효에서 움직이는 효(동효)가 괘를 바꾸는 것도 같은 생각이에요.",
            "출처: 『주역』 계사전 하편 2장 '궁즉변 변즉통 통즉구(窮則變 變則通 通則久)', 우리 말로 옮김"),
           "『주역』 계사전 책 카드: 궁하면 변하고, 변하면 통하고, 통하면 오래간다. 육효의 움직이는 효가 괘를 바꾸는 것도 같은 생각이라는 설명",
           "『주역』 계사전에는 '궁하면 변하고, 변하면 통하고, 통하면 오래간다'는 말이 있어요.\n육효에서 움직이는 효가 괘를 바꾸는 것도 이 생각에서 나와요."),
        R=(lambda n, c: D3.bignum(n, c, "내 손에 든 컵은 더 비싸요", "2배 넘게", "컵을 가진 쪽이 부른 값 ÷ 사려는 쪽이 부른 값",
            [("실험", "대학생 절반에게 머그컵을 나눠 주고, 가진 쪽과 없는 쪽이 값을 부르게 했어요"), ("결과", "가진 쪽은 사려는 쪽보다 두 배 넘게 높은 값을 불렀어요"),
             ("우리 글", "이미 가진 자리를 잃는 쪽이 더 무겁게 느껴져서, 이직 앞에서 손을 놓기 어려워요")],
            "출처: Kahneman, Knetsch & Thaler (1990), J. Political Economy"),
           "카너먼 연구진(1990) 머그컵 실험: 컵을 가진 쪽은 사려는 쪽보다 두 배 넘게 높은 값을 불렀다는 큰 숫자 그림",
           "카너먼 연구진(1990)은 대학생 절반에게 머그컵을 나눠 주고 사고팔게 했어요.\n컵을 가진 쪽은 사려는 쪽보다 두 배 넘게 높은 값을 불렀어요. 가진 것을 잃는 쪽을 더 무겁게 느끼는 거예요."))
    # n47 사주 보는 법 — 절기 시각 흐름(본문 값) + 자기효능감 네 가지 원천
    P["n47"] = dict(key="47",
        C=(3, lambda n, c: D3.timeline3(n, c, "사주의 달과 해가 바뀌는 시각", [
            ("2026.10.8", "한로 · 오후 3시 29분", "이때부터 술(戌)의 달이에요"),
            ("2026.11.7", "입동 · 오후 6시 52분", "이때부터 해(亥)의 달이에요"),
            ("2027.2.4", "입춘 · 오전 10시 46분", "이 시각부터 2027년 정미년이에요. 그 전은 아직 병오년이에요")],
            "생일이 절기 날짜와 같다면|태어난 시각까지 확인해요", "출처: 자오선 만세력 계산(한국 시각)"),
           "사주의 달과 해가 바뀌는 시각 흐름: 2026년 10월 8일 오후 3시 29분 한로부터 술의 달, 11월 7일 오후 6시 52분 입동부터 해의 달, 2027년 2월 4일 오전 10시 46분 입춘부터 정미년",
           "1일이 아니라 절기 시각에 바뀌는 순서를 차례로 놓아 보면 이래요."),
        R=(lambda n, c: D3.quad(n, c, "'할 수 있다'는 믿음이 자라는 네 길",
            [("해낸 경험", "작게라도 직접 해낸 일이 가장 큰 힘이에요"), ("남이 하는 걸 보기", "나와 비슷한 사람이 해내는 걸 봐요"),
             ("말로 북돋움", "'할 수 있어'라는 말을 들어요"), ("몸과 마음 상태", "긴장이 풀려야 할 수 있다고 느껴요")], 0,
            "출처: Bandura (1977), Psychological Review", note="일간 하나를 찾아 읽어 보는 일이 첫 칸, '해낸 경험'이에요."),
           "반두라(1977)의 자기효능감이 자라는 네 길: 해낸 경험, 남이 하는 걸 보기, 말로 북돋움, 몸과 마음 상태. 일간 하나를 찾아 읽는 일이 첫 칸",
           "심리학자 반두라(1977)는 '할 수 있다'는 믿음이 네 길로 자란다고 봤어요.\n그중 가장 큰 길이 작게라도 직접 해낸 경험이에요."))
    # n48 물고기자리 — 두 별이 머문 햇수(본문 값) + 반추 지진 연구
    P["n48"] = dict(key="48",
        C=(3, lambda n, c: D3.vbar(n, c, "물고기자리에 머문 두 별", [("해왕성", 14, True), ("토성", 3, False)], 14,
            "두 별 모두 2026년 초에 떠났어요.|2027년엔 연중 양자리에 있어요",
            "출처: 자오선 천문 계산(2026년 10월 15일 기준) · 해왕성 2012년 2월~2026년 1월, 토성 2023년 3월~2026년 2월", fmt="약 {:.0f}년", step=2),
           "물고기자리에 머문 두 별의 햇수 막대그래프: 해왕성 약 14년(2012년 2월~2026년 1월), 토성 약 3년(2023년 3월~2026년 2월). 2027년엔 두 별 모두 양자리",
           "물고기자리에 머문 두 별의 햇수를 막대로 그려 보면 이래요.\n해왕성은 약 14년, 토성은 약 3년을 머물다 떠났어요."),
        R=(lambda n, c: D3.exp(n, c, "큰 지진 뒤, 곱씹는 버릇", "놀런혹스마·모로 · 1991",
            [("마침", "지진 전에 대학생들의 기분과 생각 버릇을 재 둔 상태였어요"), ("지진", "1989년 샌프란시스코 근처에 큰 지진(로마 프리타)이 났어요"),
             ("다시", "지진 뒤 몇 주에 걸쳐 같은 학생들을 다시 쟀어요")],
            "일을 곱씹는 버릇이 큰 학생일수록|몇 주 뒤에도 우울한 마음이 더 컸어요", "출처: Nolen-Hoeksema & Morrow (1991), J. Personality and Social Psychology"),
           "놀런혹스마와 모로(1991) 실험 카드: 1989년 로마 프리타 지진 전후로 대학생을 쟀더니, 일을 곱씹는 버릇이 큰 학생일수록 몇 주 뒤에도 우울한 마음이 더 컸다는 연구",
           "심리학자 놀런혹스마와 모로(1991)는 1989년 샌프란시스코 지진 전후로 대학생들의 마음을 쟀어요.\n일을 곱씹는 버릇이 큰 학생일수록 몇 주 뒤에도 우울한 마음이 더 컸어요."))
    # n57 자미두수 명반 — 처음 읽을 세 칸(본문) + 칭찬 실험(고정 마음가짐)
    P["n57"] = dict(key="57",
        C=(5, lambda n, c: D3.triad(n, c, "처음 읽을 세 칸", [("명궁", "타고난 바탕이에요"), ("신궁", "살면서 점점 드러나는 쪽이에요"),
             ("천이궁", "명궁에 큰 별이 없으면 이 칸의 별을 빌려 읽어요(차성)")], 0,
            "두 칸이 비슷하면 겉과 속이 비슷해요.|다르면 장소마다 다른 모습을 꺼내요", "출처: 자미두수 명반 읽는 법(이 글 5절)"),
           "자미두수 명반에서 처음 읽을 세 칸: 명궁은 타고난 바탕, 신궁은 살면서 드러나는 쪽, 천이궁은 명궁에 큰 별이 없을 때 별을 빌려 읽는 칸",
           "처음 읽을 세 칸을 나란히 놓아 보면 이래요."),
        R=(lambda n, c: D3.compare(n, c, "어떤 칭찬을 들었나요", ("'똑똑하구나'", "'열심히 했구나'"),
            [("다음 문제", "쉬운 문제를 더 많이 골랐어요", "배울 게 많은 어려운 문제를 더 많이 골랐어요"),
             ("막힌 뒤", "덜 즐겁고 일찍 그만뒀어요", "더 오래 붙잡았어요"), ("마지막 점수", "처음보다 떨어졌어요", "처음보다 올랐어요")],
            "출처: Mueller & Dweck (1998), J. Personality and Social Psychology · 초등학교 5학년"),
           "뮐러와 드웩(1998) 칭찬 실험 비교표: 똑똑하다고 칭찬받은 아이들은 쉬운 문제를 고르고 일찍 그만뒀고, 열심히 했다고 칭찬받은 아이들은 어려운 문제를 고르고 더 오래 붙잡았다는 표",
           "뮐러와 드웩(1998)은 아이들에게 '똑똑하구나'와 '열심히 했구나', 두 가지 칭찬을 나눠 해 봤어요.\n타고난 머리를 칭찬받은 아이들이 오히려 쉬운 문제만 고르고 일찍 그만뒀어요."))
    # n11 자오선 소개 — 같게·다르게 말하는 곳 표(본문) + 로터 학자 카드
    P["n11"] = dict(key="11",
        C=(4, lambda n, c: D3.compare(n, c, "겹쳐 읽으면 나오는 두 이야기", ("같게 말하는 곳", "다르게 말하는 곳"),
            [("뜻", "타고난 성격이에요", "내가 고를 수 있는 곳이에요"), ("예", "사주의 흙도 별자리의 흙도 같은 말을 해요", "사주는 안정을, 별은 떠나라고 해요"),
             ("읽는 법", "나를 오래 따라다닌 성향으로 읽어요", "상황에 따라 다른 얼굴을 꺼낼 수 있다고 읽어요")],
            "출처: 자오선 교차 읽기 방식(이 글 4절)"),
           "겹쳐 읽으면 나오는 두 이야기 표: 같게 말하는 곳은 타고난 성격, 다르게 말하는 곳은 내가 고를 수 있는 곳",
           "두 이야기를 표로 나란히 놓으면 이래요."),
        R=(lambda n, c: D3.person(n, c, "결과는 누구 손에 있을까", "줄리언 로터", "Julian B. Rotter · 미국 심리학자", "1966 · 통제 소재",
            [("생각", "일의 결과가 내 행동 때문인지, 운이나 남 때문인지 믿는 쪽이 사람마다 달라요"),
             ("이름", "내 손이라고 믿는 쪽을 '내부', 운이라고 믿는 쪽을 '외부'라고 불렀어요"),
             ("재는 법", "두 문장 중 더 맞는 쪽을 고르는 문항으로 쟀어요")],
            "풀이는 흐름을 읽는 도구예요.|바꿀 몫은 내 손에 남겨 둬요", "출처: Rotter (1966), Psychological Monographs"),
           "심리학자 줄리언 로터(1966) 카드: 일의 결과를 내 손으로 믿는 쪽을 내부, 운으로 믿는 쪽을 외부라고 부른 통제 소재",
           "심리학자 로터(1966)는 일의 결과를 내 손에 있다고 믿는지, 운에 있다고 믿는지가 사람마다 다르다고 봤어요.\n이것을 '통제 소재'라고 불러요."))
    # n51 별자리 기본기 — 원소 네 칸(본문 값, b4 자리) + 포러 실험
    P["n51"] = dict(key="51",
        C=("naver_z51_b4", lambda n, c: D3.quad(n, c, "열두 별자리, 네 원소로 묶으면",
            [("불", "양자리 · 사자자리|사수자리 · 표현과 추진"), ("흙", "황소자리 · 처녀자리|염소자리 · 현실과 안정"),
             ("공기", "쌍둥이자리 · 천칭자리|물병자리 · 생각과 관계"), ("물", "게자리 · 전갈자리|물고기자리 · 감정과 공감")], 3,
            "출처: 서양 점성술 원소·양태 분류(이 글 2·3절)", note="원소 넷 × 양태 셋(활동·고정·변통) = 12별자리. 물고기자리는 '물 + 변통'이에요."),
           "열두 별자리를 네 원소로 묶은 그림: 불은 양자리·사자자리·사수자리, 흙은 황소자리·처녀자리·염소자리, 공기는 쌍둥이자리·천칭자리·물병자리, 물은 게자리·전갈자리·물고기자리",
           None),
        R=(lambda n, c: D3.bignum(n, c, "모두 같은 풀이를 받았는데", "4.26", "'잘 맞는다' 점수 평균(5점 만점)",
            [("실험", "심리학자 포러가 학생 39명에게 각자 성격 검사 결과라며 풀이를 나눠 줬어요"),
             ("사실", "모두가 받은 풀이는 누구에게나 들어맞을 만한 같은 문장이었어요"),
             ("우리 글", "맞는 문장만 남기는 마음이에요. 안 맞았던 문장도 하나 골라 봐요")],
            "출처: Forer (1949), J. Abnormal and Social Psychology"),
           "포러(1949) 실험 큰 숫자: 학생 39명이 모두 같은 성격 풀이를 받고도 잘 맞는다는 점수를 5점 만점에 평균 4.26으로 매겼다는 그림",
           "1949년 심리학자 포러는 학생 39명에게 각자 성격 검사 결과라며 풀이를 나눠 줬어요.\n사실 모두 같은 문장이었는데, '잘 맞는다' 점수는 5점 만점에 평균 4.26이었어요."))
    return P


DROP = {"n47": ["naver_z47_c4"], "n48": ["naver_z48_c4"], "n57": ["naver_z57_c4"]}


def remote_names():
    out = subprocess.run(["git", "-C", os.path.join(HERE, ".."), "ls-tree", "-r", "--name-only", "HEAD", "naver/img/"], capture_output=True, text=True).stdout
    return {os.path.basename(x) for x in out.split()}


def fb_map():
    """이미 발행 글에 들어간 여백 없는 판(old → new). K-138로 다시 고친 사진은 5f."""
    m = {}
    for items in json.load(open(os.path.join(HERE, "fullbleed_plan.json"), encoding="utf-8")).values():
        for it in items:
            if it.get("new"): m[it["old"]] = it["new"]
    m.update({"naver_i02_여섯운명학4.jpg": "naver_i02_여섯운명학5f.jpg", "naver_i03_읽는순서4.jpg": "naver_i03_읽는순서5f.jpg"})
    return m


def run(only=None):
    import fullbleed as FBK
    P = plan(); pages = json.load(open(PG, encoding="utf-8")); made = []; rn_ = remote_names(); fbp = {}
    FB = fb_map()
    for pid, sp in P.items():
        if only and pid not in only: continue
        c = CV.Ctx(PAL_OVR[pid]) if pid in PAL_OVR else V2.pal(pid); key = sp["key"]
        cs, cfn, calt, ctxt = sp["C"]; rfn, ralt, rtxt = sp["R"]
        rn, cn = f"naver_z{key}_e8.jpg", f"naver_z{key}_g8.jpg"
        for n, fn in ((rn, rfn), (cn, cfn)):
            if not B.PREVIEW:
                assert n not in rn_ and n.replace(".jpg", "f.jpg") not in rn_, ("이미 있는 이름", n)
            if B.PREVIEW or not B1.have(n): fn(n, c)
            made.append(n)
        if B.PREVIEW: continue
        # K-137 여백 없는 판(새 이름 f)
        rows = []
        for n in (rn, cn):
            r, why = FBK.convert(n, [FBK.IMG, os.path.join(FBK.IMG, "m1280")])
            rows.append({"old": n, "new": r[0] if r else None, "how": r[1] if r else why})
        fbp[pid] = rows; nf = {x["old"]: x["new"] or x["old"] for x in rows}
        body = pages[pid]["body"]
        if "B3" in pages[pid].get("k131", ""): print("이미 B3:", pid); continue
        m = re.search(re.escape(LEAD) + r'<p><img[^>]*src="[^"]*naver_z' + key + r'_q4[^"]*"[^>]*></p>', body); assert m, pid
        body = body[:m.start()] + P_(rtxt) + B1.IMG(nf[rn], ralt).replace(B1.BL, "") + body[m.end():]
        for part in DROP.get(pid, []): body = V3drop(body, part)
        if isinstance(cs, str): body = B1.replace_img(body, cs, (P_(ctxt) if ctxt else "") + B1.IMG(nf[cn], calt))
        else: body = B1.after_head(body, cs, P_(ctxt) + B1.IMG(nf[cn], calt))
        body, k = FUN.subn("", body)
        # 남은 옛 사진 이름 → 발행 글에 이미 들어간 여백 없는 판
        from urllib.parse import unquote, quote   # 한글 이름은 주소에 %xx 로 들어 있다
        body = re.sub(r'/naver/img/([^"/]+)"', lambda m: ("/naver/img/" + quote(FB[unquote(m.group(1))]) + '"') if unquote(m.group(1)) in FB else m.group(0), body)
        pages[pid]["body"] = body; pages[pid]["k131"] = TAG
    if not B.PREVIEW:
        open(PG, "w", encoding="utf-8").write(json.dumps(pages, ensure_ascii=False, indent=1) + "\n")
        # fullbleed_plan.json 에 새 그림 old→new 더하기(k131_check FB 맵이 f판을 원래 이름으로 읽게)
        fp = os.path.join(HERE, "fullbleed_plan.json"); plan_ = json.load(open(fp, encoding="utf-8"))
        for pid, rows in fbp.items():
            have = {x.get("old") for x in plan_.get(pid, [])}
            plan_.setdefault(pid, []).extend([{"pos": None, **x, "src": "B3 10/19"} for x in rows if x["old"] not in have])
        json.dump(plan_, open(fp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return made


def V3drop(body, part):
    pat = re.compile(r'<p><img[^>]*src="[^"]*' + re.escape(part) + r'[^"]*"[^>]*></p>(?:<p>&nbsp;</p>)?')
    body, k = pat.subn("", body); assert k == 1, (part, k); return body


if __name__ == "__main__":
    print(run({a for a in sys.argv[1:]} or None))
