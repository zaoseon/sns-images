"""채널별 데드존 가이드 템플릿 — channel_specs.py 값으로 그린다(손으로 그린 판이 아니다).
11/11 대표 "채널별 콘텐츠 데드존 가이드 템플릿을 만들어서 콘텐츠별로 자동 조정 가능하게".
근거 수치: MP 유튜브·릴스·쇼츠 데드존 무료 가이드라인(대표 첨부) + 우리 캡처 실측. 값은 channel_specs.DZ_* 에만 둔다.

  python3 pipeline/deadzone_guide.py              → assets/deadzone/<채널>.png (투명 판) + templates.json(모든 채널 값, 다른 도구용)
  채널: 릴스 reel · 네이버 클립 naver_clip · 쇼츠 youtube_shorts · 유튜브 youtube · 캐러셀 insta_carousel
        · 블로그 섬네일 naver_blog_thumb · 블로그 본문 이미지 naver_blog_body · 사이트 섬네일 site_blog_thumb · CTA 배너 naver_cta_banner(6)
  python3 pipeline/deadzone_guide.py 그림.png reel → 그림 위에 얹은 확인 그림(<그림>_데드존_reel.png)
코드에서: overlay(PIL 이미지, "youtube_shorts") → 얹은 이미지.
색: 빨강 빗금=UI가 덮음(글·얼굴 금지) · 노랑 빗금=제목·로고 띠(고정 요소만) · 주황 점선=기종에 따라 덮임 · 초록 선=안전 영역 · 하늘 점선=구역."""
import os, sys
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import channel_specs as CS

COL = dict(ui=(229, 57, 53), band=(255, 193, 7), caution=(255, 112, 0))


def _font(px):
    for f in ("PRETENDARD-BOLD.OTF", "PRETENDARD-SEMIBOLD.OTF"):
        p = os.path.join(HERE, "fonts", f)
        if os.path.exists(p): return ImageFont.truetype(p, px)
    return ImageFont.load_default()


def _hatch(d, box, rgb, a, step=22, width=6):
    x0, y0, x1, y1 = box
    for k in range(-(y1 - y0), x1 - x0, step):
        d.line([(x0 + k, y1), (x0 + k + (y1 - y0), y0)], fill=rgb + (a,), width=width)


def guide(ch, labels=True):
    """채널 하나의 데드존 판(RGBA, 안전 영역은 투명)."""
    C = CS.CH[ch]; w, h = C["w"], C["h"]
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    for kind, box, why in C.get("deadzone", []):
        lay = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
        x0, y0, x1, y1 = box
        if kind == "ui":
            d.rectangle(box, fill=COL["ui"] + (70,)); _hatch(d, box, COL["ui"], 120)
        elif kind == "band":
            _hatch(d, box, COL["band"], 95, step=30, width=4)
        else:
            d.rectangle(box, fill=COL["caution"] + (45,)); _hatch(d, box, COL["caution"], 90, step=34, width=4)
            for x in range(x0, x1, 28): d.line([(x, y0), (x + 14, y0)], fill=COL["caution"] + (230,), width=4)
        lay = Image.alpha_composite(Image.new("RGBA", (w, h), (0, 0, 0, 0)), lay)
        mask = Image.new("L", (w, h), 0); ImageDraw.Draw(mask).rectangle(box, fill=255)
        im.paste(Image.alpha_composite(im, lay), (0, 0), mask)
    d = ImageDraw.Draw(im); f = _font(26 if w < 1500 else 30)
    d.rectangle(C["safe"], outline=(46, 189, 107, 255), width=5)
    for z in C.get("zones", []):
        n, x0, y0, x1, y1 = z[:5]
        if n == "마무리 카드": continue
        for x in range(x0, x1, 24): d.line([(x, y0), (x + 12, y0)], fill=(79, 195, 247, 230), width=3); d.line([(x, y1), (x + 12, y1)], fill=(79, 195, 247, 230), width=3)
        if labels: d.text((x0 + 10, y0 + 4), n, font=f, fill=(79, 195, 247, 255), stroke_width=3, stroke_fill=(0, 0, 0, 200))
    if labels:
        d.text((C["safe"][0] + 10, C["safe"][3] - 40), f"{C['name']} {w}x{h} · 안전 {C['safe']}", font=f, fill=(46, 189, 107, 255), stroke_width=3, stroke_fill=(0, 0, 0, 200))
    return im


def overlay(img, ch, labels=True):
    """화면 그림 위에 데드존 판을 얹는다. 크기가 다르면 판을 그림 크기로 맞춘다."""
    g = guide(ch, labels)
    base = img.convert("RGBA")
    if base.size != g.size: g = g.resize(base.size)
    return Image.alpha_composite(base, g)


def main():
    a = sys.argv[1:]
    if a and os.path.exists(a[0]):
        ch = a[1] if len(a) > 1 else "reel"; out = os.path.splitext(a[0])[0] + f"_데드존_{ch}.png"
        overlay(Image.open(a[0]), ch).convert("RGB").save(out); print(out); return 0
    od = os.path.join(ROOT, "assets", "deadzone"); os.makedirs(od, exist_ok=True)
    print(CS.export(os.path.join(od, "templates.json")))
    for ch, C in CS.CH.items():
        if not C.get("deadzone"): continue
        p = os.path.join(od, f"{ch}.png"); guide(ch).save(p); print(p)
    return 0


if __name__ == "__main__":
    sys.exit(main())
