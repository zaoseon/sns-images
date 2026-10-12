"""인스타 릴스 → 네이버 클립 재활용 (10/12 대표 승인 21:43, 수정 기록 D-190).
방식: [클립 전용 첫 장면 2.6초] + [릴스 본문(끝의 팔로우·프로필 링크 장면은 자름, 음악 없음)] + [끝 장면 3초: 블로그에서 전체 글 보기 · zaoseon.com].
- 릴스를 그대로 올리지 않는다(R39): 첫 장면 문구·썸네일·설명글은 클립 전용으로 따로 쓴다.
- 릴스 화면 속 인스타 전용 글(프로필 링크 등)과 금지어('상담가')는 masks 로 가리거나 바꾼다.
- 규격: 세로 9:16 1080x1920, 30fps, H.264 MP4, 소리 없음, 파일명 영문·숫자·하이픈. 길이는 보통 20~30초(네이버 도움말에서 최대 길이를 확인하지 못해 1분 안쪽으로 둔다).
- 안전영역(제작 가이드 §1): 글은 x 50~900, y 330~1470 안.
- 유료 Claude API를 쓰지 않는다. ffmpeg + PIL 만 쓴다.
사용:
  python3 pipeline/clip_from_reel.py --all            명세(content/clips_from_reels.json)의 클립을 모두 렌더 + 검사
  python3 pipeline/clip_from_reel.py --id rc-1014-rabbit
  python3 pipeline/clip_from_reel.py --detect 영상.mp4   릴스의 장면이 바뀌는 시각을 보여 준다(trim_end 정할 때)
  python3 pipeline/clip_from_reel.py --audit           설명글·문구 검사만(영상 안 만듦)
  python3 pipeline/clip_from_reel.py --queue           업로드 큐 문서(clips_reel/QUEUE.md)와 설명글 파일 만들기
결과: clips_reel/<id>.mp4, <id>_thumb.png(클립 전용 썸네일), <id>_check.png(첫·중간·끝 프레임), desc/<id>.txt"""
import os, sys, re, json, subprocess, tempfile, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "..")); sys.path.insert(0, HERE)
from PIL import Image, ImageDraw, ImageFont
import clip_sop as C
_bg0 = C.bg; _bgc = []
def _bg():   # 배경은 그리는 데 오래 걸려 한 번만 그리고 복사해 쓴다
    if not _bgc: _bgc.append(_bg0())
    return _bgc[0].copy()
C.bg = _bg
SPEC = os.path.join(ROOT, "content", "clips_from_reels.json"); OUT = os.path.join(ROOT, "clips_reel")
W, H = 1080, 1920; CX = 475                      # 안전영역 x 50~900 의 가운데
RAW = "https://raw.githubusercontent.com/zaoseon/sns-images/main/clips_reel/"
FORBID = [("상담", "'상담' 금지(코칭·코치로)"), ("치료", "치료 표현 금지"), ("적중", "적중률 표현 금지"), ("반드시", "단정 금지"), ("무조건", "단정 금지")]
INTRO_DUR, OUTRO_DUR = 2.6, 3.0

def spec(): return json.load(open(SPEC, encoding="utf-8"))
def fit(text, path, size, maxw, lo=72):
    """가장 긴 줄이 maxw 안에 들어오는 가장 큰 글자 크기(최대 size)."""
    while size > lo:
        f = C.font(path, size); ok = all(f.getlength("".join(c[0] for c in ln)) <= maxw for ln in C.wrap(text, f, 10 ** 6))
        if ok: break
        size -= 4
    return size
def band(d):
    f = ImageFont.truetype(C.SERIF, 40, index=2); d.text((60, 345), "子午線 자오선", font=f, fill=C.GOLD)
    g = C.font(C.MED, 34); d.text((900 - g.getlength("zaoseon.com"), 1428), "zaoseon.com", font=g, fill=C.GOLD)
def hook_frame(kicker, text):
    im = C.bg(); d = ImageDraw.Draw(im, "RGBA"); band(d)
    size = fit(text, C.BLACK, 112, 840); tot = C.block_h(text, size, maxw=840, lh=1.3) + 108
    y0 = 910 - tot // 2; y0 = C.chip(d, kicker, y0, 44) + 54
    C.draw_lines(d, text, y0, size, maxw=840, lh=1.3); return im
def outro_frame(o):
    im = C.bg(); d = ImageDraw.Draw(im, "RGBA"); band(d)
    size = fit(o["text"], C.BLACK, 96, 840); th = C.block_h(o["text"], size, maxw=840, lh=1.3)
    sub = o.get("sub"); sh = (C.block_h(sub, 44, maxw=840, lh=1.45, path=C.MED) + 70) if sub else 0
    tot = th + 60 + 116 + sh; y = 910 - tot // 2
    y = C.draw_lines(d, o["text"], y, size, maxw=840, lh=1.3)
    fnt = C.font(C.BLACK, 58); w = fnt.getlength(o["pill"]) + 90; x = CX - w / 2; y += 60
    d.rounded_rectangle((x, y, x + w, y + 116), radius=58, fill=C.GOLD); d.text((CX - fnt.getlength(o["pill"]) / 2, y + 28), o["pill"], font=fnt, fill=(23, 20, 15))
    if sub: C.draw_lines(d, sub, y + 116 + 70, 44, color=C.DIM, path=C.MED, maxw=840, lh=1.45)
    return im
def mask_png(masks, path):
    """투명 PNG 한 장: masks 의 칸을 단색으로 덮고 text 가 있으면 그 자리에 새 글을 쓴다."""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for m in masks:
        x0, y0, x1, y1 = m["rect"]; d.rectangle((x0, y0, x1, y1), fill=tuple(m["color"]) + (255,))
        if m.get("text"):
            f = C.font(os.path.join(HERE, "fonts", "PRETENDARD-REGULAR.OTF"), m.get("size", 25)); d.text((x0 + 7, y0 + 3), m["text"], font=f, fill=tuple(m.get("tcolor", (255, 255, 255))) + (255,))
    im.save(path)
def run(cmd): subprocess.run(cmd, check=True, stderr=subprocess.DEVNULL if "-loglevel" in cmd else None)
ENC = ["-c:v", "libx264", "-crf", "19", "-preset", "medium", "-pix_fmt", "yuv420p", "-r", "30", "-an"]
def still_seg(png, dur, out):
    run(["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-framerate", "30", "-t", str(dur), "-i", png, "-vf",
         f"fade=t=in:st=0:d=0.18,fade=t=out:st={dur - 0.16}:d=0.16,format=yuv420p"] + ENC + [out])
def body_seg(c, sp, out, tmp):
    groups = []                                      # [(from_sec, [mask...])] — 시작 시각이 같은 칸끼리 한 장으로
    allm = (sp["masks_common_panel"] if c.get("panel") else []) + c.get("masks", [])
    for m in allm:
        t = m.get("from", 0); g = next((g for g in groups if g[0] == t), None)
        if g: g[1].append(m)
        else: groups.append((t, [m]))
    ins = ["-i", os.path.join(ROOT, c["src"])]; filt = "[0:v]fps=30,scale=1080:1920,setsar=1[v0]"; last = "v0"
    for i, (t, ms) in enumerate(groups):
        p = os.path.join(tmp, f"m{i}.png"); mask_png(ms, p); ins += ["-loop", "1", "-i", p]
        filt += f";[{last}][{i + 1}:v]overlay=0:0:enable='gte(t,{t})':shortest=1[v{i + 1}]"; last = f"v{i + 1}"
    run(["ffmpeg", "-y", "-loglevel", "error"] + ins + ["-t", str(c["trim_end"]), "-filter_complex", filt, "-map", f"[{last}]"] + ENC + [out])
def render(c, sp):
    os.makedirs(OUT, exist_ok=True); tmp = tempfile.mkdtemp(); outp = os.path.join(OUT, c["id"] + ".mp4")
    hook_frame(c["kicker"], c["hook"]).save(os.path.join(tmp, "i.png")); outro_frame(sp["outro"]).save(os.path.join(tmp, "o.png"))
    still_seg(os.path.join(tmp, "i.png"), INTRO_DUR, os.path.join(tmp, "i.mp4")); still_seg(os.path.join(tmp, "o.png"), OUTRO_DUR, os.path.join(tmp, "o.mp4"))
    body_seg(c, sp, os.path.join(tmp, "b.mp4"), tmp)
    lst = os.path.join(tmp, "l.txt"); open(lst, "w").write("".join(f"file '{os.path.join(tmp, n)}'\n" for n in ("i.mp4", "b.mp4", "o.mp4")))
    run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", "-movflags", "+faststart", outp])
    # 클립 전용 썸네일: 첫 장면과 같은 틀, 문구는 제목과 다른 말(thumb)
    hook_frame(c["kicker"], c["thumb"].replace(", ", ",\n") if len(c["thumb"]) > 14 and "\n" not in c["thumb"] and ", " in c["thumb"] else c["thumb"]).save(os.path.join(OUT, c["id"] + "_thumb.png"))
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", outp]))
    check_sheet(outp, dur, os.path.join(OUT, c["id"] + "_check.png")); shutil.rmtree(tmp); return outp, dur
def check_sheet(mp4, dur, out):
    """눈으로 확인용: 첫·중간·끝 프레임 6장을 한 장으로(글자 잘림·안전영역 선 표시)."""
    ts = [0.4, INTRO_DUR + 1.0, dur * 0.5, dur * 0.72, dur - OUTRO_DUR - 0.4, dur - 0.9]; sh = Image.new("RGB", (360 * 6, 640)); tmp = tempfile.mkdtemp()
    for i, t in enumerate(ts):
        p = os.path.join(tmp, f"{i}.png"); run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{max(t, 0):.2f}", "-i", mp4, "-frames:v", "1", "-vf", "scale=360:640", p])
        im = Image.open(p).convert("RGB"); d = ImageDraw.Draw(im)
        d.rectangle((50 / 3, 330 / 3, 900 / 3, 1470 / 3), outline=(255, 60, 60), width=1)       # 안전영역
        sh.paste(im, (360 * i, 0))
    sh.save(out); shutil.rmtree(tmp)
def probe(mp4):
    j = json.loads(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,codec_name,width,height,r_frame_rate:format=duration,size", "-of", "json", mp4]))
    return j
def audit(sp):
    """설명글·문구 검사. 문제 목록을 돌려준다(빈 목록이면 통과)."""
    import natural_audit as N
    bad = []
    for c in sp["clips"]:
        body = c["desc"]; tags = c["tags"]
        full = body + "\n\n" + " ".join("#" + t for t in tags)
        if len(body) > 300: bad.append((c["id"], f"설명 {len(body)}자 > 300"))
        if len(tags) != 5 or len(set(tags)) != 5: bad.append((c["id"], "해시태그는 서로 다른 5개"))
        if tags[0] != "사주": bad.append((c["id"], "첫 해시태그는 사주"))
        if re.search(r"https?://|zaoseon\.com|utm_", body): bad.append((c["id"], "설명에 주소 금지(블로그 스티커가 연결)"))
        if "블로그" not in body: bad.append((c["id"], "관련 블로그 글 안내 문장 없음"))
        if "돌아보" not in body: bad.append((c["id"], "코칭 관점(돌아보기) 한 줄 없음"))
        if not re.search(r"(돌아보|정해 보|건네 보|해 보면|먼저 .*보세요)", body): bad.append((c["id"], "행동 한 줄 없음"))
        for w, why in FORBID:
            for where, t in (("설명", full), ("첫장면", c["hook"] + c["kicker"]), ("썸네일", c["thumb"])):
                if w in t: bad.append((c["id"], f"{where}: {why}"))
        if c["thumb"].replace("*", "").replace("\n", "") in c["hook"].replace("*", "").replace("\n", ""): bad.append((c["id"], "썸네일 문구가 첫 장면과 같음(R39)"))
        if not os.path.exists(os.path.join(ROOT, c["src"])): bad.append((c["id"], "원본 릴스 없음: " + c["src"]))
        texts = [(c["id"] + ":desc", body), (c["id"] + ":hook", c["hook"].replace("*", "")), (c["id"] + ":thumb", c["thumb"]), (c["id"] + ":kicker", c["kicker"])]
        for h in N.scan(texts): bad.append((c["id"], f"natural_audit {h[0]} | {h[2]}"))
    ids = [c["id"] for c in sp["clips"]]
    if len(set(ids)) != len(ids): bad.append(("-", "id 중복"))
    ups = [c["upload"] for c in sp["clips"]]
    if len(set(ups)) != len(ups): bad.append(("-", "올리는 날 중복(하루 1개)"))
    return bad
def verify(c, mp4):
    j = probe(mp4); v = [s for s in j["streams"] if s["codec_type"] == "video"]; a = [s for s in j["streams"] if s["codec_type"] == "audio"]; bad = []
    if a: bad.append("소리가 있음")
    if not v or (v[0]["width"], v[0]["height"]) != (1080, 1920): bad.append("1080x1920 아님")
    if v and v[0]["codec_name"] != "h264": bad.append("h264 아님")
    d = float(j["format"]["duration"]); mb = int(j["format"]["size"]) / 1e6
    if d > 60: bad.append(f"길이 {d:.0f}초 > 60")
    if mb > 100: bad.append(f"용량 {mb:.0f}MB")
    return bad, d, mb
def detect(f):
    import numpy as np
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", f, "-vf", "fps=10,scale=54:96,format=gray", "-f", "rawvideo", "-"], capture_output=True).stdout
    a = np.frombuffer(raw, np.uint8).reshape(-1, 96, 54).astype(float); d = np.abs(np.diff(a, axis=0)).mean(axis=(1, 2))
    print("길이", len(a) / 10, "초 · 화면이 크게 바뀐 시각(초):", [round((i + 1) / 10, 1) for i, v in enumerate(d) if v > 1.5])
def blog_info(pid):
    try:
        p = json.load(open(os.path.join(ROOT, "naver", "pages.json"), encoding="utf-8"))[pid]; pub = json.load(open(os.path.join(ROOT, "naver", "published.json"), encoding="utf-8")).get(pid, {})
        return p["title"], p["dt"][:10], pub.get("url", ""), pub.get("status", "")
    except Exception: return pid, "", "", ""
def queue(sp):
    os.makedirs(os.path.join(OUT, "desc"), exist_ok=True); rows = []; wd = "월화수목금토일"
    import datetime
    for c in sp["clips"]:
        txt = c["desc"] + "\n\n" + " ".join("#" + t for t in c["tags"]); open(os.path.join(OUT, "desc", c["id"] + ".txt"), "w", encoding="utf-8").write(txt + "\n")
        t, dt, url, st = blog_info(c["blog"]); dd = datetime.date.fromisoformat(c["upload"])
        rows.append(f"| {c['upload'][5:].replace('-', '/')}({wd[dd.weekday()]}) | [{c['id']}.mp4]({RAW}{c['id']}.mp4) | [설명 글]({RAW}desc/{c['id']}.txt) | {c['blog']} {t} (원고 날짜 {dt[5:].replace('-', '/')}) | {c['reel_date'][5:]} 인스타 릴스 |")
    head = ("# 네이버 클립 일일 업로드 큐 (릴스 재활용)\n\n"
            "하루 1개, 최근 7일 릴스부터. 대표가 파일 1개씩 폰에서 올린다. 영상은 소리가 없다(음악은 올릴 때 앱에서 고르지 않는다 — 대표 결정 10/12).\n"
            "영상 파일은 공개 주소(raw)라 폰 브라우저에서 열어 사진첩에 저장하면 된다. 만드는 법·최소 절차는 `HANDOFF.md` 'D-190 네이버 클립' 참고.\n\n"
            "| 올릴 날 | 영상 | 설명 | 스티커로 걸 블로그 글 | 원본 릴스 |\n|---|---|---|---|---|\n")
    open(os.path.join(OUT, "QUEUE.md"), "w", encoding="utf-8").write(head + "\n".join(rows) + "\n"); print("큐", len(rows), "줄 →", os.path.join(OUT, "QUEUE.md"))
def main(a):
    sp = spec()
    if "--detect" in a: return detect(a[a.index("--detect") + 1])
    if "--audit" in a:
        bad = audit(sp); print("문구 검사:", "통과" if not bad else ""); [print("  ", b) for b in bad]; sys.exit(1 if bad else 0)
    if "--queue" in a: return queue(sp)
    ids = [a[a.index("--id") + 1]] if "--id" in a else [c["id"] for c in sp["clips"]] if "--all" in a else []
    if not ids: print(__doc__); return
    bad = audit(sp)
    if bad: print("문구 검사 실패(영상 만들기 전에 고친다):"); [print("  ", b) for b in bad]; sys.exit(1)
    fails = []
    for c in [c for c in sp["clips"] if c["id"] in ids]:
        p, d = render(c, sp); vb, d, mb = verify(c, p); print(f"{c['id']}: {d:.1f}초 {mb:.1f}MB", "OK" if not vb else vb); fails += [(c["id"], x) for x in vb]
    queue(sp); sys.exit(1 if fails else 0)
if __name__ == "__main__": main(sys.argv[1:])
