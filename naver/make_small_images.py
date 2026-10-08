"""본문 이미지 작은 판 만들기 (10/5 대표 요청: 이미지가 문서 너비로 크게 붙어서 손으로 줄이고 있다).
원본(가로 1280px)을 가로 IMG_W px로 줄여 naver/img/m640/<같은 파일명> 에 둔다. format_v2가 본문 이미지 주소를 이 작은 판으로 바꾼다.
CTA 배너(naver_cta*)는 링크 카드와 같은 가로 LINE_W px 판을 naver/img/m480/ 에 만든다. 다시 실행해도 같은 결과(이미 있고 최신이면 건너뜀).
사용: python3 make_small_images.py   (pages.json 본문에 나온 이미지만 만든다)"""
import os, re, json, urllib.parse
from PIL import Image
import format_v2 as V2
HERE = os.path.dirname(os.path.abspath(__file__)); IMG = os.path.join(HERE, "img"); OUT = os.path.join(IMG, V2.SMALL_DIR); OUT_CTA = OUT; os.makedirs(OUT, exist_ok=True); os.makedirs(OUT_CTA, exist_ok=True)
def main():
    pg = json.load(open(os.path.join(HERE, "pages.json"), encoding="utf-8")); names = set()
    for v in pg.values():
        if v.get("done") or "body" not in v: continue
        for m in re.finditer(r'<img[^>]*src="[^"]*/naver/img/([^"?]+)', v["body"]):
            n = urllib.parse.unquote(m.group(1))
            if "/" not in n: names.add(n)
    made = skipped = missing = 0
    for n in sorted(names):
        cta = "naver_cta" in n; src, dst = os.path.join(IMG, n), os.path.join(OUT_CTA if cta else OUT, n); W = V2.DELIV_W   # 10/8: 640이 아니라 1280(납품판). 새 이미지는 imgkit이 직접 만든다
        if not os.path.exists(src): missing += 1; print("원본 없음:", n); continue
        if os.path.exists(dst) and os.path.getmtime(dst) >= os.path.getmtime(src): skipped += 1; continue
        im = Image.open(src).convert("RGB")
        if im.width > W: im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
        im.save(dst, quality=88, optimize=True); made += 1
    tot = sum(os.path.getsize(os.path.join(d, f)) for d in (OUT, OUT_CTA) for f in os.listdir(d)) / 1e6
    print(f"작은 판 {made}개 만듦 · {skipped}개 건너뜀 · 원본 없음 {missing}개 · 폴더 합계 {tot:.1f}MB")
if __name__ == "__main__": main()
