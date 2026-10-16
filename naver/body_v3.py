"""네이버 원고 안 이미지 새 틀 v3 (10/16 대표: "기존 이미지와 똑같은 형태로 색감만 바뀐 것 같다").
표지 v3c와 같은 문법: 그 글 표지와 같은 두 색 판을 꽉 채운 바탕, 굵은 고딕 큰 글자, 흰 칸·테두리·한자 워터마크 없음.
- table_v3: 세 풀이 표 → 줄마다 [이름표(강조색)] 큰 값 + 한 줄 설명, 줄 사이 얇은 선
- rows_v3 : 해 볼 것 → 큰 번호 원(강조색) + 큰 글 + 작은 글
- intro_v3: 한눈에 보기(한 줄 결론) → 정월은 여기만(K-062), 결론 문장을 가장 크게
파일은 새 이름만(*4.jpg). 사용: python3 naver/body_v3.py n34   (시안: PREVIEW=폴더 를 주면 그 폴더에만)"""
import os, sys, json, re
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "pipeline"))
import imgkit as K
from imgkit import Cv, L, RT, SER, WHITE
import cover_v3 as V
XB = K.FD + "PRETENDARD-EXTRABOLD.OTF"; BK = K.FD + "PRETENDARD-BLACK.OTF"; SB = K.FD + "PRETENDARD-SEMIBOLD.OTF"
PREVIEW = os.environ.get("PREVIEW")

def _save(cv, name):
    if PREVIEW:
        from PIL import Image
        cv.d.rectangle([0, 0, K.OX * K.S - 1, cv.h * K.S], fill=WHITE); cv.d.rectangle([(K.OX + K.CW) * K.S, 0, K.BW * K.S, cv.h * K.S], fill=WHITE)
        cv.img.resize((K.BW, cv.h), Image.LANCZOS).save(os.path.join(PREVIEW, name), quality=92); return
    cv.save(name)

def _panel(H, c):
    cv = Cv(H, c.bg); return cv

def _head(cv, c, head):
    cv.text(L + 10, 96, head, XB, cv.fit(head, XB, 68, RT - L - 220, 52), c.fg, "ls")
    cv.text(RT - 10, 92, "子午線 자오선", SER, 30, c.gray, "rs")

def table_v3(name, c, head, cols, rows_):
    rh = 170; top = 150; H = top + rh * len(rows_) + 50; cv = _panel(H, c); _head(cv, c, head)
    for i, r in enumerate(rows_):
        y = top + i * rh
        if i: cv.line(L + 10, y, RT - 10, y, c.line, 2)
        lab, val = r[0], r[1]; one = r[2] if len(r) > 2 else ""
        lw = cv.tw(lab, XB, 40) + 48
        cv.rr([L + 10, y + 30, L + 10 + lw, y + 30 + 62], 31, fill=c.acc); cv.text(L + 10 + lw / 2, y + 61, lab, XB, 40, c.pillfg, "mm")
        x = L + 10 + max(lw, 190) + 34; mw = RT - 10 - x
        cv.text(x, y + 76, val, XB, cv.fit(val, XB, 60, mw, 42), c.fg, "ls")
        if one: cv.text(x, y + 132, one, SB, cv.fit(one, SB, 42, mw, 34), c.gray, "ls")
    _save(cv, name)

def rows_v3(name, c, head, items):
    rh = 168; top = 150; H = top + rh * len(items) + 40; cv = _panel(H, c); _head(cv, c, head)
    for i, it in enumerate(items):
        lab, big, small = it[0], it[1], (it[2] if len(it) > 2 else "")
        y = top + i * rh; r = 46; cx = L + 10 + r
        cv.d.ellipse([(cx - r) * K.S, (y + 30) * K.S, (cx + r) * K.S, (y + 30 + 2 * r) * K.S], fill=c.acc)
        cv.text(cx, y + 30 + r, str(i + 1), BK, 50, c.pillfg, "mm")
        x = cx + r + 34; mw = RT - 10 - x
        cv.text(x, y + 78, big, XB, cv.fit(big, XB, 58, mw, 42), c.fg, "ls")
        sub = f"{lab} · {small}" if small else lab
        cv.text(x, y + 132, sub, SB, cv.fit(sub, SB, 40, mw, 32), c.gray, "ls")
    _save(cv, name)

def intro_v3(name, c, summary, maps, label, face):
    import thumb_sq as TQ
    tmp = Cv(100, c.bg); mw = RT - L - 20
    for size in range(76, 50, -2):
        ls = K.balanced(tmp, summary, XB, size, mw)
        if len(ls) <= 3: break
    lh = int(size * 1.3); R_ = 70
    H = 70 + 2 * R_ + 40 + 70 + len(ls) * lh + 40 + 60 + 60; cv = _panel(H, c)
    cy = 70 + R_; cx = L + 10 + R_
    TQ.badge(cv.img, cv.d, face, c, int(cx * K.S), int(cy * K.S), int(R_ * K.S))
    cv.text(cx + R_ + 30, cy - 18, "정월의 한 줄 결론", XB, 40, c.acc, "lm"); cv.text(cx + R_ + 30, cy + 30, "AI로 생성한 가상의 캐릭터입니다", SB, 26, c.gray, "lm")
    y = 70 + 2 * R_ + 50
    for l in ls: cv.text(L + 10, y, l, XB, size, c.fg, "la"); y += lh
    cv.line(L + 10, y + 20, L + 170, y + 20, c.acc, 10)
    plain = re.sub(r"\([^)]*[\u4e00-\u9fff][^)]*\)", "", maps); m = label + "  " + plain   # 한자 괄호는 빼고(글꼴이 섞여 보임)
    cv.text(L + 10, y + 70, m, SB, cv.fit(m, SB, 38, mw, 28), c.gray, "la")
    _save(cv, name)

def pal_of(pid):
    pick = json.load(open(os.path.join(HERE, "cover_v3_pick.json"), encoding="utf-8")); p = pick.get(pid)
    return V.Ctx(p)
