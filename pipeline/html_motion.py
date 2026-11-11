"""HTML 모션을 MP4 로 뽑는다 — 대표 10/16 오AI완 '클로드 모션그래픽 키트' 벤치마크.

가져온 것
  **모션을 HTML/CSS/JS 로 만든다.** 지금 우리 릴스는 PIL 로 그려서 글자가 떠오르는 정도밖에 못 한다.
  CSS 는 수십 개가 동시에 움직이고, 숫자가 올라가고, 선이 그려지는 것을 쉽게 한다 —
  K-073 2단('숫자·표가 쌓이는 과정')이 바로 그것이다.

**안 가져온 것 둘**
  ① 원문 프롬프트("showreel for a résumé. go all out")는 모션 디자이너 과시용이다.
     K-073 은 "움직임은 정보를 나르거나 스크롤을 멈출 때만 쓴다" 이다. 화려하기만 한 영상은 안 만든다.
  ② **화면 녹화로 뽑는 방법**(Cmd+Shift+5 · Xbox Game Bar). 사람이 15초를 손으로 녹화하고 잘라야 한다 —
     노가다이고, 길이·fps·규격이 매번 다르고, 화질도 떨어진다.
     우리는 Playwright 헤드리스 크로미움이 이미 있다. **프레임을 한 장씩 찍어 붙인다** —
     사람 손이 안 들어가고 길이·fps·크기가 정확하다.

HTML 쪽 약속 하나
  페이지가 `window.seek(t)` 를 내놔야 한다(t = 초). 렌더러가 프레임마다 이것을 불러 시각을 맞춘다.
  CSS 애니메이션을 시간에 맡기지 않고 우리가 시각을 지정하므로 **몇 번을 돌려도 같은 영상**이 나온다
  (화면 녹화는 그때그때 다르다).

사용: python3 pipeline/html_motion.py 파일.html 나갈이름 [--초=15] [--fps=30] [--소리=fun|love|data|없음] [--출력=경로.mp4] [--블러=4]
     python3 pipeline/html_motion.py 파일.html --확인=1.5,4,7.6,11.5      박자별 확인 컷 한 장(전체 렌더 전에 본다)
결과: 2026-motion/html/<나갈이름>.mp4 (소리 있음 — K-070)

11/10 보완(대표 "이 제작 기법도 콘텐츠 제작 파이프라인에 추가", 빌더 조쉬 모션 프롬프트 벤치마크)
  ① 소리를 붙인다. 전에는 소리 없는 mp4 만 나왔다(K-070 위반 위험). 음악은 music_plan(→reel_music) 그대로 쓰고
     — 음악 도구를 새로 만들지 않는다 — HTML 이 `window.SFX=[{t:초,k:'swoosh|tick|chime|press'}]` 를 내놓으면
     그 시각에 효과음을 얹는다. 소리는 48kHz(네이버 클립이 96kHz 를 거부, 11/5).
  ② 금지 검사: 시간이 seek(t) 밖에서 흐르는 것(CSS 애니메이션·transition·타이머·Math.random·Date.now)과
     빌더 조쉬 금지 목록 중 코드로 잴 수 있는 것(blur·glow 그림자)을 그리기 전에 막는다.
  ③ 확인 컷: 박자 시각 몇 개만 먼저 찍어 한 장으로 붙인다 — 360장 다 찍고 틀린 것을 알지 않게.
  ⑤ --블러=N: 한 프레임 안을 N장 찍어 평균(모션 블러). 빠른 움직임이 끊겨 보일 때만. 렌더 시간 N배.
  ④ render_html(html, 나갈경로, 초): motion_kinetic·motion_litho 등이 부르던 이름이 없어서 깨져 있었다. 되살렸다.
  만드는 법 정리: zaoseon-site:docs/제작_가이드라인_최종_2026-10-16.md 16절.
"""
import os, sys, json, shutil, asyncio, subprocess, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
import channel_specs as CS

CH = CS.CH["reel"]
OUT = os.path.join(ROOT, "2026-motion", "html")


async def _shoot(html, 초, fps, w, h, tmp, 한계, 구역, 블러=1, ch="reel"):
    from playwright.async_api import async_playwright
    n = int(round(초 * fps))
    async with async_playwright() as pw:
        b = await pw.chromium.launch(args=["--force-color-profile=srgb", "--disable-lcd-text"])
        pg = await b.new_page(viewport={"width": w, "height": h}, device_scale_factor=1)
        await pg.add_init_script(_spec_js(ch))
        await pg.goto("file://" + os.path.abspath(html))
        await pg.wait_for_function("typeof window.seek === 'function'", timeout=15000)
        # 글이 아래 고정 줄을 넘는지 **브라우저로 재서** 막는다.
        # 눈대중으로 여백을 맞추다 두 번 겹쳤다(10/16). 끝 시각에서 제일 아래 글의 바닥을 잰다.
        await pg.evaluate("t => window.seek(t)", 초 - 0.01)
        바닥 = await pg.evaluate("""() => {
          const els = [...document.querySelectorAll('.safe *')].filter(e => e.offsetHeight);
          return els.length ? Math.max(...els.map(e => e.getBoundingClientRect().bottom)) : 0; }""")
        if 바닥 > 한계:
            await b.close()
            raise SystemExit(f"[막음] 글이 아래 고정 줄을 넘어요 — 맨 아래 글 바닥 {바닥:.0f}px, "
                             f"넘으면 안 되는 선 {한계}px (하단 고정 줄 위 24px). "
                             f"{바닥 - 한계:.0f}px 줄이세요.")
        # 구역을 넘는지도 잰다. 아래 고정 줄만 보면 **구역끼리 겹치는 것**을 놓친다 —
        # 10/16 막대 세 줄이 '본문·그림' 구역을 166px 넘어 AI 고지 위로 올라갔는데 통과했다.
        if 구역:
            # 바깥 상자만 재면 안 된다 — 자식이 넘쳐도 부모 rect 는 그대로라서 놓친다(10/16).
            # 상자와 **그 안 모든 자손**의 바닥 중 제일 아래를 쓴다.
            잰것 = await pg.evaluate("""() => [...document.querySelectorAll('.mk[data-z]')]
              .map(e => {
                const all = [e, ...e.querySelectorAll('*')].filter(x => x.offsetHeight);
                return [e.dataset.z, all.length ? Math.max(...all.map(x => x.getBoundingClientRect().bottom)) : 0];
              }).filter(r => r[1] > 0)""")
            넘침 = [(z, b_, 구역[z]) for z, b_ in 잰것 if z in 구역 and b_ > 구역[z] + 1]
            if 넘침:
                await b.close()
                raise SystemExit("[막음] 구역을 넘었어요 — " + " / ".join(
                    f"'{z}' 바닥 {b_:.0f}px, 구역 끝 {끝}px ({b_ - 끝:.0f}px 넘침)"
                    for z, b_, 끝 in 넘침) + ". 글을 줄이거나 더 넓은 구역('마무리 카드')으로 옮기세요.")
        for i in range(n):
            if 블러 <= 1:
                await pg.evaluate("t => window.seek(t)", i / fps)
                await pg.screenshot(path=os.path.join(tmp, f"f{i:05d}.png")); continue
            # 11/10 모션 블러(Prompt Motion 고친 쇼릴 프롬프트): 한 프레임 시간(셔터 절반) 안을 블러장 찍어 평균한다
            import numpy as np, io
            from PIL import Image
            acc = None
            for k in range(블러):
                await pg.evaluate("t => window.seek(t)", (i + 0.5 * k / 블러) / fps)
                a = np.asarray(Image.open(io.BytesIO(await pg.screenshot())).convert("RGB"), dtype=np.float32)
                acc = a if acc is None else acc + a
            Image.fromarray((acc / 블러).round().astype("uint8")).save(os.path.join(tmp, f"f{i:05d}.png"))
        await b.close()
    return n


def _spec_js(ch="reel"):
    """channel_specs 값을 페이지에 넣는다(window.ZS_SPEC) + 캔버스 글자 위치 기록기.
    11/11 대표 "채널 별 콘텐츠 안전영역 … 기억하지?": 캔버스 릴스 4편이 안전 영역을 안 지켰다.
    DOM 검사(.safe/.mk)는 캔버스 글자를 못 잰다. 그래서 fillText 를 감싸 글자 상자를 직접 잰다."""
    C = CS.CH[ch]; z = {r[0]: list(r[1:5]) for r in C["zones"]}
    spec = dict(safe=list(C["safe"]), top=z["상단 고정"], bottom=z["하단 고정"])
    return ("window.ZS_SPEC=" + json.dumps(spec) + ";window.__zsTxt=[];window.__zsFrame=0;"
            "(function(){const P=CanvasRenderingContext2D.prototype;['fillText','strokeText'].forEach(k=>{const o=P[k];P[k]=function(s,x,y,...r){"
            "try{if(!window.__zsFrame&&this.globalAlpha>0.15&&String(s).trim()){const m=this.measureText(s),T=this.getTransform(),"
            "w=m.width,al=this.textAlign,x0=al==='center'?x-w/2:(al==='right'||al==='end')?x-w:x,a=m.actualBoundingBoxAscent,d=m.actualBoundingBoxDescent,"
            "bx=[[x0,y-a],[x0+w,y-a],[x0,y+d],[x0+w,y+d]].map(([px,py])=>[T.a*px+T.c*py+T.e,T.b*px+T.d*py+T.f]),"
            "xs=bx.map(p=>p[0]),ys=bx.map(p=>p[1]),sc=Math.hypot(T.a,T.b);"
            "const cr=this.canvas.getBoundingClientRect(),kx=cr.width/this.canvas.width,ky=cr.height/this.canvas.height;"
            "const fm=/(\\d+(?:\\.\\d+)?)px\\s+(.+)$/.exec(this.font)||[0,0,''];"
            "if(sc>0.85)window.__zsTxt.push([String(s).slice(0,20),cr.left+kx*Math.min(...xs),cr.top+ky*Math.min(...ys),cr.left+kx*Math.max(...xs),cr.top+ky*Math.max(...ys),parseFloat(fm[1])*sc*kx,fm[2].replace(/['\"]/g,'').split(',')[0].trim()])}}catch(e){}"
            "return o.call(this,s,x,y,...r)}})})();"
            # DOM 글자도 잰다(캔버스+DOM 섞어 쓴 페이지가 있다). 고정 요소(.bf)는 뺀다.
            "window.__zsDom=()=>{const R=[],W=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n;while(n=W.nextNode()){"
            "const e=n.parentElement;if(!e||!n.textContent.trim()||e.closest('.bf,script,style'))continue;"
            "if(e.checkVisibility&&!e.checkVisibility({opacityProperty:true,visibilityProperty:true}))continue;"
            "let o=1;for(let x=e;x&&x.nodeType===1;x=x.parentElement)o*=parseFloat(getComputedStyle(x).opacity);if(o<0.15)continue;"
            "const rg=document.createRange();rg.selectNodeContents(n);const r=rg.getBoundingClientRect();if(!r.width)continue;"
            "if(e.offsetWidth&&e.getBoundingClientRect().width/e.offsetWidth<0.85)continue;"
            "const cs=getComputedStyle(e),k=e.offsetWidth?e.getBoundingClientRect().width/e.offsetWidth:1;"
            "const fz=parseFloat(cs.fontSize)*k,cy_=(r.top+r.bottom)/2,hh=Math.min((r.bottom-r.top)/2,fz*.55);"
            "R.push([n.textContent.trim().slice(0,20),r.left,cy_-hh,r.right,cy_+hh,fz,cs.fontFamily.replace(/['\"]/g,'').split(',')[0].trim()])}return R};")


def 안전영역_검사(pg, 초, ch="reel", 간격=0.1):
    """캔버스 글자가 '글 칸'(안전 영역 안, 위·아래 고정 줄 사이)을 0.3초 넘게 벗어나면 막는다.
    들어오고 나가는 순간(잠깐 밖에 있는 것)은 봐준다. 크기가 85% 미만으로 커지는 중인 글도 뺀다."""
    C = CS.CH[ch]; z = {r[0]: r[1:5] for r in C["zones"]}
    x0, x1 = C["safe"][0], C["safe"][2]; y0 = z["상단 고정"][3] + 10; y1 = z["하단 고정"][1] - 10
    밖 = {}; 작음 = {}
    import fonts_kit as FK
    이름 = {"BZ": "hand_bazzi", "DK": "hand_brush", "HC": "hand_cute", "HP": "hand_pen", "DG": "hand_round"}
    손글씨_최소 = {f: FK.HAND_MIN[k] for f, k in 이름.items()}
    일반_최소 = CS.BALANCE["min_text"]   # 11/11 대표 '본문·배지 글자 크게' — channel_specs.BALANCE
    n = int(초 / 간격)
    for i in range(n + 1):
        t = min(i * 간격, 초 - 0.01)
        pg.evaluate("t => {window.__zsTxt=[];window.seek(t)}", t)
        rows = pg.evaluate("() => window.__zsTxt.concat(window.__zsDom())")
        for s, a, b, c, d, px, fam in rows:
            넘 = max(x0 - a, c - x1, y0 - b, d - y1)
            if 넘 > 2: 밖.setdefault(s, []).append((round(t, 2), round(넘)))
            # 11/11 대표 13:09 "가독성 잘 생각해줘": 글자가 너무 작으면 막는다(손글씨는 더 크게)
            최소 = 손글씨_최소.get(fam, 일반_최소)
            if px and px < 최소 - 0.5: 작음.setdefault(s, []).append((round(t, 2), round(px), 최소, fam))
    문제 = []
    for s, v in 밖.items():
        ts = [t for t, _ in v]; run = best = 1
        for k in range(1, len(ts)):
            run = run + 1 if ts[k] - ts[k - 1] <= 간격 + 1e-6 else 1; best = max(best, run)
        if best * 간격 >= 0.3: 문제.append(f"'{s}' {v[0][0]}초부터 {max(n_ for _, n_ in v)}px 밖")
    for s, v in 작음.items():
        if len(v) >= 3: 문제.append(f"'{s}' 글자 {v[0][1]}px — {v[0][3] or '글꼴'}는 {v[0][2]}px 이상(가독성)")
    return 문제, (x0, y0, x1, y1)


def 균형_검사(pg, 초, ch="reel", 간격=0.25):
    """화면 픽셀로 장면 균형을 잰다(11/11 대표 13:27). 글 칸 안에서 배경과 다른 픽셀의 묶음 상자를 구해
    ① 위 간격(상단 고정 줄 + gap_top) ② 세로·가로 가운데 ③ 채움(작은 글만 위에 떠 있는 장면) 을 본다.
    hold 초 넘게 이어질 때만 문제로 친다. 배경색은 글 칸 가장자리 픽셀의 중앙값."""
    import numpy as np, io
    from PIL import Image
    B = CS.BALANCE; C = CS.CH[ch]; z = {r[0]: r[1:5] for r in C["zones"]}
    sx0, sx1 = C["safe"][0], C["safe"][2]; top = z["상단 고정"][3]; bot = z["하단 고정"][1]
    ay0, ay1 = top + 10, bot - 10; acx = (sx0 + sx1) / 2; acy = (top + B["gap_top"] + bot - 10) / 2
    keys = {"위 간격": [], "가운데": [], "채움": []}
    n = int(초 / 간격)
    for i in range(n + 1):
        t = min(i * 간격, 초 - 0.01)
        pg.evaluate("t => {window.__zsTxt=[];window.seek(t)}", t)
        a = np.asarray(Image.open(io.BytesIO(pg.screenshot())).convert("RGB")).astype(int)
        # 11/11 대표 13:38 "뱃지나 텍스트, 그래픽 구성 요소들 간 간격이 붙지 않게": 글자 상자 둘레(글자 크기의 1/4, 최소 14px)에
        # 다른 것(선·그림·다른 글자·뱃지 가장자리)이 들어와 있으면 '붙음'. 뱃지 안 글자는 뱃지 여백이 모자랄 때 걸린다.
        rows_ = pg.evaluate("() => window.__zsTxt.concat(window.__zsDom())")
        # 한 덩어리 글(줄바꿈한 두 줄, 같은 글자 크기)은 하나로 합친다 — 같은 글의 줄 사이는 '붙음'이 아니다
        rows_.sort(key=lambda r: (r[2], r[1]))
        def _붙일(q, r):
            fs_ = max(q[5] or 40, r[5] or 40); 같은크기 = abs((q[5] or 0) - (r[5] or 0)) <= .3 * fs_
            세로잇기 = -fs_ * .6 < r[2] - q[4] < fs_ * .6 and min(q[3], r[3]) > max(q[1], r[1])           # 줄바꿈한 다음 줄
            가로잇기 = min(q[4], r[4]) - max(q[2], r[2]) > .5 * min(q[4] - q[2], r[4] - r[2]) and max(q[1], r[1]) - min(q[3], r[3]) < fs_ * .6   # 같은 줄의 굵게·색 바꾼 조각
            return 같은크기 and (세로잇기 or 가로잇기)
        합 = [list(r) for r in rows_]; 바뀜 = True
        while 바뀜:
            바뀜 = False
            for ii in range(len(합)):
                for jj in range(ii + 1, len(합)):
                    q, r = 합[ii], 합[jj]
                    if r[2] < q[2]: q, r = r, q
                    if _붙일(q, r):
                        u = [q[0] + " " + r[0], min(q[1], r[1]), min(q[2], r[2]), max(q[3], r[3]), max(q[4], r[4]), q[5], q[6]]
                        합[ii] = u; del 합[jj]; 바뀜 = True; break
                if 바뀜: break
        for row in 합:
            tx, bx0, by0, bx1, by1, px = row[0], *[int(round(v)) for v in row[1:5]], row[5] or 40
            mg = min(40, max(14, int(px * B["near"])))
            X0, Y0, X1, Y1 = max(bx0 - mg, 0), max(by0 - mg, 0), min(bx1 + mg, a.shape[1] - 1), min(by1 + mg, a.shape[0] - 1)
            if Y1 <= Y0 or X1 <= X0 or by0 < top or by1 > bot: continue
            R_ = a[Y0:Y1, X0:X1]; inner = np.zeros(R_.shape[:2], bool); inner[by0 - Y0:by1 - Y0, bx0 - X0:bx1 - X0] = True
            ring = R_[~inner]
            if len(ring) < 50: continue
            med = np.median(ring, 0); diff = np.abs(ring - med).max(1) > 60
            if diff.mean() > 0.03: keys.setdefault("붙음 · " + tx[:12], []).append((t, f"'{tx}' 둘레 {mg}px 안에 다른 요소({diff.mean() * 100:.0f}%)"))
        A = a[ay0:ay1, :]
        edge = np.concatenate([A[:, :24].reshape(-1, 3), A[:, -24:].reshape(-1, 3)])
        bg = np.median(edge, 0)
        m = np.abs(A - bg).max(2) > 48
        rows = np.where(m.sum(1) > 14)[0]
        if len(rows) == 0: continue
        cols = np.where(m[rows.min():rows.max() + 1].sum(0) > 14)[0]
        if len(cols) == 0: continue
        y0, y1 = rows.min() + ay0, rows.max() + ay0; x0, x1 = cols.min(), cols.max()
        h, w = y1 - y0, x1 - x0
        if y0 < top + B["gap_top"] - 4: keys["위 간격"].append((t, f"내용 위 끝 y{y0} (상단 고정 줄 아래 {y0 - top}px, {B['gap_top']}px 이상)"))
        if abs((y0 + y1) / 2 - acy) > B["center_tol_y"] or abs((x0 + x1) / 2 - acx) > B["center_tol_x"]:
            keys["가운데"].append((t, f"내용 묶음 가운데 ({(x0 + x1) / 2:.0f},{(y0 + y1) / 2:.0f}) — 칸 가운데 ({acx:.0f},{acy:.0f})"))
        if h < B["min_fill_h"] * (bot - top - B["gap_top"]) and w < B["min_fill_w"] * (sx1 - sx0):
            keys["채움"].append((t, f"내용 {w}x{h}px — 비어 보임(글자를 키우거나 그림을 더 크게)"))
    문제 = []
    for k, v in keys.items():
        if not v: continue
        ts = [x[0] for x in v]; run = 1; s0 = 0; best = (1, 0)
        for j in range(1, len(ts)):
            if ts[j] - ts[j - 1] <= 간격 + 1e-6: run += 1
            else: run = 1; s0 = j
            if run > best[0]: best = (run, s0)
        if best[0] * 간격 > (B["hold"] * .75 if k.startswith("붙음") else B["hold"]):
            x = v[best[1]]; 문제.append(f"[{k}] {x[0]:.2f}초부터 {best[0] * 간격:.1f}초 동안 — {x[1]}")
    return 문제


금지 = [  # (찾을 것, 까닭) — 시간은 seek(t) 하나가 정한다. 꾸밈만 하는 효과는 안 쓴다(K-073·빌더 조쉬 금지 목록)
    (r"@keyframes|animation\s*:", "CSS 애니메이션 — 시간이 seek 밖에서 흐른다"),
    (r"transition\s*:", "transition — 프레임마다 결과가 달라진다"),
    (r"setTimeout|setInterval|requestAnimationFrame", "타이머 — seek(t) 하나로 정해야 한다"),
    (r"Math\.random|Date\.now|performance\.now", "무작위·현재 시각 — 몇 번을 돌려도 같은 영상이어야 한다"),
    (r"filter\s*:[^;]*blur|backdrop-filter", "blur — 흐림 등장·배경 흐림 금지"),
    (r"text-shadow\s*:[^;]*\d{2,}px", "큰 글자 그림자(glow) 금지"),
]


def 금지_검사(html):
    import re
    s = open(html, encoding="utf-8").read()
    걸림 = [why for pat, why in 금지 if re.search(pat, s)]
    if 걸림:
        raise SystemExit("[막음] " + os.path.basename(html) + " — " + " / ".join(걸림))


def 확인컷(html, 시각, ch="reel"):
    """박자 시각 몇 개만 찍어 가로로 붙인 한 장(1/3 크기). 돌려줌: png 경로."""
    from PIL import Image
    from playwright.sync_api import sync_playwright
    금지_검사(html)
    C = CS.CH[ch]; w, h = C["w"], C["h"]; ims = []
    with sync_playwright() as pw:
        b = pw.chromium.launch(); pg = b.new_page(viewport={"width": w, "height": h}); pg.add_init_script(_spec_js(ch))
        pg.goto("file://" + os.path.abspath(html)); pg.wait_for_function("typeof window.seek === 'function'")
        pg.evaluate("document.fonts.ready")
        for t in 시각:
            pg.evaluate("t => window.seek(t)", t); f = tempfile.mktemp(suffix=".png"); pg.screenshot(path=f)
            ims.append(Image.open(f).convert("RGB").resize((w // 3, h // 3))); os.remove(f)
        b.close()
    c = Image.new("RGB", (w // 3 * len(ims), h // 3), "white")
    for i, im in enumerate(ims): c.paste(im, (i * (w // 3), 0))
    out = os.path.splitext(os.path.abspath(html))[0] + "_확인.png"; c.save(out); return out


def _효과음(path, 초, cues, sr=48000):
    import numpy as np, wave
    n = int(sr * 초); a = np.zeros(n); tt = lambda d: np.arange(int(sr * d)) / sr
    g = np.random.default_rng(7)   # 씨앗 고정 — 같은 영상엔 같은 소리
    def sw():  t = tt(.4);  return .10 * g.standard_normal(len(t)) * np.sin(np.pi * t / .4)
    def tick(): t = tt(.04); return .12 * g.standard_normal(len(t)) * np.exp(-t * 120)
    def chime(f): t = tt(1.2); return .22 * (np.sin(2*np.pi*f*t) + .5*np.sin(4*np.pi*f*t)) * np.exp(-t * 3.5)
    def press(): t = tt(.12); return .35 * np.sin(2*np.pi*(180 - 600*t)*t) * np.exp(-t * 30)
    # 11/11 대표 "효과음 같은 것도 넣어주고": 종류 더함 — pop(말풍선) · ding(정답) · whoosh(빠른 이동) · boing(통통) · cash(돈) · sparkle(반짝) · thud(쾅)
    def pop(): t = tt(.09); return .4 * np.sin(2*np.pi*(500 + 2400*t)*t) * np.exp(-t * 45)
    def ding(): t = tt(1.0); return .26 * (np.sin(2*np.pi*1568*t) + .6*np.sin(2*np.pi*2349*t)) * np.exp(-t * 4)
    def whoosh(): t = tt(.35); n = g.standard_normal(len(t)); f = np.convolve(n, np.ones(6)/6, "same"); return .22 * f * np.sin(np.pi * t / .35) ** 2
    def boing(): t = tt(.4); return .3 * np.sin(2*np.pi*(220 + 160*np.sin(2*np.pi*9*t))*t) * np.exp(-t * 7)
    def cash(): t = tt(.6); return .22 * (np.sin(2*np.pi*2093*t) + np.sin(2*np.pi*2637*t)) * np.exp(-t * 6) * (t > .04) + ding()[:len(t)] * .0
    def sparkle(): t = tt(.7); return .14 * sum(np.sin(2*np.pi*f*t) * np.exp(-((t - k*.08) ** 2) / .0006) for k, f in enumerate([2637, 3136, 3520, 4186]))
    def thud(): t = tt(.3); return .6 * np.sin(2*np.pi*(90 - 40*t)*t) * np.exp(-t * 14)
    ci = 0
    for c in cues:
        k = c.get("k"); s_ = {"swoosh": sw, "tick": tick, "press": press, "pop": pop, "ding": ding, "whoosh": whoosh, "boing": boing, "cash": cash, "sparkle": sparkle, "thud": thud}.get(k, lambda: None)()
        if k == "chime": s_ = chime([880, 1174.7, 1318.5][ci % 3]); ci += 1
        if s_ is None: continue
        i = int(float(c["t"]) * sr); j = min(n, i + len(s_))
        if i < n: a[i:j] += s_[:j - i]
    s = (np.tanh(a * 1.2) * .85 * 32767).astype("int16")
    w = wave.open(path, "wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr)
    w.writeframes(np.stack([s, s], 1).tobytes()); w.close()


def 소리붙이기(mp4, 초, html, 분위기="fun", 이름=None):
    """music_plan 음악 + HTML 의 window.SFX 효과음 → 48kHz aac. 영상은 다시 인코딩하지 않는다."""
    import music_plan as MP
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch(); pg = b.new_page(); pg.goto("file://" + os.path.abspath(html))
        cues = pg.evaluate("() => window.SFX || []"); b.close()
    info = MP.choose(분위기, 이름 or os.path.splitext(os.path.basename(mp4))[0])
    MP.mux(mp4, [초], info, 91)                      # 음악(박자 맞춤)은 기존 도구 그대로
    if cues:
        wav = mp4 + ".sfx.wav"; _효과음(wav, 초, cues); tmp = mp4 + ".s.mp4"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", mp4, "-i", wav, "-filter_complex",
                        "[0:a]volume=0.7[m];[m][1:a]amix=inputs=2:duration=first:normalize=0[a]",
                        "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-ar", "48000", "-b:a", "160k",
                        "-movflags", "+faststart", tmp], check=True)
        os.replace(tmp, mp4); os.remove(wav)
    else:
        tmp = mp4 + ".r.mp4"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", mp4, "-c:v", "copy", "-c:a", "aac", "-ar", "48000",
                        "-b:a", "160k", "-movflags", "+faststart", tmp], check=True); os.replace(tmp, mp4)
    return info


def render_html(html, 나갈경로, 초, fps=30, ch="reel"):
    """motion_* 모듈이 부르는 이름(소리 없이 렌더만 — 음악은 부른 쪽이 MP.mux 로 붙인다). 돌려줌: 초."""
    out, secs = render(html, "_tmp_" + os.path.basename(나갈경로).rsplit(".", 1)[0], 초, fps, ch)
    os.makedirs(os.path.dirname(os.path.abspath(나갈경로)), exist_ok=True); shutil.move(out, 나갈경로); return secs


FXLOG = os.path.join(ROOT, "ads", "fx_log.json")


def 기법_검사(html, 이름, 기록=False):
    """11/10 대표 22:04 "같은 틀이라니 모션이 얼마나 많은데": HTML 의 window.FX(motion_fx.js 기법 이름)가
    앞 3편과 3개 넘게 겹치면 막는다. ZS_FX_OK=1 로만 건너뛴다. 기록=True 면 렌더 뒤 fx_log 에 적는다."""
    import re
    m = re.search(r"window\.FX\s*=\s*\[([^\]]*)\]", open(html, encoding="utf-8").read())
    if not m: return
    fx = [x.strip().strip("'\"") for x in m.group(1).split(",") if x.strip()]
    try: log = json.load(open(FXLOG, encoding="utf-8"))
    except Exception: log = []
    앞 = [x for x in log if x.get("name") != 이름][-3:]
    for x in 앞:
        겹 = sorted(set(fx) & set(x.get("fx", [])))
        if len(겹) > 3 and os.environ.get("ZS_FX_OK") != "1":
            raise SystemExit(f"[막음] 기법이 '{x['name']}' 와 {len(겹)}개 겹쳐요({'·'.join(겹)}). 3개까지만. motion_fx.js LIST 에서 다른 기법을 고르세요.")
    if 기록:
        log = [x for x in log if x.get("name") != 이름] + [{"name": 이름, "fx": fx}]
        json.dump(log, open(FXLOG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def 안전영역_막기(html, 초, ch="reel"):
    from playwright.sync_api import sync_playwright
    C = CS.CH[ch]
    with sync_playwright() as pw:
        b = pw.chromium.launch(); pg = b.new_page(viewport={"width": C["w"], "height": C["h"]}); pg.add_init_script(_spec_js(ch))
        pg.goto("file://" + os.path.abspath(html)); pg.wait_for_function("typeof window.seek === 'function'", timeout=15000)
        pg.evaluate("document.fonts.ready")
        src = open(html, encoding="utf-8").read(); frame = ".frame(" in src
        문제, 칸 = 안전영역_검사(pg, 초, ch); 문제 += 균형_검사(pg, 초, ch); b.close()
    canvas = "<canvas" in src
    if canvas and not frame: 문제.insert(0, "고정 요소 없음 — draw 끝에 F.frame(g) 를 부르세요(위 가운데 한 줄·AI 고지·zaoseon.com)")
    if 문제 and os.environ.get("ZS_SAFE_OK") != "1":
        raise SystemExit(f"[막음] 안전 영역·균형({ch}) — 글 칸 x {칸[0]}~{칸[2]}, y {칸[1]}~{칸[3]}:\n  " + "\n  ".join(문제[:30])
                         + "\n  (규격: pipeline/channel_specs.py. 가운데는 F.cx, 칸은 F.area())")


def render(html, 이름, 초=15.0, fps=30, ch="reel", 블러=1):
    금지_검사(html); 기법_검사(html, 이름); 안전영역_막기(html, 초, ch)
    C = CS.CH[ch]
    w, h = C["w"], C["h"]            # 크기는 channel_specs 에서 — 여기 숫자를 박지 않는다
    os.makedirs(OUT, exist_ok=True)
    tmp = tempfile.mkdtemp(prefix="htmlmo_")
    try:
        구역 = {z[0]: z[4] for z in C["zones"]}          # 구역 이름 → 아래 끝 y
        고정top = {z[0]: z[2] for z in C["zones"]}.get("하단 고정", h - 495)
        # 넘으면 안 되는 선은 **하단 고정 구역이 시작하는 자리**다. 전에는 brand_frame 의
        # bottom(=zaoseon.com 글자 줄, y1465)을 썼는데 고지 칸은 y1425 에서 시작해
        # 1441 까지 글이 내려와도 통과했다 — 실제로는 이미 겹친 상태였다(10/16).
        한계 = 고정top - 24
        n = asyncio.run(_shoot(html, 초, fps, w, h, tmp, 한계, 구역, 블러, ch))
        out = os.path.join(OUT, 이름 + ".mp4")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(fps),
                        "-i", os.path.join(tmp, "f%05d.png"),
                        "-vf", "format=yuv420p", "-c:v", "libx264", "-profile:v", "high",
                        "-crf", "16", "-preset", "medium",
                        "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
                        "-movflags", "+faststart", out], check=True)
        return out, n / fps
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main():
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    opt = lambda k, d=None: next((x.split("=", 1)[1] for x in sys.argv if x.startswith("--" + k + "=")), d)
    if any(x.startswith("--기법") for x in sys.argv):
        # 11/11 대표 "어떤 콘텐츠 만들든 상황이나 내용에 따라 사용할 수 있게": 상황별 기법 표(motion_fx.js FX.USE·LIST)
        js = os.path.join(HERE, "motion_fx.js")
        out = subprocess.run(["node", "-e", f"global.window={{}};require({json.dumps(js)});require({json.dumps(js.replace("motion_fx.js","motion_fx100.js"))});console.log(JSON.stringify({{u:window.FXK.USE,l:window.FXK.LIST}}))"], capture_output=True, text=True).stdout
        d = json.loads(out); want = opt("기법", "")
        for k, v in d["u"].items():
            if want and want not in k: continue
            print(f"[{k}]"); [print(f"  · {n} — {d['l'].get(n, '')}") for n in v]
        print("함수 쓰는 법·견본: 2026-reels-test/fx_gallery/ad.html, 목록 문서: zaoseon-site docs/모션_기법_목록_2026-11-11.md"); return 0
    if a and opt("확인"):
        print("확인 컷:", 확인컷(a[0], [float(x) for x in opt("확인").split(",")]))
        try: 안전영역_막기(a[0], float(opt("초", "15"))); print("안전 영역: 통과")
        except SystemExit as e: print(e)
        return 0
    if len(a) < 2:
        print(__doc__); return 1
    초 = float(next((x.split("=")[1] for x in sys.argv if x.startswith("--초=")), 15))
    fps = int(next((x.split("=")[1] for x in sys.argv if x.startswith("--fps=")), 30))
    p, d = render(a[0], a[1], 초, fps, 블러=int(opt("블러", "1")))
    기법_검사(a[0], a[1], 기록=True)
    if opt("출력"):
        os.makedirs(os.path.dirname(os.path.abspath(opt("출력"))), exist_ok=True); shutil.move(p, opt("출력")); p = opt("출력")
    if opt("소리", "fun") != "없음":
        mi = 소리붙이기(p, d, a[0], opt("소리", "fun"), a[1]); print(f"  음악: {mi['style']} {mi['bpm']}bpm {mi['key']} + 효과음")
    else:
        print("  [주의] 소리 없음 — 릴스·클립·광고로 내보내지 않는다(K-070)")
    print(f"  {p} · {d:.1f}초 · {fps}fps · {CH['w']}x{CH['h']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
