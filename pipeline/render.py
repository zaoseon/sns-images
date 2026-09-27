"""자오선 SNS 이미지 렌더러.
사용: python3 render.py ../content/2026-w42.json  -> ../2026-w42/*.jpg
JSON 형식은 README.md 참고.
"""
import json, os, sys, datetime as D
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
FD = HERE + "/fonts/"
SER, MED, SEMI = FD + "serif.otf", FD + "PRETENDARD-MEDIUM.OTF", FD + "PRETENDARD-SEMIBOLD.OTF"
W, H = 1080, 1350
INK, PAPER, GOLD, DIM, RED, LINE = (18,16,14), (236,227,208), (196,160,98), (160,150,132), (150,40,34), (70,62,52)
EL = {"나무":(92,150,92),"불":(196,72,56),"흙":(184,140,72),"쇠":(210,206,196),"물":(70,110,170)}
_fc = {}
def F(p, s):
    k = (p, s)
    if k not in _fc: _fc[k] = ImageFont.truetype(p, s)
    return _fc[k]

def wrap(d, text, font, maxw):
    out = []
    for para in text.split("\n"):
        cur = ""
        for w in para.split(" "):
            t = (cur + " " + w).strip()
            if d.textlength(t, font=font) <= maxw: cur = t
            else:
                if cur: out.append(cur)
                while d.textlength(w, font=font) > maxw:
                    i = len(w)
                    while d.textlength(w[:i], font=font) > maxw: i -= 1
                    out.append(w[:i]); w = w[i:]
                cur = w
        out.append(cur)
    return out

def base(n=None, total=None, idx=None):
    img = Image.new("RGB", (W, H), INK); d = ImageDraw.Draw(img); L, R = 90, W - 90
    d.ellipse([L,80,L+84,164], fill=RED); d.text((L+42,122), "子午線", font=F(SER,24), fill=(245,236,220), anchor="mm")
    d.text((L+104,104), "자오선", font=F(SER,32), fill=GOLD, anchor="lm")
    d.text((L+104,142), "상담가 정월", font=F(MED,23), fill=DIM, anchor="lm")
    d.line([(L,H-130),(R,H-130)], fill=LINE, width=1)
    d.text((R,H-88), "동서양 6가지 운명학", font=F(MED,24), fill=DIM, anchor="rm")
    if total:
        for k in range(total):
            x = W//2 - (total-1)*12 + k*24
            d.ellipse([x-5,H-45,x+5,H-35], fill=GOLD if k == n else LINE)
    return img, d, L, R

def foot(d, L, t): d.text((L,H-88), t, font=F(MED,26), fill=GOLD, anchor="lm")

def card(s, path):
    """{"type":"card","title":"..","lines":[..],"foot":".."}  '→'/'※'로 시작하는 줄은 금색"""
    img, d, L, R = base(s.get("_n"), s.get("_t")); mw = R - L
    tf = F(SER, 78); tl = wrap(d, s["title"], tf, mw)
    if len(tl) > 2: tf = F(SER, 64); tl = wrap(d, s["title"], tf, mw)
    tlh = int(tf.size * 1.3)
    for bs in range(42, 25, -1):
        bf = F(MED, bs); lh = int(bs * 1.6)
        bl = [wrap(d, l, bf, mw) if l else [""] for l in s["lines"]]
        total = len(tl)*tlh + 90 + sum(len(x) for x in bl)*lh
        if total <= H - 390: break
    y = 240 + max(0, (H - 390 - total)//2 - 20)
    for l in tl: d.text((L,y), l, font=tf, fill=PAPER); y += tlh
    y += 30; d.line([(L,y),(L+80,y)], fill=GOLD, width=3); y += 60
    for x in bl:
        for l in x:
            d.text((L,y), l, font=bf, fill=GOLD if l[:1] in "→※" else PAPER); y += lh
    foot(d, L, s.get("foot", "저장해 두고 다시 보세요")); img.save(path, quality=90)

def trait(s, path):
    """{"type":"trait","kicker":"태어난 날 이름의 첫 글자가 갑(甲)","big":"큰 나무","mark":"甲",
        "rows":[["성격",".."],["사랑",".."]],"tip":"..","foot":".."}"""
    img, d, L, R = base(s.get("_n"), s.get("_t"))
    d.text((L,360), s["kicker"], font=F(SER,36), fill=DIM)
    if s.get("mark"): d.text((R+10,320), s["mark"], font=F(SER,260), fill=(44,40,34), anchor="ra")
    d.text((L,415), s["big"], font=F(SER,110), fill=PAPER)
    y = 580; d.line([(L,y),(L+80,y)], fill=GOLD, width=3); y += 40
    lf, bf = F(SEMI,32), F(MED,36)
    for lab, txt in s["rows"]:
        d.text((L,y+4), lab, font=lf, fill=GOLD)
        for l in wrap(d, txt, bf, R-L-110): d.text((L+110,y), l, font=bf, fill=PAPER); y += 54
        y += 22
    if s.get("tip"):
        y += 10; tf = F(SEMI,34); tl = wrap(d, s["tip"], tf, R-L-60); bh = len(tl)*52 + 84
        d.rounded_rectangle([L,y,R,y+bh], radius=14, outline=GOLD, width=2)
        d.text((L+30,y+26), "정월의 한마디", font=F(MED,26), fill=GOLD); yy = y + 68
        for l in tl: d.text((L+30,yy), l, font=tf, fill=PAPER); yy += 52
    foot(d, L, s.get("foot", "내 태어난 날이 궁금하면 댓글로")); img.save(path, quality=90)

# ---- 일진(날마다의 기운) ----
GAN = {"甲":("갑","큰 나무","나무"),"乙":("을","풀","나무"),"丙":("병","태양","불"),"丁":("정","등불","불"),"戊":("무","큰 산","흙"),
       "己":("기","논밭","흙"),"庚":("경","쇠","쇠"),"辛":("신","보석","쇠"),"壬":("임","강물","물"),"癸":("계","비","물")}
ZHI = {"子":("자","쥐","물"),"丑":("축","소","흙"),"寅":("인","호랑이","나무"),"卯":("묘","토끼","나무"),"辰":("진","용","흙"),"巳":("사","뱀","불"),
       "午":("오","말","불"),"未":("미","양","흙"),"申":("신","원숭이","쇠"),"酉":("유","닭","쇠"),"戌":("술","개","흙"),"亥":("해","돼지","물")}
G10, Z12 = "甲乙丙丁戊己庚辛壬癸", "子丑寅卯辰巳午未申酉戌亥"
WD = "월화수목금토일"
def jdn(y, m, d):
    a = (14-m)//12; y2 = y+4800-a; m2 = m+12*a-3
    return d + (153*m2+2)//5 + 365*y2 + y2//4 - y2//100 + y2//400 - 32045
def pillar(dt):
    k = (jdn(dt.year, dt.month, dt.day) + 49) % 60
    return G10[k%10] + Z12[k%12]
def ko(hz): return GAN[hz[0]][0] + ZHI[hz[1]][0]
def wa(w): return w + ("과" if (ord(w[-1])-0xAC00) % 28 else "와")
def dname(hz): return f"{wa(GAN[hz[0]][1])} {ZHI[hz[1]][1]}의 날"
def dot(d, x, y, el, r=12): d.ellipse([x-r,y-r,x+r,y+r], fill=EL[el])

def week(s, outdir, prefix):
    """{"type":"week","start":"2026-10-12","days":[{"mean":"두 줄 뜻(\\n)","tip":".."} x7]}
    -> prefix_1..9.jpg. 날짜와 일진 글자는 자동 계산."""
    st = D.date.fromisoformat(s["start"]); n = 9; files = []
    days = [(st + D.timedelta(i)) for i in range(7)]
    rng = f"{days[0].month}/{days[0].day} - {days[-1].month}/{days[-1].day}"
    img, d, L, R = base(0, n)
    d.text((L,330), "이번 주", font=F(SER,64), fill=DIM); d.text((L,420), "날마다의 기운", font=F(SER,110), fill=PAPER)
    d.text((L,580), rng, font=F(SER,60), fill=GOLD); d.line([(L,700),(L+80,700)], fill=GOLD, width=3)
    for i, l in enumerate(["옛 달력에는 날마다 이름이 있어요.", "'오늘 일진이 사납다'의 그 일진이에요.", "이번 주 일곱 날의 이름을 풀어 드릴게요."]):
        d.text((L,750+i*64), l, font=F(MED,38), fill=PAPER)
    foot(d, L, "옆으로 넘겨 보세요 →"); p = f"{outdir}/{prefix}_1.jpg"; img.save(p, quality=92); files.append(p)
    img, d, L, R = base(1, n); ex = pillar(days[0])
    d.text((L,250), "날 이름 읽는 법", font=F(SER,80), fill=PAPER); d.line([(L,395),(L+80,395)], fill=GOLD, width=3)
    d.text((L+150,540), ex[0], font=F(SER,200), fill=PAPER, anchor="mm"); d.text((L+400,540), ex[1], font=F(SER,200), fill=PAPER, anchor="mm")
    d.text((L+150,690), "앞 글자", font=F(SEMI,34), fill=GOLD, anchor="mm"); d.text((L+400,690), "뒷 글자", font=F(SEMI,34), fill=GOLD, anchor="mm")
    d.text((L+150,740), "하늘의 기운", font=F(MED,30), fill=DIM, anchor="mm"); d.text((L+400,740), "땅의 기운 · 띠 동물", font=F(MED,30), fill=DIM, anchor="mm")
    x0 = R - 250; d.text((x0,430), "다섯 가지 기운", font=F(SEMI,30), fill=GOLD)
    for i, el in enumerate(["나무","불","흙","쇠","물"]):
        dot(d, x0+14, 500+i*56, el, 13); d.text((x0+44,500+i*56), el, font=F(MED,32), fill=PAPER, anchor="lm")
    y = 830
    for l in ["앞 글자와 뒷 글자에는 각각 기운이 하나씩 있어요.", "두 기운이 서로 키워 주는지, 겹치는지를 보고", "그날의 분위기를 읽어요."]:
        d.text((L,y), l, font=F(MED,36), fill=PAPER); y += 62
    d.text((L,y+20), "※ 재미로, 나를 돌아보는 계기로 봐 주세요.", font=F(MED,28), fill=DIM)
    foot(d, L, "옆으로 넘겨 보세요 →"); p = f"{outdir}/{prefix}_2.jpg"; img.save(p, quality=92); files.append(p)
    for i, (dt, info) in enumerate(zip(days, s["days"])):
        hz = pillar(dt); img, d, L, R = base(i+2, n)
        d.text((L,320), f"{dt.month}/{dt.day} {WD[dt.weekday()]}요일", font=F(SEMI,40), fill=GOLD)
        d.text((L-8,370), hz, font=F(SER,230), fill=PAPER)
        d.text((L,670), f"{ko(hz)} · {dname(hz)}", font=F(SER,56), fill=PAPER); y = 780
        for c, t in [(hz[0], GAN[hz[0]]), (hz[1], ZHI[hz[1]])]:
            d.rounded_rectangle([L,y,L+560,y+64], radius=32, outline=LINE, width=2)
            d.text((L+28,y+32), f"{c}  {t[0]} · {t[1]}", font=F(SER,32), fill=PAPER, anchor="lm")
            dot(d, L+420, y+32, t[2], 11); d.text((L+442,y+32), t[2], font=F(MED,30), fill=PAPER, anchor="lm"); y += 84
        y += 20
        for l in info["mean"].split("\n"): d.text((L,y), l, font=F(MED,40), fill=PAPER); y += 64
        y += 20; d.rounded_rectangle([L,y,R,y+100], radius=14, outline=GOLD, width=2)
        d.text((L+30,y+50), "정월의 한마디", font=F(MED,26), fill=GOLD, anchor="lm")
        d.text((L+230,y+50), info["tip"], font=F(SEMI,34), fill=PAPER, anchor="lm")
        foot(d, L, "재미로, 나를 돌아보는 계기로"); p = f"{outdir}/{prefix}_{i+3}.jpg"; img.save(p, quality=92); files.append(p)
    return files

def week_texts(s):
    """스레드 3개 글과 인스타 캡션을 자동으로 만든다."""
    st = D.date.fromisoformat(s["start"]); days = [st + D.timedelta(i) for i in range(7)]
    rng = f"{days[0].month}/{days[0].day}~{days[-1].month}/{days[-1].day}"
    intro = (f"이번 주 날마다의 기운 ({rng})\n\n옛 달력에는 날마다 이름이 있어요. 이것을 일진(日辰)이라고 불러요. "
             "'오늘 일진이 사납다'의 그 일진이에요.\n\n날 이름은 두 글자예요.\n앞 글자는 하늘의 기운이에요. 나무·불·흙·쇠·물 중 하나예요.\n"
             "뒷 글자는 땅의 기운이에요. 열두 띠 동물 중 하나이고, 이 동물에도 다섯 기운 중 하나가 있어요.\n\n"
             "두 기운이 서로 키워 주는지, 겹치는지를 보고 그날의 분위기를 읽어요.\n")
    def blk(dt, info):
        hz = pillar(dt); g, z = GAN[hz[0]], ZHI[hz[1]]
        return f"{WD[dt.weekday()]} {dt.month}/{dt.day} {ko(hz)}({hz})\n{g[1]}({g[2]}) + {z[1]}({z[2]}). {info['mean'].replace(chr(10),' ')}\n→ {info['tip']}"
    pairs = list(zip(days, s["days"]))
    th = [intro + "이어지는 글에서 요일별로 풀어 드릴게요.",
          "\n\n".join(blk(*p) for p in pairs[:4]),
          "\n\n".join(blk(*p) for p in pairs[4:]) + "\n\n이 내용은 재미로, 그리고 나를 돌아보는 계기로 봐 주세요.\n여러분은 이번 주 어느 요일이 제일 바쁘세요?"]
    dl = "\n".join(f"{WD[dt.weekday()]} {dt.month}/{dt.day} {ko(pillar(dt))}({pillar(dt)}) · {i['mean'].split(chr(10))[0]}" for dt, i in pairs)
    ig = intro + "옆으로 넘기면 요일별 풀이가 있어요.\n\n" + dl + "\n\n저장해 두고 요일마다 꺼내 보세요.\n이 내용은 재미로, 그리고 나를 돌아보는 계기로 봐 주세요."
    return th, ig

if __name__ == "__main__":
    src = sys.argv[1]; C = json.load(open(src)); name = os.path.splitext(os.path.basename(src))[0]
    out = os.path.join(os.path.dirname(os.path.abspath(src)), "..", name); os.makedirs(out, exist_ok=True)
    for i, p in enumerate(C["posts"]):
        pre = f"{i+1:02d}"
        if p["image"]["type"] == "week": week(p["image"], out, pre)
        elif p["image"]["type"] == "trait": trait(p["image"], f"{out}/{pre}.jpg")
        else: card(p["image"], f"{out}/{pre}.jpg")
    print("rendered", len(C["posts"]), "->", out)
