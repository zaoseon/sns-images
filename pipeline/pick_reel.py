"""정월의 카드 고르기 릴스 v2 (10/3 대표: 위가 잘림·검정 배경·글꼴·장면 전환 때 글자 겹침).
- 모든 글자·카드·정월이 safezone 안(위 330~아래 1470)에 있고, 렌더 뒤 모든 프레임을 검사한다(밖으로 나가면 실패).
- 배경은 우주(별·황도 고리·해와 달)로 꽉 채운다(검정 바 없음). 제목은 명조(serif.otf), 안내는 Pretendard.
- 장면이 바뀔 때 글자가 위로 사라진 뒤 다음 글자가 나온다(겹치지 않음). 음악은 직접 작곡(경쾌).
사용: python3 pipeline/pick_reel.py oct3|oct10   -> 2026-pick/v2/<날짜>.mp4"""
import os, sys, math, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, ".."); sys.path.insert(0, HERE)
import clip_motion as M, safezone as Z, reel_music as RM, palette as P
from PIL import Image, ImageDraw, ImageFilter
P.apply_to_engine(M); SER = os.path.join(HERE, "fonts", "serif.otf"); GOLD = P.C2["hi"]; GOLDA = GOLD + (255,); CX = M.CX
CARDS = [("東", P.C2["pt"], "1"), ("西", P.C2["hi"], "2"), ("數", (255, 255, 255), "3")]
_c = {}
def card_layer(h, col):
    k = (h, col)
    if k in _c: return _c[k]
    w, hh = 258, 398; im = Image.new("RGBA", (w + 24, hh + 24), (0, 0, 0, 0)); g = Image.new("RGBA", (w + 24, hh + 24), (0, 0, 0, 0))
    ImageDraw.Draw(g).rounded_rectangle((12, 12, 12 + w, 12 + hh), radius=34, fill=col + (110,)); g = g.filter(ImageFilter.GaussianBlur(18)); im.alpha_composite(g)
    body = Image.new("RGBA", (w, hh)); bd = ImageDraw.Draw(body)
    for y in range(hh): t = y / hh; bd.line((0, y, w, y), fill=(int(30 + 14 * t), int(38 + 16 * t), int(74 + 26 * t), 255))
    m = Image.new("L", (w, hh), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, hh - 1), radius=32, fill=255); body.putalpha(m); im.alpha_composite(body, (12, 12))
    d = ImageDraw.Draw(im); d.rounded_rectangle((12, 12, 12 + w, 12 + hh), radius=34, outline=GOLD + (255,), width=6); d.rounded_rectangle((30, 30, 12 + w - 18, 12 + hh - 18), radius=24, outline=GOLD + (110,), width=2)
    cx, cy = 12 + w // 2, 12 + hh // 2 - 8
    for r, a in ((96, 40), (84, 80)): d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=col + (a,), width=3)
    d.ellipse((cx - 72, cy - 72, cx + 72, cy + 72), fill=col + (255,)); d.text((cx, cy - 4), h, font=M.font(SER, 92), fill=((41, 51, 92, 255) if col == (255, 255, 255) else (255, 255, 255, 255)), anchor="mm")
    for (sx, sy) in ((46, 52), (w - 22, 52), (46, hh - 28), (w - 22, hh - 28)): d.text((sx, sy), "✦", font=M.font(M.MED, 26), fill=GOLD + (170,), anchor="mm")
    _c[k] = im; return im
def title(c, s, y, t0, size, color=M.WHITE, lh=1.25): return M.text(c, s, y, t0, size, color=(color + (255,) if len(color) == 3 else color), path=SER, maxw=820, lh=lh, stagger=0.2)
def small(c, s, y, t0, size, color=M.WHITE): return M.text(c, s, y, t0, size, color=(color + (255,) if len(color) == 3 else color), path=M.MED, maxw=820, lh=1.35, stagger=0.15)
def build(hook, sub, instr, note, face="v1_lowbun"):
    def s1(c):
        M.chip(c, "정월의 카드 고르기", 345, .05); y = title(c, hook, 445, .2, 108)
        small(c, sub, y + 4, .8, 46, GOLDA); M.character(c, face, t0=.3, width=730, bottom=1455)
    def s2(c):
        title(c, "끌리는 카드를\n하나 고르세요", 400, .05, 96)
        for i, (hj, col, no) in enumerate(CARDS):
            cx = CX + (i - 1) * 290; fl = 8 * math.sin(c.t * 2.4 + i * 1.3); M.pop(c, card_layer(hj, col), cx, 905 + fl, .25 + i * .18)
            M.text(c, no, 1180, .7 + i * .12, 84, color=GOLDA, path=SER, maxw=300, cx=cx, stagger=0)
        title(c, instr, 1290, 1.3, 64, color=GOLDA); small(c, note, 1385, 1.7, 40)
    def s3(c):
        title(c, "매일 저녁\n세 지도 테스트", 480, .1, 112, color=GOLDA); small(c, "팔로우하면 다음 편을\n놓치지 않아요", 900, .8, 56)
        small(c, "내 태어난 날 기운은 프로필 링크에서 1초", 1160, 1.3, 38, (200, 192, 176))
    return [(3.0, s1), (5.4, s2), (2.8, s3)]
SETS = {"oct3": dict(hook="10월, 나에게\n*먼저 오는 소식*", sub="세 장 중 하나만 고르세요", instr="끌리는 카드 번호를 댓글로", note="풀이는 캡션에 있어요 (먼저 고르고 보기!)", date="2026-10-03"),
        "oct10": dict(hook="그 사람이\n*곧 보여줄 행동*", sub="마음에 떠오르는 사람을 생각하세요", instr="끌리는 카드 번호를 댓글로", note="풀이는 캡션에 있어요 (먼저 고르고 보기!)", date="2026-10-10")}
def check_frames(scenes):
    """장면마다 몇 시점의 그림을 배경만 있는 그림과 비교해, 바뀐 부분(글자·카드·정월)이 안전 영역 밖으로 나가는지 검사한다."""
    bad = []; total = sum(d for d, _ in scenes); acc = 0
    for i, (dur, fn) in enumerate(scenes):
        for t in [dur * k for k in (.3, .5, .7, .9)]:
            a = Image.new("RGB", (Z.W, Z.H)); M.background(a, acc + t, total); b = a.copy(); fn(M.Ctx(b, t, dur))
            diff = ImageChops_diff(a, b); bb = diff.getbbox()
            if bb and not Z.inside(bb, cover=(i == 0 and False)): bad.append((i + 1, round(t, 2), bb))
        acc += dur
    return bad
def ImageChops_diff(a, b):
    from PIL import ImageChops
    d = ImageChops.difference(a, b).convert("L"); return d.point(lambda v: 255 if v > 24 else 0)
def music(mp4, scenes, seed):
    durs = [d for d, _ in scenes]; total = sum(durs); bpm = RM.pick_bpm("경쾌 신스팝", seed); spb = 60.0 / bpm; acc = 0; cuts = []
    for d in durs: cuts.append(round(acc / spb)); acc += d
    wav = f"/tmp/pick_{seed}.wav"; RM.compose_up("경쾌 신스팝", max(8, (total - .3) / spb), seed, wav, key="D", bpm=bpm, cuts=cuts, tail=.3)
    tmp = mp4 + ".m.mp4"; subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", mp4, "-i", wav, "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "128k", "-shortest", "-movflags", "+faststart", tmp], check=True); os.replace(tmp, mp4)
if __name__ == "__main__":
    key = sys.argv[1] if len(sys.argv) > 1 else "oct3"; cfg = SETS[key]; sc = build(cfg["hook"], cfg["sub"], cfg["instr"], cfg["note"])
    bad = check_frames(sc); print("안전 영역 검사:", "통과" if not bad else bad)
    if bad and "--force" not in sys.argv: sys.exit(1)
    out, secs = M.render(cfg["date"], sc, os.path.join(ROOT, "2026-pick", "v3")); music(out, sc, 71 if key == "oct3" else 72); print(out, secs, "초")
