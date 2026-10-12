# 10/12 대표 앱 요청 mv56yi0u: R55 '만드는 방식 공개' 캐러셀 7장 시안(승인 전 시범).
# 글은 새로 지어내지 않고 사이트 정본(zaoseon-site public/index.html '여섯 운명학을 겹쳐 읽어요'·'마음 코치, 정월'·FAQ 'AI가 쓴 감정서인가요?')의 문장만 줄여 쓴다.
# 틀: 2026-w43min7/build.py와 같은 R46·R47 표지·본문·CTA(build3 블록 높이 계산 배치). 6장은 정월 얼굴 + 검수·AI 고지.
# 사용: python3 2026-w43howto/build.py → 2026-w43howto/cards/howto_{n}.jpg (1080x1440)
import sys, os, asyncio, re
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, '..')
sys.path[:0] = [os.path.join(ROOT, '2026-vd-mockups'), os.path.join(ROOT, 'pipeline'), os.path.join(ROOT, '2026-w43min7')]
import build3 as B
from build3 import PILL, PANEL, FACE, place, new, GOLD, C_, X0
import build as MB          # 2026-w43min7/build.py: T(줄바꿈 검사)·IN·cover_face·body·cta
from build import T, IN, cover_face, body, cta
import carousel_rules as CR

FACE_NAME = 'v4_glasses'
COVER = dict(face=FACE_NAME, kicker='자오선이 만드는 방식', coverTitle='한 사람을\n어떻게 읽을까요?', coverSub='감정서가 만들어지는 순서')
BODIES = [
 ('1 · 넣는 값', '태어난 날과\n시간을 넣어요', '태어난 해·달·날·시간,\n태어난 곳까지 넣어요.\n이 값으로\n만세력과 출생 차트를 세워요.'),
 ('2 · 여섯 운명학', '동양의 넷과\n서양의 둘을 세워요', '사주명리 · 자미두수\n당사주 · 하락이수\n서양 점성술 · 수비학\n한 가지만 보면\n한쪽 이야기만 듣는 셈이에요.'),
 ('3 · 같은 말', '여럿이 같은 말을\n하는 곳부터 봐요', '여럿이 같은 말을 하면\n더 눈여겨볼 이야기예요.\n감정서 첫 장에 결론으로 적어요.'),
 ('4 · 다른 말', '서로 다른 말을\n하는 곳도 있어요', '그곳이 바로\n내가 고를 수 있는 부분이에요.\n선택지와 결과를 함께 풀어요.'),
]
CHECK = ('5 · 직접 읽기', 'AI가 돕고,\n코치가 직접 읽어요',
         '교차 분석·정리는 AI가 도와요.\n검수는 코치가 직접 해요.\n원국과 풀이를 보완해 완성해요.')
CTA = ('내 생일로도\n*겹쳐* 볼까요?', '무료 풀이', '내 태어난 날의 기운', '프로필 링크에서\n1초면 볼 수 있어요')

def check_page_(badge, title, text):
    for fh in (300, 260, 220, 180):
        p = new(); p.bg = 'ink'
        place(p, [FACE(p, FACE_NAME, fh, 'center'), PILL(p, badge, 52, None, 'center'), T(p, title, 84, '#fff', 'title', 1.3, 'center', 900, '제목'), PANEL(p, [IN(p, text, 52)])])
        t, bt, c = B.metrics(p)
        if not p.problems and t >= B.TOP - 1 and bt <= B.BOT + 1: break
    return p

def pages():
    return [cover_face(COVER)] + [body(*b) for b in BODIES] + [check_page_(*CHECK), cta(*CTA)]

async def main(out):
    from playwright.async_api import async_playwright
    from PIL import Image
    import card_kit as CK; from style_spec import check_page
    os.makedirs(out, exist_ok=True); bad = 0; ps = pages()
    for e in CR.check_count(len(ps), 'howto 캐러셀'): print('장 수:', e); bad += 1
    async with async_playwright() as pw:
        br = await pw.chromium.launch(executable_path='/opt/pw-browsers/chromium'); pg = await br.new_page(viewport={'width': 1080, 'height': 1440})
        for i, p in enumerate(ps, 1):
            n = f'howto_{i}'; t, b, c = B.metrics(p)
            for pr in p.problems: print('엔진:', n, pr); bad += 1
            if t < B.TOP - 1 or b > B.BOT + 1 or abs(c - B.CEN) > 15: print('배치:', n, f'위 {t:.0f} 아래 {b:.0f} 가운데 {c:.0f}'); bad += 1
            open('/tmp/howto.html', 'w', encoding='utf-8').write(CK.page(''.join(p.html) + CK.frame(getattr(p, 'ai', False)), getattr(p, 'bg', 'sun'), GOLD))
            await pg.goto('file:///tmp/howto.html'); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(250)
            for x in await check_page(pg, n, 'bundle'): print('검사:', x); bad += 1
            await pg.screenshot(path=f'{out}/{n}.png'); Image.open(f'{out}/{n}.png').convert('RGB').save(f'{out}/{n}.jpg', quality=92); os.remove(f'{out}/{n}.png')
        await br.close()
    print(len(ps), '장, 문제', bad, '건')
if __name__ == '__main__':
    asyncio.run(main(os.path.join(HERE, 'cards')))
