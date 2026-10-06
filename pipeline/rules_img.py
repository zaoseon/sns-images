"""확정 규칙을 대표가 앱에서 볼 수 있는 그림 5장으로(대표는 md를 못 연다). 내용은 rules.py와 audit 결과에서 온다. style_spec 자동 검사.
사용: python3 pipeline/rules_img.py -> 2026-motion/rules_01.png ~ 05.png"""
import os, sys, json, asyncio
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from style_spec import check_page
import fonts_kit as K, rules
from playwright.async_api import async_playwright
R = os.path.abspath(os.path.join(HERE, ".."))
GOLD = "#e7c88d"; TEAL = "#7fd6c8"; CORAL = "#ff8a73"
BASE = f'''<!doctype html><meta charset=utf-8><style>{K.css('gm')}
html,body{{margin:0;width:1080px;height:1350px;background:#0b1020;color:#fff;font-family:{K.B};font-weight:800;word-break:keep-all;line-break:strict;overflow:hidden;position:relative}}
.k{{position:absolute;left:60px;top:48px;font-size:44px;font-weight:900;font-family:{K.D};color:{GOLD}}}
.t1{{position:absolute;left:60px;top:112px;font-size:70px;font-weight:900;font-family:{K.D};line-height:1.3}}
.row{{background:#161c33;border-radius:28px;padding:12px 34px 16px;margin-bottom:14px;font-size:42px;line-height:1.5}}
.row b{{color:{GOLD};font-family:{K.D};font-weight:900}}.st{{display:inline-block;font-size:40px;font-weight:900;color:#111;padding:0 18px;border-radius:26px;margin-left:14px;line-height:1.5}}
</style><body>'''
def page(tag, title, body): return BASE + f'<div class=k>{tag}</div><div class=t1>{title}</div><div style="position:absolute;left:60px;right:60px;top:250px">{body}</div><script>document.title=\'ok\'</script>'
SHORT = {"R01": "왼쪽 자오선 · 오른쪽 동서양 6개 운명학 교차분석", "R02": "우측 하단 zaoseon.com 고정", "R03": "정월이 나올 때 좌측 하단 '정월은 가상의 AI 캐릭터입니다'(흐린 색)", "R04": "릴스·클립 x 50~900 · y 330~1470. 바깥은 배경만", "R05": "영상 제목 G마켓 산스 · 카드 제목 페이퍼로지 · 본문 프리텐다드",
         "R06": "본문 44px 이상 · 굵기 800 이상 · 줄간격 1.5 이상", "R07": "단색만 · 색 그림자 금지 · 도형에 걸치지 않음", "R08": "안 끝나면 의미 단위로 줄바꿈 · 가운데 정렬", "R09": "제목과 차트 간격은 하단 여백을 고려", "R10": "말풍선 가운데 · 배지 중앙 · 여섯 방향 3×2 · 설명글 작게",
         "R11": "댓글 질문 → 팔로우 → 프로필 링크(홈페이지 유입)", "R12": "해·달·별 브랜드 소재, 가려지는 곳도 배경으로", "R13": "표지 따로 · 첫 프레임 완성 · 정지 0.5초 이하", "R14": "새 그림·영상은 틀로 만들고, 지적은 틀에 올림",
         "R15": "클립은 9:16 영상으로만(4:5 카드 금지)", "R16": "캐러셀을 1080x1440(3:4)으로 전환", "R17": "캡션 프로필 링크 문장: 하루 1건 vs 영상마다", "R18": "카드·말풍선·배지·버튼 안 글은 정중앙"}
def row(rid, color=None):
    r = next(x for x in rules.RULES if x[0] == rid); col = {"확정": TEAL, "임시": GOLD, "미정": CORAL}[r[3]]
    return f'<div class=row><b>{r[1]}</b><span class=st style="background:{col}">{r[3]}</span><br>{SHORT[rid]}</div>'
aud = json.load(open(os.path.join(R, "content", "audit", "rules_audit.json"), encoding="utf-8")); ok = sum(1 for x in aud if x["status"] == "통과"); tot = len(aud)
S = [page("확정 규칙 · 1 / 5", "확정 규칙 ①", "".join(row(i) for i in ("R01", "R02", "R03", "R05", "R06"))),
     page("2 / 5", "확정 규칙 ②", "".join(row(i) for i in ("R07", "R18", "R08", "R09", "R10"))),
     page("3 / 5", "확정 규칙 ③ · 임시", "".join(row(i) for i in ("R11", "R12", "R13", "R14", "R04"))),
     page("4 / 5", "미정(적용 안 함)", "".join(row(i) for i in ("R15", "R16", "R17")) + '<div class=row style="margin-top:30px">이 세 가지는 <b>대표님 답</b>을 받을 때까지 적용하지 않아요</div>'),
     page("5 / 5", "적용 현황", f'<div class=row>앱 영상·그림 <b>{tot}개</b> 자동 측정<br>처음 <b>4개</b> → 지금 <b>{ok}개</b> 적용</div><div class=row>글 연결 클립 <b>13편</b> 모두 통과</div><div class=row>아직 <b>{tot - ok}개</b> 미적용<br>릴스 14 · 견본 6 · 카드·클립·퀴즈 등</div><div class=row>다시 만들 때 자동으로 규칙이 들어가요</div>')]
async def main():
    bad = 0
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 1080, "height": 1350})
        for n, h in enumerate(S, 1):
            open("/tmp/ri.html", "w", encoding="utf-8").write(h); await pg.goto("file:///tmp/ri.html"); await pg.wait_for_function("document.title=='ok'"); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(250)
            for x in await check_page(pg, f"rules{n:02d}", "cover"): print("검사:", x); bad += 1
            await pg.screenshot(path=os.path.join(R, "2026-motion", f"rules_{n:02d}.png"))
        await b.close()
    print("검사 문제", bad, "건,", len(S), "장")
asyncio.run(main())
