"""네이버 글 연결 클립 12초판 5편 (n42~n46, 10/4). 문장은 해당 글(naver/pages.json n42~n46) 본문에 있는 내용만 쓴다."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "pipeline"))
from clip_motion import *
import clips_motion as CM
SC = CM.SC
def close(lines, face, size=108): return lambda c: (chip(c, "정리하면", 250, .05), text(c, lines, 400, .2, size, lh=1.32), character(c, face, t0=.3, width=640))
# n42 예민 (오해 교정형)
SC[("n42-c1", "12")] = [
 (2.2, hook("예민 · 오해", "예민하면\n*약한 걸까요?*", "v2_straight", size=104)),
 (2.6, lambda c: (chip(c, "아니에요", 250, .05), text(c, "약함", 420, .3, 140), text(c, "≠", 600, .8, 150, color=GOLD), text(c, "감각이 커요", 820, 1.2, 130, color=GOLD), text(c, "받아들이는 정보가\n많아서일 수 있어요", 1020, 1.6, 66, path=MED, color=DIM, lh=1.4))),
 (2.6, point("그래서", "자극 사이에\n*조용한 10분*을 넣어요", lambda c: check_row(c, 980, "조용한 10분 넣기", .9, 60), y=300, size=96)),
 (2.4, close("감각이 큰 만큼\n*쉬는 시간*도\n더 필요해요", "v2_straight", 100)),
 (2.2, lambda c: cta(c, "자세한 기준은\n블로그 예민한 피로 글에서")),
]
# n43 소비 후회 (질문형)
SC[("n43-c1", "12")] = [
 (2.2, hook("소비 · 질문", "결제하고 나서\n*후회한 적 있나요?*", "v3_ponytail", size=96)),
 (2.6, point("후회는", "쓴 돈보다\n*쓴 이유*에서 올 수 있어요", None, y=330, size=92)),
 (2.6, point("내 후회의 모양은", "*세 가지*예요", lambda c: (pop(c, chip_layer("불 · 설렐 때", 84), CX, 860, .9), pop(c, chip_layer("물 · 기분이 흔들릴 때", 84), CX, 1020, 1.3), pop(c, chip_layer("흙 · 참다가 한 번에", 84), CX, 1180, 1.7)), y=300, size=104)),
 (2.4, close("결제 전에\n*하루만*\n기다려 보세요", "v3_ponytail", 108)),
 (2.2, lambda c: cta(c, "자세한 기준은\n블로그 소비 습관 글에서")),
]
# n44 결정 미루기 (체크리스트형)
SC[("n44-c1", "12")] = [
 (2.0, hook("결정 · 체크", "결정을 못 할 때\n*해 볼 세 가지*", "v1_lowbun")),
 (7.2, lambda c: (chip(c, "이번 주에", 250, .05), check_row(c, 420, "고민을 한 사건으로 적기", .5, 60), check_row(c, 610, "정할 기한 하나 적기", 2.6, 60), check_row(c, 800, "포기할 것 한 가지 정하기", 4.7, 60))),
 (2.8, lambda c: cta(c, "자세한 기준은\n블로그 결정 미루기 글에서")),
]
# n45 퇴근 방전 (오해 교정형)
SC[("n45-c1", "12")] = [
 (2.2, hook("퇴근 후 · 오해", "아무것도 하기 싫으면\n*게으른 걸까요?*", "v13_horn_glasses", size=92)),
 (2.6, lambda c: (chip(c, "아니에요", 250, .05), text(c, "게으름", 420, .3, 140), text(c, "≠", 600, .8, 150, color=GOLD), text(c, "방전", 820, 1.2, 140, color=GOLD), text(c, "에너지를 쓴 방식에 따라\n달라지는 피로예요", 1040, 1.6, 66, path=MED, color=DIM, lh=1.4))),
 (2.6, point("그래서", "퇴근 뒤 *30분*은\n아무것도 안 해요", lambda c: check_row(c, 980, "퇴근 뒤 30분 비우기", .9, 60), y=300, size=100)),
 (2.4, close("방전은\n*하루를 열심히 쓴*\n흔적일 수 있어요", "v13_horn_glasses", 96)),
 (2.2, lambda c: cta(c, "자세한 기준은\n블로그 방전과 충전 글에서")),
]
# n46 가면 (질문형)
SC[("n46-c1", "12")] = [
 (2.2, hook("가면 · 질문", "웃는 얼굴 뒤에\n*마음을 숨기나요?*", "v8_gesture", size=96)),
 (2.6, point("가면은", "*거짓*이 아니라\n나를 지키는 방식일 수 있어요", None, y=330, size=92)),
 (2.6, point("내 가면은", "*분위기*를 맞추거나\n*속*을 숨기거나\n*역할* 때문이에요", None, y=300, size=92)),
 (2.4, close("속마음은\n*한 사람에게만*\n먼저 열어 보세요", "v8_gesture", 100)),
 (2.2, lambda c: cta(c, "자세한 기준은\n블로그 가면 글에서")),
]
IDS = ["n42-c1", "n43-c1", "n44-c1", "n45-c1", "n46-c1"]
