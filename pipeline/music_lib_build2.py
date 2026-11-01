"""음악 라이브러리 2판 (대표 11/1 17:42 "다들 비슷비슷하던데, 기본적으로 경쾌하고 활기찬 느낌이면 좋겠어").

1판이 비슷하게 들린 까닭(코드로 확인): 32곡이 같은 뼈대 — 같은 패드·같은 진행 6개·같은 4박 드럼·같은 마무리, 앞 2마디 비움.
2판은 곡마다 따로 짠다:
- 장르 8개 × 3곡 = 24곡. 곡마다 리드·화음·베이스·양념 악기가 모두 다르고(같은 리드 두 번 없음), 진행·훅 리듬·드럼 무늬도 다르다.
- 전부 빠르다(110~150). 첫 박에 심벌 + 드럼 전체가 바로 들어온다(릴스 첫 1초). 8마디마다 짧게 멈췄다 필인 → 다시 터짐.
- 패드는 기본으로 깔지 않는다(뭉개져서 비슷하게 들림). 소리를 밝게(고음 올림)·넓게.
- 대표가 1판에서 뺀 장르(시네마틱 빌드업·가을 인디)는 넣지 않는다. 멜로디는 남의 곡을 따라 하지 않는다.
음색 GeneralUser GS(상업 사용 가능) — 받는 법은 music_lib_build.py 머리말.
결과: assets/music_lib/v2_<id>.mp3 + content/music_lib.json 에 더함(1판 곡은 status "old" 로 내려 쓰지 않음).
사용: python3 pipeline/music_lib_build2.py [장르 ...]"""
import os, sys, json, random, subprocess, tempfile
import mido
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, ".."))
SF = os.environ.get("ZS_SF2", "/home/claude/mrbumpy409/generaluser-gs/GeneralUser-GS.sf2")
OUT = os.path.join(ROOT, "assets", "music_lib"); LIST = os.path.join(ROOT, "content", "music_lib.json")
NOTE = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
MAJ = [0, 2, 4, 5, 7, 9, 11]; MIN = [0, 2, 3, 5, 7, 8, 10]
PROGS = [[0, 4, 5, 3], [5, 3, 0, 4], [3, 4, 2, 5], [0, 5, 3, 4], [1, 4, 0, 0], [3, 0, 4, 5], [0, 3, 4, 3], [5, 4, 3, 4]]
# 악기: (리드, 화음, 베이스, 양념) GM 번호. 장르 안 세 곡이 서로 다르고, 리드는 24곡 모두 다르다.
G = {
 "funk":   dict(name="디스코 펑크",     bpm=(118, 124), drums="disco",  minor=0.3,
              ins=[(62, 7, 36, 48), (56, 4, 38, 61), (17, 7, 36, 49)]),
 "kpop":   dict(name="케이팝 신스",     bpm=(124, 128), drums="kpop",   minor=0.5,
              ins=[(81, 90, 38, 85), (80, 5, 39, 98), (84, 88, 38, 55)]),
 "spedup": dict(name="스피드업 팝",     bpm=(142, 150), drums="spedup", minor=0.2,
              ins=[(1, 81, 39, 9), (10, 5, 38, 13), (98, 4, 39, 11)]),
 "dembow": dict(name="뎀보우",          bpm=(104, 110), drums="dembow", minor=0.6,
              ins=[(114, 45, 38, 12), (75, 25, 39, 108), (69, 45, 38, 114)]),
 "tropic": dict(name="트로피컬 하우스", bpm=(112, 118), drums="tropic", minor=0.2,
              ins=[(108, 12, 33, 75), (72, 24, 34, 78), (46, 12, 33, 85)]),
 "jersey": dict(name="저지 클럽",       bpm=(138, 142), drums="jersey", minor=0.5,
              ins=[(85, 99, 38, 55), (82, 81, 39, 55), (83, 90, 38, 55)]),
 "funpop": dict(name="펑키 팝",         bpm=(108, 114), drums="funk",   minor=0.0,
              ins=[(78, 7, 36, 61), (22, 17, 33, 61), (26, 4, 36, 57)]),
 "candy":  dict(name="캔디 팝",         bpm=(130, 136), drums="candy",  minor=0.0,
              ins=[(9, 0, 34, 13), (13, 6, 33, 10), (12, 1, 34, 14)]),
}
KEYS = ["C", "D", "E", "F", "G", "A", "Bb", "Eb"]
# 드럼 한 마디(박, 소리, 세기). 36 킥 38 스네어 39 박수 42 닫힌햇 44 페달햇 46 열린햇 54 탬버린 69 카바사 70 셰이커 37 림 56 카우벨 75 클라베
def drum_bar(kind, bar):
    d = []; h16 = lambda v1, v2: [(i * 0.25, 42, v1 if i % 2 == 0 else v2) for i in range(16)]
    if kind == "disco":
        d += [(b, 36, 112) for b in range(4)] + [(1, 39, 96), (3, 39, 96), (1, 38, 70), (3, 38, 70)] + [(b + 0.5, 46, 72) for b in range(4)] + h16(44, 30)
    elif kind == "kpop":
        d += [(0, 36, 118), (1.5, 36, 100), (2, 36, 112), (3.25, 36, 90)] + [(1, 38, 104), (3, 38, 104), (1, 39, 92), (3, 39, 92)] + h16(62, 38)
        if bar % 4 == 3: d += [(3 + i * 0.25, 38, 70 + i * 10) for i in range(4)]
    elif kind == "spedup":
        d += [(0, 36, 118), (1.5, 36, 104), (2.5, 36, 108)] + [(1, 38, 108), (3, 38, 108), (1, 39, 84), (3, 39, 84)] + h16(66, 44) + [(3.5, 46, 70)]
    elif kind == "dembow":
        d += [(b, 36, 116) for b in range(4)] + [(0.75, 38, 98), (1.5, 38, 102), (2.75, 38, 98), (3.5, 38, 102)] + [(i * 0.5, 42, 50) for i in range(8)] + [(i * 0.5 + 0.25, 69, 40) for i in range(8)]
    elif kind == "tropic":
        d += [(b, 36, 100) for b in range(4)] + [(1, 39, 88), (3, 39, 88)] + [(b + 0.5, 37, 64) for b in range(4)] + [(i * 0.25, 70, 46 if i % 2 else 58) for i in range(16)]
    elif kind == "jersey":
        d += [(0, 36, 120), (0.75, 36, 106), (1.5, 36, 112), (2.5, 36, 112), (3, 36, 104), (3.5, 36, 108)] + [(1, 39, 104), (3, 39, 104)] + [(i * 0.5, 42, 56) for i in range(8)]
        if bar % 2: d += [(2.75, 56, 70)]
    elif kind == "funk":
        d += [(0, 36, 112), (0.75, 36, 92), (2.25, 36, 100), (2.5, 36, 96)] + [(1, 38, 106), (3, 38, 106), (1.75, 38, 40), (3.75, 38, 44)] + h16(60, 34) + [(3.5, 46, 64)]
    else:  # candy
        d += [(0, 36, 110), (2, 36, 110), (2.5, 36, 86)] + [(1, 39, 104), (3, 39, 104), (3.5, 39, 80)] + [(i * 0.5, 54, 70 if i % 2 == 0 else 52) for i in range(8)]
    return d

def bass_bar(kind, r, fifth=7):
    if kind in ("disco", "kpop"): return [(i * 0.5, r + (12 if i % 2 else 0), 92) for i in range(8)]
    if kind == "dembow": return [(0, r, 100), (0.75, r, 90), (2, r, 100), (2.75, r + fifth, 90)]
    if kind == "jersey": return [(0, r, 104), (0.75, r, 92), (1.5, r + 12, 96), (2.5, r, 100), (3.5, r + fifth, 92)]
    if kind == "funk": return [(0, r, 100), (0.75, r + 12, 80), (1.5, r, 90), (2.25, r + fifth, 88), (2.75, r + 10, 80), (3.5, r + 12, 86)]
    if kind == "tropic": return [(0, r, 92), (1.5, r, 84), (2, r + fifth, 88), (3, r + 12, 80)]
    if kind == "candy": return [(i, r + [0, 12, fifth, 12][i], 90) for i in range(4)]
    return [(0, r, 98), (0.75, r, 84), (1.5, r + fifth, 90), (2.5, r, 96), (3.25, r + 12, 86)]   # spedup

def chord_bar(kind, up):
    if kind == "disco": return [(s, x, 0.22, 72) for s in (0.5, 1.5, 2.5, 3.5) for x in up]
    if kind == "kpop": return [(s, x, 0.18, 70) for s in (0, 0.75, 1.5, 2.25, 3, 3.5) for x in up]
    if kind == "spedup": return [(i * 0.5, x, 0.2, 66 if i % 2 else 76) for i in range(8) for x in up]
    if kind == "dembow": return [(s, x + 12, 0.16, 74) for s in (0, 0.75, 1.5, 2, 2.75, 3.5) for x in up[:2]]
    if kind == "tropic": return [(s, x, 0.2, 76) for s in (0.5, 1.5, 2.5, 3.5) for x in up]
    if kind == "jersey": return [(s, x, 0.15, 74) for s in (0, 0.75, 1.5, 3) for x in up]
    if kind == "funk": return [(s, x, 0.14, 68 + (10 if s % 1 == 0 else 0)) for s in (0, 0.5, 0.75, 1.5, 2, 2.75, 3.25, 3.5) for x in up]
    return [(s, x, 0.25, 70) for s in (0, 1, 1.5, 2, 3, 3.5) for x in up]   # candy

def hook(rnd):
    """2마디 훅(16분음 단위로 촘촘하게). 같은 훅을 되풀이 + 대답 마디."""
    pool = [[0, 0.5, 0.75, 1.5, 2, 2.5, 3, 3.5], [0, 0.25, 0.75, 1, 1.5, 2.25, 2.75, 3.5], [0, 0.75, 1.5, 2, 2.5, 2.75, 3.5], [0.5, 1, 1.25, 1.75, 2.5, 3, 3.25, 3.75],
            [0, 0.5, 1, 1.75, 2.5, 3, 3.75], [0, 0.25, 0.5, 1.5, 2, 2.25, 2.5, 3.5]]
    rh = rnd.choice(pool); contour = rnd.choice([[0, 2, 4, 2, 5, 4, 2, 0], [4, 4, 2, 4, 5, 7, 5, 4], [0, 0, 2, 4, 4, 2, 1, 0], [7, 5, 4, 5, 4, 2, 4, 2], [2, 4, 5, 4, 2, 0, 2, 4]])
    st = [contour[i % len(contour)] for i in range(len(rh))]
    ans = [s + (2 if i == len(st) - 1 else rnd.choice([0, 0, -1, 1])) for i, s in enumerate(st)]
    return rh, st, ans

def build(gid, n, used_prog):
    cfg = G[gid]; rnd = random.Random(f"v2-{gid}-{n}")
    bpm = rnd.randint(*cfg["bpm"]); key = KEYS[(n * 3 + len(gid) * 5) % len(KEYS)]
    minor = rnd.random() < cfg["minor"]; scale = MIN if minor else MAJ
    pi = (len(used_prog) * 3 + n) % len(PROGS); prog = PROGS[pi]; used_prog.append(pi)
    lead, chord, bass, spice = cfg["ins"][n]
    k = key[0]; root = 12 * 4 + NOTE[k] + (-1 if key.endswith("b") else 0)    # 화음 기준 4옥타브
    bars = max(12, int(round(32 * bpm / 240.0)))
    tpb = 480; mid = mido.MidiFile(ticks_per_beat=tpb)
    tempo = mido.MidiTrack(); mid.tracks.append(tempo); tempo.append(mido.MetaMessage("set_tempo", tempo=mido.bpm2tempo(bpm), time=0))
    tracks = {}
    for ch, (part, prog_no, rev) in enumerate([("lead", lead, 34), ("chord", chord, 18), ("bass", bass, 0), ("spice", spice, 30)]):
        t = mido.MidiTrack(); mid.tracks.append(t); tracks[part] = (t, ch)
        t.append(mido.Message("program_change", program=prog_no, channel=ch, time=0))
        t.append(mido.Message("control_change", control=91, value=rev, channel=ch, time=0))
        t.append(mido.Message("control_change", control=10, value=[64, 44, 64, 86][ch], channel=ch, time=0))   # 좌우로 벌림
    dt = mido.MidiTrack(); mid.tracks.append(dt); tracks["drum"] = (dt, 9)
    dt.append(mido.Message("control_change", control=91, value=12, channel=9, time=0))
    ev = {p: [] for p in tracks}
    def add(p, beat, dur, note, vel):
        ch = tracks[p][1]; ev[p].append((int(beat * tpb), 1, max(0, min(127, note)), max(1, min(127, int(vel))), ch)); ev[p].append((int((beat + dur) * tpb), 0, max(0, min(127, note)), 0, ch))
    rh, st, ans = hook(rnd)
    def sc(step, base):  # 음계 위 step 번째 음
        return base + scale[step % 7] + 12 * (step // 7)
    for bar in range(bars):
        b0 = bar * 4; deg = prog[bar % 4]
        tri = [root + scale[(deg + i) % 7] + 12 * ((deg + i) // 7) for i in (0, 2, 4)]
        r = root + scale[deg % 7] - 24
        brk = bar % 8 == 7                       # 8마디째: 마지막 박에서 멈췄다가 필인
        for s, x, d, v in chord_bar(cfg["drums"], tri):
            if not (brk and s >= 3): add("chord", b0 + s, d, x, v)
        for s, x, v in bass_bar(cfg["drums"], r):
            if not (brk and s >= 3): add("bass", b0 + s, 0.3, x, v)
        seq = st if (bar // 2) % 2 == 0 else ans
        if bar % 2 == 0 or bar % 4 == 1:
            for s, step in zip(rh, seq):
                if brk and s >= 3: continue
                add("lead", b0 + s, 0.28, sc(deg + step, root + 12), 92)
        # 양념: 마디마다 다른 자리에서 짧게(곡 성격을 만든다)
        if bar % 2 == 1 and not brk: add("spice", b0 + 2.5, 0.4, tri[2] + 24, 84)
        if bar % 4 == 0: add("spice", b0, 0.6, tri[0] + 12, 90)
        for s, note, v in drum_bar(cfg["drums"], bar):
            if brk and s >= 3: continue
            add("drum", b0 + s, 0.12, note, v)
        if brk:
            for i in range(4): add("drum", b0 + 3 + i * 0.25, 0.1, 38, 80 + i * 12)   # 스네어 필
        if bar == 0 or bar % 8 == 0: add("drum", b0, 1.2, 49, 110)                     # 첫 박·구간 시작 심벌
    for p, (t, ch) in tracks.items():
        last = 0
        for tick, on, note, vel, c in sorted(ev[p], key=lambda e: (e[0], e[1])):
            t.append(mido.Message("note_on" if on else "note_off", note=note, velocity=vel, channel=c, time=tick - last)); last = tick
    tmp = tempfile.mktemp(suffix=".mid"); mid.save(tmp); raw = tmp + ".wav"
    subprocess.run(["fluidsynth", "-ni", "-g", "0.6", "-R", "1", "-C", "0", "-r", "44100", "-F", raw, SF, tmp], check=True, capture_output=True)
    dur = bars * 4 * 60.0 / bpm; tid = f"v2_{gid}{n + 1}"; out = os.path.join(OUT, tid + ".mp3")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", raw, "-t", f"{dur:.3f}",
                    "-af", "highpass=f=35,equalizer=f=9000:t=h:w=1:g=3,equalizer=f=250:t=q:w=1:g=-2,extrastereo=m=1.4,"
                           f"acompressor=threshold=-16dB:ratio=3.5:attack=5:release=90:makeup=2,afade=t=out:st={dur - 1.0:.2f}:d=1.0,loudnorm=I=-13:TP=-1:LRA=6",
                    "-ar", "44100", "-ac", "2", "-b:a", "128k", out], check=True)
    os.remove(tmp); os.remove(raw)
    return dict(id=tid, genre=gid, name=f"{cfg['name']} {n + 1}", bpm=bpm, key=key + ("m" if minor else ""), dur=round(dur, 1),
                file=f"assets/music_lib/{tid}.mp3", hook_at=0.0, ins=[lead, chord, bass, spice], prog=pi, status="ok", ver=2)

if __name__ == "__main__":
    if not os.path.exists(SF): sys.exit("사운드폰트 없음: " + SF)
    os.makedirs(OUT, exist_ok=True)
    want = sys.argv[1:] or list(G)
    leads = [v[0] for g in G.values() for v in g["ins"]]; assert len(leads) == len(set(leads)), "리드 악기가 겹친다"
    lib = json.load(open(LIST)); keep = {t["id"]: t for t in lib["tracks"]}
    for t in keep.values():
        if t.get("ver", 1) == 1 and t.get("status") == "ok" and t["genre"] != "holiday": t["status"] = "old"   # 1판은 내려 둔다(대표 17:42 '비슷비슷')
    used = []
    for gid in want:
        for n in range(3):
            e = build(gid, n, used); old = keep.get(e["id"])
            if old and old.get("status") == "out": e["status"] = "out"
            keep[e["id"]] = e; print(e["id"], e["name"], e["bpm"], e["key"], e["dur"], e["ins"])
    lib["tracks"] = sorted(keep.values(), key=lambda t: (-t.get("ver", 1), t["id"]))
    lib["note"] = "릴스·클립 음악 라이브러리. 2판(ver 2, 11/1 17:42 대표 '비슷비슷·경쾌하게')만 쓴다. 1판은 old/out. status out = 대표가 뺀 곡. 고르기 pipeline/music_lib.py"
    json.dump(lib, open(LIST, "w"), ensure_ascii=False, indent=1)
