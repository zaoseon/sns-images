"""원고 줄 점검(zaoseon-site tools/naver_audit/linecheck.py)에 걸린 문장(두 줄 불균형·줄 끝 규칙·짧은 끝줄)을
낱말 경계에서 다시 끊어 line_overrides.json에 넣는다 (10/15, 인계문 4·5번).
규칙: 폰 폭(MOBILE_BODY) 안, 줄 끝 '와/과/의'·한 글자 꾸밈말 금지, 끝줄 4.0 이상, 두 줄이면 짧은 줄이 긴 줄의 45% 이상,
서술어만 다음 줄에 남기지 않음(끝줄 낱말 2개 이상). 조건을 다 맞추는 끊기가 없으면 건너뛰고 목록으로 남긴다.
사용: python3 naver/fix_lines.py [--write]   (SITE 환경변수 = zaoseon-site 경로)"""
import os, re, sys, json, itertools, html
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import format_body as FB
SITE = os.environ.get("SITE", "/home/claude/zaoseon-site") + "/public/naver"
OV = os.path.join(HERE, "line_overrides.json")
ONE = "몇안못더잘꼭또큰한두세네그이저새각첫온모든"
def bad_end(l):
    toks = l.split(" ")
    if toks[-1].endswith(","): return False
    last = re.sub(r"[,.!?·:)\]]", "", toks[-1])
    if re.search(r"['’”\"()]", toks[-1]): return False
    if len(last) == 1 and last in ONE and len(toks) > 1: return True
    if re.search(r"(와|과)$", last) and len(last) >= 2 and not re.search(r"(영과|보와)$", last): return True
    if re.search(r"의$", last) and len(last) >= 3: return True
    return False
def best(sent, lim):
    """엔진의 끊는 자리 벌점(FB.bpen)·따옴표/괄호 안 금지(FB._inside)를 쓰고, 점검 조건은 반드시 지킨다."""
    toks = FB.tokenize(html.escape(sent, quote=False)); n = len(toks)
    words = [t["p"].strip() for t in toks]
    if " ".join(words) != sent: return None
    ins = FB._inside(toks); cand = None
    for k in range(1, min(4, n) + 1):
        for cuts in itertools.combinations(range(1, n), k - 1):
            if any(ins[c - 1] for c in cuts): continue
            ls = [" ".join(words[a:b]) for a, b in zip((0,) + cuts, cuts + (n,))]
            ws = [FB.width(x) for x in ls]
            if max(ws) > lim or any(bad_end(l) for l in ls[:-1]): continue
            if len(ls) > 1 and (min(ws) < 4.0 or any(len(l.split(" ")) < 2 and FB.width(l) < 6 for l in ls)): continue
            if len(ls) > 1 and len(ls[-1].split(" ")) < 2: continue
            if len(ls) == 2 and not ls[0].endswith((",", "을", "를", "중")) and min(ws) / max(ws) < .45: continue
            if any(re.search(r"[.!?] \S", l) for l in ls): continue
            pen = sum(min(FB.bpen(toks[c - 1], c - 1), 50) for c in cuts)
            sc = len(ls) * 10 + pen + (max(ws) - min(ws)) * .5
            if cand is None or sc < cand[0]: cand = (sc, ls)
        if cand: break
    return cand[1] if cand and cand[0] - len(cand[1]) * 10 < 25 else None
def flagged():
    idx = open(SITE + "/index.html", encoding="utf-8").read(); ids = re.findall(r'href="/naver/(n\d+)\.html"', idx)
    for k in ids:
        h = open(f"{SITE}/{k}.html", encoding="utf-8").read(); b = h[h.index('<div id="body">'):]
        tr = [(m.start(), m.end()) for m in re.finditer(r"<table.*?</table>", b, re.S)]
        for m in re.finditer(r'<span style="font-size:(16|19)px">(.*?)</span>', b, re.S):
            if m.group(1) == "19" or any(a <= m.start() < z for a, z in tr) or "&nbsp;" in m.group(2): continue
            raw = m.group(2).split("<br>"); pl = [FB.plain_of(l).strip() for l in raw]; ws = [FB.width(x) for x in pl]
            if len(pl) < 2: continue
            why = []
            if any(bad_end(l) for l in pl[:-1]): why.append("줄끝")
            if ws[-1] < 4.0 and not all(x.endswith(",") for x in pl[:-1]): why.append("짧은끝줄")
            if len(pl) == 2 and not pl[0].endswith((",", "을", "를", "중")) and "(" not in m.group(2) and not re.match(r"^[\U0001F300-\U0001FAFF]", pl[0]) and ws[0] < 18 and min(ws) / max(ws) < .45 and not re.search(r"[:：]$", pl[0]): why.append("불균형")
            if why: yield k, pl, any("<" in x for x in raw), why
if __name__ == "__main__":
    ov = json.load(open(OV, encoding="utf-8")); add = {}; skip = []
    for k, pl, tagged, why in flagged():
        sent = " ".join(pl)
        if tagged: skip.append((k, sent, "굵은 글씨 등 태그가 있어 수동 줄바꿈이 안 먹음")); continue
        ls = best(sent, FB.MOBILE_BODY)
        if not ls or ls == pl: skip.append((k, sent, "조건을 다 맞추는 끊기 없음")); continue
        add[sent] = ls; print(k, "/".join(why), "|", " / ".join(pl), "  →  ", " / ".join(ls))
    print("고침", len(add), "건너뜀", len(skip))
    for s in skip: print("  건너뜀", s)
    if "--write" in sys.argv:
        ov.update(add); json.dump(ov, open(OV, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
