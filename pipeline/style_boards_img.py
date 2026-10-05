"""외부 가이드(스타일 30)의 프롬프트를 자오선 내용으로 바꾼 '우리 프롬프트'와 장면표 스토리보드 그림(승인 요청).
리소그래프(30) · 지하철 노선도(14) · 탑승권(19). 큰 글씨·굵게, style_spec 자동 검사.
사용: python3 pipeline/style_boards_img.py -> 2026-motion/sbx_01.png ~ 07.png"""
import os, sys, asyncio
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from style_spec import check_page
import fonts_kit as K
from playwright.async_api import async_playwright
R = os.path.join(HERE, "..")
GOLD = "#e7c88d"; TEAL = "#7fd6c8"; CORAL = "#ff8a73"
STYLES = [
 dict(no="30", name="리소그래프", pillar="교차 데이터", col=CORAL,
      prompt="리소그래프 인쇄 스타일로 \"사주와 별자리, 같은 말을 할까요?\" 모션그래픽. 미색 종이에 형광 핑크·블루 두 잉크, 겹친 곳은 보라. 판이 한 장씩 툭툭 찍히고 장면마다 새 종이가 넘어가게. 박자에 맞춰 9:16 15초.",
      changed=[("색", "미색 종이 + 핑크(사주) + 블루(별자리)"), ("내용", "겹친 곳 = 같은 말, 100명 중 14명(13.5%)")],
      scenes=[("0~3초", "핑크 판이 툭 찍히며 \"사주\"가 큼직하게(첫 화면부터 제목이 보임)"), ("3~6초", "블루 판이 겹쳐 찍히며 \"별자리\", 겹친 곳이 보라"), ("6~10초", "점 100개 중 겹친 14개만 보라로 켜지고 14가 올라감"), ("10~13초", "새 종이가 넘어와 \"다른 말은 내가 고를 곳\""), ("13~15초", "\"떠오르는 사람에게 보내 보세요\"")]),
 dict(no="14", name="지하철 노선도", pillar="소개·상품", col=TEAL,
      prompt="지하철 노선도 스타일로 \"내 인생 노선도(대운)\" 모션그래픽. 흰 바탕에 코랄·민트·블루 노선, 노선이 그어지며 역이 10년마다 하나씩 찍히고 마지막에 \"지금 내 역은?\" 안내판이 켜지게. 박자에 맞춰 9:16 15초.",
      changed=[("색", "흰 바탕 + 코랄·민트·블루 노선(우리 강조색)"), ("내용", "10년 단위 역 6개, 질문은 \"지금 나는 몇 번째 역?\"")],
      scenes=[("0~3초", "노선이 그어지며 \"내 인생 노선도\"(첫 화면부터 제목이 보임)"), ("3~7초", "역 6개가 박자마다 하나씩 찍힘(10년 단위)"), ("7~10초", "열차가 들어오고 \"다음 역\" 안내"), ("10~13초", "안내판 \"지금 내 역은?\" 번호 1~6, 댓글로 답하기"), ("13~15초", "\"떠오르는 사람에게 보내 보세요\"")]),
 dict(no="19", name="탑승권", pillar="소개·상품", col=GOLD,
      prompt="비행기 탑승권 스타일로 \"2027 정미년행 탑승권\" 모션그래픽. 남색+크림 종이+붉은 도장, 안내가 탑승권 한 장에 찍혀 내려오고 도장이 쾅, 마지막 박에 절취선이 뜯기게. 박자에 맞춰 9:16 15초.",
      changed=[("색", "남색 + 크림 종이 + 붉은 도장(금색 포인트)"), ("내용", "출발 2026 병오 → 도착 2027 정미, 좌석 12칸(12개월)")],
      scenes=[("0~3초", "탑승권 한 장이 내려오며 \"2027 정미년행\"(첫 화면부터 제목이 보임)"), ("3~7초", "출발 2026 병오 → 도착 2027 정미, 좌석 12칸이 박자마다 찍힘"), ("7~10초", "\"정월 확인\" 도장이 쾅"), ("10~13초", "\"여섯 운명학으로 읽는 12개월\""), ("13~15초", "마지막 박에 절취선이 뜯김 + \"당신의 한 해, 12개월 풀이\"")])]
BASE = f'''<!doctype html><meta charset=utf-8><style>{K.css('gm')}
html,body{{margin:0;width:1080px;height:1350px;background:#0b1020;color:#fff;font-family:{K.B};font-weight:800;word-break:keep-all;line-break:strict;overflow:hidden;position:relative}}
.k{{position:absolute;left:60px;top:50px;font-size:46px;font-weight:900;font-family:{K.D};color:{GOLD}}}
.t1{{position:absolute;left:60px;top:120px;font-size:76px;font-weight:900;font-family:{K.D};line-height:1.4}}
.box{{position:absolute;left:60px;right:60px;background:#161c33;border-radius:32px;padding:28px 42px 32px}}
.lb{{font-size:42px;font-weight:900}}.vl{{font-size:46px;font-weight:800;line-height:1.6;margin-top:6px}}
.sc{{display:flex;gap:26px;align-items:flex-start;margin-bottom:20px;background:#161c33;border-radius:28px;padding:20px 34px 22px}}.sc .tm{{flex:none;width:170px;font-size:44px;font-weight:900;font-family:{K.D}}}.sc .ds{{font-size:44px;font-weight:800;line-height:1.5}}
</style><body>'''
def prompt_slide(i, s):
    ch = "".join(f'<div class=lb style="color:{TEAL};margin-top:14px">바꾼 것 · {k}</div><div class=vl style="font-size:44px">{v}</div>' for k, v in s["changed"])
    return BASE + f'<div class=k>우리 프롬프트 {i+1} / 3</div><div class=t1 style="font-size:70px">{s["no"]} {s["name"]}</div>' \
        f'<div class=box style="top:240px"><div class=lb style="color:{s["col"]}">프롬프트</div><div class=vl style="font-size:44px">{s["prompt"]}</div>{ch}</div><script>document.title=\'ok\'</script>'
def scene_slide(i, s):
    rows = "".join(f'<div class=sc><div class=tm style="color:{s["col"]}">{t}</div><div class=ds>{d}</div></div>' for t, d in s["scenes"])
    return BASE + f'<div class=k>장면표 {i+1} / 3</div><div class=t1 style="font-size:66px;top:100px">{s["name"]} · 5장면</div><div style="position:absolute;left:60px;right:60px;top:260px">{rows}</div><script>document.title=\'ok\'</script>'
S7 = BASE + f'''<div class=k>결정 요청 · 마지막</div><div class=t1 style="top:110px">대표님께<br>질문 3개</div><div style="position:absolute;left:60px;right:60px;top:400px">
<div class=sc style="display:block"><div class=ds>① 이 3개 스토리보드 그대로 만들어도 될까요?</div></div>
<div class=sc style="display:block"><div class=ds>② 탑승권은 판매 정보 없이 맛보기만 넣어도 될까요?</div></div>
<div class=sc style="display:block"><div class=ds>③ 프로필 링크 문구를 세 편 중 한 편에만 넣을까요?</div></div>
<div class=sc style="display:block;background:{GOLD};color:#111"><div class=ds style="font-weight:900">번호와 답만 알려 주세요</div></div></div><script>document.title='ok'</script>'''
async def main():
    slides = []
    for i, s in enumerate(STYLES): slides += [prompt_slide(i, s), scene_slide(i, s)]
    slides.append(S7); bad = 0
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 1080, "height": 1350})
        for n, h in enumerate(slides, 1):
            open("/tmp/sbx.html", "w", encoding="utf-8").write(h); await pg.goto("file:///tmp/sbx.html"); await pg.wait_for_function("document.title=='ok'"); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(250)
            for x in await check_page(pg, f"sbx{n:02d}", "cover"): print("검사:", x); bad += 1
            await pg.screenshot(path=os.path.join(R, "2026-motion", f"sbx_{n:02d}.png"))
        await b.close()
    print("검사 문제", bad, "건,", len(slides), "장")
asyncio.run(main())
