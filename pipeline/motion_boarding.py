"""탑승권 모션그래픽 '2027 정미년행 탑승권'(10/5, 스타일 30 가이드의 탑승권 프롬프트를 자오선 내용으로 바꿈).
출발 2026 병오 → 도착 2027 정미, 좌석 12칸 = 12개월. 판매 정보(가격·기한) 없음.
규칙: 첫 프레임 완성, 글자 단색·굵게·크게(색 그림자 없음), 글자는 도형 경계에 걸치지 않음(도장은 비워 둔 자리에), 화면을 채움.
사용: python3 pipeline/motion_boarding.py -> 2026-motion/boarding_2027.mp4"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import music_plan as MP, html_motion as HM, fonts_kit as K
NAVY = "#12183a"; CREAM = "#f7efdc"; RED = "#d6362f"; INK = "#12183a"
def html(beat):
    h = """<!doctype html><meta charset=utf-8><style>@@FONTS@@
html,body{margin:0;width:1080px;height:1920px;overflow:hidden;background:@@NAVY@@;font-family:'JW-B',sans-serif;font-weight:800;color:@@INK@@;word-break:keep-all}
.a{position:absolute}.d{font-family:'JW-D',sans-serif;font-weight:900}.t{text-align:center;white-space:nowrap}
.seat{width:190px;height:118px;border-radius:26px;border:6px solid @@INK@@;box-sizing:border-box;background:@@CREAM@@;display:flex;align-items:center;justify-content:center;font-family:'JW-D',sans-serif;font-weight:900;font-size:60px}
</style><body>
<svg class="a" id=bg width=1080 height=1920 viewBox="0 0 1080 1920" style="left:0;top:0">
 <path d="M-80 1820 C 260 1500, 520 1700, 700 1320 S 1000 500, 1180 120" stroke="@@CREAM@@" stroke-width="8" stroke-dasharray="26 22" fill="none" opacity=".22"/>
 <path d="M-80 1640 C 220 1380, 420 1560, 640 1180 S 940 380, 1180 -60" stroke="@@CREAM@@" stroke-width="8" stroke-dasharray="26 22" fill="none" opacity=".14"/>
 <circle cx="860" cy="170" r="118" fill="@@CREAM@@" opacity=".92"/>
 <circle cx="820" cy="140" r="26" fill="#e4d8bb" opacity=".8"/><circle cx="905" cy="215" r="18" fill="#e4d8bb" opacity=".8"/><circle cx="880" cy="110" r="12" fill="#e4d8bb" opacity=".8"/>
 <path d="M60 1860 C 200 1790, 300 1760, 360 1700" stroke="@@CREAM@@" stroke-width="10" stroke-dasharray="28 24" fill="none" opacity=".35"/>
 <g transform="translate(330 1500) scale(4.4) rotate(-14 50 50)"><path d="M6 54 L94 12 L68 92 L50 62 Z" fill="@@CREAM@@" opacity=".95"/><path d="M28 48 L94 12 L50 62 Z" fill="#c9bd9f" opacity=".8"/></g>
 <g id=stars></g>
</svg>
<div class="a" id=ticket style="left:60px;top:330px;width:960px;height:1130px">
 <div class="a" style="left:0;top:0;width:960px;height:900px;background:@@CREAM@@;border-radius:48px 48px 0 0"></div>
 <div class="a d t" style="left:0;top:0;width:960px;height:104px;background:@@INK@@;color:@@CREAM@@;font-size:52px;line-height:104px;border-radius:48px 48px 0 0">탑승권 · BOARDING PASS</div>
 <div class="a d t" id=title style="left:0;top:128px;width:960px;font-size:104px;line-height:1.3">2027 정미년행</div>
 <div class="a" style="left:40px;top:300px;width:380px"><div style="font-size:46px;color:@@RED@@;font-weight:900">출발</div><div class="d" style="font-size:60px;line-height:1.3">2026 병오</div></div>
 <div class="a" style="left:540px;top:300px;width:380px;text-align:right"><div style="font-size:46px;color:@@RED@@;font-weight:900">도착</div><div class="d" style="font-size:60px;line-height:1.3">2027 정미</div></div>
 <svg class="a" id=plane viewBox="0 0 100 100" style="left:430px;top:316px;width:100px;height:100px"><path d="M6 54 L94 12 L68 92 L50 62 Z" fill="@@INK@@"/></svg>
 <div id=seats></div>
 <div class="a" id=stamp style="left:290px;top:457px;width:380px;height:380px;opacity:0"><div class="a" style="left:0;top:0;width:380px;height:380px;border-radius:50%;border:14px solid @@RED@@;box-sizing:border-box"></div><div class="a" style="left:26px;top:26px;width:328px;height:328px;border-radius:50%;border:5px solid @@RED@@;box-sizing:border-box"></div>
  <div class="a d t" style="left:0;top:70px;width:380px;font-size:104px;line-height:1.2;color:@@RED@@">정월<br>확인</div></div>
 <div class="a" id=perf style="left:0;top:880px;width:960px;height:0;border-top:7px dashed @@INK@@;opacity:.55;z-index:4"></div>
 <div class="a" style="left:-38px;top:844px;width:76px;height:76px;border-radius:50%;background:@@NAVY@@;z-index:5"></div><div class="a" style="left:922px;top:844px;width:76px;height:76px;border-radius:50%;background:@@NAVY@@;z-index:5"></div>
 <div class="a" id=stub style="left:0;top:880px;width:960px;height:250px;background:@@CREAM@@;border-radius:0 0 48px 48px;z-index:3">
  <div class="a d t" id=m1 style="left:0;top:56px;width:960px;font-size:68px;line-height:1.4;opacity:0">여섯 운명학으로 읽는<br>12개월</div>
  <div class="a d t" id=m2 style="left:0;top:56px;width:960px;font-size:68px;line-height:1.4;opacity:0">당신의 한 해<br>12개월 풀이</div>
 </div>
</div>
<script>
const BEAT=@@BEAT@@, B=ms=>ms/1000/BEAT, cl=(x,a=0,b=1)=>Math.min(b,Math.max(a,x));
function bez(x1,y1,x2,y2){return t=>{if(t<=0)return 0;if(t>=1)return 1;let a=0,b=1,u=t;for(let i=0;i<24;i++){const x=3*(1-u)*(1-u)*u*x1+3*(1-u)*u*u*x2+u*u*u;if(x<t)a=u;else b=u;u=(a+b)/2}return 3*(1-u)*(1-u)*u*y1+3*(1-u)*u*u*y2+u*u*u}}
const out=bez(.23,1,.32,1), g=id=>document.getElementById(id), NS='http://www.w3.org/2000/svg';
// 좌석 12칸(4x3)
const SE=[]; for(let i=0;i<12;i++){const e=document.createElement('div');e.className='a seat';e.textContent=(i+1)+'월';e.style.left=(70+(i%4)*210)+'px';e.style.top=(450+Math.floor(i/4)*138)+'px';g('seats').appendChild(e);SE.push(e)}
// 별(고정 위치)
let sd=11;const rnd=()=>{sd=(sd*16807)%2147483647;return sd/2147483647};
for(let i=0;i<46;i++){const c=document.createElementNS(NS,'circle');c.setAttribute('cx',rnd()*1080);c.setAttribute('cy',rnd()<.5?rnd()*320:1480+rnd()*420);c.setAttribute('r',2+rnd()*4);c.setAttribute('fill','@@CREAM@@');c.setAttribute('opacity',.25+rnd()*.5);g('stars').appendChild(c)}
function seek(ms){const b=B(ms), ph=b-Math.floor(b), pulse=0.03*Math.exp(-ph*5);
 // 종이 비행기와 티켓은 아주 천천히 흔들림(움직이는 정지)
 g('ticket').style.transform=`rotate(${Math.sin(b*.32)*.7}deg) scale(${1+pulse*.35})`;
 g('plane').style.transform=`translateX(${Math.sin(b*.9)*8}px)`;
 g('bg').style.transform=`translateY(${Math.sin(b*.25)*10}px)`;
 // 좌석: 박 6부터 하나씩 찍힘(0.55박 간격), 박 14에 사라지고 도장이 자리를 대신함
 SE.forEach((e,i)=>{const t0=6+i*.55, q=out(cl((b-t0)/.3)), on=b>=t0; e.style.background=on?'@@INK@@':'@@CREAM@@'; e.style.color=on?'@@CREAM@@':'@@INK@@';
   const fade=1-cl((b-14)/.5); e.style.opacity=fade; e.style.transform=`scale(${(on?1+.12*(1-q):1)*(1-.2*(1-fade))})`});
 // 도장: 박 14.4에 크게 내려찍힘
 const st=g('stamp'), sp=out(cl((b-14.4)/.35)); st.style.opacity=b<14.4?0:Math.min(1,sp*5)*(1-cl((b-26)/.5)*0); st.style.transform=`rotate(-10deg) scale(${1.7-.7*sp+(b>15?pulse*.7:0)})`;
 // 안내 문구 두 개
 g('m1').style.opacity=cl((b-19.5)/.4)*(1-cl((b-25.6)/.4)); g('m2').style.opacity=cl((b-26)/.4);
 // 마지막 박(31~32): 절취선이 뜯김 — 아랫 부분이 살짝 떨어져 기울어짐
 const tear=out(cl((b-30.6)/.9)); g('stub').style.transform=`translate(${tear*34}px,${tear*80}px) rotate(${tear*6}deg)`; g('perf').style.opacity=.55*(1-tear*.0);
}
seek(0);
</script>"""
    for k, v in {"@@FONTS@@": K.css("gm"), "@@NAVY@@": NAVY, "@@CREAM@@": CREAM, "@@RED@@": RED, "@@INK@@": INK, "@@BEAT@@": repr(beat)}.items(): h = h.replace(k, v)
    return h
if __name__ == "__main__":
    mi = MP.choose("fun", "boarding-2027"); beat = 60.0 / mi["bpm"]; nb = 32; total = nb * beat
    hp = "/tmp/boarding.html"; open(hp, "w", encoding="utf-8").write(html(beat))
    out = os.path.join(HERE, "..", "2026-motion", "boarding_2027.mp4"); secs = HM.render_html(hp, out, total)
    MP.mux(out, [6 * beat, 8 * beat, 6 * beat, 6 * beat, 6 * beat], mi, 101)
    print("음악:", mi["style"], mi["bpm"], mi["key"], "| 박자", round(beat, 3), "초 | 길이", round(secs, 1), "초")
