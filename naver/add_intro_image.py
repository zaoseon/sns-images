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
def nohanja(t): return re.sub(r"\([^)]*[\u4e00-\u9fff][^)]*\)", "", t)      # 명조 글꼴에 한자가 없어 괄호 속 한자는 뺀다
def render(pid, summary, maps, path, label="세 지도"):
    t = TQ.T[pid]; c = TQ.Ctx(t["el"], False); face = t.get("face") or TQ.FACES[sum(map(ord, pid)) % len(TQ.FACES)]
    W, H = 1080, 540; img = Image.new("RGB", (W, H), c.bg); d = ImageDraw.Draw(img)
    d.rounded_rectangle([30, 30, W - 30, H - 30], 44, fill=c.card, outline=c.line, width=5)
    TQ.badge(img, d, face, c, 210, 270, 130)                                         # 왼쪽 큰 얼굴 원
    f = TQ.F(TQ.SEMI, 36); lab = "한눈에 보기"; w = d.textlength(lab, font=f) + 56
    d.rounded_rectangle([420, 76, 420 + w, 140], 32, fill=c.acc); d.text((420 + 28, 108), lab, font=f, fill=c.pillfg, anchor="lm")
    maxw = 600; fm = TQ.F(TQ.MED, 28)
    for size in range(56, 33, -2):                                                   # 요약 3줄 이하 + 세 지도 줄이 아래 로고와 겹치지 않을 때까지 글자를 줄인다
        fs = TQ.F(TQ.SER, size); ls = wrap(d, summary, fs, maxw); mall = wrap(d, label + "  " + nohanja(maps), fm, maxw)
        y = 168 + len(ls) * int(size * 1.25); ok = False
        for nl in (2, 1):                                                            # 세 지도 줄은 2줄이 안 들어가면 1줄로(쉼표 단위로 끊어 문장 중간에서 잘리지 않게)
            if nl == 2 or len(mall) == 1: ml = mall[:nl]
            else:
                items = (label + "  " + nohanja(maps)).split(", "); ml = [items[0]]
                for it in items[1:]:
                    if d.textlength(ml[0] + ", " + it, font=fm) <= maxw: ml[0] += ", " + it
                    else: break
            if len(ls) <= 3 and y + 46 + len(ml) * 38 <= 436 and (len(ml) == len(mall) or nl == 1 or len(mall) <= 2): ok = True; break
        if ok: break
    y = 168
    for l in ls: d.text((420, y), l, font=fs, fill=c.fg); y += int(size * 1.25)
    d.line([(420, y + 22), (420 + 130, y + 22)], fill=c.acc, width=9)
    yy = y + 46
    for l in ml: d.text((420, yy), l, font=fm, fill=c.acc); yy += 38
    d.text((420, H - 74), "子午線 자오선", font=TQ.F(TQ.SER, 32), fill=c.acc)
    fa = TQ.F(TQ.MED, 22); d.text((W - 62, H - 66), "AI로 생성한 가상의 캐릭터입니다", font=fa, fill=c.gray, anchor="rm")
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
