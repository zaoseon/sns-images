"""릴스 10개(10/2~10/11 12:00). 일간 릴스는 그날 아침 캐러셀과 같은 얼굴·강조색·문구. 사주·별자리·숫자 릴스는 w40fix 카드의 세 줄을 그대로 쓴다."""
import json, os
from carousel_sets import SETS
HERE = os.path.dirname(os.path.abspath(__file__))
YEL = "#ffd640"
fix = json.load(open(os.path.join(HERE, "2026-w40fix.json"), encoding="utf-8"))["posts"]
def cross(i):
    im = fix[i-1]["image"]; rows = []
    for badge, lab, val, desc in im["rows"]:
        rows.append(({"사주": "사주(동양)", "별자리": "별자리(서양)", "수비학": "수비학(숫자)"}[badge], val.replace("일생", "일생")))
    return im["title"], rows
def day(date, hook, nxt):
    S = SETS[date]
    return dict(face=S["face"], accent=S["accent"], kicker="오늘의 성격 카드", sub=S["coverSub"], hook=S["coverTitle"],
        rows=[("성격", S["personality"][0]), ("연애", S["love"][0]), ("돈", S["money"][0])], q=S["ctaQ"], next=nxt)
def tri(face, n, sub, nxt, q, hook=None):
    title, rows = cross(n)
    return dict(face=face, accent=YEL, kicker="정월의 사주·별자리·숫자", sub=sub, hook=hook or (title if "\n" in title else _split(title)), rows=rows, q=q, next=nxt)
def _split(t):
    # 쉼표·띄어쓰기 중간에서 두 줄로(의미 단위)
    words = t.split(" "); best = None
    for i in range(1, len(words)):
        a, b = " ".join(words[:i]), " ".join(words[i:])
        sc = abs(len(a) - len(b))
        if best is None or sc < best[0]: best = (sc, a, b)
    return best[1] + "\n" + best[2] if best else t
REELS = {
 "2026-10-02": day("2026-10-02", None, "내일: 사주·별자리·숫자 테스트"),
 "2026-10-03": tri("v3_ponytail", 1, "사주·별자리·숫자, 셋 중 몇 개 겹치나요?", "내일: 기(己)일생 편", "나는 몇 개 *겹치나요*?", "헤어진 뒤 다시\n연락하는 사람"),
 "2026-10-04": day("2026-10-04", None, "내일: 사주·별자리·숫자 테스트"),
 "2026-10-05": tri("v5_halfup_v2", 3, "동양과 서양이 같은 답을 했어요", "다음 편: 사주·별자리·숫자 테스트", "나는 몇 개 *겹치나요*?", "돈이 모이는\n사람의 공통점"),
 "2026-10-06": day("2026-10-06", None, "내일: 신(辛)일생 편"),
 "2026-10-07": day("2026-10-07", None, "내일: 임(壬)일생 편"),
 "2026-10-08": day("2026-10-08", None, "내일: 계(癸)일생 편"),
 "2026-10-09": day("2026-10-09", None, "내일: 사주·별자리·숫자 테스트"),
 "2026-10-10": tri("v7_hanbok", 4, "사주·별자리·숫자, 셋 중 몇 개 겹치나요?", "다음 편: 사주·별자리·숫자 테스트", "나는 몇 개 *겹치나요*?"),
 "2026-10-11": tri("v11_mug", 5, "사주·별자리·숫자로 보는 나의 속도", "다음 편: 사주·별자리·숫자 테스트", "나는 *어느 쪽*인가요?", "'일단 하자' vs\n'한 번 더 생각하자'"),
}
