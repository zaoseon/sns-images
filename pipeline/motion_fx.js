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
window.FXK=FX;})();
