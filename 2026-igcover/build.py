"""인스타·스레드 표지를 '단색 판 + 흰 글자'로 만든다 (대표 10/16).

10/16 1판을 버리고 다시 짠 것. 1판은 네이버 표지 틀(naver/cover_v3.py)을 인스타에
가져다 써서 채널 규격을 통째로 어겼다 — 상단·하단 고정 요소 없음, 글꼴 프리텐다드(카드 제목은
페이퍼로지), 여백 임의값, 색은 문서 안 읽고 id 만 보고 고름, 밝은 단색 위 정월 누끼가 지저분.

이 판이 읽는 곳 (전부 이미 있던 것):
  pipeline/channel_specs.py  안전 영역·구역·글꼴 크기 (insta_carousel: safe 55,55,1025,1385)
  pipeline/brand_frame.py    상단 좌 자오선 · 상단 우 동서양 6개 운명학 교차분석 ·
                             하단 우 zaoseon.com · 하단 좌 AI 고지(정월이 나올 때만)
  pipeline/fonts_kit.py      JW-D 제목(페이퍼로지 ExtraBold·Black) · JW-B 본문(프리텐다드 800)
  assets/palettes/color_combos.json   판(K-059 역할·비율, K-068 연속 금지)

대표가 정한 것 (10/16):
  - 단색 판에 흰 글자. 검정 글자는 칙칙해 보인다.
  - 정월 누끼는 밝은 판 위에 놓지 않는다. 가장자리가 지저분하다. 어두운 판에만.
  - 정월은 '말하는 글'(모집·공지·인사)에만 전면. 정보 글 표지에는 없다. (K-061)
  - 어두운 판은 6편에 1편 이하. (K-060)

사용: python3 2026-igcover/build.py [id ...]
"""
import os, sys, json, base64, asyncio

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(ROOT, "pipeline"))
import fonts_kit as K, brand_frame as BF, channel_specs as CS, card_gate as G

OUT = os.path.join(HERE, "cards")
SPEC = os.path.join(HERE, "cards.json")
CH = CS.CH["insta_carousel"]
SX0, SY0, SX1, SY1 = CH["safe"]                      # 55, 55, 1025, 1385
W, H = CH["w"], CH["h"]                              # 1080 x 1440
Z = {z[0]: z[1:5] for z in CH["zones"]}              # 구역 이름 -> (x0,y0,x1,y1)


def palettes():
    d = json.load(open(os.path.join(ROOT, "assets", "palettes", "color_combos.json"), encoding="utf-8"))
    return {p["id"]: p for p in d["palettes"]}


def lum(hx):
    r, g, b = (int(hx[i:i + 2], 16) / 255 for i in (1, 3, 5))
    f = lambda c: c / 12.92 if c <= .04045 else ((c + .055) / 1.055) ** 2.4
    return .2126 * f(r) + .7152 * f(g) + .0722 * f(b)


def contrast(a, b):
    la, lb = lum(a), lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + .05) / (lo + .05)


def b64(p):
    return base64.b64encode(open(p, "rb").read()).decode()


def page(c, pal):
    """단색 판 한 장. 글자는 모두 안전 영역 안, 구역을 따른다."""
    cols = list(pal["colors"].values())
    bg = c.get("bg") or cols[0]                       # 메인 색을 꽉 찬 판으로 (K-068 _s 판)
    acc = c.get("acc") or cols[1]
    dark = lum(bg) < 0.38
    fg = "#ffffff" if dark else "#141414"             # 대표: 가독성 되면 흰 글자. 밝은 판에서는 흰 글자가 안 읽힌다
    if contrast(fg, bg) < 4.5:                        # 안 되면 반대로
        fg = "#141414" if fg == "#ffffff" else "#ffffff"
    sub_c = acc if contrast(acc, bg) >= 3.0 else fg

    tz = Z["제목"]; bz = Z["본문·선택지"]
    LY0 = c.get("layout", "L1")
    align = "left" if LY0 in ("L8", "L5", "L9") else "center"   # 승인본(_a4)은 가운데가 기본, 목록형만 왼쪽
    band = ""
    if LY0 == "L4":                                   # 하단 띠형 — 위는 그림, 아래 띠에 글
        bh = c.get("band_h", 700)
        band_bg = c.get("band_bg") or acc
        band = (f'<div style="position:absolute;left:0;right:0;bottom:0;height:{bh}px;'
                f'background:{band_bg};z-index:3"></div>')
        tz = (tz[0], H - bh + 56, tz[2], H - bh + 56 + 230)
        bz = (bz[0], tz[3] + 6, bz[2], H - 210)
        # 띠 위에 올라가는 글은 띠 색을 기준으로 정한다. 바탕 기준으로 두면 흰 글자가 밝은 띠에 얹힌다(10/16).
        fg = "#ffffff" if lum(band_bg) < .38 else "#141414"
        sub_c = bg if contrast(bg, band_bg) >= 3.0 else fg
    tone = "light" if lum(bg) >= .38 else "dark"
    parts = []

    # 정월이 있으면 그림이 차지하는 네모를 먼저 잡는다. 글은 그 안으로 들어가지 않는다.
    face_left, face_top = W, H
    if c.get("face"):
        fh = int(H * c.get("face_h", 0.52))
        fw = int(fh * 1086 / 1448)                    # 컷 비율
        face_left = W - c.get("face_right", 55) - fw
        face_bottom = H - (c.get("band_h", 700) if LY0 == "L4" else 0)   # L4 는 띠 위에 앉힌다
        face_top = face_bottom - fh
    GUT = 36                                          # 글과 그림 사이 최소 간격

    # 라벨(배지) — 글자는 배지 안에서 가운데. 34px 이상(채널 규격)
    lz = Z["상단 라벨"]
    parts.append(
        f'<div style="position:absolute;left:0;right:0;top:{lz[1]}px;height:{lz[3]-lz[1]}px;'
        f'display:flex;align-items:center;justify-content:center;'
        f'"><span style="display:inline-flex;align-items:center;justify-content:center;height:100%;'
        f'padding:0 34px;border-radius:999px;background:{acc};color:{"#141414" if lum(acc)>.38 else "#fff"};'
        f'font-family:{K.B};font-weight:800;font-size:38px;line-height:1">{c["kick"]}</span></div>')

    # 제목 — 페이퍼로지 84~112px, 의미 단위로 미리 끊어 둔 줄을 그대로 쓴다
    ts = c.get("title_size", 104)
    parts.append(
        f'<div style="position:absolute;left:{tz[0]}px;top:{tz[1]}px;width:{tz[2]-tz[0]}px;'
        f'font-family:{K.D};font-weight:900;font-size:{ts}px;line-height:1.32;color:{fg};text-align:{align}">'
        + "<br>".join(c["hook"]) + "</div>")

    LY = LY0
    if LY == "L4":
        band_c = c.get("band_bg") or acc
        fg = "#ffffff" if lum(band_c) < .38 else "#141414"
        sub_c = bg if contrast(bg, band_c) >= 3.0 else fg                        # sns-studio/templates/layouts.css · SKILL.md 의 주제별 표를 따른다

    def 폭(y_top, y_bot):
        """그 높이에서 글이 쓸 수 있는 폭. 정월과 겹치는 높이면 그림 왼쪽까지만."""
        right = bz[2]
        if y_bot > face_top:
            right = min(right, face_left - GUT)
        return max(200, right - bz[0])

    # 본문 덩어리를 먼저 쌓아 높이를 재고, 본문 구역 안에서 세로 가운데에 놓는다(아래가 휑하지 않게)
    블록 = []
    if c.get("big"):
        bs = c.get("big_size", 240)
        블록.append(("big", c["big"], bs, int(bs * 1.05), 30))
    if c.get("items"):
        블록.append(("items" if LY != "L8" else "numlist", c["items"], 0,
                     118 if LY != "L8" else 96 * len(c["items"]) + 30 * (len(c["items"]) - 1), 30))
    for l in c.get("subs", []):
        블록.append(("sub", l, 46, 69, 0))
    총높이 = sum(b[3] + b[4] for b in 블록) - (블록[-1][4] if 블록 else 0)
    y = bz[1] + max(0, ((bz[3] - bz[1]) - 총높이) // 3)   # 위쪽으로 조금 치우치게(1/3 지점)

    for kind, val, size, hgt, gap in 블록:
        wmax = 폭(y, y + hgt)
        if kind == "big":
            s = size
            while s * 0.62 * len(val) > wmax and s > 110: s -= 6    # 그림 위로 넘지 않게
            parts.append(f'<div style="position:absolute;left:{bz[0]}px;top:{y}px;width:{wmax}px;'
                         f'font-family:{K.D};font-weight:900;font-size:{s}px;line-height:1.05;'
                         f'color:{sub_c};white-space:nowrap;text-align:{align}">{val}</div>')
        elif kind == "numlist":                       # L8 번호 리스트형 — 저장을 부른다
            rows = "".join(
                f'<div style="display:flex;gap:26px;align-items:center;height:96px">'
                f'<div style="flex:0 0 72px;height:72px;border-radius:999px;background:{sub_c};'
                f'color:{"#141414" if lum(sub_c)>.38 else "#fff"};font-family:{K.D};font-weight:900;'
                f'font-size:44px;display:flex;align-items:center;justify-content:center">{i+1}</div>'
                f'<div style="font-family:{K.B};font-weight:800;font-size:54px;color:{fg};'
                f'line-height:1.3;white-space:nowrap">{t}</div></div>' for i, t in enumerate(val))
            parts.append(f'<div style="position:absolute;left:{bz[0]}px;top:{y}px;width:{wmax}px;'
                         f'display:flex;flex-direction:column;gap:30px">{rows}</div>')
        elif kind == "items":
            n = len(val); g = 18
            cw = (wmax - g * (n - 1)) // n
            mx = max(len(t) for t in val)
            fs = max(34, min(46, int(cw * 0.90 / mx)))              # 칩 글자는 상자 안에 한 줄로(터지면 두 줄이 된다)
            row = "".join(
                f'<div style="width:{cw}px;height:112px;display:flex;align-items:center;justify-content:center;'
                f'border:4px solid {fg}55;border-radius:26px;font-family:{K.B};font-weight:800;'
                f'font-size:{fs}px;color:{fg};box-sizing:border-box;white-space:nowrap">{t}</div>' for t in val)
            parts.append(f'<div style="position:absolute;left:{bz[0]}px;top:{y}px;width:{wmax}px;'
                         f'display:flex;gap:{g}px">{row}</div>')
        else:
            s = size
            while s * 0.52 * len(val) > wmax and s > 36: s -= 2     # 본문도 기둥 안에서 한 줄로
            if s * 0.52 * len(val) > wmax:                           # 더 줄이면 안 읽힌다 — 멈추고 알린다
                raise SystemExit(f"\n[막음] {c['id']}: 본문 \"{val}\" 이 기둥({wmax}px)에 36px 로도 안 들어가요.\n"
                                 f"  글을 줄이거나, 정월을 작게 하거나, 레이아웃을 바꾸세요.\n")
            parts.append(f'<div style="position:absolute;left:{bz[0]}px;top:{y}px;width:{wmax}px;'
                         f'font-family:{K.B};font-weight:800;font-size:{s}px;line-height:1.5;'
                         f'color:{fg};opacity:.92;white-space:nowrap;text-align:{align}">{val}</div>')
        y += hgt + gap

    if c.get("cta"):                                  # 규격의 '버튼·마무리' 구역 — 행동 한 줄
        cz = Z["버튼·마무리"]
        if LY0 == "L4": cz = (cz[0], H - 190, cz[2], H - 110)
        parts.append(f'<div style="position:absolute;left:{cz[0]}px;top:{cz[1]}px;width:{폭(cz[1], cz[3])}px;'
                     f'height:{cz[3]-cz[1]}px;display:flex;align-items:center;'
                     f'font-family:{K.B};font-weight:800;font-size:42px;color:{fg};opacity:.75;white-space:nowrap;'
                     f'justify-content:{"center" if align=="center" else "flex-start"}">{c["cta"]}</div>')

    face = ""
    if c.get("face"):                                 # 정월 — 어두운 판에만(밝은 판에서 누끼 가장자리가 보인다)
        if not dark:
            raise SystemExit(f"[막음] {c['id']}: 밝은 판({bg})에 정월을 놓으려 합니다. 누끼 가장자리가 지저분해집니다. 어두운 판을 쓰세요.")
        fp = os.path.join(ROOT, "characters", "cut_light", c["face"] + ".png")
        face = (f'<img src="data:image/png;base64,{b64(fp)}" style="position:absolute;right:{c.get("face_right",-60)}px;'
                f'bottom:{H-face_bottom}px;height:{fh}px;z-index:2">')

    inner = face + band + "".join(f'<div style="z-index:5;position:absolute;inset:0">{p}</div>' for p in parts)
    return (f'<html><head><meta charset="utf-8"><style>{K.css(c.get("display","pl"))}{BF.css(tone)}</style></head>'
            f'<body style="margin:0;width:{W}px;height:{H}px;position:relative;overflow:hidden;background:{bg};'
            f'color:{fg};word-break:keep-all;line-break:strict">'
            + inner + BF.html("card", ai=bool(c.get("face")), tone=tone) + "</body></html>")


async def shoot(pages):
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        br = await p.chromium.launch(args=["--allow-file-access-from-files", "--font-render-hinting=none"])
        pg = await br.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
        for cid, html in pages:
            await pg.set_content(html, wait_until="load")
            await pg.evaluate("document.fonts.ready")
            await pg.screenshot(path=os.path.join(OUT, cid + ".jpg"), quality=94, type="jpeg")
            print(f"  {cid}")
        await br.close()


def main():
    os.makedirs(OUT, exist_ok=True)
    PAL = palettes()
    spec = json.load(open(SPEC, encoding="utf-8"))
    want = sys.argv[1:]
    pages, 쓴판, 쓴컷, 쓴틀 = [], [], [], []
    for c in spec["cards"]:                           # 관문이 먼저다 — 한 장이라도 걸리면 아무것도 안 그린다
        G.before(c, channel="insta_carousel", prev=쓴판, prev_faces=쓴컷, prev_layouts=쓴틀)
        쓴판.append(c["pal"])
        if c.get("face"): 쓴컷.append(c["face"])
        쓴틀.append(c.get("layout"))
    print("관문 통과 ✓ (판·대비·정월·글꼴 크기·입말·훅 유형·연속 금지)\n")
    for c in spec["cards"]:
        if want and c["id"] not in want:
            continue
        pages.append((c["id"], page(c, PAL[c["pal"]])))
    asyncio.run(shoot(pages))
    print()
    for c in spec["cards"]:                           # 그린 뒤 결과물을 숫자로
        if want and c["id"] not in want:
            continue
        G.after(os.path.join(OUT, c["id"] + ".jpg"), c, channel="insta_carousel")
    print(f"결과물 검사 통과 ✓ · {len(pages)}장")


if __name__ == "__main__":
    main()
