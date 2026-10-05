"""영상 품질 측정(10/5, 외부 모션 프롬프트의 '품질 기준'을 참고). 재생만 보고 통과시키지 않고 숫자로 잰다.
- 정지 구간: 앞뒤 프레임이 거의 같은 구간(읽을 시간을 주는 홀드 포함). 가장 긴 정지와 합계를 센다.
- 첫 프레임 채움: 첫 프레임에 글자·도형이 얼마나 차 있는지(빈 화면으로 시작하는지).
- 콘택트 시트: 0.5초 간격 프레임을 한 장에 모은다.
사용: python3 pipeline/video_qa.py 영상.mp4 [...]  -> /tmp/qa_<이름>.png + 숫자"""
import sys, os, subprocess, json
import numpy as np
from PIL import Image
def frames(path, fps=30, w=108, h=192):
    p = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", path, "-vf", f"fps={fps},scale={w}:{h}", "-f", "rawvideo", "-pix_fmt", "gray", "-"], capture_output=True)
    a = np.frombuffer(p.stdout, np.uint8); n = len(a) // (w * h); return a[: n * w * h].reshape(n, h, w).astype(np.float32)
def qa(path, fps=30, thr=0.35):
    F = frames(path, fps); n = len(F); d = np.abs(np.diff(F, axis=0)).mean(axis=(1, 2)); frozen = d < thr
    best = cur = 0; total = 0; runs = []
    for i, f in enumerate(frozen):
        if f: cur += 1; total += 1
        else:
            if cur: runs.append(cur)
            cur = 0
    if cur: runs.append(cur)
    longest = max(runs) / fps if runs else 0
    # 첫 프레임: 배경과 다른 정도(변화가 있는 화소 비율). 배경(우주)만 있으면 낮다
    f0 = F[0]; bgv = np.median(F[:, :, :], axis=0); fill0 = float((np.abs(f0 - bgv) > 40).mean())
    fill_mid = float((np.abs(F[n // 2] - bgv) > 40).mean())
    sec = n / fps
    return dict(file=os.path.basename(path), seconds=round(sec, 1), frozen_total=round(total / fps, 1), frozen_per30s=round(total / fps * 30 / sec, 1), longest_freeze=round(longest, 2), first_frame_fill=round(fill0 * 100, 1), mid_frame_fill=round(fill_mid * 100, 1), freezes_over_0_5s=sum(1 for r in runs if r / fps > 0.5))
def sheet(path, step=0.5, cols=8, w=135, h=240):
    p = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", path, "-vf", f"fps={1/step},scale={w}:{h}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True)
    a = np.frombuffer(p.stdout, np.uint8); n = len(a) // (w * h * 3); a = a[: n * w * h * 3].reshape(n, h, w, 3)
    rows = (n + cols - 1) // cols; S = Image.new("RGB", (cols * w, rows * h), (20, 20, 20))
    for i in range(n): S.paste(Image.fromarray(a[i]), ((i % cols) * w, (i // cols) * h))
    out = f"/tmp/qa_{os.path.splitext(os.path.basename(path))[0]}.png"; S.save(out); return out
if __name__ == "__main__":
    for f in sys.argv[1:]:
        r = qa(f); r["sheet"] = sheet(f); print(json.dumps(r, ensure_ascii=False))
