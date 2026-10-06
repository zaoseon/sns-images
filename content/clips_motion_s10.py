"""네이버 클립 9:16판 '10월 손 없는 날'(10/6, R15: 클립은 9:16 영상으로만). 4:5 카드 클립(post_clip s10)을 대체한다.
문장은 글·카드에 있는 말만 쓰고, 날짜는 기존 검증 코드(손 없는 날=음력 끝자리 9·0)로 먼저 맞춘다.
사용: python3 content/clips_motion_s10.py -> clips_post/s10_9x16/s10_12s.mp4 (음악 포함)"""
import sys, os, subprocess, datetime as D
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, ".."); sys.path.insert(0, os.path.join(ROOT, "pipeline"))
from clip_motion import *
import music_plan as MP
try:
    import post_clip as PC
    cal = {d: PC.lunar(D.date(2026, 10, d)) for d in range(1, 32)}; hot = [d for d in cal if cal[d][1] % 10 in (9, 0)]
    assert hot == [9, 10, 19, 20, 29, 30], hot
    assert D.date(2026, 10, 9).weekday() == 4 and [d for d in hot if D.date(2026, 10, d).weekday() >= 5] == [10]
    print("날짜 검증 통과:", hot)
except ImportError as e: print("날짜 검증 건너뜀(불러오기 실패):", e)
SC = [
 (2.2, hook("10월 이사", "이사 날짜,\n*이 6일*이면 돼요", "v1_lowbun", size=104)),
 (2.6, point("손 없는 날은", "*9 · 10 · 19*\n*20 · 29 · 30일*", None, size=104)),
 (2.6, point("주말이 필요하다면", "*10일(토)*이에요", lambda c: text(c, "10월의 유일한\n주말 손 없는 날이에요", 760, .9, 76, color=DIM, path=MED), size=112)),
 (2.4, point("9일(금)은", "한글날 연휴\n*첫날*과 겹쳐요", lambda c: text(c, "예약이 일찍\n찰 수 있어요", 820, .9, 76, color=DIM, path=MED), size=104)),
 (2.2, lambda c: cta(c, "자세한 기준은\n블로그 손 없는 날 글에서")),
]
if __name__ == "__main__":
    out = os.path.join(ROOT, "clips_post", "s10_9x16"); p, d = render("s10_12s", SC, out); mi = MP.choose("fun", "s10-clip-9x16"); MP.mux(p, [x for x, _ in SC], mi, 117)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", "0.8", "-i", p, "-frames:v", "1", os.path.join(out, "s10_thumb.png")], check=True)
    print("완료", os.path.basename(p), round(d, 1), "초 · 음악", mi["style"], mi["bpm"])
