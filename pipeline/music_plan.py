"""릴스 음악 돌려 쓰기(10/5 대표 지적: 음악이 다 똑같다).
원인: 릴스 음악이 템포 114~128의 경쾌한 4종(상큼 팝·발랄 우쿨렐레·경쾌 신스팝·통통 마림바)뿐이었고, 카드 고르기와 모션그래픽은 '경쾌 신스팝'으로 고정이었다.
고침: 주제 분위기별로 느린 곡(피아노 로파이·별빛 오르골·따뜻한 기타·맑은 팝)과 템포를 낮춘 경쾌한 곡을 섞고, 최근 3편과 같은 곡·같은 조는 쓰지 않는다. 기록은 content/music_log.json.
사용: info = choose('love', 'pick-1031'); mux(mp4, total_sec, info, seed)"""
import os, sys, json, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import reel_music as RM
LOG = os.path.join(HERE, "..", "content", "music_log.json")
CAT = {   # 분위기별 후보: (곡, 방식, 템포)  방식 slow=compose, up=compose_up
    "love": [("피아노 로파이", "slow", None), ("따뜻한 기타", "slow", None), ("별빛 오르골", "slow", None), ("발랄 우쿨렐레", "up", 98)],
    "data": [("맑은 팝", "slow", None), ("경쾌 신스팝", "up", 108), ("별빛 오르골", "slow", None), ("통통 마림바", "up", 104)],
    "fun":  [("상큼 팝", "up", 124), ("통통 마림바", "up", 118), ("발랄 우쿨렐레", "up", 114), ("경쾌 신스팝", "up", 120)],
}
KEYS = ["C", "D", "E", "F", "G", "A"]
def _load():
    try: return json.load(open(LOG, encoding="utf-8"))
    except Exception: return []
def choose(kind, name, write=True):
    log = _load()
    for x in log:
        if x["name"] == name: return x          # 같은 이름은 처음 고른 곡을 그대로(다시 만들어도 곡이 바뀌지 않게)
    recent = [x["style"] for x in log[-3:]]; last_key = log[-1]["key"] if log else None; n = len(log)
    cands = [c for c in CAT[kind] if c[0] not in recent] or CAT[kind]
    style, mode, bpm = cands[n % len(cands)]
    key = [k for k in KEYS if k != last_key][n % (len(KEYS) - 1)]
    cfg = RM.STYLES.get(style) if mode == "slow" else RM.UP[style]
    info = dict(name=name, kind=kind, style=style, mode=mode, bpm=bpm or sum(cfg["bpm"]) // 2, key=key)
    if write: log.append(info); json.dump(log, open(LOG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return info
def mux(mp4, durs, info, seed):
    total = sum(durs); spb = 60.0 / info["bpm"]; acc = 0; cuts = []
    for d in durs: cuts.append(round(acc / spb)); acc += d
    wav = f"/tmp/mp_{info['name']}.wav"; beats = max(8, (total - .3) * info["bpm"] / 60.0)
    if info["mode"] == "slow": RM.compose(info["style"], beats, seed, wav, key=info["key"], tail=.3)
    else: RM.compose_up(info["style"], beats, seed, wav, key=info["key"], bpm=info["bpm"], cuts=cuts, tail=.3)
    tmp = mp4 + ".m.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", mp4, "-i", wav, "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "128k", "-shortest", "-movflags", "+faststart", tmp], check=True)
    os.replace(tmp, mp4); return info
