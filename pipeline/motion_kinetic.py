"""키네틱 타이포 모션그래픽 견본 K1 '읽고도 답장 못 한 날'(10/5). 검정 + 흰 글자 + 강조색, 글자와 도형이 음악 박자마다 튀어나온다. 얼굴 없음(글자가 주인공).
사용: python3 pipeline/motion_kinetic.py -> 2026-motion/kinetic_reply.mp4"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import music_plan as MP, html_motion as HM, fonts_kit as K, brand_frame as BF
ACC = "#ff5c8a"; BLACK = os.path.join(HERE, "fonts", "PRETENDARD-BLACK.OTF")
SPEC_REPLY = dict(acc="#ff5c8a", name="kinetic_reply", tag="정월의 연락 테스트", hook=["읽고도", "답장", "못 한 날"], q="나는 <span class=c>어느 쪽</span>?", opts=["바로 답해야 편해요", "고민하다 늦게 보내요", "읽고 이따 하고 잊어요"],
    r="많이 고른 번호는<span class=c>?</span>", res=["바로 답하는 쪽", "다듬어 보내는 쪽", "천천히 답하는 쪽"], note="빠르다 느리다가 아니라<br><span class=c>연락의 리듬</span>이에요", cta=["떠오르는", "사람에게", "보내 보세요"], music="fun")
def html(beat, S=None):
    S = S or SPEC_REPLY
    h = """<!doctype html><meta charset=utf-8><style>
@@FONTS@@
html,body{margin:0;width:1080px;height:1920px;background:#0a0a0c;overflow:hidden;word-break:keep-all;line-break:strict;font-family:'JW-B',sans-serif;font-weight:800;color:#fff}
.e{position:absolute;left:0;width:1080px;text-align:center;opacity:0;will-change:transform}
.w{font-family:'JW-D',sans-serif;font-weight:900;font-size:150px;line-height:1.3;letter-spacing:-2px}
.t{font-family:'JW-D',sans-serif;font-weight:900;font-size:100px;line-height:1.35}
.o{font-size:64px;line-height:1.45;text-align:left;left:60px;width:840px;display:flex;align-items:center;gap:28px}
.o b{font-family:'JW-D',sans-serif;flex:none;width:96px;height:96px;border-radius:50%%;background:%s;color:#0a0a0c;display:flex;align-items:center;justify-content:center;font-size:64px}
.c{color:%s}
.sh{position:absolute;opacity:0}
.tag{position:absolute;left:60px;top:412px;font-size:46px;color:%s;font-family:'JW-D',sans-serif;font-weight:900;opacity:0}   /* R04: 배지 대신 작은 글, 상단 문구 띠 아래 */
@@BFCSS@@
</style><body>
<div class=tag id=tag>@@TAG@@</div>
<div class=sh id=c1 style="left:-140px;top:700px;width:520px;height:520px;border-radius:50%%;background:%s"></div>
<div class=sh id=bar style="left:260px;top:1360px;width:640px;height:40px;background:#fff"></div>
<div class=sh id=tri style="left:790px;top:420px;width:0;height:0;border-left:120px solid transparent;border-right:120px solid transparent;border-bottom:208px solid %s"></div>
<div class="e w" id=a1 style="top:600px">@@H1@@</div><div class="e w c" id=a2 style="top:840px">@@H2@@</div><div class="e w" id=a3 style="top:1080px">@@H3@@</div>
<div class="e t" id=b0 style="top:520px">@@Q@@</div>
<div class="e o" id=b1 style="top:700px"><b>1</b>@@O1@@</div><div class="e o" id=b2 style="top:920px"><b>2</b>@@O2@@</div><div class="e o" id=b3 style="top:1140px"><b>3</b>@@O3@@</div>
<div class="e t" id=c0 style="top:520px">@@R@@</div>
<div class="e o" id=d1 style="top:660px"><b>1</b>@@D1@@</div><div class="e o" id=d2 style="top:830px"><b>2</b>@@D2@@</div><div class="e o" id=d3 style="top:1000px"><b>3</b>@@D3@@</div>
<div class="e t" id=c9 style="top:1170px;font-size:68px;line-height:1.5">@@N@@</div>
<div class="e w" id=f1 style="top:560px;font-size:140px">@@F1@@</div><div class="e w c" id=f2 style="top:780px;font-size:140px">@@F2@@</div><div class="e w" id=f3 style="top:1000px;font-size:140px">@@F3@@</div>
@@BF@@
<script>
const BEAT=%f; const B=ms=>ms/1000/BEAT;
function bez(x1,y1,x2,y2){return t=>{if(t<=0)return 0;if(t>=1)return 1;let a=0,b=1,u=t;for(let i=0;i<24;i++){const x=3*(1-u)*(1-u)*u*x1+3*(1-u)*u*u*x2+u*u*u;if(x<t)a=u;else b=u;u=(a+b)/2}return 3*(1-u)*(1-u)*u*y1+3*(1-u)*u*u*y2+u*u*u}}
const ez={out:bez(0.23,1,0.32,1),back:x=>{const c=1.2;return 1+(c+1)*Math.pow(x-1,3)+c*Math.pow(x-1,2)}};
const cl=(x,a=0,b=1)=>Math.min(b,Math.max(a,x));
// 요소: [id, 들어옴(박자), 나감(박자), 종류, 방향]
const E=[['a1',0,5.5,'slam',0],['a2',1,5.5,'slam',0],['a3',2,5.5,'slam',0],
 ['b0',6,14.5,'slam',0],['b1',8,14.5,'slide',-1],['b2',10,14.5,'slide',1],['b3',12,14.5,'slide',-1],
 ['c0',15,24.5,'slam',0],['d1',17,24.5,'slide',-1],['d2',19,24.5,'slide',1],['d3',21,24.5,'slide',-1],['c9',23,24.5,'slam',0],
 ['f1',25,33,'slam',0],['f2',26,33,'slam',0],['f3',27,33,'slam',0]];
const els=Object.fromEntries(E.map(e=>[e[0],document.getElementById(e[0])]));
function seek(ms){const b=B(ms);
 for(const [id,tin,tout,kind,dir] of E){const el=els[id];let p=cl((b-tin)/0.5),q=cl((b-tout)/0.5);
  if(b<tin||q>=1){el.style.opacity=0;continue}
  let op=Math.min(1,p*2)*(1-q),tx=0,ty=0,sc=1;
  if(kind=='slam'){sc=(1+0.6*(1-ez.back(p)))*(1-0.08*ez.out(q))}
  else{tx=dir*520*(1-ez.out(p))+dir*520*ez.out(q);sc=1+0.04*(1-ez.back(p))}   // 들어온 쪽으로 다시 나간다
  el.style.opacity=op;el.style.transform=`translate(${tx}px,${ty}px) scale(${sc})`}
 const pulse=x=>Math.pow(Math.max(0,1-(b%%1)/0.45),2);
 const tg=document.getElementById('tag');tg.style.opacity=cl(b/1)*(b<32?1:cl(33-b));tg.style.transform=`scale(${1+0.05*pulse()})`;
 const c1=document.getElementById('c1');c1.style.opacity=((b>3&&b<5.5)?cl((b-3)/1)*0.9:(b>14.8&&b<17)?cl((b-14.8)/0.4)*0.9*cl(17-b):0);c1.style.transform=`scale(${1+0.12*pulse()+0.25}) translateY(${Math.sin(b*0.8)*20}px)`;
 const bar=document.getElementById('bar');bar.style.opacity=(b>6&&b<14.5)||(b>15&&b<22.5)?0.9:0;bar.style.transform=`translateX(${(1-ez.out(cl((b%%8)/1.5)))*400}px)`;
 const tri=document.getElementById('tri');tri.style.opacity=(b>25&&b<33)?0.95:(b>0&&b<6?0.0:0);tri.style.transform=`rotate(${b*22}deg) scale(${1+0.15*pulse()})`;
}
seek(0);
</script>""" % (S["acc"], S["acc"], S["acc"], S["acc"], S["acc"], beat)
    m = {"H1": S["hook"][0], "H2": S["hook"][1], "H3": S["hook"][2], "TAG": S["tag"], "Q": S["q"], "O1": S["opts"][0], "O2": S["opts"][1], "O3": S["opts"][2], "R": S["r"], "D1": S["res"][0], "D2": S["res"][1], "D3": S["res"][2], "N": S["note"], "F1": S["cta"][0], "F2": S["cta"][1], "F3": S["cta"][2]}
    for k, v in m.items(): h = h.replace("@@" + k + "@@", v)
    h = h.replace("@@FONTS@@", K.css("gm")).replace("@@BFCSS@@", BF.css()).replace("@@BF@@", BF.html("reel", ai=False))   # 확정 규칙 층: 상단 왼쪽 자오선·상단 오른쪽 문구·우측 하단 주소(R01·R02)
    return h
def check_spec(S):
    import re
    bad = []
    for t in S["opts"] + S["res"]:
        if len(t) > 12: bad.append("선택지·결과는 12자 이내: " + t)
    for t in S["hook"] + S["cta"]:
        if len(re.sub("<[^>]+>", "", t)) > 6: bad.append("큰 글자는 한 줄 6자 이내: " + t)
    if bad: raise SystemExit("대본 점검 실패\n" + "\n".join(bad))
def build(S):
    check_spec(S)
    mi = MP.choose(S.get("music", "fun"), S["name"]); beat = 60.0 / mi["bpm"]; total = 33 * beat
    hp = "/tmp/%s.html" % S["name"]; open(hp, "w", encoding="utf-8").write(html(beat, S))
    out = os.path.join(HERE, "..", "2026-motion", S["name"] + ".mp4"); secs = HM.render_html(hp, out, total)
    MP.mux(out, [6 * beat, 9 * beat, 10 * beat, 8 * beat], mi, 91 + len(S["name"])); print("음악:", mi["style"], mi["bpm"], mi["key"], "| 박자", round(beat, 3), "초 | 길이", round(secs, 1), "초 |", out); return out
if __name__ == "__main__":
    S = dict(SPEC_REPLY)
    if len(sys.argv) > 1: S.update(json.load(open(sys.argv[1], encoding="utf-8")))     # 대본 JSON만 바꿔서 새 편을 만든다
    build(S)
