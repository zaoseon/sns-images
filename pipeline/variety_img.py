"""양산형 방지 구성안(스토리보드) 그림 7장 — 대표 승인 요청(10/7). 사용: python3 pipeline/variety_img.py -> 2026-motion/var_01.png ~ 07.png"""
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
.t1{{position:absolute;left:60px;top:112px;font-size:68px;font-weight:900;font-family:{K.D};line-height:1.3}}
.row{{background:#161c33;border-radius:26px;padding:8px 32px 12px;margin-bottom:10px;font-size:41px;line-height:1.5}}
.row b{{color:{GOLD};font-family:{K.D};font-weight:900}}.row u{{text-decoration:none;color:{TEAL}}}.row s{{text-decoration:none;color:{CORAL}}}
</style><body>'''
def page(tag, title, rows, top=250): return BASE + f'<div class=k>{tag}</div><div class=t1>{title}</div><div style="position:absolute;left:60px;right:60px;top:{top}px">' + "".join(f'<div class=row>{r}</div>' for r in rows) + '</div><script>document.title=\'ok\'</script>'
S = [
 page("양산형 방지 구성안 · 1 / 7", "지적이 맞았어요<br>숫자로 확인했어요", ["앱 대기 영상 <b>39편</b>의 장면을 비교했어요", "<b>처음 장면</b> 34편이 거의 같은 모양 <s>(87%)</s>", "<b>중간 장면</b> 29편 · <b>끝 장면</b> 35편이 같은 모양", "원인: 같은 엔진 · 같은 구성(표지→핵심3→조언→마무리) · 같은 마무리 카드 · 정월 얼굴 반복"], 330),
 page("2 / 7", "새 규칙 R19<br>양산형 방지", ["정월 얼굴은 <b>장면의 40% 이하</b><br>영상의 절반은 얼굴 없는 모션그래픽", "장면 <b>형태</b>를 영상마다 다르게<br>숫자 · 점 격자 · 막대 · 도형 · 체크 · 키네틱", "<b>마무리도 5가지</b> 이상 돌려 써요<br>(팔로우+홈페이지는 모두 넣되 모양만 다르게)", "이웃한 영상은 같은 얼굴·효과·끝 장면 금지<br>유사한 장면 묶음은 전체의 <u>30% 이하</u>"], 330),
 page("3 / 7", "쓸 수 있는 장면 형태 10가지", ["① 큰 숫자 세기 · ② 점 격자 100칸 · ③ 막대 순위", "④ 겹치는 두 원 · ⑤ 여섯 방향 칸 · ⑥ 체크 목록", "⑦ 배터리·게이지 · ⑧ 키네틱 글자 · ⑨ 카드 뒤집기", "<b>⑩ 새로 만들기</b><br>좌우 비교 화면 · 동전 던지기 · 12궁·60괘 판 · 오행 그림", "글 효과도 돌려요: 쾅 · 글자 하나씩 · 마스크 열기 · 숫자 세기 · 해독 · 옆에서 밀기"], 300),
 page("4 / 7", "릴스 14편 새 구성 ①", ["<b>같은 말?</b><br>숫자 세기 14 → 점 격자 100 → 두 원 · 얼굴 없음", "<b>닮은 운명학</b><br>막대 24%·13% → 우연선 17% · 얼굴 없음", "<b>별자리 통할까</b><br>12별자리 원형 판에 불이 켜짐 · 얼굴 끝 1장면", "<b>명궁에 별</b><br>12궁 판에서 명궁 하나가 깜빡 · 얼굴 1장면", "<b>중심별</b><br>12개 별이 원형으로 고르게 쌓임 · 얼굴 없음", "<b>내 괘 바뀔까</b><br>동전 여섯 번 → 효 6줄, 바뀌는 효가 반짝", "<b>하락이수 괘</b><br>60칸 판에서 곤괘가 켜짐 · 얼굴 1장면"], 232),
 page("5 / 7", "릴스 14편 새 구성 ②", ["<b>내 사주만 혼자?</b><br>점 6개 중 사주 점 하나만 떨어짐 · 얼굴 없음", "<b>여섯 중 몇 개</b><br>6개 점이 모이는 모임 애니메이션 · 얼굴 1장면", "<b>사주 vs 별자리</b><br>좌우 비교 화면 → 가운데에서 만남 · 얼굴 없음", "<b>3초 사랑</b><br>사주·별자리·숫자 3칸이 겹쳐 체크 · 얼굴 표지만", "<b>말하면 끄덕</b><br>말풍선이 쌓이는 글자 효과 · 얼굴 1장면", "<b>갑·을</b><br>큰 나무 / 휘는 풀 그림이 주인공 · 얼굴 1장면"], 250),
 page("6 / 7", "글 연결 클립 13편", ["<b>틀은 같아도 형태는 다르게</b><br>질문→오해→정리 틀 안에서 체크 목록 · 배터리 · 좌우 비교 · 타임라인 · 숫자를 돌려 써요", "<b>정월 얼굴은 클립당 1장면</b><br>표지 또는 정리 중 한 곳에만", "<b>마무리 5가지를 돌려요</b><br>① 팔로우 카드 ② 댓글 질문 크게 ③ 스티커 알약<br>④ 한 줄 정리+팔로우 ⑤ 숫자 반복+팔로우", "<b>팔로우·홈페이지 문구</b><br>모든 마무리에 들어가요"], 280),
 page("7 / 7", "진행 순서와 부탁", ["<b>① 시범 3편</b><br>데이터 · 비교 · 오행 영상을 먼저 만들어 앱에 올려요", "<b>② 대표님이 보시고 괜찮으면</b><br>나머지 릴스·클립을 순서대로 만들어요", "<b>③ 끝나면 양산형 검사</b><br>지금 87%인 숫자를 다시 재요", "<b>부탁: 이 구성으로 시범 3편 먼저 만들어도 될까요?</b><br>바꿀 형태나 마무리는 번호로 알려 주세요"], 280),
]
async def main():
    bad = 0
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 1080, "height": 1350})
        for n, h in enumerate(S, 1):
            open("/tmp/vi.html", "w", encoding="utf-8").write(h); await pg.goto("file:///tmp/vi.html"); await pg.wait_for_function("document.title=='ok'"); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(250)
            for x in await check_page(pg, f"var{n:02d}", "cover"): print("검사:", x); bad += 1
            await pg.screenshot(path=os.path.join(R, "2026-motion", f"var_{n:02d}.png"))
        await b.close()
    print("검사 문제", bad, "건,", len(S), "장")
asyncio.run(main())
