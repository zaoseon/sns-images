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
CL = [f"sopclip-n{n}" for n in range(34, 47)]; DR = ["data-vs14", "data-pair", "data-star", "data-ziwei", "data-dang", "data-liuyao", "data-harak", "data-alone", "data-four"]
OT = ["tri-vs", "tri-first", "tri-talk", "gab-ig", "eul-ig", "new-sky-2027", "clip-s10-video"]
S = [
 page("트렌디 표현 적용안 · 1 / 8", "○○코어, 이렇게 써요", ["<b>쓰는 곳</b><br>표지 · 캡션 첫 줄 · 해시태그 (영상 하나에 하나)", "<b>형태</b><br>소재+코어 (예: 일요일 밤 생각코어, 제철코어, 갑목코어)", "<b>쓰지 않는 곳</b><br>풀이·설명 본문 · 면책 · 마음이 무거운 소재(가면 등)", "<b>지켜요</b><br>존댓말 유지 · 비하·장애 표현 금지 · 한 달마다 점검"], 330),
 page("2 / 8", "글 연결 클립 ① 새 캡션 첫 줄", [row(i) for i in CL[:5]], 232),
 page("3 / 8", "글 연결 클립 ② 새 캡션 첫 줄", [row(i) for i in CL[5:9]], 232),
 page("4 / 8", "글 연결 클립 ③ 새 캡션 첫 줄", [row(i) for i in CL[9:]], 232),
 page("5 / 8", "데이터 릴스 ① 새 캡션 첫 줄", [row(i) for i in DR[:4]], 232),
 page("6 / 8", "데이터 릴스 ② 새 캡션 첫 줄", [row(i) for i in DR[4:]], 232),
 page("7 / 8", "그 밖의 영상 새 캡션 첫 줄", [row(i) for i in OT[:4]], 232),
 page("8 / 8", "그 밖의 영상 새 캡션 첫 줄(이어서)", [row(i) for i in OT[4:]], 232),
]
async def main():
    bad = 0
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 1080, "height": 1350})
        for n, h in enumerate(S, 1):
            open("/tmp/ty.html", "w", encoding="utf-8").write(h); await pg.goto("file:///tmp/ty.html"); await pg.wait_for_function("document.title=='ok'"); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(250)
            for x in await check_page(pg, f"ty{n:02d}", "cover"): print("검사:", x); bad += 1
            await pg.screenshot(path=os.path.join(R, "2026-motion", f"trendy_{n:02d}.png"))
        await b.close()
    print("검사 문제", bad, "건,", len(S), "장")
asyncio.run(main())
