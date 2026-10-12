"""네이버 대표 이미지 가로 판(1200x720) 만들기 - make_wide_covers.py·regen_badges.py가 같이 쓴다.
10/12 대표 지적(블로그 목록 썸네일에서 제목 글자가 잘림): 네이버 목록은 가운데 정사각이 아니라 '얼굴을 가운데'로 정사각을 자른다.
캡처로 확인: n26(정월 원이 오른쪽 위) -> 오른쪽 끝 정사각 480~1200, n06 소띠(정월 원이 왼쪽) -> 왼쪽 끝 정사각 0~720.
그래서 정사각 원본(720x720)을 얼굴이 있는 쪽 끝에 붙인다. 그러면 얼굴 기준 자르기가 그림 끝에 막혀 정확히 원본 정사각이 잘려 나온다.
얼굴이 가운데(±40px)면 가운데에 둔다. 얼굴은 OpenCV 얼굴 찾기로 찾고, 못 찾으면 가운데(이전 방식)."""
import statistics
from PIL import Image
import numpy as np
def edge_color(im):
    w, h = im.size; px = []
    for x in (2, w // 2, w - 3):
        for y in (2, h - 3): px.append(im.getpixel((x, y)))
    for y in (h // 2,): px += [im.getpixel((2, y)), im.getpixel((w - 3, y))]
    return tuple(int(statistics.median(p[i] for p in px)) for i in range(3))
def face_x(sq):
    """720 정사각 기준 가장 큰 얼굴의 가운데 x. 없으면 None"""
    import cv2
    g = cv2.cvtColor(np.asarray(sq), cv2.COLOR_RGB2GRAY); best = None
    for casc in ("haarcascade_frontalface_default.xml", "haarcascade_frontalface_alt2.xml"):
        cc = cv2.CascadeClassifier(cv2.data.haarcascades + casc)
        for (x, y, w, h) in cc.detectMultiScale(g, 1.08, 4, minSize=(36, 36)):
            if best is None or w * h > best[2] * best[3]: best = (x, y, w, h)
        if best is not None: break
    return None if best is None else best[0] + best[2] / 2
def side(sq):
    fx = face_x(sq)
    if fx is None or abs(fx - 360) <= 40: return "center", fx
    return ("right" if fx > 360 else "left"), fx
def make(src_path, out_path):
    """정사각 원본 -> 1200x720. 반환 (붙인 쪽, 얼굴 x)"""
    im = Image.open(src_path).convert("RGB").resize((720, 720), Image.LANCZOS); s, fx = side(im)
    can = Image.new("RGB", (1200, 720), edge_color(im)); can.paste(im, ({"left": 0, "center": 240, "right": 480}[s], 0))
    can.save(out_path, quality=95); return s, fx
if __name__ == "__main__":   # python3 naver/wide_cover.py : img/wide/ 안의 모든 가로 판을 정사각 원본(img/<같은 이름>)에서 다시 만든다
    import os; H = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(H, "img", "wide"); from collections import Counter; cnt = Counter()
    for f in sorted(os.listdir(D)):
        src = os.path.join(H, "img", f)
        if f.endswith(".jpg") and os.path.exists(src): cnt[make(src, os.path.join(D, f))[0]] += 1
    print(dict(cnt))
