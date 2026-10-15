"""N2(소제목 절반 이상 질문형 + 바로 아래 직답)를 원고 원본(pages.json)에 넣는다 (10/15, 인계문 2번).
고친 내용은 naver/n2_edits.json에 글마다 남는다: {"n47": [[번호, "새 소제목", "직답 한 문장 또는 null"], ...]}.
- 소제목은 한 줄(폰 소제목 폭 13.8) 안에 들어가게 짧게. 점검기는 소제목 첫 줄만 본다.
- 직답은 그 단락에 이미 있는 내용만. 첫 문장이 이미 답이면 null(새 문장을 넣지 않는다).
- 목차(📌 이 글의 순서)의 같은 번호 줄도 같이 바꾼다.
여러 번 돌려도 같다(이미 바뀐 소제목·이미 들어간 직답은 건너뛴다). 사용: python3 naver/n2_apply.py [글 id ...]"""
import json, os, re, sys, html
HERE = os.path.dirname(os.path.abspath(__file__)); REG = os.path.join(HERE, "pages.json"); ED = os.path.join(HERE, "n2_edits.json")

def apply(body, edits):
    for num, new, ans in edits:
        m = re.search(rf"<p><b>{num}\.\s*([^<]*)</b></p>", body)
        if not m: raise SystemExit(f"소제목 {num} 못 찾음")
        old = m.group(1); esc = html.escape(new, quote=False)
        if old != esc:
            body = body[:m.start()] + f"<p><b>{num}. {esc}</b></p>" + body[m.end():]
            toc = f"<p>{num}. {old}</p>"
            i = body.find(toc)
            if 0 <= i < m.start(): body = body[:i] + f"<p>{num}. {esc}</p>" + body[i + len(toc):]
        m = re.search(rf"<p><b>{num}\.\s*[^<]*</b></p>", body)
        if ans and not body[m.end():].startswith(f"<p>{html.escape(ans, quote=False)}</p>"):
            body = body[:m.end()] + f"<p>{html.escape(ans, quote=False)}</p>" + body[m.end():]
    return body

if __name__ == "__main__":
    reg = json.load(open(REG, encoding="utf-8")); E = json.load(open(ED, encoding="utf-8"))
    ids = sys.argv[1:] or list(E)
    for k in ids:
        reg[k]["body"] = apply(reg[k]["body"], E[k]); print(k, "소제목", len(E[k]), "곳")
    json.dump(reg, open(REG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
