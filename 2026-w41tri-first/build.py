# "3초 만에 사랑에 빠지는 사람" 카드 6장 (10/10 기획안 docs/기획_3초사랑_채널별_기획안_2026-10-10.md)
# 틀: 발행 카드 색 체계(해·달 배경, #181615 패널, 금 강조색), 배치는 2026-vd-mockups/build3.py의 블록 계산(R46·R47). 출력 01~06.jpg (1080x1440).
import sys, os, asyncio
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..', '2026-vd-mockups'))
import build3 as B
from build3 import T, PILL, ROW, FACE, PANEL, place, new, GOLD, C_, X0
def S1():
    p = new(); p.bg = 'ink'
    place(p, [FACE(p, 'v4_glasses', 420, 'center'), PANEL(p, [T(p, '정월의 연애 테스트', 52, GOLD, 'body', 1.3, 'center', 788, '라벨', X0 + 56), T(p, '3초 만에\n사랑에 빠지는 사람', 92, '#fff', 'title', 1.3, 'center', 788, '제목', X0 + 56), T(p, '주변에 꼭 한 명 있죠?', 56, '#fff', 'body', 1.5, 'center', 788, '질문', X0 + 56)])]); return p
def S2():
    p = new(); place(p, [PILL(p, '① 별자리', 52, None, 'center'), T(p, '내 생일이\n이 안에 있나요?', 88, align=C_, name='제목'), ROW(p, '양자리', '', '3월 21일 ~ 4월 19일'), ROW(p, '사자자리', '', '7월 23일 ~ 8월 22일'), T(p, '있으면 ✓', 72, GOLD, 'body', 1.5, C_, name='확인')]); return p
def S3():
    p = new(); place(p, [PILL(p, '② 숫자', 52, None, 'center'), T(p, '생년월일 숫자를 더해서\n한 자리로 만들어요', 80, align=C_, name='제목'), PANEL(p, [T(p, '예) 1990-05-15\n1+9+9+0+0+5+1+5 = 30\n3+0 = 3', 56, '#fff', 'body', 1.5, 'center', 788, '예시', X0 + 56)]), T(p, '3 또는 5가 나오면 ✓', 64, GOLD, 'body', 1.5, C_, name='확인')]); return p
def S4():
    p = new(); place(p, [PILL(p, '③ 사주', 52, None, 'center'), T(p, '내 일간이\n병화(丙)인가요?', 88, align=C_, name='제목'), PANEL(p, [T(p, '일간은 태어난 날의 기운이에요.\n모르면 프로필 링크에서\n생년월일만 넣어 보세요.\n1초면 나와요.', 52, '#fff', 'body', 1.5, 'center', 788, '안내', X0 + 56)]), T(p, '병화(丙)면 ✓', 64, GOLD, 'body', 1.5, C_, name='확인')]); return p
def S5():
    p = new(); place(p, [ROW(p, '사주', '동양', '병화(丙)일생\n태양처럼 바로 달아오르고,\n사람을 끌어요', size=46, vw=580), ROW(p, '별자리', '서양', '양자리 · 사자자리\n직진하는 불의 별자리', size=46, vw=580), ROW(p, '숫자', '수비학', '3번 · 5번\n표현의 3, 새로움에 끌리는 5', size=46, vw=580),
                         T(p, '하나도 안 겹친다면,\n천천히 스며드는 사랑을\n하는 사람일지도 몰라요.', 52, '#fff', 'body', 1.5, C_, name='설명')]); return p
def S6():
    p = new(); p.bg = 'ink'
    place(p, [FACE(p, 'v2_straight', 480, 'center'), PANEL(p, [T(p, '몇 개 겹쳤나요?', 92, '#fff', 'title', 1.3, 'center', 788, '제목', X0 + 56), T(p, '숫자로 댓글을 남겨 주세요.\n떠오르는 사람에게도\n보내서 물어보세요.', 52, '#fff', 'body', 1.5, 'center', 788, '요청', X0 + 56)])]); return p
PAGES = dict(S1=S1, S2=S2, S3=S3, S4=S4, S5=S5, S6=S6)
async def main(out):
    from playwright.async_api import async_playwright
    from PIL import Image
    import card_kit as CK; from style_spec import check_page
    os.makedirs(out, exist_ok=True); bad = 0
    async with async_playwright() as pw:
        br = await pw.chromium.launch(executable_path='/opt/pw-browsers/chromium'); pg = await br.new_page(viewport={'width': 1080, 'height': 1440})
        for i, (k, fn) in enumerate(PAGES.items(), 1):
            p = fn(); t, b, c = B.metrics(p)
            for pr in p.problems: print('엔진:', k, pr); bad += 1
            if t < B.TOP - 1 or b > B.BOT + 1 or abs(c - B.CEN) > 15: print('배치:', k, f'위 {t:.0f} 아래 {b:.0f} 가운데 {c:.0f}'); bad += 1
            open('/tmp/tri.html', 'w', encoding='utf-8').write(CK.page(''.join(p.html) + CK.frame(getattr(p, 'ai', False)), getattr(p, 'bg', 'sun'), GOLD))
            await pg.goto('file:///tmp/tri.html'); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(350)
            for x in await check_page(pg, k, 'bundle'): print('검사:', x); bad += 1
            await pg.screenshot(path=f'{out}/{i:02d}.png'); Image.open(f'{out}/{i:02d}.png').convert('RGB').save(f'{out}/{i:02d}.jpg', quality=92); os.remove(f'{out}/{i:02d}.png')
            print(k, f'묶음 {t:.0f}~{b:.0f} 가운데 {c:.0f}')
        await br.close()
    print('문제', bad, '건')
if __name__ == '__main__': asyncio.run(main(sys.argv[1] if len(sys.argv) > 1 else HERE))
