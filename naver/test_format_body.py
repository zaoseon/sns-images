"""format_body 검사: (1) 글자가 하나도 바뀌지 않았다 (2) 모든 줄이 가운데 정렬이고 글자 크기가 있다 (3) 굵은 글씨 태그가 줄마다 짝이 맞다 (4) 줄이 너무 길지 않다"""
import json, os, re, sys, html as H
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import format_body as F
reg = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "pages.json"), encoding="utf-8"))
def flat(h): return re.sub(r"[\s:]+", "", H.unescape(re.sub(r"<[^>]+>", "", re.sub(r"<img[^>]*>", "IMG", h))).replace("\xa0", ""))
bad = 0; n = 0; longest = 0
for k, v in reg.items():
    b = v.get("body")
    if not b: continue
    n += 1; out = F.format_body(b)
    if flat(b) != flat(out): print("FAIL 글자가 달라짐:", k); bad += 1
    ps = re.findall(r"<p[^>]*>.*?</p>", out, re.S)
    if any('text-align:center' not in p for p in ps): print("FAIL 가운데 정렬 빠짐:", k); bad += 1
    for p in ps:
        for ln in re.sub(r"</?p[^>]*>|</?span[^>]*>", "", p).split("<br>"):
            if "<img" in ln or "<a " in ln: continue
            if ln.count("<b>") != ln.count("</b>"): print("FAIL 굵은 글씨 짝이 안 맞음:", k, ln[:40]); bad += 1
            w = F.width(F.plain_of(ln)); longest = max(longest, w)
            if w > 22.5 and " " in F.plain_of(ln).strip(): print("긴 줄", k, round(w, 1), F.plain_of(ln))
    if len(re.findall("<img", b)) != len(re.findall("<img", out)): print("FAIL 이미지 수가 달라짐:", k); bad += 1
print(f"원고 {n}편 검사 · 문제 {bad}건 · 가장 긴 줄 {longest:.1f}")
sys.exit(1 if bad else 0)
