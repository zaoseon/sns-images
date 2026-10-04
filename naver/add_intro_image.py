"""10/3 대표 요청: 원고 '이 글의 순서' 다음, 1번 항목 앞에 이미지 하나(한눈에 보기 카드). n26~n46(10/4: n34~n46으로 확대, 10/4 재빌드 때 n26~n33에서 빠졌던 것을 복구). 다시 실행해도 같은 결과(이미 있으면 건너뜀).
카드 = 정월 얼굴 + 한 줄 요약 + 세 지도 키워드. 오행 색·글꼴은 thumb_sq(대표 이미지)와 같다. 1280x640(2:1, 10/4 해상도 2배). 파일 naver/img/naver_zNN_i.jpg
사용: python3 naver/add_intro_image.py   (그 뒤 apply_links_26_33.py 로 원고 페이지를 다시 만든다)"""
import os, re, sys, json
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import thumb_sq as TQ
RAW = "https://raw.githubusercontent.com/zaoseon/sns-images/main/naver/img/"
def wrap(d, text, font, maxw):
    """띄어쓰기 단위로 줄을 나눈다(낱말 가운데서 끊지 않음). 한 낱말이 한 줄보다 길면 글자 단위."""
    lines, cur = [], ""
    for wd in text.split():
        trial = (cur + " " + wd).strip()
        if d.textlength(trial, font=font) <= maxw: cur = trial
        else:
            if cur: lines.append(cur)
            cur = wd
    if cur: lines.append(cur)
    return lines
def balanced(d, text, font, maxw):
    """줄 수는 그대로 두고 줄 너비를 고르게(마지막 줄에 한두 글자만 남는 일을 막는다)."""
    ls = wrap(d, text, font, maxw); n = len(ls)
    if n < 2: return ls
    lo, hi = int(max(d.textlength(l, font=font) for l in ls) / 2), maxw
    while hi - lo > 4:
        mid = (lo + hi) // 2
        if len(wrap(d, text, font, mid)) == n: hi = mid
        else: lo = mid
    return wrap(d, text, font, hi)
def nohanja(t): return re.sub(r"\([^)]*[\u4e00-\u9fff][^)]*\)", "", t)      # 명조 글꼴에 한자가 없어 괄호 속 한자는 뺀다
def render(pid, summary, maps, path, label="세 지도"):
    """10/4 대표 지적: 원 안에 캐릭터가 제대로 안 들어감, 로고(子午線 자오선)가 카드 아래 선에 붙음, 글씨가 작다.
    -> 얼굴 원을 조금 줄여(반지름 130->108) 글 칸을 600->690으로 넓히고, 라벨 36->40, 요약 최대 56->64, 지도 줄 28->31로 키움.
       로고·AI 표시는 아래 선에서 40px 띄운 한 줄(y=H-100)에 두고, 글 내용은 그 위(H-125)까지만 쓴다."""
    t = TQ.T[pid]; c = TQ.Ctx(t["el"], False); face = t.get("face") or TQ.FACES[sum(map(ord, pid)) % len(TQ.FACES)]
    W, H = 1080, 540; img = Image.new("RGB", (W, H), c.bg); d = ImageDraw.Draw(img)
    d.rounded_rectangle([30, 30, W - 30, H - 30], 44, fill=c.card, outline=c.line, width=5)
    R = 108; TQ.badge(img, d, face, c, 70 + R + 10, 270, R)                            # 왼쪽 얼굴 원(머리~턱~어깨가 원 안에 들어옴)
    X0 = 330; maxw = W - 62 - X0                                                      # 글 시작 x, 글 칸 너비(오른쪽 카드 선에서 32px 안쪽)
    f = TQ.F(TQ.SEMI, 40); lab = "한눈에 보기"; w = d.textlength(lab, font=f) + 60
    d.rounded_rectangle([X0, 62, X0 + w, 132], 35, fill=c.acc); d.text((X0 + 30, 97), lab, font=f, fill=c.pillfg, anchor="lm")
    fm = TQ.F(TQ.MED, 31); LIM = H - 125; Y0 = 156
    for size in range(64, 33, -2):                                                   # 요약 3줄 이하 + 지도 줄이 아래 로고와 겹치지 않을 때까지 글자를 줄인다
        fs = TQ.F(TQ.SER, size); ls = balanced(d, summary, fs, maxw); mall = wrap(d, label + "  " + nohanja(maps), fm, maxw)
        lh = int(size * 1.22); y = Y0 + len(ls) * lh; ok = False
        for nl in (2, 1):                                                            # 지도 줄은 2줄이 안 들어가면 1줄로(쉼표 단위로 끊어 문장 중간에서 잘리지 않게)
            if nl == 2 or len(mall) == 1: ml = mall[:nl]
            else:
                items = (label + "  " + nohanja(maps)).split(", "); ml = [items[0]]
                for it in items[1:]:
                    if d.textlength(ml[0] + ", " + it, font=fm) <= maxw: ml[0] += ", " + it
                    else: break
            if len(ls) <= 3 and y + 44 + len(ml) * 42 <= LIM and (len(ml) == len(mall) or nl == 1 or len(mall) <= 2): ok = True; break
        if ok: break
    y = Y0
    for l in ls: d.text((X0, y), l, font=fs, fill=c.fg); y += lh
    d.line([(X0, y + 18), (X0 + 130, y + 18)], fill=c.acc, width=9)
    yy = y + 44
    for l in ml: d.text((X0, yy), l, font=fm, fill=c.acc); yy += 42
    d.text((X0, H - 100), "子午線 자오선", font=TQ.F(TQ.SER, 32), fill=c.acc)
    fa = TQ.F(TQ.MED, 23); d.text((W - 62, H - 84), "AI로 생성한 가상의 캐릭터입니다", font=fa, fill=c.gray, anchor="rm")
    img.resize((1280, 640), Image.LANCZOS).save(path, quality=95, subsampling=0, optimize=True)
def main():
    reg = json.load(open(os.path.join(HERE, "pages.json"), encoding="utf-8")); done = []
    for k in [f"n{i}" for i in range(26, 47)]:
        b = reg[k]["body"]; fn = f"naver_z{k[1:]}_i.jpg"
        if fn in b and not os.environ.get("FORCE"): continue
        m1 = re.search(r"<b>한 줄 요약</b>:\s*(.*?)</p>", b); m2 = re.search(r"<b>(세 지도|두 지도)</b>:\s*(.*?)</p>", b)
        assert m1 and m2, k
        render(k, re.sub(r"<[^>]+>", "", m1.group(1)), re.sub(r"<[^>]+>", "", m2.group(2)), os.path.join(HERE, "img", fn), label=m2.group(1))
        if fn in b: continue                                           # FORCE: 이미지만 다시 그리고 본문은 그대로
        j = b.find("이 글의 순서"); h = re.search(r"<p><b>1\. ", b[j:]); assert h, k
        pos = j + h.start(); alt = reg[k]["title"].split(",")[0] + " 한눈에 보기"
        reg[k]["body"] = b[:pos] + f'<p><img src="{RAW}{fn}" alt="{alt}"></p><p>&nbsp;</p>' + b[pos:]; done.append(k)
    json.dump(reg, open(os.path.join(HERE, "pages.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("추가:", done or "없음(이미 있음)")
if __name__ == "__main__": main()
