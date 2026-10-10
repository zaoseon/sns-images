# 자오선 비주얼 방향 3안 시안 (2026-10-10). 같은 주제 1편을 VD-A/B/C 구성 문법으로 각 4장.
# 강조색은 3안 모두 같은 값(ACC)이다. 달라지는 것은 구성(여백·표·대사)이다. 표 값은 시안용 예시다.
import base64, os, sys
from playwright.sync_api import sync_playwright
HERE=os.path.dirname(os.path.abspath(__file__))
CH=os.path.join(HERE,'..','characters','cut')
ACC='#E0A83E'
def b64(name):
    return 'data:image/png;base64,'+base64.b64encode(open(os.path.join(CH,name),'rb').read()).decode()
J={k:b64(v) for k,v in dict(low='v1_lowbun.png',gl='v4_glasses.png',ges='v8_gesture.png',st='v2_straight.png').items()}
SERIF="'Noto Serif CJK KR','Noto Serif CJK JP',serif"; SANS="'Noto Sans CJK KR','Noto Sans CJK JP',sans-serif"
BASE=f"""<html><head><meta charset=utf-8><style>
*{{box-sizing:border-box;margin:0;padding:0}} body{{width:1080px;height:1440px;position:relative;overflow:hidden;font-family:{SANS}}}
.abs{{position:absolute}} .tl{{left:55px;top:50px;font-size:26px;letter-spacing:.12em}} .tr{{right:55px;top:58px;font-size:24px;opacity:.7}}
.hd{{left:55px;bottom:48px;font-size:25px;opacity:.85}} .ai{{right:55px;bottom:46px;font-size:19px;opacity:.55;text-align:right;line-height:1.4}}
.dot{{display:inline-block;width:12px;height:12px;border-radius:50%;background:{ACC};margin-right:10px}}
</style></head><body>"""
def page(inner,bg,fg): return BASE.replace('<body>',f'<body style="background:{bg};color:{fg}">')+inner+'</body></html>'
def chrome(fg,cover=False):
    s=f'<div class="abs tl" style="color:{fg}">자오선</div><div class="abs hd" style="color:{fg}"><span class="dot"></span>zaoseon.com</div>'
    if cover: s+=f'<div class="abs ai" style="color:{fg}">※ 자오선의 상담가 정월은<br>AI로 생성한 가상 캐릭터입니다</div>'
    return s
slides={}
# ---------------- VD-A Editorial Scene: 여백이 주인공, 텍스트 1~2줄, 정월은 작게 ----------------
A_BG='#15161D'; A_FG='#EDE7DB'
meridian=f'<div class="abs" style="left:960px;top:0;width:2px;height:1440px;background:linear-gradient(#0000,{ACC}88 35%,{ACC}88 65%,#0000)"></div>'
slides['A1']=page(chrome(A_FG,True)+meridian+f'''
<div class="abs" style="left:960px;top:640px;width:26px;height:26px;margin:-13px 0 0 -12px;border-radius:50%;background:{ACC}"></div>
<div class="abs tr" style="color:{A_FG}">2027 · 연락</div>
<div class="abs" style="left:110px;top:210px;font-family:{SERIF};font-size:30px;color:{ACC};letter-spacing:.08em">밤 11시, 읽지 않은 메시지</div>
<div class="abs" style="left:110px;top:270px;font-family:{SERIF};font-size:92px;line-height:1.28;font-weight:700">연락을 기다리다<br>지치는 밤에</div>
<img class="abs" src="{J['low']}" style="right:150px;bottom:-30px;width:430px;opacity:.9;-webkit-mask-image:linear-gradient(#000 60%,#0000)">
''',A_BG,A_FG)
slides['A2']=page(chrome(A_FG)+f'''
<div class="abs" style="left:110px;top:520px;font-family:{SERIF};font-size:84px;line-height:1.35;font-weight:700">기다리는 마음에도<br>결이 있어요</div>
<div class="abs" style="left:110px;top:880px;width:760px;font-size:36px;line-height:1.7;opacity:.72">같은 기다림이라도 어떤 사람은 먼저 정리하고,<br>어떤 사람은 한 번 더 기다려요.</div>
<div class="abs" style="left:110px;top:800px;width:120px;height:3px;background:{ACC}"></div>
''',A_BG,A_FG)
slides['A3']=page(chrome(A_FG)+f'''
<div class="abs" style="left:110px;top:430px;font-family:{SERIF};font-size:64px;line-height:1.4;font-weight:700">여러 지도가<br><span style="color:{ACC}">같은 말</span>을 하면<br>결론으로 적고,</div>
<div class="abs" style="left:110px;top:900px;font-family:{SERIF};font-size:64px;line-height:1.4;font-weight:700;opacity:.55">다르게 말하면<br>그곳은 내가 고를 수<br>있는 부분이에요.</div>
''',A_BG,A_FG)
slides['A4']=page(chrome(A_FG)+f'''
<div class="abs" style="left:110px;top:360px;font-family:{SERIF};font-size:30px;color:{ACC}">오늘 밤</div>
<div class="abs" style="left:110px;top:420px;font-family:{SERIF};font-size:80px;line-height:1.35;font-weight:700">하나만<br>정해 보세요</div>
<div class="abs" style="left:110px;top:760px;font-size:36px;line-height:1.7;opacity:.72">답장을 기다릴지,<br>내 하루를 먼저 챙길지.</div>
<div class="abs" style="left:110px;top:1010px;padding:22px 40px;border-radius:60px;background:{ACC};color:#15161D;font-size:32px;font-weight:700">프로필 링크에서 내 첫 글자 1초로 보기</div>
<div class="abs" style="left:110px;top:1120px;font-size:26px;opacity:.55">내일 저녁 · 다음 편</div>
''',A_BG,A_FG)
# ---------------- VD-B Utility Chart: 표가 본체, 결론은 상단 한 줄, 정월은 작은 아바타 ----------------
B_BG='#EEF0F3'; B_FG='#1C2430'; COOL='#2F6F9F'
def ava(img,size=120): return f'<div style="width:{size}px;height:{size}px;border-radius:50%;overflow:hidden;background:#222733;flex:none"><img src="{img}" style="width:{int(size*1.9)}px;margin:{-int(size*0.08)}px 0 0 {-int(size*0.45)}px"></div>'
def head(kicker,title):
    return f'<div class="abs" style="left:55px;top:120px;right:55px"><div style="display:inline-block;padding:8px 22px;border-radius:30px;background:{ACC};color:#1C2430;font-size:26px;font-weight:700">{kicker}</div><div style="margin-top:26px;font-size:68px;line-height:1.28;font-weight:900">{title}</div><div style="margin-top:28px;height:5px;width:100%;background:{ACC}"></div></div>'
def table(rows,top):
    cols=['먼저 연락','기다림','정리']
    h=''.join(f'<div style="flex:1;text-align:center;font-size:28px;font-weight:700;color:#fff">{c}</div>' for c in cols)
    s=f'<div class="abs" style="left:55px;right:55px;top:{top}px"><div style="display:flex;align-items:center;height:76px;background:{COOL};border-radius:14px 14px 0 0"><div style="width:230px;padding-left:28px;font-size:28px;font-weight:700;color:#fff">지도</div>{h}</div>'
    for n,(name,hit) in enumerate(rows):
        cells=''.join(f'<div style="flex:1;text-align:center;font-size:46px;color:{ACC if i in hit else "#C5CBD3"}">{"●" if i in hit else "○"}</div>' for i in range(3))
        s+=f'<div style="display:flex;align-items:center;height:112px;background:{"#fff" if n%2==0 else "#F7F8FA"}"><div style="width:230px;padding-left:28px;font-size:34px;font-weight:700">{name}</div>{cells}</div>'
    return s+'</div>'
rowsB=[('사주',{1}),('별자리',{1}),('생일 숫자',{1}),('자미두수',{2})]
slides['B1']=page(chrome(B_FG,True)+head('교차표 · 연락을 기다릴 때','기다림의 결,<br>네 지도 비교표')+table(rowsB,500)+f'''
<div class="abs" style="left:55px;right:55px;top:1050px;font-size:30px;line-height:1.6">같은 칸에 <span style="color:{ACC}">●</span> 이 몰리면 <b>같은 말</b>, 갈리면 <b>내가 고를 수 있는 곳</b></div>
<div class="abs" style="left:55px;top:1150px;display:flex;gap:20px;align-items:center">{ava(J['st'],110)}<div style="font-size:28px;line-height:1.5">정월의 한 줄<br><b>표를 먼저, 풀이는 그다음에.</b></div></div>
<div class="abs" style="left:55px;bottom:110px;left:55px;font-size:19px;opacity:.5">※ 시안의 표 값은 예시입니다. 실제 제작은 엔진 계산값을 씁니다.</div>
''',B_BG,B_FG)
slides['B2']=page(chrome(B_FG)+head('같은 말','4개 중 3개가<br>"기다림"에 모였어요')+table([('사주',{1}),('별자리',{1}),('생일 숫자',{1}),('자미두수',{2})],520)+f'''
<div class="abs" style="left:55px;right:55px;top:1030px;padding:30px 36px;background:#fff;border-left:8px solid {ACC};font-size:34px;line-height:1.55"><b>읽는 법</b> · 모인 곳은 결론으로, 갈린 곳은 선택지로 적어요.</div>
''',B_BG,B_FG)
slides['B3']=page(chrome(B_FG)+head('갈리는 곳','자미두수만<br>"정리"를 가리켰어요')+f'''
<div class="abs" style="left:55px;right:55px;top:520px;display:flex;gap:30px">
<div style="flex:1;background:#fff;border-radius:18px;padding:36px;height:520px"><div style="font-size:28px;color:{COOL};font-weight:700">같은 말 (3)</div><div style="margin-top:20px;font-size:40px;font-weight:900;line-height:1.4">지금은 서두르지<br>않아도 되는 때</div><div style="margin-top:26px;font-size:28px;line-height:1.6;opacity:.7">사주 · 별자리 · 생일 숫자</div></div>
<div style="flex:1;background:#fff;border-radius:18px;padding:36px;height:520px;border-top:8px solid {ACC}"><div style="font-size:28px;color:#9A6B10;font-weight:700">다른 말 (1)</div><div style="margin-top:20px;font-size:40px;font-weight:900;line-height:1.4">내 쪽에서 먼저<br>정리해 볼 수도</div><div style="margin-top:26px;font-size:28px;line-height:1.6;opacity:.7">자미두수 · 고를 수 있는 부분</div></div></div>
''',B_BG,B_FG)
slides['B4']=page(chrome(B_FG)+head('오늘 해 볼 일','하나만 고르세요')+'<div class="abs" style="left:55px;right:55px;top:520px">'+''.join(f'<div style="display:flex;align-items:center;gap:28px;background:#fff;border-radius:16px;padding:34px 36px;margin-bottom:22px"><div style="width:52px;height:52px;border:4px solid {COOL};border-radius:10px;flex:none"></div><div style="font-size:38px;font-weight:700">{t}</div></div>' for t in ['답장은 내일 아침에 확인하기','연락 대신 내 일정 먼저 챙기기','하고 싶은 말 한 줄 적어 두기'])+f'<div style="margin-top:34px;display:inline-block;padding:22px 40px;border-radius:60px;background:{ACC};font-size:32px;font-weight:700">프로필 링크에서 내 첫 글자 1초로 보기</div></div>',B_BG,B_FG)
# ---------------- VD-C Micro Story: 정월이 주인공 70%, 대사체, 컷 흐름 ----------------
def bubble(txt,left,top,w,tail='left',dark=False):
    bg='#FFF6E0' if not dark else '#232837'; fg='#1C1A16' if not dark else '#EDE7DB'
    return f'<div class="abs" style="left:{left}px;top:{top}px;width:{w}px;background:{bg};color:{fg};border-radius:34px;padding:34px 40px;font-size:44px;line-height:1.5;font-weight:700">{txt}</div>'
def cutchrome(n,fg): return f'<div class="abs tr" style="color:{fg}">{n} / 4</div>'
C1='#2B2220'; C2='#1E2630'; C3='#1A1F2B'; C4='#2A2418'
def glow(c): return f'<div class="abs" style="left:0;top:0;width:1080px;height:1440px;background:radial-gradient(circle at 50% 70%,{c}55,#0000 60%)"></div>'
slides['C1']=page(glow('#C77A4A')+chrome('#EDE7DB',True)+cutchrome(1,'#EDE7DB')+f'''
<img class="abs" src="{J['low']}" style="left:130px;bottom:-60px;width:880px">
{bubble('연락이 늦으면,<br>먼저 마음이 식는 쪽인가요?',55,170,900)}
<div class="abs" style="left:100px;top:100px;font-size:26px;color:{ACC}">정월</div>
''',C1,'#EDE7DB')
slides['C2']=page(glow('#4A6E8F')+chrome('#EDE7DB')+cutchrome(2,'#EDE7DB')+f'''
<img class="abs" src="{J['gl']}" style="left:-120px;bottom:-60px;width:880px">
{bubble('…그냥 기다리게 돼요.',520,170,505,dark=True)}
<div class="abs" style="left:520px;top:395px;font-size:26px;opacity:.6">독자 댓글</div>
{bubble('기다리는 것도<br>하나의 방식이에요.',480,1000,545)}
''',C2,'#EDE7DB')
slides['C3']=page(glow('#4A6E8F')+chrome('#EDE7DB')+cutchrome(3,'#EDE7DB')+f'''
<img class="abs" src="{J['ges']}" style="left:150px;bottom:-60px;width:880px">
{bubble('여섯 지도를 겹쳐 보면<br><span style="color:#B07400">같은 말</span>을 한 곳이 있어요.',55,170,900)}
''',C3,'#EDE7DB')
slides['C4']=page(glow(ACC)+chrome('#EDE7DB')+cutchrome(4,'#EDE7DB')+f'''
<img class="abs" src="{J['low']}" style="left:-60px;bottom:-60px;width:880px">
{bubble('그래서 오늘은 하나만.<br>내 하루 먼저 챙겨 볼까요?',55,170,900)}
<div class="abs" style="right:55px;top:1130px;padding:22px 34px;border-radius:60px;background:{ACC};color:#1C1A16;font-size:30px;font-weight:700;text-align:center;line-height:1.4">프로필 링크에서<br>내 첫 글자 1초로 보기</div>
''',C4,'#EDE7DB')
if __name__=='__main__':
    out=sys.argv[1] if len(sys.argv)>1 else os.path.join(HERE,'out'); os.makedirs(out,exist_ok=True)
    with sync_playwright() as p:
        b=p.chromium.launch(executable_path='/opt/pw-browsers/chromium'); pg=b.new_page(viewport={'width':1080,'height':1440})
        for k,h in slides.items():
            pg.set_content(h); pg.wait_for_timeout(300); pg.screenshot(path=f'{out}/{k}.png')
        b.close()
    from PIL import Image
    ks=list(slides); W,H=360,480
    sheet=Image.new('RGB',(W*4+50,H*3+40),(30,30,34))
    for i,k in enumerate(ks):
        im=Image.open(f'{out}/{k}.png').resize((W,H)); sheet.paste(im,(10+(i%4)*(W+10),10+(i//4)*(H+10)))
    sheet.save(f'{out}/sheet.png')
