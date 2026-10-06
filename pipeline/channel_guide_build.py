"""channel_specs.py에서 (1) 채널별 규격·안전영역 문서(md) (2) 대표가 볼 그림 8장을 만든다. 값은 channel_specs.py 한 곳에서만 나온다.
사용: python3 pipeline/channel_guide_build.py -> ../zaoseon-site/docs/채널별_규격_안전영역_2026-10-06.md, 2026-motion/chan_01.png ~ 08.png"""
import os, sys, asyncio
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import channel_specs as CS, fonts_kit as K
from style_spec import check_page
from playwright.async_api import async_playwright
R = os.path.abspath(os.path.join(HERE, ".."))
GOLD = "#e7c88d"; TEAL = "#7fd6c8"; CORAL = "#ff8a73"
CH = CS.CH
# ---------------- 1) 문서 ----------------
def doc():
    L = ["# 채널별 규격·안전영역·레이아웃 표준 (2026-10-06, ①)", "",
         "> 대표 지시(10/6): 블로그 썸네일 · 네이버 클립 · 인스타 캐러셀 · 인스타 릴스를 채널별로 정리해 두면 작업이 빨라진다. **값은 `sns-images/pipeline/channel_specs.py` 한 곳**에서 나오고, 이 문서와 앱 그림(`guide-channels`)은 그 파일에서 자동으로 만든다.",
         "> 근거 표시: **ok** = 2026 가이드 여러 건으로 확인 · **실측** = 우리 계정·앱에서 잰 값 · **추정** = 공식 수치를 못 찾아 가까운 채널 값을 빌림(확인 필요).",
         "> 공통 글꼴: 영상 제목 G마켓 산스 · 카드/썸네일 제목 페이퍼로지 · 본문 프리텐다드(800) · 한자 명조. 공통 고정 요소: 우상단 서비스 문구 · 우하단 zaoseon.com · 좌하단 AI 생성 캐릭터(정월이 나올 때)(`제작_기준_통합_2026-10-06.md`).", ""]
    L += ["## 한눈에", "", "| 채널 | 크기 | 비율 | 안전 영역(x0,y0 ~ x1,y1) | 근거 |", "|---|---|---|---|---|"]
    for k, v in CH.items(): L.append(f'| {v["name"]} | {v["w"]}x{v["h"]} | {v["ratio"]} | {v["safe"][0]},{v["safe"][1]} ~ {v["safe"][2]},{v["safe"][3]} | {v["conf"][:60]} |')
    L += ["", "- **인스타 변화(2026 확인):** 프로필 격자가 3:4(1080x1440)로 바뀌었다. 릴스는 1080x1920 그대로이고 격자에는 가운데 3:4(y 240~1680)만 보인다. 4:5(1080x1350) 이미지는 격자에서 좌우가 약 34px씩 잘린다. 3:4 피드 게시물도 정식 지원(2025.5).", ""]
    for k, v in CH.items():
        L += [f"## {v['name']}  ({v['w']}x{v['h']}, {v['ratio']})", "", f"- 길이/분량: {v['length']} · 근거: {v['conf']}",
              f"- UI가 가리는 폭: 위 {v['ui']['top']} · 아래 {v['ui']['bottom']} · 오른쪽 {v['ui']['right']}", f"- **안전 영역:** x {v['safe'][0]}~{v['safe'][2]}, y {v['safe'][1]}~{v['safe'][3]}"]
        for n, b in v["crops"].items(): L.append(f"- 잘림/보이는 영역 · {n}: x {b[0]}~{b[2]}, y {b[1]}~{b[3]}")
        L += ["", "| 구역 | x0 | y0 | x1 | y1 | 설명 |", "|---|---|---|---|---|---|"] + [f"| {n} | {a} | {b} | {c} | {d} | {t} |" for n, a, b, c, d, t in v["zones"]]
        L += ["", f"- 글꼴·크기: 제목 {v['fonts']['title']} · 본문 {v['fonts']['body']} · 라벨 {v['fonts']['label']}", f"- **표지:** {v['cover']}", f"- **CTA:** {v['cta']}", f"- **본문 구성:** {v['body']}", ""]
    L += ["## 대표 확인이 필요한 것", "", "1. 캐러셀을 4:5(1080x1350)에서 **3:4(1080x1440)**로 바꿀지(격자에 딱 맞음, 2026 권장).  2. 네이버 클립 안전 영역을 **릴스와 같은 값**으로 쓰는 것(공식 수치 못 찾음).  3. 블로그 썸네일 서비스 표시를 가운데 정사각 안 하단에 두는 것.  4. 클립에 블로그 스티커를 붙이는 자리(앱에서 실제 위치).  5. 사이트 블로그 썸네일도 같은 글꼴·표시 규칙.", ""]
    return "\n".join(L)
# ---------------- 2) 그림 ----------------
BASE = f'''<!doctype html><meta charset=utf-8><style>{K.css('gm')}
html,body{{margin:0;width:1080px;height:1350px;background:#0b1020;color:#fff;font-family:{K.B};font-weight:800;word-break:keep-all;line-break:strict;overflow:hidden;position:relative}}
.k{{position:absolute;left:60px;top:48px;font-size:44px;font-weight:900;font-family:{K.D};color:{GOLD}}}
.t1{{position:absolute;left:60px;top:112px;font-size:70px;font-weight:900;font-family:{K.D};line-height:1.3}}
.row{{background:#161c33;border-radius:28px;padding:16px 34px 20px;margin-bottom:16px;font-size:44px;line-height:1.5}}
.row b{{color:{GOLD};font-family:{K.D};font-weight:900}}.row u{{text-decoration:none;color:{TEAL}}}
.mock{{position:absolute;background:#0a1226;border:4px solid #aab3d6;overflow:hidden}}
.z{{position:absolute;box-sizing:border-box}}
.mk{{position:absolute;width:52px;height:52px;border-radius:50%;background:{GOLD};color:#111;font-family:{K.D};font-weight:900;font-size:42px;line-height:52px;text-align:center}}
.lg{{position:absolute;font-size:42px;line-height:1.5}}.lg b{{color:{GOLD};font-family:{K.D};font-weight:900}}
.sw{{display:inline-block;width:44px;height:22px;vertical-align:middle;margin-right:14px}}
</style><body>'''
def page(tag, title, body): return BASE + f'<div class=k>{tag}</div><div class=t1>{title}</div>' + body + "<script>document.title='ok'</script>"
def mock(name, left, top, sc, markers_x, legend_x, legend_w, extra=""):
    v = CH[name]; w, h = int(v["w"] * sc), int(v["h"] * sc); o = [f'<div class=mock style="left:{left}px;top:{top}px;width:{w}px;height:{h}px;border-radius:26px">']
    u = v["ui"]
    if u["top"]: o.append(f'<div class=z style="left:0;top:0;width:{w}px;height:{int(u["top"] * sc)}px;background:rgba(255,92,92,.38)"></div>')
    if u["bottom"]: o.append(f'<div class=z style="left:0;top:{h - int(u["bottom"] * sc)}px;width:{w}px;height:{int(u["bottom"] * sc)}px;background:rgba(255,92,92,.38)"></div>')
    if u["right"]: o.append(f'<div class=z style="left:{w - int(u["right"] * sc)}px;top:{int(u["top"] * sc)}px;width:{int(u["right"] * sc)}px;height:{h - int((u["top"] + u["bottom"]) * sc)}px;background:rgba(255,92,92,.38)"></div>')
    s = v["safe"]; o.append(f'<div class=z style="left:{int(s[0] * sc)}px;top:{int(s[1] * sc)}px;width:{int((s[2] - s[0]) * sc)}px;height:{int((s[3] - s[1]) * sc)}px;border:4px dashed {TEAL}"></div>')
    cols = ["#ffb84d", "#c9a6ff", "#9fe870"]
    for i, (n, b) in enumerate(v["crops"].items()): o.append(f'<div class=z style="left:{int(b[0] * sc)}px;top:{int(b[1] * sc)}px;width:{int((b[2] - b[0]) * sc)}px;height:{int((b[3] - b[1]) * sc)}px;border:4px dotted {cols[i % 3]}"></div>')
    zc = ["rgba(231,200,141,.45)", "rgba(127,214,200,.40)", "rgba(255,138,115,.40)", "rgba(143,183,255,.40)", "rgba(201,166,255,.40)", "rgba(231,200,141,.30)"]
    for i, (n, x0, y0, x1, y1, t) in enumerate(v["zones"]): o.append(f'<div class=z style="left:{int(x0 * sc)}px;top:{int(y0 * sc)}px;width:{int((x1 - x0) * sc)}px;height:{max(8, int((y1 - y0) * sc))}px;background:{zc[i % 6]}"></div>')
    o.append('</div>')
    # 번호 표시: 구역 높이 중앙에 맞추되 겹치지 않게 아래로 민다
    ys = sorted([(top + int(((y0 + y1) / 2) * sc), i) for i, (n, x0, y0, x1, y1, t) in enumerate(v["zones"])]); last = -99; pos = {}
    for y, i in ys:
        y = max(y, last + 58); pos[i] = y; last = y
    for i in range(len(v["zones"])): o.append(f'<div class=mk style="left:{markers_x}px;top:{pos[i] - 26}px">{i + 1}</div>')
    lg = f'<div class=lg style="left:{legend_x}px;top:{top}px;width:{legend_w}px">' + "".join(f'<div style="margin-bottom:0"><b>{i + 1}</b> {n}<br><span style="font-size:40px;color:#c5cdf0;font-weight:800">y {y0}~{y1}</span></div>' for i, (n, x0, y0, x1, y1, t) in enumerate(v["zones"])) + '</div>'
    return "".join(o) + lg + extra
S = []
S.append(page("채널별 표준 · 1 / 8", "채널마다 크기와<br>안전영역이 달라요", '<div style="position:absolute;left:60px;right:60px;top:330px">' + "".join(
  f'<div class=row><b>{CH[k]["name"]}</b> {CH[k]["w"]}x{CH[k]["h"]}<br>안전 영역 <u>x {CH[k]["safe"][0]}~{CH[k]["safe"][2]} · y {CH[k]["safe"][1]}~{CH[k]["safe"][3]}</u></div>' for k in ("reel", "naver_clip", "insta_carousel", "naver_blog_thumb", "site_blog_thumb")) + '</div>'))
S.append(page("2 / 8 · 인스타 릴스", "릴스 1080x1920", mock("reel", 110, 250, .36, 40, 560, 480,
  f'<div class=lg style="left:60px;top:1150px;width:960px;font-size:40px"><span class=sw style="background:rgba(255,92,92,.55)"></span>빨강 = 인스타가 가리는 곳 <span class=sw style="background:transparent;border:4px dashed {TEAL}"></span>안전 영역<br><span class=sw style="background:transparent;border:4px dotted #ffb84d"></span>격자 3:4 <span class=sw style="background:transparent;border:4px dotted #c9a6ff"></span>피드 4:5 <span class=sw style="background:transparent;border:4px dotted #9fe870"></span>표지 핵심 1:1</div>')))
def clip_slide():
    sc = .46; L0, T0 = 130, 232            # 캡처 540x1158을 .46*2=0.92배로 쓰지 않고 CSS로 497 폭에 맞춘다
    f = 497 / 1080
    def r(x0, y0, x1, y1, col, dash=False, fill=True):
        st = f"left:{x0 * f:.0f}px;top:{y0 * f:.0f}px;width:{(x1 - x0) * f:.0f}px;height:{max(4, (y1 - y0) * f):.0f}px;"
        return f'<div class=z style="{st}border:3px {"dashed" if dash else "solid"} {col};{"background:" + col.replace("rgb", "rgba").replace(")", ",.28)") if fill else ""}"></div>'
    ov = (r(40, 140, 100, 225, "rgb(255,92,92)") + r(945, 140, 1040, 225, "rgb(255,92,92)") + r(905, 925, 1055, 1880, "rgb(255,92,92)") + r(45, 1580, 810, 1910, "rgb(255,92,92)")
          + r(50, 424, 900, 1564, "rgb(127,214,200)", True, False) + r(0, 94, 1080, 1972, "rgb(255,184,77)", True, False))
    box = f'<div class=mock style="left:{L0}px;top:{T0}px;width:497px;height:1065px;border-radius:22px;background:url(file://{R}/assets/ref/naver_clip_cap2.jpg) 0 0/497px 1065px">{ov}</div>'
    ys = [(150 + 182 * f / f * 0) for _ in range(1)]
    marks = [(1, 200), (2, 560), (3, 900), (4, 400), (5, 1120)]
    mk = "".join(f'<div class=mk style="left:66px;top:{T0 + int(y * f) - 26}px">{n}</div>' for n, y in [(1, 190), (4, 330), (2, 700), (3, 1000), (5, 1090)])
    lg = f'<div class=lg style="left:668px;top:232px;width:372px;font-size:40px">' + "".join(f'<div style="display:flex;gap:16px;margin-bottom:14px"><b style="flex:none;width:36px">{n}</b><span>{t}</span></div>' for n, t in (
        ("1", "위 뒤로·소리<br>y 50~130"), ("2", "오른쪽 버튼 줄<br>x 905 이상<br>y 830~1830"), ("3", "아래 프로필·설명<br>링크 칩<br>y 1489 이상"), ("4", "영상 표시 영역<br>높이 1878"), ("5", "초록 점선 = 안전 영역<br>(릴스와 공통)<br>x 50~900<br>y 330~1470"))) + '</div>'
    return page("3 / 8 · 네이버 클립", "클립 캡처로 잰 영역", box + mk + lg)
S.append(clip_slide())
S.append(page("4 / 8 · 인스타 캐러셀", "캐러셀 1080x1350", mock("insta_carousel", 110, 250, .40, 40, 590, 450,
  f'<div class=lg style="left:60px;top:1128px;width:960px;font-size:40px"><b>2026 변화:</b> 프로필 격자 3:4(1080x1440).<br>4:5 이미지는 좌우 약 34px씩 잘려요.<br><b>3:4로 바꿀지</b> 정해 주세요.</div>')))
b = CH["naver_blog_thumb"]; sc = .70
S.append(page("5 / 8 · 블로그 원고 썸네일", "네이버 블로그 대표 이미지", mock("naver_blog_thumb", 150, 250, sc, 80, 90, 900, "").replace('class=lg style="left:90px;top:250px;width:900px"', 'class=lg style="left:60px;top:820px;width:960px;columns:2;column-gap:30px"') +
  f'<div class=lg style="left:60px;top:1100px;width:960px;font-size:40px"><b>목록</b>은 가운데 정사각만 보여요.<br><b>링크 카드</b>는 전체가 보여요.<br>본문 이미지 1280x600 · CTA 배너 1280x400</div>'))
S.append(page("6 / 8 · 글꼴과 글자 크기", "채널별 글자 규칙", '<div style="position:absolute;left:60px;right:60px;top:280px">' + "".join(
  f'<div class=row style="font-size:40px;padding:12px 30px 16px"><b>{CH[k]["name"]}</b><br>제목 {CH[k]["fonts"]["title"]}<br>본문 {CH[k]["fonts"]["body"]}</div>' for k in ("reel", "naver_clip", "insta_carousel", "naver_blog_thumb")) + '</div>'))
S.append(page("7 / 8 · 표지와 CTA", "채널별 표지와 마무리", '<div style="position:absolute;left:60px;right:60px;top:270px">' + "".join(
  f'<div class=row style="font-size:40px;padding:10px 28px 14px"><b>{n}</b><br>{t}</div>' for n, t in (
  ("릴스 표지", "제목·핵심은 가운데 1:1(y 420~1500) 안"), ("릴스·클립 CTA", "댓글 → 팔로우 → 프로필 링크 안내"), ("캐러셀", "1번 장이 표지(좌우 55px 안)"), ("블로그 썸네일", "가운데 정사각 안 제목 2줄"))) + '</div>'))
S.append(page("8 / 8 · 질문", "정해 주실 것 5가지", '<div style="position:absolute;left:60px;right:60px;top:250px">' + "".join(f'<div class=row style="font-size:42px">{t}</div>' for t in (
  "① 캐러셀을 <b>3:4(1080x1440)</b>로 바꿀까요?", "② 클립 안전 영역을<br><b>릴스와 같은 값</b>으로 써도 될까요?", "③ 블로그 썸네일 <b>서비스 표시</b>는<br>가운데 정사각 안 하단에?", "④ 클립 <b>블로그 스티커</b>가 앱에서 어디에 붙나요?", "⑤ 사이트 블로그 썸네일도 같은 규칙?")) + '</div>'))
async def main():
    docp = os.path.abspath(os.path.join(R, "..", "zaoseon-site", "docs", "채널별_규격_안전영역_2026-10-06.md")); open(docp, "w", encoding="utf-8").write(doc()); print("문서", os.path.getsize(docp), "바이트")
    bad = 0
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 1080, "height": 1350})
        for n, h in enumerate(S, 1):
            open("/tmp/cg.html", "w", encoding="utf-8").write(h); await pg.goto("file:///tmp/cg.html"); await pg.wait_for_function("document.title=='ok'"); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(250)
            for x in await check_page(pg, f"chan{n:02d}", "cover"): print("검사:", x); bad += 1
            await pg.screenshot(path=os.path.join(R, "2026-motion", f"chan_{n:02d}.png"))
        await b.close()
    print("검사 문제", bad, "건,", len(S), "장")
asyncio.run(main())
