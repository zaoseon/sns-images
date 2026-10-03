"""데이터 시리즈 '100명 중 N명' 릴스. 근거: content/cross_data/README.md (자오선 엔진, 무작위 3,000명). 샘플 서체(Noto Sans CJK KR 굵은 고딕)·v5 CTA 간격·음악 포함.
사용: EDITOR_HTML=pipeline/assets/carousel_editor_2026-10-03_v5.html python3 pipeline/data_reels.py -> 2026-w42reel-data/ig/<키>.mp4"""
import sys, os
sys.path.insert(0,'pipeline'); sys.path.insert(0,'content')
import carousel_editor as CE, reel_v2 as RV, new_tri_reels as N
defs = {
 "vs14": N.tri("v8_gesture", "사주와 별자리,\n같은 말을 할까요?", "자오선 엔진 · 무작위 3,000명 시험",
    [("100명 중 14명", "사주와 별자리가 같은 방향을 가리켰어요"), ("100명 중 86명", "서로 다른 방향을 가리켰어요. 이게 보통이에요"), ("염소·황소자리 23%", "천칭자리는 5.6%. 별자리마다 크게 달라요")],
    "같은 말은 타고난 결이에요.\n다른 말은 내가 고를 수 있는 곳이에요.", "나는 어느 쪽일까요?", ["같은 방향", "다른 방향", "별자리별"],
    dict(struct="S1", style="상큼 팝", seed=71, key="E"), advice_title="다르다고\n틀린 게 아니에요", nt="여섯 운명학 시험"),
}
for _k,(_d,_o) in defs.items(): _d["kicker"]="자오선 데이터"
if __name__ == "__main__":
    RV.render(list(defs), defs, os.path.join(CE.ROOT, "2026-w42reel-data", "ig"))
