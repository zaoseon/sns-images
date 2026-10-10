# swap 카드 3세트(a_1009·b_1011·d_1023)를 R46·R47 방식으로 다시 만든다(10/10). 글은 옛 빌더(pipeline/swap_cards_w43.py)와 같다.
# 틀: 해·달 배경·#181615 패널·금 강조색, 블록 높이 계산 배치(2026-vd-mockups/build3.py). 출력 cards/{세트}_{번호}.jpg (1080x1440)
import sys, os, asyncio
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..', '2026-vd-mockups'))
import build3 as B
from build3 import T, PILL, PANEL, FACE, place, new, GOLD, C_, X0
def cover(face, label, sub, title, fh=420):
    p = new(); p.bg = 'ink'
    place(p, [FACE(p, face, fh, 'center'), PANEL(p, [T(p, label, 52, GOLD, 'body', 1.3, 'center', 788, '라벨', X0 + 56), T(p, title, 92, '#fff', 'title', 1.3, 'center', 788, '제목', X0 + 56), T(p, sub, 52, '#fff', 'body', 1.5, 'center', 788, '질문', X0 + 56)])]); return p
def choose(title, lines):
    p = new(); place(p, [PILL(p, '선택지', 52, None, 'center'), T(p, title, 88, align=C_, name='제목'), PANEL(p, [T(p, lines, 52, '#fff', 'body', 1.5, 'center', 788, '선택지', X0 + 56)])]); return p
def result(badge, title, body, foot):
    p = new(); place(p, [PILL(p, badge, 52, None, 'center'), T(p, title, 88, align=C_, name='제목'), PANEL(p, [T(p, body, 52, '#fff', 'body', 1.5, 'center', 788, '결과', X0 + 56)]), T(p, foot, 56, GOLD, 'body', 1.5, C_, name='안내')]); return p
SETS = {
 'a_1009': [lambda: cover('v2_straight', '정월의 연애 테스트', '한 번 정하면 뒤돌아보지 않는 나', '연애에서도\n몇 개 해당되나요?'),
            lambda: choose('세 가지 중\n몇 개인가요?', '1 마음이 식으면 정리가 빨라요\n2 좋아하면 먼저 표현해요\n3 헤어진 뒤 뒤돌아본 적이 드물어요'),
            lambda: result('결과', '2개 이상이라면', '확신이 빠른 만큼\n상대는 갑작스럽게 느낄 수 있어요.\n정리하기 전에 이유를\n한 문장으로 말해 주세요.', '내 숫자를 댓글로 남겨 주세요')],
 'b_1011': [lambda: cover('v3_ponytail', '정월의 관계 테스트', '먼저 말하지 못하고\n기다리다 놓친 사람이 있다면', '나는 몇 개\n해당되나요?', 330),
            lambda: choose('세 가지 중\n몇 개인가요?', '1 상대가 먼저 말해 주길 기다려요\n2 말할까 고민하다 때를 놓친 적 있어요\n3 놓치고 나서야 말할걸 생각해요'),
            lambda: result('결과', '2개 이상이라면', '말이 느린 게 아니라\n거절을 먼저 헤아리는 쪽일 수 있어요.\n이번 주에 안부 한 줄을\n먼저 보내 보세요.', '내 숫자를 댓글로 남겨 주세요')],
 'd_1023': [lambda: cover('v1_lowbun', '정월의 연락 테스트', '읽고 답장하기까지 걸리는 시간', '나는 어느 쪽에\n가까울까요?'),
            lambda: choose('세 가지 중\n어느 쪽인가요?', '1 메시지가 오면 바로 답해야 편해요\n2 답장을 썼다 지웠다 하다 늦게 보내요\n3 읽고 이따 답해야지 하고 잊어요'),
            lambda: result('결과', '많이 고른 번호는요', '1번은 바로 답하는 쪽,\n2번은 다듬어 보내는 쪽,\n3번은 천천히 답하는 쪽이에요.\n빠르다 느리다가 아니라\n연락의 리듬이에요.', '내 번호를 댓글로 남겨 주세요')],
}
async def main(out):
    from playwright.async_api import async_playwright
    from PIL import Image
    import card_kit as CK; from style_spec import check_page
    os.makedirs(out, exist_ok=True); bad = 0
    async with async_playwright() as pw:
        br = await pw.chromium.launch(executable_path='/opt/pw-browsers/chromium'); pg = await br.new_page(viewport={'width': 1080, 'height': 1440})
        for k, fns in SETS.items():
            for i, fn in enumerate(fns, 1):
                p = fn(); t, b, c = B.metrics(p); n = f'{k}_{i}'
                for pr in p.problems: print('엔진:', n, pr); bad += 1
                if t < B.TOP - 1 or b > B.BOT + 1 or abs(c - B.CEN) > 15: print('배치:', n, f'위 {t:.0f} 아래 {b:.0f} 가운데 {c:.0f}'); bad += 1
                open('/tmp/swap.html', 'w', encoding='utf-8').write(CK.page(''.join(p.html) + CK.frame(getattr(p, 'ai', False)), getattr(p, 'bg', 'sun'), GOLD))
                await pg.goto('file:///tmp/swap.html'); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(350)
                for x in await check_page(pg, n, 'bundle'): print('검사:', x); bad += 1
                await pg.screenshot(path=f'{out}/{n}.png'); Image.open(f'{out}/{n}.png').convert('RGB').save(f'{out}/{n}.jpg', quality=92); os.remove(f'{out}/{n}.png')
                print(n, f'묶음 {t:.0f}~{b:.0f} 가운데 {c:.0f}')
        await br.close()
    print('문제', bad, '건')
if __name__ == '__main__': asyncio.run(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'cards')))
