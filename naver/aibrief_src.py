"""AI 브리핑 기준(N3·N7·N8)을 원고 원본(pages.json body)에 넣는다 (10/15).
왜: 10/14·10/15 고침(patch_alt·add_sources·기준일)은 사이트 HTML만 고쳐서, 원고를 다시 만들면(render_all) 사라졌다
(10/15 오전 줄바꿈 재생성 때 출처 5편이 다시 빠짐). 원본에 넣어야 다시 만들어도 남는다.
여러 번 돌려도 같다. 미예약(done 아님) 원고만. 사용: python3 naver/aibrief_src.py [--dry]"""
import json, re, os, sys, html
HERE = os.path.dirname(os.path.abspath(__file__)); REG = os.path.join(HERE, "pages.json")
SRC = {  # Crossref 확인(10/14 add_sources.py와 같은 값): 글 → (저자·연도, 학술지, DOI)
    "n34": ("Nolen-Hoeksema (1991)", "J. Abnormal Psychology", "10.1037/0021-843X.100.4.569"),
    "n37": ("Festinger (1954)", "Human Relations", "10.1177/001872675400700202"),
    "n39": ("Hazan & Shaver (1987)", "J. Personality & Social Psych.", "10.1037/0022-3514.52.3.511"),
    "n43": ("Thaler (1985)", "Marketing Science", "10.1287/mksc.4.3.199"),
    "n44": ("Iyengar & Lepper (2000)", "J. Personality & Social Psych.", "10.1037/0022-3514.79.6.995"),
    "n71": ("Forer (1949)", "J. Abnormal & Social Psych.", "10.1037/h0059240"),
}
BASE_DATE = {"n48": "2026년 10월 15일", "n55": "2026년 10월 15일"}   # N7: 시기 글 첫머리 기준일
GREET = "<p>안녕하세요, 자오선의 정월이에요.</p>"

def fix_alt(title, body):
    n = 0
    def one(m):
        nonlocal n
        tag, alt = m.group(0), m.group(1)
        if not re.search(r"\.(jpg|png)$", alt, re.I): return tag
        if re.search(r"_b\.(jpg|png)$", alt): new = f"{title} 핵심 표"
        elif re.search(r"_c\.(jpg|png)$", alt): new = f"{title} 이번에 해 볼 것"
        elif "cta" in alt: new = "자오선 무료 1초 풀이 안내 배너"
        else:
            head = ""
            for hm in re.finditer(r"<p><b>\d+\.\s*([^<]*)</b>", body[:m.start()]): head = html.unescape(hm.group(1)).strip()
            new = f"{title} {head} 설명 그림" if head else f"{title} 본문 설명 그림"
        n += 1
        return tag.replace(f'alt="{alt}"', f'alt="{html.escape(new, quote=True)}"')
    return re.sub(r'<img[^>]*alt="([^"]*)"[^>]*>', one, body), n

def add_source(pid, body):
    if pid not in SRC or "📚" in body: return body, 0
    i = body.find("심리학으로 읽으면"); j = body.find("<p>&nbsp;</p>", i) if i >= 0 else -1
    if j < 0: print(pid, "심리학 단락 자리 못 찾음"); return body, 0
    a, b, doi = SRC[pid]
    line = f'<p>📚 <b>출처</b>: <a href="https://doi.org/{doi}">{a}, {b}</a></p>'
    return body[:j] + line + body[j:], 1

def add_base_date(pid, body):
    if pid not in BASE_DATE or "기준으로 정리한" in body: return body, 0
    if GREET not in body: print(pid, "인사 줄 못 찾음"); return body, 0
    return body.replace(GREET, GREET + f"<p>{BASE_DATE[pid]} 기준으로 정리한 내용이에요.</p>", 1), 1

if __name__ == "__main__":
    reg = json.load(open(REG, encoding="utf-8")); tot = [0, 0, 0]
    for pid, v in reg.items():
        if v.get("done") or "body" not in v: continue
        b = v["body"]; b, a = fix_alt(v["title"], b); b, s = add_source(pid, b); b, d = add_base_date(pid, b)
        tot[0] += a; tot[1] += s; tot[2] += d; v["body"] = b
    print(f"대체텍스트 {tot[0]}장 · 출처 {tot[1]}편 · 기준일 {tot[2]}편")
    if "--dry" not in sys.argv: json.dump(reg, open(REG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
