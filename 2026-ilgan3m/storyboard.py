"""일간 3회차 모션 판(ilgan3m) 스토리보드 — 영상을 만들기 전에 대표 승인을 받는 한 장 그림.

왜: to-content 11/2 19:55 CT 항목(대표 19:48 "모션그래픽도 쓰고 시선 고정되게, 겁나 심심하잖아")과
    11/2 20:15 알림 "스토리보드를 먼저 앱 카드로 올려 대표 승인 뒤 영상".
무엇: 8편(갑~신) × 6장면. 장면마다 motion_kit 기법으로 실제 페이지를 만들고, 장면 끝 시각의 한 프레임을 찍어
      썸네일로 쓴다(그림으로 짐작한 견본이 아니라 키트가 그린 진짜 화면).
글: 2026-ilgan3/build.py REELS 문장을 그대로 쓴다(이미 copy_rules 첫줄검사·capfix 통과). 새 문장을 짓지 않는다.
같은 장면 틀 반복 금지(K-007): 기운그림 8가지가 모두 다르고, '까닭'·'해 볼 것' 장면 기법 짝이 편마다 다르다.

실행: python3 2026-ilgan3m/storyboard.py   → 2026-ilgan3m/storyboard_ilgan3m.jpg (+ sb_<id>.jpg 8장)
"""
import os, sys, json, asyncio, tempfile, shutil, importlib.util
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(ROOT, "pipeline"))
import motion_kit as M, channel_specs as CS, fonts_kit as K  # noqa: E402

# 3회차 문장 그대로 읽기 (build.py 를 실행하지 않고 REELS 표만 가져온다)
_src = open(os.path.join(ROOT, "2026-ilgan3", "build.py"), encoding="utf-8").read()
_s = _src.index("GAN = "); _e = _src.index("# 2회차 문장과")
_ns = {}; exec(_src[_s:_e], _ns)
GAN, REELS = _ns["GAN"], _ns["REELS"]

기운 = {"gab": "나무", "eul": "덩굴", "byeong": "해", "jeong": "촛불", "mu": "산", "gi": "싹", "gyeong": "칼", "sin": "보석"}
그림말 = {"나무": "나무가 위로 자람", "덩굴": "덩굴이 옆으로 뻗음", "해": "해가 떠오름", "촛불": "촛불이 켜짐",
         "산": "산이 솟음", "싹": "씨앗에서 싹이 남", "칼": "칼날에 빛이 섬", "보석": "보석 면이 그려짐"}

# 3회차 정지판의 v_* 판(v_emerald·v_violet·v_choco)은 color_combos 에 모션용 theme 이 없다 → theme 있는 판으로 바꿔 쓴다.
# 같은 판이 두 편에 겹치지 않게 고른다.
판 = {"gab": "dg_gold", "eul": "g_ivory", "byeong": "m_young", "jeong": "p_purple", "mu": "y_olive",
      "gi": "k_gold", "gyeong": "w_ink", "sin": "w_navy_butter"}


def 두줄(*줄):
    """글을 두 줄로(이미 두 줄이면 그대로). 한 줄이면 가운데에 가까운 띄어쓰기에서 자른다."""
    if len(줄) == 1:
        t = 줄[0]; sp = [i for i, ch in enumerate(t) if ch == " "]
        if not sp:
            return t
        m = min(sp, key=lambda i: abs(i - len(t) / 2))
        return t[:m] + "\n" + t[m + 1:]
    return "\n".join(줄)


def 크(글, 최대=100, 폭=800):
    """긴 줄 글자 수로 크기를 정한다(한 글자 ≈ 1em). 제목 칸 폭 850px 안에 들게."""
    n = max(len(x) for x in 글.split("\n"))
    return min(최대, int(폭 / max(n, 1)))


def 까닭(r):
    a, b = r["why"]
    k = {"gab": "게이지빼기", "eul": "게이지빼기", "byeong": "가리개열기", "jeong": "낱말강조",
         "mu": "낱말강조", "gi": "게이지빼기", "gyeong": "가리개열기", "sin": "낱말강조"}[r["id"]]
    if k == "게이지빼기":
        return k, [M.쓰기("나타나기", 왜="멈춤", s=.1, d=.5, 단="제목", 글=f"{a}\n{b}", 크기=크(f"{a}\n{b}")),
                   M.쓰기("게이지빼기", 왜="정보", s=.6, d=2.2, 단="본문·그림", 부터=100, 까지=15, 설명="")]
    if k == "줄바꾸기":
        return k, [M.쓰기("줄바꾸기", 왜="정보", s=.3, d=2.0, 단="제목", 앞줄=a, 뒷줄=b, 크기=min(84, 크(a + "\n" + b)))]
    if k == "가리개열기":
        return k, [M.쓰기("가리개열기", 왜="정보", s=.3, d=1.6, 단="제목", 쪽="왼쪽", 글=f"{a}\n{b}", 크기=크(f"{a}\n{b}"))]
    # 낱말강조: 뒷줄의 무게 실린 낱말
    낱 = {"mu": ("버티는 게 익숙해서\n", "힘든 티를", " 안 내요"),
          "sin": ("다듬느라 끝내는 날이\n", "늦어지기도 해요", ""),
          "jeong": ("챙긴 만큼 안 돌아오면\n", "서운해지기도 해요", "")}[r["id"]]
    return k, [M.쓰기("낱말강조", 왜="정보", s=.3, d=1.4, 단="제목", 앞=낱[0], 낱말=낱[1], 뒤=낱[2].replace(" ", "\u00a0", 1), 크기=크(낱[0] + 낱[1] + 낱[2]))]


def 해볼것(r):
    a, b = r["todo"]
    k = {"gab": "블록꽂기", "eul": "낱말강조", "byeong": "블록꽂기", "jeong": "가리개열기",
         "mu": "흐름선", "gi": "쌓이기", "gyeong": "흐름선", "sin": "눈금이동"}[r["id"]]
    라벨 = M.쓰기("나타나기", 왜="정보", s=.1, d=.4, 단="상단 라벨", 글="오늘 해 볼 것")
    if k == "블록꽂기":
        칸, 자리, 글 = ({"gab": (["월", "화", "수", "목", "금"], 2, "쉬는 시간"),
                       "byeong": (["아침", "점심", "저녁", "밤"], 2, "혼자 30분")})[r["id"]]
        return k, [라벨, M.쓰기("나타나기", 왜="멈춤", s=.2, d=.5, 단="제목", 글=f"{a}\n{b}", 크기=크(f"{a}\n{b}")),
                   M.쓰기("블록꽂기", 왜="정보", s=.9, d=1.0, 단="본문·그림", 칸=칸, 자리=자리, 글=글)]
    if k == "낱말강조":
        return k, [라벨, M.쓰기("낱말강조", 왜="정보", s=.3, d=1.4, 단="제목", 앞="원하는 것 하나를\n", 낱말="먼저", 뒤="\u00a0말해 보세요", 크기=크("원하는 것 하나를\n먼저 말해 보세요"))]
    if k == "가리개열기":
        return k, [라벨, M.쓰기("가리개열기", 왜="정보", s=.3, d=1.4, 단="제목", 쪽="왼쪽", 글=f"{a}\n{b}", 크기=크(f"{a}\n{b}"))]
    if k == "흐름선":
        단계 = {"mu": ["힘든 것 하나", "말로 꺼내기"], "gyeong": ["좋은 점 하나", "그다음 할 말"]}[r["id"]]
        return k, [라벨, M.쓰기("나타나기", 왜="멈춤", s=.2, d=.5, 단="제목", 글=f"{a}\n{b}", 크기=크(f"{a}\n{b}")),
                   M.쓰기("흐름선", 왜="정보", s=.9, d=1.4, 단="본문·그림", 단계=단계)]
    if k == "쌓이기":
        return k, [라벨, M.쓰기("나타나기", 왜="멈춤", s=.2, d=.5, 단="제목", 글=f"{a}\n{b}", 크기=크(f"{a}\n{b}")),
                   M.쓰기("쌓이기", 왜="정보", s=.9, d=.45, 단="본문·그림", 간격=.5, 항목=["뒷정리", "설거지", "자리 정돈"])]
    return k, [라벨, M.쓰기("나타나기", 왜="멈춤", s=.2, d=.5, 단="제목", 글=f"{a}\n{b}", 크기=크(f"{a}\n{b}")),
               M.쓰기("눈금이동", 왜="정보", s=.9, d=1.5, 단="본문·그림", 값=80, 왼="0점", 오="100점", 설명="여기서 마치기")]


def 편(r):
    g = GAN[r["i"]]; 모양 = 기운[r["id"]]
    k4, s4 = 까닭(r); k5, s5 = 해볼것(r)
    return [
        dict(이름="표지", 초=(0, 2.4), 기법="한자찍기 + 나타나기",
             움직임=f"0초에 훅 글자·{g} 다 보임 → 0.3초 한자 쾅 뒤로 물러남",
             장면=[M.쓰기("한자찍기", 왜="멈춤", s=0, d=.9, 글자=g, 위=1000),
                   M.쓰기("나타나기", 왜="멈춤", s=-1, d=.01, 단="제목", 글="\n".join(r["hook"]), 크기=크("\n".join(r["hook"]), 118))], 상단줄=False),
        dict(이름="둘째 줄", 초=(2.4, 5.0), 기법="나타나기 ×2",
             움직임="둘째 줄 → 태어난 날 첫 글자 알림",
             장면=[M.쓰기("나타나기", 왜="정보", s=.1, d=.5, 단="제목", 글=두줄(r["sub"]), 크기=크(두줄(r["sub"]))),
                   M.쓰기("나타나기", 왜="정보", s=.8, d=.5, 단="본문·그림", 글=f"태어난 날 첫 글자가\n{r['name']}({g})인 분")]),
        dict(이름="기운", 초=(5.0, 9.0), 기법="기운그림",
             움직임=그림말[모양],
             장면=[M.쓰기("나타나기", 왜="정보", s=.1, d=.4, 단="상단 라벨", 글=f"{r['name']}({g})"),
                   M.쓰기("나타나기", 왜="정보", s=.2, d=.5, 단="제목", 글=두줄(r["gi"]), 크기=크(두줄(r["gi"]))),
                   M.쓰기("기운그림", 왜="정보", s=.7, d=.9, 단="본문·그림", 모양=모양)]),
        dict(이름="까닭", 초=(9.0, 13.0), 기법=k4, 움직임="", 장면=s4),
        dict(이름="해 볼 것", 초=(13.0, 17.0), 기법=k5, 움직임="", 장면=s5),
        dict(이름="끝", 초=(17.0, 18.5), 기법="나타나기", 움직임="마지막 1초 행동",
             장면=[M.쓰기("나타나기", 왜="정보", s=.1, d=.4, 단="마무리 카드",
                        글="맞으면 ♥\n\n프로필 링크에서\n생년월일만 넣으면\n내 첫 글자 1초 확인")]),
    ]


async def 찍기(목록, out_dir):
    from playwright.async_api import async_playwright
    C = CS.CH["reel"]
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": C["w"], "height": C["h"]})
        for path, t, png in 목록:
            await pg.goto("file://" + path)
            await pg.wait_for_function("typeof window.seek === 'function'")
            await pg.evaluate("t => window.seek(t)", t)
            await pg.wait_for_timeout(60)
            await pg.screenshot(path=png, type="jpeg", quality=80)
        await b.close()


def main():
    tmp = tempfile.mkdtemp(prefix="sb3m_")
    목록, 표 = [], []
    try:
        for r in REELS:
            sc = 편(r)
            for j, s in enumerate(sc):
                html = M.페이지(s["장면"], 판=판[r["id"]], ch="reel", 상단줄=s.get("상단줄", True))
                p = os.path.join(tmp, f"{r['id']}_{j}.html")
                open(p, "w", encoding="utf-8").write(html)
                t = 0.0 if j == 0 else (s["초"][1] - s["초"][0]) - 0.2
                목록.append((p, t, os.path.join(tmp, f"{r['id']}_{j}.jpg")))
            표.append((r, sc))
        asyncio.run(찍기(목록, tmp))
        시트(표, tmp)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def 시트(표, tmp):
    from PIL import ImageFont
    def F(sz, bold=True):
        for c in ["/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc", "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"]:
            if os.path.exists(c):
                return ImageFont.truetype(c, sz)
        return ImageFont.load_default()
    TW, TH = 270, 480
    rows = []
    for r, sc in 표:
        g = GAN[r["i"]]
        im = Image.new("RGB", (60 + 6 * (TW + 20) + 40, 150 + TH + 230), "#0b1020")
        d = ImageDraw.Draw(im)
        d.text((60, 36), f"{r['name']}({g}) · {기운[r['id']]}  —  \"{' '.join(r['hook'])}\"", font=F(46), fill="#e7c88d")
        d.text((60, 98), "18.5초 · 장면 6개 · 음악 clip_v3_music(라이브러리 v2)", font=F(30), fill="#aab3d6")
        for j, s in enumerate(sc):
            x = 60 + j * (TW + 20); y = 150
            th = Image.open(os.path.join(tmp, f"{r['id']}_{j}.jpg")).resize((TW, TH))
            im.paste(th, (x, y))
            d.rectangle([x, y, x + TW, y + TH], outline="#2a3360", width=3)
            d.text((x, y + TH + 12), f"{j+1} {s['이름']}", font=F(32), fill="#e7c88d")
            d.text((x, y + TH + 56), f"{s['초'][0]:g}~{s['초'][1]:g}초", font=F(26), fill="#aab3d6")
            d.text((x, y + TH + 92), s["기법"], font=F(26), fill="#7fd6c8")
            if s["움직임"]:
                m = s["움직임"]; d.text((x, y + TH + 128), m[:11], font=F(24), fill="#dfe4f7")
                if len(m) > 11: d.text((x, y + TH + 160), m[11:22], font=F(24), fill="#dfe4f7")
        im.save(os.path.join(HERE, f"sb_{r['id']}.jpg"), quality=85)
        rows.append(im)
    # 머리 + 8줄 한 장
    head_h = 330
    W_ = rows[0].width
    sheet = Image.new("RGB", (W_, head_h + sum(x.height for x in rows) + 260), "#0b1020")
    d = ImageDraw.Draw(sheet)
    d.text((60, 50), "스토리보드 · 승인 요청", font=F(40), fill="#e7c88d")
    d.text((60, 110), "일간 성격 3회차 모션 판 8편 (갑~신) — 11/18~27 평일 17:00 후보", font=F(54), fill="#ffffff")
    d.text((60, 200), "글은 3회차 그대로 · 0초부터 훅 글자 · 1.5~4초마다 장면 바뀜 · 기운 그림 8가지 모두 다름", font=F(32), fill="#aab3d6")
    d.text((60, 248), "까닭·해 볼 것 기법 짝도 편마다 다름(K-007) · 상단 고정 줄은 2장면부터 · 글·그림은 안전 영역 가운데", font=F(32), fill="#aab3d6")
    y = head_h
    for x in rows:
        sheet.paste(x, (0, y)); y += x.height
    d.rounded_rectangle([60, y + 40, W_ - 60, y + 220], radius=30, fill="#e7c88d")
    d.text((100, y + 70), "고칠 곳(장면 순서·기법·길이)이 있으면 프로젝트 대화에 알려 주세요.", font=F(36), fill="#111111")
    d.text((100, y + 130), "괜찮으면 승인만 누르면 ①이 8편 영상을 만들어 다시 올려요(예약은 영상 승인 뒤).", font=F(36), fill="#111111")
    sheet.save(os.path.join(HERE, "storyboard_ilgan3m.jpg"), quality=82)
    print("만듦:", os.path.join(HERE, "storyboard_ilgan3m.jpg"), sheet.size)


if __name__ == "__main__":
    main()
