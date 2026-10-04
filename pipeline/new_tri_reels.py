"""사주·별자리·숫자 릴스 새 3편(10/3 밤 대표 승인 '1단계+새로 만들기'): 10/5 사주vs별자리, 10/10 첫눈, 10/12 설득. 내용은 같은 주제 밤 테스트 카드와 같다.
사용: python3 pipeline/new_tri_reels.py  ->  2026-w42reel-new/ig/<키>.mp4"""
import sys, os
sys.path.insert(0,'pipeline'); sys.path.insert(0,'content')
import carousel_editor as CE, reel_v2 as RV
def tri(face, hook, sub, rows, note, q, badges, cfg, advice_title="셋 중 두 개 이상\n겹쳤다면", nb="다음 편", nt="사주·별자리·숫자 테스트"):
    d = dict(dayChar="", hanja="", accent="#ffd640", face=face, kicker="정월의 사주·별자리·숫자", coverTitle=hook, coverSub=sub,
             personality=[rows[0][0], rows[0][1]], love=[rows[1][0], rows[1][1]], money=[rows[2][0], rows[2][1]],
             advice=[advice_title, note], chartNote="", values=[.3,.3,.3,.3,.3], highlight=0, ctaQ=q, nextTitle=nt)
    return (d, dict(badges=badges, nextBadge=nb, nextTitle=nt, _cfg=cfg))
B3 = ["사주(동양)", "별자리(서양)", "수비학(숫자)"]
defs = {
 "vs": tri("v8_gesture", "사주와 별자리가\n다른 말을 할 때", "어느 쪽 말을 들어야 할까요?",
    [("타고난 결", "여러 풀이가 같은 답을 하면, 그건 바꾸기 어려운 나의 모양이에요"), ("고를 수 있는 곳", "풀이끼리 답이 갈리는 곳은, 내가 선택해서 바꿀 수 있는 영역이에요"), ("겹쳐 읽기", "사주·별자리·수비학 등 여섯 가지를 겹쳐, 같은 답과 다른 답을 나눠 봐요")],
    "모순처럼 보여도, 그 사이에 내가 서 있어요.", "나는 어느 쪽을 *더 믿어요*?", ["같은 말", "다른 말", "자오선"],
    dict(struct="S1", style="상큼 팝", seed=41, key="D"), advice_title="같은 답은 결,\n다른 답은 선택"),
 "first": tri("v1_lowbun", "3초 만에\n사랑에 빠지는 사람", "사주·별자리·숫자, 셋 중 몇 개 겹쳐요?",
    [("병화(丙)일생, 도화가 있는 사주", "태양처럼 바로 달아오르고, 사람을 끌어요"), ("양자리 · 사자자리", "직진하는 불의 별자리 (3/21~4/19, 7/23~8/22)"), ("3번 · 5번", "표현의 3, 새로움에 끌리는 5")],
    "하나도 안 겹친다면, 천천히 스며드는 사랑을 하는 사람일지도 몰라요.", "나는 몇 개 *겹쳐요*?", B3,
    dict(struct="S2", style="발랄 우쿨렐레", seed=42, key="G")),
 "talk": tri("v4_glasses", "이 사람이 말하면\n이상하게 다들 끄덕여요", "사주·별자리·숫자, 셋 중 몇 개 겹쳐요?",
    [("병화(丙) · 정화(丁)일생", "생각을 밖으로 비추는 불의 표현력"), ("쌍둥이자리 · 천칭자리", "말과 관계의 공기 별자리 (5/21~6/21, 9/23~10/22)"), ("3번 · 5번", "표현의 3, 순발력의 5")],
    "설명하고 설득하는 일에서 빛나요.\n말이 앞서지 않게만 조심하세요.", "나는 몇 개 *겹쳐요*?", B3,
    dict(struct="S3", style="경쾌 신스팝", seed=43, key="E"), advice_title="말은 무기,\n속도는 조절해요"),
}
if __name__ == "__main__":
    RV.render(list(defs), defs, os.path.join(CE.ROOT, "2026-w42reel-new", "ig"))
