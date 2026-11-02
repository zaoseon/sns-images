"""모션 기법 모음 — 열두 가지 움직임을 한 곳에 모아 돌려 쓴다 (대표 10/16 "다양한 모션그래픽 기법 좀 적용하자")

왜 모아 두나
  `html_motion.py`(D-338)로 HTML 모션을 뽑을 길은 났지만, 기법은 `bars.py` 한 조각에
  손으로 쓴 CSS·JS 뿐이었다. 다음 편을 만들 때마다 처음부터 다시 쓰게 된다 —
  그러면 편마다 움직임이 조금씩 달라지고(양산형의 반대가 아니라 그냥 제각각) 겹침 사고도 되풀이된다.
  **움직임을 열두 개의 이름 있는 기법으로 묶어 두고 골라 쓴다.**

K-073 을 코드가 강제한다
  "움직임은 정보를 나르거나 스크롤을 멈출 때만 쓴다." 그래서 모든 기법에 `왜` 를 **반드시** 적는다 —
  `"정보"`(숫자·관계·과정을 나른다) 또는 `"멈춤"`(첫 1초에 눈을 붙든다) 둘 중 하나다.
  꾸미려고 넣는 움직임은 `쓰기()` 가 거절한다. 적는 칸이 있으면 적으면서 한 번 생각하게 된다.

쓰는 법
  from motion_kit import 쓰기, 페이지, 고르기
  장면 = [
    쓰기("나타나기", 왜="멈춤", s=0.1, d=0.7, 글="같은 나를 두고\\n왜 말이 다를까요?", 단="제목"),
    쓰기("막대자라기", 왜="정보", s=1.8, d=1.1, 줄=[("사주와 하락이수",24),("사주와 별자리",17)], 최대=30),
  ]
  open("x.html","w").write(페이지(장면, 판="dg_gold_s"))
  html_motion.render("x.html", "x", 초=8)

  python3 pipeline/motion_kit.py            기법 열두 가지와 어디에 쓰는지 표
  python3 pipeline/motion_kit.py --견본     기법마다 한 장면씩 든 견본 영상
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
import channel_specs as CS, fonts_kit as K, brand_frame as BF

PAL = {x["id"]: x for x in json.load(
    open(os.path.join(ROOT, "assets", "palettes", "color_combos.json"), encoding="utf-8"))["palettes"]}

왜값 = ("정보", "멈춤")

# ── 기법 열두 가지 ────────────────────────────────────────────────────────────
# 칸 뜻:  쓸곳 = 어떤 내용에 맞나 · 나르는것 = 이 움직임이 실제로 전하는 것
#         (나르는 것이 없으면 그 기법은 꾸밈이다 — 목록에 넣지 않는다)
기법 = {
 "나타나기":   dict(쓸곳="훅 한 줄, 장면 첫 글", 나르는것="여기부터 읽으라는 순서"),
 "숫자세기":   dict(쓸곳="퍼센트·사람 수·배수", 나르는것="0에서 그 값까지 올라간 폭"),
 "막대자라기": dict(쓸곳="항목 2~4개 비교", 나르는것="항목끼리의 길이 차이"),
 "선그리기":   dict(쓸곳="추세, 이어짐, 둘레", 나르는것="시작에서 끝까지 가는 방향"),
 "가리개열기": dict(쓸곳="사진·표를 한쪽부터 보여 줄 때", 나르는것="가린 것이 열리는 순서"),
 "쌓이기":     dict(쓸곳="목록 세 줄, 조건 모음", 나르는것="항목이 하나씩 더해지는 것"),
 "원형채우기": dict(쓸곳="비율 하나(몇 명 중 몇)", 나르는것="전체 대비 차지한 몫"),
 "낱말강조":   dict(쓸곳="한 문장에서 뒤집히는 낱말", 나르는것="문장의 무게가 실린 자리"),
 "줄바꾸기":   dict(쓸곳="흔한 오해 → 사실", 나르는것="앞말이 뒷말로 바뀌는 대조"),
 "표채우기":   dict(쓸곳="운명학별 교차표", 나르는것="칸이 채워지며 드러나는 모양"),
 "흐름선":     dict(쓸곳="절차·입력에서 결과까지", 나르는것="거쳐 가는 길과 순서"),
 "한자찍기":   dict(쓸곳="표지 첫 1초 — 그 글의 한자 하나(천간·띠·괘)", 나르는것="이 글이 어떤 글자 이야기인지(첫 화면에서 눈을 붙든다)"),
 "기운그림":   dict(쓸곳="기운·성질 설명(나무·덩굴·해·촛불·산·싹·칼·보석)", 나르는것="그 기운이 어떤 모양으로 뻗는지"),
 "게이지빼기": dict(쓸곳="지치는·줄어드는 이야기", 나르는것="힘이 빠져나가는 흐름(숫자 없이 칸만)"),
 "블록꽂기":   dict(쓸곳="해 볼 것을 일정·자리에 넣는 이야기", 나르는것="그 행동이 들어갈 자리"),
 "그림넘김":   dict(쓸곳="실험 판(K-167): 장면마다 전면 그림 + 천천히 확대", 나르는것="장면이 바뀌었다는 신호, 눈을 붙듦(실험 판만 허용)"),
 "센표지":     dict(쓸곳="실험 판(K-167) 표지: 띠·숫자·센 말 3~4줄", 나르는것="첫 0.5초에 읽히는 약속 하나"),
 "장면글":     dict(쓸곳="실험 판(K-167) 한 장면의 제목+자막을 한 덩어리로 화면 가운데에 크게", 나르는것="그 장면의 약속과 풀이(여백 없이 크게)"),
 "자막":       dict(쓸곳="실험 판(K-167) 그림 위 한 줄", 나르는것="그 장면의 한 줄 풀이"),
 "눈금이동":   dict(쓸곳="내가 어디쯤인지(분포 위 자리)", 나르는것="눈금 위에서 멈추는 위치"),
}

# 내용 유형 → 권장 기법. 사양에 유형만 적으면 기법이 따라오게 하려고 둔 표다.
기법표 = {
 "훅·질문 표지":   ["나타나기", "낱말강조"],
 "숫자·통계":      ["숫자세기", "막대자라기", "원형채우기"],
 "비교·맞대결":    ["줄바꾸기", "막대자라기"],
 "목록·해결책":    ["쌓이기", "나타나기"],
 "절차·따라하기":  ["흐름선", "가리개열기"],
 "교차·표":        ["표채우기", "선그리기"],
 "자가진단·분포":  ["눈금이동", "원형채우기"],
}


def 고르기(내용유형):
    """사양의 내용 유형으로 권장 기법을 받는다. 모르는 유형이면 훅 기본값."""
    return 기법표.get(내용유형, 기법표["훅·질문 표지"])


# ── 움직임 틀 ────────────────────────────────────────────────────────────────
# 자리는 channel_specs 구역에서 가져온다 — 여기에 숫자를 박지 않는다(K-094).
def _단(ch="reel"):
    return {z[0]: z[1:5] for z in CS.CH[ch]["zones"]}


def 쓰기(종류, 왜=None, s=0.0, d=0.8, 단="본문·그림", 완화="out3", **kw):
    """장면 한 조각. 왜(정보|멈춤)를 적지 않으면 거절한다 — K-073."""
    if 종류 not in 기법:
        raise SystemExit(f"[막음] 모르는 기법 '{종류}'. 쓸 수 있는 것: {' · '.join(기법)}")
    if 왜 not in 왜값:
        raise SystemExit(f"[막음] '{종류}' 에 왜 를 적으세요 — {왜값[0]}(숫자·관계·과정을 나른다) 또는 "
                         f"{왜값[1]}(첫 1초에 눈을 붙든다). 꾸미려고 넣는 움직임은 쓰지 않아요(K-073). "
                         f"나르는 것: {기법[종류]['나르는것']}")
    return dict(종류=종류, 왜=왜, s=float(s), d=float(d), 단=단, 완화=완화, **kw)


def _esc(t):
    return (str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace("\n", "<br>"))


def _조각(c, T, i):
    """장면 하나를 (markup, 추가 css) 로. data-k/-s/-d 를 붙이면 런타임이 알아서 돌린다."""
    a = f'data-k="{c["종류"]}" data-s="{c["s"]}" data-d="{c["d"]}" data-e="{c["완화"]}"'
    z = c["단"]
    k = c["종류"]
    if k == "나타나기":
        cls = "t-ttl" if z == "제목" else ("t-lbl" if z == "상단 라벨" else "t-body")
        return f'<div class="mk {cls}" data-z="{z}" {a}>{_esc(c["글"])}</div>', ""
    if k == "숫자세기":
        # 숫자와 설명을 **한 상자 안에** 넣는다. 둘을 각각 data-z 로 내보냈더니 둘 다 구역 꼭대기에
        # 절대 배치돼 설명이 숫자 위에 겹쳤다(10/16 견본에서 눈으로 잡았다 — 구역은 안 넘겨서
        # 구역 검사에는 안 걸린다).
        suf = c.get("단위", "")
        return (f'<div class="mk" data-z="{z}">'
                f'<div class="t-num" {a} data-v="{c["값"]}" data-suf="{suf}" '
                f'data-dec="{c.get("소수", 0)}">0{suf}</div>'
                f'<div class="t-cap" data-k="나타나기" data-s="{c["s"] + c["d"]}" '
                f'data-d="0.5" data-e="out3" data-dy="18">{_esc(c.get("설명", ""))}</div></div>', "")
    if k == "막대자라기":
        최대 = c.get("최대") or max(v for _, v in c["줄"]) * 1.25
        # 이름과 숫자를 **한 줄에** 둔다. 숫자를 막대 아래에 따로 두었더니 한 줄이 172px 이 되어
        # 세 줄이 '본문·그림' 구역(350px)을 166px 넘어 AI 고지와 겹쳤다(10/16). 읽기에도 이쪽이 빠르다.
        rows = "".join(
            f'<div class="mkrow" data-k="나타나기" data-s="{c["s"] + j * 0.35}" data-d="0.4" data-e="out3">'
            f'<div class=mkhead><span class=mklab>{_esc(n)}</span>'
            f'<span class=mknum data-k="숫자세기" data-s="{c["s"] + j * 0.35 + .1}" data-d="{c["d"]}" '
            f'data-e="out3" data-v="{v}" data-suf="{c.get("단위", "%")}" data-dec="0">0</span></div>'
            f'<div class=mktrack><div class=mkfill style="--w:{v / 최대 * 100:.1f}%" '
            f'data-k="막대자라기" data-s="{c["s"] + j * 0.35 + .1}" data-d="{c["d"]}" data-e="out3"></div></div>'
            f'</div>'
            for j, (n, v) in enumerate(c["줄"]))
        return f'<div class="mk" data-z="{z}">{rows}</div>', ""
    if k == "선그리기":
        pts = c["점"]                       # [(x,y)…] 0~1 비율
        w, h = 800, 300
        dd = " ".join(("M" if j == 0 else "L") + f"{x * w:.0f} {(1 - y) * h:.0f}"
                      for j, (x, y) in enumerate(pts))
        return (f'<div class="mk" data-z="{z}"><svg class=mksvg viewBox="0 0 {w} {h}">'
                f'<path class=mkpath d="{dd}" {a}/></svg></div>', "")
    if k == "가리개열기":
        쪽 = {"왼쪽": "inset(0 VAR% 0 0)", "위": "inset(0 0 VAR% 0)",
              "가운데": "inset(0 CAL% 0 CAL%)"}[c.get("쪽", "왼쪽")]
        return (f'<div class="mk t-body" data-z="{z}" {a} data-side="{c.get("쪽", "왼쪽")}">'
                f'{_esc(c["글"])}</div>', "")
    if k == "쌓이기":
        it = "".join(f'<li data-k="나타나기" data-s="{c["s"] + j * c.get("간격", 0.45)}" '
                     f'data-d="0.45" data-e="out3" data-dy="26">{_esc(x)}</li>'
                     for j, x in enumerate(c["항목"]))
        return f'<ul class="mk mklist" data-z="{z}">{it}</ul>', ""
    if k == "원형채우기":
        return (f'<div class="mk mkdonutwrap" data-z="{z}">'
                f'<div class=mkdonut {a} data-v="{c["값"]}" style="--p:0deg"></div>'
                f'<div class=mkdonutnum data-k="숫자세기" data-s="{c["s"]}" data-d="{c["d"]}" '
                f'data-e="out3" data-v="{c["값"]}" data-suf="%" data-dec="0">0%</div>'
                f'<div class=mkdonutcap>{_esc(c.get("설명", ""))}</div></div>', "")
    if k == "낱말강조":
        앞, 낱, 뒤 = c["앞"], c["낱말"], c["뒤"]
        return (f'<div class="mk t-ttl" data-z="{z}" data-k="나타나기" data-s="{c["s"]}" data-d="0.6" '
                f'data-e="out3">{_esc(앞)}<span class=mkword {a}>{_esc(낱)}</span>{_esc(뒤)}</div>', "")
    if k == "줄바꾸기":
        return (f'<div class="mk mkswap" data-z="{z}" {a}>'
                f'<div class="mksw mksw-a">{_esc(c["앞줄"])}</div>'
                f'<div class="mksw mksw-b">{_esc(c["뒷줄"])}</div></div>', "")
    if k == "표채우기":
        머리 = "".join(f"<th>{_esc(x)}</th>" for x in c["머리"])
        몸 = ""
        n = 0
        for r in c["칸"]:
            tds = ""
            for v in r:
                tds += (f'<td data-k="나타나기" data-s="{c["s"] + n * c.get("간격", 0.18)}" '
                        f'data-d="0.3" data-e="out3" data-dy="10">{_esc(v)}</td>')
                n += 1
            몸 += f"<tr>{tds}</tr>"
        return (f'<div class="mk" data-z="{z}"><table class=mktab>'
                f'<thead><tr>{머리}</tr></thead><tbody>{몸}</tbody></table></div>', "")
    if k == "흐름선":
        단계 = c["단계"]
        bits = "".join(
            f'<div class=mkstep data-k="나타나기" data-s="{c["s"] + j * 0.5}" data-d="0.4" '
            f'data-e="out3" data-dy="20"><span class=mkdot></span>{_esc(x)}</div>'
            for j, x in enumerate(단계))
        return (f'<div class="mk mkflow" data-z="{z}">'
                f'<div class=mkline {a}></div>{bits}</div>', "")
    if k == "눈금이동":
        return (f'<div class="mk mkscale" data-z="{z}">'
                f'<div class=mkbar></div><div class=mkpin {a} data-v="{c["값"]}"></div>'
                f'<div class=mkends><span>{_esc(c.get("왼", ""))}</span>'
                f'<span>{_esc(c.get("오", ""))}</span></div>'
                f'<div class=mkscap>{_esc(c.get("설명", ""))}</div></div>', "")
    if k == "그림넘김":   # 배경층(글 뒤) — 그림 파일은 data URI 로 넣는다(임시 HTML이라 저장소에 안 남음)
        import base64
        b = base64.b64encode(open(c["그림"], "rb").read()).decode()
        return (f'<div class="mkimg" {a} style="background-image:url(data:image/jpeg;base64,{b});'
                f'background-position:{c.get("자리", "50% 40%")}"></div><div class=mkshade></div>', "")
    if k == "센표지":
        크 = c.get("크기", 118)
        줄 = "".join(f'<div class="mkbig{" hi" if j in c.get("강조", []) else ""}{" hi2" if j in c.get("강조2", []) else ""}" data-j="{j}" style="font-size:{크}px;-webkit-text-stroke:{max(8, 크 // 8)}px #000">{_esc(x)}</div>' for j, x in enumerate(c["줄"]))
        return f'<div class="mk mkcover" data-z="{z}" {a}>{줄}</div>', ""
    if k == "장면글":   # 11/3 대표 "검은 바탕 글자 작고 여백 많아": 제목·자막을 한 구역(마무리 카드)에 묶어 세로 가운데, 크게
        def _em(t): return sum(.68 if ch.isdigit() else .34 if ch == " " else .55 if ch in "·,.!?" else 1.04 for ch in t) + .25   # 11/3: G마켓 산스 숫자·가운뎃점이 넓고 외곽선이 양쪽에 붙어 '78·90·02년생'이 줄바꿈됐다
        def _tk(x): return min(c.get("크기", 132), int(830 / _em(x)))   # 11/3: 줄마다 따로(긴 연도 줄 때문에 '3위 말띠'까지 작아지지 않게)
        sk = min(c.get("자막크기", 86), int(800 / max(_em(x) for x in c["자막"].split("\n"))))
        줄 = "".join(f'<div class="mkbig{" hi" if j in c.get("강조", []) else ""}{" hi2" if j in c.get("강조2", []) else ""}" data-j="{j}" style="white-space:nowrap;font-size:{_tk(x)}px;-webkit-text-stroke:{max(8, _tk(x) // 8)}px #000">{_esc(x)}</div>' for j, x in enumerate(c["줄"]))
        낱 = "<br>".join(" ".join(f'<i class=mkw>{_esc(w)}</i>' for w in 줄_.split(" ")) for 줄_ in c["자막"].split("\n"))
        return (f'<div class="mk mkscene" data-z="{z}">'
                f'<div class="mkcover" data-k="센표지" data-s="{c["s"]}" data-d="0.5" data-e="out3">{줄}</div>'
                f'<span class="mksub" data-k="자막" data-s="{c["s"] + 0.75}" data-d="0.4" data-e="out3" style="font-size:{sk}px;margin-top:34px">{낱}</span></div>', "")
    if k == "자막":
        em = lambda t: sum(.58 if ch.isdigit() else .3 if ch == " " else .45 if ch in "·,.!?" else 1.0 for ch in t)
        크 = min(c.get("크기", 70), int(780 / max(em(x) for x in c["글"].split("\n"))))   # 한 줄이 칸을 넘으면 줄여서 줄바꿈 터짐을 막는다(11/3)
        낱 = "<br>".join(" ".join(f'<i class=mkw>{_esc(w)}</i>' for w in 줄.split(" ")) for 줄 in c["글"].split("\n"))
        return f'<div class="mk" data-z="{z}"><span class="mksub" {a} style="font-size:{크}px">{낱}</span></div>', ""
    if k == "한자찍기":   # 11/2 대표 "모션그래픽으로 시선 고정": 구역 밖 배경층(글 뒤). 0초 프레임에 이미 보인다(표지=첫 프레임)
        return (f'<div class="mkhan" {a} data-z0="{c.get("위", 380)}">{_esc(c["글자"])}</div>', "")
    if k == "기운그림":
        모양 = {
         "나무": ["M400 340 L400 40", "M400 220 L300 120", "M400 160 L500 60", "M400 110 L340 40"],
         "덩굴": ["M120 320 C220 300 200 200 300 190 S420 120 480 140 S640 60 700 40", "M300 190 C320 150 360 150 370 120", "M480 140 C500 110 540 110 550 80"],
         "해":   ["M400 300 m-110 0 a110 110 0 1 0 220 0", "M400 150 L400 70", "M290 190 L240 130", "M510 190 L560 130", "M200 300 L120 300", "M600 300 L680 300"],
         "촛불": ["M360 330 L360 200 L440 200 L440 330", "M400 200 C370 160 380 110 400 70 C420 110 430 160 400 200"],
         "산":   ["M100 330 L300 80 L420 230 L520 120 L700 330", "M300 80 L340 140 L300 160 L260 140 Z"],
         "싹":   ["M400 330 L400 170", "M400 220 C330 220 300 170 310 120 C360 120 400 160 400 220", "M400 190 C470 190 500 140 490 90 C440 90 400 130 400 190"],
         "칼":   ["M400 330 L400 60", "M340 270 L460 270", "M400 60 L380 110 M400 60 L420 110"],
         "보석": ["M400 60 L520 160 L400 330 L280 160 Z", "M280 160 L520 160", "M340 160 L400 60 L460 160 L400 330"],
        }[c["모양"]]
        간격 = c.get("간격", 0.25)
        paths = "".join(f'<path class=mkpath d="{d}" data-k="선그리기" data-s="{c["s"] + j * 간격}" data-d="{c["d"]}" data-e="out3"/>'
                        for j, d in enumerate(모양))
        return (f'<div class="mk" data-z="{z}"><svg class="mksvg mkfig" viewBox="0 0 800 350">{paths}</svg>'
                + (f'<div class="t-cap" data-k="나타나기" data-s="{c["s"] + c["d"]}" data-d="0.5" data-e="out3" data-dy="16">{_esc(c["설명"])}</div>' if c.get("설명") else "")
                + '</div>', "")
    if k == "게이지빼기":
        return (f'<div class="mk" data-z="{z}"><div class=mkgauge><div class=mkgfill {a} data-from="{c.get("부터", 100)}" data-to="{c.get("까지", 12)}"></div></div>'
                f'<div class="t-cap" data-k="나타나기" data-s="{c["s"]}" data-d="0.4" data-e="out3" data-dy="10">{_esc(c.get("설명", ""))}</div></div>', "")
    if k == "블록꽂기":
        칸 = c.get("칸", ["월", "화", "수", "목", "금"]); 자리 = c.get("자리", 2)
        cells = "".join(f'<div class=mkday>{_esc(x)}<i></i><i></i></div>' for x in 칸)
        return (f'<div class="mk" data-z="{z}"><div class=mkweek>{cells}'
                f'<div class=mkblock {a} data-col="{자리}" data-n="{len(칸)}">{_esc(c["글"])}</div></div></div>', "")
    raise SystemExit(f"[막음] '{k}' 의 그리는 길이 아직 없어요")


# ── 런타임: 기법마다 진행도 g(0~1)를 어떻게 쓰는지만 적는다 ──────────────────
RUNTIME = """
const CL=(x)=>x<0?0:x>1?1:x;
const EASE={
  lin:(x)=>CL(x),
  out3:(x)=>1-Math.pow(1-CL(x),3),
  out5:(x)=>1-Math.pow(1-CL(x),5),
  inout:(x)=>{x=CL(x);return x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2;},
  back:(x)=>{x=CL(x);const c=1.6;return 1+(c+1)*Math.pow(x-1,3)+c*Math.pow(x-1,2);}
};
const AP={
  "나타나기":(el,g)=>{const dy=+(el.dataset.dy||40);
     el.style.opacity=g; el.style.transform=`translateY(${(1-g)*dy}px)`;},
  "숫자세기":(el,g)=>{const v=+el.dataset.v, d=+(el.dataset.dec||0);
     el.textContent=(g*v).toFixed(d)+(el.dataset.suf||''); el.style.opacity=g>0?1:0;},
  "막대자라기":(el,g)=>{el.style.width=`calc(${g} * var(--w))`;},
  "선그리기":(el,g)=>{const L=el.getTotalLength();
     el.style.strokeDasharray=L; el.style.strokeDashoffset=L*(1-g); el.style.opacity=g>0?1:0;},
  "가리개열기":(el,g)=>{const s=el.dataset.side||'왼쪽', r=(1-g)*100;
     el.style.clipPath = s==='위' ? `inset(0 0 ${r}% 0)`
       : s==='가운데' ? `inset(0 ${r/2}% 0 ${r/2}%)` : `inset(0 ${r}% 0 0)`;
     el.style.opacity=g>0?1:0;},
  "원형채우기":(el,g)=>{el.style.setProperty('--p',(g*(+el.dataset.v)*3.6)+'deg'); el.style.opacity=g>0?1:0;},
  "낱말강조":(el,g)=>{el.style.transform=`scale(${1+g*0.14})`;
     el.style.setProperty('--u',(g*100)+'%');},
  "줄바꾸기":(el,g)=>{const a=el.querySelector('.mksw-a'), b=el.querySelector('.mksw-b');
     const h=CL((g-0.45)/0.3);
     a.style.opacity=1-h; a.style.transform=`translateY(${-h*26}px)`;
     b.style.opacity=h;   b.style.transform=`translateY(${(1-h)*26}px)`;},
  "표채우기":(el,g)=>{el.style.opacity=g>0?1:0;},
  "흐름선":(el,g)=>{el.style.transform=`scaleX(${g})`;},
  "그림넘김":(el,g)=>{el.style.transform=`scale(${1.0+0.12*g})`; el.style.opacity=1;},
  "센표지":(el,g,t)=>{const s0=+el.dataset.s; el.style.opacity=1;
     const L=[...el.querySelectorAll('.mkbig')];
     if(s0<0){ // 표지: 0초 프레임에 이미 다 보인다(K-139). 0.15초부터 줄마다 한 번씩 쾅 펄스
       L.forEach((x,j)=>{const u=CL((t-0.15-j*0.12)/0.28), k=Math.sin(u*Math.PI); x.style.transform=`scale(${1+0.14*k}) rotate(${(j%2?1:-1)*2.5*k}deg)`;});
       return;}
     L.forEach((x,j)=>{const hi=x.classList.contains('hi')||x.classList.contains('hi2'); const st=j*0.16+(hi?0.08:0);
       const u=CL((t-s0-st)/0.32), b=EASE.back(u); x.style.opacity=u>0?1:0;
       x.style.transform=`translateY(${(1-b)*-60}px) scale(${(hi?1.9:1.5)-(hi?0.9:0.5)*b}) rotate(${(1-b)*(j%2?6:-6)}deg)`;
       if(hi&&u>=1){const w=CL((t-s0-st-0.32)/0.25); x.style.transform+=` translateX(${Math.sin(w*Math.PI*6)*(1-w)*10}px)`;}});},
  "자막":(el,g,t)=>{const s0=+el.dataset.s; el.style.opacity=t>=s0?1:0; el.style.transform=`scaleY(${0.6+0.4*EASE.back(CL((t-s0)/0.25))})`;
     [...el.querySelectorAll('.mkw')].forEach((w,i)=>{const u=CL((t-s0-0.12-i*0.09)/0.22), b=EASE.back(u);
       w.style.opacity=u>0?1:0; w.style.transform=`translateY(${(1-b)*26}px) scale(${0.7+0.3*b})`;
       w.style.color = (u>0&&u<1)?'#FFD43B':'#fff';});},
  "한자찍기":(el,g)=>{const b=EASE.back(g); el.style.transform=`translateX(-50%) scale(${1.35-0.35*b}) rotate(${(1-b)*-6}deg)`;
     el.style.opacity = Math.max(0.16, 0.7 - 0.55*CL((window.__t||0)/0.9));},
  "게이지빼기":(el,g)=>{const a=+el.dataset.from, b=+el.dataset.to, v=a+(b-a)*g;
     el.style.width=v+'%'; el.classList.toggle('low', v<30);
     el.parentNode.style.transform = v<30 ? `translateX(${Math.sin(g*80)*5}px)` : 'none';},
  "블록꽂기":(el,g)=>{const c=+el.dataset.col, n=+el.dataset.n, b=EASE.back(g);
     const dd=el.parentNode.querySelectorAll('.mkday')[c]; el.style.left=(dd.offsetLeft+dd.offsetWidth/2)+'px'; el.style.top=`${-420+(420+90)*b}px`;
     el.style.transform=`rotate(${(1-b)*-10}deg)`; el.style.opacity=g>0?1:0;},
  "눈금이동":(el,g)=>{el.style.left=`calc(${g*(+el.dataset.v)}% - 18px)`; el.style.opacity=g>0?1:0;}
};
const MK=[...document.querySelectorAll('[data-k]')];
const END=+(document.body.dataset.end||0);
window.seek=(t)=>{ window.__t=t;
  if(END){const o=CL((t-(END-0.25))/0.25), e=o*o*o; const sf=document.querySelector('.safe');
    sf.style.transform=`translateX(${-e*1100}px) skewX(${-o*10}deg)`; sf.style.opacity=1-o*.3;
    const h=document.querySelector('.mkhan'); if(h) h.style.marginLeft=(-e*600)+'px';}
  for(const el of MK){
    const s=+el.dataset.s, d=+el.dataset.d||0.8, k=el.dataset.k;
    const g=(EASE[el.dataset.e||'out3'])((t-s)/d);
    (AP[k]||AP['나타나기'])(el,g,t);
  }
};
window.seek(0);
"""


def _tone(bg):
    """밝은 판에서는 고정 요소를 짙게 바꾼다 — 금색 글씨가 크림·흰 바탕에서 안 보인다.
    기준(.38)은 2026-igcover/build.py 와 같은 값을 쓴다. 처음에 늘 dark 로 두었더니
    흰 판(k_white_s)에서 상단 오른쪽 '동서양 6개 운명학 교차분석'이 아예 안 보였다(10/16)."""
    h = str(bg).lstrip("#")
    r, g, b = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    f = lambda c: c / 12.92 if c <= .04045 else ((c + .055) / 1.055) ** 2.4
    return "light" if (.2126 * f(r) + .7152 * f(g) + .0722 * f(b)) >= .38 else "dark"


def _css(T, ch):
    Z = _단(ch)
    C = CS.CH[ch]
    sx0, sy0, sx1, sy1 = C["safe"]
    # 구역 하나하나를 CSS 로 — 자리를 손으로 적지 않게 한다
    단자리 = "\n".join(
        f'.mk[data-z="{n}"]{{position:absolute;left:{x0 - sx0}px;top:{y0 - sy0}px;'
        f'width:{x1 - x0}px}}'   # max-height 를 두지 않는다 — 안 보이게 가둘 뿐 검사가 못 잡는다
        for n, (x0, y0, x1, y1) in Z.items())
    return f"""
{K.css_inline(display="gm" if ch in ("reel", "naver_clip") else "pl")}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:{C['w']}px;height:{C['h']}px;background:{T['bg']};overflow:hidden;
     font-family:'JW-B',sans-serif;color:{T['ink']};-webkit-font-smoothing:antialiased}}
.safe{{position:absolute;left:{sx0}px;top:{sy0}px;width:{sx1 - sx0}px;height:{sy1 - sy0}px}}
{단자리}
.t-ttl{{font-family:'JW-D',sans-serif;font-size:100px;line-height:1.3;letter-spacing:-.01em}}
.t-body{{font-size:56px;line-height:1.5}}
.t-lbl{{font-size:38px;color:{T['sub']}}}
.t-cap{{font-size:46px;color:{T['sub']};line-height:1.5;margin-top:8px}}
.t-num{{font-family:'JW-D',sans-serif;font-size:170px;line-height:1.1;color:{T['acc']}}}
/* 막대 */
.mkrow{{margin-bottom:22px}}
.mkrow:last-child{{margin-bottom:0}}
.mkhead{{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:8px}}
.mklab{{font-size:42px;color:{T['sub']}}}
.mknum{{font-family:'JW-D',sans-serif;font-size:48px;color:{T['acc']}}}
.mktrack{{height:26px;background:{T['card']};border-radius:13px;overflow:hidden}}
.mkfill{{height:100%;width:0;background:{T['acc']};border-radius:13px}}
/* 선 */
.mksvg{{width:100%;height:300px;overflow:visible}}
.mkpath{{fill:none;stroke:{T['acc']};stroke-width:10;stroke-linecap:round;stroke-linejoin:round}}
/* 목록 */
.mklist{{list-style:none}}
.mklist li{{font-size:54px;line-height:1.5;margin-bottom:22px;padding-left:46px;position:relative}}
.mklist li:before{{content:'';position:absolute;left:0;top:26px;width:22px;height:22px;
  border-radius:11px;background:{T['acc']}}}
/* 원 */
.mkdonutwrap{{text-align:center}}
/* 크기는 '본문·그림' 구역(350px) 안에 들어가야 한다 — 처음에 300px 로 두었다가
   구역을 43px 넘겨 검사에 막혔다(10/16). 230 + 숫자 + 설명 두 줄 = 343px. */
.mkdonut{{width:230px;height:230px;margin:0 auto;border-radius:50%;
  background:conic-gradient({T['acc']} var(--p),{T['card']} 0);
  -webkit-mask:radial-gradient(circle,transparent 74px,#000 75px);
          mask:radial-gradient(circle,transparent 74px,#000 75px)}}
.mkdonutnum{{font-family:'JW-D',sans-serif;font-size:68px;color:{T['acc']};margin-top:-152px}}
.mkdonutcap{{font-size:40px;color:{T['sub']};margin-top:74px;line-height:1.45}}
/* 낱말 */
.mkword{{display:inline-block;color:{T['acc']};background:
  linear-gradient(to top,{T['acc']}33 var(--u,0%),transparent var(--u,0%))}}
/* 줄 바꾸기 */
.mkswap{{position:relative}}
.mksw{{font-family:'JW-D',sans-serif;font-size:84px;line-height:1.3}}
.mksw-a{{color:{T['sub']}}}
.mksw-b{{position:absolute;left:0;top:0;color:{T['acc']};opacity:0}}
/* 표 */
.mktab{{width:100%;border-collapse:collapse;font-size:40px}}
.mktab th{{text-align:left;color:{T['sub']};font-weight:400;padding:10px 8px;
  border-bottom:2px solid {T['card']}}}
.mktab td{{padding:14px 8px;border-bottom:1px solid {T['card']}}}
/* 흐름 */
.mkflow{{position:relative;padding-left:40px}}
.mkline{{position:absolute;left:11px;top:14px;width:4px;height:calc(100% - 28px);
  background:{T['acc']};transform-origin:top;transform:scaleX(0)}}
.mkstep{{font-size:50px;line-height:1.5;margin-bottom:26px;position:relative}}
.mkdot{{position:absolute;left:-40px;top:16px;width:26px;height:26px;border-radius:13px;
  background:{T['acc']}}}
/* 눈금 */
.mkscale{{position:relative;padding-top:40px}}
.mkbar{{height:18px;border-radius:9px;background:{T['card']}}}
.mkpin{{position:absolute;top:28px;left:-18px;width:36px;height:36px;border-radius:18px;
  background:{T['acc']};box-shadow:0 0 0 8px {T['bg']}}}
.mkends{{display:flex;justify-content:space-between;margin-top:34px;font-size:36px;color:{T['sub']}}}
.mkscap{{font-size:44px;color:{T['sub']};margin-top:28px;line-height:1.5}}
body{{background:radial-gradient(120% 70% at 50% 40%,{T['card']} 0%,{T['bg']} 55%,{T['bg']} 100%)}}
.mkstars{{position:absolute;inset:0;z-index:0;background-image:radial-gradient(2px 2px at 12% 18%,{T['ink']}55 50%,transparent 51%),radial-gradient(3px 3px at 78% 12%,{T['ink']}44 50%,transparent 51%),radial-gradient(2px 2px at 30% 72%,{T['ink']}44 50%,transparent 51%),radial-gradient(3px 3px at 88% 64%,{T['ink']}33 50%,transparent 51%),radial-gradient(2px 2px at 55% 88%,{T['ink']}44 50%,transparent 51%),radial-gradient(2px 2px at 8% 52%,{T['ink']}33 50%,transparent 51%)}}
.mkimg{{position:absolute;inset:0;background-size:cover;z-index:0;transform-origin:50% 45%}}
.mkshade{{position:absolute;inset:0;z-index:1;background:linear-gradient(180deg,rgba(0,0,0,.35) 0%,rgba(0,0,0,0) 30%,rgba(0,0,0,0) 60%,rgba(0,0,0,.45) 100%)}}
.mkcover{{text-align:center}}
.mk.mkcover[data-z="마무리 카드"]{{display:flex;flex-direction:column;justify-content:center;height:{Z.get("마무리 카드", (0,0,0,890))[3] - Z.get("마무리 카드", (0,0,0,0))[1]}px}}
.mkscene{{display:flex;flex-direction:column;align-items:center;justify-content:center;height:{Z.get("마무리 카드", (0,0,0,890))[3] - Z.get("마무리 카드", (0,0,0,0))[1]}px}}
.mkbig{{font-family:'JW-D',sans-serif;font-size:118px;line-height:1.1;color:#fff;-webkit-text-stroke:14px #000;paint-order:stroke fill;text-shadow:0 6px 0 #000}}
.mkbig.hi{{color:#FFD43B}} .mkbig.hi2{{color:#FF4D4D}}
.mkw{{display:inline-block;font-style:normal}}
.mksub{{transform-origin:50% 50%;display:inline-block;font-family:'JW-B',sans-serif;font-weight:800;font-size:70px;line-height:1.35;color:#fff;background:rgba(0,0,0,.72);padding:14px 28px;border-radius:14px}}
.mkhan{{position:absolute;left:475px;top:860px;font-family:serif;font-size:560px;line-height:1;color:{T['acc']};z-index:0;transform-origin:50% 60%}}
.safe{{z-index:2}}
.mkfig{{height:320px}}
.mkgauge{{height:110px;border:8px solid {T['ink']};border-radius:24px;padding:10px;position:relative;width:720px;margin:0 auto}}
.mkgauge:after{{content:'';position:absolute;right:-26px;top:28px;width:16px;height:38px;border-radius:0 8px 8px 0;background:{T['ink']}}}
.mkgfill{{height:100%;border-radius:12px;background:{T['acc']}}}
.mkgfill.low{{background:#E07A5F}}
.mkweek{{position:relative;display:flex;gap:14px;justify-content:center}}
.mkday{{width:140px;height:240px;border-radius:18px;background:{T['card']};font-family:'JW-D',sans-serif;font-size:40px;color:{T['sub']};text-align:center;padding-top:16px}}
.mkday i{{display:block;margin:16px 14px 0;height:30px;border-radius:8px;background:{T['bg']};opacity:.6}}
.mkblock{{position:absolute;white-space:nowrap;font-family:'JW-D',sans-serif;font-size:44px;background:{T['acc']};color:{T['bg']};border-radius:999px;padding:16px 30px;opacity:0;transform-origin:50% 50%;margin-left:0;translate:-50% 0}}
{BF.css(_tone(T['bg']))}
{".mk{text-align:center} .mklist,.mkflow{display:inline-block;text-align:left} .mkhead{justify-content:center;gap:24px} .mksw-b{left:0;right:0} .mktab th{text-align:center}" if C.get("align") == "center" else ""}
"""


def 페이지(장면, 판="dg_gold_s", ch="reel", ai=True, 끝=None, 상단줄=True):
    """장면 목록을 완성된 HTML 한 장으로. 고정 요소·글꼴·판은 기존 단일 출처에서 가져온다."""
    if 판 not in PAL:
        raise SystemExit(f"[막음] 모르는 판 '{판}'. assets/palettes/color_combos.json 에서 고르세요")
    T = PAL[판]["theme"]
    # 구역은 절대 배치다 — 같은 단을 두 번 쓰면 둘이 꼭대기에서 겹친다.
    # 한 단에는 한 조각만. 두 가지를 같이 보여야 하면 더 넓은 단('마무리 카드')을 쓴다.
    본 = {}
    for c in 장면:
        if c["종류"] in ("한자찍기", "그림넘김"):   # 배경층 — 구역을 차지하지 않는다
            continue
        if c["단"] in 본:
            raise SystemExit(f"[막음] '{c['단']}' 단을 두 번 썼어요 — '{본[c['단']]}' 와 '{c['종류']}' 가 "
                             f"같은 자리에 겹칩니다. 한 단에는 한 조각만 두거나 더 넓은 단('마무리 카드')을 쓰세요.")
        본[c["단"]] = c["종류"]
    몸, 덧, 뒤 = [], [], []
    for i, c in enumerate(장면):
        m, x = _조각(c, T, i)
        (뒤 if c["종류"] in ("한자찍기", "그림넘김") else 몸).append(m)   # 배경층은 안전 영역 밖(글 뒤)
        if x:
            덧.append(x)
    return (f"<!doctype html><html><head><meta charset=utf-8><style>{_css(T, ch)}"
            f"{''.join(덧)}</style></head><body>"
            f"<div class=mkstars></div>{''.join(뒤)}<div class=safe>{''.join(몸)}</div>{BF.html(ch, ai=ai, tone=_tone(T['bg'])) if 상단줄 else ''}"
            f"<script>{RUNTIME}</script></body></html>").replace("<body>", f'<body data-end="{끝 or 0}">', 1)


def 만들기(이름, 장면, 판="dg_gold_s", 초=8.0, fps=30, ch="reel"):
    """장면 → MP4. **중간 HTML 은 임시 폴더에 쓰고 지운다.**
    글꼴을 base64 로 박기 때문에 HTML 한 장이 39MB 다 — 저장소에 두면 열세 편에 500MB 가 된다(10/16).
    남는 것은 MP4 하나뿐이고, 같은 장면이면 언제든 똑같이 다시 뽑힌다."""
    import tempfile, html_motion as HM
    d = tempfile.mkdtemp(prefix="mk_")
    try:
        p = os.path.join(d, 이름 + ".html")
        open(p, "w", encoding="utf-8").write(페이지(장면, 판=판, ch=ch))
        return HM.render(p, 이름, 초=초, fps=fps, ch=ch)
    finally:
        import shutil
        shutil.rmtree(d, ignore_errors=True)


# ── 표 보기 · 견본 ───────────────────────────────────────────────────────────
def 표():
    out = [f"모션 기법 {len(기법)}가지 — 움직임은 정보를 나르거나 스크롤을 멈출 때만(K-073)", ""]
    out.append(f"{'기법':<12} {'쓸 곳':<26} 나르는 것")
    out.append("-" * 86)
    for k, v in 기법.items():
        out.append(f"{k:<12} {v['쓸곳']:<26} {v['나르는것']}")
    out += ["", "내용 유형 → 권장 기법", "-" * 86]
    for k, v in 기법표.items():
        out.append(f"{k:<16} {' · '.join(v)}")
    return "\n".join(out)


def 견본():
    """기법마다 한 장면씩. 새 기법을 넣으면 여기서 눈으로 확인한다."""
    import html_motion as HM
    묶음 = [
     ("mk-나타나기", "dg_gold_s", [
       쓰기("나타나기", 왜="멈춤", s=.1, d=.7, 단="제목", 글="같은 나를 두고\n왜 말이 다를까요?"),
       쓰기("나타나기", 왜="정보", s=.9, d=.6, 단="본문·그림", 글="여섯 가지를 겹쳐서 봐요")]),
     ("mk-숫자세기", "p_red_s", [
       쓰기("나타나기", 왜="멈춤", s=.1, d=.6, 단="제목", 글="셋 중 하나는\n같은 말을 들어요"),
       쓰기("숫자세기", 왜="정보", s=.9, d=1.4, 단="본문·그림", 값=24, 단위="%",
            설명="사주와 하락이수가 같은 말을 한 사람")]),
     ("mk-막대자라기", "y_olive_s", [
       쓰기("나타나기", 왜="멈춤", s=.1, d=.6, 단="제목", 글="어느 둘이\n제일 닮았을까요?"),
       쓰기("막대자라기", 왜="정보", s=1.0, d=1.1, 단="본문·그림", 최대=30,
            줄=[("사주와 하락이수", 24), ("사주와 별자리", 17), ("사주와 숫자", 14)])]),
     ("mk-선그리기", "w_navy", [
       쓰기("나타나기", 왜="멈춤", s=.1, d=.6, 단="제목", 글="한 해 동안\n어떻게 움직였나"),
       쓰기("선그리기", 왜="정보", s=.9, d=1.6, 단="본문·그림",
            점=[(0, .2), (.25, .45), (.5, .35), (.75, .75), (1, .6)])]),
     ("mk-가리개열기", "m_soft", [
       쓰기("나타나기", 왜="멈춤", s=.1, d=.6, 단="제목", 글="가린 쪽부터\n열어 볼게요"),
       쓰기("가리개열기", 왜="정보", s=.9, d=1.2, 단="본문·그림", 쪽="왼쪽",
            글="태어난 날의 첫 글자가\n성격의 바탕이 돼요")]),
     ("mk-쌓이기", "k_white_s", [
       쓰기("나타나기", 왜="멈춤", s=.1, d=.6, 단="제목", 글="오늘 해 볼 것\n세 가지"),
       쓰기("쌓이기", 왜="정보", s=.9, d=.45, 단="본문·그림", 간격=.5,
            항목=["한 가지만 내려놓기", "먼저 기대 보기", "내 것을 맨 앞에 두기"])]),
     ("mk-원형채우기", "p_black_s", [
       쓰기("나타나기", 왜="멈춤", s=.1, d=.6, 단="제목", 글="열 명 중\n몇 명일까요?"),
       쓰기("원형채우기", 왜="정보", s=.9, d=1.4, 단="본문·그림", 값=24,
            설명="세 가지 이상이 같은 말을 한 사람")]),
     ("mk-낱말강조", "m_young_s", [
       쓰기("낱말강조", 왜="멈춤", s=.2, d=1.0, 단="제목",
            앞="맞는 말이 ", 낱말="세게", 뒤=" 들릴 때가 있어요"),
       쓰기("나타나기", 왜="정보", s=1.2, d=.6, 단="본문·그림", 글="말한 뒤 한 번만 더 들어 보세요")]),
     ("mk-줄바꾸기", "y_black_s", [
       쓰기("나타나기", 왜="멈춤", s=.1, d=.5, 단="상단 라벨", 글="흔한 오해"),
       쓰기("줄바꾸기", 왜="정보", s=.6, d=1.8, 단="제목",
            앞줄="안 맞으면 틀린 거예요", 뒷줄="안 맞는 쪽도 답이에요")]),
     ("mk-표채우기", "dg_gold_s", [
       쓰기("나타나기", 왜="멈춤", s=.1, d=.6, 단="제목", 글="여섯 가지가\n뭐라고 했나"),
       쓰기("표채우기", 왜="정보", s=.9, d=.18, 단="본문·그림", 간격=.2,
            머리=["운명학", "한 말"],
            칸=[["사주", "밀고 가는 힘"], ["하락이수", "멈추기 어려움"], ["별자리", "곧게 자람"]])]),
     ("mk-흐름선", "k_neon", [
       쓰기("나타나기", 왜="멈춤", s=.1, d=.6, 단="제목", 글="1분이면\n끝나요"),
       쓰기("흐름선", 왜="정보", s=.9, d=1.6, 단="본문·그림",
            단계=["생년월일 넣기", "여섯 가지 겹쳐 보기", "같은 말 찾기"])]),
     ("mk-눈금이동", "p_red_s", [
       쓰기("나타나기", 왜="멈춤", s=.1, d=.6, 단="제목", 글="나는\n어디쯤일까요?"),
       쓰기("눈금이동", 왜="정보", s=.9, d=1.5, 단="본문·그림", 값=72,
            왼="드문 쪽", 오="흔한 쪽", 설명="같은 괘를 가진 사람이 100명 중 72명")]),
    ]
    out = os.path.join(ROOT, "2026-motion", "html")
    os.makedirs(out, exist_ok=True)
    만든것 = []
    다시 = "--다시" in sys.argv
    for 이름, 판, 장면 in 묶음:
        if not 다시 and os.path.exists(os.path.join(out, 이름 + ".mp4")):
            print(f"  {이름:<16} 이미 있음 (다시 뽑으려면 --다시)", flush=True)
            continue
        mp4, dur = 만들기(이름, 장면, 판=판, 초=3.6, fps=30)
        만든것.append((이름, 판, mp4, dur))
        print(f"  {이름:<16} {판:<12} {dur:.1f}초", flush=True)
    return 만든것


def main():
    if "--견본" in sys.argv:
        견본()
        return 0
    print(표())
    return 0


if __name__ == "__main__":
    sys.exit(main())
