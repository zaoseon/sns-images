"""네이버 일간 클립(무·기·경·신·임·계)을 CTA 간격 v5 + 새 순서 예고(다음 편 ○일생 편)로 다시 렌더 -> 2026-w42clip-sched/naver/<키>.mp4 (음악 포함). 이미 올린 정·병은 제외."""
import sys, os
sys.path.insert(0,'pipeline'); sys.path.insert(0,'content')
import carousel_editor as CE, reel_v2 as RV, reel_plan as RP
RP.NEXT.update({"mu":"기(己)일생 편","gi":"경(庚)일생 편","gyeong":"신(辛)일생 편","sin":"임(壬)일생 편","im":"계(癸)일생 편","gye":"갑(甲)일생 편"})
defs=RP.naver_defs(); keys=["mu","gi","gyeong","sin","im","gye"]
RV.render(keys, defs, os.path.join(CE.ROOT,"2026-w42clip-sched","naver"))
print("CLIPS_DONE")
