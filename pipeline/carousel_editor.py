"""캐러셀을 대표가 만든 편집기(자오선 캐러셀 편집기 아티팩트) 자체로 그린다. 배지 크기·위치, 핸들 점, 막대 크기 등 샘플과 같은 값이 나온다.
바꾼 것은 둘뿐이다: (1) 글꼴 sans-serif -> Pretendard(+한자는 시스템 고딕) (2) 글이 겹치지 않게 본문·질문 위치를 줄 수에 맞춰 내림.
사용: python3 pipeline/carousel_editor.py  -> 2026-w40car/MMDD_1~7.jpg
편집기 원본: https://claude.ai/artifact/ASXLsYV9nmh6EKicKs2ZrE (Artifact read 로 받아 EDITOR 경로에 둔다)"""
import base64, io, json, os, sys
from PIL import Image
from playwright.sync_api import sync_playwright
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, os.path.join(ROOT, "content"))
EDITOR = os.environ.get("EDITOR_HTML", "/mnt/user-data/outputs/artifacts/4c728a9e-f8e6-479f-b4cb-53a0b2b79d6f/index.html")
FD = os.path.join(HERE, "fonts") + "/"
CUT = os.path.join(ROOT, "characters", "cut") + "/"
def b64(p): return base64.b64encode(open(p, "rb").read()).decode()
def build_html():
    s = open(EDITOR, encoding="utf-8", errors="replace").read()
    s = s.replace("px sans-serif", "px PretendardX, sans-serif")
    ff = "".join(f"@font-face{{font-family:'PretendardX';font-weight:{w};src:url(data:font/otf;base64,{b64(FD+f)}) format('opentype')}}" for w, f in
                 [(400, "PRETENDARD-REGULAR.OTF"), (500, "PRETENDARD-MEDIUM.OTF"), (600, "PRETENDARD-SEMIBOLD.OTF"), (700, "PRETENDARD-SEMIBOLD.OTF"), (900, "PRETENDARD-BLACK.OTF")])
    s = s.replace("</style>", ff + "</style>", 1)
    open("/tmp/editor_mod.html", "w", encoding="utf-8").write(s)
def face_dataurl(key):
    """편집기에 내장되지 않은 얼굴은 저장소 누끼를 편집기와 같은 675x900으로 줄여 쓴다. v5 원본은 금지(수정본으로 치환)."""
    if key == "v5_halfup": key = "v5_halfup_v2"
    im = Image.open(CUT + key + ".png").convert("RGBA").resize((675, 900), Image.LANCZOS)
    buf = io.BytesIO(); im.save(buf, "PNG"); return key, "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()

FIT = r"""
(def) => {
  const F=(w,px)=>`${w} ${px}px PretendardX, sans-serif`;
  const sl = buildSet(def); slides.length = 0; sl.forEach(s => slides.push(s));
  globalCfg.accent = def.accent; globalCfg.handle.text = 'zaoseon.com';
  const fitLines = (txt, maxW, w, start, lo, maxLines, step=2) => { let s=start; while (s>lo && wrapRich(txt,maxW,F(w,s)).length>maxLines) s-=step; return s; };
  // 1 표지: 부제가 제목 위(대표 샘플 순서). 얼굴은 위쪽, 글자는 패널 영역
  const c = slides[0];
  c.titleSize = fitLines(c.title, W-120, 900, 84, 56, c.title.split('\n').length);
  c.subSize = fitLines(c.sub, W-120, 900, 52, 36, 1);
  c.subY = 705; c.titleY = 705 + Math.round(c.subSize*0.35) + Math.round(c.titleSize*0.8) + 22;
  ctx.font = F(600,22);
  const ai = ['※ 자오선의 상담가 정월은', 'AI로 생성한 가상 캐릭터입니다'];
  c.extraTexts = ai.map((t,i)=>({text:t, x: W-60-ctx.measureText(t).width, y: 1262+i*28, size:22, color:'#8d8782', bold:false, align:'left', stroke:false}));
  // 2~4 본문, 6 조언: 배지 690 / 제목 800은 샘플 그대로, 본문만 제목 줄 수에 맞춰 내림
  [1,2,3,5].forEach(i => {
    const s = slides[i];
    if (i < 4) { s.face = 'bg_sunmoon'; s.imgScale = 1.875; }
    s.titleSize = fitLines(s.title, W-100, 900, 100, 66, 2, 4);
    const n = wrapRich(s.title, W-100, F(900,s.titleSize)).length;
    let bs = 50; const nl = s.body.split('\n').length;
    while (bs > 34 && wrapRich(s.body, W-140, F(600,bs)).length > nl) bs -= 2;
    s.bodySize = bs;
    const last = s.titleY + (n-1)*s.titleSize*1.22;
    s.bodyY = Math.round(last + 0.3*s.titleSize + 0.95*bs + 20);
  });
  // 5 오행 차트: 우주 배경 72% 오버레이(샘플의 useChartBg)
  const ch = slides[4]; ch.face='bg_sunmoon'; ch.imgScale=1.875; ch.useChartBg = true;
  // 7 CTA: 질문이 얼굴(머리·턱)을 가리지 않도록 패널 영역으로
  const t = slides[6];
  t.qSize = fitLines(t.q, W-100, 900, 84, 52, 2, 4);
  const qn = wrapRich(t.q, W-100, F(900,t.qSize)).length;
  t.qY = 705; const qLast = t.qY + (qn-1)*t.qSize*1.24;
  t.btnY = Math.round(qLast + 0.3*t.qSize + 26);
  t.nextY = t.btnY + 117 + 34;
  t.nextTitleSize = fitLines(t.nextTitle, W-100, 900, 60, 40, 1, 2);
  slides.forEach(s => { s.pageBadgeEnabled = false; });
  return slides.length;
}
"""

def main():
    from carousel_sets import SETS
    build_html()
    out_dir = os.path.join(ROOT, "2026-w40car2"); os.makedirs(out_dir, exist_ok=True)
    only = sys.argv[1:]  # 예: 2026-10-02
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1300, "height": 900})
        pg.goto("file:///tmp/editor_mod.html"); pg.wait_for_timeout(1500)
        pg.evaluate("Promise.all([400,500,600,700,900].map(w=>document.fonts.load(w+' 40px PretendardX','가한丁')))")
        need = {S["face"] for S in SETS.values()} - {"v1_lowbun", "v2_straight", "v3_ponytail", "v4_glasses", "v5_halfup_v2"}
        for key in need:
            k, url = face_dataurl(key)
            pg.evaluate("async ([k,u])=>{FACES[k]=u; const im=new Image(); im.src=u; await im.decode(); imgCache[k]=im;}", [k, url])
        for date, S in SETS.items():
            if only and date not in only: continue
            face = "v5_halfup_v2" if S["face"] == "v5_halfup" else S["face"]
            d = dict(dayChar=S["dayChar"], hanja=S["hanja"], accent=S["accent"], face=face, kicker=S["kicker"], coverTitle=S["coverTitle"], coverSub=S["coverSub"],
                     personality=S["personality"], love=S["love"], money=S["money"], advice=S["advice"], chartNote=S["chartNote"], values=S["values"], highlight=S["highlight"],
                     ctaQ=S["ctaQ"], nextTitle=S["nextTitle"])
            n = pg.evaluate(FIT, d); pg.wait_for_timeout(200)
            for i in range(n):
                url = pg.evaluate(f"(()=>{{active={i}; draw(false); return cv.toDataURL('image/png');}})()")
                im = Image.open(io.BytesIO(base64.b64decode(url.split(",")[1]))).convert("RGB")
                im.save(os.path.join(out_dir, f"{date[5:].replace('-', '')}_{i+1}.jpg"), quality=93)
            print(date, S["dayChar"], n)
        b.close()
if __name__ == "__main__": main()
