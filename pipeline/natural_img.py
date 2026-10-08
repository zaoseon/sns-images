"""자연스러운 말투 적용 그림(대표 확인용, R23). 실제로 고친 문장을 전(×)과 후(○)로 보여 준다. 사용: python3 pipeline/natural_img.py -> 2026-motion/natural_01.png ~"""
import os, sys, asyncio
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
.row{{background:#161c33;border-radius:26px;padding:8px 32px 12px;margin-bottom:10px;font-size:41px;line-height:1.5}}
.row b{{color:{GOLD};font-family:{K.D};font-weight:900}}.row u{{text-decoration:none;color:{TEAL}}}.row s{{text-decoration:line-through;color:{CORAL}}}
</style><body>'''
def page(tag, title, rows, top=250): return BASE + f'<div class=k>{tag}</div><div class=t1>{title}</div><div style="position:absolute;left:60px;right:60px;top:{top}px">' + "".join(f'<div class=row>{r}</div>' for r in rows) + '</div><script>document.title=\'ok\'</script>'
def ba(before, after, tag=""): return (f'<b>{tag}</b><br>' if tag else '') + f'<s>{before}</s><br><u>{after}</u>'
S = [
 page("자연스러운 말투 · 1 / 4", "이렇게 바꿔요", ["<b>질문 끝은</b><br>~인가요? · ~나요? · ~까요? · ~뭔가요? · ~세요?", "<b>쓰지 않아요</b><br>~예요? · ~이에요? · ~어요? · ~해요?", "<b>호응을 맞춰요</b><br>사람을 계산하지 않고, 사주를 계산해요", "<b>AI 말투를 피해요</b><br>~에 대해 · 다양한 · 도움이 돼요 · 정말/매우"], 300),
 page("2 / 4", "질문을 자연스럽게", [ba("여러분은 무슨 띠예요?", "여러분은 무슨 띠인가요?"), ba("여러분은 몇 개 겹쳐요?", "여러분은 몇 개 겹치나요?"), ba("첫눈파예요, 스며듦파예요?", "첫눈파인가요, 스며듦파인가요?"), ba("나는 어느 쪽이에요?", "나는 어느 쪽인가요?"), ba("요즘 배우는 건 뭐예요?", "요즘 배우는 건 뭔가요?")], 232),
 page("3 / 4", "질문을 자연스럽게 (이어서)", [ba("최근에 운 적 있어요?", "최근에 운 적이 있나요?"), ba("연애할 때 먼저 식는 편이에요?", "연애할 때 먼저 식는 편인가요?"), ba("태어난 시간 알아요?", "태어난 시간을 아시나요?"), ba("주말 밤 뭐 해요?", "주말 밤에는 뭘 하나요?"), ba("왜 사람마다 다르게 느껴져요?", "왜 사람마다 다르게 느껴질까요?")], 232),
 page("4 / 4", "호응과 번역투 고치기", [ba("무작위 3,000명을 계산했어요", "무작위 3,000명의 사주를 계산했어요", "호응"), ba("공통점에 대해 여러 풀이로 읽어 봤어요", "공통점을 여러 풀이로 읽어 봤어요", "번역투"), ba("하루만 묵혀 보는 습관이 도움이 돼요", "하루만 묵혀 보면 한결 나아요", "AI 말투"), ba("사람을 모으는 다양한 방식이 있어요", "사람을 모으는 방식이 여러 가지 있어요", "AI 말투")], 232),
]
async def main():
    bad = 0
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 1080, "height": 1350})
        for n, h in enumerate(S, 1):
            open("/tmp/nt.html", "w", encoding="utf-8").write(h); await pg.goto("file:///tmp/nt.html"); await pg.wait_for_function("document.title=='ok'"); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(250)
            for x in await check_page(pg, f"nt{n:02d}", "cover"): print("검사:", x); bad += 1
            await pg.screenshot(path=os.path.join(R, "2026-motion", f"natural_{n:02d}.png"))
        await b.close()
    print("검사 문제", bad, "건,", len(S), "장")
asyncio.run(main())
