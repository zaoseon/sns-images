"""박자 격자 재기 (K-294 묶음 A, 대표 11/24 "A부터 진행").

외부 자료 분석(커리어해커 알렉스 5종): 잘 만든 릴스는 곡의 BPM 숫자만 쓰지 않고 **첫 박이 언제인지(오프셋)** 까지 재서
컷·타격·드롭을 박·반 박에 맞춘다. 우리는 파일 이름의 BPM 만 쓰고 0초를 첫 박으로 가정했다 → 박이 어긋날 수 있었다.

쓰는 법:
  python tools/beat_grid.py <음악파일>                 # BPM·첫 박·박 목록(JSON) 출력
  python tools/beat_grid.py <음악파일> --초=15.6       # 앞 15.6초만 재기(릴스 길이)
  python tools/beat_grid.py check <음악파일> <ad.html> # 페이지 window.SFX 의 타격음이 반 박 격자에서 얼마나 벗어났나(확인 등급)
페이지에는 html_motion 이 window.ZS_BEAT={bpm,offset} 으로 넣는다(--음악=<파일>). 페이지는 F.BEAT.T(k) 로 k번째 박 시각을 쓴다.

방법: ffmpeg 로 22.05kHz 모노 → 스펙트럼 변화량(onset) 곡선 → 자기상관으로 BPM(이름에 bpm 이 있으면 그 근처 ±4%) →
그 BPM 격자를 0~1박 밀어 보며 onset 합이 가장 큰 자리 = 첫 박(오프셋).
"""
import json, os, re, subprocess, sys

import numpy as np

SR, HOP, N = 22050, 256, 1024


def _pcm(path, secs=None):
    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-i", path]
    if secs: cmd += ["-t", str(secs)]
    cmd += ["-ac", "1", "-ar", str(SR), "-f", "f32le", "-"]
    return np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, dtype=np.float32)


def _onset(x):
    n = 1 + (len(x) - N) // HOP
    fr = np.lib.stride_tricks.as_strided(x, (n, N), (x.strides[0] * HOP, x.strides[0])) * np.hanning(N)
    m = np.log1p(100 * np.abs(np.fft.rfft(fr, axis=1)))
    f = np.maximum(0, np.diff(m, axis=0)).sum(1)
    f = f - np.convolve(f, np.ones(16) / 16, "same")          # 느린 변화 빼기
    return np.maximum(f, 0)


def measure(path, secs=None):
    x = _pcm(path, secs)
    if len(x) < SR * 2: raise SystemExit(f"[막음] 음악이 너무 짧아요({len(x)/SR:.1f}초)")
    env = _onset(x); fps = SR / HOP
    hint = re.search(r"(\d{2,3})bpm", os.path.basename(path), re.I)
    lo, hi = (int(hint.group(1)) * .96, int(hint.group(1)) * 1.04) if hint else (70, 180)
    ac = np.correlate(env, env, "full")[len(env) - 1:]
    best, bpm = -1, None
    for b in np.arange(lo, hi, 0.05):
        lag = 60 * fps / b; i = int(lag); fr_ = lag - i
        v = ac[i] * (1 - fr_) + ac[i + 1] * fr_ + .5 * np.interp(2 * lag, np.arange(len(ac)), ac)
        if v > best: best, bpm = v, b
    per = 60 * fps / bpm
    t = np.arange(len(env)); sc = []
    for ph in np.arange(0, per, .25):
        idx = np.arange(ph, len(env), per)
        sc.append((np.interp(idx, t, env).sum(), ph))
    s_, ph = max(sc)
    offset = (ph + 1) * HOP / SR          # diff 로 한 칸 밀림 보정
    B = 60 / bpm
    beats = [round(offset + k * B, 4) for k in range(int((len(x) / SR - offset) / B) + 1)]
    strength = float(s_ / (np.mean([s for s, _ in sc]) + 1e-9))
    return {"file": os.path.basename(path), "bpm": round(float(bpm), 2), "offset": round(float(offset), 4),
            "beat_sec": round(B, 4), "named_bpm": int(hint.group(1)) if hint else None, "confidence": round(strength, 2), "beats": beats}


def check(path, html, secs=None):
    """페이지 window.SFX 중 타격음(thud·whoosh·swoosh·pop)이 반 박 격자에서 몇 ms 벗어났나. 확인 등급(막지 않음)."""
    from playwright.sync_api import sync_playwright
    g = measure(path, secs)
    with sync_playwright() as pw:
        b = pw.chromium.launch(); pg = b.new_page(); pg.add_init_script("window.ZS_BEAT=" + json.dumps({"bpm": g["bpm"], "offset": g["offset"]})); pg.goto("file:///" + os.path.abspath(html).replace(os.sep, "/"))
        cues = pg.evaluate("() => window.SFX || []"); b.close()
    q = g["beat_sec"] / 2; off = g["offset"]; rows = []
    for c in cues:
        if c.get("k") not in ("thud", "whoosh", "swoosh", "pop"): continue
        t = float(c["t"]); d = (t - off) - round((t - off) / q) * q
        rows.append((t, c["k"], round(d * 1000)))
    bad = [r for r in rows if abs(r[2]) > 35]
    return g, rows, bad


def main():
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    secs = next((float(x.split("=")[1]) for x in sys.argv if x.startswith("--초=")), None)
    if not a: print(__doc__); return 1
    if a[0] == "check":
        g, rows, bad = check(a[1], a[2], secs)
        print(f"박자 {g['bpm']}bpm · 첫 박 {g['offset']}초 (이름 {g['named_bpm']}bpm · 확신 {g['confidence']})")
        for t, k, d in rows: print(f"  {t:7.3f}초 {k:7s} 반 박에서 {d:+5d}ms" + ("  ← 35ms 넘음" if abs(d) > 35 else ""))
        print(f"[확인] 타격음 {len(rows)}개 중 {len(bad)}개가 반 박 격자에서 35ms 넘게 벗어남" if bad else f"[통과] 타격음 {len(rows)}개 모두 반 박 격자 ±35ms 안")
        return 0
    g = measure(a[0], secs); out = dict(g); out["beats"] = g["beats"][:16] + (["…"] if len(g["beats"]) > 16 else [])
    print(json.dumps(out, ensure_ascii=False)); return 0


if __name__ == "__main__":
    sys.exit(main())
