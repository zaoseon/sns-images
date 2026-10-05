"""스토리보드를 '한 장면 = 한 장'으로 크게 만든다(10/5 대표: 얇고 작고 다닥다닥 붙이지 말라).
규칙: 글자 굵기 800 이상, 본문 글자 44px 이상, 줄간격 1.6 이상, 덩어리 사이 여백 넉넉히. 만든 뒤 style_spec으로 자동 검사한다.
사용: python3 pipeline/storyboard_slides.py -> 2026-motion/sb_M1_01.png ~ 08.png"""
import os, sys, base64, asyncio
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from style_spec import check_page
from playwright.async_api import async_playwright
R = os.path.join(HERE, "..")
CH = base64.b64encode(open(os.path.join(R, "meridian_intro/src/assets/chart.svg"), "rb").read()).decode()
GOLD = "#e7c88d"; TEAL = "#7fd6c8"
SCENES = [("1 훅", "박자 0~4", "금빛 입자 120~200개가 깊이를 두고 떠다녀요", "깊이 있는 파티클, 카메라가 천천히 앞으로", "내 사주는 혼자 다른 말을 하고 있을까요?"),
          ("2 질문", "박자 4~10", "입자가 여섯 무리로 나뉘어요", "무리가 차례로 등장, 강한 ease-out", "1 아니다  2 그럴 수도  3 그렇다"),
          ("3 모임", "박자 10~18", "입자가 흘러 차트 고리가 돼요", "모핑, 음악 박자에 맞춰 합쳐짐", "(글자 없음)"),
          ("4 숫자", "박자 18~26", "사주 무리만 따로 떨어져요", "카운트업: 감속해서 올라가고 끝에서 살짝 팝", "100명 중 약 37명은 사주만 혼자 달랐어요"),
          ("5 결과", "박자 26~30", "차트가 완성되고 빛이 퍼져요", "한 박 가만히 머물기", "같은 말은 타고난 결, 다른 말은 내가 고를 곳"),
          ("6 공유", "박자 30~34", "차트가 작아지고 문구가 올라와요", "차례로 등장", "떠오르는 사람에게 보내 보세요")]
BASE = f'''<!doctype html><meta charset=utf-8><style>
html,body{{margin:0;width:1080px;height:1350px;background:#0b1020;color:#fff;font-family:'Noto Sans CJK KR',sans-serif;font-weight:800;word-break:keep-all;line-break:strict;overflow:hidden;position:relative}}
.k{{position:absolute;left:60px;top:56px;font-size:48px;font-weight:900;color:{GOLD}}}
.nm{{position:absolute;left:60px;top:130px;font-size:96px;font-weight:900;color:{GOLD};line-height:1.3}} .nm span{{font-size:52px;color:#c5cdf0;font-weight:800;margin-left:20px}}
.th{{position:absolute;left:60px;top:300px;width:380px;height:676px;border-radius:28px;overflow:hidden;border:4px solid #3a4585;background:#0a1226}}canvas{{width:380px;height:676px;display:block}}
.col{{position:absolute;left:490px;top:300px;width:530px}}.lb{{font-size:44px;font-weight:900;color:{GOLD};margin-top:0}}.vl{{font-size:54px;font-weight:800;line-height:1.65;margin:8px 0 44px}}.mv{{color:{TEAL}}}
.box{{position:absolute;left:60px;right:60px;top:1020px;background:#161c33;border-radius:32px;padding:34px 44px 38px}}.box .lb{{font-size:44px}}.box .vl{{margin:6px 0 0;font-size:56px;line-height:1.6}}
.info{{position:absolute;left:60px;right:60px;top:380px}}.row{{background:#161c33;border-radius:30px;padding:22px 40px 26px;margin-bottom:22px}}.row .lb{{font-size:44px}}.row .vl{{font-size:52px;margin:6px 0 0;line-height:1.55}}
.t1{{position:absolute;left:60px;top:120px;font-size:80px;font-weight:900;line-height:1.4}}
#c2 .row{{padding:16px 40px 20px;margin-bottom:16px}}#c2 .vl{{font-size:50px;line-height:1.5}}
</style><body>'''
JS = f'''<script>
const CHI="data:image/svg+xml;base64,{CH}";let seed=7;const rnd=()=>{{seed=(seed*16807)%2147483647;return seed/2147483647}};
const GOLD='#e7c88d';const COL=['#e7c88d','#7fd6c8','#ff8a73','#8fb7ff','#f6b042','#c9a6ff'];
const img=new Image();img.src=CHI;
function draw(i){{const c=document.getElementById('cv'),x=c.getContext('2d');x.setTransform(1.2667,0,0,1.2667,0,0);x.fillStyle='#0a1226';x.fillRect(0,0,300,533);
 if(i>=2){{x.globalAlpha=0.25;x.drawImage(img,-60,100,420,420);x.globalAlpha=1}}
 const dot=(px,py,col,r=3)=>{{x.fillStyle=col;x.beginPath();x.arc(px,py,r,0,7);x.fill()}};
 const ring=(n,cx,cy,R,off=0)=>{{for(let k=0;k<n;k++){{const a=k/n*6.283+off;dot(cx+R*Math.cos(a),cy+R*Math.sin(a),COL[k%6],3.2)}}}};
 x.textAlign='center';
 if(i==0){{for(let k=0;k<90;k++)dot(rnd()*300,60+rnd()*400,GOLD,2+rnd()*2);x.fillStyle='#fff';x.font='900 22px sans-serif';x.fillText('내 사주는',150,250);x.fillText('혼자 다른 말을',150,280);x.fillText('하고 있을까요?',150,310)}}
 if(i==1){{[[70,150],[230,150],[70,260],[230,260],[70,370],[230,370]].forEach((p,k)=>{{for(let j=0;j<14;j++)dot(p[0]+(rnd()-.5)*60,p[1]+(rnd()-.5)*60,COL[k],3)}});[['1',90],['2',150],['3',210]].forEach(p=>{{x.fillStyle=GOLD;x.beginPath();x.arc(p[1],480,18,0,7);x.fill();x.fillStyle='#111';x.font='900 20px sans-serif';x.fillText(p[0],p[1],487)}})}}
 if(i==2){{ring(72,150,266,105);ring(48,150,266,60,0.3)}}
 if(i==3){{ring(60,150,230,95);for(let k=0;k<14;k++)dot(240+(rnd()-.5)*40,410+(rnd()-.5)*40,'#ff8a73',3.4);x.fillStyle='#ff8a73';x.font='900 40px sans-serif';x.fillText('약 37명',150,490)}}
 if(i==4){{const g=x.createRadialGradient(150,266,10,150,266,150);g.addColorStop(0,'rgba(231,200,141,.55)');g.addColorStop(1,'rgba(231,200,141,0)');x.fillStyle=g;x.fillRect(0,0,300,533);ring(72,150,230,100);x.fillStyle='#fff';x.font='900 20px sans-serif';x.fillText('같은 말은 타고난 결',150,420);x.fillText('다른 말은 내가 고를 곳',150,452)}}
 if(i==5){{ring(40,150,150,60);x.fillStyle='#fff';x.font='900 24px sans-serif';x.fillText('떠오르는 사람에게',150,330);x.fillText('보내 보세요',150,366);
   x.fillStyle='#e7c88d';x.beginPath();x.moveTo(190,420);x.lineTo(250,445);x.lineTo(205,455);x.lineTo(200,480);x.lineTo(185,458);x.lineTo(170,450);x.closePath();x.fill()}}
 if(i==9){{const g=x.createRadialGradient(150,300,10,150,300,220);g.addColorStop(0,'rgba(231,200,141,.35)');g.addColorStop(1,'rgba(231,200,141,0)');x.fillStyle=g;x.fillRect(0,0,300,533);
   x.globalAlpha=.55;x.drawImage(img,-40,140,380,380);x.globalAlpha=1;
   x.fillStyle='#e7c88d';x.beginPath();x.roundRect(80,96,140,30,15);x.fill();x.fillStyle='#111';x.font='900 15px sans-serif';x.fillText('정월의 숫자 퀴즈',150,117);
   x.fillStyle='#fff';x.font='900 36px sans-serif';x.fillText('내 사주는',150,215);x.fillText('혼자 다른 말을',150,262);x.fillText('하고 있을까요?',150,309);
   x.setLineDash([6,5]);x.strokeStyle='#ff8a73';x.lineWidth=2;x.strokeRect(2,66,296,400);x.setLineDash([])}}
 document.title='ok'}}
'''
def slide_scene(i, s):
    return BASE + f'<div class=k>스토리보드 · 장면 {i+1} / 6</div><div class=nm>{s[0]}<span>{s[1]}</span></div><div class=th><canvas id=cv width=380 height=676></canvas></div>' \
        f'<div class=col><div class=lb>화면</div><div class=vl>{s[2]}</div><div class=lb>움직임</div><div class="vl mv">{s[3]}</div></div>' \
        f'<div class=box><div class=lb>화면 글자</div><div class=vl>"{s[4]}"</div></div>' + JS + f'img.onload=()=>draw({i});</script>'
S1 = BASE + '''<div class=k>스토리보드 · 승인 요청</div><div class=t1>파티클 편<div style="font-size:64px;line-height:1.5;margin-top:8px">내 사주는 혼자 다른 말을<br>하고 있을까요?</div></div><div class=info style="top:520px">
<div class=row><div class=lb>길이 · 색</div><div class=vl>약 16초 세로 · 남색+금색+흰색</div></div>
<div class=row><div class=lb>음악 · 정월 얼굴</div><div class=vl>느린 곡 자동 선택 · 얼굴 없음</div></div>
<div class=row><div class=lb>숫자 출처</div><div class=vl>사주만 혼자 다른 비율 36.5% (자오선 계산)</div></div>
</div><script>document.title='ok'</script>'''
S_COVER = BASE + f'<div class=k>스토리보드 · 표지</div><div class=nm style="font-size:84px">표지<span>프로필 격자에 보이는 그림</span></div><div class=th><canvas id=cv width=380 height=676></canvas></div>' \
    '<div class=col><div class=lb>글자</div><div class=vl>제목 3줄, 아주 크게</div><div class=lb>색</div><div class="vl mv">남색 + 금색 + 흰색 (최근 표지와 다름)</div></div>' \
    '<div class=box><div class=lb>표지 글자</div><div class=vl>내 사주는 혼자 다른 말을 하고 있을까요?</div></div>' + JS + 'img.onload=()=>draw(9);</script>'
S_CTA = BASE + '''<div class=k>스토리보드 · CTA</div><div class=t1 style="top:120px">CTA<span style="font-size:56px;margin-left:22px;color:#c5cdf0">끝 2초 · 캡션 · 링크</span></div><div class=info style="top:270px" id=c2>
<div class=row><div class=lb>끝 2초 화면</div><div class=vl>"떠오르는 사람에게 보내 보세요"<br>+ 종이비행기</div></div>
<div class=row><div class=lb>캡션 마지막 줄</div><div class=vl>맞으면 ♥, 떠오르는 사람에게<br>보내 보세요</div></div>
<div class=row><div class=lb>이번 편에 넣지 않는 것</div><div class=vl>프로필 링크 문구<br>(하루 1건에만 넣는 규칙)</div></div>
<div class=row style="background:#e7c88d;color:#111;margin-bottom:0"><div class=lb style="color:#111">대표님께 질문</div><div class=vl style="font-weight:900">프로필 링크 문구도 넣을까요?</div></div></div><script>document.title='ok'</script>'''
S8 = BASE + '''<div class=k>스토리보드 · 마지막</div><div class=t1 style="top:150px">고칠 곳이 있으면<br>번호로 알려 주세요</div><div class=info style="top:450px">
<div class=row><div class=vl>① 주제 문장</div></div><div class=row><div class=vl>② 선택지</div></div><div class=row><div class=vl>③ 색</div></div><div class=row><div class=vl>④ 장면 순서</div></div>
<div class=row style="background:#e7c88d;color:#111"><div class=vl style="font-weight:900">괜찮으면 "그대로 만들어"</div></div></div><script>document.title='ok'</script>'''
async def main():
    slides = [S1, S_COVER] + [slide_scene(i, s) for i, s in enumerate(SCENES)] + [S_CTA, S8]; bad = 0; outs = []
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 1080, "height": 1350})
        for n, h in enumerate(slides, 1):
            open("/tmp/sbs.html", "w", encoding="utf-8").write(h); await pg.goto("file:///tmp/sbs.html"); await pg.wait_for_function("document.title=='ok'"); await pg.wait_for_timeout(300)
            for x in await check_page(pg, f"sb{n:02d}", "cover"): print("검사:", x); bad += 1
            o = os.path.join(R, "2026-motion", f"sb_M1_{n:02d}.png"); await pg.screenshot(path=o); outs.append(o)
        await b.close()
    print("검사 문제", bad, "건,", len(outs), "장")
asyncio.run(main())
