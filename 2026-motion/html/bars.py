"""숫자가 쌓이는 모션 한 편 (K-073 2단) — 이제 `pipeline/motion_kit.py` 기법으로 만든다.

10/16 처음엔 이 파일 안에 CSS·JS 를 손으로 썼다. 두 가지가 드러나 고쳤다.
  ① 같은 CSS 를 편마다 다시 쓰게 된다 → 기법 열둘을 `motion_kit` 으로 옮겼다(K-115).
  ② **겹침이 남아 있었다.** 검사가 "넘으면 안 되는 선"을 brand_frame 의 bottom(y1465,
     zaoseon.com **글자 줄**)으로 잡았는데 AI 고지 칸은 **y1425 에서 시작**한다.
     맨 아래 글이 1432px 까지 내려와 실제로는 이미 겹쳤는데 검사는 통과시켰다.
     선을 하단 고정 **구역이 시작하는 자리**로 고치니 바로 막혔다(1432 > 1401).
     기법으로 다시 세우면서 구역에 맞춰 앉혔다 — 자리를 손으로 적지 않으니 다시 어긋나지 않는다.

규칙은 그대로 지킨다
  크기·안전 영역·구역  channel_specs   고정 요소  brand_frame   글꼴  fonts_kit   판  color_combos
  첫 줄  체계 이름 금지(K-102) — "같은 나를 두고 / 왜 말이 다를까요?"
  움직임  정보를 나르는 데만(K-073) — 막대가 자라며 숫자가 올라간다

사용: python3 2026-motion/html/bars.py
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "pipeline"))
import motion_kit as MK

# 실제로 우리가 센 숫자다(무작위 3,000명). 지어낸 값이 아니다.
막대 = [("사주와 하락이수", 24), ("사주와 별자리", 17), ("사주와 숫자", 14)]


def 장면():
    return [
        MK.쓰기("나타나기", 왜="멈춤", s=0.1, d=0.7, 단="제목",
                글="같은 나를 두고\n왜 말이 다를까요?"),
        MK.쓰기("나타나기", 왜="정보", s=0.8, d=0.6, 단="상단 라벨",
                글="무작위 3,000명을 하나하나 세어 봤어요"),
        MK.쓰기("막대자라기", 왜="정보", s=1.8, d=1.1, 단="본문·그림", 최대=30, 줄=막대),
        MK.쓰기("나타나기", 왜="정보", s=5.6, d=0.7, 단="버튼·마무리",
                글="같은 말이 나오는 곳이 타고난 자리예요"),
    ]


def main():
    # 중간 HTML 은 motion_kit.만들기 가 임시 폴더에 쓰고 지운다 —
    # 글꼴이 base64 로 박혀 한 장이 39MB 라 저장소에 두면 안 된다(10/16).
    out, dur = MK.만들기("bars_3000", 장면(), 판="dg_gold_s", 초=8.0, fps=30)
    print(f"  {os.path.relpath(out, ROOT)} · {dur:.1f}초")


if __name__ == "__main__":
    main()
