"""양산형 방지 검사(10/7 대표 지적: "같은 캐릭터·같은 효과가 계속 나오면 양산형 AI 피드로 보인다"). 앱 대기 영상의 처음·중간·끝 장면이 서로 얼마나 비슷한지 잰다.
방법: 장면을 16x16 흑백 지문(aHash)으로 바꿔 비슷한 것끼리 묶는다(거리 40/256 이하). 묶음이 클수록 같은 모양이 반복된다.
사용: python3 pipeline/diversity_audit.py"""
import os, re, json, subprocess, collections
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.abspath(os.path.join(HERE, ".."))
RAW_RE = re.compile(r"^https://raw\.githubusercontent\.com/zaoseon/sns-images/[^/]+/")
def ahash(im):
    a = np.asarray(im.convert("L").resize((16, 16), Image.LANCZOS)).astype(float); return (a > a.mean()).flatten()
def frame(p, t):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{t:.2f}", "-i", p, "-frames:v", "1", "/tmp/_dv.png"], check=True); return Image.open("/tmp/_dv.png")
def clusters(items, thr=40):
    par = list(range(len(items)))
    def f(x):
        while par[x] != x: par[x] = par[par[x]]; x = par[x]
        return x
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            if int((items[i][1] != items[j][1]).sum()) <= thr: par[f(i)] = f(j)
    g = collections.defaultdict(list)
    for i in range(len(items)): g[f(i)].append(items[i][0])
    return sorted(g.values(), key=len, reverse=True)
def run():
    d = json.load(open(os.path.join(R, "content", "reel_swaps.json"), encoding="utf-8")); vids = []
    for r in d:
        if r.get("status") in ("new", "wait", "hold") and r.get("video") and r.get("kind") in ("릴스", "글 연결 클립", "네이버 클립", "모션그래픽 견본", "카드 고르기", "릴스 추가(카드 고르기 주 1회 이어가기)"):
            p = os.path.join(R, RAW_RE.sub("", r["video"].split("?")[0]))
            if os.path.exists(p): vids.append((r["id"], r["kind"], p))
    res = {}
    H = {"처음": [], "중간": [], "끝": []}
    for vid, kind, p in vids:
        dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p], capture_output=True, text=True).stdout.strip() or 0)
        H["처음"].append((vid, ahash(frame(p, 1.0)))); H["중간"].append((vid, ahash(frame(p, dur * .5)))); H["끝"].append((vid, ahash(frame(p, max(0, dur - .9)))))
    out = {"영상": len(vids)}
    for k, v in H.items():
        c = clusters(v); out[k] = dict(가장큰묶음=len(c[0]), 묶음수=len(c), 상위=[len(x) for x in c[:4]], 예=c[0][:5])
    return out
if __name__ == "__main__":
    o = run(); print(json.dumps(o, ensure_ascii=False)[:900]); json.dump(o, open(os.path.join(R, "content", "audit", "diversity_audit.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
