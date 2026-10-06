"""장면(페이지)별 안전영역 겹쳐 보기 — 대표가 페이지마다 위치를 정해 주실 수 있게(10/6 대표 지시).
각 장: 영상의 실제 정지 화면 + 릴스 UI(빨강) + 네이버 클립 UI(주황) + 공통 안전 영역(초록 점선) + 캐러셀로 쓸 때(파랑) + 100px 눈금 + 안전 영역을 넘는 요소(자홍 상자).
사용: python3 pipeline/page_overlay.py  -> 2026-motion/pages/litho_p1.jpg ~ p7.jpg  (다른 영상은 PAGES와 모듈만 바꾸면 된다)"""
import os, sys, json, asyncio, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from PIL import Image, ImageDraw, ImageFont
import fonts_kit as K, brand_frame as BF
R = os.path.abspath(os.path.join(HERE, ".."))
SAFE = (50, 330, 900, 1470)
B = 0.645                                                       # 리소그래프 6판 박자 간격(초)
PAGES = [("p1", "1 표지·훅", 4.2), ("p2", "2 정월 설명 ①", 9.5), ("p3", "3 정월 설명 ② 같은 말", 13.0), ("p4", "4 정월 설명 ③ 다른 말", 16.4), ("p5", "5 12별자리 순위", 25.3), ("p6", "6 마무리 ① 댓글", 28.2), ("p7", "7 마무리 ② 팔로우·홈페이지", 35.0)]
FONT = lambda sz: ImageFont.truetype(K.P["pr_xb"], sz)
async def dom_boxes():
    """같은 박자의 HTML을 열어 요소 위치를 잰다(영상 v3은 우측 고정 요소가 x 960이라 같은 값으로 맞춘다)."""
    import motion_litho_star as M
    from playwright.async_api import async_playwright
    open("/tmp/page_dom.html", "w", encoding="utf-8").write(M.html(B))   # 현재 brand_frame(우측 x 900) 기준 — 영상 v4와 같다
    JS = r"""()=>{const out=[];const skip=new Set(['bg','chart','sun','moon','stars']);document.querySelectorAll('body *').forEach(e=>{
      if(skip.has(e.id)||e.closest('#stars')||e.tagName==='SCRIPT'||e.tagName==='STYLE'||e.tagName==='path'||e.tagName==='circle'||e.tagName==='svg'&&e.id==='stars')return;
      const cs=getComputedStyle(e); if(parseFloat(cs.opacity)<0.35||cs.display==='none')return; let p=e.parentElement,op=1; while(p&&p!==document.body){op*=parseFloat(getComputedStyle(p).opacity);p=p.parentElement}
      if(op<0.35)return; let r=e.getBoundingClientRect(); const txt=(e.childElementCount===0||e.classList.contains('bt')||e.classList.contains('t')||e.classList.contains('xt')||e.classList.contains('xban'))?(e.textContent||'').trim():''; if(txt&&!['c','bar','chip','tok','avatar','bub'].some(c=>e.classList.contains(c))&&!/^(chip\d|bub|jw)$/.test(e.id)){const rg=document.createRange();rg.selectNodeContents(e);const rr=rg.getBoundingClientRect();if(rr.width>0)r=rr} if(r.width<8||r.height<8||r.width>1070&&r.height>1900)return; const isShape=['c','bar','chip','tok','avatar','bub'].some(c=>e.classList.contains(c))||['fcard','fbtn','jw','bub','tkP','tkB'].includes(e.id)||/^chip\d$/.test(e.id);
      if(!txt&&!isShape)return; out.push({id:e.id||e.className.toString().split(' ')[0],t:txt.slice(0,14),x0:r.left,y0:r.top,x1:r.right,y1:r.bottom})});return out}"""
    res = {}
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 1080, "height": 1920}); await pg.goto("file:///tmp/page_dom.html"); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(500)
        for k, n, beat in PAGES:
            await pg.evaluate(f"seek({beat * B * 1000})"); await pg.wait_for_timeout(200); res[k] = await pg.evaluate(JS)
        await b.close()
    return res
def violations(boxes):
    v = []
    for e in boxes:
        if e["id"].startswith("bf") or e["id"] in ("hl",) and False: pass
        out = []
        if e["x1"] > SAFE[2] + 2: out.append(f'오른쪽 끝 x {e["x1"]:.0f}')
        if e["x0"] < SAFE[0] - 2: out.append(f'왼쪽 끝 x {e["x0"]:.0f}')
        if e["y1"] > SAFE[3] + 2 and not e["id"].startswith("bf"): out.append(f'아래 끝 y {e["y1"]:.0f}')
        if e["y0"] < SAFE[1] - 2 and not e["id"].startswith("bf") and e["id"] not in ("bfTag",): out.append(f'위 y {e["y0"]:.0f}')
        if out: v.append((e, out))
    return v

def center_issues(boxes, tol=10):
    """카드(fcard)·말풍선(bub) 안 글 묶음이 박스 가운데에 있는지(R18). 반환: [(박스, 설명)]"""
    out = []
    for sh in boxes:
        if sh["id"] not in ("fcard", "bub"): continue
        ins = [t for t in boxes if t is not sh and t["t"] and t["x0"] >= sh["x0"] - 2 and t["x1"] <= sh["x1"] + 2 and t["y0"] >= sh["y0"] + 8 and t["y1"] <= sh["y1"] + 2 and not t["id"].startswith("bf")]   # 테두리에 걸친 이름표(정월)는 본문이 아님
        if not ins: continue
        ux0 = min(t["x0"] for t in ins); uy0 = min(t["y0"] for t in ins); ux1 = max(t["x1"] for t in ins); uy1 = max(t["y1"] for t in ins)
        top, bot, lef, rig = uy0 - sh["y0"], sh["y1"] - uy1, ux0 - sh["x0"], sh["x1"] - ux1
        if abs(top - bot) > tol: out.append((sh, [f"글이 세로로 치우침(위 {top:.0f}px · 아래 {bot:.0f}px)"]))
        if abs(lef - rig) > (tol if sh["id"] == "fcard" else 40): out.append((sh, [f"글이 가로로 치우침(왼쪽 {lef:.0f}px · 오른쪽 {rig:.0f}px)"]))
    return out
def draw(im, title, viol):
    W, H = im.size; base = im.convert("RGBA"); ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    RED, ORG, TEAL, BLUE, MAG = (255, 80, 80), (255, 170, 60), (127, 214, 200), (110, 170, 255), (255, 60, 200)
    # 인스타 릴스 UI(빨강): 위 250 · 아래 450 · 오른쪽 120
    for b in ((0, 0, W, 250), (0, 1470, W, H), (960, 250, W, 1470)): d.rectangle(b, fill=RED + (70,))
    # 네이버 클립 UI(주황): 뒤로·소리, 오른쪽 버튼 줄, 하단 프로필·설명·링크 칩, 진행 막대 선
    for b in ((40, 50, 100, 130), (945, 50, 1040, 130), (905, 830, W, 1830), (45, 1489, 810, 1850)): d.rectangle(b, outline=ORG + (255,), width=7, fill=ORG + (45,))
    d.line([(0, 1876), (W, 1876)], fill=ORG + (255,), width=5)
    # 캐러셀로 쓸 때(파랑): 격자 3:4(y 240~1680), 피드 4:5(y 285~1635), 4:5 안전(좌우 55·위아래 55)
    for y in (240, 1680): d.line([(0, y), (W, y)], fill=BLUE + (255,), width=5)
    for y in (285, 1635): d.line([(0, y), (W, y)], fill=(160, 120, 255, 255), width=4)
    x0, y0, x1, y1 = 55, 340, 1025, 1580
    for (a, b, c, e) in ((x0, y0, x1, y0), (x1, y0, x1, y1), (x1, y1, x0, y1), (x0, y1, x0, y0)):
        steps = int(max(abs(c - a), abs(e - b)) // 22)
        for i in range(0, steps, 2): d.line([(a + (c - a) * i / steps, b + (e - b) * i / steps), (a + (c - a) * (i + 1) / steps, b + (e - b) * (i + 1) / steps)], fill=BLUE + (255,), width=5)
    # 공통 안전 영역(초록 점선)
    sx0, sy0, sx1, sy1 = SAFE
    for (a, b, c, e) in ((sx0, sy0, sx1, sy0), (sx1, sy0, sx1, sy1), (sx1, sy1, sx0, sy1), (sx0, sy1, sx0, sy0)):
        steps = int(max(abs(c - a), abs(e - b)) // 24)
        for i in range(0, steps, 2): d.line([(a + (c - a) * i / steps, b + (e - b) * i / steps), (a + (c - a) * (i + 1) / steps, b + (e - b) * (i + 1) / steps)], fill=TEAL + (255,), width=7)
    # 100px 눈금
    f26 = FONT(28)
    for y in range(100, H, 100):
        d.line([(0, y), (W, y)], fill=(255, 255, 255, 38), width=1); t = str(y); w = d.textlength(t, font=f26); d.rectangle((2, y - 17, 2 + w + 12, y + 17), fill=(0, 0, 0, 150)); d.text((8, y - 15), t, font=f26, fill=(255, 235, 120, 255))
    for x in range(100, W, 100):
        d.line([(x, 0), (x, H)], fill=(255, 255, 255, 30), width=1); t = str(x); w = d.textlength(t, font=f26); d.rectangle((x - w / 2 - 6, H - 40, x + w / 2 + 6, H - 6), fill=(0, 0, 0, 150)); d.text((x - w / 2, H - 38), t, font=f26, fill=(255, 235, 120, 255))
    # 안전 영역을 넘는 요소(자홍 상자)
    for e, why in viol:
        d.rectangle((e["x0"], e["y0"], e["x1"], e["y1"]), outline=MAG + (255,), width=6)
    # 제목칩과 범례
    f44, f34 = FONT(44), FONT(34); tw = d.textlength(title, font=f44); d.rounded_rectangle((38, 52, 38 + tw + 40, 120), 24, fill=(0, 0, 0, 200)); d.text((58, 60), title, font=f44, fill=(231, 200, 141, 255))
    d.rounded_rectangle((20, 1560, W - 20, 1850), 24, fill=(0, 0, 0, 215))
    rows = [(RED, "빨강 = 인스타 릴스 UI (위 250 · 아래 450 · 오른쪽 120)"), (ORG, "주황 = 네이버 클립 UI (오른쪽 버튼 줄 x 905~ · 아래 y 1489~)"), (TEAL, "초록 점선 = 공통 안전 영역 x 50~900 · y 330~1470"), (BLUE, "파랑 = 캐러셀로 쓸 때 (3:4 격자 · 4:5 · 안전 점선)"), (MAG, f"자홍 상자 = 안전 영역을 넘는 요소 {len(viol)}개")]
    for i, (c, t) in enumerate(rows):
        yy = 1578 + i * 54; d.rectangle((44, yy + 8, 84, yy + 32), fill=c + (255,)); d.text((100, yy), t, font=f34, fill=(255, 255, 255, 255))
    return Image.alpha_composite(base, ov).convert("RGB")
async def main():
    boxes = await dom_boxes(); os.makedirs(os.path.join(R, "2026-motion", "pages"), exist_ok=True); report = {}
    for k, n, beat in PAGES:
        still = Image.open(f"/tmp/still_{k}.png").convert("RGB"); v = violations(boxes[k]) + center_issues(boxes[k]); out = draw(still, f"페이지 {n}", v)
        out.save(os.path.join(R, "2026-motion", "pages", f"litho_{k}.jpg"), quality=90)
        report[k] = [f'{e["id"]}「{e["t"]}」 ' + ", ".join(w) for e, w in v]
    json.dump(report, open("/tmp/page_report.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for k, n, _ in PAGES: print(k, n, "→ 넘는 요소", len(report[k]))
if __name__ == "__main__":
    asyncio.run(main())
