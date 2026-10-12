"""카드형 릴스(HTML 캔버스 슬라이드를 장면으로 쓰는 릴스) 자막 수집기 — sub_harvest 와 같은 형식의 장면표를 돌려준다(10/13).
reel_v2.render 가 쓰는 defs(d, override)를 같은 방식으로 그려 보며, 캔버스 fillText 호출을 가로채 '실제로 그려진 글 줄'을 모은다.
줄 = 같은 y의 글 조각을 x 순서로 이은 것, 덩어리 = 같은 글자 크기로 줄 간격이 1.8배 이내인 연속 줄. 상단 문구·주소·AI 고지(브랜드 글)는 뺀다.
최종 영상은 CTA 슬라이드(6번)를 R11 끝 장면으로 갈아 끼우므로(r11_tail) 6번 슬라이드는 장면에서 뺀다.
사용: import card_harvest as CH; CH.harvest_all() -> {이름: [장면표]}"""
import os, sys, re
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.abspath(os.path.join(HERE, "..")); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(R, "content"))
HOOK = """
(()=>{ window.__rec=[]; const P=CanvasRenderingContext2D.prototype; if(!P.__orig){ P.__orig=P.fillText; P.fillText=function(t,x,y,mw){ try{ const w=this.measureText(t).width; const a=this.textAlign; let x0=x; if(a==='center') x0=x-w/2; else if(a==='right') x0=x-w; window.__rec.push({t:String(t),x:x0,x1:x0+w,y:y,f:this.font}); }catch(e){} return P.__orig.apply(this,arguments); }; } })()
"""
BRAND = re.compile(r"^(자오선|동서양 6개 운명학 교차분석|zaoseon\.com|정월은 가상의 AI 캐릭터입니다)$|zaoseon|jeongwol")
SECS = {"S1": {0: 2.5, 1: 2.0, 2: 2.0, 3: 2.0, 5: 2.5, 6: 2.5}, "S2": {0: 2.2, 4: 2.2, 1: 2.0, 2: 2.0, 5: 2.4, 6: 2.4}, "S3": {0: 2.0, 1: 1.8, 2: 1.8, 3: 1.8, 5: 2.2, 6: 2.2}}
ORDER = {"S1": [0, 1, 2, 3, 5, 6], "S2": [0, 4, 1, 2, 5, 6], "S3": [0, 1, 2, 3, 5, 6]}
def _size(f):
    m = re.search(r"(\d+(?:\.\d+)?)px", f); return float(m.group(1)) if m else 0
def _blocks(rec):
    rows = {}
    for r in rec:
        if BRAND.search(r["t"].strip()): continue
        k = round(r["y"] / 6)
        rows.setdefault(k, []).append(r)
    lines = []
    for k in sorted(rows):
        rs = sorted(rows[k], key=lambda r: r["x"]); txt = ""; end = None
        for r in rs:
            txt += (" " if (end is not None and r["x"] - end > 3) else "") + r["t"].strip(); end = r["x1"]
        if txt.strip(): lines.append(dict(t=txt.strip(), y=sum(r["y"] for r in rs) / len(rs), s=max(_size(r["f"]) for r in rs)))
    out = []
    for ln in lines:
        if out and abs(out[-1]["size"] - ln["s"]) < 1 and ln["y"] - out[-1]["y"] <= ln["s"] * 1.8: out[-1]["lines"].append(ln["t"]); out[-1]["y"] = ln["y"]
        else: out.append(dict(lines=[ln["t"]], size=int(ln["s"]), y=ln["y"]))
    return [dict(lines=b["lines"], size=b["size"]) for b in out]
def harvest(page, d, ov, struct, tri):
    import carousel_editor as CE
    page.evaluate(CE.LAYOUT_JS, [d, None]); page.evaluate(CE.OVERRIDE_JS, ov); page.wait_for_timeout(100); page.evaluate(HOOK)
    order = [0, 1, 2, 3, 5, 6] if tri else ORDER[struct]; secs = SECS["S1"] if tri else SECS[struct]; res = []
    for n, si in enumerate([s for s in order if s != 6]):
        page.evaluate("window.__rec=[]"); page.evaluate(f"(()=>{{active={si}; draw(false);}})()"); rec = page.evaluate("window.__rec")
        res.append(dict(no=n + 1, dur=secs[si], blocks=_blocks(rec)))
    return res
def sets():
    """검사 대상 defs: {이름: (def, override, struct, tri)}"""
    import carousel_sets as CS, carousel_editor as CE, reel_plan as RP
    out = {}
    src = open(os.path.join(HERE, "gapeul_reels_v5.py"), encoding="utf-8").read().split("root=os.path.join")[0]; ns = {}; exec(compile(src, "gapeul", "exec"), ns)
    for k, (d, ov) in ns["igd"].items(): out["일간/" + k] = (d, {a: b for a, b in ov.items() if a != "_cfg"}, ov["_cfg"].get("struct", "S1"), False)
    import swap_reels_w43 as W, swap_reels_w43b as W2
    for mod in (W, W2):
        for k, (d, ov) in mod.defs.items(): out["사주밖/" + k] = (d, {a: b for a, b in ov.items() if a != "_cfg"}, "S1", True)
    return out
def harvest_all():
    import carousel_editor as CE
    from playwright.sync_api import sync_playwright
    import base64
    CE.build_html(); res = {}
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1300, "height": 900}); pg.goto("file:///tmp/editor_noto.html"); pg.wait_for_timeout(1500)
        pg.evaluate("Promise.all([400,500,600,700,900].map(w=>document.fonts.load(w+' 40px \"Noto Sans CJK KR\"','가한丁')))")
        for name, (d, ov, st, tri) in sets().items():
            k, u = CE.face_dataurl(d["face"])
            if k not in ("v1_lowbun", "v2_straight", "v3_ponytail", "v4_glasses", "v5_halfup_v2"): pg.evaluate("async ([k,u])=>{FACES[k]=u; const im=new Image(); im.src=u; await im.decode(); imgCache[k]=im;}", [k, u])
            res[name] = harvest(pg, d, ov, st, tri)
        b.close()
    return res
if __name__ == "__main__":
    import sub_rules as SR
    os.environ.setdefault("EDITOR_HTML", os.path.join(HERE, "assets", "carousel_editor_2026-10-03_v5.html"))
    allr = harvest_all(); tot = 0
    for name, sc in allr.items():
        r = SR.check("card/" + name, sc, "완화"); r += [("(엄격)",) + x for x in SR.check("card/" + name, sc, "엄격") if x not in r] if "--strict" in sys.argv else []
        print(name, "장면", len(sc), "위반", len(r))
        for x in r: print("   ", x)
        tot += len(r)
        if "--show" in sys.argv:
            for s in sc: print("   장면", s["no"], s["dur"], [(b["lines"], b["size"]) for b in s["blocks"]])
