import sys, subprocess, os
from playwright.sync_api import sync_playwright
src, out, dur = sys.argv[1], sys.argv[2], float(sys.argv[3]); fps=30
fr=os.path.join(os.path.dirname(out),'fr'); os.makedirs(fr,exist_ok=True)
with sync_playwright() as p:
    b=p.chromium.launch(args=["--allow-file-access-from-files"]); pg=b.new_page(viewport={"width":1080,"height":1920})
    pg.goto("file://"+os.path.abspath(src)); pg.wait_for_timeout(800)
    n=int(dur*fps)
    for i in range(n):
        pg.evaluate(f"seek({i/fps})"); pg.screenshot(path=f"{fr}/{i:04d}.jpg",type="jpeg",quality=92)
    b.close()
subprocess.run(["ffmpeg","-y","-loglevel","error","-framerate",str(fps),"-i",f"{fr}/%04d.jpg","-c:v","libx264","-preset","veryfast","-crf","20","-pix_fmt","yuv420p",out],check=True)
