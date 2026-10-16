"""인스타 광고용 릴스(1080x1920) — 대표 10/16 "릴스가 낫지 않겠어? 광고 돌릴건데".

캐러셀 2026-igad 와 같은 내용·같은 판을 릴스 규격에 다시 앉힌 것이다. 캐러셀 그림을 그대로
움직이지 않는다(4:5 와 9:16 은 세로가 달라 글 자리가 바뀐다).

움직임은 톤 전환 계획의 2단(K-073) — 숫자와 표가 쌓이는 과정을 보여 준다.
  첫 1초   훅 두 줄이 시간차로 들어온다 (스크롤을 세우는 자리)
  3~7초    0 에서 24.4% 까지 숫자가 올라간다 (3,000명을 세는 과정)
  7~11초   여섯 가지가 한 줄씩 쌓인다
  11~14초  마음 코칭 한 줄 + 분홍 단추
움직임은 정보를 나르거나 스크롤을 멈출 때만 쓴다. 장식으로 움직이지 않는다.

소리는 반드시 넣는다(K-070). 음악은 pipeline/reel_music.py 로 직접 작곡한다 —
clip_v3_music.py 가 쓰는 바로 그 엔진이다. 따로 만들지 않는다.

읽는 곳(전부 이미 있던 것):
  pipeline/channel_specs.py  reel 1080x1920 · 안전 영역 (50,330,900,1470) · 글꼴 크기
  pipeline/brand_frame.py    상단 좌 자오선 · 상단 우 교차분석 · 하단 우 zaoseon.com
  pipeline/fonts_kit.py      영상 제목은 G마켓 산스(JW-D), 본문 프리텐다드(JW-B)
  assets/palettes/color_combos.json  p_black_s (캐러셀과 같은 판)

사용: python3 2026-igad/reel.py [--frames-only]
"""
import os, sys, json, glob, shutil, asyncio, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(ROOT, "pipeline"))
import fonts_kit as K, brand_frame as BF, channel_specs as CS

CH = CS.CH["reel"]
W, H = CH["w"], CH["h"]                       # 1080 x 1920
SX0, SY0, SX1, SY1 = CH["safe"]               # 50, 330, 900, 1470
L, CW = 70, 810                               # 글 기둥: 안전 영역 안
Z = {z[0]: z[1:5] for z in CH["zones"]}       # 구역은 channel_specs 가 정한다. 여기서 숫자를 만들지 않는다
TY = Z["상단 라벨"][1]                         # 490 — 상단 고정 줄에서 100px 아래(대표 10/16)
BY = Z["버튼·마무리"][3]                        # 1380 — 하단 고정 줄 위까지
TH_ = BY - TY                                 # 890 — 글이 쓸 수 있는 세로
_나쁨 = CS.check("reel")                       # 규격표가 스스로 어긋나 있으면 그리기 전에 멈춘다
if _나쁨: raise SystemExit("[막음] 릴스 규격이 어긋나 있어요 —\n  · " + "\n  · ".join(_나쁨))
FPS, SEC = 24, 14.0
NF = int(FPS * SEC)
OUT = os.path.join(HERE, "reel")
VID = os.path.join(OUT, "igad-reel.mp4")

PAL = {p["id"]: p for p in json.load(open(
    os.path.join(ROOT, "assets", "palettes", "color_combos.json"), encoding="utf-8"))["palettes"]}
TH = PAL["p_black_s"]["theme"]
BG, INK, ACC = TH["bg"], TH["ink"], TH["acc"]      # #171717 / #F5F5F5 / #FF4F9A

TITLE_MIN = 100      # 채널 규격: G마켓 산스 100~118px
BODY_MIN = 52        # 프리텐다드 52~58px
LABEL_MIN = 34


def 장면(i, t0, t1, inner):
    return (f'<div class="sc" id="s{i}" data-a="{t0}" data-b="{t1}" '
            f'style="position:absolute;left:{L}px;top:{TY}px;width:{CW}px;height:{TH_}px">{inner}</div>')


def 줄(id_, txt, size, color, top, face="D", fit=True, extra=""):
    f = K.D if face == "D" else K.B
    wt = 900 if face == "D" else 800
    lo = TITLE_MIN if face == "D" else BODY_MIN
    return (f'<div id="{id_}" class="an"{" data-fit=1" if fit else ""} data-min="{lo}" data-room="{CW}" '
            f'style="position:absolute;left:0;top:{top}px;width:{CW}px;font-family:{f};font-weight:{wt};'
            f'font-size:{size}px;line-height:1.22;color:{color};white-space:nowrap;{extra}">{txt}</div>')


def 알약(id_, txt, size, top, bg, fg):
    return (f'<div id="{id_}" class="an" style="position:absolute;left:0;top:{top}px">'
            f'<span data-fit=1 data-min="{LABEL_MIN}" data-room="{CW-96}" '
            f'style="display:inline-flex;align-items:center;background:{bg};color:{fg};'
            f'border-radius:999px;padding:18px 44px;font-family:{K.B};font-weight:800;'
            f'font-size:{size}px;line-height:1;white-space:nowrap">{txt}</span></div>')


def html():
    s1 = (알약("a1", "여섯 운명학 교차", 44, 0, ACC, "#171717")
          + 줄("a2", "사주만 봤다면", 110, INK, 170)
          + 줄("a3", "반쪽만", 110, ACC, 316)
          + 줄("a4", "들은 거예요", 110, ACC, 462)
          + 줄("a5", "동서양 여섯 가지를", 58, INK, 700, "B")
          + 줄("a6", "겹쳐서 읽어요", 58, INK, 776, "B"))
    s2 = (알약("b1", "직접 세어 봤어요", 44, 0, ACC, "#171717")
          + 줄("b2", "사주와 하락이수,", 104, INK, 170)
          + 줄("b3", "얼마나 같을까요?", 104, INK, 308)
          + f'<div id="b4" class="an" style="position:absolute;left:0;top:450px;width:{CW}px;'
            f'font-family:{K.D};font-weight:900;font-size:230px;line-height:1;color:{ACC};'
            f'white-space:nowrap"><span id="bnum">0.0</span>%</div>'
          + 줄("b5", "무작위 3,000명을", 56, INK, 730, "B")
          + 줄("b6", "하나하나 계산했어요", 56, INK, 802, "B"))
    행 = lambda i, n, t: (
        f'<div id="c{i}" class="an" style="position:absolute;left:0;top:{290 + (i - 1) * 124}px;'
        f'display:flex;gap:26px;align-items:center;width:{CW}px">'
        f'<div style="flex:0 0 72px;height:72px;border-radius:999px;background:{ACC};color:#171717;'
        f'font-family:{K.D};font-weight:900;font-size:40px;display:flex;align-items:center;'
        f'justify-content:center">{n}</div>'
        f'<div data-fit=1 data-min="{BODY_MIN}" data-room="{CW-110}" style="font-family:{K.B};'
        f'font-weight:800;font-size:58px;color:{INK};white-space:nowrap">{t}</div></div>')
    s3 = (알약("c0", "겹쳐 읽는 여섯", 44, 0, ACC, "#171717")
          + 줄("cT", "한 가지만 보면", 104, INK, 140)
          + 행(1, 1, "동양 사주·자미두수") + 행(2, 2, "서양 별자리·수비학")
          + 행(3, 3, "옛 셈법 하락이수·당사주")
          + 줄("c4", "여섯이 같게 말하는 곳이", 54, ACC, 706, "B")
          + 줄("c5", "타고난 자리예요", 54, ACC, 778, "B"))
    s4 = (알약("d1", "마음 코칭까지", 44, 0, ACC, "#171717")
          + 줄("d2", "성격만 말하고", 110, INK, 170)
          + 줄("d3", "끝내지 않아요", 110, INK, 316)
          + 줄("d4", "타고난 성격을 읽고,", 56, INK, 510, "B")
          + 줄("d5", "요즘 마음을 묻고,", 56, INK, 582, "B")
          + 줄("d6", "오늘 해 볼 일 하나까지", 56, INK, 654, "B")
          + 알약("d7", "프로필 링크에서 무료로 보기", 54, 790, ACC, "#171717"))
    body = (장면(1, 0.0, 3.3, s1) + 장면(2, 3.3, 7.1, s2)
            + 장면(3, 7.1, 10.7, s3) + 장면(4, 10.7, 14.0, s4))
    return (f'<html><head><meta charset="utf-8"><style>{K.css_inline("gm")}{BF.css("dark")}'
            f'.an{{opacity:0}}.sc{{display:none}}</style></head>'
            f'<body style="margin:0;width:{W}px;height:{H}px;position:relative;overflow:hidden;'
            f'background:{BG};word-break:keep-all">{body}{BF.html("reel", ai=False)}</body></html>')


FIT_JS = """() => {                      // 글자 폭을 짐작하지 않고 브라우저에서 잰다
  const over = [];
  document.querySelectorAll('.sc').forEach(e => e.style.display = 'block');
  const 잰다 = el => { const r = document.createRange(); r.selectNodeContents(el);
    return Math.max(el.scrollWidth, Math.ceil(r.getBoundingClientRect().width)); };
  for (const el of document.querySelectorAll('[data-fit]')) {
    const min = +el.dataset.min, room = +el.dataset.room;
    let s = parseFloat(getComputedStyle(el).fontSize);
    while (잰다(el) > room && s > min) { s -= 2; el.style.fontSize = s + 'px'; }
    if (잰다(el) > room) over.push([el.textContent.trim(), room, 잰다(el), min]);
  }
  document.querySelectorAll('.sc').forEach(e => e.style.display = 'none');
  return over;
}"""

# 한 프레임을 t(초)로 그린다. 모든 움직임이 t 하나에서 나오므로 되돌려 그려도 같은 그림이 나온다.
DRAW_JS = """(t) => {
  const E = id => document.getElementById(id);
  const ease = x => 1 - Math.pow(1 - x, 3);
  const clamp = x => Math.max(0, Math.min(1, x));
  document.querySelectorAll('.sc').forEach(sc => {
    const a = +sc.dataset.a, b = +sc.dataset.b;
    sc.style.display = (t >= a && t < b) ? 'block' : 'none';
  });
  // 줄이 아래에서 올라오며 들어온다
  const inn = (id, t0, dy) => { const e = E(id); if (!e) return;
    const k = ease(clamp((t - t0) / 0.45));
    e.style.opacity = k; e.style.transform = `translateY(${(1 - k) * (dy === undefined ? 34 : dy)}px)`; };
  // 단추는 톡 튀어나온다 — 누를 곳이라는 신호
  const pop = (id, t0) => { const e = E(id); if (!e) return;
    const p = clamp((t - t0) / 0.5), k = ease(p);
    e.style.opacity = k; e.style.transform = `scale(${0.82 + 0.18 * k + 0.05 * Math.sin(Math.PI * p)})`;
    e.style.transformOrigin = 'left center'; };

  inn('a1', 0.10); inn('a2', 0.30); inn('a3', 0.70); inn('a4', 0.95); inn('a5', 1.70); inn('a6', 1.85);

  inn('b1', 3.40); inn('b2', 3.55); inn('b3', 3.75);
  { const e = E('b4'); const p = clamp((t - 4.15) / 0.40);
    e.style.opacity = ease(p); e.style.transform = `translateY(${(1 - ease(p)) * 26}px)`;
    const q = clamp((t - 4.30) / 1.90);                 // 0 에서 24.4 까지 세어 올라간다
    E('bnum').textContent = (24.4 * ease(q)).toFixed(1); }
  inn('b5', 6.35); inn('b6', 6.50);

  inn('c0', 7.20); inn('cT', 7.35);
  inn('c1', 7.70); inn('c2', 8.25); inn('c3', 8.80);     // 한 줄씩 쌓인다
  inn('c4', 9.55); inn('c5', 9.70);

  inn('d1', 10.80); inn('d2', 10.95); inn('d3', 11.15);
  inn('d4', 11.75); inn('d5', 11.90); inn('d6', 12.05);
  pop('d7', 12.55);
}"""


async def shoot():
    from playwright.async_api import async_playwright
    shutil.rmtree(OUT, ignore_errors=True)
    os.makedirs(OUT, exist_ok=True)
    async with async_playwright() as p:
        br = await p.chromium.launch(args=["--font-render-hinting=none"])
        pg = await br.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
        await pg.set_content(html(), wait_until="load")
        await pg.evaluate("document.fonts.ready")
        넘침 = await pg.evaluate(FIT_JS)
        if 넘침:
            raise SystemExit("\n[막음] 다음 글이 기둥(810px) 안에 규격 바닥 크기로도 안 들어가요 —\n  "
                             + "\n  ".join(f'"{a}" ({b}px 자리에 {c}px 필요, 바닥 {d}px)' for a, b, c, d in 넘침)
                             + "\n  글을 줄이세요.\n")
        for i in range(NF):
            await pg.evaluate(DRAW_JS, i / FPS)
            await pg.screenshot(path=os.path.join(OUT, f"f{i:04d}.jpg"), quality=92, type="jpeg")
            if i % 48 == 0:
                print(f"  {i}/{NF}")
        await br.close()


def 영상():
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS),
                    "-i", os.path.join(OUT, "f%04d.jpg"), "-c:v", "libx264", "-pix_fmt", "yuv420p",
                    "-crf", "19", "-movflags", "+faststart", VID + ".silent.mp4"], check=True)


def 소리():
    """K-070: 소리 없이 내보내지 않는다. clip_v3_music 과 같은 엔진(reel_music)으로 직접 작곡한다."""
    import reel_music as RM
    style, key, seed = "경쾌 신스팝", "D", 2610
    bpm = RM.pick_bpm(style, seed)
    beats = max(8, (SEC - 0.3) / (60.0 / bpm))
    wav = "/tmp/igad_reel.wav"
    RM.compose_up(style, beats, seed, wav, key=key, bpm=bpm, tail=0.3)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", VID + ".silent.mp4", "-i", wav,
                    "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                    "-af", f"afade=t=out:st={SEC - 0.6:.2f}:d=0.6", "-c:a", "aac", "-b:a", "128k",
                    "-t", f"{SEC:.3f}", "-movflags", "+faststart", VID], check=True)
    os.remove(VID + ".silent.mp4")
    return dict(style=style, bpm=bpm, key=key, seed=seed)


def 검사():
    """만든 영상을 숫자로 잰다 — 규격·길이·소리."""
    j = json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format",
                                   "-of", "json", VID], capture_output=True, text=True, check=True).stdout)
    v = next(s for s in j["streams"] if s["codec_type"] == "video")
    a = [s for s in j["streams"] if s["codec_type"] == "audio"]
    bad = []
    if (v["width"], v["height"]) != (W, H):
        bad.append(f"규격 {v['width']}x{v['height']} (= {W}x{H} 이어야 해요)")
    if not a:
        bad.append("소리가 없어요 — 릴스·클립은 소리 없이 내보내지 않습니다(K-070)")
    d = float(j["format"]["duration"])
    if not (SEC - 0.5 <= d <= SEC + 0.5):
        bad.append(f"길이 {d:.1f}초 (= {SEC}초 안팎이어야 해요)")
    if bad:
        raise SystemExit("[결과물 검사에 걸렸어요]\n  · " + "\n  · ".join(bad))
    print(f"결과물 검사 통과 ✓ · {v['width']}x{v['height']} · {d:.1f}초 · 소리 있음")


if __name__ == "__main__":
    asyncio.run(shoot())
    영상()
    if "--frames-only" not in sys.argv:
        print("음악:", 소리())
    검사()
    for f in glob.glob(os.path.join(OUT, "f*.jpg")):
        os.remove(f)
    print("만들었어요:", VID)
