# -*- coding: utf-8 -*-
"""10/15 OSMU 심리 규칙(O1): 캐러셀에 '심리학으로 읽으면' 한 장을 더한다. 기존 7장 세트(topic_sets_night7)의 편집기·글꼴·배경 그대로 쓰려고,
본문 1장 자리(personality)에 심리 카드를 넣어 그린 뒤 그 한 장(_2.jpg)만 기존 세트의 5번째 뒤(조언 앞)에 끼운다. 글은 해당 블로그 글(public/naver/nXX.html '심리학으로 읽으면')에 있는 말만 쓴다.
렌더: TOPIC_SETS=topic_sets_psych TOPIC_OUT=2026-w43psych python3 pipeline/topic_carousels.py"""
import copy, topic_sets_night7 as N
PSY = {
 "2026-10-22": ("비교는 심리학에서\n'사회 비교'라고 해요", "사람은 자기를 알려고\n남과 견준다고 해요.\n비교 자체는 자연스러운 일이에요."),
 "2026-10-24": ("가까운 사람과 맺는\n'애착 유형'이 있어요", "관계를 맺는 방식이\n연애에도 이어진다는 생각이에요.\n진단이 아니라 경향이에요."),
 "2026-10-29": ("고를 것이 많을수록\n고르기 어려워져요", "잼 24가지보다 6가지일 때\n실제로 산 사람이 많았어요.\n결정이 느린 건 성격 탓만은 아니에요."),
}
SETS = {}
for d, (t, b) in PSY.items():
    s = copy.deepcopy(N.SETS[d]); s["badges"][0] = "심리학으로 읽으면"; s["body"][0] = (t, b); SETS[d] = s
