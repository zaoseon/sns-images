"""릴스 배경음악 작곡(저작권 문제 없는 직접 작곡). MIDI를 만들고 FluidSynth(GM 사운드폰트 FluidR3)로 악기 소리를 입힌다.
스타일 4가지 x 조성·진행·박자 조합으로 릴스마다 다르게 만든다. 사용: from reel_music import compose  -> wav 경로"""
import os, random, subprocess, tempfile
import mido
SF = "/usr/share/sounds/sf2/FluidR3_GM.sf2"
NOTE = {"C":0,"D":2,"E":4,"F":5,"G":7,"A":9,"B":11}
def midi_of(name):          # 'C4' -> 60
    n = NOTE[name[0]]; acc = 0; i = 1
    if len(name) > 2 and name[1] in "#b": acc = 1 if name[1] == "#" else -1; i = 2
    return 12 * (int(name[i:]) + 1) + n + acc
MAJ = [0,2,4,5,7,9,11]; MIN = [0,2,3,5,7,8,10]
def triad(root, scale, deg, seventh=False):
    # 음계 위의 diatonic 화음: deg 0~6
    idx = [deg, deg+2, deg+4] + ([deg+6] if seventh else [])
    return [root + scale[i % 7] + 12*(i//7) for i in idx]
# 코드 진행(음계 번호 0=I ... 5=vi), 4마디 반복
PROG = {"pop": [0,5,3,4], "emo": [5,3,0,4], "ref": [0,4,5,3], "lofi": [1,4,0,5], "dream": [3,0,4,5], "calm": [0,3,5,4]}
STYLES = {
  # 이름: (설명, 템포 범위, 코드악기, 멜로디악기, 베이스악기, 패드악기, 드럼 세기)
  "피아노 로파이": dict(bpm=(84,92), chord=0,  lead=0,  bass=32, pad=89, drums=1, prog=["lofi","emo","ref"], seventh=True),
  "별빛 오르골":   dict(bpm=(88,98), chord=88, lead=10, bass=33, pad=88, drums=0, prog=["dream","pop","calm"], seventh=False),
  "따뜻한 기타":   dict(bpm=(92,100), chord=24, lead=25, bass=32, pad=48, drums=1, prog=["pop","calm","emo"], seventh=False),
  "맑은 팝":       dict(bpm=(100,110), chord=4,  lead=11, bass=33, pad=89, drums=2, prog=["pop","ref","emo"], seventh=False),
}
def compose(style, beats, seed, out_wav, key="C", tail=1.2):
    cfg = STYLES[style]; rnd = random.Random(seed)
    bpm = rnd.randint(*cfg["bpm"]); prog = PROG[rnd.choice(cfg["prog"])]
    minor = rnd.random() < 0.25 and style != "맑은 팝"
    scale = MIN if minor else MAJ; root = midi_of(key + "3")
    tpb = 480; mid = mido.MidiFile(ticks_per_beat=tpb)
    def tr(prog_no=None, ch=0):
        t = mido.MidiTrack(); mid.tracks.append(t)
        if prog_no is not None: t.append(mido.Message("program_change", program=prog_no, channel=ch, time=0))
        return t
    tempo = tr(); tempo.append(mido.MetaMessage("set_tempo", tempo=mido.bpm2tempo(bpm), time=0))
    T = {k: tr(v, i) for i, (k, v) in enumerate([("chord", cfg["chord"]), ("lead", cfg["lead"]), ("bass", cfg["bass"]), ("pad", cfg["pad"])])}
    drum = tr(None, 9)
    ev = {k: [] for k in list(T) + ["drum"]}   # (tick, kind, note, vel)
    def add(k, beat, dur, note, vel, ch):
        ev[k].append((int(beat*tpb), "on", note, vel, ch)); ev[k].append((int((beat+dur)*tpb), "off", note, 0, ch))
    total = beats + tail*bpm/60.0; bars = int(total/4) + 1
    for bar in range(bars):
        deg = prog[bar % 4]; b0 = bar*4
        ch3 = triad(root, scale, deg, cfg["seventh"]); ch_up = [n+12 for n in ch3]
        # 패드: 마디 전체 길게
        for n in ch3: add("pad", b0, 3.9, n+12, 46, 3)
        # 베이스: 근음을 1·3박(2박 반 변형)
        r = root + scale[deg % 7] - 12
        add("bass", b0, 1.5, r, 78, 2); add("bass", b0+2, 1.0, r + (7 if bar%2 else 0), 70, 2)
        # 코드 악기: 스타일별 패턴
        if style == "피아노 로파이":
            for n in ch_up[:3]: add("chord", b0, 1.8, n, 58, 0)
            for n in ch_up[:3]: add("chord", b0+2.5, 1.2, n, 52, 0)
            for i, n in enumerate((ch_up*2)[:8]): add("lead", b0+i*0.5, 0.45, n+12, 44 + (8 if i%4==0 else 0), 1)
        elif style == "별빛 오르골":
            seq = [ch_up[0], ch_up[1], ch_up[2], ch_up[1]]
            for i in range(8): add("lead", b0+i*0.5, 0.9, seq[i%4]+12, 50 if i%2==0 else 42, 1)
            for n in ch3: add("chord", b0, 3.8, n+12, 36, 0)
        elif style == "따뜻한 기타":
            order = [0,2,1,2,0,2,1,2]
            for i in range(8): add("chord", b0+i*0.5, 0.6, ch3[order[i]%3]+12, 56 if i%2==0 else 46, 0)
            for n in ch_up[:3]: add("lead", b0+2, 1.8, n, 40, 1)
        else:  # 맑은 팝
            for st in (0, 1.5, 2, 3.5): 
                for n in ch_up[:3]: add("chord", b0+st, 0.4, n, 62, 0)
            mel = [ch_up[2], ch_up[1], ch_up[2], ch_up[0]+12 if False else ch_up[2]+2]
            for i, n in enumerate(mel): add("lead", b0+i, 0.8, n+12, 66, 1)
        # 드럼
        if cfg["drums"] >= 1:
            for beat in range(4):
                if beat in (0, 2): add("drum", b0+beat, 0.2, 36, 80 if cfg["drums"] == 2 else 62, 9)      # kick
                if beat in (1, 3): add("drum", b0+beat, 0.2, 37, 52 if cfg["drums"] == 1 else 70, 9)      # rim
            for e in range(8): add("drum", b0+e*0.5, 0.1, 42, 34 if e%2 else 46, 9)                       # closed hat
        if cfg["drums"] == 0:
            for beat in (0, 2): add("drum", b0+beat, 0.2, 70, 28, 9)                                         # shaker
    for k, track in list(T.items()) + [("drum", drum)]:
        last = 0
        for tick, kind, note, vel, ch in sorted(ev[k], key=lambda e: (e[0], e[1] == "on")):
            track.append(mido.Message("note_on" if kind == "on" else "note_off", note=max(0, min(127, note)), velocity=vel, channel=ch, time=tick - last)); last = tick
    tmp = tempfile.mktemp(suffix=".mid"); mid.save(tmp)
    raw = out_wav + ".raw.wav"
    subprocess.run(["fluidsynth", "-ni", "-g", "0.9", "-R", "1", "-r", "44100", "-F", raw, SF, tmp], check=True, capture_output=True)
    dur = beats*60.0/bpm + tail
    # 길이에 맞춰 자르고 끝 페이드, 잔잔한 음량으로 정리
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", raw, "-t", f"{dur:.3f}", "-af", f"afade=t=out:st={dur-1.0:.3f}:d=1.0,loudnorm=I=-19:TP=-3:LRA=7", "-ar", "44100", "-ac", "2", out_wav], check=True)
    os.remove(raw); os.remove(tmp)
    return dict(path=out_wav, bpm=bpm, minor=minor, prog=prog, dur=dur)
