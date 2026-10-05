"""돌려쓰기용 새 카드 틀 5종 견본(10/5 대표: 피드가 질리지 않게 틀을 여러 개 두고 돌려 쓴다).
T3 배치표(2축) · T4 순위 사다리 · T5 대화형 · T6 투표(A vs B) · T7 한마디 카드. 견본의 내용은 예시이며 올리기 전에 풀이 기준으로 확정한다.
사용: python3 pipeline/templates_w43.py -> 2026-w43tpl/T3~T7.jpg"""
import base64, asyncio, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style_spec import check_page
from playwright.async_api import async_playwright
def b64(p): return base64.b64encode(open(p,'rb').read()).decode()
BG=b64('characters/cut/bg_sunmoon.jpg'); SKYB=b64('meridian_intro/src/assets/sky.png'); CHARTB=b64('meridian_intro/src/assets/chart.svg'); INTROB=b64('meridian_intro/src/assets/character.png')
F="font-family:'Noto Sans CJK KR','Noto Sans KR',sans-serif;font-weight:900"
INK="#12111a"; PAPER="#f6f1e8"
def face(n): return b64(f'characters/cut/{n}.png')
def handle(c,dark=True):
    col="#fff" if dark else "#222"
    return f'<div style="position:absolute;left:55px;bottom:46px;display:flex;align-items:center;gap:14px;font-size:34px;color:{col};{F}"><span style="width:34px;height:34px;border-radius:50%;background:{c}"></span>zaoseon.com</div>'
def wrap(inner,bg): return f'<html><body style="margin:0;width:1080px;height:1350px;position:relative;overflow:hidden;{F};{bg}">{inner}</body></html>'
def chip(t,c,x,y,fs=34,fg="#111"): return f'<div style="position:absolute;left:{x}px;top:{y}px;background:{c};color:{fg};font-size:{fs}px;padding:10px 26px;border-radius:40px;white-space:nowrap">{t}</div>'
# T3 배치표
def t3():
    A="#ff8a73"
    dots=[("불",A,"#111",760,430),("나무","#7fd6a0","#111",430,470),("쇠","#d9dde3","#111",790,860),("흙","#e8c36a","#111",440,930),("물","#6fb7ff","#111",170,880)]
    d=''.join(chip(n,c,x,y,40,fg) for n,c,fg,x,y in dots)
    inner=f'''<div style="position:absolute;left:70px;top:70px;font-size:36px;color:{A}">정월의 배치표 · 견본</div>
<div style="position:absolute;left:70px;top:130px;width:940px;font-size:72px;line-height:1.4;color:#fff">연락할 때<br>나는 어디에 있을까요?</div>
<div style="position:absolute;left:90px;top:330px;width:900px;height:760px;border:3px solid #ffffff55;border-radius:24px"></div>
<div style="position:absolute;left:540px;top:330px;width:3px;height:760px;background:#ffffff55"></div><div style="position:absolute;left:90px;top:710px;width:900px;height:3px;background:#ffffff55"></div>
<div style="position:absolute;left:0;right:0;top:345px;text-align:center;font-size:40px;color:#fff">먼저 연락해요</div><div style="position:absolute;left:0;right:0;top:1025px;text-align:center;font-size:40px;color:#fff">기다려요</div>
<div style="position:absolute;left:92px;top:665px;font-size:40px;color:#fff">속으로 품어요</div><div style="position:absolute;right:92px;top:665px;font-size:40px;color:#fff">바로 표현해요</div>
{d}<div style="position:absolute;left:70px;right:70px;top:1180px;font-size:36px;color:#fff;text-align:center">내 오행은 어디에 있나요? 댓글로 알려 주세요</div>{handle(A)}'''
    return wrap(inner,f"background:#050912 url(data:image/png;base64,{SKYB}) center/cover;color:#fff")
# T4 순위 사다리
def t4():
    C="#7fd6c8"; rows=[("1","물","깊게 생각해 쓴다"),("2","나무","먼저 말을 꺼낸다"),("3","불","마음이 바로 나온다"),("4","흙","느려도 꾸준하다"),("5","쇠","짧고 분명하다")]
    d=''.join(f'<div style="position:absolute;left:{70+i*28}px;right:{70+i*28}px;top:{330+i*150}px;height:124px;background:#ffffff14;border:2px solid {C};border-radius:26px;display:flex;align-items:center;gap:22px;padding:0 30px;color:#fff"><span style="font-size:64px;color:#fff;width:56px">{n}</span><span style="background:{C};color:#111;font-size:40px;padding:6px 22px;border-radius:30px">{o}</span><span style="font-size:40px">{t}</span></div>' for i,(n,o,t) in enumerate(rows))
    inner=f'''<div style="position:absolute;left:70px;top:70px;font-size:36px;color:{C}">정월의 순위 · 견본</div>
<div style="position:absolute;left:70px;top:130px;width:940px;font-size:72px;line-height:1.4;color:#fff">답장 쓰는 방식<br>오행별로 늘어놓으면?</div>{d}
<div style="position:absolute;left:70px;right:70px;top:1100px;font-size:40px;color:#fff;text-align:center">재미로 본 순위예요. 리듬의 차이일 뿐이에요</div>
<div style="position:absolute;left:70px;right:70px;top:1190px;font-size:40px;color:#fff;text-align:center">내 오행은 몇 번에 있나요?</div>{handle(C)}'''
    inner=f'<img src="data:image/svg+xml;base64,{CHARTB}" style="position:absolute;left:-210px;top:140px;width:1500px;opacity:.28">'+inner
    return wrap(inner,"background:#070b16;color:#fff")
# T5 대화형
def t5():
    C="#f6b042"; fc=face('v3_ponytail')
    def me(t,y): return f'<div style="position:absolute;right:70px;top:{y}px;max-width:640px;background:#fee500;color:#111;font-size:42px;line-height:1.6;padding:28px 36px;border-radius:34px 34px 6px 34px">{t}</div>'
    def jw(t,y): return f'<div style="position:absolute;left:190px;top:{y}px;max-width:700px;background:#fff;color:#111;font-size:42px;line-height:1.6;padding:28px 36px;border-radius:34px 34px 34px 6px">{t}</div><img src="data:image/png;base64,{fc}" style="position:absolute;left:50px;top:{y}px;width:110px;height:110px;border-radius:50%;object-fit:cover;object-position:50% 12%;border:4px solid {C}">'
    inner=f'''<div style="position:absolute;left:70px;top:70px;font-size:36px;color:{C}">정월과 나의 대화 · 견본</div>
<div style="position:absolute;left:70px;top:130px;font-size:64px;line-height:1.4;color:#fff;width:940px">읽씹한 건 아닌데<br>답을 못 하겠어요</div>
{me("읽고도 답장이 안 나가요. 제가 이상한 걸까요?",400)}{jw("이상한 게 아니에요.<br>말을 고르는 중일 수 있어요.",580)}{me("그럼 어떻게 해요?",830)}{jw("한 줄만 먼저 보내 보세요.<br>읽었어, 이따 답할게. 그걸로 충분해요.",940)}
<div style="position:absolute;left:70px;right:70px;top:1220px;font-size:30px;color:#cfc9e0;text-align:center">비슷한 고민이 있다면 댓글로 남겨 주세요</div>{handle(C)}'''
    return wrap(inner,"background:#2b2a3a;color:#fff")
# T6 투표
def t6():
    A="#ff8a73"; B="#6fb7ff"
    inner=f'''<div style="position:absolute;left:0;top:0;width:540px;height:1350px;background:{A}"></div><div style="position:absolute;left:540px;top:0;width:540px;height:1350px;background:{B}"></div>
<div style="position:absolute;left:0;right:0;top:80px;text-align:center;font-size:36px;color:#111">정월의 투표 · 견본</div>
<div style="position:absolute;left:60px;right:60px;top:150px;text-align:center;font-size:70px;line-height:1.4;color:#111">좋아하는 사람에게<br>연락은 누가 먼저?</div>
<div style="position:absolute;left:0;width:540px;top:560px;text-align:center;font-size:260px;color:#111">A</div><div style="position:absolute;left:540px;width:540px;top:560px;text-align:center;font-size:260px;color:#111">B</div>
<div style="position:absolute;left:0;width:540px;top:900px;text-align:center;font-size:46px;color:#111;line-height:1.4">내가<br>먼저 한다</div><div style="position:absolute;left:540px;width:540px;top:900px;text-align:center;font-size:46px;color:#111;line-height:1.4">상대가 할 때<br>기다린다</div>
<div style="position:absolute;left:0;right:0;top:1150px;text-align:center;font-size:42px;color:#111">댓글에 A 또는 B를 남겨 주세요</div>{handle("#111",False)}'''
    return wrap(inner,"background:#222")
# T7 한마디
def t7():
    C="#ffd84d"; fc=INTROB
    inner=f'''<div style="position:absolute;left:70px;top:80px;font-size:36px;color:{C}">정월의 한마디 · 견본</div>
<div style="position:absolute;left:90px;top:230px;width:900px;font-size:92px;line-height:1.45;color:#fff">답장이 늦는 건<br>마음이 식어서가<br>아니라,<br><span style="color:{C}">말을 고르는 중</span><br>일 수 있어요.</div>
<img src="data:image/png;base64,{fc}" style="position:absolute;right:-60px;bottom:0;height:640px">
<div style="position:absolute;left:90px;bottom:150px;font-size:40px;color:#fff;text-shadow:0 0 8px #000">오늘 한 줄만 먼저 보내 보세요</div>{handle(C)}'''
    return wrap(inner,f"background:#050912 url(data:image/png;base64,{SKYB}) center/cover;color:#fff")
async def m():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1080,'height':1350})
        for k,f in (('T3',t3),('T4',t4),('T5',t5),('T6',t6),('T7',t7)):
            await pg.set_content(f()); await pg.wait_for_timeout(300)
            for _i in await check_page(pg, k): print('검사:', _i)
            await pg.screenshot(path=f'2026-w43tpl/{k}.jpg',type='jpeg',quality=92)
        await b.close()
asyncio.run(m())
from PIL import Image
ims=[Image.open(f'2026-w43tpl/{k}.jpg').resize((432,540)) for k in ('T3','T4','T5','T6','T7')]
s=Image.new('RGB',(1296,1080),(20,20,20))
for i,im in enumerate(ims): s.paste(im,((i%3)*432,(i//3)*540))
s.save('/tmp/sheets/tpl.png')
