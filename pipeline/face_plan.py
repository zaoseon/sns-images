"""정월 사진 돌려 쓰기(10/5 대표 지적: 캐릭터가 다 똑같다 — 소품 든 사진과 계절 사진을 안 썼다).
분위기별로 후보를 두고, 최근 3편과 같은 사진은 쓰지 않는다. 계절 사진은 날짜가 맞을 때만 쓴다. 기록: content/face_log.json
사진: v1 정장 · v2 니트 · v3 포니테일 · v4 안경 · v5 버건디 · v6 겨울 목도리 · v7 한복 · v8 손짓 · v9 할로윈 · v10 빼빼로 · v11 머그컵 · v12 크리스마스 선물 · v13 뿔테 · intro 새 캐릭터"""
import os, json
LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "content", "face_log.json")
CAT = {"ask": ["v8_gesture", "v2_straight", "v3_ponytail", "v1_lowbun"], "comfort": ["v11_mug", "v5_halfup", "v5_halfup_v2", "v2_straight"],
       "data": ["v13_horn_glasses", "v4_glasses", "intro", "v1_lowbun"], "tradition": ["v7_hanbok"], "love": ["v5_halfup", "v3_ponytail", "v5_halfup_v2", "intro"]}
SEASON = [("10-24", "11-01", "v9_halloween"), ("11-03", "11-10", "v6_winter"), ("11-08", "11-12", "v10_pepero"), ("12-15", "12-26", "v12_christmas")]
def _load():
    try: return json.load(open(LOG, encoding="utf-8"))
    except Exception: return []
def pick(kind, name, md=None, write=True):
    """md='MM-DD'이면 그 날짜에 맞는 계절 사진이 있으면 먼저 쓴다."""
    log = _load()
    for x in log:
        if x["name"] == name: return x
    recent = [x["face"] for x in log[-3:]]
    if md:
        for a, b, f in SEASON:
            if a <= md <= b and f not in recent: face = f; break
        else: face = None
    else: face = None
    if not face:
        c = [f for f in CAT[kind] if f not in recent] or CAT[kind]; face = c[len(log) % len(c)]
    flip = (len(log) % 2 == 1)
    info = dict(name=name, kind=kind, face=face, flip=flip)
    if write: log.append(info); json.dump(log, open(LOG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return info
