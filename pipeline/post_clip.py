"""네이버 '게시물 클립'(이미지+짧은 글) 만들기 (10/3 대표 승인: 블로그 글 1편 -> 동영상 클립 + 게시물 클립).
규칙: 1080x1350(4:5). 핵심 글자는 가운데 1080x1080 안(1:1로 잘려도 읽히게). 정월이 나오는 장에는 AI 표시를 가운데 정사각 안, 우하단 연회색.
숫자(음력·요일·방향별 날짜)는 코드로 계산하고 글에 적은 값과 다르면 생성을 멈춘다. 사용: python3 pipeline/post_clip.py s10
출력: clips_post/<글>/<글>_1~N.jpg, clips_post/<글>.zip, content/post_clips.json 갱신"""
import os, sys, json, zipfile, calendar, datetime as D
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, "..")
sys.path.insert(0, os.path.join(ROOT, "naver"))
from PIL import Image, ImageDraw
import thumb_sq as T
sys.path.insert(0, os.path.join(ROOT, "..", "zaoseon-site", "tools", "checks"))
W, H = 1080, 1350; WD = "일월화수목금토"      # 달력은 일요일 시작
F, SER, SEMI, MED, BLK = T.F, T.SER, T.SEMI, T.MED, T.BLK
def lunar(d):
    from korean_lunar_calendar import KoreanLunarCalendar
    c = KoreanLunarCalendar(); c.setSolarDate(d.year, d.month, d.day); a = c.LunarIsoFormat().split("-"); return int(a[1]), int(a[2])
def wk(d): return "월화수목금토일"[d.weekday()]
def new(c): im = Image.new("RGB", (W, H), c.bg); return im, ImageDraw.Draw(im)
def pill(d, c, x, y, t):
    f = F(SEMI, 38); w = d.textlength(t, font=f) + 58; d.rounded_rectangle([x, y, x + w, y + 70], 35, fill=c.acc); d.text((x + 29, y + 35), t, font=f, fill=c.pillfg, anchor="lm")
NOPAGE = bool(os.environ.get("NOPAGE"))        # 10/4 대표: 영상용은 위 페이지 번호를 뺀다
def pager(d, c, n, total):
    if NOPAGE: return
    d.text((W - 80, 125), f"{n} / {total}", font=F(SEMI, 34), fill=c.gray, anchor="rm")
def footer(d, c):
    d.text((80, 1262), "子午線 자오선", font=F(SER, 34), fill=c.acc); d.text((W - 80, 1262), "zaoseon.com", font=F(MED, 28), fill=c.gray, anchor="rm")
def ai(d, c, y=1170):
    t = "AI로 생성한 가상의 캐릭터입니다"; f = F(MED, 24); tw = d.textlength(t, font=f)
    d.rounded_rectangle([W - 70 - tw - 26, y, W - 70, y + 42], 21, fill=c.bg); d.text((W - 83, y + 21), t, font=f, fill=c.gray, anchor="rm")
def lines(d, ls, x, y, size, col, path=SER, center=False, lh=1.2):
    for l in ls:
        d.text((W // 2 if center else x, y), l, font=F(path, size), fill=col, anchor="ma" if center else "la"); y += int(size * lh)
    return y
def fit(d, ls, maxw, start, lo=70, path=SER):
    s = start
    while s > lo and max(d.textlength(l, font=F(path, s)) for l in ls) > maxw: s -= 4
    return s
def build_s10():
    Y, M = 2026, 10; E = "흙"; tot = 6
    cal = {day: lunar(D.date(Y, M, day)) for day in range(1, 32)}
    hot = [day for day in cal if cal[day][1] % 10 in (9, 0)]
    assert hot == [9, 10, 19, 20, 29, 30], hot                                  # 글에 적은 손 없는 날과 같은가
    assert [wk(D.date(Y, M, d)) for d in hot] == ["금", "토", "월", "화", "목", "금"]
    assert D.date(Y, 10, 9).weekday() == 4 and D.date(Y, 10, 11).weekday() == 6  # 한글날 금요일 → 9~11일 연휴
    assert [d for d in hot if D.date(Y, M, d).weekday() >= 5] == [10]            # 주말 손 없는 날은 10일 하루
    dirs = {"동쪽": (1, 2), "남쪽": (3, 4), "서쪽": (5, 6), "북쪽": (7, 8)}
    dd = {k: [d for d in range(1, 32) if cal[d][1] % 10 in v] for k, v in dirs.items()}
    assert dd["남쪽"] == [3, 4, 13, 14, 23, 24] and dd["동쪽"] == [1, 2, 11, 12, 21, 22, 31]
    L, Dk = T.Ctx(E, False), T.Ctx(E, True); out = []
    # 1 표지(어두운 판)
    im, d = new(Dk); pill(d, Dk, 80, 150, "10월 손 없는 날"); pager(d, Dk, 1, tot)
    d.text((820, 640), "宅", font=F(SER, 760), fill=Dk.tint, anchor="mm")
    cv = T.head_circle("v1_lowbun", 240, Dk); d.ellipse([80, 255, 340, 515], fill=T.GOLD); im.paste(cv, (90, 265), cv)
    y = lines(d, ["이사 날짜,", "이 6일이면", "돼요"], 80, 540, 140, Dk.fg)
    d.text((80, y + 10), "9 · 10 · 19 · 20 · 29 · 30일", font=F(SEMI, 50), fill=Dk.acc); (None if NOPAGE else d.text((80, y + 88), "옆으로 넘겨서 달력 보기 →", font=F(MED, 34), fill=Dk.gray))
    ai(d, Dk); footer(d, Dk); out.append(im)
    # 2 달력
    im, d = new(L); pill(d, L, 80, 150, "10월 달력"); pager(d, L, 2, tot)
    d.text((80, 260), "손 없는 날은", font=F(SER, 88), fill=L.fg); d.text((80, 365), "이 여섯 날이에요", font=F(SER, 88), fill=L.fg)
    x0, cw, g = 55, 130, 8; y0 = 550
    for i, n in enumerate(WD): d.text((x0 + i * (cw + g) + cw // 2, y0 - 36), n, font=F(SEMI, 34), fill=L.acc if n != "일" else (196, 74, 52), anchor="mm")
    first = D.date(Y, M, 1).weekday(); col0 = (first + 1) % 7
    for day in range(1, 32):
        pos = col0 + day - 1; x = x0 + (pos % 7) * (cw + g); yy = y0 + (pos // 7) * (108 + g); on = day in hot
        d.rounded_rectangle([x, yy, x + cw, yy + 108], 20, fill=L.acc if on else L.card, outline=L.acc if on else L.line, width=3)
        d.text((x + cw // 2, yy + 54), str(day), font=F(BLK if on else SEMI, 52 if on else 46), fill=(255, 255, 255) if on else L.fg, anchor="mm")
    d.text((80, 1178), "음력 날짜의 끝자리가 9나 0인 날이에요", font=F(MED, 34), fill=L.gray); footer(d, L); out.append(im)
    # 3 주말
    im, d = new(L); pill(d, L, 80, 150, "주말이 필요하다면"); pager(d, L, 3, tot)
    d.text((80, 300), "10일(토)", font=F(BLK, 230), fill=L.acc)
    y = lines(d, ["10월의 유일한", "주말 손 없는 날이에요"], 80, 590, 86, L.fg)
    d.rounded_rectangle([80, y + 50, W - 80, y + 330], 36, fill=L.card, outline=L.line, width=4)
    d.text((120, y + 90), "9일(금)은", font=F(SEMI, 46), fill=L.acc)
    lines(d, ["한글날 연휴 첫날과 겹쳐요.", "예약이 일찍 찰 수 있어요."], 120, y + 160, 50, L.fg, path=SEMI, lh=1.35); footer(d, L); out.append(im)
    # 4 평일
    im, d = new(L); pill(d, L, 80, 150, "평일이 괜찮다면"); pager(d, L, 4, tot)
    d.text((80, 285), "평일은 네 날이에요", font=F(SER, 92), fill=L.fg)
    for i, (lab, days, note) in enumerate([("중순", "19일(월) · 20일(화)", "일정 조율이 쉬워요"), ("월말", "29일(목) · 30일(금)", "이사가 몰리기 쉬워 붐빌 수 있어요")]):
        top = 470 + i * 330; d.rounded_rectangle([80, top, W - 80, top + 290], 40, fill=L.card, outline=L.acc if i == 0 else L.line, width=5)
        d.text((125, top + 45), lab, font=F(SEMI, 44), fill=L.acc); d.text((125, top + 115), days, font=F(SER, 66), fill=L.fg); d.text((125, top + 215), note, font=F(MED, 40), fill=L.gray)
    footer(d, L); out.append(im)
    # 5 방향별
    im, d = new(L); pill(d, L, 80, 150, "손 없는 날이 아니어도"); pager(d, L, 5, tot)
    d.text((80, 270), "방향만 맞아도 괜찮아요", font=F(SER, 80), fill=L.fg)
    d.text((80, 385), "새집 방향에 손이 없는 날이면 된다고 봐요", font=F(MED, 38), fill=L.gray)
    for i, (k, v) in enumerate(dirs.items()):
        top = 500 + i * 170; d.rounded_rectangle([60, top, W - 60, top + 150], 30, fill=L.card, outline=L.line, width=3)
        d.text((100, top + 28), k, font=F(SER, 54), fill=L.acc); d.text((100, top + 98), f"음력 끝자리 {v[0]}·{v[1]}", font=F(MED, 30), fill=L.gray)
        days = " · ".join(str(x) for x in dd[k]) + "일"; s = fit(d, [days], 560, 40, 28, SEMI)
        d.text((W - 100, top + 75), days, font=F(SEMI, s), fill=L.fg, anchor="rm")
    d.text((80, 1190), "이 날짜를 피하면 돼요. 방향은 지금 집에서 새집을 본 쪽이에요", font=F(MED, 30), fill=L.gray); footer(d, L); out.append(im)
    # 6 CTA(어두운 판)
    im, d = new(Dk); pill(d, Dk, 80, 150, "전체는 블로그에"); pager(d, Dk, 6, tot)
    d.text((800, 560), "擇", font=F(SER, 700), fill=Dk.tint, anchor="mm")
    y = lines(d, ["날짜 고르는", "순서까지", "정리했어요"], 80, 290, 132, Dk.fg)
    lines(d, ["방향별 전체 표와", "고르는 순서는", "블로그에 있어요"], 80, y + 30, 50, Dk.acc, path=SEMI, lh=1.4)
    d.rounded_rectangle([80, 1050, 640, 1140], 45, fill=Dk.acc); d.text((360, 1095), "블로그 스티커 눌러 보기", font=F(BLK, 40), fill=Dk.bg, anchor="mm")
    cv = T.head_circle("v1_lowbun", 200, Dk); d.ellipse([786, 950, 996, 1160], fill=T.GOLD); im.paste(cv, (791, 955), cv)
    d.text((80, 1180), "오래 이어져 온 생활 풍습이에요. 재미로 참고해 주세요", font=F(MED, 28), fill=Dk.gray)
    ai(d, Dk, 1178); footer(d, Dk); out.append(im)
    return out
BUILD = {"s10": build_s10}
if __name__ == "__main__":
    if os.environ.get("ALLOW_45_CLIP") != "1": sys.exit("R15(10/6 확정): 네이버 클립은 9:16 영상으로만 만든다. 4:5 카드를 클립으로 올리지 않는다 — 클립 엔진(clip_motion)으로 만들 것. (예외로 쓰려면 ALLOW_45_CLIP=1)")
    pid = sys.argv[1] if len(sys.argv) > 1 else "s10"; imgs = BUILD[pid](); od = os.path.join(ROOT, "clips_post", pid + ("_nopage" if NOPAGE else "")); os.makedirs(od, exist_ok=True)
    names = []
    for i, im in enumerate(imgs, 1):
        p = os.path.join(od, f"{pid}_{i}.jpg"); im.save(p, quality=92); names.append(p)
    with zipfile.ZipFile(os.path.join(ROOT, "clips_post", f"{pid}{'_nopage' if NOPAGE else ''}.zip"), "w", zipfile.ZIP_STORED) as z:
        for p in names: z.write(p, os.path.basename(p))
    print(pid, len(imgs), "장", [os.path.getsize(p) // 1024 for p in names], "KB")
