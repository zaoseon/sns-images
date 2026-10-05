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
 let n; while(n=w.nextNode()){ const t=n.textContent.trim(); if(!t) continue; const e=n.parentElement; if(e.closest('[data-deco]')) continue; const cs=getComputedStyle(e);
  const r=document.createRange(); r.selectNodeContents(n); const b=r.getBoundingClientRect(); if(b.width<2) continue;
  out.push({t:t.slice(0,24),fs:parseFloat(cs.fontSize),fw:parseInt(cs.fontWeight),color:cs.color,lh:cs.lineHeight,x:b.left,y:b.top,w:b.width,h:b.height}); } return out; }"""
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
    # 전체 배치: 위쪽과 아래쪽을 다 써야 한다(가운데 몰림 방지)
    main=[e for e in els if not (e['y']>1150 and e['w']<520)]
    if main:
        top=min(e['y'] for e in main); bot=max(e['y']+e['h'] for e in main)
        if top>200: issues.append(f"{name}: 글자가 아래로 치우침(맨 위 글자 y={top:.0f}, 200 이내여야 함)")
        if bot<1050 and kind_hint!='cover': issues.append(f"{name}: 글자가 위로 몰림(맨 아래 글자 끝 y={bot:.0f}, 1050 이상이어야 함)")
    # 화면 밖으로 넘침, 글자끼리 겹침
    for e in els:
        if e['y']+e['h']>1325: issues.append(f"{name} 「{e['t']}」: 아래 여백 부족(끝 y={e['y']+e['h']:.0f}, 1325 이내여야 함)")
    for a_i in range(len(els)):
        for b_i in range(a_i+1,len(els)):
            a,b=els[a_i],els[b_i]
            ox=min(a['x']+a['w'],b['x']+b['w'])-max(a['x'],b['x']); oy=min(a['y']+a['h'],b['y']+b['h'])-max(a['y'],b['y'])
            if ox>4 and oy>4 and ox*oy>0.2*min(a['w']*a['h'],b['w']*b['h']): issues.append(f"{name}: 글자끼리 겹침 「{a['t']}」/「{b['t']}」")
    for e in els:
        if e['fw']<800: issues.append(f"{name} 「{e['t']}」: 글꼴 굵기 {e['fw']} (800 이상 필요)")
        try: ratio=float(e['lh'].replace('px',''))/e['fs']
        except Exception: ratio=None
        if ratio and e['h']>1.6*e['fs']:
            need=1.3 if e['fs']>=72 else 1.5
            if ratio<need: issues.append(f"{name} 「{e['t']}」: 줄간격 {ratio:.2f} (필요 {need} 이상)")
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
