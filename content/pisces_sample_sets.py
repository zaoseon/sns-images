# -*- coding: utf-8 -*-
"""10/4 샘플: 물고기자리 주제(네이버 n48 10/6, 사이트 글 10/7)의 인스타 3장 카드 샘플 1세트. 문장은 n48 원고에 있는 내용만 쓴다.
틀: 오해 풀기(night_sets_w42 와 같은 구조). 대표 확인 전까지 예약하지 않는다."""
def N(face, accent, kicker, sub, title, s2, s3, variant, date, systems):
    return dict(face=face, accent=accent, kicker=kicker, coverSub=sub, coverTitle=title, badges=[s2[0], s3[0], s3[0], s3[0]],
                body=[(s2[1], s2[2]), (s3[1], s3[2]), (s3[1], s3[2]), (s3[1], s3[2])], advice=("x", "x"), ctaQ="x", nextTitle="x",
                variant=variant, date=date, systems=systems)
SETS = {
 "sample-pisces": N("v1_lowbun", "#6fb3e0", "정월의 별자리 읽기", "친구의 한마디가 하루 종일 남을 때", "물고기자리는\n우유부단할까?",
   ("오해", "결정을 못 하는\n게 아니에요", "결정 전에 주변 마음을\n먼저 읽느라 시간이 걸려요.\n마감을 먼저 말해 보세요."),
   ("겹쳐 보면", "2027년,\n느린 별이 떠나요", "해왕성과 토성이\n양자리로 옮겨 가요.\n방향을 직접 정하는 해예요."),
   {"cover": "C2", "advice": "A1", "cta": "T1"}, "sample-pisces", ["별자리", "사주"]),
}
