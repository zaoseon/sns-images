"""네이버 클립 SOP판 영상 렌더러 (10/2): 블로그 글 1편 → 클립 3종(질문형·오해 교정형·체크리스트형)의 12초판/30초판.
- 장면 목록(scenes)으로 1080x1920 PNG를 그리고 ffmpeg로 이어 붙인다(소리 없음: 음악은 대표가 네이버 앱에서 고른다).
- 네이버 클립 재생 화면이 가리는 곳(위 y<125, 오른쪽 x>=905, 아래 y>=1485)을 피해 글자는 x 70~880, y 190~1440 안에 둔다.
- 캐릭터 이미지를 쓰지 않는다(AI 생성 캐릭터 표시가 필요 없게). 글자 중심, 한 화면 한 메시지.
장면 종류: hook / point / list / close / cta. 글자 안 *...* 는 금색 강조.
사용: python3 pipeline/clip_sop.py (content/clips_sop.py 의 CLIPS를 모두 렌더)"""
import os, sys, random, subprocess, tempfile, shutil, json
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, "..")
SERIF = "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc"   # 한자(子午線)가 들어 있는 글꼴
BLACK = os.path.join(HERE, "fonts", "PRETENDARD-BLACK.OTF"); MED = os.path.join(HERE, "fonts", "PRETENDARD-MEDIUM.OTF")
W, H = 1080, 1920; CX = 470; L, R, T, B = 70, 880, 190, 1440
NAVY1, NAVY2, GOLD, WHITE, DIM = (14, 17, 27), (26, 33, 54), (224, 184, 102), (255, 255, 255), (214, 218, 228)
_fc = {}
def font(path, size):
    k = (path, size)
    if k not in _fc: _fc[k] = ImageFont.truetype(path, size)
    return _fc[k]
def bg():
    im = Image.new("RGB", (W, H)); px = im.load()
    for y in range(H):
        t = y / H; c = tuple(int(NAVY1[i] + (NAVY2[i] - NAVY1[i]) * (1 - abs(t - .42) * 1.6 if abs(t - .42) < .625 else 0)) for i in range(3))
        for x in range(0, W, 1): px[x, y] = c
    d = ImageDraw.Draw(im, "RGBA"); rnd = random.Random(7)
    for _ in range(90):
        x, y = rnd.randint(0, W), rnd.randint(150, 1500); r = rnd.choice([1, 1, 2]); d.ellipse((x - r, y - r, x + r, y + r), fill=(255, 236, 190, rnd.randint(60, 170)))
    for r, a in ((470, 36), (452, 22)): d.ellipse((CX - r, 800 - r, CX + r, 800 + r), outline=(224, 184, 102, a), width=2)
    return im
def wrap(text, fnt, maxw):
    """*강조*를 유지한 채 띄어쓰기에서 줄을 나눈다. 글자별 (문자, 강조 여부) 목록을 돌려준다."""
    chars, hl = [], False
    for ch in text:
        if ch == "*": hl = not hl; continue
        chars.append((ch, hl))
    words, cur = [], []
    for c in chars:
        if c[0] == " ":
            if cur: words.append(cur); cur = []
        elif c[0] == "\n":
            if cur: words.append(cur); cur = []
            words.append("BR")
        else: cur.append(c)
    if cur: words.append(cur)
    lines, line = [], []
    def w(cs): return fnt.getlength("".join(c[0] for c in cs))
    for wd in words:
        if wd == "BR": lines.append(line); line = []; continue
        cand = line + ([(" ", False)] if line else []) + wd
        if line and w(cand) > maxw: lines.append(line); line = list(wd)
        else: line = cand
    if line: lines.append(line)
    return lines
def draw_lines(d, text, y, size, color=WHITE, path=BLACK, maxw=R - L, lh=1.28, align="center", hl=GOLD, x0=None):
    fnt = font(path, size); lines = wrap(text, fnt, maxw)
    for ln in lines:
        wtot = fnt.getlength("".join(c[0] for c in ln)); x = (CX - wtot / 2) if align == "center" else (x0 if x0 is not None else L)
        for ch, h in ln:
            d.text((x, y), ch, font=fnt, fill=hl if h else color); x += fnt.getlength(ch)
        y += int(size * lh)
    return y
def chip(d, text, y, size=38):
    fnt = font(BLACK, size); w = fnt.getlength(text) + 56; x = CX - w / 2
    d.rounded_rectangle((x, y, x + w, y + size + 28), radius=(size + 28) // 2, outline=GOLD, width=3)
    d.text((CX - fnt.getlength(text) / 2, y + 12), text, font=fnt, fill=GOLD); return y + size + 28
def brand(d):
    f = ImageFont.truetype(SERIF, 44, index=2) if SERIF.endswith(".ttc") else font(BLACK, 44)   # index 2 = KR
    d.text((CX - f.getlength("子午線 자오선") / 2, 200), "子午線 자오선", font=f, fill=GOLD)
def block_h(text, size, maxw=R - L, lh=1.28, path=BLACK): return len(wrap(text, font(path, size), maxw)) * int(size * lh)
def frame(scene, idx, total, kicker=None):
    im = bg(); d = ImageDraw.Draw(im, "RGBA"); k = scene["kind"]
    brand(d)
    if k == "hook":
        hh = block_h(scene["text"], 124, lh=1.3) + (96 if kicker else 0); y0 = 800 - hh // 2
        if kicker: y0 = chip(d, kicker, y0, 46) + 50
        draw_lines(d, scene["text"], y0, 124, lh=1.3)
    elif k == "point":
        hh = block_h(scene["text"], 104, lh=1.32) + (110 if scene.get("kicker") else 0) + (block_h(scene["sub"], 56, lh=1.45, path=MED) + 50 if scene.get("sub") else 0); y = 800 - hh // 2
        if scene.get("kicker"): y = chip(d, scene["kicker"], y, 46) + 56
        y = draw_lines(d, scene["text"], y, 104, lh=1.32)
        if scene.get("sub"): draw_lines(d, scene["sub"], y + 40, 56, color=DIM, path=MED, lh=1.45)
    elif k == "list":
        n = scene.get("show", len(scene["items"])); cur = scene.get("active")
        allh = block_h(scene["title"], 74, lh=1.3) + 50 + sum(block_h(it, 66, maxw=R - L - 110, lh=1.3) + 46 for it in scene["items"])   # 세 줄을 모두 보인 높이로 맞춰 줄이 늘어도 위치가 안 움직이게
        y = 800 - allh // 2
        if scene.get("title"): y = draw_lines(d, scene["title"], y, 74, color=GOLD, lh=1.3) + 50
        for i, it in enumerate(scene["items"][:n]):
            on = (cur is None) or (i == cur); col = WHITE if on else (150, 156, 172)
            d.ellipse((L, y + 6, L + 76, y + 82), fill=GOLD if on else (74, 82, 104)); nf = font(BLACK, 46)
            d.text((L + 38 - nf.getlength(str(i + 1)) / 2, y + 17), str(i + 1), font=nf, fill=(23, 20, 15))
            y2 = draw_lines(d, it, y, 66, color=col, align="left", x0=L + 110, maxw=R - L - 110, lh=1.3); y = y2 + 46
    elif k == "close":
        hh = block_h(scene["text"], 112, lh=1.33) + (110 if scene.get("kicker") else 0) + (block_h(scene["sub"], 56, lh=1.45, path=MED) + 46 if scene.get("sub") else 0); y = 800 - hh // 2
        if scene.get("kicker"): y = chip(d, scene["kicker"], y, 46) + 48
        y = draw_lines(d, scene["text"], y, 112, lh=1.33)
        if scene.get("sub"): draw_lines(d, scene["sub"], y + 36, 56, color=DIM, path=MED, lh=1.45)
    elif k == "cta":
        hh = block_h(scene["text"], 90, lh=1.33) + 190; y0 = 800 - hh // 2
        y = draw_lines(d, scene["text"], y0, 90, lh=1.33)
        fnt = font(BLACK, 58); label = scene.get("pill", "zaoseon.com 무료 풀이 · 1초"); w = fnt.getlength(label) + 80; x = CX - w / 2; y += 60
        d.rounded_rectangle((x, y, x + w, y + 116), radius=58, fill=GOLD); d.text((CX - fnt.getlength(label) / 2, y + 28), label, font=fnt, fill=(23, 20, 15))
    # 진행 점
    x0 = CX - (total * 34) / 2 + 12
    for i in range(total): d.ellipse((x0 + i * 34, 1405, x0 + i * 34 + 14, 1419), fill=GOLD if i == idx else (74, 82, 104))
    return im
def render(name, scenes, kicker, outdir):
    tmp = tempfile.mkdtemp(); segs = []
    for i, sc in enumerate(scenes):
        p = os.path.join(tmp, f"s{i}.png"); frame(sc, i, len(scenes), kicker).save(p)
        seg = os.path.join(tmp, f"s{i}.mp4"); dur = sc["dur"]
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-framerate", "30", "-t", str(dur), "-i", p, "-vf",
                        f"fade=t=in:st=0:d=0.18,fade=t=out:st={dur - 0.14}:d=0.14,format=yuv420p", "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-an", seg], check=True); segs.append(seg)
    lst = os.path.join(tmp, "list.txt"); open(lst, "w").write("".join(f"file '{s}'\n" for s in segs))
    out = os.path.join(outdir, name + ".mp4"); os.makedirs(outdir, exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", "-movflags", "+faststart", out], check=True)
    frame(scenes[0], 0, len(scenes), kicker).save(os.path.join(outdir, name + "_first.png"))
    shutil.rmtree(tmp); return out, sum(s["dur"] for s in scenes)
def cover(name, phrase, kicker, outdir):
    im = bg(); d = ImageDraw.Draw(im, "RGBA")
    brand(d); hh = block_h(phrase, 124, lh=1.3) + 96; y0 = 800 - hh // 2
    y0 = chip(d, kicker, y0, 46) + 50; draw_lines(d, phrase, y0, 124, lh=1.3)
    p = os.path.join(outdir, name + "_thumb.png"); im.save(p); return p
if __name__ == "__main__":
    sys.path.insert(0, os.path.join(ROOT, "content")); import clips_sop
    out = os.path.join(ROOT, "clips_sop")
    for c in clips_sop.CLIPS:
        for ver in ("12", "30"):
            if ver in c["scenes"]:
                p, dur = render(f'{c["id"]}_{ver}s', c["scenes"][ver], c["kicker"], out); print(os.path.basename(p), dur, "초")
        cover(c["id"], c["thumbs"][0], c["kicker"], out)
