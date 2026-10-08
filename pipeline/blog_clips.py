"""블로그 글 연결 클립(게시물형): 블로그 원고에 쓴 이미지에 캡션을 얹은 영상. 10/4 대표 지적: 글 연결 클립은 새 카드를 디자인하는 게 아니라 원고 이미지 + 캡션으로 만든다.
이미지 순서: 대표 이미지(a) -> 한눈에 보기(i, 있으면) -> 세 지도로 보면(b) -> 이번에 해 볼 것(c). 캡션은 원고에 있는 말만 짧게 줄여 쓴다.
사용: python3 pipeline/blog_clips.py  -> clips_sop/<id>_12s.mp4 (앱 글 연결 클립 영상 교체) + 썸네일"""
import os, sys, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); ROOT = os.path.join(HERE, "..")
from images_to_clip import images_to_clip
IMG = os.path.join(ROOT, "naver", "img")
CLIPS = {
 "n22-c1": ("22", ["첫눈에 반하는 사람, 어떤 결일까요?", None, "사주·별자리·숫자가 같은 쪽을 가리켜요", "세 번 만나 보고, 말이 통하는지 확인해요"], dict(style="발랄 우쿨렐레", seed=101, key="D")),
 "n26-c1": ("26", ["좋아해도 티가 안 나는 건 타고난 결일 수 있어요", "말보다 행동으로 사랑을 보여 주는 사람이에요", "사주·별자리·숫자가 가리키는 곳", "작은 표현 하나를 하루 안에 보내 봐요"], dict(style="통통 마림바", seed=102, key="F")),
 "n27-c1": ("27", ["말 한마디로 분위기를 바꾸는 사람", "설명하고 설득하는 일에서 빛나요", "불의 표현력과 말·관계의 별자리", "말하기 전에 결론 한 줄부터 정해요"], dict(style="상큼 팝", seed=103, key="A")),
 "n30-c1": ("30", ["빨리 달아오르고 빨리 식는 사람", "불씨를 계속 넣어 주면 오래 가요", "불이 많은 사주, 불의 별자리, 숫자 5", "시작하고 3개월 뒤에 점검해 봐요"], dict(style="경쾌 신스팝", seed=104, key="G")),
}
for cid, (n, caps, kw) in CLIPS.items():
    names = [f"naver_z{n}_a.jpg"] + ([f"naver_z{n}_i.jpg"] if os.path.exists(os.path.join(IMG, f"naver_z{n}_i.jpg")) else []) + [f"naver_z{n}_b.jpg", f"naver_z{n}_c.jpg"]
    if len(names) == 3: caps = [c for c in caps if c is not None]
    imgs = [(os.path.join(IMG, "master", x) if os.path.exists(os.path.join(IMG, "master", x)) else os.path.join(IMG, x)) for x in names]   # 10/8: 2560 원본이 있으면 그것을 쓴다(영상 1080폭에 줄여 쓰므로 선명); assert len(imgs) == len(caps), (cid, names, caps)
    out = os.path.join(ROOT, "clips_sop", f"{cid}_12s.mp4")
    t = images_to_clip(out, imgs, hold=2.8, first_hold=3.2, last_hold=3.6, captions=caps, **kw)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", "0.8", "-i", out, "-frames:v", "1", os.path.join(ROOT, "clips_sop", f"{cid}_thumb.png")], check=True)
    print(cid, names, round(t, 1), "s")
