"""띠별 릴스 -> Metricool TRIAL_REEL 입력. 게시일 12:00 KST. 사용: python3 reel_payloads.py ../content/2026-w42.json"""
import json, os, sys
BASE = "https://raw.githubusercontent.com/zaoseon/sns-images/main/"
def build(src):
    folder = os.path.splitext(os.path.basename(src))[0]; out = []
    for i, p in enumerate(json.load(open(src))["posts"]):
        im = p["image"]
        if im["type"] != "tti": continue
        text = (f"{im['hook']}\n{im['name']}({im['years']})의 2027년, 한 줄로는 '{im['one']}'.\n\n"
                f"힘을 쓸 달과 아낄 달, 행운의 색까지 영상에 담았어요. 저장해 두고 1년 동안 보세요.\n"
                f"나머지 띠도 매일 아침 하나씩 올려요. 팔로우해 두면 내 띠 차례에 볼 수 있어요.\n\n"
                f"이 내용은 재미로, 그리고 나를 돌아보는 계기로 봐 주세요.\n\n#사주 #운세 #2027년운세 #띠별운세 #{im['name']}운세")
        dt = f"{p['date']}T12:00:00"
        out.append((f"{i+1:02d} reel {dt}", {"autoPublish": True, "draft": False, "firstCommentText": "", "hasNotReadNotes": False,
            "shortener": False, "smartLinkData": {"ids": []}, "publicationDate": {"dateTime": dt, "timezone": "Asia/Seoul"},
            "text": text, "media": [f"{BASE}{folder}/reel_{i+1:02d}.mp4"], "providers": [{"network": "instagram"}],
            "instagramData": {"type": "TRIAL_REEL", "isAiGenerated": False}, "descendants": []}))
    return out
if __name__ == "__main__":
    for k, v in build(sys.argv[1]): print("##", k); print(json.dumps(v, ensure_ascii=False))
