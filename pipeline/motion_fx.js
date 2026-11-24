

// 글꼴은 이 파일이 페이지에 직접 붙인다(페이지마다 @font-face 를 다시 적지 않는다). 이름: PL 페이퍼로지 · PR 프리텐다드 · BZ 배찌체 · DK 동해독도 · HC 개구 · HP 나눔펜 · DG 동글
(function(){if(typeof document==='undefined'||!document.currentScript||typeof FontFace==='undefined')return;const base=document.currentScript.src.replace(/[^/]*$/,'')+'fonts/';
 // 11/24 대표 '페이퍼로지 실제 적용, 다른 기본 폰트 절대 금지'(K-291): PL 은 굵기별 파일을 따로 붙인다(700 Bold · 800 ExtraBold · 900 Black). 못 읽은 글꼴은 조용히 넘기지 않고 window.__zsFontFail 에 적는다 → html_motion 관문이 막는다
 const L=[['PL','Paperlogy-7Bold.ttf','700'],['PL','Paperlogy-8ExtraBold.ttf','800'],['PL','Paperlogy-9Black.ttf','900'],['PR','PRETENDARD-EXTRABOLD.OTF','800'],['BZ','Bazzi.ttf','400'],['DK','EastSeaDokdo-Regular.ttf','400'],['HC','Gaegu-Bold.ttf','700'],['HP','NanumPenScript-Regular.ttf','400'],['DG','Dongle-Bold.ttf','700']];
 window.__zsFontFail=[];const have=new Set([...document.fonts].map(f=>f.family.replace(/['"]/g,'')+'|'+f.weight));
 window.__zsFonts=Promise.all(L.filter(([k,,w])=>!have.has(k+'|'+w)).map(([k,f,w])=>new FontFace(k,`url(${base+f})`,{weight:w}).load().then(ff=>document.fonts.add(ff)).catch(()=>window.__zsFontFail.push(k+' '+w+' '+base+f))))})();
// 11/11 대표 13:09 "곡선·그래프·선 같은 구성 요소가 얇은 느낌… 볼륨감 있게": 모든 선 두께를 한 곳에서 키운다.
// 선 굵기 = 적은 값 × 1.7(20px 넘는 굵은 선은 × 1.15), 가장 가는 선도 6px. 끝·꺾임은 둥글게. 페이지에서 window.ZS_VOL 로 바꿀 수 있다.
(function(){const P=typeof CanvasRenderingContext2D!=='undefined'&&CanvasRenderingContext2D.prototype;if(!P||P.__zsVol)return;const d=Object.getOwnPropertyDescriptor(P,'lineWidth');if(!d||!d.set)return;P.__zsVol=1;
 Object.defineProperty(P,'lineWidth',{configurable:true,get(){return d.get.call(this)},set(v){const k=(typeof window!=='undefined'&&window.ZS_VOL)||1.7;
  const w=v<=0?v:(v>=20?v*Math.min(k,1.15):Math.max(v*k,6));d.set.call(this,w);try{this.lineJoin='round'}catch(e){}}})})();
/* 모션 기법 모음(화려한 쪽, K-186 대표 11/10 "화려하게" · 22:04 "모션이 얼마나 많은데")
   광고·릴스 HTML 이 <script src=".../pipeline/motion_fx.js"> 로 불러 쓴다. 모든 함수는 시간 t 만으로 그린다(seek 규칙).
   편마다 다른 조합을 쓴다: HTML 에 window.FX=[기법 이름…] 을 적으면 html_motion.py 가 앞 3편과 겹침을 잰다.
   이름 목록(아래 FX_LIST)과 v3 에서 쓴 것: 박자글자·배경뒤집기·글자띠·원와이프·도형격자변형·입자글자·UI시연·방사형 (ads/2611_dapjang/moneymonth_v3/ad.html) */
(function(){
const cl=(x,a=0,b=1)=>Math.min(b,Math.max(a,x)), mix=(a,b,p)=>a+(b-a)*p;
const ease=x=>{x=cl(x);return 1-Math.pow(1-x,3)}, eio=x=>{x=cl(x);return x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2};
function sp(t,k=14,z=.72){if(t<=0)return 0;const wd=k*Math.sqrt(1-z*z);return 1-Math.exp(-z*k*t)*(Math.cos(wd*t)+(z*k/wd)*Math.sin(wd*t))}
const H=i=>{const x=Math.sin(i*127.1+311.7)*43758.5453;return x-Math.floor(x)};
const FX={cl,mix,ease,eio,sp,H};
FX.LIST={
 '박자글자':'큰 글자가 박자마다 바뀜(v3)', '배경뒤집기':'박자마다 판 색 반전(v3)', '글자띠':'기울어진 글자 띠가 반대로 흐름(v3)',
 '원와이프':'원이 커지며 다음 판으로(v3)', '도형격자변형':'원→네모→십자 격자, 핵심만 커짐(v3)', '입자글자':'입자가 모여 글자(v3)',
 'UI시연':'입력·커서·누름·결과(v3)', '방사형':'회전 방사형 끝장면(v3)',
 '글자겹쳐쌓기':'같은 낱말이 외곽선으로 반 박마다 쌓이고 마지막만 채움', '슬롯롤링':'낱말이 세로로 굴러가다 하나에 멈춤',
 '점파동':'점 격자가 한 점에서 물결, 두 점을 선으로 잇기', '궤도링':'진행 링이 차고 점들이 궤도를 돎',
 '카드뒤집기':'카드가 3D로 뒤집혀 뒷면이 나옴', '궤적선':'점이 곡선을 따라 날며 꼬리를 남김'};
// 글자겹쳐쌓기: n줄, 반 박(step)마다 한 줄, 마지막 줄만 채움
FX.stack=(g,t,t0,{word,x=FX.cx,y0=480,dy=150,n=6,step=.25,font='900 170px PL',color='#FF4F9A',fill='#FF4F9A'})=>{
 g.save();g.font=font;g.textAlign='center';g.textBaseline='middle';g.lineWidth=4;g.lineJoin='round';
 for(let i=0;i<n;i++){const a=sp(t-t0-i*step,16,.65);if(a<=0)continue;const y=y0+i*dy;
  g.globalAlpha=cl(a*3);g.save();g.translate(x,y+(1-a)*60);g.scale(1,cl(a,0,1.2));
  if(i==n-1){g.fillStyle=fill;g.fillText(word,0,0)}else{g.strokeStyle=color;g.strokeText(word,0,0)}g.restore()}
 g.restore()};
// 슬롯롤링: 창(x,y,w,h) 안에서 words 가 굴러가다 stop 시각에 target 에서 멈춤
FX.slot=(g,t,t0,t1,{words,target,x=FX.cx,y=FX.cy,h=260,font='900 220px PL',color='#171717',loops=3})=>{
 const n=words.length, ti=words.indexOf(target), total=loops*n+ti, p=t>=t1?1:eio(cl((t-t0)/(t1-t0)));
 let pos=p*total; if(t>=t1){pos=total-Math.sin((t-t1)*18)*Math.exp(-(t-t1)*7)*.15}
 g.save();g.beginPath();g.rect(0,y-h/2,1080,h);g.clip();g.font=font;g.textAlign='center';g.textBaseline='middle';g.fillStyle=color;
 for(let k=Math.floor(pos)-1;k<=Math.floor(pos)+1;k++){const w=words[((k%n)+n)%n];g.fillText(w,x,y+(k-pos)*h)}g.restore()};
// 점파동: 격자 점, 중심들에서 물결
FX.dotwave=(g,t,t0,{cols=13,rows=20,x0=90,y0=420,gap=75,centers=[[FX.cx,FX.cy]],color='rgba(255,255,255,.55)',r0=5,amp=9})=>{
 g.save();g.fillStyle=color;const T=t-t0;
 for(let j=0;j<rows;j++)for(let i=0;i<cols;i++){const x=x0+i*gap,y=y0+j*gap;let w=0;
  centers.forEach(([cx,cy],k)=>{const d=Math.hypot(x-cx,y-cy),f=T*900-k*450-d;if(f>0)w+=Math.max(0,Math.sin(f/90))*Math.exp(-f/900)});
  const a=sp(T-(i+j)*.012,14,.8);g.beginPath();g.arc(x,y,Math.max(0,(r0+amp*w)*a),0,7);g.fill()}g.restore()};
// 궤도링: 진행 비율 p(0~1)
FX.ring=(g,t,{x=FX.cx,y=900,r=300,p=0,color='#FF4F9A',track='rgba(0,0,0,.08)',dots=10})=>{
 g.save();g.lineCap='round';g.lineWidth=34;g.strokeStyle=track;g.beginPath();g.arc(x,y,r,0,7);g.stroke();
 g.strokeStyle=color;g.beginPath();g.arc(x,y,r,-Math.PI/2,-Math.PI/2+6.283*p);g.stroke();
 for(let i=0;i<dots;i++){const a=t*(1.2+i*.08)+i*6.283/dots, rr=r+70+(i%3)*28;g.fillStyle=i%2?color:'#171717';
  g.beginPath();g.arc(x+Math.cos(a)*rr,y+Math.sin(a)*rr,6+(i%3)*3,0,7);g.fill()}g.restore()};
// 카드뒤집기: DOM 요소 앞(front)·뒤(back), t0 부터 dur 동안 180도
FX.flip=(front,back,t,t0,dur=.6)=>{const p=eio((t-t0)/dur),deg=p*180,s=1+Math.sin(p*Math.PI)*.08;
 front.style.transform=`perspective(1800px) rotateY(${deg}deg) scale(${s})`;back.style.transform=`perspective(1800px) rotateY(${deg-180}deg) scale(${s})`;
 front.style.visibility=deg<90?'visible':'hidden';back.style.visibility=deg>=90?'visible':'hidden'};
// 궤적선: 곡선 f(u)->[x,y], 점이 u=0..1 로 날고 꼬리 n개
FX.trail=(g,t,t0,dur,f,{color='#FF4F9A',n=26,r=16,loop=false})=>{let u=(t-t0)/dur;if(u<0)return;if(loop)u=u%1;else u=cl(u);
 g.save();for(let k=n;k>=0;k--){const v=u-k*.012;if(v<0)continue;const [x,y]=f(eio(v));g.globalAlpha=(1-k/n)*.9;g.fillStyle=color;
  g.beginPath();g.arc(x,y,r*(1-k/n*.7),0,7);g.fill()}g.restore()};

// ── 11/11 대표 화면 녹화(AI 신사장 '클로드가 만든 330만뷰 모션 그래픽', 106초) 기법 전부 ── 번호는 docs 제작 가이드라인 15절 표
FX.LIST=Object.assign(FX.LIST,{
 '로딩선열기':'#1 스피너가 돌다 가로선으로 펴짐','점착지':'#2 점이 떨어져 찌그러졌다 마침표 자리에 앉음','픽셀블록':'#3 네모 블록이 떨어져 줄을 채움',
 '사전정의':'#5 큰 낱말 + 사전 뜻 한 줄이 타자처럼','도형변신':'#7·35 원·네모·십자·별·세모를 점으로 이어 변신(+위성)','입자소용돌이':'#8 입자가 고리로 돌다 모임',
 '점3D':'#9·37 점으로 된 구·도넛·물결면이 돎','방사선터널':'#10 가운데서 선이 뻗는 터널','버튼상태전환':'#12 단추 글자·색이 상태대로 바뀜(전송 중→완료)',
 '칩줄세우기':'#13 태그 칩이 하나씩 붙음','손글씨주석':'#14·21 손글씨 화살표·메모가 그려짐','공튀기기':'#14 찌그러짐·늘어남 있는 공',
 '글자스태거':'#15 글자가 한 자씩 기울며 들어옴','낱말이뜻대로':'#16 BOUNCE는 튀고 STRETCH는 늘고 SPIN은 돎','이징그래프':'#17 직선 대 부드러운 곡선 그래프',
 '모양변신':'#22 단추가 원→카드로 커짐','슬라이더':'#23 재생·볼륨 막대 끌기','토글':'#23 스위치','탭전환':'#23 일·주·월 탭','명령창':'#23 검색창에 치면 목록이 걸러짐',
 '토스트':'#23 체크와 함께 뜨는 알림 줄','위아래비교':'#24 위·아래 두 판 비교','낱말블록교체':'#25 꽉 찬 색 블록에 낱말이 박자마다 바뀜','숫자폭주':'#26 숫자가 1→999+로 폭주, 뒤로 글자 줄이 날아감',
 '물결링':'#27 빛점에서 동심원이 퍼짐','허브연결':'#29 가운데 아이콘에 노드가 선으로 붙고 숫자가 셈','로고조립':'#31 조각이 날아와 로고가 됨',
 '별폭발':'#32 점이 선 다발로 터지고 둘레 글자가 돎','글자늘이기':'#33 자간이 쫙 벌어지며 화면을 가로지름','이징비교줄':'#34 여섯 줄 점이 서로 다른 속도로 A→B',
 '트루쳇무늬':'#36 반원 타일 무늬가 깔리고 색이 휩쓺','회전별표':'#39 별표가 돌며 로고 옆에 붙음','영상벽':'#40 카드 벽이 옆으로 흐름'});
const ez={lin:x=>x,inq:x=>x*x*x,outq:x=>1-Math.pow(1-x,3),io:x=>x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2,back:x=>{const c=1.7;return 1+(c+1)*Math.pow(x-1,3)+c*Math.pow(x-1,2)},el:x=>x<=0?0:x>=1?1:Math.pow(2,-10*x)*Math.sin((x*10-.75)*2.094)+1};
FX.ez=ez;
FX.loaderLine=(g,t,t0,{x=FX.cx,y=FX.cy,w=800,color='#fff'})=>{const T=t-t0;if(T<0)return;g.save();g.strokeStyle=color;g.lineWidth=8;g.lineCap='round';
 if(T<.7){g.beginPath();g.arc(x,y,40,T*9,T*9+4.2);g.stroke()}else{const p=eio((T-.7)/.5);g.beginPath();g.moveTo(x-w/2*p,y);g.lineTo(x+w/2*p,y);g.stroke()}g.restore()};
FX.dotLand=(g,t,t0,{x=900,y=1000,r=34,color='#FF7A1A',h=500})=>{const T=t-t0;if(T<0)return;let yy,sx=1,sy=1;
 if(T<.35){const p=T/.35;yy=y-h*(1-p*p)}else{const u=T-.35,b=Math.abs(Math.sin(u*14))*Math.exp(-u*5)*120;yy=y-b;const sq=Math.exp(-u*6)*Math.cos(u*28)*.35;sx=1+sq;sy=1-sq}
 g.save();g.fillStyle=color;g.translate(x,yy+r);g.scale(sx,sy);g.beginPath();g.arc(0,-r,r,0,7);g.fill();g.restore()};
FX.pixelBlocks=(g,t,t0,{x=90,y=700,cols=9,rows=5,s=100,color='#111'})=>{for(let j=0;j<rows;j++)for(let i=0;i<cols;i++){const k=j*cols+i,d=t0+H(k)*.8,p=cl((t-d)/.35);if(p<=0)continue;
 const yy=mix(y+j*s-600,y+j*s,ez.outq(p));g.fillStyle=color;g.globalAlpha=H(k+5)>.25?1:.4;g.fillRect(x+i*s+4,yy+4,s-8,s-8)}g.globalAlpha=1};
FX.dict=(g,t,t0,{word,sub,x=FX.cx,y=900,color='#111',font='900 220px PL',sfont='italic 400 48px SR'})=>{const a=sp(t-t0,14,.7);g.save();g.fillStyle=color;g.textAlign='center';g.textBaseline='middle';
 g.font=font;g.globalAlpha=cl((t-t0)/.1);g.fillText(word,x,y+(1-a)*80);const n=Math.floor(cl((t-t0-.4)/.8)*sub.length);g.font=sfont;g.fillText(sub.slice(0,n),x,y+170);g.restore()};
function shapePts(kind,s,N=72){const o=[];for(let i=0;i<N;i++){const u=i/N,a=-Math.PI/2+u*6.283;let r=s;
 if(kind=='square'){const c=Math.cos(a),q=Math.sin(a);r=s/Math.max(Math.abs(c),Math.abs(q))*.78}
 else if(kind=='tri'){const k=Math.floor(u*3),f=u*3-k,A=[0,1,2].map(m=>[Math.cos(-Math.PI/2+m*2.094)*s,Math.sin(-Math.PI/2+m*2.094)*s]),P=A[k],Q=A[(k+1)%3];o.push([mix(P[0],Q[0],f),mix(P[1],Q[1],f)]);continue}
 else if(kind=='star'){const m=(u*10)%2,f=m<1?m:2-m;r=s*mix(1,.45,f)}
 else if(kind=='plus'){const c=Math.abs(Math.cos(a)),q=Math.abs(Math.sin(a));const w=.34;r=s*Math.min(1/Math.max(c,1e-3),w/Math.max(q,1e-3))*(c>q?1:0)+s*Math.min(1/Math.max(q,1e-3),w/Math.max(c,1e-3))*(q>=c?1:0);r=Math.min(r,s*1.05)}
 o.push([Math.cos(a)*r,Math.sin(a)*r])}return o}
FX.shapeMorph=(g,x,y,s,seq,p,{color='#F5EFE6',sat=0,t=0,satColor='#fff'}={})=>{const k=Math.min(seq.length-2,Math.floor(p)),f=ez.io(cl(p-k)),A=shapePts(seq[k],s),B=shapePts(seq[k+1],s);
 g.fillStyle=color;g.beginPath();A.forEach((q,i)=>{const X=x+mix(q[0],B[i][0],f),Y=y+mix(q[1],B[i][1],f);i?g.lineTo(X,Y):g.moveTo(X,Y)});g.closePath();g.fill();
 for(let i=0;i<sat;i++){const a=t*.8+i*6.283/sat;g.fillStyle=satColor;g.beginPath();g.arc(x+Math.cos(a)*s*1.7,y+Math.sin(a)*s*1.7,9,0,7);g.fill()}};
FX.vortex=(g,t,t0,{n=1500,x=FX.cx,y=900,R=330,target=null,tGather=1.2,color='rgba(255,240,220,.85)'})=>{const T=t-t0;if(T<0)return;g.fillStyle=color;
 for(let i=0;i<n;i++){const h=H(i),h2=H(i+71),a=h*6.283+T*(1.5+h2),rr=R*(.75+.35*h2)+Math.sin(T*3+i)*12;let px=x+Math.cos(a)*rr,py=y+Math.sin(a)*rr*.9;
  if(target){const q=target[i%target.length],p=ez.io(cl((T-tGather-h*.4)/.8));px=mix(px,q[0],p);py=mix(py,q[1],p)}g.fillRect(px,py,3,3)}};
FX.dot3D=(g,t,{kind='sphere',x=FX.cx,y=900,R=330,rot=0,tilt=.5,n=900,color='#fff'})=>{const ps=[];
 for(let i=0;i<n;i++){let X,Y,Z;const u=H(i)*6.283,v=H(i+9);
  if(kind=='sphere'){const ph=Math.acos(2*v-1);X=Math.sin(ph)*Math.cos(u);Y=Math.cos(ph);Z=Math.sin(ph)*Math.sin(u)}
  else if(kind=='torus'){const w=v*6.283;X=(1+.38*Math.cos(w))*Math.cos(u)*.72;Z=(1+.38*Math.cos(w))*Math.sin(u)*.72;Y=.38*Math.sin(w)*.72}
  else{const gx=(i%30)/29*2-1,gz=Math.floor(i/30)/29*2-1;X=gx;Z=gz;Y=Math.sin(gx*3+rot*2)*Math.cos(gz*3)*.25}
  const c=Math.cos(rot),s=Math.sin(rot);[X,Z]=[X*c-Z*s,X*s+Z*c];const ct=Math.cos(tilt),st=Math.sin(tilt);[Y,Z]=[Y*ct-Z*st,Y*st+Z*ct];ps.push([X,Y,Z])}
 ps.sort((a,b)=>a[2]-b[2]);ps.forEach(([X,Y,Z])=>{const k=1/(1.8-Z*.6);g.globalAlpha=cl(.25+(Z+1)*.38);g.fillStyle=color;g.beginPath();g.arc(x+X*R*k,y+Y*R*k,2.2*k*1.4,0,7);g.fill()});g.globalAlpha=1};
FX.tunnel=(g,t,{x=FX.cx,y=900,n=90,color='rgba(255,255,255,.55)',r0=110})=>{g.save();g.strokeStyle=color;g.lineWidth=2;for(let i=0;i<n;i++){const a=i*6.283/n+t*.15,L=900+H(i)*500,ph=((t*1.4+H(i+3))%1);
 const r1=r0+ph*L*.3,r2=r1+120+H(i+5)*220;g.beginPath();g.moveTo(x+Math.cos(a)*r1,y+Math.sin(a)*r1);g.lineTo(x+Math.cos(a)*r2,y+Math.sin(a)*r2);g.stroke()}
 g.fillStyle='#000';g.beginPath();g.arc(x,y,r0,0,7);g.fill();g.restore()};
FX.stateBtn=(g,t,{x=FX.cx,y=1300,w=640,h=130,states,times,colors,font='900 54px PL'})=>{let k=0;times.forEach((tt,i)=>{if(t>=tt)k=i});const press=times.some(tt=>t>=tt&&t<tt+.12)?.94:1;
 g.save();g.translate(x,y);g.scale(press,press);g.fillStyle=colors[k][0];g.beginPath();g.roundRect(-w/2,-h/2,w,h,h/2);g.fill();g.fillStyle=colors[k][1];g.font=font;g.textAlign='center';g.textBaseline='middle';g.fillText(states[k],0,3);g.restore()};
FX.chips=(g,t,t0,{labels,x=null,y=1200,gap=18,font='800 36px PR',bg='#fff',fg='#111',align='center'})=>{g.save();g.font=font;const fs=parseFloat(font.match(/(\d+)px/)[1]),ch=fs*1.6,A=FX.area(),x0=x==null?A.x0:x;
 // 11/11: 줄마다 가운데(안전 영역 가운데 F.cx). 먼저 줄을 나눈 뒤 줄 폭만큼 민다. 돌려줌: 칩마다 [가운데x, 가운데y]
 const rows=[[]];let cx=x0;labels.forEach((l,i)=>{const w=g.measureText(l).width+fs*1.3;if(cx+w>A.x1&&rows[rows.length-1].length){rows.push([]);cx=x0}rows[rows.length-1].push([l,i,w]);cx+=w+gap});
 const pos=[];rows.forEach((r,ri)=>{const rw=r.reduce((a,[, ,w])=>a+w,0)+gap*(r.length-1);let px=align=='center'?FX.cx-rw/2:x0;const py=y+ri*(ch+gap);
  r.forEach(([l,i,w])=>{pos[i]=[px+w/2,py+ch/2];const s=sp(t-t0-i*.12,16,.55);if(s>0){g.save();g.translate(px+w/2,py+ch/2);g.scale(s,s);g.fillStyle=bg;g.beginPath();g.roundRect(-w/2,-ch/2,w,ch,ch/2);g.fill();g.fillStyle=fg;g.textAlign='center';g.textBaseline='middle';g.fillText(l,0,2);g.restore()}px+=w+gap})});g.restore();return pos};
FX.annot=(g,t,t0,{from,to,text,color='#E53935',font='72px BZ'})=>{const p=eio((t-t0)/.5);if(p<=0)return;g.save();
 // 11/11 대표 "나 여기 표시선이랑 텍스트도 겹쳐": 글은 from 을 가운데로 놓고, 선은 글 상자 가장자리 + 20px 에서 시작한다(글 위로 선이 지나가지 않음)
 g.font=font;const fs=parseFloat(font.match(/(\d+)px/)[1]),w=g.measureText(text).width,hx=w/2+20,hy=fs*.6+20,dx=to[0]-from[0],dy=to[1]-from[1],L=Math.hypot(dx,dy)||1,
  k=Math.min(Math.abs(dx)>1e-3?hx/Math.abs(dx):1e9,Math.abs(dy)>1e-3?hy/Math.abs(dy):1e9),st=[from[0]+dx*k,from[1]+dy*k];
 g.strokeStyle=color;g.lineWidth=5;g.lineCap='round';const mx=(st[0]+to[0])/2+30,my=(st[1]+to[1])/2-30,N=20;g.beginPath();for(let i=0;i<=N*p;i++){const u=i/N,X=(1-u)*(1-u)*st[0]+2*u*(1-u)*mx+u*u*to[0],Y=(1-u)*(1-u)*st[1]+2*u*(1-u)*my+u*u*to[1];i?g.lineTo(X,Y):g.moveTo(X,Y)}g.stroke();
 if(p>.95){const a=Math.atan2(to[1]-my,to[0]-mx);g.beginPath();g.moveTo(to[0],to[1]);g.lineTo(to[0]-26*Math.cos(a-.5),to[1]-26*Math.sin(a-.5));g.moveTo(to[0],to[1]);g.lineTo(to[0]-26*Math.cos(a+.5),to[1]-26*Math.sin(a+.5));g.stroke()}
 g.fillStyle=color;g.textAlign='center';g.textBaseline='middle';g.globalAlpha=cl((t-t0-.3)/.2);g.fillText(text,from[0],from[1]);g.restore()};
FX.ball=(g,t,t0,{x0=150,x1=930,yb=1250,r=46,color='#2F6BFF',hops=3,dur=2})=>{const T=cl((t-t0)/dur);if(t<t0)return;const x=mix(x0,x1,ez.io(T)),ph=(T*hops)%1,h=420*Math.exp(-T*1.2);
 const y=yb-r-h*4*ph*(1-ph),vy=Math.abs(1-2*ph),near=ph<.08||ph>.92;const sx=near?1.35:1-vy*.0+(.15*(1-vy)),sy=near?.68:1+.18*vy;
 g.save();g.strokeStyle='rgba(0,0,0,.25)';g.lineWidth=3;g.beginPath();g.moveTo(80,yb);g.lineTo(1000,yb);g.stroke();g.translate(x,near?yb-r*sy:y);g.scale(sx,sy);g.fillStyle=color;g.beginPath();g.arc(0,0,r,0,7);g.fill();g.restore()};
FX.stagger=(g,t,t0,{word,x=FX.cx,y=900,font='900 170px PL',color='#111',step=.07})=>{g.save();g.font=font;g.textBaseline='middle';const W=g.measureText(word).width;let cx=x-W/2;
 [...word].forEach((ch,i)=>{const w=g.measureText(ch).width,a=sp(t-t0-i*step,13,.6);if(a>0){g.save();g.translate(cx+w/2,y+(1-a)*140);g.rotate((1-a)*-.5);g.globalAlpha=cl(a*2);g.fillStyle=color;g.textAlign='center';g.fillText(ch,0,0);g.restore()}cx+=w});g.restore()};
FX.verb=(g,t,t0,{word,act,x=FX.cx,y=FX.cy,font='900 210px PL',color='#fff'})=>{const T=t-t0;if(T<0)return;g.save();g.font=font;g.textAlign='center';g.textBaseline='middle';g.fillStyle=color;g.translate(x,y);
 if(act=='bounce'){g.translate(0,-Math.abs(Math.sin(T*7))*Math.exp(-T*2)*220);const q=Math.exp(-T*3)*.25*Math.abs(Math.cos(T*7));g.scale(1+q,1-q)}
 else if(act=='stretch'){const s=1+Math.sin(cl(T/.6)*Math.PI)*.5+(sp(T-.6,12,.4)-1)*.3;g.scale(s,1/Math.sqrt(s))}
 else if(act=='spin'){g.rotate(ez.back(cl(T/.9))*Math.PI*2.5)}
 g.fillText(word,0,0);g.restore()};
FX.easeGraph=(g,t,t0,{x=140,y=1250,w=800,h=560,c1='#E53935',c2='#2F6BFF'})=>{const p=cl((t-t0)/1.2);g.save();g.strokeStyle='rgba(0,0,0,.3)';g.lineWidth=3;g.beginPath();g.moveTo(x,y-h);g.lineTo(x,y);g.lineTo(x+w,y);g.stroke();
 [[c1,ez.lin],[c2,ez.io]].forEach(([c,f],k)=>{if(k==1&&t<t0+.6)return;const q=k?cl((t-t0-.6)/1.2):p;g.strokeStyle=c;g.lineWidth=7;g.beginPath();for(let i=0;i<=60*q;i++){const u=i/60;i?g.lineTo(x+u*w,y-f(u)*h):g.moveTo(x,y)}g.stroke();
  g.fillStyle=c;g.beginPath();g.arc(x+q*w,y-f(q)*h,14,0,7);g.fill()});g.restore()};
FX.morphBox=(g,t,t0,dur,A,B,{x=FX.cx,y=FX.cy,color='#111'})=>{const p=sp(t-t0,9,.8),pp=cl(p);const w=mix(A[0],B[0],p),h=mix(A[1],B[1],p),r=mix(A[2],B[2],pp);g.fillStyle=color;g.beginPath();g.roundRect(x-w/2,y-h/2,w,h,Math.min(r,w/2,h/2));g.fill()};
FX.slider=(g,{x=190,y=FX.cy,w=700,p=.3,fg='#fff',bg='rgba(255,255,255,.25)',knob=true})=>{g.save();g.lineCap='round';g.lineWidth=14;g.strokeStyle=bg;g.beginPath();g.moveTo(x,y);g.lineTo(x+w,y);g.stroke();
 g.strokeStyle=fg;g.beginPath();g.moveTo(x,y);g.lineTo(x+w*p,y);g.stroke();if(knob){g.fillStyle=fg;g.beginPath();g.arc(x+w*p,y,22,0,7);g.fill()}g.restore()};
FX.toggle=(g,{x=FX.cx,y=FX.cy,p=0,on='#111',off='#ccc'})=>{const w=260,h=140;g.save();g.fillStyle=p>.5?on:off;g.beginPath();g.roundRect(x-w/2,y-h/2,w,h,h/2);g.fill();
 g.fillStyle='#fff';g.beginPath();g.arc(mix(x-w/2+h/2,x+w/2-h/2,ez.back(cl(p))),y,h/2-12,0,7);g.fill();g.restore()};
FX.tabs=(g,{x=FX.cx,y=FX.cy,labels=['일','주','월'],p=0,font='800 44px PR',w=760})=>{const n=labels.length,cw=w/n;g.save();g.fillStyle='#fff';g.beginPath();g.roundRect(x-w/2,y-55,w,110,55);g.fill();
 g.fillStyle='#111';g.beginPath();g.roundRect(x-w/2+p*cw+8,y-47,cw-16,94,47);g.fill();g.font=font;g.textAlign='center';g.textBaseline='middle';
 labels.forEach((l,i)=>{g.fillStyle=Math.abs(p-i)<.5?'#fff':'#888';g.fillText(l,x-w/2+cw*(i+.5),y+2)});g.restore()};
FX.palette=(g,t,t0,{x=140,y=700,w=800,query,items,font='800 44px PR'})=>{const n=Math.floor(cl((t-t0)/.9)*query.length),q=query.slice(0,n);const vis=items.filter(s=>s.includes(q));
 g.save();g.fillStyle='#fff';g.beginPath();g.roundRect(x,y,w,140+vis.length*96,32);g.fill();g.fillStyle='#111';g.font=font;g.textBaseline='middle';g.fillText('⌕  '+q+((Math.floor(t*4)%2)?'|':''),x+40,y+70);
 vis.forEach((s,i)=>{g.fillStyle=i==0?'#F2F2F2':'#fff';g.beginPath();g.roundRect(x+20,y+130+i*96,w-40,84,18);g.fill();g.fillStyle='#333';g.fillText(s,x+50,y+172+i*96)});g.restore()};
FX.toast=(g,t,t0,{text,x=FX.cx,y=1350,font='800 46px PR',color='#111'})=>{const a=sp(t-t0,14,.65);if(a<=0)return;g.save();g.font=font;const w=g.measureText(text).width+150;g.translate(x,y+(1-a)*80);g.globalAlpha=cl(a*2);
 g.fillStyle=color;g.beginPath();g.roundRect(-w/2,-55,w,110,55);g.fill();g.fillStyle='#3DDC84';g.beginPath();g.arc(-w/2+60,0,24,0,7);g.fill();g.strokeStyle='#fff';g.lineWidth=6;g.beginPath();g.moveTo(-w/2+48,0);g.lineTo(-w/2+57,10);g.lineTo(-w/2+73,-10);g.stroke();
 g.fillStyle='#fff';g.textBaseline='middle';g.fillText(text,-w/2+100,2);g.restore()};
FX.split=(g,t,{top,bottom,y=FX.cy,color='#fff',font='800 40px PR'})=>{g.save();g.strokeStyle=color;g.lineWidth=4;g.beginPath();g.moveTo(0,y);g.lineTo(1080*cl(t),y);g.stroke();g.fillStyle=color;g.font=font;g.fillText(top,90,y-30);g.fillText(bottom,90,y+60);g.restore()};
FX.wordBlocks=(g,t,t0,{words,colors,step=.5,y=0,h=1920,font='900 230px PL',fg='#fff'})=>{const k=Math.max(0,Math.min(words.length-1,Math.floor((t-t0)/step)));const a=sp(t-t0-k*step,16,.55);
 g.fillStyle=colors[k%colors.length];g.fillRect(0,y,1080,h);g.save();g.fillStyle=fg;g.font=font;{const m=g.measureText(words[k]).width;if(m>FX.aw()){const px=parseFloat(font.match(/(\d+)px/)[1])*FX.aw()/m;g.font=font.replace(/\d+px/,Math.floor(px)+'px')}}g.textAlign='center';g.textBaseline='middle';g.translate(540,y+h/2);g.scale(mix(1.25,1,a),mix(1.25,1,a));g.fillText(words[k],0,0);g.restore()};
FX.counterRush=(g,t,t0,{to=999,dur=1.6,x=FX.cx,y=900,font='900 230px PL',color='#fff',plus='+',streak=['your agent','motion','one key','skills']})=>{const T=t-t0;if(T<0)return;
 g.save();g.font='800 30px PR';for(let i=0;i<26;i++){const h=H(i+40),sx=((T*(500+h*900)+h*1400)%1500)-200,sy=500+H(i+90)*900;g.fillStyle=`rgba(255,255,255,${.12+.2*h})`;g.fillText(streak[i%streak.length],1080-sx,sy)}
 const v=Math.round(to*ez.inq(cl(T/dur)));g.font=font;g.textAlign='center';g.textBaseline='middle';g.fillStyle=color;g.fillText(v.toLocaleString()+(T>=dur?plus:''),x,y);g.restore()};
FX.ripples=(g,t,t0,{x=FX.cx,y=900,n=6,color='255,255,255',core='#FF7A1A'})=>{const T=t-t0;if(T<0)return;for(let i=0;i<n;i++){const p=((T*.7+i/n)%1);g.strokeStyle=`rgba(${color},${(1-p)*.6})`;g.lineWidth=4;g.beginPath();g.arc(x,y,40+p*700,0,7);g.stroke()}
 g.fillStyle=core;g.beginPath();g.arc(x,y,30+Math.sin(T*6)*4,0,7);g.fill()};
FX.hub=(g,t,t0,{x=FX.cx,y=920,nodes,R=330,color='#FF7A1A',fg='#fff',font='800 38px PR'})=>{g.save();nodes.forEach((nd,i)=>{const a=-Math.PI/2+i*6.283/nodes.length,nx=x+Math.cos(a)*R,ny=y+Math.sin(a)*R,p=eio((t-t0-.3-i*.15)/.4);if(p<=0)return;
 g.strokeStyle=color;g.globalAlpha=.7;g.lineWidth=4;g.beginPath();g.moveTo(x,y);g.lineTo(mix(x,nx,p),mix(y,ny,p));g.stroke();g.globalAlpha=1;
 if(p>=1){const s=sp(t-t0-.7-i*.15,16,.6);g.save();g.translate(nx,ny);g.scale(s,s);g.fillStyle='#1b1b1b';g.beginPath();g.roundRect(-110,-55,220,110,24);g.fill();g.fillStyle=fg;g.font=font;g.textAlign='center';g.textBaseline='middle';
  g.fillText(nd[0],0,-14);g.fillStyle=color;g.fillText(Math.round(nd[1]*cl((t-t0-.9-i*.15)/.8)).toLocaleString()+(nd[2]||''),0,26);g.restore()}});
 const s=sp(t-t0,14,.6);g.fillStyle=color;g.beginPath();g.roundRect(x-80*s,y-80*s,160*s,160*s,36*s);g.fill();g.restore()};
FX.assemble=(g,t,t0,{pieces,color='#FF7A1A'})=>{pieces.forEach((pc,i)=>{const [x,y,w,h]=pc,a=sp(t-t0-i*.06,12,.7),fx=x+(H(i)-.5)*1400,fy=y+(H(i+3)-.5)*1600;g.save();g.globalAlpha=cl(a*3);g.fillStyle=color;
 g.translate(mix(fx,x,a),mix(fy,y,a));g.rotate((1-a)*(H(i+7)-.5)*4);g.fillRect(-w/2,-h/2,w,h);g.restore()})};
FX.starBurst=(g,t,t0,{x=FX.cx,y=900,n=16,L=260,color='#FF4A3D',ring='',font='800 30px PR'})=>{const T=t-t0;if(T<0)return;const p=sp(T-.2,10,.6);g.save();g.strokeStyle=color;g.lineWidth=10;g.lineCap='round';
 for(let i=0;i<n;i++){const a=i*6.283/n+T*.4;g.beginPath();g.moveTo(x,y);g.lineTo(x+Math.cos(a)*L*p,y+Math.sin(a)*L*p);g.stroke()}g.fillStyle=color;g.beginPath();g.arc(x,y,18,0,7);g.fill();
 if(ring){g.font=font;g.fillStyle=color;const N=ring.length;for(let i=0;i<N;i++){const a=-T*.6+i*6.283/N;g.save();g.translate(x+Math.cos(a)*(L+90),y+Math.sin(a)*(L+90));g.rotate(a+Math.PI/2);g.globalAlpha=cl((T-.6)/.3);g.fillText(ring[i],0,0);g.restore()}}g.restore()};
FX.stretchWord=(g,t,t0,{word,x=FX.cx,y=900,font='900 200px PL',color='#111'})=>{const p=sp(t-t0,8,.8);g.save();g.font=font;g.textBaseline='middle';const n=word.length,ws=[...word].map(c=>g.measureText(c).width),W=ws.reduce((a,b)=>a+b,0),sp2=mix(-10,(1000-W)/(n-1),cl(p));
 let cx=x-(W+sp2*(n-1))/2;g.fillStyle=color;[...word].forEach((c,i)=>{g.fillText(c,cx,y);cx+=ws[i]+sp2});g.restore()};
FX.easeRows=(g,t,t0,{x=200,y=600,w=760,gap=120,dur=1.4,colors=['#111','#2F6BFF','#E53935']})=>{const names=[['직선','lin'],['천천히 시작','inq'],['천천히 멈춤','outq'],['둘 다','io'],['넘쳤다 돌아옴','back'],['통통','el']];
 g.save();g.font='800 34px PR';names.forEach(([nm,k],i)=>{const yy=y+i*gap;g.fillStyle='#666';g.fillText(nm,90,yy-34);g.strokeStyle='rgba(0,0,0,.15)';g.lineWidth=3;g.beginPath();g.moveTo(x,yy);g.lineTo(x+w,yy);g.stroke();
  const p=ez[k](cl((t-t0)/dur));g.fillStyle=colors[i%colors.length];g.beginPath();g.arc(x+w*p,yy,20,0,7);g.fill()});g.restore()};
FX.truchet=(g,t,t0,{cell=90,c1='#111',c2='#fff',c3='#FF4A3D'})=>{const cols=Math.ceil(1080/cell),rows=Math.ceil(1920/cell),sweep=(t-t0)*900;g.save();g.lineWidth=cell*.28;g.lineCap='butt';
 for(let j=0;j<rows;j++)for(let i=0;i<cols;i++){const x=i*cell,y=j*cell,a=sp(t-t0-(i+j)*.015,12,.7);if(a<=0)continue;g.fillStyle=c1;g.fillRect(x,y,cell,cell);g.strokeStyle=(x+y)<sweep?c3:c2;g.globalAlpha=cl(a);
  const f=H(i*97+j)>.5;g.beginPath();if(f){g.arc(x,y,cell/2,0,Math.PI/2);g.moveTo(x+cell,y+cell/2);g.arc(x+cell,y+cell,cell/2,-Math.PI/2,-Math.PI,true)}else{g.arc(x+cell,y,cell/2,Math.PI/2,Math.PI);g.moveTo(x+cell/2,y+cell);g.arc(x,y+cell,cell/2,0,-Math.PI/2,true)}g.stroke()}g.restore()};
FX.asterisk=(g,t,{x=FX.cx,y=900,r=90,color='#111',n=8})=>{g.save();g.translate(x,y);g.rotate(t*1.4);g.strokeStyle=color;g.lineWidth=r*.28;g.lineCap='round';for(let i=0;i<n;i++){g.rotate(Math.PI/n);g.beginPath();g.moveTo(-r,0);g.lineTo(r,0);g.stroke()}g.restore()};
FX.videoWall=(g,t,{rows=3,y=560,h=260,w=340,gap=24,speed=120,cards=[],font='900 56px PL'})=>{g.save();for(let j=0;j<rows;j++){const off=((t*speed*(j%2?-1:1))%(w+gap)+(w+gap))%(w+gap);
 for(let i=-1;i<5;i++){const x=i*(w+gap)+off-(j%2?0:w/2),k=(i+j*5+50)%Math.max(1,cards.length),c=cards[k]||['#222',''];g.fillStyle=c[0];g.beginPath();g.roundRect(x,y+j*(h+gap),w,h,22);g.fill();
  g.fillStyle=c[2]||'#fff';g.font=font;g.textAlign='center';g.textBaseline='middle';g.fillText(c[1],x+w/2,y+j*(h+gap)+h/2)}}g.restore()};

FX.LIST['액체방울']='#11 크롬 같은 방울이 흐르며 글자 띠 뒤로 지나감(셰이더 대신 겹친 원 그라데이션)';
FX.LIST['빛덩이']='#20 번지는 빛 덩이가 화면을 가로지름';
FX.blobs=(g,t,{n=5,colors=[['#FF4A3D','#FFD27A'],['#2F2FE0','#9BE7FF'],['#111','#C6FF3D']],R=170})=>{for(let i=0;i<n;i++){const h=H(i+11),x=FX.cx+Math.sin(t*(.6+h)+i*2)*360,y=950+Math.cos(t*(.5+h*.6)+i)*560,r=R*(.7+h*.6),c=colors[i%colors.length];
 const gr=g.createRadialGradient(x-r*.35,y-r*.35,r*.1,x,y,r);gr.addColorStop(0,'#fff');gr.addColorStop(.25,c[1]);gr.addColorStop(.8,c[0]);gr.addColorStop(1,'#000');g.fillStyle=gr;g.beginPath();g.arc(x,y,r,0,7);g.fill()}};
FX.glowOrb=(g,t,t0,{y=FX.cy,r=240,color='255,255,255',dur=1.4})=>{const p=eio(cl((t-t0)/dur)),x=mix(-r,1080+r,p),gr=g.createRadialGradient(x,y,0,x,y,r);gr.addColorStop(0,`rgba(${color},.95)`);gr.addColorStop(1,`rgba(${color},0)`);g.fillStyle=gr;g.beginPath();g.arc(x,y,r,0,7);g.fill()};
// 상황별로 고르는 표(docs/모션_기법_목록_2026-11-11.md 와 같음). html_motion.py --기법=<상황> 이 이 표를 보여 준다.
FX.LIST=Object.assign(FX.LIST,{'채팅말풍선':'카톡 말풍선이 박자에 맞춰 뜸(reel_1113)','속마음쾅':'(속마음) 큰 글자가 기울며 쾅(reel_1113)','덮개그리기':'선으로 그림을 그려 개념을 보여 줌(reel_1113)','고르기카드':'1·2 카드가 번갈아 커짐(reel_1113)','온도계게이지':'온도계가 올랐다 식음(reel_1114)','태양그리기':'돌아가는 태양과 한자(reel_1114)','별자리선긋기':'점을 선으로 이어 별자리(reel_1114)','숫자카드팝':'0~3 카드가 튀어나와 차례로 켜짐(reel_1114)','원형배치':'12개를 원으로 놓기(reel_1115)','삼각형그리기':'세 점을 잇는 삼각형(reel_1115)','카메라줌':'팀마다 그쪽으로 당겨 보기(reel_1115)'});
FX.USE={
 '훅(첫 1초)':['박자글자','배경뒤집기','글자띠','원와이프','글자늘이기','낱말블록교체','별폭발','점착지','픽셀블록','글자겹쳐쌓기','글자스태거','속마음쾅'],
 '숫자·통계':['숫자폭주','입자글자','도형격자변형','온도계게이지','궤도링','허브연결','이징그래프'],
 '관계·궁합':['점파동','삼각형그리기','원형배치','허브연결','궤적선','카메라줌'],
 '상품·앱 소개':['UI시연','버튼상태전환','모양변신','슬라이더','토글','탭전환','명령창','토스트','카드뒤집기'],
 '개념 설명':['사전정의','손글씨주석','위아래비교','이징비교줄','덮개그리기','별자리선긋기','태양그리기','슬롯롤링'],
 '감성·신비':['입자소용돌이','도형변신','점3D','방사선터널','물결링','트루쳇무늬','액체방울','빛덩이'],
 '대화·사연':['채팅말풍선','속마음쾅','고르기카드','숫자카드팝'],
 '끝장면(행동)':['회전별표','로고조립','방사형','칩줄세우기','영상벽','궤적선','공튀기기','낱말이뜻대로','로딩선열기']};

// 앞서 각 편 HTML 안에만 있던 기법도 여기서 부를 수 있게(11/11, 대표 "어떤 콘텐츠 만들든 쓸 수 있게")
FX.textPoints=(txt,{font='900 520px PL',step=10,top=480}={})=>{const c=document.createElement('canvas');c.width=1080;c.height=800;const x=c.getContext('2d');x.font=font;x.textAlign='center';x.textBaseline='middle';x.fillText(txt,540,420);
 const d=x.getImageData(0,0,1080,800).data,o=[];for(let y=0;y<800;y+=step)for(let xx=0;xx<1080;xx+=step)if(d[(y*1080+xx)*4+3]>128)o.push([xx,y+top]);return o};
FX.beatWords=(g,t,t0,o)=>FX.wordBlocks(g,t,t0,o);   // 박자글자 + 배경뒤집기
FX.marquee=(g,t,{text='돈 들어오는 달 — ',rows=5,y=540,gap=175,font='900 150px PL',fill='#fff',stroke='#FFD600',angle=-.157,speed=620})=>{g.save();g.translate(540,960);g.rotate(angle);g.translate(-540,-960);g.font=font;g.textBaseline='top';
 for(let r=0;r<rows;r++){const s=text.repeat(8),w=g.measureText(text).width,d=r%2?1:-1,x=((t*speed*d)%w+w)%w-w*2;if(r%2){g.strokeStyle=stroke;g.lineWidth=3;g.strokeText(s,x,y+r*gap)}else{g.fillStyle=fill;g.fillText(s,x,y+r*gap)}}g.restore()};
FX.circleWipe=(g,t,t0,{x=FX.cx,y=FX.cy,color='#FFD600',dur=.4})=>{const p=eio(cl((t-t0)/dur));if(p<=0)return;g.fillStyle=color;g.beginPath();g.arc(x,y,p*2300,0,7);g.fill()};
FX.shapeGrid=(g,t,t0,{cols=3,rows=4,x0=270,y0=560,dx=270,dy=230,s=75,seq=['circle','square','plus'],hl=[],color='#1E2A55',hlColor='#0F1730',labels=null,font='900 44px PL',fg='#fff'})=>{
 for(let i=0;i<cols*rows;i++){const cx=x0+(i%cols)*dx,cy=y0+Math.floor(i/cols)*dy,a=sp(t-t0-i*.035,13,.65);if(a<=0)continue;const big=hl.includes(i)&&t>t0+1.4,ss=s*a*(hl.length&&t>t0+1.4?(big?1.5:.35):1);
  FX.shapeMorph(g,cx,cy,ss,seq,cl((t-t0-.15-i*.035)/.5)*(seq.length-1),{color:big?hlColor:color});if(labels&&ss>40){g.fillStyle=fg;g.font=font;g.textAlign='center';g.textBaseline='middle';g.fillText(labels[i],cx,cy+2)}}};
FX.particleText=(g,t,t0,{target,n,R=900,color='#FFD600',size=7})=>{const N=n||target.length;g.fillStyle=color;for(let i=0;i<N;i++){const q=target[i%target.length],h=H(i),a=sp(t-t0-h*.4,9,.75),ang=h*6.283;g.fillRect(mix(540+Math.cos(ang)*R,q[0],a)-size/2,mix(960+Math.sin(ang)*R,q[1],a)-size/2,size,size)}};
FX.radial=(g,t,{x=FX.cx,y=780,n=16,L=1400,w=70,color='rgba(255,214,0,.13)'})=>{g.save();g.translate(x,y);g.rotate(t*.35);g.fillStyle=color;for(let i=0;i<n;i++){g.rotate(6.283/n);g.beginPath();g.moveTo(0,0);g.lineTo(-w,-L);g.lineTo(w,-L);g.fill()}g.restore()};
FX.chat=(g,t,t0,{text,side='l',y=520,font='800 54px PR',bg,fg='#111',maxw=700})=>{const a=sp(t-t0,15,.6);if(a<=0)return;g.save();g.font=font;const lines=String(text).split('\n'),w=Math.min(maxw,Math.max(...lines.map(l=>g.measureText(l).width))+80),h=lines.length*72+50;
 const x=side=='l'?90:1080-90-w;g.translate(side=='l'?x:x+w,y+h);g.scale(a,a);g.translate(side=='l'?0:-w,-h);g.fillStyle=bg||(side=='l'?'#fff':'#FFD93D');g.beginPath();g.roundRect(0,0,w,h,[44,44,side=='l'?44:12,side=='l'?12:44]);g.fill();
 g.fillStyle=fg;g.textBaseline='top';lines.forEach((l,i)=>g.fillText(l,40,25+i*72));g.restore()};
FX.typingDots=(g,t,{x=135,y=568,color='#9AA7BF'})=>{for(let i=0;i<3;i++){g.fillStyle=color;g.beginPath();g.arc(x+i*40,y-Math.max(0,Math.sin(t*8-i*.9))*10,11,0,7);g.fill()}};
FX.bigPop=(g,t,t0,{text,x=FX.cx,y=1250,font='900 220px PL',color='#FFD93D',burst='rgba(255,217,61,.22)'})=>{const a=sp(t-t0,18,.5);if(a<=0)return;g.save();g.translate(x,y);g.fillStyle=burst;for(let i=0;i<14;i++){g.rotate(6.283/14);const L=mix(0,700,ease((t-t0)/.4));g.fillRect(-10,-L,20,L*.55)}
 g.rotate(mix(-.2,-.07,a));g.scale(mix(2.2,1,a),mix(2.2,1,a));g.fillStyle=color;g.font=font;g.textAlign='center';g.textBaseline='middle';g.fillText(text,0,0);g.restore()};
FX.pickCards=(g,t,t0,{labels=['1','2'],subs=[],y=900,w=400,h=400,colors=['#FFD93D','#fff'],cycle=.5})=>{const n=labels.length,gap=(1080-180-n*w)/Math.max(1,n-1);labels.forEach((l,i)=>{const a=sp(t-t0-i*.15,15,.55),on=t>t0+.8&&Math.floor((t-t0-.8)/cycle)%n==i;
 if(a<=0)return;const x=90+i*(w+gap);g.save();g.translate(x+w/2,y+h/2);g.scale(a*(on?1.08:1),a*(on?1.08:1));g.fillStyle=colors[i%colors.length];g.beginPath();g.roundRect(-w/2,-h/2,w,h,48);g.fill();
 g.fillStyle='#111';g.textAlign='center';g.textBaseline='middle';g.font=`900 ${Math.round(w*.38)}px PL`;g.fillText(l,0,subs[i]?-40:0);if(subs[i]){g.font=`900 ${Math.round(w*.17)}px PL`;g.fillText(subs[i],0,w*.25)}g.restore()})};
FX.gauge=(g,{x=FX.cx,y0=1250,h=780,p=.5,hot='#FF5A5F',cold='#7FA7FF',label=true})=>{g.fillStyle='rgba(255,255,255,.12)';g.beginPath();g.roundRect(x-55,y0-h,110,h,55);g.fill();g.beginPath();g.arc(x,y0+40,95,0,7);g.fill();
 g.fillStyle=p>.6?hot:cold;g.beginPath();g.roundRect(x-34,y0-h*p,68,h*p+20,34);g.fill();g.beginPath();g.arc(x,y0+40,72,0,7);g.fill();if(label){g.fillStyle='#fff';g.font='900 72px PL';g.textAlign='left';g.fillText(Math.round(mix(20,100,p))+'°',x+110,y0-h*p+20)}};
FX.sun=(g,t,t0,{x=FX.cx,y=860,r=200,char='丙',c1='#FF5A5F',c2='#FFB199',L=250})=>{const a=sp(t-t0,10,.7);g.save();g.translate(x,y);g.rotate(t*.6);for(let i=0;i<16;i++){g.rotate(6.283/16);const l=mix(0,L,sp(t-t0-.2-i*.02,12,.6));g.fillStyle=i%2?c1:c2;g.beginPath();g.moveTo(-22,-r-10);g.lineTo(0,-r-10-l);g.lineTo(22,-r-10);g.fill()}g.restore();
 g.fillStyle=c1;g.beginPath();g.arc(x,y,r*a,0,7);g.fill();g.fillStyle='#fff';g.font=`900 ${r*.85*a}px PL`;g.textAlign='center';g.textBaseline='middle';g.fillText(char,x,y+12)};
FX.constellation=(g,t,t0,{pts,label='',color='#FF5A5F',lab='#FFD7D8'})=>{const p=cl((t-t0)/.5)*(pts.length-1);g.strokeStyle=color;g.lineWidth=6;g.beginPath();for(let i=0;i<=Math.floor(p)&&i<pts.length;i++){i?g.lineTo(pts[i][0],pts[i][1]):g.moveTo(pts[i][0],pts[i][1])}
 if(p<pts.length-1&&p>0){const i=Math.floor(p),f=p-i;g.lineTo(mix(pts[i][0],pts[i+1][0],f),mix(pts[i][1],pts[i+1][1],f))}g.stroke();pts.forEach((q,i)=>{const s=sp(t-t0-i*.08,16,.55);g.fillStyle='#fff';g.beginPath();g.arc(q[0],q[1],12*s,0,7);g.fill()});
 if(label&&t>t0+.4){g.fillStyle=lab;g.font='800 40px PR';g.textAlign='center';g.fillText(label,pts[0][0]+40,pts[0][1]-50)}};
FX.ringPos=(i,n,{x=FX.cx,y=900,R=330}={})=>{const a=-Math.PI/2+i*6.283/n;return[x+Math.cos(a)*R,y+Math.sin(a)*R]};
FX.polyDraw=(g,pts,p,{color='#477A61',width=12,fill=0})=>{g.save();g.strokeStyle=color;g.lineWidth=width;g.lineJoin='round';g.lineCap='round';const n=pts.length,seg=p*n;g.beginPath();g.moveTo(pts[0][0],pts[0][1]);
 for(let i=0;i<n;i++){const a=pts[i],b=pts[(i+1)%n],f=cl(seg-i);if(f<=0)break;g.lineTo(mix(a[0],b[0],f),mix(a[1],b[1],f))}g.stroke();if(fill>0){g.globalAlpha=fill*.18;g.fillStyle=color;g.beginPath();pts.forEach((q,i)=>i?g.lineTo(q[0],q[1]):g.moveTo(q[0],q[1]));g.fill()}g.restore()};

// ── 캐릭터 애니메이션(11/11 대표 "모션그래픽·텍스트 위주보다 캐릭터 애니메이션 등 잘 섞어서") — 정월 누끼(characters/cut/*.png), 어두운 판에만(K-076), 크게(K-061)
FX.LIST=Object.assign(FX.LIST,{'캐릭터등장':'정월이 아래에서 튀어 오르며 등장, 숨쉬듯 살짝 움직임','캐릭터말하기':'말하는 동안 박자에 맞춰 끄덕·기울임, 몸짓 컷으로 바뀜','손글씨말풍선':'손글씨 글꼴 말풍선이 꼬리와 함께 톡 뜸','스티커테두리':'누끼에 흰 테두리를 둘러 스티커처럼'});
FX.USE['캐릭터']=['캐릭터등장','캐릭터말하기','손글씨말풍선','스티커테두리','속마음쾅','손글씨주석'];
FX.img=(src)=>new Promise(r=>{const i=new Image();i.onload=()=>r(i);i.src=src});
FX.sticker=(img,{px=10,color='#fff'}={})=>{const c=document.createElement('canvas');c.width=img.width+px*2;c.height=img.height+px*2;const x=c.getContext('2d');
 for(let a=0;a<16;a++){x.drawImage(img,px+Math.cos(a*Math.PI/8)*px,px+Math.sin(a*Math.PI/8)*px)}x.globalCompositeOperation='source-in';x.fillStyle=color;x.fillRect(0,0,c.width,c.height);x.globalCompositeOperation='source-over';x.drawImage(img,px,px);return c};
// imgs: [기본, 몸짓…] 캔버스/이미지. talk: [[t0,t1],…] 말하는 구간, beat: 박 간격
FX.character=(g,t,{imgs,x=FX.cx,y=1920,h=1150,enter=0,exit=null,talk=[],beat=.5,from='bottom'})=>{const a=sp(t-enter,11,.62);if(a<=0)return;let out=0;if(exit!=null&&t>exit)out=eio((t-exit)/.35);
 const talking=talk.some(([s,e])=>t>=s&&t<e),im=(talking&&imgs[1])?imgs[1]:imgs[0],w=im.width*h/im.height;
 const breath=1+Math.sin(t*2.4)*.008,bob=talking?Math.abs(Math.sin(t*Math.PI/beat))*-14:0,tilt=talking?Math.sin(t*Math.PI/beat/2)*.025:Math.sin(t*1.1)*.008;
 const dy=from=='bottom'?(1-a)*700+out*900:0,dx=from=='left'?(1-a)*-800-out*900:from=='right'?(1-a)*800+out*900:0;
 g.save();g.translate(x+dx,y+dy+bob);g.rotate(tilt);g.scale(breath*(a>1?1:mix(.9,1,a)),breath);g.drawImage(im,-w/2,-h,w,h);g.restore();
 if(a>.85&&out<.15&&typeof window!=='undefined'){(window.__zsChar=window.__zsChar||[]).push([x+dx-w*.3,y+dy-h,x+dx+w*.3,y+dy-h*.55])}};   // 11/12 대표 '뱃지랑 정월 얼굴이랑 겹치잖아': 얼굴 자리(위 45%·가운데 60%)를 관문에 넘긴다
FX.bubble=(g,t,t0,{text,x=FX.cx,y=600,tail='down',tx=null,font='72px BZ',color='#111',bg='#fff',maxw=820,pad=46,lh=1.25,sticker=true,tilt=-.03,edge='#FFFFFF'})=>{const a=sp(t-t0,16,.55);if(a<=0)return;g.save();g.font=font;
 // 11/11 대표 13:40 "정월이 스티커 느낌이면 말풍선도 그런 느낌으로 통일감": 말풍선도 스티커 — 꼬리까지 한 덩어리, 흰 테두리 + 아래로 떨어진 단단한 그림자, 살짝 기울기
 const lines=String(text).split('\n'),fs=parseFloat(font.match(/(\d+)px/)[1]),w=Math.min(maxw,Math.max(...lines.map(l=>g.measureText(l).width))+pad*2),h=lines.length*fs*lh+pad*1.4,ttx=(tx==null?0:tx-x),r=Math.min(48,h/2);
 const shape=()=>{g.beginPath();g.roundRect(-w/2,-h/2,w,h,r);if(tail=='down'){g.moveTo(ttx-34,h/2-4);g.lineTo(ttx+2,h/2+56);g.lineTo(ttx+38,h/2-4)}else{g.moveTo(ttx-34,-h/2+4);g.lineTo(ttx+2,-h/2-56);g.lineTo(ttx+38,-h/2+4)}};
 g.translate(x,y);g.scale(a,a);g.rotate((1-a)*-.15+(sticker?tilt:0));
 if(sticker){g.save();g.translate(0,12);g.fillStyle='rgba(0,0,0,.28)';shape();g.fill();g.restore();g.lineJoin='round';g.strokeStyle=edge;g.lineWidth=18;shape();g.stroke()}
 g.fillStyle=bg;shape();g.fill();
 g.fillStyle=color;g.textAlign='center';g.textBaseline='middle';lines.forEach((l,i)=>g.fillText(l,0,(i-(lines.length-1)/2)*fs*lh+4));g.restore()};

// 11/11 대표 "채널 별 콘텐츠 안전영역 관련해서도 준 거 기억하지?": 규격은 channel_specs.py 가 단일 출처다.
// html_motion.py 가 페이지를 열 때 window.ZS_SPEC 를 넣는다(여기 숫자는 node 견본용 대체값일 뿐, 제작은 주입값을 쓴다).
FX.SPEC=(typeof window!=='undefined'&&window.ZS_SPEC)||{safe:[60,330,900,1470],top:[60,340,900,390],bottom:[60,1425,900,1465]};
FX.cx=(FX.SPEC.safe[0]+FX.SPEC.safe[2])/2;          // 글·그림 가운데 = 안전 영역 가운데(K-165). 540 이 아니다
FX.aw=()=>FX.SPEC.safe[2]-FX.SPEC.safe[0]-40;FX.cy=(FX.SPEC.top[3]+FX.SPEC.bottom[1])/2;
FX.area=()=>({x0:FX.SPEC.safe[0],x1:FX.SPEC.safe[2],y0:FX.SPEC.top[3]+10,y1:FX.SPEC.bottom[1]-10});  // 글이 들어갈 수 있는 칸
// 고정 요소(brand_frame.py 와 같은 자리): 위 가운데 한 줄(K-166) · 아래 왼쪽 AI 고지 · 아래 오른쪽 주소 — 글자는 브랜드 설정에서
// AI 고지는 **그리지 않는 것이 기본값**이다(ai=''). 정월 캐릭터가 화면에 실제로 나오는 편에서만 페이지가 {ai:FX.BRAND.ai} 로 넘긴다
// (대표 2026-11-22 13:4x "정월 캐릭터가 나올 때만 AI 캐릭터 고지", K-265). 캐릭터 없이 글자·도형만 나오는 릴스·카드에는 넣지 않는다.
// 브랜드 값은 html_motion.py 가 brands/<id>.json 을 읽어 window.ZS_BRAND 로 넣는다(아래는 주입이 없을 때 대체값).
FX.BRAND=Object.assign({name:'자오선',tag:'동서양 6개 운명학 교차분석',url:'zaoseon.com',ai:'정월은 가상의 AI 캐릭터입니다',accent:'#F4CE62',ink:'#FFFFFF',pill:'#0D1424',
 palette:['#FF5A1F','#2F6BFF','#2EBD6B','#FFC21A','#FFD400'],fonts:{title:'PL',body:'PL',hand:'PL'}},(typeof window!=='undefined'&&window.ZS_BRAND)||{});
FX.C=FX.BRAND.palette.concat(['#FF5A1F','#2F6BFF','#2EBD6B','#FFC21A','#FFD400'].slice(FX.BRAND.palette.length));
FX.frame=(g,{ai='',gold=FX.BRAND.accent,ink=FX.BRAND.ink,pill=FX.BRAND.pill}={})=>{if(window.__zsNoFrame){window.__zsFrameOpt={ai};return}window.__zsFrame=1;g.save();g.setTransform(1,0,0,1,0,0);g.globalAlpha=1;
 const B=FX.BRAND,TF=B.fonts.title,BF=B.fonts.body,[tx0,ty0,tx1,ty1]=FX.SPEC.top,[bx0,by0,bx1,by1]=FX.SPEC.bottom,cy=(ty0+ty1)/2,by=(by0+by1)/2;g.textBaseline='middle';
 if(B.name||B.tag){const sep=B.name&&B.tag?'  ·  ':'';g.font='900 42px '+TF;const a=g.measureText(B.name||'').width;g.font='800 34px '+BF;const d=g.measureText(sep).width,b=g.measureText(B.tag||'').width;let x=(tx0+tx1)/2-(a+d+b)/2;
 g.fillStyle=pill;g.beginPath();g.roundRect(x-22,ty0-6,a+d+b+44,ty1-ty0+12,28);g.fill();
 g.textAlign='left';g.font='900 42px '+TF;g.fillStyle=gold;if(B.name)g.fillText(B.name,x,cy);g.font='800 34px '+BF;g.fillStyle=ink;g.globalAlpha=.6;if(sep)g.fillText(sep,x+a,cy);g.globalAlpha=.95;if(B.tag)g.fillText(B.tag,x+a+d,cy);g.globalAlpha=1}
 if(B.url){g.font='900 40px '+TF;const u=g.measureText(B.url).width;g.fillStyle=pill;g.beginPath();g.roundRect(bx1-u-18,by0-4,u+36,by1-by0+8,24);g.fill();g.fillStyle=gold;g.textAlign='right';g.fillText(B.url,bx1,by)}
 if(ai){g.font='800 28px '+BF;const w=g.measureText(ai).width;g.fillStyle=pill;g.beginPath();g.roundRect(bx0,by0,w+32,by1-by0,20);g.fill();g.fillStyle='rgba(255,255,255,.7)';g.textAlign='left';g.fillText(ai,bx0+16,by)}
 g.restore();window.__zsFrame=0};
// 11/17 20:38 대표 "선은 곡선 화살표 같은것도 좀 쓰고": 곡선화살표 — 두 점 사이를 휘어진 선이 그려지며 끝에 화살촉이 붙는다.
// bend: 가운데가 휘는 정도(px, +면 진행 방향 왼쪽으로). p: 0~1 그려진 정도. both: 양쪽 화살촉. 끝이 상자에 닿지 않게 gap 만큼 띄운다.
FX.curveArrow=(g,x0,y0,x1,y1,p,{bend=120,color='#fff',w=10,head=30,both=false,dash=null}={})=>{if(p<=0)return;const mx=(x0+x1)/2,my=(y0+y1)/2,dx=x1-x0,dy=y1-y0,L=Math.hypot(dx,dy)||1,
 cx=mx-dy/L*bend,cy=my+dx/L*bend,Q=u=>[(1-u)*(1-u)*x0+2*(1-u)*u*cx+u*u*x1,(1-u)*(1-u)*y0+2*(1-u)*u*cy+u*u*y1],N=40,pp=cl(p);
 g.save();g.strokeStyle=color;g.fillStyle=color;g.lineWidth=w;g.lineCap='round';g.lineJoin='round';if(dash)g.setLineDash(dash);g.beginPath();
 for(let k=0;k<=N*pp;k++){const [x,y]=Q(k/N);k?g.lineTo(x,y):g.moveTo(x,y)}g.stroke();g.setLineDash([]);
 const tip=(u,v)=>{const [ax,ay]=Q(u),[bx,by]=Q(v),an=Math.atan2(ay-by,ax-bx);g.save();g.translate(ax,ay);g.rotate(an);g.beginPath();g.moveTo(w*.6,0);g.lineTo(-head,-head*.62);g.lineTo(-head*.72,0);g.lineTo(-head,head*.62);g.closePath();g.fill();g.restore()};
 if(pp>.15)tip(pp,Math.max(0,pp-.05));if(both&&pp>=1)tip(0,.05);g.restore()};
FX.LIST['곡선화살표']='두 점 사이를 휘어진 화살표가 그려지며 이어짐(서로 주고받음은 both·두 개)';
FX.USE['관계·궁합'].push('곡선화살표');FX.USE['개념 설명'].push('곡선화살표');
// 11/17 22:06 대표 "제발 규칙 적용 좀"(K-235): 기법을 실제로 그린 순간 이름을 적는다. 관문이 window.FX(적은 이름)와 실제로 그린 이름을 맞춰 본다.
// 배경 층(11/19 대표 승인 "배경 무늬/모션 레이어는 간격 검사에서 제외"): 판 전체에 깔리는 무늬·흐르는 글자 띠·격자·터널·모서리 라벨 같은 장식은 F.layerBG(g,()=>{…}) 안에서 그린다.
// 관문(html_motion 안전영역·균형·표지·CTA 검사)은 window.__zsNoBG=1 로 페이지를 열어 이 층을 건너뛰고, 글자·상자·로고·칩·버튼 사이만 잰다. 실제 영상에는 그대로 그려진다.
// 지킬 것: 대본의 정보(훅·본문·CTA)는 배경 층에 넣지 않는다. 배경 층 글은 기록(__zsTxt·__zsBox·__zsImg)에도 안 남는다.
FX.layerBG=(g,fn)=>{if(typeof window!=='undefined'&&window.__zsNoBG)return;const w=typeof window!=='undefined';if(w)window.__zsBG=1;try{g.save();fn();g.restore()}finally{if(w)window.__zsBG=0}};
// 11/19 대표 16:17 "분석하고 검토해서 빠져있는 것들 추가해"(milesahead.ai '클로드 인스타 스킬 13개' 릴스): 목록형 영상의 위 진행 칸 · 핵심어 강조 자막
// 진행칸: n칸 중 i번째까지 차고, 지금 칸은 p(0~1)만큼 찬다. 목록·단계 영상(13가지·5단계)에서 '지금 몇 번째'를 보여 준다
FX.segBar=(g,{n=13,i=0,p=1,x=null,y=null,w=null,h=26,gap=8,on='#E8613C',off='rgba(0,0,0,.12)',r=6}={})=>{const A=FX.area(),X=x==null?A.x0+20:x,W=w==null?(A.x1-A.x0-40):w,Y=y==null?A.y0+20:y,cw=(W-gap*(n-1))/n;
 g.save();for(let k=0;k<n;k++){const xx=X+k*(cw+gap);g.fillStyle=off;g.beginPath();g.roundRect(xx,Y,cw,h,r);g.fill();const f=k<i?1:k==i?cl(p):0;if(f>0){g.fillStyle=on;g.beginPath();g.roundRect(xx,Y,cw*f,h,r);g.fill()}}g.restore()};
// 핵심어강조자막: 낱말이 박자대로 나타나고 keys 에 든 낱말만 강조색. 한 줄 자막(내레이션과 같은 시각)
FX.keyCaption=(g,t,t0,{text,keys=[],x=FX.cx,y=1300,font='900 72px PL',col='#16161A',keyCol='#E8613C',step=.12}={})=>{const ws=String(text).split(' ');g.save();g.font=font;g.textBaseline='middle';
 const sp_=g.measureText(' ').width,W=ws.reduce((s,w)=>s+g.measureText(w).width,0)+sp_*(ws.length-1);let xx=x-W/2;
 ws.forEach((w,k)=>{const a=sp(t-t0-k*step,18,.7);const ww=g.measureText(w).width;if(a>0){g.save();g.globalAlpha=cl(a*2);g.translate(xx+ww/2,y+(1-cl(a))*24);g.fillStyle=keys.some(q=>w.includes(q))?keyCol:col;g.textAlign='center';g.fillText(w,0,0);g.restore()}xx+=ww+sp_});g.restore()};
FX.LIST['진행칸']='목록·단계 영상 위에 n칸 진행 막대(지금 몇 번째)(milesahead 11/19)';FX.LIST['핵심어강조자막']='낱말이 차례로 뜨고 핵심어만 강조색(milesahead 11/19)';
FX.USE['개념 설명'].push('진행칸','핵심어강조자막');FX.USE['상품·앱 소개'].push('진행칸');
// K-289(대표 11/24 TV 자막·연출 레퍼런스): 레이아웃 3종 — [2분할 대비]·[3·4분할 근거] = splitGrid, [원형 PIP 리액션] = pip, [체크리스트 요약 카드] = checkCard.
// 선·카드는 레이아웃 틀(구분선·상자)이라 코드로 그린다. 칸 안 그림·PIP 얼굴은 draw 콜백에서 승인 에셋만 그린다(K-285). 글꼴은 고딕 1종(FX.BRAND.fonts.body).
FX.LIST=Object.assign(FX.LIST,{'분할대비':'2·3·4분할 칸이 열리고 경계선 1줄(강조색) + 칸마다 괄호 라벨(K-289)','원형PIP':'원형 리액션 창이 튀어나오고 강조색 링(K-289)','체크리스트카드':'카드 제목 + ☑ 항목이 하나씩 켜짐(K-289)'});
FX.USE['개념 설명'].push('분할대비','체크리스트카드');FX.USE['대화·사연'].push('원형PIP');
FX.splitGrid=(g,t,t0,{n=2,area=null,line=null,lw=6,labels=[],font=null,fg='#fff',dur=.35,draw=null})=>{const T=t-t0;if(T<0)return;const A=area||FX.area(),acc=line||FX.BRAND.accent,F_=font||`800 48px ${FX.BRAND.fonts.body}`;
 const W=A.x1-A.x0,H=A.y1-A.y0,cells=n===4?[[0,0,.5,.5],[.5,0,1,.5],[0,.5,.5,1],[.5,.5,1,1]]:[...Array(n)].map((_,i)=>[i/n,0,(i+1)/n,1]);
 cells.forEach((c,i)=>{const p=eio(cl((T-i*.08)/dur));if(p<=0)return;const x0=A.x0+c[0]*W,y0=A.y0+c[1]*H,x1=A.x0+c[2]*W,y1=A.y0+c[3]*H;g.save();g.beginPath();g.rect(x0,y0+(y1-y0)*(1-p),x1-x0,(y1-y0)*p);g.clip();
  if(draw)draw(i,{x0,y0,x1,y1});if(labels[i]){g.font=F_;g.fillStyle=fg;g.textAlign='center';g.textBaseline='alphabetic';g.lineWidth=3;g.strokeStyle='rgba(0,0,0,.55)';const s=`(${labels[i]})`;g.strokeText(s,(x0+x1)/2,y1-28);g.fillText(s,(x0+x1)/2,y1-28)}g.restore()});
 const q=eio(cl((T-.15)/dur));g.save();g.strokeStyle=acc;g.lineWidth=lw;g.lineCap='butt';g.beginPath();
 if(n===4){g.moveTo(A.x0+W/2,A.y0);g.lineTo(A.x0+W/2,A.y0+H*q);g.moveTo(A.x0,A.y0+H/2);g.lineTo(A.x0+W*q,A.y0+H/2)}else for(let i=1;i<n;i++){const x=A.x0+W*i/n;g.moveTo(x,A.y0);g.lineTo(x,A.y0+H*q)}g.stroke();g.restore()};
FX.pip=(g,t,t0,{x,y,r=130,ring=null,ringW=8,draw=null,label='',font=null,fg='#fff'})=>{const a=sp(t-t0,16,.55);if(a<=0)return;g.save();g.translate(x,y);g.scale(a,a);g.save();g.beginPath();g.arc(0,0,r,0,7);g.clip();g.fillStyle='#fff';g.fillRect(-r,-r,2*r,2*r);if(draw)draw({r});g.restore();
 g.strokeStyle=ring||FX.BRAND.accent;g.lineWidth=ringW;g.beginPath();g.arc(0,0,r,0,7);g.stroke();
 if(label){g.font=font||`900 56px ${FX.BRAND.fonts.hand}`;g.fillStyle=fg;g.textBaseline='middle';const L_=x+r+16+g.measureText(label).width>FX.area().x1;g.textAlign=L_?'right':'left';g.fillText(label,L_?-r-16:r+16,-r*.55)}g.restore()};   // 라벨이 안전 영역 밖으로 나가면 왼쪽에
FX.checkCard=(g,t,t0,{x,y,w=520,title='',items=[],font=null,tfont=null,fg='#111',bg='#fff',acc=null,step=.18,lh=1.55})=>{const a=sp(t-t0,14,.65);if(a<=0)return;const A_=acc||FX.BRAND.accent,F_=font||`800 46px ${FX.BRAND.fonts.body}`,TF=tfont||`900 58px ${FX.BRAND.fonts.body}`,fs=parseFloat(F_.match(/(\d+)px/)[1]),ts=parseFloat(TF.match(/(\d+)px/)[1]);
 const h=56+ts*1.5+items.length*fs*lh+40;g.save();g.globalAlpha=cl(a*1.5);g.translate(0,(1-a)*60);g.fillStyle=bg;g.beginPath();g.roundRect(x,y,w,h,28);g.fill();
 g.fillStyle=A_;g.beginPath();g.roundRect(x+28,y+36,w-56,ts*1.35,16);g.fill();g.font=TF;g.fillStyle='#111';g.textAlign='center';g.textBaseline='middle';g.fillText(title,x+w/2,y+36+ts*.68);
 g.font=F_;g.textAlign='left';items.forEach((s,i)=>{const p=cl((t-t0-.25-i*step)/.2);if(p<=0)return;const yy=y+56+ts*1.5+(i+.5)*fs*lh;g.globalAlpha=p;g.fillStyle=A_;g.fillText('☑',x+36,yy);g.fillStyle=fg;g.fillText(s,x+36+fs*1.3,yy)});g.restore()};
FX.mark=n=>{if(typeof window!=='undefined'&&!window.__zsFrame)(window.__zsFxUsed=window.__zsFxUsed||{})[n]=1};
window.FXK=FX;})();
// ───────── K-294 묶음 A(대표 11/24 "A부터 진행", 외부 자료 분석 커리어해커 알렉스 5종 → 노션 422435565da9811fb808c13eff992f2c) ─────────
// ⑱ 지적 '루즈함·끊김' 대응: ① 화면 전체 카메라 층 ② 실제 박자 격자(첫 박 오프셋) ③ 전환 5 · 글자 4 · 장면 4 ④ 움직임 기본값 ⑤ 빠른 순간만 모션 블러.
// 모두 시간 t 만으로 그린다(seek 규칙). 색·글꼴은 인자로 받는다(브랜드 값을 박지 않음). 자료의 프롬프트 문장·색은 옮기지 않고 움직임만 우리 코드로 다시 만들었다.
(function(){const FX=typeof window!=='undefined'&&window.FXK;if(!FX)return;const {cl,mix,ease,eio,sp,H}=FX,W_=()=>1080,PI=Math.PI;
const fs_=f=>parseFloat((/(\d+(?:\.\d+)?)px/.exec(f)||[0,80])[1]);
// ④ 움직임 기본값(자료 용어 카드 21종에서 공통으로 쓰는 값): 예비동작 0.1~0.2초 · 오버랩 0.12초 · 스태거 0.06~0.12초 · 결과는 0.8~1초 멈춰 읽히기(그동안도 카메라 드리프트는 계속)
FX.MOTION={anticip:.15,overlap:.12,stagger:.08,hold:.9,punch:.2,drift:.02};
// 역할별 이징: 등장=expo.out · 빨려 들어감=ease-in · 카메라=inOut · 튐=spring
FX.EZ={in:x=>{x=cl(x);return x>=1?1:1-Math.pow(2,-10*x)},out:x=>{x=cl(x);return x*x*x},cam:eio,spring:x=>sp(x,16,.6)};
// 예비동작: t0 부터 d 초 동안 반대로 살짝(back) 물러났다가 dur 동안 1 로. 0~1 이 아닌 값(-back~1)을 돌려준다
FX.anticip=(t,t0,{d=FX.MOTION.anticip,back=.12,dur=.45}={})=>{const u=t-t0;if(u<=0)return 0;if(u<d)return -back*Math.sin(u/d*PI/2);return mix(-back,1,FX.EZ.in((u-d)/dur))};

// ⑤ 빠른 순간만 모션 블러: 페이지가 FX.fast(a,b) 로 구간을 적으면 html_motion 이 그 구간 프레임만 셔터 4장 평균, 나머지는 선명하게 1장.
// (window.FAST 가 없는 옛 페이지는 지금처럼 전 프레임 2장 평균 그대로)
FX.fast=(a,b)=>{if(typeof window==='undefined')return;window.FAST=window.FAST||[];if(!window.FAST.some(r=>Math.abs(r[0]-a)<1e-3&&Math.abs(r[1]-b)<1e-3))window.FAST.push([a,b])};

// ② 박자 격자: html_motion --음악=<파일> 이 tools/beat_grid.py 로 잰 값을 window.ZS_BEAT={bpm,offset} 으로 넣는다.
// T(k)=k번째 박 시각(첫 박 오프셋 포함) · snap(t,div)=가장 가까운 1/div 박 · build(k0,[2,2,4])=한 박→반 박→¼박으로 빨라지는 타격 시각 · breath(k)=큰 타격 k 직전 반 박 쉼 시작
FX.beat=({bpm=120,offset=0}={})=>{const B=60/bpm,T=k=>offset+k*B;return {bpm,offset,B,T,
 snap:(t,div=2)=>{const q=B/div;return offset+Math.round((t-offset)/q)*q},
 build:(k0,counts=[2,2,4])=>{const r=[];let k=k0;counts.forEach((n,i)=>{const st=1/Math.pow(2,i);for(let j=0;j<n;j++){r.push(T(k));k+=st}});return r},
 breath:k=>T(k)-B/2}};
FX.BEAT=FX.beat((typeof window!=='undefined'&&window.ZS_BEAT)||{});

// ① 카메라 층: FX.camSetup({scenes:[[a,b],…], hits:[초…], drops:[[a,b],…], zooms:[{t,d,s,x,y}]}) 를 한 번 부르고, 장면마다 g.save();FX.cam(g,t);…;g.restore().
//  · 장면 안 드리프트: 1→1+drift(기본 2%) 확대 + 장면마다 방향을 바꾸는 미세 이동(멈춘 화면 없애기)
//  · 타격 펀치: hits 시각마다 0.2초 안에 줌 펀치 + 짧은 흔들림(감쇠)
//  · 상태 확대: zooms 로 한 점을 향해 확대(주인공이 화면을 채움)
//  · 무음 드롭 구간에서는 끈다(멈춤 자체가 연출)
FX.camSetup=(o={})=>{FX._cam=Object.assign({scenes:[],hits:[],drops:[],zooms:[],drift:FX.MOTION.drift,punch:.035,shake:12,dur:FX.MOTION.punch},o)};
FX.camAt=t=>{const C=FX._cam;if(!C)return {s:1,dx:0,dy:0,r:0,fx:FX.cx,fy:FX.cy};let s=1,dx=0,dy=0,r=0,fx=FX.cx,fy=FX.cy;
 if(C.drops.some(([a,b])=>t>=a&&t<b))return {s,dx,dy,r,fx,fy};
 const i=C.scenes.findIndex(([a,b])=>t>=a&&t<b);if(i>=0){const [a,b]=C.scenes[i],u=cl((t-a)/Math.max(.01,b-a));s*=1+C.drift*u;const d=i%2?1:-1;dx+=d*C.drift*300*u}   // 세로로는 밀지 않는다(위·아래 여백 균형 관문 — ⑱ v7 시험)
 for(const h of C.hits){const u=t-h;if(u<0||u>=C.dur)continue;const e=Math.pow(1-u/C.dur,2);s*=1+C.punch*e;dx+=C.shake*e*Math.sin(u*90+h*7);dy+=C.shake*.7*e*Math.cos(u*75+h*5);r+=.004*e*Math.sin(u*60)}
 for(const z of C.zooms){const p=eio(cl((t-z.t)/(z.d||.5)));if(p<=0)continue;s*=mix(1,z.s||1.2,p);fx=mix(fx,z.x??FX.cx,p);fy=mix(fy,z.y??FX.cy,p)}
 return {s,dx,dy,r,fx,fy}};
FX.cam=(g,t)=>{const c=FX.camAt(t);g.translate(c.fx+c.dx,c.fy+c.dy);g.rotate(c.r);g.scale(c.s,c.s);g.translate(-c.fx,-c.fy);FX.mark('카메라층');return c};

// 오프스크린 판(글자 창·셔터용). 연결 안 된 캔버스라 관문 기록에 안 남는다 — 전환 0.3~0.6초 동안만 쓴다
FX._off=(g,k='a')=>{FX.__off=FX.__off||{};let c=FX.__off[k];const w=g.canvas.width,h=g.canvas.height;if(!c||c.width!==w||c.height!==h){c=document.createElement('canvas');c.width=w;c.height=h;FX.__off[k]=c}const x=c.getContext('2d');x.setTransform(1,0,0,1,0,0);x.globalAlpha=1;x.globalCompositeOperation='source-over';x.clearRect(0,0,w,h);return [c,x]};

// ③-전환 5종
// 대각선마커와이프: 굵은 사선 띠(color)가 왼→오로 지나가고, 지나간 자리에 다음 장면(drawNext(g)). 지금 장면을 먼저 그린 뒤 부른다
FX.diagWipe=(g,t,t0,{dur=.35,color='#F4CE62',band=180,ang=-.32,drawNext=null}={})=>{const p=eio(cl((t-t0)/dur));if(p<=0)return;if(p>=1){drawNext&&drawNext(g);return}
 const Hh=g.canvas.height,k=Math.tan(ang)*Hh,X=mix(-band-Math.abs(k),W_()+band+Math.abs(k),p);FX.fast(t0,t0+dur);
 g.save();g.beginPath();g.moveTo(-10,-10);g.lineTo(X,-10);g.lineTo(X+k,Hh+10);g.lineTo(-10,Hh+10);g.closePath();g.clip();drawNext&&drawNext(g);g.restore();
 g.save();g.fillStyle=color;g.beginPath();g.moveTo(X,-10);g.lineTo(X+band,-10);g.lineTo(X+band+k,Hh+10);g.lineTo(X+k,Hh+10);g.closePath();g.fill();g.restore();FX.mark('대각선와이프')};
// 휩팬: 지금 장면이 dir 쪽으로 빠르게 밀려나고 다음 장면이 반대쪽에서 들어옴. 속도 곡선(가운데 가장 빠름) + 넘어가는 순간만 잔상 3겹
FX.whip=(g,t,t0,{dur=.3,dir=1,drawA,drawB}={})=>{const u=cl((t-t0)/dur);if(t<t0){drawA(g);return}if(u>=1){drawB(g);return}FX.fast(t0,t0+dur);
 const p=eio(u),v=Math.sin(u*PI),Wd=W_();const one=(off)=>{g.save();g.translate(-dir*Wd*p+off,0);drawA(g);g.restore();g.save();g.translate(dir*Wd*(1-p)+off,0);drawB(g);g.restore()};
 one(0);if(v>.35){g.save();g.globalAlpha=.22*v;for(const k of [1,2,3]){one(dir*k*28*v)}g.restore()}FX.mark('휩팬')};
// 글자창: 큰 글자 안에 다음 장면이 비치고, 글자가 확 커지며 화면 전체가 다음 장면이 됨
FX.textWindow=(g,t,t0,{text,font='800 300px PL',x=FX.cx,y=FX.cy,dur=.6,hold=.25,drawNext}={})=>{const u=t-t0;if(u<0)return;const [c,x2]=FX._off(g,'tw');drawNext(x2);
 const z=u<hold?1:Math.pow(40,FX.EZ.out(cl((u-hold)/(dur-hold))));if(z>30){g.drawImage(c,0,0);return}FX.fast(t0+hold,t0+dur);
 x2.globalCompositeOperation='destination-in';x2.font=font;x2.textAlign='center';x2.textBaseline='middle';x2.fillStyle='#000';x2.save();x2.translate(x,y);x2.scale(z,z);x2.fillText(text,0,0);x2.restore();g.drawImage(c,0,0);FX.mark('글자창전환')};
// 글자셔터: 큰 글자가 n개 세로 판으로 갈라져 위·아래 번갈아 열리며 다음 장면이 드러남(bg=지금 판 색)
FX.textShutter=(g,t,t0,{text,font='800 260px PL',x=FX.cx,y=FX.cy,ink='#FAF8F3',bg='#0D1424',n=5,dur=.5,hold=.3,drawNext}={})=>{const u=t-t0;if(u<0)return;const p=FX.EZ.out(cl((u-hold)/(dur-hold)));
 if(p>=1){drawNext(g);return}if(p>0){drawNext(g);FX.fast(t0+hold,t0+dur)}const Hh=g.canvas.height,Wd=W_(),sw=Wd/n;
 for(let i=0;i<n;i++){g.save();g.beginPath();g.rect(i*sw-.5,0,sw+1,Hh);g.clip();g.translate(0,(i%2?1:-1)*Hh*p);g.fillStyle=bg;g.fillRect(0,0,Wd,Hh);g.font=font;g.textAlign='center';g.textBaseline='middle';g.fillStyle=ink;g.fillText(text,x,y);g.restore()}FX.mark('글자셔터')};
// 점매치컷: 골드 점 하나가 앞 장면의 동그라미(from)에서 다음 장면의 동그라미(to)로 날아가며 크기가 바뀜(해→달→로고). 날아가는 동안 진행 방향으로 늘어남
FX.dotMatch=(g,t,t0,{from,to,dur=.5,color='#F4CE62'}={})=>{const u=cl((t-t0)/dur);if(t<t0)return;const p=eio(u),x=mix(from.x,to.x,p),y=mix(from.y,to.y,p),r=mix(from.r,to.r,p),v=Math.sin(u*PI),an=Math.atan2(to.y-from.y,to.x-from.x);
 if(u<1&&u>0)FX.fast(t0,t0+dur);g.save();g.translate(x,y);g.rotate(an);g.scale(1+.6*v,1-.25*v);g.fillStyle=color;g.beginPath();g.arc(0,0,r,0,7);g.fill();g.restore();FX.mark('점매치컷')};

// ③-글자 4종
// 형광반전: 글자 위로 띠가 지나가고, 띠가 덮은 부분만 글자색이 반전(inv). 강조 1색 규칙과 맞음(band=강조색)
// 띠는 둥근 상자로 그려 관문이 '상자 안 글'로 잰다(여백 = 관문 둘레 기준 글자 크기의 0.4 이상: 가로 pad·세로 bh). 띠 위·아래 요소는 띠 끝에서 122px 넘게 띄운다
FX.highlight=(g,t,t0,{text,font='800 140px PL',x=FX.cx,y=FX.cy,ink='#FAF8F3',inv='#0D1424',band='#F4CE62',dur=.4,pad=.42}={})=>{g.save();g.font=font;g.textAlign='center';g.textBaseline='middle';const w=g.measureText(text).width,fs=fs_(font),x0=x-w/2-fs*pad,bw=w+2*fs*pad,bh=fs*1.6;
 g.fillStyle=ink;g.fillText(text,x,y);const p=FX.EZ.in(cl((t-t0)/dur));if(p>0){g.beginPath();g.roundRect(x0,y-bh/2,Math.max(1,bw*p),bh,Math.min(fs*.12,bw*p/2));g.fillStyle=band;g.fill();g.clip();g.fillStyle=inv;const w0=window.__zsBG;window.__zsBG=1;g.fillText(text,x,y);window.__zsBG=w0}g.restore();if(p>0)FX.mark('형광반전')};
// 핵심어뽑기: 한 줄 문장이 보이다가 t0 부터 나머지 낱말은 작아지며 사라지고 key 낱말만 가운데로 와서 커짐(사주 풀이 문장 → 1~2단어)
FX.keyword=(g,t,t0,{text,key,font='800 84px PL',x=FX.cx,y=FX.cy,ink='#FAF8F3',acc='#F4CE62',scale=2.2,dur=.55}={})=>{const ws=String(text).split(' ');g.save();g.font=font;g.textBaseline='middle';g.textAlign='center';
 const spw=g.measureText(' ').width,wd=ws.map(w=>g.measureText(w).width),TW=wd.reduce((a,b)=>a+b,0)+spw*(ws.length-1);let xx=x-TW/2;const p=eio(cl((t-t0)/dur));
 ws.forEach((w,i)=>{const cx_=xx+wd[i]/2;xx+=wd[i]+spw;const isK=w.includes(key);g.save();
  if(isK){g.translate(mix(cx_,x,p),y);g.scale(mix(1,scale,p),mix(1,scale,p));g.fillStyle=p>.5?acc:ink;g.fillText(w,0,0)}
  else{const a=1-cl(p*1.6);if(a>.02){g.globalAlpha=a;g.translate(cx_,y+p*30);g.scale(1-.4*p,1-.4*p);g.fillStyle=ink;g.fillText(w,0,0)}}g.restore()});g.restore();if(p>0)FX.mark('핵심어뽑기')};
// 태그수렴: 흩어진 작은 낱말(tags)이 빨려 들어가듯(ease-in) 가운데로 모이며 사라지고, 그 자리에 큰 문장(text)이 쾅
FX.tagConverge=(g,t,t0,{tags=[],text,font='800 150px PL',tfont='700 54px PL',x=FX.cx,y=FX.cy,ink='#FAF8F3',acc='#F4CE62',dur=.45,seed=3}={})=>{const u=t-t0;if(u<-.6)return;const A=FX.area();g.save();g.textAlign='center';g.textBaseline='middle';
 if(u<dur){window.__zsLoose=1;g.font=tfont;tags.forEach((s,i)=>{const sx=mix(A.x0+80,A.x1-80,H(i*3+seed)),sy=mix(A.y0+60,A.y1-60,H(i*7+seed+1)),a0=cl((u+.6-i*.04)/.2),p=FX.EZ.out(cl(u/dur));
  g.globalAlpha=a0*(1-p);g.fillStyle=i%3?ink:acc;g.fillText(s,mix(sx,x,p),mix(sy,y,p))});window.__zsLoose=0;if(u>0)FX.fast(t0,t0+dur)}
 if(u>=dur*.85){const a=sp(u-dur*.85,18,.55);g.globalAlpha=1;g.font=font;g.fillStyle=ink;g.translate(x,y);g.scale(mix(1.4,1,cl(a)),mix(1.4,1,cl(a)));g.fillText(text,0,0)}g.restore();if(u>=0)FX.mark('태그수렴')};
// 마스크상승: 줄마다 자기 줄 칸 안에서 아래→위로 올라오며 기울기가 바로 섬(stagger 로 줄 차례)
FX.maskRise=(g,t,t0,{lines=[],font='800 120px PL',x=FX.cx,y=FX.cy,lh=1.25,ink='#FAF8F3',dur=.45,stagger=FX.MOTION.stagger,tilt=-.12,colors=null}={})=>{const fs=fs_(font),n=lines.length;g.save();g.font=font;g.textAlign='center';g.textBaseline='middle';
 lines.forEach((s,i)=>{const p=FX.EZ.in(cl((t-t0-i*stagger)/dur));if(p<=0)return;const yy=y+(i-(n-1)/2)*fs*lh;g.save();g.beginPath();g.rect(0,yy-fs*.62,W_(),fs*1.24);g.clip();
  g.translate(x,yy+(1-p)*fs*1.1);g.transform(1,0,tilt*(1-p),1,0,0);g.fillStyle=colors?colors[i]:ink;g.fillText(s,0,0);g.restore()});g.restore();FX.mark('마스크상승')};

// ③-장면 4종
// 스포트라이트: items(12띠 등)를 cols 칸 격자로 깔고, t0+lift 에 pick 하나만 떠오르고(크기·골드 원판) 나머지는 어두워짐
FX.spotlight=(g,t,t0,{items=[],pick=0,cols=4,font='800 64px PL',ink='#FAF8F3',acc='#F4CE62',on='#0D1424',lift=.7,area=null,dim=.22}={})=>{const A=area||FX.area(),rows=Math.ceil(items.length/cols),cw=(A.x1-A.x0)/cols,ch=Math.min(200,(A.y1-A.y0)/rows),y0=(A.y0+A.y1)/2-rows*ch/2;
 const L=sp(t-t0-lift,14,.6);g.save();g.font=font;g.textAlign='center';g.textBaseline='middle';
 items.forEach((s,i)=>{const a=cl(sp(t-t0-i*.04,18,.7));if(a<=0)return;const cx_=A.x0+(i%cols+.5)*cw,cy_=y0+(Math.floor(i/cols)+.5)*ch,me=i===pick;g.save();
  if(me&&L>0){g.translate(cx_,cy_-14*cl(L));const k=1+.3*L;g.scale(k,k);g.fillStyle=acc;g.beginPath();g.arc(0,0,Math.min(cw,ch)*.46,0,7);g.globalAlpha=cl(L);g.fill();g.globalAlpha=1;g.fillStyle=on;g.fillText(s,0,0)}
  else{g.globalAlpha=a*(L>0?mix(1,dim,cl(L)):1);g.translate(cx_,cy_+(1-a)*30);g.fillStyle=ink;g.fillText(s,0,0)}g.restore()});g.restore();FX.mark('스포트라이트')};
// 원형글자링: 낱말들이 원 둘레에 서서 천천히 돎. hi 에 든 번호만 강조색. bg=true 면 배경 층(간격 검사 제외 — 정보가 아닌 장식일 때만)
FX.textRing=(g,t,t0,{items=[],x=FX.cx,y=FX.cy,r=330,font='800 58px PL',ink='#FAF8F3',acc='#F4CE62',spin=.25,hi=[],bg=false}={})=>{const a=cl(sp(t-t0,12,.7));if(a<=0)return;const draw=()=>{g.save();g.translate(x,y);g.rotate((t-t0)*spin);g.font=font;g.textAlign='center';g.textBaseline='middle';
 items.forEach((s,i)=>{const an=i/items.length*2*PI-PI/2;g.save();g.rotate(an);g.translate(0,-r*mix(.6,1,a));g.globalAlpha=a;g.fillStyle=hi.includes(i)?acc:ink;g.fillText(s,0,0);g.restore()});g.restore()};bg?FX.layerBG(g,draw):draw();FX.mark('원형글자링')};
// 링탈출: n겹 동심원 안의 공이 튀며 고리를 하나씩 깨고 밖으로(12달·한 해 은유). step 초마다 한 겹. 깨진 고리는 커지며 사라짐
FX.ringEscape=(g,t,t0,{n=12,x=FX.cx,y=FX.cy,r0=60,dr=26,step=.25,color='#FAF8F3',ball='#F4CE62',br=18}={})=>{const u=t-t0;if(u<0)return;const k=Math.floor(u/step),f=(u%step)/step;g.save();g.lineCap='round';
 for(let i=0;i<n;i++){const R=r0+i*dr;if(i<k){const q=u-(i+1)*step;if(q>.3)continue;g.globalAlpha=1-q/.3;g.strokeStyle=color;g.lineWidth=4;g.beginPath();g.arc(x,y,R+q*120,0,7);g.stroke();g.globalAlpha=1;continue}
  const gap=.5,base=i*1.3+u*.6;g.strokeStyle=color;g.lineWidth=4;g.beginPath();g.arc(x,y,R,base+gap,base+2*PI-gap);g.stroke()}
 const R=r0+Math.min(k,n)*dr-dr*.5,bounce=Math.abs(Math.sin(f*PI))*dr*.45,an=u*7;g.fillStyle=ball;g.beginPath();g.arc(x+Math.cos(an)*(R+bounce),y+Math.sin(an)*(R+bounce),br,0,7);g.fill();g.restore();FX.mark('링탈출')};
// 질문답하기: pairs=[[질문,답],…] 를 step 초마다 하나씩. 질문이 마스크상승으로 서고, 답이 형광반전으로 붙음. 앞 쌍은 위로 밀리며 흐려짐
FX.qa=(g,t,t0,{pairs=[],x=FX.cx,y=FX.cy,step=1.4,qfont='800 96px PL',afont='800 110px PL',ink='#FAF8F3',acc='#F4CE62',inv='#0D1424',gap=1.1}={})=>{const u=t-t0;if(u<0)return;const i=Math.min(pairs.length-1,Math.floor(u/step)),lu=u-i*step,qf=fs_(qfont);
 if(i>0){const [pq,pa]=pairs[i-1],p=eio(cl(lu/.35));g.save();g.globalAlpha=1-p;g.translate(0,-p*160);g.font=qfont;g.textAlign='center';g.textBaseline='middle';g.fillStyle=ink;g.fillText(pq,x,y-qf*gap*.5);g.font=afont;g.fillStyle=acc;g.fillText(pa,x,y+qf*gap*.6);g.restore()}
 const [q,a]=pairs[i];FX.maskRise(g,t,t0+i*step+.1,{lines:[q],font:qfont,x,y:y-qf*gap*.5,ink});if(lu>.55)FX.highlight(g,t,t0+i*step+.6,{text:a,font:afont,x,y:y+qf*gap*.6,ink,inv,band:acc});FX.mark('질문답하기')};

FX.LIST=Object.assign(FX.LIST,{'카메라층':'장면 안 1~3% 드리프트·타격 줌 펀치·흔들림·상태 확대(K-294)','대각선와이프':'굵은 사선 띠가 지나간 자리에 다음 장면(K-294)','휩팬':'빠른 팬+넘어가는 순간만 잔상(K-294)',
 '글자창전환':'큰 글자 안에 다음 장면이 비치고 글자가 커져 화면이 됨(K-294)','글자셔터':'큰 글자가 세로 판으로 갈라져 열림(K-294)','점매치컷':'골드 점 하나가 다음 장면의 동그라미로(K-294)',
 '형광반전':'띠가 지나간 글자만 색 반전(K-294)','핵심어뽑기':'문장에서 핵심 낱말만 남아 커짐(K-294)','태그수렴':'흩어진 낱말이 빨려 들어가고 큰 문장 쾅(K-294)','마스크상승':'줄마다 칸 안에서 올라오며 기울기가 섬(K-294)',
 '스포트라이트':'격자 중 하나만 떠오르고 나머지 어두워짐(K-294)','원형글자링':'낱말이 원 둘레에 서서 돎(K-294)','링탈출':'공이 동심원을 하나씩 깨고 밖으로(K-294)','질문답하기':'질문이 서고 답이 형광으로 붙음, 차례로(K-294)'});
FX.USE['전환']=['원와이프','대각선와이프','휩팬','글자창전환','글자셔터','점매치컷'];
FX.USE['훅(첫 1초)'].push('태그수렴','글자셔터');FX.USE['개념 설명'].push('형광반전','핵심어뽑기','마스크상승','질문답하기');FX.USE['관계·궁합'].push('스포트라이트','원형글자링');FX.USE['감성·신비'].push('링탈출','점매치컷');FX.USE['끝장면(행동)'].push('형광반전');
FX.USE['모든 장면(기본)']=['카메라층'];
})();

// 프롬프트 100 기법(motion_fx100.js)을 같이 불러온다 — 페이지는 motion_fx.js 하나만 넣으면 된다
(function(){if(typeof document!=='undefined'&&document.currentScript&&document.readyState==='loading'){document.write('<script src="'+document.currentScript.src.replace(/[^/]*$/,'')+'motion_fx100.js"><\/script>')}})();
