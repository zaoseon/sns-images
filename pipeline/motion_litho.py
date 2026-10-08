"""리소그래프 모션그래픽 v2 '내 별자리, 사주랑 같은 말 할까요?'(10/5 대표 지적 반영).
지적: ①겹치는 영역이 커서 글자가 앉을 자리가 없다 ②원 안 글자는 흰색이 깔끔 ③내용이 안 끌린다(릴스 공식과 안 맞음).
고침: 겹침을 좁히고, 원 안 글자를 흰색으로, 가운데를 '12별자리 순위'(자기 별자리를 찾아보게)로 바꿨다.
숫자: content/cross_data/README.md '태양별자리별 사주=점성술 일치율'(무작위 3,000명, 별자리당 약 250명이라 오차가 큼).
사용: python3 pipeline/motion_litho.py -> 2026-motion/litho_cross.mp4"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import music_plan as MP, html_motion as HM, fonts_kit as K
PINK = "#ee3f86"; BLUE = "#4560f0"; INK = "#17102b"; PAPER = "#f4ead7"
RANK = [("염소", 23.0), ("황소", 22.7), ("처녀", 18.1), ("사자", 16.3), ("물병", 14.1), ("사수", 13.4), ("쌍둥이", 12.9), ("게", 12.6), ("양", 9.9), ("전갈", 7.3), ("물고기", 6.1), ("천칭", 5.6)]
GRAIN = "data:image/svg+xml;utf8," + "%3Csvg xmlns='http://www.w3.org/2000/svg' width='300' height='300'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/%3E%3CfeColorMatrix values='0 0 0 0 .35  0 0 0 0 .28  0 0 0 0 .2  0 0 0 .55 0'/%3E%3C/filter%3E%3Crect width='300' height='300' filter='url(%23n)'/%3E%3C/svg%3E"
def HT(col, pos, fade, op): return f'<div class="a" style="left:0;{pos};width:1080px;height:560px;background:radial-gradient(circle at center,{col} 34%,transparent 36%) 0 0/34px 34px;-webkit-mask-image:linear-gradient(to {fade},#000,transparent);mix-blend-mode:multiply;opacity:{op}"></div>'
def html(beat):
    bars = "".join(f'<div class="a bar" id=bar{i} style="top:{520 + i * 76}px"><div class="a d bl" style="left:24px;top:6px;font-size:46px;color:#fff">{n}</div><div class="a d bv" id=bv{i} style="top:6px;font-size:46px;color:@@INK@@">{v:.1f}%</div></div>' for i, (n, v) in enumerate(RANK))
    h = """<!doctype html><meta charset=utf-8><style>@@FONTS@@
html,body{margin:0;width:1080px;height:1920px;overflow:hidden;background:@@PAPER@@;font-family:'JW-B',sans-serif;font-weight:800;color:@@INK@@;word-break:keep-all}
.a{position:absolute}.d{font-family:'JW-D',sans-serif;font-weight:900}.t{text-align:center;white-space:nowrap}
.c{border-radius:50%;mix-blend-mode:multiply;will-change:transform,opacity}
.paper{left:0;top:0;width:1080px;height:1920px;background:@@PAPER@@}
.grain{left:0;top:0;width:1080px;height:1920px;background:url("@@GRAIN@@");mix-blend-mode:multiply;opacity:.26;pointer-events:none;z-index:50}
.bar{left:70px;height:64px;width:0;background:#5b2fb0;border-radius:0 32px 32px 0;opacity:0}
.bv{white-space:nowrap}
</style><body>
<div class="a paper" id=p0>
 @@HT1@@@@HT2@@
 <div class="a d t" id=hl style="left:0;width:1080px;top:340px;font-size:96px;line-height:1.3">내 별자리,<br>사주랑 같은 말 할까요?</div>
 <div class="a c" id=pinkC style="left:-20px;top:700px;width:660px;height:660px;background:@@PINK@@"></div>
 <div class="a c" id=blueC style="left:440px;top:700px;width:660px;height:660px;background:@@BLUE@@"></div>
 <div class="a c" id=blueD style="left:440px;top:700px;width:660px;height:660px;box-sizing:border-box;border:10px dashed @@BLUE@@;background:transparent;opacity:.6"></div>
 <div class="a d t" id=wSaju style="left:20px;width:380px;top:962px;font-size:120px;color:#fff">사주</div>
 <div class="a d t" id=wStar style="left:670px;width:420px;top:975px;font-size:96px;color:#fff">별자리</div>
 <div class="a d t" id=wSame style="left:440px;width:200px;top:1090px;font-size:46px;color:#fff">같은 말</div>
 @@BARS@@
 <div class="a d t" id=rk style="left:0;width:1080px;top:310px;font-size:66px;line-height:1.3">사주와 같은 말을 하는<br>별자리 순위</div>
</div>
<div class="a paper" id=p4 style="box-shadow:-30px 0 40px rgba(60,40,20,.25)">
 @@HT3@@@@HT4@@
 <div class="a c" id=disk4 style="left:80px;top:520px;width:920px;height:920px;background:@@BLUE@@"></div>
 <div class="a d t" id=t4a style="left:0;width:1080px;top:730px;font-size:108px;line-height:1.3;color:#fff">내 별자리는</div>
 <div class="a d t" id=t4b style="left:0;width:1080px;top:880px;font-size:108px;line-height:1.3;color:#fff">몇 위일까요?</div>
 <div class="a t d" id=t4c style="left:0;width:1080px;top:1100px;font-size:60px;line-height:1.4;color:#fff">댓글로 알려 주세요</div>
 <div class="a t" id=t4d style="left:0;width:1080px;top:1210px;font-size:54px;line-height:1.4;color:#fff">친구 별자리도 보내 보세요</div>
</div>
<div class="a grain"></div>
<script>
const BEAT=@@BEAT@@, B=ms=>ms/1000/BEAT, cl=(x,a=0,b=1)=>Math.min(b,Math.max(a,x));
function bez(x1,y1,x2,y2){return t=>{if(t<=0)return 0;if(t>=1)return 1;let a=0,b=1,u=t;for(let i=0;i<24;i++){const x=3*(1-u)*(1-u)*u*x1+3*(1-u)*u*u*x2+u*u*u;if(x<t)a=u;else b=u;u=(a+b)/2}return 3*(1-u)*(1-u)*u*y1+3*(1-u)*u*u*y2+u*u*u}}
const out=bez(.23,1,.32,1), g=id=>document.getElementById(id);
const VAL=@@VALS@@; let b=0;
const stamp=(b0,dur,from)=>{const p=out(cl((b-b0)/dur));return {o:Math.min(1,p*6),s:from+(1-from)*p}};
function seek(ms){b=B(ms);
 const ph=b-Math.floor(b), pulse=0.03*Math.exp(-ph*5), drift=1+0.03*cl(b/8)+pulse, fo=1-cl((b-8)/.6);
 g('hl').style.opacity=fo; g('hl').style.transform=`scale(${drift})`;
 const s=stamp(0,.45,1.1); g('pinkC').style.opacity=fo; g('pinkC').style.transform=`scale(${s.s*drift})`; g('wSaju').style.opacity=fo; g('wSaju').style.transform=`scale(${s.s*drift})`;
 const bs=stamp(4,.45,1.18), bo=b<4?0:Math.min(1,bs.o);
 g('blueC').style.opacity=bo*fo; g('blueC').style.transform=`scale(${bo?bs.s*drift:1})`; g('blueD').style.opacity=(b<4?.6:0)*fo; g('blueD').style.transform=`scale(${drift}) rotate(${b*9}deg)`;
 g('wStar').style.opacity=bo*fo; g('wStar').style.transform=`scale(${bo?bs.s*drift:1})`;
 const ss=stamp(5,.4,1.3); g('wSame').style.opacity=(b<5?0:ss.o)*fo; g('wSame').style.transform=`scale(${b<5?1:ss.s})`;
 // 순위: 박 9부터 아래(천칭)에서 위(염소)로 한 박에 하나씩
 g('rk').style.opacity=cl((b-8.8)/.5)*(1-cl((b-22)/.6));
 for(let i=0;i<12;i++){const t0=9+(11-i)*1.0; const q=out(cl((b-t0)/.7)); const el=g('bar'+i);
   el.style.opacity=q*(1-cl((b-22)/.6)); el.style.width=(168+VAL[i]*27*q)+'px';
   const bv=g('bv'+i); bv.style.left=(168+VAL[i]*27*q+18)+'px'; const top1=(i===0&&b>20)?1+0.06*Math.exp(-ph*5):1; el.style.transform=`scaleY(${top1})`}
 // 종이 넘기기
 const x4=(1-out(cl((b-22)/.7)))*1180; g('p4').style.transform=`translateX(${x4}px)`; g('p4').style.display=b<21.9?'none':'block';
 g('disk4').style.transform=`scale(${1+(b>22?pulse*.8:0)})`;
 g('t4a').style.opacity=cl((b-22.6)/.4); g('t4b').style.opacity=cl((b-23.4)/.4); g('t4c').style.opacity=cl((b-24.4)/.4); g('t4d').style.opacity=cl((b-25.2)/.4);
 const gr=document.querySelector('.grain'); gr.style.backgroundPosition=((Math.floor(b*6)%7)*41)+'px '+((Math.floor(b*6)%5)*57)+'px';
}
seek(0);
</script>"""
    for k, v in {"@@FONTS@@": K.css("gm"), "@@PAPER@@": PAPER, "@@INK@@": INK, "@@PINK@@": PINK, "@@BLUE@@": BLUE, "@@GRAIN@@": GRAIN, "@@BEAT@@": repr(beat), "@@BARS@@": bars,
                 "@@HT1@@": HT(PINK, "top:0", "bottom", ".5"), "@@HT2@@": HT(BLUE, "top:1360px", "top", ".5"), "@@HT3@@": HT(PINK, "top:0", "bottom", ".5"), "@@HT4@@": HT(BLUE, "top:1360px", "top", ".5"), "@@VALS@@": str([v for _, v in RANK])}.items(): h = h.replace(k, v)
    return h
if __name__ == "__main__":
    mi = MP.choose("data", "litho-cross"); beat = 60.0 / mi["bpm"]; nb = 27; total = nb * beat
    hp = "/tmp/litho.html"; open(hp, "w", encoding="utf-8").write(html(beat))
    out = os.path.join(HERE, "..", "2026-motion", "litho_cross.mp4"); secs = HM.render_html(hp, out, total)
    MP.mux(out, [4 * beat, 4 * beat, 14 * beat, 5 * beat], mi, 97)
    print("음악:", mi["style"], mi["bpm"], mi["key"], "| 박자", round(beat, 3), "초 | 길이", round(secs, 1), "초")
