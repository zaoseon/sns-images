"""정월의 카드 고르기 릴스 v2 (10/3 대표: 위가 잘림·검정 배경·글꼴·장면 전환 때 글자 겹침).
- 모든 글자·카드·정월이 safezone 안(위 330~아래 1470)에 있고, 렌더 뒤 모든 프레임을 검사한다(밖으로 나가면 실패).
- 배경은 우주(별·황도 고리·해와 달)로 꽉 채운다(검정 바 없음). 제목은 명조(serif.otf), 안내는 Pretendard.
- 장면이 바뀔 때 글자가 위로 사라진 뒤 다음 글자가 나온다(겹치지 않음). 음악은 직접 작곡(경쾌).
사용: python3 pipeline/pick_reel.py oct3|oct10   -> 2026-pick/v2/<날짜>.mp4"""
import os, sys, math, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, ".."); sys.path.insert(0, HERE)
import fonts_kit as K, clip_motion as M, safezone as Z, reel_music as RM, palette as P, music_plan as MP, face_plan as FP
from PIL import Image, ImageDraw, ImageFilter
P.apply_to_engine(M); M.BLACK = K.P["pr_xb"]; SER = os.path.join(HERE, "fonts", "serif.otf"); GM = K.P["gm_bold"]; PR = K.P["pr_xb"]; BOLD = GM; CX = M.CX
유형 = "훅·질문 표지"      # 10/16 기획 표(asset_lib.바탕표·판표)에서 이 글이 어디에 드는지 — 바탕과 판을 이 이름으로 고른다

# 색은 그릴 때 판에서 읽는다(10/16). 예전에는 금색 하나로 박혀 있어서 판을 돌려도 색이 안 바뀌었다 — K-071 의 '작은 층'만 바뀌는 꼴.
def 강조(a=255): return M.ACC(a)
def 밝은(a=255): return M.WHITE[:3] + (a,)
def _밝기(c): return (0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]) / 255
def CARDS():
    """카드 세 장의 색 — 판의 강조색·글색·보조색에서 가져온다. 서로 또렷하게 달라야 번호를 가리킬 수 있다."""
    acc, ink, sub = M.GOLD[:3], M.WHITE[:3], M.DIM[:3]
    if abs(_밝기(sub) - _밝기(ink)) < 0.18:      # 보조색이 글색과 닮았으면 강조색을 어둡게 돌려 쓴다
        sub = tuple(int(v * 0.55) for v in acc)
    return [("東", acc, "1"), ("西", ink, "2"), ("數", sub, "3")]
_c = {}
def card_layer(h, col, body_col, acc):
    k = (h, col, body_col, acc)
    if k in _c: return _c[k]
    w, hh = 258, 398; im = Image.new("RGBA", (w + 24, hh + 24), (0, 0, 0, 0)); g = Image.new("RGBA", (w + 24, hh + 24), (0, 0, 0, 0))
    ImageDraw.Draw(g).rounded_rectangle((12, 12, 12 + w, 12 + hh), radius=34, fill=col + (110,)); g = g.filter(ImageFilter.GaussianBlur(18)); im.alpha_composite(g)
    body = Image.new("RGBA", (w, hh)); bd = ImageDraw.Draw(body)
    for y in range(hh):   # 카드 바탕은 판의 카드색에서 위는 밝게 아래는 어둡게
        t = y / hh; bd.line((0, y, w, y), fill=tuple(min(255, int(v * (1.0 + 0.45 * t))) for v in body_col) + (255,))
    m = Image.new("L", (w, hh), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, hh - 1), radius=32, fill=255); body.putalpha(m); im.alpha_composite(body, (12, 12))
    d = ImageDraw.Draw(im); d.rounded_rectangle((12, 12, 12 + w, 12 + hh), radius=34, outline=acc + (255,), width=6); d.rounded_rectangle((30, 30, 12 + w - 18, 12 + hh - 18), radius=24, outline=acc + (110,), width=2)
    cx, cy = 12 + w // 2, 12 + hh // 2 - 8
    for r, a in ((96, 40), (84, 80)): d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=col + (a,), width=3)
    글색 = (26, 26, 30, 255) if _밝기(col) > 0.55 else (255, 255, 255, 255)   # 동그라미 색에 맞춰 글자색을 고른다(대비)
    d.ellipse((cx - 72, cy - 72, cx + 72, cy + 72), fill=col + (255,)); d.text((cx, cy - 4), h, font=M.font(SER, 92), fill=글색, anchor="mm")
    for (sx, sy) in ((46, 52), (w - 22, 52), (46, hh - 28), (w - 22, hh - 28)): d.text((sx, sy), "✦", font=M.font(M.MED, 26), fill=acc + (170,), anchor="mm")
    _c[k] = im; return im
def title(c, s, y, t0, size, color=None, lh=1.4): color = color or M.WHITE; return M.text(c, s, y, t0, size, color=(color + (255,) if len(color) == 3 else color), path=GM, maxw=820, lh=lh, stagger=0.2)
def small(c, s, y, t0, size, color=None): color = color or M.WHITE; return M.text(c, s, y, t0, size, color=(color + (255,) if len(color) == 3 else color), path=PR, maxw=820, lh=1.5, stagger=0.15)
def build(hook, sub, instr, note, face="v1_lowbun", cta="follow", dx=0, labels=None):
    def s1(c):
        M.chip(c, "정월의 카드 고르기", 345, .05); y = title(c, hook, 445, .2, 108)
        small(c, sub, y + 10, .8, 48, 강조()); M.character(c, face, t0=.3, width=730, bottom=1455, dx=dx)
    def s2(c):
        title(c, "끌리는 카드를\n하나 고르세요", 400, .05, 96)
        몸, 테 = M.CARD[:3], M.GOLD[:3]
        for i, (hj, col, no) in enumerate(CARDS()):
            cx = CX + (i - 1) * 290; fl = 8 * math.sin(c.t * 2.4 + i * 1.3); M.pop(c, card_layer(hj, col, 몸, 테), cx, 870 + fl, .25 + i * .18)
            if labels:   # 10/23 대표 요청: 카드마다 운명학 이름 + 한마디 역할(자세한 풀이는 캡션 본문)
                M.text(c, no, 1095, .7 + i * .12, 64, color=강조(), path=BOLD, maxw=300, cx=cx, stagger=0)
                M.text(c, labels[i][0], 1172, .85 + i * .12, 46, color=밝은(), path=BOLD, maxw=300, cx=cx, stagger=0)
                M.text(c, labels[i][1], 1230, .95 + i * .12, 42, color=강조(), path=PR, maxw=300, cx=cx, stagger=0)
            else:
                M.text(c, no, 1120, .7 + i * .12, 84, color=강조(), path=BOLD, maxw=300, cx=cx, stagger=0)
        if labels: title(c, instr, 1310, 1.5, 54, color=강조()); small(c, note, 1378, 1.9, 40)
        else: title(c, instr, 1240, 1.3, 62, color=강조()); small(c, note, 1334, 1.7, 44)   # 하단 고정 줄(y 1425~1465) 위에서 끝나게(10/7 규칙 층)
    def s3(c):
        if cta == "share":
            title(c, "떠오르는 사람에게\n보내 보세요", 480, .1, 112, color=강조()); small(c, "고른 번호와 함께 보내도 좋아요\n다음 편은 매주 올라와요", 900, .8, 56)
        else:
            title(c, "매일 저녁\n사주·별자리·숫자 테스트", 480, .1, 112, color=강조()); small(c, "팔로우하면 다음 편을\n놓치지 않아요", 900, .8, 56)
        small(c, "내 태어난 날 기운은 프로필 링크에서 1초", 1160, 1.3, 44, (255, 255, 255))
    return [(3.0, s1), (5.4, s2), (2.8, s3)]
def build_seq(hook, sub, labels, face="v1_lowbun", dx=0):
    """10/23 대표 요청(mvk2hxb3 다시): 한꺼번에 보이지 않고 차례로 — 세 카드 나란히 → 1번 카드가 커지며 '말 고르기' → 2번 '숨 고르기' → 3번 '정하기'
    → 다시 세 카드와 번호 아래 사주·별자리·수비학 → 몇 번 카드 골랐는지 댓글 묻기 → 마무리. 제목은 '지금 끌리는 카드를 하나 골라보세요',
    위 고정 줄과 붙지 않게 장면을 짧게 쪼개 자동 맞춤(맨 위 470 이상)이 글을 아래로 내리게 한다."""
    몸, 테 = M.CARD[:3], M.GOLD[:3]; 이름 = ["사주", "별자리", "수비학"]
    def s1(c):
        M.chip(c, "정월의 카드 고르기", 345, .05); y = title(c, hook, 445, .2, 108)
        small(c, sub, y + 10, .8, 48, 강조()); M.character(c, face, t0=.3, width=730, bottom=1455, dx=dx)
    def 세카드(c, cy, t0=.2, 둥실=True):
        for i, (hj, col, no) in enumerate(CARDS()):
            cx = CX + (i - 1) * 290; fl = (8 * math.sin(c.t * 2.4 + i * 1.3)) if 둥실 else 0
            M.pop(c, card_layer(hj, col, 몸, 테), cx, cy + fl, t0 + i * .15)
    def a(c):
        title(c, "지금 끌리는 카드를\n하나 골라보세요", 470, .05, 96); 세카드(c, 960)
    def 크게(i):
        def f(c):
            hj, col, no = CARDS()[i]; q = M.e_back((c.t - .1) / .45); k = 1.55 * max(.02, q)
            L = card_layer(hj, col, 몸, 테); L = L.resize((max(1, int(L.width * k)), max(1, int(L.height * k))))
            M.blit(c.fr, L, CX - L.width / 2, 800 - L.height / 2, c.alpha(M.cl(q * 2)))
            M.text(c, labels[i][1], 1175, .45, 96, color=강조(), path=BOLD, maxw=820, stagger=0)
        return f
    def d(c):
        세카드(c, 700, .1, 둥실=False)
        for i in range(3):
            cx = CX + (i - 1) * 290
            M.text(c, str(i + 1), 940, .55 + i * .12, 64, color=강조(), path=BOLD, maxw=300, cx=cx, stagger=0)
            M.text(c, 이름[i], 1020, .7 + i * .12, 56, color=밝은(), path=BOLD, maxw=300, cx=cx, stagger=0)
        title(c, "카드를 고르시고\n캡션 확인해보세요", 1150, 1.2, 60, color=강조())
    def e(c):
        y = title(c, "몇 번 카드\n고르셨어요?", 520, .1, 112, color=강조()); small(c, "댓글에 남겨 주세요", y + 30, .7, 64)
    def s3(c):
        title(c, "떠오르는 사람에게\n보내 보세요", 480, .1, 112, color=강조()); small(c, "고른 번호와 함께 보내도 좋아요\n다음 편은 매주 올라와요", 900, .8, 56)
        small(c, "내 태어난 날 기운은 프로필 링크에서 1초", 1160, 1.3, 44, (255, 255, 255))
    return [(2.6, s1), (2.4, a), (1.6, 크게(0)), (1.6, 크게(1)), (1.6, 크게(2)), (3.0, d), (2.4, e), (2.8, s3)]
SETS = {"oct3": dict(hook="10월, 나에게\n*먼저 오는 소식*", sub="세 장 중 하나만 고르세요", instr="끌리는 카드 번호를 댓글로", note="고른 뒤에 캡션을 열어 보세요", date="2026-10-03"),
        "oct10": dict(hook="그 사람이\n*곧 보여줄 행동*", sub="마음에 떠오르는 사람을 생각하세요", instr="끌리는 카드 번호를 댓글로", note="고른 뒤에 캡션을 열어 보세요", date="2026-10-10"),
        "oct17": dict(hook="마음이 복잡한 날,\n*나에게 필요한 것*", sub="카드 3장 중 하나만 고르세요", instr="끌리는 카드 번호를 댓글로", note="고른 뒤에 캡션을 열어 보세요", date="2026-10-17"),
        "oct24": dict(hook="요즘 마음에 걸린 일,\n*풀어 가는 순서*", sub="마음에 걸린 일 하나를 떠올리세요", instr="끌리는 카드 번호를 댓글로", note="고른 뒤에 캡션을 열어 보세요", date="2026-10-24"),
        "oct31": dict(hook="읽고도 답장 못 한 날,\n*내 마음이 하는 말*", sub="카드 3장 중 하나만 고르세요", instr="끌리는 카드 번호를 댓글로", note="고른 뒤에 캡션을 열어 보세요", date="2026-10-31", cta="share", face="v3_ponytail_flip", dx=-80, labels=[("사주", "말 고르기"), ("별자리", "숨 고르기"), ("수비학", "정하기")], seq=True),
        "nov7": dict(hook="말 걸고 싶은 날,\n*필요한 한 걸음*", sub="카드 3장 중 하나만 고르세요", instr="끌리는 카드 번호를 댓글로", note="고른 뒤에 캡션을 열어 보세요", date="2026-11-07", cta="share", face="intro", dx=140)}
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
    key = sys.argv[1] if len(sys.argv) > 1 else "oct3"; cfg = dict(SETS[key])
    if key in ("oct31", "nov7"):      # 새 편은 얼굴·음악을 돌려 쓰기 계획에서 고른다(계절 사진 포함)
        fi = FP.pick("ask", "pick-" + key, md=cfg["date"][5:]); cfg["face"] = fi["face"] + ("_flip" if fi["flip"] else ""); cfg["dx"] = -80 if fi["flip"] else 80
    # 그리기 전에 기획 표에서 판과 바탕을 고른다(대표 10/16 "배경이나 에셋 라이브러리처럼 만들어놓고 골라서", "컬러 조합도 마찬가지").
    # 검사도 렌더와 같은 판·바탕으로 해야 뜻이 있으니 여기서 먼저 정해 두고, 같은 값을 render 에 넘긴다.
    import asset_lib as A
    # 편마다 따로 돌려도 '앞 편과 같은 판·배경'이 안 나오게, 날짜 순서대로 한 번 쭉 정해 보고 이 편 것만 쓴다(K-068).
    쓴판, 쓴배경, 몫 = [], [], {}
    for k2 in sorted(SETS, key=lambda x: SETS[x]["date"]):
        d2 = SETS[k2]["date"]
        p2, 왜2 = A.판(유형, None, d2, 쓴판)
        m2 = 1
        while A.pick("bg", d2, 몫=m2) in 쓴배경[-2:] and m2 < 9:   # 배경도 앞 두 편과 겹치지 않게 다음 것을 뽑는다
            m2 += 1
        쓴판.append(p2); 쓴배경.append(A.pick("bg", d2, 몫=m2)); 몫[k2] = (p2, m2, 왜2)
    판번호, 배경몫, 판까닭 = 몫[key]
    if os.environ.get("ZS_PAL"): 판번호, 판까닭 = os.environ["ZS_PAL"], "사양에 직접 적음"
    M.set_pal(판번호); M.set_bg(M.bg_for(cfg["date"]))
    바탕종류, 배경이름, 바탕까닭 = M.set_backdrop(유형, os.environ.get("ZS_BACKDROP"), cfg["date"])
    if 바탕종류 == "배경" and 배경몫 > 1:       # 앞 편과 겹쳐서 다음 것을 뽑기로 한 편
        M.BACKDROP_IMG = 배경이름 = A.pick("bg", cfg["date"], 몫=배경몫)
        M.bg_static.cache_clear() if hasattr(M.bg_static, "cache_clear") else None
    print(f"판 {판번호} ({판까닭}) · 바탕 {바탕종류}" + (f" — {배경이름}" if 배경이름 else "") + f" ({바탕까닭})")
    sc = build_seq(cfg["hook"], cfg["sub"], cfg["labels"], face=cfg.get("face", "v1_lowbun"), dx=cfg.get("dx", 0)) if cfg.get("seq") else build(cfg["hook"], cfg["sub"], cfg["instr"], cfg["note"], cta=cfg.get("cta", "follow"), face=cfg.get("face", "v1_lowbun"), dx=cfg.get("dx", 0), labels=cfg.get("labels"))
    bad = check_frames(sc); print("안전 영역 검사:", "통과" if not bad else bad)
    if bad and "--force" not in sys.argv: sys.exit(1)
    out, secs = M.render(cfg["date"], sc, os.path.join(ROOT, "2026-pick", os.environ.get("ZS_PICK_OUT", "v3")), 내용유형=유형, 판=판번호)
    if key in ("oct31", "nov7"): mi = MP.choose("love", "pick-" + key); MP.mux(out, [d for d, _ in sc], mi, {"oct31": 75, "nov7": 76}[key]); print("음악:", mi["style"], mi["bpm"], mi["key"], "| 얼굴:", cfg["face"])
    else: music(out, sc, {"oct3": 71, "oct10": 72, "oct17": 73, "oct24": 74}[key])
    print(out, secs, "초")
