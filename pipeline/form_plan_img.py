"""영상 형태 8가지를 자오선에 맞춰 정리한 그림(결정 요청). 큰 글씨·굵게·넉넉한 간격, 만든 뒤 style_spec 자동 검사.
사용: python3 pipeline/form_plan_img.py -> 2026-motion/form_01.png ~ 07.png"""
import os, sys, asyncio
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from style_spec import check_page
import fonts_kit as K
from playwright.async_api import async_playwright
R = os.path.join(HERE, "..")
GOLD = "#e7c88d"; TEAL = "#7fd6c8"; CORAL = "#ff8a73"; GRAY = "#9aa0bd"
ST = {"주력": GOLD, "보조": TEAL, "조건부": CORAL, "보류": GRAY}
TYPES = [("04", "키네틱 타이포", "주력", "장면 한 줄 자가진단 · 첫 편 완성", '키네틱 타이포로 "읽고도 답장 못 한 날". 핵심어만 강조색으로.'),
         ("05", "인포그래픽", "주력", "교차 데이터를 숫자로 · 100명 점 격자, 별자리 막대", "인포그래픽으로 이 숫자 3개. 0부터 감속하며 카운트업."),
         ("03", "쇼릴", "주력", "정월 소개 영상 · 프로필 맨 위 고정 게시물", '쇼릴로 "정월이 보는 여섯 가지"를 15초에. 챕터마다 배경색.'),
         ("06", "파티클·제너러티브", "보조", "6체계 차트가 모이는 순간 · 스토리보드 승인 대기", "파티클 배경으로 6체계 차트를. 금빛 입자 120~200개."),
         ("02", "제품 데모", "보조", '무료 풀이 "생일 넣으면 1초" 시연', "제품 데모로 무료 풀이를. 커서가 3단계를 차례로 누르게."),
         ("07", "원테이크 모핑", "보조", "사주 명식 → 별자리 → 숫자로 모양이 바뀜", "원테이크 모핑으로 명식에서 숫자까지 컷 없이 이어지게."),
         ("08", "캐릭터 애니", "조건부", "정월은 사진이라 눈 깜빡임·말풍선만 가능", "2D 마스코트를 새로 만들면 팔·표정 연기도 가능."),
         ("01", "런칭 필름", "보류", "신년 감정서 판매를 시작할 때 한 편", "광고 느낌 지적 때문에 지금은 만들지 않아요.")]
BASE = f'''<!doctype html><meta charset=utf-8><style>{K.css('gm')}
html,body{{margin:0;width:1080px;height:1350px;background:#0b1020;color:#fff;font-family:{K.B};font-weight:800;word-break:keep-all;line-break:strict;overflow:hidden;position:relative}}
.k{{font-family:{K.D};position:absolute;left:60px;top:50px;font-size:46px;font-weight:900;color:{GOLD}}}
.card{{position:absolute;left:60px;right:60px;background:#161c33;border-radius:34px;padding:30px 44px 34px}}
.hd{{display:flex;align-items:center;gap:26px;margin-bottom:12px}}.no{{font-family:{K.D};flex:none;width:92px;height:92px;border-radius:50%;background:{GOLD};color:#111;font-size:50px;font-weight:900;display:flex;align-items:center;justify-content:center}}
.nm{{font-family:{K.D};font-size:62px;font-weight:900;line-height:1.3;flex:1}}.chip{{font-family:{K.D};flex:none;font-size:44px;font-weight:900;color:#111;padding:6px 26px;border-radius:40px}}
.lb{{font-size:40px;font-weight:900;margin-top:12px}}.vl{{font-size:48px;font-weight:800;line-height:1.55;margin-top:2px}}
.t1{{font-family:{K.D};position:absolute;left:60px;top:130px;font-size:80px;font-weight:900;line-height:1.4}}
.row{{background:#161c33;border-radius:30px;padding:22px 40px 26px;margin-bottom:22px}}.info{{position:absolute;left:60px;right:60px}}
</style><body>'''
def card(t, top):
    n, name, st, use, ask = t
    return f'<div class=card style="top:{top}px"><div class=hd><div class=no>{n}</div><div class=nm>{name}</div><div class=chip style="background:{ST[st]}">{st}</div></div><div class=lb style="color:{GOLD}">우리 쓰임</div><div class=vl>{use}</div><div class=lb style="color:{TEAL}">시키는 말</div><div class=vl>{ask}</div></div>'
def pair(i, tag):
    a, b = TYPES[i], TYPES[i + 1]
    return BASE + f'<div class=k>{tag}</div>' + card(a, 130) + card(b, 720) + "<script>document.title='ok'</script>"
S1 = BASE + f'''<div class=k>영상 형태 정리 · 결정 요청</div><div class=t1>8가지 중<br>우리가 만들 순서</div><div class=info style="top:430px">
<div class=row><div class=lb style="color:{GOLD};margin-top:0">주력 (먼저 시작)</div><div class=vl>키네틱 타이포 · 인포그래픽 · 쇼릴</div></div>
<div class=row><div class=lb style="color:{TEAL};margin-top:0">보조 (그다음)</div><div class=vl>파티클 · 제품 데모 · 원테이크 모핑</div></div>
<div class=row><div class=lb style="color:{CORAL};margin-top:0">조건부</div><div class=vl>캐릭터 애니 (마스코트를 새로 만들면)</div></div>
<div class=row><div class=lb style="color:{GRAY};margin-top:0">보류</div><div class=vl>런칭 필름 (신년 감정서 판매 때)</div></div></div><script>document.title='ok'</script>'''
S6 = BASE + f'''<div class=k>4주 순서</div><div class=t1 style="top:120px">한 주에<br>한 가지씩 시험</div><div class=info style="top:420px">
<div class=row><div class=lb style="color:{GOLD};margin-top:0">1주</div><div class=vl>키네틱 타이포 2편 + 인포그래픽 1편</div></div>
<div class=row><div class=lb style="color:{GOLD};margin-top:0">2주</div><div class=vl>쇼릴(정월 소개) + 키네틱 1편</div></div>
<div class=row><div class=lb style="color:{TEAL};margin-top:0">3주</div><div class=vl>파티클 + 제품 데모</div></div>
<div class=row><div class=lb style="color:{TEAL};margin-top:0">4주</div><div class=vl>원테이크 모핑 + 4주 결과 비교</div></div></div><script>document.title='ok'</script>'''
S7 = BASE + f'''<div class=k>결정 요청 · 마지막</div><div class=t1 style="top:120px">대표님께<br>질문 3개</div><div class=info style="top:420px">
<div class=row><div class=vl>① 정월 소개 영상(쇼릴)을 먼저 만들까요?</div></div>
<div class=row><div class=vl>② 2D 마스코트를 새로 만들까요, 정월 사진으로만 갈까요?</div></div>
<div class=row><div class=vl>③ 위 순서(주력 → 보조) 그대로 갈까요?</div></div>
<div class=row style="background:{GOLD};color:#111;margin-bottom:0"><div class=vl style="font-weight:900">번호와 답만 알려 주세요</div></div></div><script>document.title='ok'</script>'''
async def main():
    slides = [S1, pair(0, "주력 1 · 2 / 3"), pair(2, "주력 3 · 보조 1"), pair(4, "보조 2 · 3"), pair(6, "조건부 · 보류"), S6, S7]; bad = 0
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 1080, "height": 1350})
        for n, h in enumerate(slides, 1):
            open("/tmp/fp.html", "w", encoding="utf-8").write(h); await pg.goto("file:///tmp/fp.html"); await pg.wait_for_function("document.title=='ok'"); await pg.wait_for_timeout(250)
            for x in await check_page(pg, f"form{n:02d}", "cover"): print("검사:", x); bad += 1
            await pg.screenshot(path=os.path.join(R, "2026-motion", f"form_{n:02d}.png"))
        await b.close()
    print("검사 문제", bad, "건,", len(slides), "장")
asyncio.run(main())
