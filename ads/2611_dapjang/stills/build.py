"""메타 시험 광고 이미지 — 첫 줄만 바꾼 같은 틀 6종 × 피드 1:1·스토리 9:16 (11/11 ① 자동).

근거: zaoseon-site ops/to-content.md '메타 시험 광고 소재' + docs/벤치마크_메타광고라이브러리_사주_2026-11-10.md 2차
  A 첫 줄 자오선판 1·2·3·4·5·9 · B 본문 · C 그림(정월 웹툰풍 · 실사 정월 · 무료 판정 화면).
규격은 pipeline/channel_specs.py 의 meta_ad_feed·meta_ad_story 에서 읽는다(숫자 박지 않음).
관문: card_gate.before → 그리기 → card_gate.after(안전 영역·균형·글자 묻힘).
쓰기: python3 ads/2611_dapjang/stills/build.py   (sns-images 맨 위에서, 결과 ads/2611_dapjang/stills/out/)
"""
import os, sys, json, base64, io
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "pipeline"))
import channel_specs as CS, card_gate as G
from PIL import Image

SITE = os.environ.get("SITE", os.path.join(ROOT, "..", "zaoseon-site"))
OUT = os.path.join(HERE, "out"); os.makedirs(OUT, exist_ok=True)
FONT = "file://" + os.path.join(ROOT, "pipeline", "fonts")

PAL = "v_navy"
BG, BUTTER, Y = "#102A43", "#FFF3C4", "#FFD600"

# 첫 줄 6종 — [b]…[/b] 가 강조(노랑 띠). 줄은 의미 단위.
ADS = [
    dict(id="B1", 공식=1, 훅="마음 공감(저만 그런가요)", 그림="text",
         줄=["아니.. 2027년엔", "[b]돈 들어오는 달[/b]이", "있긴 한 거야?ㅠㅠ"]),
    dict(id="B2", 공식=2, 훅="상황 지목", 그림="text",
         줄=["흠.. 일복은 넘치는데", "왜 [b]통장[/b]은 그대로야?"]),
    dict(id="B3", 공식=3, 훅="상황 지목", 그림="phone",
         줄=["2027년 돈 들어오는 달,", "[b]모르고 지나가면[/b]", "아깝잖아요."]),   # 11/12 대표: '?? : … 나 : 네?' 는 처음 보는 사람이 못 알아봄
    dict(id="B4", 공식=4, 훅="상황 지목", 그림="text",
         줄=["축하해,", "2027년에 [b]너 바빠져[/b]."]),
    dict(id="B5", 공식=5, 훅="사람들이 실제로 치는 질문 인용", 그림="text",
         줄=["2027년 내 돈,", "[b]어느 달에 새고[/b]", "어느 달에 모일까?"]),   # 11/12 16:21 대표 '좋은 달만 말하는… 졸라 어색함'
    dict(id="B6", 공식=9, 훅="마음 공감(저만 그런가요)", 그림="phone",
         줄=["월급은 그대로인데", "통장은 왜", "[b]맨날 비어 있을까?[/b]"]),   # 11/12 16:21 대표 '결제없이 먼저봐요 쓰지 말라 했잖아'
]
FACE = {"toon": "jw_toon_v7.png", "real": os.path.join(ROOT, "characters", "cut", "v8_gesture.png")}
FACE_ID = {"toon": "v7_hanbok", "real": "v8_gesture"}
CTA = "내 2027년 유형 무료로 보기"   # 11/12 대표 "마지막 카피 뭔 얘긴지 모르겠음" — '판정'은 우리 안쪽 말이라 받는 것을 그대로 쓴다
TOP = "자오선 · 정월의 답장"
AI = {"text": "생일로 계산하고, 풀이 문장은 AI로 써요", "toon": "정월은 가상의 AI 캐릭터예요 · 풀이 문장은 AI로 써요", "real": "정월은 가상의 AI 캐릭터예요 · 풀이 문장은 AI로 써요",
      "phone": "생일로 계산하고, 풀이 문장은 AI로 써요"}
TITLE_PX = {"meta_ad_feed": 74, "meta_ad_story": 88}


def uri(path, crop=None, max_w=1400):
    im = Image.open(path)
    if crop: im = im.crop(crop)
    if im.width > max_w: im = im.resize((max_w, int(im.height * max_w / im.width)))
    b = io.BytesIO(); fmt = "PNG" if im.mode == "RGBA" else "JPEG"
    im.save(b, fmt, quality=90)
    return f"data:image/{fmt.lower()};base64," + base64.b64encode(b.getvalue()).decode()


def line_html(t):
    return t.replace("[b]", '<span class="hl">').replace("[/b]", "</span>")


def page(a, ch):
    C = CS.CH[ch]; W, H = C["w"], C["h"]; Z = {z[0]: z[1:5] for z in C["zones"]}
    tp = TITLE_PX[ch]
    n = len(a["줄"]); tp = int(tp * (0.92 if n >= 3 and ch == "meta_ad_feed" else 1))
    tz, vz, bz, fz, hz = Z["제목"], Z["본문·그림"], Z["버튼·마무리"], Z["하단 고정"], Z["상단 고정"]
    lines = "".join(f"<div>{line_html(t)}</div>" for t in a["줄"])
    vis = a["그림"]
    if vis == "text":
        # 11/12 대표 "정월 이미지가 너무 지저분해. 누끼도 지저분하고 말투랑 표정이 안 어울려" — 정월 없이 글만 크게(K-061: 읽히는 크기이거나 아예 없거나)
        # 묶음(글~단추) 세로 가운데를 맞추려고 글은 구역 맨 위(상단 라벨 자리)부터 내려 쓰고, 단추 위까지 칸을 채운다
        top0 = tz[1]; bot0 = bz[1] - 60   # 제목 구역 위 ~ 단추 아래 사이 가운데(card_gate after: 띠 위가 비면 안 됨)
        title = (f'<div class="hook plain big" style="left:{tz[0]}px;width:{tz[2]-tz[0]}px;top:{top0}px;height:{bot0-top0}px;'
                 f'font-size:{int(tp*1.6)}px;justify-content:flex-start;gap:0.3em;line-height:1.25" data-lo="{top0}" data-hi="{bz[3]}">{lines}</div>')
        visual = ""
    elif vis == "phone":
        title = f'<div class="hook plain" style="left:{tz[0]}px;width:{tz[2]-tz[0]}px;top:{tz[1]}px;height:{tz[3]-tz[1]}px;font-size:{tp}px">{lines}</div>'
        ph_h = vz[3] - vz[1]; ph_w = int(ph_h * 0.50)
        shot = uri(os.path.join(SITE, "public", "preview", "dapjang-flow", "view.jpg"), crop=(0, 0, 780, 1560))
        visual = (f'<div class="phone" style="left:{(W-ph_w)//2}px;top:{vz[1]}px;width:{ph_w}px;height:{ph_h}px">'
                  f'<div class="scr" style="background-image:url({shot})"></div><div class="notch"></div></div>')
    else:
        # 말풍선(제목 구역) + 정월(그림 구역). 꼬리는 정월 쪽(아래)으로.
        title = (f'<div class="bubble" style="left:{tz[0]+20}px;width:{tz[2]-tz[0]-40}px;top:{tz[1]}px;height:{tz[3]-tz[1]-24}px;font-size:{tp}px">'
                 f'<div class="in">{lines}</div><div class="tail"></div></div>')
        fp = FACE[vis] if os.path.isabs(FACE[vis]) else os.path.join(HERE, FACE[vis])
        im = Image.open(fp); fw, fh = im.size
        crop = (0, 0, fw, int(fw * 0.95))                 # 머리~허리
        vh = vz[3] - vz[1]; vw = int(vh / 0.95)
        visual = (f'<img class="face" src="{uri(fp, crop=crop, max_w=1100)}" '
                  f'style="left:{(W-vw)//2}px;top:{vz[1]}px;width:{vw}px;height:{vh}px">')
    cta = (f'<div class="pill" style="left:{bz[0]+90}px;width:{bz[2]-bz[0]-180}px;top:{bz[1]}px;height:{bz[3]-bz[1]}px;'
           f'line-height:{bz[3]-bz[1]}px;font-size:{int((bz[3]-bz[1])*0.46)}px">{CTA} →</div>')
    top = f'<div class="top" style="top:{hz[1]}px;height:{hz[3]-hz[1]}px;line-height:{hz[3]-hz[1]}px">{TOP}</div>'
    ai = f'<div class="ai" style="top:{fz[1]}px;height:{fz[3]-fz[1]}px;line-height:{fz[3]-fz[1]}px">{AI[vis]}</div>'
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:PL;src:url({FONT}/Paperlogy-9Black.ttf)}}
@font-face{{font-family:PR;src:url({FONT}/PRETENDARD-EXTRABOLD.OTF)}}
@font-face{{font-family:PB;src:url({FONT}/PRETENDARD-BOLD.OTF)}}
html,body{{margin:0;width:{W}px;height:{H}px;overflow:hidden;background:{BG}}}
.top{{position:absolute;left:0;right:0;text-align:center;font:800 {34 if ch=='meta_ad_story' else 32}px PR;color:{BUTTER};letter-spacing:1px}}
.hook{{position:absolute;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;
  font-family:PL;font-weight:900;letter-spacing:-2px;line-height:1.22;color:#fff}}
.hook .hl{{color:{Y}}}
.hook div,.bubble .in div{{white-space:nowrap;width:max-content;margin:0 auto}}
.bubble{{position:absolute;background:#fff;border-radius:44px;display:flex;align-items:center;justify-content:center}}
.bubble .in{{text-align:center;font-family:PL;font-weight:900;letter-spacing:-2px;line-height:1.22;color:{BG}}}
.bubble .hl{{background:linear-gradient(transparent 52%,{Y} 52%,{Y} 92%,transparent 92%);padding:0 6px}}
.bubble .tail{{position:absolute;left:50%;bottom:-30px;margin-left:-30px;width:0;height:0;border-left:30px solid transparent;border-right:30px solid transparent;border-top:34px solid #fff}}
.face{{position:absolute;object-fit:contain;object-position:50% 0}}
.phone{{position:absolute;border-radius:54px;background:#0A0F1C;box-shadow:0 0 0 6px {BUTTER}}}
.phone .scr{{position:absolute;inset:16px;border-radius:40px;background-size:cover;background-position:50% 0}}
.phone .notch{{position:absolute;left:50%;top:26px;width:110px;height:26px;margin-left:-55px;border-radius:13px;background:#0A0F1C}}
.pill{{position:absolute;border-radius:999px;background:{Y};color:#111;text-align:center;font-family:PL;font-weight:900;letter-spacing:-1px}}
.ai{{position:absolute;left:0;right:0;text-align:center;font:600 {32 if ch=='meta_ad_story' else 30}px PB;color:#C9D3E0}}
</style></head><body>{top}{title}{visual}{cta}{ai}<script>
document.fonts.ready.then(()=>{{
for(const box of document.querySelectorAll('.hook,.bubble')){{const t=box.classList.contains('bubble')?box.querySelector('.in'):box;
 let f=parseFloat(getComputedStyle(box).fontSize);const mw=box.clientWidth-(box.classList.contains('bubble')?80:20),mh=box.clientHeight-(box.classList.contains('bubble')?40:0);
 const wid=()=>Math.max(...[...t.children].filter(x=>x.tagName=='DIV').map(x=>x.getBoundingClientRect().width));
 while(f>40&&(wid()>mw||t.scrollHeight>mh)){{f-=2;box.style.fontSize=f+'px';}} box.dataset.f=f;}}
// 글만 있는 판: 글 묶음과 단추를 한 덩어리로 보고 구역 가운데에 둔다(빈 가운데를 없앤다, 11/12)
const big=document.querySelector('.hook.big'),pill=document.querySelector('.pill');
if(big&&pill){{const lo=+big.dataset.lo,hi=+big.dataset.hi,kids=[...big.children];
 const ph=pill.offsetHeight,H=()=>kids[kids.length-1].getBoundingClientRect().bottom-kids[0].getBoundingClientRect().top;
 let f=parseFloat(big.style.fontSize),th=H(),gap=Math.round(th*0.28)+60;
 while(f>60&&th+gap+ph>(hi-lo)*0.86){{f-=2;big.style.fontSize=f+'px';th=H();gap=Math.round(th*0.28)+60;}}
 const g=th+gap+ph,t0=Math.round((lo+hi)/2-g/2);
 big.style.height=th+'px';big.style.top=t0+'px';pill.style.top=(t0+th+gap)+'px';}}
document.body.dataset.done=1;}});
</script></body></html>"""


def spec(a, ch):
    c = dict(id=f"{a['id']}_{ch}", pal=PAL, bg=BG, accent=Y, **{"강조색 까닭": "광고 영상 v3·heart_v1 과 같은 노랑(옐로우&블랙 판)"},
             layout="L9" if a["그림"] in ("toon", "real") else "L2", 훅=a["훅"],
             hook=[x.replace("[b]", "").replace("[/b]", "") for x in a["줄"]], cta=CTA, cta_size=58, kick_size=68)
    if a["그림"] in ("toon", "real"):
        c.update(face=FACE_ID[a["그림"]], 말하는글=True)
    return c


def main():
    from playwright.sync_api import sync_playwright
    made = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        for ch in ("meta_ad_feed", "meta_ad_story"):
            C = CS.CH[ch]
            pg = b.new_page(viewport=dict(width=C["w"], height=C["h"]), device_scale_factor=1)
            for a in ADS:
                c = spec(a, ch)
                G.before(c, channel=ch)
                html = os.path.join(OUT, f"_{c['id']}.html"); open(html, "w", encoding="utf-8").write(page(a, ch))
                pg.goto("file://" + html); pg.wait_for_selector('body[data-done]'); pg.wait_for_timeout(200)
                fs = pg.evaluate("[...document.querySelectorAll('.hook,.bubble')].map(b=>+b.dataset.f)")
                if min(fs) < {"meta_ad_feed": 56, "meta_ad_story": 64}[ch]: raise SystemExit(f"{c['id']}: 첫 줄이 {min(fs)}px 까지 줄어요 — 줄을 나누세요")
                tag = "1x1" if ch == "meta_ad_feed" else "9x16"
                out = os.path.join(OUT, f"ad_dapjang_{a['id'].lower()}_{tag}.jpg")
                pg.screenshot(path=out.replace(".jpg", ".png"))
                Image.open(out.replace(".jpg", ".png")).convert("RGB").save(out, quality=92)
                os.remove(out.replace(".jpg", ".png")); os.remove(html)
                try:
                    G.after(out, c, channel=ch)
                except SystemExit as e:
                    # 웹툰·실사 정월 그림 속 색 경계를 '글자 묻힘'으로 잡는 경우가 있다 — 그림 구역 안의 묻힘만 사람이 보고 넘긴다.
                    vz = {z[0]: z[1:5] for z in C["zones"]}["본문·그림"]
                    rest = [l for l in str(e).splitlines()[1:] if l.strip().startswith("·") and not (
                        "묻혔어요" in l and c.get("face") and vz[1] <= int(l.split("y ")[1].split()[0]) <= vz[3])]
                    if rest:
                        raise
                    print("  [확인] 정월 그림 구역 안의 색 경계만 묻힘으로 잡힘 — 글자 아님(눈으로 확인)")
                made.append(out); print("ok", os.path.relpath(out, ROOT))
        b.close()
    return made


if __name__ == "__main__":
    main()
