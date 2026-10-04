# -*- coding: utf-8 -*-
"""물고기자리 카드(네이버 n48 10/6, 사이트 글 10/7과 같은 주제). 10/4 Metricool 실측: 번호로 답하게 하는 자가진단이 반응(댓글·저장)이 가장 컸다.
문장은 n48 원고(naver/pages.json)에 있는 내용만 쓴다."""
def N(face, accent, kicker, sub, title, s2, s3, variant, date, systems):
    return dict(face=face, accent=accent, kicker=kicker, coverSub=sub, coverTitle=title, badges=[s2[0], s3[0], s3[0], s3[0]],
                body=[(s2[1], s2[2]), (s3[1], s3[2]), (s3[1], s3[2]), (s3[1], s3[2])], advice=("x", "x"), ctaQ="x", nextTitle="x",
                variant=variant, date=date, systems=systems)
SETS = {
 "sample-pisces": N("v1_lowbun", "#6fb3e0", "정월의 별자리 테스트", "친구의 한마디가 하루 종일 남는다면", "물고기자리인 나,\n몇 개 해당돼요?",
   ("선택지", "세 가지 중\n몇 개예요?", "1 친구 한마디가 하루 종일 남아요\n2 결정 전에 주변 기분부터 살펴요\n3 회의에서 누가 불편한지 먼저 봐요"),
   ("겹쳐 보면", "우유부단이 아니라\n마음부터 읽는 거예요", "결정 전에 주변 마음을\n읽느라 시간이 걸려요.\n2027년엔 방향을 직접 정해요."),
   {"cover": "C1", "advice": "A1", "cta": "T1"}, "sample-pisces", ["별자리", "사주"]),
}
