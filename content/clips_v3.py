"""네이버 클립 v3 (10/15 대표 2차 지적: v2가 확정판 규칙을 안 따름 - 배지 글 가운데·박스 아래 글이 하단 핸들에 붙음·글자 작음·여백 불균형·입말).
v2(pipeline/clip_v2.py)는 엔진 밖에서 직접 그려 제작 가이드 확정판(docs/제작_가이드_확정판_2026-10-07.md)의 숫자를 어겼다. v3는 규칙 엔진(clip_motion)만 쓴다.
지키는 것
- 화면 구조(§1): 안전 영역 x 50~900·y 330~1470, 상단 띠(자오선·동서양 6개 운명학 교차분석), 하단 zaoseon.com = clip_motion.brand_layer. 묶음 470~1350·가운데 910 = autofit(R21).
- 배경(R22·R34): 브랜드 황도 차트 + 별, 날마다 navy·violet-moon·burgundy-sun·forest·teal 차례.
- 글(§3): 제목 G마켓 산스 96~104px, 본문 프리텐다드 Black 56px 이상(R46), 작은 머리말 52px, 한자는 세리프. 상자·알약 안 글은 정중앙(R18, anchor mm·층 높이 계산).
- 자막(R60·R61·R63·R64 엄격): 덩어리 2줄 이하·한 줄 14자 이하·장면 2~5초·장면 글 덩어리 3개 이하. 표는 한 장면 2행(R68).
- 효과(R36): 장면마다 다른 글 등장 효과·전환(clip_motion.FX), 클립마다 시작점을 옮긴다.
- 끝 장면(K-008): 그 글에 맞춘 질문 + '블로그에서 전체 글 보기'. 정월 얼굴은 쓰지 않는다(AI 표시 불필요).
- 첫 장면 모양은 클립마다 다르다(K-026·R43): 알림·표·노트·고르기·막대·선·저울·연대표·대화·원·눈금·일정표·영수증·병·배터리·가면.
사용: python3 content/clips_v3.py [id ...] (없으면 전부)  /  --check (자막·배치 검사만)
결과: clips_v3/<id>.mp4, <id>_thumb.jpg(첫 장면 완성 화면), <id>_check.jpg(장면마다 한 장)"""
import os, sys, math, json, subprocess, tempfile, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "..")); sys.path.insert(0, os.path.join(ROOT, "pipeline")); sys.path.insert(0, HERE)
from PIL import Image, ImageDraw
import clip_motion as M
from clip_motion import text, text_h, line_layers, blit, rr, e_out, e_back, cl, font, GOLD, WHITE, DIM, INK, CX, BLACK
import fonts_kit as FK
GM = FK.P["gm_bold"]; CORAL = (255, 138, 115, 255); TEAL = (127, 214, 200, 255); PANEL = (26, 33, 54, 235); PANEL2 = (45, 43, 42, 255)
OUT = os.path.join(ROOT, "clips_v3")
BGS = ["navy", "violet-moon", "burgundy-sun", "forest", "teal"]

# ───────── 단색 판(10/15 대표 재요청 mv9gs1t9: "저 배경에 저 내용과 구성이 어울린다고 생각하냐?") ─────────
# 약속 문자·노트·영수증·배터리 같은 생활 장면 뒤에 황도 차트·별·해달·색 그라데이션을 깔아 내용과 배경이 따로 놀았다.
# K-041(그라데이션·빛 방울 금지, 바탕 단색 #121214) · K-042(장식 그림 빼고 단색 면+선) · K-043(강조색 하나 #FFD640 + 누른 톤 #B09646 + 흰색, 면·선 무채색)을 따른다.
# 결과는 새 폴더 clips_v3s/(같은 이름 덮어쓰기 금지). 옛 판으로 다시 그리려면 SOLID=0 환경 변수.
SOLID = os.environ.get("SOLID", "1") != "0"
if SOLID:
    import numpy as _np
    OUT = os.path.join(ROOT, "clips_v3s")
    BG_SOLID = (18, 18, 20); YEL = (255, 214, 64, 255); YEL_D = (176, 150, 70, 255)
    GOLD = M.GOLD = YEL; CORAL = YEL_D; TEAL = WHITE; PANEL = (34, 34, 38, 255); PANEL2 = (44, 44, 48, 255); DIM = M.DIM = (200, 200, 204, 255)
    _YU = _np.array([1.0, (214 - 64) / (255 - 64), 0.0], dtype="float32")   # 노랑 #FFD640의 색 방향(최솟값 위에 얹는 비율)
    def _bg_solid(fr, t, total_t):
        fr.paste(BG_SOLID, (0, 0, M.W, M.H)); d = ImageDraw.Draw(fr, "RGBA")
        d.rectangle((70, 143, 880, 147), fill=(255, 255, 255, 40)); d.rectangle((70, 143, 70 + int(810 * cl(t / total_t)), 147), fill=YEL)
    def _palette(fr):
        """K-043: 색 있는 픽셀은 밝기·채도는 두고 색만 노랑 계열로, 거의 무채색인 픽셀은 회색으로. 장면 안 남은 색(얼굴·병·오행 원·빨간 줄)도 한 계열로 묶인다."""
        a = _np.asarray(fr).astype("float32"); mx = a.max(axis=2); mn = a.min(axis=2); ch = mx - mn
        col = mn[..., None] + ch[..., None] * _YU; gray = a.mean(axis=2, keepdims=True).repeat(3, axis=2)
        out = _np.where((ch > 24)[..., None], col, gray)
        fr.paste(Image.fromarray(_np.clip(out, 0, 255).astype("uint8")))
    def _brand_solid(fr, ai=False):
        _palette(fr); d = ImageDraw.Draw(fr, "RGBA"); R = 900
        d.text((60, 340), M._BF.TAG1, font=font(FK.P["gm_bold"], 42), fill=YEL, anchor="la")
        d.text((R, 346), M._BF.TAG2, font=font(FK.P["pr_xb"], 34), fill=(255, 255, 255, 242), anchor="ra")
        d.text((R, 1465), M._BF.URL, font=font(FK.P["gm_bold"], 40), fill=YEL_D, anchor="rd")
    M.background = _bg_solid; M.brand_layer = _brand_solid

# ───────── 공용 조각 (모두 엔진 text/line_layers를 거친다 → 자막 검사 대상) ─────────
def kick(c, s, y, t0=.05): return text(c, s, y, t0, 52, color=GOLD, maxw=820, stagger=0)
def title(c, s, y, t0=.2, size=100, color=WHITE): return text(c, s, y, t0, size, color=color, path=GM, maxw=820, lh=1.25, stagger=.22)
def body(c, s, y, t0=.5, size=58, color=WHITE): return text(c, s, y, t0, size, color=color, maxw=820, lh=1.4, stagger=.18)
def ctext(c, s, cx, cy, size, color, t0, path=BLACK, maxw=700, lh=1.3):
    """상자 안 글: 줄 묶음의 세로 가운데를 cy에 맞춘다(R18 정중앙)."""
    ls, step = line_layers(s, size, color, path, maxw, lh); tot = step * (len(ls) - 1) + size; y = cy - tot / 2 - 22 - size * .06 - (size * .1 if len(s) == 1 and '\u4e00' <= s <= '\u9fff' else 0)   # 한자 명조는 글자 몸이 아래로 처져 보여 살짝 올린다
    p = e_out((c.t - t0) / .4)
    for L in ls: blit(c.fr, L, cx - L.width / 2, y, c.alpha(cl(p * 1.6))); y += step
def box(c, x0, y0, x1, y1, t0, fill=PANEL, outline=None, r=34, ow=4):
    p = e_out((c.t - t0) / .4); L = rr(int(x1 - x0), int(y1 - y0), fill, outline, r, ow)
    blit(c.fr, L, x0 - 4, y0 - 4 + (1 - p) * 40, c.alpha(cl(p * 1.6)))
def pill(c, s, cy, t0, fill=GOLD, color=INK, size=56):
    fnt = font(BLACK, size); w = int(fnt.getlength(s)) + 96; h = size + 46; L = Image.new("RGBA", (w + 8, h + 8), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.rounded_rectangle((4, 4, 4 + w, 4 + h), radius=h // 2, fill=fill); d.text((4 + w / 2, 4 + h / 2), s, font=fnt, fill=color, anchor="mm")   # 알약 안 글 정중앙(R18)
    p = e_back((c.t - t0) / .45); s_ = max(.02, min(p, 1.06)); L2 = L.resize((max(1, int(L.width * s_)), max(1, int(L.height * s_))))
    blit(c.fr, L2, CX - L2.width / 2, cy - L2.height / 2, c.alpha(cl(p * 2)))
def end_scene(q):
    """끝 장면(K-008): 글에 맞춘 질문 + 블로그 안내 알약. 위아래 여백은 autofit이 맞춘다."""
    def f(c):
        y = title(c, q, 520, .05, 92); pill(c, "블로그에서 전체 글 보기", y + 110, .55)
        bob = 12 * math.sin(c.t * 6); ar = Image.new("RGBA", (80, 60), (0, 0, 0, 0)); ImageDraw.Draw(ar).polygon([(8, 6), (72, 6), (40, 54)], fill=GOLD)
        blit(c.fr, ar, CX - 40, y + 200 + bob, c.alpha(cl((c.t - .8) / .3)))
    return f
def row2(c, y, label, big, small, t0, col=GOLD):
    """표 한 행(R68): 왼쪽 라벨 56px, 오른쪽 큰 한자/값 + 작은 풀이. 행 높이 210."""
    box(c, 70, y, 900, y + 210, t0, outline=(224, 184, 102, 110), ow=3)
    ls, _ = line_layers(label, 58, WHITE, BLACK, 430, 1.25); tot = len(ls) * int(58 * 1.25); yy = y + 105 - tot / 2 - 22
    p = e_out((c.t - t0 - .1) / .4)
    for L in ls: blit(c.fr, L, 110 - 30, yy, c.alpha(cl(p * 1.6))); yy += int(58 * 1.25)
    ctext(c, big, 700, y + 105, 104, col, t0 + .25, maxw=200)   # 한자는 행 가운데, 뜻은 오른쪽에 나란히(겹치지 않게)
    ctext(c, small, 815, y + 105, 50, DIM, t0 + .35, maxw=120)

def bar_row(c, y, s, col, t0, size=58):
    """한 줄짜리 비교 행: 왼쪽 색 띠 + 글 한 덩어리(*낱말*은 금색). 행 높이 190, 글은 정중앙(R18)."""
    box(c, 70, y, 900, y + 190, t0, outline=col, ow=4); d = ImageDraw.Draw(c.fr, "RGBA"); p = e_out((c.t - t0) / .4)
    if p > .02: d.rounded_rectangle((70, y + 30 + M.DY + (1 - p) * 40, 86, y + 160 + M.DY + (1 - p) * 40), radius=8, fill=col[:3] + (int(255 * cl(p * 1.6)),))
    ctext(c, s, CX + 10, y + 95, size, WHITE, t0 + .1, maxw=760)

# ───────── 클립별 장면 ─────────
def n33():
    def s1(c):
        y = kick(c, "약속 취소 문자를 받은 날", 520)
        p = e_out((c.t - .3) / .5); L = rr(780, 170, (245, 245, 250, 255), None, r=44); d = ImageDraw.Draw(L)
        d.ellipse((30, 41, 118, 129), fill=GOLD); d.text((74, 86), "!", font=font(BLACK, 56), fill=INK, anchor="mm")
        d.text((146, 62), "친구", font=font(BLACK, 40), fill=(30, 30, 40, 255), anchor="lm"); d.text((146, 116), "오늘 약속 미룰까? ㅠㅠ", font=font(BLACK, 50), fill=(60, 60, 72, 255), anchor="lm")
        blit(c.fr, L, CX - L.width / 2, y + 30 + (1 - p) * -80, c.alpha(cl(p * 2)))
        title(c, "속으로 웃은 적\n있나요?", y + 270, .7, 104)
    def s2(c):
        y = kick(c, "사주에서 화개 찾는 법", 470); row2(c, y + 30, "원숭이·쥐·용띠", "辰", "용", .3); row2(c, y + 270, "호랑이·말·개띠", "戌", "개", .8)
    def s3(c):
        y = kick(c, "네 기둥에 이 글자가 있나요?", 470); row2(c, y + 30, "뱀·닭·소띠", "丑", "소", .3); row2(c, y + 270, "돼지·토끼·양띠", "未", "양", .8)
    def s4(c):
        y = title(c, "사람이 싫은 게\n아니에요", 520, .05, 100); body(c, "혼자 있을 때\n힘이 다시 차는 거예요", y + 50, .7, 60, DIM)
    def s5(c):
        y = kick(c, "이번 주에 해 볼 것", 500); box(c, 70, y + 30, 900, y + 330, .3, outline=GOLD, ow=4); ctext(c, "약속 잡을 때\n쉬는 날을 먼저 말해요", CX, y + 180, 62, WHITE, .5, maxw=760)
    return [(2.8, s1), (3.4, s2), (3.4, s3), (2.8, s4), (3.0, s5), (2.6, end_scene("나는 약속 취소가\n반가운 편인가요?"))]

def n34():
    def notebook(c, k, y0, circle=False):
        """줄 노트(R78 O6: 반추는 '종이로 옮기기' 장면). 줄 위에 글, 첫 줄에 빨간 동그라미."""
        x0, x1 = 110, 830; h = 2 * 120 + 70
        box(c, x0, y0, x1, y0 + h, .2, fill=(250, 248, 240, 255), r=24)
        d = ImageDraw.Draw(c.fr, "RGBA"); dy = M.DY; a = cl(e_out((c.t - .2) / .4) * 1.6)
        if a > .5:
            d.line((x0 + 70, y0 + dy + 10, x0 + 70, y0 + h + dy - 10), fill=(220, 120, 120, 255), width=3)
            for j in range(2): d.line((x0 + 20, y0 + 115 + j * 120 + dy, x1 - 20, y0 + 115 + j * 120 + dy), fill=(190, 205, 230, 255), width=2)
        items = ["월요일 회의 준비", "그때 그 말 괜찮았나"]
        for j, s in enumerate(items[:k]):
            L = line_layers(s, 56, (31, 58, 122, 255), BLACK, 640, 1.2)[0][0]; p = e_out((c.t - .5 - j * .5) / .4); yt = y0 + 115 + j * 120 - 72
            blit(c.fr, L, x0 + 100 - 30, yt - 22, c.alpha(cl(p * 1.6)))
        if circle:
            p = e_out((c.t - 1.4) / .5); w = font(BLACK, 56).getlength(items[0]); yt = y0 + 115 - 72
            if p > .02: d.arc((x0 + 78, yt - 14 + dy, x0 + 122 + w, yt + 76 + dy), -90, -90 + 360 * p, fill=(210, 69, 59, 255), width=7)
    def s1(c):
        y = kick(c, "일요일 밤마다", 470); y = title(c, "같은 생각이\n자꾸 도나요?", y + 10, .2, 104); notebook(c, 1, y + 50)
    def s2(c):
        y = title(c, "떠오르는 걸\n종이에 다 적어요", 480, .05, 96); notebook(c, 2, y + 50, circle=True)
    def s3(c):
        y = kick(c, "심리학에서는 이걸", 520); y = title(c, "'반추'라고\n불러요", y + 10, .2, 104); body(c, "놀렌-혹세마, 1991", y + 40, .8, 48, DIM)
    def s4(c):
        y = kick(c, "사주·별자리·숫자로 보면", 500); box(c, 70, y + 30, 900, y + 300, .3); ctext(c, "물의 날, 게·물고기자리,\n숫자 7과 2", CX, y + 165, 56, WHITE, .5, maxw=780)
    def s5(c):
        title(c, "오늘 잠들기 전\n잘한 일 하나", 520, .05, 100); body(c, "한 줄만 적어 보세요", 820, .7, 60, GOLD)
    return [(2.8, s1), (3.6, s2), (3.0, s3), (3.2, s4), (2.6, s5), (2.6, end_scene("일요일 밤 생각,\n어디서 오나요?"))]

def n35():
    def card(c, y, letter, a, b, t0, col):
        box(c, 70, y, 900, y + 190, t0, outline=col, ow=4)
        p = e_back((c.t - t0 - .1) / .4); L = Image.new("RGBA", (110, 110), (0, 0, 0, 0)); ImageDraw.Draw(L).ellipse((5, 5, 105, 105), fill=col); ImageDraw.Draw(L).text((55, 57), letter, font=font(BLACK, 58), fill=INK, anchor="mm")
        blit(c.fr, L, 110, y + 40, c.alpha(cl(p * 2)))
        ctext(c, a, 560, y + 95, 58, WHITE, t0 + .2, maxw=620)   # 풀이(관록궁·명궁 등)는 설명 글에 둔다(R64: 장면 글 덩어리 3개 이하)
    def s1(c):
        y = title(c, "월요일 출근길,\n왜 무거울까요?", 480, .05, 100); card(c, y + 40, "A", "일 방식이 안 맞아서", "일을 보는 관록궁", .6, GOLD)
    def s2(c):
        y = kick(c, "또는", 520); card(c, y + 30, "B", "모습을 바꿔야 해서", "", .2, CORAL); card(c, y + 260, "C", "쉬는 시간이 모자라서", "", .9, TEAL)
    def s3(c):
        y = kick(c, "사주 일간의 첫 속도", 470)
        for i, (el, s, col) in enumerate((("불", "시작이 빨라요", CORAL), ("물", "먼저 살펴요", TEAL))):
            yy = y + 40 + i * 250; box(c, 70, yy, 900, yy + 210, .3 + i * .5, outline=col, ow=4); ctext(c, el, 200, yy + 105, 88, col, .4 + i * .5, maxw=200); ctext(c, s, 590, yy + 105, 60, WHITE, .5 + i * .5, maxw=520)
    def s4(c):
        y = kick(c, "이번 주에 해 볼 것", 500); title(c, "월요일 첫 일\n하나만 정해 두기", y + 20, .3, 96)
    return [(3.0, s1), (3.6, s2), (3.4, s3), (2.8, s4), (2.6, end_scene("내 월요일 무게는\n어디서 오나요?"))]

def n36():
    def curve(c, upto):
        d = ImageDraw.Draw(c.fr, "RGBA"); gy = 1040 + M.DY; x0, x1 = 190, 750; prev = None   # 양 끝 라벨이 안전 영역(x 50~900) 안에 들도록
        d.line((x0, gy, x1, gy), fill=(214, 218, 228, 160), width=5)
        for i in range(0, 101):
            t = i / 100; v = .82 - .5 * math.sin(math.pi * t) + .1 * math.sin(6 * t); p = (x0 + t * (x1 - x0), gy - 40 - v * 260)
            if prev and t <= cl((c.t - .2) / 1.2): d.line((prev, p), fill=GOLD, width=8)
            prev = p
        for k, (t, lab, col) in enumerate(((0.1, "시작 직후", TEAL), (0.5, "중반", CORAL), (0.9, "마무리 직전", GOLD))[:upto]):
            px = x0 + t * (x1 - x0); a = e_back((c.t - 1.2 - k * .4) / .4)
            if a > .02: d.ellipse((px - 20, gy - 20, px + 20, gy + 20), fill=col)
            L = line_layers(lab, 48, col, BLACK, 300, 1.2)[0][0]; blit(c.fr, L, px - L.width / 2, 1090 - 22, c.alpha(cl(a * 2)))
    def s1(c):
        title(c, "나는 어디서\n멈추나요?", 480, .05, 104); curve(c, 3)
    def s2(c):
        y = kick(c, "멈추는 곳마다 해 볼 것", 470)
        bar_row(c, y + 40, "*시작 직후*면 시작을 작게", TEAL, .3); bar_row(c, y + 270, "*중반*이면 점검일 하나", CORAL, .8)
    def s3(c):
        y = kick(c, "당사주는 인생을 네 칸으로", 470)
        for i, (a, b) in enumerate((("초년", "해"), ("중년", "달"), ("말년", "날"), ("평생", "시각"))):
            x = 70 + (i % 2) * 425; yy = y + 40 + (i // 2) * 250; box(c, x, yy, x + 405, yy + 220, .3 + i * .25)
            ctext(c, a, x + 202, yy + 110, 80, WHITE, .4 + i * .25, maxw=360)
        body(c, "해·달·날·시각 자리에\n별이 하나씩 놓여요", y + 560, 1.4, 54, DIM)
    def s4(c):
        y = kick(c, "이번 주에 해 볼 것", 500); title(c, "멈춘 일 하나를\n오늘 5분만", y + 20, .3, 100)
    return [(3.4, s1), (3.4, s2), (3.4, s3), (2.8, s4), (2.6, end_scene("나는 어느 구간에서\n멈추는 편인가요?"))]

def n37():
    def scale(c, tilt):
        d = ImageDraw.Draw(c.fr, "RGBA"); cy = 920 + M.DY; a = math.radians(tilt * cl((c.t - .4) / .8))
        d.polygon([(CX - 50, cy + 260), (CX + 50, cy + 260), (CX, cy)], fill=GOLD)
        lx, ly, rx, ry = CX - 270 * math.cos(a), cy - 270 * math.sin(-a), CX + 270 * math.cos(a), cy + 270 * math.sin(-a)   # 접시가 x 70~870 안에
        d.line((lx, ly, rx, ry), fill=GOLD, width=10)
        for (x, y_, lab, col) in ((lx, ly, "남의\n하이라이트", CORAL), (rx, ry, "내\n일상", TEAL)):
            d.line((x, y_, x, y_ + 90), fill=GOLD, width=4); d.rounded_rectangle((x - 125, y_ + 90, x + 125, y_ + 260), radius=30, fill=col)
            ls, st = line_layers(lab, 50, INK, BLACK, 230, 1.2); yy = y_ + 175 - (st + 50) / 2 - 22 - M.DY
            for L in ls: blit(c.fr, L, x - L.width / 2, yy, c.alpha(1)); yy += st
    def s1(c):
        title(c, "비교하면 왜\n작아질까요?", 470, .05, 104); scale(c, 14)
    def s2(c):
        y = kick(c, "심리학에서는 이걸", 520); y = title(c, "'사회 비교'라고\n불러요", y + 10, .2, 100); body(c, "페스팅거, 1954", y + 40, .8, 48, DIM)
    def s3(c):
        y = kick(c, "견주는 대상을 바꿔요", 500); box(c, 70, y + 40, 900, y + 230, .3, outline=CORAL); ctext(c, "그 사람의 승진 소식", CX, y + 135, 56, DIM, .4, maxw=780)
        box(c, 70, y + 290, 900, y + 480, .9, outline=TEAL, ow=5); ctext(c, "어제의 나보다\n나아진 한 가지", CX, y + 385, 56, WHITE, 1.0, maxw=780)
    def s4(c):
        y = kick(c, "부러운 마음이 들면", 500); title(c, "나는 지금\n무엇을 바라지?", y + 20, .3, 100)
    return [(3.4, s1), (3.0, s2), (3.6, s3), (2.8, s4), (2.6, end_scene("요즘 나를 작게 하는\n비교는 어디서 오나요?"))]

def n38():
    def s1(c):
        y = title(c, "오늘은 상강,\n가을의 마지막 문턱", 470, .05, 96); x = 140
        for i, (date, name, col) in enumerate((("10/23", "상강 · 오늘", GOLD), ("11/7", "입동", DIM))):
            yy = y + 60 + i * 150; d = ImageDraw.Draw(c.fr, "RGBA"); p = e_back((c.t - .5 - i * .4) / .4)
            if i: d.line((x, yy - 150 + 40 + M.DY, x, yy + M.DY), fill=(214, 218, 228, 140), width=5)
            r = 26 if i == 0 else 18
            if p > .02: d.ellipse((x - r, yy + 20 - r + M.DY, x + r, yy + 20 + r + M.DY), fill=col)
            L = line_layers(date + "  " + name, 60 if i == 0 else 54, col if i == 0 else WHITE, BLACK, 640, 1.2)[0][0]; blit(c.fr, L, x + 60 - 30, yy + 20 - 22 - 34, c.alpha(cl(p * 2)))
    def s2(c):
        y = kick(c, "오늘 두 풀이가 같이 바뀌어요", 470)
        bar_row(c, y + 40, "*사주* 개(戌)의 달 한가운데", GOLD, .3, 56); bar_row(c, y + 270, "*별자리* 전갈자리 시작", CORAL, .8, 56)
    def s3(c):
        y = title(c, "마음이 허하면\n적어 볼 두 가지", 470, .05, 96)
        bar_row(c, int(y + 50), "올해 이룬 것 세 가지", GOLD, .7); bar_row(c, int(y + 270), "내려놓을 것 하나", TEAL, 1.3)   # 엔진 check_row는 x 40에서 시작해 안전 영역 밖이라 쓰지 않는다
    def s4(c):
        y = kick(c, "그리고", 520); title(c, "안부를 묻고 싶은\n한 사람에게 메시지", y + 20, .3, 92)
    return [(3.6, s1), (3.4, s2), (3.4, s3), (2.8, s4), (2.6, end_scene("찬 바람이 불면\n누가 떠오르나요?"))]

def n39():
    def screen(c, msgs, t0):
        x0, x1, y0 = 110, 830, 600; box(c, x0, y0, x1, y0 + 560, t0, fill=(PANEL2 if SOLID else (24, 22, 21, 255)), outline=((90, 90, 96, 255) if SOLID else None), ow=2, r=40)
        d = ImageDraw.Draw(c.fr, "RGBA"); y = y0 + 40 + M.DY
        for k, (who, s) in enumerate(msgs):
            a = e_out((c.t - t0 - .3 - k * .45) / .35)
            if a <= .01: continue
            L, st = line_layers(s, 52, WHITE if who == "you" else INK, BLACK, 520, 1.25); L = L[0]; w = L.width - 60 + 70; h = 96
            xx = x0 + 30 if who == "you" else x1 - 30 - w
            d.rounded_rectangle((xx, y, xx + w, y + h), radius=34, fill=(45, 43, 42, int(255 * a)) if who == "you" else GOLD[:3] + (int(255 * a),))
            blit(c.fr, L, xx + 35 - 30, y - M.DY + 48 - 22 - 52 * .62, c.alpha(a)); y += h + (14 if k + 1 < len(msgs) and msgs[k + 1][0] == who else 36)
        return y
    def s1(c):
        title(c, "답장 기다리다\n폰만 보나요?", 470, .05, 100)
        screen(c, [("me", "이번 주말에 시간 돼?"), ("you", "읽음 · 3시간 전")], .6)
    def s2(c):
        y = kick(c, "사주로 보면 기다리는 모양", 470)
        for i, (el, s, col) in enumerate((("불", "자꾸 확인해요", CORAL), ("물", "속으로 생각이 깊어져요", TEAL))):
            yy = y + 40 + i * 250; box(c, 70, yy, 900, yy + 210, .3 + i * .5, outline=col); ctext(c, el, 180, yy + 105, 80, col, .4 + i * .5, maxw=160); ctext(c, s, 590, yy + 105, 54, WHITE, .5 + i * .5, maxw=560)
    def s3(c):
        y = kick(c, "심리학에서는", 520); y = title(c, "'불안형 애착'이라고\n불러요", y + 10, .2, 92); body(c, "진단이 아니라 경향이에요", y + 40, .8, 54, DIM)
    def s4(c):
        y = kick(c, "이번 주에 해 볼 것", 470); box(c, 70, y + 40, 900, y + 400, .3, outline=GOLD)
        ctext(c, "기다릴 날짜 하나", CX, y + 150, 58, WHITE, .5, maxw=780); ctext(c, "그 사이 내가 할 일 하나", CX, y + 290, 58, GOLD, .9, maxw=780)
    return [(3.4, s1), (3.4, s2), (3.0, s3), (3.2, s4), (2.6, end_scene("기다릴 때 나는\n어느 쪽인가요?"))]

def n40():
    ELC = [((168, 116, 47, 255), "土", "흙", "챙기는 사람"), ((63, 111, 163, 255), "水", "물", "살피는 사람"), ((208, 72, 44, 255), "火", "불", "띄우는 사람")]
    def s1(c):
        title(c, "가족 모임 뒤\n유독 지치나요?", 480, .05, 100)
        for i, (col, han, el, role) in enumerate(ELC):
            cx = 200 + i * 270; p = e_back((c.t - .6 - i * .3) / .4); cy = 960
            L = Image.new("RGBA", (230, 230), (0, 0, 0, 0)); ImageDraw.Draw(L).ellipse((5, 5, 225, 225), fill=col); ImageDraw.Draw(L).text((115, 117), han, font=M.serif(120), fill=WHITE, anchor="mm")
            s_ = max(.02, min(p, 1.05)); L2 = L.resize((max(1, int(230 * s_)), max(1, int(230 * s_)))); blit(c.fr, L2, cx - L2.width / 2, cy - L2.height / 2, c.alpha(cl(p * 2)))
    def s2(c):
        y = kick(c, "사주 일간으로 보면 모임 속 역할", 470)
        for i, (col, han, el, role) in enumerate(ELC[:2]):
            yy = y + 40 + i * 250; box(c, 70, yy, 900, yy + 210, .3 + i * .5, outline=col); ctext(c, el, 180, yy + 105, 80, col, .4 + i * .5, maxw=160); ctext(c, role, 590, yy + 105, 60, WHITE, .5 + i * .5, maxw=560)
    def s3(c):
        y = title(c, "가족이 싫은 게\n아니에요", 480, .05, 100); body(c, "오래 맡아 온 역할이\n힘을 쓰게 해요", y + 50, .7, 58, DIM)
    def s4(c):
        y = kick(c, "이번 모임에서는", 500); title(c, "내려놓을 역할\n하나만 정하기", y + 20, .3, 100)
    return [(3.2, s1), (3.4, s2), (3.0, s3), (2.8, s4), (2.6, end_scene("가족 모임에서 나는\n어떤 역할인가요?"))]

def n41():
    def gauge(c, val):
        d = ImageDraw.Draw(c.fr, "RGBA"); y = 980 + M.DY; x0, x1 = 120, 820
        d.rounded_rectangle((x0, y - 18, x1, y + 18), radius=18, fill=(214, 218, 228, 70))
        p = e_out((c.t - .6) / 1.2); xv = x0 + (x1 - x0) * val / 10 * p; d.rounded_rectangle((x0, y - 18, xv, y + 18), radius=18, fill=TEAL)
        d.ellipse((xv - 34, y - 34, xv + 34, y + 34), fill=WHITE)
        for v, s in ((0, "0"), (10, "10")):
            L = line_layers(s, 52, DIM, BLACK, 200, 1.2)[0][0]; blit(c.fr, L, x0 + (x1 - x0) * v / 10 - L.width / 2, 1040 - 22, c.alpha(1))
    def s1(c):
        y = kick(c, "낯선 자리에서", 470); title(c, "내 긴장, 남에게\n몇 점쯤 보일까요?", y + 10, .2, 92); gauge(c, 7)
    def s2(c):
        y = title(c, "말이 주는 건\n소심해서가 아니에요", 480, .05, 92); body(c, "먼저 살피고\n나중에 말하는 거예요", y + 50, .7, 58, DIM)
    def s3(c):
        y = kick(c, "사주·별자리·숫자로 보면", 500); box(c, 70, y + 30, 900, y + 300, .3); ctext(c, "산(戊)과 보석(辛),\n처녀·염소자리, 숫자 7", CX, y + 165, 56, WHITE, .5, maxw=780)
    def s4(c):
        y = kick(c, "첫 만남 전에", 470); box(c, 70, y + 40, 900, y + 400, .3, outline=TEAL)
        ctext(c, "물어볼 질문 하나", CX, y + 150, 58, WHITE, .5, maxw=780); ctext(c, "'천천히 말하는 편이에요'", CX, y + 290, 54, TEAL, .9, maxw=780)
    return [(3.4, s1), (3.0, s2), (3.2, s3), (3.4, s4), (2.6, end_scene("편한 사람 앞에서는\n무엇이 다른가요?"))]

def n42():
    def s1(c):
        y = title(c, "예민해서 쉽게\n지친다면", 470, .05, 100)
        for i, (s, hi) in enumerate((("10:00 회의", False), ("10:50 조용한 10분", True))):   # 시각과 일은 한 덩어리(R64)
            yy = y + 50 + i * 190; box(c, 70, yy, 900, yy + 160, .5 + i * .4, fill=GOLD if hi else PANEL); ctext(c, s, CX, yy + 80, 58, INK if hi else WHITE, .6 + i * .4, maxw=780)
    def s2(c):
        y = kick(c, "별자리로 보면", 470)
        bar_row(c, y + 40, "*처녀자리*는 작은 것까지", GOLD, .3, 56); bar_row(c, y + 270, "*물고기자리*는 남의 기분까지", TEAL, .8, 54)
    def s3(c):
        y = kick(c, "자미두수로는", 520); y = title(c, "마음의 여유를\n복덕궁으로 봐요", y + 10, .2, 96)
    def s4(c):
        y = kick(c, "이번 주에 해 볼 것", 500); title(c, "신경 쓰인 것을\n한 단어씩 모으기", y + 20, .3, 96)
    return [(3.6, s1), (3.4, s2), (2.8, s3), (2.8, s4), (2.6, end_scene("하루 중 언제\n가장 예민해지나요?"))]

def n43():
    def receipt(c, k, y0):
        x0, x1 = 140, 800; h = 140 + 120 * 2 + 40; p = e_out((c.t - .3) / .5)
        L = Image.new("RGBA", (x1 - x0, h + 24), (0, 0, 0, 0)); d = ImageDraw.Draw(L); d.rectangle((0, 0, x1 - x0, h), fill=(251, 250, 246, 255))
        for i in range(0, x1 - x0, 30): d.polygon([(i, h), (i + 15, h + 20), (i + 30, h)], fill=(251, 250, 246, 255))
        d.text((40, 52), "내 후회 영수증", font=font(BLACK, 46), fill=(29, 43, 44, 255), anchor="lm"); d.line((30, 100, x1 - x0 - 30, 100), fill=(160, 170, 170, 255), width=2)
        blit(c.fr, L, x0, y0 + (1 - p) * 60, c.alpha(cl(p * 1.6)))
        for i, (a, b) in enumerate((("설렐 때 결제", "불"), ("참다가 한 번에", "흙"))[:k]):
            yy = y0 + 150 + i * 120; q = e_out((c.t - .8 - i * .4) / .35)
            La = line_layers(a, 54, (29, 43, 44, 255), BLACK, 420, 1.2)[0][0]; blit(c.fr, La, x0 + 40 - 30, yy - 22, c.alpha(cl(q * 2)))
            Lb = line_layers(b, 58, (224, 83, 60, 255), BLACK, 120, 1.2)[0][0]; blit(c.fr, Lb, x1 - 40 - Lb.width + 30, yy - 22, c.alpha(cl(q * 2)))
    def s1(c):
        y = title(c, "결제하고 나서\n후회한 적 있나요?", 470, .05, 96); receipt(c, 2, int(y + 60))   # 영수증이 제목에 붙지 않게 제목 끝에서 60 띄운다
    def s2(c):
        y = kick(c, "행동경제학에서는", 520); y = title(c, "'심리적 회계'라고\n불러요", y + 10, .2, 96); body(c, "리처드 탈러, 1985", y + 40, .8, 48, DIM)
    def s3(c):
        y = title(c, "같은 돈도\n다르게 써요", 480, .05, 100); body(c, "보너스는 쉽게,\n월급은 아끼는 식이에요", y + 50, .7, 58, DIM)
    def s4(c):
        y = kick(c, "결제 전에 하나만", 500); box(c, 70, y + 40, 900, y + 300, .3, outline=CORAL); ctext(c, "장바구니에 담고\n하루 뒤에 다시 보기", CX, y + 170, 60, WHITE, .5, maxw=780)
    return [(3.6, s1), (3.0, s2), (2.8, s3), (3.0, s4), (2.6, end_scene("후회한 결제,\n그때 기분은 어땠나요?"))]

def n44():
    JAR = [(196, 61, 47, 255), (224, 138, 30, 255), (122, 46, 143, 255), (214, 176, 42, 255), (63, 122, 58, 255), (184, 50, 90, 255)]
    def jars(c, n, y, sz, gap, cols, t0):
        for j in range(n):
            x = 470 - (cols * (sz + gap) - gap) / 2 + (j % cols) * (sz + gap); yy = y + (j // cols) * (sz + 20); p = e_back((c.t - t0 - j * .03) / .3)
            if p <= .02: continue
            L = Image.new("RGBA", (sz, sz), (0, 0, 0, 0)); d = ImageDraw.Draw(L); d.rounded_rectangle((0, sz * .2, sz - 1, sz - 1), radius=int(sz * .2), fill=JAR[j % 6]); d.rectangle((sz * .15, 0, sz * .85, sz * .2), fill=(214, 218, 228, 255))
            blit(c.fr, L, x, yy + (1 - min(p, 1)) * 40, c.alpha(cl(p * 2)))
    def s1(c):
        y = kick(c, "잼 시식대 실험", 470); y = title(c, "24가지와 6가지,\n어디서 더 샀을까요?", y + 10, .2, 88)
        jars(c, 24, y + 50, 52, 14, 12, .8); jars(c, 6, y + 220, 96, 34, 6, 1.6)
    def s2(c):
        y = title(c, "6가지일 때\n훨씬 많이 샀어요", 480, .05, 96); body(c, "아이엔가·레퍼, 2000", y + 40, .7, 48, DIM)
    def s3(c):
        y = kick(c, "질문을 또렷하게", 470); box(c, 70, y + 40, 900, y + 220, .3); ctext(c, "이직할까 말까", CX, y + 130, 58, DIM, .4, maxw=780)
        p = e_out((c.t - .9) / .3); d = ImageDraw.Draw(c.fr, "RGBA"); w = font(BLACK, 58).getlength("이직할까 말까")
        if p > .02: d.line((CX - w / 2 - 10, y + 130 + M.DY, CX - w / 2 - 10 + (w + 20) * p, y + 130 + M.DY), fill=(214, 98, 82, 255), width=8)
        box(c, 70, y + 280, 900, y + 520, 1.2, outline=GOLD, ow=5); ctext(c, "올해 안에 옮기면\n어떻게 될까요?", CX, y + 400, 58, WHITE, 1.3, maxw=780)
    def s4(c):
        y = kick(c, "이번 주에 해 볼 것", 500); title(c, "결정 기준 3개를\n순서대로 적기", y + 20, .3, 96)
    return [(3.8, s1), (2.8, s2), (3.8, s3), (2.8, s4), (2.6, end_scene("미루고 있는 결정,\n선택지는 몇 개인가요?"))]

def n45():
    def bats(c, t0):
        for i, (el, lv, col) in enumerate((("불", .08, CORAL), ("물", .3, TEAL), ("흙", .45, GOLD))):
            cx = 200 + i * 270; y = 760; p = e_out((c.t - t0 - i * .3) / .6); lvl = 1 - (1 - lv) * p
            L = Image.new("RGBA", (190, 380), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
            d.rounded_rectangle((60, 0, 130, 26), radius=8, fill=(214, 218, 228, 255)); d.rounded_rectangle((8, 22, 182, 372), radius=28, outline=WHITE, width=8)
            fh = int(320 * lvl); d.rounded_rectangle((24, 356 - fh, 166, 356), radius=16, fill=col if lvl > .2 else (220, 90, 80, 255))
            blit(c.fr, L, cx - 95, y, c.alpha(cl((c.t - t0 - i * .3) / .3)))
            Lt = line_layers(el, 64, col, BLACK, 200, 1.2)[0][0]; blit(c.fr, Lt, cx - Lt.width / 2, y + 400 - 22, c.alpha(cl((c.t - t0 - i * .3) / .3)))
    def s1(c):
        title(c, "현관문만 닫으면\n의욕이 꺼지나요?", 480, .05, 96); bats(c, .6)
    def s2(c):
        y = kick(c, "사주·별자리 원소로 보면", 470)
        for i, (el, s, col) in enumerate((("불", "확 꺼져요", CORAL), ("물", "마음이 닳아요", TEAL))):
            yy = y + 40 + i * 250; box(c, 70, yy, 900, yy + 210, .3 + i * .5, outline=col); ctext(c, el, 180, yy + 105, 80, col, .4 + i * .5, maxw=160); ctext(c, s, 590, yy + 105, 60, WHITE, .5 + i * .5, maxw=560)
    def s3(c):
        y = kick(c, "흙은", 520); y = title(c, "몸이 먼저\n무거워져요", y + 10, .2, 100); body(c, "식사와 잠이 먼저예요", y + 40, .7, 56, DIM)
    def s4(c):
        y = kick(c, "오늘부터", 500); title(c, "퇴근 뒤 30분은\n아무것도 안 하기", y + 20, .3, 92)
    return [(3.4, s1), (3.4, s2), (3.0, s3), (2.8, s4), (2.6, end_scene("오늘 가장 지친 일은\n무엇이었나요?"))]

def n46():
    def mask(c, cx, cy, t0, mood, col):
        p = e_back((c.t - t0) / .4)
        if p <= .02: return
        L = Image.new("RGBA", (240, 290), (0, 0, 0, 0)); d = ImageDraw.Draw(L); d.ellipse((5, 5, 235, 285), fill=col)
        for ex in (60, 140): d.ellipse((ex, 100, ex + 42, 136), fill=(29, 16, 48, 255))
        if mood == 0: d.arc((70, 150, 170, 230), 20, 160, fill=(29, 16, 48, 255), width=10)
        elif mood == 1: d.line((80, 200, 160, 200), fill=(29, 16, 48, 255), width=10)
        else: d.arc((70, 180, 170, 250), 200, 340, fill=(29, 16, 48, 255), width=10)
        s_ = min(p, 1.05); L2 = L.resize((max(1, int(240 * s_)), max(1, int(290 * s_)))); blit(c.fr, L2, cx - L2.width / 2, cy - L2.height / 2, c.alpha(cl(p * 2)))
    def s1(c):
        y = kick(c, "오늘은 핼러윈", 470); title(c, "평소에도 쓰는\n가면이 있나요?", y + 10, .2, 100)
        for i, col in enumerate(((244, 233, 255, 255), (255, 214, 170, 255), (210, 220, 240, 255))): mask(c, 200 + i * 270, 1000, .7 + i * .3, i, col)
    def s2(c):
        y = kick(c, "이런 가면, 있지 않나요?", 470)
        for i, (a, col) in enumerate((("분위기를 맞추는 가면", GOLD), ("속을 숨기는 가면", CORAL))):
            yy = y + 40 + i * 250; box(c, 70, yy, 900, yy + 210, .3 + i * .5, outline=col); ctext(c, a, CX, yy + 105, 58, WHITE, .4 + i * .5, maxw=780)
    def s3(c):
        y = kick(c, "자미두수·별자리로 보면", 520); y = title(c, "겉과 속의 거리가\n클수록 지쳐요", y + 10, .2, 96); body(c, "명궁과 신궁, 쌍둥이·전갈자리", y + 40, .8, 48, DIM)
    def s4(c):
        y = kick(c, "이번 주에 해 볼 것", 500); title(c, "가면을 벗어도 되는\n한 사람 떠올리기", y + 20, .3, 92)
    return [(3.4, s1), (3.0, s2), (3.2, s3), (2.8, s4), (2.6, end_scene("속마음을 숨기는 건\n어떤 자리인가요?"))]

# ───────── 릴스 본문을 쓰는 두 편: 첫 장면·끝 장면만 클립용으로 새로(K-008) ─────────
def n49_intro():
    def s1(c):
        y = kick(c, "2027 돼지띠", 470); y = title(c, "힘을 쓸 달은\n언제일까요?", y + 10, .2, 100)
        for i, (m, col) in enumerate((("2월", GOLD), ("3월", GOLD), ("7월", GOLD))):
            cx = 200 + i * 270; p = e_back((c.t - .7 - i * .3) / .4)
            if p <= .02: continue
            L = Image.new("RGBA", (220, 220), (0, 0, 0, 0)); d = ImageDraw.Draw(L); d.ellipse((5, 5, 215, 215), outline=col, width=8, fill=(26, 33, 54, 235)); d.text((110, 112), m, font=font(GM, 76), fill=col, anchor="mm")
            s_ = min(p, 1.05); L2 = L.resize((max(1, int(220 * s_)), max(1, int(220 * s_)))); blit(c.fr, L2, cx - L2.width / 2, y + 60 + 110 - L2.height / 2, c.alpha(cl(p * 2)))
    return [(3.2, s1)], [(2.6, end_scene("도움을 줄 사람,\n누가 먼저 떠오르나요?"))]
def n51_intro():
    def s1(c):
        y = title(c, "3,000명 중 사주와\n가장 자주 같았던 별자리", 480, .05, 84)
        for i, (lab, v, col) in enumerate((("염소자리", 23.0, GOLD), ("천칭자리", 5.6, CORAL))):
            yy = y + 60 + i * 200; p = e_out((c.t - .7 - i * .4) / .8)
            L = line_layers(f"{lab} {v}%", 56, col, BLACK, 820, 1.2)[0][0]; blit(c.fr, L, 70 - 30, yy - 22, c.alpha(cl(p * 2)))   # 이름과 값은 한 덩어리(R64)
            d = ImageDraw.Draw(c.fr, "RGBA"); w = int(830 * v / 23.0 * p); d.rounded_rectangle((70, yy + M.DY + 90, 70 + max(4, w), yy + M.DY + 150), radius=20, fill=col)
    return [(3.6, s1)], [(2.6, end_scene("내 별자리와 사주,\n같은 말을 하나요?"))]

CLIPS = {   # id: (올리는 날, 블로그 글, 장면 함수)
 "v3-1016-n33": ("2026-10-16", "n33", n33), "v3-1017-n49": ("2026-10-17", "n49", None), "v3-1018-n34": ("2026-10-18", "n34", n34),
 "v3-1019-n35": ("2026-10-19", "n35", n35), "v3-1020-n51": ("2026-10-20", "n51", None), "v3-1021-n36": ("2026-10-21", "n36", n36),
 "v3-1022-n37": ("2026-10-22", "n37", n37), "v3-1023-n38": ("2026-10-23", "n38", n38), "v3-1024-n39": ("2026-10-24", "n39", n39),
 "v3-1025-n40": ("2026-10-25", "n40", n40), "v3-1026-n41": ("2026-10-26", "n41", n41), "v3-1027-n42": ("2026-10-27", "n42", n42),
 "v3-1028-n43": ("2026-10-28", "n43", n43), "v3-1029-n44": ("2026-10-29", "n44", n44), "v3-1030-n45": ("2026-10-30", "n45", n45),
 "v3-1031-n46": ("2026-10-31", "n46", n46)}
REEL = {"v3-1017-n49": ("rc-1025-pig", n49_intro), "v3-1020-n51": ("rc-1020-star", n51_intro)}
TX = ["zoom", "slide_l", "drop", "mask", "pop", "slide_r", "flip", "alt"]; TR = ["sweep", "iris", "drip", "zoom", "flash"]
def fx_for(k, n):
    """R36: 장면마다 다른 효과, 클립마다 시작점을 옮긴다. 첫 장면은 강한 효과(zoom·drop·pop)."""
    starts = [0, 2, 4]; s0 = starts[k % 3] + (k // 3) % 2 * 3
    fx = [(TX[(s0 + i) % 8], TR[(k + 2 * i) % 5]) for i in range(n)]
    if fx[0][0] not in ("zoom", "drop", "pop"): fx[0] = (["zoom", "drop", "pop"][k % 3], fx[0][1])
    return fx
def scenes_of(cid):
    day, blog, fn = CLIPS[cid]
    if fn: return fn()
    a, b = REEL[cid][1](); return a + b
def setup(cid):
    k = list(CLIPS).index(cid); M.BG_VARIANT = BGS[k % len(BGS)]; M.FX = fx_for(k, len(scenes_of(cid)) + 1)
def check(cid):
    """엄격 자막 규칙(R60·R61·R63·R64·R62·R66·R67)과 배치(R21: 맨 위 470·맨 아래 1350·가운데 910±15)."""
    import sub_harvest as H, sub_rules as SR, layout_audit as LA
    setup(cid); sc = scenes_of(cid); bad = [f"{r} 장면{no} {m}" for r, no, m in SR.check("clips3/" + cid, H.harvest(sc), "엄격")]
    for r in LA.audit(cid, [(d, M._auto(f, d)) for d, f in sc]):
        if r[5]: bad.append(f"배치 장면{r[1]} " + " / ".join(r[5]))
    import numpy as np   # 가로 안전 영역(§1 x 50~900): 내용 있음/없음 두 번 그려 차이로 잰다
    for i in range(len(sc)):
        M.BRAND = False; t = sc[i][0] * .86; M.still(sc, i, t, "/tmp/_v3a.png"); sc2 = list(sc); sc2[i] = (sc[i][0], lambda c: None); M.still(sc2, i, t, "/tmp/_v3b.png"); M.BRAND = True
        a = np.asarray(Image.open("/tmp/_v3a.png").convert("RGB")).astype(int); b = np.asarray(Image.open("/tmp/_v3b.png").convert("RGB")).astype(int)
        xs = np.where((np.abs(a - b).sum(axis=2) > 40).sum(axis=0) > 2)[0]
        if len(xs) and (xs.min() < 50 or xs.max() > 900): bad.append(f"가로 안전 영역 장면{i + 1}: x {xs.min()}~{xs.max()} (50~900)")
    return bad
def render(cid):
    setup(cid); os.makedirs(OUT, exist_ok=True); sc = scenes_of(cid)
    if cid not in REEL:
        out, dur = M.render(cid, sc, OUT)
    else:
        a, b = REEL[cid][1](); k = list(CLIPS).index(cid); tmp = tempfile.mkdtemp()
        M.FX = fx_for(k, 2); ia, _ = M.render("intro", a, tmp); M.FX = fx_for(k + 1, 2); ib, _ = M.render("outro", b, tmp)
        import clip_from_reel as CF
        sp = json.load(open(os.path.join(ROOT, "content", "clips_from_reels.json"), encoding="utf-8")); src = next(x for x in sp["clips"] if x["id"] == REEL[cid][0])
        body_mp4 = os.path.join(tmp, "b.mp4"); CF.body_seg(src, sp, body_mp4, tmp)   # 릴스 본문(끝의 팔로우·프로필 장면은 자르고 인스타 전용 글은 masks로 가림), 크기 그대로(릴스도 같은 안전 영역)
        out = os.path.join(OUT, cid + ".mp4")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", ia, "-i", body_mp4, "-i", ib, "-filter_complex", "[0:v]fps=30,setsar=1[a];[1:v]fps=30,scale=1080:1920,setsar=1[b];[2:v]fps=30,setsar=1[c];[a][b][c]concat=n=3:v=1:a=0,format=yuv420p[v]",
                        "-map", "[v]", "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-an", "-movflags", "+faststart", out], check=True)
        dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", out])); shutil.rmtree(tmp)
    # 썸네일 = 첫 장면 완성 화면(영상 속 실제 화면) · 확인용 = 장면마다 끝 무렵 한 장
    setup(cid); tmpd = tempfile.mkdtemp(); shots = []
    for i, (d, f) in enumerate(sc):
        p = os.path.join(tmpd, f"{i}.png"); M.still(sc, i, d * .86, p); shots.append(p)
    Image.open(shots[0]).convert("RGB").save(os.path.join(OUT, cid + "_thumb.jpg"), quality=90)
    sh = Image.new("RGB", (270 * len(shots), 480))
    for i, p in enumerate(shots):
        im = Image.open(p).convert("RGB").resize((270, 480)); ImageDraw.Draw(im).rectangle((50 / 4, 330 / 4, 900 / 4, 1470 / 4), outline=(255, 60, 60)); sh.paste(im, (270 * i, 0))
    sh.save(os.path.join(OUT, cid + "_check.jpg"), quality=88); shutil.rmtree(tmpd)
    return out, dur
if __name__ == "__main__":
    ids = [a for a in sys.argv[1:] if not a.startswith("--")] or list(CLIPS)
    tot = 0
    for cid in ids:
        b = check(cid); tot += len(b); print(cid, "검사", "통과" if not b else f"걸림 {len(b)}"); [print("   ", x) for x in b]
        if "--check" not in sys.argv and not b: o, d = render(cid); print("   ", o, f"{d:.1f}초")
    sys.exit(1 if tot else 0)
