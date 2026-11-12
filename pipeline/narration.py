"""릴스·클립 목소리(TTS) 얹기 — 11/3 oaiwan 5단계 중 1단계, 대표가 speech.platform.bing.com 허용(11/3 11:42).
음악은 clip_v3_music.py가 이미 깐 영상에 목소리만 더한다(음악 도구를 따로 만들지 않음, K-070).
- 목소리: edge-tts ko-KR-SunHiNeural(무료, 키 없음 · 비용 0). 프록시를 거쳐야 해서 proxy=HTTPS_PROXY를 넘긴다.
- 줄마다 [시작초, 글, 칸 길이]. 목소리가 칸보다 길면 빠르기를 올려(최대 1.35배) 칸 안에 넣고, 그래도 넘치면 막는다.
- 목소리가 나오는 동안 음악을 낮춘다(사이드체인). 마지막에 -14 LUFS로 맞춘다.
사용: from narration import 얹기; 얹기("in.mp4", [(0.2,"첫 줄",2.6), ...], "out.mp4")"""
import os, asyncio, subprocess, json, tempfile

VOICE = os.environ.get("ZS_VOICE", "ko-KR-SunHiNeural")

def _dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p], capture_output=True, text=True).stdout.strip())

async def _say(text, out, rate, voice=None, pitch="+0Hz"):
    import edge_tts
    c = edge_tts.Communicate(text, voice or VOICE, rate=rate, pitch=pitch, proxy=os.environ.get("HTTPS_PROXY"))
    await c.save(out)

def 말(text, out, rate="+8%", voice=None, pitch="+0Hz"):
    os.environ.setdefault("SSL_CERT_FILE", "/root/.ccr/ca-bundle.crt")
    asyncio.run(_say(text, out, rate, voice, pitch))
    # 앞뒤 무음 자르기
    t = out + ".t.wav"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", out, "-af",
                    "silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse",
                    "-ar", "44100", "-ac", "2", t], check=True)
    return t

def 얹기(video, lines, out, rate="+8%", music_vol=0.30):
    tmp = tempfile.mkdtemp(prefix="nar_")
    parts, log = [], []
    for i, (s, text, slot) in enumerate(lines):
        w = 말(text, f"{tmp}/l{i}.mp3", rate)
        d = _dur(w); sp = 1.0
        if d > slot:
            sp = d / slot
            if sp > 1.35: raise SystemExit(f"목소리가 칸보다 너무 길어요({i}번 줄 {d:.1f}초 > {slot:.1f}초): 글을 줄이세요 — {text}")
            f2 = f"{tmp}/l{i}f.wav"
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", w, "-af", f"atempo={sp:.3f}", f2], check=True); w = f2; d = _dur(w)
        parts.append((s, w)); log.append({"줄": i, "시작": s, "길이": round(d, 2), "칸": slot, "빠르기": round(sp, 2), "글": text})
    ins = ["-i", video] + sum((["-i", w] for _, w in parts), [])
    fc = "".join(f"[{k+1}:a]adelay={int(s*1000)}|{int(s*1000)},apad[v{k}];" for k, (s, _) in enumerate(parts))
    fc += "".join(f"[v{k}]" for k in range(len(parts))) + f"amix=inputs={len(parts)}:normalize=0:duration=first,volume=1.6[vo];"
    fc += "[vo]asplit=2[vo1][vo2];"
    fc += f"[0:a]volume={music_vol}[mu];[mu][vo1]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=300[md];"
    fc += "[md][vo2]amix=inputs=2:normalize=0:duration=first,loudnorm=I=-14:TP=-1.5:LRA=11[a]"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error"] + ins + ["-filter_complex", fc, "-map", "0:v", "-map", "[a]",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-shortest", out], check=True)
    return log


async def _say_wb(text, out, rate):
    import edge_tts
    c = edge_tts.Communicate(text, VOICE, rate=rate, boundary="WordBoundary", proxy=os.environ.get("HTTPS_PROXY"))
    ws = []
    with open(out, "wb") as f:
        async for ch in c.stream():
            if ch["type"] == "audio": f.write(ch["data"])
            elif ch["type"] == "WordBoundary": ws.append((ch["text"], ch["offset"] / 1e7, ch["duration"] / 1e7))
    return ws

def 말시간(text, out, rate="+8%"):
    """목소리 + 낱말마다 시작 시각(초). 앞 무음을 자르지 않아 시각이 그대로 맞는다. 자막을 목소리에 맞출 때 쓴다(11/3)."""
    os.environ.setdefault("SSL_CERT_FILE", "/root/.ccr/ca-bundle.crt")
    ws = asyncio.run(_say_wb(text, out, rate))
    w = out + ".wav"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", out, "-ar", "44100", "-ac", "2", w], check=True)
    return w, ws, _dur(w)

def 섞기(video, parts, out, music_vol=0.30):
    """parts = [(시작초, wav)]. 음악 낮추기·-14 LUFS는 얹기와 같다."""
    ins = ["-i", video] + sum((["-i", w] for _, w in parts), [])
    fc = "".join(f"[{k+1}:a]adelay={int(s*1000)}|{int(s*1000)},apad[v{k}];" for k, (s, _) in enumerate(parts))
    fc += "".join(f"[v{k}]" for k in range(len(parts))) + f"amix=inputs={len(parts)}:normalize=0:duration=first,volume=1.6[vo];"
    fc += "[vo]asplit=2[vo1][vo2];"
    fc += f"[0:a]volume={music_vol}[mu];[mu][vo1]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=300[md];"
    fc += "[md][vo2]amix=inputs=2:normalize=0:duration=first,loudnorm=I=-14:TP=-1.5:LRA=11[a]"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error"] + ins + ["-filter_complex", fc, "-map", "0:v", "-map", "[a]",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-shortest", out], check=True)

# 11/12 대표 "TTS는 자연스럽게": 말하는 사람마다 결을 나눈다. edge-tts 한국어 여성 목소리는 SunHi 하나뿐이라 높이·빠르기로 나눈다.
#   cust(손님 속마음): 조금 높고 빠르게 — 한탄·혼잣말 결 / jw(정월): 낮고 차분하게 — 답해 주는 결 / nar(안내): 기본
WHO = {"cust": dict(voice="ko-KR-SunHiNeural", rate="+12%", pitch="+12Hz"),
       "jw":   dict(voice="ko-KR-SunHiNeural", rate="+0%",  pitch="-6Hz"),
       "nar":  dict(voice="ko-KR-SunHiNeural", rate="+6%",  pitch="+0Hz"),
       "man":  dict(voice="ko-KR-InJoonNeural", rate="+6%", pitch="+0Hz")}


def 목소리들(cues, tmp):
    """cues = [{t, text, who, slot}] (HTML window.VO). 글자 그대로 읽히면 어색한 것(ㅠㅠ·ㅋㅋ·;;)은 HTML 쪽 text 에서 뺀다.
    칸보다 길면 1.25배까지만 빠르게(그 이상은 부자연스러워 막는다). 돌려줌: [(시작초, wav)], 기록"""
    parts, log = [], []
    for i, c in enumerate(cues):
        w = WHO.get(c.get("who", "nar"), WHO["nar"])
        f = 말(c["text"], f"{tmp}/vo{i}.mp3", w["rate"], w["voice"], w["pitch"]); d = _dur(f); slot = float(c.get("slot", 9)); sp = 1.0
        if d > slot:
            sp = d / slot
            if sp > 1.25: raise SystemExit(f"[막음] 목소리가 칸보다 길어요({i}번 {d:.1f}초 > {slot:.1f}초) — 글을 줄이세요: {c['text']}")
            f2 = f"{tmp}/vo{i}f.wav"; subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", f, "-af", f"atempo={sp:.3f}", f2], check=True); f = f2; d = _dur(f)
        parts.append((float(c["t"]), f)); log.append({"줄": i, "누구": c.get("who", "nar"), "시작": c["t"], "길이": round(d, 2), "칸": slot, "빠르기": round(sp, 2), "글": c["text"]})
    return parts, log


if __name__ == "__main__":
    import sys
    spec = json.load(open(sys.argv[1], encoding="utf-8"))
    print(json.dumps(얹기(spec["video"], spec["lines"], spec["out"]), ensure_ascii=False, indent=1))
