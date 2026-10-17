"""글 끝 차례 고치기 (10/17 서브 노트북 발행 글 29편 점검 1절, 대표 지시).

틀린 꼴: 사진 > … > CTA > 카드 > 카드     (CTA 배너 뒤에 공유·댓글 문단이 와서 키트가 카드를 CTA 뒤에 넣었다)
맞은 꼴: 사진 > … > 카드 > CTA

원본(pages.json)에서 CTA 배너 뒤에 남은 문단(공유·댓글 유도, 마무리 한 줄)을
'👇 함께 볼 글' 유도 문구 앞으로 옮긴다. 그러면 본문 끝은
  … 공유·댓글 → 마무리 → 👇 함께 볼 글(유도 문구 한 줄, 링크) → [카드] → CTA 배너
가 된다. 여러 번 돌려도 같다(CTA 뒤에 글이 없으면 그대로).

돌리기: python3 naver/tail_order.py          (바꿀 글만 보여 줌)
        python3 naver/tail_order.py --apply  (pages.json 고치고 원고 페이지 다시 만들기는 make_page.render_all())
"""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
REG = os.path.join(HERE, "pages.json")
PT = re.compile(r"<p[^>]*>.*?</p>", re.S)


def _txt(p): return re.sub(r"<[^>]+>", "", p).replace("&nbsp;", " ").replace("\xa0", " ").strip()


def fix(body):
    """CTA 뒤 글을 함께 볼 글 앞으로. 바꾼 본문과 옮긴 문단 수를 돌려준다."""
    ps = list(PT.finditer(body))
    ci = [i for i, m in enumerate(ps) if "naver_cta" in m.group(0)]
    if not ci: return body, 0
    c = ci[-1]
    tail = [m.group(0) for m in ps[c + 1:]]
    if not any(_txt(p) for p in tail): return body, 0
    while tail and not _txt(tail[-1]): tail.pop()              # 끝 빈 줄은 버린다
    while tail and not _txt(tail[0]): tail.pop(0)              # CTA 바로 뒤 빈 줄도
    # 넣을 자리: CTA 바로 앞의 '👇' 함께 볼 글 문단(있으면) 앞, 없으면 CTA 앞
    at = c
    j = c - 1
    while j >= 0 and not _txt(ps[j].group(0)): j -= 1
    if j >= 0 and _txt(ps[j].group(0)).startswith("👇"): at = j
    k = at - 1                                                  # 그 앞 빈 줄 하나는 '마무리 | 빈 줄 | 👇' 사이로 둔다
    while k >= 0 and not _txt(ps[k].group(0)): k -= 1
    if k + 1 < at:   # 앞 글 | 빈 줄 | 👇 → 앞 글 | 빈 줄 | 옮긴 글 | 빈 줄 | 👇
        ins = ps[k + 1].end(); blk = "".join(tail) + "<p>&nbsp;</p>"
    else:
        ins = ps[at].start(); blk = "<p>&nbsp;</p>" + "".join(tail) + "<p>&nbsp;</p>"
    new = body[:ins] + blk + body[ins:ps[c].end()]
    return new, len([p for p in tail if _txt(p)])


def main(apply=False):
    reg = json.load(open(REG, encoding="utf-8")); out = []
    for k, v in reg.items():
        if "body" not in v: continue
        nb, n = fix(v["body"])
        if n:
            out.append((k, n)); v["body"] = nb
    if apply and out:
        json.dump(reg, open(REG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return out


if __name__ == "__main__":
    print(main("--apply" in sys.argv))
