"""에셋 라이브러리 — 대표 10/16 "배경이나 에셋 라이브러리처럼 만들어놓고 이거저거 골라서 쓰도록 하라고".

그동안 빌더마다 쓸 그림을 코드에 박아 뒀다(배경은 우주 고리 한 장, 정월은 같은 컷).
그래서 아무리 색을 바꿔도 양산형으로 읽혔다(K-071). 이제 가진 것을 한 카탈로그로 모아
두고 골라 쓴다. 폴더에 파일을 더 넣으면 선택지가 저절로 는다 — 코드를 고치지 않는다.

담는 것
  배경(bg)      assets/brand_bg/scenes/*.jpg     짜임이 서로 다른 9:16 배경. pipeline/bg_make.py 가 만든다
  장식(deco)    assets/brand_bg/derived/*.png    해·달 같은 큰 소재
  정월(face)    characters/cut/*.png             금지 컷은 sns-studio/brands/zaoseon.json 이 정한다
  아이콘(icon)  assets/icons/lucide/*.svg        2,000개 남짓
  일러스트      assets/illust/undraw/*.svg        1,700개 남짓

쓰는 법
    import asset_lib as A
    A.pick("bg", "n33")           # 이름으로 고른다 — 같은 이름은 늘 같은 것, 이웃은 다른 것(K-068)
    A.pick("face", "n33", 금지=True)   # 금지 컷을 빼고 고른다
    A.list("bg")                  # 쓸 수 있는 것 전부
    A.index()                     # 카탈로그 전체(운영앱·문서에서 본다)

고르는 방식은 '이름 해시'다. 무작위가 아니라서 같은 글을 다시 그리면 같은 그림이 나오고,
이웃한 글끼리는 다른 그림이 나온다.
"""
import os, json, glob, functools

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))

곳 = {
    "bg":     ("assets/brand_bg/scenes", ".jpg", "9:16 배경. 짜임이 서로 다르다. 색은 판이 입힌다"),
    "deco":   ("assets/brand_bg/derived", ".png", "해·달 같은 큰 장식 소재"),
    "face":   ("characters/cut", ".png", "정월 컷. 금지 컷은 brands/zaoseon.json"),
    "icon":   ("assets/icons/lucide", ".svg", "선 아이콘"),
    "illust": ("assets/illust/undraw", ".svg", "사람·상황 일러스트"),
}


@functools.lru_cache(maxsize=16)
def list(kind):
    """그 갈래에서 쓸 수 있는 것의 이름 목록(확장자 없이), 늘 같은 차례로."""
    d, ext, _ = 곳[kind]
    fs = sorted(glob.glob(os.path.join(ROOT, d, "*" + ext)))
    out = [os.path.splitext(os.path.basename(f))[0] for f in fs]
    return tuple(x for x in out if not x.isupper() and x not in ("README", "LICENSE", "LICENCE"))


def path(kind, name):
    d, ext, _ = 곳[kind]
    return os.path.join(ROOT, d, name + ext)


@functools.lru_cache(maxsize=1)
def _금지컷():
    try:
        B = json.load(open(os.path.join(ROOT, "sns-studio", "brands", "zaoseon.json"), encoding="utf-8"))
        ch = B.get("character", {})
        return tuple(os.path.splitext(x)[0] for x in ch.get("forbidden", []))
    except Exception:
        return ()


def pick(kind, 이름, 금지=True, 몫=1):
    """글 이름으로 하나 고른다. 무작위가 아니라 해시라 되돌려 그려도 같은 것이 나온다.
    몫을 바꾸면 같은 이름에서 다른 것을 뽑는다(한 글에 배경과 장식을 따로 고를 때)."""
    본 = [x for x in list(kind)]
    if kind == "face" and 금지:
        본 = [x for x in 본 if x not in _금지컷() and not x.startswith("bg_")]
    if not 본:
        return None
    h = sum(ord(c) * (i + 3) for i, c in enumerate(str(이름))) * 몫
    return 본[h % len(본)]


# ── 바탕 고르는 표 (대표 10/16 "콘텐츠 기획하면서 ... 구성안에 따라 저 배경을 쓸지 단색을 쓸지 등을 정해야한다")
# 바탕은 해시로 아무거나 고르는 게 아니라 **무엇을 말하는 글이냐**가 정한다.
#   단색  글이 많거나 숫자·표를 읽혀야 할 때. 배경이 있으면 읽는 데 방해가 된다
#   배경  분위기로 멈춰 세워야 할 때(훅·위로·한 문장). 글이 적어야 쓴다
#   사진  정월이 말하는 글(모집·공지·인사). 정월이 장면 안에 있어야 할 때
바탕표 = {
    "훅·질문 표지":        ("배경", "첫 1초에 분위기로 멈춰 세운다. 글이 두세 줄뿐이라 배경이 방해하지 않는다"),
    "한 줄 운세·위로":      ("배경", "한 문장만 있는 글. 여백과 분위기가 내용이다"),
    "저장 유도 체크리스트":  ("단색", "항목을 세어 읽어야 한다. 배경이 있으면 줄이 안 읽힌다"),
    "여섯 운명학 교차 결과": ("단색", "숫자·표가 주인공이다. 배경과 겨루면 숫자가 죽는다"),
    "오해 교정":           ("단색", "앞뒤를 비교해 읽는 글. 바탕이 조용해야 한다"),
    "띠·별자리 순위":       ("단색", "순위를 세어 읽는다"),
    "정월의 상담실":        ("사진", "정월이 말하는 글. 정월이 장면 안에 있어야 한다"),
    "CTA·상품 안내":        ("사진", "모집·공지는 사람이 말해야 믿긴다(K-061 정월은 말하는 사람일 때만)"),
}
바탕기본 = ("단색", "정하지 않았으면 단색. 글이 먼저 읽히는 쪽으로 기운다")


def 바탕(내용유형=None, 적은것=None):
    """이 글의 바탕을 무엇으로 할지. 사양에 '바탕'을 적었으면 그것이 먼저다(기획이 이긴다)."""
    if 적은것:
        return (적은것, "사양에 직접 적음")
    return 바탕표.get(내용유형 or "", 바탕기본)


# ── 판 고르는 표 (대표 10/16 "컬러 조합도 마찬가지다")
# 판도 해시로 아무거나 고르지 않는다. **무엇을 말하는 글이냐**가 먼저 후보를 좁히고,
# 그 안에서 이름 해시로 돌린다(K-068 이웃끼리 같은 판 금지). 사양에 적으면 그것이 이긴다.
# 후보는 전부 assets/palettes/color_combos.json 안의 승인된 판이다 — 임의 HEX 를 쓰지 않는다.
판표 = {
    "훅·질문 표지":        (["p_black_s", "k_neon", "y_black_d", "m_young"],
                         "첫 1초에 스크롤을 세워야 한다. 대비가 가장 센 판"),
    "여섯 운명학 교차 결과": (["k_white_s", "y_gray_s", "k_white", "p_black_s"],
                         "숫자·표가 주인공. 바탕이 조용하고 강조 하나만 튀는 판"),
    "저장 유도 체크리스트":  (["g_ivory_s", "y_olive_s", "w_navy", "k_white_s"],
                         "여러 줄을 차분히 읽는다. 눈이 안 피로한 판"),
    "오해 교정":           (["k_white_s", "y_gray_s", "g_ivory_s"],
                         "앞뒤 비교. 색이 끼어들면 비교가 흐려진다"),
    "띠·별자리 순위":       (["y_black_d", "y_olive_s", "p_purple_s"],
                         "순위는 밝고 또렷하게"),
    "한 줄 운세·위로":      (["dg_gold_s", "g_ivory_s", "m_soft", "w_ink"],
                         "한 문장만 남는 글. 차분하고 깊은 판"),
    "정월의 상담실":        (["dg_gold_s", "k_gold", "m_young"],
                         "사람이 말하는 글. 정월 컷이 얹히므로 어두운 판"),
    "CTA·상품 안내":        (["dg_gold_s", "k_gold", "p_black_s"],
                         "값을 치르는 결정. 프리미엄으로 읽히는 판(K-076 정월 누끼는 어두운 판에만)"),
}
판기본 = (["g_ivory_s", "dg_gold_s", "k_white_s", "p_black_s", "y_black_d"],
         "정하지 않았으면 기본 다섯에서 돌린다")


def 판(내용유형=None, 적은것=None, 이름="", 쓴판=()):
    """이 글의 판을 고른다. 사양에 적었으면 그것이 먼저(기획이 이긴다).
    아니면 글 종류가 후보를 좁히고, 그 안에서 이름 해시로 고르되 최근에 쓴 판은 건너뛴다(K-068).
    돌려주는 값: (판 id, 까닭)"""
    if 적은것:
        return 적은것, "사양에 직접 적음"
    후보, 왜 = 판표.get(내용유형 or "", 판기본)
    남은 = [x for x in 후보 if x not in tuple(쓴판)[-5:]] or 후보
    h = sum(ord(c) * (i + 3) for i, c in enumerate(str(이름 or 내용유형 or "자오선")))
    return 남은[h % len(남은)], 왜


def index():
    """카탈로그 전체. 운영앱·문서가 읽는다."""
    out = {"설명": "자오선 에셋 라이브러리. 폴더에 넣으면 선택지가 저절로 는다.", "갈래": {}}
    for k, (d, ext, 설명) in 곳.items():
        items = list(k)
        out["갈래"][k] = {"폴더": d, "확장자": ext, "설명": 설명, "개수": len(items),
                         "보기": items[:12] if len(items) > 12 else items}
    out["갈래"]["face"]["금지"] = _금지컷()
    out["바탕 고르는 표"] = {k: {"바탕": v[0], "왜": v[1]} for k, v in 바탕표.items()}
    out["바탕 기본값"] = {"바탕": 바탕기본[0], "왜": 바탕기본[1]}
    out["판 고르는 표"] = {k: {"후보": v[0], "왜": v[1]} for k, v in 판표.items()}
    out["판 기본값"] = {"후보": 판기본[0], "왜": 판기본[1]}
    return out


if __name__ == "__main__":
    import sys
    if "--json" in sys.argv:
        print(json.dumps(index(), ensure_ascii=False, indent=1))
    else:
        for k, v in index()["갈래"].items():
            print(f'{k:7s} {v["개수"]:5d}개  {v["폴더"]:28s} {v["설명"]}')
            if k in ("bg", "deco", "face"):
                print("        ", ", ".join(list(k)))
