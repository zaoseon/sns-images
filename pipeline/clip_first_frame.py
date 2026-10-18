"""K-139(대표 10/18 14:05): 클립·릴스 첫 프레임(0초)에 제목·핵심 글이 이미 보여야 한다.

네이버 클립 목록은 영상 첫 장면을 표지로 보여 준다. clips_v3 16편은 제목이 0.2초부터 한 글자씩
들어오는 구조라 0초 프레임이 빈 판(워드마크·주소만)이었다(CT 10/18 14:40 실측: 15편 0초 글자 0~0.01%).

  python3 pipeline/clip_first_frame.py check clips_v3t/*.mp4        # 0초 프레임 검사(걸리면 종료 코드 1)
  python3 pipeline/clip_first_frame.py fix clips_v3m/v3-1019-n35.mp4 --out clips_v3t
      → 첫 장면이 다 들어온 시점부터 시작하는 새 파일(같은 이름, 새 폴더 — 원본 덮어쓰기 금지)

검사 기준: 0초 프레임 가운데 칸(위 15%~아래 18% 뺀 곳)의 글·그림 면적이 2초 프레임의 70% 이상, 그리고 2% 이상.
"""
import io, os, subprocess, sys

FAST = 0.70     # 0초 면적 / 2초 면적
MIN_AREA = 0.02


def _frame(path, t):
    import numpy as np
    from PIL import Image
    out = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.2f}", "-i", path, "-frames:v", "1",
                          "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True).stdout
    return np.asarray(Image.open(io.BytesIO(out)).convert("L"))


def area(path, t):
    import numpy as np
    a = _frame(path, t)
    h, w = a.shape
    c = a[int(h * .15):int(h * .82), int(w * .08):int(w * .92)].astype(int)
    return float((np.abs(c - np.median(c)) > 60).mean())


def check(path):
    """걸리면 까닭 목록, 통과하면 []."""
    a0, a2 = area(path, 0.0), area(path, 2.0)
    bad = []
    if a0 < MIN_AREA or (a2 > 0 and a0 < a2 * FAST):
        bad.append(f"0초 프레임에 글·그림이 {a0*100:.1f}% 뿐이에요(2초 {a2*100:.1f}%). 첫 장면이 다 보인 상태로 시작해야 해요(K-139).")
    return bad


def start_point(path, step=0.1, upto=2.5):
    """첫 장면이 2초 면적의 95% 이상 들어오고, 0.2초 뒤와 화면이 거의 같은(움직임 끝) 가장 이른 시각.
    면적만 보면 흐리게 들어오는 제목(n37)·겹쳐 들어오는 줄(n43)이 반쯤 투명한 채 첫 장면이 된다(10/18 실측)."""
    import numpy as np
    goal = area(path, 2.0) * 0.95
    t = 0.0
    while t <= upto:
        if area(path, t) >= goal:
            d = float(np.abs(_frame(path, t).astype(int) - _frame(path, t + 0.2).astype(int)).mean())
            if d < 0.5:
                return round(t, 2)
        t += step
    return round(upto, 2)


def fix(src, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, os.path.basename(src))
    if os.path.exists(dst):
        raise SystemExit(f"{dst} 가 이미 있어요 — 같은 이름 덮어쓰기 금지, 다른 폴더를 쓰세요.")
    ss = start_point(src)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", src, "-ss", f"{ss:.2f}",
                    "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", "-r", "30",
                    "-af", "afade=t=in:st=0:d=0.15", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", dst],
                   check=True)
    bad = check(dst)
    return dst, ss, bad


if __name__ == "__main__":
    cmd, args = sys.argv[1], [a for a in sys.argv[2:] if not a.startswith("--")]
    if cmd == "check":
        n = 0
        for p in args:
            b = check(p); n += bool(b)
            print(("걸림 " if b else "통과 ") + os.path.basename(p) + ("  " + b[0] if b else ""))
        sys.exit(1 if n else 0)
    if cmd == "fix":
        out = sys.argv[sys.argv.index("--out") + 1]
        args = [a for a in args if a != out]
        for p in args:
            dst, ss, b = fix(p, out)
            print(f"{os.path.basename(p)}: {ss:.1f}초부터 시작 → {dst} {'걸림 ' + b[0] if b else '0초 검사 통과'}")
