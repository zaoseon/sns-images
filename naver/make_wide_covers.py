"""네이버 블로그 대표 이미지를 링크 카드·정사각 목록에서 모두 안 잘리게 만든다 (10/4 대표 지적: 함께 볼 글 링크 카드에서 정사각 대표 이미지가 위 60%만 보이고 아래가 잘렸다).
원인: 링크 카드는 가로 약 1.67:1 틀이라 정사각 이미지를 위에서부터 자른다. 해결: 정사각 대표 이미지를 1200x720 가로 판 가운데(720x720)에 그대로 놓고 양옆은 이미지 가장자리 색으로 채운다.
-> 링크 카드는 전체가 보이고, 블로그 홈 정사각 자르기는 가운데 720x720 = 원래 이미지 그대로. 결과 naver/img/wide/<원래 파일명>. pages.json의 cover를 wide 판으로 바꾼다. 다시 실행해도 같은 결과."""
import os, json, statistics
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); IMG = os.path.join(HERE, "img"); OUT = os.path.join(IMG, "wide"); os.makedirs(OUT, exist_ok=True)
def edge_color(im):
    w, h = im.size; px = []
    for x in (2, w // 2, w - 3):
        for y in (2, h - 3): px.append(im.getpixel((x, y)))
    for y in (h // 2,): px += [im.getpixel((2, y)), im.getpixel((w - 3, y))]
    return tuple(int(statistics.median(p[i] for p in px)) for i in range(3))
pg = json.load(open(os.path.join(HERE, "pages.json"), encoding="utf-8")); done = []
for pid, p in pg.items():
    c = p.get("cover")
    if not c or c.startswith("wide/"): continue
    src = os.path.join(IMG, c)
    if not os.path.exists(src): continue
    im = Image.open(src).convert("RGB")
    if abs(im.width / im.height - 1.0) > 0.12: continue          # 이미 가로형이면 그대로
    bg = edge_color(im); can = Image.new("RGB", (1200, 720), bg); can.paste(im.resize((720, 720), Image.LANCZOS), (240, 0))
    can.save(os.path.join(OUT, c), quality=95); p["cover_old"] = c; p["cover"] = "wide/" + c; done.append(pid)
# 이미 올렸거나 올릴 정사각 대표 이미지 sq_<글>.jpg(thumb_sq)도 같은 방식으로 가로 판을 만든다(예: 여섯 운명학 글)
sq = []
for f in sorted(os.listdir(IMG)):
    if f.startswith("sq_") and f.endswith(".jpg"):
        im = Image.open(os.path.join(IMG, f)).convert("RGB"); bg = edge_color(im); can = Image.new("RGB", (1200, 720), bg)
        can.paste(im.resize((720, 720), Image.LANCZOS), (240, 0)); can.save(os.path.join(OUT, f), quality=95); sq.append(f[3:-4])
print("정사각 대표 이미지 가로 판", len(sq))
json.dump(pg, open(os.path.join(HERE, "pages.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("가로 판 만든 글", len(done), done)
