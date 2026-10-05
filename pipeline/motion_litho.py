"""리소그래프 모션그래픽 '사주와 별자리, 같은 말을 할까요?'(10/5, 스타일 30 가이드 프롬프트를 자오선 내용으로 바꿈).
핑크 잉크=사주, 블루 잉크=별자리, 겹친 곳(곱하기 섞임)=보라=같은 말. 숫자는 cross_data(사주-점성술 같은 축 13.5% → 100명 중 14명).
규칙: 첫 프레임 완성, 글자 굵게·크게, 문장은 2초 이상, 정지 구간엔 천천히 움직임(움직이는 정지), 장면마다 새 종이가 넘어감.
사용: python3 pipeline/motion_litho.py -> 2026-motion/litho_cross.mp4"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import music_plan as MP, html_motion as HM, fonts_kit as K
PINK = "#ff6fa8"; BLUE = "#5b7bff"; INK = "#17102b"; PAPER = "#f4ead7"
GRAIN = "data:image/svg+xml;utf8," + "%3Csvg xmlns='http://www.w3.org/2000/svg' width='300' height='300'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/%3E%3CfeColorMatrix values='0 0 0 0 .35  0 0 0 0 .28  0 0 0 0 .2  0 0 0 .55 0'/%3E%3C/filter%3E%3Crect width='300' height='300' filter='url(%23n)'/%3E%3C/svg%3E"
def html(beat):
    h = """<!doctype html><meta charset=utf-8><style>@@FONTS@@
html,body{margin:0;width:1080px;height:1920px;overflow:hidden;background:@@PAPER@@;font-family:'JW-B',sans-serif;font-weight:800;color:@@INK@@;word-break:keep-all}
.a{position:absolute}.d{font-family:'JW-D',sans-serif;font-weight:900}
.c{border-radius:50%;mix-blend-mode:multiply;will-change:transform,opacity}
.t{text-align:center;white-space:nowrap}
.paper{left:0;top:0;width:1080px;height:1920px;background:@@PAPER@@}
.grain{left:0;top:0;width:1080px;height:1920px;background:url("@@GRAIN@@");mix-blend-mode:multiply;opacity:.26;pointer-events:none;z-index:50}
.dot{width:52px;height:52px;border-radius:50%;background:#d8ccb8;box-shadow:inset 0 0 0 4px #c7baa3}
</style><body>
<div class="a paper" id=p0>
 <div class="a d t" id=hl style="left:0;width:1080px;top:350px;font-size:84px;line-height:1.35">사주와 별자리,<br>같은 말을 할까요?</div>
 <div class="a c" id=pinkC style="left:100px;top:600px;width:600px;height:600px;background:@@PINK@@"></div>
 <div class="a c" id=blueC style="left:380px;top:600px;width:600px;height:600px;background:@@BLUE@@"></div>
 <div class="a c" id=blueD style="left:380px;top:600px;width:592px;height:592px;border:8px dashed @@BLUE@@;background:transparent;opacity:.55"></div>
 <div class="a d t" id=wSaju style="left:130px;width:360px;top:850px;font-size:120px">사주</div>
 <div class="a d t" id=wStar style="left:610px;width:360px;top:860px;font-size:92px">별자리</div>
 <div class="a d t" id=wSame style="left:390px;width:300px;top:1100px;font-size:64px;color:#fff">같은 말</div>
 <div id=dots></div>
 <div class="a t d" id=cnLb style="left:0;width:1080px;top:350px;font-size:104px;line-height:1.3">100명 중 <span id=cnNum style="color:#7a4fd0;font-size:150px">0</span>명이</div>
 <div class="a t d" id=cnTx style="left:0;width:1080px;top:520px;font-size:76px;line-height:1.4">같은 말을 했어요</div>
</div>
<div class="a paper" id=p4 style="box-shadow:-30px 0 40px rgba(60,40,20,.25)">
 <div class="a d t" id=t4a style="left:0;width:1080px;top:640px;font-size:132px;line-height:1.3;color:@@INK@@;text-shadow:7px 5px 0 @@PINK@@">다른 말은</div>
 <div class="a d t" id=t4b style="left:0;width:1080px;top:860px;font-size:132px;line-height:1.3;color:@@INK@@;text-shadow:-7px 5px 0 @@BLUE@@">내가 고를 곳</div>
 <div class="a t" id=t4c style="left:0;width:1080px;top:1180px;font-size:56px;line-height:1.5">같은 말은 타고난 결이에요</div>
</div>
<div class="a paper" id=p5 style="box-shadow:-30px 0 40px rgba(60,40,20,.25)">
 <div class="a d t" id=t5a style="left:0;width:1080px;top:620px;font-size:116px;line-height:1.35;text-shadow:6px 4px 0 @@PINK@@">떠오르는 사람에게</div>
 <div class="a d t" id=t5b style="left:0;width:1080px;top:820px;font-size:116px;line-height:1.35;text-shadow:-6px 4px 0 @@BLUE@@">보내 보세요</div>
 <svg class="a" id=plane viewBox="0 0 100 100" style="left:410px;top:1060px;width:260px;height:260px"><path d="M8 52 L92 10 L66 90 L50 60 Z" fill="@@PINK@@" style="mix-blend-mode:multiply"/><path d="M30 46 L92 10 L50 60 Z" fill="@@BLUE@@" style="mix-blend-mode:multiply"/></svg>
 <div class="a t" id=zs style="left:0;width:1080px;top:1380px;font-size:46px">zaoseon.com</div>
</div>
<div class="a grain"></div>
<script>
const BEAT=@@BEAT@@, B=ms=>ms/1000/BEAT, cl=(x,a=0,b=1)=>Math.min(b,Math.max(a,x));
function bez(x1,y1,x2,y2){return t=>{if(t<=0)return 0;if(t>=1)return 1;let a=0,b=1,u=t;for(let i=0;i<24;i++){const x=3*(1-u)*(1-u)*u*x1+3*(1-u)*u*u*x2+u*u*u;if(x<t)a=u;else b=u;u=(a+b)/2}return 3*(1-u)*(1-u)*u*y1+3*(1-u)*u*u*y2+u*u*u}}
const out=bez(.23,1,.32,1), g=id=>document.getElementById(id);
// 점 100개(10x10) — 겹침 14개는 고정 위치
const dots=g('dots'); const PUR=[7,13,22,28,35,41,47,53,58,66,72,79,85,93]; const D=[];
for(let i=0;i<100;i++){const e=document.createElement('div');e.className='a dot';const r=Math.floor(i/10),c=i%10;e.style.left=(189+c*72)+'px';e.style.top=(720+r*72)+'px';e.style.opacity=0;dots.appendChild(e);D.push(e)}
const stamp=(el,b0,dur=.5,from=1.12)=>{const p=out(cl((b-b0)/dur));return {o:Math.min(1,p*6),s:from+(1-from)*p}};
let b=0;
function seek(ms){b=B(ms);
 const drift=1+0.025*cl(b/12);               // 움직이는 정지: 장면 1·2 동안 천천히 커짐
 // 헤드라인
 const hl=g('hl'); hl.style.opacity=1-cl((b-12)/.8); hl.style.transform=`scale(${drift})`;
 // 핑크 원(첫 프레임부터 보임, 도장 찍히듯 살짝 줄어듦)
 let s=stamp(null,0,.45,1.1); g('pinkC').style.opacity=1-cl((b-12)/.8); g('pinkC').style.transform=`scale(${s.s*drift})`;
 g('wSaju').style.opacity=1-cl((b-12)/.8); g('wSaju').style.transform=`scale(${s.s*drift})`;
 // 블루 원(박 6에 도장)
 const bs=stamp(null,6,.45,1.18); const bo=b<6?0:Math.min(1,bs.o);
 g('blueC').style.opacity=bo*(1-cl((b-12)/.6)); g('blueC').style.transform=`scale(${bo?bs.s*drift:1})`;
 g('blueD').style.opacity=(b<6?.55:0)*(1-cl((b-12)/.6)); g('blueD').style.transform=`scale(${drift})`;
 g('wStar').style.opacity=(b<6?0.0:bo)*(1-cl((b-12)/.6)); g('wStar').style.transform=`scale(${bo?bs.s*drift:1})`;
 const ss=stamp(null,7,.4,1.3); g('wSame').style.opacity=(b<7?0:ss.o)*(1-cl((b-12)/.6)); g('wSame').style.transform=`scale(${b<7?1:ss.s})`;
 // 점 격자(박 12~20)
 let purOn=0;
 for(let i=0;i<100;i++){const t0=12.9+i/100*2.8; const p=out(cl((b-t0)/.5)); const isP=PUR.indexOf(i)>=0; let col='#d8ccb8', sc=p, ring='#c7baa3';
   if(isP){const k=PUR.indexOf(i), tp=15.4+k*.18; const q=out(cl((b-tp)/.35)); if(q>0){col='#7a4fd0';ring='#5b2fb0';sc=p*(1+0.28*q);} if(b>=tp+.1)purOn=Math.max(purOn,k+1)}
   D[i].style.opacity=p*(1-cl((b-20)/.6)); D[i].style.background=col; D[i].style.boxShadow=`inset 0 0 0 4px ${ring}`; D[i].style.transform=`scale(${Math.max(sc,0.001)})`}
 const cnOn=cl((b-12.9)/.5); const fade=1-cl((b-20)/.6);
 g('cnLb').style.opacity=cnOn*fade; g('cnTx').style.opacity=cl((b-16.2)/.5)*fade;
 g('cnNum').textContent=purOn; 
 // 종이 넘기기: 박 20(문장 2), 박 26(보내기)
 const x4=(1-out(cl((b-20)/.7)))*1180; g('p4').style.transform=`translateX(${x4}px)`; g('p4').style.display=b<19.9?'none':'block';
 const d4=1+0.02*cl((b-20.7)/5); const f4=b<20.4?0:1;
 g('t4a').style.opacity=cl((b-20.6)/.4); g('t4a').style.transform=`scale(${d4})`;
 g('t4b').style.opacity=cl((b-22)/.4); g('t4b').style.transform=`scale(${d4})`;
 g('t4c').style.opacity=cl((b-22.6)/.5);
 const x5=(1-out(cl((b-26)/.7)))*1180; g('p5').style.transform=`translateX(${x5}px)`; g('p5').style.display=b<25.9?'none':'block';
 const d5=1+0.025*cl((b-26.7)/5.3);
 g('t5a').style.opacity=cl((b-26.6)/.4); g('t5a').style.transform=`scale(${d5})`;
 g('t5b').style.opacity=cl((b-27.8)/.4); g('t5b').style.transform=`scale(${d5})`;
 const pf=out(cl((b-29)/.8)); g('plane').style.opacity=cl((b-29)/.3); g('plane').style.transform=`translate(${(1-pf)*-160}px,${(1-pf)*120}px) rotate(${-8+8*pf}deg)`;
 g('zs').style.opacity=cl((b-29.6)/.5);
}
seek(0);
</script>"""
    for k, v in {"@@FONTS@@": K.css("gm"), "@@PAPER@@": PAPER, "@@INK@@": INK, "@@PINK@@": PINK, "@@BLUE@@": BLUE, "@@GRAIN@@": GRAIN, "@@BEAT@@": repr(beat)}.items(): h = h.replace(k, v)
    return h
if __name__ == "__main__":
    mi = MP.choose("data", "litho-cross"); beat = 60.0 / mi["bpm"]; nb = 32; total = nb * beat
    hp = "/tmp/litho.html"; open(hp, "w", encoding="utf-8").write(html(beat))
    out = os.path.join(HERE, "..", "2026-motion", "litho_cross.mp4"); secs = HM.render_html(hp, out, total)
    MP.mux(out, [6 * beat, 6 * beat, 8 * beat, 6 * beat, 6 * beat], mi, 97)
    print("음악:", mi["style"], mi["bpm"], mi["key"], "| 박자", round(beat, 3), "초 | 길이", round(secs, 1), "초")
