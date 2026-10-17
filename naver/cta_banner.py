"""네이버 글 맨 아래 CTA 배너 (10/17 대표, 서브 노트북 점검 결과 3절).

옛 배너(naver_cta4, 1280x229 납품판)는 폰(가로 360px)에서 높이 64px, 제목 8px, 부제 4.5px로 줄어 읽을 수 없었다.
새 배너는 1280x400(약 3:1), 제목 57px 이상·부제 50px 이상, 좌우 여백을 줄여 글자 폭을 넓힌다.
크기·안전 영역·구역·최소 글자 크기는 pipeline/channel_specs.py 의 'naver_cta_banner' 에서 읽는다(숫자를 여기 박지 않는다).
판은 assets/palettes/color_combos.json 의 k_gold(블랙 & 골드, 자오선 기본 배너 색과 같은 역할).

naver/img 규칙: 이미 발행한 글이 옛 배너 주소를 링크로 쓰므로 옛 파일은 건드리지 않고 **새 이름(naver_cta5_)으로만** 추가한다.
만들기: python3 naver/cta_banner.py   (img/ 원본과 img/m1280/ 납품판 두 곳에 같은 그림)
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "pipeline"))
import channel_specs as CS, fonts_kit as FK, card_gate as G
from PIL import Image, ImageDraw, ImageFont

NAME = "naver_cta5_1초무료풀이.jpg"
PAL = "k_gold"
TITLE = "생년월일만 넣으면 1초면 돼요"
SUB = "내 기운과 2027년 한 줄 풀이, 무료"
BTN = "1초 만에 내 기운 보기"
WANT = dict(title=78, body=56, label=56)   # 바람. 실제 크기는 구역 폭에 맞춰 줄이되 min_px 밑으로는 안 내려간다


def _hex(h): h = h.lstrip("#"); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _fit(d, text, key, want, low, room):
    s = want
    while s > low and d.textlength(text, font=ImageFont.truetype(FK.P[key], s)) > room: s -= 1
    f = ImageFont.truetype(FK.P[key], s)
    if d.textlength(text, font=f) > room:
        raise SystemExit(f"[배너] '{text}' 가 {low}px 로도 {room}px 폭에 안 들어가요. 문구를 줄이세요.")
    return s, f


def build(out_dirs=("img", "img/m1280")):
    S = CS.CH["naver_cta_banner"]; W, H = S["w"], S["h"]; MIN = S["min_px"]
    Z = {z[0]: z[1:5] for z in S["zones"]}
    T = {p["id"]: p for p in json.load(open(os.path.join(ROOT, "assets", "palettes", "color_combos.json"), encoding="utf-8"))["palettes"]}[PAL]["theme"]
    bg, ink, acc = _hex(T["bg"]), _hex(T["ink"]), _hex(T["acc"])
    c = {"id": "naver-cta5", "pal": PAL, "bg": T["bg"], "accent": T["acc"], "kick_size": WANT["title"], "layout": "L1",
         "훅": "빠른 이해(1분이면)", "hook": [TITLE], "subs": [SUB], "cta": BTN}
    G.before(c, channel="naver_cta_banner")   # 판·대비·글말·구역 높이 — 걸리면 멈춘다
    for f_ in ("pl_blk", "pr_xb"):
        miss = FK.missing(f_, TITLE + SUB + BTN)
        if miss: raise SystemExit(f"[배너] {f_} 글꼴에 없는 글자: {''.join(miss)}")
    if G.contrast(T["acc"], T["bg"]) < 3.0 or G.contrast(T["ink"], T["bg"]) < 4.5 or G.contrast(T["bg"], T["acc"]) < 4.5:
        raise SystemExit("[배너] 글자 대비가 모자라요.")

    img = Image.new("RGB", (W, H), bg); d = ImageDraw.Draw(img)
    x0, x1 = Z["제목"][0], Z["제목"][2]; room = x1 - x0
    ts, tf = _fit(d, TITLE, "pl_blk", WANT["title"], MIN["title"], room)
    bs, bf = _fit(d, SUB, "pr_xb", WANT["body"], MIN["body"], room)
    ls, lf = _fit(d, BTN, "pr_xb", WANT["label"], MIN["label"], room - 160)
    cx = (x0 + x1) // 2
    d.text((cx, (Z["제목"][1] + Z["제목"][3]) // 2), TITLE, font=tf, fill=acc, anchor="mm")
    d.text((cx, (Z["본문·그림"][1] + Z["본문·그림"][3]) // 2), SUB, font=bf, fill=ink, anchor="mm")
    by0, by1 = Z["버튼·마무리"][1] + 6, Z["버튼·마무리"][3] - 6
    bw = int(d.textlength(BTN, font=lf)) + 140
    d.rounded_rectangle([cx - bw // 2, by0, cx + bw // 2, by1], (by1 - by0) // 2, fill=acc)
    d.text((cx, (by0 + by1) // 2), BTN, font=lf, fill=bg, anchor="mm")
    outs = []
    for od in out_dirs:
        p = os.path.join(HERE, od, NAME); os.makedirs(os.path.dirname(p), exist_ok=True)
        if os.path.exists(p) and os.environ.get("ZS_CTA_REBUILD") != "1":
            raise SystemExit(f"[배너] {p} 가 이미 있어요. naver/img 는 덮어쓰지 않아요 — 새 판이면 이름(번호)을 올리세요.")
        img.save(p, quality=95, subsampling=0, optimize=True); outs.append(p)
    G.after(outs[0], c, channel="naver_cta_banner")
    return dict(files=outs, size=(W, H), title_px=ts, sub_px=bs, button_px=ls)


if __name__ == "__main__":
    print(build())
