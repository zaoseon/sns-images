"""콘텐츠 제작 기준 통합판을 대표가 읽을 수 있게 그림 10장으로 만든다(대표는 md를 못 연다). style_spec 자동 검사.
사용: python3 pipeline/guide_img.py -> 2026-motion/guide_01.png ~ 10.png"""
import os, sys, asyncio
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from style_spec import check_page
import fonts_kit as K
from playwright.async_api import async_playwright
R = os.path.join(HERE, "..")
GOLD = "#e7c88d"; TEAL = "#7fd6c8"; CORAL = "#ff8a73"; PINK = "#ff5c9d"
BASE = f'''<!doctype html><meta charset=utf-8><style>{K.css('gm')}
html,body{{margin:0;width:1080px;height:1350px;background:#0b1020;color:#fff;font-family:{K.B};font-weight:800;word-break:keep-all;line-break:strict;overflow:hidden;position:relative}}
.k{{position:absolute;left:60px;top:48px;font-size:44px;font-weight:900;font-family:{K.D};color:{GOLD}}}
.t1{{position:absolute;left:60px;top:116px;font-size:78px;font-weight:900;font-family:{K.D};line-height:1.35}}
.list{{position:absolute;left:60px;right:60px}}
.row{{background:#161c33;border-radius:30px;padding:20px 38px 24px;margin-bottom:18px;font-size:46px;line-height:1.5}}
.row b{{color:{GOLD};font-family:{K.D};font-weight:900}}.row u{{text-decoration:none;color:{TEAL}}}
.step{{display:flex;align-items:center;gap:26px;background:#161c33;border-radius:30px;padding:18px 34px;margin-bottom:16px;font-size:46px;line-height:1.4}}
.no{{flex:none;width:76px;height:76px;border-radius:50%;background:{GOLD};color:#111;font-family:{K.D};font-weight:900;font-size:44px;display:flex;align-items:center;justify-content:center}}
.star{{background:{CORAL}}}.tag{{flex:none;font-size:40px;font-weight:900;color:#111;background:{CORAL};padding:4px 20px;border-radius:30px}}
.phone{{position:absolute;left:60px;top:250px;width:450px;height:800px;border:5px solid #aab3d6;border-radius:34px;overflow:hidden;background:#0a1226}}
.ui{{position:absolute;background:rgba(255,92,92,.35)}}.safe{{position:absolute;border:4px dashed {TEAL}}}
.mk{{position:absolute;width:56px;height:56px;border-radius:50%;background:{GOLD};color:#111;font-family:{K.D};font-weight:900;font-size:44px;display:flex;align-items:center;justify-content:center}}
</style><body>'''
def slide(tag, title, body): return BASE + f'<div class=k>{tag}</div><div class=t1>{title}</div>' + body + "<script>document.title='ok'</script>"
def rows(items, top, size=46): return f'<div class=list style="top:{top}px">' + "".join(f'<div class=row style="font-size:{size}px">{x}</div>' for x in items) + '</div>'
S = []
S.append(slide("제작 기준 통합판 · 1 / 10", "콘텐츠 제작 기준<br>한 번 정하면 반복되지 않게", rows([
  "<b>기존 가이드(10/4)</b><br>주제 · 채널별 글 · OSMU · 검수", "<b>이번에 추가</b><br>그림·영상을 만드는 <u>화면·영상 기준</u>", "대표님 지적 10/4~10/6을 모두 모았어요", "<b>읽고 고칠 곳만</b> 말씀해 주세요"], 440)))
S.append(slide("2 / 10 · 만드는 순서", "대표님 확인은<br>딱 2곳이에요", '<div class=list style="top:360px">' + "".join(
  f'<div class=step><div class="no{" star" if st else ""}">{i}</div><div>{t}{("<br><span class=tag>대표님 확인</span>" if st else "")}</div></div>' for i, (t, st) in enumerate([
  ("주제와 한 줄 정하기", False), ("스토리보드 그림 보여 드리기", True), ("제작 (기준이 자동 적용)", False), ("자동 검사 · 앱에 올리고 반영 확인", False), ("완성 영상 보기", True), ("일정 제안 → 승인 후 예약", False)], 1)) + '</div>'))
S.append(slide("3 / 10 · 내용 기준", "무엇을 말할까", rows([
  "<b>첫 장면</b>은 통계가 아니라 <u>장면 한 줄</u>", "<b>숫자</b>는 우리 계산 값만. 단정하거나 겁주지 않아요", "<b>낯선 말</b>은 영상 안에서 정월이 풀이해요", "<b>가격·기한</b> 같은 판매 정보는 영상에 안 넣어요", "정월이 나오면 <b>AI 생성 캐릭터</b> 표시"], 270)))
S.append(slide("4 / 10 · 글자 기준", "글자는 이렇게", rows([
  "<b>제목</b> 영상 G마켓 산스 · 카드 페이퍼로지<br><b>본문</b> 프리텐다드", "굵기 <u>800 이상</u> · 본문 <u>44px 이상</u><br>줄간격 <u>1.5 이상</u>", "글자는 <b>단색</b>(흰·금·어두운 잉크)<br>색 그림자·테두리 없음", "도형 위 글자는 도형 <u>안에 온전히</u><br>단어 중간에서 줄을 끊지 않아요"], 270)))
ph = '<div class=phone><div class=ui style="left:0;top:0;width:450px;height:104px"></div><div class=ui style="left:0;top:663px;width:450px;height:137px"></div><div class=ui style="left:400px;top:104px;width:50px;height:559px"></div><div class=safe style="left:21px;top:137px;width:379px;height:476px"></div>' \
     '<div class=mk style="left:330px;top:142px">1</div><div class=mk style="left:330px;top:555px">2</div><div class=mk style="left:30px;top:555px">3</div></div>'
leg = f'<div class=list style="top:250px;left:550px;right:50px">' + "".join(f'<div class=row style="font-size:42px;padding:16px 26px 18px;margin-bottom:14px"><b>{n}</b> {t}</div>' for n, t in (("1", "우측 상단<br>자오선 | 동서양<br>6개 운명학 교차분석"), ("2", "우측 하단<br>zaoseon.com"), ("3", "좌측 하단<br>AI 생성 캐릭터<br>(정월이 나올 때)"))) + '</div>'
S.append(slide("5 / 10 · 고정 요소", "항상 같은 자리", ph + leg + f'<div class=list style="top:1090px"><div class=row style="font-size:44px">빨간 곳은 인스타가 <u>가리는 곳</u><br>점선 안(위 330 ~ 아래 1470)에 글자를 둬요</div></div>'))
S.append(slide("6 / 10 · 화면 채움", "배경과 여백", rows([
  "배경은 <b>해·달·별 브랜드 소재</b>", "가려지는 위·아래도 <u>배경으로 채워요</u>", "글자는 크게. <b>여백만 크게 남기지 않아요</b>", "말풍선은 <b>정월 원형 아바타 + 이름표</b><br>반투명 남색 · 금색 테두리"], 270)))
S.append(slide("7 / 10 · 영상 기준", "움직임과 시간", rows([
  "<b>첫 프레임</b>은 완성된 그림", "문장 <u>2초</u> · 낱말 <u>1초</u> 이상 보여 줘요", "정지 <u>0.5초 이하</u><br>가만히 있어도 박자마다 살짝 움직여요", "곡은 최근 3편과 다르게<br>정월은 숨쉬기·머리·머리카락만", "길이 <b>15~25초</b> (설명이 있으면 25초까지)"], 270, 44)))
S.append(slide("8 / 10 · 표지와 마무리", "표지와 마지막 장면", rows([
  "<b>표지</b>는 따로 만들어요<br>프로필 격자(가운데 3:4)에서도 다 보여요", "<b>마무리 ①</b> 댓글 질문 한 줄", "<b>마무리 ②</b> 팔로우하고<br>더 많은 이야기 나눠요", "<b>마무리 ③</b> 프로필 링크에서 생년월일<br>입력하고 내 첫글자와 타고난<br>기운 알아보기"], 270, 44)))
S.append(slide("9 / 10 · 검사", "누가 무엇을 확인할까", rows([
  "<b>기계</b> 굵기·크기·줄간격·겹침·여백<br>글꼴·소리·정지·첫 화면", "<b>저</b> 처음·중간·끝 화면을 직접 보고<br>앱 반영까지 확인", "<b>대표님</b> 분위기·말투·끌리는지·소리", "지적하시면 <u>기준에 올려요</u><br>다음 영상부터 자동 적용"], 270, 44)))
S.append(slide("10 / 10 · 질문", "정해 주실 것 7가지", rows([
  "① 마무리를 <b>팔로우 + 홈페이지</b>로<br>모든 릴스에 통일해도 될까요?", "② 캡션의 <b>프로필 링크</b> 문장은<br>하루 1건? 영상마다?", "③ <b>내 첫글자</b>는 정확히 무엇인가요?", "④ 영상 길이 <b>25초</b>까지 괜찮나요?", "⑤ 낯선 말마다 <b>정월 설명 장면</b>을 넣을까요?", "⑥ 우측 상단 문구 확정?<br>⑦ 카드에도 두 줄로 넣을까요?"], 240, 42)))
async def main():
    bad = 0
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 1080, "height": 1350})
        for n, h in enumerate(S, 1):
            open("/tmp/gd.html", "w", encoding="utf-8").write(h); await pg.goto("file:///tmp/gd.html"); await pg.wait_for_function("document.title=='ok'"); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(250)
            for x in await check_page(pg, f"guide{n:02d}", "cover"): print("검사:", x); bad += 1
            await pg.screenshot(path=os.path.join(R, "2026-motion", f"guide_{n:02d}.png"))
        await b.close()
    print("검사 문제", bad, "건,", len(S), "장")
asyncio.run(main())
