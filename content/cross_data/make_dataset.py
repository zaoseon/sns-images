import sys, json, random, time
sys.path.insert(0,'/home/claude/zaoseon-site/engine')
from datetime import datetime, timedelta
import consensus
from multiprocessing import Pool
def one(seed):
    rnd=random.Random(seed)
    y=rnd.randint(1950,2008); m=rnd.randint(1,12); d=rnd.randint(1,28)
    h=rnd.randint(0,23); mi=rnd.choice([0,10,20,30,40,50]); sex=rnd.choice(['F','M'])
    try:
        r=consensus.consensus(datetime(y,m,d,h,mi),37.57,126.98,skip=(),sex=sex)
        return dict(b=[y,m,d,h,mi],sex=sex,axis=r['최대합의축'],str=r['합의강도'],by=r['체계별_주축'],votes=r['축별_득표'],prof=r['종합프로파일'])
    except Exception as e:
        return None
if __name__=='__main__':
    t=time.time(); N=int(sys.argv[1])
    with Pool(4) as p: out=[x for x in p.map(one, range(N), chunksize=20) if x]
    json.dump(out,open('/tmp/dataset.json','w',encoding='utf-8'),ensure_ascii=False)
    print('done',len(out),round(time.time()-t,1),'s')
