"""10/4 대표 요청(게시물 클립에 쓰이는 것과 별개로 블로그 원고에 이미지를 하나 더):
(1) n47~n63(정보 글): 「이 글의 순서」 다음, 1번 앞에 한눈에 보기 카드(n26~n46은 add_intro_image.py가 이미 넣음)
(2) n26~n46(공통점 글): 「나는 몇 개나 겹칠까」 첫 줄 앞에 '나는 몇 개 겹칠까?' 점수 카드(3개/2개/1개/0개 한 줄씩, 원고 문장 그대로)
다시 실행해도 같은 결과(이미 있으면 건너뜀). 이미지 naver/img/naver_zNN_i.jpg(한눈에), naver_zNN_s.jpg(점수). 그 뒤 make_page.render_all()로 원고 페이지를 다시 만든다."""
import os, re, sys, json
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import thumb_sq as TQ, add_intro_image as AI
RAW = AI.RAW; ELS = sorted({v["el"] for v in TQ.T.values()})
def cfg(pid):
    if pid not in TQ.T:
        n = int(pid[1:]); TQ.T[pid] = dict(el=ELS[n % len(ELS)], face=TQ.FACES[n % len(TQ.FACES)])
    t = TQ.T[pid]; return TQ.Ctx(t["el"], False), (t.get("face") or TQ.FACES[sum(map(ord, pid)) % len(TQ.FACES)])
def score_card(pid, title, rows, path):
    c, face = cfg(pid); W, H = 1080, 540; img = Image.new("RGB", (W, H), c.bg); d = ImageDraw.Draw(img)
    d.rounded_rectangle([30, 30, W - 30, H - 30], 44, fill=c.card, outline=c.line, width=5)
    f = TQ.F(TQ.SEMI, 36); w = d.textlength(title, font=f) + 56
    d.rounded_rectangle([70, 58, 70 + w, 122], 32, fill=c.acc); d.text((98, 90), title, font=f, fill=c.pillfg, anchor="lm")
    n = len(rows); rh = 88 if n <= 3 else 80; y = 146
    for lab, txt in rows:
        d.rounded_rectangle([70, y, W - 70, y + rh - 8], 22, fill=c.bg, outline=c.line, width=3)
        size = 30
        while size > 20 and d.textlength(lab, font=TQ.F(TQ.SEMI, size)) > 214: size -= 2
        d.rounded_rectangle([84, y + 10, 84 + 236, y + rh - 18], 18, fill=c.acc); d.text((84 + 118, y + (rh - 8) // 2), lab, font=TQ.F(TQ.SEMI, size), fill=c.pillfg, anchor="mm")
        fs = 28; fm = TQ.F(TQ.MED, fs); ls = AI.wrap(d, txt, fm, W - 70 - 350 - 24)
        while len(ls) > 2 and fs > 22: fs -= 2; fm = TQ.F(TQ.MED, fs); ls = AI.wrap(d, txt, fm, W - 70 - 350 - 24)
        ty = y + (rh - 8) // 2 - (len(ls[:2]) - 1) * (fs + 4) // 2
        for k, l in enumerate(ls[:2]): d.text((344, ty + k * (fs + 4)), l, font=fm, fill=c.fg, anchor="lm")
        y += rh
    d.text((W - 70, H - 48), "子午線 자오선", font=TQ.F(TQ.SER, 28), fill=c.acc, anchor="rm")
    img.resize((1280, 640), Image.LANCZOS).save(path, quality=95, subsampling=0, optimize=True)
def parse_rows(b):
    i = b.find("<b>3. "); j = b.find("<b>4. ", i)
    sec = b[i:j] if j > i else b[i:i + 2500]
    title = re.sub(r"<[^>]+>", "", re.search(r"<b>3\. (.*?)</b>", sec).group(1)).strip()
    ps = re.findall(r"<p>(.*?)</p>", sec, re.S); rows = []
    for n, pp in enumerate(ps):
        if not pp.startswith("🔹"): continue
        m = re.match(r"🔹\s*<b>(.*?)</b>(.*)", pp, re.S)
        if not m: continue
        lab = re.sub(r"<[^>]+>", "", m.group(1)).strip(); rest = re.sub(r"<[^>]+>", "", m.group(2)).strip()
        rest = re.sub(r"^(이면|이라면|면|이에요)?\s*[,:]\s*", "", rest).strip(); rest = re.sub(r"^:\s*", "", rest)
        if len(rest) < 6:
            nxt = ps[n + 1] if n + 1 < len(ps) else ""
            if nxt and not nxt.startswith(("🔹", "&nbsp;", "<b>")): rest = (rest + " " + re.sub(r"<[^>]+>", "", nxt)).strip()
        if lab.endswith(("이면", "라면")): lab = lab[:-2]
        if re.fullmatch(r"\d개", lab): lab = lab
        rows.append((lab, rest))
    return title, rows
def main():
    reg = json.load(open(os.path.join(HERE, "pages.json"), encoding="utf-8")); done_i, done_s, skip = [], [], []
    for k in [f"n{i}" for i in range(47, 64)]:
        b = reg[k]["body"]; fn = f"naver_z{k[1:]}_i.jpg"
        if fn in b: continue
        m1 = re.search(r"<b>한 줄 요약</b>:\s*(.*?)</p>", b); m2 = re.search(r"<b>(세 가지|달력|세 지도|두 지도|[^<]{2,6})</b>:\s*(.*?)</p>", b[b.find("한 줄 요약") + 10:])
        if not (m1 and m2): skip.append(k); continue
        summ = re.sub(r"<[^>]+>", " ", m1.group(1)).split("  ")[0].strip(); summ = re.sub(r"\s+", " ", summ)
        cfg(k); AI.render(k, summ, re.sub(r"<[^>]+>", "", m2.group(2)), os.path.join(HERE, "img", fn), label=m2.group(1))
        j = b.find("이 글의 순서"); h = re.search(r"<p><b>1\. ", b[j:]) or re.search(r"<p>1\. ", b[j:]); h = h or re.search(r"1\. ", b[j + 20:])
        if not h: skip.append(k + "(1번 위치 못 찾음)"); continue
        pos = j + h.start(); alt = reg[k]["title"].split(",")[0] + " 한눈에 보기"
        reg[k]["body"] = b[:pos] + f'<p><img src="{RAW}{fn}" alt="{alt}"></p><p>&nbsp;</p>' + b[pos:]; done_i.append(k)
    for k in [f"n{i}" for i in range(26, 47)]:
        b = reg[k]["body"]; fn = f"naver_z{k[1:]}_s.jpg"
        if fn in b: continue
        try: title, rows = parse_rows(b)
        except Exception as e: skip.append(k + "(3번 소제목 못 찾음)"); continue
        rows = [(l, t) for l, t in rows if t][:4]
        if len(rows) < 3: skip.append(k + "(점수 줄 3개 미만)"); continue
        score_card(k, title, rows, os.path.join(HERE, "img", fn))
        idx = b.find("🔹"); pstart = b.rfind("<p>", 0, idx); alt = reg[k]["title"].split(",")[0] + " " + title
        reg[k]["body"] = b[:pstart] + f'<p><img src="{RAW}{fn}" alt="{alt}"></p><p>&nbsp;</p>' + b[pstart:]; done_s.append(k)
    json.dump(reg, open(os.path.join(HERE, "pages.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("한눈에 보기 추가:", done_i); print("점수 카드 추가:", done_s); print("건너뜀:", skip)
if __name__ == "__main__": main()
