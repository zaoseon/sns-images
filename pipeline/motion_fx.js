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
FX.stack=(g,t,t0,{word,x=540,y0=480,dy=150,n=6,step=.25,font='900 170px PL',color='#FF4F9A',fill='#FF4F9A'})=>{
 g.save();g.font=font;g.textAlign='center';g.textBaseline='middle';g.lineWidth=4;g.lineJoin='round';
 for(let i=0;i<n;i++){const a=sp(t-t0-i*step,16,.65);if(a<=0)continue;const y=y0+i*dy;
  g.globalAlpha=cl(a*3);g.save();g.translate(x,y+(1-a)*60);g.scale(1,cl(a,0,1.2));
  if(i==n-1){g.fillStyle=fill;g.fillText(word,0,0)}else{g.strokeStyle=color;g.strokeText(word,0,0)}g.restore()}
 g.restore()};
// 슬롯롤링: 창(x,y,w,h) 안에서 words 가 굴러가다 stop 시각에 target 에서 멈춤
FX.slot=(g,t,t0,t1,{words,target,x=540,y=960,h=260,font='900 220px PL',color='#171717',loops=3})=>{
 const n=words.length, ti=words.indexOf(target), total=loops*n+ti, p=t>=t1?1:eio(cl((t-t0)/(t1-t0)));
 let pos=p*total; if(t>=t1){pos=total-Math.sin((t-t1)*18)*Math.exp(-(t-t1)*7)*.15}
 g.save();g.beginPath();g.rect(0,y-h/2,1080,h);g.clip();g.font=font;g.textAlign='center';g.textBaseline='middle';g.fillStyle=color;
 for(let k=Math.floor(pos)-1;k<=Math.floor(pos)+1;k++){const w=words[((k%n)+n)%n];g.fillText(w,x,y+(k-pos)*h)}g.restore()};
// 점파동: 격자 점, 중심들에서 물결
FX.dotwave=(g,t,t0,{cols=13,rows=20,x0=90,y0=420,gap=75,centers=[[540,960]],color='rgba(255,255,255,.55)',r0=5,amp=9})=>{
 g.save();g.fillStyle=color;const T=t-t0;
 for(let j=0;j<rows;j++)for(let i=0;i<cols;i++){const x=x0+i*gap,y=y0+j*gap;let w=0;
  centers.forEach(([cx,cy],k)=>{const d=Math.hypot(x-cx,y-cy),f=T*900-k*450-d;if(f>0)w+=Math.max(0,Math.sin(f/90))*Math.exp(-f/900)});
  const a=sp(T-(i+j)*.012,14,.8);g.beginPath();g.arc(x,y,Math.max(0,(r0+amp*w)*a),0,7);g.fill()}g.restore()};
// 궤도링: 진행 비율 p(0~1)
FX.ring=(g,t,{x=540,y=900,r=300,p=0,color='#FF4F9A',track='rgba(0,0,0,.08)',dots=10})=>{
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
FX.loaderLine=(g,t,t0,{x=540,y=960,w=800,color='#fff'})=>{const T=t-t0;if(T<0)return;g.save();g.strokeStyle=color;g.lineWidth=8;g.lineCap='round';
 if(T<.7){g.beginPath();g.arc(x,y,40,T*9,T*9+4.2);g.stroke()}else{const p=eio((T-.7)/.5);g.beginPath();g.moveTo(x-w/2*p,y);g.lineTo(x+w/2*p,y);g.stroke()}g.restore()};
FX.dotLand=(g,t,t0,{x=900,y=1000,r=34,color='#FF7A1A',h=500})=>{const T=t-t0;if(T<0)return;let yy,sx=1,sy=1;
 if(T<.35){const p=T/.35;yy=y-h*(1-p*p)}else{const u=T-.35,b=Math.abs(Math.sin(u*14))*Math.exp(-u*5)*120;yy=y-b;const sq=Math.exp(-u*6)*Math.cos(u*28)*.35;sx=1+sq;sy=1-sq}
 g.save();g.fillStyle=color;g.translate(x,yy+r);g.scale(sx,sy);g.beginPath();g.arc(0,-r,r,0,7);g.fill();g.restore()};
FX.pixelBlocks=(g,t,t0,{x=90,y=700,cols=9,rows=5,s=100,color='#111'})=>{for(let j=0;j<rows;j++)for(let i=0;i<cols;i++){const k=j*cols+i,d=t0+H(k)*.8,p=cl((t-d)/.35);if(p<=0)continue;
 const yy=mix(y+j*s-600,y+j*s,ez.outq(p));g.fillStyle=color;g.globalAlpha=H(k+5)>.25?1:.4;g.fillRect(x+i*s+4,yy+4,s-8,s-8)}g.globalAlpha=1};
FX.dict=(g,t,t0,{word,sub,x=540,y=900,color='#111',font='900 220px PL',sfont='italic 400 48px SR'})=>{const a=sp(t-t0,14,.7);g.save();g.fillStyle=color;g.textAlign='center';g.textBaseline='middle';
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
FX.vortex=(g,t,t0,{n=1500,x=540,y=900,R=330,target=null,tGather=1.2,color='rgba(255,240,220,.85)'})=>{const T=t-t0;if(T<0)return;g.fillStyle=color;
 for(let i=0;i<n;i++){const h=H(i),h2=H(i+71),a=h*6.283+T*(1.5+h2),rr=R*(.75+.35*h2)+Math.sin(T*3+i)*12;let px=x+Math.cos(a)*rr,py=y+Math.sin(a)*rr*.9;
  if(target){const q=target[i%target.length],p=ez.io(cl((T-tGather-h*.4)/.8));px=mix(px,q[0],p);py=mix(py,q[1],p)}g.fillRect(px,py,3,3)}};
FX.dot3D=(g,t,{kind='sphere',x=540,y=900,R=330,rot=0,tilt=.5,n=900,color='#fff'})=>{const ps=[];
 for(let i=0;i<n;i++){let X,Y,Z;const u=H(i)*6.283,v=H(i+9);
  if(kind=='sphere'){const ph=Math.acos(2*v-1);X=Math.sin(ph)*Math.cos(u);Y=Math.cos(ph);Z=Math.sin(ph)*Math.sin(u)}
  else if(kind=='torus'){const w=v*6.283;X=(1+.38*Math.cos(w))*Math.cos(u)*.72;Z=(1+.38*Math.cos(w))*Math.sin(u)*.72;Y=.38*Math.sin(w)*.72}
  else{const gx=(i%30)/29*2-1,gz=Math.floor(i/30)/29*2-1;X=gx;Z=gz;Y=Math.sin(gx*3+rot*2)*Math.cos(gz*3)*.25}
  const c=Math.cos(rot),s=Math.sin(rot);[X,Z]=[X*c-Z*s,X*s+Z*c];const ct=Math.cos(tilt),st=Math.sin(tilt);[Y,Z]=[Y*ct-Z*st,Y*st+Z*ct];ps.push([X,Y,Z])}
 ps.sort((a,b)=>a[2]-b[2]);ps.forEach(([X,Y,Z])=>{const k=1/(1.8-Z*.6);g.globalAlpha=cl(.25+(Z+1)*.38);g.fillStyle=color;g.beginPath();g.arc(x+X*R*k,y+Y*R*k,2.2*k*1.4,0,7);g.fill()});g.globalAlpha=1};
FX.tunnel=(g,t,{x=540,y=900,n=90,color='rgba(255,255,255,.55)',r0=110})=>{g.save();g.strokeStyle=color;g.lineWidth=2;for(let i=0;i<n;i++){const a=i*6.283/n+t*.15,L=900+H(i)*500,ph=((t*1.4+H(i+3))%1);
 const r1=r0+ph*L*.3,r2=r1+120+H(i+5)*220;g.beginPath();g.moveTo(x+Math.cos(a)*r1,y+Math.sin(a)*r1);g.lineTo(x+Math.cos(a)*r2,y+Math.sin(a)*r2);g.stroke()}
 g.fillStyle='#000';g.beginPath();g.arc(x,y,r0,0,7);g.fill();g.restore()};
FX.stateBtn=(g,t,{x=540,y=1300,w=640,h=130,states,times,colors,font='900 54px PL'})=>{let k=0;times.forEach((tt,i)=>{if(t>=tt)k=i});const press=times.some(tt=>t>=tt&&t<tt+.12)?.94:1;
 g.save();g.translate(x,y);g.scale(press,press);g.fillStyle=colors[k][0];g.beginPath();g.roundRect(-w/2,-h/2,w,h,h/2);g.fill();g.fillStyle=colors[k][1];g.font=font;g.textAlign='center';g.textBaseline='middle';g.fillText(states[k],0,3);g.restore()};
FX.chips=(g,t,t0,{labels,x=90,y=1200,gap=18,font='800 36px PR',bg='#fff',fg='#111'})=>{g.save();g.font=font;let cx=x,cy=y;labels.forEach((l,i)=>{const w=g.measureText(l).width+48;if(cx+w>990){cx=x;cy+=80}
 const s=sp(t-t0-i*.12,16,.55);if(s>0){g.save();g.translate(cx+w/2,cy+30);g.scale(s,s);g.fillStyle=bg;g.beginPath();g.roundRect(-w/2,-30,w,60,30);g.fill();g.fillStyle=fg;g.textAlign='center';g.textBaseline='middle';g.fillText(l,0,2);g.restore()}cx+=w+gap});g.restore()};
FX.annot=(g,t,t0,{from,to,text,color='#E53935',font='italic 400 46px SR'})=>{const p=eio((t-t0)/.5);if(p<=0)return;g.save();g.strokeStyle=color;g.lineWidth=5;g.lineCap='round';
 const mx=(from[0]+to[0])/2+40,my=(from[1]+to[1])/2-50,N=20;g.beginPath();for(let i=0;i<=N*p;i++){const u=i/N,X=(1-u)*(1-u)*from[0]+2*u*(1-u)*mx+u*u*to[0],Y=(1-u)*(1-u)*from[1]+2*u*(1-u)*my+u*u*to[1];i?g.lineTo(X,Y):g.moveTo(X,Y)}g.stroke();
 if(p>.95){const a=Math.atan2(to[1]-my,to[0]-mx);g.beginPath();g.moveTo(to[0],to[1]);g.lineTo(to[0]-22*Math.cos(a-.5),to[1]-22*Math.sin(a-.5));g.moveTo(to[0],to[1]);g.lineTo(to[0]-22*Math.cos(a+.5),to[1]-22*Math.sin(a+.5));g.stroke()}
 g.fillStyle=color;g.font=font;g.globalAlpha=cl((t-t0-.3)/.2);g.fillText(text,from[0]-10,from[1]-14);g.restore()};
FX.ball=(g,t,t0,{x0=150,x1=930,yb=1250,r=46,color='#2F6BFF',hops=3,dur=2})=>{const T=cl((t-t0)/dur);if(t<t0)return;const x=mix(x0,x1,ez.io(T)),ph=(T*hops)%1,h=420*Math.exp(-T*1.2);
 const y=yb-r-h*4*ph*(1-ph),vy=Math.abs(1-2*ph),near=ph<.08||ph>.92;const sx=near?1.35:1-vy*.0+(.15*(1-vy)),sy=near?.68:1+.18*vy;
 g.save();g.strokeStyle='rgba(0,0,0,.25)';g.lineWidth=3;g.beginPath();g.moveTo(80,yb);g.lineTo(1000,yb);g.stroke();g.translate(x,near?yb-r*sy:y);g.scale(sx,sy);g.fillStyle=color;g.beginPath();g.arc(0,0,r,0,7);g.fill();g.restore()};
FX.stagger=(g,t,t0,{word,x=540,y=900,font='900 170px PL',color='#111',step=.07})=>{g.save();g.font=font;g.textBaseline='middle';const W=g.measureText(word).width;let cx=x-W/2;
 [...word].forEach((ch,i)=>{const w=g.measureText(ch).width,a=sp(t-t0-i*step,13,.6);if(a>0){g.save();g.translate(cx+w/2,y+(1-a)*140);g.rotate((1-a)*-.5);g.globalAlpha=cl(a*2);g.fillStyle=color;g.textAlign='center';g.fillText(ch,0,0);g.restore()}cx+=w});g.restore()};
FX.verb=(g,t,t0,{word,act,x=540,y=960,font='900 210px PL',color='#fff'})=>{const T=t-t0;if(T<0)return;g.save();g.font=font;g.textAlign='center';g.textBaseline='middle';g.fillStyle=color;g.translate(x,y);
 if(act=='bounce'){g.translate(0,-Math.abs(Math.sin(T*7))*Math.exp(-T*2)*220);const q=Math.exp(-T*3)*.25*Math.abs(Math.cos(T*7));g.scale(1+q,1-q)}
 else if(act=='stretch'){const s=1+Math.sin(cl(T/.6)*Math.PI)*.5+(sp(T-.6,12,.4)-1)*.3;g.scale(s,1/Math.sqrt(s))}
 else if(act=='spin'){g.rotate(ez.back(cl(T/.9))*Math.PI*2.5)}
 g.fillText(word,0,0);g.restore()};
FX.easeGraph=(g,t,t0,{x=140,y=1250,w=800,h=560,c1='#E53935',c2='#2F6BFF'})=>{const p=cl((t-t0)/1.2);g.save();g.strokeStyle='rgba(0,0,0,.3)';g.lineWidth=3;g.beginPath();g.moveTo(x,y-h);g.lineTo(x,y);g.lineTo(x+w,y);g.stroke();
 [[c1,ez.lin],[c2,ez.io]].forEach(([c,f],k)=>{if(k==1&&t<t0+.6)return;const q=k?cl((t-t0-.6)/1.2):p;g.strokeStyle=c;g.lineWidth=7;g.beginPath();for(let i=0;i<=60*q;i++){const u=i/60;i?g.lineTo(x+u*w,y-f(u)*h):g.moveTo(x,y)}g.stroke();
  g.fillStyle=c;g.beginPath();g.arc(x+q*w,y-f(q)*h,14,0,7);g.fill()});g.restore()};
FX.morphBox=(g,t,t0,dur,A,B,{x=540,y=960,color='#111'})=>{const p=sp(t-t0,9,.8),pp=cl(p);const w=mix(A[0],B[0],p),h=mix(A[1],B[1],p),r=mix(A[2],B[2],pp);g.fillStyle=color;g.beginPath();g.roundRect(x-w/2,y-h/2,w,h,Math.min(r,w/2,h/2));g.fill()};
FX.slider=(g,{x=190,y=960,w=700,p=.3,fg='#fff',bg='rgba(255,255,255,.25)',knob=true})=>{g.save();g.lineCap='round';g.lineWidth=14;g.strokeStyle=bg;g.beginPath();g.moveTo(x,y);g.lineTo(x+w,y);g.stroke();
 g.strokeStyle=fg;g.beginPath();g.moveTo(x,y);g.lineTo(x+w*p,y);g.stroke();if(knob){g.fillStyle=fg;g.beginPath();g.arc(x+w*p,y,22,0,7);g.fill()}g.restore()};
FX.toggle=(g,{x=540,y=960,p=0,on='#111',off='#ccc'})=>{const w=260,h=140;g.save();g.fillStyle=p>.5?on:off;g.beginPath();g.roundRect(x-w/2,y-h/2,w,h,h/2);g.fill();
 g.fillStyle='#fff';g.beginPath();g.arc(mix(x-w/2+h/2,x+w/2-h/2,ez.back(cl(p))),y,h/2-12,0,7);g.fill();g.restore()};
FX.tabs=(g,{x=540,y=960,labels=['일','주','월'],p=0,font='800 44px PR',w=760})=>{const n=labels.length,cw=w/n;g.save();g.fillStyle='#fff';g.beginPath();g.roundRect(x-w/2,y-55,w,110,55);g.fill();
 g.fillStyle='#111';g.beginPath();g.roundRect(x-w/2+p*cw+8,y-47,cw-16,94,47);g.fill();g.font=font;g.textAlign='center';g.textBaseline='middle';
 labels.forEach((l,i)=>{g.fillStyle=Math.abs(p-i)<.5?'#fff':'#888';g.fillText(l,x-w/2+cw*(i+.5),y+2)});g.restore()};
FX.palette=(g,t,t0,{x=140,y=700,w=800,query,items,font='800 44px PR'})=>{const n=Math.floor(cl((t-t0)/.9)*query.length),q=query.slice(0,n);const vis=items.filter(s=>s.includes(q));
 g.save();g.fillStyle='#fff';g.beginPath();g.roundRect(x,y,w,140+vis.length*96,32);g.fill();g.fillStyle='#111';g.font=font;g.textBaseline='middle';g.fillText('⌕  '+q+((Math.floor(t*4)%2)?'|':''),x+40,y+70);
 vis.forEach((s,i)=>{g.fillStyle=i==0?'#F2F2F2':'#fff';g.beginPath();g.roundRect(x+20,y+130+i*96,w-40,84,18);g.fill();g.fillStyle='#333';g.fillText(s,x+50,y+172+i*96)});g.restore()};
FX.toast=(g,t,t0,{text,x=540,y=1350,font='800 46px PR',color='#111'})=>{const a=sp(t-t0,14,.65);if(a<=0)return;g.save();g.font=font;const w=g.measureText(text).width+150;g.translate(x,y+(1-a)*80);g.globalAlpha=cl(a*2);
 g.fillStyle=color;g.beginPath();g.roundRect(-w/2,-55,w,110,55);g.fill();g.fillStyle='#3DDC84';g.beginPath();g.arc(-w/2+60,0,24,0,7);g.fill();g.strokeStyle='#fff';g.lineWidth=6;g.beginPath();g.moveTo(-w/2+48,0);g.lineTo(-w/2+57,10);g.lineTo(-w/2+73,-10);g.stroke();
 g.fillStyle='#fff';g.textBaseline='middle';g.fillText(text,-w/2+100,2);g.restore()};
FX.split=(g,t,{top,bottom,y=960,color='#fff',font='800 40px PR'})=>{g.save();g.strokeStyle=color;g.lineWidth=4;g.beginPath();g.moveTo(0,y);g.lineTo(1080*cl(t),y);g.stroke();g.fillStyle=color;g.font=font;g.fillText(top,90,y-30);g.fillText(bottom,90,y+60);g.restore()};
FX.wordBlocks=(g,t,t0,{words,colors,step=.5,y=0,h=1920,font='900 230px PL',fg='#fff'})=>{const k=Math.max(0,Math.min(words.length-1,Math.floor((t-t0)/step)));const a=sp(t-t0-k*step,16,.55);
 g.fillStyle=colors[k%colors.length];g.fillRect(0,y,1080,h);g.save();g.fillStyle=fg;g.font=font;{const m=g.measureText(words[k]).width;if(m>960){const px=parseFloat(font.match(/(\d+)px/)[1])*960/m;g.font=font.replace(/\d+px/,Math.floor(px)+'px')}}g.textAlign='center';g.textBaseline='middle';g.translate(540,y+h/2);g.scale(mix(1.25,1,a),mix(1.25,1,a));g.fillText(words[k],0,0);g.restore()};
FX.counterRush=(g,t,t0,{to=999,dur=1.6,x=540,y=900,font='900 230px PL',color='#fff',plus='+',streak=['your agent','motion','one key','skills']})=>{const T=t-t0;if(T<0)return;
 g.save();g.font='800 30px PR';for(let i=0;i<26;i++){const h=H(i+40),sx=((T*(500+h*900)+h*1400)%1500)-200,sy=500+H(i+90)*900;g.fillStyle=`rgba(255,255,255,${.12+.2*h})`;g.fillText(streak[i%streak.length],1080-sx,sy)}
 const v=Math.round(to*ez.inq(cl(T/dur)));g.font=font;g.textAlign='center';g.textBaseline='middle';g.fillStyle=color;g.fillText(v.toLocaleString()+(T>=dur?plus:''),x,y);g.restore()};
FX.ripples=(g,t,t0,{x=540,y=900,n=6,color='255,255,255',core='#FF7A1A'})=>{const T=t-t0;if(T<0)return;for(let i=0;i<n;i++){const p=((T*.7+i/n)%1);g.strokeStyle=`rgba(${color},${(1-p)*.6})`;g.lineWidth=4;g.beginPath();g.arc(x,y,40+p*700,0,7);g.stroke()}
 g.fillStyle=core;g.beginPath();g.arc(x,y,30+Math.sin(T*6)*4,0,7);g.fill()};
FX.hub=(g,t,t0,{x=540,y=920,nodes,R=330,color='#FF7A1A',fg='#fff',font='800 38px PR'})=>{g.save();nodes.forEach((nd,i)=>{const a=-Math.PI/2+i*6.283/nodes.length,nx=x+Math.cos(a)*R,ny=y+Math.sin(a)*R,p=eio((t-t0-.3-i*.15)/.4);if(p<=0)return;
 g.strokeStyle=color;g.globalAlpha=.7;g.lineWidth=4;g.beginPath();g.moveTo(x,y);g.lineTo(mix(x,nx,p),mix(y,ny,p));g.stroke();g.globalAlpha=1;
 if(p>=1){const s=sp(t-t0-.7-i*.15,16,.6);g.save();g.translate(nx,ny);g.scale(s,s);g.fillStyle='#1b1b1b';g.beginPath();g.roundRect(-110,-55,220,110,24);g.fill();g.fillStyle=fg;g.font=font;g.textAlign='center';g.textBaseline='middle';
  g.fillText(nd[0],0,-14);g.fillStyle=color;g.fillText(Math.round(nd[1]*cl((t-t0-.9-i*.15)/.8)).toLocaleString()+(nd[2]||''),0,26);g.restore()}});
 const s=sp(t-t0,14,.6);g.fillStyle=color;g.beginPath();g.roundRect(x-80*s,y-80*s,160*s,160*s,36*s);g.fill();g.restore()};
FX.assemble=(g,t,t0,{pieces,color='#FF7A1A'})=>{pieces.forEach((pc,i)=>{const [x,y,w,h]=pc,a=sp(t-t0-i*.06,12,.7),fx=x+(H(i)-.5)*1400,fy=y+(H(i+3)-.5)*1600;g.save();g.globalAlpha=cl(a*3);g.fillStyle=color;
 g.translate(mix(fx,x,a),mix(fy,y,a));g.rotate((1-a)*(H(i+7)-.5)*4);g.fillRect(-w/2,-h/2,w,h);g.restore()})};
FX.starBurst=(g,t,t0,{x=540,y=900,n=16,L=260,color='#FF4A3D',ring='',font='800 30px PR'})=>{const T=t-t0;if(T<0)return;const p=sp(T-.2,10,.6);g.save();g.strokeStyle=color;g.lineWidth=10;g.lineCap='round';
 for(let i=0;i<n;i++){const a=i*6.283/n+T*.4;g.beginPath();g.moveTo(x,y);g.lineTo(x+Math.cos(a)*L*p,y+Math.sin(a)*L*p);g.stroke()}g.fillStyle=color;g.beginPath();g.arc(x,y,18,0,7);g.fill();
 if(ring){g.font=font;g.fillStyle=color;const N=ring.length;for(let i=0;i<N;i++){const a=-T*.6+i*6.283/N;g.save();g.translate(x+Math.cos(a)*(L+90),y+Math.sin(a)*(L+90));g.rotate(a+Math.PI/2);g.globalAlpha=cl((T-.6)/.3);g.fillText(ring[i],0,0);g.restore()}}g.restore()};
FX.stretchWord=(g,t,t0,{word,x=540,y=900,font='900 200px PL',color='#111'})=>{const p=sp(t-t0,8,.8);g.save();g.font=font;g.textBaseline='middle';const n=word.length,ws=[...word].map(c=>g.measureText(c).width),W=ws.reduce((a,b)=>a+b,0),sp2=mix(-10,(1000-W)/(n-1),cl(p));
 let cx=x-(W+sp2*(n-1))/2;g.fillStyle=color;[...word].forEach((c,i)=>{g.fillText(c,cx,y);cx+=ws[i]+sp2});g.restore()};
FX.easeRows=(g,t,t0,{x=200,y=600,w=760,gap=120,dur=1.4,colors=['#111','#2F6BFF','#E53935']})=>{const names=[['직선','lin'],['천천히 시작','inq'],['천천히 멈춤','outq'],['둘 다','io'],['넘쳤다 돌아옴','back'],['통통','el']];
 g.save();g.font='800 34px PR';names.forEach(([nm,k],i)=>{const yy=y+i*gap;g.fillStyle='#666';g.fillText(nm,90,yy-34);g.strokeStyle='rgba(0,0,0,.15)';g.lineWidth=3;g.beginPath();g.moveTo(x,yy);g.lineTo(x+w,yy);g.stroke();
  const p=ez[k](cl((t-t0)/dur));g.fillStyle=colors[i%colors.length];g.beginPath();g.arc(x+w*p,yy,20,0,7);g.fill()});g.restore()};
FX.truchet=(g,t,t0,{cell=90,c1='#111',c2='#fff',c3='#FF4A3D'})=>{const cols=Math.ceil(1080/cell),rows=Math.ceil(1920/cell),sweep=(t-t0)*900;g.save();g.lineWidth=cell*.28;g.lineCap='butt';
 for(let j=0;j<rows;j++)for(let i=0;i<cols;i++){const x=i*cell,y=j*cell,a=sp(t-t0-(i+j)*.015,12,.7);if(a<=0)continue;g.fillStyle=c1;g.fillRect(x,y,cell,cell);g.strokeStyle=(x+y)<sweep?c3:c2;g.globalAlpha=cl(a);
  const f=H(i*97+j)>.5;g.beginPath();if(f){g.arc(x,y,cell/2,0,Math.PI/2);g.moveTo(x+cell,y+cell/2);g.arc(x+cell,y+cell,cell/2,-Math.PI/2,-Math.PI,true)}else{g.arc(x+cell,y,cell/2,Math.PI/2,Math.PI);g.moveTo(x+cell/2,y+cell);g.arc(x,y+cell,cell/2,0,-Math.PI/2,true)}g.stroke()}g.restore()};
FX.asterisk=(g,t,{x=540,y=900,r=90,color='#111',n=8})=>{g.save();g.translate(x,y);g.rotate(t*1.4);g.strokeStyle=color;g.lineWidth=r*.28;g.lineCap='round';for(let i=0;i<n;i++){g.rotate(Math.PI/n);g.beginPath();g.moveTo(-r,0);g.lineTo(r,0);g.stroke()}g.restore()};
FX.videoWall=(g,t,{rows=3,y=560,h=260,w=340,gap=24,speed=120,cards=[],font='900 56px PL'})=>{g.save();for(let j=0;j<rows;j++){const off=((t*speed*(j%2?-1:1))%(w+gap)+(w+gap))%(w+gap);
 for(let i=-1;i<5;i++){const x=i*(w+gap)+off-(j%2?0:w/2),k=(i+j*5+50)%Math.max(1,cards.length),c=cards[k]||['#222',''];g.fillStyle=c[0];g.beginPath();g.roundRect(x,y+j*(h+gap),w,h,22);g.fill();
  g.fillStyle=c[2]||'#fff';g.font=font;g.textAlign='center';g.textBaseline='middle';g.fillText(c[1],x+w/2,y+j*(h+gap)+h/2)}}g.restore()};

FX.LIST['액체방울']='#11 크롬 같은 방울이 흐르며 글자 띠 뒤로 지나감(셰이더 대신 겹친 원 그라데이션)';
FX.LIST['빛덩이']='#20 번지는 빛 덩이가 화면을 가로지름';
FX.blobs=(g,t,{n=5,colors=[['#FF4A3D','#FFD27A'],['#2F2FE0','#9BE7FF'],['#111','#C6FF3D']],R=170})=>{for(let i=0;i<n;i++){const h=H(i+11),x=540+Math.sin(t*(.6+h)+i*2)*360,y=950+Math.cos(t*(.5+h*.6)+i)*560,r=R*(.7+h*.6),c=colors[i%colors.length];
 const gr=g.createRadialGradient(x-r*.35,y-r*.35,r*.1,x,y,r);gr.addColorStop(0,'#fff');gr.addColorStop(.25,c[1]);gr.addColorStop(.8,c[0]);gr.addColorStop(1,'#000');g.fillStyle=gr;g.beginPath();g.arc(x,y,r,0,7);g.fill()}};
FX.glowOrb=(g,t,t0,{y=960,r=240,color='255,255,255',dur=1.4})=>{const p=eio(cl((t-t0)/dur)),x=mix(-r,1080+r,p),gr=g.createRadialGradient(x,y,0,x,y,r);gr.addColorStop(0,`rgba(${color},.95)`);gr.addColorStop(1,`rgba(${color},0)`);g.fillStyle=gr;g.beginPath();g.arc(x,y,r,0,7);g.fill()};
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
FX.circleWipe=(g,t,t0,{x=540,y=960,color='#FFD600',dur=.4})=>{const p=eio(cl((t-t0)/dur));if(p<=0)return;g.fillStyle=color;g.beginPath();g.arc(x,y,p*2300,0,7);g.fill()};
FX.shapeGrid=(g,t,t0,{cols=3,rows=4,x0=270,y0=560,dx=270,dy=230,s=75,seq=['circle','square','plus'],hl=[],color='#1E2A55',hlColor='#0F1730',labels=null,font='900 44px PL',fg='#fff'})=>{
 for(let i=0;i<cols*rows;i++){const cx=x0+(i%cols)*dx,cy=y0+Math.floor(i/cols)*dy,a=sp(t-t0-i*.035,13,.65);if(a<=0)continue;const big=hl.includes(i)&&t>t0+1.4,ss=s*a*(hl.length&&t>t0+1.4?(big?1.5:.35):1);
  FX.shapeMorph(g,cx,cy,ss,seq,cl((t-t0-.15-i*.035)/.5)*(seq.length-1),{color:big?hlColor:color});if(labels&&ss>40){g.fillStyle=fg;g.font=font;g.textAlign='center';g.textBaseline='middle';g.fillText(labels[i],cx,cy+2)}}};
FX.particleText=(g,t,t0,{target,n,R=900,color='#FFD600',size=7})=>{const N=n||target.length;g.fillStyle=color;for(let i=0;i<N;i++){const q=target[i%target.length],h=H(i),a=sp(t-t0-h*.4,9,.75),ang=h*6.283;g.fillRect(mix(540+Math.cos(ang)*R,q[0],a)-size/2,mix(960+Math.sin(ang)*R,q[1],a)-size/2,size,size)}};
FX.radial=(g,t,{x=540,y=780,n=16,L=1400,w=70,color='rgba(255,214,0,.13)'})=>{g.save();g.translate(x,y);g.rotate(t*.35);g.fillStyle=color;for(let i=0;i<n;i++){g.rotate(6.283/n);g.beginPath();g.moveTo(0,0);g.lineTo(-w,-L);g.lineTo(w,-L);g.fill()}g.restore()};
FX.chat=(g,t,t0,{text,side='l',y=520,font='800 54px PR',bg,fg='#111',maxw=700})=>{const a=sp(t-t0,15,.6);if(a<=0)return;g.save();g.font=font;const lines=String(text).split('\n'),w=Math.min(maxw,Math.max(...lines.map(l=>g.measureText(l).width))+80),h=lines.length*72+50;
 const x=side=='l'?90:1080-90-w;g.translate(side=='l'?x:x+w,y+h);g.scale(a,a);g.translate(side=='l'?0:-w,-h);g.fillStyle=bg||(side=='l'?'#fff':'#FFD93D');g.beginPath();g.roundRect(0,0,w,h,[44,44,side=='l'?44:12,side=='l'?12:44]);g.fill();
 g.fillStyle=fg;g.textBaseline='top';lines.forEach((l,i)=>g.fillText(l,40,25+i*72));g.restore()};
FX.typingDots=(g,t,{x=135,y=568,color='#9AA7BF'})=>{for(let i=0;i<3;i++){g.fillStyle=color;g.beginPath();g.arc(x+i*40,y-Math.max(0,Math.sin(t*8-i*.9))*10,11,0,7);g.fill()}};
FX.bigPop=(g,t,t0,{text,x=540,y=1250,font='900 220px PL',color='#FFD93D',burst='rgba(255,217,61,.22)'})=>{const a=sp(t-t0,18,.5);if(a<=0)return;g.save();g.translate(x,y);g.fillStyle=burst;for(let i=0;i<14;i++){g.rotate(6.283/14);const L=mix(0,700,ease((t-t0)/.4));g.fillRect(-10,-L,20,L*.55)}
 g.rotate(mix(-.2,-.07,a));g.scale(mix(2.2,1,a),mix(2.2,1,a));g.fillStyle=color;g.font=font;g.textAlign='center';g.textBaseline='middle';g.fillText(text,0,0);g.restore()};
FX.pickCards=(g,t,t0,{labels=['1','2'],subs=[],y=900,w=400,h=400,colors=['#FFD93D','#fff'],cycle=.5})=>{const n=labels.length,gap=(1080-180-n*w)/Math.max(1,n-1);labels.forEach((l,i)=>{const a=sp(t-t0-i*.15,15,.55),on=t>t0+.8&&Math.floor((t-t0-.8)/cycle)%n==i;
 if(a<=0)return;const x=90+i*(w+gap);g.save();g.translate(x+w/2,y+h/2);g.scale(a*(on?1.08:1),a*(on?1.08:1));g.fillStyle=colors[i%colors.length];g.beginPath();g.roundRect(-w/2,-h/2,w,h,48);g.fill();
 g.fillStyle='#111';g.textAlign='center';g.textBaseline='middle';g.font=`900 ${Math.round(w*.38)}px PL`;g.fillText(l,0,subs[i]?-40:0);if(subs[i]){g.font=`900 ${Math.round(w*.17)}px PL`;g.fillText(subs[i],0,w*.25)}g.restore()})};
FX.gauge=(g,{x=540,y0=1250,h=780,p=.5,hot='#FF5A5F',cold='#7FA7FF',label=true})=>{g.fillStyle='rgba(255,255,255,.12)';g.beginPath();g.roundRect(x-55,y0-h,110,h,55);g.fill();g.beginPath();g.arc(x,y0+40,95,0,7);g.fill();
 g.fillStyle=p>.6?hot:cold;g.beginPath();g.roundRect(x-34,y0-h*p,68,h*p+20,34);g.fill();g.beginPath();g.arc(x,y0+40,72,0,7);g.fill();if(label){g.fillStyle='#fff';g.font='900 72px PL';g.textAlign='left';g.fillText(Math.round(mix(20,100,p))+'°',x+110,y0-h*p+20)}};
FX.sun=(g,t,t0,{x=540,y=860,r=200,char='丙',c1='#FF5A5F',c2='#FFB199',L=250})=>{const a=sp(t-t0,10,.7);g.save();g.translate(x,y);g.rotate(t*.6);for(let i=0;i<16;i++){g.rotate(6.283/16);const l=mix(0,L,sp(t-t0-.2-i*.02,12,.6));g.fillStyle=i%2?c1:c2;g.beginPath();g.moveTo(-22,-r-10);g.lineTo(0,-r-10-l);g.lineTo(22,-r-10);g.fill()}g.restore();
 g.fillStyle=c1;g.beginPath();g.arc(x,y,r*a,0,7);g.fill();g.fillStyle='#fff';g.font=`900 ${r*.85*a}px PL`;g.textAlign='center';g.textBaseline='middle';g.fillText(char,x,y+12)};
FX.constellation=(g,t,t0,{pts,label='',color='#FF5A5F',lab='#FFD7D8'})=>{const p=cl((t-t0)/.5)*(pts.length-1);g.strokeStyle=color;g.lineWidth=6;g.beginPath();for(let i=0;i<=Math.floor(p)&&i<pts.length;i++){i?g.lineTo(pts[i][0],pts[i][1]):g.moveTo(pts[i][0],pts[i][1])}
 if(p<pts.length-1&&p>0){const i=Math.floor(p),f=p-i;g.lineTo(mix(pts[i][0],pts[i+1][0],f),mix(pts[i][1],pts[i+1][1],f))}g.stroke();pts.forEach((q,i)=>{const s=sp(t-t0-i*.08,16,.55);g.fillStyle='#fff';g.beginPath();g.arc(q[0],q[1],12*s,0,7);g.fill()});
 if(label&&t>t0+.4){g.fillStyle=lab;g.font='800 40px PR';g.textAlign='center';g.fillText(label,pts[0][0]+40,pts[0][1]-50)}};
FX.ringPos=(i,n,{x=540,y=900,R=330}={})=>{const a=-Math.PI/2+i*6.283/n;return[x+Math.cos(a)*R,y+Math.sin(a)*R]};
FX.polyDraw=(g,pts,p,{color='#477A61',width=12,fill=0})=>{g.save();g.strokeStyle=color;g.lineWidth=width;g.lineJoin='round';g.lineCap='round';const n=pts.length,seg=p*n;g.beginPath();g.moveTo(pts[0][0],pts[0][1]);
 for(let i=0;i<n;i++){const a=pts[i],b=pts[(i+1)%n],f=cl(seg-i);if(f<=0)break;g.lineTo(mix(a[0],b[0],f),mix(a[1],b[1],f))}g.stroke();if(fill>0){g.globalAlpha=fill*.18;g.fillStyle=color;g.beginPath();pts.forEach((q,i)=>i?g.lineTo(q[0],q[1]):g.moveTo(q[0],q[1]));g.fill()}g.restore()};
window.FXK=FX;})();
