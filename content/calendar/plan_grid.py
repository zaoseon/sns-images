import json, sys, os, collections, datetime as D
sys.path.insert(0,'/home/claude/repo/naver'); os.chdir('/home/claude/repo/naver')
import thumb_sq as TQ
from PIL import Image
cal=json.load(open('/home/claude/cal/calendar_2026-11.json',encoding='utf-8'))['days']
pg=json.load(open('pages.json',encoding='utf-8')); pub=json.load(open('published.json'))
FACES=TQ.FACES
# ── 블로그: 시간순 목록(기존 + 새 칸). 기존 글은 표지 색으로 오행 팔레트를 짐작
def classify(path):
    im=Image.open(path).convert('RGB'); w,h=im.size
    px=[im.getpixel((x,y)) for x in (3,w//2,w-4) for y in (3,h-4)]
    avg=tuple(sum(p[i] for p in px)//len(px) for i in range(3)); lum=sum(avg)/3
    best=min(TQ.EL, key=lambda k: sum((avg[i]-TQ.EL[k][0][i])**2 for i in range(3)))
    return best, lum<110
blog=[]
for k,v in pub.items():
    if '2026-10-25'<=v['date']<='2026-11-30':
        c=pg.get(k,{}).get('cover'); el=dark=None
        if c and os.path.exists('img/'+c): el,dark=classify('img/'+c)
        blog.append(dict(date=v['date'],time=v.get('time',''),id=k,title=v['title'],locked=True,el=el,dark=dark,face=None))
blog=[b for b in blog if b['date']>='2026-10-25']
KNOWN_FACE={'n70':'v4_glasses','n71':'v2_straight'}
for b in blog:
    if b['id'] in KNOWN_FACE: b['face']=KNOWN_FACE[b['id']]
blog_ids={b['id'] for b in blog}
for d in cal:
    for s in ('B12','B21'):
        sl=d['slots'][s]
        if sl['status']=='NEW':
            blog.append(dict(date=d['date'],time=sl['time'],id=f"new-{d['date'][5:]}-{s}",title=sl['theme'],locked=False,el=None,dark=None,face=None))
blog.sort(key=lambda b:(b['date'],b['time']))
# 새 글 표지 배정: 오행 팔레트는 앞뒤 이웃과 달라야 하고, 어두운 판은 5개에 1개 이하이며 어두운 판끼리 이웃하지 않는다. 얼굴은 최근 3개와 달라야 한다
ELS=['불','물','흙','나무','쇠']
fi=0
for i,b in enumerate(blog):
    if b['locked']: continue
    near=set(x['el'] for x in blog[max(0,i-3):i]+blog[i+1:i+4] if x['el'])
    cand=[e for e in ELS if e not in near] or [e for e in ELS if e not in set(x['el'] for x in blog[max(0,i-2):i]+blog[i+1:i+3] if x['el'])]
    # 가장 오래 안 쓴 팔레트
    last={e:max([j for j in range(i) if blog[j]['el']==e],default=-99) for e in cand}
    b['el']=min(cand,key=lambda e:last[e])
    win=blog[max(0,i-4):i]+blog[i+1:i+5]
    anydark=any(x['dark'] for x in win)
    since=[j for j in range(i) if blog[j]['dark']]; gap=i-(since[-1] if since else -99)
    b['dark']= (not anydark) and gap>=5
    used=set(x['face'] for x in blog[max(0,i-3):i]+blog[i+1:i+4] if x['face'])
    for _ in range(len(FACES)):
        f=FACES[fi%len(FACES)]; fi+=1
        if f not in used: b['face']=f; break
# ── 인스타 캐러셀(프로필 그리드, 3열): 시간순
SETS=[('코랄','버건디','#3a1a1a','#ff6663'),('블루','네이비','#1a2650','#6c8cff'),('민트','딥그린','#14382e','#4fe0b0'),('금','딥퍼플','#2e1a47','#e8c15a')]
KINDS=['큰 숫자','도형·차트','한자 워터마크','질문 글자']
ig=[]
for d in cal:
    for s in ('P08','P21'):
        sl=d['slots'][s]
        if sl['status']=='COVERED': continue
        ig.append(dict(date=d['date'],slot=s,time=(sl.get('time') or (sl['items'][0]['t'] if sl.get('items') else '')),locked=sl['status']=='LOCKED',
                       title=(sl.get('theme') or (sl['items'][0]['title'] if sl.get('items') else ''))[:40],set=None,face=None,kind=None))
ig.sort(key=lambda x:(x['date'],x['time']))
for x in ig:
    if x['locked']: x['face']='?'   # 기존 예약 표지는 만든 사람 확인 필요, 얼굴이 있다고 보고 이웃을 비움
fi2=0; ki=0
for i,x in enumerate(ig):
    if x['locked']: continue
    near=ig[max(0,i-3):i]+ig[i+1:i+4]
    can_face=not any(y['face'] for y in near)
    # 얼굴은 최소 4칸마다 한 번(25%대)
    sincef=[j for j in range(i) if ig[j]['face']]; gap=i-(sincef[-1] if sincef else -99)
    if can_face and gap>=4:
        x['face']=FACES[fi2%len(FACES)]; fi2+=1; x['kind']='정월 얼굴'
    else:
        prev=set(y['kind'] for y in ig[max(0,i-2):i] if y['kind'])
        for _ in range(len(KINDS)):
            k=KINDS[ki%len(KINDS)]; ki+=1
            if k not in prev: x['kind']=k; break
    # 세트 색: 앞뒤 3칸과 달라야 한다
    usedset=set(y['set'] for y in ig[max(0,i-3):i]+ig[i+1:i+4] if y['set'] is not None)
    x['set']=next(j for j in [ (i+n)%4 for n in range(4)] if j not in usedset) if len(usedset)<4 else i%4
# ── 릴스(릴스 탭): 새 칸만
SC=['큰 숫자 세기','점 격자','막대','겹치는 두 원','좌우 비교 패널','여섯 방향 칸','체크 목록','게이지','키네틱 글자','카드 뒤집기','오행 그림','12궁·60괘 판','노선도']
EN=['팔로우 카드','댓글 질문 크게','정월+알약','한 줄 정리+팔로우','숫자 반복+팔로우']
reels=[]
for d in cal:
    for s in ('R08','R12','R20'):
        sl=d['slots'].get(s)
        if not sl: continue
        reels.append(dict(date=d['date'],slot=s,time=(sl.get('time') or (sl['items'][0]['t'] if sl.get('items') else '')),locked=sl['status']=='LOCKED',title=(sl.get('theme') or sl['items'][0]['title'])[:40],scene=None,ending=None,face=None))
reels.sort(key=lambda x:(x['date'],x['time']))
si=0; ei=0; fi3=0
for i,r in enumerate(reels):
    if r['locked']: continue
    psc=set(y['scene'] for y in reels[max(0,i-3):i] if y['scene']); pen=set(y['ending'] for y in reels[max(0,i-2):i] if y['ending'])
    for _ in range(len(SC)):
        c=SC[si%len(SC)]; si+=1
        if c not in psc: r['scene']=c; break
    for _ in range(len(EN)):
        c=EN[ei%len(EN)]; ei+=1
        if c not in pen: r['ending']=c; break
    near=reels[max(0,i-2):i]+reels[i+1:i+3]
    if i%3==0 and not any(y['face'] for y in reels[max(0,i-2):i]):
        r['face']=FACES[fi3%len(FACES)]; fi3+=1
# ── 검증
rep={}
nb=[b for b in blog]
rep['blog_neighbor_same_el']=[(nb[i]['id'],nb[i+1]['id'],nb[i]['el']) for i in range(len(nb)-1) if nb[i]['el'] and nb[i]['el']==nb[i+1]['el']]
rep['blog_new_dark']=sum(1 for b in blog if not b['locked'] and b['dark']); rep['blog_new']=sum(1 for b in blog if not b['locked'])
dk=[i for i,b in enumerate(blog) if b['dark']]; rep['blog_dark_adjacent']=[(blog[a]['id'],blog[b]['id']) for a,b in zip(dk,dk[1:]) if b-a==1]
rep['ig_new']=sum(1 for x in ig if not x['locked']); rep['ig_face_new']=sum(1 for x in ig if not x['locked'] and x['face'] and x['face']!='?')
bad=[]
for i in range(len(ig)):
    for j in range(i+1,min(len(ig),i+4)):
        a,b=ig[i],ig[j]
        if a['set'] is not None and a['set']==b['set']: bad.append(('같은 색',a['date'],a['slot'],b['date'],b['slot']))
        if a['face'] and b['face'] and j-i<=3: bad.append(('얼굴 이웃',a['date'],a['slot'],b['date'],b['slot']))
rep['ig_violations']=bad
rep['ig_face_share']=round(sum(1 for x in ig if x['face'])/len(ig)*100)
rep['reel_new']=sum(1 for r in reels if not r['locked']); rep['reel_face']=sum(1 for r in reels if r['face'])
json.dump(dict(blog=blog,ig=ig,reels=reels,report=rep,SETS=SETS),open('/home/claude/grid/grid_2026-11.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print(json.dumps(rep,ensure_ascii=False,indent=1))
