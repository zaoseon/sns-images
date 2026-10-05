"""정월 사진 한 장으로 움직임을 시험한다(10/5, 대표 질문: 정월도 이렇게 움직일 수 있나).
방법: 한 장짜리 사진을 겹쳐서 얇은 움직임만 준다 — 숨쉬기, 머리 끄덕임, 머리카락 흔들림, 눈 깜빡임(눈꺼풀을 그려 덮음).
사용: python3 pipeline/char_anim_test.py -> 2026-motion/char_anim_test.mp4"""
import os, subprocess, math
import numpy as np, cv2
from PIL import Image
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
src = Image.open(os.path.join(R, "characters/cut/v2_straight.png")).convert("RGBA"); W0, H0 = src.size
base = np.array(src.crop((0, 0, W0, int(H0 * 0.66)))); H, W = base.shape[:2]          # 위 66%만 쓴다(릴스와 같은 자르기)
EYES = [(449, 344, 75), (579, 361, 89)]                                              # 눈 위치(찾아낸 값)
def smooth(a, b, x): t = np.clip((x - a) / (b - a), 0, 1); return t * t * (3 - 2 * t)
def with_blink(c):
    """c=0 뜬 눈, c=1 감은 눈. 눈두덩(눈 바로 위) 피부색에서 뺨 색으로 이어지는 그라데이션으로 눈꺼풀을 만들고, 주변과 자연스럽게 섞는다."""
    if c <= 0.02: return base.copy()
    rgb = np.ascontiguousarray(base[..., :3]); out = rgb.copy()
    for cx, cy, sz in EYES:
        up = rgb[cy - int(sz * 0.80): cy - int(sz * 0.62), cx - 14: cx + 14].reshape(-1, 3).mean(0)           # 눈두덩 위쪽 피부
        lo = rgb[cy + int(sz * 0.62): cy + int(sz * 0.80), cx - 14: cx + 14].reshape(-1, 3).mean(0)           # 눈 아래 뺨
        rx = int(sz * 0.50); ry = int(sz * 0.27 * c) + 2; h0 = int(sz * 0.62)
        patch = np.zeros((2 * h0, 2 * rx + 20, 3), np.float32)
        for yy in range(2 * h0): patch[yy] = up * (1 - yy / (2 * h0 - 1)) + lo * (yy / (2 * h0 - 1))            # 위→아래 색이 이어지는 면
        mask = np.zeros(patch.shape[:2], np.uint8); cv2.ellipse(mask, (rx + 10, h0 + 1), (rx, ry), -8, 0, 360, 255, -1)
        mask = cv2.GaussianBlur(mask, (0, 0), 2.2)
        region = out[cy - h0: cy + h0, cx - rx - 10: cx + rx + 10].astype(np.float32); mm = (mask.astype(np.float32) / 255)[..., None]
        out[cy - h0: cy + h0, cx - rx - 10: cx + rx + 10] = np.clip(region * (1 - mm) + patch * mm, 0, 255).astype(np.uint8)
        ln = np.zeros((H, W), np.uint8); cv2.ellipse(ln, (cx, cy + 1), (rx, max(ry, 2)), -8, 20, 160, 255, max(2, int(sz * 0.05))); ln = cv2.GaussianBlur(ln, (0, 0), 1.3).astype(np.float32) / 255 * 0.85
        out = out * (1 - ln[..., None]) + np.array([62, 40, 36])[None, None, :] * ln[..., None]
    res = base.copy(); res[..., :3] = np.clip(out, 0, 255).astype(np.uint8); return res
BL = {k: with_blink(k / 5) for k in range(0, 6)}
YY, XX = np.mgrid[0:H, 0:W].astype(np.float32); CX = W * 0.5
def frame(t, blink_level):
    img = BL[blink_level].copy()
    # 머리카락 흔들림: 가운데에서 먼 바깥쪽, 아래쪽일수록 크게
    wx = np.clip((np.abs(XX - CX) - 160) / 260, 0, 1) ** 1.4; wy = smooth(260, 900, YY)
    dx = 5.0 * wx * wy * np.sin(2 * math.pi * t / 2.8 + YY / 130.0); dy = 1.2 * wx * wy * np.sin(2 * math.pi * t / 2.2 + XX / 90.0)
    img = cv2.remap(img, XX + dx, YY + dy, cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))
    # 머리 끄덕임: 목을 축으로 살짝 돌리고, 몸과 부드럽게 이어 붙인다
    ang = 1.1 * math.sin(2 * math.pi * t / 4.0); M = cv2.getRotationMatrix2D((CX, 585), ang, 1.0)
    head = cv2.warpAffine(img, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))
    m = (1 - smooth(580, 780, YY))[..., None]; a = head.astype(np.float32) * m + img.astype(np.float32) * (1 - m); a[..., 3] = np.maximum(head[..., 3] * m[..., 0], img[..., 3] * (1 - m[..., 0]))
    img = a.astype(np.uint8)
    # 숨쉬기: 아래를 기준으로 아주 조금 늘고 줄고
    s = 1 + 0.006 * math.sin(2 * math.pi * t / 3.2); M2 = np.float32([[s, 0, CX * (1 - s)], [0, s, H * (1 - s) - 2.0 * math.sin(2 * math.pi * t / 3.2)]])
    return cv2.warpAffine(img, M2, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))
def blink_at(t):
    seq = [(1.5, 0.0), (1.56, 0.4), (1.62, 1.0), (1.68, 0.4), (1.76, 0.0)]; tt = t % 4.0
    for (a, ca), (b, cb) in zip(seq, seq[1:]):
        if a <= tt <= b: return ca + (cb - ca) * (tt - a) / (b - a)
    return 0.0
import sys
BLINK = "--no-blink" not in sys.argv
if __name__ == "__main__":
    VW, VH, FPS, DUR = 720, 1280, 30, 8.0; bg = np.zeros((VH, VW, 3), np.uint8); bg[:] = (22, 16, 12)
    for y in range(VH): bg[y] = (int(30 + 20 * y / VH), int(24 + 14 * y / VH), int(60 + 40 * y / VH))                 # 남색 바탕(BGR)
    out = os.path.join(R, "2026-motion", "char_anim_B.mp4" if BLINK else "char_anim_A.mp4"); os.makedirs(os.path.dirname(out), exist_ok=True)
    pr = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{VW}x{VH}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-crf", "17", "-pix_fmt", "yuv420p", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    sc = 0.78 * VW / W; frames = []
    for i in range(int(FPS * DUR)):
        t = i / FPS; f = frame(t, int(round(blink_at(t) * 5)) if BLINK else 0); fr = cv2.resize(f, (int(W * sc * 1.28), int(H * sc * 1.28)), interpolation=cv2.INTER_AREA)
        canvas = cv2.cvtColor(bg, cv2.COLOR_BGR2RGB).astype(np.float32); x0 = (VW - fr.shape[1]) // 2; y0 = VH - fr.shape[0] - 80
        al = fr[..., 3:4].astype(np.float32) / 255; canvas[y0:y0 + fr.shape[0], x0:x0 + fr.shape[1]] = canvas[y0:y0 + fr.shape[0], x0:x0 + fr.shape[1]] * (1 - al) + fr[..., :3] * al
        pr.stdin.write(canvas.astype(np.uint8).tobytes())
    pr.stdin.close(); pr.wait(); print(out)
