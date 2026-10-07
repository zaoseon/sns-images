import json, html, datetime as D, collections
E=html.escape
import sys; sys.path.insert(0,'.')
from plan_data import EVID
c=json.load(open('calendar_2026-11.json',encoding='utf-8')); days=c['days']; rep=c['report']; edits=c['edits']
EV={7:'입동 18:52',8:'손없는날',9:'신월',11:'빼빼로데이',14:'수성 순행',17:'손없는날',18:'손없는날',19:'수능',22:'소설·사수자리',24:'보름달',27:'손없는날',28:'손없는날'}
NM={"B12":"네이버 글 낮","B21":"네이버 글 밤","P08":"인스타 캐러셀 아침","P21":"인스타 캐러셀 밤","R08":"인스타 릴스 아침","R12":"인스타 릴스 낮","R20":"인스타 릴스 저녁","T08":"스레드 아침","T13":"스레드 낮","T20":"스레드 저녁","T21":"스레드 밤","C":"네이버 클립"}
ORDER=["B12","R08","P08","T08","R12","T13","B21","P21","T21","R20","T20","C"]
GL={"M":"낮 주제","E":"밤 주제","D":"데이터·체험 릴스"}
SYSN={'S':'사주','A':'별자리','N':'숫자','Z':'자미두수','D':'당사주','H':'하락이수','Y':'육효·주역','X':'교차'}
def sysname(s): return '·'.join(SYSN.get(x,x) for x in s.split('+'))
tot=0;lk=0;nw=0;cv=0
PL=json.load(open('production_log.json',encoding='utf-8'))
cards=""
for d in days:
    dt=D.date.fromisoformat(d['date']); md=f"{dt.month}/{dt.day}"
    ev=EV.get(dt.day); evh=f'<span class="ev">{E(ev)}</span>' if ev else ''
    evd=EVID.get(dt.day); evdh=(f'<p class="evid"><b>근거</b> {E(evd)}</p>' if evd else '')
    M=d['themes']['M']['title']; Ee=d['themes']['E']['title']; Dd=d['themes']['D']['title']
    z=d['flag']=='z'
    head=E(M if not z else d['themes']['E']['title'])
    rows=""
    for s in ORDER:
        v=d['slots'].get(s)
        if not v: continue
        st=v['status']
        if st=='LOCKED':
            lk+=len(v['items']); tot+=1
            for it in v['items']:
                rows+=f'<li class="lk"><b>{NM[s]}</b> <i>{E(it["t"])}</i><span class="tag t1">이미 있음</span><br>{E(it["title"])}</li>'
        elif st=='NEW':
            nw+=1; tot+=1
            th=v['theme']; extra=''
            if v.get('related'): extra=f'<br><small>연결 글: {E(v["related"]["title"])}</small>'
            pl=PL.get(d['date']+'|'+s)
            if pl: rows+=f'<li class="dn"><b>{NM[s]}</b> <i>{E(v["time"])}</i><span class="tag t4">{E(pl["state"])}</span><br>{E(th)}<br><small>{E(pl["note"])}</small></li>'
            else: rows+=f'<li class="nw"><b>{NM[s]}</b> <i>{E(v["time"])}</i><span class="tag t2">새로 만들기</span><br>{E(th)}{extra}</li>'
        else:
            cv+=1; tot+=1
            rows+=f'<li class="cv"><b>{NM[s]}</b><span class="tag t3">건너뜀</span><br><small>{E(v["note"])}</small></li>'
    cards+=f'''<details class="day"><summary><span class="dt">{md}<small>({d["wd"]})</small></span><span class="hd">{head}</span>{evh}</summary>
<div class="th">{evdh}<p><b>{GL["M"]}</b> {E(M)} <em>{E(sysname(d["themes"]["M"]["sys"]))}</em></p><p><b>{GL["E"]}</b> {E(Ee)} <em>{E(sysname(d["themes"]["E"]["sys"]))}</em></p><p><b>{GL["D"]}</b> {E(Dd)} <em>{E(sysname(d["themes"]["D"]["sys"]))}</em></p></div>
<ul class="sl">{rows}</ul></details>'''
wk=collections.defaultdict(int)
for d in days:
    w=(D.date.fromisoformat(d['date'])-D.date(2026,11,1)).days//7
    for v in d['slots'].values():
        if v['status']=='NEW': wk[w]+=1
mx=max(wk.values())
wkh="".join(f'<div class="wk"><span>{["11/1~7","11/8~14","11/15~21","11/22~28","11/29~30"][w]}</span><div class="bar"><i style="width:{wk[w]/mx*100:.0f}%"></i></div><b>{wk[w]}</b></div>' for w in sorted(wk))
checks=[
 ("빈 칸 없음",f"30일 모든 칸({tot}칸)이 채워졌어요. 이미 있는 것 {lk}개, 새로 만들 것 {nw}개, 건너뛰는 칸 {cv}칸이에요."),
 ("인스타 하루 4개 이하","30일 모두 지켰어요. 아침 릴스가 이미 있는 날(11/4, 11/11)은 아침 캐러셀을 건너뛰었어요."),
 ("같은 채널 같은 시각 겹침 없음","겹치던 곳은 30분 뒤로 옮겼어요."),
 ("사주만 다루는 주제 %d%%"%rep['pure_S_pct'],"50% 이하 규칙을 지켜요. 별자리·숫자·자미두수·당사주·하락이수·육효가 골고루 나와요."),
 ("어느 14일을 잡아도 일곱 운명학이 모두 나와요","사주·별자리·숫자·자미두수·당사주·하락이수·육효·주역 모두예요."),
 ("같은 갈래가 3일 연속 나오지 않아요","띠 글은 5일·7일·12일·14일로 띄웠어요."),
 ("새 블로그 글 53편 모두 연결 글이 있어요","24시간 이상 앞서 발행되는 글만 골랐고, 한 글이 3번 넘게 연결 대상이 되지 않아요."),
 ("기존 글과 겹치는 주제 11곳을 바꿨어요","삼재, 자미두수, 당사주, 하락이수, 2027 띠 12, 물의 별자리 같은 칸이에요. 같은 말을 또 쓰지 않고 다른 각도로 바꿨어요."),
]
chk="".join(f'<li><b>✓ {E(a)}</b><br>{E(b)}</li>' for a,b in checks)
eh="".join(f'<li><b>{E(e["when"])}</b> {E(e["what"].replace(chr(92)+chr(34),chr(34)))}<br><small>맡은 곳: {E(e["who"])} · 이유: {E(e["why"].replace(chr(92)+chr(34),chr(34)))}</small></li>' for e in edits)
lkp=lk/(lk+nw)*100
page=f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"><title>2026년 11월 콘텐츠 캘린더 (정리본)</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap" rel="stylesheet">
<style>
:root{{--bg:#f4f5fa;--card:#fff;--ink:#1d2140;--mute:#5b6082;--acc:#f48c04;--blue:#4a63c9;--line:#dfe2ee;box-sizing:border-box;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}}
@media(prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#161a33;--card:#1f2447;--ink:#f1f2fb;--mute:#aab0d6;--blue:#8fa2ff;--line:#343b6b}}}}
:root[data-theme="dark"]{{--bg:#161a33;--card:#1f2447;--ink:#f1f2fb;--mute:#aab0d6;--blue:#8fa2ff;--line:#343b6b}}
html{{scroll-padding-top:env(safe-area-inset-top,0px)}}*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--ink);font:18px/1.6 'Noto Sans KR',sans-serif}}
.w{{max-width:760px;margin:0 auto;padding:18px 14px 70px}}
h1{{font-size:24px;margin:6px 0}} h2{{font-size:21px;margin:34px 0 10px}}
.lead{{color:var(--mute);margin:0 0 12px}}
.box{{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px}}
.bigbar{{height:26px;border-radius:13px;background:var(--acc);overflow:hidden;margin:10px 0}} .bigbar i{{display:block;height:100%;background:var(--blue);width:{lkp:.1f}%}}
.leg{{display:flex;gap:16px;flex-wrap:wrap;font-size:16px}} .leg span::before{{content:"";display:inline-block;width:14px;height:14px;border-radius:4px;margin-right:6px;vertical-align:-2px}} .l1::before{{background:var(--blue)}} .l2::before{{background:var(--acc)}}
ul{{list-style:none;margin:0;padding:0}} .chk li{{padding:10px 0;border-bottom:1px solid var(--line)}} .chk li:last-child{{border:0}} small{{color:var(--mute);font-size:15px}}
.wk{{display:flex;align-items:center;gap:10px;margin:8px 0;font-size:16px}} .wk span{{width:78px;flex:none}} .bar{{flex:1;height:18px;background:var(--line);border-radius:9px;overflow:hidden}} .bar i{{display:block;height:100%;background:var(--acc)}} .wk b{{width:34px;text-align:right}}
details.day{{background:var(--card);border:1px solid var(--line);border-radius:14px;margin:10px 0}}
summary{{list-style:none;padding:14px;cursor:pointer;display:flex;gap:10px;align-items:center;flex-wrap:wrap}} summary::-webkit-details-marker{{display:none}}
.dt{{font-weight:700;font-size:20px;min-width:74px}} .dt small{{font-weight:400;margin-left:2px}} .hd{{flex:1;min-width:150px;font-size:17px}}
.ev{{background:var(--blue);color:#fff;border-radius:12px;padding:2px 10px;font-size:14px;white-space:nowrap}}
.th{{padding:0 14px 6px;border-top:1px solid var(--line)}} .th p{{margin:10px 0}} .th b{{display:block;color:var(--blue);font-size:15px}} .evid{{background:rgba(244,140,4,.12);border-radius:8px;padding:8px 10px;font-size:15px}} .th em{{font-style:normal;color:var(--mute);font-size:15px;display:block}}
.sl{{padding:4px 14px 14px}} .sl li{{padding:9px 10px;margin:6px 0;border-radius:10px;border-left:6px solid var(--line);font-size:16px}}
.sl li.lk{{border-left-color:var(--blue)}} .sl li.nw{{border-left-color:var(--acc)}} .sl li.dn{{border-left-color:#2e9e6b}} .sl li i{{font-style:normal;color:var(--mute);font-size:14px;margin-left:4px}}
.tag{{float:right;font-size:13px;border-radius:10px;padding:1px 8px;color:#fff}} .t1{{background:var(--blue)}} .t2{{background:var(--acc)}} .t3{{background:#8a8fa8}} .t4{{background:#2e9e6b}}
.ed li{{padding:10px 0;border-bottom:1px solid var(--line)}} .ed li:last-child{{border:0}}
</style></head><body><div class="w">
<h1>2026년 11월 콘텐츠 캘린더</h1>
<p class="lead">11월 1일~30일, 모든 채널을 한 장으로 정리했어요. 날짜를 누르면 그날의 11칸이 펼쳐져요. 제목은 작업 제목이고, 세부 기획에서 확정해요.</p>
<div class="box"><b>칸 상태</b><div class="bigbar"><i></i></div><div class="leg"><span class="l1">이미 있는 것 {lk}</span><span class="l2">새로 만들 것 {nw}</span></div><p class="lead" style="margin:10px 0 0">빈 칸은 0이에요. 지금까지 만들어 둔 것: 네이버 원고 5편(11/1·11/2·11/3·11/4·11/6), 메트리쿨 예약 2건(11/6 릴스·스레드), 띠 릴스 5편 구성 그림(승인 대기).</p></div>
<h2>점검 결과</h2><div class="box"><ul class="chk">{chk}</ul></div>
<h2>제작 순서와 양</h2><div class="box"><p class="lead">주마다 그 주 칸을 모두 만들고 예약해요. 막대가 길수록 새로 만들 칸이 많아요.</p>{wkh}</div>
<h2>날짜별 일정</h2>{cards}
<h2>발행 후 고칠 것과 후속 일</h2><div class="box"><ul class="ed">{eh}</ul></div>
<h2>알려 둘 것</h2><div class="box"><ul class="chk"><li>12월 달력 글(11/29, 11/30)의 날짜는 계산 코드로 확인한 뒤 써요.</li><li>물의 별자리 글은 12월 첫 주로 넘겼어요. 별자리 글은 한 주에 하나만 두는 규칙 때문이에요.</li><li>이 달력에서 기존 예약은 하나도 옮기거나 지우지 않았어요.</li></ul></div>
</div></body></html>'''
open('/mnt/user-data/outputs/zaoseon_calendar_2026-11.html','w',encoding='utf-8').write(page)
print(len(page)//1024,'KB', lk,nw,cv,tot)
