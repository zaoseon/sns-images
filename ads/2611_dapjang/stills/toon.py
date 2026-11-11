"""정월 실사 누끼를 웹툰풍(평면 색 + 외곽선)으로 바꾼다. 얼굴은 그대로, 그림체만 바뀐다(벤치마크 2차 C절).
쓰기: python3 toon.py ../../../characters/cut/v7_hanbok.png out.png"""
import sys, cv2, numpy as np
src, out = sys.argv[1], sys.argv[2]
im = cv2.imread(src, cv2.IMREAD_UNCHANGED)
bgr, a = im[:, :, :3], im[:, :, 3]
s = bgr.copy()
for _ in range(10):
    s = cv2.bilateralFilter(s, 9, 40, 9)
Z = s.reshape(-1, 3).astype(np.float32)
K = 12
_, lab, cen = cv2.kmeans(Z, K, None, (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0), 3, cv2.KMEANS_PP_CENTERS)
q = cen[lab.flatten()].reshape(s.shape).astype(np.uint8)
g = cv2.medianBlur(cv2.cvtColor(s, cv2.COLOR_BGR2GRAY), 9)
e = cv2.adaptiveThreshold(g, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, 9)
e = cv2.erode(255 - e, np.ones((1, 1), np.uint8))
e = cv2.GaussianBlur(e, (3, 3), 0)
line = np.array([40, 30, 28], np.float32)                     # 짙은 남갈색 선
k = (e.astype(np.float32) / 255.0 * 0.85)[..., None]
o = (q.astype(np.float32) * (1 - k) + line * k).astype(np.uint8)
# 누끼 가장자리에 흰 테두리(웹툰 스티커 느낌, 남색 판에서 가장자리가 지저분해 보이지 않게)
m = (a > 128).astype(np.uint8) * 255
ring = cv2.dilate(m, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (17, 17)))
canvas = np.zeros_like(im)
canvas[ring > 0] = (255, 255, 255, 255)
canvas[m > 0, :3] = o[m > 0]; canvas[m > 0, 3] = 255
cv2.imwrite(out, canvas)
