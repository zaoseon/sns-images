"""글마다 '어디에 쓰이는 글인지'를 내보낸다(앱의 '글 주소' 구역이 주소가 필요한 글을 쓰임과 함께 보여 주기 위함).
- clips: 이 글을 블로그 스티커로 연결할 클립들(links_plan.CLIP 의 sticker)
- links: 이 글을 '함께 볼 글'로 거는 글들(REL: n26~n33, REL_FIX: n02~n25)
출력: ../content/post_needs.json   사용: python3 naver/export_post_needs.py"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import links_plan as LP
titles = json.load(open(os.path.join(HERE, "clip_titles.json"), encoding="utf-8"))
pub = json.load(open(os.path.join(HERE, "published.json"), encoding="utf-8"))
def short(pid): return LP.TITLE.get(pid) or (pub.get(pid, {}).get("title", pid))[:30]
def label(cid):
    t = titles.get(cid, "")
    if cid == "clip-post-s10": return "게시물 클립 (10월 손 없는 날)"
    if "SOP 클립" in t: return "글 연결 클립 " + t.replace("SOP 클립 · ", "").split(" · ")[0]
    return t.split(" · ")[0] or cid
needs = {}
def slot(pid): return needs.setdefault(pid, {"clips": [], "links": []})
for cid, m in LP.CLIP.items():
    if cid.endswith("-30s"): continue                       # 같은 클립의 30초판
    up = m["upload"]; slot(m["sticker"])["clips"].append({"label": label(cid), "upload": (up[0] + " " + up[1]) if up else "올라가 있음"})
for rel in (LP.REL, LP.REL_FIX):
    for p, (t, _) in rel.items(): slot(t)["links"].append({"id": p, "title": short(p), "at": LP.fmt(LP.POST_DT[p])})
for p, t in LP.FIX_KEEP.items(): slot(t)["links"].append({"id": p, "title": short(p), "at": LP.fmt(LP.POST_DT[p])})   # 바꾸지 않는 연결(허브 n01·손없는날 s10)
out = os.path.join(HERE, "..", "content", "post_needs.json"); json.dump(needs, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(needs), "편에 쓰임 표시:", {k: (len(v["clips"]), len(v["links"])) for k, v in sorted(needs.items())})
