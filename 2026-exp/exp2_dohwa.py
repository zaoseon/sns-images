# 릴스 실험 판 2편(K-167, 확인형): 도화살 있는 사람 특징 5가지 — CT 11/3.
# 구조는 27saju '신기 있는 사람 특징 7가지'(142만, 113초)를 따름: 센 표지 → '첫 번째…' 하나씩(그림+자막) → "몇 개 해당?" 댓글.
# 내용은 n79(도화살 뜻) 발행 원고 그대로 — 단정 없음("~로 읽어요"), 지어낸 수치 없음.
import os, sys, json, subprocess
sys.path.insert(0, "/home/claude/sns-images/pipeline")
import motion_kit as MK, html_motion as HM
from motion_kit import 쓰기
ART = "/home/claude/sns-images/assets/pd_art"
def img(f): return f"{ART}/{f}"
P = "k_gold"
def item(n, 번째, 제목, 자막, 그림, 강조=[1], 초=8.0):
    return (f"dh-{n}", 초, True, [쓰기("그림넘김", 왜="멈춤", s=0, d=초 + .2, 단="배경", 그림=img(그림)),
        쓰기("센표지", 왜="멈춤", s=0, d=0.5, 단="제목", 줄=[번째, 제목], 크기=110, 강조=강조),
        쓰기("자막", 왜="정보", s=0.8, d=0.4, 단="본문·그림", 글=자막)])
씬 = [
 ("dh-0", 3.0, False, [쓰기("그림넘김", 왜="멈춤", s=-0.2, d=3.4, 단="배경", 그림=img("003_Hyewon_Wolha_jeongin_3.jpg")),
   쓰기("센표지", 왜="멈춤", s=-0.5, d=0.6, 단="마무리 카드", 줄=["도화살", "있는 사람", "특징 5가지"], 강조=[0], 크기=140)]),
 item(1, "첫 번째", "끌리는 분위기", "도화는 복숭아꽃이에요\n사람을 끌어당기는 매력으로 읽어요", "001_Hyewon_Imhatuho.jpg"),
 item(2, "두 번째", "사람 앞에서 빛나요", "무대나 영업처럼\n사람을 대하는 일에서 빛난다고 읽어요", "008_Danwon_Jangteogil.jpg"),
 item(3, "세 번째", "드러나는 자리가 달라요", "일 칸에 있으면 가까운 사이에서\n월 칸에 있으면 일터에서 드러나요", "002_Hyewon_Ssangryuksammae.jpg"),
 item(4, "네 번째", "바람기와는 달라요", "매력과 표현으로 읽는 글자예요\n태도는 사람마다 달라요", "016_Unknown_Korean_Lotus_Pond_2016_1_Detroit.jpg"),
 item(5, "다섯 번째", "2027년엔 달로 와요", "호랑이·말·개띠는 3월\n소·뱀·닭띠는 6월이 도화 달이에요", "011_Crane_and_Pine_National_Museum_of_Korea_.jpg"),
 ("dh-6", 5.5, True, [쓰기("그림넘김", 왜="멈춤", s=0, d=5.7, 단="배경", 그림=img("003_Hyewon_Wolha_jeongin_3.jpg"), 자리="70% 40%"),
   쓰기("센표지", 왜="멈춤", s=0, d=0.5, 단="제목", 줄=["몇 개나", "해당되세요?"], 크기=118, 강조=[1]),
   쓰기("자막", 왜="정보", s=0.8, d=0.4, 단="본문·그림", 글="숫자 하나만 댓글로 남겨 주세요\n내 도화 글자는 프로필 링크에서 1초")]),
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
