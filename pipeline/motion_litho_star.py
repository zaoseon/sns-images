"""리소그래프 6판 '내 별자리, 사주랑 같은 말 할까?' — 별빛 배경판(10/6 대표 지적 반영).
지적: ①글자를 더 가운데로, "같은 말"을 사주·별자리와 같은 줄로 ②배경은 해·달·별이 있는 우리 소재로 ③UI에 가려지는 위아래도 알차게 채우고 글자는 크게 ④표지와 CTA가 없다.
소재: assets/brand_bg (남색 별빛 아틀라스를 돌려 위·아래에 성운, 금빛 황도 차트, 해·달 잘라냄). 숫자: content/cross_data/README.md '태양별자리별 일치율'.
규칙: 글자 단색(흰색·금색), 색 그림자 없음, 도형 경계에 글자가 걸치지 않음, 첫 프레임 완성, 문장 2초 이상.
사용: python3 pipeline/motion_litho_star.py -> 2026-motion/litho_star6.mp4 + litho_star6_cover.jpg"""
import os, sys, asyncio
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import music_plan as MP, html_motion as HM, fonts_kit as K
R = os.path.abspath(os.path.join(HERE, ".."))
AS = os.path.join(R, "assets", "brand_bg")
GOLD = "#e7c88d"; PINK = "#ff5c9d"; BLUE = "#4560f0"
RANK = [("염소", 23.0), ("황소", 22.7), ("처녀", 18.1), ("사자", 16.3), ("물병", 14.1), ("사수", 13.4), ("쌍둥이", 12.9), ("게", 12.6), ("양", 9.9), ("전갈", 7.3), ("물고기", 6.1), ("천칭", 5.6)]
def html(beat):
    bars = "".join(f'<div class="a bar" id=bar{i} style="top:{540 + i * 77}px"><div class="a d bl">{n}</div><div class="a d bv">{v:.1f}%</div></div>' for i, (n, v) in enumerate(RANK))
    h = """<!doctype html><meta charset=utf-8><style>@@FONTS@@
html,body{margin:0;width:1080px;height:1920px;overflow:hidden;background:#050a1c;font-family:'JW-B',sans-serif;font-weight:800;color:#fff;word-break:keep-all}
.a{position:absolute}.d{font-family:'JW-D',sans-serif;font-weight:900}.t{text-align:center;white-space:nowrap}
#bg{left:0;top:0;width:1080px;height:1920px}
#chart{left:-60px;top:360px;width:1200px;height:1200px;opacity:.42}
#sun{left:60px;top:90px;width:300px;height:288px;mix-blend-mode:screen;-webkit-mask-image:radial-gradient(circle,#000 52%,transparent 74%)}
#moon{left:730px;top:70px;width:262px;height:288px;mix-blend-mode:screen;-webkit-mask-image:radial-gradient(circle,#000 52%,transparent 74%)}
.cover #sun{left:20px;top:300px;width:230px;height:221px}.cover #moon{left:834px;top:290px;width:216px;height:238px}
.vig{left:0;top:0;width:1080px;height:1920px;background:radial-gradient(ellipse 62% 40% at 50% 52%,rgba(4,8,26,.62),transparent 78%)}
.grp{left:0;top:0;width:1080px;height:1920px;isolation:isolate}
.c{border-radius:50%;mix-blend-mode:multiply;will-change:transform,opacity}
.lab{transform:translate(-50%,-50%);line-height:1}
.bar{left:70px;height:66px;width:0;border-radius:0 33px 33px 0;background:linear-gradient(90deg,#6a3fc8,#ff5c9d);opacity:0;overflow:hidden}
.bl{left:26px;top:7px;font-size:52px;line-height:1.15;color:#fff}.bv{right:26px;top:7px;font-size:52px;line-height:1.15;color:#fff}
.top1{background:linear-gradient(90deg,#c9a24a,#e7c88d)}.top1 .bl,.top1 .bv{color:#17102b}
</style><body>
<img class="a" id=bg src="file://@@BG@@">
<img class="a" id=chart src="file://@@CHART@@">
<img class="a" id=sun src="file://@@SUN@@"><img class="a" id=moon src="file://@@MOON@@">
<div class="a vig"></div><svg class="a" id=stars width=1080 height=1920 style="left:0;top:0"></svg>
<div class="a d t" id=hl style="left:0;width:1080px;top:330px;font-size:112px;line-height:1.22">내 별자리,<br>사주랑 같은 말<br>할까?</div>
<div class="a grp" id=grp>
 <div class="a c" id=pinkC style="left:50px;top:790px;width:640px;height:640px;background:@@PINK@@"></div>
 <div class="a c" id=blueC style="left:390px;top:790px;width:640px;height:640px;background:@@BLUE@@"></div>
</div>
<div class="a c" id=blueD style="left:390px;top:790px;width:640px;height:640px;box-sizing:border-box;border:8px dashed @@BLUE@@;background:transparent;opacity:.7;mix-blend-mode:normal"></div>
<div class="a d t lab" id=wSaju style="left:215px;top:1110px;font-size:122px">사주</div>
<div class="a d t lab" id=wStar style="left:866px;top:1110px;font-size:92px">별자리</div>
<div class="a d t lab" id=wSame style="left:540px;top:1110px;font-size:68px">같은 말</div>
<div class="a d t" id=rk style="left:0;width:1080px;top:340px;font-size:66px;line-height:1.25;opacity:0">사주와 같은 말을 하는<br>별자리 순위</div>
@@BARS@@
<div class="a d t" id=c1 style="left:0;width:1080px;top:520px;font-size:116px;line-height:1.22;opacity:0">내 별자리는</div>
<div class="a d t" id=c2 style="left:0;width:1080px;top:670px;font-size:116px;line-height:1.22;opacity:0;color:@@GOLD@@">몇 위일까요?</div>
<div class="a d t" id=c3 style="left:0;width:1080px;top:880px;font-size:78px;line-height:1.3;opacity:0">댓글로 알려 주세요</div>
<div class="a d t" id=c4 style="left:0;width:1080px;top:990px;font-size:66px;line-height:1.3;opacity:0">친구 별자리도 보내 보세요</div>
<svg class="a" id=plane viewBox="0 0 100 100" style="left:410px;top:1130px;width:260px;height:260px;opacity:0"><path d="M8 52 L92 10 L66 90 L50 60 Z" fill="@@GOLD@@"/><path d="M30 46 L92 10 L50 60 Z" fill="#b8903c"/></svg>
<script>
const BEAT=@@BEAT@@, B=ms=>ms/1000/BEAT, cl=(x,a=0,b=1)=>Math.min(b,Math.max(a,x));
function bez(x1,y1,x2,y2){return t=>{if(t<=0)return 0;if(t>=1)return 1;let a=0,b=1,u=t;for(let i=0;i<24;i++){const x=3*(1-u)*(1-u)*u*x1+3*(1-u)*u*u*x2+u*u*u;if(x<t)a=u;else b=u;u=(a+b)/2}return 3*(1-u)*(1-u)*u*y1+3*(1-u)*u*u*y2+u*u*u}}
const out=bez(.23,1,.32,1), g=id=>document.getElementById(id), NS='http://www.w3.org/2000/svg';
const VAL=@@VALS@@; let seed=5; const rnd=()=>{seed=(seed*16807)%2147483647;return seed/2147483647};
const SP=[]; for(let i=0;i<70;i++){const c=document.createElementNS(NS,'circle');const y=rnd()<.55?rnd()*330:(rnd()<.5?1470+rnd()*450:330+rnd()*1140);c.setAttribute('cx',rnd()*1080);c.setAttribute('cy',y);c.setAttribute('r',1.6+rnd()*3.2);c.setAttribute('fill',rnd()<.5?'#e7c88d':'#ffffff');g('stars').appendChild(c);SP.push([c,rnd()*6.28,.25+rnd()*.6])}
let b=0;
function lab(id,o,s){const e=g(id);e.style.opacity=o;e.style.transform=`translate(-50%,-50%) scale(${s})`}
function seek(ms){b=B(ms);
 const ph=b-Math.floor(b), pulse=0.03*Math.exp(-ph*5), fo=1-cl((b-8)/.6);
 // 배경: 황도 차트가 천천히 돈다, 해와 달은 박자에 맞춰 살짝 숨 쉼, 별은 반짝임
 g('chart').style.transform=`rotate(${b*1.6}deg) scale(${1+pulse*.3})`; g('sun').style.transform=`scale(${1+pulse*.9}) rotate(${b*2}deg)`; g('moon').style.transform=`scale(${1+pulse*.9})`;
 SP.forEach(o=>o[0].setAttribute('opacity',(0.25+0.75*Math.abs(Math.sin(b*.9+o[1])))*o[2]+0.1));
 // 장면 1: 헤드라인 + 두 원 + 같은 줄 라벨
 g('hl').style.opacity=fo; g('hl').style.transform=`scale(${1+0.02*cl(b/8)+pulse*.6})`;
 const ps=out(cl(b/.45)), s0=1.1+(1-1.1)*ps;
 g('pinkC').style.transform=`scale(${s0*(1+pulse*.5)})`; const bp=out(cl((b-3)/.45)), bo=b<3?0:Math.min(1,bp*6), bs=1.18+(1-1.18)*bp;
 g('blueC').style.opacity=bo; g('blueC').style.transform=`scale(${bo?bs*(1+pulse*.5):1})`; g('blueD').style.opacity=(b<3?.7:0)*fo; g('blueD').style.transform=`rotate(${b*9}deg)`;
 g('grp').style.opacity=fo;
 lab('wSaju',fo,s0*(1+pulse*.5)); lab('wStar',(b<3?0:bo)*fo,bo?bs:1);
 const ss=out(cl((b-4)/.4)); lab('wSame',(b<4?0:Math.min(1,ss*6))*fo,b<4?1:1.3+(1-1.3)*ss);
 // 장면 2: 순위(박 9~19, 천칭부터 염소까지 한 박에 하나)
 const rf=1-cl((b-20.6)/.6); g('rk').style.opacity=cl((b-8.8)/.5)*rf;
 for(let i=0;i<12;i++){const t0=9+(11-i)*.9, q=out(cl((b-t0)/.6)); const el=g('bar'+i); el.style.opacity=q*rf; el.style.width=(190+VAL[i]*30*q)+'px'; if(i===0){el.classList.add('top1'); el.style.transform=`scaleY(${1+(b>19&&b<20.6?pulse*1.6:0)})`}}
 // 장면 3: CTA(박 21.2~28)
 const cp=b>21?1:0; g('c1').style.opacity=cl((b-21.2)/.4); g('c2').style.opacity=cl((b-22.2)/.4); g('c3').style.opacity=cl((b-23.6)/.4); g('c4').style.opacity=cl((b-24.8)/.4);
 const pf=out(cl((b-25.4)/.8)); g('plane').style.opacity=cl((b-25.4)/.3); g('plane').style.transform=`translate(${(1-pf)*-170}px,${(1-pf)*130}px) rotate(${-8+8*pf}deg) scale(${1+(b>26.4?pulse*.7:0)})`;
}
seek(0);
</script>"""
    for k, v in {"@@FONTS@@": K.css("gm"), "@@BG@@": os.path.join(AS, "derived", "bg_cosmos.jpg"), "@@CHART@@": os.path.join(AS, "chart.png"), "@@SUN@@": os.path.join(AS, "derived", "sun.png"), "@@MOON@@": os.path.join(AS, "derived", "moon.png"),
                 "@@PINK@@": PINK, "@@BLUE@@": BLUE, "@@GOLD@@": GOLD, "@@BEAT@@": repr(beat), "@@BARS@@": bars, "@@VALS@@": str([v for _, v in RANK])}.items(): h = h.replace(k, v)
    return h
async def cover(hp, beat, out):
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 1080, "height": 1920}); await pg.goto("file://" + hp); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(600)
        await pg.evaluate("document.body.classList.add('cover')"); await pg.evaluate(f"seek({6.5 * beat * 1000})"); await pg.wait_for_timeout(300); await pg.screenshot(path=out, type="jpeg", quality=92); await b.close()
if __name__ == "__main__":
    mi = MP.choose("data", "litho-star6"); beat = 60.0 / mi["bpm"]; nb = 28; total = nb * beat
    hp = "/tmp/litho_star.html"; open(hp, "w", encoding="utf-8").write(html(beat))
    outp = os.path.join(R, "2026-motion", "litho_star6.mp4"); secs = HM.render_html(hp, outp, total)
    MP.mux(outp, [3 * beat, 5 * beat, 13 * beat, 7 * beat], mi, 103)
    asyncio.run(cover(hp, beat, os.path.join(R, "2026-motion", "litho_star6_cover.jpg")))
    print("음악:", mi["style"], mi["bpm"], mi["key"], "| 박자", round(beat, 3), "초 | 길이", round(secs, 1), "초")
