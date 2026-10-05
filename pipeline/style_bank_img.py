"""외부 가이드(모션그래픽 스타일 30)에서 자오선에 맞는 12가지를 골라 정리한 그림(결정 요청). 큰 글씨·굵게, style_spec 자동 검사.
사용: python3 pipeline/style_bank_img.py -> 2026-motion/styles_01.png ~ 06.png"""
import os, sys, asyncio
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from style_spec import check_page
import fonts_kit as K
from playwright.async_api import async_playwright
R = os.path.join(HERE, "..")
GOLD = "#e7c88d"; TEAL = "#7fd6c8"; CORAL = "#ff8a73"; BLUE = "#8fb7ff"
PIL = {"교차 데이터": TEAL, "연애·관계": CORAL, "시기·숫자": BLUE, "소개·상품": GOLD}
ST = [("30", "리소그래프", "교차 데이터", "사주=핑크, 별자리=블루. 겹친 곳이 보라(같은 말)"),
      ("27", "스크램블 해독", "교차 데이터", "여섯 운명학 글자가 해독되며 같은 말로 고정"),
      ("05", "벤토 그리드", "교차 데이터", "여섯 운명학 6칸이 하나씩 튀어 들어와 한 화면에"),
      ("21", "픽셀 게임", "연애·관계", "번호를 고를 때마다 CLEAR!와 코인 +1"),
      ("18", "만화 컷", "연애·관계", "고민 한 칸, 정월 답 한 칸, 말풍선과 효과음"),
      ("16", "네온사인", "연애·관계", "밤 9시 테스트 코너 오프닝, 네온이 깜빡이다 켜짐"),
      ("28", "롤링 실린더", "시기·숫자", "12개월 운이 전광판처럼 차르륵 넘어감"),
      ("17", "LED 전광판", "시기·숫자", "오늘의 기운 한 줄이 점 전광판에 흐름"),
      ("25", "3D 입체 글자", "시기·숫자", "2027 숫자가 돌며 날아와 정면에 멈춤"),
      ("14", "지하철 노선도", "소개·상품", "10년 대운을 역 하나씩, 지금 내 역에 불"),
      ("19", "탑승권", "소개·상품", "2027 정미년행 탑승권에 12개월이 찍힘"),
      ("20", "붓글씨와 낙관", "소개·상품", "먹 글씨가 드러나고 붉은 낙관이 쿵")]
BASE = f'''<!doctype html><meta charset=utf-8><style>{K.css('gm')}
html,body{{margin:0;width:1080px;height:1350px;background:#0b1020;color:#fff;font-family:{K.B};font-weight:800;word-break:keep-all;line-break:strict;overflow:hidden;position:relative}}
.k{{position:absolute;left:60px;top:50px;font-size:46px;font-weight:900;font-family:{K.D};color:{GOLD}}}
.t1{{position:absolute;left:60px;top:120px;font-size:80px;font-weight:900;font-family:{K.D};line-height:1.4}}
.card{{position:absolute;left:60px;right:60px;background:#161c33;border-radius:34px;padding:26px 44px 30px}}
.hd{{display:flex;align-items:center;gap:24px;margin-bottom:8px}}.no{{flex:none;width:84px;height:84px;border-radius:50%;background:{GOLD};color:#111;font-size:44px;font-weight:900;font-family:{K.D};display:flex;align-items:center;justify-content:center}}
.nm{{font-size:58px;font-weight:900;font-family:{K.D};line-height:1.3;flex:1}}.chip{{flex:none;font-size:42px;font-weight:900;color:#111;padding:6px 24px;border-radius:40px}}
.vl{{font-size:48px;font-weight:800;line-height:1.55;margin-top:6px}}
.row{{background:#161c33;border-radius:30px;padding:22px 40px 26px;margin-bottom:22px}}.info{{position:absolute;left:60px;right:60px}}.lb{{font-size:40px;font-weight:900;margin-top:0}}.row .vl{{font-size:50px;margin-top:6px}}
</style><body>'''
def card(s, top):
    n, nm, pl, tx = s
    return f'<div class=card style="top:{top}px"><div class=hd><div class=no>{n}</div><div class=nm>{nm}</div><div class=chip style="background:{PIL[pl]}">{pl}</div></div><div class=vl>{tx}</div></div>'
def trio(i, tag): return BASE + f'<div class=k>{tag}</div>' + card(ST[i], 120) + card(ST[i + 1], 480) + card(ST[i + 2], 840) + "<script>document.title='ok'</script>"
S1 = BASE + f'''<div class=k>스타일 후보 · 결정 요청</div><div class=t1>같은 내용을<br>스타일만 바꿔서</div><div class=info style="top:400px">
<div class=row><div class=lb style="color:{GOLD}">외부 가이드</div><div class=vl>같은 안내를 스타일 30가지로 만든 자료예요</div></div>
<div class=row><div class=lb style="color:{CORAL}">조심할 점</div><div class=vl>색·글꼴만 바꾸면 같은 영상이 돼요. 장면 구성부터 새로 짜야 해요</div></div>
<div class=row><div class=lb style="color:{CORAL}">우리 사례</div><div class=vl>키네틱 2편은 색과 문구만 바꾼 같은 영상이었어요</div></div>
<div class=row style="margin-bottom:0"><div class=lb style="color:{TEAL}">다음 장</div><div class=vl>자오선에 맞는 12가지를 골랐어요</div></div></div><script>document.title='ok'</script>'''
S6 = BASE + f'''<div class=k>결정 요청 · 마지막</div><div class=t1 style="top:110px">대표님께<br>질문 3개</div><div class=info style="top:400px">
<div class=row><div class=vl>① 먼저 스토리보드로 만들 3가지는? (제안: 30 리소그래프 · 14 노선도 · 19 탑승권)</div></div>
<div class=row><div class=vl>② 색만 바꾼 키네틱 2번째 편은 쓰지 않을까요?</div></div>
<div class=row><div class=vl>③ 신년 감정서 안내를 탑승권 스타일로 해도 될까요?</div></div>
<div class=row style="background:{GOLD};color:#111;margin-bottom:0"><div class=vl style="font-weight:900">번호와 답만 알려 주세요</div></div></div><script>document.title='ok'</script>'''
async def main():
    slides = [S1, trio(0, "교차 데이터에 어울리는 것"), trio(3, "연애·관계에 어울리는 것"), trio(6, "시기·숫자에 어울리는 것"), trio(9, "소개·상품에 어울리는 것"), S6]; bad = 0
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 1080, "height": 1350})
        for n, h in enumerate(slides, 1):
            open("/tmp/sty.html", "w", encoding="utf-8").write(h); await pg.goto("file:///tmp/sty.html"); await pg.wait_for_function("document.title=='ok'"); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(250)
            for x in await check_page(pg, f"styles{n:02d}", "cover"): print("검사:", x); bad += 1
            await pg.screenshot(path=os.path.join(R, "2026-motion", f"styles_{n:02d}.png"))
        await b.close()
    print("검사 문제", bad, "건,", len(slides), "장")
asyncio.run(main())
