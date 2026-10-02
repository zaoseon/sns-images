"""샘플 슬라이드에 편집기 값을 맞추는 도구: 편집기 그리기 코드로 직접 그려 보고 샘플과의 차이가 줄어드는 쪽으로 값을 옮긴다(좌표하강).
정 샘플에서 알려진 값(표지 1.2/230/800 등)을 거꾸로 맞춰 검증했다. 사용은 python3 pipeline/variant_fit.py <이름>"""
import os, sys, io, base64, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image
import carousel_editor as CE
from playwright.sync_api import sync_playwright

BASE = os.path.join(CE.ROOT, "samples", "carousel_2026-10-01")
EDITOR_NEW = "/mnt/user-data/outputs/artifacts/4c728a9e-f8e6-479f-b4cb-53a0b2b79d6f/index.html"

class Fitter:
    def __init__(self, pw):
        CE.EDITOR = EDITOR_NEW; CE.build_html()
        self.b = pw.chromium.launch(); self.pg = self.b.new_page(viewport={"width": 1300, "height": 900})
        self.pg.goto("file:///tmp/editor_noto.html"); self.pg.wait_for_timeout(2500)
        self.pg.evaluate("Promise.all([400,500,600,700,900].map(w=>document.fonts.load(w+' 40px \"Noto Sans CJK KR\"','가한丁')))"); self.pg.wait_for_timeout(500)
        add = {"chart_plate": "data:image/png;base64," + base64.b64encode(open(CE.PLATE, "rb").read()).decode()}
        for k in ("v6_winter", "v13_horn_glasses"):
            kk, u = CE.face_dataurl(k); add[kk] = u
        for k, u in add.items():
            self.pg.evaluate("async ([k,u])=>{FACES[k]=u; const im=new Image(); im.src=u; await im.decode(); imgCache[k]=im;}", [k, u])
    def setup(self, kind, fields):
        self.pg.evaluate("([kind,f])=>{globalCfg.applyAll=false;globalCfg.applyAllHandle=true;if(f.accent)globalCfg.accent=f.accent;slides.length=0;const s=defaultSlide(kind,1);const set=(o,p)=>{for(const k in p){if(p[k]&&typeof p[k]==='object'&&!Array.isArray(p[k])){o[k]=Object.assign(o[k]||{},p[k])}else o[k]=p[k]}};set(s,f);slides.push(s);active=0;}", [kind, fields])
    def render(self, patch):
        url = self.pg.evaluate("(p)=>{const s=slides[0];const set=(o,q)=>{for(const k in q){if(q[k]&&typeof q[k]==='object'&&!Array.isArray(q[k])){o[k]=Object.assign(o[k]||{},q[k])}else o[k]=q[k]}};set(s,p);active=0;draw(false);return cv.toDataURL('image/png');}", patch)
        return np.array(Image.open(io.BytesIO(base64.b64decode(url.split(',')[1]))).convert('RGB')).astype(np.int16)
    def close(self): self.b.close()

def get(d, path):
    for k in path.split('.'): d = d[k]
    return d
def put(d, path, v):
    ks = path.split('.'); o = d
    for k in ks[:-1]: o = o.setdefault(k, {})
    o[ks[-1]] = v

def fit(F, sample, kind, fixed, init, free, steps=(40, 20, 10, 5, 3, 2, 1), rounds=2, mask=None, log=print):
    ref = np.array(Image.open(sample).convert('RGB')).astype(np.int16)
    cur = json.loads(json.dumps(init))
    F.setup(kind, fixed)
    def score(p):
        img = F.render(json.loads(json.dumps({**{k: v for k, v in p.items()}})))
        d = np.abs(img - ref).mean(axis=2)
        return float((d if mask is None else d[mask]).mean())
    best = score(cur); log('시작', round(best, 2))
    for r in range(rounds):
        for st in steps:
            improved = True
            while improved:
                improved = False
                for name, lo, hi, unit in free:
                    v = get(cur, name); s = st * unit
                    for cand in (v + s, v - s):
                        if cand < lo or cand > hi: continue
                        trial = json.loads(json.dumps(cur)); put(trial, name, cand)
                        sc = score(trial)
                        if sc < best - 1e-4: best, cur, improved = sc, trial, True; break
        log(f'라운드 {r+1} 끝: {round(best,2)}')
    return cur, best
