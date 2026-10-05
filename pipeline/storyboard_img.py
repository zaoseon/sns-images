"""스토리보드를 그림 한 장으로 만든다(대표가 md 파일을 못 봐서, 앱 '새 영상'에서 바로 보게).
사용: python3 pipeline/storyboard_img.py -> 2026-motion/storyboard_M1.png"""
import os, base64, asyncio
from playwright.async_api import async_playwright
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
CH = base64.b64encode(open(os.path.join(R, "meridian_intro/src/assets/chart.svg"), "rb").read()).decode()
GOLD = "#e7c88d"
SCENES = [("1 훅", "박자 0~4", "금빛 입자 120~200개가 깊이를 두고 떠다님(앞은 크고 흐림)", "3D 깊이 파티클 · 카메라 전진", "내 사주는 혼자 다른 말을 하고 있을까요?"),
          ("2 질문", "박자 4~10", "입자가 여섯 무리로 나뉨", "스태거 · 이징", "1 아니다  2 그럴 수도  3 그렇다"),
          ("3 모임", "박자 10~18", "입자가 흘러 차트 고리가 됨", "모핑 · 비트 싱크", "(글자 없음, 음악에 맞춰 합쳐짐)"),
          ("4 숫자", "박자 18~26", "사주 무리만 따로 떨어짐", "카운트업", "100명 중 약 37명은 사주만 혼자 달랐어요"),
          ("5 결과", "박자 26~30", "차트 완성, 빛이 퍼짐", "홀드", "같은 말은 타고난 결, 다른 말은 내가 고를 곳"),
          ("6 공유", "박자 30~34", "차트가 작아지고 문구 등장", "스태거", "떠오르는 사람에게 보내 보세요")]
def card(i, s):
    return f'''<div class=card><div class=th id=t{i}><canvas width=300 height=533></canvas></div>
<div class=nm>{s[0]} <span>{s[1]}</span></div><div class=tx>{s[2]}</div><div class=mv>{s[3]}</div><div class=sc>"{s[4]}"</div></div>'''
HTML = f'''<!doctype html><meta charset=utf-8><style>
html,body{{margin:0;width:1080px;background:#0b1020;color:#fff;font-family:'Noto Sans CJK KR',sans-serif;font-weight:900}}
.h{{padding:70px 60px 20px}}.k{{font-size:40px;color:{GOLD}}}.tt{{font-size:76px;line-height:1.4;margin-top:14px}}
.info{{display:grid;grid-template-columns:1fr 1fr;gap:22px;padding:20px 60px 10px}}
.i{{background:#161c33;border-radius:26px;padding:24px 30px;font-size:38px;line-height:1.6}}.i b{{color:{GOLD};display:block;font-size:34px}}
.g{{display:grid;grid-template-columns:repeat(3,320px);gap:30px;padding:30px 45px}}
.card{{}} .th{{width:320px;height:569px;border-radius:24px;overflow:hidden;background:#0a1226;border:3px solid #2a3360}}canvas{{width:320px;height:569px;display:block}}
.nm{{font-size:44px;margin-top:16px;color:{GOLD}}}.nm span{{font-size:32px;color:#aab3d6}}.tx{{font-size:36px;line-height:1.5;margin-top:6px}}.mv{{font-size:32px;color:#7fd6c8;margin-top:6px}}.sc{{font-size:32px;line-height:1.5;color:#dfe4f7;margin-top:8px;font-weight:700}}
.f{{margin:20px 60px 70px;background:{GOLD};color:#111;border-radius:30px;padding:34px 40px;font-size:42px;line-height:1.6}}
</style><body>
<div class=h><div class=k>스토리보드 · 승인 요청</div><div class=tt>파티클 편<br>"내 사주는 혼자 다른 말을 하고 있을까요?"</div></div>
<div class=info><div class=i><b>길이·비율</b>약 16초 · 세로</div><div class=i><b>색</b>짙은 남색 + 금색 + 흰색</div>
<div class=i><b>음악</b>느린 곡 (자동 선택, 최근 3편과 다름)</div><div class=i><b>정월 얼굴</b>없음 (차트가 주인공)</div>
<div class=i><b>숫자 출처</b>사주만 혼자 다른 비율 36.5% (자오선 계산)</div><div class=i><b>움직임 규칙</b>입자는 깊이 있게, 숫자는 감속해 올라가고 끝에서 살짝 팝, 바운스는 약하게</div></div>
<div class=g>{"".join(card(i, s) for i, s in enumerate(SCENES))}</div>
<div class=f>고칠 곳이 있으면 채팅으로 알려 주세요.<br>① 주제 문장 ② 선택지 ③ 색 ④ 장면 순서<br>괜찮으면 "그대로 만들어"라고만 하시면 돼요.</div>
<script>
const CHI="data:image/svg+xml;base64,{CH}";let seed=7;const rnd=()=>{{seed=(seed*16807)%2147483647;return seed/2147483647}};
const GOLD='#e7c88d';const COL=['#e7c88d','#7fd6c8','#ff8a73','#8fb7ff','#f6b042','#c9a6ff'];
function pts(n,f){{const a=[];for(let i=0;i<n;i++)a.push(f(i));return a}}
const img=new Image();img.src=CHI;
function draw(i){{const c=document.querySelector('#t'+i+' canvas'),x=c.getContext('2d');x.fillStyle='#0a1226';x.fillRect(0,0,300,533);
 if(i>=2){{x.globalAlpha=0.25;x.drawImage(img,-60,100,420,420);x.globalAlpha=1}}
 const dot=(px,py,col,r=3)=>{{x.fillStyle=col;x.beginPath();x.arc(px,py,r,0,7);x.fill()}};
 const ring=(n,cx,cy,R,off=0)=>{{for(let k=0;k<n;k++){{const a=k/n*6.283+off;dot(cx+R*Math.cos(a),cy+R*Math.sin(a),COL[k%6],3.2)}}}};
 if(i==0){{for(let k=0;k<90;k++)dot(rnd()*300,60+rnd()*400,GOLD,2+rnd()*2);x.fillStyle='#fff';x.font='900 22px sans-serif';x.textAlign='center';x.fillText('내 사주는',150,250);x.fillText('혼자 다른 말을',150,280);x.fillText('하고 있을까요?',150,310)}}
 if(i==1){{const cs=[[70,150],[230,150],[70,260],[230,260],[70,370],[230,370]];cs.forEach((p,k)=>{{for(let j=0;j<14;j++)dot(p[0]+(rnd()-.5)*60,p[1]+(rnd()-.5)*60,COL[k],3)}});[['1',90],['2',150],['3',210]].forEach((p,k)=>{{x.fillStyle=GOLD;x.beginPath();x.arc(p[1],480,18,0,7);x.fill();x.fillStyle='#111';x.font='900 20px sans-serif';x.fillText(p[0],p[1],487)}})}}
 if(i==2){{ring(72,150,266,105);ring(48,150,266,60,0.3)}}
 if(i==3){{ring(60,150,230,95);for(let k=0;k<14;k++)dot(240+(rnd()-.5)*40,410+(rnd()-.5)*40,'#ff8a73',3.4);x.fillStyle='#ff8a73';x.font='900 40px sans-serif';x.textAlign='center';x.fillText('약 37명',150,490)}}
 if(i==4){{const g=x.createRadialGradient(150,266,10,150,266,150);g.addColorStop(0,'rgba(231,200,141,.55)');g.addColorStop(1,'rgba(231,200,141,0)');x.fillStyle=g;x.fillRect(0,0,300,533);ring(72,150,230,100);x.fillStyle='#fff';x.font='900 20px sans-serif';x.textAlign='center';x.fillText('같은 말은 타고난 결',150,420);x.fillText('다른 말은 내가 고를 곳',150,452)}}
 if(i==5){{ring(40,150,150,60);x.fillStyle='#fff';x.font='900 24px sans-serif';x.textAlign='center';x.fillText('떠오르는 사람에게',150,330);x.fillText('보내 보세요',150,366)}}
}}
img.onload=()=>{{for(let i=0;i<6;i++)draw(i);document.title='ok'}};
</script>'''
async def main():
    open("/tmp/sb.html", "w", encoding="utf-8").write(HTML)
    out = os.path.join(R, "2026-motion", "storyboard_M1.png")
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 1080, "height": 1600}); await pg.goto("file:///tmp/sb.html"); await pg.wait_for_function("document.title=='ok'"); await pg.wait_for_timeout(500)
        await pg.screenshot(path=out, full_page=True); await b.close()
    print(out)
asyncio.run(main())
