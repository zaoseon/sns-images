"""브랜드 고정 요소(10/6 대표 지시) — 모든 이미지·영상에 같은 자리에 넣는다.
- 상단 왼쪽: "자오선" · 상단 오른쪽: "동서양 6개 운명학 교차분석" (서비스를 계속 알린다, 10/6 대표 지정)
- 우측 하단: zaoseon.com (고정)
- 좌측 하단: "정월은 가상의 AI 캐릭터입니다"(흐린 색, 10/6 대표 지정) (정월이 나오는 이미지·장면에만, 위치는 항상 같은 곳)
위치는 인스타 화면 가림(UI)을 피한다. 릴스·클립 1080x1920: 안전 영역 위 330 · 아래 1470 · 오른쪽 900(10/6 네이버 클립 캡처 실측: 버튼 줄 x 905~). 카드 1080x1350: 가장자리 55px.
HTML을 쓰는 생성기(카드·키네틱·리소그래프)는 css()와 html()을 붙이고, PIL 영상 엔진은 draw_reel()을 쓴다."""
GOLD = "#e7c88d"
TAG1, TAG2, URL, AI = "자오선", "동서양 6개 운명학 교차분석", "zaoseon.com", "정월은 가상의 AI 캐릭터입니다"
REEL = dict(right=180, tag_top=340, bottom=455)       # 릴스·클립 공통: 오른쪽 180px(= x 900, 네이버 클립 버튼 줄 x 905~ 피함), 위 340, 아래 455(= y 1465)
CARD = dict(right=55, tag_top=58, bottom=46)
def css():
    return (".bf{position:absolute;white-space:nowrap;z-index:40}"
            ".bf-l{font-family:'JW-D',sans-serif;font-weight:900;font-size:42px;color:#e7c88d;line-height:1.2}"
            ".bf-r{font-family:'JW-B',sans-serif;font-weight:800;font-size:34px;color:#fff;opacity:.95;line-height:1.2;text-align:right}"
            ".bf-url{font-family:'JW-D',sans-serif;font-weight:900;color:#e7c88d;letter-spacing:.5px}"
            ".bf-ai{font-family:'JW-B',sans-serif;font-weight:800;color:rgba(255,255,255,.55);background:rgba(0,0,0,.28);padding:5px 16px;border-radius:24px;line-height:1.2}")
def html(kind="reel", ai=False, ai_id="bfAI", stacked=False):
    """상단 왼쪽 '자오선' · 상단 오른쪽 '동서양 6개 운명학 교차분석'(10/6 대표 지정). stacked는 옛 호출 호환용으로 무시한다."""
    P = REEL if kind == "reel" else CARD
    left = 60 if kind == "reel" else 55
    url_fs, ai_fs = (40, 28) if kind == "reel" else (36, 26)
    tl = f'<div class="bf bf-l" id=bfL style="left:{left}px;top:{P["tag_top"]}px">{TAG1}</div>'
    tr = f'<div class="bf bf-r" id=bfR style="right:{P["right"]}px;top:{P["tag_top"] + 6}px">{TAG2}</div>'
    pill = ";background:rgba(0,0,0,.45);padding:6px 20px;border-radius:24px" if kind != "reel" else ""
    url = f'<div class="bf bf-url" id=bfUrl style="right:{P["right"]}px;bottom:{P["bottom"]}px;font-size:{url_fs}px{pill}">{URL}</div>'
    a = f'<div class="bf bf-ai" id={ai_id} style="left:{left}px;bottom:{P["bottom"]}px;font-size:{ai_fs}px">{AI}</div>' if ai else ""
    return tl + tr + url + a
