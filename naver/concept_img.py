"""네이버 본문 '심리 개념 도식' (10/15, AI 브리핑 기준 문서 이미지 방침 C · OSMU O6).
같은 틀(한눈에 보기·핵심 표·해 볼 것)이 54편에서 반복되는 문제를 줄이려고, '🧠 심리학으로 읽으면' 단락마다 그 개념 모양의 도식을 1장 넣는다.
반추=고리, 사회 비교=저울, 결정=선택지 칸, 소비=영수증, 애착=대화 화면(O6 표). 글 안에 있는 말만 쓴다(그림에만 있는 정보 금지).
이미지 안에 설명·안내 문구(예시·출처·실제 화면 등)는 넣지 않고 원고 본문 문장으로 쓴다(대표 10/15, 기준 대장 K-036). 넣을 때 쓸 본문 문장은 BODY_LINE.
imgkit 규칙(1280 납품·2배 원본·글자 42px 이상·로고 오른쪽 위)을 그대로 쓴다. 파일은 새 이름 naver_zNN_p.jpg 로만 추가(덮어쓰기 금지).
사용: python3 naver/concept_img.py n34   -> img/naver_z34_p.jpg (+ master/·m1280/)"""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "pipeline"))
import imgkit as K, naver2 as N2
from imgkit import Cv, L, RT, TITLE, BODY, DIM, WHITE
# 10/15 대표 "색감이 칙칙하다, 깔끔하고 세련되게": 오행 탁한 바탕·차트 무늬 대신 흰 바탕 + 남색 하나 + 금색 포인트, 연회색 칸
CLEAN = dict(bg=(250, 250, 248), ink=(22, 24, 32), sub=(110, 114, 124), acc=(27, 42, 82), gold=(196, 154, 64), cell=(241, 243, 248), line=(226, 229, 236), red=(214, 72, 56))
def clean_theme(): return CLEAN["bg"], CLEAN["acc"], CLEAN["ink"], CLEAN["line"]

def arrow(cv, x0, y0, x1, y1, col, w=6, head=22):
    cv.line(x0, y0, x1, y1, col, w); a = math.atan2(y1 - y0, x1 - x0)
    p = [(x1, y1), (x1 - head * math.cos(a - .45), y1 - head * math.sin(a - .45)), (x1 - head * math.cos(a + .45), y1 - head * math.sin(a + .45))]
    cv.d.polygon([(x * K.S, y * K.S) for x, y in p], fill=col)

def box_text(cv, cx, cy, lines, size, fg, path=BODY):
    step = size * 1.3; y = cy - step * (len(lines) - 1) / 2
    for l in lines: cv.text(cx, y, l, path, size, fg, "mm"); y += step

def loop(name, head, nodes, exit_label, exit_text, note, el="물"):
    """되풀이 고리: nodes 4개가 시계 방향으로 돌고, 아래 '끊는 법' 띠로 빠져나가는 빨간 화살표."""
    bg, acc, fg, line = clean_theme()
    H = 960 if not note else 1025; cv = Cv(H, bg); K.head_block(cv, head, acc, fg)
    cx, cy, r = (L + RT) / 2, 465, 225; bw, bh = 300, 118
    pos = [(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)]
    for i in range(4):
        a0 = -90 + i * 90 + 26; a1 = -90 + (i + 1) * 90 - 26; pts = []
        for k in range(13):
            t = math.radians(a0 + (a1 - a0) * k / 12); pts.append((cx + r * math.cos(t), cy + r * math.sin(t)))
        for p_, q in zip(pts, pts[1:]): cv.line(p_[0], p_[1], q[0], q[1], CLEAN["gold"], 5)
        arrow(cv, pts[-2][0], pts[-2][1], pts[-1][0], pts[-1][1], CLEAN["gold"])
    cv.text(cx, cy, "되풀이", TITLE, 46, CLEAN["gold"], "mm")
    for (x, y), t in zip(pos, nodes):
        cv.rr([x - bw / 2, y - bh / 2, x + bw / 2, y + bh / 2], 26, fill=CLEAN["cell"])
        box_text(cv, x, y, t, 42, fg)
    by0, by1 = 795, 915                                     # 끊는 법 띠
    cv.rr([L, by0, RT, by1], 32, fill=acc)
    lw = cv.tw(exit_label, TITLE, 50); cv.text(L + 40, (by0 + by1) / 2, exit_label, TITLE, 50, CLEAN["gold"], "lm")
    cv.text(L + 40 + lw + 36, (by0 + by1) / 2, exit_text, BODY, cv.fit(exit_text, BODY, 46, RT - L - lw - 110, 42), WHITE, "lm")
    arrow(cv, cx + r + bw / 2 - 30, cy + bh / 2 + 6, cx + r + bw / 2 - 30, by0 - 10, acc, 6, 26)
    if note: cv.text(L, H - 52, note, BODY, cv.fit(note, BODY, 42, RT - L, 36), DIM, "lm")
    cv.save(name)


def screen(name, head, shot, crop_h, notes, caption, el="흙"):
    """실제 화면 캡처 1장(AI 브리핑 기준 B·N5 '실제 화면'): 폰 화면 + 오른쪽에 화면 속 내용을 짚는 말. 가상 생년월일은 '예시'로 적는다."""
    from PIL import Image
    bg, acc, fg, line = clean_theme()
    im = Image.open(shot).convert("RGB"); im = im.crop((0, 0, im.width, min(crop_h, im.height)))
    pw = 430; ph = int(im.height * pw / im.width); H = ph + 230
    cv = Cv(H, bg); K.head_block(cv, head, acc, fg)
    x0, y0 = L + 10, 170
    cv.rr([x0 - 14, y0 - 14, x0 + pw + 14, y0 + ph + 14], 40, fill=(20, 20, 26))
    sm = im.resize((pw * K.S, ph * K.S)); cv.img.paste(sm, (x0 * K.S, y0 * K.S))
    tx = x0 + pw + 70; y = y0 + 20
    for lab, txt in notes:
        cv.text(tx, y, lab, BODY, 42, CLEAN["sub"], "la"); y += 58
        for l in cv.wrap(txt, BODY, 50, RT - tx): cv.text(tx, y, l, BODY, 50, fg, "la"); y += 66
        cv.line(tx, y + 18, RT, y + 18, CLEAN["line"], 2); y += 58
    if caption: cv.text(L, H - 52, caption, BODY, cv.fit(caption, BODY, 40, RT - L, 34), DIM, "lm")
    cv.save(name)

# 10/15 대표 "애플처럼 세련되게"(slide_design_master_guide: Apple Keynote 프리셋) — 단일 초점, 큰 글자, 테두리 없는 카드, 회색으로 계층, 강조색 하나(브랜드 금색)
FD = os.path.join(HERE, "..", "pipeline", "fonts") + "/"
PB, PS, PM = FD + "PRETENDARD-BOLD.OTF", FD + "PRETENDARD-SEMIBOLD.OTF", FD + "PRETENDARD-MEDIUM.OTF"
PX = FD + "PRETENDARD-EXTRABOLD.OTF"
# v3(10/15 대표 "검은 바탕 도식은 칸·원을 다른 색으로, 디자인 자료 참고"): 저장된 대표 기준 반영 — 검정+금색 금지(다른 운세 블로그 같음),
# 밝은 애플 판(#F5F5F7·흰 카드) + 디자인 기준(10/5) 강조색 4종(코랄·노랑·민트·하늘)을 칸마다 다르게, 진한 남색(#29335C, 대표 색 조합2) 띠, 회색 글자도 굵고 진하게
POP = [(255, 138, 115), (246, 176, 66), (127, 214, 200), (111, 183, 255)]          # 코랄·노랑·민트·하늘
def tint(c, k=.16): return tuple(int(255 - (255 - v) * k) for v in c)
def deep(c, k=.55): return tuple(int(v * k) for v in c)
NAVY = (41, 51, 92)
# v4(10/15 대표 "검정도 괜찮다, 칙칙해서 그런 것. 검정에 노랑·민트·핫핑크 강조가 예쁘다"): 어두운 판은 순검정 대신 #121214(다크 모드 권장),
# 칸은 한 단 밝은 면 + 칸마다 다른 쨍한 강조색(노랑·민트·핫핑크·하늘), 글자는 흰색, 강조색은 화면 일부에만(띠·화살표·이름표)
NEON = [(255, 216, 77), (62, 230, 193), (255, 61, 139), (77, 184, 255)]          # 노랑·민트·핫핑크·하늘 (v7부터 어두운 판에서는 쓰지 않음)
# v7(10/15 대표 "강조색 하나, 강조색 계열의 약간 누른 톤 하나, 나머지는 흰색", K-043): 색은 딱 셋 — 강조(노랑)·누른 노랑·흰색. 면·선은 무채색
ACC, ACC_MUTE = (255, 214, 64), (176, 150, 70)
def mix(a, b, k): return tuple(int(a[i] * (1 - k) + b[i] * k) for i in range(3))
KEY = {"dark": dict(bg=(18, 18, 20), card=(30, 30, 34), ink=(250, 250, 250), sub=(161, 161, 170), acc=(255, 216, 77), quiet=(58, 58, 62)),
       "light": dict(bg=(245, 245, 247), card=(255, 255, 255), ink=(29, 29, 31), sub=(81, 81, 86), acc=NAVY, quiet=(200, 200, 206))}
def k_head(cv, head, st):
    cv.text(L + 10, 118, head, PX, cv.fit(head, PX, 64, RT - L - 210, 50), st.get("head", st["ink"]), "ls")
    cv.text(RT - 10, 114, "子午線 자오선", K.SER, 28, st["sub"], "rs")

# v8(10/15 대표 "검은 바탕만 고집할 필요 없다. 대표 이미지 색조와 배경색을 맞추는 것도 방법. 글자는 가급적 흰색, 강조색 한두 개. 화살표가 얇아 옹졸해 보이지 않게", K-044)
AW, AH = 14, 46                      # 도식 화살표 굵기·머리 크기(이전 3/18 → 굵게, 10/15 대표 '얇아서 옹졸해 보인다')
KEY["dark"].update(line=(52, 52, 58), acc2=ACC_MUTE, frame=(0, 0, 0))
def cover_colors(path):
    """대표 이미지에서 바탕색(가장자리)과 강조색(채도 높은 색 중 가장 많은 것)을 뽑는다."""
    from PIL import Image
    import colorsys, collections
    im = Image.open(path).convert("RGB"); bg = im.getpixel((5, 5)); sm = im.resize((300, 180))
    px = [sm.getpixel((x, y)) for y in range(180) for x in range(300)]
    sat = [p for p in px if colorsys.rgb_to_hsv(*[v / 255 for v in p])[1] > .45 and sum(p) > 120] or px
    q = collections.Counter((p[0] // 8, p[1] // 8, p[2] // 8) for p in sat).most_common(1)[0][0]
    grp = [p for p in sat if (p[0] // 8, p[1] // 8, p[2] // 8) == q]
    return bg, tuple(sum(c[i] for c in grp) // len(grp) for i in range(3))
def cover_theme(path, kind="tone"):
    """tone: 대표 이미지의 강조색을 바탕으로(글자 흰색, 강조 = 밝은 노랑 한 가지 + 그 누른 톤).
    same: 대표 이미지 바탕색 그대로(밝은 바탕이라 글자는 진한 색, 강조 = 대표 이미지 강조색)."""
    bg, ac = cover_colors(path)
    if kind == "tone":
        b = mix(ac, (0, 0, 0), .18)
        return dict(bg=b, card=mix(b, (0, 0, 0), .16), line=mix(b, (255, 255, 255), .16), ink=(255, 255, 255), sub=mix((255, 255, 255), b, .32),
                    acc=(255, 220, 120), acc2=mix((255, 220, 120), b, .22), frame=mix(b, (0, 0, 0), .45), quiet=mix(b, (0, 0, 0), .3))
    import colorsys
    hh = colorsys.rgb_to_hls(*[v / 255 for v in ac])[0]
    def hls(l, s_): return tuple(int(v * 255) for v in colorsys.hls_to_rgb(hh, l, s_))
    vivid, vivid2 = hls(.46, .88), hls(.70, .70)              # 대표 이미지 색상(色相)만 따고 채도를 올려 맑게(10/16 대표 "똥색깔, 지저분": 탁한 중간 톤 금지)
    if kind == "cream":                                       # 대표 이미지 바탕 그대로 + 흰 칸 + 검정 글자 + 맑은 강조색 하나
        return dict(bg=bg, card=(255, 255, 255), line=mix(bg, (0, 0, 0), .10), ink=(20, 20, 22), sub=(96, 96, 102), acc=vivid, acc2=hls(.38, .60), frame=(20, 20, 22), quiet=mix(bg, (0, 0, 0), .1))
    if kind == "white":                                       # 흰 바탕 + 아주 옅은 회색 칸 + 검정 글자 + 맑은 강조색 하나
        return dict(bg=(255, 255, 255), card=(245, 245, 247), line=(226, 226, 230), ink=(17, 17, 19), sub=(96, 96, 102), acc=vivid, acc2=hls(.38, .60), frame=(17, 17, 19), quiet=(226, 226, 230))
    if kind == "vivid":                                       # 맑은 강조색 바탕 + 흰 칸 + 검정 글자(흰 글자는 노랑·주황 위에서 안 읽힘)
        b = hls(.56, .92)
        return dict(bg=b, card=(255, 255, 255), line=mix(b, (0, 0, 0), .12), ink=(17, 17, 19), sub=(70, 60, 50), acc=(17, 17, 19), acc2=hls(.20, .80), frame=(17, 17, 19), quiet=mix(b, (0, 0, 0), .12))
    ink = mix(ac, (0, 0, 0), .72)
    return dict(bg=bg, card=(255, 255, 255), line=mix(bg, ac, .3), ink=ink, sub=mix(ink, bg, .45), acc=ac, acc2=mix(ac, bg, .18), frame=ink, quiet=mix(bg, ac, .3))

# v9(10/16 대표 참고 영상 '조회수 폭발하는 색조합'): 진한 맑은 색 하나 + 옅은 반대 계열 색 하나, 두 색만. 진한 바탕엔 흰 글자·옅은 색 강조, 옅은 바탕엔 진한 색 글자
PAIRS = {"violet": ((0x31, 0x1B, 0x92), (0xFF, 0xE0, 0xB2)),   # Violet Purple + Tangerine Cream
         "royal": ((0x0A, 0x46, 0xB3), (0xFF, 0xEA, 0xD2)),    # Royal Blue + Apricot Peach
         "navy": ((0x10, 0x2A, 0x43), (0xFF, 0xF3, 0xC4)),     # Midnight Navy + Soft Butter
         "emerald": ((0x00, 0x4D, 0x40), (0xEF, 0xE5, 0xFD)),  # Deep Emerald + Dusty Lilac
         "olive": ((0x4A, 0x53, 0x3C), (0xFF, 0xD3, 0xE8)),    # Olive Khaki + Refreshing Pink
         "charcoal": ((0x24, 0x27, 0x29), (0xD2, 0xFF, 0x28)), # Matte Charcoal + Neon Lime
         "choco": ((0x3E, 0x27, 0x23), (0xE1, 0xF5, 0xFE))}    # Deep Chocolate + Powder Blue
def pair_theme(name, inverse=False):
    d, l = PAIRS[name]
    if not inverse:   # 진한 바탕: 칸은 한 단 밝은 같은 색, 글자 흰색, 강조 = 옅은 색
        return dict(bg=d, card=mix(d, (255, 255, 255), .09), line=mix(d, (255, 255, 255), .2), ink=(255, 255, 255), sub=mix((255, 255, 255), d, .3),
                    acc=l, acc2=mix(l, d, .25), frame=mix(d, (0, 0, 0), .4), quiet=mix(d, (255, 255, 255), .2))
    return dict(bg=l, card=(255, 255, 255), line=mix(l, d, .18), ink=d, sub=mix(d, l, .35), acc=d, acc2=mix(d, l, .3), frame=d, quiet=mix(l, d, .18))

PAL_JSON = os.path.join(HERE, "..", "assets", "palettes", "color_combos.json")
def palette_theme(pid):
    """색 조합 목록(대표 참고 자료 모음)에서 판을 만든다. 두 색 조합(pair)은 pair_theme 규칙, 나머지는 목록에 적힌 theme 그대로."""
    import json
    inv = pid.endswith("_inv"); key = pid[:-4] if inv else pid
    e = next(x for x in json.load(open(PAL_JSON, encoding="utf-8"))["palettes"] if x["id"] == key)
    h2 = lambda c: tuple(int(c[i:i + 2], 16) for i in (1, 3, 5))
    if "pair" in e:
        PAIRS[key] = tuple(h2(c) for c in e["pair"]); return pair_theme(key, inv)
    return {k: h2(v) for k, v in e["theme"].items()}

ICONS = []
def loop_k(name, head, nodes, exit_label, exit_text, mode="dark", icons=()):
    global ICONS; ICONS = list(icons)
    st = KEY[mode]; H = 1145; cv = Cv(H, st["bg"])
    # 10/15 대표 "그라데이션 진짜...": 빛 방울·그라데이션 배경 쓰지 않는다(K-041). 바탕은 단색
    k_head(cv, head, st)
    cx, cy, r = (L + RT) / 2, 545, 262; bw, bh = 340, 190
    pos = [(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)]
    for i in range(4):
        a0 = -90 + i * 90 + 27; a1 = -90 + (i + 1) * 90 - 27; pts = []
        for k in range(13):
            t = math.radians(a0 + (a1 - a0) * k / 12); pts.append((cx + r * math.cos(t), cy + r * math.sin(t)))
        ac = POP[(i + 1) % 4] if mode == "light" else st["acc2"]
        for p_, q in zip(pts, pts[1:]): cv.line(p_[0], p_[1], q[0], q[1], ac, 6 if mode == "light" else AW)
        arrow(cv, pts[-2][0], pts[-2][1], pts[-1][0], pts[-1][1], ac, 6 if mode == "light" else AW, 24 if mode == "light" else AH)
    if mode != "light": cv.text(cx, cy, "되풀이", PX, 34, st["sub"], "mm")
    else: cv.text(cx, cy, "되풀이", PX, 42, st["sub"], "mm")
    for i, ((x, y), t) in enumerate(zip(pos, nodes)):
        c = POP[i]
        if mode == "light":
            cv.rr([x - bw / 2, y - bh / 2, x + bw / 2, y + bh / 2], 30, fill=tint(c, .22))
            cv.rr([x - bw / 2, y - bh / 2, x - bw / 2 + 12, y + bh / 2], 6, fill=c)
            box_text(cv, x + 6, y, t, 42, deep(c, .38) if i != 1 else (110, 70, 10), PX)
        else:
            c = NEON[i]
            # 10/15 대표 "AI 특유의 아이콘 빼고 깔끔하게"(K-042): 아이콘 없음. 번호(01~04)만 강조색, 칸은 단색 면 + 1px 선
            cv.rr([x - bw / 2, y - bh / 2, x + bw / 2, y + bh / 2], 28, fill=st["card"], outline=st["line"], w=1.5)
            cv.text(x - bw / 2 + 32, y - bh / 2 + 40, f"0{i + 1}", PX, 30, st["acc2"], "lm")
            for k2, l2 in enumerate(t): cv.text(x - bw / 2 + 32, y - bh / 2 + 96 + k2 * 52, l2, PX, 40, st["ink"], "lm")
    by0, by1 = 965, 1085
    band, lab_c, txt_c = (NAVY, POP[1], WHITE) if mode == "light" else (st.get("hl", st["acc"]), st.get("hl_ink", st["bg"]), st.get("hl_ink", st["bg"]))
    cv.rr([L, by0, RT, by1], 32, fill=band)
    L0 = L
    lw = cv.tw(exit_label, PX, 46); cv.text(L0 + 44, (by0 + by1) / 2, exit_label, PX, 46, lab_c, "lm")
    cv.text(L0 + 44 + lw + 34, (by0 + by1) / 2, exit_text, PX, cv.fit(exit_text, PX, 46, RT - L - lw - 120, 42), txt_c, "lm")
    arrow(cv, cx + r + bw / 2 - 34, cy + bh / 2 + 8, cx + r + bw / 2 - 34, by0 - 12, NAVY if mode == "light" else st["acc"], 6 if mode == "light" else AW, 24 if mode == "light" else AH)
    cv.save(name)

def screen_k(name, head, shot, crop_h, notes, mode="dark"):
    from PIL import Image
    st = KEY[mode]; im = Image.open(shot).convert("RGB"); im = im.crop((0, 0, im.width, min(crop_h, im.height)))
    pad_px = 60; bgc = im.getpixel((im.width - 4, 6)); cvs = Image.new("RGB", (im.width + pad_px * 2, im.height + pad_px), bgc); cvs.paste(im, (pad_px, pad_px)); im = cvs   # 캡처 글자가 틀에 붙지 않게 화면 안쪽 여백
    pw = 420; ph = int(im.height * pw / im.width); H = ph + 260; cv = Cv(H, st["bg"])
    x0, y0, pad = L + 34, 186, 22                              # 폰 틀: 화면 둘레에 검은 테두리 여백
    if mode == "dark":
        pass   # 그라데이션·빛 배경 금지(K-041)
    k_head(cv, head, st)
    cv.rr([x0 - pad, y0 - pad, x0 + pw + pad, y0 + ph + pad], 48, fill=st["frame"] if mode != "light" else (29, 29, 31), outline=st["line"] if mode != "light" else None, w=1.5)
    cv.img.paste(im.resize((pw * K.S, ph * K.S)), (x0 * K.S, y0 * K.S))
    tx = x0 + pw + pad + 40; n = len(notes); gap = 20; ch = (ph - gap * (n - 1)) / n; y = y0
    for j, (lab, txt) in enumerate(notes):                    # 벤토 카드: 칸마다 다른 강조색 띠 + 이름표 + 큰 값
        c = POP[j % 4] if mode == "light" else st["acc2"]
        cv.rr([tx, y, RT, y + ch], 30, fill=st["card"] if mode != "light" else tint(c, .2))
        if mode != "light":                                     # 아이콘 없음(K-042): 단색 면 + 1px 선, 이름표만 강조색
            cv.rr([tx, y, RT, y + ch], 28, fill=st["card"], outline=st["line"], w=1.5)
        else: cv.rr([tx, y + 22, tx + 10, y + ch - 22], 5, fill=c)
        cv.text(tx + 36, y + 44, lab, PB, 34, c if mode != "light" else deep(c, .45) if j != 1 else (120, 76, 10), "lm")
        cv.text(tx + 36, y + ch - 34, txt, PB if not any('\u4e00' <= c <= '\u9fff' for c in txt) else PB, cv.fit(txt, PX, 52, RT - tx - 72, 40), st["ink"], "ls")
        y += ch + gap
    cv.save(name)


# ---- v5(10/15 대표 "디자인 감 좀 올려라", docs/디자인_레퍼런스_라이브러리): 아이콘(Lucide)·빛 방울 배경(Haikei 방식)·기기 목업(Shots.so 방식) ----
ICON_DIR = os.path.join(HERE, "..", "assets", "icons", "lucide")
def icon(name, color, px, stroke=2.2):
    import cairosvg, io
    from PIL import Image
    svg = open(os.path.join(ICON_DIR, name + ".svg"), encoding="utf-8").read().replace("currentColor", "#%02x%02x%02x" % color).replace('stroke-width="2"', f'stroke-width="{stroke}"')
    return Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg.encode(), output_width=px * K.S, output_height=px * K.S))).convert("RGBA")
def put_icon(cv, name, color, cx, cy, px, chip=None):
    if chip: cv.rr([cx - px * .9, cy - px * .9, cx + px * .9, cy + px * .9], px * .45, fill=chip)
    im = icon(name, color, px); cv.img.paste(im, (int((cx - px / 2) * K.S), int((cy - px / 2) * K.S)), im)
def glow(cv, H, spots):   # 쓰지 않음(대표 10/15 그라데이션 금지, K-041). 남겨 두되 호출하지 않는다
    """어두운 판 위에 흐린 빛 방울(색, 중심, 반지름, 세기). 바탕 판 안에서만."""
    from PIL import Image, ImageDraw, ImageFilter
    W = K.BW * K.S; layer = Image.new("RGB", (W, H * K.S), (0, 0, 0)); d = ImageDraw.Draw(layer)
    for col, (x, y), r, a in spots:
        d.ellipse([(x - r) * K.S, (y - r) * K.S, (x + r) * K.S, (y + r) * K.S], fill=tuple(int(v * a) for v in col))
    layer = layer.filter(ImageFilter.GaussianBlur(140 * K.S))
    from PIL import ImageChops
    m = Image.new("L", layer.size, 0); ImageDraw.Draw(m).rounded_rectangle([K.OX * K.S, 0, (K.OX + K.CW) * K.S - 1, H * K.S - 1], 44 * K.S, fill=255)
    lit = ImageChops.add(cv.img, layer); cv.img.paste(lit, (0, 0), m); cv.d = ImageDraw.Draw(cv.img)
def soft_shadow(cv, box, r, blur=40, alpha=170):
    from PIL import Image, ImageDraw, ImageFilter
    W, Hh = cv.img.size; sh = Image.new("L", (W, Hh), 0)
    ImageDraw.Draw(sh).rounded_rectangle([v * K.S for v in (box[0], box[1] + 24, box[2], box[3] + 24)], r * K.S, fill=alpha)
    sh = sh.filter(ImageFilter.GaussianBlur(blur * K.S)); black = Image.new("RGB", (W, Hh), (0, 0, 0)); cv.img.paste(black, (0, 0), sh); cv.d = ImageDraw.Draw(cv.img)

def calc_k(name, head, digits, steps, result_big, result_label, result_line, mode="dark"):
    """계산 과정(비실사 이미지 1순위 '계산 과정', 10/15 조사 보고서): 생년월일 숫자 칸 → 더하기 → 한 자리로 → 결과. 색은 K-043(강조 하나·누른 톤·흰색)."""
    st = KEY[mode]; H = 900; cv = Cv(H, st["bg"]); k_head(cv, head, st)
    n = len(digits); g = 14; cw = (RT - L - 20 - g * (n - 1)) / n; y0 = 200; ch = 120
    for i, d_ in enumerate(digits):                          # 1행: 숫자 칸
        x = L + 10 + i * (cw + g)
        cv.rr([x, y0, x + cw, y0 + ch], 22, fill=st["card"], outline=st["line"], w=1.5)
        cv.text(x + cw / 2, y0 + ch / 2, d_, PX, 64, st["ink"], "mm")
    for k, (lab, expr) in enumerate(steps):                 # 2~3행: 단계(누른 노랑 이름표 + 흰 식)
        y = y0 + ch + 70 + k * 110
        cv.text(L + 14, y, lab, PB, 42, st["acc2"], "lm")
        cv.text(L + 240, y, expr, PX, 52, st["ink"], "lm")
        cv.line(L + 14, y + 52, RT - 14, y + 52, st["line"], 1.5)
    yb = y0 + ch + 70 + len(steps) * 110 + 20               # 결과: 강조색은 여기 한 곳
    hl = st.get("hl"); hi = st.get("hl_ink", st["ink"])          # 색 조합에 '강조 면'(hl)이 있으면 결과 칸을 그 색으로 채운다
    cv.rr([L + 10, yb, RT - 10, yb + 200], 30, fill=hl or st["card"], outline=None if hl else st["line"], w=1.5)
    cv.text(L + 60, yb + 100, result_big, PX, 150, hi if hl else st["acc"], "lm")
    cv.text(L + 230, yb + 68, result_label, PB, 42, hi if hl else st["acc2"], "lm")
    cv.text(L + 230, yb + 130, result_line, PX, 50, hi if hl else st["ink"], "lm")
    cv.save(name)

def compare_k(name, head, cols, rows, same_rows=(), mode="dark"):
    """비교·대조(조사 보고서 2순위): 두 사람·두 풀이를 나란히. 같은 말인 줄은 값만 강조색(K-043), 다른 말은 흰색."""
    st = KEY[mode]; rh = 176; H = 220 + 110 + rh * len(rows) + 70; cv = Cv(H, st["bg"]); k_head(cv, head, st)
    lw = 250; cw = (RT - L - 20 - lw - 20) / 2; x1 = L + 10 + lw; x2 = x1 + cw + 20; y = 200
    for j, c_ in enumerate(cols):                            # 머리 칸
        x = x1 if j == 0 else x2
        cv.text(x + cw / 2, y + 40, c_, PX, 44, st["ink"], "mm")
    cv.line(L + 10, y + 90, RT - 10, y + 90, st["line"], 1.5); y += 110
    for i, (lab, a, b) in enumerate(rows):
        same = i in same_rows; hlr = same and st.get("hl"); col = st.get("hl_ink", st["ink"]) if hlr else st["acc"] if same else st["ink"]
        cv.text(L + 20, y + rh / 2, lab, PB, 42, st["acc2"], "lm")
        for x, v in ((x1, a), (x2, b)):
            cv.rr([x, y + 14, x + cw, y + rh - 14], 24, fill=st["hl"] if hlr else st["card"], outline=None if hlr else st["line"], w=1.5)
            vs = v if isinstance(v, (list, tuple)) else [v]
            if len(vs) == 1: cv.text(x + cw / 2, y + rh / 2, vs[0], PX, cv.fit(vs[0], PX, 52, cw - 40, 38), col, "mm")
            else:
                cv.text(x + cw / 2, y + rh / 2 - 26, vs[0], PX, cv.fit(vs[0], PX, 48, cw - 40, 36), col, "mm")
                cv.text(x + cw / 2, y + rh / 2 + 36, vs[1], PB, 40, st["sub"], "mm")
        y += rh
    cv.save(name)

def calc_kb(name, head, digits, steps, result_big, result_label, result_line, mode="dark", char="v11_mug"):
    """B안(조사 보고서 A/B 검증): calc_k와 같고 결과 칸 오른쪽에 정월 컷 + AI 표기(오른쪽 아래)."""
    from PIL import Image
    st = KEY[mode]; H = 980; cv = Cv(H, st["bg"]); k_head(cv, head, st)
    n = len(digits); g = 14; cw = (RT - L - 20 - g * (n - 1)) / n; y0 = 200; ch = 120
    for i, d_ in enumerate(digits):
        x = L + 10 + i * (cw + g)
        cv.rr([x, y0, x + cw, y0 + ch], 22, fill=st["card"], outline=st["line"], w=1.5)
        cv.text(x + cw / 2, y0 + ch / 2, d_, PX, 64, st["ink"], "mm")
    for k, (lab, expr) in enumerate(steps):
        y = y0 + ch + 70 + k * 110
        cv.text(L + 14, y, lab, PB, 42, st["acc2"], "lm"); cv.text(L + 260, y, expr, PX, 52, st["ink"], "lm")
        cv.line(L + 14, y + 52, RT - 14, y + 52, st["line"], 1.5)
    yb = y0 + ch + 70 + len(steps) * 110 + 20; xr = RT - 330
    cv.rr([L + 10, yb, xr, yb + 220], 30, fill=st["card"], outline=st["line"], w=1.5)
    cv.text(L + 50, yb + 110, result_big, PX, 150, st["acc"], "lm")
    cv.text(L + 200, yb + 76, result_label, PB, 40, st["acc2"], "lm")
    cv.text(L + 200, yb + 146, result_line, PX, cv.fit(result_line, PX, 50, xr - L - 230, 40), st["ink"], "lm")
    im = Image.open(os.path.join(HERE, "..", "characters", "cut", char + ".png")).convert("RGBA"); im = im.crop(im.getbbox())
    hh = H - 64 - (yb - 60); ww = int(im.width * hh / im.height); im = im.resize((int(ww * K.S), int(hh * K.S)))
    cx = (xr + RT) / 2 + 10; cv.img.paste(im, (int((cx - ww / 2) * K.S), int((yb - 60) * K.S)), im)
    cv.text(RT - 14, H - 22, "AI로 생성한 가상의 캐릭터입니다", PB, 24, st["sub"], "rs")
    cv.save(name)

def screen_wide_k(name, head, shot, crop_h, mode="dark"):
    """실제 화면(가로로 넓은 부분): 캡처를 내용 폭 그대로, 얇은 테두리 틀만. 설명 문구는 본문에(K-036)."""
    from PIL import Image
    st = KEY[mode]; im = Image.open(shot).convert("RGB"); im = im.crop((0, 0, im.width, min(crop_h, im.height)))
    w = RT - L - 120; h = int(im.height * w / im.width); H = h + 260; cv = Cv(H, st["bg"]); k_head(cv, head, st)
    x0, y0, pad = L + 60, 180, 18
    cv.rr([x0 - pad, y0 - pad, x0 + w + pad, y0 + h + pad], 40, fill=st.get("frame", st["ink"]), outline=st["line"], w=1.5)
    cv.img.paste(im.resize((int(w * K.S), int(h * K.S))), (int(x0 * K.S), int(y0 * K.S)))
    cv.save(name)

BODY_LINE = {   # 이미지 바로 위에 넣을 본문 문장(이미지에 박지 않는 설명)
 "n47": "아래는 1995년 3월 19일(예시 생일)로 자오선 무료 풀이를 직접 열어 본 화면이에요.",
 "n34": "같은 생각이 되풀이되는 모양을 그림으로 그려 보면 이래요.",
}
SPEC = {
 "n53v": lambda m="dark": compare_k("naver_z53_v.jpg", "같은 3번, 다른 두 사람", ["1990년 5월 15일", "1991년 3월 7일"],
                       [("생일 숫자", "3번", "3번"), ("사주 일간", ["경(庚)", "다듬기 전의 쇠"], ["병(丙)", "한낮의 태양"]), ("별자리", "황소자리", "물고기자리")], same_rows=(0,), mode=m),
 "n53s": lambda m="dark": screen_wide_k("naver_z53_s.jpg", "무료 풀이에서 확인한 내 숫자", os.environ.get("SHOT53", "free_map.png"), 760, m),
 "n53b": lambda m="dark": calc_kb("naver_z53_kb.jpg", "생일 숫자, 이렇게 더해요", list("19900515"),
                       [("모두 더하기", "1+9+9+0+0+5+1+5 = 30"), ("한 자리로", "3+0 = 3")], "3", "1990년 5월 15일생", "표현이 풍부한 3번", m),
 "n53": lambda m="dark": calc_k("naver_z53_k.jpg", "생일 숫자, 이렇게 더해요", list("19900515"),
                       [("모두 더하기", "1+9+9+0+0+5+1+5 = 30"), ("한 자리로", "3+0 = 3")], "3", "1990년 5월 15일생", "표현이 풍부한 3번", m),
 "n47": lambda m="dark": screen_k("naver_z47_s7.jpg" if m == "dark" else "naver_z47_s_light.jpg", "무료 풀이를 직접 열어 봤어요", os.environ.get("SHOT", "free.png"), 1365,
                       [("생년월일", "1995년 3월 19일"), ("태어난 날 첫 글자", "기(己) · 기름진 논밭"), ("이어서 나오는 것", "성격 · 사랑 · 일 · 돈")], m),
 "n34": lambda m="dark": loop_k("naver_z34_p7.jpg" if m == "dark" else "naver_z34_p_light.jpg", "생각이 같은 자리를 도는 고리",
                       [["같은 걱정이", "떠올라요"], ["그 장면을", "되짚어요"], ["기분이 더", "가라앉아요"], ["잠이 줄고", "월요일이 무겁죠"]],
                       "끊는 법", "종이에 다 적고, 내일 할 일 하나만 정해요", m),
}
if __name__ == "__main__":
    m = os.environ.get("MODE", "dark")
    if m.startswith("pal:"):                                     # MODE=pal:y_blue — sns-images assets/palettes/color_combos.json
        KEY[m] = palette_theme(m[4:])
    elif m.startswith("pair"):                                     # MODE=pair:violet / pairinv:violet
        KEY[m] = pair_theme(m.split(":")[1], m.startswith("pairinv"))
    elif os.environ.get("COVER"):                                  # COVER=대표이미지경로 MODE=tone|same → 대표 이미지 색조에 맞춘 판
        KEY[m] = cover_theme(os.environ["COVER"], m)
    if os.environ.get("SUFX"):                                   # 색조 판은 새 이름으로(naver_z53_k.jpg → naver_z53_kt.jpg). 덮어쓰기 금지 규칙
        _sv = K.Cv.save
        K.Cv.save = lambda s_, name: _sv(s_, name.replace(".jpg", os.environ["SUFX"] + ".jpg"))
    if os.environ.get("PREVIEW"):                                # 시안: img/에 넣지 않고 지정 폴더에만 저장(새 이름 규칙 보호)
        from PIL import Image as _I
        def _pv(s_, name, _d=os.environ["PREVIEW"]):
            s_.d.rectangle([0, 0, K.OX * K.S - 1, s_.h * K.S], fill=WHITE); s_.d.rectangle([(K.OX + K.CW) * K.S, 0, K.BW * K.S, s_.h * K.S], fill=WHITE)
            s_.img.resize((K.BW, s_.h), _I.LANCZOS).save(os.path.join(_d, m + "_" + name), quality=93)
        K.Cv.save = _pv
    for k in sys.argv[1:]: SPEC[k](m); print(k, m, "만듦", K.WARN or "")
