# 밤 카드 7장 세트(10/16·22·24·27·29·30·31)를 R46·R47 방식으로 다시 만든다(10/10, R32 ④). 글은 content/topic_sets_night7.py 그대로.
# 틀: 해·달 배경, #181615 패널, 금 강조색, 블록 높이 계산 배치(2026-vd-mockups/build3.py). 출력 {MMDD}_{1..7}.jpg (1080x1440)
import sys, os, asyncio, re
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..', '2026-vd-mockups')); sys.path.insert(0, os.path.join(HERE, '..', 'content'))
import build3 as B
from build3 import T, PILL, PANEL, FACE, place, new, GOLD, C_, X0
import topic_sets_night7 as NS
def cover(s):
    p = new(); p.bg = 'ink'
    place(p, [FACE(p, s['face'], 400, 'center'), PANEL(p, [T(p, s['kicker'], 52, GOLD, 'body', 1.3, 'center', 788, '라벨', X0 + 56), T(p, s['coverTitle'], 88, '#fff', 'title', 1.3, 'center', 788, '제목', X0 + 56), T(p, s['coverSub'], 52, '#fff', 'body', 1.5, 'center', 788, '질문', X0 + 56)])]); return p
def body(badge, title, text):
    p = new(); place(p, [PILL(p, badge, 52, None, 'center'), T(p, title, 88, align=C_, name='제목'), PANEL(p, [T(p, text, 52, '#fff', 'body', 1.5, 'center', 788, '본문', X0 + 56)])]); return p
def advice(s, fh):
    t, x = s['advice']; p = new(); p.bg = 'ink'
    place(p, [FACE(p, s['face'], fh, 'center'), PILL(p, '조언', 52, None, 'center'), T(p, t, 84, '#fff', 'title', 1.3, 'center', 900, '제목'), PANEL(p, [T(p, x, 52, '#fff', 'body', 1.5, 'center', 788, '본문', X0 + 56)])]); return p
def cta(s):
    p = new(); q = re.sub(r'\*(.+?)\*', r'[[\1]]', s['ctaQ'])
    place(p, [T(p, q, 92, '#fff', 'title', 1.3, C_, 900, '질문'), PILL(p, '팔로우하고 같이 얘기 나눠요', 52, None, 'center'),
              PANEL(p, [T(p, '다음 편', 52, GOLD, 'body', 1.3, 'center', 788, '라벨', X0 + 56), T(p, s['nextTitle'], 56, '#fff', 'title', 1.5, 'center', 788, '다음 편', X0 + 56), T(p, '프로필 링크에서 생년월일 입력', 52, '#efe9e4', 'body', 1.5, 'center', 788, '안내', X0 + 56)])]); return p
def pages(s):
    sl = s['body']; b = s['badges']; out = [cover(s), body(b[0], *sl[0]), body(b[1], *sl[1]), body(b[2], *sl[2]), body(b[3], *sl[3])]
    for fh in (300, 260, 220, 180):
        p = advice(s, fh); p.html  # 높이 계산은 metrics로
        t, bt, c = B.metrics(p)
        if not p.problems and t >= B.TOP - 1 and bt <= B.BOT + 1: break
    return out + [p, cta(s)]
async def main(out):
    from playwright.async_api import async_playwright
    from PIL import Image
    import card_kit as CK; from style_spec import check_page
    os.makedirs(out, exist_ok=True); bad = 0
    async with async_playwright() as pw:
        br = await pw.chromium.launch(executable_path='/opt/pw-browsers/chromium'); pg = await br.new_page(viewport={'width': 1080, 'height': 1440})
        for date, s in NS.SETS.items():
            for i, p in enumerate(pages(s), 1):
                n = f"{date[5:].replace('-', '')}_{i}"; t, b, c = B.metrics(p)
                for pr in p.problems: print('엔진:', n, pr); bad += 1
                if t < B.TOP - 1 or b > B.BOT + 1 or abs(c - B.CEN) > 15: print('배치:', n, f'위 {t:.0f} 아래 {b:.0f} 가운데 {c:.0f}'); bad += 1
                open('/tmp/n7.html', 'w', encoding='utf-8').write(CK.page(''.join(p.html) + CK.frame(getattr(p, 'ai', False)), getattr(p, 'bg', 'sun'), GOLD))
                await pg.goto('file:///tmp/n7.html'); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(300)
                for x in await check_page(pg, n, 'bundle'): print('검사:', x); bad += 1
                await pg.screenshot(path=f'{out}/{n}.png'); Image.open(f'{out}/{n}.png').convert('RGB').save(f'{out}/{n}.jpg', quality=92); os.remove(f'{out}/{n}.png')
        await br.close()
    print('문제', bad, '건')
if __name__ == '__main__': asyncio.run(main(os.path.join(HERE, 'cards')))
