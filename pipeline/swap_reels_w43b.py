"""수비학 '계산법' 릴스 1편(10/5 대표 지시: 수비학 반응 근거로 추가). 인스타 10월 28일 20:00 칸 교체용. 예시 계산은 네이버 글 '생일 숫자로 보는 수비학'과 같다.
사용: EDITOR_HTML=pipeline/assets/carousel_editor_2026-10-03_v5.html python3 pipeline/swap_reels_w43b.py -> 2026-w43swap/ig/numerology_calc.mp4"""
import sys, os
sys.path.insert(0,'pipeline'); sys.path.insert(0,'content')
import carousel_editor as CE, reel_v2 as RV, new_tri_reels as N
defs = {
 "numerology_calc": N.tri("v11_mug", "내 생일 숫자,\n직접 더해 볼까요?", "한 자리가 될 때까지 더해요",
    [("1990년 5월 15일", "1+9+9+0+0+5+1+5=30, 3+0=3이라 3번이에요"), ("2000년 3월 5일", "2+0+0+0+0+3+0+5=10, 1+0=1이라 1번이에요"), ("내 생일은?", "한 자리가 될 때까지 계속 더하면 내 숫자가 나와요")],
    "같은 숫자여도 사주와 별자리가\n다르면 읽는 결이 달라요.", "내 숫자는\n몇 번일까요?", ["첫 번째 예", "두 번째 예", "내 차례"],
    dict(struct="S1", style="상큼 팝", seed=86, key="E"), advice_title="같은 숫자도\n사람마다 달라요", nt="여섯 운명학 이야기"),
}
for _k,(_d,_o) in defs.items(): _d["kicker"]="숫자로 보는 운명학"
if __name__ == "__main__":
    RV.render(list(defs), defs, os.path.join(CE.ROOT, "2026-w43swap", "ig"))
