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
FPS = 24

SET = os.environ.get("ZS_SET", "2026-igad")   # 릴스 한 편을 따로 만들 때: ZS_SET=2026-igevent
BASE = os.path.join(ROOT, SET)
SPEC = json.load(open(os.path.join(BASE, "reel.json"), encoding="utf-8"))
OUT = os.path.join(BASE, "reel")
VID = os.path.join(OUT, SPEC.get("이름", SET) + ".mp4")

PAL = {p["id"]: p for p in json.load(open(
    os.path.join(ROOT, "assets", "palettes", "color_combos.json"), encoding="utf-8"))["palettes"]}
TH = PAL[SPEC.get("판", "p_black_s")]["theme"]
BG, INK, ACC = TH["bg"], TH["ink"], TH["acc"]
SEC = float(SPEC["길이"]); NF = int(FPS * SEC)

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


def 행(id_, n, t, top):
    return (f'<div id="{id_}" class="an" style="position:absolute;left:0;top:{top}px;'
            f'display:flex;gap:26px;align-items:center;width:{CW}px">'
            f'<div style="flex:0 0 72px;height:72px;border-radius:999px;background:{ACC};color:{BG};'
            f'font-family:{K.D};font-weight:900;font-size:40px;display:flex;align-items:center;'
            f'justify-content:center">{n}</div>'
            f'<div data-fit=1 data-min="{BODY_MIN}" data-room="{CW-110}" style="font-family:{K.B};'
            f'font-weight:800;font-size:58px;color:{INK};white-space:nowrap">{t}</div></div>')


def 숫자(id_, 글, 단위, 크기, top):
    return (f'<div id="{id_}" class="an" style="position:absolute;left:0;top:{top}px;width:{CW}px;'
            f'font-family:{K.D};font-weight:900;font-size:{크기}px;line-height:1;color:{ACC};'
            f'white-space:nowrap"><span id="{id_}n">0</span>{단위}</div>')


def 단추(id_, 글, 크기, top):
    return (f'<div id="{id_}" class="an" style="position:absolute;left:0;top:{top}px">'
            f'<span data-fit=1 data-min="{LABEL_MIN}" data-room="{CW-120}" '
            f'style="display:inline-flex;align-items:center;background:{ACC};color:{BG};'
            f'border-radius:999px;padding:22px 52px;font-family:{K.B};font-weight:800;'
            f'font-size:{크기}px;line-height:1;white-space:nowrap">{글}</span></div>')


def 조각():
    """사양(reel.json)에서 장면 HTML 과 그리기 명령을 함께 만든다."""
    속, 명령, t0 = [], [], 0.0
    for si, sc in enumerate(SPEC["장면"], 1):
        안 = []
        for ei, e in enumerate(sc["요소"], 1):
            id_ = f"s{si}e{ei}"
            형, 글, 위 = e["형"], e.get("글", ""), e["위"]
            색 = ACC if e.get("색") == "acc" else INK
            if 형 == "배지":
                안.append(알약(id_, 글, e.get("크기", 44), 위, ACC, BG))
                명령.append(("pop" if e.get("튐") else "inn", id_, e["at"]))
            elif 형 in ("제목", "본문"):
                안.append(줄(id_, 글, e.get("크기", 110 if 형 == "제목" else 56), 색, 위,
                            "D" if 형 == "제목" else "B"))
                명령.append(("inn", id_, e["at"]))
            elif 형 == "행":
                안.append(행(id_, e["번호"], 글, 위))
                명령.append(("inn", id_, e["at"]))
            elif 형 == "숫자":
                안.append(숫자(id_, 글, e.get("단위", ""), e.get("크기", 230), 위))
                명령.append(("inn", id_, e["at"]))
                명령.append(("count", id_, e["at"] + 0.15, e["값"], e.get("셈", 1.9), e.get("소수", 0)))
            elif 형 == "단추":
                안.append(단추(id_, 글, e.get("크기", 54), 위))
                명령.append(("pop", id_, e["at"]))
        속.append(장면(si, t0, sc["끝"], "".join(안)))
        t0 = sc["끝"]
    return "".join(속), 명령


def html():
    body, _ = 조각()
    return (f'<html><head><meta charset="utf-8"><style>{K.css_inline("gm")}{BF.css("dark")}'
            f'.an{{opacity:0}}.sc{{display:none}}</style></head>'
            f'<body style="margin:0;width:{W}px;height:{H}px;position:relative;overflow:hidden;'
            f'background:{BG};word-break:keep-all">{body}{BF.html("reel", ai=False)}</body></html>')


def draw_js():
    _, 명령 = 조각()
    줄들 = []
    for m in 명령:
        if m[0] == "count":
            _, id_, at, 값, 셈, 소수 = m
            줄들.append(f"{{const q=clamp((t-{at})/{셈}); "
                       f"E('{id_}n').textContent=({값}*ease(q)).toFixed({소수});}}")
        else:
            줄들.append(f"{m[0]}('{m[1]}', {m[2]});")
    return """(t) => {
  const E = id => document.getElementById(id);
  const ease = x => 1 - Math.pow(1 - x, 3);
  const clamp = x => Math.max(0, Math.min(1, x));
  document.querySelectorAll('.sc').forEach(sc => {
    const a = +sc.dataset.a, b = +sc.dataset.b;
    sc.style.display = (t >= a && t < b) ? 'block' : 'none';
  });
  const inn = (id, t0) => { const e = E(id); if (!e) return;
    const k = ease(clamp((t - t0) / 0.45));
    e.style.opacity = k; e.style.transform = `translateY(${(1 - k) * 34}px)`; };
  const pop = (id, t0) => { const e = E(id); if (!e) return;
    const p = clamp((t - t0) / 0.5), k = ease(p);
    e.style.opacity = k; e.style.transform = `scale(${0.82 + 0.18 * k + 0.05 * Math.sin(Math.PI * p)})`;
    e.style.transformOrigin = 'left center'; };
""" + "\n  ".join(줄들) + "\n}"


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
        DJ = draw_js()
        for i in range(NF):
            await pg.evaluate(DJ, i / FPS)
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
    style = SPEC.get("음악", "경쾌 신스팝"); key = SPEC.get("조성", "D"); seed = SPEC.get("씨앗", 2610)
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
