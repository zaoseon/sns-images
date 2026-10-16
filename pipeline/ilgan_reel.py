"""일간 성격 릴스 — `2026-ilgan2/cards.json` 하나를 읽어 열 편을 만든다.

왜 새로 만들었나
  1회차를 만든 `reel_plan.py` 는 10/1~10/9 배치에 묶인 일회용이다(샘플 PNG 파일명이 박혀 있다).
  2회차는 표지 사양(cards.json)이 이미 있으니 그것을 그대로 읽어 영상으로 민다 —
  표지와 영상의 첫 줄이 어긋날 일이 없다.

오늘 정한 규칙을 그대로 쓴다
  판·바탕   표지 사양에 적힌 것을 그대로(clip_motion.set_pal/set_backdrop) — 표지와 영상이 같은 색
  소리      K-070, 영상마다 다른 곡
  첫 줄     표지의 hook 을 그대로 쓴다(K-102 는 표지 관문에서 이미 걸렀다)
  글자 크기  channel_specs 의 reel 범위 안에서(숫자를 여기 박지 않는다)

시험 설계(K-103): 첫 줄만 행동 5 · 형용사 5 로 갈랐다. 나머지는 전부 고정이라
2주 뒤 3초율을 두 갈래로 나누면 첫 줄의 값이 바로 나온다.

사용: python3 pipeline/ilgan_reel.py            전부
      python3 pipeline/ilgan_reel.py ilgan2-gab  한 편
"""
import os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
import fonts_kit as K, clip_motion as M, reel_music as RM, music_plan as MP, asset_lib as AL, channel_specs as CS

SPEC = os.path.join(ROOT, "2026-ilgan2", "cards.json")
OUT = os.path.join(ROOT, "2026-ilgan2", "reels")
CH = CS.CH["reel"]
Z = {z[0]: z[1:5] for z in CH["zones"]}
GM, PR = K.P["gm_bold"], K.P["pr_xb"]
유형 = "훅·질문 표지"

# 천간마다 본문 — 성격 한 줄 · 왜 그런지 한 줄 · 오늘 해 볼 것 한 줄.
# 사주의 일반적인 십간 풀이를 입말로 옮긴 것이다. 단정하지 않고, 없는 기능을 말하지 않는다.
본문 = {
 "ilgan2-gab":   ("곧게 자라는 나무의 기운이에요", "밀고 가는 힘은 센데 멈추는 데 힘이 들어요", "오늘은 한 가지만 내려놔 보세요"),
 "ilgan2-eul":   ("덩굴처럼 감고 올라가는 기운이에요", "부드러운 쪽이 오래 남는 경우가 많아요", "굽힌 날의 나를 탓하지 마세요"),
 "ilgan2-byeong":("한낮의 해 같은 기운이에요", "표정이 먼저 나가서 손해를 보기도 해요", "티 난 마음에 이름을 붙여 보세요"),
 "ilgan2-jeong": ("등불처럼 오래 타는 기운이에요", "그래서 작은 말에도 오래 흔들려요", "담아 둔 것 하나만 적어 보세요"),
 "ilgan2-mu":    ("큰 산 같은 기운이에요", "무겁다는 말을 칭찬으로만 들어 왔어요", "오늘은 먼저 기대 보세요"),
 "ilgan2-gi":    ("논밭처럼 품는 기운이에요", "남의 급한 일이 내 급한 일보다 먼저 보여요", "내 것 하나를 맨 앞에 두세요"),
 "ilgan2-gyeong":("잘 벼린 쇠 같은 기운이에요", "맞는 말이어도 세게 들릴 때가 있어요", "말한 뒤 한 번만 더 들어 보세요"),
 "ilgan2-sin":   ("보석처럼 깎인 기운이에요", "기준이 높은 건 나한테도 똑같이 적용돼요", "오늘은 판단을 하루만 미뤄 보세요"),
 "ilgan2-im":    ("큰 물 같은 기운이에요", "묻지 않으면 끝까지 안 꺼내요", "들은 것 중 하나는 말해 보세요"),
 "ilgan2-gye":   ("스며드는 비 같은 기운이에요", "남 마음은 잘 읽는데 내 것은 뒤로 미뤄요", "오늘 내 마음 한 줄만 꺼내 보세요"),
}


def 장면(c):
    """세 장면 — 훅 / 풀이 / 해 볼 것. 자리는 channel_specs 구역에서 가져온다."""
    제목y, 본문y, 끝y = Z["제목"][1], Z["본문·그림"][1], Z["버튼·마무리"][1]
    hook = "\n".join(c["hook"])
    설명, 까닭, 할것 = 본문[c["id"]]
    간 = c["kick"].split(" · ")[0]          # "을(乙) · 덩굴" -> "을(乙)"

    def s1(x):
        M.chip(x, c["kick"], Z["상단 라벨"][1], .05)
        M.text(x, hook, 제목y, .2, 100, path=GM, maxw=820, lh=1.35)
        M.text(x, c["subs"][0], 본문y, .9, 48, color=M.ACC(), path=PR, maxw=820, lh=1.5)

    def s2(x):
        # 릴스는 배지를 안 그린다(R04 — 인스타 상단 버튼에 가려지는 자리). 코드 주석대로
        # 분류 글은 본문에 넣는다. 안 넣으면 **어느 천간 이야기인지 영상 어디에도 안 나온다**(10/16 실제로 그랬다).
        M.text(x, 설명, 제목y, .05, 84, path=GM, maxw=820, lh=1.35)
        M.text(x, f"태어난 날 첫 글자가 {간}이에요", 본문y, .5, 48, color=M.ACC(), path=PR, maxw=820, lh=1.5)
        M.text(x, 까닭, 본문y + 86, .9, 46, color=M.DIM, path=PR, maxw=820, lh=1.5)

    def s3(x):
        M.text(x, "오늘 해 볼 것", 제목y, .05, 72, color=M.ACC(), path=GM, maxw=820)
        M.text(x, 할것, 본문y, .5, 56, path=PR, maxw=820, lh=1.5)
        M.text(x, "내 첫 글자는 프로필 링크에서 1초", 끝y, 1.1, 44, color=M.DIM, path=PR, maxw=820)

    return [(3.2, s1), (4.6, s2), (3.4, s3)]


def main():
    want = sys.argv[1:]
    spec = json.load(open(SPEC, encoding="utf-8"))
    os.makedirs(OUT, exist_ok=True)
    for i, c in enumerate(spec["cards"]):
        if want and c["id"] not in want:
            continue
        M.set_pal(c["pal"])                       # 표지와 같은 판
        M.set_bg(M.bg_for(c["id"]))
        # 표지(cards_reel)는 판 색 단색 바탕으로 그려졌다. 영상 첫 화면이 배경 그림이면 둘이 달라 보인다 —
        # 같은 편의 표지와 영상은 같아야 하므로 단색으로 맞춘다.
        M.set_backdrop(유형, "단색", c["id"])
        sc = 장면(c)
        # 바탕을 render 에도 넘겨야 한다 — render 안에서 set_backdrop 을 다시 부르기 때문에
        # 넘기지 않으면 위에서 정한 "단색"이 덮여 배경 그림이 깔린다(10/16 실제로 그랬다).
        p, dur = M.render(c["id"], sc, OUT, 내용유형=유형, 판=c["pal"], 바탕="단색")
        # 음악은 **짝끼리 똑같이** 쓴다. 영상마다 고르게 했더니 갈래가 번갈아 나가는 탓에
        # 행동 갈래는 상큼 팝·신스팝, 형용사 갈래는 우쿨렐레·마림바로 **곡이 완전히 갈려 버렸다**.
        # 그러면 결과가 첫 줄 때문인지 음악 때문인지 못 가린다(K-103). 짝(갑·을 / 병·정 …) 안에서는
        # 곡이 같고 첫 줄만 다르게 둔다.
        짝 = i // 2
        mi = MP.choose("fun", f"ilgan2-pair{짝}")
        MP.mux(p, [d for d, _ in sc], mi, 300 + 짝)
        print(f"  {c['id']:16} {c['첫줄 갈래']:4} {dur:.1f}초 · {c['pal']:12} · 음악 {mi['style']} {mi['bpm']}", flush=True)


if __name__ == "__main__":
    main()
