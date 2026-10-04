"""이미지 여러 장 -> 네이버 클립용 세로 영상(1080x1920, 음악 포함). 10/4 대표 지시: 게시물 클립 이미지(블로그 원고 이미지+캡션)로 영상을 만든다.
이미지는 가운데 1000폭으로 놓아 클립 앱이 덮는 위 330px·아래 340px을 비우고, 배경은 같은 이미지를 흐리게 늘려 채운다. 장마다 2.6초, 살짝 확대, 0.35초 겹침.
사용: images_to_clip(out_mp4, [이미지경로...], hold=2.6, first_hold=3.0, last_hold=3.4, style='상큼 팝', seed=1, key='D')"""
import os, sys, subprocess, tempfile
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from PIL import Image, ImageFilter, ImageEnhance
import reel_music as RM
W, H = 1080, 1920; FG_W = 1000; TOP = 330; XF = 0.35; FPS = 30
def frame(src, dst):
    im = Image.open(src).convert("RGB"); r = FG_W / im.width; fg = im.resize((FG_W, int(im.height * r)), Image.LANCZOS)
    bg = im.copy(); s = max(W / bg.width, H / bg.height); bg = bg.resize((int(bg.width * s) + 1, int(bg.height * s) + 1), Image.LANCZOS)
    bx, by = (bg.width - W) // 2, (bg.height - H) // 2; bg = bg.crop((bx, by, bx + W, by + H)).filter(ImageFilter.GaussianBlur(40))
    bg = ImageEnhance.Brightness(bg).enhance(0.55); can = bg.copy(); y = TOP if fg.height <= H - TOP - 340 else max(40, (H - fg.height) // 2)
    can.paste(fg, ((W - FG_W) // 2, y)); can.save(dst, quality=95)
def images_to_clip(out_mp4, images, hold=2.6, first_hold=3.0, last_hold=3.4, style="상큼 팝", seed=1, key="D"):
    tmp = tempfile.mkdtemp(); segs = []; durs = []
    for i, p in enumerate(images):
        f = os.path.join(tmp, f"f{i}.jpg"); frame(p, f)
        d = (first_hold if i == 0 else last_hold if i == len(images) - 1 else hold) + (XF if i < len(images) - 1 else 0); durs.append(d)
        seg = os.path.join(tmp, f"s{i}.mp4"); n = int(d * FPS)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-i", f, "-vf", f"zoompan=z='1+0.035*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={n}:s={W}x{H}:fps={FPS},format=yuv420p", "-t", f"{d:.3f}", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", seg], check=True); segs.append(seg)
    cmd = ["ffmpeg", "-y", "-loglevel", "error"]
    for s in segs: cmd += ["-i", s]
    fc = ""; last = "[0:v]"; off = 0.0
    for i in range(1, len(segs)):
        off += durs[i - 1] - XF; fc += f"{last}[{i}:v]xfade=transition=fade:duration={XF}:offset={off:.3f}[v{i}];"; last = f"[v{i}]"
    total = sum(durs) - XF * (len(segs) - 1); vid = os.path.join(tmp, "v.mp4")
    subprocess.run(cmd + ["-filter_complex", fc.rstrip(";"), "-map", last, "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p", vid], check=True)
    bpm = RM.pick_bpm(style, seed); beats = max(8, int((total - 0.3) * bpm / 60.0)); wav = os.path.join(tmp, "m.wav")
    RM.compose_up(style, beats, seed, wav, key=key, bpm=bpm, cuts=[])
    os.makedirs(os.path.dirname(out_mp4), exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", vid, "-i", wav, "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "128k", "-t", f"{total:.3f}", "-shortest", "-movflags", "+faststart", out_mp4], check=True)
    return total
if __name__ == "__main__":
    ROOT = os.path.join(HERE, "..")
    imgs = [os.path.join(ROOT, "clips_post", "s10_nopage", f"s10_{i}.jpg") for i in range(1, 7)]
    t = images_to_clip(os.path.join(ROOT, "clips_post", "s10_nopage", "s10_clip.mp4"), imgs, style="발랄 우쿨렐레", seed=91, key="G"); print("s10 clip", round(t, 1), "s")
