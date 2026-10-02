"""캐러셀 렌더러 v2 (10/1 밤): 대표가 올린 샘플(정 세트 7장)을 픽셀로 재서 편집기 파라미터로 옮겼다.
- 편집기(캐러셀 편집기 아티팩트)를 헤드리스 크롬으로 열어 편집기 그리기 코드 그대로 렌더 (글꼴: 샘플과 같은 Noto Sans CJK KR)
- 샘플에서 잰 값: 배지 55 / 제목 100(본문) 113(표지) / 본문 54 / 핸들 38+점 18 / 얼굴 배율·오프셋(템플릿 매칭, 일치도 0.997) / 배경 배율·패널 흐림·어둡기 / 오행 차트 막대·라벨
- 줄 수에 따른 세로 위치(본문 2줄·3줄)는 샘플 정-3/정-2 값을 그대로 쓴다
사용:
  python3 pipeline/carousel_editor.py            -> 2026-w40car3/MMDD_1~7.jpg 전체
  python3 pipeline/carousel_editor.py --compare  -> 정 샘플과 픽셀 비교(/tmp/cmp_N.jpg)
편집기 HTML: Artifact read 로 받은 파일(EDITOR_HTML). 샘플: /mnt/user-data/uploads/정-N.png"""
import base64, io, json, os, sys
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, "..")
sys.path.insert(0, os.path.join(ROOT, "content"))
EDITOR = os.environ.get("EDITOR_HTML", "/mnt/user-data/outputs/artifacts/4c728a9e-f8e6-479f-b4cb-53a0b2b79d6f/index.html")
SAMPLES = os.environ.get("SAMPLE_DIR", os.path.join(ROOT, "samples", "carousel_2026-10-01"))
CUT = os.path.join(ROOT, "characters", "cut") + "/"
PLATE = os.path.join(HERE, "assets", "chart_plate.png")
FONT = '"Noto Sans CJK KR", sans-serif'
SAMPLE_ACCENT = "#f36435"

def build_html():
    s = open(EDITOR, encoding="utf-8", errors="replace").read()
    s = s.replace("px sans-serif", "px " + FONT)
    # 본문 글자: 샘플은 세미볼드(600)인데 이 환경의 Noto는 Medium/Bold뿐이라 Bold(700)로 맞추고, 의도치 않은 자동 줄바꿈이 없게 폭 여유를 둔다
    s = s.replace("`600 ${s.bodySize}px", "`700 ${s.bodySize}px").replace("wrapRich(s.body, W-140, bodyFont)", "wrapRich(s.body, W-60, bodyFont)")
    s = s.replace("BODY_W = W-140, BODY_WEIGHT = 600;", "BODY_W = W-60, BODY_WEIGHT = 700;")   # 편집기 자체 배치 계산도 이 환경의 본문 폭·굵기에 맞춘다
    open("/tmp/editor_noto.html", "w", encoding="utf-8").write(s)

def make_plate():
    """오행 차트 배경(음양 이미지)은 편집기에 내장돼 있지 않아 샘플 정-5에서 막대·글자를 지우고(인페인팅)
    편집기의 72% 어두운 오버레이를 거꾸로 풀어 원본 판을 만든다. 편집기가 같은 오버레이를 다시 씌우면 샘플과 같아진다."""
    import cv2
    a = np.array(Image.open(os.path.join(SAMPLES, "정-5.png")).convert("RGB"))
    m = np.zeros(a.shape[:2], np.uint8)
    vals = [0.3, 0.9, 0.4, 0.3, 0.45]
    for i, v in enumerate(vals):
        x = 108 + i * 181; top = 949 - int(562 * v) - 4; m[top:955, x - 3:x + 143] = 255
    m[190:290, 215:860] = 255; m[955:1030, 85:1000] = 255; m[1022:1135, 52:1030] = 255; m[1245:1310, 30:420] = 255
    m = cv2.dilate(m, np.ones((9, 9), np.uint8))
    bgr = cv2.cvtColor(a, cv2.COLOR_RGB2BGR)
    ink = cv2.inpaint(bgr, m, 9, cv2.INPAINT_TELEA)
    ink = cv2.cvtColor(ink, cv2.COLOR_BGR2RGB).astype(np.float32)
    ov = np.array([10, 9, 8], np.float32) * 0.72
    orig = np.clip((ink - ov) / 0.28, 0, 255).astype(np.uint8)
    os.makedirs(os.path.dirname(PLATE), exist_ok=True); Image.fromarray(orig).save(PLATE)

def face_dataurl(path_or_key):
    key = "v5_halfup_v2" if path_or_key == "v5_halfup" else path_or_key
    im = Image.open(CUT + key + ".png").convert("RGBA").resize((675, 900), Image.LANCZOS)
    buf = io.BytesIO(); im.save(buf, "PNG"); return key, "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()

LAYOUT_JS = r"""
(args) => {
  const [def, ref] = args;
  const FONT='"Noto Sans CJK KR", sans-serif';
  const F=(w,px)=>`${w} ${px}px ${FONT}`;
  globalThis.__rawBuild = true; const sl = buildSet(def); globalThis.__rawBuild = false; slides.length = 0; sl.forEach(s => slides.push(s));
  const tw=(t,w,px)=>{ ctx.font=F(w,px); return ctx.measureText(t).width; };
  const balance=(txt,w,px,maxW)=>{ if (txt.includes('\n')) return txt.split('\n').map(l=>balance(l,w,px,maxW)).join('\n');
    if (tw(txt,w,px) <= maxW) return txt; let best=null;
    for (let i=1;i<txt.length-1;i++){ if (txt[i]!==' ') continue; const a=txt.slice(0,i), b=txt.slice(i+1); const wa=tw(a,w,px), wb=tw(b,w,px);
      if (wa<=maxW && wb<=maxW){ const sc=Math.abs(wa-wb)-((/[,.]$/.test(a))?120:0); if(!best||sc<best.sc) best={sc,s:a+'\n'+b}; } }
    return best?best.s:txt; };
  const report=[];
  [1,2,3,5].forEach(i=>{ const s=slides[i]; s.title=balance(s.title,900,100,930); s.body=balance(s.body,700,54.5,946); });
  globalCfg.accent = def.accent; globalCfg.applyAll = false;
  globalCfg.handle = {text:'zaoseon.com', x:104, y:1278, size:38, dot:18}; globalCfg.applyAllHandle = true;
  const panel = (x,y,w,h,blur,dark)=>({x,y,w,h,blur,dark,round:0,enabled:true});
  const nolines = (txt,maxW,font)=>wrapRich(txt,maxW,font).length;
  const bgOff = (scale, top)=> top - (H - 720*scale);
  slides.forEach(s => { s.pageBadgeEnabled = false; });

  // ---- 1 표지 ----
  const c = slides[0];
  c.bgColor = '#100a05'; c.imgScale = 1.2; c.imgOffX = 230; c.imgOffY = 800; c.panelOverride = panel(0,0,0,0,0,0); c.panelOverride.enabled = false;
  c.kickerX = 75; c.kickerY = 79; c.kickerSize = 51;
  c.subSize = 66; while (c.subSize > 40 && wrapRich(c.sub, W-120, F(900,c.subSize)).length > 1) c.subSize -= 1;
  c.subX = 88; c.subY = 270;
  const tl = def.coverTitle.split('\n').length;
  c.titleSize = 113; while (c.titleSize > 70 && nolines(c.title, W-120, F(900,c.titleSize)) > tl) c.titleSize -= 1;
  c.titleX = 88; c.titleY = 416;
  ctx.font = F(600,22);
  const ai = ['※ 자오선의 상담가 정월은', 'AI로 생성한 가상 캐릭터입니다'];
  c.extraTexts = ai.map((t,i)=>({text:t, x: 1052-ctx.measureText(t).width, y: 1280+i*24, size:22, color:'#8d8782', bold:false, align:'left', stroke:false}));

  // ---- 2~4 본문 / 6 조언 ----
  [1,2,3].forEach(i => {
    const s = slides[i]; s.bgColor = '#1a1816'; s.face = 'bg_sunmoon'; s.imgScale = 1.265; s.imgOffX = -40; s.imgOffY = bgOff(1.265, 216);
    s.panelOverride = panel(0,216,1080,916,6,102);
    s.badgeX = 540; s.badgeSize = 55; s.titleSize = 100; s.bodySize = 54.5;
    const nb = wrapRich(s.body, W-60, F(700,54.5)).length, nt = wrapRich(s.title, W-100, F(900,100)).length; report.push(['body',i+1,nt,nb,Math.round(Math.max(...s.title.split('\n').map(l=>tw(l,900,100)))),Math.round(Math.max(...s.body.split('\n').map(l=>tw(l,700,54.5))))]);
    if (nb >= 3) { s.badgeY = 327; s.titleY = 541; s.bodyY = 841; } else { s.badgeY = 350; s.titleY = 597; s.bodyY = 902; }
    if (nt === 1) { s.titleY += 61; }
  });
  const a = slides[5]; a.bgColor = '#1a1816'; a.imgScale = 0.8; a.imgOffX = 0; a.imgOffY = -205; a.panelOverride = panel(0,625,1080,620,14,212);
  a.badgeX = 540; a.badgeSize = 55; a.titleSize = 100; a.bodySize = 54.5;
  { const nb = wrapRich(a.body, W-60, F(700,54.5)).length, nt = wrapRich(a.title, W-100, F(900,100)).length; report.push(['advice',6,nt,nb,Math.round(Math.max(...a.title.split('\n').map(l=>tw(l,900,100)))),Math.round(Math.max(...a.body.split('\n').map(l=>tw(l,700,54.5))))]); const up = Math.max(0, nb-2)*40; a.panelOverride = panel(0,625-up,1080,620+up,14,212);
    a.badgeY = 695-up; a.titleY = 874-up + (nt===1?61:0); a.bodyY = 1098-up; }

  // ---- 5 오행 차트 ----
  const ch = slides[4]; ch.bgColor = '#0d0b0a'; ch.face = 'chart_plate'; ch.imgScale = 1; ch.imgOffX = 0; ch.imgOffY = 0; ch.useChartBg = true;
  ch.titleSize = 62; ctx.font = F(900,62); const cw = ctx.measureText(ch.title).width; ch.titleX = 533.5 - cw/2; ch.titleY = 262;
  ch.barWidth = 140; ch.barGap = 41; ch.barLabelSize = 52; ch.barMaxH = 949 - 50 - (262 + 1.2*62);
  ch.noteSize = 41;

  // ---- 7 CTA ----
  const t = slides[6]; t.bgColor = '#1a1816'; t.face = 'bg_sunmoon'; t.imgScale = 1.379; t.imgOffX = -90; t.imgOffY = bgOff(1.379, 167);
  t.panelOverride = panel(0,167,1080,993,14,128);
  t.qSize = 89; t.qY = 378.5; t.btn = '팔로우하고 같이 얘기 나눠요'; t.btnSize = 50; t.btnY = 558;
  t.nextBadgeSize = 39; t.nextY = 785; t.nextTitleSize = 67; t.hint = '프로필 링크에서 내 기운 1초만에 확인'; t.hintSize = 38;

  // ---- 변형 레이아웃 (대표 샘플 병·무에서 잰 값, pipeline/variant_fit.py) ----
  const VAR = def.variant || {};
  const anchors = {};
  const faceAnchor = (key) => { if (anchors[key]) return anchors[key]; const im = imgCache[key]; if (!im || !im.naturalWidth) return null;
    const Hb = im.naturalHeight * (W / im.naturalWidth), cvx = document.createElement('canvas'); cvx.width = W; cvx.height = Math.round(Hb);
    const x = cvx.getContext('2d'); x.drawImage(im, 0, 0, W, Hb); const d = x.getImageData(0, 0, W, cvx.height).data;
    let top = -1; for (let y = 0; y < cvx.height && top < 0; y++){ let n = 0; for (let xx = 0; xx < W; xx++) if (d[(y*W+xx)*4+3] > 40) n++; if (n > 8) top = y; }
    let sx = 0, sn = 0; const lim = Math.min(cvx.height, top + Math.round((cvx.height - top) * 0.3));
    for (let y = top; y < lim; y++) for (let xx = 0; xx < W; xx++) if (d[(y*W+xx)*4+3] > 40){ sx += xx; sn++; }
    return anchors[key] = {cx: sx / Math.max(sn, 1), top, Hb}; };
  // 기준 얼굴(샘플에서 맞춘 얼굴)의 머리 위치를 다른 얼굴에도 같게 옮긴다
  const adjFace = (refKey, ref, key) => { const a = faceAnchor(refKey), b = faceAnchor(key); if (!a || !b || refKey === key) return {imgScale: ref.scale, imgOffX: ref.offX, imgOffY: ref.offY};
    const s = ref.scale, cTop = (H - a.Hb*s) + ref.offY + a.top*s, cCx = (W - W*s)/2 + ref.offX + a.cx*s;
    return {imgScale: s, imgOffX: cCx - (W - W*s)/2 - b.cx*s, imgOffY: cTop - (H - b.Hb*s) - b.top*s}; };
  const fitTitle = (s, tl, start, floor) => { s.titleSize = start; while (s.titleSize > floor && nolines(s.title, W-120, F(900,s.titleSize)) > tl) s.titleSize -= 1; };
  const fitSub = (s, start) => { s.subSize = start; while (s.subSize > 40 && wrapRich(s.sub, W-120, F(900,s.subSize)).length > 1) s.subSize -= 1; };
  if (VAR.cover === 'C3') {            // 무 샘플형: 얼굴 오른쪽, 아래 패널, 부제(포인트색) 위 · 제목 아래
    const f = adjFace('v3_ponytail', {scale:1.12, offX:239, offY:303}, def.face);
    Object.assign(c, f, {bgColor:'#100a05', kickerX:75, kickerY:103, kickerSize:51, subX:88, subY:950, titleX:85, titleY:1087});
    c.panelOverride = panel(0,865,1080,393,14,175); fitSub(c, 66); fitTitle(c, tl, 108, 70);
  } else if (VAR.cover === 'C2') {     // 병 샘플형: 얼굴 위쪽 오른쪽, 아래 패널, 제목 위 · 부제(포인트색) 아래
    const f = adjFace('v1_lowbun', {scale:1.3, offX:190, offY:547}, def.face);
    Object.assign(c, f, {bgColor:'#1a1816', kickerX:90, kickerY:117, kickerSize:47, titleX:111, titleY:952, subX:110, subY:1148});
    c.panelOverride = panel(0,829,1080,398,15,121); fitSub(c, 43); fitTitle(c, tl, 94, 60);
  }
  if (VAR.advice === 'A2') {           // 본문형 조언(해·달 배경, 얼굴 없음)
    const s = slides[5]; s.face = 'bg_sunmoon'; s.imgScale = 1.265; s.imgOffX = -40; s.imgOffY = bgOff(1.265, 216); s.panelOverride = panel(0,216,1080,916,6,102);
    s.badgeX = 540; s.badgeSize = 55; s.titleSize = 100; s.bodySize = 54.5;
    const nb = wrapRich(s.body, W-60, F(700,54.5)).length, nt = wrapRich(s.title, W-100, F(900,100)).length;
    if (nb >= 3) { s.badgeY = 327; s.titleY = 541; s.bodyY = 841; } else { s.badgeY = 350; s.titleY = 597; s.bodyY = 902; }
    if (nt === 1) s.titleY += 61;
  }
  if (VAR.cta === 'T2') {              // 무 샘플형: 어두운 바탕, 얼굴 오른쪽 아래, 글자 왼쪽
    const f = adjFace('v3_ponytail', {scale:0.62, offX:304, offY:74}, def.face);
    Object.assign(t, f, {bgColor:'#1a1816', face:def.face, qX:422, qY:210, qSize:89, btnX:434, btnY:391, btnSize:45, nextX:269, nextY:866, nextBadgeSize:39, nextTitleSize:67, hint:''});
    t.panelOverride = panel(0,0,0,0,0,0); t.panelOverride.enabled = false;
    t.extraTexts = [{text:(def.hintText || '프로필 링크에서\n내 기운 1초만에 확인'), x:71, y:1122, size:36, color:'#a8a39e', bold:false, align:'left', stroke:false}];
  }
  globalThis.__report = report;
  return slides.length;
}
"""

def render(sets, out_dir, ref_accent=None, prefix=lambda d: d[5:].replace("-", "")):
    build_html()
    if not os.path.exists(PLATE): make_plate()
    os.makedirs(out_dir, exist_ok=True); results = {}
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1300, "height": 900})
        pg.goto("file:///tmp/editor_noto.html"); pg.wait_for_timeout(1500)
        pg.evaluate("Promise.all([400,500,600,700,900].map(w=>document.fonts.load(w+' 40px \"Noto Sans CJK KR\"','가한丁')))")
        add = {"chart_plate": "data:image/png;base64," + base64.b64encode(open(PLATE, "rb").read()).decode()}
        for S in sets.values():
            k, u = face_dataurl(S["face"])
            if k not in ("v1_lowbun", "v2_straight", "v3_ponytail", "v4_glasses", "v5_halfup_v2"): add[k] = u
        for k, u in add.items():
            pg.evaluate("async ([k,u])=>{FACES[k]=u; const im=new Image(); im.src=u; await im.decode(); imgCache[k]=im;}", [k, u])
        for date, S in sets.items():
            face = "v5_halfup_v2" if S["face"] == "v5_halfup" else S["face"]
            d = dict(dayChar=S["dayChar"], hanja=S["hanja"], accent=ref_accent or S["accent"], face=face, kicker=S["kicker"], coverTitle=S["coverTitle"], coverSub=S["coverSub"],
                     personality=S["personality"], love=S["love"], money=S["money"], advice=S["advice"], chartNote=S["chartNote"], values=S["values"], highlight=S["highlight"],
                     ctaQ=S["ctaQ"], nextTitle=S["nextTitle"], variant=S.get("variant", {}))
            n = pg.evaluate(LAYOUT_JS, [d, None]); pg.wait_for_timeout(150)
            for rep in pg.evaluate('globalThis.__report'): print('   ', rep, '(슬라이드, 제목줄수, 본문줄수, 제목최대폭(<=980), 본문최대폭(<=940))')
            imgs = []
            for i in range(n):
                url = pg.evaluate(f"(()=>{{active={i}; draw(false); return cv.toDataURL('image/png');}})()")
                im = Image.open(io.BytesIO(base64.b64decode(url.split(",")[1]))).convert("RGB"); imgs.append(im)
                im.save(os.path.join(out_dir, f"{prefix(date)}_{i+1}.jpg"), quality=93)
            results[date] = imgs; print(date, S["dayChar"], n)
        b.close()
    return results

def compare():
    """정 샘플 대비 렌더 비교: 슬라이드별 평균 절대 차이와 나란히 보기 이미지"""
    from carousel_sets import SETS
    sets = {"2026-10-02": SETS["2026-10-02"]}
    res = render(sets, "/tmp/cmp_out", ref_accent=SAMPLE_ACCENT, prefix=lambda d: "jeong")
    imgs = res["2026-10-02"]
    for i, im in enumerate(imgs, 1):
        sm = Image.open(os.path.join(SAMPLES, f"정-{i}.png")).convert("RGB")
        d = np.abs(np.array(im).astype(int) - np.array(sm).astype(int)).mean(axis=2)
        sheet = Image.new("RGB", (1620, 675)); sheet.paste(sm.resize((540, 675)), (0, 0)); sheet.paste(im.resize((540, 675)), (540, 0))
        dd = Image.fromarray(np.clip(d * 4, 0, 255).astype(np.uint8)).convert("RGB").resize((540, 675)); sheet.paste(dd, (1080, 0)); sheet.save(f"/tmp/cmp_{i}.jpg", quality=88)
        print(f"정-{i}: mean abs diff {d.mean():.2f}  (>40px diff pixels {(d>40).mean()*100:.1f}%)")



# ================= 릴스 (캐러셀 샘플 규칙 그대로) =================
OVERRIDE_JS = """
(o) => {
  if (o.badges) { slides[1].badge = o.badges[0]; slides[2].badge = o.badges[1]; slides[3].badge = o.badges[2]; }
  if (o.nextBadge) slides[6].nextBadge = o.nextBadge;
  if (o.nextTitle) slides[6].nextTitle = o.nextTitle;
  if (o.btn) slides[6].btn = o.btn;
  if (o.hint) slides[6].hint = o.hint;
  return 1;
}
"""
REEL_W, REEL_H, REEL_TOP = 1080, 1920, 230    # 슬라이드(1080x1350)를 인스타 UI 안전 영역(위 230, 아래 340)에 정확히 맞춘다
REEL_DUR = [2.6, 2.0, 2.0, 2.0, 2.6]; REEL_FADE = 0.3

def reel_defs():
    from carousel_sets import SETS
    from reel_sets import REELS
    fix = json.load(open(os.path.join(ROOT, "content", "2026-w40fix.json"), encoding="utf-8"))["posts"]
    tri_idx = {"2026-10-03": 1, "2026-10-05": 3, "2026-10-10": 4, "2026-10-11": 5}
    defs = {}
    for date, R in REELS.items():
        nxt = R["next"]
        nb, nt = ("내일 낮 12시", nxt.split(": ", 1)[1]) if nxt.startswith("내일 낮 12시: ") else ("월요일 아침 8시", "이번 주 기운 편")
        if date in tri_idx:
            im = fix[tri_idx[date] - 1]["image"]; rows = im["rows"]
            d = dict(dayChar="", hanja="", accent=R["accent"], face=R["face"], kicker=R["kicker"], coverTitle=R["hook"], coverSub=R["sub"],
                     personality=[rows[0][2], rows[0][3]], love=[rows[1][2], rows[1][3]], money=[rows[2][2], rows[2][3]], advice=["셋 중 두 개 이상\n겹쳤다면", im.get("note", "")], chartNote="", values=[.3, .3, .3, .3, .3], highlight=0,
                     ctaQ=R["q"], nextTitle=nt)
            ov = dict(badges=["사주(동양)", "별자리(서양)", "수비학(숫자)"], nextBadge=nb, nextTitle=nt)
        else:
            S = SETS[date]
            d = dict(dayChar=S["dayChar"], hanja=S["hanja"], accent=S["accent"], face=S["face"], kicker=S["kicker"], coverTitle=S["coverTitle"], coverSub=S["coverSub"],
                     personality=S["personality"], love=S["love"], money=S["money"], advice=S["advice"], chartNote=S["chartNote"], values=S["values"], highlight=S["highlight"],
                     ctaQ=S["ctaQ"], nextTitle=nt, variant=S.get("variant", {}))
            ov = dict(nextBadge=nb, nextTitle=nt)
        d["face"] = "v5_halfup_v2" if d["face"] == "v5_halfup" else d["face"]
        defs[date] = (d, ov)
    return defs

def render_reels():
    import subprocess
    build_html()
    if not os.path.exists(PLATE): make_plate()
    defs = reel_defs(); out_dir = os.path.join(ROOT, "2026-w40car3-reel"); os.makedirs(out_dir, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1300, "height": 900})
        pg.goto("file:///tmp/editor_noto.html"); pg.wait_for_timeout(1500)
        pg.evaluate("Promise.all([400,500,600,700,900].map(w=>document.fonts.load(w+' 40px \"Noto Sans CJK KR\"','가한丁')))")
        add = {"chart_plate": "data:image/png;base64," + base64.b64encode(open(PLATE, "rb").read()).decode()}
        for d, _ in defs.values():
            k, u = face_dataurl(d["face"])
            if k not in ("v1_lowbun", "v2_straight", "v3_ponytail", "v4_glasses", "v5_halfup_v2"): add[k] = u
        for k, u in add.items():
            pg.evaluate("async ([k,u])=>{FACES[k]=u; const im=new Image(); im.src=u; await im.decode(); imgCache[k]=im;}", [k, u])
        for date, (d, ov) in defs.items():
            pg.evaluate(LAYOUT_JS, [d, None]); pg.evaluate(OVERRIDE_JS, ov); pg.wait_for_timeout(120)
            frames = []
            for i in (0, 1, 2, 3, 6):
                url = pg.evaluate(f"(()=>{{active={i}; draw(false); return cv.toDataURL('image/png');}})()")
                im = Image.open(io.BytesIO(base64.b64decode(url.split(",")[1]))).convert("RGB")
                canvas = Image.new("RGB", (REEL_W, REEL_H), im.getpixel((5, 5))); canvas.paste(im, (0, REEL_TOP))
                fp = f"/tmp/reelframe_{date[5:]}_{i}.png"; canvas.save(fp); frames.append(fp)
            mp4 = os.path.join(out_dir, f"{date}.mp4")
            cmd = ["ffmpeg", "-y", "-loglevel", "error"]
            for f, t in zip(frames, REEL_DUR): cmd += ["-loop", "1", "-t", str(t), "-i", f]
            total = sum(REEL_DUR) - REEL_FADE * (len(frames) - 1)
            cmd += ["-f", "lavfi", "-t", f"{total:.2f}", "-i", "anullsrc=r=44100:cl=stereo"]
            fl = ""; prev = "[0:v]"; acc = REEL_DUR[0]
            for k in range(1, len(frames)):
                off = acc - REEL_FADE * k; lab = f"[x{k}]"
                fl += f"{prev}[{k}:v]xfade=transition=fade:duration={REEL_FADE}:offset={off:.2f}{lab};"; prev = lab; acc += REEL_DUR[k]
            fl += f"{prev}format=yuv420p,fps=30[vout]"
            cmd += ["-filter_complex", fl, "-map", "[vout]", "-map", f"{len(frames)}:a", "-c:v", "libx264", "-crf", "20", "-c:a", "aac", "-b:a", "96k", "-shortest", "-movflags", "+faststart", mp4]
            subprocess.run(cmd, check=True); print(date, "->", mp4, f"{total:.1f}s")
        b.close()

def main():
    if "--reels" in sys.argv: render_reels(); return
    if "--compare" in sys.argv: compare(); return
    from carousel_sets import SETS
    only = [a for a in sys.argv[1:] if not a.startswith("--")]
    sets = {k: v for k, v in SETS.items() if not only or k in only}
    render(sets, os.path.join(ROOT, "2026-w40car3"))

if __name__ == "__main__": main()
