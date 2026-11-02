# 릴스 실험 판 2편(K-167, 확인형): 도화살 있는 사람 특징 5가지 — CT 11/3.
# 구조는 27saju '신기 있는 사람 특징 7가지'(142만, 113초)를 따름: 센 표지 → '첫 번째…' 하나씩(그림+자막) → "몇 개 해당?" 댓글.
# 자막은 한 줄 11자 안팎·3줄까지(70px 유지 — 대표 11/3 '텍스트 더 크게'). 내용은 n79(도화살 뜻) 발행 원고 그대로 — 단정 없음("~로 읽어요"), 지어낸 수치 없음.
import os, sys, json, subprocess
sys.path.insert(0, "/home/claude/sns-images/pipeline")
import motion_kit as MK, html_motion as HM
from motion_kit import 쓰기
ART = "/home/claude/sns-images/assets/pd_art"
def img(f): return f"{ART}/{f}"
P = "k_gold"
def fit(줄, 최대=110, 폭=830):   # 한 줄이 제목 칸(850px)을 넘지 않게 글자 크기를 줄인다(11/3 '사람 앞에서 빛나요'가 3줄로 터져 구역을 93px 넘음)
    em = lambda t: sum(.58 if c.isdigit() else .3 if c == " " else .45 if c in "·,.!?" else 1.0 for c in t)
    return min(최대, int(폭 / max(em(x) for x in 줄)))
def item(n, 번째, 제목, 자막, 그림, 강조=[1], 초=8.0):
    return (f"dh-{n}", 초, True, [쓰기("그림넘김", 왜="멈춤", s=0, d=초 + .2, 단="배경", 그림=img(그림)),
        쓰기("장면글", 왜="정보", s=0, d=0.5, 단="마무리 카드", 줄=[번째, 제목], 강조=강조, 자막=자막)])
씬 = [
 ("dh-0", 3.0, False, [쓰기("그림넘김", 왜="멈춤", s=-0.2, d=3.4, 단="배경", 그림=img("003_Hyewon_Wolha_jeongin_3.jpg")),
   쓰기("센표지", 왜="멈춤", s=-0.5, d=0.6, 단="마무리 카드", 줄=["도화살", "있는 사람", "특징 5가지"], 강조=[0], 크기=140)]),
 item(1, "첫 번째", "끌리는 분위기", "도화는 복숭아꽃\n사람을 끌어당기는\n매력으로 읽어요", "001_Hyewon_Imhatuho.jpg"),
 item(2, "두 번째", "무대에서 빛나요", "무대나 영업처럼\n사람 대하는 일에서\n빛난다고 읽어요", "008_Danwon_Jangteogil.jpg"),
 item(3, "세 번째", "자리마다 달라요", "일 칸이면\n가까운 사이에서\n월 칸이면 일터에서", "002_Hyewon_Ssangryuksammae.jpg"),
 item(4, "네 번째", "바람기와 달라요", "매력과 표현으로\n읽는 글자예요\n태도는 사람 나름", "016_Unknown_Korean_Lotus_Pond_2016_1_Detroit.jpg"),
 item(5, "다섯 번째", "2027년엔 달로 와요", "호랑이·말·개띠 3월\n소·뱀·닭띠 6월\n도화 달이에요", "011_Crane_and_Pine_National_Museum_of_Korea_.jpg"),
 ("dh-6", 5.5, True, [쓰기("그림넘김", 왜="멈춤", s=0, d=5.7, 단="배경", 그림=img("003_Hyewon_Wolha_jeongin_3.jpg"), 자리="70% 40%"),
   쓰기("장면글", 왜="정보", s=0, d=0.5, 단="마무리 카드", 줄=["몇 개나", "해당되세요?"], 강조=[1], 자막="숫자 하나만\n댓글로 남겨 주세요\n프로필에서 1초 확인")]),
]
OUT = os.environ.get("ZS_OUT", "/tmp/claude-0/mk/dohwa.mp4")
outs = []
for i, (name, sec, top, parts) in enumerate(씬):
    p = f"/tmp/claude-0/mk/{name}.html"
    open(p, "w", encoding="utf-8").write(MK.페이지(parts, 판=P, ch="reel", ai=False, 끝=(sec if i < len(씬) - 1 else None), 상단줄=top))
    outs.append(HM.render(p, name, 초=sec, fps=30, ch="reel")[0])
open("/tmp/claude-0/mk/ld.txt", "w").write("".join(f"file '{o}'\n" for o in outs))
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", "/tmp/claude-0/mk/ld.txt", "-c", "copy", OUT], check=True)
for o in outs: os.replace(o, "/tmp/claude-0/mk/parts/" + os.path.basename(o))
print("ok", OUT)
