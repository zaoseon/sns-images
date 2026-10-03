"""10/3 밤 일정 개편용 다시 렌더: (1) CTA 간격 v5(배지-제목-안내문 사이 넓힘) (2) 다음 편 예고를 \"다음 편\" + 새 순서(기→경→신→임→계→갑→을)로.
산출: 2026-w42car-sched/MMDD_N.jpg(캐러셀 7장), 2026-w42reel-sched/ig/<키>.mp4. 사용: EDITOR_HTML=pipeline/assets/carousel_editor_2026-10-03_v5.html python3 pipeline/sched_render.py"""
import sys, os, inspect
sys.path.insert(0,'pipeline'); sys.path.insert(0,'content')
import carousel_sets as CS, carousel_editor as CE, reel_v2 as RV, reel_plan as RP
CHAIN = {"기":"경(庚)일생 편","경":"신(辛)일생 편","신":"임(壬)일생 편","임":"계(癸)일생 편","계":"갑(甲)일생 편","갑":"을(乙)일생 편","을":"세 지도 테스트"}
src=inspect.getsource(CE.render)
src=src.replace("n = pg.evaluate(LAYOUT_JS, [d, None]); pg.wait_for_timeout(150)","n = pg.evaluate(LAYOUT_JS, [d, None]); pg.evaluate(OVERRIDE_JS, S.get('_ov', {})); pg.wait_for_timeout(150)")
exec(src, CE.__dict__)
sets={}
for date in ("2026-10-04","2026-10-06","2026-10-07","2026-10-08","2026-10-09"):
    s=dict(CS.SETS[date]); nt=CHAIN[s["dayChar"]]; s["nextTitle"]=nt; s["_ov"]={"nextBadge":"다음 편","nextTitle":nt}; sets[date]=s
g=dict(CS.SPARE["갑"], variant={"cover":"C3","advice":"A1","cta":"T1"}, _ov={"nextBadge":"다음 편","nextTitle":CHAIN["갑"]}); g["nextTitle"]=CHAIN["갑"]
g["advice"]=["곧음은 무기,\n휘는 법도 알아요","센 바람엔 가지도 흔들려야\n부러지지 않아요.\n한 번쯤은 먼저 끄덕여 보세요."]
e=dict(CS.SPARE["을"], variant={"cover":"C1","advice":"A2","cta":"T2"}, _ov={"nextBadge":"다음 편","nextTitle":CHAIN["을"]}); e["nextTitle"]=CHAIN["을"]
e["advice"]=["유연함은 무기,\n내 마음도 챙겨요","맞추는 건 강점이지만 늘 내가 맞추면 지쳐요.\n하고 싶은 말 하나는 꼭 꺼내 보세요."]
sets["2026-10-16"]=g; sets["2026-10-20"]=e
CE.render(sets, os.path.join(CE.ROOT,"2026-w42car-sched"))
# ---- 릴스(인스타) ----
defs=RP.ig_defs(); keep={}
for k in ("2026-10-04","2026-10-06","2026-10-07","2026-10-08","2026-10-09","2026-10-05","2026-10-10","2026-10-11"):
    d,ov=defs[k]; d=dict(d); ov=dict(ov)
    if k in sets: d["nextTitle"]=sets[k]["nextTitle"]; ov["nextTitle"]=sets[k]["nextTitle"]
    ov["nextBadge"]="다음 편"; keep[k]=(d,ov)
RV.render(list(keep), keep, os.path.join(CE.ROOT,"2026-w42reel-sched","ig"))
print("SCHED_RENDER_DONE")
