"""게시물형 클립(블로그 이미지+캡션)을 인스타·스레드 릴스로 만든다 (10/5 대표 지적: 네이버용 클립이 CTA를 안 바꾼 채 인스타에 올라갔다).
reuse_clips.py는 게시물형을 네이버 클립 그대로 복사했다(끝 장면이 없거나 \"블로그 스티커 눌러 보기\"가 남음). 이 도구는 원본 클립 끝에
인스타용 CTA 장면(\"프로필 링크에서 전체 풀이 보기\" + zaoseon.com · 무료 풀이 1초, 2.2초)을 이어 붙이고, 음악은 처음 부분을 이어 붙여 CTA까지 흐르게 한다.
결과: reuse/<클립id>/reel.mp4 (네이버용 clips_sop/<id>_12s.mp4는 그대로). 다시 실행해도 같은 결과.
사용: python3 pipeline/ig_post_reels.py n22-c1 n26-c1 ...   (한 편 약 30초)"""
import os, sys, subprocess, tempfile, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "..")); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(ROOT, "content"))
import clip_motion as M
import reuse_clips as R
CTA_SEC = 2.2; XFADE = 0.8; OUT = os.path.join(ROOT, "reuse")
OWN = {"s10-p": ("clips_post/s10_nopage/s10_clip.mp4", 13.6)}   # 게시물 클립: (원본, 네이버 CTA 슬라이드가 시작하는 초). 그 앞까지만 쓰고 인스타용 CTA를 붙인다
def dur(p): return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]).decode().strip())
def make(cid):
    src, cut = (os.path.join(ROOT, OWN[cid][0]), OWN[cid][1]) if cid in OWN else (os.path.join(ROOT, "clips_sop", f"{cid}_12s.mp4"), None); D = cut or dur(src); total = D + CTA_SEC; tmp = tempfile.mkdtemp(); dst = os.path.join(OUT, cid, "reel.mp4"); os.makedirs(os.path.dirname(dst), exist_ok=True)
    orig = M.background; M.background = lambda fr, t, tot: orig(fr, t + D, total)     # 배경 움직임이 원래 영상 끝에서 이어지게
    try: M.render("tail", [(CTA_SEC, R.ig_cta())], tmp)
    finally: M.background = orig
    head, cat, aud = (os.path.join(tmp, n) for n in ("head.mp4", "cat.mp4", "a.m4a"))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-t", f"{D:.3f}", "-an", "-c:v", "libx264", "-profile:v", "high", "-crf", "14", "-preset", "medium", "-pix_fmt", "yuv420p", "-r", "30", head], check=True)
    lst = os.path.join(tmp, "l.txt"); open(lst, "w").write(f"file '{head}'\nfile '{os.path.join(tmp, 'tail.mp4')}'\n")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", cat], check=True)
    fc = f"[0:a]atrim=0:{D:.3f},asetpts=PTS-STARTPTS[a0];[1:a]atrim=0:{CTA_SEC + XFADE},asetpts=PTS-STARTPTS[b];[a0][b]acrossfade=d={XFADE}:c1=tri:c2=tri,afade=t=out:st={total - 0.7:.2f}:d=0.7[a]"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-i", src, "-filter_complex", fc, "-map", "[a]", "-c:a", "aac", "-b:a", "192k", aud], check=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", cat, "-i", aud, "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "copy", "-shortest", "-movflags", "+faststart", dst], check=True)
    shutil.rmtree(tmp); print(cid, "완료", round(dur(dst), 2), "초 (원본", round(D, 2), "+ CTA", CTA_SEC, ")", "[네이버 CTA 장면 제거]" if cut else "", flush=True)
if __name__ == "__main__":
    for c in (sys.argv[1:] or ["n22-c1", "n26-c1", "n27-c1", "n30-c1"]): make(c)
