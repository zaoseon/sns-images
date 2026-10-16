"""인스타·스레드 표지를 네이버 표지와 같은 문법으로 만든다 (K-061·K-068·K-072, 대표 10/16 승인).

왜 따로 만드나: 지금 인스타 빌더(2026-w44night7/build.py 등)는 bg='ink' 와 FACE() 가
코드에 박혀 있고 assets/palettes/color_combos.json 을 아예 안 읽는다. 그래서 K-058~062 가
10/16 새벽에 적혔는데도 같은 날 밤 캐러셀이 어겼다. 네이버 쪽이 이미 쓰는
naver/cover_v3.py 의 '정월 없는 표지' 틀 여섯 가지를 그대로 불러 쓴다.
그쪽 파일은 고치지 않는다(세션 담당: naver/ 는 네이버 세션).

틀: nf_text(QL·QC) · nf_ring(ring) · nf_big(BIG) · nf_n(N) · nf_trio(trio) · nf_cal(cal)
판: cover_v3.ALL_S (대표가 캡처로 준 '메인 색 + 다른 색' 조합, K-068)
크기: wide=False -> 720x720. 인스타 4:5(1080x1350)로 늘려 저장한다(격자에서 더 큼).

사용: python3 2026-igcover/build.py           # cards.json 전부
      python3 2026-igcover/build.py ig1016a   # 하나만
"""
import os, sys, json
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(ROOT, "naver"))
import cover_v3 as V

OUT = os.path.join(HERE, "cards")
SPEC = os.path.join(HERE, "cards.json")


def to_tall(sq_path, out_path, bg, H=1440):
    """정사각 표지를 캐러셀과 같은 1080x1440 으로. 빈 띠가 크게 남지 않게 정사각을 키워 넣고
    위아래를 조금씩 잘라 낸다(글자는 가운데 모여 있어 잘리지 않는다). 남는 띠는 판 바탕색."""
    sq = Image.open(sq_path).convert("RGB")
    # 틀 안에서 글자·칸이 쓰는 폭은 1080 중 900 쯤이다. 1240 까지 키워야 900*1.148=1033 로
    # 1080 안에 남는다. 더 키우면 N 틀의 칩 양 끝이 잘린다(10/16 확인).
    side = int(H * 0.861)                      # 1239
    big = sq.resize((side, side), Image.LANCZOS)
    can = Image.new("RGB", (1080, H), bg)
    can.paste(big, ((1080 - side) // 2, (H - side) // 2))
    can.save(out_path, quality=94, subsampling=0)


def face_big(cid, c, T, out, H=1440, W=1080):
    """정월이 '말하는 사람'인 표지(모집·공지·인사)용 — K-061 의 '전면, 크게'.
    기존 틀의 작은 원형 배지는 대표 10/16 지적대로 얼굴도 안 보이고 글자 자리만 뺏는다.
    그래서 컷을 오른쪽 아래에 거의 원래 크기로 두고, 글자는 왼쪽 위에 왼쪽 정렬로 쌓는다.
    정월이 보이므로 AI 고지를 반드시 넣는다."""
    from PIL import ImageDraw
    import thumb_sq as TQ
    F, SER, SEMI, BLK, XB = TQ.F, TQ.SER, TQ.SEMI, TQ.BLK, getattr(TQ, "XB", TQ.BLK)
    img = Image.new("RGB", (W, H), c.bg)

    cut = Image.open(os.path.join(ROOT, "characters", "cut", T.get("face", "v5_halfup_v2") + ".png")).convert("RGBA")
    fh = int(H * T.get("face_h", 0.62))
    cut = cut.resize((int(cut.width * fh / cut.height), fh), Image.LANCZOS)
    img.paste(cut, (W - cut.width + T.get("face_dx", 40), H - cut.height), cut)

    d = ImageDraw.Draw(img)
    x, y = 72, 96
    kt = T["kick"]; kf = F(SEMI, 46); kw = d.textlength(kt, font=kf)
    d.rounded_rectangle([x, y, x + kw + 56, y + 76], 38, fill=c.pill)
    d.text((x + 28, y + 38), kt, font=kf, fill=c.pillfg, anchor="lm"); y += 118

    for l in T["hook"]:
        d.text((x, y), l, font=F(SEMI, 62), fill=c.fg, anchor="la"); y += 78
    y += 18

    # 글자는 왼쪽 기둥 안에만 둔다. 정월 위로 넘어가면 둘 다 안 읽힌다(10/16 첫 판에서 '명'이 머리에 겹쳤다).
    tw = int(W * T.get("text_w", 0.58)) - x
    bs = 300
    while d.textlength(T["big"], font=F(BLK, bs)) > tw and bs > 110: bs -= 6
    d.text((x, y), T["big"], font=F(BLK, bs), fill=c.acc, anchor="la"); y += int(bs * 1.06) + 16

    subs = T.get("subs", [])
    ss = 46                                   # 부제도 기둥 안에 넣는다. 넘치면 머리카락 위로 올라가 안 읽힌다
    while subs and max(d.textlength(l, font=F(SEMI, ss)) for l in subs) > tw and ss > 30: ss -= 2
    for l in subs:
        d.text((x, y), l, font=F(SEMI, ss), fill=c.fg, anchor="la"); y += int(ss * 1.35)

    d.text((x, H - 62), "정월은 AI로 생성한 가상 캐릭터입니다", font=F(SEMI, 28), fill=c.fg, anchor="ls")
    d.text((x, H - 112), "子午線 자오선", font=F(SER, 42), fill=c.acc, anchor="ls")
    img.save(out, quality=94, subsampling=0)
    return out


def main():
    os.makedirs(OUT, exist_ok=True)
    spec = json.load(open(SPEC, encoding="utf-8"))
    want = sys.argv[1:]
    made = []
    for i, c in enumerate(spec["cards"]):
        cid = c["id"]
        if want and cid not in want:
            continue
        pal = c.get("pal") or V.ALL_S[i % len(V.ALL_S)]
        T = {k: v for k, v in c.items() if k not in ("id", "pal", "note")}
        if c["d"] == "face_big":                       # 정월 전면(모집·공지·인사) — 정사각을 거치지 않는다
            p = os.path.join(OUT, cid + ".jpg")
            face_big(cid, V.Ctx(pal), T, p)
            made.append((cid, pal, c["d"])); print(f"  {cid:12s} {pal:12s} {c['d']:9s} -> {os.path.relpath(p, ROOT)}")
            continue
        sqp = os.path.join(OUT, cid + "_sq.jpg")
        V.render(cid, T, sqp, pal=pal, wide=False, face_on=bool(c.get("face_on")))
        ctx = V.Ctx(pal)
        p45 = os.path.join(OUT, cid + ".jpg")
        to_tall(sqp, p45, ctx.bg)
        made.append((cid, pal, c["d"]))
        print(f"  {cid:12s} {pal:12s} {c['d']:5s} -> {os.path.relpath(p45, ROOT)}")
    print(f"\n{len(made)}장 만들었어요.")


if __name__ == "__main__":
    main()
