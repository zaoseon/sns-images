"""HTML 모션을 MP4 로 뽑는다 — 대표 10/16 오AI완 '클로드 모션그래픽 키트' 벤치마크.

가져온 것
  **모션을 HTML/CSS/JS 로 만든다.** 지금 우리 릴스는 PIL 로 그려서 글자가 떠오르는 정도밖에 못 한다.
  CSS 는 수십 개가 동시에 움직이고, 숫자가 올라가고, 선이 그려지는 것을 쉽게 한다 —
  K-073 2단('숫자·표가 쌓이는 과정')이 바로 그것이다.

**안 가져온 것 둘**
  ① 원문 프롬프트("showreel for a résumé. go all out")는 모션 디자이너 과시용이다.
     K-073 은 "움직임은 정보를 나르거나 스크롤을 멈출 때만 쓴다" 이다. 화려하기만 한 영상은 안 만든다.
  ② **화면 녹화로 뽑는 방법**(Cmd+Shift+5 · Xbox Game Bar). 사람이 15초를 손으로 녹화하고 잘라야 한다 —
     노가다이고, 길이·fps·규격이 매번 다르고, 화질도 떨어진다.
     우리는 Playwright 헤드리스 크로미움이 이미 있다. **프레임을 한 장씩 찍어 붙인다** —
     사람 손이 안 들어가고 길이·fps·크기가 정확하다.

HTML 쪽 약속 하나
  페이지가 `window.seek(t)` 를 내놔야 한다(t = 초). 렌더러가 프레임마다 이것을 불러 시각을 맞춘다.
  CSS 애니메이션을 시간에 맡기지 않고 우리가 시각을 지정하므로 **몇 번을 돌려도 같은 영상**이 나온다
  (화면 녹화는 그때그때 다르다).

사용: python3 pipeline/html_motion.py 파일.html 나갈이름 [--초 15] [--fps 30]
결과: 2026-motion/html/<나갈이름>.mp4
"""
import os, sys, json, shutil, asyncio, subprocess, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
import channel_specs as CS

CH = CS.CH["reel"]
OUT = os.path.join(ROOT, "2026-motion", "html")


async def _shoot(html, 초, fps, w, h, tmp, 한계, 구역):
    from playwright.async_api import async_playwright
    n = int(round(초 * fps))
    async with async_playwright() as pw:
        b = await pw.chromium.launch(args=["--force-color-profile=srgb", "--disable-lcd-text"])
        pg = await b.new_page(viewport={"width": w, "height": h}, device_scale_factor=1)
        await pg.goto("file://" + os.path.abspath(html))
        await pg.wait_for_function("typeof window.seek === 'function'", timeout=15000)
        # 글이 아래 고정 줄을 넘는지 **브라우저로 재서** 막는다.
        # 눈대중으로 여백을 맞추다 두 번 겹쳤다(10/16). 끝 시각에서 제일 아래 글의 바닥을 잰다.
        await pg.evaluate("t => window.seek(t)", 초 - 0.01)
        바닥 = await pg.evaluate("""() => {
          const els = [...document.querySelectorAll('.safe *')].filter(e => e.offsetHeight);
          return els.length ? Math.max(...els.map(e => e.getBoundingClientRect().bottom)) : 0; }""")
        if 바닥 > 한계:
            await b.close()
            raise SystemExit(f"[막음] 글이 아래 고정 줄을 넘어요 — 맨 아래 글 바닥 {바닥:.0f}px, "
                             f"넘으면 안 되는 선 {한계}px (하단 고정 줄 위 24px). "
                             f"{바닥 - 한계:.0f}px 줄이세요.")
        # 구역을 넘는지도 잰다. 아래 고정 줄만 보면 **구역끼리 겹치는 것**을 놓친다 —
        # 10/16 막대 세 줄이 '본문·그림' 구역을 166px 넘어 AI 고지 위로 올라갔는데 통과했다.
        if 구역:
            # 바깥 상자만 재면 안 된다 — 자식이 넘쳐도 부모 rect 는 그대로라서 놓친다(10/16).
            # 상자와 **그 안 모든 자손**의 바닥 중 제일 아래를 쓴다.
            잰것 = await pg.evaluate("""() => [...document.querySelectorAll('.mk[data-z]')]
              .map(e => {
                const all = [e, ...e.querySelectorAll('*')].filter(x => x.offsetHeight);
                return [e.dataset.z, all.length ? Math.max(...all.map(x => x.getBoundingClientRect().bottom)) : 0];
              }).filter(r => r[1] > 0)""")
            넘침 = [(z, b_, 구역[z]) for z, b_ in 잰것 if z in 구역 and b_ > 구역[z] + 1]
            if 넘침:
                await b.close()
                raise SystemExit("[막음] 구역을 넘었어요 — " + " / ".join(
                    f"'{z}' 바닥 {b_:.0f}px, 구역 끝 {끝}px ({b_ - 끝:.0f}px 넘침)"
                    for z, b_, 끝 in 넘침) + ". 글을 줄이거나 더 넓은 구역('마무리 카드')으로 옮기세요.")
        for i in range(n):
            await pg.evaluate("t => window.seek(t)", i / fps)
            await pg.screenshot(path=os.path.join(tmp, f"f{i:05d}.png"))
        await b.close()
    return n


def render(html, 이름, 초=15.0, fps=30, ch="reel"):
    C = CS.CH[ch]
    w, h = C["w"], C["h"]            # 크기는 channel_specs 에서 — 여기 숫자를 박지 않는다
    os.makedirs(OUT, exist_ok=True)
    tmp = tempfile.mkdtemp(prefix="htmlmo_")
    try:
        구역 = {z[0]: z[4] for z in C["zones"]}          # 구역 이름 → 아래 끝 y
        고정top = {z[0]: z[2] for z in C["zones"]}.get("하단 고정", h - 495)
        # 넘으면 안 되는 선은 **하단 고정 구역이 시작하는 자리**다. 전에는 brand_frame 의
        # bottom(=zaoseon.com 글자 줄, y1465)을 썼는데 고지 칸은 y1425 에서 시작해
        # 1441 까지 글이 내려와도 통과했다 — 실제로는 이미 겹친 상태였다(10/16).
        한계 = 고정top - 24
        n = asyncio.run(_shoot(html, 초, fps, w, h, tmp, 한계, 구역))
        out = os.path.join(OUT, 이름 + ".mp4")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(fps),
                        "-i", os.path.join(tmp, "f%05d.png"),
                        "-vf", "format=yuv420p", "-c:v", "libx264", "-profile:v", "high",
                        "-crf", "16", "-preset", "medium",
                        "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
                        "-movflags", "+faststart", out], check=True)
        return out, n / fps
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main():
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    if len(a) < 2:
        print(__doc__); return 1
    초 = float(next((x.split("=")[1] for x in sys.argv if x.startswith("--초=")), 15))
    fps = int(next((x.split("=")[1] for x in sys.argv if x.startswith("--fps=")), 30))
    p, d = render(a[0], a[1], 초, fps)
    print(f"  {os.path.relpath(p, ROOT)} · {d:.1f}초 · {fps}fps · {CH['w']}x{CH['h']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
