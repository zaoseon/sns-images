# 자오선 비주얼 방향 3안 시안 v2 (2026-10-10). v1은 저장소의 카드 규칙·도구를 쓰지 않아 폐기했다.
# 쓴 것: pipeline/card_kit.py(배경·정월 컷·말풍선·휴대폰 소품), brand_frame(상단 문구·주소·AI 고지, R01~R03), fonts_kit(페이퍼로지·프리텐다드, R05),
#        style_spec.check_page(글자 크기·굵기·줄간격·대비·겹침 자동 검사). 문안은 이미 발행 예정인 "3초 만에 사랑에 빠지는 사람"(10/10 18:30) 값이다.
# 세 안은 강조색이 같다(금). 달라지는 것은 구성 문법이다.
import sys, os, asyncio
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..', 'pipeline'))
import card_kit as CK
from card_kit import K, BF, page, img_tag, bubble, phone, frame
from style_spec import check_page
from playwright.async_api import async_playwright
ACC = '#f6b042'; CORAL = '#ff8a73'; INK = '#111'
BODY = f"font-family:{K.B};font-weight:800"
def T(txt, top, size, left=90, w=900, color='#fff', align='left', lh=1.3, body=False, extra=''):
    f = BODY if body else ''
    return f'<div style="position:absolute;left:{left}px;top:{top}px;width:{w}px;font-size:{size}px;line-height:{lh};color:{color};text-align:{align};{f};{extra};z-index:5">{txt}</div>'
def pill(txt, left, top, bg=ACC, fg=INK, size=44, w=None):
    ww = f'width:{w}px;' if w else ''
    return f'<div style="position:absolute;left:{left}px;top:{top}px;{ww}background:{bg};color:{fg};font-size:{size}px;padding:14px 42px;border-radius:60px;text-align:center;box-sizing:border-box;z-index:5;{BODY}">{txt}</div>'
S = {}
# ======== VD-A Editorial Scene: 여백이 주인공, 글 2덩어리 이하, 정월은 표지에서만 작게 ========
S['A1'] = (page(
    T('정월의 연애 테스트', 150, 56, color=ACC, body=True) +
    T('3초 만에<br>사랑에 빠지는<br>사람', 330, 112, lh=1.3) +
    img_tag('v4_glasses', 600, 'right:-70px;bottom:0') + frame(True), 'chart', ACC))
S['A2'] = (page(
    T('주변에 꼭<br>한 명 있죠?', 170, 108, lh=1.3) +
    T('사주·별자리·숫자로 보면 이래요.', 1085, 48, color='#fff', body=True, lh=1.5, extra='opacity:.85') + frame(False), 'chart', ACC))
S['A3'] = (page(
    T('세 지도가<br><span style="color:'+ACC+'">같은 말</span>을 해요', 170, 100, lh=1.3) +
    T('바로 달아오르고,<br>먼저 표현하고,<br>새로움에 끌려요.', 940, 52, body=True, lh=1.6, extra='opacity:.9') + frame(False), 'chart', ACC))
S['A4'] = (page(
    T('여러분은<br>몇 개 겹치나요?', 170, 100, lh=1.3) +
    T('하나도 안 겹친다면,<br>천천히 스며드는 사랑을 하는<br>사람일지도 몰라요.', 800, 48, body=True, lh=1.6, extra='opacity:.85') +
    pill('내 숫자를 댓글로 남겨 주세요', 90, 1130, w=900) + frame(False), 'chart', ACC))
# ======== VD-B Utility Chart: 표가 본체, 결론은 위 한 줄, 정월은 작은 얼굴(마지막 장) ========
def row(label, sub, val, top, h=200):
    return (f'<div style="position:absolute;left:90px;top:{top}px;width:900px;height:{h}px;background:rgba(255,255,255,.08);border-radius:28px;z-index:4"></div>'
            f'<div style="position:absolute;left:90px;top:{top}px;width:270px;height:{h}px;display:flex;flex-direction:column;align-items:center;justify-content:center;z-index:5;{BODY}"><div style="font-size:52px;color:{ACC};line-height:1.3">{label}</div><div style="font-size:40px;color:#fff;opacity:.8;line-height:1.3">{sub}</div></div>'
            f'<div style="position:absolute;left:390px;top:{top}px;width:570px;height:{h}px;display:flex;align-items:center;font-size:44px;line-height:1.5;color:#fff;z-index:5;{BODY}">{val}</div>')
S['B1'] = (page(
    pill('정월의 연애 테스트', 75, 122) +
    T('사주 · 별자리 · 숫자,<br>세 지도 교차표', 260, 88, lh=1.3) +
    T('3초 만에 사랑에 빠지는 사람', 560, 52, color=ACC, body=True, lh=1.5) +
    row('사주', '동양', '병화일생, 도화가 있는 사주', 700, 190) + row('별자리', '서양', '양자리 · 사자자리', 920, 190) + row('숫자', '수비학', '3번 · 5번', 1140, 150) + frame(False), 'ink', ACC))
S['B2'] = (page(
    pill('세 지도 교차표', 75, 122) +
    T('태양처럼 바로 달아오르고,<br>사람을 끌어요', 260, 76, lh=1.3) +
    row('사주', '동양', '병화일생,<br>도화가 있는 사주', 600, 210) + row('별자리', '서양', '양자리 · 사자자리<br>직진하는 불의 별자리', 840, 210) + row('숫자', '수비학', '3번 · 5번<br>표현의 3, 새로움에 끌리는 5', 1080, 210) + frame(False), 'ink', ACC))
S['B3'] = (page(
    pill('몇 개 겹치나요?', 75, 122) +
    T('겹친 개수로<br>읽는 법', 260, 92, lh=1.3) +
    row('1개 이상', '겹침', '첫눈에 빠지는 쪽에<br>가까울 수 있어요', 640, 230) + row('0개', '안 겹침', '천천히 스며드는<br>사랑을 하는 사람일지도 몰라요', 920, 230) +
    T('세 지도의 결과를 함께 읽어요.', 1220, 44, body=True, extra='opacity:.8') + frame(False), 'ink', ACC))
S['B4'] = (page(
    pill('결과', 75, 122) +
    T('여러분은<br>몇 개 겹치나요?', 260, 96, lh=1.3) +
    img_tag('v4_glasses', 420, 'left:60px;bottom:330px') +
    T('표를 먼저,<br>풀이는 그다음에 읽어요.', 850, 48, left=430, w=560, body=True, lh=1.6) +
    pill('내 숫자를 댓글로 남겨 주세요', 90, 1190, w=900) + frame(True), 'ink', ACC))
# ======== VD-C Micro Story: 대사 흐름 5컷, 정월 얼굴은 1컷과 5컷만(2/5 = 40%) ========
S['C1'] = (page(
    T('정월의 연애 테스트', 150, 56, color=ACC, body=True) +
    bubble(ACC, '3초 만에 사랑에 빠지는 사람,<br>주변에 꼭 한 명 있죠?', 90, 250, 800).replace('background:#fff','background:#fff') +
    img_tag('v2_straight', 1000, 'right:-120px;bottom:0') + frame(True), 'sun', ACC))
S['C2'] = (page(
    bubble(ACC, '아까 그 사람,<br>계속 생각나요.', 90, 170, 560) +
    bubble(ACC, '만난 지<br>3분인데요?', 430, 1020, 560).replace('left:60px','left:380px') +
    phone(ACC, 90, 560) + frame(False), 'sky', ACC))
S['C3'] = (page(
    T('사주 · 별자리 · 숫자로<br>보면 이래요', 150, 80, lh=1.3) +
    bubble(ACC, '사주 · 병화일생, 도화가 있어요', 90, 440, 900) +
    bubble(ACC, '별자리 · 양자리와 사자자리예요', 90, 740, 900) +
    bubble(ACC, '숫자 · 3번과 5번이에요', 90, 1075, 900) + frame(False), 'sky', ACC))
S['C4'] = (page(
    T('하나도 안 겹친다면', 260, 76, lh=1.3) +
    bubble(ACC, '천천히 스며드는 사랑을<br>하는 사람일지도 몰라요.', 90, 470, 900) +
    T('여러분은 몇 개 겹치나요?', 1085, 56, color=ACC, body=True, lh=1.5) + frame(False), 'chart', ACC))
S['C5'] = (page(
    bubble(ACC, '내 숫자를 댓글로<br>남겨 주세요.', 90, 200, 620) +
    img_tag('v4_glasses', 900, 'left:-60px;bottom:0') +
    pill('프로필 링크에서<br>생년월일을 입력해 보세요', 440, 1060, w=560).replace('padding:14px 42px', 'padding:20px 30px;line-height:1.4') + frame(True), 'sun', ACC))
async def main(out):
    os.makedirs(out, exist_ok=True); CK.CUR = 'pl'; bad = 0
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/opt/pw-browsers/chromium'); pg = await b.new_page(viewport={'width': 1080, 'height': 1440})
        for k, h in S.items():
            open('/tmp/vd2.html', 'w', encoding='utf-8').write(h); await pg.goto('file:///tmp/vd2.html'); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(350)
            for x in await check_page(pg, k, 'cover' if k.endswith('1') else None): print('검사:', x); bad += 1
            await pg.screenshot(path=f'{out}/{k}.png')
        await b.close()
    print('검사 문제', bad, '건')
    from PIL import Image
    ks = list(S); W, H = 300, 400; sheet = Image.new('RGB', (W * 5 + 60, H * 3 + 40), (30, 30, 34))
    for i, k in enumerate(ks):
        r = 0 if k[0] == 'A' else 1 if k[0] == 'B' else 2; c = int(k[1]) - 1
        sheet.paste(Image.open(f'{out}/{k}.png').resize((W, H)), (10 + c * (W + 10), 10 + r * (H + 10)))
    sheet.save(f'{out}/sheet.png')
if __name__ == '__main__': asyncio.run(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'out')))
