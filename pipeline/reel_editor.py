"""릴스 렌더러 (10/1 밤): 대표가 올린 캐러셀 샘플 레이아웃을 그대로 9:16(1080x1920)에 얹는다.
장면(약 10.5초, 무음): 표지(훅) -> 성격 -> 연애 -> 돈 -> CTA. 캐러셀 슬라이드 1·2·3·4·7과 같은 배치(배지 55, 제목 100/113, 본문 54.5, 핸들, 얼굴 위치, 우주 배경 밴드, 흐림 패널, CTA 버튼).
- 같은 편집기 코드로 그림(캔버스만 1080x1920으로 늘림), 글꼴 Noto Sans CJK KR
- 인스타 릴스 UI 안전 영역: 위 약 230px, 아래 약 340px(캡션·버튼) -> 표지는 위로 170px 내리고, 본문·CTA는 세로 가운데(285px 내림), 핸들은 y 1528
- 얼굴이 나오는 표지에만 AI 문구(우하단 2줄)
사용: python3 pipeline/reel_editor.py [날짜...]  -> 2026-w40car-reel2/YYYY-MM-DD.mp4"""
import base64, io, json, os, subprocess, sys
from PIL import Image
from playwright.sync_api import sync_playwright
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, "..")
sys.path.insert(0, os.path.join(ROOT, "content")); sys.path.insert(0, HERE)
import carousel_editor as CE
from carousel_sets import SETS
OUT = os.path.join(ROOT, "2026-w40car-reel2")
H_REEL = 1920

def build_html():
    s = open(CE.EDITOR, encoding="utf-8", errors="replace").read()
    s = s.replace("px sans-serif", "px " + CE.FONT)
    s = s.replace("`600 ${s.bodySize}px", "`700 ${s.bodySize}px").replace("wrapRich(s.body, W-140, bodyFont)", "wrapRich(s.body, W-60, bodyFont)")
    assert "const W=1080, H=1350;" in s and 'width="1080" height="1350"' in s
    s = s.replace("const W=1080, H=1350;", f"const W=1080, H={H_REEL};").replace('width="1080" height="1350"', f'width="1080" height="{H_REEL}"')
    open("/tmp/editor_reel.html", "w", encoding="utf-8").write(s)

REEL_JS = r"""
(args) => {
  const [def, extra] = args;
  const FONT='"Noto Sans CJK KR", sans-serif'; const F=(w,px)=>`${w} ${px}px ${FONT}`;
  const sl = buildSet(def); slides.length = 0; sl.forEach(s => slides.push(s));
  const tw=(t,w,px)=>{ ctx.font=F(w,px); return ctx.measureText(t).width; };
  const balance=(txt,w,px,maxW)=>{ if (txt.includes('\n')) return txt.split('\n').map(l=>balance(l,w,px,maxW)).join('\n');
    if (tw(txt,w,px) <= maxW) return txt; let best=null;
    for (let i=1;i<txt.length-1;i++){ if (txt[i]!==' ') continue; const a=txt.slice(0,i), b=txt.slice(i+1); const wa=tw(a,w,px), wb=tw(b,w,px);
      if (wa<=maxW && wb<=maxW){ const sc=Math.abs(wa-wb)-((/[,.]$/.test(a))?120:0); if(!best||sc<best.sc) best={sc,s:a+'\n'+b}; } }
    return best?best.s:txt; };
  globalCfg.accent = def.accent; globalCfg.applyAll = false;
  globalCfg.applyAllHandle = false;
  slides.forEach((s,i)=>{ s.handleX=104; s.handleSize=38; if(i===0){ s.handleText='zaoseon.com'; s.handleY=1448; s.handleDot=18; } else { s.handleText=''; s.handleY=1528; s.handleDot=0.01; } });
  const panel=(x,y,w,h,blur,dark)=>({x,y,w,h,blur,dark,round:0,enabled:true});
  const bgOff=(scale,top)=> top - (H - 720*scale);
  slides.forEach(s => { s.pageBadgeEnabled = false; });
  // 표지: 캐러셀 표지를 170px 아래로(위 UI 피함), 얼굴은 화면 아래까지
  const c = slides[0]; const TA = 170;
  c.bgColor='#100a05'; c.imgScale=1.2; c.imgOffX=230; c.imgOffY=(422+TA)-(H-1728); c.panelOverride=panel(0,0,0,0,0,0); c.panelOverride.enabled=false;
  c.kickerX=75; c.kickerY=79+TA; c.kickerSize=51;
  c.subSize=66; while (c.subSize>40 && wrapRich(c.sub,W-120,F(900,c.subSize)).length>1) c.subSize-=1; c.subX=88; c.subY=270+TA;
  const tl=def.coverTitle.split('\n').length; c.titleSize=113; while (c.titleSize>70 && wrapRich(c.title,W-120,F(900,c.titleSize)).length>tl) c.titleSize-=1;
  c.titleX=88; c.titleY=416+TA;
  ctx.font=F(600,22); const ai=['※ 자오선의 상담가 정월은','AI로 생성한 가상 캐릭터입니다'];
  c.extraTexts = ai.map((t,i)=>({text:t, x:1052-ctx.measureText(t).width, y:1450+i*24, size:22, color:'#8d8782', bold:false, align:'left', stroke:false}));
  // 본문 3장(성격/연애/돈): 캐러셀 본문 배치를 세로 가운데(+285)로
  const TB = 285;
  [1,2,3].forEach((i,k) => {
    const s = slides[i];
    if (extra.badges) s.badge = extra.badges[k];
    s.bgColor='#1a1816'; s.face='bg_sunmoon'; s.imgScale=1.265; s.imgOffX=-40; s.imgOffY=bgOff(1.265,216+TB); s.panelOverride=panel(0,216+TB,1080,916,6,102);
    s.title=balance(s.title,900,100,930); s.body=balance(s.body,700,54.5,946);
    s.badgeX=540; s.badgeSize=55; s.titleSize=100; s.bodySize=54.5;
    const nb=wrapRich(s.body,W-60,F(700,54.5)).length, nt=wrapRich(s.title,W-100,F(900,100)).length;
    if (nb>=3) { s.badgeY=327+TB; s.titleY=541+TB; s.bodyY=841+TB; } else { s.badgeY=350+TB; s.titleY=597+TB; s.bodyY=902+TB; }
    if (nt===1) s.titleY+=61;
  });
  // CTA
  const t = slides[6]; t.bgColor='#1a1816'; t.face='bg_sunmoon'; t.imgScale=1.379; t.imgOffX=-90; t.imgOffY=bgOff(1.379,167+TB); t.panelOverride=panel(0,167+TB,1080,993,14,128);
  t.qSize=89; t.qY=378.5+TB; t.btn='팔로우하고 같이 얘기 나눠요'; t.btnSize=50; t.btnY=558+TB;
  t.nextBadge = extra.nextBadge || '내일 밤 9시'; t.nextBadgeSize=39; t.nextY=785+TB; t.nextTitleSize=67; t.nextTitle = extra.nextTitle || t.nextTitle;
  t.hint='프로필 링크에서 내 기운 1초만에 확인'; t.hintSize=38;
  return slides.length;
}
"""

def split_val(v):
    if len(v) <= 10: return v
    parts = [p.strip() for p in v.split(" · ")]
    if len(parts) == 2: return "\n".join(parts)
    if len(parts) >= 3: return parts[0] + " · " + parts[1] + "\n" + " · ".join(parts[2:])
    if ", " in v: a, b = v.split(", ", 1); return a + ",\n" + b
    return v

def tri_def(date, fix_idx, face, hook, sub, q, nxt):
    fix = json.load(open(os.path.join(ROOT, "content", "2026-w40fix.json"), encoding="utf-8"))["posts"][fix_idx - 1]["image"]
    rows = fix["rows"]; lab = {"사주": "사주", "별자리": "별자리", "수비학": "수비학"}
    mk = lambda r: [split_val(r[2]), r[3]]
    return dict(dayChar="세", hanja="圖", accent="#ffd640", face=face, kicker="정월의 세 지도", coverTitle=hook, coverSub=sub,
                personality=mk(rows[0]), love=mk(rows[1]), money=mk(rows[2]), advice=["", ""], chartNote="", values=[.3, .3, .3, .3, .3], highlight=0, ctaQ=q, nextTitle=nxt), [lab[r[0]] for r in rows]

def day_def(S):
    return dict(dayChar=S["dayChar"], hanja=S["hanja"], accent=S["accent"], face=("v5_halfup_v2" if S["face"] == "v5_halfup" else S["face"]), kicker=S["kicker"], coverTitle=S["coverTitle"],
                coverSub=S["coverSub"], personality=S["personality"], love=S["love"], money=S["money"], advice=S["advice"], chartNote=S["chartNote"], values=S["values"], highlight=S["highlight"],
                ctaQ=S["ctaQ"], nextTitle=S["nextTitle"])

REELS = {  # date: (kind, args)
    "2026-10-02": ("day", "2026-10-02", "내일 낮 12시", "세 지도 테스트"),
    "2026-10-03": ("tri", 1, "v3_ponytail", "헤어진 뒤 다시\n연락하는 사람", "사주·별자리·숫자, 셋 중 몇 개 겹쳐요?", "나는 몇 개\n*겹쳐요*?", "내일 낮 12시", "기(己)일생 편"),
    "2026-10-04": ("day", "2026-10-04", "내일 낮 12시", "세 지도 테스트"),
    "2026-10-05": ("tri", 3, "v5_halfup_v2", "돈이 모이는\n사람의 공통점", "동양과 서양이 같은 답을 했어요", "나는 몇 개\n*겹쳐요*?", "내일 낮 12시", "경(庚)일생 편"),
    "2026-10-06": ("day", "2026-10-06", "내일 낮 12시", "신(辛)일생 편"),
    "2026-10-07": ("day", "2026-10-07", "내일 낮 12시", "임(壬)일생 편"),
    "2026-10-08": ("day", "2026-10-08", "내일 낮 12시", "계(癸)일생 편"),
    "2026-10-09": ("day", "2026-10-09", "내일 낮 12시", "세 지도 테스트"),
    "2026-10-10": ("tri", 4, "v7_hanbok", "빨리 달아오르고\n빨리 식는 사람", "사주·별자리·숫자, 셋 중 몇 개 겹쳐요?", "나는 몇 개\n*겹쳐요*?", "내일 낮 12시", "세 지도 테스트"),
    "2026-10-11": ("tri", 5, "v11_mug", "'일단 하자' vs\n'한 번 더 생각하자'", "세 지도로 보는 나의 속도", "나는 *어느 쪽*\n이에요?", "내일부터", "이번 주 기운 편"),
}
DUR = [2.4, 1.9, 1.9, 1.9, 2.4]; FADE = 0.25

from PIL import ImageFilter, ImageDraw, ImageFont
BG = Image.open(os.path.join(ROOT, "characters", "cut", "bg_sunmoon.jpg")).convert("RGB")
def backdrop():
    w = int(BG.width * H_REEL / BG.height); im = BG.resize((w, H_REEL), Image.LANCZOS); x = (w - 1080) // 2
    im = im.crop((x, 0, x + 1080, H_REEL)).filter(ImageFilter.GaussianBlur(28))
    return Image.eval(im, lambda v: int(v * 0.42))
def post(im, band, accent):
    """본문·CTA: 샘플의 밴드는 그대로 두고, 위아래 빈 막대만 어둡게 흐린 우주 배경으로 채운 뒤 핸들(샘플과 같은 크기)을 그린다"""
    top, bot = band; bd = backdrop(); out = bd.copy()
    out.paste(im.crop((0, top, 1080, bot)), (0, top))
    # 밴드 경계 40px 페더
    for (y0, y1, up) in [(top, top + 40, True), (bot - 40, bot, False)]:
        for y in range(y0, y1):
            t = (y - y0) / 40.0; a = t if up else 1 - t
            row_band = im.crop((0, y, 1080, y + 1)); row_bd = bd.crop((0, y, 1080, y + 1))
            out.paste(Image.blend(row_bd, row_band, a), (0, y))
    d = ImageDraw.Draw(out); ac = tuple(int(accent.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4))
    d.ellipse([74 - 18, 1528 - 18, 74 + 18, 1528 + 18], fill=ac)
    f = ImageFont.truetype("/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc", 38, index=1)
    d.text((104, 1528), "zaoseon.com", font=f, fill=(255, 255, 255), anchor="lm")
    return out
def assemble(frames, mp4):
    cmd = ["ffmpeg", "-y", "-loglevel", "error"]
    for f, d in zip(frames, DUR): cmd += ["-loop", "1", "-t", str(d), "-i", f]
    total = sum(DUR) - FADE * (len(DUR) - 1)
    cmd += ["-f", "lavfi", "-t", f"{total:.2f}", "-i", "anullsrc=r=44100:cl=stereo"]
    fl = ""; prev = "[0:v]"; off = 0.0
    for i in range(1, len(frames)):
        off += DUR[i - 1] - FADE; out = f"[v{i}]"
        fl += f"{prev}[{i}:v]xfade=transition=fade:duration={FADE}:offset={off:.2f}{out};"; prev = out
    fl += f"{prev}format=yuv420p,fps=30[vout]"
    cmd += ["-filter_complex", fl, "-map", "[vout]", "-map", f"{len(frames)}:a", "-c:v", "libx264", "-crf", "20", "-c:a", "aac", "-b:a", "96k", "-shortest", "-movflags", "+faststart", mp4]
    subprocess.run(cmd, check=True)

def main():
    only = [a for a in sys.argv[1:] if not a.startswith("--")]
    build_html(); os.makedirs(OUT, exist_ok=True)
    if not os.path.exists(CE.PLATE): CE.make_plate()
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1300, "height": 900})
        pg.goto("file:///tmp/editor_reel.html"); pg.wait_for_timeout(1500)
        pg.evaluate("Promise.all([400,500,600,700,900].map(w=>document.fonts.load(w+' 40px \"Noto Sans CJK KR\"','가한丁')))")
        faces = {"v7_hanbok", "v11_mug", "v13_horn_glasses", "v6_winter", "v8_gesture", "v1_lowbun", "v3_ponytail"} | {S["face"] for S in SETS.values()}
        for f in faces:
            k, u = CE.face_dataurl(f)
            if k in ("v1_lowbun", "v2_straight", "v3_ponytail", "v4_glasses", "v5_halfup_v2"): continue
            pg.evaluate("async ([k,u])=>{FACES[k]=u; const im=new Image(); im.src=u; await im.decode(); imgCache[k]=im;}", [k, u])
        for date, spec in REELS.items():
            if only and date not in only: continue
            if spec[0] == "day":
                S = SETS[spec[1]]; d = day_def(S); extra = {"nextBadge": spec[2], "nextTitle": spec[3]}
            else:
                _, fi, face, hook, sub, q, nb, nt = spec; d, badges = tri_def(date, fi, face, hook, sub, q, nt); extra = {"badges": badges, "nextBadge": nb, "nextTitle": nt}
            pg.evaluate(REEL_JS, [d, extra]); pg.wait_for_timeout(150)
            frames = []
            for idx in [0, 1, 2, 3, 6]:
                url = pg.evaluate(f"(()=>{{active={idx}; draw(false); return cv.toDataURL('image/png');}})()")
                im = Image.open(io.BytesIO(base64.b64decode(url.split(',')[1]))).convert("RGB")
                if idx in (1, 2, 3): im = post(im, (501, 1417), d["accent"])
                if idx == 6: im = post(im, (452, 1445), d["accent"])
                fp = f"/tmp/reel_{date}_{idx}.png"; im.save(fp); frames.append(fp)
            mp4 = os.path.join(OUT, f"{date}.mp4"); assemble(frames, mp4)
            print(date, spec[0], mp4)
        b.close()

if __name__ == "__main__": main()
