"""예약 릴스 끝 장면을 R11(댓글 질문 -> 팔로우하고 더 많은 이야기 나눠요 -> 프로필 링크에서 생년월일 입력)으로 바꿔 붙인다 (10/12 대표 "예약 릴스 전수 확인·수정").
옛 영상의 마지막 장면(\"프로필 링크에서 전체 풀이 보기\" 또는 \"다음 편\" 배지 장면)을 잘라 내고, 같은 문구 순서의 새 끝 장면(4.2초)을 이어 붙인다.
소리는 원본 음악을 그대로 쓰고(끝 장면 아래에는 음악 처음 부분을 이어 붙여 0.8초 크로스페이드), 원본이 무음이면 `--music`으로 경쾌한 음악을 새로 입힌다.
사용: python3 pipeline/r11_tail.py <원본.mp4> <결과.mp4> "<질문 첫 줄>\\n<질문 둘째 줄>" [--cut 초] [--music 스타일] [--fx zoom|wipe|slide]
  --cut 을 생략하면 마지막 장면 전환 시각을 장면 검출로 찾는다. 질문은 한 줄 10자 안팎, 두 줄까지(끝 장면 안전 영역).
결과는 R11 문구가 정확히 들어가고 길이가 4.2초 늘어난다. 같은 질문의 끝 장면은 /tmp/r11_tails 에 캐시한다."""
import os, sys, re, subprocess, tempfile, shutil, hashlib
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(ROOT, "content"))
TAIL_SEC = 4.2; XFADE = 0.8; CACHE = "/tmp/r11_tails"
def dur(p): return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]).decode().strip())
def has_audio(p): return bool(subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "stream=index", "-of", "csv=p=0", p]).decode().strip())
def last_cut(src, lo_from_end=7.0, hi_from_end=1.2, thr=0.12):
    """마지막 장면이 시작하는 시각(초)을 장면 검출로 찾는다."""
    D = dur(src); out = subprocess.run(["ffmpeg", "-v", "info", "-i", src, "-vf", f"select='gt(scene,{thr})',showinfo", "-an", "-f", "null", "-"], capture_output=True, text=True).stderr
    ts = [float(m) for m in re.findall(r"pts_time:([0-9.]+)", out)]; ts = [t for t in ts if D - lo_from_end <= t <= D - hi_from_end]
    if not ts: raise SystemExit(f"{src}: 마지막 장면 전환을 못 찾음 (--cut 으로 직접 지정)")
    return ts[-1]
def tail_video(q, fx="zoom", labels=None):
    os.makedirs(CACHE, exist_ok=True); key = hashlib.md5((q + fx + str(labels)).encode()).hexdigest()[:10]; dst = os.path.join(CACHE, key + ".mp4")
    if os.path.exists(dst): return dst
    from data_reels_v2 import render, end_recap, end_choice       # 새 끝 장면(마무리 ④ 한 줄 정리+팔로우)을 그대로 쓴다: 질문 -> 팔로우 -> 프로필 링크 -> 팔로우 알약
    tmp = tempfile.mkdtemp(); p, _ = render("tail", [(TAIL_SEC, end_choice(q, *labels) if labels else end_recap(q, fx))], tmp); shutil.move(p, dst); shutil.rmtree(tmp); return dst
def attach(src, dst, q, cut=None, music=None, fx="zoom", seed=7, labels=None):
    D = dur(src); cut = cut if cut is not None else last_cut(src); tail = tail_video(q, fx, labels); total = cut + TAIL_SEC
    os.makedirs(os.path.dirname(os.path.abspath(dst)), exist_ok=True)
    vf = (f"[0:v]trim=0:{cut:.3f},setpts=PTS-STARTPTS,fps=30,format=yuv420p[v0];[1:v]fps=30,format=yuv420p,setpts=PTS-STARTPTS[v1];[v0][v1]concat=n=2:v=1:a=0[v]")
    venc = ["-c:v", "libx264", "-profile:v", "high", "-crf", "15", "-preset", "medium", "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-movflags", "+faststart"]
    if has_audio(src) and not music and _loud(src):
        af = (f"[0:a]atrim=0:{cut:.3f},asetpts=PTS-STARTPTS[a0];[0:a]atrim=0:{TAIL_SEC + XFADE},asetpts=PTS-STARTPTS[a1];[a0][a1]acrossfade=d={XFADE}:c1=tri:c2=tri,afade=t=out:st={total - 0.7:.2f}:d=0.7[a]")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-i", tail, "-filter_complex", vf + ";" + af, "-map", "[v]", "-map", "[a]", *venc, "-c:a", "aac", "-b:a", "192k", dst], check=True)
    else:     # 원본이 무음: 경쾌한 음악을 새로 만들어 입힌다(소리 없는 릴스 금지, 운영 규칙 5)
        import reel_music as RM
        style = music or "상큼 팝"; bpm = RM.pick_bpm(style, seed); beats = max(8, int((total - 0.3) * bpm / 60.0)); wav = tempfile.mktemp(suffix=".wav")
        RM.compose_up(style, beats, seed, wav, key="G", bpm=bpm, cuts=[])
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-i", tail, "-i", wav, "-filter_complex", vf + f";[2:a]apad=whole_dur={total:.3f},atrim=0:{total:.3f},afade=t=out:st={total - 0.7:.2f}:d=0.7[a]", "-map", "[v]", "-map", "[a]", *venc, "-c:a", "aac", "-b:a", "192k", dst], check=True); os.remove(wav)
    print(os.path.basename(dst), f"원본 {D:.1f}s -> 자름 {cut:.2f}s + 끝 {TAIL_SEC}s = {dur(dst):.1f}s", flush=True)
def _loud(p):
    out = subprocess.run(["ffmpeg", "-i", p, "-af", "volumedetect", "-vn", "-f", "null", "-"], capture_output=True, text=True).stderr; m = re.search(r"mean_volume: (-?[0-9.]+) dB", out)
    return bool(m) and float(m.group(1)) > -40
if __name__ == "__main__":
    a = sys.argv[1:]; opt = {}
    for k in ("--cut", "--music", "--fx"):
        if k in a: i = a.index(k); opt[k] = a[i + 1]; del a[i:i + 2]
    attach(a[0], a[1], a[2].replace("\\n", "\n"), cut=float(opt["--cut"]) if "--cut" in opt else None, music=opt.get("--music"), fx=opt.get("--fx", "zoom"))
