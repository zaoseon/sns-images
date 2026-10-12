# 10/12 대표 "캐러셀은 최소 7장(표지·본문·CTA)" - 7장 미만으로 예약된 인스타 캐러셀 18세트를 7~8장으로 다시 그린다.
# 글: content/min7_sets_1012.py. 틀: 2026-w44night7/build.py(R46·R47, build3 블록 높이 계산 배치)와 같은 표지·본문, 끝에서 두 번째 장은 '이번 주에 해 볼 것 하나', 마지막 장은 프로필 링크 1초 무료 풀이 CTA.
# 사용: python3 2026-w43min7/build.py [MMDD,MMDD,...]  출력 2026-w43min7/cards/{MMDD}_{n}.jpg (1080x1440)
import sys, os, asyncio, re
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, '..')
sys.path[:0] = [os.path.join(ROOT, '2026-vd-mockups'), os.path.join(ROOT, 'content'), os.path.join(ROOT, 'pipeline')]
import build3 as B
from build3 import T as _T, PILL, PANEL, FACE, ROW, place, new, GOLD, C_, X0
from template_engine import font, wrap
import min7_sets_1012 as M
sys.path.insert(0, os.path.join(ROOT, 'pipeline')); import carousel_rules as CR

def T(p, txt, size, color='#fff', role='title', lh=1.3, align='left', w=B.W, name='글', x=None):
    """build3.T + 명시한 줄바꿈이 그대로 나오는지 확인(자동으로 더 나뉘면 문제로 적는다: 뜻 단위 줄바꿈 R08)."""
    path = B.TP if role == 'title' else B.BP; ls = wrap(B.strip(txt), font(path, size), w)
    if len(ls) != len(txt.split('\n')): p.problems.append(f'{name} 줄이 자동으로 더 나뉨({len(txt.split(chr(10)))}→{len(ls)}줄): {ls}')
    for l in txt.split('\n'):
        if len(B.strip(l).strip()) == 1: p.problems.append(f'{name} 한 글자 줄: {l!r}')
    return _T(p, txt, size, color, role, lh, align, w, name, x)
def IN(p, txt, size, color='#fff', role='body', lh=1.5, name='본문'): return T(p, txt, size, color, role, lh, 'center', 788, name, X0 + 56)

def cover_face(s):
    p = new(); p.bg = 'ink'
    for ts in (88, 80, 76):
        q = new(); q.bg = 'ink'; t = T(q, s['coverTitle'], ts, '#fff', 'title', 1.3, 'center', 788, '제목', X0 + 56)
        if not q.problems: break
    place(p, [FACE(p, s['face'], 400, 'center'), PANEL(p, [IN(p, s['kicker'], 52, GOLD, lh=1.3, name='라벨'), T(p, s['coverTitle'], ts, '#fff', 'title', 1.3, 'center', 788, '제목', X0 + 56), IN(p, s['coverSub'], 52, name='질문')])]); return p
def body(badge, title, text, ts=88):
    for size in (ts, 80, 76):
        q = new(); T(q, title, size, align=C_, name='제목')
        if not q.problems: break
    p = new(); place(p, [PILL(p, badge, 52, None, 'center'), T(p, title, size, align=C_, name='제목'), PANEL(p, [IN(p, text, 52)])]); return p
def advice(s, title, text):
    for fh in (300, 260, 220, 180):
        p = new(); p.bg = 'ink'
        place(p, [FACE(p, s['face'], fh, 'center'), PILL(p, '이번 주에 해 볼 것 하나', 52, None, 'center'), T(p, title, 84, '#fff', 'title', 1.3, 'center', 900, '제목'), PANEL(p, [IN(p, text, 52)])])
        t, bt, c = B.metrics(p)
        if not p.problems and t >= B.TOP - 1 and bt <= B.BOT + 1: break
    return p
def cta(q, label, line1, line2):
    p = new(); q = re.sub(r'\*(.+?)\*', r'[[\1]]', q)
    place(p, [T(p, q, 92, '#fff', 'title', 1.3, C_, 900, '질문'), PILL(p, '팔로우하고 같이 얘기 나눠요', 52, None, 'center'),
              PANEL(p, [IN(p, label, 52, GOLD, lh=1.3, name='라벨'), T(p, line1, 56, '#fff', 'title', 1.5, 'center', 788, '안내', X0 + 56), IN(p, line2, 52, '#efe9e4', name='안내2')])]); return p

def night_pages(s):
    out = [cover_face(s)] + [body(*b) for b in s['bodies']] + [advice(s, *s['advice'])]
    return out + [cta(s['ctaQ'], '무료 풀이', '내 태어난 날의 기운', '프로필 링크에서\n1초면 볼 수 있어요')]
def promo_pages(s):
    out = [cover_face(s)] + [body(*b) for b in s['bodies']] + [advice(s, *s['advice'])]
    return out + [cta(s['ctaQ'], '10월 얼리버드 · 선착순 50명', '프로필 링크 → 감정서', '2027 신년에서 신청해요\nzaoseon.com/ny')]
def tti_cover(z):
    p = new(); p.bg = 'ink'
    place(p, [IN(p, '2027 정미년 띠 이야기', 52, GOLD, lh=1.3, name='라벨'), T(p, z['name'], 124, '#fff', 'title', 1.2, C_, 900, '띠'), T(p, z['years'], 48, '#efe9e4', 'body', 1.3, C_, 900, '년생'),
              PANEL(p, [IN(p, '한 줄로는', 52, GOLD, lh=1.3, name='라벨2'), T(p, f"'{z['one']}'", 72, '#fff', 'title', 1.3, 'center', 788, '한 줄', X0 + 56), IN(p, z['hook'], 52, name='훅')])]); return p
def tti_cal(z):
    p = new()
    luck = f"행운의 색: {z['color']}\n행운의 숫자: {z['num']}\n행운의 방향: {z['dir']}"
    place(p, [PILL(p, '2027년 달력과 행운', 52, None, 'center'), ROW(p, '힘을 쓸 달', '', z['good'], '힘 쓸 달'), ROW(p, '아낄 달', '', z['save'], '아낄 달'), PANEL(p, [IN(p, luck, 52, name='행운')])]); return p
def tti_do(z):
    p = new(); p.bg = 'ink'
    place(p, [PILL(p, '이번 주에 해 볼 것 하나', 52, None, 'center'), T(p, z['do'], 84, '#fff', 'title', 1.3, C_, 900, '해 볼 것'),
              PANEL(p, [IN(p, '조심할 것', 52, GOLD, lh=1.3, name='라벨'), IN(p, z['dont'], 56, name='조심')])]); return p
def tti_pages(z):
    out = [tti_cover(z), body(f"{z['name']}와 2027년", z['rel'], z['why'], 80), tti_cal(z),
           body('돈', *z['money'], 80), body('일', *z['work'], 80), body('사람', *z['people'], 80), tti_do(z)]
    return out + [cta('여러분은\n*무슨 띠*인가요?', '무료 풀이', '같은 띠라도\n태어난 날에 따라 달라요', '내 태어난 날의 기운은\n프로필 링크에서 1초면 볼 수 있어요')]
def pages(s): return {'night': night_pages, 'promo': promo_pages, 'tti': tti_pages}[s['kind']](s)

async def main(out, only):
    from playwright.async_api import async_playwright
    from PIL import Image
    import card_kit as CK; from style_spec import check_page
    os.makedirs(out, exist_ok=True); bad = 0
    async with async_playwright() as pw:
        br = await pw.chromium.launch(executable_path='/opt/pw-browsers/chromium'); pg = await br.new_page(viewport={'width': 1080, 'height': 1440})
        for date, s in M.SETS.items():
            key = date[5:].replace('-', '')
            if only and key not in only: continue
            ps = pages(s)
            for e in CR.check_count(len(ps), f'{key} 캐러셀'): print('장 수:', e); bad += 1
            for i, p in enumerate(ps, 1):
                n = f'{key}_{i}'; t, b, c = B.metrics(p)
                for pr in p.problems: print('엔진:', n, pr); bad += 1
                if t < B.TOP - 1 or b > B.BOT + 1 or abs(c - B.CEN) > 15: print('배치:', n, f'위 {t:.0f} 아래 {b:.0f} 가운데 {c:.0f}'); bad += 1
                open('/tmp/min7.html', 'w', encoding='utf-8').write(CK.page(''.join(p.html) + CK.frame(getattr(p, 'ai', False)), getattr(p, 'bg', 'sun'), GOLD))
                await pg.goto('file:///tmp/min7.html'); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(250)
                for x in await check_page(pg, n, 'bundle'): print('검사:', x); bad += 1
                await pg.screenshot(path=f'{out}/{n}.png'); Image.open(f'{out}/{n}.png').convert('RGB').save(f'{out}/{n}.jpg', quality=92); os.remove(f'{out}/{n}.png')
            print(key, len(ps), '장')
        await br.close()
    print('문제', bad, '건')
if __name__ == '__main__':
    only = set(sys.argv[1].split(',')) if len(sys.argv) > 1 else set()
    asyncio.run(main(os.path.join(HERE, 'cards'), only))
