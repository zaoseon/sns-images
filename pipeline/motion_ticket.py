"""탑승권 모션그래픽 '2027 정미년행 탑승권'(10/5, 스타일 30 가이드의 탑승권 프롬프트를 자오선 내용으로 바꿈).
출발 2026 병오 → 도착 2027 정미, 좌석 12칸 = 12개월. 판매 정보(가격·기한)는 넣지 않는다(광고 느낌 지적).
규칙: 첫 프레임 완성, 글자 단색·굵게·크게, 글자는 도형 경계에 걸치지 않음, 화면을 채움, 박자에 맞춰 움직임, 문장 2초 이상.
사용: python3 pipeline/motion_ticket.py -> 2026-motion/ticket_2027.mp4"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import music_plan as MP, html_motion as HM, fonts_kit as K
NAVY = "#0f1a3d"; CREAM = "#f6efdd"; RED = "#d83a30"; GOLD = "#e7c88d"
def html(beat):
    seats = "".join(f'<div class="a seat" id=s{i} style="left:{(i%4)*224}px;top:{(i//4)*98}px"><span class=d>{i+1}월</span></div>' for i in range(12))
    h = """<!doctype html><meta charset=utf-8><style>@@FONTS@@
html,body{margin:0;width:1080px;height:1920px;overflow:hidden;background:@@NAVY@@;font-family:'JW-B',sans-serif;font-weight:800;color:@@NAVY@@;word-break:keep-all}
.a{position:absolute}.d{font-family:'JW-D',sans-serif;font-weight:900}.t{text-align:center;white-space:nowrap}
.ticket{left:60px;top:330px;width:960px;height:1140px;background:@@CREAM@@;border-radius:36px;overflow:hidden}
.seat{width:208px;height:84px;border:6px solid @@NAVY@@;border-radius:22px;box-sizing:border-box;display:flex;align-items:center;justify-content:center;font-size:48px;background:transparent}
.seat span{font-size:48px}
.lb{font-size:44px;color:#5b5f78}
</style><body>
<svg class="a" width=1080 height=1920 viewBox="0 0 1080 1920" style="left:0;top:0" id=bg>
 <path d="M-40 250 Q300 40 620 170 T1120 90" stroke="@@GOLD@@" stroke-width="6" stroke-dasharray="4 20" fill="none" opacity=".6" stroke-linecap="round"/>
 <path d="M-40 330 Q360 200 700 280 T1120 250" stroke="@@GOLD@@" stroke-width="6" stroke-dasharray="4 20" fill="none" opacity=".35" stroke-linecap="round"/>
 <path d="M-40 1650 Q320 1500 640 1620 T1120 1560" stroke="@@GOLD@@" stroke-width="6" stroke-dasharray="4 20" fill="none" opacity=".6" stroke-linecap="round"/>
 <path d="M-40 1790 Q380 1650 700 1760 T1120 1700" stroke="@@GOLD@@" stroke-width="6" stroke-dasharray="4 20" fill="none" opacity=".35" stroke-linecap="round"/>
 <g id=stars></g><g id=plane1><path d="M-26 6 L30 -12 L18 22 L6 8 Z" fill="@@GOLD@@"/></g><g id=plane2><path d="M-26 6 L30 -12 L18 22 L6 8 Z" fill="@@CREAM@@" opacity=".8"/></g>
</svg>
<div class="a ticket" id=ticket>
 <div class="a" style="left:0;top:0;width:960px;height:120px;background:@@NAVY@@"></div>
 <div class="a d" style="left:44px;top:30px;font-size:56px;color:@@CREAM@@;line-height:1.3">BOARDING PASS</div>
 <div class="a" style="right:44px;top:34px;font-size:50px;color:@@GOLD@@;line-height:1.3">정월 항공</div>
 <div class="a d t" id=tt1 style="left:0;width:960px;top:118px;font-size:150px;line-height:1.1">2027</div>
 <div class="a d t" id=tt2 style="left:0;width:960px;top:266px;font-size:120px;line-height:1.2">정미년행</div>
 <div id=route>
  <div class="a lb" style="left:44px;top:430px">출발</div><div class="a d" style="left:44px;top:476px;font-size:62px">2026 병오</div>
  <div class="a lb" style="right:44px;top:430px;text-align:right">도착</div><div class="a d" style="right:44px;top:476px;font-size:62px;text-align:right">2027 정미</div>
  <div class="a" style="left:360px;top:512px;width:240px;height:0;border-top:6px dashed @@NAVY@@;opacity:.4"></div>
  <svg class="a" id=tplane viewBox="-40 -30 80 60" style="left:440px;top:482px;width:80px;height:60px;transform:scaleX(-1)"><path d="M-26 6 L30 -12 L18 22 L6 8 Z" fill="@@RED@@"/></svg>
 </div>
 <div class="a d t" id=six style="left:0;width:960px;top:452px;font-size:58px;line-height:1.35;opacity:0">여섯 운명학으로 읽는 12개월</div>
 <div class="a" id=seats style="left:44px;top:604px;width:880px;height:280">@@SEATS@@</div>
 <div class="a" style="left:0;top:912px;width:960px;height:0;border-top:5px dashed @@NAVY@@;opacity:.35"></div>
 <div class="a" style="left:-30px;top:882px;width:60px;height:60px;border-radius:50%;background:@@NAVY@@"></div><div class="a" style="right:-30px;top:882px;width:60px;height:60px;border-radius:50%;background:@@NAVY@@"></div>
 <div class="a" id=bar style="left:270px;top:970px;width:500px;height:72px"></div>
 <div class="a d t" id=cta style="left:250px;width:666px;top:950px;font-size:56px;line-height:1.4;opacity:0">떠오르는 사람에게<br>보내 보세요</div>
 <div class="a" id=ring style="left:44px;top:938px;width:176px;height:176px;border:6px dashed @@NAVY@@;border-radius:50%;box-sizing:border-box;opacity:.35"></div>
 <div class="a d t" id=stamp style="left:40px;top:934px;width:184px;height:184px;border:10px solid @@RED@@;border-radius:50%;box-sizing:border-box;color:@@RED@@;font-size:50px;line-height:1.1;display:flex;align-items:center;justify-content:center;opacity:0;background:rgba(246,239,221,.0)"><span>정월<br>확인</span></div>
</div>
<script>
const BEAT=@@BEAT@@, B=ms=>ms/1000/BEAT, cl=(x,a=0,b=1)=>Math.min(b,Math.max(a,x));
function bez(x1,y1,x2,y2){return t=>{if(t<=0)return 0;if(t>=1)return 1;let a=0,b=1,u=t;for(let i=0;i<24;i++){const x=3*(1-u)*(1-u)*u*x1+3*(1-u)*u*u*x2+u*u*u;if(x<t)a=u;else b=u;u=(a+b)/2}return 3*(1-u)*(1-u)*u*y1+3*(1-u)*u*u*y2+u*u*u}}
const out=bez(.23,1,.32,1), g=id=>document.getElementById(id), NS='http://www.w3.org/2000/svg';
// 바코드와 별
const bar=g('bar'); for(let i=0;i<26;i++){const e=document.createElement('div');e.className='a';e.style.left=(i*19+ (i%3))+'px';e.style.top='0px';e.style.width=((i%4)+1)*4+'px';e.style.height='72px';e.style.background='@@NAVY@@';bar.appendChild(e)}
const stars=g('stars'); let seed=11; const rnd=()=>{seed=(seed*16807)%2147483647;return seed/2147483647};
for(let i=0;i<46;i++){const c=document.createElementNS(NS,'circle');const y=rnd()<.5?rnd()*300:1500+rnd()*420;c.setAttribute('cx',rnd()*1080);c.setAttribute('cy',y);c.setAttribute('r',2+rnd()*3.5);c.setAttribute('fill','@@CREAM@@');c.setAttribute('opacity',.35+rnd()*.5);stars.appendChild(c)}
let b=0;
function seek(ms){b=B(ms);
 const ph=b-Math.floor(b), pulse=0.025*Math.exp(-ph*5);
 // 탑승권: 첫 프레임부터 보이고, 처음에 살짝 내려앉음. 이후 박자마다 아주 조금 뜀
 const drop=(1-out(cl(b/.7)))*-40; let shake=0; if(b>16&&b<17.2){shake=Math.sin((b-16)*60)*7*(1-(b-16)/1.2)}
 g('ticket').style.transform=`translate(${shake}px,${drop}px) scale(${1+pulse*.6})`;
 // 배경 비행기 두 대: 천천히 곡선을 따라
 const p1=(b/34), p2=((b+10)/34)%1; g('plane1').setAttribute('transform',`translate(${-60+p1*1200} ${230-Math.sin(p1*3.1)*90}) rotate(-8)`); g('plane2').setAttribute('transform',`translate(${1140-p2*1200} ${1700-Math.sin(p2*3.1)*80}) rotate(172)`);
 // 좌석 12칸: 박 6부터 0.8박 간격으로 펀칭
 for(let i=0;i<12;i++){const t0=6+i*.8; const q=out(cl((b-t0)/.4)); const e=g('s'+i); const on=b>=t0; e.style.background=on?'@@NAVY@@':'transparent'; e.querySelector('span').style.color=on?'@@CREAM@@':'@@NAVY@@'; e.style.transform=`scale(${on?1+0.14*(1-q):1})`}
 // 출발→도착 비행기: 박 6~16 사이 왼쪽에서 오른쪽으로
 const f=out(cl((b-6)/10)); g('tplane').style.left=(380+f*130-40)+'px';
 // 도장: 박 16에 쾅
 const st=cl((b-16)/.45), sq=out(st); g('stamp').style.opacity=b<16?0:Math.min(1,sq*4); g('stamp').style.transform=`rotate(-12deg) scale(${b<16?2:1+(1-sq)*1.0})`; g('ring').style.opacity=b<16?.35:0;
 // 경로 줄 → "여섯 운명학으로 읽는 12개월" (박 20)
 g('route').style.opacity=1-cl((b-20)/.4); g('six').style.opacity=cl((b-20.2)/.4);
 // 바코드 → 공유 문구 (박 26)
 g('bar').style.opacity=1-cl((b-26)/.4); g('cta').style.opacity=cl((b-26.2)/.4);
}
seek(0);
</script>"""
    for k, v in {"@@FONTS@@": K.css("gm"), "@@NAVY@@": NAVY, "@@CREAM@@": CREAM, "@@RED@@": RED, "@@GOLD@@": GOLD, "@@SEATS@@": seats, "@@BEAT@@": repr(beat)}.items(): h = h.replace(k, v)
    return h
if __name__ == "__main__":
    mi = MP.choose("fun", "ticket-2027"); beat = 60.0 / mi["bpm"]; nb = 32; total = nb * beat
    hp = "/tmp/ticket.html"; open(hp, "w", encoding="utf-8").write(html(beat))
    out = os.path.join(HERE, "..", "2026-motion", "ticket_2027.mp4"); secs = HM.render_html(hp, out, total)
    MP.mux(out, [6 * beat, 10 * beat, 4 * beat, 6 * beat, 6 * beat], mi, 101)
    print("음악:", mi["style"], mi["bpm"], mi["key"], "| 박자", round(beat, 3), "초 | 길이", round(secs, 1), "초")
