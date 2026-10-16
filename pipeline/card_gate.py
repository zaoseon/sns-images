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
글말 = ["타고난 결", "~하는 결", "결이 맞", "두 겹으로", "~에 대해", "~을 통해", "~에 있어",
        "세 지도", "세 가지 지도"]   # 세 지도 -> 사주·별자리·숫자 (대표 10/16)
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


def before(c, channel="insta_carousel", prev=None, prev_faces=None, prev_layouts=None):
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
        if c.get("accent") and c["accent"] != "하단배지":
            모든색 = {v.upper() for q in P.values() for v in (q.get("colors") or {}).values()}
            모든색 |= {v.upper() for q in P.values() for v in (q.get("theme") or {}).values() if isinstance(v, str) and v.startswith("#")}
            if c["accent"].upper() not in 모든색:
                bad.append(f"강조색 {c['accent']} 가 승인된 판 어디에도 없어요. color_combos.json 에서 고르세요.")
            elif c["accent"].upper() not in 쓸수있는색 and not c.get("강조색 까닭"):
                bad.append(f"강조색 {c['accent']} 는 판 '{c['pal']}' 밖의 색이에요. 섞는 까닭을 \"강조색 까닭\" 에 적으세요.")
        for k in ("bg", "acc"):
            if c.get(k) and c[k].upper() not in 쓸수있는색:
                bad.append(f"{k} {c[k]} 가 판 '{c['pal']}' 의 색이 아니에요. 판 안의 색만 쓰세요(섞지 않기).")

    # 2. 글자 색 대비 — 단색 판 + 흰 글자가 기본(대표 10/16), 안 되면 멈춘다
    for _k, _sz in (("accent", c.get("kick_size", 68)), ("big_color", c.get("big_size", 240))):
        if c.get(_k) and c[_k].startswith("#") and c.get("bg"):
            _need = 3.0 if _sz >= 60 else 4.5      # WCAG: 큰 글자는 3.0
            if contrast(c[_k], c["bg"]) < _need:
                bad.append(f"{_k} {c[_k]} 가 바탕 {c['bg']} 에서 대비 {contrast(c[_k], c['bg']):.1f}:1 이라 안 보여요({_need} 이상).")
    if c.get("bg"):
        fg = "#FFFFFF" if lum(c["bg"]) < .38 else "#141414"
        if contrast(fg, c["bg"]) < 4.5:
            bad.append(f"바탕 {c['bg']} 에서는 글자 대비가 {contrast(fg, c['bg']):.1f}:1 이라 안 읽혀요(4.5 이상 필요).")

    # 3. 정월 (K-061) — '말하는 글'에만, 어두운 판에만, 같은 컷을 돌려쓰지 않기
    if c.get("face"):
        try:
            B = json.load(open(os.path.join(ROOT, "sns-studio", "brands", "zaoseon.json"), encoding="utf-8"))
            ch = B.get("character", {})
            if c["face"] + ".png" in ch.get("forbidden", []):
                bad.append(f"컷 '{c['face']}' 은 쓰지 않기로 했어요 — {ch.get('금지 까닭','')}")
            if prev_faces and c["face"] in list(prev_faces)[-5:]:
                bad.append(f"컷 '{c['face']}' 을 앞 5편 안에서 이미 썼어요. {ch.get('rotate',[])[:4]} 중에서 고르세요.")
        except Exception:
            pass
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
    줄 = (list(c.get("hook", [])) + list(c.get("subs", [])) + [c.get("kick", ""), c.get("cta", "")]
         + list(c.get("serial", [])) + list(c.get("items", [])))
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

    # 7. 쌓은 높이가 구역을 넘는가 — 넘치면 글끼리 겹친다(10/16 L4 띠에서 났다)
    CH2 = CS.CH[channel]
    ZZ = {z[0]: z[1:5] for z in CH2["zones"]}
    LY = c.get("layout", "L1")
    if LY == "L4":
        bh = c.get("band_h", 700)
        쓸높이 = bh - 56 - 230 - 6 - 210               # 띠 - 윗여백 - 제목 - 사이 - 마무리·고정
    else:
        쓸높이 = ZZ["본문·선택지"][3] - ZZ["본문·선택지"][1]
    필요 = 0
    if c.get("big"): 필요 += int(c.get("big_size", 240) * 1.05) + 30
    if c.get("items"):
        필요 += (90 * len(c["items"]) + 26 * (len(c["items"]) - 1) + 30) if LY == "L8" else 148
    필요 += int(c.get("sub_size", 56) * 1.5) * len(c.get("subs", []))
    if 필요 > 쓸높이:
        bad.append(f"본문이 {필요}px 인데 들어갈 자리는 {쓸높이}px 이에요. 글끼리 겹칩니다 — "
                   f"줄을 줄이거나 큰 숫자를 작게 하거나 띠를 키우세요.")

    # 8-1. 배지 (가이드라인 6-1절, 대표 10/16 "배지 안에 텍스트 배치와 텍스트 크기")
    #      배지를 넣을지는 글에 따라 가변이다. 넣을 때 안을 어떻게 채우느냐가 규칙이다.
    if c.get("kick"):
        lab_lo = 범위(fonts["label"])[0]
        ks = c.get("kick_size", 68)
        if ks < lab_lo:
            bad.append(f"배지 글자 {ks}px 가 라벨 규격({fonts['label']}) 아래예요. "
                       f"작게 줄이지 말고 배지를 키우거나 글자 수를 줄이세요.")
        lz = {z[0]: z[1:5] for z in CS.CH[channel]["zones"]}.get("상단 라벨")
        위고정 = max((z[4] for z in CS.CH[channel]["zones"] if "상단" in z[0] and "고정" in z[0]), default=0)  # z=(이름,x0,y0,x1,y1)
        if lz and lz[1] < 위고정 + 60:
            bad.append(f"배지가 상단 고정 문구와 {lz[1]-위고정}px 밖에 안 떨어졌어요(60px 이상). "
                       f"channel_specs 의 '상단 라벨' 구역을 내리세요.")
        if len(str(c["kick"])) > 12:
            bad.append(f"배지 글자가 {len(str(c['kick']))}자예요. 한 줄에 안 들어가면 두 줄로 터집니다(12자 이내).")

    # 8-2. 본문 글자 크기 — 채널 규격 아래로 못 내려간다(가이드라인 2절)
    body_lo = 범위(fonts["body"])[0]
    if c.get("cta"):                                  # CTA 도 '너무 작은 글자 금지' 를 받는다(대표 10/16)
        if c.get("cta_size", 58) < 52:
            bad.append(f"CTA 글자 {c.get('cta_size')}px 는 작아요(52px 이상). 글을 줄이고 크기를 지키세요.")
    if c.get("subs") and c.get("sub_size", 46) < body_lo:
        bad.append(f"본문 {c.get('sub_size', 46)}px 가 채널 규격({fonts['body']}) 아래예요.")

    # 9. 레이아웃 — 주제표에서 고르고, 앞 5편과 다르게 (K-077)
    if not c.get("layout"):
        bad.append("레이아웃을 사양에 적으세요(L1~L12). sns-studio/SKILL.md 의 주제·유형 표에서 고릅니다.")
    elif prev_layouts and c["layout"] in list(prev_layouts)[-3:]:
        bad.append(f"레이아웃 '{c['layout']}' 을 앞 3편 안에서 이미 썼어요(K-077). 주제표에서 다른 것을 고르세요.")

    # 10. 연속 금지 (K-068) — 앞 5편과 같은 판 금지
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
        LY = c.get("layout", "L1")
        가장자리허용 = LY in ("L3", "L4") or "M1" in c.get("method", "")   # 띠형·배경 이미지형(M1)은 일부러 가장자리까지 간다
        if not 가장자리허용 and (l < sx0 - 2 or r < (W - sx1) - 2 or t < sy0 - 2):
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

    # 글과 그림 겹침은 픽셀로 짐작하지 않는다 — 정월 얼굴 하이라이트를 글자로 오인했다(10/16).
    # 그리는 쪽이 글 기둥을 face_left - 간격 으로 자르고, 줄일 수 있는 한계에 닿으면 스스로 멈춘다.

    # 세로 배치 — 구역에서 계산한다. 옛 R47 의 "묶음 y183~1265"는 '버튼·마무리' 구역(1240~1340)이
    # 생기기 전 값이라 서로 부딪혔다. 단일 출처는 channel_specs 이므로 구역으로 잰다(가이드라인 0절).
    if len(ys) and "M1" not in c.get("method", ""):
        z = {x[0]: x[1:5] for x in CH["zones"]}
        위 = min(v[1] for k, v in z.items() if "고정" not in k)
        아래 = max(v[3] for k, v in z.items() if "고정" not in k)
        b2 = diff[위:아래, :]; yy = np.where(b2.any(1))[0]
        if len(yy):
            t2, b3 = 위 + int(yy[0]), 위 + int(yy[-1])
            가, 목표 = (t2 + b3) // 2, (위 + 아래) // 2
            if b3 > 아래 + 8:
                bad.append(f"묶음 맨 아래가 {b3} 예요(구역 끝 {아래}).")
            if abs(가 - 목표) > 24:
                bad.append(f"묶음 세로 가운데가 {가} 예요(구역 가운데 {목표} ±24). 위아래가 치우쳤어요.")

    if bad:
        raise SystemExit("\n[결과물 검사에 걸렸어요] " + c.get("id", path) + "\n"
                         + "\n".join("  · " + x for x in bad) + "\n")
    return []


if __name__ == "__main__":
    print(__doc__)
