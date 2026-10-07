import json, re, sys, datetime as D, collections
sys.path.insert(0,'/home/claude/repo/content'); sys.path.insert(0,'.')
from plan_data import DAYS
live=json.load(open('/home/claude/zaoseon-site/data/sns_live.json',encoding='utf-8'))['items']
pub=json.load(open('/home/claude/repo/naver/published.json'))
pages=json.load(open('/home/claude/repo/naver/pages.json'))
swaps=json.load(open('/home/claude/repo/content/reel_swaps.json',encoding='utf-8'))
try:
    import clips_sop as CS; CLIPS=[(c['date'],c['id'],c['post']) for c in CS.CLIPS if c.get('date')]
except Exception as e: CLIPS=[]; print('clips_sop load fail',e)
START=D.date(2026,11,1); N=30
SLOTS=["B12","B21","P08","P21","R12","R20","T08","T13","T20","T21","C"]
TIME={"B12":"12:00","B21":"21:00","P08":"08:00","P21":"21:00","R12":"12:00","R20":"20:00","T08":"08:30","T13":"13:00","T20":"20:30","T21":"21:00","C":"저녁(앱에서 직접)"}
NAME={"B12":"네이버 글 낮","B21":"네이버 글 밤","P08":"인스타 캐러셀 아침","P21":"인스타 캐러셀 밤","R12":"인스타 릴스 낮","R20":"인스타 릴스 저녁","T08":"스레드 아침","T13":"스레드 낮","T20":"스레드 저녁","T21":"스레드 밤","C":"네이버 클립"}
def slot_of(i):
    h=int(i['t'][11:13]); m=int(i['t'][14:16]); n=i['n'][0]; k=i['k']
    if n=='instagram':
        if k in('REEL','TRIAL_REEL'): return 'R08' if h<10 else ('R12' if h<16 else 'R20')
        return 'P08' if h<15 else 'P21'
    if h<10: return 'T08'
    if h<15: return 'T13'
    return 'T20' if h<21 else 'T21'
cal={}
for d in range(N):
    dt=START+D.timedelta(days=d); cal[dt.isoformat()]={s:[] for s in SLOTS+["R08"]}
for i in live:
    if i['st']=='PUBLISHED': continue
    ds=i['t'][:10]
    if ds in cal: cal[ds][slot_of(i)].append(dict(src='sns',locked=True,t=i['t'][11:16],title=i['x'].replace('\n',' ')[:60],kind=i['k']))
for k,v in pub.items():
    if v['date'] in cal:
        s='B12' if v.get('time','21')[:2]<'16' else 'B21'
        cal[v['date']][s].append(dict(src='blog',locked=True,t=v.get('time',''),title=v['title'][:70],id=k))
for dd,cid,post in CLIPS:
    if dd in cal: cal[dd]['C'].append(dict(src='clip',locked=True,t='',title=f'{cid} ({post} 연결 클립)',id=cid))
for s in swaps:
    if s.get('date') in cal and s.get('status') in ('wait','new') and s['kind'].startswith(('모션','릴스 표지')):
        pass
# 날마다 주제와 새 칸 채우기
GROUP={"B12":"M","P08":"M","R12":"M","T08":"M","T13":"M","B21":"E","P21":"E","T21":"E","R20":"D","T20":"D"}
out=[]; new_total=0; locked_total=0; gaps=0
blog_new=[]
for d in range(N):
    dt=START+D.timedelta(days=d); ds=dt.isoformat(); M,E,Dd,flag=DAYS[d+1]
    th={"M":M.split('|'),"E":E.split('|'),"D":Dd.split('|')}
    # 블로그 연결: 일반 날은 B12<->M, B21<->E / 띠 날(z)은 B21<->M, B12<->E
    def theme_of(slot):
        g=GROUP.get(slot)
        if slot=='B12': g='E' if flag=='z' else 'M'
        if slot=='B21': g='M' if flag=='z' else 'E'
        return g
    day=dict(date=ds,wd='월화수목금토일'[dt.weekday()],flag=flag,themes={g:dict(title=v[0],series=v[1],sys=v[2]) for g,v in th.items()},slots={})
    for s in SLOTS:
        ex=cal[ds][s]
        if s=='P08' and cal[ds]['R08'] and not ex:
            day['slots']['R08']=dict(status='LOCKED',items=cal[ds]['R08'],time=cal[ds]['R08'][0]['t']); locked_total+=len(cal[ds]['R08'])
            day['slots']['P08']=dict(status='COVERED',note='아침 릴스가 이미 있어 아침 캐러셀은 건너뜀(인스타 하루 4개 이하)'); continue
        if s=='C':
            if ex: day['slots'][s]=dict(status='LOCKED',items=ex); locked_total+=len(ex)
            elif dt.weekday() not in (0,2,4,6):
                day['slots'][s]=dict(status='COVERED',note='클립은 주 4편(월·수·금·일)만 올려요. 대표가 폰 앱에서 직접 올리는 일이라 매일은 하지 않아요')
            else:
                # 전날 블로그 글(밤 우선)에서 파생: 발행 다음 날 올림
                prev=(dt-D.timedelta(days=1)).isoformat(); src=None
                if prev in cal:
                    for ss in ('B21','B12'):
                        if cal[prev][ss]: src=cal[prev][ss][0]['title']; srcid=cal[prev][ss][0].get('id'); break
                day['slots'][s]=dict(status='NEW',theme=f"전날 글을 클립으로: {src[:34] if src else '(전날 글 확정 후)'}",time=TIME[s],src=src)
                new_total+=1
            continue
        if ex:
            day['slots'][s]=dict(status='LOCKED',items=ex,time=ex[0]['t']); locked_total+=len(ex)
        else:
            g=theme_of(s); t=th[g]; tm=TIME[s]
            if s[0] in 'PRT':
                chn='IG' if s[0] in 'PR' else 'TH'
                used={it['t'] for ss in SLOTS if ss!='C' and ss[0] in ('PR' if chn=='IG' else 'T') for it in cal[ds][ss]}|day.setdefault('_new_'+chn,set())
                while tm in used:
                    h,mi=map(int,tm.split(':')); mi+=30; h+=mi//60; mi%=60; tm=f"{h:02d}:{mi:02d}"
                day['_new_'+chn].add(tm)
            day['slots'][s]=dict(status='NEW',theme=t[0],series=t[1],sys=t[2],time=tm,group=g); new_total+=1
            if s.startswith('B'): blog_new.append((ds,s,t[0],t[1],t[2]))
    day.pop('_new_IG',None); day.pop('_new_TH',None)
    out.append(day)
# 검증
def has(day,s): return bool(day['slots'][s].get('items') or day['slots'][s].get('theme') or day['slots'][s].get('status')=='COVERED')
for day in out:
    for s in SLOTS:
        if not has(day,s): gaps+=1
    ig=sum(1 for s in ('P08','P21','R08','R12','R20') if s in day['slots'] and day['slots'][s].get('status')!='COVERED' for _ in (day['slots'][s].get('items') or [1]))
    day['ig_count']=ig
rep={}
rep['gaps']=gaps; rep['new']=new_total; rep['locked']=locked_total
rep['ig_over4']=[d['date'] for d in out if d['ig_count']>4]
# 같은 갈래 연속 2일 초과(M/E 주제 기준)
viol=[]
for g in ('M','E'):
    run=1
    for a,b in zip(out,out[1:]):
        sa=a['themes'][g]['series']; sb=b['themes'][g]['series']
        if sa==sb and sa not in('INFO',): run+=1
        else: run=1
        if run>2: viol.append((b['date'],g,sb))
rep['series_run_gt2']=viol
cnt=collections.Counter(); pure=0; tot=0
for day in out:
    for g,t in day['themes'].items():
        tot+=1; cnt[t['series']]+=1
        if t['sys']=='S': pure+=1
rep['pure_S_pct']=round(pure/tot*100); rep['series']=dict(cnt)
# 주별 운명학 포함
syscov=collections.defaultdict(set)
for day in out:
    wk=(D.date.fromisoformat(day['date'])-START).days//7
    for t in day['themes'].values():
        for k in t['sys'].replace('X','S+A+N').split('+'): syscov[wk].add(k)
rep['missing_by_week']={w:sorted(set('SANZDHY')-v) for w,v in syscov.items() if set('SANZDHY')-v}
print('새 블로그 칸',len(blog_new),'(낮',sum(1 for b in blog_new if b[1]=='B12'),'밤',sum(1 for b in blog_new if b[1]=='B21'),')')

# ---- 보강 검증 ----
def sys_of_title(t):
    r=set()
    if re.search(r'육효|동전|괘',t) and '하락' not in t: r.add('Y')
    if '하락이수' in t: r.add('H')
    if re.search(r'자미두수|명궁|신궁',t): r.add('Z')
    if '당사주' in t: r.add('D')
    if re.search(r'숫자|생명수|수비',t): r.add('N')
    if '별자리' in t or '신월' in t or '수성' in t: r.add('A')
    if re.search(r'사주|일간|오행|띠|궁합|입동|손없',t): r.add('S')
    return r
daysys=[]
for day in out:
    ss=set()
    for t in day['themes'].values():
        for k in t['sys'].replace('X','S+A+N').split('+'): ss.add(k)
    for s_ in SLOTS:
        for it in day['slots'][s_].get('items',[]): ss|=sys_of_title(it['title'])
    daysys.append(ss)
bad=[]
for i in range(0,len(out)-13):
    w=set().union(*daysys[i:i+14]); miss=set('SANZDHY')-w
    if miss: bad.append((out[i]['date'],sorted(miss)))
# 마지막 14일(달 끝까지)도 확인
tail=set().union(*daysys[-14:]); rep['rolling14_missing']=bad; rep['tail14_missing']=sorted(set('SANZDHY')-tail)
# 같은 채널 같은 분 겹침
conf=[]
for day in out:
    ch=collections.defaultdict(list)
    for s_ in SLOTS:
        if s_=='C' or s_.startswith('B'): continue
        c='IG' if s_[0] in 'PR' else 'TH'
        sl=day['slots'][s_]
        for it in sl.get('items',[]): ch[c].append(it['t'])
        if sl['status']=='NEW': ch[c].append(sl['time'])
    for c,ts in ch.items():
        d_=[t for t,n in collections.Counter(ts).items() if n>1]
        if d_: conf.append((day['date'],c,d_))
rep['same_minute']=conf
# 연결 글(related) 배정: 새 블로그 글마다 24시간 이상 앞서 발행되는 글 중 운명학이 겹치는 글, 대상 사용 횟수 3 이하
posts=[]  # (date,slot,id,title,sys)
for k,v in pub.items(): posts.append((v['date'],'B12' if v.get('time','21')[:2]<'16' else 'B21',k,v['title'],sys_of_title(v['title'])))
for day in out:
    for s_ in ('B12','B21'):
        sl=day['slots'][s_]
        if sl['status']=='NEW':
            ss=set(sl['sys'].replace('X','S+A+N').split('+')); sl['sysset']=sorted(ss)
            posts.append((day['date'],s_,f"c{day['date'][5:].replace('-','')}{s_}",sl['theme'],ss))
use=collections.Counter()
def key(p): return (p[0],0 if p[1]=='B12' else 1)
posts.sort(key=key)
rel={}
for p in posts:
    if not p[2].startswith('c'): continue
    cands=[q for q in posts if (D.date.fromisoformat(q[0])+D.timedelta(days=0))<=D.date.fromisoformat(p[0])-D.timedelta(days=1) and q[2]!=p[2] and use[q[2]]<3]
    best=None;bs=-1
    for q in cands:
        sc=len(set(p[4])&set(q[4]))*3 + (1 if q[2] in pages and pages[q[2]].get('category')!='띠별 운세' else 0)
        if q[0]>=p[0][:8]+'01': sc+=1   # 같은 달 글 우대 안 함(낮게)
        sc-= (D.date.fromisoformat(p[0])-D.date.fromisoformat(q[0])).days*0.02
        if sc>bs: bs=sc;best=q
    if best:
        use[best[2]]+=1; rel[p[2]]=(best[2],best[3][:40],best[0])
rep['rel_assigned']=len(rel); rep['rel_over3']=[k for k,v in use.items() if v>3]
for day in out:
    for s_ in ('B12','B21'):
        sl=day['slots'][s_]
        if sl['status']=='NEW':
            pid=f"c{day['date'][5:].replace('-','')}{s_}"
            if pid in rel: sl['related']=dict(id=rel[pid][0],title=rel[pid][1],pub=rel[pid][2])
# 수정·후속 목록
edits=[
 dict(when='11/01 새벽',what='n11(10월 5일 글) 82번째 줄 \\"2027 신년 감정서는 10월 얼리버드를 진행 중이에요(10월 31일까지, 선착순 50명, STANDARD 14,900원부터).\\"를 \\"2027 신년 감정서는 zaoseon.com에서 신청할 수 있어요. 가격과 구성은 사이트에서 확인해 주세요.\\"로 고침(발행된 글이라 네이버 편집창에서 한 줄만 바꿈)',who='대표(네이버 편집)·①(문구 준비)',why='얼리버드가 10/31에 끝나고 사이트 가격이 19,000원부터로 바뀌어 글과 사이트가 달라짐. n12·n46의 \\"10월 31일\\"은 그날의 사실이라 그대로 둠'),
 dict(when='11/01 이후',what='SNS 새 글·영상 끝 안내는 \"프로필 링크에서 확인\"까지만 쓰고 가격·얼리버드 문구는 넣지 않음(감정서 소개 글 3편만 가격 표기)',who='①',why='얼리버드 종료 후 가격 표기는 사이트가 자동으로 바꾸므로 본문에 고정하지 않는 게 안전'),
 dict(when='새 블로그 글 발행 직후마다',what='이 글을 연결 글로 쓰는 다른 글의 제목 줄에 링크가 걸리도록 글 주소를 앱에 저장',who='대표(앱 저장)·①(확인)',why='연결 대상은 발행된 글만 링크로 걸림'),
 dict(when='글 발행 다음 날',what='글 연결 클립을 올리고 블로그 스티커를 그 글로 연결',who='대표(폰 앱에서 업로드)',why='스티커는 발행된 글만 고를 수 있음'),
 dict(when='11/28~11/29',what='12월 운세 달력·12월 손없는날 글의 날짜는 대설·동지·신월·보름달·음력 변환을 계산 코드로 확인한 뒤 쓴다',who='①',why='확인 안 된 날짜를 쓰지 않는 규칙'),
 dict(when='11/14 12:00 겹침',what='쥐띠 인스타 릴스와 돼지띠 인스타 릴스가 같은 시각이라 돼지띠를 12:30으로 옮겨 예약(앱 불일치 알림 1번 해결)',who='①',why='같은 채널 같은 분 두 글 금지'),
 dict(when='11/06 11:59',what='수성 역행 2027 영상은 표지 시안과 함께 11/6 12:00 릴스로 예약(앱 불일치 알림 2번 해결)',who='①',why='새 영상 탭에서 대기 중인 승인 영상'),
]
rep['edits']=len(edits)
json.dump(dict(days=out,report=rep,edits=edits),open('calendar_2026-11.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print(json.dumps({k:rep[k] for k in ('rolling14_missing','tail14_missing','same_minute','rel_assigned','rel_over3','edits')},ensure_ascii=False))
