"""10/13 r11_tail.attach 음악 끊김 수리: acrossfade에 같은 입력을 두 번 넣어 결과 소리가 4.3초뿐이었다(영상 14~22초 중 4초 뒤 무음).
2026-r11/ 의 각 영상에서 소리가 영상보다 1초 넘게 짧으면, 원본(r11_batch.M 의 원본·src)의 음악으로 소리만 다시 만들어 영상은 그대로(-c:v copy) 붙인다.
사용: python3 pipeline/r11_audiofix.py [--check] [키워드…]   (--check: 고칠 것만 나열)"""
import os, sys, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); ROOT = os.path.abspath(os.path.join(HERE, ".."))
import r11_batch as B, r11_tail as R
def adur(p):
    o = subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "stream=duration", "-of", "csv=p=0", p]).decode().strip()
    return float(o) if o else 0.0
def src_of(k):
    src = os.path.join(ROOT, k)
    for pre, grp in (("2026-w40car6-reel/ig/", "w40"), ("2026-w42reel-sched/ig/", "sched"), ("2026-w42reel-sched/gapeul/ig/", "gapeul"), ("2026-w43swap/ig/", "swap")):
        if k.startswith(pre): src = os.path.join(ROOT, "2026-r11", "src", grp, k[len(pre):])
    return src
def fix(k, check=False):
    out = os.path.join(ROOT, "2026-r11", k.replace("/", "__"))
    if not os.path.exists(out): return None
    v = R.dur(out)
    if adur(out) >= v - 1.0: return None
    src = src_of(k)
    if check: return (k, round(v, 1), round(adur(out), 1))
    cut = v - R.TAIL_SEC; total = v
    af = (f"[0:a]atrim=0:{cut:.3f},asetpts=PTS-STARTPTS[a0];[1:a]atrim=0:{R.TAIL_SEC + R.XFADE},asetpts=PTS-STARTPTS[a1];[a0][a1]acrossfade=d={R.XFADE}:c1=tri:c2=tri,afade=t=out:st={total - 0.7:.2f}:d=0.7[a]")
    tmp = out + ".fix.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-i", src, "-i", out, "-filter_complex", af, "-map", "2:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-t", f"{total:.3f}", "-movflags", "+faststart", tmp], check=True)
    os.replace(tmp, out); return (k, round(R.dur(out), 1), round(adur(out), 1))
if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if not x.startswith("--")]; chk = "--check" in sys.argv
    for k in B.M:
        if a and not any(x in k for x in a): continue
        r = fix(k, chk)
        if r: print(r, flush=True)
