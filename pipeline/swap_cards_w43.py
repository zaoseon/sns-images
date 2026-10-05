import base64,asyncio
from playwright.async_api import async_playwright
def b64(p): return base64.b64encode(open(p,'rb').read()).decode()
BG=b64('characters/cut/bg_sunmoon.jpg')
F="font-family:'Noto Sans CJK KR','Noto Sans KR',sans-serif;font-weight:800"
def handle(c): return f'<div style="position:absolute;left:55px;bottom:48px;display:flex;align-items:center;gap:14px;font-size:34px;color:#fff;{F}"><span style="width:34px;height:34px;border-radius:50%;background:{c};display:inline-block"></span>zaoseon.com</div>'
def cover(face,acc,badge,sub,title):
    ch=b64(f'characters/cut/{face}.png')
    return f"""<body style="margin:0;width:1080px;height:1350px;background:#0b0806;position:relative;overflow:hidden;{F};color:#fff">
<div style="position:absolute;left:75px;top:78px;background:{acc};color:#111;font-size:44px;padding:16px 42px;border-radius:60px">{badge}</div>
<div style="position:absolute;left:90px;top:225px;font-size:54px;line-height:1.3;color:{acc}">{sub}</div>
<div style="position:absolute;left:90px;top:430px;font-size:100px;line-height:1.2;z-index:3">{title}</div>
<img src="data:image/png;base64,{ch}" style="position:absolute;right:-150px;bottom:0;height:760px;z-index:1">
{handle(acc)}
<div style="position:absolute;right:46px;bottom:34px;text-align:right;font-size:23px;color:#fff;line-height:1.3;z-index:4;text-shadow:0 0 6px #000,0 0 10px #000">※ 자오선의 상담가 정월은<br>AI로 생성한 가상 캐릭터입니다</div></body>"""
def band(acc,badge,title,body,foot='',bs=40):
    return f"""<body style="margin:0;width:1080px;height:1350px;background:#181615;position:relative;overflow:hidden;{F};color:#fff">
<div style="position:absolute;left:0;right:0;top:216px;height:914px;background:url(data:image/jpeg;base64,{BG}) center/cover"></div>
<div style="position:absolute;left:0;right:0;top:216px;height:914px;background:rgba(5,5,15,.35)"></div>
<div style="position:absolute;left:0;right:0;top:290px;text-align:center"><span style="background:{acc};color:#111;font-size:44px;padding:14px 46px;border-radius:60px">{badge}</span></div>
<div style="position:absolute;left:0;right:0;top:420px;text-align:center;font-size:84px;line-height:1.25">{title}</div>
<div style="position:absolute;left:0;right:0;top:740px;text-align:center;font-size:{bs}px;line-height:1.7;color:#efe9e4">{body}</div>
{('<div style="position:absolute;left:0;right:0;top:1180px;text-align:center;font-size:34px;color:'+acc+'">'+foot+'</div>') if foot else ''}
{handle(acc)}</body>"""
A='#ff8a73'; B='#f6b042'
sets={
 'a_1009':[cover('v2_straight',A,'정월의 연애 테스트','한 번 정하면 뒤돌아보지 않는 나','연애에서도<br>몇 개 해당돼요?'),
   band(A,'선택지','세 가지 중<br>몇 개예요?','1 마음이 식으면 정리가 빨라요<br>2 좋아하면 먼저 표현해요<br>3 헤어진 뒤 뒤돌아본 적이 드물어요'),
   band(A,'결과','2개 이상이라면','확신이 빠른 만큼 상대는 갑작스럽게 느낄 수 있어요.<br>정리하기 전에 이유를 한 문장으로<br>말해 주세요.','내 숫자를 댓글로 남겨 주세요',36)],
 'b_1011':[cover('v3_ponytail',B,'정월의 관계 테스트','먼저 말하지 못하고<br>기다리다 놓친 사람이 있다면','나는 몇 개<br>해당돼요?'),
   band(B,'선택지','세 가지 중<br>몇 개예요?','1 상대가 먼저 말해 주길 기다려요<br>2 말할까 고민하다 때를 놓친 적 있어요<br>3 놓치고 나서야 말할걸 생각해요'),
   band(B,'결과','2개 이상이라면','말이 느린 게 아니라<br>거절을 먼저 헤아리는 쪽일 수 있어요.<br>이번 주에 안부 한 줄을 먼저 보내 보세요.','내 숫자를 댓글로 남겨 주세요',36)],
}
async def m():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1080,'height':1350})
        for k,s in sets.items():
            for i,h in enumerate(s,1):
                await pg.set_content('<html>'+h+'</html>'); await pg.wait_for_timeout(300)
                await pg.screenshot(path=f'2026-w43swap/cards/{k}_{i}.jpg',type='jpeg',quality=92)
        await b.close()
asyncio.run(m())
from PIL import Image
ims=[Image.open(f'2026-w43swap/cards/{k}_{i}.jpg').resize((360,450)) for k in('a_1009','b_1011') for i in (1,3)]
s=Image.new('RGB',(1440,450))
for n,im in enumerate(ims): s.paste(im,(n*360,0))
s.save('/tmp/sheets/cards2.png')
