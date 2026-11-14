"""완성 파일 감사 — 릴스·클립·쇼츠(영상) · 캐러셀(카드 그림) · 네이버 대표 이미지(섬네일) · 네이버 본문 이미지(모바일).
(11/14 대표 "릴스·캐러셀·쇼츠·네이버 대표이미지(섬네일 고려)·원고 내부 이미지 모바일 최적화도 감사도구가 필요하다", K-208)

만드는 쪽 관문(card_gate·html_motion)이 '그리기 전·그리는 중'을 막는다면, 이 도구는 **끝난 파일**을 다시 잰다.
어느 프로젝트가 만들었든(자오선·인스타툰·BB) 파일만 있으면 같은 값(channel_specs)으로 잰다 — 규격·균형 값은 specs/channel_specs.py 한 곳.

사용:
  python3 tools/content_audit.py video  <채널> 파일.mp4 [...]          # 채널: reel · naver_clip · youtube_shorts
  python3 tools/content_audit.py carousel 폴더또는카드.jpg [...]        # 인스타 캐러셀 1080x1440
  python3 tools/content_audit.py thumb 파일.jpg [...]                   # 네이버 대표 이미지 1200x720
  python3 tools/content_audit.py body 파일.jpg [...]                    # 네이버 본문 이미지(1280 폭, 모바일)
  --경고도   경고(참고)까지 실패로 센다.   종료 코드: 막음 있으면 1.
채널 규격 위치: ZS_SPECS=<channel_specs.py 가 있는 폴더> (없으면 이 저장소 specs/ → sns-images pipeline/)."""
import os, sys, io, json, subprocess, glob
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
for p in (os.environ.get("ZS_SPECS"), os.path.join(HERE, "..", "specs"), os.path.join(HERE, "..", "pipeline"), HERE):
    if p and os.path.exists(os.path.join(p, "channel_specs.py")): sys.path.insert(0, p); break
import channel_specs as CS
B = CS.BALANCE

def _z(ch): return {r[0]: r[1:5] for r in CS.CH[ch]["zones"]}
def _bbox(a, ay0, ay1, bgthr=48):
    """a: HxWx3. ay0~ay1 사이에서 배경(양옆 24px 중앙값)과 다른 픽셀의 상자와 블록들."""
    A = a[ay0:ay1]; edge = np.concatenate([A[:, :24].reshape(-1, 3), A[:, -24:].reshape(-1, 3)]); bg = np.median(edge, 0)
    m = np.abs(A - bg).max(2) > bgthr; rows = np.where(m.sum(1) > 14)[0]
    if not len(rows): return None
    cols = np.where(m[rows.min():rows.max() + 1].sum(0) > 14)[0]
    if not len(cols): return None
    ys = rows + ay0; blocks = []; s = ys[0]; p = ys[0]
    for y in ys[1:]:
        if y - p - 1 >= B["rhythm_band"]: blocks.append((int(s), int(p))); s = y
        p = y
    blocks.append((int(s), int(p)))
    return dict(y0=int(rows.min() + ay0), y1=int(rows.max() + ay0), x0=int(cols.min()), x1=int(cols.max()), fill=float(m.mean()), blocks=blocks)

def _run(문제, key, t, msg, hold, step):
    pass

# ───────────── 영상 ─────────────
VIDEO_LEN = {"reel": (7, 90), "naver_clip": (7, 60), "youtube_shorts": (7, 60)}   # 초. 너무 짧거나 긴 영상 거름(정확한 길이는 규격 문서가 아니라 채널 한계)
def video(path, ch="reel", step=0.25):
    막음, 경고 = [], []
    pr = json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,width,height,duration", "-of", "json", path], capture_output=True, text=True).stdout)["streams"]
    v = [s for s in pr if s["codec_type"] == "video"][0]; C = CS.CH[ch]
    if (v["width"], v["height"]) != (C["w"], C["h"]): 막음.append(f"크기 {v['width']}x{v['height']} — {C['name']} 은 {C['w']}x{C['h']}")
    if not any(s["codec_type"] == "audio" for s in pr): 막음.append("소리 없음(릴스·클립·광고는 소리 없이 내보내지 않는다, K-070)")
    sec = float(v.get("duration") or 0); lo, hi = VIDEO_LEN.get(ch, (3, 120))
    if not lo <= sec <= hi: 경고.append(f"길이 {sec:.1f}초 (이 채널 {lo}~{hi}초)")
    z = _z(ch); top = z["상단 고정"][3]; bot = z["하단 고정"][1]; sx0, sx1 = C["safe"][0], C["safe"][2]; acx = (sx0 + sx1) / 2; acy = (top + bot) / 2
    n = int(sec / step); keys = {}
    def hit(k, t, m): keys.setdefault(k, []).append((t, m))
    for i in range(n + 1):
        t = min(i * step, max(sec - 0.05, 0))
        out = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", path, "-frames:v", "1", "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True).stdout
        if not out: continue
        a = np.asarray(Image.open(io.BytesIO(out)).convert("RGB")).astype(int)
        b = _bbox(a, top + 10, bot - 10)
        if i == 0:   # 표지(0번 프레임)
            ok = b and b["fill"] >= B["cover_fill"] and (b["y1"] - b["y0"]) / (bot - top - 20) >= B["cover_h"]
            if not ok: (막음 if ch == "naver_clip" else 경고).append(f"표지(0초 프레임)가 비었어요 — 채움 {(b['fill'] if b else 0) * 100:.1f}%(5%↑) 높이 {((b['y1'] - b['y0']) / (bot - top - 20) if b else 0) * 100:.0f}%(22%↑). 목록 표지는 첫 프레임이다(K-205)")
        if not b: continue
        g_top, g_bot = b["blocks"][0][0] - top, bot - b["blocks"][-1][1]; 안 = [b["blocks"][j + 1][0] - b["blocks"][j][1] for j in range(len(b["blocks"]) - 1)]
        if b["y0"] < top + B["gap_top"] - 4: hit("위 간격", t, f"내용 위 끝이 상단 고정 줄 아래 {b['y0'] - top}px (60↑)")
        if g_bot < B["gap_bottom"] - 4: hit("아래 간격", t, f"내용 아래 끝이 하단 고정 줄 위 {g_bot}px (60↑)")
        if abs(g_top - g_bot) > B["edge_tol"]: hit("상하 균형", t, f"위 {g_top} · 아래 {g_bot} (차이 80↓)")
        전부 = [g_top, g_bot] + 안
        if 안 and max(전부) > B["rhythm_ratio"] * max(min(전부), 1): hit("균형 리듬", t, f"간격 {전부} — 가장 넓은 것이 가장 좁은 것의 {max(전부) / max(min(전부), 1):.1f}배(2.5↓)")
        if abs((b["x0"] + b["x1"]) / 2 - acx) > B["center_tol_x"]: hit("가로 가운데", t, f"내용 가운데 x {(b['x0'] + b['x1']) / 2:.0f} (칸 {acx:.0f}±50)")
        if b["x0"] < sx0 - 4 or b["x1"] > sx1 + 4: hit("안전 영역 밖(경고: 배경·전환 효과일 수 있음)", t, f"내용 x {b['x0']}~{b['x1']} (안전 {sx0}~{sx1})")
    for k, v_ in keys.items():
        ts = [x[0] for x in v_]; run = best = 1
        for j in range(1, len(ts)):
            run = run + 1 if ts[j] - ts[j - 1] <= step + 1e-6 else 1; best = max(best, run)
        if best * step > B["hold"]: (경고 if k.startswith("안전 영역 밖") else 막음).append(f"[{k}] {v_[0][0]:.1f}초부터 {best * step:.1f}초 이상 — {v_[0][1]}")
    return 막음, 경고

# ───────────── 이미지 공통 ─────────────
def _faint(path):
    try:
        import faint_gate as FG
        return [f"y {y} 근처 글자가 배경에 묻힘(대비 {r}:1)" for y, n, r in (FG.hits(path) or [])[:3]]
    except Exception: return []

def carousel(path):
    막음, 경고 = [], []; C = CS.CH["insta_carousel"]; im = Image.open(path).convert("RGB"); W, H = im.size
    if (W, H) != (C["w"], C["h"]): 막음.append(f"크기 {W}x{H} — {C['w']}x{C['h']} 이어야 함")
    a = np.asarray(im).astype(int); z = _z("insta_carousel"); sx0, sy0, sx1, sy1 = C["safe"]
    위 = min(v[1] for k, v in z.items() if "고정" not in k); 아래 = max(v[3] for k, v in z.items() if "고정" not in k)
    b = _bbox(a, 위, 아래)
    if b:
        l, r = b["x0"] - sx0, sx1 - b["x1"]
        if abs(l - r) > (sx1 - sx0) * 0.07: 경고.append(f"좌우 여백 {l} 대 {r} — 치우침")
        g_top, g_bot = b["y0"] - 위, 아래 - b["y1"]
        if abs(g_top - g_bot) > B["edge_tol"]: 막음.append(f"위아래 여백 {g_top} 대 {g_bot} — 한쪽으로 쏠림(차이 80↓)")
        if b["y1"] > 아래 + 8: 막음.append(f"내용 맨 아래 y{b['y1']} 가 구역 끝 {아래} 을 넘음")
    else: 막음.append("내용이 비었음")
    막음 += _faint(path); return 막음, 경고

def thumb(path):
    막음, 경고 = [], []; C = CS.CH["naver_blog_thumb"]; im = Image.open(path).convert("RGB"); W, H = im.size
    if (W, H) != (C["w"], C["h"]): 막음.append(f"크기 {W}x{H} — {C['w']}x{C['h']} 이어야 함")
    a = np.asarray(im.convert("L"), float)
    if W == 1200 and max(a[:, :236].std(), a[:, 964:].std()) > 3: 막음.append("양옆 240px 띠에 글자·그림이 있음 — 목록이 정사각으로 자르면 잘림")
    # 목록에서 실제로 보이는 크기(가로 약 170px 정사각 중심)로 줄여 글자가 남는지: 가운데 720 을 160px 로 줄여 대비·채움을 본다
    c = im.crop((240, 0, 960, 720)).resize((160, 160)); g = np.asarray(c.convert("L"), float)
    if g.std() < 25: 막음.append(f"작게 줄이면(목록 크기) 대비가 약해 안 보임(밝기 편차 {g.std():.0f}, 25↑)")
    big = np.asarray(im.crop((240, 0, 960, 720)).convert("RGB")).astype(int); bb = _bbox(big, 40, 680)
    if bb and (bb["y1"] - bb["y0"]) < 0.35 * 640: 경고.append("내용 높이가 가운데 칸의 35% 미만 — 작게 보일 수 있음")
    if os.path.getsize(path) > 1_500_000: 경고.append(f"파일 {os.path.getsize(path) // 1000}KB — 목록 로딩 무거움(1.5MB↓)")
    막음 += _faint(path); return 막음, 경고

def body(path):
    막음, 경고 = [], []; im = Image.open(path).convert("RGB"); W, H = im.size
    if W not in (1280, 640, 480): 경고.append(f"폭 {W}px — 본문 이미지는 1280(원본)·640·480")
    if W >= 1000 and (H < 300 or H > 2400): 경고.append(f"높이 {H}px — 모바일 한 화면에 보기 어렵거나 너무 길어요(300~2400)")
    # 모바일 가독성: 폰 화면 폭 360 에 맞춰 줄였을 때 글자 높이 = 원본 × 360/W. 글자 덩어리(가로로 이어진 줄)의 높이 하위 10% 를 잰다
    s = 360 / W; a = np.asarray(im.convert("L"), float); small = np.asarray(im.resize((360, max(1, int(H * s))), Image.LANCZOS).convert("L"), float)
    edge = np.abs(np.diff(small, axis=1)) > 40; rows = edge.sum(1) > 4; runs = []; c = 0
    for r in rows:
        if r: c += 1
        elif c: runs.append(c); c = 0
    if c: runs.append(c)
    글줄 = [x for x in runs if 3 <= x <= 40]
    if 글줄 and np.percentile(글줄, 10) < 7: 경고.append(f"폰 폭(360px)에서 가장 작은 글줄 높이 약 {np.percentile(글줄, 10):.0f}px — 7px 미만은 읽기 힘듦(원본 글자 {int(7 / s)}px↑ 권장)")
    if os.path.getsize(path) > 2_500_000: 경고.append(f"파일 {os.path.getsize(path) // 1000}KB — 모바일 로딩 무거움")
    막음 += _faint(path); return 막음, 경고

def main():
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    if len(a) < 2: print(__doc__); return 2
    kind = a[0]; ch = "reel"
    if kind == "video": ch = a[1]; files = a[2:]
    else: files = a[1:]
    paths = []
    for f in files: paths += sorted(glob.glob(os.path.join(f, "*.jp*g")) + glob.glob(os.path.join(f, "*.png"))) if os.path.isdir(f) else [f]
    fn = {"video": lambda p: video(p, ch), "carousel": carousel, "thumb": thumb, "body": body}[kind]
    경고도 = "--경고도" in sys.argv; 막힘 = 0
    if kind == "carousel" and len(paths) < 7 and len(files) == 1 and os.path.isdir(files[0]): print(f"[막음] {files[0]}: 카드 {len(paths)}장 — 캐러셀은 최소 7장(R58)"); 막힘 += 1
    for p in paths:
        m, w = fn(p); name = os.path.relpath(p)
        for x in m: print(f"[막음] {name}: {x}")
        for x in w: print(f"[경고] {name}: {x}")
        막힘 += (1 if m else 0) + (1 if (w and 경고도) else 0)
    print(f"감사 {len(paths)}개 · 막힘 {막힘}"); return 1 if 막힘 else 0

if __name__ == "__main__": sys.exit(main())
