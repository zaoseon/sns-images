"""지하철 노선도 모션그래픽 v2 '내 10년은 어느 역?'(10/5 대표 지적: 역마다 운명학적 의미가 있어야 한다, 릴스 공식·내용이 안 끌린다).
역 5개 = 대운(10년 운)에 들어오는 기운 5가지(십성 묶음): 비겁(나)·식상(표현)·재성(돈)·관성(일)·인성(공부).
※ 역 순서는 사람마다 다르다(영상에도 밝힘). 풀이는 단정하지 않고 '요즘 내 중심은?' 질문으로 끝낸다.
사용: python3 pipeline/motion_subway.py -> 2026-motion/subway_life.mp4"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import music_plan as MP, html_motion as HM, fonts_kit as K
CORAL = "#ff6b57"; MINT = "#2bc5a0"; BLUE = "#4a7bff"; INK = "#17102b"; PAPER = "#fbf8f1"
ST = [("비겁", "나", "나를 세우는 10년"), ("식상", "표현", "재능을 꺼내는 10년"), ("재성", "돈", "성과를 만드는 10년"), ("관성", "일", "책임을 지는 10년"), ("인성", "공부", "배우고 쉬는 10년")]
def html(beat):
    plates = "".join(f'<div class="a plate" id=pl{i}><div class="d" style="font-size:54px;line-height:1.2">{n}</div><div style="font-size:46px;line-height:1.3">{m}</div></div>' for i, (n, m, _) in enumerate(ST))
    boards = "".join(f'<div class="a bt" id=bk{i} style="opacity:0"><div class="d" style="font-size:80px;line-height:1.25">{n}역 · {m}</div><div style="font-size:56px;line-height:1.4;color:#ffd9d2">{t}</div></div>' for i, (n, m, t) in enumerate(ST))
    h = """<!doctype html><meta charset=utf-8><style>@@FONTS@@
html,body{margin:0;width:1080px;height:1920px;overflow:hidden;background:@@PAPER@@;font-family:'JW-B',sans-serif;font-weight:800;color:@@INK@@;word-break:keep-all}
.a{position:absolute}.d{font-family:'JW-D',sans-serif;font-weight:900}.t{text-align:center;white-space:nowrap}
.grid{left:0;top:0;width:1080px;height:1920px;background-image:linear-gradient(#e9e2d2 2px,transparent 2px),linear-gradient(90deg,#e9e2d2 2px,transparent 2px);background-size:90px 90px;opacity:.7}
.board{left:60px;top:1190px;width:960px;height:270px;background:@@INK@@;border-radius:44px;color:#fff;overflow:hidden}
.bt{left:0;top:30px;width:960px;text-align:center;white-space:nowrap}
.plate{top:985px;width:180px;height:150px;margin-left:-90px;background:#fff;border:6px solid @@INK@@;border-radius:30px;text-align:center;box-sizing:border-box;padding-top:8px;opacity:0}
svg text{font-family:'JW-D',sans-serif;font-weight:900}
</style><body>
<div class="a grid"></div>
<svg class="a" id=decor width=1080 height=1920 viewBox="0 0 1080 1920" style="left:0;top:0">
 <path d="M-60 170 L520 170 L580 230 L1140 230" stroke="@@CORAL@@" stroke-width="20" fill="none" opacity=".28" stroke-linejoin="round"/>
 <path d="M-60 290 L240 290 L300 230 L1140 230" stroke="@@MINT@@" stroke-width="20" fill="none" opacity=".3" stroke-linejoin="round"/>
 <path d="M-60 1590 L380 1590 L440 1650 L1140 1650" stroke="@@BLUE@@" stroke-width="22" fill="none" opacity=".32" stroke-linejoin="round"/>
 <path d="M-60 1740 L620 1740 L690 1670 L1140 1670" stroke="@@CORAL@@" stroke-width="22" fill="none" opacity=".3" stroke-linejoin="round"/>
 <path d="M-60 1860 L1140 1860" stroke="@@MINT@@" stroke-width="22" fill="none" opacity=".35"/>
 <g id=ticks></g>
 <path id=route d="M-60 800 L300 800 L360 860 L1140 860" stroke="@@CORAL@@" stroke-width="52" fill="none" stroke-linejoin="round"/>
 <g id=train></g>
 <g id=stations></g>
</svg>
<div class="a d t" id=title style="left:0;width:1080px;top:340px;font-size:104px;line-height:1.2">내 10년은 어느 역?</div>
<div class="a t" id=sub style="left:0;width:1080px;top:490px;font-size:60px;line-height:1.3">대운은 10년마다 갈아타는 역이에요</div>
<div class="a t" id=sub2 style="left:0;width:1080px;top:572px;font-size:50px;line-height:1.3;color:#6b6277">역 순서는 사람마다 달라요</div>
@@PLATES@@
<div class="a board" id=board>@@BOARDS@@
 <div class="a bt d" id=bq style="top:40px;font-size:82px;line-height:1.3;opacity:0">요즘 내 중심은<br>어느 역일까?</div>
 
 <div class="a bt d" id=bi style="top:40px;font-size:80px;line-height:1.3">대운에 들어오는<br>기운 5가지</div>
 <div class="a bt d" id=bc style="top:40px;font-size:80px;line-height:1.3;opacity:0">떠오르는 사람에게<br>보내 보세요</div>
</div>
<script>
const BEAT=@@BEAT@@, B=ms=>ms/1000/BEAT, cl=(x,a=0,b=1)=>Math.min(b,Math.max(a,x));
function bez(x1,y1,x2,y2){return t=>{if(t<=0)return 0;if(t>=1)return 1;let a=0,b=1,u=t;for(let i=0;i<24;i++){const x=3*(1-u)*(1-u)*u*x1+3*(1-u)*u*u*x2+u*u*u;if(x<t)a=u;else b=u;u=(a+b)/2}return 3*(1-u)*(1-u)*u*y1+3*(1-u)*u*u*y2+u*u*u}}
const out=bez(.23,1,.32,1), inout=bez(.77,0,.175,1), g=id=>document.getElementById(id), NS='http://www.w3.org/2000/svg';
const PTS=[[-60,800],[300,800],[360,860],[1140,860]]; const SEG=[],CUM=[0]; let L=0;
for(let i=0;i<3;i++){const dx=PTS[i+1][0]-PTS[i][0],dy=PTS[i+1][1]-PTS[i][1],l=Math.hypot(dx,dy);SEG.push({l,dx,dy});L+=l;CUM.push(L)}
function pos(s){let i=0;while(i<2&&s>CUM[i+1])i++;const t=(s-CUM[i])/SEG[i].l;return {x:PTS[i][0]+SEG[i].dx*t,y:PTS[i][1]+SEG[i].dy*t}}
const route=g('route'); const ST=[]; const SA=[210,405,600,795,990]; const POPB=[0,0,1.5,3,4.5]; const LET=['비','식','재','관','인'];
SA.forEach((s,i)=>{const p=pos(s);const gr=document.createElementNS(NS,'g');
 const c=document.createElementNS(NS,'circle');c.setAttribute('r',60);c.setAttribute('fill','#fff');c.setAttribute('stroke','@@INK@@');c.setAttribute('stroke-width',14);
 const tx=document.createElementNS(NS,'text');tx.setAttribute('text-anchor','middle');tx.setAttribute('y',20);tx.setAttribute('font-size',58);tx.setAttribute('fill','@@INK@@');tx.textContent=LET[i];
 gr.appendChild(c);gr.appendChild(tx);g('stations').appendChild(gr);ST.push({gr,c,tx,p});const pl=g('pl'+i);pl.style.left=p.x+'px'});
[[100,170],[380,170],[700,230],[960,230],[160,290],[860,230],[160,1590],[320,1590],[600,1650],[900,1650],[300,1740],[520,1740],[800,1670],[1000,1670],[140,1860],[420,1860],[700,1860],[980,1860]].forEach(q=>{const c=document.createElementNS(NS,'circle');c.setAttribute('cx',q[0]);c.setAttribute('cy',q[1]);c.setAttribute('r',17);c.setAttribute('fill','#fff');c.setAttribute('stroke','@@INK@@');c.setAttribute('stroke-width',6);c.setAttribute('opacity',.45);g('ticks').appendChild(c)});
const tr=g('train'); const body=document.createElementNS(NS,'rect');body.setAttribute('x',-84);body.setAttribute('y',-40);body.setAttribute('width',168);body.setAttribute('height',80);body.setAttribute('rx',28);body.setAttribute('fill','@@INK@@');tr.appendChild(body);
[-58,-22,14].forEach(x=>{const w=document.createElementNS(NS,'rect');w.setAttribute('x',x);w.setAttribute('y',-22);w.setAttribute('width',32);w.setAttribute('height',30);w.setAttribute('rx',8);w.setAttribute('fill','#ffe4dd');tr.appendChild(w)});
const T0=6, DW=3;   // 열차는 박 6에 출발해 역마다 3박씩 선다
function trainS(b){ // 열차 위치(경로 거리)
 if(b<T0) return -160; let k=Math.floor((b-T0)/DW); if(k>4){const q=cl((b-(T0+5*DW))/1.0); return SA[4]+(1300-SA[4])*inout(q)}
 const t=(b-T0)-k*DW; const prev=k===0?-160:SA[k-1]; return prev+(SA[k]-prev)*inout(cl(t/.9))}
let b=0;
function seek(ms){b=B(ms);
 const ph=b-Math.floor(b), pulse=0.03*Math.exp(-ph*5);
 const pr=0.4+0.6*out(cl(b/5)); route.setAttribute('stroke-dasharray',(L*pr)+' '+(L+200));
 let cur=-1; if(b>=T0&&b<T0+5*DW) cur=Math.floor((b-T0)/DW); const atSt=cur>=0&&((b-T0)-cur*DW)>.9;
 ST.forEach((o,i)=>{const t0=POPB[i]; const q=out(cl((b-t0)/.45)); let sc=b<t0?0:(i<2?1:q*(1+.22*(1-q)));
   const hot=atSt&&cur===i; if(hot) sc*=1+0.1*Math.exp(-((b-T0)-i*DW-.9)*4); sc*=1+(b>t0?pulse*.5:0);
   o.gr.setAttribute('transform',`translate(${o.p.x} ${o.p.y}) scale(${Math.max(sc,.001)})`);
   o.c.setAttribute('fill',hot?'@@CORAL@@':'#fff'); o.tx.setAttribute('fill',hot?'#fff':'@@INK@@');
   const pl=g('pl'+i); pl.style.opacity=cl((b-t0-.3)/.4); pl.style.transform=`scale(${1+(hot?0.06:0)})`; pl.style.borderColor=hot?'@@CORAL@@':'@@INK@@'; pl.style.top=(985+(hot?-8:0))+'px'});
 const ts=trainS(b); if(b>=T0-.5&&ts<1250){const p=pos(Math.max(ts,-60)); tr.setAttribute('transform',`translate(${ts<-60?-300:p.x} ${ts<-60?p.y:p.y})`); tr.style.opacity=1} else tr.style.opacity=0;
 g('title').style.transform=`scale(${1+pulse*.6})`;
 // 안내판: 역마다 뜻 → 질문 → 보내기
 for(let i=0;i<5;i++){const a=T0+i*DW+.5, c=T0+(i+1)*DW+.2; g('bk'+i).style.opacity=cl((b-a)/.3)*(1-cl((b-c)/.3))}
 const qa=T0+5*DW+.4, qc=qa+5; g('bq').style.opacity=cl((b-qa)/.4)*(1-cl((b-qc)/.4)); g('bc').style.opacity=cl((b-qc-.2)/.4);
 // 시작 장면: 안내판에 질문을 보여 둔다(첫 프레임 완성)
 g('bi').style.opacity=1-cl((b-(T0+.3))/.3);
 g('board').style.transform=`scale(${1+pulse*.35})`; g('decor').style.transform=`translateX(${Math.sin(b*.35)*10}px)`;
}
seek(0);
</script>"""
    for k, v in {"@@FONTS@@": K.css("gm"), "@@PAPER@@": PAPER, "@@INK@@": INK, "@@CORAL@@": CORAL, "@@MINT@@": MINT, "@@BLUE@@": BLUE, "@@BEAT@@": repr(beat), "@@PLATES@@": plates, "@@BOARDS@@": boards}.items(): h = h.replace(k, v)
    return h
if __name__ == "__main__":
    mi = MP.choose("love", "subway-life"); beat = 60.0 / mi["bpm"]; nb = 31; total = nb * beat
    hp = "/tmp/subway.html"; open(hp, "w", encoding="utf-8").write(html(beat))
    out = os.path.join(HERE, "..", "2026-motion", "subway_life.mp4"); secs = HM.render_html(hp, out, total)
    MP.mux(out, [6 * beat, 15 * beat, 5 * beat, 5 * beat], mi, 99)
    print("음악:", mi["style"], mi["bpm"], mi["key"], "| 박자", round(beat, 3), "초 | 길이", round(secs, 1), "초")
