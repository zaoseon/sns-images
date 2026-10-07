"""글 연결 클립 13편 새 구성(n34~n46, 10/7 대표 '제안대로'). 문장은 기존 클립(=블로그 본문 내용)과 같다. 바뀐 것: 그림 형태 · 글 효과 · 마무리 · 정월 얼굴(정리 장면 1곳만) · 배치 자동 맞춤(R21).
12초판 = 훅 2.2 / 핵심 2.6+2.6 / 정리 2.4 / 마무리 2.2 (체크 목록형은 2.0 / 7.2 / 2.8). 사용: python3 content/clips_v2.py <클립 id>  -> clips_v2/<id>_12s.mp4"""
import sys, os, math, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "..")); sys.path.insert(0, os.path.join(ROOT, "pipeline")); sys.path.insert(0, HERE)
from pilot_variety import *
import music_plan as MP
EFF = ["slide", "wipe", "zoom", "slide-"]
def E(i): return EFF[i % 4]
def eff2(name, c, s, y, t0, size, color=WHITE, **kw):
    base = name.rstrip("-"); f = {"wipe": fx_wipe, "slide": fx_slide, "zoom": fx_zoom}[base]
    if base == "slide": kw["dirn"] = -1 if name.endswith("-") else 1
    return f(c, s, y, t0, size, color, **kw)
def head(c, kicker, title, e, y=490, size=96, t0=.05):
    """작은 머리말 + 큰 제목(별표*로 강조). 아래 y를 돌려준다."""
    fx_slide(c, kicker, y, t0, 50, DIM, dirn=-1); return eff2(e, c, title, y + 74, t0 + .15, size, WHITE, maxw=840, lh=1.28)
def A(fn, dur, char=False): return (dur, fn if char else autofit(fn, dur))
# ---------- 훅 ----------
def motif(c, kind, y0, h):
    im, d = lay(900); a = int(255 * e_out(cl((c.t - .05) / .5)) * .35)
    if kind == "ring": d.ellipse((CX - 330, 900 - 330 - 480, CX + 330, 900 + 330 - 480), outline=GOLD[:3] + (a,), width=6)
    elif kind == "bars": d.rounded_rectangle((CX - 260, y0 - 70 - 480, CX + 260, y0 - 58 - 480), radius=6, fill=GOLD[:3] + (a * 2,)); d.rounded_rectangle((CX - 260, y0 + h + 40 - 480, CX + 260, y0 + h + 52 - 480), radius=6, fill=GOLD[:3] + (a * 2,))
    elif kind == "dots":
        for k in range(5): r = 12 + 6 * (k % 2); x = CX - 120 + k * 60; d.ellipse((x - r, y0 + h + 60 - 480 - r, x + r, y0 + h + 60 - 480 + r), fill=GOLD[:3] + (a * 2,))
    elif kind == "brackets":
        x0, x1, ya, yb = CX - 400, CX + 400, y0 - 50 - 480, y0 + h + 40 - 480
        for (x, y, sx, sy) in ((x0, ya, 1, 1), (x1, ya, -1, 1), (x0, yb, 1, -1), (x1, yb, -1, -1)): d.line([(x, y + sy * 70), (x, y), (x + sx * 70, y)], fill=GOLD[:3] + (a * 2,), width=8)
    blit(c.fr, im, 0, 480, 1.0)
def hook(kicker, title, i, mk):
    def f(c):
        h = 74 + text_h(title, 98, 840, 1.28); y0 = MID - h / 2; motif(c, mk, y0, h); head(c, kicker, title, E(i), y=int(y0), size=98)
    return f
# ---------- 핵심 장면 ----------
def s_neq(kicker, a, b, note, i):
    def f(c):
        fx_slide(c, kicker, 490, .05, 50, DIM, dirn=-1); im, d = lay(700); fa = font(BLACK, 62); PW_, PH_ = 340, 250; y = 640 - 480
        for k, (txt, col, x0, sgn) in enumerate(((a, CORAL, 60, -1), (b, GOLD, 540, 1))):
            g = e_out(cl((c.t - .2 - k * .15) / .5)); xo = x0 + (1 - g) * sgn * 260; al = int(255 * cl(g * 1.5))
            d.rounded_rectangle((xo, y, xo + PW_, y + PH_), radius=40, fill=col[:3] + (al,))
            ls, st = line_layers(txt, 62, (24, 20, 36, 255), BLACK, 290, 1.2); tot = len(ls) * st; yy = y + (PH_ - tot) / 2 + 6
        blit(c.fr, im, 0, 480, 1.0)
        # 패널 안 글은 층으로 올려 투명도를 맞춘다
        for k, (txt, x0, sgn) in enumerate(((a, 60, -1), (b, 540, 1))):
            g = e_out(cl((c.t - .2 - k * .15) / .5)); xo = x0 + (1 - g) * sgn * 260; ls, st = line_layers(txt, 62, (24, 20, 36, 255), BLACK, 290, 1.2); tot = len(ls) * st; yy = 640 + (PH_ - tot) / 2 + 6
            for L in ls: blit(c.fr, L, xo + PW_ / 2 - L.width / 2, yy - 20, c.alpha(cl(g * 1.5))); yy += st
        q = e_back(cl((c.t - .9) / .4))
        if q > .03: L = line_layers("≠", max(8, int(150 * min(q, 1.1))), GOLD, BLACK, 200, 1.0)[0][0]; blit(c.fr, L, CX - L.width / 2, 640 + PH_ / 2 - L.height / 2 - 6, c.alpha(cl(q * 2)))   # 시작 순간 크기 0 방지
        eff2(E(i + 1), c, note, 940, 1.5, 52, DIM, maxw=840, lh=1.4)
    return f
def s_chips(kicker, title, chips, i, cols=None):
    def f(c):
        y = head(c, kicker, title, E(i), size=96); im, d = lay(900); fnt = font(BLACK, 58)
        for k, ch in enumerate(chips):
            g = e_back(cl((c.t - .9 - k * .4) / .4)); w = int(fnt.getlength(ch)) + 90; yy = y + 60 + k * 128 - 480 - 0; al = int(255 * cl(g))
            if g <= 0: continue
            col = (cols or [GOLD, CORAL, TEAL])[k % 3]; sc = min(g, 1.0); ww = int(w * sc)
            d.rounded_rectangle((CX - ww / 2, yy, CX + ww / 2, yy + 100), radius=50, fill=(26, 33, 54, int(235 * cl(g))), outline=col[:3] + (al,), width=5); d.text((CX, yy + 51), ch, font=fnt, fill=(255, 255, 255, al), anchor="mm")
        blit(c.fr, im, 0, 480, 1.0)
    return f
def s_check(kicker, title, item, i):
    def f(c): y = head(c, kicker, title, E(i), size=96); check_row(c, int(y + 50), item, .9, 60)
    return f
def s_battery(kicker, title, label, i):
    def f(c): y = head(c, kicker, title, E(i), size=96); battery(c, CX, int(y + 230), .7, frm=.8, to=.2, dur=1.6, label=label)
    return f
def s_text(kicker, title, i, size=100):
    def f(c): head(c, kicker, title, E(i), size=size)
    return f
def s_list3(title, items, i):
    def f(c):
        fx_slide(c, title, 490, .05, 54, DIM, dirn=-1)
        for k, it in enumerate(items): check_row(c, 580 + k * 190, it, .5 + k * 2.1, 60)
    return f
# ---------- 정리(정월은 여기 한 곳) ----------
def s_close(lines, face, i, size=90):
    """정리 장면: 글 아래 빈 높이에 맞춰 정월 크기를 정한다(글을 가리지 않게). 겹치면 렌더 전에 오류."""
    ty = 550; bottom = ty + text_h(lines, size, 840, 1.28); ratio = char_layer(face, 400).height / 400.0; avail = 1440 - (bottom + 36); width = int(min(520, avail / ratio))
    assert width >= 330, f"정월이 들어갈 자리가 모자라요({face}, 글 끝 {bottom}, 폭 {width})"
    def f(c):
        fx_slide(c, "정리하면", 490, .05, 50, DIM, dirn=-1); eff2(E(i + 2), c, lines, ty, .2, size, WHITE, maxw=840, lh=1.28); character(c, face, t0=.3, width=width)
    return f
# ---------- 마무리 3종 ----------
PILL = "블로그 스티커 눌러 보기"
def cta_pill(c, y, t0=.7):
    fnt = font(BLACK, 58); w = int(fnt.getlength(PILL)) + 90; pl = Image.new("RGBA", (w + 20, 140), (0, 0, 0, 0)); d = ImageDraw.Draw(pl); d.rounded_rectangle((10, 10, 10 + w, 130), radius=60, fill=GOLD); d.text((10 + w / 2, 71), PILL, font=fnt, fill=INK, anchor="mm")
    p = e_back((c.t - t0) / .45); pulse = 1 + .035 * math.sin(c.t * 6); L = pl.resize((int(pl.width * pulse), int(pl.height * pulse))); blit(c.fr, L, CX - L.width / 2, y + (1 - e_out(p)) * 50, c.alpha(cl(p * 2)))
def s_cta(text_, form, i):
    def f(c):
        if form == "C":
            H = text_h(text_, 88, 780, 1.3); top = 520; im, d = lay(900); g = e_out(cl((c.t - .1) / .5)); d.rounded_rectangle((70, top - 480, 870, top - 480 + H + 300), radius=50, outline=GOLD[:3] + (int(255 * g),), width=5, fill=(26, 33, 54, int(205 * g)))
            blit(c.fr, im, 0, 480, 1.0); y = eff2(E(i), c, text_, top + 50, .15, 88, WHITE, maxw=780, lh=1.3); cta_pill(c, y + 40)
            return
        y = eff2(E(i), c, text_, 560, .15, 88, WHITE, maxw=840, lh=1.3)
        if form == "A": cta_pill(c, y + 50)
        else:
            im, d = lay(300); bob = 14 * math.sin(c.t * 7); g = e_back(cl((c.t - .5) / .4)); a = int(255 * cl(g)); cy = 90 + bob
            d.polygon([(CX - 70, cy - 30), (CX + 70, cy - 30), (CX, cy + 60)], fill=GOLD[:3] + (a,)); blit(c.fr, im, 0, y + 20, 1.0); cta_pill(c, y + 190, .9)
    return f

CT = lambda name: f"자세한 기준은\n블로그 {name} 글에서"
def spec():
    L = {}
    def add(cid, kind, scenes, kinds_note): L[cid] = (kind, scenes, kinds_note)
    # n34 일요일 밤 (질문형)
    add("n34-c1", "질문형", [A(hook("일요일 밤 · 질문", "일요일 밤마다\n*생각이 많아지나요?*", 0, "ring"), 2.2), A(s_chips("쉬는 밤엔", "*안쪽 생각*이\n더 크게 들려요", ["월요일 일정", "지난 한 주의 말"], 1), 2.6), A(s_check("잠들기 전에", "내일 할 일\n*한 가지만* 적어요", "내일 할 일 한 가지", 2), 2.6), A(s_close("생각이 많은 건\n*정리가 필요*하다는\n신호예요", "v1_lowbun", 3), 2.4, True), A(s_cta(CT("일요일 밤"), "A", 0), 2.2)], "알약 목록·체크·정월(정리)")
    # n35 월요일 (오해 교정형)
    add("n35-c1", "오해 교정형", [A(hook("월요일 · 오해", "월요일이 무거우면\n*게으른 걸까요?*", 1, "bars"), 2.2), A(s_neq("아니에요", "게으름", "모습의 차이", "타고난 바탕과 일터의 모습이\n달라서일 수 있어요", 1), 2.6), A(s_check("일요일 밤에", "월요일 *첫 일*\n한 가지만 정해요", "월요일 첫 일 한 가지", 2), 2.6), A(s_close("월요일이 무거운 건\n*맞는 방식을 찾는*\n신호일 수 있어요", "v11_mug", 3), 2.4, True), A(s_cta(CT("월요일"), "B", 1), 2.2)], "좌우 비교·체크·정월(정리)")
    # n36 끝을 못 내는 사람 (체크리스트형)
    add("n36-c1", "체크리스트형", [A(hook("끈기 · 체크", "힘이 빠지는\n*구간 세 가지*", 2, "dots"), 2.0), A(s_list3("나는 어디서 멈추나요", ["시작 직후 · 시작을 작게", "중반 · 점검일과 작은 보상", "마무리 · 마지막을 작게 나누기"], 2), 7.2), A(s_cta(CT("끈기"), "C", 2), 2.8)], "체크 목록 3(정월 없음)")
    # n37 비교하는 습관 (오해 교정형)
    add("n37-c1", "오해 교정형", [A(hook("비교 · 오해", "비교하면 작아지는 건\n*약점일까요?*", 3, "brackets"), 2.2), A(s_neq("아니에요", "약점", "눈이 밝다", "좋은 것을 알아보는\n눈이 밝다는 뜻이에요", 2), 2.6), A(s_check("그래서", "견주는 대상을\n*어제의 나*로 바꿔요", "어제의 나와 한 가지만", 3), 2.6), A(s_close("같은 눈이\n*성장의 힘*이 돼요", "v13_horn_glasses", 0), 2.4, True), A(s_cta(CT("비교"), "A", 3), 2.2)], "좌우 비교·체크·정월(정리)")
    # n38 상강 (질문형)
    add("n38-c1", "질문형", [A(hook("상강 · 질문", "찬 바람이 불면\n*마음이 허해지나요?*", 0, "ring"), 2.2), A(s_chips("10월 23일 상강은", "*가을이 끝나는*\n문턱이에요", ["개(戌)의 달", "전갈자리 시작"], 3), 2.6), A(s_text("그래서", "마음도 *정리하고*\n거두는 쪽으로 기울어요", 0, 92), 2.6), A(s_close("올해 거둔 것\n*세 가지*를\n적어 보세요", "v6_winter", 1), 2.4, True), A(s_cta(CT("상강 마음"), "B", 0), 2.2)], "알약 목록·글·정월(정리)")
    # n39 연락 기다림 (체크리스트형)
    add("n39-c1", "체크리스트형", [A(hook("기다림 · 체크", "연락을 기다릴 때\n*해 볼 세 가지*", 1, "bars"), 2.0), A(s_list3("이번 주에", ["기다릴 기한 하나 적기", "그 사이 내가 할 일 하나", "확인은 하루 두 번만"], 1), 7.2), A(s_cta(CT("기다림"), "A", 1), 2.8)], "체크 목록 3(정월 없음)")
    # n40 가족 모임 뒤 (질문형)
    add("n40-c1", "질문형", [A(hook("가족 모임 · 질문", "가족 모임 뒤\n*유독 지치나요?*", 2, "dots"), 2.2), A(s_battery("지치는 건", "가족이 싫어서가\n*아니에요*", "모임 뒤", 2), 2.6), A(s_text("그보다는", "*오래된 역할*을\n계속 하고 있어서예요", 3, 94), 2.6), A(s_close("모임 전에\n*쉬는 시간*을 먼저\n일정에 넣어요", "v7_hanbok", 2), 2.4, True), A(s_cta(CT("가족 모임"), "C", 2), 2.2)], "배터리·글·정월(정리)")
    # n41 낯선 사람 앞 (오해 교정형)
    add("n41-c1", "오해 교정형", [A(hook("첫인상 · 오해", "말이 줄어들면\n*소심한 걸까요?*", 3, "brackets"), 2.2), A(s_neq("아니에요", "말의 양", "사회성", "별개예요", 3), 2.6), A(s_text("말이 줄어드는 건", "*상대를 파악하는*\n시간이에요", 0, 100), 2.6), A(s_close("첫 만남엔\n*질문 하나*만\n준비해 가요", "v4_glasses", 3), 2.4, True), A(s_cta(CT("첫인상"), "B", 3), 2.2)], "좌우 비교·글·정월(정리)")
    # n42 예민 (오해 교정형)
    add("n42-c1", "오해 교정형", [A(hook("예민 · 오해", "예민하면\n*약한 걸까요?*", 0, "ring"), 2.2), A(s_neq("아니에요", "약함", "감각이 커요", "받아들이는 정보가\n많아서일 수 있어요", 0), 2.6), A(s_check("그래서", "자극 사이에\n*조용한 10분*을 넣어요", "조용한 10분 넣기", 1), 2.6), A(s_close("감각이 큰 만큼\n*쉬는 시간*도\n더 필요해요", "v2_straight", 0), 2.4, True), A(s_cta(CT("예민한 피로"), "A", 0), 2.2)], "좌우 비교·체크·정월(정리)")
    # n43 소비 후회 (질문형)
    add("n43-c1", "질문형", [A(hook("소비 · 질문", "결제하고 나서\n*후회한 적 있나요?*", 1, "bars"), 2.2), A(s_text("후회는", "쓴 돈보다\n*쓴 이유*에서 올 수 있어요", 1, 94), 2.6), A(s_chips("내 후회의 모양은", "*세 가지*예요", ["불 · 설렐 때", "물 · 기분이 흔들릴 때", "흙 · 참다가 한 번에"], 2), 2.6), A(s_close("결제 전에\n*하루만*\n기다려 보세요", "v3_ponytail", 1), 2.4, True), A(s_cta(CT("소비 습관"), "C", 1), 2.2)], "글·알약 목록 3·정월(정리)")
    # n44 결정 미루기 (체크리스트형)
    add("n44-c1", "체크리스트형", [A(hook("결정 · 체크", "결정을 못 할 때\n*해 볼 세 가지*", 2, "dots"), 2.0), A(s_list3("이번 주에", ["고민을 한 사건으로 적기", "정할 기한 하나 적기", "포기할 것 한 가지 정하기"], 2), 7.2), A(s_cta(CT("결정 미루기"), "B", 2), 2.8)], "체크 목록 3(정월 없음)")
    # n45 퇴근 방전 (오해 교정형)
    add("n45-c1", "오해 교정형", [A(hook("퇴근 후 · 오해", "아무것도 하기 싫으면\n*게으른 걸까요?*", 3, "brackets"), 2.2), A(s_neq("아니에요", "게으름", "방전", "에너지를 쓴 방식에 따라\n달라지는 피로예요", 3), 2.6), A(s_check("그래서", "퇴근 뒤 *30분*은\n아무것도 안 해요", "퇴근 뒤 30분 비우기", 0), 2.6), A(s_close("방전은\n*하루를 열심히 쓴*\n흔적일 수 있어요", "v13_horn_glasses", 3), 2.4, True), A(s_cta(CT("방전과 충전"), "A", 3), 2.2)], "좌우 비교·체크·정월(정리)")
    # n46 가면 (질문형)
    add("n46-c1", "질문형", [A(hook("가면 · 질문", "웃는 얼굴 뒤에\n*마음을 숨기나요?*", 0, "ring"), 2.2), A(s_text("가면은", "*거짓*이 아니라\n나를 지키는 방식일 수 있어요", 1, 92), 2.6), A(s_text("내 가면은", "*분위기*를 맞추거나\n*속*을 숨기거나\n*역할* 때문이에요", 2, 88), 2.6), A(s_close("속마음은\n*한 사람에게만*\n먼저 열어 보세요", "v8_gesture", 0), 2.4, True), A(s_cta(CT("가면"), "B", 0), 2.2)], "글·글·정월(정리)")
    return L
IDS = [f"n{n}-c1" for n in range(34, 47)]
def build(cid):
    kind, sc, note = spec()[cid]; out = os.path.join(ROOT, "clips_v2"); p, d = render(cid + "_12s", sc, out); mi = MP.choose("fun", "clip2-" + cid); MP.mux(p, [x for x, _ in sc], mi, 600 + int(cid[1:3]))
    print("완료", cid, round(d, 1), "초 · 음악", mi["style"], mi["bpm"])
if __name__ == "__main__":
    build(sys.argv[1])
