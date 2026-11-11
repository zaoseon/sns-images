"""한 채널용으로 만든 영상 장면을 다른 채널 데드존에 맞게 자동으로 옮긴다(11/11 대표 "콘텐츠별로 자동 조정").
방법: ① 원래 채널(보통 reel)로 고정 요소 없이 찍는다 ② 원래 '글 칸'을 새 채널 '글 칸'에 맞게 같은 비율로 줄이거나 키워 가운데 놓는다
③ 바깥은 원래 화면(배경)을 그대로 두고 경계는 부드럽게 섞는다 ④ 새 채널 고정 요소(F.frame)를 새 자리에 얹는다.
값은 모두 channel_specs.py 에서 읽는다. 비율이 다른 채널(9:16 → 16:9)은 옮기지 않는다(장면을 새로 짠다)."""
import os, sys, json, tempfile
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import channel_specs as CS
from PIL import Image, ImageFilter, ImageDraw


def 글칸(ch):
    C = CS.CH[ch]; z = {r[0]: r[1:5] for r in C["zones"]}
    return (C["safe"][0], z["상단 고정"][3] + 10, C["safe"][2], z["하단 고정"][1] - 10)


def 옮길수있나(src, dst):
    a, b = CS.CH[src], CS.CH[dst]
    return (a["w"], a["h"]) == (b["w"], b["h"]) and "상단 고정" in {z[0] for z in b["zones"]}


def 행렬(src, dst):
    """원래 글 칸 → 새 글 칸: 배율 k, 원래 칸, 새 자리 (x, y)."""
    s, d = 글칸(src), 글칸(dst)
    sw, sh, dw, dh = s[2] - s[0], s[3] - s[1], d[2] - d[0], d[3] - d[1]
    k = min(dw / sw, dh / sh, 1.0)
    nw, nh = round(sw * k), round(sh * k)
    return k, s, ((d[0] + d[2]) // 2 - nw // 2, (d[1] + d[3]) // 2 - nh // 2), (nw, nh)


def 고정판(dst, opt, 브랜드):
    """새 채널 고정 요소만 그린 투명 PNG(F.frame 그대로)."""
    from playwright.sync_api import sync_playwright
    C = CS.CH[dst]; z = {r[0]: list(r[1:5]) for r in C["zones"]}
    spec = dict(safe=list(C["safe"]), top=z["상단 고정"], bottom=z["하단 고정"])
    js = os.path.join(HERE, "motion_fx.js")
    html = (f"<html><body style='margin:0;background:transparent'><canvas id=c width={C['w']} height={C['h']}></canvas>"
            f"<script>window.ZS_SPEC={json.dumps(spec)};window.ZS_BRAND={json.dumps(브랜드, ensure_ascii=False)};</script>"
            f"<script src='file://{js}'></script><script>document.fonts.ready.then(()=>setTimeout(()=>{{const g=c.getContext('2d');"
            f"FXK.frame(g,{json.dumps(opt or {}, ensure_ascii=False)});window.done=1}},300))</script></body></html>")
    f = tempfile.mktemp(suffix=".html", dir=HERE); open(f, "w", encoding="utf-8").write(html)
    out = tempfile.mktemp(suffix=".png")
    try:
        with sync_playwright() as pw:
            b = pw.chromium.launch(); pg = b.new_page(viewport={"width": C["w"], "height": C["h"]})
            pg.goto("file://" + f); pg.wait_for_function("window.done===1", timeout=15000)
            pg.locator("#c").screenshot(path=out, omit_background=True); b.close()
    finally:
        os.remove(f)
    return Image.open(out).convert("RGBA")


def 옮기기(png, src, dst, 판, M=None):
    """프레임 한 장을 새 채널로. 판 = 고정판() 결과."""
    k, s, (x, y), (nw, nh) = M or 행렬(src, dst)
    im = Image.open(png).convert("RGBA"); W, H = im.size
    # 화면 전체를 같은 배율로 줄여 글 칸이 새 자리에 오게 놓고, 생긴 가장자리 틈은 흐린 원래 화면(배경색)으로 채운다.
    # (글 칸만 잘라 붙이면 칸 밖 원래 글·그림 조각이 가장자리에 비친다 — 11/11 확인 컷)
    out = im.filter(ImageFilter.GaussianBlur(40))
    if k < 0.999 or (x, y) != (s[0], s[1]):
        fw, fh = round(W * k), round(H * k); ox, oy = round(x - s[0] * k), round(y - s[1] * k)
        sm = im.resize((fw, fh), Image.LANCZOS).crop((max(-ox, 0), max(-oy, 0), fw, fh))
        out.alpha_composite(sm, (max(ox, 0), max(oy, 0)))
    else:
        out = im.copy()
    out.alpha_composite(판)
    out.convert("RGB").save(png)
