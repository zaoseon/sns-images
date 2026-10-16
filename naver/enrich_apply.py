"""원고 보강 적용 (10/16 대표: "모든 원고에 여섯 운명학·심리학 내용, AI 브리핑 기준·모바일·롱테일 검색어 제대로, 태그는 실제 검색 유입 반영").
입력: naver/enrich_1016.json  {"nXX": {psych, lens, title, headings, tags, longtail, notes}}  (작업 규칙: 같은 폴더 enrich_1016_RULES.md)
- 여섯 운명학 단락(🔭)과 심리학 단락(🧠 + 📚 출처 DOI)을 '해 볼 것'(없으면 FAQ) 소제목 바로 앞에 넣는다. 이미 있으면 건너뛴다.
- 제목: 이미 발행한 글은 바꾸지 않는다(naver_urls에 주소가 있는 글 + n33).
- 소제목: 폰 한 줄(번호 포함 폭 13.8) 안일 때만 바꾸고 목차 줄도 같이.
- 태그: 10개, 본문에 나오는 말만(띄어쓰기 무시 비교). 없는 태그는 빼고 보고.
여러 번 돌려도 같다. 사용: python3 naver/enrich_apply.py [--dry]"""
import json, os, re, sys, html
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import format_body as FB
REG = os.path.join(HERE, "pages.json"); ED = os.path.join(HERE, "enrich_1016.json")
SITE = os.environ.get("SITE", "/home/claude/zaoseon-site")
PUBLISHED = {x["id"] for x in json.load(open(f"{SITE}/data/naver_urls.json", encoding="utf-8"))["items"] if x.get("url")} | {"n33"}
NO_TITLE = {"n62"}   # 10/16: '손없는날'을 넣으면 n60(11월 손없는날)과 같은 검색어를 두고 겨룬다 → 제목 그대로

def esc(s): return html.escape(s, quote=False)
def block(label, lines, src=None):
    b = "<p>&nbsp;</p>" + f"<p>{label}</p>" + "".join(f"<p>{esc(l)}</p>" for l in lines)
    if src:
        b += f'<p>📚 <b>출처</b>: <a href="https://doi.org/{src["doi"]}">{esc(src["author"])} ({src["year"]}), {esc(src["journal"])}</a></p>'
    return b
def insert_before(body, num, blk):
    m = re.search(rf"<p>&nbsp;</p><p><b>{num}\.", body) or re.search(rf"<p><b>{num}\.", body)
    if not m: raise ValueError(f"소제목 {num} 못 찾음")
    return body[:m.start()] + blk + body[m.start():]
def plain(b): return re.sub(r"\s", "", html.unescape(re.sub(r"<[^>]+>", "", b)))

def apply(reg, E):
    rep = []
    for k, e in E.items():
        v = reg[k]; b = v["body"]
        if e.get("lens") and "여섯 운명학으로 넓혀 보면" not in b:
            b = insert_before(b, e["lens"]["before_heading"], block("🔭 <b>여섯 운명학으로 넓혀 보면</b>", e["lens"]["lines"]))
        if e.get("psych") and "심리학으로 읽으면" not in b:
            p = e["psych"]; b = insert_before(b, p["before_heading"], block("🧠 <b>심리학으로 읽으면</b>", p["lines"], p["source"]))
        for num, new in e.get("headings") or []:
            new = re.sub(rf"^{num}\.\s*", "", new).strip()
            if FB.width(f"{num}. {new}") > 13.8: rep.append((k, "소제목 길어 건너뜀", new)); continue
            m = re.search(rf"<p><b>{num}\.\s*([^<]*)</b></p>", b)
            if not m: rep.append((k, "소제목 못 찾음", num)); continue
            old = m.group(1); b = b[:m.start()] + f"<p><b>{num}. {esc(new)}</b></p>" + b[m.end():]
            toc = f"<p>{num}. {old}</p>"; i = b.find(toc)
            if i >= 0: b = b[:i] + f"<p>{num}. {esc(new)}</p>" + b[i + len(toc):]
        v["body"] = b
        if e.get("title") and k not in PUBLISHED and k not in NO_TITLE and len(e["title"]) <= 40: v["title"] = e["title"]
        if e.get("tags"):
            pb = plain(b) + plain(v["title"])
            tags = [t for t in e["tags"] if t == "자오선" or t in pb]
            miss = [t for t in e["tags"] if t not in tags]
            if miss: rep.append((k, "본문에 없는 태그 뺌", miss))
            v["tags"] = tags[:10]
    return rep

if __name__ == "__main__":
    reg = json.load(open(REG, encoding="utf-8")); E = json.load(open(ED, encoding="utf-8"))
    rep = apply(reg, E)
    for r in rep: print(*r)
    print("적용", len(E), "편")
    if "--dry" not in sys.argv: json.dump(reg, open(REG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
