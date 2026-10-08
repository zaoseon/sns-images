"""리소그래프 6판 '내 별자리, 사주랑 같은 말 할까요?' — 별빛 배경판(10/6 대표 지적 반영).
지적: ①글자를 더 가운데로, "같은 말"을 사주·별자리와 같은 줄로 ②배경은 해·달·별이 있는 우리 소재로 ③UI에 가려지는 위아래도 알차게 채우고 글자는 크게 ④표지와 CTA가 없다.
소재: assets/brand_bg (남색 별빛 아틀라스를 돌려 위·아래에 성운, 금빛 황도 차트, 해·달 잘라냄). 숫자: content/cross_data/README.md '태양별자리별 일치율'.
규칙: 글자 단색(흰색·금색), 색 그림자 없음, 도형 경계에 글자가 걸치지 않음, 첫 프레임 완성, 문장 2초 이상.
사용: python3 pipeline/motion_litho_star.py -> 2026-motion/litho_star6.mp4 + litho_star6_cover.jpg"""
import os, sys, asyncio
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import music_plan as MP, html_motion as HM, fonts_kit as K, brand_frame as BF, template_engine as TE
R = os.path.abspath(os.path.join(HERE, ".."))
AS = os.path.join(R, "assets", "brand_bg")
GOLD = "#e7c88d"; PINK = "#ff5c9d"; BLUE = "#4560f0"
RANK = [("염소", 23.0), ("황소", 22.7), ("처녀", 18.1), ("사자", 16.3), ("물병", 14.1), ("사수", 13.4), ("쌍둥이", 12.9), ("게", 12.6), ("양", 9.9), ("전갈", 7.3), ("물고기", 6.1), ("천칭", 5.6)]

def ex_blocks():
    L = TE.explain_layout("reel"); u = L["u"]; cx = L["cx"]; ax, ay, D = L["avatar"]; bl, bt, bw, bh = L["bubble"]; fs = L["bubble_fs"]
    def mark(l): return l.replace("'같은\u00a0말'", "<b class=gm>'같은&nbsp;말'</b>").replace("'다른\u00a0말'", "<b class=gm>'다른&nbsp;말'</b>")
    texts = "".join(f'<div class="a xt" id=b{i + 1}><div style="text-align:center">{"<br>".join(mark(l) for l in L["bubble_lines"][i])}</div></div>' for i in range(3))
    bx, by, bhh = L["badge"]; bwid = TE.font(K.P["gm_bold"], int(38 * u)).getlength("정월") + 56 * u
    h = (f'<div class="a" id=jw style="left:{ax:.0f}px;top:{ay:.0f}px;width:{D:.0f}px;height:{D:.0f}px;border-radius:50%;overflow:hidden;border:{6 * u:.0f}px solid #e7c88d;background:radial-gradient(circle at 50% 35%,#27346f,#0b1235);box-shadow:0 0 44px rgba(231,200,141,.35);opacity:0"><img style="position:absolute;left:{-D * .158:.0f}px;top:{D * .03:.0f}px;width:{D * 1.333:.0f}px" src="file://@@JW@@"></div>'
         f'<div class="a" id=tlo style="left:{bl - 30:.0f}px;top:{bt + bh / 2 - 26:.0f}px;width:0;height:0;border:26px solid transparent;border-right:34px solid #e7c88d;border-left:0;opacity:0"></div><div class="a" id=tli style="left:{bl - 26:.0f}px;top:{bt + bh / 2 - 21:.0f}px;width:0;height:0;border:21px solid transparent;border-right:29px solid #151f55;border-left:0;opacity:0"></div>'
         f'<div class="a" id=bub style="left:{bl:.0f}px;top:{bt:.0f}px;width:{bw:.0f}px;height:{bh:.0f}px;box-sizing:border-box;background:linear-gradient(145deg,rgba(28,40,92,.95),rgba(9,14,44,.95));border:3px solid #e7c88d;border-radius:{42 * u:.0f}px;box-shadow:0 0 46px rgba(231,200,141,.28);opacity:0">'
         f'<div class="a d" style="left:{30 * u:.0f}px;top:{-27 * u:.0f}px;width:{bwid:.0f}px;height:{bhh:.0f}px;border-radius:{bhh:.0f}px;background:#e7c88d;color:#17102b;display:flex;align-items:center;justify-content:center;font-size:{int(38 * u)}px;line-height:1">정월</div>{texts}</div>')
    btop, bfs = L["banner"]; ltop, lfs = L["label"]; ttop, td = L["tok"]; gtop, gh, gfs = L["legend"]
    h += (f'<div class="a d xban" id=banA style="top:{btop:.0f}px;font-size:{bfs}px">같은 말 = 타고난 결</div><div class="a d xban" id=banB style="top:{btop:.0f}px;font-size:{bfs}px">다른 말 = 내가 고를 곳</div>'
          f'<div class="a" id=grp2 style="left:0;top:0;width:1080px;height:1920px;isolation:isolate"><div class="a" id=tkP style="top:{ttop:.0f}px;width:{td:.0f}px;height:{td:.0f}px;border-radius:50%;background:@@PINK@@;mix-blend-mode:multiply;opacity:0"></div><div class="a" id=tkB style="top:{ttop:.0f}px;width:{td:.0f}px;height:{td:.0f}px;border-radius:50%;background:@@BLUE@@;mix-blend-mode:multiply;opacity:0"></div></div>'
          f'<div class="a d xban" id=sixl style="top:{ltop:.0f}px;font-size:{lfs}px;opacity:0">자오선이 나눈 여섯 방향</div>')
    for k, (xx, yy, ww, hh) in enumerate(L["chips"]): h += f'<div class="a d" id=chip{k} style="left:{xx:.0f}px;top:{yy:.0f}px;width:{ww:.0f}px;height:{hh:.0f}px;box-sizing:border-box;border-radius:{26 * u:.0f}px;border:4px solid rgba(231,200,141,.65);background:rgba(255,255,255,.1);color:#fff;display:flex;align-items:center;justify-content:center;font-size:{L["chip_fs"]}px;opacity:0">{TE.SIX[k]}</div>'
    for j, (col, tx) in enumerate((("@@PINK@@", "사주가 짚은 방향"), ("@@BLUE@@", "별자리가 짚은 방향"))): h += f'<div class="a d xban" id=leg{j + 1} style="top:{gtop + j * gh:.0f}px;font-size:{gfs}px;line-height:{gh:.0f}px;color:rgba(255,255,255,.88);opacity:0"><span style="display:inline-block;width:{gfs * .8:.0f}px;height:{gfs * .8:.0f}px;border-radius:50%;background:{col};vertical-align:-2px;margin-right:14px"></span>{tx}</div>'
    js = (" // 장면 2: 정월이 설명(박 6.2~17.8) — 좌표는 template_engine.explain_layout 계산값\n const e2=cl((b-6.2)/.6), x2=1-cl((b-17.4)/.6); const jwq=out(e2);\n"
          " g('jw').style.opacity=jwq*x2; g('jw').style.transform=`translateX(${(1-jwq)*-140}px) scale(${1+(b>6.6&&b<17.4?pulse*.4:0)})`; const bfa=g('bfAI'); if(bfa) bfa.style.opacity=jwq*x2*.9;\n"
          " g('bub').style.opacity=jwq*x2; g('bub').style.transform=`scale(${.96+.04*jwq+(b>6.6&&b<17?pulse*.35:0)})`; g('tlo').style.opacity=jwq*x2; g('tli').style.opacity=jwq*x2;\n"
          " const tx=(id,a,c)=>{g(id).style.opacity=cl((b-a)/.35)*(1-cl((b-c)/.35))};\n tx('b1',6.7,10.3); tx('b2',10.5,14.1); tx('b3',14.3,17.4);\n g('sixl').style.opacity=cl((b-7.2)/.5)*x2;\n"
          " for(let k=0;k<6;k++){const ch=g('chip'+k), q=out(cl((b-(7.0+k*.2))/.4)); ch.style.opacity=q*x2; ch.style.transform=`translateY(${(1-q)*30}px)`;\n"
          "   const on=(b>10.8&&b<14.6&&k===0)||(b>=14.8&&b<17.4&&(k===0||k===1)); ch.style.background=on?(k===0&&b<14.8?'rgba(122,79,208,.75)':(k===0?'rgba(255,92,157,.55)':'rgba(69,96,240,.6)')):'rgba(255,255,255,.1)'}\n"
          " g('leg1').style.opacity=cl((b-8.4)/.5)*x2; g('leg2').style.opacity=cl((b-8.9)/.5)*x2;\n"
          f" const tq=out(cl((b-10.6)/.45)), mv=out(cl((b-14.4)/.8)); const dd={td:.1f}, c0={L['tok_c0']:.1f}, c1={L['tok_c1']:.1f}, off=dd*.28;\n"
          " const pkx=(c0-dd/2-off)+(b>14.4?off*mv:0), bkx=(c0-dd/2+off)+(c1-c0-off)*mv;\n"
          " const tk=g('tkP'), tb=g('tkB'); tk.style.left=pkx+'px'; tb.style.left=bkx+'px'; tk.style.opacity=tq*x2; tb.style.opacity=tq*x2; tk.style.transform=`scale(${.6+.4*tq})`; tb.style.transform=`scale(${.6+.4*tq})`;\n"
          " g('banA').style.opacity=cl((b-11.0)/.4)*(1-cl((b-14.5)/.3))*x2; g('banB').style.opacity=cl((b-15.0)/.4)*x2;\n")
    return h, js

import functools
@functools.lru_cache(maxsize=None)
def lay():
    """표지(1)·순위(5)·마무리(7) 페이지를 틀 엔진이 계산한 값으로 쓴다 — 가로는 안전 영역 x 50~900 안(R04), 가운데 정렬·간격은 R08·R09·R18."""
    p1 = TE.t_hook("reel", "내 별자리,\n사주랑 같은 말\n할까요?", "사주", "별자리", "같은 말")
    p5 = TE.t_ranking("reel", "사주와 같은 말을 하는\n별자리 순위", list(RANK))
    p7 = TE.t_cta("reel", "팔로우하고", "더 많은 이야기 나눠요", "프로필 링크에서", ("생년월일 입력하고", "내 첫글자와 타고난 기운 알아보기"), "＋ 팔로우")
    return p1, p5, p7
def hook_blocks(p):
    m = p.meta; D = m["D"]; gap = m["gap"]; gx0 = m["gx0"]; cy = m["cy"]
    h = f'<div class="a d t" id=hl style="left:0;width:950px;top:{m["title_top"]:.0f}px;font-size:{m["title_size"]}px;line-height:1.2">{"<br>".join(m["title_lines"])}</div>\n'
    h += f'<div class="a grp" id=grp><div class="a c" id=pinkC style="left:{gx0:.0f}px;top:{cy:.0f}px;width:{D:.0f}px;height:{D:.0f}px;background:@@PINK@@"></div><div class="a c" id=blueC style="left:{gx0 + gap:.0f}px;top:{cy:.0f}px;width:{D:.0f}px;height:{D:.0f}px;background:@@BLUE@@"></div></div>\n'
    h += f'<div class="a c" id=blueD style="left:{gx0 + gap:.0f}px;top:{cy:.0f}px;width:{D:.0f}px;height:{D:.0f}px;box-sizing:border-box;border:8px dashed @@BLUE@@;background:transparent;opacity:.7;mix-blend-mode:normal"></div>\n'
    for i, k, tx in (("wSaju", "왼쪽 글자", "사주"), ("wStar", "오른쪽 글자", "별자리"), ("wSame", "가운데 글자", "같은 말")):
        cx_, cy_, sz = m["labels"][k]; h += f'<div class="a d t lab" id={i} style="left:{cx_:.0f}px;top:{cy_:.0f}px;font-size:{sz}px">{tx}</div>\n'
    return h
def rank_blocks(p):
    m = p.meta
    rk = f'<div class="a d t" id=rk style="left:0;width:950px;top:{m["title_top"]:.0f}px;font-size:{m["title_size"]}px;line-height:1.2;opacity:0">{"<br>".join(m["title_lines"])}</div>'
    bars = "".join(f'<div class="a bar" id=bar{i} style="left:{m["x0"]:.0f}px;top:{t:.0f}px;height:{bh:.0f}px;border-radius:0 {bh / 2:.0f}px {bh / 2:.0f}px 0"><div class="a d bl" style="font-size:{m["fs"]}px;line-height:{bh:.0f}px;top:0">{n}</div><div class="a d bv" style="font-size:{m["fs"]}px;line-height:{bh:.0f}px;top:0">{v:.1f}%</div></div>' for i, ((t, bh, w), (n, v)) in enumerate(zip(m["rows"], RANK)))
    return rk, bars, [round(w) for _, _, w in m["rows"]]
def cta_blocks():
    """마무리 ② 페이지: 틀 엔진 계산값(카드 높이=글 높이+같은 위아래 여백, 묶음 전체 가운데, 가로는 안전 영역 안)을 그대로 쓴다."""
    m = lay()[2].meta; T = m["T"]; fz = {k: m[k] for k in ("fa", "fb", "fia", "fib", "fic")}
    def d(i, k, f, color=""): return f'<div class="a d t" id={i} style="left:0;width:950px;top:{T[k]:.0f}px;font-size:{f["size"]}px;line-height:{f["lh"]};{color}opacity:0">{"<br>".join(f["lines"])}</div>'
    h = d("f1", "a", fz["fa"]) + "\n" + d("f2", "b", fz["fb"], "color:@@GOLD@@;") + "\n"
    h += f'<div class="a" id=fcard style="left:{m["cxl"]:.0f}px;top:{T["card"]:.0f}px;width:{m["cxr"] - m["cxl"]:.0f}px;height:{T["card_h"]:.0f}px;box-sizing:border-box;border:3px solid #e7c88d;border-radius:44px;background:linear-gradient(145deg,rgba(28,40,92,.9),rgba(9,14,44,.9));box-shadow:0 0 46px rgba(231,200,141,.25);opacity:0"></div>\n'
    h += d("f3", "ia", fz["fia"], "color:@@GOLD@@;") + "\n" + d("f4", "ib", fz["fib"]) + "\n" + d("f5", "ic", fz["fic"]) + "\n"
    h += f'<div class="a d t" id=fbtn style="left:{m["cx"] - m["bw"] / 2:.0f}px;top:{T["btn"]:.0f}px;width:{m["bw"]:.0f}px;height:{m["bh"]:.0f}px;border-radius:{m["bh"] / 2:.0f}px;background:#e7c88d;color:#17102b;font-size:58px;line-height:{m["bh"]:.0f}px;opacity:0">＋ 팔로우</div>\n'
    return h

def html(beat):
    chips = "".join(f'<div class="a d chip" id=chip{k} style="left:{60 + k * 162}px">{n}</div>' for k, n in enumerate(["안정", "표현", "유연", "생성", "결단", "소통"]))
    p1_, p5_, p7_ = lay(); rk_html, bars, WIDS = rank_blocks(p5_); p1_html = hook_blocks(p1_)
    h = """<!doctype html><meta charset=utf-8><style>@@FONTS@@
html,body{margin:0;width:1080px;height:1920px;overflow:hidden;background:#050a1c;font-family:'JW-B',sans-serif;font-weight:800;color:#fff;word-break:keep-all}
.a{position:absolute}.d{font-family:'JW-D',sans-serif;font-weight:900}.t{text-align:center;white-space:nowrap}
#bg{left:0;top:0;width:1080px;height:1920px}
#chart{left:-60px;top:360px;width:1200px;height:1200px;opacity:.42}
#sun{left:60px;top:60px;width:270px;height:259px;mix-blend-mode:screen;-webkit-mask-image:radial-gradient(circle,#000 52%,transparent 74%)}
#moon{left:760px;top:20px;width:230px;height:253px;mix-blend-mode:screen;-webkit-mask-image:radial-gradient(circle,#000 52%,transparent 74%)}
.cover #sun{left:20px;top:420px;width:230px;height:221px}.cover #moon{left:834px;top:410px;width:216px;height:238px}
.avatar{left:40px;top:420px;width:330px;height:330px;border-radius:50%;overflow:hidden;border:6px solid #e7c88d;background:radial-gradient(circle at 50% 35%,#27346f,#0b1235);box-shadow:0 0 44px rgba(231,200,141,.35);opacity:0}
.avatar img{position:absolute;left:-52px;top:10px;width:440px}
.bub{left:402px;top:430px;width:622px;height:322px;background:linear-gradient(145deg,rgba(28,40,92,.95),rgba(9,14,44,.95));border:3px solid #e7c88d;border-radius:42px;box-shadow:0 0 46px rgba(231,200,141,.28),inset 0 0 36px rgba(231,200,141,.10);opacity:0}
.tailo{left:372px;top:540px;width:0;height:0;border:26px solid transparent;border-right:34px solid #e7c88d;border-left:0;opacity:0}
.taili{left:376px;top:545px;width:0;height:0;border:21px solid transparent;border-right:29px solid #151f55;border-left:0;opacity:0}
.spk{left:42px;top:-27px;padding:4px 26px 6px;border-radius:30px;background:#e7c88d;color:#17102b;font-size:38px;line-height:1.2}
.bt{left:36px;top:52%;transform:translateY(-50%);width:550px;font-size:58px;line-height:1.36;font-weight:800;font-family:'JW-B',sans-serif;color:#fff;opacity:0}
.bt em{font-style:normal;font-family:'JW-D',sans-serif;font-weight:900;color:#e7c88d}
.chip{top:1115px;width:150px;height:100px;border-radius:30px;border:4px solid rgba(231,200,141,.65);background:rgba(255,255,255,.1);font-size:52px;line-height:92px;text-align:center;opacity:0}
.tok{width:120px;height:120px;border-radius:50%;opacity:0;mix-blend-mode:multiply}
.ban{left:0;width:1080px;top:795px;text-align:center;font-size:72px;line-height:1.2;color:#e7c88d;opacity:0;white-space:nowrap}
.leg{left:70px;font-size:54px;line-height:1.2;opacity:0;white-space:nowrap}.leg i{display:inline-block;width:44px;height:44px;border-radius:50%;vertical-align:-6px;margin-right:22px}
.sixl{left:0;width:1080px;top:1046px;text-align:center;font-size:50px;color:#e7c88d;opacity:0;white-space:nowrap}
.vig{left:0;top:0;width:1080px;height:1920px;background:radial-gradient(ellipse 62% 40% at 50% 52%,rgba(4,8,26,.62),transparent 78%)}
.grp{left:0;top:0;width:1080px;height:1920px;isolation:isolate}
.c{border-radius:50%;mix-blend-mode:multiply;will-change:transform,opacity}
.lab{transform:translate(-50%,-50%);line-height:1}
.bar{left:70px;height:58px;width:0;border-radius:0 29px 29px 0;background:linear-gradient(90deg,#6a3fc8,#ff5c9d);opacity:0;overflow:hidden}
.bl{left:26px;top:4px;font-size:46px;line-height:1.15;color:#fff}.bv{right:26px;top:4px;font-size:46px;line-height:1.15;color:#fff}
.top1{background:linear-gradient(90deg,#c9a24a,#e7c88d)}.top1 .bl,.top1 .bv{color:#17102b}
.xt{left:0;top:0;width:100%;height:100%;box-sizing:border-box;display:flex;align-items:center;justify-content:center;padding:0 30px;font-family:'JW-B',sans-serif;font-weight:800;font-size:@@XFS@@px;line-height:1.32;color:#fff;opacity:0}.xt .gm,.gm{font-family:'JW-D',sans-serif;font-weight:900;color:#e7c88d}.xban{left:0;width:950px;text-align:center;white-space:nowrap;color:#e7c88d}
@@BFCSS@@</style><body>
<img class="a" id=bg src="file://@@BG@@">
<img class="a" id=chart src="file://@@CHART@@">
<img class="a" id=sun src="file://@@SUN@@"><img class="a" id=moon src="file://@@MOON@@">
<div class="a vig"></div><svg class="a" id=stars width=1080 height=1920 style="left:0;top:0"></svg>
@@P1HTML@@
@@EXHTML@@
@@RKHTML@@
@@BARS@@
<div class="a d t" id=c1 style="left:0;width:950px;top:520px;font-size:116px;line-height:1.22;opacity:0">내 별자리는</div>
<div class="a d t" id=c2 style="left:0;width:950px;top:670px;font-size:116px;line-height:1.22;opacity:0;color:@@GOLD@@">몇 위일까요?</div>
<div class="a d t" id=c3 style="left:0;width:950px;top:880px;font-size:78px;line-height:1.3;opacity:0">댓글로 알려 주세요</div>
@@CTAHTML@@
@@BF@@
<script>
const BEAT=@@BEAT@@, B=ms=>ms/1000/BEAT, cl=(x,a=0,b=1)=>Math.min(b,Math.max(a,x));
function bez(x1,y1,x2,y2){return t=>{if(t<=0)return 0;if(t>=1)return 1;let a=0,b=1,u=t;for(let i=0;i<24;i++){const x=3*(1-u)*(1-u)*u*x1+3*(1-u)*u*u*x2+u*u*u;if(x<t)a=u;else b=u;u=(a+b)/2}return 3*(1-u)*(1-u)*u*y1+3*(1-u)*u*u*y2+u*u*u}}
const out=bez(.23,1,.32,1), g=id=>document.getElementById(id), NS='http://www.w3.org/2000/svg';
const VAL=@@VALS@@; const WID=@@WIDS@@; let seed=5; const rnd=()=>{seed=(seed*16807)%2147483647;return seed/2147483647};
const SP=[]; for(let i=0;i<70;i++){const c=document.createElementNS(NS,'circle');const y=rnd()<.55?rnd()*330:(rnd()<.5?1470+rnd()*450:330+rnd()*1140);c.setAttribute('cx',rnd()*1080);c.setAttribute('cy',y);c.setAttribute('r',1.6+rnd()*3.2);c.setAttribute('fill',rnd()<.5?'#e7c88d':'#ffffff');g('stars').appendChild(c);SP.push([c,rnd()*6.28,.25+rnd()*.6])}
let b=0;
function lab(id,o,s){const e=g(id);e.style.opacity=o;e.style.transform=`translate(-50%,-50%) scale(${s})`}
function seek(ms){b=B(ms);
 const ph=b-Math.floor(b), pulse=0.03*Math.exp(-ph*5), fo=1-cl((b-5.6)/.6);
 // 배경: 황도 차트가 천천히 돈다, 해와 달은 박자에 맞춰 살짝 숨 쉼, 별은 반짝임
 g('chart').style.transform=`rotate(${b*1.6}deg) scale(${1+pulse*.3})`; g('sun').style.transform=`scale(${1+pulse*.9}) rotate(${b*2}deg)`; g('moon').style.transform=`scale(${1+pulse*.9})`;
 SP.forEach(o=>o[0].setAttribute('opacity',(0.25+0.75*Math.abs(Math.sin(b*.9+o[1])))*o[2]+0.1));
 // 장면 1: 헤드라인 + 두 원 + 같은 줄 라벨
 g('hl').style.opacity=fo; g('hl').style.transform=`scale(${1+0.02*cl(b/6)+pulse*.6})`;
 const ps=out(cl(b/.45)), s0=1.1+(1-1.1)*ps;
 g('pinkC').style.transform=`scale(${s0*(1+pulse*.5)})`; const bp=out(cl((b-2)/.45)), bo=b<2?0:Math.min(1,bp*6), bs=1.18+(1-1.18)*bp;
 g('blueC').style.opacity=bo; g('blueC').style.transform=`scale(${bo?bs*(1+pulse*.5):1})`; g('blueD').style.opacity=(b<2?.7:0)*fo; g('blueD').style.transform=`rotate(${b*9}deg)`;
 g('grp').style.opacity=fo;
 lab('wSaju',fo,s0*(1+pulse*.5)); lab('wStar',(b<2?0:bo)*fo,bo?bs:1);
 const ss=out(cl((b-3)/.4)); lab('wSame',(b<3?0:Math.min(1,ss*6))*fo,b<3?1:1.3+(1-1.3)*ss);
@@EXJS@@
 // 장면 3: 순위(박 18.2~27)
 const rf=1-cl((b-25.6)/.6); g('rk').style.opacity=cl((b-18)/.5)*rf;
 for(let i=0;i<12;i++){const t0=18.4+(11-i)*.5, q=out(cl((b-t0)/.45)); const el=g('bar'+i); el.style.opacity=q*rf; el.style.width=(WID[i]*q)+'px'; if(i===0){el.classList.add('top1'); el.style.transform=`scaleY(${1+(b>24.2&&b<25.6?pulse*1.6:0)})`}}
 // 장면 4: 마무리 — 댓글 한 줄(박 26~29) 뒤 팔로우 + 홈페이지(박 29~36)
 const cA=1-cl((b-28.6)/.5); g('c1').style.opacity=cl((b-26)/.4)*cA; g('c2').style.opacity=cl((b-26.6)/.4)*cA; g('c3').style.opacity=cl((b-27.4)/.4)*cA;
 g('f1').style.opacity=cl((b-29.2)/.4); g('f2').style.opacity=cl((b-29.9)/.4); g('fcard').style.opacity=cl((b-30.6)/.5); g('f3').style.opacity=cl((b-31)/.4); g('f4').style.opacity=cl((b-31.6)/.4); g('f5').style.opacity=cl((b-32.4)/.4);
 const bq=out(cl((b-33.2)/.5)); g('fbtn').style.opacity=bq; g('fbtn').style.transform=`scale(${.8+.2*bq+(b>34?pulse*1.2:0)})`;
}
seek(0);
</script>"""
    for _ in range(2):
        for k, v in {"@@FONTS@@": K.css("gm"), "@@BG@@": os.path.join(AS, "derived", "bg_cosmos.jpg"), "@@CHART@@": os.path.join(AS, "chart.png"), "@@SUN@@": os.path.join(AS, "derived", "sun.png"), "@@MOON@@": os.path.join(AS, "derived", "moon.png"),
                 "@@PINK@@": PINK, "@@BLUE@@": BLUE, "@@GOLD@@": GOLD, "@@BEAT@@": repr(beat), "@@BF@@": BF.html("reel", ai=True), "@@BFCSS@@": BF.css(), "@@XFS@@": str(TE.explain_layout("reel")["bubble_fs"]), "@@EXHTML@@": ex_blocks()[0], "@@CTAHTML@@": cta_blocks(), "@@EXJS@@": ex_blocks()[1], "@@BARS@@": bars, "@@P1HTML@@": p1_html, "@@RKHTML@@": rk_html, "@@WIDS@@": str(WIDS), "@@CHIPS@@": chips, "@@JW@@": os.path.join(AS, "derived", "jw_gesture.png"), "@@VALS@@": str([v for _, v in RANK])}.items(): h = h.replace(k, v)
    return h
async def cover(hp, beat, out):
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 1080, "height": 1920}); await pg.goto("file://" + hp); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(600)
        await pg.evaluate("document.body.classList.add('cover')"); await pg.evaluate(f"seek({4.2 * beat * 1000})"); await pg.wait_for_timeout(300); await pg.screenshot(path=out, type="jpeg", quality=92); await b.close()
if __name__ == "__main__":
    mi = MP.choose("data", "litho-star6"); beat = 60.0 / mi["bpm"]; nb = 36; total = nb * beat
    hp = "/tmp/litho_star.html"; open(hp, "w", encoding="utf-8").write(html(beat))
    outp = os.path.join(R, "2026-motion", "litho_star6.mp4"); secs = HM.render_html(hp, outp, total)
    MP.mux(outp, [6 * beat, 12 * beat, 8 * beat, 3 * beat, 7 * beat], mi, 103)
    asyncio.run(cover(hp, beat, os.path.join(R, "2026-motion", "litho_star6_cover.jpg")))
    print("음악:", mi["style"], mi["bpm"], mi["key"], "| 박자", round(beat, 3), "초 | 길이", round(secs, 1), "초")
