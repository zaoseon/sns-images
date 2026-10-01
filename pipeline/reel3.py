"""릴스 정식 모듈(10/1 밤, CARD_STYLE_GUIDE 규칙을 릴스에 적용). 1080x1920, 약 10.5초, 무음.
10/1 시안(2026-final3)에서 고친 점: 한자 글꼴 깨짐(병(▤)) 수정 / 얼굴 흐림 처리 폐기(2장면도 얼굴 선명) / 가짜 좋아요·공유 표시 삭제 /
글자는 모두 하단 그라데이션 구역에만(얼굴 보호선 위로 올라가면 크기 자동 축소) / 인스타 UI 안전 영역 지킴 / 강조색 세트별 / AI 고지 표지에만.
장면: A 훅 2.5초 → B 내용 5.5초 → C 팔로우 2.5초"""
import os, sys, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import carousel as C
from PIL import Image, ImageDraw
W, H = 1080, 1920
DARK = (20, 18, 17)
SAFE_TOP, SAFE_BOTTOM, SAFE_RIGHT, SAFE_LEFT = 230, 340, 160, 56
TEXT_W = W - SAFE_LEFT - SAFE_RIGHT          # 864: 오른쪽 버튼 줄을 피한 글자 폭
FACE_PROTECT = 1180                           # 이 선 위(얼굴)에는 글자 금지
def stage(face, face_h=1500):
    img = Image.new("RGB", (W, H), DARK)
    f = C.face_img(face, face_h); img.paste(f, ((W - f.width)//2, 170), f)
    g = Image.new("L", (1, 520)); [g.putpixel((0, y), int(255*(y/519)**1.4)) for y in range(520)]
    img.paste(Image.new("RGB", (W, 520), DARK), (0, FACE_PROTECT - 120), g.resize((W, 520)))
    d = ImageDraw.Draw(img); d.rectangle([0, FACE_PROTECT + 400, W, H], fill=DARK)
    return img, d
def handle(d, acc):
    d.ellipse([SAFE_LEFT, H-SAFE_BOTTOM-52, SAFE_LEFT+24, H-SAFE_BOTTOM-28], fill=acc)
    C.draw_line(d, SAFE_LEFT+38, H-SAFE_BOTTOM-30, "zaoseon.com", C.SEMI_F, 30, C.WHITE, C.WHITE)
def ai_notice(d):
    for i, t in enumerate(["※ 자오선의 상담가 정월은", "AI로 생성한 가상 캐릭터입니다"]):
        C.draw_line(d, W-SAFE_RIGHT, H-SAFE_BOTTOM-56+i*28, t, C.MED_F, 22, C.GRAY, C.GRAY, "r")
def stack_up(d, bottom, items):
    """items: [(kind, text, path, start, lo)] 위→아래 순서. 아래에서 위로 높이를 먼저 재서 FACE_PROTECT보다 올라가면 크기를 줄인다."""
    k = 1.0
    while True:
        y = bottom; placed = []
        for kind, text, path, start, lo in reversed(items):
            s = max(lo, int(C.fit(d, text, path, int(start*k), lo, TEXT_W)))
            h = int(s*1.28)*(text.count("\n")+1)
            y -= h + (24 if kind != "last" else 0); placed.append((text, path, s, y, h))
        if y >= FACE_PROTECT or k < 0.55: break
        k -= 0.05
    return list(reversed(placed))
def scene_a(S, out):
    img, d = stage(S["face"]); acc = C.hexrgb(S["accent"])
    C.pill(d, SAFE_LEFT, SAFE_TOP + 20, S["kicker"], acc, DARK, 34)
    items = [("sub", S["sub"], C.SEMI_F, 52, 34), ("title", S["hook"], C.BLACK_F, 98, 60)]
    for text, path, s, y, h in stack_up(d, H - SAFE_BOTTOM - 70, items):
        col = acc if text == S["sub"] else C.WHITE
        yy = y + s
        for l in text.split("\n"):
            C.draw_line(d, SAFE_LEFT, yy, l, path, s, col, acc); yy += int(s*1.28)
    handle(d, acc); ai_notice(d); img.save(out, quality=92)
def scene_b(S, out):
    img, d = stage(S["face"]); acc = C.hexrgb(S["accent"])
    C.pill(d, SAFE_LEFT, SAFE_TOP + 20, S["kicker"], acc, DARK, 34)
    rows = S["rows"]; n = len(rows); bottom = H - SAFE_BOTTOM - 100
    ts = int(min(C.fit(d, r[1], C.BLACK_F, 58, 36, TEXT_W) for r in rows)); PH = 46; GAP1 = 12; GAP2 = 30
    while True:
        rh = PH + GAP1 + int(ts*1.25) + GAP2; y = bottom - n*rh + GAP2
        if y >= FACE_PROTECT or ts <= 34: break
        ts -= 2
    for lab, txt in rows:
        C.pill(d, SAFE_LEFT, y, lab, acc, DARK, 30, padx=22, pady=8)
        C.draw_line(d, SAFE_LEFT, y + PH + GAP1 + int(ts*0.95), txt, C.BLACK_F, ts, C.WHITE, acc); y += rh
    handle(d, acc); img.save(out, quality=92)
def scene_c(S, out):
    img, d = stage(S["face"]); acc = C.hexrgb(S["accent"])
    cx = W//2 - (SAFE_RIGHT - SAFE_LEFT)//2; y = 1090
    qs = int(C.fit(d, S["q"], C.BLACK_F, 82, 50, TEXT_W))
    C.draw_line(d, cx, y + qs, S["q"], C.BLACK_F, qs, C.WHITE, acc, "c"); y += int(qs*1.4) + 16
    bt = "+ 떠오르면 태그하고 팔로우까지!"; bs = int(C.fit(d, bt, C.BLACK_F, 48, 34, TEXT_W - 80)); bw = int(C.width(d, bt, C.BLACK_F, bs)) + 80
    d.rounded_rectangle([cx - bw//2, y, cx + bw//2, y + 100], 50, fill=acc)
    C.draw_line(d, cx, y + 66, bt, C.BLACK_F, bs, DARK, DARK, "c"); y += 100 + 36
    ns = int(C.fit(d, S["next"], C.SEMI_F, 44, 30, TEXT_W))
    C.draw_line(d, cx, y + ns, S["next"], C.SEMI_F, ns, C.WHITE, acc, "c"); y += int(ns*1.3) + 14
    C.draw_line(d, cx, y + 30, "내 태어난 날 기운은 프로필 링크에서 1초", C.MED_F, 32, C.GRAY, C.GRAY, "c")
    handle(d, acc); img.save(out, quality=92)
def make(S, mp4, dur=(2.5, 5.5, 2.5), fade=0.35):
    base = mp4[:-4]; fs = [base + "_a.jpg", base + "_b.jpg", base + "_c.jpg"]
    scene_a(S, fs[0]); scene_b(S, fs[1]); scene_c(S, fs[2])
    cmd = ["ffmpeg", "-y", "-loglevel", "error"]
    for f, t in zip(fs, dur): cmd += ["-loop", "1", "-t", str(t), "-i", f]
    cmd += ["-f", "lavfi", "-t", str(sum(dur) - 2*fade), "-i", "anullsrc=r=44100:cl=stereo"]
    fl = (f"[0:v][1:v]xfade=transition=fade:duration={fade}:offset={dur[0]-fade:.2f}[v1];"
          f"[v1][2:v]xfade=transition=fade:duration={fade}:offset={dur[0]+dur[1]-2*fade:.2f}[v2];[v2]format=yuv420p,fps=30[vout]")
    cmd += ["-filter_complex", fl, "-map", "[vout]", "-map", "3:a", "-c:v", "libx264", "-crf", "20", "-c:a", "aac", "-b:a", "96k", "-shortest", "-movflags", "+faststart", mp4]
    subprocess.run(cmd, check=True)
    return fs
