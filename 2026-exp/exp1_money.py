# 릴스 실험 판 1편(K-167): 2027 돈 들어오는 띠 3가지 — CT 11/2. 값은 n05(엔진 계산) 그대로. 다음 편은 이 파일을 본보기로 장면만 바꾼다. 결과 mp4는 저장소에 두지 않는다.
import os, sys, json, subprocess
sys.path.insert(0, "/home/claude/sns-images/pipeline")
import motion_kit as MK, html_motion as HM
from motion_kit import 쓰기
ART = "/home/claude/sns-images/assets/pd_art"
idx = []
pick = json.load(open("/home/claude/sns-images/2026-exp/exp1_pick.json"))   # 장면 → 파일
P = "k_gold"
def img(k): return f"{ART}/{pick[k]}"
씬 = [
 ("mx-0", 2.8, False, [쓰기("그림넘김", 왜="멈춤", s=-0.2, d=3.2, 단="배경", 그림=img("표지")),
   쓰기("센표지", 왜="멈춤", s=-0.5, d=0.6, 단="마무리 카드", 줄=["2027년", "돈 들어오는", "띠 3가지"], 강조=[1], 크기=140)]),
 ("mx-1", 6.0, True, [쓰기("그림넘김", 왜="멈춤", s=0, d=6.2, 단="배경", 그림=img("까닭")),
   쓰기("장면글", 왜="정보", s=0, d=0.5, 단="마무리 카드", 줄=['2027년은', '불의 해'], 강조=[1], 강조2=[], 자막='물의 띠에게 불은\n손에 쥐는\n재물이 돼요')]),
 ("mx-2", 6.0, True, [쓰기("그림넘김", 왜="멈춤", s=0, d=6.2, 단="배경", 그림=img("말")),
   쓰기("장면글", 왜="정보", s=0, d=0.5, 단="마무리 카드", 줄=['3위 말띠', '78·90·02년생'], 강조=[0], 강조2=[], 자막='양띠와 짝인 띠\n좋은 조건의\n제안이 와요')]),
 ("mx-3", 6.0, True, [쓰기("그림넘김", 왜="멈춤", s=0, d=6.2, 단="배경", 그림=img("쥐")),
   쓰기("장면글", 왜="정보", s=0, d=0.5, 단="마무리 카드", 줄=['2위 쥐띠', '84·96·08년생'], 강조=[0], 강조2=[], 자막='돈 들어올 기회는 분명\n돈거래는\n글로 남기세요')]),
 ("mx-4", 6.5, True, [쓰기("그림넘김", 왜="멈춤", s=0, d=6.7, 단="배경", 그림=img("돼지")),
   쓰기("장면글", 왜="정보", s=0, d=0.5, 단="마무리 카드", 줄=['1위 돼지띠', '83·95·07년생'], 강조=[0], 강조2=[], 자막='사람이 돈을\n데려와요\n2·3·7월에 힘을')]),
 ("mx-5", 5.5, True, [쓰기("그림넘김", 왜="멈춤", s=0, d=5.7, 단="배경", 그림=img("조심")),
   쓰기("장면글", 왜="정보", s=0, d=0.5, 단="마무리 카드", 줄=['이 띠는', '조심'], 강조=[], 강조2=[1], 자막='소띠 큰 지출은\n두 번 나눠서\n개띠 보증은 피하기')]),
 ("mx-6", 5.0, True, [쓰기("그림넘김", 왜="멈춤", s=0, d=5.2, 단="배경", 그림=img("끝")),
   쓰기("장면글", 왜="정보", s=0, d=0.5, 단="마무리 카드", 줄=['다음 편 듣고 싶은', '띠 댓글로!'], 강조=[1], 강조2=[], 자막='많이 나온 띠부터\n만들어요')]),
]
outs = []
for i, (name, sec, top, parts) in enumerate(씬):
    p = f"/tmp/claude-0/mk/{name}.html"
    open(p, "w", encoding="utf-8").write(MK.페이지(parts, 판=P, ch="reel", ai=False, 끝=(sec if i < len(씬) - 1 else None), 상단줄=top))
    outs.append(HM.render(p, name, 초=sec, fps=30, ch="reel")[0])
open("/tmp/claude-0/mk/lm.txt", "w").write("".join(f"file '{o}'\n" for o in outs))
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", "/tmp/claude-0/mk/lm.txt", "-c", "copy", "/tmp/claude-0/mk/money.mp4"], check=True)
print("ok")
