#!/usr/bin/env python3
"""대본 JSON을 브랜드 규칙에 맞춰 검사한다.
  python3 qa.py <대본.json>
검사: 금지 표현 / 단어 중간 줄바꿈 / 끝줄 한 글자 / 한 줄 글자 수 /
      표지·CTA 유무 / CTA 개수 / 금지 캐릭터 파일 / 레이아웃 쏠림
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# 한 줄 글자 수는 글자 크기에 따라 다르다. 큰 제목일수록 짧아야 한다.
LIMITS = {            # (권장, 상한) - 공백 뺀 글자 수
    "title": (12, 16),
    "label": (10, 14),
    "sub": (16, 24),
    "cta": (99, 99),  # 주소는 길어도 된다
    "lines[0]": (14, 20),
    "lines[1]": (12, 16),
    "lines[2]": (16, 24),
}
DEFAULT_LIMIT = (14, 20)


def lines_of(card):
    out = []
    for key in ("label", "title", "sub", "cta"):
        v = card.get(key)
        if v:
            out += [(key, l) for l in str(v).split("\n")]
    for i, l in enumerate(card.get("lines") or []):
        out += [(f"lines[{i}]", x) for x in str(l).split("\n")]
    return out


def main():
    spec = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    brand = json.loads((ROOT / "brands" / f"{spec['brand']}.json")
                       .read_text(encoding="utf-8"))
    banned = brand.get("voice", {}).get("banned", [])
    forbidden_files = (brand.get("character") or {}).get("forbidden", [])

    errors, warns = [], []
    cards = spec["cards"]

    for c in cards:
        cid = c.get("id", "?")

        for where, line in lines_of(c):
            s = line.strip()
            if not s:
                continue
            for b in banned:
                if b in s:
                    errors.append(f"[{cid}] {where}: 금지 표현 '{b}' - \"{s}\"")
            warn_at, max_at = LIMITS.get(where, DEFAULT_LIMIT)
            n = len(s.replace(" ", ""))
            if n > max_at:
                errors.append(f"[{cid}] {where}: 한 줄 {n}자. {max_at}자를 넘겼다 - \"{s}\"")
            elif n > warn_at:
                warns.append(f"[{cid}] {where}: 한 줄 {n}자. {warn_at}자 안쪽을 권한다 - \"{s}\"")

        # 끝줄에 한 글자만 남는지
        for key in ("title", "sub"):
            v = c.get(key)
            if v and "\n" in str(v):
                last = str(v).split("\n")[-1].strip()
                if len(last.replace(" ", "")) <= 1:
                    errors.append(f"[{cid}] {key}: 끝줄에 '{last}' 한 글자만 남았다")

        # 캐릭터 금지 파일
        ch = c.get("character") or ""
        for f in forbidden_files:
            if ch.endswith(f):
                errors.append(f"[{cid}] 쓰면 안 되는 캐릭터 파일이다: {f}")

        # 캐릭터가 있으면 AI 고지가 붙는다(렌더러가 자동) - 없으면 알림
        if ch and not (brand.get("character") or {}).get("notice"):
            warns.append(f"[{cid}] 캐릭터를 썼는데 브랜드 파일에 AI 고지 문구가 없다")

    # 묶음 단위 검사
    ctas = [c for c in cards if c.get("cta")]
    if len(cards) > 1:
        if not ctas:
            errors.append("묶음에 CTA가 하나도 없다. 한 개는 있어야 한다")
        if len(ctas) > 1:
            errors.append(f"CTA가 {len(ctas)}개다. 게시물당 한 개만 둔다")

        layouts = [c.get("layout") for c in cards]
        top = max(set(layouts), key=layouts.count)
        if layouts.count(top) > max(2, len(layouts) // 2):
            errors.append(f"레이아웃 {top}이 {len(layouts)}장 중 {layouts.count(top)}장이다. "
                          "한 묶음에서 절반을 넘기면 안 된다")
        if len(set(layouts)) < min(3, len(layouts)):
            warns.append(f"레이아웃이 {len(set(layouts))}종뿐이다. 유형에 맞춰 섞는다")

        techs = [tuple(sorted(c.get("tech") or [])) for c in cards]
        if len(set(techs)) == 1 and len(cards) >= 4:
            warns.append("가독성 기법이 전부 같다. 배경·기법도 같이 바꾼다")

    for e in errors:
        print("오류 :", e)
    for w in warns:
        print("알림 :", w)
    print(f"\n카드 {len(cards)}장 · 오류 {len(errors)}건 · 알림 {len(warns)}건")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
