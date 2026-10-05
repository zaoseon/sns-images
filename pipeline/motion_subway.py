"""지하철 노선도 모션그래픽 '내 인생 노선도'(10/5, 스타일 30 가이드의 노선도 프롬프트를 자오선 내용으로 바꿈).
역 6개 = 10년 단위 6칸(대운의 비유), 질문은 "지금 내 역은?"(번호로 댓글). 숫자·풀이 단정 없음.
규칙: 첫 프레임 완성, 글자 단색·굵게·크게, 글자는 도형 경계에 걸치지 않음, 화면을 채움, 박자에 맞춰 움직임.
사용: python3 pipeline/motion_subway.py -> 2026-motion/subway_life.mp4"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import music_plan as MP, html_motion as HM, fonts_kit as K
CORAL = "#ff6b57"; MINT = "#2bc5a0"; BLUE = "#4a7bff"; INK = "#17102b"; PAPER = "#fbf8f1"
def html(beat):
    h = """<!doctype html><meta charset=utf-8><style>@@FONTS@@
html,body{margin:0;width:1080px;height:1920px;overflow:hidden;background:@@PAPER@@;font-family:'JW-B',sans-serif;font-weight:800;color:@@INK@@;word-break:keep-all}
.a{position:absolute}.d{font-family:'JW-D',sans-serif;font-weight:900}.t{text-align:center;white-space:nowrap}
.grid{left:0;top:0;width:1080px;height:1920px;background-image:linear-gradient(#e9e2d2 2px,transparent 2px),linear-gradient(90deg,#e9e2d2 2px,transparent 2px);background-size:90px 90px;opacity:.7}
.board{left:60px;top:1190px;width:960px;height:270px;background:@@INK@@;border-radius:44px;color:#fff;overflow:hidden}
.bt{left:0;width:960px;text-align:center;white-space:nowrap}
svg text{font-family:'JW-D',sans-serif;font-weight:900}
</style><body>
<div class="a grid"></div>
<svg class="a" id=decor width=1080 height=1920 viewBox="0 0 1080 1920" style="left:0;top:0">
 <path d="M-60 660 L300 660 L360 720 L1140 720" stroke="@@BLUE@@" stroke-width="22" fill="none" opacity=".35" stroke-linejoin="round"/>
 <path d="M-60 1110 L420 1110 L520 1010 L1140 1010" stroke="@@MINT@@" stroke-width="22" fill="none" opacity=".4" stroke-linejoin="round"/>

 <path d="M-60 170 L520 170 L580 230 L1140 230" stroke="@@CORAL@@" stroke-width="20" fill="none" opacity=".28" stroke-linejoin="round"/>
 <path d="M-60 290 L240 290 L300 230 L1140 230" stroke="@@MINT@@" stroke-width="20" fill="none" opacity=".3" stroke-linejoin="round"/>
 <path d="M-60 1590 L380 1590 L440 1650 L1140 1650" stroke="@@BLUE@@" stroke-width="22" fill="none" opacity=".32" stroke-linejoin="round"/>
 <path d="M-60 1740 L620 1740 L690 1670 L1140 1670" stroke="@@CORAL@@" stroke-width="22" fill="none" opacity=".3" stroke-linejoin="round"/>
 <path d="M-60 1860 L1140 1860" stroke="@@MINT@@" stroke-width="22" fill="none" opacity=".35"/>
 <g id=ticks></g>
 <path id=route d="M-60 800 L250 800 L410 960 L700 960 L860 800 L1140 800" stroke="@@CORAL@@" stroke-width="52" fill="none" stroke-linejoin="round" stroke-linecap="butt"/>
 <g id=train></g>
 <g id=stations></g>
</svg>
<div class="a d t" id=title style="left:0;width:1080px;top:340px;font-size:128px;line-height:1.2">내 인생 노선도</div>
<div class="a t" id=sub style="left:0;width:1080px;top:500px;font-size:64px;line-height:1.3">역 하나가 10년이에요</div>
<div class="a board" id=board>
 <div class="a bt d" id=b1a style="top:34px;font-size:104px;line-height:1.3">지금 내 역은?</div>
 <div class="a bt" id=b1b style="top:170px;font-size:60px;line-height:1.4;color:#ffd9d2">번호를 댓글로 남겨 주세요</div>
 <div class="a bt d" id=b2a style="top:46px;font-size:76px;line-height:1.35;opacity:0">지금 역이 어디든<br>다음 길은 내가 정해요</div>
 <div class="a bt d" id=b3a style="top:46px;font-size:80px;line-height:1.35;opacity:0">떠오르는 사람에게<br>보내 보세요</div>
</div>
<script>
const BEAT=@@BEAT@@, B=ms=>ms/1000/BEAT, cl=(x,a=0,b=1)=>Math.min(b,Math.max(a,x));
function bez(x1,y1,x2,y2){return t=>{if(t<=0)return 0;if(t>=1)return 1;let a=0,b=1,u=t;for(let i=0;i<24;i++){const x=3*(1-u)*(1-u)*u*x1+3*(1-u)*u*u*x2+u*u*u;if(x<t)a=u;else b=u;u=(a+b)/2}return 3*(1-u)*(1-u)*u*y1+3*(1-u)*u*u*y2+u*u*u}}
const out=bez(.23,1,.32,1), inout=bez(.77,0,.175,1), g=id=>document.getElementById(id), NS='http://www.w3.org/2000/svg';
const PTS=[[-60,800],[250,800],[410,960],[700,960],[860,800],[1140,800]]; const SEG=[],CUM=[0]; let L=0;
for(let i=0;i<5;i++){const dx=PTS[i+1][0]-PTS[i][0],dy=PTS[i+1][1]-PTS[i][1],l=Math.hypot(dx,dy);SEG.push({l,dx,dy});L+=l;CUM.push(L)}
function pos(s){s=cl(s,0,L);let i=0;while(i<4&&s>CUM[i+1])i++;const t=(s-CUM[i])/SEG[i].l;return {x:PTS[i][0]+SEG[i].dx*t,y:PTS[i][1]+SEG[i].dy*t,a:Math.atan2(SEG[i].dy,SEG[i].dx)*180/Math.PI}}
const route=g('route'); route.setAttribute('stroke-dasharray',L+' '+L);
const ST=[]; const SA=[170,360,550,740,930,1120]; const POPB=[0,0,2.5,4.5,6.5,8.5];
SA.forEach((s,i)=>{const p=pos(s);const gr=document.createElementNS(NS,'g');gr.setAttribute('transform',`translate(${p.x} ${p.y})`);
 const c=document.createElementNS(NS,'circle');c.setAttribute('r',58);c.setAttribute('fill','#fff');c.setAttribute('stroke','@@INK@@');c.setAttribute('stroke-width',14);
 const tx=document.createElementNS(NS,'text');tx.setAttribute('text-anchor','middle');tx.setAttribute('y',22);tx.setAttribute('font-size',64);tx.setAttribute('fill','@@INK@@');tx.textContent=String(i+1);
 gr.appendChild(c);gr.appendChild(tx);g('stations').appendChild(gr);ST.push({gr,c,tx,p})});
// 보조 노선의 작은 정거장 점
[[100,660],[300,660],[560,720],[800,720],[1000,720],[200,1110],[420,1110],[620,1010],[860,1010],[1040,1010],[120,170],[380,170],[700,230],[960,230],[160,290],[860,230],[160,1590],[320,1590],[600,1650],[900,1650],[300,1740],[520,1740],[800,1670],[1000,1670],[140,1860],[420,1860],[700,1860],[980,1860]].forEach(q=>{const c=document.createElementNS(NS,'circle');c.setAttribute('cx',q[0]);c.setAttribute('cy',q[1]);c.setAttribute('r',17);c.setAttribute('fill','#fff');c.setAttribute('stroke','@@INK@@');c.setAttribute('stroke-width',6);c.setAttribute('opacity',.45);g('ticks').appendChild(c)});
// 열차
const tr=g('train'); const body=document.createElementNS(NS,'rect');body.setAttribute('x',-110);body.setAttribute('y',-48);body.setAttribute('width',220);body.setAttribute('height',96);body.setAttribute('rx',32);body.setAttribute('fill','@@INK@@');tr.appendChild(body);
[-76,-30,16].forEach(x=>{const w=document.createElementNS(NS,'rect');w.setAttribute('x',x);w.setAttribute('y',-26);w.setAttribute('width',40);w.setAttribute('height',36);w.setAttribute('rx',10);w.setAttribute('fill','#ffe4dd');tr.appendChild(w)});
let b=0;
function seek(ms){b=B(ms);
 const ph=b-Math.floor(b), pulse=0.03*Math.exp(-ph*5);
 // 노선: 처음부터 절반쯤 그려져 있고(첫 프레임 완성) 박 9까지 끝까지
 const pr=0.36+0.64*out(cl(b/9)); route.setAttribute('stroke-dashoffset',0); route.setAttribute('stroke-dasharray',(L*pr)+' '+(L+200));
 // 역: 박마다 하나씩 도착, 도착한 뒤에도 박자에 맞춰 살짝 뜀
 ST.forEach((o,i)=>{const t0=POPB[i]; const q=out(cl((b-t0)/.45)); let sc=b<t0?0:(i<2?1:q*(1+.22*(1-q))); let hot=false;
   if(b>=16&&b<22){const k=Math.floor(b-16); if(k===i){hot=true; sc*=1+0.22*Math.exp(-(b-16-k)*4)}}
   sc*=1+(b>t0?pulse*.5:0); o.gr.setAttribute('transform',`translate(${o.p.x} ${o.p.y}) scale(${Math.max(sc,.001)})`);
   o.c.setAttribute('fill',hot?'@@CORAL@@':'#fff'); o.tx.setAttribute('fill',hot?'#fff':'@@INK@@')});
 // 열차: 박 10~22에 왼쪽에서 들어와 5번 역을 지나감
 const tp=cl((b-10)/12); const tv=b>10&&b<23; if(tv){const p=pos(-140+(SA[4]+140)*inout(tp)); tr.setAttribute('transform',`translate(${p.x} ${p.y})`); tr.style.opacity=1-cl((b-21)/.6)} else tr.style.opacity=0;
 // 제목은 박마다 아주 살짝 뜀
 g('title').style.transform=`scale(${1+pulse*.6})`;
 // 안내판 글자: 박 0~24 / 24~28 / 28~32
 const sw=(id,a,c)=>{g(id).style.opacity=cl((b-a)/.4)*(1-cl((b-c)/.4))};
 g('b1a').style.opacity=1-cl((b-24)/.4); g('b1b').style.opacity=1-cl((b-24)/.4);
 sw('b2a',24.2,28); g('b3a').style.opacity=cl((b-28.2)/.4);
 g('board').style.transform=`scale(${1+pulse*.35})`;
 // 보조 노선이 천천히 흐름(움직이는 정지)
 g('decor').style.transform=`translateX(${Math.sin(b*.35)*10}px)`;
}
seek(0);
</script>"""
    for k, v in {"@@FONTS@@": K.css("gm"), "@@PAPER@@": PAPER, "@@INK@@": INK, "@@CORAL@@": CORAL, "@@MINT@@": MINT, "@@BLUE@@": BLUE, "@@BEAT@@": repr(beat)}.items(): h = h.replace(k, v)
    return h
if __name__ == "__main__":
    mi = MP.choose("love", "subway-life"); beat = 60.0 / mi["bpm"]; nb = 32; total = nb * beat
    hp = "/tmp/subway.html"; open(hp, "w", encoding="utf-8").write(html(beat))
    out = os.path.join(HERE, "..", "2026-motion", "subway_life.mp4"); secs = HM.render_html(hp, out, total)
    MP.mux(out, [10 * beat, 6 * beat, 8 * beat, 4 * beat, 4 * beat], mi, 99)
    print("음악:", mi["style"], mi["bpm"], mi["key"], "| 박자", round(beat, 3), "초 | 길이", round(secs, 1), "초")
