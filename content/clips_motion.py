"""네이버 SOP 클립 v2 장면표 (움직이는 글자·그림·정월). 문장은 글 n28·n33 본문에 있는 내용만 쓴다."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "pipeline"))
from clip_motion import *
def S12(*a): return list(a)
SC = {}
# ───────── n28 궁합 ─────────
SC[("n28-c1", "12")] = [
 (2.2, hook("궁합 · 질문", "이 사람과 나,\n*잘 맞을까요?*", "v2_straight")),
 (2.6, point("궁합은", "지도 하나만 보면\n*한쪽 이야기*만 들어요", lambda c: three_maps(c, 760, 0.9, filled=1, caption="한쪽 이야기만 들려요"), y=300)),
 (2.6, point("그래서", "사주·별자리·숫자\n*세 지도*를 나란히 봐요", lambda c: three_maps(c, 760, 0.8, filled=3, gap=0.3, caption="세 지도를 나란히"), y=300)),
 (2.4, lambda c: (chip(c, "몇 개가 맞나요?", 250, .05), text(c, "세 지도 중\n*몇 개*가 맞는지\n세어 보세요", 400, .2, 104, lh=1.32), score_rows(c, 860, 1.0, [("3", "편안한 사이"), ("2", "대체로 잘 맞아요"), ("1", "대화가 열쇠")], step=190))),
 (2.2, lambda c: cta(c, "내 일간·별자리·숫자는\n무료 풀이에서 확인")),
]
SC[("n28-c2", "12")] = [
 (2.2, hook("궁합 · 오해", "궁합이 안 맞으면\n*끝일까요?*", "v3_ponytail")),
 (2.6, lambda c: (chip(c, "정말일까요?", 250, .05), strike(c, "안 맞으면 끝", 420, .5, 120), text(c, "*아니에요*", 640, 1.1, 150), text(c, "한 지도가 안 맞아도\n걱정할 필요는 없어요", 880, 1.5, 70, path=MED, color=DIM, lh=1.4))),
 (2.6, point("그 부분은", "*규칙*으로 조율해요", lambda c: (pop(c, chip_layer("연락 빈도", 84), CX, 840, .9), pop(c, chip_layer("쉬는 방식", 84), CX, 1000, 1.3), pop(c, chip_layer("대화 방식", 84), CX, 1160, 1.7)), y=330)),
 (2.4, lambda c: (chip(c, "정리하면", 250, .05), text(c, "안 맞는 게 아니라\n*조율할 곳*이에요", 400, .2, 108, lh=1.32), character(c, "v2_straight", t0=.3, width=640))),
 (2.2, lambda c: cta(c, "자세한 기준은\n블로그 궁합 글에서")),
]
SC[("n28-c3", "12")] = [
 (2.0, hook("궁합 · 체크", "궁합 볼 때\n*확인할 세 가지*", "v8_gesture")),
 (7.2, lambda c: (chip(c, "두 사람을 나란히", 250, .05), check_row(c, 420, "사주 · 서로 키워 주는 기운인가", .5), check_row(c, 610, "별자리 · 불과 공기, 흙과 물인가", 2.6), check_row(c, 800, "숫자 · 같은 무리의 숫자인가", 4.7),
                  text(c, "몇 개가 맞나요?", 1090, 5.9, 96, color=GOLD) if c.t > 5.9 else None)),
 (2.8, lambda c: cta(c, "자세한 기준은\n블로그에서")),
]
SC[("n28-c1", "30")] = [
 (2.0, hook("궁합 · 질문", "이 사람과 나,\n*잘 맞을까요?*", "v2_straight")),
 (4.0, point("먼저", "궁합을 지도 하나로만 보면\n*한쪽 이야기*만 듣게 돼요", lambda c: three_maps(c, 800, 1.2, filled=1, caption="한쪽 이야기만 들려요"), y=300, size=88)),
 (4.0, point("첫째 · 사주", "서로 *키워 주는 기운*이면\n편안한 사이로 봐요", lambda c: wuxing(c, CX, 1130, 1.0, dur=2.6, R=215), y=300, size=84)),
 (4.0, lambda c: (chip(c, "둘째 · 별자리", 200, .05), text(c, "*불과 공기*, *흙과 물*이\n잘 맞아요", 330, .2, 92, lh=1.32), pairs(c, 700, 1.0))),
 (4.0, lambda c: (chip(c, "셋째 · 숫자", 200, .05), text(c, "*같은 무리*의 숫자는\n말이 잘 통해요", 330, .2, 92, lh=1.32), groups(c, 760, 1.0))),
 (7.0, lambda c: (chip(c, "세 지도 중 몇 개?", 200, .05), score_rows(c, 380, .6, [("3", "편안한 사이예요"), ("2", "대체로 잘 맞아요"), ("1", "대화가 열쇠예요")]), text(c, "한 곳이 안 맞아도\n걱정할 필요는 없어요", 960, 2.4, 72, path=MED, color=DIM, lh=1.4), character(c, "v2_straight", t0=2.0, width=520) if False else None)),
 (5.0, lambda c: cta(c, "자세한 기준은\n블로그 궁합 글에서")),
]
# ───────── n33 약속 취소 / 화개 ─────────
SC[("n33-c1", "12")] = [
 (2.2, lambda c: (chip(c, "혼자 충전 · 질문", 220, .05), notice(c, .2), text(c, "속으로 웃은 적\n있나요?", 560, .9, 112, lh=1.3), character(c, "v1_lowbun", t0=.6, width=620))),
 (2.6, point("사람이", "*싫은 게* 아니에요", lambda c: battery(c, CX, 1130, .7, frm=.1, to=.35, dur=1.4, label="사람 만난 뒤"), y=330)),
 (2.6, point("혼자 있는 시간에", "*힘을 채우는*\n사람이에요", lambda c: battery(c, CX, 1130, .5, frm=.15, to=1.0, dur=1.8, label="혼자 충전 중"), y=300)),
 (2.4, lambda c: (chip(c, "정리하면", 250, .05), text(c, "*충전 방식*이\n다를 뿐이에요", 400, .2, 112, lh=1.32), character(c, "v1_lowbun", t0=.3, width=640))),
 (2.2, lambda c: cta(c, "자세한 기준은\n블로그 화개 글에서")),
]
SC[("n33-c2", "12")] = [
 (2.2, hook("혼자 충전 · 오해", "약속 취소가 반가우면\n*사회성이 없는 걸까요?*", "v3_ponytail", size=96)),
 (2.6, lambda c: (chip(c, "아니에요", 250, .05), text(c, "사회성", 420, .3, 140), text(c, "≠", 600, .8, 150, color=GOLD), text(c, "충전 방식", 820, 1.2, 140, color=GOLD), text(c, "별개예요", 1040, 1.6, 84, path=MED, color=DIM))),
 (2.6, point("만나서 즐거워도", "혼자 *충전*이 필요한\n사람이 있어요", lambda c: battery(c, CX, 1130, .7, frm=.8, to=.18, dur=1.6, label="즐거운 약속 후"), y=300, size=96)),
 (2.4, lambda c: (chip(c, "정리하면", 250, .05), text(c, "마음이 없는 게 아니라\n*충전이 필요*한 거예요", 400, .2, 98, lh=1.32), character(c, "v1_lowbun", t0=.3, width=640))),
 (2.2, lambda c: cta(c, "자세한 기준은\n블로그 화개 글에서")),
]
SC[("n33-c3", "12")] = [
 (2.0, hook("혼자 충전 · 체크", "충전형인 사람이\n*해 볼 세 가지*", "v1_lowbun")),
 (7.2, lambda c: (chip(c, "이번 주에", 250, .05), check_row(c, 420, "약속 사이에 혼자 쉬는 시간 먼저", .5, 60), check_row(c, 610, "취소는 미리 솔직하게, 대안 날짜 하나", 2.6, 60), check_row(c, 800, "힘든 주엔 짧은 메시지로 마음만", 4.7, 60))),
 (2.8, lambda c: cta(c, "자세한 기준은\n블로그 화개 글에서")),
]
if __name__ == "__main__":
    cid, ver = sys.argv[1], sys.argv[2]; out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "clips_sop")
    sc = SC[(cid, ver)]; p, d = render(f"{cid}_{ver}s", sc, out); print(os.path.basename(p), d, "초")
