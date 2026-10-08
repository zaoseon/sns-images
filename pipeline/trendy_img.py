"""트렌디 표현(○○코어) 적용안 그림(대표 확인용, R23). 영상 이름 옆에 새 캡션 첫 줄을 보여 준다. 사용: python3 pipeline/trendy_img.py -> 2026-motion/trendy_01.png ~"""
import os, sys, json, asyncio
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from style_spec import check_page
import fonts_kit as K
from playwright.async_api import async_playwright
R = os.path.abspath(os.path.join(HERE, ".."))
GOLD = "#e7c88d"; TEAL = "#7fd6c8"; CORAL = "#ff8a73"
BASE = f'''<!doctype html><meta charset=utf-8><style>{K.css('gm')}
html,body{{margin:0;width:1080px;height:1350px;background:#0b1020;color:#fff;font-family:{K.B};font-weight:800;word-break:keep-all;line-break:strict;overflow:hidden;position:relative}}
.k{{position:absolute;left:60px;top:48px;font-size:44px;font-weight:900;font-family:{K.D};color:{GOLD}}}
.t1{{position:absolute;left:60px;top:112px;font-size:64px;font-weight:900;font-family:{K.D};line-height:1.3}}
.row{{background:#161c33;border-radius:26px;padding:6px 32px 10px;margin-bottom:8px;font-size:41px;line-height:1.5}}
.row b{{color:{GOLD};font-family:{K.D};font-weight:900}}.row u{{text-decoration:none;color:{TEAL}}}.row s{{text-decoration:none;color:{CORAL}}}.row i{{font-style:normal;color:#aab3cf;font-weight:800}}
</style><body>'''
def page(tag, title, rows, top=250): return BASE + f'<div class=k>{tag}</div><div class=t1>{title}</div><div style="position:absolute;left:60px;right:60px;top:{top}px">' + "".join(f'<div class=row>{r}</div>' for r in rows) + '</div><script>document.title=\'ok\'</script>'
T = json.load(open(os.path.join(R, "content", "trendy_lines.json"), encoding="utf-8"))
def row(i):
    t = T[i]
    return f'<b>{t["name"]}</b><br>' + (f'<u>{t["opener"]}</u>' if t["opener"] else '<i>코어 표현 없음 · 마음이 무거운 소재라 뺐어요</i>')
def row2(i):
    t = T[i]; return f'<b>{t["name"]}</b><br><u>{t["opener"]}</u>'
USED = [k for k, v in T.items() if v["opener"]]
S = [
 page("트렌디 표현 사용 규칙 · 1 / 5", "쓰는 순서", ["<b>① 매달 찾아요</b><br>신조어 테스트·요즘 뜨는 밈·기사를 검색해 목록을 새로 만들어요", "<b>② 세 가지로 걸러요</b><br>실제로 쓰는지 · 아직 인기인지 · 위험은 없는지(비하·논란)", "<b>③ 맥락을 봐요</b><br>영상 소재와 뜻이 맞을 때만 써요. 안 맞으면 평이한 말이 더 나아요", "<b>④ 섞어 써요</b><br>한 영상에 하나 · 이웃한 영상 연속 금지 · 한 주 영상의 40% 이하"], 300),
 page("2 / 5", "표지 제목·훅에 쓸 때", ["<b>큰 제목은 평이한 문장</b><br>트렌디 표현은 작은 글(키커)이나 부제에 둬요", "<b>뜻이 한눈에 보일 때만</b><br>설명이 필요한 신조어는 캡션 첫 줄에서 풀어 줘요", "<b>훅 첫 2초에는 하나만</b><br>신조어를 겹쳐 쓰지 않아요", "<b>유행어가 주인공이 되면 안 돼요</b><br>풀이 내용이 먼저 읽히게 해요"], 300),
 None,
 page("4 / 5", "이번 달 쓰는 표현 (32개 중 7개)", [row2(i) for i in USED[:4]], 232),
 page("5 / 5", "이번 달 쓰는 표현 (이어서)", [row2(i) for i in USED[4:]] + ["<b>나머지 25개</b><br><i>맥락에 안 맞거나 같은 말 반복이라 평이한 말로 둬요</i>"], 232),
]
async def main():
    bad = 0
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 1080, "height": 1350})
        for n, h in enumerate(S, 1):
            if h is None: continue
            open("/tmp/ty.html", "w", encoding="utf-8").write(h); await pg.goto("file:///tmp/ty.html"); await pg.wait_for_function("document.title=='ok'"); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(250)
            for x in await check_page(pg, f"ty{n:02d}", "cover"): print("검사:", x); bad += 1
            await pg.screenshot(path=os.path.join(R, "2026-motion", f"trendy_{n:02d}.png"))
        await b.close()
    print("검사 문제", bad, "건,", len(S), "장")
asyncio.run(main())
# ---- 3번 장: 나쁜 예 / 좋은 예 (표지·훅 큰 제목) ----
def pair_slide():
    sys.path.insert(0, os.path.join(R, "content"))
    from PIL import Image, ImageDraw, ImageFont
    import clip_motion as M, pilot_variety as PV
    PV.AUDIT = True; M.BRAND = True
    def scene(kick, title, ksize=50, tsize=100, kcol=None):
        def f(c):
            y = 760
            if kick: PV.fx_slide(c, kick, y, 0, ksize, kcol or PV.GOLD, dirn=-1); y += 78
            PV.fx_wipe(c, title, y, 0, tsize, PV.WHITE, maxw=840, lh=1.28)
        return [(2.4, f)]
    bad = scene("", "도파민 폭발 갑목코어\n찐 레전드 갓생", tsize=84); good = scene("갑목코어 · 큰 나무 감성", "곧게 뻗어\n굽히기 싫은 사람")
    M.still(bad, 0, 2.0, "/tmp/tb.png"); M.still(good, 0, 2.0, "/tmp/tg.png")
    FD = ImageFont.truetype(K.P["gm_bold"], 54); F = ImageFont.truetype(K.P["pr_xb"], 40); FT = ImageFont.truetype(K.P["gm_bold"], 40); FH = ImageFont.truetype(K.P["gm_bold"], 64)
    c = Image.new("RGB", (1080, 1350), (11, 16, 32)); d = ImageDraw.Draw(c); d.text((60, 44), "3 / 5", font=FT, fill=(231, 200, 141)); d.text((60, 104), "큰 제목은 평이하게", font=FH, fill=(255, 255, 255))
    for x0, path, col, lab, note in ((60, "/tmp/tb.png", (255, 107, 90), "× 우르르", "신조어를 겹쳐 쓰면\\n무슨 말인지 안 보여요"), (560, "/tmp/tg.png", (110, 220, 190), "○ 섞어서", "큰 제목은 평이하게,\\n트렌디 표현은 작은 글에")):
        im = Image.open(path).convert("RGB").resize((460, 818)); c.paste(im, (x0, 250)); d.rounded_rectangle((x0 - 4, 246, x0 + 464, 1072), radius=8, outline=col, width=6); d.text((x0, 1098), lab, font=FD, fill=col)
        for i, ln in enumerate(note.replace("\\\\n", "\\n").split("\\n")): d.text((x0, 1166 + i * 52), ln, font=F, fill=(255, 255, 255))
    c.save(os.path.join(R, "2026-motion", "trendy_03.png")); print("3번 장(나쁜 예·좋은 예) 저장")
if __name__ == "__main__": pair_slide()
