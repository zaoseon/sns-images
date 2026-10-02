"""네이버 클립용 릴스: 인스타 릴스(reel_v2)와 같은 영상, 마지막 장만 네이버용
 - 다음 편 배지 "내일 낮 12시" → "다음 편" (인스타 일정 문구 제거)
 - 힌트 "프로필 링크에서 내 기운 1초만에 확인" → "블로그에서 내 기운 확인"
 - 변형 레이아웃은 쓰지 않는다(인스타에 예약된 릴스와 같은 모양 유지)
출력 2026-w40car3-reel/naver/<이름>.mp4   사용: python3 pipeline/naver_clips.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "content"))
import carousel_editor as CE, reel_v2 as RV
from carousel_sets import SETS
ORDER = [("byeong", None, "정(丁)일생 편"), ("jeong", "2026-10-02", "무(戊)일생 편"), ("mu", "2026-10-03", "기(己)일생 편"), ("gi", "2026-10-04", "경(庚)일생 편"),
         ("gyeong", "2026-10-06", "신(辛)일생 편"), ("sin", "2026-10-07", "임(壬)일생 편"), ("im", "2026-10-08", "계(癸)일생 편"), ("gye", "2026-10-09", "열 가지 한눈에 편")]
HINT = "블로그에서 내 기운 확인"
def defs():
    out = {}
    for key, date, nxt in ORDER:
        if key == "byeong": d = dict(RV.BYEONG)
        else:
            S = SETS[date]; d = dict(dayChar=S["dayChar"], hanja=S["hanja"], accent=S["accent"], face=("v5_halfup_v2" if S["face"] == "v5_halfup" else S["face"]), kicker=S["kicker"], coverTitle=S["coverTitle"], coverSub=S["coverSub"],
                                     personality=S["personality"], love=S["love"], money=S["money"], advice=S["advice"], chartNote=S["chartNote"], values=S["values"], highlight=S["highlight"], ctaQ=S["ctaQ"], nextTitle=nxt)
        d["variant"] = {}; d["nextTitle"] = nxt
        out[key] = (d, dict(nextBadge="다음 편", nextTitle=nxt, hint=HINT))
    return out
if __name__ == "__main__":
    RV.render([k for k, _, _ in ORDER], defs(), os.path.join(CE.ROOT, "2026-w40car3-reel", "naver"))
