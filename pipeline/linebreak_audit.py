"""의미 단위 줄바꿈 검사(R08, 10/7 대표 지적: '책임지는 사랑을 / 해요'처럼 서술어만 한 줄에 남으면 어색하다).
명시한 줄바꿈(\\n)으로 나뉜 줄이 3글자 이하 짜투리이거나 서술어(해요·이에요·예요·요?·다)만 남으면 걸린다. 수식어 | 목적어+서술어('책임지는 | 사랑을 해요')로 나눈다.
사용: python3 pipeline/linebreak_audit.py"""
import os, re, glob
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.abspath(os.path.join(HERE, ".."))
END = ("해요", "이에요", "예요", "에요", "나요?", "까요?", "세요?", "해요.", "어요", "아요", "다")
def bad_lines(text):
    out = []; ls = [l.strip() for l in text.split("\n")]
    for i, l in enumerate(ls):
        l2 = l.replace("*", ""); han = re.sub(r"[^가-힣]", "", l2)
        if i > 0 and 0 < len(han) <= 3 and not re.search(r"\d", l2) and (l2.endswith(END) or len(han) <= 2): out.append(l)
    return out
def scan(files):
    hits = []
    for f in files:
        if not os.path.exists(f): continue
        for ln, line in enumerate(open(f, encoding="utf-8", errors="replace"), 1):
            for s in re.findall(r'"([^"\n]*\\n[^"\n]*)"', line):
                t = s.replace("\\n", "\n")
                if re.search(r"[가-힣]", t):
                    b = bad_lines(t)
                    if b: hits.append((os.path.basename(f), ln, t.replace("\n", " / ")[:50], b))
    return hits
if __name__ == "__main__":
    files = [os.path.join(R, "content", x) for x in ("pilot_variety.py", "clips_motion_2027.py", "reels_engine.py")] + [os.path.join(R, "pipeline", x) for x in ("data_reels.py", "new_tri_reels.py", "pick_reel.py", "motion_dots.py", "motion_kinetic.py")] + sorted(glob.glob(os.path.join(R, "content", "clips_motion*.py")))
    h = scan(files); print("명시한 줄바꿈 중 짜투리·서술어만 남은 곳:", len(h))
    for x in h[:12]: print(x)
