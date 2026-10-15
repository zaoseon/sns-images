# 10/15 대표 재요청 "넣더라도 제대로 느낌있게 넣어야지": 캐릭터를 빼는 게 아니라 제대로 넣는다.
# 아치 판에 잘라 붙인 사진(sharitrial_1) 대신, 선물 상자를 든 정월(v12)을 오른쪽에 크게 세우고
# 뒤에 금빛 달(원)과 빛 번짐, 아래로 자연스럽게 사라지는 그라데이션을 깐다. 글은 왼쪽 단, 참여 방법은 반투명 판.
# 사용: python3 2026-event/build_sharitrial3.py [얼굴키]  출력 2026-event/cards/sharitrial3_1.jpg
import sys, os, asyncio
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, '..')
sys.path.insert(0, os.path.join(ROOT, 'pipeline'))
import card_kit as CK, fonts_kit as K
from style_spec import check_page

GOLD = '#f2b04a'; CREAM = '#f6e7c8'
FACE = sys.argv[1] if len(sys.argv) > 1 else 'v12_christmas'
OUT = sys.argv[2] if len(sys.argv) > 2 else 'sharitrial3_1'

def stars():
    pts = ((612, 236, 30), (980, 300, 18), (1010, 560, 26), (560, 470, 16), (930, 170, 14), (700, 150, 20))
    return ''.join(f'<div data-deco="1" style="position:absolute;left:{x}px;top:{y}px;font-size:{s}px;color:{CREAM};opacity:.8;z-index:1;text-shadow:0 0 12px {GOLD}">✦</div>' for x, y, s in pts)

def inner():
    B = K.B
    bg = ('<div data-deco="1" style="position:absolute;inset:0;background:'
          'radial-gradient(circle at 74% 40%,rgba(242,176,74,.42),rgba(242,176,74,.10) 32%,transparent 58%),'
          'linear-gradient(180deg,#140d08 0%,#1d120a 55%,#0b0705 100%);z-index:0"></div>')
    moon = ('<div data-deco="1" style="position:absolute;left:470px;top:250px;width:560px;height:560px;border-radius:50%;'
            'border:3px solid rgba(246,231,200,.55);box-shadow:0 0 60px rgba(242,176,74,.35),inset 0 0 80px rgba(242,176,74,.18);z-index:1"></div>'
            '<div data-deco="1" style="position:absolute;left:440px;top:220px;width:620px;height:620px;border-radius:50%;'
            'border:1px dashed rgba(246,231,200,.25);z-index:1"></div>')
    face = (f'<img src="data:image/png;base64,{CK.face_b64(FACE)}" style="position:absolute;right:-90px;bottom:0;height:1180px;z-index:2;'
            'filter:drop-shadow(0 0 40px rgba(242,176,74,.35)) saturate(1.05);'
            '-webkit-mask-image:linear-gradient(180deg,#000 72%,transparent 98%);mask-image:linear-gradient(180deg,#000 72%,transparent 98%)">')
    floor = '<div data-deco="1" style="position:absolute;left:0;right:0;bottom:0;height:420px;background:linear-gradient(180deg,transparent,rgba(11,7,5,.92));z-index:3"></div>'
    kicker = (f'<div style="position:absolute;left:75px;top:196px;background:{GOLD};color:#1a1008;font-family:{B};font-weight:900;'
              'font-size:40px;line-height:1.3;padding:14px 32px;border-radius:60px;z-index:5">스하리 하고 받아 가세요</div>')
    title = ('<div style="position:absolute;left:72px;top:318px;width:560px;font-size:128px;line-height:1.3;z-index:5;'
             'text-shadow:0 6px 24px rgba(0,0,0,.6)">무료<br>감정서<br><span style="color:' + GOLD + '">체험단</span></div>')
    sub = (f'<div style="position:absolute;left:78px;top:842px;width:460px;font-family:{B};font-weight:800;font-size:40px;line-height:1.5;'
           f'color:{CREAM};z-index:5;text-shadow:0 2px 12px rgba(0,0,0,.7)">다섯 분께<br>2027 신년 감정서를 드려요</div>')
    steps = [('1', '이 글에 스하리'), ('2', '프로필 링크에서 무료 풀이'), ('3', '결과 아래 체험단 신청')]
    rows = ''.join(f'<div style="display:flex;align-items:center;gap:22px;margin:{0 if i == 0 else 18}px 0 0"><span style="flex:none;width:58px;height:58px;border-radius:50%;'
                   f'background:{GOLD};color:#1a1008;font-size:40px;line-height:58px;text-align:center">{n}</span><span style="font-family:{B};font-weight:800;font-size:42px;line-height:1.3">{t}</span></div>'
                   for i, (n, t) in enumerate(steps))
    panel = ('<div style="position:absolute;left:55px;top:960px;width:680px;padding:30px 36px;border-radius:36px;z-index:5;'
             'background:rgba(20,12,7,.58);border:2px solid rgba(242,176,74,.45);backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);'
             'box-shadow:0 20px 60px rgba(0,0,0,.45)">' + rows + '</div>')
    due = (f'<div style="position:absolute;left:75px;top:1258px;font-family:{B};font-weight:800;font-size:40px;line-height:1.3;color:{GOLD};z-index:5">'
           '다섯 분께 · 10월 19일 밤 11시 59분까지</div>')
    return bg + moon + stars() + face + floor + kicker + title + panel + due + CK.frame(True)

async def main():
    from playwright.async_api import async_playwright
    from PIL import Image
    out = os.path.join(HERE, 'cards'); html = CK.page(inner(), 'ink', GOLD).replace('background:#0b0806', 'background:#0b0705')
    p = os.path.join(HERE, '_tmp_s3.html'); open(p, 'w', encoding='utf-8').write(html)
    async with async_playwright() as pw:
        br = await pw.chromium.launch(executable_path='/opt/pw-browsers/chromium'); pg = await br.new_page(viewport={'width': 1080, 'height': 1440})
        await pg.goto('file://' + p); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(300)
        for x in await check_page(pg, OUT, 'cover'): print('검사:', x)
        await pg.screenshot(path=f'{out}/{OUT}.png'); Image.open(f'{out}/{OUT}.png').convert('RGB').save(f'{out}/{OUT}.jpg', quality=92); os.remove(f'{out}/{OUT}.png')
        await br.close()
    os.remove(p); print('완료', OUT)
asyncio.run(main())
