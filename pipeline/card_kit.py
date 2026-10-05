"""카드 3장 세트 v3 (10/5 대표 지적: 줄간격 붙음·글꼴 얇음·가운데 몰림·배경/캐릭터 한 가지만 씀).
- 전체 화면을 쓴다(위아래 검은 띠 없음). 제목은 위, 설명은 아래로 나눠 놓는다.
- 글꼴은 Noto Sans CJK KR Black(900), 줄간격 제목 1.4 · 본문 1.9.
- 배경(우주 사진·새 인트로 하늘·6체계 차트)과 정월 사진(14종 + 새 캐릭터)을 세트마다 다르게 돌려 쓴다.
사용: python3 pipeline/card_kit.py"""
import base64, asyncio, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style_spec import check_page
from playwright.async_api import async_playwright
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
def b64(p): return base64.b64encode(open(os.path.join(R, p), 'rb').read()).decode()
SUN = b64('characters/cut/bg_sunmoon.jpg'); SKY = b64('meridian_intro/src/assets/sky.png'); CHART = b64('meridian_intro/src/assets/chart.svg')
INTRO = b64('meridian_intro/src/assets/character.png')
def face_b64(n): return INTRO if n == 'intro' else b64(f'characters/cut/{n}.png')
F = "font-family:'Noto Sans CJK KR','Noto Sans KR',sans-serif;font-weight:900"
def bg(kind, acc):
    if kind == 'sun':   return f"background:#0e0c18 url(data:image/jpeg;base64,{SUN}) center/cover", '<div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(6,6,16,.45),rgba(6,6,16,.72))"></div>'
    if kind == 'sky':   return f"background:#050912 url(data:image/png;base64,{SKY}) center/cover", '<div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(2,4,10,.2),rgba(2,4,10,.55))"></div>'
    if kind == 'chart': return "background:#070b16", f'<img src="data:image/svg+xml;base64,{CHART}" style="position:absolute;left:-210px;top:150px;width:1500px;opacity:.30"><div style="position:absolute;inset:0;background:radial-gradient(circle at 50% 45%,rgba(7,11,22,.15),rgba(7,11,22,.8))"></div>'
    if kind == 'ink':   return "background:#0b0806", f'<div style="position:absolute;inset:0;background:radial-gradient(circle at 80% 85%,{acc}33,transparent 55%)"></div>'
def handle(acc): return f'<div style="position:absolute;left:55px;bottom:46px;display:flex;align-items:center;gap:14px;font-size:34px;color:#fff;z-index:6"><span style="width:34px;height:34px;border-radius:50%;background:{acc};display:inline-block"></span>zaoseon.com</div>'
AI = '<div style="position:absolute;right:46px;bottom:36px;text-align:right;font-size:23px;color:#fff;line-height:1.4;z-index:6;background:rgba(0,0,0,.65);padding:8px 14px;border-radius:12px">※ 자오선의 상담가 정월은<br>AI로 생성한 가상 캐릭터입니다</div>'
def page(inner, bgkind, acc):
    st, ov = bg(bgkind, acc); return f'<html><body style="margin:0;width:1080px;height:1350px;position:relative;overflow:hidden;{F};color:#fff;{st}">{ov}{inner}</body></html>'
def cover(c):
    acc = c['acc']; fc = face_b64(c['face']); big = c['face'] == 'intro'
    img = f'<img src="data:image/png;base64,{fc}" style="position:absolute;right:{-40 if big else -150}px;bottom:0;height:{820 if big else 800}px;z-index:2">'
    ink = f'''<div style="position:absolute;left:75px;top:80px;background:{acc};color:#111;font-size:44px;padding:14px 42px;border-radius:60px;z-index:5">{c['badge']}</div>
<div style="position:absolute;left:90px;top:232px;width:820px;font-size:56px;line-height:1.45;color:{acc};z-index:5">{c['sub']}</div>
<div style="position:absolute;left:90px;top:{c.get('ty',470)}px;width:900px;font-size:108px;line-height:1.35;z-index:5;text-shadow:0 4px 18px rgba(0,0,0,.55)">{c['title']}</div>{img}{handle(acc)}{AI}'''
    return page(ink, c['bg'], acc)
def options(c):
    acc = c['acc']; rows = ''.join(f'<div style="position:absolute;left:70px;right:70px;top:{500+i*210}px;height:180px;background:rgba(10,10,24,.62);border:3px solid {acc};border-radius:36px;display:flex;align-items:center;gap:32px;padding:0 38px;z-index:5"><span style="flex:none;width:92px;height:92px;border-radius:50%;background:{acc};color:#111;font-size:60px;display:flex;align-items:center;justify-content:center">{i+1}</span><span style="font-size:46px;line-height:1.5">{t}</span></div>' for i, t in enumerate(c['opts']))
    ink = f'''<div style="position:absolute;left:75px;top:80px;background:{acc};color:#111;font-size:44px;padding:14px 42px;border-radius:60px;z-index:5">선택지</div>
<div style="position:absolute;left:90px;top:210px;width:900px;font-size:100px;line-height:1.4;z-index:5;text-shadow:0 4px 18px rgba(0,0,0,.55)">{c['q']}</div>{rows}
<div style="position:absolute;left:0;right:0;top:1150px;text-align:center;font-size:44px;color:{acc};z-index:5">고른 번호를 세어 보세요</div>{handle(acc)}'''
    return page(ink, c['bg2'], acc)
def result(c):
    acc = c['acc']; fc = c.get('face2'); img = f'<img src="data:image/png;base64,{face_b64(fc)}" style="position:absolute;right:-60px;bottom:0;height:380px;z-index:3">' if fc else ''
    body = c['body']; w = 840
    ink = f'''<div style="position:absolute;left:75px;top:80px;background:{acc};color:#111;font-size:44px;padding:14px 42px;border-radius:60px;z-index:5">결과</div>
<div style="position:absolute;left:90px;top:210px;width:900px;font-size:100px;line-height:1.4;z-index:5;text-shadow:0 4px 18px rgba(0,0,0,.55)">{c['rt']}</div>
<div style="position:absolute;left:70px;top:470px;width:{w+60}px;background:rgba(10,10,24,.66);border-radius:36px;padding:44px 48px;font-size:46px;line-height:1.9;z-index:5;box-sizing:border-box">{body}</div>{img}
<div style="position:absolute;left:70px;right:70px;top:1090px;height:110px;background:{acc};color:#111;border-radius:60px;display:flex;align-items:center;justify-content:center;font-size:46px;z-index:5">{c['cta']}</div>{handle(acc)}'''
    return page(ink, c['bg3'], acc)
SETS = {
 'a_1009': dict(acc='#ff8a73', face='v2_straight', bg='sky', badge='정월의 연애 테스트', sub='한 번 정하면 뒤돌아보지 않는 나', title='연애에서도<br>몇 개 해당돼요?',
    bg2='chart', q='세 가지 중<br>몇 개예요?', opts=['마음이 식으면 정리가 빨라요', '좋아하면 먼저 표현해요', '헤어진 뒤 뒤돌아본 적이 드물어요'],
    bg3='sun', face2='v2_straight', rt='2개 이상이라면', body='확신이 빠른 만큼 상대는<br>갑작스럽게 느낄 수 있어요.<br>정리하기 전에 이유를<br>한 문장으로 말해 주세요.', cta='내 숫자를 댓글로 남겨 주세요'),
 'b_1011': dict(acc='#f6b042', face='intro', bg='chart', badge='정월의 관계 테스트', sub='먼저 말하지 못하고<br>기다리다 놓친 사람이 있다면', title='나는 몇 개<br>해당돼요?',
    bg2='sun', q='세 가지 중<br>몇 개예요?', opts=['상대가 먼저 말해 주길 기다려요', '말할까 고민하다 때를 놓친 적 있어요', '놓치고 나서야 말할걸 생각해요'],
    bg3='sky', face2=None, rt='2개 이상이라면', body='말이 느린 게 아니라<br>거절을 먼저 헤아리는 쪽일 수 있어요.<br>이번 주에 안부 한 줄을 먼저 보내 보세요.', cta='내 숫자를 댓글로 남겨 주세요'),
 'd_1023': dict(acc='#7fd6c8', face='v3_ponytail', bg='ink', badge='정월의 연락 테스트', sub='읽고 답장하기까지 걸리는 시간', title='나는 어느 쪽에<br>가까울까요?',
    bg2='sky', q='세 가지 중<br>어느 쪽이에요?', opts=['메시지가 오면 바로 답해야 편해요', '답장을 썼다 지웠다 하다 늦게 보내요', '읽고 이따 답해야지 하고 잊어요'],
    bg3='chart', face2=None, rt='많이 고른 번호는요', body='1번은 바로 답하는 쪽,<br>2번은 다듬어 보내는 쪽,<br>3번은 천천히 답하는 쪽이에요.<br>빠르다 느리다가 아니라<br>연락의 리듬이에요.', cta='내 번호를 댓글로 남겨 주세요'),
}
async def main():
    out = os.path.join(R, '2026-w43swap', 'cards'); os.makedirs(out, exist_ok=True); bad = 0
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 1080, 'height': 1350})
        for k, c in SETS.items():
            for i, fn in enumerate((cover, options, result), 1):
                await pg.set_content(fn(c)); await pg.wait_for_timeout(350)
                for x in await check_page(pg, f'{k}_{i}', 'cover' if i == 1 else None): print('검사:', x); bad += 1
                await pg.screenshot(path=os.path.join(out, f'{k}_{i}.jpg'), type='jpeg', quality=92)
        await b.close()
    print('검사 문제', bad, '건')
if __name__ == '__main__': asyncio.run(main())
