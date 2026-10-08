# -*- coding: utf-8 -*-
"""물고기자리 카드 5장 시안(10/7 ③, 대표 지적: 캐러셀은 표지·본문·CTA가 있어야 하고 기승전결이 닫혀야 한다).
올라간 3장(표지·선택지·풀이)은 본문 2장만 쓰고 조언·마무리를 버려서 이야기가 중간에 끊겼다. 같은 7장 틀(표지-본문4-조언-CTA)에서 표지·선택지·풀이·조언·마무리 5장을 쓴다.
문장은 네이버 n48 원고(naver/pages.json)에 있는 내용만 쓴다(새로 지어내지 않는다). 렌더: TOPIC_SETS=topic_sets_pisces5 TOPIC_OUT=2026-w43sample5 python3 pipeline/topic_carousels.py
7장으로 그린 뒤 1(표지)·2(선택지)·3(풀이)·6(조언)·7(마무리)만 쓴다. 4·5번 본문 장은 쓰지 않는다."""
def T(face, accent, kicker, sub, title, badges, slides, advice, q, nxt, variant, date, systems):
    return dict(face=face, accent=accent, kicker=kicker, coverSub=sub, coverTitle=title, badges=badges, body=slides, advice=advice,
                ctaQ=q, nextTitle=nxt, variant=variant, date=date, systems=systems)
SETS = {
 "2026-12-31": T("v1_lowbun", "#6fb3e0", "정월의 별자리 테스트", "친구의 한마디가 하루 종일 남는다면", "물고기자리인 나,\n몇 개 해당되나요?",
   ["선택지", "겹쳐 보면", "2027년", "해 볼 것"],
   [("세 가지 중\n몇 개인가요?", "1 친구 한마디가 하루 종일 남아요\n2 결정 전에 주변 기분부터 살펴요\n3 회의에서 누가 불편한지 먼저 봐요"),
    ("우유부단이 아니라\n마음부터 읽는 거예요", "결정 전에 주변 마음을\n읽느라 시간이 걸려요.\n마감을 먼저 말해 보세요."),
    ("2027년, 느린 별\n두 개가 떠나요", "해왕성과 토성이 모두\n물고기자리를 떠난 뒤 맞는 첫 해예요.\n방향을 직접 정하는 해로 읽어요."),
    ("해 볼 것", "2027년 2월 19일에\n올해 하고 싶은 일을\n한 줄로 적어 두세요.")],
   ("2027년 2월 19일에\n한 줄만 적어 두세요", "올해 하고 싶은 일 한 가지를\n한 줄로 적어요.\n방향은 내가 정하는 거예요."),
   "나는 물 일간일까\n*불 일간*일까요?", "2027 띠별 운세 편", {"cover": "C1", "advice": "A1", "cta": "T1"}, "2026-12-31T18:30", ["별자리", "사주"]),
}
