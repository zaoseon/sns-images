# 10/16 대표 "빨리 다시 만들자": sharitrial3(검정+금색·빛 번짐·반짝이)이 색 규칙 K-038·K-041·K-043·K-060에 걸려
# 색 조합 목록 p_red(핑크 & 레드, 대담함·트렌디함)로 다시 만든다. 정월(빨간 니트)과 같은 계열이라 한 장이 한 톤으로 묶인다.
# 바탕 단색 #FFF1F5, 정월 뒤 단색 원(#FFD9E4), 면·선 무채색에 가까운 흰 판 + 1px 선, 강조는 레드 하나(제목 한 단어·번호·마감 줄).
# 그라데이션·빛 번짐·반짝이·흐림 없음. 글은 sharitrial3 그대로.
# 사용: python3 2026-event/build_sharitrial4.py  출력 2026-event/cards/sharitrial4_1.jpg (새 이름으로만 추가)
import sys, os, asyncio
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, '..')
sys.path.insert(0, os.path.join(ROOT, 'pipeline'))
import card_kit as CK, fonts_kit as K
from style_spec import check_page

BG, DISC, CARD, LINE = '#FFF1F5', '#FFD9E4', '#FFFFFF', '#F3C6D4'
INK, SUB, RED = '#2A0E16', '#7A3A4C', '#C62828'
FACE = 'v12_christmas'; OUT = sys.argv[1] if len(sys.argv) > 1 else 'sharitrial4_1'

LIGHT_FRAME = ('.bf-l{color:%s!important}.bf-r{color:%s!important;opacity:1!important}'
               '.bf-url{color:%s!important;background:%s!important;border:1px solid %s}'
               '.bf-ai{color:%s!important;background:rgba(255,255,255,.85)!important;border:1px solid %s}') % (RED, INK, INK, CARD, LINE, SUB, LINE)

def face_clean():
    # 잘라 낸 정월 사진 가장자리에 어두운 판용 회색 테두리가 남아 밝은 바탕에서 보인다 → 알파를 3px 깎아 테두리를 없앤다
    import base64, io
    from PIL import Image, ImageFilter
    im = Image.open(os.path.join(ROOT, 'characters', 'cut', FACE + '.png')).convert('RGBA')
    a = im.getchannel('A').filter(ImageFilter.MinFilter(7)).filter(ImageFilter.GaussianBlur(1.2))
    im.putalpha(a); b = io.BytesIO(); im.save(b, 'PNG'); return base64.b64encode(b.getvalue()).decode()

def inner():
    B = K.B
    disc = f'<div data-deco="1" style="position:absolute;left:500px;top:250px;width:600px;height:600px;border-radius:50%;background:{DISC};z-index:1"></div>'
    face = f'<img src="data:image/png;base64,{face_clean()}" style="position:absolute;right:-90px;bottom:0;height:1180px;z-index:2">'
    kicker = (f'<div style="position:absolute;left:75px;top:196px;background:{RED};color:#fff;font-family:{B};font-weight:900;'
              'font-size:40px;line-height:1.3;padding:14px 32px;border-radius:60px;z-index:5">스하리 하고 받아 가세요</div>')
    title = (f'<div style="position:absolute;left:72px;top:318px;width:560px;font-size:128px;line-height:1.3;color:{INK};z-index:5">'
             f'무료<br>감정서<br><span style="color:{RED}">체험단</span></div>')
    sub = (f'<div style="position:absolute;left:78px;top:842px;width:440px;font-family:{B};font-weight:800;font-size:40px;line-height:1.5;'
           f'color:{SUB};z-index:5">다섯 분께<br>2027 신년 감정서를 드려요</div>')
    steps = [('1', '이 글에 스하리'), ('2', '프로필 링크에서 무료 풀이'), ('3', '결과 아래 체험단 신청')]
    rows = ''.join(f'<div style="display:flex;align-items:center;gap:22px;margin:{0 if i == 0 else 18}px 0 0"><span style="flex:none;width:58px;height:58px;border-radius:50%;'
                   f'background:{RED};color:#fff;font-size:40px;line-height:58px;text-align:center">{n}</span>'
                   f'<span style="font-family:{B};font-weight:800;font-size:42px;line-height:1.3;color:{INK}">{t}</span></div>'
                   for i, (n, t) in enumerate(steps))
    due_row = (f'<div style="margin:26px 0 0;padding:22px 0 0;border-top:1px solid {LINE};font-family:{B};font-weight:800;font-size:40px;line-height:1.3;color:{RED}">'
               '다섯 분께 · 10월 19일 밤 11시 59분까지</div>')
    panel = (f'<div style="position:absolute;left:55px;top:930px;width:720px;padding:32px 38px;border-radius:32px;z-index:5;'
             f'background:{CARD};border:1px solid {LINE}">' + rows + due_row + '</div>')
    due = (f'<div style="position:absolute;left:75px;top:1282px;font-family:{B};font-weight:800;font-size:40px;line-height:1.3;color:{RED};z-index:5">'
           '10월 19일 밤 11시 59분까지</div>')
    return disc + face + kicker + title + panel + CK.frame(True)

async def main():
    from playwright.async_api import async_playwright
    from PIL import Image
    out = os.path.join(HERE, 'cards')
    html = (f'<html><head><meta charset="utf-8"><style>{K.css(CK.CUR)}{CK.BF.css()}{LIGHT_FRAME}</style></head>'
            f'<body style="margin:0;width:1080px;height:1440px;position:relative;overflow:hidden;{CK.F};color:{INK};word-break:keep-all;line-break:strict;background:{BG}">{inner()}</body></html>')  # 단색 바탕(CK.page의 ink 판은 빛 번짐이 깔려서 안 씀)
    p = os.path.join(HERE, '_tmp_s4.html'); open(p, 'w', encoding='utf-8').write(html)
    async with async_playwright() as pw:
        br = await pw.chromium.launch(executable_path='/opt/pw-browsers/chromium'); pg = await br.new_page(viewport={'width': 1080, 'height': 1440})
        await pg.goto('file://' + p); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(300)
        for x in await check_page(pg, OUT, 'cover'): print('검사:', x)
        await pg.screenshot(path=f'{out}/{OUT}.png'); Image.open(f'{out}/{OUT}.png').convert('RGB').save(f'{out}/{OUT}.jpg', quality=92); os.remove(f'{out}/{OUT}.png')
        await br.close()
    os.remove(p); print('완료', OUT)
asyncio.run(main())
