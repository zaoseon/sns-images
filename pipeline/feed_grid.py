"""피드 격자를 보고 판을 고른다 — 대표 10/16 "피드 감안해서 컬러조합 만들어야한다".

왜 필요한가
  K-068(판 연속 금지)은 **시간 순서**만 본다. 그런데 사람은 프로필에서 **3열 격자**로 본다.
  격자에서는 옆(i±1)과 위아래(i±3)가 닿는다. 시간 순서로는 안 겹쳐도 격자에서는 뭉칠 수 있다.
  10/16 일간 2회차 열 편이 그랬다 — 어두운 판 7개에 거의 같은 검정이 넷이라 덩어리로 보였다.

규칙(K-111)
  ① 밝음·어두움이 바둑판으로 엇갈린다(닿는 칸끼리 밝기 차 0.35 이상)
  ② 거의 같은 색(밝기도 색상도 비슷한 판)은 격자에서 **안 닿는 자리**에 둔다
  ③ 인스타 격자는 최신이 왼쪽 위다 — 발행 순서를 뒤집어서 본다

사용: python3 pipeline/feed_grid.py 2026-ilgan2      검사만
      python3 pipeline/feed_grid.py 2026-ilgan2 --png 격자 그림까지
"""
import os, sys, json, colorsys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
COLS = 3
밝기차 = 0.35      # 닿는 칸끼리 이만큼은 갈려야 한다
같은색 = (0.12, 30)  # (밝기 차, 색상 차) 둘 다 이보다 작으면 '거의 같은 색'


def _pal():
    j = json.load(open(os.path.join(ROOT, "assets", "palettes", "color_combos.json"), encoding="utf-8"))
    return {x["id"]: x for x in j["palettes"]}


def _lum(h):
    h = str(h).lstrip("#"); r, g, b = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    f = lambda c: c / 12.92 if c <= .04045 else ((c + .055) / 1.055) ** 2.4
    return .2126 * f(r) + .7152 * f(g) + .0722 * f(b)


def _hue(h):
    h = str(h).lstrip("#"); r, g, b = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return colorsys.rgb_to_hsv(r, g, b)[0] * 360


def 이웃(n):
    """3열 격자에서 서로 닿는 자리 쌍(0부터)."""
    쌍 = []
    for i in range(n):
        if i % COLS != COLS - 1 and i + 1 < n: 쌍.append((i, i + 1))     # 옆
        if i + COLS < n: 쌍.append((i, i + COLS))                        # 아래
    return 쌍


def check(cards):
    """발행 순서대로 받은 카드 목록을 격자로 놓고 본다. 걸리는 까닭 목록."""
    P = _pal()
    격자 = list(reversed(cards))        # 인스타는 최신이 왼쪽 위
    색 = []
    for c in 격자:
        v = P.get(c.get("pal"))
        bg = v["theme"]["bg"] if v else "#000000"
        색.append((c.get("id", "?"), c.get("pal"), _lum(bg), _hue(bg)))
    bad = []
    for a, b in 이웃(len(색)):
        ida, pa, la, ha = 색[a]; idb, pb, lb, hb = 색[b]
        d밝 = abs(la - lb); d색 = min(abs(ha - hb), 360 - abs(ha - hb))
        if d밝 < 같은색[0] and d색 < 같은색[1]:
            bad.append(f"격자에서 닿는 {ida}({pa})와 {idb}({pb})가 거의 같은 색이에요 "
                       f"(밝기 차 {d밝:.2f} · 색상 차 {d색:.0f}). 한 칸은 다른 쪽으로 바꾸세요.")
        elif d밝 < 밝기차:
            bad.append(f"격자에서 닿는 {ida}({pa})와 {idb}({pb})의 밝기가 비슷해요 "
                       f"(차 {d밝:.2f}, {밝기차} 이상 권장). 밝음·어두움을 엇갈리게 두세요.")
    return bad


def png(set이름, cards, out=None):
    """격자 그림을 만든다 — 눈으로 봐야 보이는 것이 있다."""
    from PIL import Image
    셀 = []
    for c in reversed(cards):
        p = os.path.join(ROOT, set이름, "cards_reel", c["id"] + ".jpg")
        if not os.path.exists(p):
            p = os.path.join(ROOT, set이름, "cards", c["id"] + ".jpg")
        im = Image.open(p); w, h = im.size
        ch = int(w * 5 / 4); top = max(0, (h - ch) // 2)
        셀.append(im.crop((0, top, w, min(h, top + ch))).resize((240, 300)))
    rows = (len(셀) + COLS - 1) // COLS
    g = Image.new("RGB", (240 * COLS + 8 * (COLS - 1), 300 * rows + 8 * (rows - 1)), (255, 255, 255))
    for k, c in enumerate(셀):
        g.paste(c, ((k % COLS) * 248, (k // COLS) * 308))
    out = out or os.path.join(ROOT, set이름, "feed_grid.jpg")
    g.save(out, quality=90)
    return out


def main():
    s = sys.argv[1] if len(sys.argv) > 1 else "2026-ilgan2"
    cards = json.load(open(os.path.join(ROOT, s, "cards.json"), encoding="utf-8"))["cards"]
    bad = check(cards)
    print(f"{s} · {len(cards)}장 · 3열 격자 검사")
    for x in bad:
        print("  ", x)
    print("  통과 ✓" if not bad else f"  걸림 {len(bad)}건")
    if "--png" in sys.argv:
        print("  격자 그림:", os.path.relpath(png(s, cards), ROOT))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
