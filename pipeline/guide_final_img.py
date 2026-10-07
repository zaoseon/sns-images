"""제작 가이드 확정판 그림 10장(대표는 md를 못 연다). 내용은 docs/제작_가이드_확정판_2026-10-07.md와 같다. style_spec 자동 검사.
사용: python3 pipeline/guide_final_img.py -> 2026-motion/guide_final_01.png ~ 10.png"""
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
.t1{{position:absolute;left:60px;top:112px;font-size:68px;font-weight:900;font-family:{K.D};line-height:1.3}}
.row{{background:#161c33;border-radius:26px;padding:8px 32px 12px;margin-bottom:10px;font-size:41px;line-height:1.5}}
.row b{{color:{GOLD};font-family:{K.D};font-weight:900}}.row u{{text-decoration:none;color:{TEAL}}}.row s{{text-decoration:none;color:{CORAL}}}
</style><body>'''
def page(tag, title, rows, top=250): return BASE + f'<div class=k>{tag}</div><div class=t1>{title}</div><div style="position:absolute;left:60px;right:60px;top:{top}px">' + "".join(f'<div class=row>{r}</div>' for r in rows) + '</div><script>document.title=\'ok\'</script>'
S = [
 page("제작 가이드 확정판 · 1 / 10", "① 화면 구조", ["<b>세로 1080x1920</b><br>안전 영역 x 50~900 · y 330~1470", "<b>상단 문구 띠 y 335~395</b><br>왼쪽 자오선 · 오른쪽 동서양 6개 운명학 교차분석", "<b>하단 고정 줄 y 1425~1465</b><br>오른쪽 zaoseon.com · 왼쪽 정월 AI 고지(정월이 나올 때만)", "<b>본문 y 475 ~ 1375</b><br>묶음 가운데는 y 910 (±35)"], 330),
 page("2 / 10", "② 간격 숫자", ["<b>상단 문구 ↔ 본문 첫 글자</b><br>80px 이상 (본문은 y 475 이상)", "<b>제목 ↔ 표·그래프</b> 40px 이상<br><b>표·그래프 ↔ 설명글</b> 50px 이상", "<b>맨 아래 ↔ 하단 주소</b><br>50px 이상 (맨 아래 y 1375 이하)", "<b>박스·카드·말풍선 안 글</b><br>위아래·좌우 여백이 같게 정중앙"], 330),
 page("3 / 10", "③ 글", ["<b>글꼴</b> 영상 제목 G마켓 산스 · 카드 제목 페이퍼로지<br>본문 프리텐다드 · 한자 세리프", "<b>크기</b> 제목 80~124 · 본문 44 이상<br>차트 라벨 40 이상 · 굵기 800 이상", "<b>색</b> 흰·금·산호·민트, 단색만<br>색 그림자·테두리 금지", "<b>값마다 색 하나</b><br>14와 '같은 말'은 금색, 86과 '다른 말'은 산호색"], 300),
 page("4 / 10", "④ 줄바꿈·말투", ["<b>의미 단위로 줄바꿈</b><br>책임지는 / 사랑을 해요", "<b>서술어(해요·이에요)만 한 줄 금지</b><br>한 줄에 안 끝나면 줄바꿈하고 가운데 정렬", "<b>시청자 질문은 존댓말</b><br>어느 쪽을 더 믿으세요?", "<b>강조 낱말만 강조색</b> · 문구 안전(확신·불안·단정 금지)"], 300),
 page("5 / 10", "⑤ 배경과 정월", ["<b>뒤 차트는 브랜드 황도 차트 하나만</b><br>진하기 30%, 가운데 x 470 · y 800, 천천히 회전", "<b>직접 그린 고리·원 금지</b><br>해·달 소재는 위쪽에", "<b>일간 한자 워터마크</b><br>차트 가운데에 윤곽선만, 뒤에 어두운 막", "<b>정월 얼굴은 장면의 40% 이하</b><br>AI 고지는 정월이 나올 때만"], 300),
 page("6 / 10", "⑥ 양산형 방지", ["<b>장면 형태를 영상마다 다르게</b><br>숫자·점 격자·막대·두 원·좌우 비교·나무·판·노선도", "<b>글 효과를 돌려 써요</b><br>닦아내기 · 밀어 넣기 · 확대 · 숫자 세기", "<b>마무리 5종을 돌려 써요</b><br>팔로우 카드·댓글 질문·정월 알약·한 줄 정리·숫자 반복", "<b>이웃 영상은 같은 얼굴·효과·끝 장면 금지</b><br>비슷한 장면 묶음은 전체의 30% 이하"], 300),
 page("7 / 10", "⑦ 마무리·캡션", ["<b>마무리</b> 댓글 질문 → 팔로우 → 프로필 링크<br>(생년월일 입력, 내 첫글자와 타고난 기운)", "<b>캡션은 영상마다 다른 한 줄</b><br>그 영상 주제에 맞춘 홈페이지 유입 문장", "<b>팔로우 유도 한 줄</b><br>프로필 링크 문장은 캡션에 정확히 1개", "<b>면책</b> 재미로 보는 풀이예요"], 300),
 page("8 / 10", "⑧ 채널", ["<b>릴스·네이버 클립</b> 1080x1920 9:16 영상<br>4:5 카드로 클립 금지 · 표지는 따로", "<b>길이</b> 릴스 15~25초 · 클립 12초 안팎", "<b>캐러셀·카드</b> 1080x1440 (3:4)<br>가장자리 55px · 상단 문구 y 58"], 330),
 page("9 / 10", "⑨ 올리기 전 검사 한 번에", ["<b>python3 pipeline/qa_all.py</b>", "상단 문구·주소 위치 · 글·그림 배치<br>안전 영역 위 침범 · 줄바꿈 · 문구 안전", "캡션(프로필 링크 1개·반복 금지)<br>양산형 유사도(30% 이하)", "<b>하나라도 걸리면 앱에 올리지 않아요</b>"], 300),
 page("10 / 10", "현황과 확인 한 가지", ["<b>앱 대기 영상 33편 전부</b> 배치 기준 밖<br>장면 178개 중 108개 (10/7 측정)", "릴스 14편: 표지·조언 장면이 y 425~437에서 시작<br>클립 13편: 59장면 전부 · 카드 고르기·점 격자 등 21장면 전부", "시범 3편·수성 역행 영상만 통과<br>새 구성으로 다시 만들 때 모두 통과시켜요", "<b>확인:</b> 영상 본문 줄간격을 1.35~1.4로 확정할까요?<br>(규칙은 1.5 이상, 영상은 1.3~1.4로 만들어 왔어요)"], 280),
]
async def main():
    bad = 0
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 1080, "height": 1350})
        for n, h in enumerate(S, 1):
            open("/tmp/gf.html", "w", encoding="utf-8").write(h); await pg.goto("file:///tmp/gf.html"); await pg.wait_for_function("document.title=='ok'"); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(250)
            for x in await check_page(pg, f"gf{n:02d}", "cover"): print("검사:", x); bad += 1
            await pg.screenshot(path=os.path.join(R, "2026-motion", f"guide_final_{n:02d}.png"))
        await b.close()
    print("검사 문제", bad, "건,", len(S), "장")
asyncio.run(main())
