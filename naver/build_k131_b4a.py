"""K-131 B4 첫 묶음(10/18 발행 n61·n34 + 오늘 21:00 예약 n50) 본문 그림 · K-135 그림 거리 · K-137 여백 없는 판 (① 자동 실행 10/19 12:20, CT 12:40 순서).
build_k131_b3.py 와 같은 방식으로 글마다 두 장(*9.jpg → *9f.jpg):
  R(e9) = 심리학 단락 자리: 그 단락이 말한 개념의 실험·학자 카드. 앞 줄('…그려 보면 이래요.')을 그 연구를 말하는 한두 문장으로 바꾼다
  C(g9) = 그 글 본문의 계산 값·순서로 그린 도식(지어낸 수치 없음)
옛 틀은 글마다 2장 이하: 옛 c4('해 볼 것' 그림) 뺌, n34 s4(겹침 틀) 뺌, n50 b4(배지 틀) → 이번 주 표, n34 p_light5(K-138 글자 묻힘) → 실험 카드.
K-067: 판이 로열 블루(#0A46B3)인 n61·n34는 본문 그림 판을 네이비로 바꾼다.
새 이름만. git ls-tree 로 이름 겹침을 먼저 잰다.
사용: PREVIEW=폴더 python3 naver/build_k131_b4a.py (그림만) · python3 naver/build_k131_b4a.py [글 번호…]"""
import os, sys, re, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import body_v3 as B, diagrams_k131 as DG, diagrams_k131b as D2, diagrams_k131c as D3
import build_k131_b1 as B1, build_k131_b2v2 as V2, build_k131_b3 as B3, cover_v3 as CV
PAL_OVR = {"n61": "v_navy_inv", "n34": "v_navy"}
PG = os.path.join(HERE, "pages.json")
TAG = "B4 10/19(K-135)"
P_ = B3.P_


def plan():
    P = {}
    # n61 당사주 — 5절 예시 계산 흐름(갑인년 7월 26일 오시 → 네 별) + 부정성 편향(바우마이스터 2001)
    P["n61"] = dict(key="61",
        C=("after", 5, lambda n, c: D3.timeline3(n, c, "예시로 네 별 찾기", [
            ("초년", "천권성", "해 · 갑인년, 인(寅) 자리에서 시작"),
            ("중년", "천고성", "달 · 7월이라 6칸을 더 세요"),
            ("말년", "천인성", "날 · 26일이라 25칸을 더 세요"),
            ("평생", "천파성", "시각 · 오시라 6칸을 더 세요")],
            "음력 갑인년 7월 26일 오시생 예시", "출처: 이 글 5절 계산(자(子)부터 천귀성·천액성·천권성… 차례)"),
           "음력 갑인년 7월 26일 오시 예시로 네 별 찾는 순서: 인 자리에서 초년 천권성, 6칸 더 세어 중년 천고성, 25칸 더 세어 말년 천인성, 6칸 더 세어 평생 천파성",
           "앞의 예시를 한 칸씩 세어 보면 이렇게 네 별이 나와요."),
        R=("lead", "naver_z61_q4", lambda n, c: D3.person(n, c, "왜 나쁜 별 하나가 크게 들릴까", "로이 바우마이스터", "Roy F. Baumeister · 미국 심리학자", "2001 · 나쁜 것이 더 세다",
            [("생각", "나쁜 일이 같은 크기의 좋은 일보다 마음에 더 크게, 더 오래 남는다고 봤어요"),
             ("근거", "관계·감정·배움·첫인상 같은 여러 분야의 연구를 모아 견줬어요"),
             ("우리 글", "네 별 중 조심할 별 하나가 나머지 세 칸보다 크게 들리는 까닭이에요")],
            "좋은 뜻부터 한 줄 적어요.|나머지 세 칸도 같이 읽어요", "출처: Baumeister, Bratslavsky, Finkenauer & Vohs (2001), Review of General Psychology"),
           "심리학자 로이 바우마이스터 연구진(2001) 카드: 나쁜 일이 같은 크기의 좋은 일보다 마음에 더 크게 남는다는 여러 분야 연구를 모아 견준 정리",
           "심리학자 바우마이스터 연구진(2001)은 여러 분야의 연구를 모아, 나쁜 일이 같은 크기의 좋은 일보다 마음에 더 크게 남는다고 정리했어요.\n그래서 네 별 중 조심할 별 하나가 유난히 크게 들려요."),
        drop=["naver_z61_c4"])
    # n34 반추 — 4절 세 풀이 삼각형(본문 말) + 잠들기 전 할 일 목록 실험(스컬린 2018)
    P["n34"] = dict(key="34",
        C=("after", 4, lambda n, c: D3.triangle(n, c, "세 풀이가 가리키는 곳", [("사주", "비·강물(계수·임수)"), ("별자리", "게·물고기자리"), ("숫자", "7번·2번")], -1,
            "안쪽으로 깊어지는 마음", "정리하지 않으면 같은 자리를 돌아요.|종이로 옮기기만 해도 밤이 가벼워져요", "출처: 이 글 2·4절 세 풀이"),
           "세 풀이가 가리키는 곳 삼각형: 사주의 계수·임수, 별자리의 게·물고기자리, 숫자 7번·2번이 모두 안쪽으로 깊어지는 마음을 가리킨다는 그림",
           "세 풀이를 한 그림에 모으면 이래요."),
        R=("lead", "naver_z34_p_light5", lambda n, c: D3.exp(n, c, "잠들기 전 5분, 무엇을 적을까", "스컬린 연구진 · 2018",
            [("모임", "젊은 성인 57명이 수면 실험실에서 잠들기 전 5분 동안 글을 썼어요"),
             ("두 무리", "한쪽은 앞으로 할 일 목록을, 다른 쪽은 이미 끝낸 일을 적었어요"),
             ("잰 것", "뇌파를 재며 잠드는 데 걸린 시간을 견줬어요")],
            "할 일 목록을 쓴 쪽이 더 빨리 잠들었어요.|자세히 쓸수록 더 빨리 잠들었어요", "출처: Scullin, Krueger, Ballard, Pruett & Bliwise (2018), J. Experimental Psychology: General"),
           "스컬린 연구진(2018) 실험 카드: 잠들기 전 5분 동안 할 일 목록을 쓴 사람이 이미 끝낸 일을 쓴 사람보다 더 빨리 잠들었고, 자세히 쓸수록 더 빨리 잠들었다는 수면 실험",
           "스컬린 연구진(2018)은 잠들기 전 5분 동안 할 일 목록을 쓴 사람과 이미 끝낸 일을 쓴 사람을 견줬어요.\n할 일 목록을 쓴 쪽이 더 빨리 잠들었어요. 머릿속 일을 종이로 옮기는 힘이에요."),
        drop=["naver_z34_s4", "naver_z34_c4"])
    # n50 오늘의 운세 — 3절 이번 주 일진 표(본문 값, b4 자리) + 통제의 착각 복권 실험(랭어 1975)
    W7 = [("10/19 월", "병인 · 불", "같은 기운"), ("10/20 화", "정묘 · 불", "같은 기운"), ("10/21 수", "무진 · 흙", "내가 쏟아내는 날"),
          ("10/22 목", "기사 · 흙", "내가 쏟아내는 날"), ("10/23 금", "경오 · 쇠", "내가 다루는 날"), ("10/24 토", "신미 · 쇠", "내가 다루는 날"),
          ("10/25 일", "임신 · 물", "나를 누르는 날")]
    P["n50"] = dict(key="50",
        C=("replace", "naver_z50_b4", lambda n, c: D3.compare(n, c, "병화 일간의 이번 주", ("그날 하늘 글자", "병화에게는"), W7,
            "출처: 자오선 만세력 계산 · 하늘 글자 오행만 본 간단한 방법(이 글 3절)"),
           "병화 일간으로 본 이번 주 표: 10월 19일 병인과 20일 정묘는 같은 기운, 21일 무진과 22일 기사는 내가 쏟아내는 날, 23일 경오와 24일 신미는 내가 다루는 날, 25일 임신은 나를 누르는 날",
           None),
        R=("lead", "naver_z50_q4", lambda n, c: D3.bignum(n, c, "내가 고른 복권은 더 귀해요", "4배 넘게", "직접 고른 복권에 부른 값 ÷ 건네받은 복권에 부른 값",
            [("실험", "두 회사 직원들에게 1달러짜리 복권을 팔면서, 절반은 직접 고르게 하고 절반은 건네줬어요"),
             ("결과", "추첨 전에 되팔라고 하자 직접 고른 쪽이 평균 8.67달러, 건네받은 쪽이 1.96달러를 불렀어요"),
             ("우리 글", "운에 달린 일도 내 손에 있다고 느끼기 쉬워요. 진짜 내 몫은 그날 하는 행동이에요")],
            "출처: Langer (1975), J. Personality and Social Psychology · 실험 2"),
           "엘런 랭어(1975) 복권 실험 큰 숫자: 1달러짜리 복권을 직접 고른 사람은 건네받은 사람보다 되팔 값을 4배 넘게(8.67달러 대 1.96달러) 불렀다는 그림",
           "심리학자 엘런 랭어(1975)는 1달러짜리 복권을 직접 고른 사람과 건네받은 사람에게 추첨 전에 되팔 값을 물었어요.\n직접 고른 쪽이 4배 넘게 불렀어요. 운에 달린 일도 내 손에 있다고 느끼기 쉬운 거예요."),
        drop=["naver_z50_c4"])
    return P


LEADS = [r'<p>이 마음이 흘러가는 모양을 그려 보면 이래요\.</p>', r'<p>같은 생각이 되풀이되는 모양을 그림으로 그려 보면 이래요\.</p>']


def swap_lead(body, part, new):
    for ld in LEADS:
        m = re.search(ld + r'(?:<p>&nbsp;</p>)?<p><img[^>]*src="[^"]*' + re.escape(part) + r'[^"]*"[^>]*></p>(?:<p>&nbsp;</p>)?', body)
        if m: return body[:m.start()] + new + body[m.end():]
    raise AssertionError(("앞 줄+그림 자리 없음", part))


def run(only=None):
    import fullbleed as FBK
    P = plan(); pages = json.load(open(PG, encoding="utf-8")); made = []; rn_ = B3.remote_names(); fbp = {}
    FB = B3.fb_map()
    for pid, sp in P.items():
        if only and pid not in only: continue
        c = CV.Ctx(PAL_OVR[pid]) if pid in PAL_OVR else V2.pal(pid); key = sp["key"]
        cmode, cpos, cfn, calt, ctxt = sp["C"]; _, rpart, rfn, ralt, rtxt = sp["R"]
        rn, cn = f"naver_z{key}_e9.jpg", f"naver_z{key}_g9.jpg"
        for n, fn in ((rn, rfn), (cn, cfn)):
            if not B.PREVIEW:
                assert n not in rn_ and n.replace(".jpg", "f.jpg") not in rn_, ("이미 있는 이름", n)
            if B.PREVIEW or not B1.have(n): fn(n, c)
            made.append(n)
        if B.PREVIEW: continue
        rows = []
        for n in (rn, cn):
            r, why = FBK.convert(n, [FBK.IMG, os.path.join(FBK.IMG, "m1280")])
            rows.append({"old": n, "new": r[0] if r else None, "how": r[1] if r else why})
        fbp[pid] = rows; nf = {x["old"]: x["new"] or x["old"] for x in rows}
        body = pages[pid]["body"]
        if "B4" in pages[pid].get("k131", ""): print("이미 B4:", pid); continue
        body = swap_lead(body, rpart, P_(rtxt) + B1.IMG(nf[rn], ralt).replace(B1.BL, ""))
        for part in sp.get("drop", []): body = B3.V3drop(body, part)
        cimg = (P_(ctxt) if ctxt else "") + B1.IMG(nf[cn], calt)
        body = B1.replace_img(body, cpos, cimg) if cmode == "replace" else B1.after_head(body, cpos, cimg)
        body, _ = B3.FUN.subn("", body)
        from urllib.parse import unquote, quote
        body = re.sub(r'/naver/img/([^"/]+)"', lambda m: ("/naver/img/" + quote(FB[unquote(m.group(1))]) + '"') if unquote(m.group(1)) in FB else m.group(0), body)
        pages[pid]["body"] = body; pages[pid]["k131"] = TAG
    if not B.PREVIEW:
        open(PG, "w", encoding="utf-8").write(json.dumps(pages, ensure_ascii=False, indent=1) + "\n")
        fp = os.path.join(HERE, "fullbleed_plan.json"); plan_ = json.load(open(fp, encoding="utf-8"))
        for pid, rows in fbp.items():
            have = {x.get("old") for x in plan_.get(pid, [])}
            plan_.setdefault(pid, []).extend([{"pos": None, **x, "src": "B4 10/19"} for x in rows if x["old"] not in have])
        json.dump(plan_, open(fp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return made


if __name__ == "__main__":
    print(run({a for a in sys.argv[1:]} or None))
