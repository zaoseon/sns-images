"""카드 3장 세트 v3 (10/5 대표 지적: 줄간격 붙음·글꼴 얇음·가운데 몰림·배경/캐릭터 한 가지만 씀).
- 전체 화면을 쓴다(위아래 검은 띠 없음). 제목은 위, 설명은 아래로 나눠 놓는다.
- 글꼴은 Noto Sans CJK KR Black(900), 줄간격 제목 1.4 · 본문 1.9.
- 배경(우주 사진·새 인트로 하늘·6체계 차트)과 정월 사진(14종 + 새 캐릭터)을 세트마다 다르게 돌려 쓴다.
사용: python3 pipeline/card_kit.py"""
import base64, asyncio, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style_spec import check_page
import fonts_kit as K, brand_frame as BF
from playwright.async_api import async_playwright
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
def b64(p): return base64.b64encode(open(os.path.join(R, p), 'rb').read()).decode()
SUN = b64('characters/cut/bg_sunmoon.jpg'); SKY = b64('meridian_intro/src/assets/sky.png'); CHART = b64('meridian_intro/src/assets/chart.svg')
INTRO = b64('meridian_intro/src/assets/character.png')
def face_b64(n): return INTRO if n == 'intro' else b64(f'characters/cut/{n}.png')
F = f"font-family:{K.D};font-weight:900"   # 제목=페이퍼로지(또는 G마켓 산스), 본문 요소에만 프리텐다드(K.B)를 따로 지정한다
CUR = 'pl'
def bg(kind, acc):
    if kind == 'sun':   return f"background:#0e0c18 url(data:image/jpeg;base64,{SUN}) center/cover", '<div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(6,6,16,.45),rgba(6,6,16,.72))"></div>'
    if kind == 'sky':   return f"background:#050912 url(data:image/png;base64,{SKY}) center/cover", '<div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(2,4,10,.2),rgba(2,4,10,.55))"></div>'
    if kind == 'chart': return "background:#070b16", f'<img src="data:image/svg+xml;base64,{CHART}" style="position:absolute;left:-210px;top:150px;width:1500px;opacity:.30"><div style="position:absolute;inset:0;background:radial-gradient(circle at 50% 45%,rgba(7,11,22,.15),rgba(7,11,22,.8))"></div>'
    if kind == 'ink':   return "background:#0b0806", f'<div style="position:absolute;inset:0;background:radial-gradient(circle at 80% 85%,{acc}33,transparent 55%)"></div>'
def handle(acc, right=False): return f'<div style="position:absolute;{"right:55px" if right else "left:55px"};bottom:46px;display:flex;align-items:center;gap:14px;font-size:34px;font-family:{K.B};font-weight:800;color:#fff;z-index:6"><span style="width:34px;height:34px;border-radius:50%;background:{acc};display:inline-block"></span>zaoseon.com</div>'
def ai_note(left=False): return '<div style="position:absolute;' + ('left:46px;text-align:left' if left else 'right:46px;text-align:right') + ';bottom:36px;font-size:23px;font-family:{K.B};font-weight:800;color:#fff;line-height:1.4;z-index:6;background:rgba(0,0,0,.65);padding:8px 14px;border-radius:12px">※ 자오선의 상담가 정월은<br>AI로 생성한 가상 캐릭터입니다</div>'
STRETCH = """()=>{const f=(1440-120)/(1350-120);document.body.querySelectorAll(':scope > *').forEach(e=>{if(getComputedStyle(e).position!=='absolute')return;const t=e.style.top;if(!t||!t.endsWith('px'))return;const v=parseFloat(t);if(v>=200)e.style.top=(120+(v-120)*f)+'px'})}"""   # 3:4(1080x1440): 4:5로 짠 배치를 위아래로 고르게 늘린다(10/6 R16)
def frame(ai=False): return BF.html('card', ai=ai, stacked=True)
def page(inner, bgkind, acc):
    st, ov = bg(bgkind, acc); return f'<html><head><meta charset="utf-8"><style>{K.css(CUR)}{BF.css()}</style></head><body style="margin:0;width:1080px;height:1440px;position:relative;overflow:hidden;{F};color:#fff;word-break:keep-all;line-break:strict;{st}">{ov}{inner}</body></html>'
def img_tag(fc, h, pos, flip=False, z=2, extra=''):
    tf = 'transform:scaleX(-1);' if flip else ''
    return f'<img src="data:image/png;base64,{face_b64(fc)}" style="position:absolute;{pos};height:{h}px;{tf}z-index:{z};{extra}">'
def halo(acc, cx, cy, r=330): return f'<div style="position:absolute;left:{cx-r}px;top:{cy-r}px;width:{2*r}px;height:{2*r}px;border-radius:50%;border:6px solid {acc};opacity:.7;z-index:1"></div><div style="position:absolute;left:{cx-r+40}px;top:{cy-r+40}px;width:{2*r-80}px;height:{2*r-80}px;border-radius:50%;background:radial-gradient(circle,{acc}55,transparent 70%);z-index:1"></div>'
def sparkles(acc): return ''.join(f'<div data-deco="1" style="position:absolute;left:{x}px;top:{y}px;font-size:{fs}px;color:{acc};z-index:4">✦</div>' for x,y,fs in ((920,380,54),(980,520,34),(120,1020,46),(900,980,36)))
def phone(acc, x, y):   # 소품: 휴대폰과 대화 말풍선
    return f'''<div data-deco="1" style="position:absolute;left:{x}px;top:{y}px;width:330px;height:560px;border:8px solid #e9e4dc;border-radius:48px;background:rgba(8,8,18,.78);z-index:3;transform:rotate(6deg)">
<div style="position:absolute;left:24px;top:60px;width:230px;background:#fff;color:#111;font-size:30px;font-family:{K.B};font-weight:800;line-height:1.5;padding:14px 20px;border-radius:24px 24px 24px 6px">읽었어요 ✓</div>
<div style="position:absolute;right:24px;top:190px;width:200px;background:{acc};color:#111;font-size:30px;font-family:{K.B};font-weight:800;line-height:1.5;padding:14px 20px;border-radius:24px 24px 6px 24px">…</div>
<div style="position:absolute;left:24px;top:320px;width:150px;background:#fff;color:#111;font-size:30px;font-family:{K.B};font-weight:800;padding:14px 20px;border-radius:24px 24px 24px 6px">곧 답할게</div></div>'''
def bubble(acc, text, x, y, w=420): return f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;background:#fff;color:#111;font-size:44px;font-family:{K.B};font-weight:800;line-height:1.5;padding:22px 30px;border-radius:36px;z-index:6">{text}<div style="position:absolute;left:60px;bottom:-26px;width:0;height:0;border-left:26px solid transparent;border-right:26px solid transparent;border-top:36px solid #fff"></div></div>'
def cover(c):
    acc = c['acc']; L = c.get('cl', 'br'); fc = c['face']; big = fc == 'intro'
    head = f'''<div style="position:absolute;left:75px;top:122px;background:{acc};color:#111;font-size:44px;padding:14px 42px;border-radius:60px;z-index:5">{c['badge']}</div>'''
    sh = 'text-shadow:0 4px 18px rgba(0,0,0,.55)'
    if L == 'br':       # 오른쪽 아래, 제목은 왼쪽 위
        ink = head + f'<div style="position:absolute;left:90px;top:232px;width:820px;font-size:56px;line-height:1.45;color:{acc};z-index:5">{c["sub"]}</div><div style="position:absolute;left:90px;top:470px;width:900px;font-size:108px;line-height:1.35;z-index:5;{sh}">{c["title"]}</div>' + img_tag(fc, 820 if big else 800, f'right:{-40 if big else -150}px;bottom:0')
    elif L == 'bl':     # 좌우 반전, 왼쪽 아래, 제목은 오른쪽 정렬
        ink = head + f'<div style="position:absolute;right:90px;top:232px;width:820px;text-align:right;font-size:56px;line-height:1.45;color:{acc};z-index:5">{c["sub"]}</div><div style="position:absolute;right:90px;top:470px;width:900px;text-align:right;font-size:108px;line-height:1.35;z-index:5;{sh}">{c["title"]}</div>' + img_tag(fc, 820 if big else 800, f'left:{-150 if not big else -40}px;bottom:0', flip=True)
    elif L == 'bc':     # 가운데 크게 + 둥근 후광, 제목은 위 가운데
        ink = head + f'<div style="position:absolute;left:0;right:0;top:232px;text-align:center;font-size:56px;line-height:1.45;color:{acc};z-index:5">{c["sub"]}</div><div style="position:absolute;left:0;right:0;top:360px;text-align:center;font-size:108px;line-height:1.35;z-index:5;{sh}">{c["title"]}</div>' + halo(acc, 540, 1060) + img_tag(fc, 780, 'left:50%;margin-left:-' + str(290 if not big else 330) + 'px;bottom:-70px')
    elif L == 'tr':     # 오른쪽 위에 걸쳐 있고 말풍선, 제목은 왼쪽 아래
        ink = head.replace('left:75px','left:75px') + img_tag(fc, 690, 'right:-60px;top:176px', flip=False) + bubble(acc, c.get('bubble', '어느 쪽일까요?'), 90, 240, 420) + f'<div style="position:absolute;left:90px;top:810px;width:900px;font-size:56px;line-height:1.45;color:{acc};z-index:5">{c["sub"]}</div><div style="position:absolute;left:90px;top:980px;width:900px;font-size:100px;line-height:1.35;z-index:5;{sh}">{c["title"]}</div>'
    elif L == 'phone':  # 소품(휴대폰) + 작은 얼굴 아래 왼쪽
        ink = head + f'<div style="position:absolute;left:90px;top:232px;width:820px;font-size:56px;line-height:1.45;color:{acc};z-index:5">{c["sub"]}</div><div style="position:absolute;left:90px;top:470px;width:900px;font-size:108px;line-height:1.35;z-index:5;{sh}">{c["title"]}</div>' + phone(acc, 690, 780) + img_tag(fc, 620, 'left:-110px;bottom:0', flip=True)
    leftchar = L in ('bl', 'phone')
    return page(ink + sparkles(acc) + frame(True), c['bg'], acc)
def options(c):
    acc = c['acc']; ql = c.get('ql', 'rows'); head = f'<div style="position:absolute;left:75px;top:122px;background:{acc};color:#111;font-size:44px;padding:14px 42px;border-radius:60px;z-index:5">선택지</div><div style="position:absolute;left:90px;top:210px;width:900px;font-size:100px;line-height:1.4;z-index:5;text-shadow:0 4px 18px rgba(0,0,0,.55)">{c["q"]}</div>'
    foot = f'<div style="position:absolute;left:0;right:0;top:1150px;text-align:center;font-size:44px;font-family:{K.B};font-weight:800;color:{acc};z-index:5">고른 번호를 세어 보세요</div>'
    if ql == 'cards':    # 세로 카드 세 장
        cards = ''.join(f'<div style="position:absolute;left:{70+i*315}px;top:520px;width:295px;height:560px;background:rgba(10,10,24,.66);border:3px solid {acc};border-radius:36px;z-index:5;padding:30px 24px;box-sizing:border-box;text-align:center;display:flex;flex-direction:column;justify-content:center;align-items:center"><div style="margin:0 0 30px;width:96px;height:96px;border-radius:50%;background:{acc};color:#111;font-size:64px;display:flex;align-items:center;justify-content:center">{i+1}</div><div style="font-size:42px;font-family:{K.B};font-weight:800;line-height:1.6">{t}</div></div>' for i, t in enumerate(c['opts_short']))
        ink = head + cards + foot
    else:                 # 가로 줄 세 개 (+ 얼굴이 오른쪽 아래에서 빼꼼)
        rows = ''.join(f'<div style="position:absolute;left:70px;right:70px;top:{500+i*210}px;height:180px;background:rgba(10,10,24,.62);border:3px solid {acc};border-radius:36px;display:flex;align-items:center;gap:32px;padding:0 38px;z-index:5"><span style="flex:none;width:92px;height:92px;border-radius:50%;background:{acc};color:#111;font-size:60px;display:flex;align-items:center;justify-content:center">{i+1}</span><span style="font-size:46px;font-family:{K.B};font-weight:800;line-height:1.5">{t}</span></div>' for i, t in enumerate(c['opts']))
        peek = img_tag(c['peek'], 360, 'right:-30px;top:60px', flip=bool(c.get('peek_flip')), z=3) if c.get('peek') else ''
        ink = head + rows + foot + peek
    return page(ink + frame(False), c['bg2'], acc)
def result(c):
    acc = c['acc']; fc = c.get('face2'); rl = c.get('rl', 'br')
    img = ''
    if fc and rl == 'br': img = img_tag(fc, 380, 'right:-60px;bottom:0', z=3)
    elif fc and rl == 'bl': img = img_tag(fc, 380, 'left:-60px;bottom:0', flip=True, z=3)
    elif fc and rl == 'tr': img = img_tag(fc, 420, 'right:-70px;top:150px', z=3)
    cta_l = '300px' if rl == 'bl' and fc else '70px'
    ink = f'''<div style="position:absolute;left:75px;top:122px;background:{acc};color:#111;font-size:44px;padding:14px 42px;border-radius:60px;z-index:5">결과</div>
<div style="position:absolute;left:90px;top:210px;width:900px;font-size:100px;line-height:1.4;z-index:5;text-shadow:0 4px 18px rgba(0,0,0,.55)">{c['rt']}</div>
<div style="position:absolute;left:70px;top:470px;width:900px;background:rgba(10,10,24,.66);border-radius:36px;padding:44px 48px;font-size:46px;font-family:{K.B};font-weight:800;line-height:1.9;z-index:5;box-sizing:border-box">{c['body']}</div>{img}
<div style="position:absolute;left:{cta_l};right:{'70px' if not (fc and rl=='br') else '240px'};top:1090px;height:110px;background:{acc};color:#111;border-radius:60px;display:flex;align-items:center;justify-content:center;font-size:46px;z-index:5">{c['cta']}</div>'''
    return page(ink + frame(fc is not None), c['bg3'], acc)
SETS = {
 'a_1009': dict(acc='#ff8a73', face='v5_halfup', cl='bc', ql='cards', opts_short=['식으면<br>정리가<br>빨라요', '좋아하면<br>먼저<br>표현해요', '뒤돌아본<br>적이<br>드물어요'], rl='bl', bg='sky', badge='정월의 연애 테스트', sub='한 번 정하면 뒤돌아보지 않는 나', title='연애에서도<br>몇 개 해당되나요?',
    bg2='chart', q='세 가지 중<br>몇 개인가요?', opts=['마음이 식으면 정리가 빨라요', '좋아하면 먼저 표현해요', '헤어진 뒤 뒤돌아본 적이 드물어요'],
    bg3='sun', face2='v8_gesture', rt='2개 이상이라면', body='확신이 빠른 만큼 상대는<br>갑작스럽게 느낄 수 있어요.<br>정리하기 전에 이유를<br>한 문장으로 말해 주세요.', cta='내 숫자를 댓글로 남겨 주세요'),
 'b_1011': dict(acc='#f6b042', face='intro', cl='tr', bubble='먼저 말할까,<br>기다릴까요?', ql='rows', peek='v11_mug', peek_flip=True, rl='tr', bg='chart', badge='정월의 관계 테스트', sub='먼저 말하지 못하고<br>기다리다 놓친 사람이 있다면', title='나는 몇 개<br>해당되나요?',
    bg2='sun', q='세 가지 중<br>몇 개인가요?', opts=['상대가 먼저 말해 주길 기다려요', '말할까 고민하다 때를 놓친 적 있어요', '놓치고 나서야 말할걸 생각해요'],
    bg3='sky', face2='v3_ponytail', rt='2개 이상이라면', body='말이 느린 게 아니라<br>거절을 먼저 헤아리는 쪽일 수 있어요.<br>이번 주에 안부 한 줄을 먼저 보내 보세요.', cta='내 숫자를 댓글로 남겨 주세요'),
 'd_1023': dict(acc='#7fd6c8', face='v4_glasses', cl='phone', ql='rows', peek=None, rl='br', bg='ink', badge='정월의 연락 테스트', sub='읽고 답장하기까지 걸리는 시간', title='나는 어느 쪽에<br>가까울까요?',
    bg2='sky', q='세 가지 중<br>어느 쪽인가요?', opts=['메시지가 오면 바로 답해야 편해요', '답장을 썼다 지웠다 하다 늦게 보내요', '읽고 이따 답해야지 하고 잊어요'],
    bg3='chart', face2='v13_horn_glasses', rt='많이 고른 번호는요', body='1번은 바로 답하는 쪽,<br>2번은 다듬어 보내는 쪽,<br>3번은 천천히 답하는 쪽이에요.<br>빠르다 느리다가 아니라<br>연락의 리듬이에요.', cta='내 번호를 댓글로 남겨 주세요'),
}
async def main():
    out = os.path.join(R, '2026-w43swap', 'cards'); os.makedirs(out, exist_ok=True); bad = 0
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 1080, 'height': 1440})
        global CUR
        for k, c in SETS.items():
            txt = ''.join(str(v) if not isinstance(v, (list, tuple)) else ''.join(v) for v in c.values() if isinstance(v, (str, list, tuple))); CUR = K.pick_display([txt], 'pl'); print(k, '제목 글꼴:', '페이퍼로지' if CUR == 'pl' else 'G마켓 산스')
            for i, fn in enumerate((cover, options, result), 1):
                open('/tmp/card_kit.html', 'w', encoding='utf-8').write(fn(c)); await pg.goto('file:///tmp/card_kit.html'); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(350)
                for x in await check_page(pg, f'{k}_{i}', 'cover' if i == 1 else None): print('검사:', x); bad += 1
                await pg.evaluate(STRETCH); await pg.screenshot(path=os.path.join(out, f'{k}_{i}.jpg'), type='jpeg', quality=92)
        await b.close()
    print('검사 문제', bad, '건')
if __name__ == '__main__': asyncio.run(main())
