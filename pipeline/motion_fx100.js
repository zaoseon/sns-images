// 빌더 조쉬 '클로드 모션그래픽 한글 프롬프트 100'(https://tuemarz.notion.site/100-401137c926d5812fa1e8c56de870617b, 대표 11/10·11/11 공유)
// 100개 프롬프트의 '핵심 움직임'을 코드 기법으로 옮긴 것. motion_fx.js 다음에 불러 FXK 에 더한다.
// 원문 문장은 옮기지 않았다 — 움직임만 우리 말·우리 코드로 다시 만들었다. 모두 seek(t) 의 순수 함수(무작위·타이머 없음).
// 기본 가운데는 F.cx·F.cy(안전 영역 가운데), 글꼴 PL(제목)·PR(본문)·BZ(손글씨). 어떤 번호가 어떤 함수인지: F.R100.
(function(){const F=window.FXK;if(!F)return;const {cl,mix,ease,eio,sp,H}=F;const PI=Math.PI;
const T_=(g,s,x,y,font,color,al='center')=>{g.font=font;g.fillStyle=color;g.textAlign=al;g.textBaseline='middle';g.fillText(s,x,y)};
const fs_=f=>parseFloat(String(f).match(/(\d+)px/)[1]);

// ── 선·그리기 ────────────────────────────────
// 1·77·70: 끊기지 않는 선 하나가 점 목록(path)을 따라 그려진다. 끝에 점(펜 끝).
F.lineDraw=(g,t,t0,{pts,dur=1.2,color='#F2EFE8',w=10,pen='#FF5A1F'})=>{const p=eio((t-t0)/dur);if(p<=0)return;const L=[0];for(let i=1;i<pts.length;i++)L.push(L[i-1]+Math.hypot(pts[i][0]-pts[i-1][0],pts[i][1]-pts[i-1][1]));
 const tot=L[L.length-1]*p;g.save();g.strokeStyle=color;g.lineWidth=w;g.lineCap='round';g.lineJoin='round';g.beginPath();g.moveTo(pts[0][0],pts[0][1]);let e=pts[0];
 for(let i=1;i<pts.length;i++){if(L[i]<=tot){g.lineTo(pts[i][0],pts[i][1]);e=pts[i]}else{const f=(tot-L[i-1])/(L[i]-L[i-1]);e=[mix(pts[i-1][0],pts[i][0],f),mix(pts[i-1][1],pts[i][1],f)];g.lineTo(e[0],e[1]);break}}g.stroke();
 if(p<1){g.fillStyle=pen;g.beginPath();g.arc(e[0],e[1],w*1.3,0,7);g.fill()}g.restore()};
// 6: 엉킨 선이 곧게 풀린다(사인 엉킴 → 직선)
F.untangle=(g,t,t0,{x0=F.SPEC.safe[0]+40,x1=F.SPEC.safe[2]-40,y=F.cy,dur=1.2,color='#fff',w=10,amp=220})=>{const p=eio((t-t0)/dur);g.save();g.strokeStyle=color;g.lineWidth=w;g.lineCap='round';g.beginPath();
 for(let i=0;i<=120;i++){const u=i/120,x=mix(x0,x1,u),k=(1-p)*amp;const yy=y+Math.sin(u*31)*k*.6+Math.sin(u*13+1)*k*.5;const xx=x+Math.cos(u*23)*k*.35;i?g.lineTo(xx,yy):g.moveTo(xx,yy)}g.stroke();g.restore()};
// 90: 흐르는 가는 선 여러 줄(파도) 위에 문구
F.flowLines=(g,t,{y=F.cy,n=7,color='rgba(255,255,255,.55)',w=4,gap=26})=>{g.save();g.strokeStyle=color;g.lineWidth=w;for(let k=0;k<n;k++){g.beginPath();for(let i=0;i<=60;i++){const x=i*18,yy=y+(k-n/2)*gap+Math.sin(i*.25+t*2+k*.6)*18;i?g.lineTo(x,yy):g.moveTo(x,yy)}g.stroke()}g.restore()};

// ── 판·타일·카드 ─────────────────────────────
// 3·80: 타일 격자가 도미노처럼 뒤집히며 앞(색 A)→뒤(색 B). 뒤면에 글자를 붙이려면 back(g,x,y,w,h,i)
F.tileFlip=(g,t,t0,{cols=6,rows=8,x=F.SPEC.safe[0],y=F.SPEC.top[3]+60,w=F.SPEC.safe[2]-F.SPEC.safe[0],h=960,A='#1F2A44',B='#FF5A1F',step=.035,dur=.35})=>{const cw=w/cols,ch=h/rows;g.save();
 for(let r=0;r<rows;r++)for(let c=0;c<cols;c++){const d=(r+c)*step,p=eio((t-t0-d)/dur),sx=Math.abs(Math.cos(p*PI));g.fillStyle=p<.5?A:B;const X=x+c*cw+cw/2,Y=y+r*ch+ch/2;g.fillRect(X-(cw-6)/2*sx,Y-(ch-6)/2,(cw-6)*sx,ch-6)}g.restore()};
// 5: 숫자가 위아래 띠로 갈라지며 다음 숫자가 나온다(카운트다운)
F.splitNumber=(g,t,t0,{from=3,step=.8,x=F.cx,y=F.cy,font='900 420px PL',color='#fff'})=>{const T=t-t0;if(T<0)return;const k=Math.floor(T/step),n=from-k;if(n<0)return;const f=(T-k*step)/step,o=eio(cl((f-.55)/.45))*360,fs=fs_(font);
 g.save();g.font=font;g.textAlign='center';g.textBaseline='middle';g.fillStyle=color;
 if(n-1>=0&&o>0){g.globalAlpha=cl(o/200);g.fillText(n-1,x,y);g.globalAlpha=1}
 [[-1,y-fs],[1,y]].forEach(([s_,top])=>{g.save();g.beginPath();g.rect(x-fs,top+s_*o,fs*2,fs);g.clip();g.globalAlpha=1-cl(o/360);g.fillText(n,x,y+s_*o);g.restore()});
 if(o>0&&o<300){g.fillStyle=color;g.fillRect(x-fs*.6,y-3,fs*1.2*(1-o/300),6)}g.restore()};

// 7: 스위스 그리드 — 굵은 선이 칸을 나누고 칸마다 글자·숫자가 박힌다
F.swissGrid=(g,t,t0,{cells,x=F.SPEC.safe[0],y=F.SPEC.top[3]+70,w=F.SPEC.safe[2]-F.SPEC.safe[0],h=900,color='#111',bg='#F2EFE8',font='900 76px PL'})=>{g.save();g.strokeStyle=color;g.lineWidth=8;
 const p=eio((t-t0)/.5);[[x,y+h*.38,x+w*p,y+h*.38],[x+w*.55,y,x+w*.55,y+h*p],[x,y+h*.72,x+w*p,y+h*.72]].forEach(([a,b,c,d])=>{g.beginPath();g.moveTo(a,b);g.lineTo(c,d);g.stroke()});
 const box=[[x,y,w*.55,h*.38],[x+w*.55,y,w*.45,h*.38],[x,y+h*.38,w*.55,h*.34],[x+w*.55,y+h*.38,w*.45,h*.34],[x,y+h*.72,w,h*.28]];
 (cells||[]).forEach((c,i)=>{const b=box[i];if(!b)return;const a=sp(t-t0-.5-i*.18,15,.6);if(a<=0)return;g.save();g.beginPath();g.rect(b[0],b[1],b[2],b[3]);g.clip();g.font=font;const k_=Math.min(1,(b[2]-50)/g.measureText(c).width);T_(g,c,b[0]+24,b[1]+b[3]-50+(1-a)*80,`900 ${Math.floor(fs_(font)*k_)}px PL`,color,'left');g.restore()});g.restore()};
// 8·44: 긴 캔버스를 카메라가 옆으로(또는 위로) 따라간다. draw(g) 는 긴 판 좌표로 그린다
F.panCanvas=(g,t,t0,{len=3000,dur=4,dir='x',draw})=>{const p=eio((t-t0)/dur);g.save();if(dir=='x')g.translate(-p*(len-1080),0);else g.translate(0,-p*(len-1920));draw&&draw(g);g.restore()};
// 23: 3×2 카드 6장이 차례로 열린다(가운데 기준). 카드 안 글자: labels
F.gridCards=(g,t,t0,{labels,cols=2,rows=3,w=380,h=230,gap=28,y=F.cy,bg='#fff',fg='#111',font='900 52px PL',step=.12})=>{const W=cols*w+(cols-1)*gap,Hh=rows*h+(rows-1)*gap,x0=F.cx-W/2,y0=y-Hh/2;g.save();
 for(let i=0;i<cols*rows;i++){const c=i%cols,r=Math.floor(i/cols),a=sp(t-t0-i*step,14,.65);if(a<=0)continue;const X=x0+c*(w+gap)+w/2,Y=y0+r*(h+gap)+h/2;g.save();g.translate(X,Y);g.scale(a,a);g.fillStyle=bg;g.beginPath();g.roundRect(-w/2,-h/2,w,h,36);g.fill();if(labels&&labels[i])T_(g,labels[i],0,4,font,fg);g.restore()}g.restore()};
// 96: 폴라로이드가 떨어져 쌓인다(살짝 기울기). drawPhoto(g,w,h,i) 로 사진 칸을 그린다
F.polaroids=(g,t,t0,{n=4,x=F.cx,y=F.cy,w=440,h=520,step=.45,drawPhoto,captions=[]})=>{for(let i=0;i<n;i++){const a=sp(t-t0-i*step,11,.7);if(a<=0)continue;const r=(H(i+3)-.5)*.3,dx=(H(i+7)-.5)*120;
 g.save();g.translate(x+dx,mix(y-900,y+(i-n/2)*14,a));g.rotate(r);g.fillStyle='rgba(0,0,0,.25)';g.fillRect(-w/2+10,-h/2+16,w,h);g.fillStyle='#fff';g.fillRect(-w/2,-h/2,w,h);g.fillStyle='#ddd';g.fillRect(-w/2+26,-h/2+26,w-52,w-52);drawPhoto&&drawPhoto(g,-w/2+26,-h/2+26,w-52,w-52,i);
 if(captions[i])T_(g,captions[i],0,h/2-60,'64px BZ','#222');g.restore()}};

// ── 앱 화면·UI ──────────────────────────────
// 26~35: 폰 틀(둥근 사각형 + 노치). content(g,x,y,w,h) 로 화면을 그린다. tap=[x,y,t]면 그 자리에 터치 물결
F.phone=(g,{x=F.cx,y=F.cy,w=470,h=960,content,tap,t=0,color='#111',screen='#fff',tilt=0})=>{g.save();g.translate(x,y);g.rotate(tilt);g.fillStyle='rgba(0,0,0,.28)';g.beginPath();g.roundRect(-w/2+12,-h/2+20,w,h,70);g.fill();
 g.fillStyle=color;g.beginPath();g.roundRect(-w/2,-h/2,w,h,70);g.fill();g.fillStyle=screen;g.beginPath();g.roundRect(-w/2+18,-h/2+18,w-36,h-36,54);g.fill();g.save();g.beginPath();g.roundRect(-w/2+18,-h/2+18,w-36,h-36,54);g.clip();content&&content(g,-w/2+18,-h/2+18,w-36,h-36);g.restore();
 g.fillStyle=color;g.beginPath();g.roundRect(-70,-h/2+30,140,34,17);g.fill();
 if(tap){const p=cl((t-tap[2])/.45);if(p>0&&p<1){g.strokeStyle='rgba(30,30,30,'+(1-p)+')';g.lineWidth=6;g.beginPath();g.arc(tap[0],tap[1],20+p*60,0,7);g.stroke();g.fillStyle='rgba(30,30,30,.25)';g.beginPath();g.arc(tap[0],tap[1],26,0,7);g.fill()}}g.restore()};
// 13: 검색창에 한 글자씩 쳐지고 결과 줄이 아래로 쏟아진다
F.searchType=(g,t,t0,{query,results=[],x=F.cx,y=F.SPEC.top[3]+160,w=780,font='800 54px PR',cps=8,fg='#111',bg='#fff',accent='#FF5A1F'})=>{const n=Math.max(0,Math.min(query.length,Math.floor((t-t0)*cps)));g.save();g.fillStyle=bg;g.beginPath();g.roundRect(x-w/2,y-60,w,120,60);g.fill();
 T_(g,'⌕',x-w/2+60,y,font,'#999');T_(g,query.slice(0,n)+((Math.floor(t*3)%2&&n<query.length)?'|':''),x-w/2+110,y,font,fg,'left');
 const tr=t0+query.length/cps;results.forEach((r,i)=>{const a=sp(t-tr-i*.1,15,.6);if(a<=0)return;const Y=y+150+i*130;g.save();g.translate(0,(1-a)*-60);g.globalAlpha=cl(a);g.fillStyle=bg;g.beginPath();g.roundRect(x-w/2,Y-50,w,100,30);g.fill();g.fillStyle=accent;g.beginPath();g.arc(x-w/2+56,Y,16,0,7);g.fill();T_(g,r,x-w/2+100,Y,'800 46px PR',fg,'left');g.restore()});g.restore()};
// 14: 할 일 목록 — 체크할 때마다 위쪽 진행 막대가 찬다
F.checklist=(g,t,t0,{items,x=F.cx,y=F.cy,w=760,step=.6,fg='#111',bg='#fff',accent='#2EBD6B',font='800 52px PR'})=>{const n=items.length,top=y-(n*120)/2;let done=0;g.save();
 items.forEach((it,i)=>{const Y=top+i*120+60,c=cl((t-t0-i*step)/.25);if(c>=1)done++;g.fillStyle=bg;g.beginPath();g.roundRect(x-w/2,Y-48,w,96,28);g.fill();
  g.strokeStyle=accent;g.lineWidth=6;g.beginPath();g.roundRect(x-w/2+28,Y-22,44,44,10);g.stroke();if(c>0){g.fillStyle=accent;g.beginPath();g.roundRect(x-w/2+28,Y-22,44,44,10);g.fill();g.strokeStyle='#fff';g.lineWidth=7;g.beginPath();g.moveTo(x-w/2+38,Y);g.lineTo(x-w/2+48,Y+10*c);g.lineTo(x-w/2+48+14*c,Y-12*c);g.stroke()}
  g.globalAlpha=c>=1?.45:1;T_(g,it,x-w/2+100,Y,font,fg,'left');g.globalAlpha=1;if(c>=1){g.strokeStyle=fg;g.lineWidth=4;g.beginPath();g.moveTo(x-w/2+100,Y);g.lineTo(x-w/2+100+g.measureText(it).width,Y);g.stroke()}});
 const pr=mix(0,1,eio(cl((t-t0)/(n*step))));g.fillStyle='rgba(255,255,255,.3)';g.beginPath();g.roundRect(x-w/2,top-70,w,22,11);g.fill();g.fillStyle=accent;g.beginPath();g.roundRect(x-w/2,top-70,w*pr,22,11);g.fill();g.restore()};
// 15: 진행 점 3개 중 지금 단계 점이 늘어나 카드가 된다
F.dotsToCard=(g,t,t0,{steps,x=F.cx,y=F.cy,step=1.2,color='#fff',fg='#111',font='900 64px PL',sub='800 44px PR'})=>{const k=Math.min(steps.length-1,Math.max(0,Math.floor((t-t0)/step))),f=eio(cl(((t-t0)-k*step)/.4));g.save();
 steps.forEach((s,i)=>{const X=x+(i-1)*60,on=i==k;g.fillStyle=on?color:'rgba(255,255,255,.35)';g.beginPath();g.arc(X,y+380,14,0,7);g.fill()});
 const w=mix(28,760,f),h=mix(28,520,f);g.fillStyle=color;g.beginPath();g.roundRect(x-w/2,y-h/2-40,w,h,mix(14,48,f));g.fill();if(f>.7){g.globalAlpha=cl((f-.7)/.3);T_(g,(k+1)+'단계',x,y-150,sub,'#999');T_(g,steps[k],x,y-40,font,fg)}g.restore()};
// 16: 블록을 끌어 와 칸에 끼운다(손가락 포인터 포함)
F.dragBlocks=(g,t,t0,{blocks,x=F.cx,y=F.cy,step=.7,colors=['#FF5A1F','#2F6BFF','#2EBD6B','#FFC21A'],font='900 50px PL'})=>{const n=blocks.length;g.save();
 for(let i=0;i<n;i++){const Y=y-(n-1)*70+i*140;g.strokeStyle='rgba(255,255,255,.4)';g.setLineDash([16,12]);g.lineWidth=4;g.beginPath();g.roundRect(x-300,Y-55,600,110,26);g.stroke();g.setLineDash([])}
 blocks.forEach((b,i)=>{const p=eio(cl((t-t0-i*step)/.55)),Y=y-(n-1)*70+i*140,sx=mix(x+520,x,p),sy=mix(Y+300,Y,p);if(t<t0+i*step-.2)return;g.fillStyle=colors[i%colors.length];g.beginPath();g.roundRect(sx-300,sy-55,600,110,26);g.fill();T_(g,b,sx,sy+2,font,'#fff');
  if(p<1){g.fillStyle='#fff';g.beginPath();g.arc(sx+200,sy+30,22,0,7);g.fill()}});g.restore()};
// 18: 결제 흐름 — 카드가 들어오고 버튼을 누르면 체크로 끝난다(상태: 대기→누름→처리→완료)
F.payFlow=(g,t,t0,{price='2,900원',x=F.cx,y=F.cy,accent='#111',fg='#fff'})=>{const T=t-t0;g.save();const a=sp(T,13,.7);g.translate(0,(1-a)*200);g.fillStyle='#fff';g.beginPath();g.roundRect(x-380,y-330,760,460,44);g.fill();
 T_(g,'결제 금액',x,y-230,'800 44px PR','#888');T_(g,price,x,y-130,'900 110px PL','#111');const st=T<1.2?0:T<1.35?1:T<2.2?2:3,w=st==3?140:620;
 g.fillStyle=st==3?'#2EBD6B':accent;g.beginPath();g.roundRect(x-w/2,y+190-(st==1?-6:0),w,130,65);g.fill();
 if(st<2)T_(g,'결제하기',x,y+255,'900 56px PL',fg);else if(st==2){g.strokeStyle=fg;g.lineWidth=8;g.beginPath();g.arc(x,y+255,30,T*8,T*8+4.5);g.stroke()}else{g.strokeStyle='#fff';g.lineWidth=10;const p=cl((T-2.2)/.3);g.beginPath();g.moveTo(x-30,y+255);g.lineTo(x-8,y+255+22*p);g.lineTo(x-8+40*p,y+255-28*p);g.stroke()}g.restore()};
// 19: 가운데 손잡이로 가르는 전·후 비교(before/after 는 그리는 함수)
F.beforeAfter=(g,t,t0,{before,after,x0=F.SPEC.safe[0],x1=F.SPEC.safe[2],y0=F.SPEC.top[3]+80,y1=F.SPEC.bottom[1]-80,dur=2})=>{const p=.5+.4*Math.sin(cl((t-t0)/dur)*PI*2),sx=mix(x0,x1,p);
 g.save();g.beginPath();g.rect(x0,y0,sx-x0,y1-y0);g.clip();before&&before(g);g.restore();g.save();g.beginPath();g.rect(sx,y0,x1-sx,y1-y0);g.clip();after&&after(g);g.restore();
 g.fillStyle='#fff';g.fillRect(sx-4,y0,8,y1-y0);g.beginPath();g.arc(sx,(y0+y1)/2,44,0,7);g.fill();T_(g,'⇆',sx,(y0+y1)/2+2,'900 44px PL','#111')};
// 20: 쌓인 알림 카드들이 한 장으로 접힌다
F.stackCollapse=(g,t,t0,{items,summary,x=F.cx,y=F.cy,w=760,font='800 46px PR',bg='#fff',fg='#111'})=>{const p=eio(cl((t-t0-items.length*.12-.4)/.5));g.save();
 items.forEach((s,i)=>{const a=sp(t-t0-i*.12,15,.6);if(a<=0)return;const Y=mix(y-(items.length-1)*65+i*130,y+i*10,p);g.globalAlpha=1-p*(i>0?1:0);g.fillStyle=bg;g.beginPath();g.roundRect(x-w/2,Y-52,w,104,30);g.fill();T_(g,s,x-w/2+40,Y,font,fg,'left')});
 if(p>.6){g.globalAlpha=cl((p-.6)/.4);g.fillStyle='#FF5A1F';g.beginPath();g.roundRect(x-w/2,y-80,w,160,40);g.fill();T_(g,summary,x,y,'900 56px PL','#fff')}g.restore()};
// 21: 빈 주간 캘린더가 스스로 채워진다
F.weekFill=(g,t,t0,{events,x=F.cx,y=F.cy,days=['월','화','수','목','금'],cw=150,rh=110,font='800 40px PR',colors=['#FF5A1F','#2F6BFF','#2EBD6B']})=>{const W=days.length*cw,x0=x-W/2,y0=y-260;g.save();
 days.forEach((d,i)=>{T_(g,d,x0+i*cw+cw/2,y0-50,'900 44px PL','#fff');g.strokeStyle='rgba(255,255,255,.25)';g.lineWidth=3;g.strokeRect(x0+i*cw,y0,cw,rh*5)});
 (events||[]).forEach((e,i)=>{const a=sp(t-t0-i*.25,14,.6);if(a<=0)return;const [d,r,n,label]=e;g.fillStyle=colors[i%colors.length];g.beginPath();g.roundRect(x0+d*cw+8,y0+r*rh+8,cw-16,(rh*n-16)*a,18);g.fill();if(a>.8)T_(g,label,x0+d*cw+cw/2,y0+r*rh+rh*n/2,font,'#fff')});g.restore()};
// 22·98: 왼쪽 코드가 한 줄씩 쳐지고 오른쪽 미리보기가 바로 바뀐다. preview(g,k) 는 k번째 줄까지의 결과를 그린다
F.codePreview=(g,t,t0,{lines,preview,step=.9,x=F.SPEC.safe[0],y=F.SPEC.top[3]+100,w=F.SPEC.safe[2]-F.SPEC.safe[0],h=900,accent='#FFB547'})=>{const k=Math.min(lines.length,Math.floor((t-t0)/step)+1),half=w*.5;g.save();
 g.fillStyle='#141417';g.beginPath();g.roundRect(x,y,half,h,30);g.fill();g.fillStyle='#F3F0E8';g.beginPath();g.roundRect(x+half+16,y,half-16,h,30);g.fill();
 lines.slice(0,k).forEach((l,i)=>{const typed=i<k-1?l:l.slice(0,Math.floor(cl(((t-t0)-(k-1)*step)/(step*.6))*l.length));T_(g,typed,x+28,y+70+i*64,'500 34px monospace',i==k-1?accent:'#ddd','left')});
 g.save();g.beginPath();g.rect(x+half+16,y,half-16,h);g.clip();preview&&preview(g,k,x+half+16+(half-16)/2,y+h/2);g.restore();g.restore()};
// 24: 클릭한 자리에서 원이 퍼지며 다크↔라이트가 바뀐다
F.themeRipple=(g,t,t0,{x=F.cx,y=F.cy,from='#111',to='#F2EFE8',dur=.6})=>{g.fillStyle=from;g.fillRect(0,0,1080,1920);const p=eio((t-t0)/dur);if(p>0){g.fillStyle=to;g.beginPath();g.arc(x,y,p*2200,0,7);g.fill()}};
// 25: 파일 카드가 끌려 들어오면 링이 돌며 차고 체크
F.uploadRing=(g,t,t0,{x=F.cx,y=F.cy,label='파일',color='#2F6BFF'})=>{const T=t-t0,a=eio(cl(T/.5));g.save();g.fillStyle='#fff';g.beginPath();g.roundRect(mix(x+420,x-90,a),mix(y-500,y-120,a),180,230,24);g.fill();T_(g,label,mix(x+510,x,a),mix(y-385,y-5,a),'900 40px PL','#111');
 if(T>.5){const p=cl((T-.5)/1.2);g.lineWidth=22;g.strokeStyle='rgba(255,255,255,.2)';g.beginPath();g.arc(x,y,230,0,7);g.stroke();g.strokeStyle=color;g.lineCap='round';g.beginPath();g.arc(x,y,230,-PI/2,-PI/2+p*2*PI);g.stroke();if(p>=1)T_(g,'✓',x,y+250+30,'900 90px PL',color)}g.restore()};

// ── 차트·데이터 ─────────────────────────────
// 36: 막대가 자라다 마지막 막대가 화면을 차지한다
F.growBars=(g,t,t0,{vals,labels=[],x=F.cx,y=F.SPEC.bottom[1]-140,maxH=760,w=110,gap=40,color='rgba(255,255,255,.6)',hero='#FF5A1F',font='800 40px PR'})=>{const n=vals.length,W=n*w+(n-1)*gap,x0=x-W/2,m=Math.max(...vals);g.save();
 vals.forEach((v,i)=>{const a=sp(t-t0-i*.12,12,.7),h=maxH*v/m*a,last=i==n-1,z=last?eio(cl((t-t0-n*.12-.4)/.6)):0;g.fillStyle=last?hero:color;const X=mix(x0+i*(w+gap),F.SPEC.safe[0],z),Ww=mix(w,F.SPEC.safe[2]-F.SPEC.safe[0],z);
  g.beginPath();g.roundRect(X,y-h,Ww,h,[18,18,0,0]);g.fill();if(labels[i]&&z<.2)T_(g,labels[i],x0+i*(w+gap)+w/2,y+40,font,'#fff')});g.restore()};
// 37: 선 그래프가 그려지고 끝점이 숫자로 바뀐다
F.lineGraph=(g,t,t0,{vals,x0=F.SPEC.safe[0]+40,x1=F.SPEC.safe[2]-40,y0=F.SPEC.bottom[1]-180,h=620,dur=1.4,color='#FF5A1F',label,font='900 120px PL'})=>{const p=eio((t-t0)/dur),m=Math.max(...vals),n=vals.length;g.save();g.strokeStyle=color;g.lineWidth=12;g.lineJoin='round';g.lineCap='round';g.beginPath();let e;
 for(let i=0;i<n;i++){const u=i/(n-1);if(u>p){const pu=(i-1)/(n-1),f=(p-pu)/(u-pu),xa=mix(x0,x1,pu),ya=y0-h*vals[i-1]/m,xb=mix(x0,x1,u),yb=y0-h*vals[i]/m;e=[mix(xa,xb,f),mix(ya,yb,f)];g.lineTo(e[0],e[1]);break}const X=mix(x0,x1,u),Y=y0-h*vals[i]/m;e=[X,Y];i?g.lineTo(X,Y):g.moveTo(X,Y)}g.stroke();
 g.fillStyle=color;g.beginPath();g.arc(e[0],e[1],18,0,7);g.fill();if(p>=1&&label){const a=sp(t-t0-dur,14,.6);g.save();g.translate(Math.min(e[0],x1-200),e[1]-110);g.scale(a,a);T_(g,label,0,0,font,'#fff');g.restore()}g.restore()};
// 38: 순위가 바뀔 때마다 막대가 자리를 바꾼다. frames=[{이름:값}…], 한 프레임 dur 초
F.barRace=(g,t,t0,{frames,dur=1,x=F.SPEC.safe[0]+20,y=F.SPEC.top[3]+140,w=F.SPEC.safe[2]-F.SPEC.safe[0]-40,rh=120,colors={},font='900 48px PL'})=>{const k=Math.min(frames.length-1,Math.max(0,(t-t0)/dur)),i0=Math.floor(k),f=eio(k-i0),A=frames[i0],B=frames[Math.min(i0+1,frames.length-1)];
 const names=Object.keys(A),val=n=>mix(A[n],B[n]??A[n],f),rank=fr=>{const s=Object.keys(fr).sort((a,b)=>fr[b]-fr[a]);return n=>s.indexOf(n)},rA=rank(A),rB=rank(B),m=Math.max(...names.map(val));g.save();
 names.forEach((n,j)=>{const r=mix(rA(n),rB(n),f),Y=y+r*rh,v=val(n),W=Math.max(140,w*v/m);g.fillStyle=colors[n]||['#FF5A1F','#2F6BFF','#2EBD6B','#FFC21A','#B26BFF'][j%5];g.beginPath();g.roundRect(x,Y,W,rh-24,20);g.fill();T_(g,n,x+28,Y+(rh-24)/2,font,'#fff','left');T_(g,Math.round(v),x+W-24,Y+(rh-24)/2,font,'#fff','right')});g.restore()};
// 32·39: 도넛 — 조각이 차례로 차고, 조각마다 바깥으로 선이 뻗어 이름표
F.donut=(g,t,t0,{vals,labels=[],x=F.cx,y=F.cy,r=230,w=90,colors=['#FF5A1F','#2F6BFF','#2EBD6B','#FFC21A','#B26BFF'],font='800 42px PR',leader=true})=>{const s=vals.reduce((a,b)=>a+b,0);let a0=-PI/2;g.save();g.lineWidth=w;
 vals.forEach((v,i)=>{const p=eio(cl((t-t0-i*.25)/.45)),a1=a0+2*PI*v/s*p;g.strokeStyle=colors[i%colors.length];g.beginPath();g.arc(x,y,r,a0,a1);g.stroke();
  if(leader&&p>=1&&labels[i]){const m=(a0+a1)/2,q=eio(cl((t-t0-i*.25-.45)/.3)),x1=x+Math.cos(m)*(r+w/2+10),y1=y+Math.sin(m)*(r+w/2+10),x2=x+Math.cos(m)*(r+w/2+70),y2=y+Math.sin(m)*(r+w/2+70),x3=x2+(Math.cos(m)>0?1:-1)*80*q;
   g.save();g.lineWidth=5;g.strokeStyle='#fff';g.beginPath();g.moveTo(x1,y1);g.lineTo(x2,y2);g.lineTo(x3,y2);g.stroke();g.globalAlpha=q;T_(g,labels[i],x3+(Math.cos(m)>0?14:-14),y2,font,'#fff',Math.cos(m)>0?'left':'right');g.restore()}
  a0=a0+2*PI*v/s});g.restore()};
// 40: 숫자 세 개가 이어 달린다(앞 숫자가 다 오르면 다음이 시작)
F.kpiRelay=(g,t,t0,{items,x=F.cx,y=F.cy,step=.9,font='900 150px PL',sub='800 48px PR',color='#fff',accent='#FF5A1F'})=>{g.save();items.forEach(([v,label,unit=''],i)=>{const T=t-t0-i*step;if(T<0)return;const Y=y+(i-1)*260,p=eio(cl(T/.7));
 T_(g,Math.round(v*p).toLocaleString()+unit,x,Y,font,i==items.length-1?accent:color);T_(g,label,x,Y+100,sub,'rgba(255,255,255,.75)');if(i<items.length-1&&T>.7){g.strokeStyle=accent;g.lineWidth=6;g.beginPath();g.moveTo(x-60,Y+150);g.lineTo(x-60+120*eio(cl((T-.7)/.2)),Y+150);g.stroke()}});g.restore()};
// 41: 아래로 갈수록 좁아지는 퍼널. leak=새는 단계 번호(옆으로 점이 샌다)
F.funnel=(g,t,t0,{steps,x=F.cx,y=F.SPEC.top[3]+150,w=800,rh=150,leak=-1,colors=['#2F6BFF','#4D7FFF','#6C95FF','#8FAEFF'],font='900 52px PL'})=>{g.save();steps.forEach(([label,v],i)=>{const a=sp(t-t0-i*.2,13,.65);if(a<=0)return;const top=w*(1-i*.18),bot=w*(1-(i+1)*.18),Y=y+i*(rh+14);
 g.fillStyle=colors[i%colors.length];g.beginPath();g.moveTo(x-top/2*a,Y);g.lineTo(x+top/2*a,Y);g.lineTo(x+bot/2*a,Y+rh);g.lineTo(x-bot/2*a,Y+rh);g.fill();T_(g,label+' '+v,x,Y+rh/2,font,'#fff');
 if(i==leak)for(let k=0;k<6;k++){const q=((t*1.5+k/6)%1);g.fillStyle='#FF5A1F';g.beginPath();g.arc(x+bot/2+q*160,Y+rh/2+q*q*120,10,0,7);g.fill()}});g.restore()};
// 42: 지도(점 격자) 위 도시 점들이 숨 쉬듯 커졌다 작아진다
F.mapPulse=(g,t,{cities,color='#FF5A1F',grid='rgba(255,255,255,.18)'})=>{g.save();g.fillStyle=grid;for(let y=F.SPEC.top[3]+80;y<F.SPEC.bottom[1]-80;y+=34)for(let x=F.SPEC.safe[0]+20;x<F.SPEC.safe[2]-20;x+=34)g.fillRect(x,y,6,6);
 cities.forEach(([x,y,v,name],i)=>{const b=1+.18*Math.sin(t*3+i);g.fillStyle=color;g.globalAlpha=.25;g.beginPath();g.arc(x,y,v*b*1.8,0,7);g.fill();g.globalAlpha=1;g.beginPath();g.arc(x,y,v*.6,0,7);g.fill();if(name)T_(g,name,x,y-v*1.4-30,'800 42px PR','#fff')});g.restore()};
// 43: 가운데 선을 두고 좌우가 맞붙는다(값 비율만큼 선이 밀린다)
F.versus=(g,t,t0,{a,b,va,vb,colA='#2F6BFF',colB='#FF5A1F',font='900 76px PL'})=>{const p=eio(cl((t-t0)/1)),r=mix(.5,va/(va+vb),p),x0=F.SPEC.safe[0],x1=F.SPEC.safe[2],sx=mix(x0,x1,r),y0=F.SPEC.top[3]+120,y1=F.SPEC.bottom[1]-120;
 g.fillStyle=colA;g.fillRect(x0,y0,sx-x0,y1-y0);g.fillStyle=colB;g.fillRect(sx,y0,x1-sx,y1-y0);g.fillStyle='#fff';g.fillRect(sx-5,y0,10,y1-y0);T_(g,a,(x0+sx)/2,F.cy-60,font,'#fff');T_(g,b,(sx+x1)/2,F.cy-60,font,'#fff');T_(g,Math.round(va*p)+'',(x0+sx)/2,F.cy+60,font,'#fff');T_(g,Math.round(vb*p)+'',(sx+x1)/2,F.cy+60,font,'#fff')};
// 45: 링 네 개가 박자를 나눠 차오른다(설문 결과)
F.ringsBeat=(g,t,t0,{vals,labels=[],x=F.cx,y=F.cy,beat=.5,colors=['#FF5A1F','#2F6BFF','#2EBD6B','#FFC21A'],font='900 56px PL'})=>{g.save();vals.forEach((v,i)=>{const c=i%2,r=Math.floor(i/2),X=x+(c-.5)*390,Y=y+(r-.5)*400,p=eio(cl((t-t0-i*beat)/.45))*v/100;
 g.lineWidth=36;g.lineCap='round';g.strokeStyle='rgba(255,255,255,.18)';g.beginPath();g.arc(X,Y,130,0,7);g.stroke();g.strokeStyle=colors[i%4];g.beginPath();g.arc(X,Y,130,-PI/2,-PI/2+p*2*PI);g.stroke();T_(g,Math.round(p*100)+'%',X,Y,font,'#fff');if(labels[i])T_(g,labels[i],X,Y+190,'800 44px PR','#fff')});g.restore()};
// 46: 지층처럼 흐르는 구성 변화(쌓인 영역). series=[[값…],…] 시간축 따라
F.stream=(g,t,t0,{series,colors=['#FF5A1F','#2F6BFF','#2EBD6B','#FFC21A'],x0=F.SPEC.safe[0],x1=F.SPEC.safe[2],y0=F.SPEC.bottom[1]-160,h=760,dur=1.6})=>{const p=eio((t-t0)/dur),n=series[0].length;let base=new Array(n).fill(0);const tot=series[0].map((_,i)=>series.reduce((a,s)=>a+s[i],0));g.save();
 series.forEach((s,k)=>{g.fillStyle=colors[k%4];g.beginPath();for(let i=0;i<n;i++){const X=mix(x0,mix(x0,x1,i/(n-1)),p);g.lineTo(X,y0-h*(base[i]+s[i])/tot[i])}for(let i=n-1;i>=0;i--){const X=mix(x0,mix(x0,x1,i/(n-1)),p);g.lineTo(X,y0-h*base[i]/tot[i])}g.fill();base=base.map((b,i)=>b+s[i])});g.restore()};
// 48: 흩어진 점이 모여 추세선으로 정리된다
F.scatterTrend=(g,t,t0,{n=40,x0=F.SPEC.safe[0]+60,x1=F.SPEC.safe[2]-60,y0=F.SPEC.bottom[1]-200,h=640,color='#fff',line='#FF5A1F'})=>{const p=eio(cl((t-t0)/1.2));g.save();for(let i=0;i<n;i++){const u=i/(n-1),X=mix(x0,x1,u),Yt=y0-h*u,Yn=Yt+(H(i)-.5)*360*(1-p*.6);g.fillStyle=color;g.beginPath();g.arc(X,Yn,11,0,7);g.fill()}
 const q=eio(cl((t-t0-1)/.6));g.strokeStyle=line;g.lineWidth=10;g.lineCap='round';g.beginPath();g.moveTo(x0,y0);g.lineTo(mix(x0,x1,q),y0-h*q);g.stroke();g.restore()};
// 49: 표의 행을 따라 내려가다 셀 하나로 들어간다(줌)
F.tableZoom=(g,t,t0,{rows,hit=[2,1],x=F.cx,y=F.cy,cw=250,rh=100,font='800 44px PR'})=>{const cols=rows[0].length,W=cols*cw,Hh=rows.length*rh,x0=x-W/2,y0=y-Hh/2,p=eio(cl((t-t0-1.2)/.7)),sel=Math.min(hit[0],Math.floor((t-t0)/.3));
 const cx=x0+hit[1]*cw+cw/2,cy=y0+hit[0]*rh+rh/2,z=mix(1,2.6,p);g.save();g.translate(x,y);g.scale(z,z);g.translate(-mix(x,cx,p),-mix(y,cy,p));
 rows.forEach((r,i)=>r.forEach((c,j)=>{g.fillStyle=i==0?'#2F6BFF':(i==sel?'rgba(255,90,31,.35)':'rgba(255,255,255,.08)');g.fillRect(x0+j*cw+3,y0+i*rh+3,cw-6,rh-6);if(i==hit[0]&&j==hit[1]&&p>0){g.strokeStyle='#FF5A1F';g.lineWidth=6;g.strokeRect(x0+j*cw+3,y0+i*rh+3,cw-6,rh-6)}T_(g,c,x0+j*cw+cw/2,y0+i*rh+rh/2,font,'#fff')}));g.restore()};

// ── 다이어그램 ──────────────────────────────
// 51: 박스가 다음 박스를 낳는다(세로 3단계, 화살표)
F.boxChain=(g,t,t0,{steps,x=F.cx,y=F.cy,step=.7,w=640,h=170,gap=110,color='#fff',fg='#111',font='900 60px PL',arrow='#FF5A1F'})=>{const n=steps.length,top=y-(n*h+(n-1)*gap)/2;g.save();steps.forEach((s,i)=>{const a=sp(t-t0-i*step,13,.65);if(a<=0)return;const Y=top+i*(h+gap),fromY=i?top+(i-1)*(h+gap):Y;
 g.save();g.translate(x,mix(fromY+h/2,Y+h/2,eio(cl((t-t0-i*step)/.4))));g.scale(a,a);g.fillStyle=color;g.beginPath();g.roundRect(-w/2,-h/2,w,h,40);g.fill();T_(g,s,0,4,font,fg);g.restore();
 if(i){const q=eio(cl((t-t0-i*step-.2)/.3));g.strokeStyle=arrow;g.lineWidth=8;g.beginPath();g.moveTo(x,Y-gap+10);g.lineTo(x,Y-gap+10+(gap-30)*q);g.stroke();if(q>=1){g.beginPath();g.moveTo(x-18,Y-36);g.lineTo(x,Y-16);g.lineTo(x+18,Y-36);g.stroke()}}});g.restore()};
// 52: 점 하나가 두 상자 사이를 왕복한다(요청→응답)
F.packet=(g,t,t0,{a='앱',b='서버',x=F.cx,y=F.cy,span=560,color='#FF5A1F',font='900 56px PL'})=>{const xa=x-span/2,xb=x+span/2;g.save();[[xa,a],[xb,b]].forEach(([X,s])=>{g.fillStyle='#fff';g.beginPath();g.roundRect(X-130,y-110,260,220,40);g.fill();T_(g,s,X,y,font,'#111')});
 g.strokeStyle='rgba(255,255,255,.4)';g.lineWidth=6;g.setLineDash([14,14]);g.beginPath();g.moveTo(xa+140,y);g.lineTo(xb-140,y);g.stroke();g.setLineDash([]);const T=(t-t0)%1.6,go=T<.8,q=eio((go?T:T-.8)/.8);
 g.fillStyle=go?color:'#2EBD6B';g.beginPath();g.arc(go?mix(xa+150,xb-150,q):mix(xb-150,xa+150,q),y+(go?-26:26),20,0,7);g.fill();g.restore()};
// 53: 위에서부터 가지를 치는 구조도
F.tree=(g,t,t0,{root,children,x=F.cx,y=F.SPEC.top[3]+180,dy=320,color='#fff',fg='#111',line='#FF5A1F',font='900 50px PL'})=>{g.save();const box=(X,Y,s,a)=>{g.save();g.translate(X,Y);g.scale(a,a);g.font=font;const w=g.measureText(s).width+70;g.fillStyle=color;g.beginPath();g.roundRect(-w/2,-50,w,100,30);g.fill();T_(g,s,0,3,font,fg);g.restore()};
 box(x,y,root,sp(t-t0,14,.6));const n=children.length,span=Math.min(800,n*260);children.forEach((c,i)=>{const X=x-span/2+span*(i+.5)/n,q=eio(cl((t-t0-.4-i*.15)/.35));g.strokeStyle=line;g.lineWidth=6;g.beginPath();g.moveTo(x,y+50);g.lineTo(x,y+50+(dy/2-50)*q);g.lineTo(mix(x,X,q),y+dy/2);g.lineTo(mix(x,X,q),y+dy/2+(dy/2-50)*cl((q-.6)/.4));g.stroke();if(q>=1)box(X,y+dy,c,sp(t-t0-.75-i*.15,14,.6))});g.restore()};
// 54: 원을 따라 도는 4단계 순환(점 하나가 돈다)
F.cycle=(g,t,t0,{steps,x=F.cx,y=F.cy,R=300,color='#FF5A1F',font='900 50px PL'})=>{const n=steps.length,k=(t-t0)/.8;g.save();g.lineWidth=10;g.strokeStyle='rgba(255,255,255,.3)';g.beginPath();g.arc(x,y,R,0,7);g.stroke();
 steps.forEach((s,i)=>{const a=-PI/2+i*2*PI/n,X=x+Math.cos(a)*R,Y=y+Math.sin(a)*R,on=Math.floor(k)%n==i;g.fillStyle=on?color:'#fff';g.beginPath();g.arc(X,Y,on?96:86,0,7);g.fill();T_(g,s,X,Y+2,font,on?'#fff':'#111')});
 const a=-PI/2+(k%n)*2*PI/n;g.fillStyle=color;g.beginPath();g.arc(x+Math.cos(a)*R,y+Math.sin(a)*R,18,0,7);g.fill();g.restore()};
// 55: 두 원이 다가와 겹치고 겹친 곳이 칠해진다(교집합)
F.venn=(g,t,t0,{a,b,mid,x=F.cx,y=F.cy,r=250,colA='#2F6BFF',colB='#FF5A1F',font='900 52px PL'})=>{const p=eio(cl((t-t0)/.8)),d=mix(520,300,p);g.save();g.globalAlpha=.85;g.fillStyle=colA;g.beginPath();g.arc(x-d/2,y,r,0,7);g.fill();g.fillStyle=colB;g.beginPath();g.arc(x+d/2,y,r,0,7);g.fill();
 g.globalAlpha=1;g.save();g.beginPath();g.arc(x-d/2,y,r,0,7);g.clip();g.fillStyle='#7A2DD6';g.beginPath();g.arc(x+d/2,y,r,0,7);g.fill();g.restore();T_(g,a,x-d/2-r*.45,y,font,'#fff');T_(g,b,x+d/2+r*.45,y,font,'#fff');if(p>.9)T_(g,mid,x,y,'900 44px PL','#fff');g.restore()};
// 56: 7단계가 2단계로 접힌다(자동화)
F.collapseSteps=(g,t,t0,{n=7,keep=['입력','결과'],x=F.cx,y=F.cy,color='#fff',accent='#2EBD6B',font='900 52px PL'})=>{const p=eio(cl((t-t0-.6)/.8));g.save();for(let i=0;i<n;i++){const Y0=y+(i-(n-1)/2)*110,first=i==0,last=i==n-1,Y=first?mix(Y0,y-130,p):last?mix(Y0,y+130,p):mix(Y0,y,p);
 g.globalAlpha=(first||last)?1:1-p;g.fillStyle=(first||last)&&p>.5?accent:color;g.beginPath();g.roundRect(x-260,Y-42,520,84,26);g.fill();T_(g,first?keep[0]:last?keep[1]:(i+1)+'단계',x,Y+2,font,(first||last)&&p>.5?'#fff':'#111')}g.restore()};
// 57: 가운데 단어에서 가지가 뻗어 나간다(마인드맵)
F.mindmap=(g,t,t0,{center,items,x=F.cx,y=F.cy,R=320,font='900 46px PL',color='#FF5A1F'})=>{g.save();items.forEach((s,i)=>{const a=-PI/2+i*2*PI/items.length,q=eio(cl((t-t0-.3-i*.12)/.4)),X=x+Math.cos(a)*R*q,Y=y+Math.sin(a)*R*q;g.strokeStyle=color;g.lineWidth=6;g.beginPath();g.moveTo(x,y);g.quadraticCurveTo(x+Math.cos(a+.4)*R*.5,y+Math.sin(a+.4)*R*.5,X,Y);g.stroke();
 if(q>.8){g.font=font;const w=g.measureText(s).width+50;g.fillStyle='#fff';g.beginPath();g.roundRect(X-w/2,Y-42,w,84,42);g.fill();T_(g,s,X,Y+2,font,'#111')}});const a=sp(t-t0,14,.6);g.save();g.translate(x,y);g.scale(a,a);g.fillStyle=color;g.beginPath();g.arc(0,0,120,0,7);g.fill();T_(g,center,0,3,'900 54px PL','#fff');g.restore();g.restore()};
// 58: 노드에 차례로 불이 들어온다(AI 작업 흐름). nodes=[[x,y,이름],…] 순서대로
F.nodeLight=(g,t,t0,{nodes,step=.5,on='#FF5A1F',off='rgba(255,255,255,.25)',font='800 40px PR'})=>{g.save();for(let i=1;i<nodes.length;i++){const q=eio(cl((t-t0-i*step+.2)/.3));const [a,b]=[nodes[i-1],nodes[i]];g.strokeStyle=off;g.lineWidth=6;g.beginPath();g.moveTo(a[0],a[1]);g.lineTo(b[0],b[1]);g.stroke();g.strokeStyle=on;g.beginPath();g.moveTo(a[0],a[1]);g.lineTo(mix(a[0],b[0],q),mix(a[1],b[1],q));g.stroke()}
 nodes.forEach(([X,Y,s],i)=>{const lit=t>=t0+i*step;g.fillStyle=lit?on:'#2A2F3A';g.beginPath();g.arc(X,Y,lit?62:54,0,7);g.fill();g.strokeStyle=lit?'#fff':off;g.lineWidth=4;g.stroke();if(s)T_(g,s,X,Y+100,font,'#fff')});g.restore()};
// 59: 층 구조가 3D로 벌어진다(평행사변형 판이 위아래로 갈라짐)
F.layers=(g,t,t0,{labels,x=F.cx,y=F.cy,w=560,colors=['#FF5A1F','#2F6BFF','#2EBD6B','#FFC21A'],font='900 48px PL'})=>{const p=eio(cl((t-t0)/.9)),n=labels.length;g.save();for(let i=n-1;i>=0;i--){const Y=y+(i-(n-1)/2)*mix(30,190,p);g.fillStyle=colors[i%4];g.beginPath();g.moveTo(x,Y-110);g.lineTo(x+w/2,Y);g.lineTo(x,Y+110);g.lineTo(x-w/2,Y);g.fill();if(p>.6)T_(g,labels[i],x,Y,font,'#fff')}g.restore()};
// 60·84: 도미노가 차례로 넘어진다 / 블록이 박자마다 쌓인다
F.dominoChain=(g,t,t0,{labels,x0=F.SPEC.safe[0]+80,y=F.cy+200,gap=150,w=60,h=300,color='#fff',accent='#FF5A1F',font='800 40px PR'})=>{g.save();labels.forEach((s,i)=>{const q=eio(cl((t-t0-i*.22)/.3)),X=x0+i*gap;g.save();g.translate(X+w/2,y);g.rotate(q*1.15);g.fillStyle=q>0?accent:color;g.fillRect(-w,-h,w,h);g.restore();T_(g,s,X,y+70,font,'#fff')});g.restore()};
F.blockTower=(g,t,t0,{labels,x=F.cx,y=F.SPEC.bottom[1]-120,bh=120,beat=.5,colors=['#FF5A1F','#2F6BFF','#2EBD6B','#FFC21A'],font='900 50px PL'})=>{g.save();labels.forEach((s,i)=>{const T=t-t0-i*beat;if(T<0)return;const q=sp(T,14,.6),Y=y-i*(bh+10),w=640-i*60;g.fillStyle=colors[i%4];g.beginPath();g.roundRect(x-w/2,mix(Y-700,Y-bh,q),w,bh,24);g.fill();T_(g,s,x,mix(Y-700,Y-bh,q)+bh/2,font,'#fff')});g.restore()};

// ── 글자 애니메이션(키네틱 타이포) ──────────────
// 61·83·89: 점 하나가 낱말 사이를 뛰어다니며 잇는다(선이 남는다)
F.dotLink=(g,t,t0,{words,pos,step=.6,font='900 90px PL',color='#fff',dot='#FF5A1F'})=>{const k=Math.min(words.length-1,Math.max(0,(t-t0)/step)),i=Math.floor(k),f=eio(k-i);g.save();g.strokeStyle=dot;g.lineWidth=6;g.beginPath();
 for(let j=0;j<=i;j++){const [X,Y]=pos[j];j?g.lineTo(X,Y+60):g.moveTo(X,Y+60)}if(i<words.length-1)g.lineTo(mix(pos[i][0],pos[i+1][0],f),mix(pos[i][1],pos[i+1][1],f)+60);g.stroke();
 words.forEach((w,j)=>{if(j<=i||(j==i+1&&f>.8))T_(g,w,pos[j][0],pos[j][1],font,color)});const [a,b]=pos[i],[c,d]=pos[Math.min(i+1,words.length-1)];g.fillStyle=dot;g.beginPath();g.arc(mix(a,c,f),mix(b,d,f)+60-Math.sin(f*PI)*120,20,0,7);g.fill();g.restore()};
// 63: 마스크(보이지 않는 선) 아래에서 줄마다 밀려 올라온다
F.maskRise=(g,t,t0,{lines,x=F.cx,y=F.cy,font='900 120px PL',color='#fff',lh=1.15,step=.12})=>{const fs=fs_(font),n=lines.length;g.save();lines.forEach((l,i)=>{const Y=y+(i-(n-1)/2)*fs*lh,q=eio(cl((t-t0-i*step)/.5));g.save();g.beginPath();g.rect(0,Y-fs*.62,1080,fs*1.24);g.clip();T_(g,l,x,Y+(1-q)*fs*1.2,font,color);g.restore()});g.restore()};
// 64: 타자기 — 한 글자씩, 커서가 깜박
F.typewriter=(g,t,t0,{text,x=F.cx,y=F.cy,font='800 72px PR',color='#fff',cps=12,lh=1.35})=>{const lines=String(text).split('\n'),fs=fs_(font);let left=Math.floor((t-t0)*cps);g.save();lines.forEach((l,i)=>{const s=l.slice(0,Math.max(0,left));left-=l.length;const Y=y+(i-(lines.length-1)/2)*fs*lh;g.font=font;const W=g.measureText(l).width;T_(g,s,x-W/2,Y,font,color,'left');
 if(left<0&&left>-l.length-1&&Math.floor(t*2.5)%2==0){const cx=x-W/2+g.measureText(s).width+8;g.fillStyle=color;g.fillRect(cx,Y-fs*.45,6,fs*.9)}});g.restore()};
// 65: 큰 숫자와 글자가 맞물린 포스터(숫자 뒤로 글자가 지나간다)
F.numPoster=(g,t,t0,{num,word,x=F.cx,y=F.cy,color='#FF5A1F',fg='#fff'})=>{const a=sp(t-t0,12,.7),q=eio(cl((t-t0-.3)/.6));g.save();g.globalAlpha=1;T_(g,num,x,y,`900 ${Math.round(620*a)}px PL`,color);g.save();g.beginPath();g.rect(0,y-40,1080,80);g.clip();g.restore();
 T_(g,word,mix(x+700,x,q),y+30,'900 120px PL',fg);g.restore()};
// 66: 단어가 녹아 흘렀다가 다시 굳는다(세로로 늘어짐)
F.meltWord=(g,t,t0,{word,x=F.cx,y=F.cy,font='900 150px PL',color='#fff',dur=1.2})=>{const T=cl((t-t0)/dur),m=Math.sin(T*PI);g.save();g.font=font;const W=g.measureText(word).width,cols=40;for(let i=0;i<cols;i++){const sx=x-W/2+W*i/cols,drop=m*(80+H(i)*220);g.save();g.beginPath();g.rect(sx,0,W/cols+1,1920);g.clip();g.translate(0,0);g.scale(1,1);
 g.fillStyle=color;g.textAlign='center';g.textBaseline='middle';g.fillText(word,x,y);if(drop>1){g.globalAlpha=.9;g.fillRect(sx,y+fs_(font)*.3,W/cols+1,drop)}g.restore()}g.restore()};
// 67: 말하는 속도에 맞춰 큰 세로 자막(낱말마다 나타나고 지금 낱말 강조)
F.karaoke=(g,t,t0,{words,times,x=F.cx,y=F.cy,font='900 110px PL',color='#fff',hi='#FFD400',per=3})=>{const k=times.findIndex((tt,i)=>t<t0+(times[i+1]??1e9))<0?words.length-1:times.findIndex((tt,i)=>t<t0+(times[i+1]??1e9)),grp=Math.floor(k/per);g.save();
 const shown=words.slice(grp*per,grp*per+per);shown.forEach((w,i)=>{const j=grp*per+i;if(t<t0+times[j])return;const a=sp(t-t0-times[j],16,.55);g.save();g.translate(x,y+(i-(shown.length-1)/2)*fs_(font)*1.2);g.scale(a,a);T_(g,w,0,0,font,j==k?hi:color);g.restore()});g.restore()};
// 68: 그림자가 겹겹이 늘어나는 3D 글자
F.extrude=(g,t,t0,{word,x=F.cx,y=F.cy,font='900 200px PL',color='#fff',shade='#FF5A1F',depth=22,dx=4,dy=5})=>{const n=Math.round(depth*eio(cl((t-t0)/.7)));g.save();for(let i=n;i>0;i--)T_(g,word,x+i*dx,y+i*dy,font,shade);T_(g,word,x,y,font,color);g.restore()};
// 70: 한 획으로 써지는 손글씨 — 글자를 왼쪽부터 드러내고 펜 끝 점이 따라간다
F.handWrite=(g,t,t0,{text,x=F.cx,y=F.cy,font='130px DK',color='#fff',dur=1.4,pen='#FF5A1F'})=>{g.save();g.font=font;const W=g.measureText(text).width,p=eio(cl((t-t0)/dur)),fs=fs_(font);g.beginPath();g.rect(x-W/2-20,y-fs,(W+40)*p,fs*2);g.clip();T_(g,text,x,y,font,color);g.restore();
 if(p>0&&p<1){g.fillStyle=pen;g.beginPath();g.arc(x-W/2+W*p,y+Math.sin(p*40)*fs*.25,12,0,7);g.fill()}};
// 72: 물음표가 휘어 느낌표가 된다
F.qToBang=(g,t,t0,{x=F.cx,y=F.cy,size=360,color='#fff',accent='#FF5A1F'})=>{const p=eio(cl((t-t0)/.6));g.save();g.lineCap='round';g.lineWidth=size*.16;g.strokeStyle=p<.5?color:accent;g.beginPath();
 const r=size*.32*(1-p);g.arc(x,y-size*.35,Math.max(r,.01),PI*(1+p),PI*(2.4-0.4*p));g.lineTo(x,y+size*.12);g.stroke();g.fillStyle=g.strokeStyle;g.beginPath();g.arc(x,y+size*.45,size*.1,0,7);g.fill();g.restore()};
// 73: 한 단어가 박자마다 옷(글꼴·색·판)을 갈아입는다
F.wordOutfits=(g,t,t0,{word,looks,beat=.5,x=F.cx,y=F.cy})=>{const k=Math.max(0,Math.floor((t-t0)/beat))%looks.length,[font,color,bg]=looks[k];if(bg){g.fillStyle=bg;g.fillRect(0,0,1080,1920)}const a=sp((t-t0)%beat,18,.55);g.save();g.translate(x,y);g.scale(mix(1.15,1,a),mix(1.15,1,a));T_(g,word,0,0,font,color);g.restore()};
// 74: 목록이 위로 흐르며 가운데 칸에 온 것이 하나씩 선택된다
F.listScroll=(g,t,t0,{items,x=F.cx,y=F.cy,rh=130,speed=1.2,font='900 72px PL',color='rgba(255,255,255,.35)',hi='#fff',bar='#FF5A1F'})=>{const off=((t-t0)*speed)%items.length;g.save();g.beginPath();g.rect(0,F.SPEC.top[3]+60,1080,F.SPEC.bottom[1]-F.SPEC.top[3]-120);g.clip();g.fillStyle=bar;g.beginPath();g.roundRect(x-400,y-rh/2,800,rh,rh/2);g.fill();
 for(let i=-4;i<=4;i++){const j=((Math.floor(off)+i)%items.length+items.length)%items.length,Y=y+(i-(off%1))*rh,d=Math.abs(Y-y)/rh;T_(g,items[j],x,Y,font,d<.5?hi:color)}g.restore()};
// 75: 이름이 올라가고(크레딧) 마지막에 로고로 닫힌다
F.credits=(g,t,t0,{names,logo,x=F.cx,y=F.cy,speed=260,font='800 56px PR',color='#fff'})=>{const T=t-t0,top=F.SPEC.bottom[1]-T*speed;g.save();names.forEach((n,i)=>{const Y=top+i*110;if(Y>F.SPEC.top[3]&&Y<F.SPEC.bottom[1])T_(g,n,x,Y,font,color)});const end=top+names.length*110;if(end<y){const a=sp(T-(names.length*110+F.SPEC.bottom[1]-y)/speed,13,.6);g.save();g.translate(x,y);g.scale(a,a);T_(g,logo,0,0,'900 140px PL','#FF5A1F');g.restore()}g.restore()};

// ── 도형·추상 ───────────────────────────────
// 79: 합쳐졌다 나뉘는 메타볼(두 원 사이를 끈적하게 잇는다)
F.metaball=(g,t,{x=F.cx,y=F.cy,R=170,color='#FF5A1F'})=>{const d=Math.abs(Math.sin(t*1.4))*420;g.save();g.fillStyle=color;[[-1],[1]].forEach(([s])=>{g.beginPath();g.arc(x+s*d/2,y,R,0,7);g.fill()});if(d<2.6*R){const k=1-d/(2.6*R),nh=R*mix(.2,.95,k);g.beginPath();g.moveTo(x-d/2,y-nh);g.quadraticCurveTo(x,y-nh*(1-k*.2)*.6,x+d/2,y-nh);g.lineTo(x+d/2,y+nh);g.quadraticCurveTo(x,y+nh*.6,x-d/2,y+nh);g.fill()}g.restore()};
// 82: 버튼(알약) → 원(로딩) → 체크. 도형 하나로
F.buttonToCheck=(g,t,t0,{x=F.cx,y=F.cy,label='보내기',color='#2F6BFF',ok='#2EBD6B'})=>{const T=t-t0,p=eio(cl((T-.3)/.35)),w=mix(560,150,p),c=T>1.4;g.save();g.fillStyle=c?ok:color;g.beginPath();g.roundRect(x-w/2,y-75,w,150,75);g.fill();
 if(p<.3)T_(g,label,x,y+3,'900 60px PL','#fff');else if(!c){g.strokeStyle='#fff';g.lineWidth=10;g.lineCap='round';g.beginPath();g.arc(x,y,36,T*9,T*9+4.4);g.stroke()}else{const q=eio(cl((T-1.4)/.3));g.strokeStyle='#fff';g.lineWidth=14;g.lineCap='round';g.beginPath();g.moveTo(x-34,y+2);g.lineTo(x-10,y+28*q);g.lineTo(x-10+48*q,y-30*q);g.stroke()}g.restore()};
// 85: 아이콘들이 궤도를 돌다 가운데(로고)로 빨려 든다
F.orbitIn=(g,t,t0,{icons,center,x=F.cx,y=F.cy,R=330,dur=2,font='900 54px PL',color='#FF5A1F'})=>{const p=eio(cl((t-t0)/dur));g.save();icons.forEach((s,i)=>{const a=t*1.2+i*2*PI/icons.length,r=R*(1-p),X=x+Math.cos(a)*r,Y=y+Math.sin(a)*r*.6;if(p<.97){g.fillStyle='#fff';g.beginPath();g.arc(X,Y,64*(1-p*.6),0,7);g.fill();T_(g,s,X,Y+2,`900 ${Math.round(46*(1-p*.6))}px PL`,'#111')}});
 const a=sp(t-t0-dur+.2,13,.6);if(a>0){g.save();g.translate(x,y);g.scale(a,a);T_(g,center,0,0,'900 130px PL',color);g.restore()}g.restore()};

// ── 파티클·빛 ───────────────────────────────
// 87: 바깥으로 그어지는 선 다발 가운데에 축하 문구
F.burstLines=(g,t,t0,{text,x=F.cx,y=F.cy,n=24,color='#FFD400',font='900 110px PL'})=>{const p=eio(cl((t-t0)/.6));g.save();g.strokeStyle=color;g.lineWidth=10;g.lineCap='round';for(let i=0;i<n;i++){const a=i*2*PI/n,r0=220+60*(i%2),r1=r0+mix(0,200,p),r00=r0+mix(0,190,cl((t-t0-.4)/.6));if(r1-r00<2)continue;g.beginPath();g.moveTo(x+Math.cos(a)*r00,y+Math.sin(a)*r00);g.lineTo(x+Math.cos(a)*r1,y+Math.sin(a)*r1);g.stroke()}
 const a=sp(t-t0-.15,13,.6);g.save();g.translate(x,y);g.scale(a,a);T_(g,text,0,0,font,'#fff');g.restore();g.restore()};
// 88: 슬릿 스캔 — 가는 틈이 지나가며 실루엣(그림)이 드러난다
F.slitScan=(g,t,t0,{draw,dur=1.4,x0=F.SPEC.safe[0],x1=F.SPEC.safe[2],color='#fff'})=>{const p=eio(cl((t-t0)/dur)),sx=mix(x0,x1,p);g.save();g.beginPath();g.rect(x0,0,sx-x0,1920);g.clip();draw&&draw(g);g.restore();if(p<1){g.fillStyle=color;g.fillRect(sx-4,F.SPEC.top[3]+40,8,F.SPEC.bottom[1]-F.SPEC.top[3]-80)}};

// ── 캐릭터·일러스트(코드로 그림) ─────────────────
// 91: 동글 블롭 캐릭터(눈 깜박·통통). 버튼 위를 눌러 준다: hops=[[x,y],…]
F.blob=(g,t,{x=F.cx,y=F.cy,r=110,color='#FF5A1F',face='#111',look=0})=>{const b=1+.05*Math.sin(t*6),bl=(t%3)<.12;g.save();g.translate(x,y);g.scale(1/b,b);g.fillStyle=color;g.beginPath();g.ellipse(0,0,r,r*.9,0,0,7);g.fill();
 g.fillStyle=face;[-1,1].forEach(s=>{g.beginPath();if(bl)g.fillRect(s*r*.32-14+look*8,-r*.15,28,6);else g.ellipse(s*r*.32+look*8,-r*.12,12,18,0,0,7);g.fill()});g.lineWidth=6;g.strokeStyle=face;g.beginPath();g.arc(look*8,r*.15,r*.18,.15*PI,.85*PI);g.stroke();g.restore()};
F.blobHelper=(g,t,t0,{buttons,x=F.cx,y=F.cy,step=.8,color='#FF5A1F',font='900 52px PL'})=>{const n=buttons.length,k=Math.min(n-1,Math.max(0,Math.floor((t-t0)/step))),f=((t-t0)%step)/step;g.save();
 buttons.forEach((s,i)=>{const Y=y+(i-(n-1)/2)*170,pressed=i<k||(i==k&&f>.55);g.fillStyle=pressed?'#2EBD6B':'#fff';g.beginPath();g.roundRect(x-260,Y-60+(pressed&&i==k&&f<.7?8:0),520,120,60);g.fill();T_(g,s,x,Y+3,font,pressed?'#fff':'#111')});
 const Yk=y+(k-(n-1)/2)*170,hop=Math.sin(cl(f/.55)*PI)*140;F.blob(g,t,{x:x+300,y:Yk-90-hop,r:80,color});g.restore()};
// 92: 작은 로봇(네모 머리·안테나·팔)이 단계마다 일한다: 단계 글자를 하나씩 들어 올린다
F.robot=(g,t,{x=F.cx,y=F.cy,s=1,color='#C9D3E0',eye='#2F6BFF',arm=0})=>{g.save();g.translate(x,y);g.scale(s,s);g.fillStyle=color;g.beginPath();g.roundRect(-90,-200,180,150,30);g.fill();g.beginPath();g.roundRect(-110,-40,220,200,36);g.fill();
 g.strokeStyle=color;g.lineWidth=10;g.beginPath();g.moveTo(0,-200);g.lineTo(0,-250);g.stroke();g.fillStyle='#FF5A1F';g.beginPath();g.arc(0,-260,16+3*Math.sin(t*8),0,7);g.fill();
 g.fillStyle=eye;const bl=(t%2.6)<.1;[-1,1].forEach(k=>{g.beginPath();bl?g.fillRect(k*38-16,-130,32,6):g.arc(k*38,-127,16,0,7);g.fill()});g.strokeStyle=color;g.lineWidth=26;g.lineCap='round';
 g.beginPath();g.moveTo(-110,10);g.lineTo(-170,80+arm*-140);g.stroke();g.beginPath();g.moveTo(110,10);g.lineTo(170,80+arm*-140);g.stroke();g.restore()};
// 93: 막대 인간(달리기·점프). phase 0~1 이 한 걸음
F.stickman=(g,t,{x=F.cx,y=F.cy,s=1,color='#fff',run=true,jump=0})=>{const ph=t*7,yy=y-jump;g.save();g.translate(x,yy);g.scale(s,s);g.strokeStyle=color;g.fillStyle=color;g.lineWidth=14;g.lineCap='round';g.beginPath();g.arc(0,-200,40,0,7);g.fill();
 g.beginPath();g.moveTo(0,-160);g.lineTo(0,-40);g.stroke();const L=run?Math.sin(ph):0,A=run?Math.sin(ph+PI):0;[[L,1],[-L,-1]].forEach(([k])=>{g.beginPath();g.moveTo(0,-40);g.lineTo(k*60,40);g.lineTo(k*60+(k>0?20:-20),110);g.stroke()});
 [[A],[-A]].forEach(([k])=>{g.beginPath();g.moveTo(0,-130);g.lineTo(k*70,-60);g.stroke()});g.restore()};
// 94: 마스코트가 손을 흔든다(코드 그림, 정월 사진 컷이 없을 때). 끝에 로고로 바뀔 수 있게 morph(0~1)
F.mascotWave=(g,t,{x=F.cx,y=F.cy,r=150,color='#FFD400',morph=0,logo='자오선'})=>{g.save();g.globalAlpha=1-morph;F.blob(g,t,{x,y,r,color});g.strokeStyle=color;g.lineWidth=28;g.lineCap='round';const w=Math.sin(t*9)*.5;g.beginPath();g.moveTo(x+r*.8,y);g.lineTo(x+r*1.4+Math.cos(-1.2+w)*60,y-r*.6+Math.sin(-1.2+w)*60);g.stroke();
 g.globalAlpha=morph;T_(g,logo,x,y,'900 150px PL',color);g.restore()};
// 95: 아이콘 캐릭터들이 줄 서서 차례로 앞으로 나와 자기소개(말풍선)
F.iconTeam=(g,t,t0,{members,step=1,x=F.cx,y=F.cy+120,colors=['#FF5A1F','#2F6BFF','#2EBD6B','#FFC21A','#B26BFF']})=>{const n=members.length,k=Math.min(n-1,Math.max(0,Math.floor((t-t0)/step)));members.forEach(([name,line],i)=>{const X=x+(i-(n-1)/2)*170,on=i==k,q=on?eio(cl(((t-t0)-k*step)/.3)):0;
 F.blob(g,t+i,{x:X,y:y-q*60,r:on?90:70,color:colors[i%5],look:(k-i)*.6});T_(g,name,X,y+130,'800 40px PR','#fff');if(on&&q>.6)F.bubble(g,t,t0+k*step+.2,{text:line,x:F.cx,y:y-360,tx:X,font:'72px BZ'})})};

// ── 사진·음악·코드 ──────────────────────────
// 97: 박자에 맞춰 숨 쉬는 원형 막대(뮤직 비주얼라이저). bpm 으로 맥박
F.visualizer=(g,t,{x=F.cx,y=F.cy,R=200,n=48,bpm=120,color='#FF5A1F'})=>{const beat=Math.pow(1-((t*bpm/60)%1),3);g.save();g.strokeStyle=color;g.lineWidth=12;g.lineCap='round';for(let i=0;i<n;i++){const a=i*2*PI/n,h=40+beat*120*(.4+.6*H(i))+20*Math.sin(t*5+i);g.beginPath();g.moveTo(x+Math.cos(a)*R,y+Math.sin(a)*R);g.lineTo(x+Math.cos(a)*(R+h),y+Math.sin(a)*(R+h));g.stroke()}
 g.fillStyle=color;g.beginPath();g.arc(x,y,R*.6*(1+beat*.08),0,7);g.fill();g.restore()};
// 100: 구독(팔로우) 버튼 — 커서가 눌러 '팔로잉'으로, 종 흔들림
F.followBtn=(g,t,t0,{x=F.cx,y=F.cy,label='팔로우',done='팔로잉 ✓',color='#FF3B30'})=>{const T=t-t0,on=T>1;g.save();const a=sp(T,14,.6);g.translate(x,y);g.scale(a*(T>.95&&T<1.1?.94:1),a);g.fillStyle=on?'#444':color;g.beginPath();g.roundRect(-260,-80,520,160,80);g.fill();T_(g,on?done:label,0,3,'900 64px PL','#fff');g.restore();
 const c=eio(cl(T/.9));g.fillStyle='#fff';g.beginPath();g.moveTo(mix(x+380,x+60,c),mix(y+260,y+20,c));g.lineTo(mix(x+380,x+60,c)+26,mix(y+260,y+20,c)+60);g.lineTo(mix(x+380,x+60,c)+60,mix(y+260,y+20,c)+40);g.fill();
 if(on){const r=Math.sin((T-1)*30)*.4*Math.max(0,1-(T-1)*2);g.save();g.translate(x+330,y-60);g.rotate(r);T_(g,'🔔',0,0,'80px PR','#fff');g.restore()}};

// ── 이름표(목록) ────────────────────────────
Object.assign(F.LIST,{선하나그리기:'끊기지 않는 선 하나가 로고·아이콘·밑줄을 그림(#1·77)',엉킨선풀기:'엉킨 선이 곧게 풀림(#6)',흐르는선:'가는 선 여러 줄이 물결처럼 흐름(#90)',타일뒤집기:'타일 격자가 도미노처럼 뒤집히며 판이 바뀜(#3·80)',숫자갈라짐:'숫자가 위아래로 갈라지며 다음 숫자(#5 카운트다운)',스위스그리드:'굵은 선이 칸을 나누고 칸마다 글자가 박힘(#7)',긴캔버스팬:'긴 판을 카메라가 따라감(#8·44)',카드6장열기:'3×2 카드가 차례로 열림(#23)',폴라로이드:'사진 카드가 떨어져 쌓임(#96)',
 폰화면:'폰 틀 + 화면 + 터치 물결(#26~35)',검색타이핑:'한 글자씩 치면 결과 줄이 쏟아짐(#13)',할일체크:'체크할 때마다 진행 막대가 참(#14)',점에서카드:'진행 점이 카드로 늘어남(#15)',블록끌어조립:'블록을 끌어 칸에 끼움(#16)',결제흐름:'버튼→처리→체크로 끝나는 결제(#18)',전후슬라이더:'가운데 손잡이로 가르는 전·후(#19)',알림접기:'쌓인 알림이 한 장으로 접힘(#20)',캘린더채움:'빈 주간 캘린더가 채워짐(#21)',코드미리보기:'코드 한 줄마다 오른쪽 화면이 바뀜(#22·98)',테마물결:'누른 자리에서 원이 퍼지며 판 색이 바뀜(#24)',업로드링:'파일이 들어오고 링이 차서 체크(#25)',
 막대가화면:'막대가 자라다 마지막 막대가 화면을 차지(#36)',선그래프숫자:'선 끝이 숫자로 바뀜(#37)',순위막대:'순위가 바뀔 때마다 막대가 자리를 바꿈(#38)',도넛이름표:'조각마다 선이 뻗어 이름표(#32·39)',숫자이어달리기:'숫자 셋이 이어 달림(#40)',퍼널:'아래로 좁아지는 퍼널과 새는 단계(#41)',지도맥박:'지도 점이 숨 쉬듯 커짐(#42)',좌우대결:'가운데 선이 비율만큼 밀림(#43)',링네개:'링 네 개가 박자를 나눠 참(#45)',지층흐름:'쌓인 영역이 흐름(#46)',점에서추세선:'흩어진 점이 추세선으로(#48)',표셀줌:'행을 따라가다 셀 하나로 줌(#49)',
 박스낳기:'박스가 다음 박스를 낳음(#51)',왕복점:'점 하나가 두 상자 사이를 왕복(#52)',구조도:'위에서 가지를 치는 구조도(#53)',순환:'원을 도는 4단계(#54)',교집합:'두 원이 겹쳐 생기는 교집합(#55)',단계접기:'7단계가 2단계로 접힘(#56)',마인드맵:'가운데에서 가지가 뻗음(#57)',노드불켜기:'노드에 차례로 불(#58)',층벌어짐:'층이 3D로 벌어짐(#59)',도미노:'도미노가 차례로 넘어짐(#60)',블록탑:'박자마다 블록이 쌓임(#84)',
 점이잇는글자:'점 하나가 낱말 사이를 뛰며 이음(#61·83·89)',마스크올라오기:'보이지 않는 선 아래에서 줄마다 올라옴(#63)',타자기:'한 글자씩·커서 깜박(#64)',숫자포스터:'큰 숫자와 글자가 맞물림(#65)',녹는단어:'단어가 녹아 흘렀다 굳음(#66)',큰세로자막:'말하는 속도에 맞춘 큰 자막·지금 낱말 강조(#67)',입체그림자글자:'그림자가 겹겹이 늘어나는 글자(#68)',한획손글씨:'펜 끝이 따라가며 써지는 손글씨(#70)',물음표느낌표:'물음표가 휘어 느낌표(#72)',옷갈아입는단어:'한 단어가 박자마다 글꼴·색·판을 바꿈(#73)',목록흐름선택:'위로 흐르며 가운데 줄이 선택됨(#74)',크레딧로고:'이름이 올라가고 로고로 닫힘(#75)',
 메타볼:'두 원이 끈적하게 합쳐졌다 나뉨(#79)',버튼에서체크:'버튼→로딩 원→체크(#82)',궤도빨려듦:'궤도를 돌다 가운데로 빨려 듦(#85)',선다발축하:'선 다발이 뻗고 가운데 문구(#87)',슬릿스캔:'가는 틈이 지나가며 그림이 드러남(#88)',
 블롭캐릭터:'눈 깜박·통통 튀는 동글 캐릭터(#91)',블롭도우미:'블롭이 버튼을 하나씩 눌러 줌(#91)',로봇:'작은 로봇(눈 깜박·안테나·팔)(#92)',막대인간:'달리고 뛰는 막대 인간(#93)',마스코트인사:'손 흔드는 마스코트가 로고로(#94)',아이콘팀소개:'줄 선 캐릭터가 차례로 나와 자기소개(#95)',비주얼라이저:'박자에 숨 쉬는 원형 막대(#97)',팔로우버튼:'커서가 눌러 팔로잉으로·종 흔들림(#100)'});

// 100개 번호 → 우리 함수(이미 있던 것 포함). 새 편을 만들 때 번호나 상황으로 찾는다.
F.R100={1:['lineDraw'],2:['counterRush','kpiRelay'],3:['tileFlip','wordBlocks'],4:['flip'],5:['splitNumber'],6:['untangle'],7:['swissGrid'],8:['panCanvas'],9:['assemble'],10:['toggle','counterRush'],
 11:['morphBox','growBars'],12:['phone','panCanvas'],13:['searchType'],14:['checklist'],15:['dotsToCard'],16:['dragBlocks'],17:['chat','growBars'],18:['payFlow','stateBtn'],19:['beforeAfter','slider'],20:['stackCollapse'],21:['weekFill'],22:['codePreview'],23:['gridCards'],24:['themeRipple','circleWipe'],25:['uploadRing','ring'],
 26:['phone'],27:['phone'],28:['phone','checklist'],29:['phone','flip'],30:['phone','toast'],31:['phone','ring','asterisk'],32:['phone','donut'],33:['phone','lineDraw'],34:['phone','gridCards'],35:['phone','circleWipe'],
 36:['growBars'],37:['lineGraph'],38:['barRace'],39:['donut'],40:['kpiRelay'],41:['funnel'],42:['mapPulse'],43:['versus'],44:['panCanvas','dotLand'],45:['ringsBeat'],46:['stream'],47:['counterRush','bigPop'],48:['scatterTrend'],49:['tableZoom'],50:['growBars','lineGraph','donut'],
 51:['boxChain'],52:['packet'],53:['tree'],54:['cycle'],55:['venn'],56:['collapseSteps'],57:['mindmap'],58:['nodeLight','hub'],59:['layers'],60:['dominoChain'],
 61:['dotLink'],62:['beatWords'],63:['maskRise'],64:['typewriter'],65:['numPoster'],66:['meltWord'],67:['karaoke'],68:['extrude'],69:['marquee'],70:['handWrite'],71:['pixelBlocks'],72:['qToBang'],73:['wordOutfits'],74:['listScroll'],75:['credits'],
 76:['shapeMorph'],77:['lineDraw'],78:['dotwave','particleText'],79:['metaball','blobs'],80:['tileFlip'],81:['ripples'],82:['buttonToCheck'],83:['constellation','dotLink'],84:['blockTower'],85:['orbitIn'],
 86:['particleText'],87:['burstLines'],88:['slitScan'],89:['particleText','dotLink'],90:['flowLines'],
 91:['blobHelper'],92:['robot'],93:['stickman'],94:['mascotWave'],95:['iconTeam'],96:['polaroids'],97:['visualizer'],98:['codePreview'],99:['counterRush','chips','followBtn'],100:['followBtn']};
Object.assign(F.USE,{'상품·앱 소개':(F.USE['상품·앱 소개']||[]).concat(['폰화면','검색타이핑','결제흐름','버튼에서체크','코드미리보기','업로드링']),'숫자·통계':(F.USE['숫자·통계']||[]).concat(['막대가화면','선그래프숫자','순위막대','도넛이름표','숫자이어달리기','링네개','지층흐름','점에서추세선']),
 '개념 설명':(F.USE['개념 설명']||[]).concat(['박스낳기','왕복점','구조도','순환','교집합','단계접기','마인드맵','노드불켜기','층벌어짐','도미노']),'관계·궁합':(F.USE['관계·궁합']||[]).concat(['교집합','좌우대결','점이잇는글자']),
 '훅(첫 1초)':(F.USE['훅(첫 1초)']||[]).concat(['숫자갈라짐','물음표느낌표','옷갈아입는단어','타일뒤집기','테마물결']),'캐릭터':(F.USE['캐릭터']||[]).concat(['블롭도우미','로봇','막대인간','마스코트인사','아이콘팀소개']),
 '끝장면(행동)':(F.USE['끝장면(행동)']||[]).concat(['팔로우버튼','크레딧로고','선다발축하','궤도빨려듦']),'대화·사연':(F.USE['대화·사연']||[]).concat(['타자기','큰세로자막','한획손글씨','알림접기']),'감성·신비':(F.USE['감성·신비']||[]).concat(['흐르는선','메타볼','슬릿스캔','녹는단어','비주얼라이저'])});
})();
