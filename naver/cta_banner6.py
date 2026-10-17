"""네이버 글 맨 아래 CTA 배너 낮은 판 (10/17 14:58 대표 "CTA 배너가 그냥 봐도 크다").

5판(naver_cta5, 1280x400)은 본문 폭 886px에서 886x276으로 보여 글줄보다 크게 도드라졌다(서브 노트북 실측).
6판은 높이를 낮추고(1280x240) 글줄과 단추를 옆으로 나란히 둔다. 폭이 같아 키트는 바꿀 것이 없다.
크기·안전 영역·구역·최소 글자 크기는 pipeline/channel_specs.py 의 'naver_cta_banner6' 에서 읽는다(숫자를 여기 박지 않는다).
판은 5판과 같은 assets/palettes/color_combos.json 의 k_gold.

naver/img 규칙: 이미 발행한 글이 옛 배너 주소를 링크로 쓰므로 옛 파일은 건드리지 않고 **새 이름(naver_cta6_)으로만** 추가한다.
만들기: python3 naver/cta_banner6.py   (img/ 원본과 img/m1280/ 납품판 두 곳에 같은 그림)
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "pipeline"))
import channel_specs as CS, fonts_kit as FK, card_gate as G
from PIL import Image, ImageDraw, ImageFont

CHN = "naver_cta_banner6"
NAME = "naver_cta6_1초무료풀이.jpg"
PAL = "k_gold"
TITLE = "생년월일만 넣으면 1초"
SUB = "내 기운과 2027년 한 줄 풀이, 무료"
BTN = "무료로 보기"
WANT = dict(title=66, body=46, label=50)   # 바람. 실제 크기는 구역 폭에 맞춰 줄이되 min_px 밑으로는 안 내려간다


def _hex(h): h = h.lstrip("#"); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _fit(d, text, key, want, low, room):
    s = want
    while s > low and d.textlength(text, font=ImageFont.truetype(FK.P[key], s)) > room: s -= 1
    f = ImageFont.truetype(FK.P[key], s)
    if d.textlength(text, font=f) > room:
        raise SystemExit(f"[배너] '{text}' 가 {low}px 로도 {room}px 폭에 안 들어가요. 문구를 줄이세요.")
    return s, f


def build(out_dirs=("img", "img/m1280")):
    S = CS.CH[CHN]; W, H = S["w"], S["h"]; MIN = S["min_px"]
    bad = CS.check(CHN)
    if bad: raise SystemExit("[배너] 규격 이상: " + " / ".join(bad))
    Z = {z[0]: z[1:5] for z in S["zones"]}
    T = {p["id"]: p for p in json.load(open(os.path.join(ROOT, "assets", "palettes", "color_combos.json"), encoding="utf-8"))["palettes"]}[PAL]["theme"]
    bg, ink, acc = _hex(T["bg"]), _hex(T["ink"]), _hex(T["acc"])
    for f_ in ("pl_blk", "pr_xb"):
        miss = FK.missing(f_, TITLE + SUB + BTN)
        if miss: raise SystemExit(f"[배너] {f_} 글꼴에 없는 글자: {''.join(miss)}")
    if G.contrast(T["acc"], T["bg"]) < 3.0 or G.contrast(T["ink"], T["bg"]) < 4.5 or G.contrast(T["bg"], T["acc"]) < 4.5:
        raise SystemExit("[배너] 글자 대비가 모자라요.")

    img = Image.new("RGB", (W, H), bg); d = ImageDraw.Draw(img)
    tz, bz, kz = Z["제목"], Z["본문·그림"], Z["버튼(오른쪽)"]
    ts, tf = _fit(d, TITLE, "pl_blk", WANT["title"], MIN["title"], tz[2] - tz[0])
    bs, bf = _fit(d, SUB, "pr_xb", WANT["body"], MIN["body"], bz[2] - bz[0])
    ls, lf = _fit(d, BTN, "pr_xb", WANT["label"], MIN["label"], (kz[2] - kz[0]) - 80)
    d.text((tz[0], (tz[1] + tz[3]) // 2), TITLE, font=tf, fill=acc, anchor="lm")
    d.text((bz[0], (bz[1] + bz[3]) // 2), SUB, font=bf, fill=ink, anchor="lm")
    d.rounded_rectangle([kz[0], kz[1], kz[2], kz[3]], (kz[3] - kz[1]) // 2, fill=acc)
    d.text(((kz[0] + kz[2]) // 2, (kz[1] + kz[3]) // 2), BTN + " →", font=lf, fill=bg, anchor="mm")
    outs = []
    for od in out_dirs:
        p = os.path.join(HERE, od, NAME); os.makedirs(os.path.dirname(p), exist_ok=True)
        if os.path.exists(p) and os.environ.get("ZS_CTA_REBUILD") != "1":
            raise SystemExit(f"[배너] {p} 가 이미 있어요. naver/img 는 덮어쓰지 않아요 — 새 판이면 이름(번호)을 올리세요.")
        img.save(p, quality=95, subsampling=0, optimize=True); outs.append(p)
    return dict(files=outs, size=(W, H), title_px=ts, sub_px=bs, button_px=ls,
                phone_px=dict(title=round(ts * 0.28, 1), sub=round(bs * 0.28, 1), button=round(ls * 0.28, 1)))


if __name__ == "__main__":
    print(build())
