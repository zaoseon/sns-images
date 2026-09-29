"""content JSON -> Metricool createScheduledPost 입력(인스타·스레드 따로). 사용: python3 payloads.py ../content/2026-w42.json"""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render
BASE = "https://raw.githubusercontent.com/zaoseon/sns-images/main/"
def media(folder, i, img):
    pre = f"{i+1:02d}"; n = {"week": 9, "tti": 5}.get(img["type"])
    return [f"{BASE}{folder}/{pre}_{k}.jpg" for k in range(1, n+1)] if n else [f"{BASE}{folder}/{pre}.jpg"]
def build(src):
    folder = os.path.splitext(os.path.basename(src))[0]; out = []
    for i, p in enumerate(json.load(open(src))["posts"]):
        t = "08:00:00" if p["slot"] == "am" else "21:00:00"; dt = f"{p['date']}T{t}"; m = media(folder, i, p["image"])
        th, ig = p.get("threads"), p.get("instagram")
        if p["image"]["type"] == "week":
            th, ig = render.week_texts(p["image"]); th[0] += "\n\n#운세"
            ig += "\n\n#사주 #운세 #사주풀이 #자오선 #주간운세 #일진 #오늘의운세"
        common = {"autoPublish": True, "draft": False, "firstCommentText": "", "hasNotReadNotes": False, "shortener": False,
                  "smartLinkData": {"ids": []}, "publicationDate": {"dateTime": dt, "timezone": "Asia/Seoul"}}
        out.append((f"{i+1:02d} ig {dt}", dict(common, text=ig, media=m, providers=[{"network": "instagram"}],
                    instagramData={"type": "POST", "isAiGenerated": False}, descendants=[])))
        tm = [] if p.get("threads_image") is False else m[:1]
        out.append((f"{i+1:02d} th {dt}", dict(common, text=th[0], media=tm, providers=[{"network": "threads"}], threadsData={},
                    descendants=[{"text": x, "media": [], "providers": [{"network": "threads"}], "threadsData": {}} for x in th[1:]])))
    return out
if __name__ == "__main__":
    P = build(sys.argv[1]); json.dump(P, open("/tmp/payloads.json", "w"), ensure_ascii=False)
    for k, v in P: print(k, len(v["text"]), len(v["media"]), len(v["descendants"]))
