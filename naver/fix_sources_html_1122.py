"""사이트 원고(public/naver/NN.html)의 본문에서 '📚 출처:' 줄을 없앤다 — 대표 11/22 승인(피클 전달), n107 방식.
- pages.json 은 fix_sources_1122.py 가 이미 고쳤다. 이 파일은 대표가 실제로 복사해 쓰는 사이트 원고를 같은 내용으로 맞춘다.
  (사이트 원고에는 pages.json 에 없는 첫 줄 장면·짧은 목차가 있어서 make_page 로 다시 그리면 그것들이 지워진다 → 글자를 그대로 두고 태그만 손댄다.)
- 지우는 것: <p><span 11px>📚 <b>출처 1/2</b>: …</span></p> 문단과 그 뒤 빈 줄 하나.
- 더하는 것: 지운 출처의 링크를 본문에서 그 자료를 말하는 낱말에 건다(링크 글자는 그대로 → 줄바꿈 그대로).
  자료 이름이 본문에 없는 네 편(n99·n100·n101·n102)은 절기 이름을 넣은 한 문장을 한 문단 더한다.
사용: SITE=<zaoseon-site> python3 naver/fix_sources_html_1122.py n95 n98 ...
"""
import os, re, sys, html as H

SITE = os.environ.get("SITE", "/home/claude/zaoseon-site")
KASI = "https://astro.kasi.re.kr/life/pageView/5"
DOI95 = "https://doi.org/10.1287/mnsc.2014.1901"
DOI98a = "https://doi.org/10.1037/0022-3514.73.2.345"
DOI98b = "https://doi.org/10.3389/fpsyg.2014.00502"
DOI93a = "https://doi.org/10.1037/1528-3542.3.1.48"
PMC93b = "https://pmc.ncbi.nlm.nih.gov/articles/PMC4141473/"
DOI94 = "https://doi.org/10.1037/0022-3514.67.3.366"
DOI103 = "https://doi.org/10.1016/S0065-2601(06)38002-1"
DOI99 = "https://doi.org/10.1037/0022-3514.50.2.392"
DOI100 = "https://doi.org/10.1177/0146167217733073"
DOI101 = "https://doi.org/10.1177/0265407508096700"
DOI102 = "https://doi.org/10.1177/0956797618783714"
NEWS104 = "https://www.newsis.com/view/NISX20250226_0003079235"
ENC105 = "https://encykorea.aks.ac.kr/Article/E0013895"
DOI105 = "https://doi.org/10.1126/science.1229294"

# 본문에서 이미 말하고 있는 낱말 → 링크 (그 낱말 글자는 그대로 두고 <a> 만 씌운다)
ANCHOR = {
    "n95": [("다이, 밀크먼, 리스 연구진", DOI95), ("5월 6일 입하", KASI, "⭐ 5월 6일 입하부터는")],
    "n98": [("일레인 아론과 아서 아론", DOI98a), ("틸뷔르흐대 연구진", DOI98b)],
    "n93": [("버틀러·그로스 연구진", DOI93a), ("스리바스타바 연구진", PMC93b)],
    "n94": [("뷸러, 그리핀, 로스 연구진", DOI94), ("음력 변환", KASI)],
    "n103": [("한국천문연구원 음양력 자료", KASI), ("골비처와 시런", DOI103)],
    "n99": [("클라이드 헨드릭과 수전 헨드릭", DOI99)],
    "n100": [("응우옌·라이언·데시", DOI100)],
    "n101": [("몬토야·호턴·커치너", DOI101)],
    "n102": [("부스비·쿠니·샌드스트롬·클라크", DOI102)],
    "n104": [("한국천문연구원 음양력 변환에서", KASI, "음력 생일이라면 한국천문연구원 음양력 변환에서"),
             ("2024년에 태어난 아기는 23만 8,300명", NEWS104)],
    "n105": [("한국민족문화대백과사전", ENC105), ("쿼이드백·길버트·윌슨", DOI105)],
}

# (앞 문단 끝말, 새 문단 — 줄은 손으로 끊어 이웃 문단과 같은 모양으로) — 링크는 낱말 자리에
INSERT = {
    "n99": ("한 번 말해 보세요.",
            f'달 글자는 절기로 나뉘어요.<br>6월 12일은 <a href="{KASI}">망종</a> 뒤라<br>午의 달이고, 위 여덟 글자의<br>壬午가 여기서 나와요.'),
    "n100": ("떠나고 싶은 마음이 커지기 쉬워요.",
             f'달 경계는 절기라서,<br>2월 4일 <a href="{KASI}">입춘</a>, 5월 6일 입하,<br>8월 8일 입추, 11월 8일 입동이<br>그 시작이에요.'),
    "n101": ("균형이 잡혀요.",
             f'두 사람의 달 글자도<br>절기로 나뉘어요.<br>3월 8일은 <a href="{KASI}">경칩</a> 뒤라 卯의 달,<br>7월 22일은 소서 뒤라<br>未의 달이에요.'),
    "n102": ("보이기 쉬워요.",
             f'달 글자도 절기로 나뉘어요.<br>12월 10일은 <a href="{KASI}">대설</a> 뒤라<br>子의 달이고, 여덟 글자의<br>甲子가 여기서 나와요.'),
}

TAGRE = re.compile(r"<[^>]+>")
P = re.compile(r"<p\b[^>]*>[\s\S]*?</p>")

def plain_map(region, base=0):
    """(글자 목록, 각 글자의 원문 위치) — 태그는 건너뛴다."""
    chars, pos = [], []
    i = 0
    for m in TAGRE.finditer(region):
        for k in range(i, m.start()):
            chars.append(region[k]); pos.append(base + k)
        i = m.end()
    for k in range(i, len(region)):
        chars.append(region[k]); pos.append(base + k)
    return "".join(chars), pos

def find_phrase(region, phrase, base=0):
    """띄어쓰기·줄바꿈(<br>)이 달라도 낱말로 찾아 원문 구간을 돌려준다."""
    text, pos = plain_map(region, base)
    key = re.sub(r"\s+", "", phrase)
    t2, p2, idx = [], [], []
    for ch, pp in zip(text, pos):
        if not ch.isspace():
            t2.append(ch); p2.append(pp); idx.append(len(t2) - 1)
    t2 = "".join(t2)
    k = t2.find(key)
    assert k >= 0, phrase[:30]
    assert t2.find(key, k + 1) < 0, ("여러 번 나옴", phrase[:30])
    return p2[k], p2[k + len(key) - 1] + 1

def para_at(text_head):
    """그 말로 끝나는 문단의 (시작, 끝) — 본문 안에서 정확히 하나."""
    for m in P.finditer(text_head[0]):
        t = re.sub(r"\s+", "", H.unescape(TAGRE.sub("", m.group(0))).replace("\xa0", ""))
        if t.endswith(re.sub(r"\s+", "", text_head[1])):
            return m.start(), m.end()
    raise AssertionError(text_head[1])

def fix(pid, page):
    i = page.find('<div id="body">'); j = page.find('</div></div>', i); assert i > 0 and j > i, pid
    head, body, tail = page[:i], page[i:j], page[j:]
    assert "📚" in body and body.count("📚") == 2, (pid, body.count("📚"))
    # 1) 출처 줄과 그 뒤 빈 줄 하나를 지운다
    body, k = re.subn(r'<p[^>]*><span style="font-size:11px">📚 <b>출처 [12]</b>:[\s\S]*?</span></p>'
                      r'(?:<p style="text-align:center"><span style="font-size:16px">&nbsp;</span></p>)?', "", body)
    assert k == 2, (pid, k)
    assert "📚" not in body and "출처" not in body, pid
    # 2) 본문 낱말에 링크 (같은 말이 여러 번이면 세 번째 값으로 그 자리를 좁힌다)
    for item in sorted(ANCHOR.get(pid, []), key=lambda x: -len(x[0])):
        phrase, url = item[0], item[1]
        if len(item) > 2:
            cs, ce = find_phrase(body, item[2])
            s2, e2 = find_phrase(body[cs:ce], phrase, base=cs); s, e = s2, e2
        else:
            s, e = find_phrase(body, phrase)
        body = body[:s] + f'<a href="{url}">' + body[s:e] + "</a>" + body[e:]
    # 3) 자료 이름이 본문에 없으면 한 문단 더
    if pid in INSERT:
        end_txt, sent = INSERT[pid]
        s, e = para_at((body, end_txt))
        body = body[:e] + f'<p style="text-align:center"><span style="font-size:16px">{sent}</span></p>' + body[e:]
    # 4) 빈 줄이 겹치면 하나로
    while '<p style="text-align:center"><span style="font-size:16px">&nbsp;</span></p><p style="text-align:center"><span style="font-size:16px">&nbsp;</span></p>' in body:
        body = body.replace('<p style="text-align:center"><span style="font-size:16px">&nbsp;</span></p>'
                            '<p style="text-align:center"><span style="font-size:16px">&nbsp;</span></p>',
                            '<p style="text-align:center"><span style="font-size:16px">&nbsp;</span></p>')
    return head + body + tail

if __name__ == "__main__":
    for pid in sys.argv[1:]:
        p = f"{SITE}/public/naver/{pid}.html"
        page = open(p, encoding="utf-8").read()
        new = fix(pid, page)
        open(p, "w", encoding="utf-8").write(new)
        ext = {u for u in re.findall(r'href="(https?://[^"]+)"', new)
               if not re.search(r"zaoseon\.com|raw\.githubusercontent|blog\.naver\.com/zaoseon", u)}
        print(pid, "고침 · 출처 0 · 바깥 링크", len(ext), "개")
