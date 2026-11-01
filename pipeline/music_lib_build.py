"""릴스·클립 음악 라이브러리 만들기 (대표 11/1 17:19 "유행 음원과 비슷한 느낌으로 만들어 놓고 쓰자" → "진행해").

- 유행 음원의 '결'(장르·빠르기·리듬·악기)만 따른다. 멜로디·가사는 따라 하지 않는다(저작권).
  근거: Buffer 2026-10-14 · SocialPilot 2026-10-30 인스타 릴스 유행 음원 목록(디스코 팝, 스피드업 팝,
  밝은 힙합 연주곡을 글 아래 깔기, 가을 인디 어쿠스틱, 크리스마스 팝, 뎀보우, 기타 빌드업 시네마틱, 몽환 신스팝).
- 음색: GeneralUser GS 2.0.3 사운드폰트(상업 사용 가능, documentation/LICENSE.txt). FluidR3 보다 소리가 좋다.
  저장소에 넣지 않는다(32MB). 없으면 아래 SF 경로에 GitHub 에서 받는다:
  GIT_LFS_SKIP_SMUDGE=1 git clone --depth 1 https://github.com/mrbumpy409/generaluser-gs /home/claude/mrbumpy409/generaluser-gs
- 결과: assets/music_lib/<id>.mp3 (32초 안팎, -14 LUFS) + content/music_lib.json(목록·상태).
  상태 "out" 은 대표가 운영앱에서 뺀 곡. 고르는 것은 pipeline/music_lib.py.
사용: python3 pipeline/music_lib_build.py            (8장르 × 4곡 = 32곡)
      python3 pipeline/music_lib_build.py disco     (한 장르만 다시)"""
import os, sys, json, random, subprocess, tempfile
import mido
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, ".."))
SF = os.environ.get("ZS_SF2", "/home/claude/mrbumpy409/generaluser-gs/GeneralUser-GS.sf2")
OUT = os.path.join(ROOT, "assets", "music_lib"); LIST = os.path.join(ROOT, "content", "music_lib.json")
NOTE = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
MAJ = [0, 2, 4, 5, 7, 9, 11]; MIN = [0, 2, 3, 5, 7, 8, 10]
PROG = {"pop": [0, 4, 5, 3], "axis": [5, 3, 0, 4], "disco": [1, 4, 0, 5], "uplift": [3, 4, 2, 5], "hold": [0, 3, 0, 4], "minor": [0, 5, 3, 4]}
# 장르: 이름, 빠르기, 악기(GM 번호), 진행, 단조 비율, 스윙
G = {
 "disco":   dict(name="디스코 팝",        bpm=(118, 124), chord=48, stab=7,  lead=62, bass=38, pad=50, prog=["disco", "pop"], minor=0.3, swing=0.0),
 "spedup":  dict(name="스피드업 팝",      bpm=(142, 150), chord=5,  stab=45, lead=81, bass=39, pad=89, prog=["axis", "pop"], minor=0.2, swing=0.0),
 "sunny":   dict(name="밝은 힙합 연주곡", bpm=(88, 94),   chord=4,  stab=11, lead=73, bass=33, pad=89, prog=["hold", "pop"], minor=0.0, swing=0.58),
 "indie":   dict(name="가을 인디 어쿠스틱", bpm=(98, 104), chord=25, stab=9,  lead=24, bass=32, pad=48, prog=["pop", "uplift"], minor=0.0, swing=0.0),
 "holiday": dict(name="크리스마스 팝",    bpm=(132, 140), chord=0,  stab=8,  lead=14, bass=32, pad=48, prog=["pop", "hold"], minor=0.0, swing=0.62),
 "dembow":  dict(name="뎀보우",           bpm=(100, 108), chord=45, stab=12, lead=84, bass=38, pad=89, prog=["minor", "axis"], minor=0.7, swing=0.0),
 "cine":    dict(name="시네마틱 빌드업",  bpm=(96, 104),  chord=48, stab=61, lead=29, bass=33, pad=49, prog=["axis", "uplift"], minor=0.5, swing=0.0),
 "dream":   dict(name="몽환 신스팝",      bpm=(110, 116), chord=89, stab=99, lead=80, bass=38, pad=91, prog=["uplift", "axis"], minor=0.25, swing=0.0),
}
KEYS = ["C", "D", "E", "F", "G", "A", "Bb"]

def midi_of(k, octv):
    n = NOTE[k[0]] + (-1 if k.endswith("b") else 0); return 12 * (octv + 1) + n
def chord_of(root, scale, deg, seventh=False):
    idx = [deg, deg + 2, deg + 4] + ([deg + 6] if seventh else [])
    return [root + scale[i % 7] + 12 * (i // 7) for i in idx]

def hook(rnd, scale):
    """2마디(8박) 훅: 화음음 위주 + 지나가는 음. 같은 훅을 되풀이해 귀에 남게(콜·리스폰스)."""
    rhythm = rnd.choice([[0, 0.5, 1, 1.5, 2.5, 3], [0, 0.75, 1.5, 2, 3], [0, 1, 1.5, 2, 2.5, 3.5], [0.5, 1, 1.5, 2.5, 3, 3.5]])
    steps = [rnd.choice([0, 2, 4, 4, 2, 1, 3, 5]) for _ in rhythm]
    answer = [s + rnd.choice([-1, 0, 1]) for s in steps]
    return rhythm, steps, answer

def build(gid, n):
    cfg = G[gid]; rnd = random.Random(f"{gid}-{n}-1101")
    bpm = rnd.randint(*cfg["bpm"]); key = KEYS[(n * 3 + len(gid)) % len(KEYS)]
    minor = rnd.random() < cfg["minor"]; scale = MIN if minor else MAJ
    prog = PROG[cfg["prog"][n % len(cfg["prog"])]]; root = midi_of(key, 3)
    bars = max(8, int(round(32 * bpm / 240.0)))     # 약 32초
    tpb = 480; mid = mido.MidiFile(ticks_per_beat=tpb); tracks = {}
    tempo = mido.MidiTrack(); mid.tracks.append(tempo); tempo.append(mido.MetaMessage("set_tempo", tempo=mido.bpm2tempo(bpm), time=0))
    for ch, part in enumerate(["chord", "stab", "lead", "bass", "pad"]):
        t = mido.MidiTrack(); mid.tracks.append(t); tracks[part] = (t, ch)
        t.append(mido.Message("program_change", program=cfg[part], channel=ch, time=0))
        t.append(mido.Message("control_change", control=91, value=40 if part in ("pad", "lead") else 22, channel=ch, time=0))  # 잔향
        t.append(mido.Message("control_change", control=93, value=20 if part == "pad" else 6, channel=ch, time=0))  # 코러스
    dt = mido.MidiTrack(); mid.tracks.append(dt); tracks["drum"] = (dt, 9)
    ev = {k: [] for k in tracks}
    sw = cfg["swing"]
    def at(b):  # 스윙: 8분 뒷박을 밀어 준다
        if sw and abs((b % 1) - 0.5) < 1e-6: return b - 0.5 + sw
        return b
    def add(part, beat, dur, note, vel):
        ch = tracks[part][1]; s = at(beat)
        ev[part].append((int(s * tpb), 1, note, max(1, min(127, int(vel))), ch)); ev[part].append((int((s + dur) * tpb), 0, note, 0, ch))
    rh, st, ans = hook(rnd, scale)
    def deg_note(base_deg, step, octv):
        i = base_deg + step; return root + 12 * octv + scale[i % 7] + 12 * (i // 7)
    for bar in range(bars):
        b0 = bar * 4; deg = prog[bar % 4]; ch3 = chord_of(root, scale, deg, gid in ("sunny", "dream", "disco"))
        up = [x + 12 for x in ch3]; r = root + scale[deg % 7] - 12
        intro = bar < 2; build_up = gid == "cine"; lift = 1.0 + (0.35 * bar / bars if build_up else 0)
        drop = (bar % 8) in (6, 7) and gid in ("spedup", "dream")      # 8마디마다 잠깐 비우고 다시 들어감
        for x in ch3[:3]: add("pad", b0, 3.95, x + 12, 34 * lift)
        # 화음 리듬
        if gid == "disco":
            for s in (0.5, 1.5, 2.5, 3.5):
                for x in up[:3]: add("chord", b0 + s, 0.3, x, 62)
            if bar % 2: add("stab", b0 + 3.5, 0.25, up[0] + 12, 70)
        elif gid == "spedup":
            for i in range(8):
                for x in up[:3]: add("chord", b0 + i * 0.5, 0.22, x, 58 if i % 2 else 66)
        elif gid == "sunny":
            for s, d in ((0, 1.4), (1.5, 0.4), (2.5, 1.2), (3.5, 0.4)):
                for x in up: add("chord", b0 + s, d, x, 54)
        elif gid == "indie":
            for s, v in ((0, 70), (1, 52), (1.5, 60), (2, 66), (3, 52), (3.5, 60)):
                for j, x in enumerate(up[:3] + [up[0] + 12]): add("chord", b0 + s + j * 0.02, 0.45, x, v)
        elif gid == "holiday":
            for s in (0, 1, 2, 3):
                for x in up[:3]: add("chord", b0 + s + 0.5, 0.3, x, 54)
            for i in range(4): add("stab", b0 + i, 0.4, up[(i % 3)] + 24, 58)
        elif gid == "dembow":
            for s in (0, 0.75, 1.5, 2, 2.75, 3.5):
                for x in up[:2]: add("chord", b0 + s, 0.2, x + 12, 60)
        elif gid == "cine":
            for i in range(16): add("chord", b0 + i * 0.25, 0.22, up[[0, 1, 2, 1][i % 4]], (48 + 3 * (i % 4 == 0) * 6) * lift)
            if bar % 4 == 3: add("stab", b0 + 3, 0.9, up[0], 92)
        else:  # dream
            for i in range(16): add("stab", b0 + i * 0.25, 0.2, (up + [up[0] + 12])[[0, 1, 2, 3, 2, 1, 2, 3][i % 8]] + 12, 46 + 10 * (i % 4 == 0))
            for x in up: add("chord", b0, 3.9, x, 40)
        # 훅(첫 두 마디는 비워 첫 1초를 깔끔하게, 이후 2마디 되풀이)
        if not intro and not drop:
            seq = st if (bar // 2) % 2 == 0 else ans
            for s, k in zip(rh, seq):
                add("lead", b0 + s + (4 if bar % 2 else 0) * 0, 0.42 if gid != "cine" else 0.9, deg_note(0, k, 2 if gid not in ("cine", "indie") else 1), 76 * lift)
        # 베이스
        if gid in ("disco",):
            for i in range(8): add("bass", b0 + i * 0.5, 0.35, r + (12 if i % 2 else 0), 86)
        elif gid == "dembow":
            for s in (0, 0.75, 2, 2.75): add("bass", b0 + s, 0.4, r, 92)
        elif gid == "sunny":
            for s, o in ((0, 0), (1.75, 0), (2.5, 7), (3.5, 5)): add("bass", b0 + s, 0.45, r + o, 84)
        elif gid == "holiday":
            for i in range(4): add("bass", b0 + i, 0.8, r + [0, 4, 7, 9][i] if not minor else r + [0, 3, 7, 8][i], 74)
        else:
            for s, o in ((0, 0), (1.5, 0), (2, 7), (3, 12 if gid == "spedup" else 0)): add("bass", b0 + s, 0.45, r + o, 82 * lift)
        # 드럼 (GS 표준 키트: 36 킥 38 스네어 39 박수 42 닫힌햇 46 열린햇 54 탬버린 83 방울 47·45 탐 49 심벌)
        if drop:
            add("drum", b0 + 3.5, 0.2, 39, 90); continue
        if intro and gid in ("cine", "dream", "indie"):
            add("drum", b0, 0.2, 49 if bar == 0 else 54, 50); continue
        if gid in ("disco", "dream"):
            for b in range(4): add("drum", b0 + b, 0.2, 36, 100)
            for b in (1, 3): add("drum", b0 + b, 0.2, 39 if gid == "disco" else 38, 82)
            for i in range(4): add("drum", b0 + i + 0.5, 0.2, 46, 58)
            for i in range(8): add("drum", b0 + i * 0.5, 0.06, 42, 40)
        elif gid == "spedup":
            for b in (0, 1.5, 2.5): add("drum", b0 + b, 0.2, 36, 104)
            for b in (1, 3): add("drum", b0 + b, 0.2, 38, 96); add("drum", b0 + b, 0.2, 39, 70)
            for i in range(16): add("drum", b0 + i * 0.25, 0.04, 42, 46 if i % 2 else 60)
        elif gid == "sunny":
            for b in (0, 1.75, 2.5): add("drum", b0 + b, 0.2, 36, 96)
            for b in (1, 3): add("drum", b0 + b, 0.2, 38, 90)
            for i in range(8): add("drum", b0 + i * 0.5, 0.06, 42, 52 if i % 2 == 0 else 36)
        elif gid == "indie":
            for b in (0, 2): add("drum", b0 + b, 0.2, 36, 78)
            for b in (1, 3): add("drum", b0 + b, 0.2, 37, 70)
            for i in range(8): add("drum", b0 + i * 0.5, 0.1, 54, 44)
        elif gid == "holiday":
            for b in (0, 2): add("drum", b0 + b, 0.2, 36, 80)
            for b in (1, 3): add("drum", b0 + b, 0.2, 38, 72)
            for i in range(8): add("drum", b0 + i * 0.5, 0.1, 83, 72 if i % 2 == 0 else 54)   # 방울
        elif gid == "dembow":
            for b in (0, 1, 2, 3): add("drum", b0 + b, 0.2, 36, 100)
            for b in (0.75, 1.5, 2.75, 3.5): add("drum", b0 + b, 0.15, 38, 90)
            for i in range(8): add("drum", b0 + i * 0.5, 0.05, 42, 44)
        else:  # cine
            add("drum", b0, 0.6, 36, 70 * lift)
            if bar % 2: add("drum", b0 + 2, 0.4, 47, 70 * lift)
            if bar % 4 == 3:
                for i in range(8): add("drum", b0 + 2 + i * 0.25, 0.2, 45 if i < 4 else 47, (60 + i * 6) * lift)
            if bar % 8 == 0 and bar: add("drum", b0, 1.5, 49, 90)
    for part, (t, ch) in tracks.items():
        last = 0
        for tick, on, note, vel, c in sorted(ev[part], key=lambda e: (e[0], e[1])):
            t.append(mido.Message("note_on" if on else "note_off", note=max(0, min(127, note)), velocity=vel, channel=c, time=tick - last)); last = tick
    tmp = tempfile.mktemp(suffix=".mid"); mid.save(tmp); raw = tmp + ".wav"
    subprocess.run(["fluidsynth", "-ni", "-g", "0.7", "-R", "1", "-C", "1", "-r", "44100", "-F", raw, SF, tmp], check=True, capture_output=True)
    dur = bars * 4 * 60.0 / bpm; tid = f"{gid}{n + 1}"; out = os.path.join(OUT, tid + ".mp3")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", raw, "-t", f"{dur:.3f}",
                    "-af", f"acompressor=threshold=-18dB:ratio=3:attack=10:release=120,afade=t=out:st={dur - 1.2:.2f}:d=1.2,loudnorm=I=-14:TP=-1.5:LRA=7",
                    "-ar", "44100", "-ac", "2", "-b:a", "128k", out], check=True)
    os.remove(tmp); os.remove(raw)
    return dict(id=tid, genre=gid, name=f"{cfg['name']} {n + 1}", bpm=bpm, key=key + ("m" if minor else ""), dur=round(dur, 1),
                file=f"assets/music_lib/{tid}.mp3", hook_at=round(2 * 4 * 60.0 / bpm, 2), status="ok")

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    if not os.path.exists(SF): sys.exit("사운드폰트 없음: " + SF + " (위 git clone 줄을 먼저 실행)")
    want = sys.argv[1:] or list(G)
    lib = json.load(open(LIST)) if os.path.exists(LIST) else {"note": "", "tracks": []}
    keep = {t["id"]: t for t in lib["tracks"]}
    for gid in want:
        for n in range(4):
            e = build(gid, n); old = keep.get(e["id"])
            if old and old.get("status") == "out": e["status"] = "out"    # 대표가 뺀 곡은 다시 만들어도 빠진 채로
            keep[e["id"]] = e; print(e["id"], e["name"], e["bpm"], e["key"], e["dur"])
    lib["note"] = "릴스·클립 음악 라이브러리(대표 11/1). status out = 대표가 운영앱에서 뺀 곡. 고르기는 pipeline/music_lib.py"
    lib["tracks"] = sorted(keep.values(), key=lambda t: (list(G).index(t["genre"]), t["id"]))
    json.dump(lib, open(LIST, "w"), ensure_ascii=False, indent=1)
