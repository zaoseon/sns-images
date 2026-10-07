"""제작 가이드 그림판(10/7 대표: '숫자로 제시하면 확인을 못함'). 나쁜 예(예전·실제 문제 화면)와 좋은 예(지금 규칙)를 나란히 놓고 문제 부분을 표시한다.
사용: python3 pipeline/guide_visual_img.py -> 2026-motion/guide_visual_01.png ~ 09.png"""
import os, sys, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.abspath(os.path.join(HERE, "..")); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(R, "content"))
from PIL import Image, ImageDraw, ImageFont
import fonts_kit as K, clip_motion as M, pilot_variety as PV, clips_motion_2027 as S27
UP = "/mnt/user-data/uploads/"; OUT = os.path.join(R, "2026-motion")
GOLD = (231, 200, 141); CORAL = (255, 107, 90); TEAL = (110, 220, 190); WHITE = (255, 255, 255); BG = (11, 16, 32)
F = lambda n: ImageFont.truetype(K.P["pr_xb"], n); FD = lambda n: ImageFont.truetype(K.P["gm_bold"], n)
def still(sc, i, t, name):
    M.BRAND = True; p = f"/tmp/gv/{name}.png"; M.still(sc, i, t, p); return Image.open(p).convert("RGB")
def frame_of(mp4, t, name):
    p = f"/tmp/gv/{name}.png"; subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{t}", "-i", os.path.join(R, mp4), "-frames:v", "1", p], check=True); return Image.open(p).convert("RGB")
def fit(im, w, h):
    k = min(w / im.width, h / im.height); im2 = im.resize((int(im.width * k), int(im.height * k)), Image.LANCZOS); c = Image.new("RGB", (w, h), (4, 7, 18)); c.paste(im2, ((w - im2.width) // 2, (h - im2.height) // 2)); return c
def canvas(tag, title):
    c = Image.new("RGB", (1080, 1350), BG); d = ImageDraw.Draw(c); d.text((60, 44), tag, font=FD(40), fill=GOLD); d.text((60, 104), title, font=FD(66), fill=WHITE); return c, d
def pair(tag, title, bad, good, bad_note, good_note, marks_bad=(), marks_good=()):
    c, d = canvas(tag, title); W_, H_ = 460, 818; k = W_ / 1080
    for x0, im, col, lab, note, marks in ((60, bad, CORAL, "× 예전", bad_note, marks_bad), (560, good, TEAL, "○ 지금", good_note, marks_good)):
        fr = fit(im, W_, H_); dd = ImageDraw.Draw(fr, "RGBA")
        for kind, y0, y1, txt in marks:   # 세로 구간 표시(절대 y 기준) 또는 원 표시(kind="ring": y0=가운데 y, y1=반지름)
            if kind == "ring":
                cy, rr_ = int(y0 * (H_ / 1920)), int(y1 * (W_ / 1080)); dd.ellipse((W_ // 2 - rr_ + 0, cy - rr_, W_ // 2 + rr_, cy + rr_), outline=col + (255,), width=5); dd.rectangle((10, 38, W_ - 10, 92), fill=(0, 0, 0, 170)); dd.text((W_ / 2, 65), txt, font=F(34), fill=col, anchor="mm"); continue
            a, b = int(y0 * (H_ / 1920)), int(y1 * (H_ / 1920)); dd.rectangle((0, a, W_, b), fill=col + (95,)); dd.rectangle((0, a, W_, b), outline=col + (255,), width=4); dd.text((W_ / 2, (a + b) / 2), txt, font=F(34), fill=WHITE, anchor="mm", stroke_width=3, stroke_fill=(0, 0, 0))
        c.paste(fr, (x0, 250)); d.rounded_rectangle((x0 - 4, 246, x0 + W_ + 4, 250 + H_ + 4), radius=8, outline=col, width=6)
        d.text((x0, 1098), lab, font=FD(54), fill=col)
        for i, ln in enumerate(note.split("\n")): d.text((x0, 1166 + i * 52), ln, font=F(40), fill=WHITE)
    return c
def save(c, n): c.save(os.path.join(OUT, f"guide_visual_{n:02d}.png")); print("저장", n)
PV.AUDIT = True
A5 = still(PV.SC_A, 4, 3.0, "A5"); A3 = still(PV.SC_A, 2, 3.2, "A3"); A7 = still(PV.SC_A, 6, 3.2, "A7"); B6 = still(PV.SC_B, 5, 3.9, "B6"); C6 = still(PV.SC_C, 5, 3.2, "C6"); SK6 = still(S27.SC, 5, 2.8, "SK6"); SK2 = still(S27.SC, 1, 5.2, "SK2"); C3 = still(PV.SC_C, 2, 3.8, "C3")
leg_clip = frame_of("clips_sop/n41-c1_12s.mp4", 1.6, "legclip"); shot1 = Image.open(UP + "1791364410340_image.png").convert("RGB"); shot2 = Image.open(UP + "1791364426925_image.png").convert("RGB")
# 1) 화면 구성도
c, d = canvas("제작 가이드 그림판 · 1 / 9", "화면은 이렇게 나눠요"); fr = fit(A5, 560, 996); fd = ImageDraw.Draw(fr, "RGBA"); H_ = 996; kk = H_ / 1920
def band(y0, y1, col, a=80): fd.rectangle((0, int(y0 * kk), 560, int(y1 * kk)), fill=col + (a,)); fd.rectangle((0, int(y0 * kk), 560, int(y1 * kk)), outline=col + (255,), width=3)
band(335, 395, GOLD); band(475, 1375, TEAL, 45); band(1425, 1465, GOLD)
c.paste(fr, (60, 260)); d.rounded_rectangle((56, 256, 624, 1260), radius=8, outline=WHITE, width=3)
labs = [(360, GOLD, "맨 위 줄", "자오선 · 동서양 6개\n운명학 교차분석"), (700, TEAL, "여기에 글·그림", "위아래 가운데에\n두어요"), (1100, GOLD, "맨 아래 줄", "zaoseon.com\n(정월이 나오면\nAI 고지)")]
for y, col, h1, h2 in labs:
    yy = 260 + int(y * kk); d.line((624, yy, 660, yy), fill=col, width=5); d.text((676, yy - 34), h1, font=FD(46), fill=col)
    for i, ln in enumerate(h2.split("\n")): d.text((676, yy + 20 + i * 48), ln, font=F(40), fill=WHITE)
d.text((676, 1190), "맨 위·맨 아래 줄과는", font=F(40), fill=WHITE); d.text((676, 1238), "충분히 띄워요", font=F(40), fill=WHITE)
save(c, 1)
# 2) 상단 간격
save(pair("2 / 9", "맨 위 줄과 본문 간격", leg_clip, A5, "본문이 맨 위 줄에\n바짝 붙어요", "맨 위 줄에서 충분히\n떨어져 시작해요", [("gap", 395, 440, "너무 좁음")], [("gap", 395, 520, "충분히 띄움")]), 2)
# 3) 가운데
save(pair("3 / 9", "글은 위아래 가운데", shot1, A5, "글이 아래로\n쏠려 있었어요", "맨 위 줄과 주소\n사이 가운데예요", [], []), 3)
# 4) 아래 간격
save(pair("4 / 9", "아래 글과 주소 간격", shot2, A3, "아래 글이 주소에\n붙어 있었어요", "아래 글과 주소 사이를\n충분히 띄웠어요", [], [("gap", 1345, 1425, "충분히 띄움")]), 4)
# 5) 줄바꿈 (엔진으로 같은 모양 두 가지)
def title_scene(txt):
    def f(c): PV.fx_zoom(c, txt, 800, 0, 92, GOLD)
    return [(2.0, f)]
bad5 = still(title_scene("책임지는 사랑을\n해요"), 0, 1.6, "lb_bad"); good5 = still(title_scene("책임지는\n사랑을 해요"), 0, 1.6, "lb_good")
save(pair("5 / 9", "줄바꿈은 뜻 단위로", bad5, good5, "서술어만 한 줄에\n혼자 남았어요", "수식어 / 목적어+\n서술어로 나눠요"), 5)
# 6) 색 맞춤
def num_scene(match):
    def f(c):
        nums, nc = PV.color_row((("14", PV.GOLD), (":", WHITE + (255,)), ("86", PV.CORAL if match else PV.GOLD)), 190); L = nums; M.blit(c.fr, L, M.CX - L.width / 2, 700, 1.0); x0 = M.CX - L.width / 2
        for tx, col, cx in (("같은 말", PV.GOLD if match else M.DIM, nc[0]), ("다른 말", PV.CORAL if match else M.DIM, nc[2])):
            Lt = M.line_layers(tx, 60, col, M.BLACK, 600, 1.2)[0][0]; M.blit(c.fr, Lt, x0 + cx - Lt.width / 2, 950, 1.0)
    return [(2.0, f)]
save(pair("6 / 9", "숫자와 글은 같은 색", still(num_scene(False), 0, 1.6, "col_bad"), still(num_scene(True), 0, 1.6, "col_good"), "숫자와 글의 색이\n짝이 안 맞아요", "14·같은 말은 금색\n86·다른 말은 산호색"), 6)
# 7) 배경 차트
save(pair("7 / 9", "뒤 차트는 브랜드 차트", leg_clip, SK2, "직접 그린 고리라서\n브랜드 차트가 아니에요", "브랜드 황도 차트가\n뒤에서 돌아요", [("ring", 800, 470, "직접 그린 고리")], [("ring", 800, 520, "브랜드 황도 차트")]), 7)
# 8) 양산형
c, d = canvas("8 / 9", "모양이 다 같으면 안 돼요"); tw, th = 230, 409
legs = [frame_of("2026-w42reel-data/ig/vs14.mp4", 3.5, "l1"), frame_of("2026-w42reel-data/ig/star.mp4", 3.5, "l2"), frame_of("clips_sop/n36-c1_12s.mp4", 4.0, "l3"), frame_of("clips_sop/n44-c1_12s.mp4", 4.0, "l4")]
news = [A3, SK2, C3, B6]
d.text((60, 250), "× 예전: 비슷한 모양", font=FD(46), fill=CORAL); d.text((560, 250), "○ 지금: 모양이 달라요", font=FD(46), fill=TEAL)
for col, ims, cc in ((0, legs, CORAL), (1, news, TEAL)):
    for i, im in enumerate(ims):
        x = 60 + col * 500 + (i % 2) * 245; y = 330 + (i // 2) * 430; c.paste(fit(im, tw, th), (x, y)); d.rectangle((x - 2, y - 2, x + tw + 2, y + th + 2), outline=cc, width=4)
d.text((60, 1210), "장면 모양·글 효과·마무리를 영상마다 다르게 해요", font=F(42), fill=WHITE); d.text((60, 1262), "정월 얼굴도 한 영상에 한두 장면만 써요", font=F(42), fill=WHITE)
save(c, 8)
# 9) 마무리 5종
c, d = canvas("9 / 9", "마무리 5가지를 돌려 써요"); import reels_engine as RE
_d, _h = RE.all_defs()[("2026-w42reel-data/ig", "vs14")]; E1 = still(RE.scenes(_d, _h), 6, 2.8, "E1")
ends = [(E1, ("①", "팔로우 카드")), (B6, ("②", "댓글 질문 크게")), (C6, ("③", "정월과 알약")), (SK6, ("④", "한 줄 정리")), (A7, ("⑤", "숫자 반복"))]
tw, th = 190, 338
for i, (im, lab) in enumerate(ends):
    x = 40 + i * 200; c.paste(fit(im, tw, th), (x, 300)); d.rectangle((x - 2, 298, x + tw + 2, 300 + th + 2), outline=GOLD, width=3); d.text((x + tw / 2, 668), lab[0], font=FD(40), fill=GOLD, anchor="mm"); d.text((x + tw / 2, 716), lab[1], font=F(32), fill=WHITE, anchor="mm")
for i, ln in enumerate(["팔로우하고 더 많은 이야기 나눠요", "프로필 링크에서 생년월일 입력하고", "내 첫글자와 타고난 기운 알아보기", "이 문구는 5가지 모두에 들어가요"]): d.text((60, 810 + i * 62), ln, font=F(46), fill=WHITE if i < 3 else GOLD)
save(c, 9)
