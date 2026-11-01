"""음악 라이브러리에서 곡 고르기 (대표 11/1 "유행 음원 결로 만들어 놓고 쓰자"). 만들기는 music_lib_build.py.
- content/music_lib.json 에서 status "ok" 곡만 쓴다(대표가 운영앱에서 뺀 곡은 "out").
- content/music_lib_used.json(render 가 쓸 때마다 적음)의 최근 6편에 쓴 곡은 피한다(같은 곡 연달아 금지).
- 12월(12/1~12/31)에는 크리스마스 팝을 넣고, 나머지 달에는 뺀다.
- 곡의 훅 시작(hook_at)부터 영상 길이만큼 자르고 끝 0.5초 페이드. 영상이 더 길면 곡을 이어 붙인다.
쓰기: from music_lib import render; info = render(total_sec, seed, out_wav)  → None 이면 라이브러리 없음(옛 작곡기로)."""
import os, json, random, subprocess, datetime
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, ".."))
LIST = os.path.join(ROOT, "content", "music_lib.json"); USED = os.path.join(ROOT, "content", "music_lib_used.json")

SITE_DATA = os.path.join(ROOT, "..", "zaoseon-site", "public", "admin", "data.json")   # 대표가 /naver/music.html 에서 뺀 곡(naver:mlout-<곡>)

def removed():
    try: return {k.split("mlout-", 1)[1] for k in json.load(open(SITE_DATA)).get("done", {}) if k.startswith("naver:mlout-")}
    except Exception: return set()

def tracks(today=None):
    if not os.path.exists(LIST): return []
    today = today or datetime.date.today()
    out = [t for t in json.load(open(LIST))["tracks"] if t.get("status") == "ok" and os.path.exists(os.path.join(ROOT, t["file"]))]
    gone = removed(); out = [t for t in out if t["id"] not in gone]
    if today.month != 12: out = [t for t in out if t["genre"] != "holiday"]
    return out

def recent(n=6):
    try: return json.load(open(USED))[-n:]
    except Exception: return []

def pick(seed, genre=None, today=None):
    pool = tracks(today)
    if genre: pool = [t for t in pool if t["genre"] == genre] or pool
    if not pool: return None
    avoid = set(recent()); fresh = [t for t in pool if t["id"] not in avoid] or pool
    return random.Random(seed).choice(fresh)

def render(total, seed, out_wav, genre=None, today=None):
    t = pick(seed, genre, today)
    if not t: return None
    src = os.path.join(ROOT, t["file"]); start = float(t.get("hook_at", 0))
    if start + total > t["dur"]: start = max(0.0, t["dur"] - total)
    loop = ["-stream_loop", "-1"] if total > t["dur"] else []
    fo = max(0.0, total - 0.5)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *loop, "-ss", f"{start:.2f}", "-i", src, "-t", f"{total:.3f}",
                    "-af", f"afade=t=in:d=0.05,afade=t=out:st={fo:.2f}:d=0.5", "-ar", "44100", "-ac", "2", out_wav], check=True)
    used = recent(50) + [t["id"]]; json.dump(used[-50:], open(USED, "w"))
    return dict(path=out_wav, lib=t["id"], style=t["name"], bpm=t["bpm"], key=t["key"], dur=total, prog=None)
