"""네이버 클립 v3(단색 판, clips_v3s/)에 음악을 입힌다 — 10/16 대표 요청 mvaez5dl "네이버 클립에 음악이 안붙어 있음".
clips_v3.py가 소리 없이 렌더했다(clip_music.py는 옛 clips_sop만 다룸). 네이버 클립은 PC·폰 업로드에서 음악을 따로 못 붙이므로 영상에 넣는다(10/3 기준).
원본은 건드리지 않고 새 폴더 clips_v3m/<같은 id>.mp4 로 만든다(같은 이름 덮어쓰기 금지). 영상은 다시 인코딩하지 않는다(-c:v copy).
스타일 4종을 날짜 순으로 돌려 쓰고(상큼 팝·발랄 우쿨렐레·경쾌 신스팝·통통 마림바), 조성도 돌린다. 끝 0.5초 페이드아웃.
사용: python3 pipeline/clip_v3_music.py [id ...]   (없으면 clips_v3s/*.mp4 전부)
필요: fluidsynth + /usr/share/sounds/sf2/FluidR3_GM.sf2 (apt fluid-soundfont-gm), pip mido"""
import os, sys, glob, json, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "..")); sys.path.insert(0, HERE)
import reel_music as RM
SRC = os.path.join(ROOT, "clips_v3s"); OUT = os.path.join(ROOT, "clips_v3m")
STYLES = ["상큼 팝", "발랄 우쿨렐레", "경쾌 신스팝", "통통 마림바"]; KEYS = ["D", "F", "C", "G", "A", "E"]

def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p], capture_output=True, text=True, check=True).stdout.strip())

def add(cid, i):
    src = os.path.join(SRC, cid + ".mp4"); dst = os.path.join(OUT, cid + ".mp4")
    style = STYLES[i % 4]; key = KEYS[i % len(KEYS)]; seed = 1600 + i; total = dur(src)
    bpm = RM.pick_bpm(style, seed); beats = max(8, (total - 0.3) / (60.0 / bpm))
    wav = f"/tmp/clipv3m_{cid}.wav"; RM.compose_up(style, beats, seed, wav, key=key, bpm=bpm, tail=0.3)
    fo = max(0.0, total - 0.5)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-i", wav, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                    "-af", f"afade=t=out:st={fo:.2f}:d=0.5", "-c:a", "aac", "-b:a", "128k", "-t", f"{total:.3f}", "-movflags", "+faststart", dst], check=True)
    return dict(name=cid, kind="clip-v3", style=style, mode="up", bpm=bpm, key=key, seed=seed)

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    ids = sys.argv[1:] or sorted(os.path.basename(p)[:-4] for p in glob.glob(os.path.join(SRC, "v3-*.mp4")))
    allids = sorted(os.path.basename(p)[:-4] for p in glob.glob(os.path.join(SRC, "v3-*.mp4")))
    logp = os.path.join(ROOT, "content", "music_log.json"); log = json.load(open(logp))
    for cid in ids:
        e = add(cid, allids.index(cid)); print(cid, e["style"], e["bpm"], e["key"])
        log = [x for x in log if x.get("name") != cid] + [e]
    json.dump(log, open(logp, "w"), ensure_ascii=False, indent=1)
