"""릴스 자막 색 조합 (10/3 대표가 준 '정보성 콘텐츠' 추천). 조합2가 우리 남색·금색 우주 배경에 맞아 기본, 조합1은 변화를 줄 때.
조합1: 딥 틸 #00272b · 라임 #e0ff4f · 코랄 #ff6663      조합2: 주황 #e4572e · 남색 #29335c · 앰버 #f3a712
쓰는 법: 제목 흰색(또는 크림) + 강조 줄 앰버 + 작은 배지·카드 포인트 주황. 배경이 남색이면 글자는 흰색·앰버가 가장 잘 읽힌다(남색 위 주황은 작은 글씨에 약함)."""
def hexrgb(h): h = h.lstrip("#"); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
C1 = dict(bg=hexrgb("00272b"), hi=hexrgb("e0ff4f"), pt=hexrgb("ff6663"))
C2 = dict(pt=hexrgb("e4572e"), bg=hexrgb("29335c"), hi=hexrgb("f3a712"))
WHITE = (255, 255, 255); CREAM = (250, 244, 232)
def apply_to_engine(M):
    """clip_motion 엔진의 강조색(*글자* 표시와 칩·진행 막대)을 조합2 앰버로 바꾼다."""
    M.GOLD = C2["hi"] + (255,)
