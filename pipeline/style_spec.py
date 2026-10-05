"""피드 가독성 기준(10/5 대표 지시)과 자동 검사. 1080px 폭 기준 값이다.
사용: from style_spec import check_page; issues = await check_page(page, '이름')  (playwright 페이지에 그림을 올린 뒤 호출)"""
import io
from PIL import Image
SPEC = dict(
    title_min=72,        # 큰 제목
    body_min=40,         # 선택지·본문·결과 설명
    note_min=34,         # 보조 안내(질문, 주의 문구)
    micro_min=22,        # 계정 핸들·AI 표시 같은 고정 표기만
    contrast_text=4.5,   # 48px 미만 글자
    contrast_large=3.0,  # 48px 이상 글자
    line_title=(1.2, 1.3), line_body=(1.5, 1.7),
    margin_x=70,         # 좌우 안쪽 여백(그리드 잘림 대비)
)
JS = """() => { const out=[]; const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);
 let n; while(n=w.nextNode()){ const t=n.textContent.trim(); if(!t) continue; const e=n.parentElement; const cs=getComputedStyle(e);
  const r=document.createRange(); r.selectNodeContents(n); const b=r.getBoundingClientRect(); if(b.width<2) continue;
  out.push({t:t.slice(0,24),fs:parseFloat(cs.fontSize),color:cs.color,lh:cs.lineHeight,x:b.left,y:b.top,w:b.width,h:b.height}); } return out; }"""
def _rgb(s):
    p=[float(v) for v in s[s.index('(')+1:s.index(')')].split(',')[:3]]; return tuple(p)
def _lum(c):
    def f(v):
        v/=255; return v/12.92 if v<=0.03928 else ((v+0.055)/1.055)**2.4
    r,g,b=c; return 0.2126*f(r)+0.7152*f(g)+0.0722*f(b)
def contrast(a,b):
    la,lb=_lum(a),_lum(b); hi,lo=max(la,lb),min(la,lb); return (hi+0.05)/(lo+0.05)
async def check_page(pg, name, kind_hint=None):
    els=await pg.evaluate(JS); png=await pg.screenshot(type='png'); im=Image.open(io.BytesIO(png)).convert('RGB'); issues=[]
    for e in els:
        fs=e['fs']; col=_rgb(e['color']); tag=f"{name} 「{e['t']}」 {fs:.0f}px"; low=e['y']>1150
        if low and e['w']<520:      # 계정 핸들·AI 표시
            if fs<SPEC['micro_min']: issues.append(f"{tag}: 고정 표기는 {SPEC['micro_min']}px 이상")
        elif low:                    # 맨 아래 한 줄 안내(댓글 유도 등)
            if fs<SPEC['note_min']: issues.append(f"{tag}: 아래 안내는 {SPEC['note_min']}px 이상")
        elif e['y']<200 and fs>=SPEC['note_min']:
            pass                     # 맨 위 라벨
        elif fs<SPEC['body_min']:
            issues.append(f"{tag}: 본문은 {SPEC['body_min']}px 이상")
        if (e['x']<SPEC['margin_x']-30 or e['x']+e['w']>1080-SPEC['margin_x']+30) and fs>=SPEC['note_min']:
            issues.append(f"{tag}: 좌우 여백 {SPEC['margin_x']}px 안쪽을 벗어남")
        x0,y0,x1,y1=[int(max(0,v)) for v in (e['x'],e['y'],e['x']+e['w'],e['y']+e['h'])]
        x1=min(x1,1079); y1=min(y1,1349)
        if x1-x0<4 or y1-y0<4: continue
        reg=im.crop((x0,y0,x1,y1)); data=list(reg.getdata()); step=max(1,len(data)//4000)
        bg=[p for p in data[::step] if sum(abs(p[i]-col[i]) for i in range(3))>150]
        if len(bg)<20: continue
        bg.sort(key=lambda p:_lum(p)); med=bg[len(bg)//2]
        need=SPEC['contrast_large'] if fs>=48 else SPEC['contrast_text']
        c=contrast(col,med)
        if c<need: issues.append(f"{tag}: 대비 {c:.1f}:1, 필요 {need}:1")
    return issues
