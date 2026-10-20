"""K-131 B5f: 남은 예약 글 n74·n78(11/6)·n79(11/7)·n68(11/12)·n69(11/14) 본문 그림 · K-135 그림 거리 · K-143 의도 카드 도입부 (① 자동 실행 10/20 11:45, CT 10/19 12:40 순서의 마지막 묶음).
build_k131_b4a.py 와 같은 방식(글마다 두 장 *9.jpg → 여백 없는 판 *9f.jpg). 다른 점: n78 은 심리 단락이 없어 R 대신 두 번째 본문 도식(C2)을 e9 이름으로 넣는다.
이웃 글 첫 도식: n59 versus → n74 timeline3 → n78 compare → n79 quad → n68 timeline3 (n78 두 번째는 quad: 배치 안 같은 모양 2번까지) → n69 compare.
새 이름만. 사용: PREVIEW=폴더 python3 naver/build_k131_b5f.py (그림만) · python3 naver/build_k131_b5f.py [글 번호…]"""
import os, sys, re, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import body_v3 as B, diagrams_k131c as D3
import build_k131_b1 as B1, build_k131_b2v2 as V2, build_k131_b3 as B3, build_k131_b4a as B4, cover_v3 as CV
PAL_OVR = {"n79": "v_navy", "n69": "v_navy_inv", "n78": "y_gray"}   # 표지 로열 블루(K-067) → 네이비, 흰 판 → 옅은 회색
PG = os.path.join(HERE, "pages.json")
TAG = "B5f 10/20(K-135)"
P_ = B3.P_


def plan():
    P = {}
    # n74 2027 수성 역행 — 2·3절 세 번의 역행과 불의 삼합 달(본문 값, b4 자리) + 이메일 말투 실험(크루거 연구진 2005)
    P["n74"] = dict(key="74",
        C=("replace", "naver_z74_b4", lambda n, c: D3.timeline3(n, c, "2027년 수성 역행 세 번", [
            ("2월", "2월 10일 ~ 3월 3일", "인월(2월 4일~3월 5일) 안에 들어 있어요"),
            ("6월", "6월 11일 ~ 7월 4일", "오월(6월 6일~7월 6일) 안에 들어 있어요"),
            ("10월", "10월 8일 ~ 10월 28일", "술월(10월 8일~11월 7일) 안에 들어 있어요")],
            "세 번 모두 불의 삼합 달 안이에요.|약속과 숫자를 한 번 더 확인해요", "출처: 이 글 2·3절 · 자오선 계산(한국 시간), 달은 절기 기준"),
           "2027년 수성 역행 세 번: 2월 10일~3월 3일은 인월 안, 6월 11일~7월 4일은 오월 안, 10월 8일~10월 28일은 술월 안이라 세 번 모두 불의 삼합 달 안에 든다는 그림",
           None),
        R=("lead", "naver_z74_q4", lambda n, c: D3.vbar(n, c, "내 말투, 전해졌을까", [("보낸 사람 짐작", 78, False), ("받은 사람 실제", 56, True)], 100,
            "보내기 전에|받는 사람 자리에서 한 번 더 읽어요", "출처: Kruger, Epley, Parker & Ng (2005), J. Personality and Social Psychology · 이메일로 보낸 말투(진지함·비꼼)를 맞힌 비율",
            fmt="{:.0f}%", step=20),
           "크루거 연구진(2005) 이메일 실험 막대: 보낸 사람은 받는 사람이 말투를 78% 맞힐 거라 짐작했지만 실제로는 56%만 맞혔다는 그림",
           "크루거 연구진(2005)은 진지한 말과 비꼬는 말을 이메일로 보내게 하고, 받는 사람이 말투를 얼마나 맞힐지 보낸 사람에게 짐작하게 했어요.\n짐작은 78%였는데 실제로 맞힌 건 56%였어요. '내가 잘 전했겠지'가 과잉 확신이에요."),
        drop=["naver_z74_c4"], intent=True,
        intro=("<p>수성 역행이라는 말을 들으면 연락도 계약도 미뤄야 하나 싶어서 날짜부터 찾아보셨나요?</p><p><b>2027년 수성 역행 날짜</b>를 천문 일정 기준으로 정리해 봤어요.</p>",
               "<p><b>2027년 수성 역행</b>은 2월 10일~3월 3일, 6월 11일~7월 4일, 10월 8일~10월 28일, 딱 세 번이에요(한국 시간).</p><p>역행 기간은 일을 멈추는 때가 아니라 연락과 계약을 한 번 더 확인하는 때로 읽어요.</p>"))
    # n78 사주 시간표 — 2절 일간별 신시 글자(본문 규칙, b4 자리) + 3절 경계 시각(본문 말, 3절 머리 아래). 심리 단락 없음
    P["n78"] = dict(key="78",
        C=("replace", "naver_z78_b4", lambda n, c: D3.compare(n, c, "오후 3시 52분, 일간마다 시주", ("자시 시주", "신시 시주"), [
            ("갑 · 기일", "갑자(甲子)", "임신(壬申)"),
            ("을 · 경일", "병자(丙子)", "갑신(甲申)"),
            ("병 · 신일", "무자(戊子)", "병신(丙申)"),
            ("정 · 임일", "경자(庚子)", "무신(戊申)"),
            ("무 · 계일", "임자(壬子)", "경신(庚申)")],
            "출처: 이 글 2절 · 자시 글자에서 한 칸씩 이어 세면 신시는 아홉째 칸"),
           "오후 3시 52분 신시의 시주를 일간마다 본 표: 갑·기일은 갑자로 시작해 임신, 을·경일은 병자로 시작해 갑신, 병·신일은 무자로 시작해 병신, 정·임일은 경자로 시작해 무신, 무·계일은 임자로 시작해 경신",
           None),
        C2=("after", 3, lambda n, c: D3.quad(n, c, "경계 시각, 어느 시일까", [
            ("오후 2:59", "아직 미시(未時)|오후 3시 전이에요"), ("오후 3:00", "신시(申時) 시작|정각부터 신시예요"),
            ("밤 11:00", "자시(子時) 시작|일 칸은 다음 날로 세워요"), ("밤 12:00", "그대로 자시|태어난 날 일 칸으로 세워요")], 1,
            "출처: 이 글 3절·자주 묻는 질문 · 자오선 감정서 기준", note="서머타임 때 태어났어도 시계에 적힌 시각 그대로 적어요."),
           "경계 시각 네 칸: 오후 2시 59분은 아직 미시, 오후 3시 정각부터 신시, 밤 11시부터 자시라 자오선은 일 칸을 다음 날로 세우고, 밤 12시는 자시이며 태어난 날의 일 칸으로 세운다는 그림",
           "헷갈리기 쉬운 시각을 차례로 놓아 보면 이래요."),
        drop=["naver_z78_c4"], intent=True,
        intro=("<p>태어난 시각이 오후 3시 52분인데, 사주에서는 무슨 시인지 헷갈리셨나요?</p><p><b>사주 시간표</b>를 열두 시 기준으로 정리하고, 시주 글자가 정해지는 방법까지 풀어 봤어요.</p>",
               "<p><b>사주 시간표</b>로 보면 오후 3시 52분은 신시(申時)예요. 오후 3시부터 5시 전까지가 신시예요.</p><p>시주의 아래 글자는 시각으로, 위 글자는 태어난 날의 일간으로 정해져요.</p>"))
    # n79 도화살 — 2절 도화 글자 네 묶음(본문 표, b4 자리) + 단순 노출 효과 강의실 실험(모어랜드·비치 1992)
    P["n79"] = dict(key="79",
        C=("replace", "naver_z79_b4", lambda n, c: D3.quad(n, c, "내 도화 글자 찾기", [
            ("인·오·술", "호랑이·말·개띠|도화 글자는 묘(卯)"), ("사·유·축", "뱀·닭·소띠|도화 글자는 오(午)"),
            ("신·자·진", "원숭이·쥐·용띠|도화 글자는 유(酉)"), ("해·묘·미", "돼지·토끼·양띠|도화 글자는 자(子)")], 2,
            "출처: 이 글 2절 · 띠(년지)나 일지 어느 쪽으로 찾아도 같아요", note="예: 용띠는 신·자·진 묶음이라 유(酉)예요. 만세력 아래 줄에 유가 있는지 봐요."),
           "도화 글자 찾기 네 칸: 인·오·술은 묘, 사·유·축은 오, 신·자·진은 유, 해·묘·미는 자가 도화 글자이고 용띠는 신·자·진 묶음이라 유라는 그림",
           None),
        R=("lead", "naver_z79_q4", lambda n, c: D3.exp(n, c, "강의실에 자주 온 사람", "모어랜드·비치 · 1992",
            [("준비", "비슷해 보이는 여학생 네 명이 큰 강의에 각각 0번·5번·10번·15번 들어와 앉았어요"),
             ("조건", "누구와도 말을 나누지 않고 조용히 듣기만 했어요"),
             ("학기 끝", "수강생들에게 네 사람 사진을 보여 주고 호감과 매력을 물었어요")],
            "말 한마디 없이도|자주 본 사람일수록 더 좋게 봤어요", "출처: Moreland & Beach (1992), J. Experimental Social Psychology"),
           "모어랜드와 비치(1992) 강의실 실험 카드: 말을 나누지 않고 강의에 자주 들어온 사람일수록 수강생들이 학기 말에 더 호감 있고 매력 있게 봤다는 단순 노출 효과 연구",
           "모어랜드와 비치(1992)는 비슷해 보이는 여학생 네 명을 큰 강의에 0번·5번·10번·15번씩 조용히 앉아 있게 했어요.\n학기 말에 수강생들은 자주 본 사람일수록 더 호감 있게 봤어요. 말 한마디 없이도요."),
        drop=["naver_z79_c4"], intent=True,
        intro=("<p>사주에 도화살이 있다는 말을 듣고, 인기가 많다는 뜻인지 걱정해야 하는 건지 궁금하셨나요?</p><p><b>도화살 뜻</b>과 내 도화 글자 찾는 법을 정리해 봤어요.</p>",
               "<p><b>도화살</b>은 사람을 끌어당기는 매력과 표현으로 읽는 글자예요. 있다고 꼭 인기가 많은 것도, 없다고 매력이 없는 것도 아니에요.</p><p>띠나 일지가 인·오·술이면 묘(卯), 사·유·축이면 오(午), 신·자·진이면 유(酉), 해·묘·미면 자(子)가 내 도화 글자예요.</p>"))
    # n68 2027 닭띠 — 3절 다섯 달(본문 값, 3절 머리 아래) + 완벽주의 세 방향(휴잇·플렛 1991)
    P["n68"] = dict(key="68",
        C=("after", 3, lambda n, c: D3.timeline3(n, c, "닭띠의 2027년 다섯 달", [
            ("2월", "인(寅) · 원진, 아낄 달", "서운함이 쌓이기 쉬워요. 칭찬도 소리 내어 말해요"),
            ("3월", "묘(卯) · 충, 아낄 달", "큰 결정은 미루고 정리하는 달로 써요"),
            ("4월", "진(辰) · 육합, 힘 쓸 달", "내 기술을 알아봐 줄 사람을 만나기 좋아요"),
            ("5월", "사(巳) · 반합, 힘 쓸 달", "준비한 일이 모양을 갖추기 좋아요"),
            ("이듬해 1월", "축(丑) · 반합, 힘 쓸 달", "한 해의 기록을 정리하기 좋아요")],
            "아낄 달 둘을 지나면|힘 쓸 달 둘이 이어져요", "출처: 이 글 3절 · 절기 기준(2월 4일·3월 6일·4월 5일·5월 6일·1월 5일 무렵부터)"),
           "닭띠의 2027년 다섯 달: 2월 인월은 원진, 3월 묘월은 충이라 아낄 달, 4월 진월은 육합, 5월 사월과 이듬해 1월 축월은 반합이라 힘 쓸 달이라는 그림",
           "다섯 달을 차례로 놓아 보면 이래요."),
        R=("lead", "naver_z68_q4", lambda n, c: D3.person(n, c, "완벽주의는 세 방향이에요", "폴 휴잇", "Paul L. Hewitt · 캐나다 심리학자", "1991 · 완벽주의의 세 방향",
            [("나에게", "내가 나에게 흠 없는 결과를 바라는 마음이에요"),
             ("남에게", "주변 사람에게 흠 없는 결과를 바라는 마음이에요"),
             ("남의 기대", "남들이 나에게 완벽을 바란다고 믿는 마음이에요")],
            "어느 방향인지 알면|'이 정도면 낸다'를 정하기 쉬워요", "출처: Hewitt & Flett (1991), J. Personality and Social Psychology"),
           "심리학자 폴 휴잇(1991) 카드: 휴잇과 플렛은 완벽주의를 나에게 바라는 것, 남에게 바라는 것, 남이 나에게 바란다고 믿는 것 세 방향으로 나눠 쟀다는 연구",
           "심리학자 휴잇과 플렛(1991)은 완벽주의를 세 방향으로 나눠 쟀어요.\n나에게 바라는 완벽, 남에게 바라는 완벽, 남들이 나에게 바란다고 믿는 완벽이에요. 내 마음이 어느 쪽인지부터 보면 내놓을 기준을 정하기 쉬워요."),
        drop=["naver_z68_c4"], intent=True,
        intro=("<p>꼼꼼함이 드디어 인정받는 해가 온다면 어떨까요?</p><p><b>2027년 닭띠 운세</b>를 달마다 정리해 봤어요.</p>",
               "<p><b>2027년 닭띠</b>는 섬세한 쇠(酉)를 해의 불(丁)이 다듬는 해라, 꼼꼼한 실력이 드러나 인정받기 좋은 흐름으로 읽어요.</p><p>힘 쓸 달은 4월·5월과 이듬해 1월, 아낄 달은 2월·3월이에요.</p>"))
    # n69 2027 쥐띠 — 3절 다섯 달 표(본문 값, 3절 머리 아래) + 호감 격차(부스비 연구진 2018)
    P["n69"] = dict(key="69",
        C=("after", 3, lambda n, c: D3.compare(n, c, "쥐띠가 고를 달 다섯", ("쥐(子)와의 사이", "이렇게 써요"), [
            ("4월 진", "함께 모임|(申子辰 반합)", "막힌 일을 풀어요"),
            ("8월 신", "함께 모임|(申子辰 반합)", "사람과 손잡아요"),
            ("이듬해|1월 축", "짝(육합)", "따뜻하게 마무리해요"),
            ("6월 오", "정면 부딪힘(충)", "큰 약속·큰 결정은 미뤄요"),
            ("7월 미", "서운함(해·원진)", "연락은 짧게라도 자주 해요")],
            "출처: 이 글 3절 · 절기 기준(4월 5일·8월 8일·1월 5일·6월 6일·7월 7일 무렵부터)"),
           "쥐띠가 고를 달 다섯 표: 4월 진월과 8월 신월은 반합이라 막힌 일을 풀고 손잡기, 이듬해 1월 축월은 육합이라 따뜻한 마무리, 6월 오월은 충이라 큰 약속을 미루고, 7월 미월은 해·원진이라 연락을 짧게라도 자주",
           "다섯 달을 한 표에 놓아 보면 이래요."),
        R=("lead", "naver_z69_q4", lambda n, c: D3.versus(n, c, "대화 뒤, 상대는 나를 얼마나 좋아했을까", "부스비 연구진 · 2018",
            ("내 짐작", "처음 본 사람과 이야기를 나눈 뒤, 상대가 나를 얼마나 좋아했을지 짐작했어요.", "덜 좋아했을 거라 봤어요"),
            ("상대의 실제 마음", "상대에게 나를 얼마나 좋아했는지 직접 물었어요.", "짐작보다 더 좋아했어요"),
            "늦은 답 하나로|상대 마음을 결론 내리지 않아요", "출처: Boothby, Cooney, Sandstrom & Clark (2018), Psychological Science"),
           "부스비 연구진(2018) 실험 카드: 처음 본 사람과 대화한 뒤 사람들은 상대가 자기를 덜 좋아했을 거라 짐작했지만, 상대는 실제로 짐작보다 더 좋아했다는 호감 격차 연구",
           "부스비 연구진(2018)은 처음 본 두 사람이 이야기를 나눈 뒤, 상대가 나를 얼마나 좋아했을지 짐작하게 하고 상대의 실제 마음과 견줬어요.\n사람들은 상대가 자기를 좋아한 정도를 실제보다 낮게 짐작했어요. 늦은 답도 '싫어하나'보다 '바쁜가' 쪽일 때가 많아요."),
        drop=["naver_z69_c4"], intent=True,
        intro=("<p>돈은 들어오는데 마음이 상하는 해가 있다면 어떨까요?</p><p><b>2027년 쥐띠 운세</b>를 달마다 정리해 봤어요.</p>",
               "<p><b>2027년 쥐띠</b>는 쥐(子)와 양(未)이 서로 서운하게 만드는 해(害)·원진이 겹쳐, 말 한마디와 연락이 엇갈리기 쉬운 해로 읽어요.</p><p>재물 기회는 분명하고, 힘 쓸 달은 4월·8월·이듬해 1월, 아낄 달은 6월·7월이에요.</p>"))
    return P


def run(only=None):
    import fullbleed as FBK
    from urllib.parse import unquote, quote
    P = plan(); pages = json.load(open(PG, encoding="utf-8")); made = []; rn_ = B3.remote_names(); fbp = {}
    FB = B3.fb_map(); intents = set()
    for pid, sp in P.items():
        if only and pid not in only: continue
        c = CV.Ctx(PAL_OVR[pid]) if pid in PAL_OVR else V2.pal(pid); key = sp["key"]
        cn, en = f"naver_z{key}_g9.jpg", f"naver_z{key}_e9.jpg"
        second = sp.get("R") or sp.get("C2")
        for n, fn in ((en, second[2]), (cn, sp["C"][2])):
            if not B.PREVIEW:
                assert n not in rn_ and n.replace(".jpg", "f.jpg") not in rn_, ("이미 있는 이름", n)
            if B.PREVIEW or not B1.have(n): fn(n, c)
            made.append(n)
        if B.PREVIEW: continue
        rows = []
        for n in (en, cn):
            r, why = FBK.convert(n, [FBK.IMG, os.path.join(FBK.IMG, "m1280")])
            rows.append({"old": n, "new": r[0] if r else None, "how": r[1] if r else why})
        fbp[pid] = rows; nf = {x["old"]: x["new"] or x["old"] for x in rows}
        body = pages[pid]["body"]
        if pages[pid].get("k131", "").startswith("B5f"): print("이미 B5f:", pid); continue
        if sp.get("R"):
            _, rpart, _, ralt, rtxt = sp["R"]
            body = B4.swap_lead(body, rpart, P_(rtxt) + B1.IMG(nf[en], ralt).replace(B1.BL, ""))
        for part in sp.get("drop", []): body = B3.V3drop(body, part)
        for slot, nm in (("C", cn), ("C2", en)):
            if slot not in sp: continue
            mode, pos, _, alt, txt = sp[slot]
            img = (P_(txt) if txt else "") + B1.IMG(nf[nm], alt)
            body = B1.replace_img(body, pos, img) if mode == "replace" else B1.after_head(body, pos, img)
        body, _ = B3.FUN.subn("", body)
        o, n_ = sp["intro"]; assert body.count(o) == 1, (pid, "도입부"); body = body.replace(o, n_)
        intents.add(pid)
        body = re.sub(r'/naver/img/([^"/]+)"', lambda m: ("/naver/img/" + quote(FB[unquote(m.group(1))]) + '"') if unquote(m.group(1)) in FB else m.group(0), body)
        pages[pid]["body"] = body; pages[pid]["k131"] = TAG
    if not B.PREVIEW:
        open(PG, "w", encoding="utf-8").write(json.dumps(pages, ensure_ascii=False, indent=1) + "\n")
        fp = os.path.join(HERE, "fullbleed_plan.json"); plan_ = json.load(open(fp, encoding="utf-8"))
        for pid, rows in fbp.items():
            have = {x.get("old") for x in plan_.get(pid, [])}
            plan_.setdefault(pid, []).extend([{"pos": None, **x, "src": "B5f 10/20"} for x in rows if x["old"] not in have])
        json.dump(plan_, open(fp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        if intents:
            ip = os.path.join(HERE, "intent_cards.json"); ic = json.load(open(ip, encoding="utf-8"))
            for pid in intents: ic["cards"][pid]["applied"] = True
            json.dump(ic, open(ip, "w", encoding="utf-8"), ensure_ascii=False, indent=1); open(ip, "a").write("\n")
    return made


if __name__ == "__main__":
    print(run({a for a in sys.argv[1:]} or None))
