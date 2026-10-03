import sys, os
sys.path.insert(0,'pipeline'); sys.path.insert(0,'content')
import carousel_sets as CS, carousel_editor as CE, reel_v2 as RV, reel_plan as RP
g=dict(CS.SPARE['갑'], variant={'cover':'C3','advice':'A1','cta':'T1'})
g['advice']=['곧음은 무기,\n휘는 법도 알아요','센 바람엔 가지도 흔들려야\n부러지지 않아요.\n한 번쯤은 먼저 끄덕여 보세요.']
e=dict(CS.SPARE['을'], variant={'cover':'C1','advice':'A2','cta':'T2'})
e['advice']=['유연함은 무기,\n내 마음도 챙겨요','맞추는 건 강점이지만 늘 내가 맞추면 지쳐요.\n하고 싶은 말 하나는 꼭 꺼내 보세요.']
NEXT={'gab':'을(乙)일생 편','eul':'세 지도 테스트'}
def mk(S,nxt):
    return dict(dayChar=S['dayChar'],hanja=S['hanja'],accent=S['accent'],face=S['face'],kicker=S['kicker'],coverTitle=S['coverTitle'],coverSub=S['coverSub'],
        personality=S['personality'],love=S['love'],money=S['money'],advice=S['advice'],chartNote=S['chartNote'],values=S['values'],highlight=S['highlight'],
        ctaQ=S['ctaQ'],nextTitle=nxt,variant=S['variant'])
SRC={'gab':g,'eul':e}
IG={'gab':dict(struct='S2',style='상큼 팝',seed=31,key='E'),'eul':dict(struct='S3',style='통통 마림바',seed=32,key='G')}
NV={'gab':dict(struct='S1',style='발랄 우쿨렐레',seed=33,key='D'),'eul':dict(struct='S2',style='경쾌 신스팝',seed=34,key='F')}
igd={}; nvd={}
for k,S in SRC.items():
    d=mk(S,NEXT[k]); igd[k]=(d, dict(nextBadge='다음 편',nextTitle=NEXT[k],_cfg=IG[k]))
    d2=mk(S,NEXT[k]); c=dict(NV[k]); c['silent']=False; c['safe']=RP.NAVER_SAFE
    ov=RP.NAVER_OV(NEXT[k])
    if d2['variant'].get('cta')=='T2': ov.pop('hint',None); d2['hintText']='블로그에서\n내 기운 확인'
    nvd[k]=(d2, dict(ov,_cfg=c))
root=os.path.join(CE.ROOT,'2026-w42reel-sched/gapeul')
RV.render(['gab','eul'],igd,os.path.join(root,'ig'))
RV.render(['gab','eul'],nvd,os.path.join(root,'naver'))
print('RENDER_DONE')
