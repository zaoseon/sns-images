"""글 중간 '무료 풀이 입력칸 모양' 상자 (K-017, 대표 승인 10/13 16:13, ops/to-content.md [열림 10/13]).
방문의 약 90%가 홈판 유입이라 맨 아래 CTA까지 내려가지 않는다 → 1번 소제목 단락 끝(2번 소제목 바로 앞)에 한 번.
그림 없이 표+글자(글자 링크는 네이버에 붙여 넣어도 살아 있다). 링크 utm_medium=mid 로 맨 아래 CTA(cta)와 나눠 잰다.
여러 번 돌려도 같다(이미 있으면 건너뜀). 사용: python3 naver/mid_box.py [--dry]"""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); REG = os.path.join(HERE, "pages.json")
URL = "https://zaoseon.com/?utm_source=naver&amp;utm_medium=mid#free"
SKIP = {"n51"}   # 10/16 13:20 먼저 확정해 예약을 다시 건 글(바꾸면 원고와 네이버 글이 어긋난다)
TD = 'style="padding:12px 10px;text-align:center;border:1px solid #d0d0d0"'
BOX = ('<p>&nbsp;</p><table style="width:100%;max-width:440px;margin:0 auto;border-collapse:collapse"><tbody>'
       f'<tr><td {TD}><b>생년월일만 넣으면 1초</b></td></tr>'
       f'<tr><td {TD}><span style="color:#9a9a9a">[ 1990 . 03 . 15 ]</span></td></tr>'
       f'<tr><td {TD}><b><a href="{URL}">내 태어난 날 글자 보기 →</a></b></td></tr>'
       '</tbody></table>')
def apply(reg):
    n = 0
    for k, v in reg.items():
        b = v.get("body", "")
        if not b or k in SKIP or "utm_medium=mid" in b: continue
        m = re.search(r"<p>&nbsp;</p><p><b>2\.", b)
        if not m: print(k, "2번 소제목 못 찾음"); continue
        v["body"] = b[:m.start()] + BOX + b[m.start():]; n += 1
    return n
if __name__ == "__main__":
    reg = json.load(open(REG, encoding="utf-8")); n = apply(reg); print("넣음", n, "편")
    if "--dry" not in sys.argv: json.dump(reg, open(REG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
