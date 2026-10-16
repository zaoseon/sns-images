"""카드·표지 제작 관문 — 통과해야 그리기가 시작된다 (대표 10/16 "규칙 강제해라").

왜 관문인가: 규칙을 문서에만 적어 두면 안 지켜진다는 것을 10/16 하루에 세 번 봤다.
K-058~062 가 새벽에 적혔는데 같은 날 밤 캐러셀이 어겼고, K-025 는 코드로 막기 전까지
덮어쓰기를 못 막았고, 채널 규격(channel_specs)·고정 요소(brand_frame)·글꼴(fonts_kit)은
10/6 부터 있었는데 10/16 표지가 하나도 안 따랐다. 그래서 검사를 그리기 앞에 둔다.

쓰는 법 — 그리는 쪽 맨 위에서 부르면 된다:
    import card_gate as G
    G.before(spec_card, channel="insta_carousel", prev=앞에_쓴_판목록)   # 못 지키면 SystemExit
    ...그린다...
    G.after(이미지경로, spec_card, channel="insta_carousel")             # 결과물을 숫자로 잰다

ZS_SKIP_GATE=1 로만 건너뛴다. 왜 건너뛰는지 커밋에 적는다.
"""
import os, sys, json, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
import channel_specs as CS

COMBOS = os.path.join(ROOT, "assets", "palettes", "color_combos.json")

# 대표가 거듭 지적한 글말·번역투. 표지 글자에 쓰지 않는다.
글말 = ["타고난 결", "~하는 결", "결이 맞", "두 겹으로", "~에 대해", "~을 통해", "~에 있어"]
# 문장이 끊긴 꼴(서술어 없이 끝남). 표지 제목에서 특히 자주 났다.
끊김 = re.compile(r"(을|를|이|가|은|는|와|과|의|에|로|으로)\s*[?!.]?$")


def _pal():
    d = json.load(open(COMBOS, encoding="utf-8"))
    return {p["id"]: p for p in d["palettes"]}


def lum(hx):
    hx = hx.lstrip("#")
    r, g, b = (int(hx[i:i + 2], 16) / 255 for i in (0, 2, 4))
    f = lambda c: c / 12.92 if c <= .04045 else ((c + .055) / 1.055) ** 2.4
    return .2126 * f(r) + .7152 * f(g) + .0722 * f(b)


def contrast(a, b):
    la, lb = lum(a), lum(b)
    return (max(la, lb) + .05) / (min(la, lb) + .05)


def before(c, channel="insta_carousel", prev=None):
    """그리기 전 검사. 하나라도 걸리면 멈춘다."""
    if os.environ.get("ZS_SKIP_GATE") == "1":
        return []
    CH = CS.CH[channel]
    fonts, bad = CH["fonts"], []
    P = _pal()
    cid = c.get("id", "?")

    # 1. 판은 색 조합 목록에서 고른다 (K-059·K-068). 눈대중 HEX 금지.
    if c.get("pal") not in P:
        bad.append(f"판 '{c.get('pal')}' 이 assets/palettes/color_combos.json 에 없어요. 목록에서 고르세요.")
    else:
        쓸수있는색 = {v.upper() for v in P[c["pal"]]["colors"].values()}
        for k in ("bg", "acc"):
            if c.get(k) and c[k].upper() not in 쓸수있는색:
                bad.append(f"{k} {c[k]} 가 판 '{c['pal']}' 의 색이 아니에요. 판 안의 색만 쓰세요(섞지 않기).")

    # 2. 글자 색 대비 — 단색 판 + 흰 글자가 기본(대표 10/16), 안 되면 멈춘다
    if c.get("bg"):
        fg = "#FFFFFF" if lum(c["bg"]) < .38 else "#141414"
        if contrast(fg, c["bg"]) < 4.5:
            bad.append(f"바탕 {c['bg']} 에서는 글자 대비가 {contrast(fg, c['bg']):.1f}:1 이라 안 읽혀요(4.5 이상 필요).")

    # 3. 정월 (K-061) — '말하는 글'에만, 어두운 판에만
    if c.get("face"):
        if c.get("bg") and lum(c["bg"]) >= .38:
            bad.append("밝은 판에 정월을 놓으려 해요. 누끼 가장자리가 지저분하게 보여요. 어두운 판에만 씁니다(대표 10/16).")
        if not c.get("말하는글"):
            bad.append("정월은 정월이 '말하는 글'(모집·공지·인사)에만 나와요(K-061). 맞으면 사양에 \"말하는글\": true 를 적으세요.")

    # 4. 글꼴 크기 — 채널 규격 아래로 못 내려간다
    def 범위(s):
        n = [int(x) for x in re.findall(r"\d+", s)]
        return (n[0], n[-1]) if n else (0, 9999)
    lo, hi = 범위(fonts["title"])
    if c.get("title_size") and not (lo <= c["title_size"] <= hi):
        bad.append(f"제목 {c['title_size']}px 가 채널 규격({fonts['title']}) 밖이에요.")
    if c.get("body_size") and c["body_size"] < 범위(fonts["body"])[0]:
        bad.append(f"본문 {c['body_size']}px 는 너무 작아요({fonts['body']}).")

    # 5. 글 — 자연어·입말·의미 단위 줄바꿈
    줄 = list(c.get("hook", [])) + list(c.get("subs", []))
    for t in 줄:
        for w in 글말:
            if w.replace("~", "") in t:
                bad.append(f"글말 '{w}' 가 있어요: \"{t}\"")
    if c.get("hook"):
        끝 = c["hook"][-1]
        if 끊김.search(끝.strip()):
            bad.append(f"제목 마지막 줄이 조사로 끝나 문장이 끊겨요: \"{끝}\" — 서술어까지 넣으세요.")
        if len(c["hook"]) > 1 and any(len(l.strip()) <= 2 for l in c["hook"]):
            bad.append("제목에 두 글자 이하 줄이 있어요. 의미 단위로 고르게 나누세요.")

    # 6. 훅 유형 (K-064) — 열한 가지에서 돌려 쓴다
    if not c.get("훅"):
        bad.append("훅 유형을 사양에 적으세요(K-064 열한 가지 중 하나). 안 적으면 같은 유형만 쓰게 돼요.")

    # 7. 연속 금지 (K-068) — 앞 5편과 같은 판 금지
    if prev:
        if c.get("pal") in list(prev)[-5:]:
            bad.append(f"판 '{c['pal']}' 을 앞 5편 안에서 이미 썼어요(K-068). 다른 판을 고르세요.")

    if bad:
        raise SystemExit("\n[관문에 걸렸어요] " + cid + "\n" + "\n".join("  · " + b for b in bad)
                         + "\n  고친 뒤 다시 돌리세요. 정말 넘겨야 하면 ZS_SKIP_GATE=1 을 붙이고 커밋에 이유를 적으세요.\n")
    return []


def after(path, c, channel="insta_carousel"):
    """그린 뒤 결과물을 숫자로 잰다 — 안전 영역·여백 균형·겹침."""
    if os.environ.get("ZS_SKIP_GATE") == "1":
        return []
    import numpy as np
    from PIL import Image
    CH = CS.CH[channel]
    sx0, sy0, sx1, sy1 = CH["safe"]
    im = Image.open(path).convert("RGB")
    W, H = im.size
    bad = []
    if (W, H) != (CH["w"], CH["h"]):
        bad.append(f"크기가 {W}x{H} 예요. {CH['name']} 은 {CH['w']}x{CH['h']} 입니다(안 맞으면 잘려요).")
    a = np.asarray(im).astype(int)
    bg = a[4, 4]
    diff = np.abs(a - bg).sum(2) > 26
    ys, xs = np.where(diff.any(1))[0], np.where(diff.any(0))[0]
    if len(ys):
        t, b, l, r = int(ys[0]), H - 1 - int(ys[-1]), int(xs[0]), W - 1 - int(xs[-1])
        if l < sx0 - 2 or r < (W - sx1) - 2 or t < sy0 - 2:
            bad.append(f"내용이 안전 영역을 벗어났어요(위{t} 왼{l} 오{r} / 안전 영역 위{sy0} 옆{sx0}).")
        if abs(l - r) > W * 0.06 and not c.get("face"):
            bad.append(f"좌우 여백이 {l} 대 {r} 로 치우쳤어요.")

    # 위 쏠림 — 고정 요소(상단 띠·하단 주소)를 빼고 '내용'만 보고 잰다.
    # 10/16 1판은 고정 요소가 아래에 있어서 균형 검사를 그냥 통과했지만, 실제로는 아래 1/4 가 비어 있었다.
    band = diff[CH["zones"][2][2]:CH["zones"][-1][2], :]            # 상단 라벨 위 ~ 하단 고정 위
    byr = np.where(band.any(1))[0]
    if len(byr):
        top, bot = int(byr[0]), band.shape[0] - 1 - int(byr[-1])
        if bot > top * 2.2 + 90:
            bad.append(f"내용이 위로 쏠렸어요(위 {top}, 아래 {bot} 비어 있음). "
                       f"규격의 '버튼·마무리' 구역에 행동 한 줄을 넣거나 내용을 고르게 펴세요.")

    # 글이 정월 위로 올라갔는지 — 그림 네모 안에서 밝은 글자 픽셀이 뭉쳐 있으면 겹친 것
    if c.get("face"):
        fh = int(H * c.get("face_h", .52)); fw = int(fh * 1086 / 1448)
        fx0, fy0 = W - c.get("face_right", 55) - fw, H - fh
        sub = a[fy0:fy0 + int(fh * .55), fx0:fx0 + fw]              # 그림 위쪽 절반(머리·얼굴)
        near_white = ((sub > 225).all(2)).sum()
        if near_white > sub.shape[0] * sub.shape[1] * 0.012:
            bad.append("글자가 정월 위로 올라간 것 같아요(그림 영역에 흰 글자 덩어리). 글 기둥을 그림 왼쪽까지로 줄이세요.")
    if bad:
        raise SystemExit("\n[결과물 검사에 걸렸어요] " + c.get("id", path) + "\n"
                         + "\n".join("  · " + x for x in bad) + "\n")
    return []


if __name__ == "__main__":
    print(__doc__)
