"""자오선 메리디안 인트로 빌드: 원본(src)에서 가볍고 기기와 상관없이 같게 나오는 웹 인트로를 만든다.
 1) 차트 SVG의 글자(한자·별자리·숫자)를 도형(outline)으로 바꾼다 → 시스템 글꼴이 없어도 깨지지 않고 iOS에서 별자리가 이모지로 바뀌지 않는다
 2) 모바일용 차트(chart-m.svg): 선·글자를 더 굵고 진하게
 3) 글꼴: 이 페이지에 실제로 쓰인 글자만 담은 woff2 (제목 Noto Serif KR 900, 본문 Pretendard Variable). 문구를 고치면 `python3 build.py`로 다시 만든다
 4) 이미지는 WebP
 사용: python3 build.py [출력폴더]  (기본 out/)   필요: pip install fonttools brotli pillow
"""
import re, os, sys, shutil, base64, html as H
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.varLib import instancer
from fontTools import subset
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); SRC = os.path.join(HERE, "src"); OUT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.join(HERE, "out")
NOTO = os.environ.get("NOTO_SERIF_KR", "/tmp/NotoSerifKR-var.ttf")      # google/fonts ofl/notoserifkr/NotoSerifKR[wght].ttf
DEJAVU = os.path.join(SRC, "assets/fonts/DejaVuSans.ttf")
SAFE_TITLE = "자오선정월감정서사주운세별연애재물이름하루오늘무료풀이"            # 제목 글꼴에 미리 넣어 두는 브랜드 글자(문구를 조금 고쳐도 안 깨지게)

def outline_svg(svg, mobile=False):
    noto = instancer.instantiateVariableFont(TTFont(NOTO), {"wght": 400}); dj = TTFont(DEJAVU)
    def glyph(ch, size, x, y):
        f = dj if ord(ch) in range(0x2648, 0x2654) else noto
        gs = f.getGlyphSet(); name = f.getBestCmap()[ord(ch)]; upm = f["head"].unitsPerEm
        asc, desc = f["hhea"].ascent, f["hhea"].descent; s = size / upm
        adv = f["hmtx"][name][0]; pen = SVGPathPen(gs, ntos=lambda v: "%d" % round(v)); gs[name].draw(pen)
        k = 1.0
        if mobile: k = 1.28                                     # 모바일: 글자를 키운다(글자 중심 기준)
        s2 = s * k; cx, cy = x, y                                # 글자의 em 상자 중심이 (x,y)
        tx = cx - adv * s2 / 2; ty = cy + (asc + desc) / 2 * s2
        extra = f' stroke="#e7c88d" stroke-width="{1.7 / s2:.0f}" stroke-linejoin="round"' if mobile else ""
        return f'<path d="{pen.getCommands()}" transform="translate({tx:.1f} {ty:.1f}) scale({s2:.5f} {-s2:.5f})"{extra}/>'
    texts = re.findall(r'<text x="([\d.]+)" y="([\d.]+)" font-size="(\d+)">([^<])</text>', svg)
    paths = "".join(glyph(ch, int(sz), float(x), float(y)) for x, y, sz, ch in texts)
    m = re.search(r'<g fill="(#[0-9a-fA-F]+)" text-anchor', svg); fill = m.group(1); i = m.start()
    paths = paths.replace('stroke="#e7c88d"', f'stroke="{fill}"')
    return svg[:i] + f'<g fill="{fill}">' + paths + "</g></svg>", len(texts)

def thicken(svg):                                                # 모바일 차트: 선을 굵게·진하게
    svg = svg.replace('stroke="#d7b572" stroke-width="1.5"', 'stroke="#efd49a" stroke-width="3.6"')
    svg = re.sub(r'opacity="0\.(\d+)"', lambda m: 'opacity="%.2f"' % min(1, float("0." + m.group(1)) + 0.28), svg)
    svg = svg.replace('fill="#e7c88d"', 'fill="#f1d9a2"')
    return svg

def text_of(html_src):
    body = re.sub(r"<(style|script)[^>]*>.*?</\1>", "", html_src, flags=re.S)
    return "".join(re.findall(r">([^<>]+)<", body))

def make_font(src_path, out_path, chars, weight=None, wrange=None):
    f = TTFont(src_path)
    if weight is not None: f = instancer.instantiateVariableFont(f, {"wght": weight})
    elif wrange is not None: f = instancer.instantiateVariableFont(f, {"wght": wrange})
    opts = subset.Options(); opts.flavor = "woff2"; opts.layout_features = ["kern", "liga", "ccmp", "locl"]; opts.desubroutinize = True; opts.name_IDs = [1, 2, 3, 4, 6]
    sub = subset.Subsetter(opts); sub.populate(text=chars); sub.subset(f)
    f.flavor = "woff2"; f.save(out_path); return os.path.getsize(out_path)

def main():
    os.makedirs(OUT, exist_ok=True)
    for f in os.listdir(OUT):                              # 영상(video)·구도(compositions)는 따로 만든 파일이라 지우지 않는다
        if f not in ("video", "compositions"):
            q = os.path.join(OUT, f); shutil.rmtree(q) if os.path.isdir(q) else os.remove(q)
    os.makedirs(os.path.join(OUT, "assets/fonts"), exist_ok=True); shutil.copy(os.path.join(SRC, "README.txt"), os.path.join(OUT, "README.txt"))
    A = os.path.join(OUT, "assets"); svg = open(os.path.join(SRC, "assets/chart.svg"), encoding="utf-8").read()
    pc, n = outline_svg(svg); m, _ = outline_svg(thicken(svg), mobile=True)
    open(os.path.join(A, "chart.svg"), "w", encoding="utf-8").write(pc); open(os.path.join(A, "chart-m.svg"), "w", encoding="utf-8").write(m)
    print(f"차트 글자 {n}개를 도형으로: chart.svg {len(pc)//1024}KB, chart-m.svg {len(m)//1024}KB")
    Image.open(os.path.join(SRC, "assets/character.png")).save(os.path.join(A, "character.webp"), "WEBP", quality=84, method=6)
    Image.open(os.path.join(SRC, "assets/sky.png")).convert("RGB").save(os.path.join(A, "sky.webp"), "WEBP", quality=76, method=6)
    html_src = open(os.path.join(SRC, "index.html"), encoding="utf-8").read()
    title = "".join(re.findall(r"<h1[^>]*>([^<]*)</h1>", html_src)); body = text_of(html_src)
    t_chars = "".join(sorted(set(title + SAFE_TITLE))); b_chars = "".join(sorted(set(body + "".join(chr(c) for c in range(0x20, 0x7f)) + "·—·…’“”")))
    s1 = make_font(NOTO, os.path.join(A, "fonts/noto-serif-kr-900.woff2"), t_chars, weight=900)
    s2 = make_font(os.path.join(SRC, "assets/fonts/pretendard-variable.woff2"), os.path.join(A, "fonts/pretendard-variable-subset.woff2"), b_chars, wrange=(400, 700))
    print(f"글꼴: 제목 {len(t_chars)}자 {s1//1024}KB, 본문 {len(b_chars)}자 {s2//1024}KB")
    for f in os.listdir(os.path.join(SRC, "assets/fonts")):
        if f.endswith("LICENSE.txt"): shutil.copy(os.path.join(SRC, "assets/fonts", f), os.path.join(A, "fonts", f))
    h = html_src
    h = re.sub(r"@font-face\{font-family:\"Pretendard Variable\".*?\}\n@font-face.*?(?=\n\*\{)", '@font-face{font-family:"Pretendard Variable";font-weight:400 700;src:url("assets/fonts/pretendard-variable-subset.woff2") format("woff2");font-display:block}\n@font-face{font-family:"Noto Serif KR";font-style:normal;font-weight:900;src:url("assets/fonts/noto-serif-kr-900.woff2") format("woff2");font-display:block}', h, flags=re.S)
    h = h.replace('src="assets/sky.png"', 'src="assets/sky.webp"').replace('src="assets/character.png"', 'src="assets/character.webp"')
    h = h.replace('<img src="assets/chart.svg" alt="', '<picture><source media="(max-width:650px)" srcset="assets/chart-m.svg"><img src="assets/chart.svg" alt="').replace('큰 원형 차트"', '큰 원형 차트"')
    h = re.sub(r'(<picture><source[^>]*><img src="assets/chart.svg" alt="[^"]*">)', r"\1</picture>", h)
    open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(h)
    # 영상용 세로 배치(reel.html): 같은 글꼴·이미지, 버튼 없음, 앱 화면 안전 영역 안쪽 배치
    r = open(os.path.join(SRC, "reel.html"), encoding="utf-8").read()
    r = re.sub(r"@font-face\{font-family:\"Pretendard Variable\".*?\}\n@font-face.*?(?=\n\*\{)", '@font-face{font-family:"Pretendard Variable";font-weight:400 700;src:url("assets/fonts/pretendard-variable-subset.woff2") format("woff2");font-display:block}\n@font-face{font-family:"Noto Serif KR";font-style:normal;font-weight:900;src:url("assets/fonts/noto-serif-kr-900.woff2") format("woff2");font-display:block}', r, flags=re.S)
    r = r.replace('src="assets/sky.png"', 'src="assets/sky.webp"').replace('src="assets/character.png"', 'src="assets/character.webp"')
    open(os.path.join(OUT, "reel.html"), "w", encoding="utf-8").write(r)
    # 단독 파일(모두 내장)
    def b64(p, mime): return f"data:{mime};base64," + base64.b64encode(open(os.path.join(OUT, p), "rb").read()).decode()
    s = h
    for p, mime in [("assets/fonts/pretendard-variable-subset.woff2", "font/woff2"), ("assets/fonts/noto-serif-kr-900.woff2", "font/woff2"), ("assets/sky.webp", "image/webp"), ("assets/character.webp", "image/webp"), ("assets/chart-m.svg", "image/svg+xml"), ("assets/chart.svg", "image/svg+xml")]:
        s = s.replace(p, b64(p, mime))
    open(os.path.join(OUT, "meridian_intro_standalone.html"), "w", encoding="utf-8").write(s)
    tot = sum(os.path.getsize(os.path.join(dp, f)) for dp, _, fs in os.walk(OUT) for f in fs if not f.endswith("standalone.html"))
    print(f"출력 {OUT}: index.html + assets 합계 {tot//1024}KB, 단독 파일 {os.path.getsize(os.path.join(OUT,'meridian_intro_standalone.html'))//1024}KB")
if __name__ == "__main__": main()
