"""병(丙) 릴스 재제작 - 대표 병 샘플(샘플1~7) 문구 그대로, 정 샘플 레이아웃으로 만든 10초 릴스. 출력 2026-w40car3-reel/2026-10-01-byeong.mp4"""
import os, sys, io, base64, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import carousel_editor as CE
from playwright.sync_api import sync_playwright
from PIL import Image
D = dict(dayChar="병", hanja="丙", accent="#e65c3c", face="v1_lowbun", kicker="오늘의 성격 카드", coverTitle="좋으면 티 나고\n식어도 티 나는 사람", coverSub="태어난 날 첫 글자가 병(丙)이라면",
    personality=["감정 표현이\n가장 빠른 타입", "태양처럼 밝은 기운이라,\n좋고 싫음이 얼굴에 바로 드러나요.\n숨기는 걸 오래 못 하는 편이에요."],
    love=["좋을 땐\n화끈하게 다가가요", "표현이 직접적이라\n상대가 마음을 바로 알아차려요.\n밀당엔 약한 편, 그게 매력이기도 해요."],
    money=["기분 좋은 날\n씀씀이가 커져요", "에너지가 넘치는 날 지갑도 쉽게 열려요.\n큰 소비 전엔 하루만 더 생각해보세요."],
    advice=["표현은 무기,\n속도만 조절하면 돼요", "다 보여주는 게 나쁜 게 아니에요.\n타이밍만 살짝 늦추면\n관계가 더 편해져요."], chartNote="불이 강해서 표현이 빠르고 에너지가 겉으로 드러나요",
    values=[.35, 1.0, .45, .3, .4], highlight=1, ctaQ="주변에 *병화* 같은\n사람이 있나요?", nextTitle="정(丁)일생 편")
OV = dict(nextBadge="내일 낮 12시", nextTitle="정(丁)일생 편")
CE.build_html()
if not os.path.exists(CE.PLATE): CE.make_plate()
fr = []
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1300, "height": 900}); pg.goto("file:///tmp/editor_noto.html"); pg.wait_for_timeout(1500)
    pg.evaluate("Promise.all([400,500,600,700,900].map(w=>document.fonts.load(w+' 40px \"Noto Sans CJK KR\"','가한丁')))")
    pg.evaluate("async ([k,u])=>{FACES[k]=u; const im=new Image(); im.src=u; await im.decode(); imgCache[k]=im;}", ["chart_plate", "data:image/png;base64," + base64.b64encode(open(CE.PLATE, "rb").read()).decode()])
    pg.evaluate(CE.LAYOUT_JS, [D, None]); pg.evaluate(CE.OVERRIDE_JS, OV); pg.wait_for_timeout(150)
    for i in (0, 1, 2, 3, 6):
        url = pg.evaluate(f"(()=>{{active={i}; draw(false); return cv.toDataURL('image/png');}})()")
        im = Image.open(io.BytesIO(base64.b64decode(url.split(",")[1]))).convert("RGB")
        c = Image.new("RGB", (CE.REEL_W, CE.REEL_H), im.getpixel((5, 5))); c.paste(im, (0, CE.REEL_TOP)); fp = f"/tmp/byeong_reel_{i}.png"; c.save(fp); fr.append(fp)
    b.close()
out = os.path.join(CE.ROOT, "2026-w40car3-reel", "2026-10-01-byeong.mp4")
cmd = ["ffmpeg", "-y", "-loglevel", "error"]
for f, t in zip(fr, CE.REEL_DUR): cmd += ["-loop", "1", "-t", str(t), "-i", f]
total = sum(CE.REEL_DUR) - CE.REEL_FADE * (len(fr) - 1)
cmd += ["-f", "lavfi", "-t", f"{total:.2f}", "-i", "anullsrc=r=44100:cl=stereo"]
fl = ""; prev = "[0:v]"; acc = CE.REEL_DUR[0]
for k in range(1, len(fr)):
    fl += f"{prev}[{k}:v]xfade=transition=fade:duration={CE.REEL_FADE}:offset={acc - CE.REEL_FADE * k:.2f}[x{k}];"; prev = f"[x{k}]"; acc += CE.REEL_DUR[k]
fl += f"{prev}format=yuv420p,fps=30[vout]"
cmd += ["-filter_complex", fl, "-map", "[vout]", "-map", f"{len(fr)}:a", "-c:v", "libx264", "-crf", "20", "-c:a", "aac", "-b:a", "96k", "-shortest", "-movflags", "+faststart", out]
subprocess.run(cmd, check=True); print("ok", out)
