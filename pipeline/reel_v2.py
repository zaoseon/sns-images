"""릴스 v2 (10/1 밤, 대표가 올린 7가지 기준 + 음악 사용 결정): 하드 컷, 컷을 박자(96BPM)에 맞춤, 후반에 조언(반전) 장면, 마지막 CTA에 다음 편 떡밥, 낮은 볼륨의 직접 작곡 배경음악(저작권 문제 없음).
사용: python3 pipeline/reel_v2.py 2026-10-02 [...]  -> 2026-w40car3-reel/v2/<날짜>.mp4"""
import os, sys, io, base64, subprocess, wave
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import carousel_editor as CE
import reel_music as RM
from playwright.sync_api import sync_playwright
from PIL import Image
BPM = 96; BEAT = 60.0 / BPM
# (슬라이드 번호, 박자 수): 훅 4 / 성격 3 / 연애 3 / 돈 3 / 조언(반전) 4 / CTA 4  -> 21박 = 13.1초
SEQ_DAY = [(0, 4), (1, 3), (2, 3), (3, 3), (5, 4), (6, 4)]
# 구조 3종(박 수): S1 기본 / S2 차트형(오행 차트를 둘째 장에) / S3 짧은형. 슬라이드 번호 0 표지 1 성격 2 연애 3 돈 4 차트 5 조언 6 CTA
STRUCTS = {"S1": [(0, 4), (1, 3), (2, 3), (3, 3), (5, 4), (6, 4)],
           "S2": [(0, 3), (4, 3), (1, 3), (2, 3), (5, 4), (6, 3)],
           "S3": [(0, 3), (1, 2), (2, 2), (3, 2), (5, 3), (6, 3)]}
# 장면 길이(초): 템포가 빨라져도 글자를 읽을 시간(본문 2초 안팎)을 지키고, 컷은 가장 가까운 박에 맞춘다
STRUCT_SECS = {"S1": [(0, 2.5), (1, 2.0), (2, 2.0), (3, 2.0), (5, 2.5), (6, 2.5)],
               "S2": [(0, 2.2), (4, 2.2), (1, 2.0), (2, 2.0), (5, 2.4), (6, 2.4)],
               "S3": [(0, 2.0), (1, 1.8), (2, 1.8), (3, 1.8), (5, 2.2), (6, 2.2)]}
SEQ_TRI = [(0, 4), (1, 3), (2, 3), (3, 3), (5, 4), (6, 4)]
def music(path, beats, sr=44100):
    n = int(sr * BEAT * beats) + sr // 2; t = np.arange(n) / sr; out = np.zeros(n)
    chords = [([220, 261.63, 329.63], 110), ([174.61, 220, 261.63], 87.31), ([261.63, 329.63, 392], 130.81), ([196, 246.94, 293.66], 98)]
    bar = BEAT * 4
    for k in range(int(beats / 4) + 1):
        c, root = chords[k % 4]; s0 = int(k * bar * sr); s1 = min(n, int((k + 1) * bar * sr) + int(0.3 * sr)); tt = t[s0:s1] - t[s0]
        env = np.minimum(1, tt / 0.35) * np.minimum(1, (t[s1 - 1] - t[s0] - tt) / 0.3 + 0.0001)
        pad = sum(np.sin(2 * np.pi * f * tt) + 0.5 * np.sin(2 * np.pi * f * 2.003 * tt) for f in c) * 0.045
        out[s0:s1] += pad * env + np.sin(2 * np.pi * root * tt) * 0.12 * env
        for j in range(8):                                  # 8분음표 플럭
            ts = k * bar + j * BEAT / 2; si = int(ts * sr)
            if si >= n: break
            note = c[(j * 2 + (j // 4)) % 3] * (2 if j % 2 else 1); seg = t[si:si + int(0.45 * sr)] - t[si]
            out[si:si + len(seg)] += (np.sin(2 * np.pi * note * seg) + 0.3 * np.sin(2 * np.pi * note * 2 * seg)) * np.exp(-7 * seg) * 0.07
    rng = np.random.default_rng(3)
    for b in range(int(beats)):                             # 킥(매 박) + 하이햇(엇박)
        si = int(b * BEAT * sr); seg = t[:int(0.2 * sr)]
        if si + len(seg) <= n: out[si:si + len(seg)] += np.sin(2 * np.pi * (45 + 80 * np.exp(-30 * seg)) * seg) * np.exp(-14 * seg) * 0.30
        hs = int((b + 0.5) * BEAT * sr); hseg = int(0.05 * sr)
        if hs + hseg <= n: out[hs:hs + hseg] += rng.normal(0, 1, hseg) * np.exp(-60 * np.arange(hseg) / sr) * 0.035
    k = 8; out = np.convolve(out, np.ones(k) / k, mode="same")  # 로파이 느낌의 부드러운 고음 깎기
    out *= np.minimum(1, (t[-1] - t) / 0.6); out = out / max(1e-6, np.abs(out).max()) * 0.5   # 맨 끝 페이드아웃, 과하지 않은 크기
    with wave.open(path, "wb") as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes((out * 32767).astype(np.int16).tobytes())

BYEONG = dict(dayChar="병", hanja="丙", accent="#e65c3c", face="v1_lowbun", kicker="오늘의 성격 카드", coverTitle="좋으면 티 나고\n식어도 티 나는 사람", coverSub="태어난 날 첫 글자가 병(丙)이라면",
    personality=["감정 표현이\n가장 빠른 타입", "태양처럼 밝은 기운이라,\n좋고 싫음이 얼굴에 바로 드러나요.\n숨기는 걸 오래 못 하는 편이에요."],
    love=["좋을 땐\n화끈하게 다가가요", "표현이 직접적이라\n상대가 마음을 바로 알아차려요.\n밀당엔 약한 편, 그게 매력이기도 해요."],
    money=["기분 좋은 날\n씀씀이가 커져요", "에너지가 넘치는 날 지갑도 쉽게 열려요.\n큰 소비 전엔 하루만 더 생각해보세요."],
    advice=["표현은 무기,\n속도만 조절하면 돼요", "다 보여주는 게 나쁜 게 아니에요.\n타이밍만 살짝 늦추면\n관계가 더 편해져요."], chartNote="", values=[.35, 1.0, .45, .3, .4], highlight=1,
    ctaQ="주변에 *병화* 같은\n사람이 있나요?", nextTitle="정(丁)일생 편")
def get_defs():
    d = CE.reel_defs(); d["byeong"] = (BYEONG, dict(nextBadge="내일 낮 12시", nextTitle="정(丁)일생 편")); return d
def main():
    render(sys.argv[1:], get_defs(), os.path.join(CE.ROOT, "2026-w40car3-reel", "v2"))

def render(dates, defs, outdir):
    """defs: {이름: (def, override)}  ->  outdir/<이름>.mp4"""
    os.makedirs(outdir, exist_ok=True)
    CE.build_html()
    if not os.path.exists(CE.PLATE): CE.make_plate()
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1300, "height": 900}); pg.goto("file:///tmp/editor_noto.html"); pg.wait_for_timeout(1500)
        pg.evaluate("Promise.all([400,500,600,700,900].map(w=>document.fonts.load(w+' 40px \"Noto Sans CJK KR\"','가한丁')))")
        from PIL import Image as _I
        add = {"chart_plate": "data:image/png;base64," + base64.b64encode(open(CE.PLATE, "rb").read()).decode()}
        for d in dates:
            k, u = CE.face_dataurl(defs[d][0]["face"])
            if k not in ("v1_lowbun", "v2_straight", "v3_ponytail", "v4_glasses", "v5_halfup_v2"): add[k] = u
        for k, u in add.items(): pg.evaluate("async ([k,u])=>{FACES[k]=u; const im=new Image(); im.src=u; await im.decode(); imgCache[k]=im;}", [k, u])
        for date in dates:
            d, ov = defs[date]; ov = dict(ov); tri = bool(ov.get("badges"))
            cfg = ov.pop("_cfg", {}); sample = cfg.get("frames")        # 대표 샘플 PNG 7장(0~6번 슬라이드) 그대로 쓰는 경우
            style = cfg.get("style", "피아노 로파이"); upbeat = style in RM.UP
            if upbeat:     # 경쾌한 스타일: 장면 길이를 초로 정하고 박 수로 바꾼다
                bpm = RM.pick_bpm(style, cfg.get("seed", 1)); beat = 60.0 / bpm
                secs = STRUCT_SECS[cfg.get("struct", "S1")] if not tri else [(0, 2.5), (1, 2.0), (2, 2.0), (3, 2.0), (5, 2.5), (6, 2.5)]
                seq = [(si, max(3, round(sec / beat))) for si, sec in secs]
            else: seq = STRUCTS[cfg["struct"]] if (cfg.get("struct") and not tri) else (SEQ_TRI if tri else SEQ_DAY)
            total_beats = sum(bt for _, bt in seq)
            wav = f"/tmp/v2_{date}.wav"
            if upbeat:
                cuts = [sum(bt for _, bt in seq[:j]) for j in range(len(seq))]
                m = RM.compose_up(style, total_beats, cfg.get("seed", 1), wav, key=cfg.get("key", "C"), bpm=bpm, cuts=cuts)
            else: m = RM.compose(style, total_beats, cfg.get("seed", 1), wav, key=cfg.get("key", "C"), tail=0.3)
            beat = 60.0 / m["bpm"]
            sample = sample or {}
            if any(si not in sample for si, _ in seq):
                pg.evaluate(CE.LAYOUT_JS, [d, None]); pg.evaluate(CE.OVERRIDE_JS, ov); pg.wait_for_timeout(120)
            frames = []
            for si, beats in seq:
                if si in sample: im = Image.open(sample[si]).convert("RGB")
                else:
                    url = pg.evaluate(f"(()=>{{active={si}; draw(false); return cv.toDataURL('image/png');}})()")
                    im = Image.open(io.BytesIO(base64.b64decode(url.split(",")[1]))).convert("RGB")
                c = Image.new("RGB", (CE.REEL_W, CE.REEL_H), im.getpixel((5, 5))); c.paste(im, (0, CE.REEL_TOP)); fp = f"/tmp/v2_{date}_{si}.png"; c.save(fp); frames.append((fp, beats * beat))
            cmd = ["ffmpeg", "-y", "-loglevel", "error"]
            for fp, dur in frames: cmd += ["-loop", "1", "-t", f"{dur:.4f}", "-i", fp]
            cmd += ["-i", wav]; n = len(frames)
            fl = "".join(f"[{i}:v]" for i in range(n)) + f"concat=n={n}:v=1:a=0,format=yuv420p,fps=30[v]"
            cmd += ["-filter_complex", fl, "-map", "[v]", "-map", f"{n}:a", "-c:v", "libx264", "-crf", "20", "-c:a", "aac", "-b:a", "128k", "-shortest", "-movflags", "+faststart", os.path.join(outdir, f"{date}.mp4")]
            subprocess.run(cmd, check=True); print(date, f"{total_beats * beat:.1f}s", len(seq), "장면", m["bpm"], "BPM", cfg.get("style", ""))
        b.close()
if __name__ == "__main__": main()
