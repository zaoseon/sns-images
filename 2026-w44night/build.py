# 밤 카드 3장 세트(10/19~10/31, 10세트)를 R46·R47 방식으로 다시 만든다(10/10, R32 ④). 글은 content/night_sets_w42.py 그대로.
# 틀: 해·달 배경, #181615 패널, 금 강조색, 블록 높이 계산 배치(2026-vd-mockups/build3.py). 출력 {MMDD}_{1..3}.jpg (1080x1440)
import sys, os, asyncio
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..', '2026-vd-mockups')); sys.path.insert(0, os.path.join(HERE, '..', 'content'))
import build3 as B
from build3 import T, PILL, PANEL, FACE, place, new, GOLD, C_, X0
import night_sets_w42 as NS
SKIP = ('2026-10-18', '2026-10-24')      # 5장·7장 세트는 따로 다룬다
def cover(s):
    p = new(); p.bg = 'ink'
    place(p, [FACE(p, s['face'], 400, 'center'), PANEL(p, [T(p, s['kicker'], 52, GOLD, 'body', 1.3, 'center', 788, '라벨', X0 + 56), T(p, s['coverTitle'], 88, '#fff', 'title', 1.3, 'center', 788, '제목', X0 + 56), T(p, s['coverSub'], 52, '#fff', 'body', 1.5, 'center', 788, '질문', X0 + 56)])]); return p
def body(badge, title, text):
    p = new(); place(p, [PILL(p, badge, 52, None, 'center'), T(p, title, 88, align=C_, name='제목'), PANEL(p, [T(p, text, 52, '#fff', 'body', 1.5, 'center', 788, '본문', X0 + 56)])]); return p
async def main(out, only=None):
    from playwright.async_api import async_playwright
    from PIL import Image
    import card_kit as CK; from style_spec import check_page
    os.makedirs(out, exist_ok=True); bad = 0; log = []
    async with async_playwright() as pw:
        br = await pw.chromium.launch(executable_path='/opt/pw-browsers/chromium'); pg = await br.new_page(viewport={'width': 1080, 'height': 1440})
        for date, s in NS.SETS.items():
            if date in SKIP or (only and date not in only): continue
            pages = [cover(s), body(s['badges'][0], s['body'][0][0], s['body'][0][1]), body(s['badges'][1], s['body'][1][0], s['body'][1][1])]
            for i, p in enumerate(pages, 1):
                n = f"{date[5:].replace('-', '')}_{i}"; t, b, c = B.metrics(p)
                for pr in p.problems: print('엔진:', n, pr); bad += 1
                if t < B.TOP - 1 or b > B.BOT + 1 or abs(c - B.CEN) > 15: print('배치:', n, f'위 {t:.0f} 아래 {b:.0f} 가운데 {c:.0f}'); bad += 1
                open('/tmp/night.html', 'w', encoding='utf-8').write(CK.page(''.join(p.html) + CK.frame(getattr(p, 'ai', False)), getattr(p, 'bg', 'sun'), GOLD))
                await pg.goto('file:///tmp/night.html'); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(300)
                for x in await check_page(pg, n, 'bundle'): print('검사:', x); bad += 1
                await pg.screenshot(path=f'{out}/{n}.png'); Image.open(f'{out}/{n}.png').convert('RGB').save(f'{out}/{n}.jpg', quality=92); os.remove(f'{out}/{n}.png')
        await br.close()
    print('문제', bad, '건')
if __name__ == '__main__': asyncio.run(main(os.path.join(HERE, 'cards')))
