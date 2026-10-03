"""모든 클립 장면의 글줄 나누기를 검사한다(10/3 대표: 줄바꿈이 어색함). 장면을 그려 보면서 text() 호출을 가로채 실제 줄을 기록한다.
사용: python3 pipeline/clip_text_audit.py  -> 문제 줄(3글자 이하 짜투리 줄, 서술어가 줄 맨 앞, 수동으로 쓴 줄이 중간에서 끊김)이 있으면 목록과 함께 종료 코드 1"""
import os, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "content"))
import clip_motion as M, clips_motion as CM
rec = []; orig = M.text
def spy(c, s, y, t0, size=104, color=M.WHITE, path=M.BLACK, maxw=800, lh=1.3, stagger=0.2, cx=M.CX, anim="rise"):
    sz = M.eff_size(s, size, maxw, path); fnt = M.font(path, sz); rec.append((s, sz, [["".join(ch[0] for ch in ln)][0] for ln in M.wrap(s, fnt, maxw)], s.count("\n") + 1))
    return orig(c, s, y, t0, size, color, path, maxw, lh, stagger, cx, anim)
M.text = spy; CM.text = spy if hasattr(CM, "text") else None
bad = []
for (cid, ver), scenes in CM.SC.items():
    for i, (d, f) in enumerate(scenes):
        rec.clear(); M.still(scenes, i, max(0.3, d - 0.35), os.path.join(tempfile.gettempdir(), "audit.png"))
        for s, sz, lines, manual in rec:
            if len(lines) > manual:                       # 엔진이 수동 줄을 더 쪼갰다 → 쪼갠 모양을 확인
                for j, ln in enumerate(lines):
                    bare = ln.replace(" ", "")
                    if len(bare) <= 3 and len(lines) > 1 and not any(ch in bare for ch in "≠→+=%"): bad.append((cid, ver, i, "짜투리 줄", lines))
                    if j and M._dep([(c, False) for c in ln.split(" ")[0]]) and len(ln.split(" ")) <= 2 and False: bad.append((cid, ver, i, "서술어 줄머리", lines))
            print(f"{cid}_{ver}s 장면{i+1} 글자{sz}: " + " / ".join(lines))
print("\\n문제 없음" if not bad else "\\n문제:\\n" + "\\n".join(map(str, bad))); sys.exit(1 if bad else 0)
