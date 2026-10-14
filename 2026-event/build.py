# 10/13 대표 승인 팔로워 이벤트·체험단(zaoseon-site docs/팔로워이벤트_체험단_설계_2026-10-13.md) 인스타 캐러셀 2세트.
# 글: zaoseon-site ops/이벤트_콘텐츠_초안_1015_1016.md 의 B(10/15 체험단 모집)·C(10/16 팔로우 이벤트). 틀: 2026-w43min7/build.py(R46·R47, 7장 R58).
# 사용: python3 2026-event/build.py [trial1015,follow1016]  출력 2026-event/cards/{key}_{n}.jpg (1080x1440)
import sys, os, asyncio, re
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, '..')
sys.path[:0] = [os.path.join(ROOT, '2026-vd-mockups'), os.path.join(ROOT, 'content'), os.path.join(ROOT, 'pipeline')]
import build3 as B
from build3 import T as _T, PILL, PANEL, FACE, place, new, GOLD, C_, X0
from template_engine import font, wrap
import card_kit as CK
import carousel_rules as CR

def T(p, txt, size, color='#fff', role='title', lh=1.3, align='left', w=B.W, name='글', x=None):
    path = B.TP if role == 'title' else B.BP; ls = wrap(B.strip(txt), font(path, size), w)
    if len(ls) != len(txt.split('\n')): p.problems.append(f'{name} 줄이 자동으로 더 나뉨({len(txt.split(chr(10)))}→{len(ls)}줄): {ls}')
    for l in txt.split('\n'):
        if len(B.strip(l).strip()) == 1: p.problems.append(f'{name} 한 글자 줄: {l!r}')
    return _T(p, txt, size, color, role, lh, align, w, name, x)
def IN(p, txt, size, color='#fff', role='body', lh=1.5, name='본문'): return T(p, txt, size, color, role, lh, 'center', 788, name, X0 + 56)

def cover(kicker, title, sub, pill=None):
    for ts in (100, 92, 88, 80):
        q = new(); T(q, title, ts, align=C_, w=900, name='제목')
        if not q.problems: break
    p = new(); p.bg = 'ink'; p.ai = True
    blocks = [IN(p, kicker, 52, GOLD, lh=1.3, name='라벨'), T(p, title, ts, '#fff', 'title', 1.3, C_, 900, '제목')]
    if pill: blocks.append(PILL(p, pill, 56, None, 'center'))
    blocks.append(PANEL(p, [IN(p, sub, 52, name='부제')]))
    place(p, blocks); return p
def body(badge, title, text, ts=88, size=52):
    for s in (ts, 80, 76):
        q = new(); T(q, title, s, align=C_, name='제목')
        if not q.problems: break
    p = new(); place(p, [PILL(p, badge, 52, None, 'center'), T(p, title, s, align=C_, name='제목'), PANEL(p, [IN(p, text, size)])]); return p
def face_page(face, badge, title, text, size=52):
    for fh in (340, 300, 260, 220, 180):
        p = new(); p.bg = 'ink'
        place(p, [FACE(p, face, fh, 'center'), PILL(p, badge, 52, None, 'center'), T(p, title, 84, '#fff', 'title', 1.3, 'center', 900, '제목'), PANEL(p, [IN(p, text, size)])])
        t, bt, c = B.metrics(p)
        if not p.problems and t >= B.TOP - 1 and bt <= B.BOT + 1: break
    return p
def panel_page(badge, title, parts):
    p = new(); kids = [IN(p, t, s, col, name=f'본문{i}') for i, (t, s, col) in enumerate(parts)]
    place(p, [PILL(p, badge, 52, None, 'center'), T(p, title, 84, align=C_, name='제목'), PANEL(p, kids)]); return p
def end_page(q, pill, label, line1, line2, lsize=52):
    p = new(); q = re.sub(r'\*(.+?)\*', r'[[\1]]', q)
    place(p, [T(p, q, 92, '#fff', 'title', 1.3, C_, 900, '질문'), PILL(p, pill, 52, None, 'center'),
              PANEL(p, [IN(p, label, 52, GOLD, lh=1.3, name='라벨'), T(p, line1, 56, '#fff', 'title', 1.5, 'center', 788, '안내', X0 + 56), IN(p, line2, lsize, '#efe9e4', name='안내2')])]); return p

def trial1015():
    return [
        cover('2027 신년 감정서', '먼저 받아 볼\n다섯 분을 찾아요', '여섯 운명학을 겹쳐 읽은 감정서를\n무료로 보내 드려요', '감정서 체험단 모집'),
        body('무엇을 드려요', '신년 감정서\nSTANDARD 한 권', '사주·별자리·숫자 등\n여섯 운명학을 겹쳐 읽은 감정서를\n무료로 보내 드려요.'),
        body('몇 분', '모두 다섯 분', '신년 2분\n연애·궁합 2분\n재물·사업 1분'),
        body('신청 방법', '프로필 링크에서\n신청해요', '생년월일 넣고 무료 풀이 보기\n결과 아래 \'감정서 체험단\' 칸\n지금 고민을 40자 이상 적기'),
        panel_page('부탁드려요', '받은 뒤 7일 안에', [('사이트 후기 1개\n공개 계정 게시물 1개', 52, '#fff'), ('게시물에 꼭 적어 주세요\n"자오선 체험단으로\n감정서를 무료로 받았어요"', 48, GOLD), ('별점과 내용은 느끼신 그대로요', 44, '#efe9e4')]),
        face_page('v2_straight', '일정', '10월 19일까지\n신청해 주세요', '모집 10/15 ~ 10/19\n발표 10/20\n감정서 발송 10/22 ~ 23'),
        end_page('아쉽게 안 되셔도\n*할인*이 있어요', '프로필 링크에서 신청해요', '수신 동의하신 분께', '얼리버드 3,000원\n추가 할인 코드', '신청 칸에서 동의만 체크해 주세요'),
    ]
def follow1016():
    return [
        cover('팔로우 이벤트 · 10/16 ~ 10/29', '2027 신년 감정서,\n매주 한 분께', '팔로우 · 댓글 · 태그\n세 가지면 돼요'),
        panel_page('참여 방법', '세 가지만\n해 주세요', [('① @zaoseon.jeongwol 팔로우', 52, '#fff'), ('② 이 게시물에 댓글\n"내 띠 + 2027년에\n가장 궁금한 것 한 단어"', 52, '#fff'), ('③ 친구 1명 태그', 52, '#fff')]),
        face_page('v5_halfup', '댓글 예시', '이렇게 남겨 주세요', '"토끼띠 · 이직"\n"용띠 · 연애"', 64),
        body('경품', '2027 신년 감정서\nSTANDARD', '매주 한 분, 두 번 드려요\n10월 22일 · 10월 29일 발표'),
        body('발표', '스토리로\n알려 드려요', '당첨되신 분께 DM을 드려요.\nDM 받은 날부터 3일 안에\n답해 주세요.'),
        panel_page('꼭 읽어 주세요', '당첨 조건', [('공개 계정\n이벤트 외 게시물 3개 이상\n계정 개설 30일 이상', 52, '#fff'), ('같은 분이 두 번 당첨되지는 않아요', 44, GOLD), ('태어난 정보는 감정서를 쓰는 데에만 쓰고\n보내 드린 뒤 바로 지워요', 40, '#efe9e4')]),
        end_page('여러분은\n*무슨 띠*인가요?', '댓글로 참여해요', '참여 기간', '10월 16일 ~ 10월 29일', '당첨 소식은 스토리로 알려 드려요'),  # 10/14 대표 재요청 mv7l6sbe: 마지막 장 Instagram 고지 뺌(고지는 캡션에 그대로)
    ]
def shari1020():   # 스레드 1장(캐러셀 아님): 매주 월 생년월일 한 줄 풀이 글 (10/14 대표 문구 확정, '스하리 데이' 말은 넣지 않음)
    # 10/14 대표: 답글이 한 줄이 아니라 마음·관계까지 담으므로 제목을 '한 줄 풀이 드려요' → '생일로 읽는 / 내 마음과 관계'(권장안 2번, 답글 규칙에 관계 문장 추가와 함께)
    # 10/14 대표 재요청 mv7s2ww9 "정월 캐릭터 저렇게 쓰는 게 별로": 가운데 작게 떠 있던 잘린 상반신(v5_halfup)을 빼고,
    # 네이버 대표 이미지처럼 정월(v5_halfup_v2, 콘텐츠_제작_가이드 5-7)을 화면 아래에 붙여 크게 둔다. 뒤에 아치 판. 글 묶음은 위쪽에서 규칙대로.
    for fh, ts in ((600, 96), (580, 96), (560, 96), (540, 96), (520, 92)):
        p = new(); p.bg = 'ink'; p.ai = True; p.face_bottom = True
        blocks = [IN(p, '생일로 읽는', 52, GOLD, lh=1.3, name='라벨'), T(p, '내 마음과 관계', ts, '#fff', 'title', 1.3, C_, 900, '제목'),
                  PANEL(p, [IN(p, '댓글에 양력 생년월일과\n성별을 남겨 주세요', 52, name='안내'), IN(p, '태어난 시간까지 적어 주시면\n조금 더 자세하게 풀어 드려요', 44, '#efe9e4', name='안내2')])]
        gaps = [40, 60]; y = B.TOP
        for b, g in zip(blocks, gaps + [0]): b['draw'](y); y += b['h'] + g
        text_bottom = y; fw = fh * 0.75; fx = (1080 - fw) / 2; ftop = 1440 - fh
        aw = fw * 0.92; ax = (1080 - aw) / 2; atop = ftop + fh * 0.10
        p.html.append(f'<div data-deco="1" style="position:absolute;left:{ax:.0f}px;top:{atop:.0f}px;width:{aw:.0f}px;height:{1440-atop+40:.0f}px;border-radius:{aw/2:.0f}px {aw/2:.0f}px 0 0;background:linear-gradient(180deg,rgba(216,169,92,.30),rgba(216,169,92,.06));z-index:1"></div>')
        p.html.append(f'<img src="data:image/png;base64,{CK.face_b64("v5_halfup_v2")}" style="position:absolute;left:{fx:.0f}px;top:{ftop:.0f}px;height:{fh}px;z-index:2">')
        p.face_top = ftop
        if not p.problems and text_bottom + 40 <= atop: break   # 글 묶음과 아치(정월 머리 위)가 겹치지 않게 40px 띄운다
    else:
        p.problems.append(f'글 묶음 아래 {text_bottom:.0f}가 아치 {atop:.0f}와 겹침')
    return [p]
SINGLE = {'shari1020'}
SETS = {'trial1015': trial1015, 'follow1016': follow1016, 'shari1020': shari1020}

async def main(out, only):
    from playwright.async_api import async_playwright
    from PIL import Image
    import card_kit as CK; from style_spec import check_page
    os.makedirs(out, exist_ok=True); bad = 0
    async with async_playwright() as pw:
        br = await pw.chromium.launch(executable_path='/opt/pw-browsers/chromium'); pg = await br.new_page(viewport={'width': 1080, 'height': 1440})
        for key, fn in SETS.items():
            if only and key not in only: continue
            ps = fn()
            for e in ([] if key in SINGLE else CR.check_count(len(ps), f'{key} 캐러셀')): print('장 수:', e); bad += 1
            for i, p in enumerate(ps, 1):
                n = f'{key}_{i}'; t, b, c = B.metrics(p)
                if getattr(p, 'face_bottom', False): t, b, c = B.TOP, B.BOT, B.CEN   # 정월이 화면 아래에 붙는 장은 바닥·가운데 규칙에서 뺀다(제작 가이드 확정판). 글은 위에서부터 TOP 규칙
                for pr in p.problems: print('엔진:', n, pr); bad += 1
                if t < B.TOP - 1 or b > B.BOT + 1 or abs(c - B.CEN) > 15: print('배치:', n, f'위 {t:.0f} 아래 {b:.0f} 가운데 {c:.0f}'); bad += 1
                open('/tmp/ev.html', 'w', encoding='utf-8').write(CK.page(''.join(p.html) + CK.frame(getattr(p, 'ai', False)), getattr(p, 'bg', 'sun'), GOLD))
                await pg.goto('file:///tmp/ev.html'); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(250)
                for x in await check_page(pg, n, 'bundle'): print('검사:', x); bad += 1
                await pg.screenshot(path=f'{out}/{n}.png'); Image.open(f'{out}/{n}.png').convert('RGB').save(f'{out}/{n}.jpg', quality=92); os.remove(f'{out}/{n}.png')
            print(key, len(ps), '장')
        await br.close()
    print('문제', bad, '건')
if __name__ == '__main__':
    only = set(sys.argv[1].split(',')) if len(sys.argv) > 1 else set()
    asyncio.run(main(os.path.join(HERE, 'cards'), only))
