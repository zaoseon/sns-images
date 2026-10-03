"""SOP 클립(clips_sop/*.mp4)에 직접 작곡한 경쾌한 음악을 입힌다(10/3: 네이버 클립은 PC에서 올리면 음악을 못 넣으므로 영상에 포함).
장면이 바뀌는 박에 작은 박수, 끝은 0.5초 페이드아웃. 영상은 다시 인코딩하지 않는다.
사용: python3 pipeline/clip_music.py            -> clips_sop/ 의 7편 전부 -> clips_sop/<id>_<길이>s.mp4 를 음악 포함본으로 덮어씀(원본은 *_nomusic.mp4)
스타일은 4종을 돌려 쓴다(상큼 팝·발랄 우쿨렐레·경쾌 신스팝·통통 마림바)."""
import os, sys, shutil, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, ".."); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(ROOT, "content"))
import reel_music as RM
import clips_motion as CM
PLAN = {("n28-c1", "12"): ("상큼 팝", 31, "D"), ("n28-c1", "30"): ("발랄 우쿨렐레", 32, "F"), ("n28-c2", "12"): ("경쾌 신스팝", 33, "C"), ("n28-c3", "12"): ("통통 마림바", 34, "G"),
        ("n33-c1", "12"): ("발랄 우쿨렐레", 35, "A"), ("n33-c2", "12"): ("상큼 팝", 36, "E"), ("n33-c3", "12"): ("경쾌 신스팝", 37, "D")}
def add_music(cid, ver):
    style, seed, key = PLAN[(cid, ver)]; scenes = CM.SC[(cid, ver)]; durs = [d for d, _ in scenes]; total = sum(durs)
    bpm = RM.pick_bpm(style, seed); spb = 60.0 / bpm; acc = 0; cuts = []
    for d in durs: cuts.append(round(acc / spb)); acc += d
    wav = f"/tmp/clipmusic_{cid}_{ver}.wav"; beats = max(8, (total - 0.3) / spb)
    m = RM.compose_up(style, beats, seed, wav, key=key, bpm=bpm, cuts=cuts, tail=0.3)
    mp4 = os.path.join(ROOT, "clips_sop", f"{cid}_{ver}s.mp4"); src = mp4.replace(".mp4", "_nomusic.mp4")
    if not os.path.exists(src): shutil.copy(mp4, src)
    tmp = mp4 + ".tmp.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-i", wav, "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "128k", "-shortest", "-movflags", "+faststart", tmp], check=True)
    os.replace(tmp, mp4); return f"{cid}_{ver}s {style} {bpm}BPM {total:.1f}s"
if __name__ == "__main__":
    for (cid, ver) in PLAN: print(add_music(cid, ver))
