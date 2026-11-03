# 실험 판(K-167) 목소리 릴스 틀 — CT 11/3. 대표 12:01 "검은 상자 안에서 통으로 나와 심심하다. 다양한 방법으로 나오고 강조도 되게 모션으로".
# 순서: ① 장면마다 목소리를 먼저 만들고 낱말 시각을 받는다(narration.말시간) ② 장면 길이 = 목소리 + 여유
#      ③ 자막을 낱말 시각에 맞춰 한 낱말씩 붙인다(motion_kit '말자막': 줄마다 등장 방식이 다르고 *강조* 낱말은 크게 터짐)
#      ④ 장면 이어 붙이기 → 음악(clip_v3_music) → 목소리 섞기(음악 낮춤, -14 LUFS).
# 장면 사양: dict(이름, 그림, 제목=[줄..], 강조=[번호], 강조2=[번호], 말제목="소리로 읽는 제목", 자막=["*강조* 낱말 포함 줄", ...], 표지=False)
import os, re, sys, json, shutil, subprocess
sys.path.insert(0, "/home/claude/sns-images/pipeline")
import motion_kit as MK, html_motion as HM, narration as NR
from motion_kit import 쓰기
SNS = "/home/claude/sns-images"
WORK = "/tmp/claude-0/mk"
LEAD = 0.2   # 장면 시작 뒤 목소리가 나오는 때

def _n(x): return re.sub(r"[^0-9A-Za-z가-힣]", "", x)

def _맞추기(토큰, 경계):
    """자막 낱말(토큰)마다 목소리 시각을 붙인다. 글자를 이어 붙인 자리로 맞춰서 낱말 나눔이 달라도 맞는다."""
    bpos, p = [], 0
    for w, t, _ in 경계: bpos.append((p, t)); p += len(_n(w))
    out, p = [], 0
    for tok in 토큰:
        t = next((tt for pp, tt in reversed(bpos) if pp <= p), bpos[0][1] if bpos else 0)
        out.append(t); p += len(_n(tok))
    return out

def 장면(c, P, i, 끝):
    os.makedirs(f"{WORK}/voice", exist_ok=True)
    자막 = c.get("자막", [])
    줄들 = [x.split(" ") for x in 자막]
    # 11/3 대표 요청(mw0j07m8): 줄 사이에 쉼표, 끝에 마침표를 넣어 목소리가 줄마다 숨을 쉬게(낱말은 그대로라 시각 맞추기에 영향 없음)
    줄말 = [x.replace("*", "").strip() for x in 자막]
    줄말 = [(x if x[-1:] in ",.?!" else x + ",") for x in 줄말[:-1]] + [(줄말[-1] if 줄말[-1][-1:] in ".?!" else 줄말[-1].rstrip(",") + ".")] if 줄말 else []
    말 = (c["말제목"] + " " + " ".join(줄말)).strip()
    wav, wb, vd = NR.말시간(말, f"{WORK}/voice/{c['이름']}.mp3")
    초 = round(max(c.get("최소", 3.0), LEAD + vd + c.get("여유", 0.8)), 2)
    제목낱 = len(c["말제목"].split(" "))
    모든 = c["말제목"].split(" ") + [w for ln in 줄들 for w in ln]
    시각 = _맞추기([w.replace("*", "") for w in 모든], wb)[제목낱:]
    rows, k, emph = [], 0, False
    for ln in 줄들:
        row = []
        for w in ln:
            e0 = emph or w.startswith("*")
            if w.count("*") % 2: emph = not emph
            row.append([w.replace("*", ""), 시각[k] + LEAD, bool(e0 or "*" in w)]); k += 1
        rows.append(row)
    s0 = -0.2 if c.get("표지") else 0
    부분 = [쓰기("그림넘김", 왜="멈춤", s=s0, d=초 + .4, 단="배경", 그림=c["그림"], **({"자리": c["자리"]} if c.get("자리") else {}))]
    if c.get("표지"):
        부분.append(쓰기("센표지", 왜="멈춤", s=-0.5, d=0.6, 단="마무리 카드", 줄=c["제목"], 강조=c.get("강조", []), 크기=c.get("크기", 140)))
    else:
        부분.append(쓰기("말자막", 왜="정보", s=0, d=0.5, 단="마무리 카드", 줄=c["제목"], 강조=c.get("강조", []), 강조2=c.get("강조2", []), 자막=rows, 모양=c.get("모양"), 작은줄=c.get("작은줄", [0] if len(c["제목"]) == 2 else [])))
    p = f"{WORK}/{c['이름']}.html"
    open(p, "w", encoding="utf-8").write(MK.페이지(부분, 판=P, ch="reel", ai=False, 끝=(None if 끝 else 초), 상단줄=not c.get("표지")))
    mp4 = HM.render(p, c["이름"], 초=초, fps=30, ch="reel")[0]
    return mp4, 초, wav

def 만들기(씬, 이름, P="k_gold", out_dir=None):
    os.makedirs(f"{WORK}/parts", exist_ok=True)
    parts, t, voice = [], 0.0, []
    for i, c in enumerate(씬):
        mp4, 초, wav = 장면(c, P, i, i == len(씬) - 1)
        dst = f"{WORK}/parts/{os.path.basename(mp4)}"; shutil.move(mp4, dst); parts.append(dst)
        voice.append((t + (0.05 if c.get("표지") else LEAD), wav)); t += 초
        print(f"  {c['이름']} {초}초")
    lst = f"{WORK}/{이름}.txt"; open(lst, "w").write("".join(f"file '{x}'\n" for x in parts))
    raw = f"{WORK}/{이름}_raw.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", raw], check=True)
    src, mo = f"{SNS}/_vr_src", f"{SNS}/_vr_out"
    shutil.rmtree(src, True); shutil.rmtree(mo, True); os.makedirs(src)
    shutil.copy(raw, f"{src}/vr-{이름}.mp4")
    subprocess.run(["python3", "pipeline/clip_v3_music.py"], cwd=SNS, env=dict(os.environ, ZS_SRC="_vr_src", ZS_OUT="_vr_out", ZS_PRE="vr-", ZS_LIB="v2"), check=True, stdout=subprocess.DEVNULL)
    mus = f"{WORK}/{이름}_music.mp4"; shutil.copy(f"{mo}/vr-{이름}.mp4", mus)
    shutil.rmtree(src, True); shutil.rmtree(mo, True)
    mix = f"{WORK}/{이름}_mix.mp4"; NR.섞기(mus, voice, mix)
    out = f"{out_dir or WORK}/{이름}.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", mix, "-c:v", "libx264", "-preset", "veryfast", "-crf", "24", "-c:a", "copy", out], check=True)
    print("끝", out, round(t, 1), "초")
    return out
