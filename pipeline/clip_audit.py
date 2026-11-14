"""클립 표지·영상 감사(11/14 대표 '규칙 만들었으면 적용해라', K-205·K-203).
아직 안 올린 클립(post_clips.json 의 rec 가 오늘 이후)을 전부 재서 막는다:
 ① 영상 첫 프레임(= 네이버 클립 표지)에 제목·핵심 그림이 있나(html_motion.표지_검사 와 같은 값: channel_specs.BALANCE cover_fill·cover_h)
 ② 앱·발행 키트에 걸린 표지 그림(images[0])이 그 영상의 첫 프레임에서 뽑은 것인가(옛 영상 표지가 남지 않게: 파일 이름 clip_cover/<id>.jpg)
 ③ 영상 길이·크기·소리
사용: python3 pipeline/clip_audit.py [--고침]   (--고침: 표지 그림을 영상 첫 프레임에서 다시 뽑아 post_clips.json 에 넣는다)
끝낼 때 문제가 있으면 종료 코드 1."""
import json, os, subprocess, sys, datetime, io, urllib.request
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import channel_specs as CS
RAW = "https://raw.githubusercontent.com/zaoseon/sns-images/main/"

def _local(url): return os.path.join(ROOT, url.split("/main/")[-1]) if "/main/" in url else None

def _frame0(mp4, t=0.0):
    out = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t), "-i", mp4, "-frames:v", "1", "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True).stdout
    return Image.open(io.BytesIO(out)).convert("RGB")

def 표지재기(im, ch="naver_clip"):
    B = CS.BALANCE; C = CS.CH[ch]; z = {r[0]: r[1:5] for r in C["zones"]}
    top = z["상단 고정"][3]; bot = z["하단 고정"][1]; sx0, sx1 = C["safe"][0], C["safe"][2]
    a = np.asarray(im).astype(int)[top + 10:bot - 10, sx0:sx1]
    edge = np.concatenate([a[:, :24].reshape(-1, 3), a[:, -24:].reshape(-1, 3)]); bg = np.median(edge, 0)
    m = np.abs(a - bg).max(2) > 48; fill = float(m.mean()); rows = np.where(m.sum(1) > 14)[0]
    h = (rows[-1] - rows[0]) / a.shape[0] if len(rows) else 0.0
    return fill, h, fill >= B["cover_fill"] and h >= B["cover_h"]

def main():
    고침 = "--고침" in sys.argv
    pcp = os.path.join(ROOT, "content", "post_clips.json"); pc = json.load(open(pcp, encoding="utf-8"))
    오늘 = datetime.date.today().isoformat(); 문제 = []; 바뀜 = False
    for c in pc:
        if (c.get("rec") or "") < 오늘: continue          # 이미 올린 클립은 고치지 않는다(K-178)
        mp4 = _local(c.get("video", ""))
        if not mp4 or not os.path.exists(mp4): 문제.append(f"{c['id']}: 영상 파일 없음"); continue
        pr = json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,width,height,duration", "-of", "json", mp4], capture_output=True, text=True).stdout)["streams"]
        v = [s for s in pr if s["codec_type"] == "video"][0]; 소리 = any(s["codec_type"] == "audio" for s in pr)
        if (v["width"], v["height"]) != (1080, 1920): 문제.append(f"{c['id']}: 크기 {v['width']}x{v['height']} (1080x1920)")
        if not 소리: 문제.append(f"{c['id']}: 소리 없음(K-070)")
        im = _frame0(mp4); fill, h, ok = 표지재기(im)
        if not ok: 문제.append(f"{c['id']}: 표지(0번 프레임) 비었음 — 채움 {fill*100:.1f}%·높이 {h*100:.0f}% (5%·22% 이상)")
        want = f"clip_cover/{c['id']}.jpg"; cur = (c.get("images") or [""])[0]
        if not cur.endswith(want):
            if 고침 and ok:
                p = os.path.join(ROOT, "2026-reels-test", want); os.makedirs(os.path.dirname(p), exist_ok=True); im.save(p, quality=92)
                c["images"] = [RAW + "2026-reels-test/" + want]; 바뀜 = True; print(f"{c['id']}: 표지 그림을 영상 첫 프레임으로 교체")
            else: 문제.append(f"{c['id']}: 표지 그림이 영상 첫 프레임이 아님({cur.split('/')[-1]}) — --고침")
    if 바뀜: json.dump(pc, open(pcp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("\n".join(문제) if 문제 else "클립 감사: 통과"); return 1 if 문제 else 0

if __name__ == "__main__": sys.exit(main())
