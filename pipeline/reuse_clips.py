"""네이버 글로 만든 클립(글 연결 클립 23 + 게시물 클립)을 인스타 릴스·캐러셀로 다시 쓴다 (10/4 대표 요청).
 - 릴스: 클립 영상(1080x1920, 음악 포함)은 그대로 쓰고, 마지막 장면(\"블로그 스티커 눌러 보기\" 네이버 전용)만 인스타용 CTA(\"프로필 링크에서 전체 풀이 보기\")로 다시 그려 바꾼다. 소리는 원본 그대로.
 - 캐러셀: 영상 장면표(clip_motion SC)의 장면마다 한 장(1080x1350, 4:5)으로 그리고, 마지막 장은 인스타용 CTA. 게시물형은 블로그 이미지를 그대로 쓴다.
 - 캡션: 네이버 설명에서 \"블로그 스티커\" 문장을 빼고 인스타용 안내(프로필 링크)를 넣는다. 같은 어구가 두 번 붙은 오류도 바로잡는다.
결과: reuse/<클립id>/reel.mp4, 01.png.., caption.txt  +  content/reuse.json  (③이 앱 자료에 \"재활용\"으로 붙인다)
사용: python3 pipeline/reuse_clips.py [클립id ...]   (영상형 1편 약 1분)"""
import os, sys, re, json, subprocess, tempfile, shutil
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "..")); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(ROOT, "content"))
import clip_motion as M
import clips_motion, clips_motion_w41, clips_motion_w42   # 장면표를 한 사전(clips_motion.SC)에 모은다
import clips_sop as CS
SC = clips_motion.SC; RAW = "https://raw.githubusercontent.com/zaoseon/sns-images/main/"; OUT = os.path.join(ROOT, "reuse")
CTA_LINES = "프로필 링크에서\n*전체 풀이* 보기"; CTA_PILL = "zaoseon.com · 무료 풀이 1초"; CROP = (0, 165, 1080, 1515)

def dedup(t):
    for _ in range(3): t = re.sub(r"([가-힣A-Za-z0-9·]{3,}(?: [가-힣A-Za-z0-9·]{2,})?) \1", r"\1", t)
    return t
def ig_caption(desc, tags=None):
    body, _, tg = desc.partition("\n\n#"); body = dedup(body); body = re.sub(r"\s*블로그 스티커를 (?:누르면|눌러)[^.\n]*\.?", "", body).strip()
    tagline = " ".join("#" + t for t in tags) if tags else ("#" + tg if tg else "")
    cap = body + "\n\n내 태어난 날의 기운은 프로필 링크에서 1초면 볼 수 있어요. 마음에 남으면 저장해 두세요.\n\n이 내용은 재미로, 그리고 나를 돌아보는 계기로 봐 주세요."
    return cap + ("\n\n" + tagline if tagline else "")
def ig_cta(): return lambda c: M.cta(c, CTA_LINES, pill=CTA_PILL)

def render_tail(scenes, dst):
    """마지막 장면만 인스타용 CTA로 그린다. 배경 움직임(별·고리·진행 막대)은 원래 영상의 그 시각에서 이어지게 시간을 맞춘다."""
    total = sum(d for d, _ in scenes); acc = sum(d for d, _ in scenes[:-1]); dur = scenes[-1][0]; orig = M.background
    M.background = lambda fr, t, tot: orig(fr, t + acc, total)
    try: M.render(os.path.basename(dst)[:-4], [(dur, ig_cta())], os.path.dirname(dst))
    finally: M.background = orig
    return acc
def ig_reel(cid, ver, dst):
    scenes = SC[(cid, ver)]; tmp = tempfile.mkdtemp(); tail = os.path.join(tmp, "tail.mp4"); acc = render_tail(scenes, tail)
    music = os.path.join(ROOT, "clips_sop", f"{cid}_{ver}s.mp4"); silent = music.replace(".mp4", "_nomusic.mp4"); silent = silent if os.path.exists(silent) else music
    head = os.path.join(tmp, "head.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", silent, "-t", f"{acc:.3f}", "-an", "-c:v", "libx264", "-profile:v", "high", "-crf", "14", "-preset", "medium", "-pix_fmt", "yuv420p", "-r", "30", head], check=True)
    lst = os.path.join(tmp, "l.txt"); open(lst, "w").write(f"file '{head}'\nfile '{tail}'\n"); cat = os.path.join(tmp, "cat.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", cat], check=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", cat, "-i", music, "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "copy", "-shortest", "-movflags", "+faststart", dst], check=True); shutil.rmtree(tmp)
def ig_slides(cid, ver, d):
    scenes = SC[(cid, ver)]; total = sum(d_ for d_, _ in scenes); n = len(scenes); tmp = tempfile.mkdtemp()
    for i in range(n):
        sc = scenes if i < n - 1 else scenes[:-1] + [(scenes[-1][0], ig_cta())]; p = os.path.join(tmp, f"{i}.png")
        M.still(sc, i, min(sc[i][0] - 0.25, 1.9), p, total=total); Image.open(p).convert("RGB").crop(CROP).save(os.path.join(d, f"{i + 1:02d}.jpg"), quality=92, optimize=True)
    shutil.rmtree(tmp); return n

def main(only=None):
    post = json.load(open(os.path.join(ROOT, "content", "post_clips.json"), encoding="utf-8")); items = []
    for c in CS.CLIPS:
        if only and c["id"] not in only: continue
        d = os.path.join(OUT, c["id"]); os.makedirs(d, exist_ok=True); gp = str(c.get("type", "")).startswith("게시물형"); ver = "12"; have = os.path.exists(os.path.join(d, "reel.mp4")) and not os.environ.get("FORCE")
        if have:
            n = len([f for f in os.listdir(d) if f.endswith(".jpg")]); how = "블로그 이미지" if gp else "클립 장면"
        elif gp:
            shutil.copy(os.path.join(ROOT, "clips_sop", f"{c['id']}_12s.mp4"), os.path.join(d, "reel.mp4")); no = c["post"][1:]
            imgs = [f for f in (f"naver_z{no}_{k}.jpg" for k in "abc") if os.path.exists(os.path.join(ROOT, "naver", "img", f))]
            for i, f in enumerate(imgs): Image.open(os.path.join(ROOT, "naver", "img", f)).convert("RGB").resize((1080, 1080)).save(os.path.join(d, f"{i + 1:02d}.jpg"), quality=92, optimize=True)
            n = len(imgs); how = "블로그 이미지"
        else:
            ig_reel(c["id"], ver, os.path.join(d, "reel.mp4")); n = ig_slides(c["id"], ver, d); how = "클립 장면"
        cap = ig_caption(c["desc"], c.get("tags")); open(os.path.join(d, "caption.txt"), "w", encoding="utf-8").write(cap)
        items.append({"id": c["id"], "post": c["post"], "type": c.get("type"), "hook": c["hook"], "date": c.get("date"), "caption": cap, "reel": RAW + f"reuse/{c['id']}/reel.mp4", "slides": [RAW + f"reuse/{c['id']}/{i + 1:02d}.jpg" for i in range(n)], "slide_from": how, "post_title": c.get("post_title", "")})
        print(c["id"], "완료", flush=True)
    for p in post:
        if only and p["id"] not in only: continue
        d = os.path.join(OUT, p["id"]); os.makedirs(d, exist_ok=True); src = os.path.join(ROOT, p["video"].split("/main/")[1]); shutil.copy(src, os.path.join(d, "reel.mp4"))
        imgs = sorted(f for f in os.listdir(os.path.join(ROOT, "clips_post", "s10_nopage")) if f.lower().endswith((".png", ".jpg", ".jpeg"))) if os.path.isdir(os.path.join(ROOT, "clips_post", "s10_nopage")) else []
        for i, f in enumerate(imgs): Image.open(os.path.join(ROOT, "clips_post", "s10_nopage", f)).convert("RGB").save(os.path.join(d, f"{i + 1:02d}.jpg"), quality=92, optimize=True)
        items.append({"id": p["id"], "post": p["post"], "type": p["type"], "hook": p["hook"], "date": p.get("rec"), "caption": ig_caption(p["desc"], re.findall(r"#(\w+)", p.get("short", ""))), "reel": RAW + f"reuse/{p['id']}/reel.mp4", "slides": [RAW + f"reuse/{p['id']}/{i + 1:02d}.jpg" for i in range(len(imgs))], "slide_from": "게시물 클립 이미지", "post_title": p.get("post_title", "")})
        print(p["id"], "완료", flush=True)
    jp = os.path.join(ROOT, "content", "reuse.json"); cur = {x["id"]: x for x in (json.load(open(jp, encoding="utf-8")) if os.path.exists(jp) else [])}
    for x in items: cur[x["id"]] = x                      # 일부 클립만 돌려도 기존 결과에 합친다
    order = [c["id"] for c in CS.CLIPS] + [p["id"] for p in post]
    json.dump([cur[i] for i in order if i in cur], open(jp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("재활용 후보", len(items))
if __name__ == "__main__": main(sys.argv[1:] or None)
