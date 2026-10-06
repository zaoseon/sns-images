"""브랜드 고정 요소(10/6 대표 지시) — 모든 이미지·영상에 같은 자리에 넣는다.
- 우측 상단: "자오선 | 동서양 6개 운명학 교차분석" (서비스를 계속 알린다)
- 우측 하단: zaoseon.com (고정)
- 좌측 하단: "AI 생성 캐릭터" (정월이 나오는 이미지·장면에만, 위치는 항상 같은 곳)
위치는 인스타 화면 가림(UI)을 피한다. 릴스 1080x1920: 안전 영역 위 330 · 아래 1470 · 오른쪽 960(오른쪽 버튼 120px). 카드 1080x1350: 가장자리 55px.
HTML을 쓰는 생성기(카드·키네틱·리소그래프)는 css()와 html()을 붙이고, PIL 영상 엔진은 draw_reel()을 쓴다."""
GOLD = "#e7c88d"
TAG1, TAG2, URL, AI = "자오선", "동서양 6개 운명학 교차분석", "zaoseon.com", "AI 생성 캐릭터"
REEL = dict(right=120, tag_top=340, bottom=455)       # 릴스: 오른쪽 120px(= x 960), 위 340, 아래 455(= y 1465)
CARD = dict(right=55, tag_top=58, bottom=46)
def css():
    return (".bf{position:absolute;white-space:nowrap;z-index:40}"
            ".bf-tag{font-family:'JW-B',sans-serif;font-weight:800;font-size:34px;color:#fff;opacity:.95;line-height:1.2;text-align:right}"
            ".bf-tag b{font-family:'JW-D',sans-serif;font-weight:900;font-size:38px;color:#e7c88d;margin-right:14px}.bf-tag i{font-style:normal;color:rgba(255,255,255,.55);margin-right:14px}"
            ".bf-tag2 b{display:block;margin:0}.bf-tag2 i{display:none}"
            ".bf-url{font-family:'JW-D',sans-serif;font-weight:900;color:#e7c88d;letter-spacing:.5px}"
            ".bf-ai{font-family:'JW-B',sans-serif;font-weight:800;color:#fff;background:rgba(0,0,0,.5);padding:6px 18px;border-radius:24px;line-height:1.2}")
def html(kind="reel", ai=False, ai_id="bfAI", stacked=False):
    P = REEL if kind == "reel" else CARD
    url_fs, ai_fs = (40, 30) if kind == "reel" else (36, 28)
    tag = f'<div class="bf bf-tag{" bf-tag2" if stacked else ""}" id=bfTag style="right:{P["right"]}px;top:{P["tag_top"]}px"><b>{TAG1}</b><i>|</i>{TAG2}</div>'
    url = f'<div class="bf bf-url" id=bfUrl style="right:{P["right"]}px;bottom:{P["bottom"]}px;font-size:{url_fs}px">{URL}</div>'
    a = f'<div class="bf bf-ai" id={ai_id} style="left:{60 if kind == "reel" else 55}px;bottom:{P["bottom"]}px;font-size:{ai_fs}px">{AI}</div>' if ai else ""
    return tag + url + a
