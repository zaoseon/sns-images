"""HTML 모션그래픽 렌더러(10/5 대표 자료: 클로드가 HTML 한 장으로 만든 화면을 녹화해 영상으로 쓴다).
- 움직임은 HTML 안의 seek(ms) 함수 하나로 계산한다(시간 -> 모든 요소의 위치·크기). 그래서 프레임을 정확히 찍을 수 있고 음악 박자에 맞출 수 있다.
- 박자(BEAT)를 HTML에 넘겨서 글자와 도형이 박자마다 튀어나오게 한다. 음악은 music_plan으로 같은 템포로 만든다.
- 사용: render_html(html_path, out_mp4, seconds, fps=30)  /  API 호출·외부 서비스 없음(내 컴퓨터에서 계산만)."""
import os, subprocess, asyncio
from playwright.async_api import async_playwright
async def _render(html_path, out_mp4, seconds, fps, w, h):
    n = int(round(seconds * fps))
    pr = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(fps), "-c:v", "mjpeg", "-i", "-", "-vf", "scale=in_range=full:out_range=tv:out_color_matrix=bt709,format=yuv420p", "-c:v", "libx264", "-profile:v", "high", "-crf", "14", "-preset", "medium", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-an", "-movflags", "+faststart", out_mp4], stdin=subprocess.PIPE)
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": w, "height": h})
        await pg.goto("file://" + os.path.abspath(html_path)); await pg.wait_for_timeout(600)
        await pg.evaluate("document.fonts.ready")
        for i in range(n):
            await pg.evaluate(f"seek({i * 1000.0 / fps})")
            pr.stdin.write(await pg.screenshot(type="jpeg", quality=95))
        await b.close()
    pr.stdin.close(); pr.wait(); return n / fps
def render_html(html_path, out_mp4, seconds, fps=30, w=1080, h=1920):
    os.makedirs(os.path.dirname(os.path.abspath(out_mp4)), exist_ok=True); return asyncio.run(_render(html_path, out_mp4, seconds, fps, w, h))
