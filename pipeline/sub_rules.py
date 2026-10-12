"""릴스·클립 자막 규칙 R60~R67 (대표 10/13 07:15 '릴스 관련 참고해' - 타 계정 릴스 프롬프트 5개를 읽고, 우리 규칙과 겹치지 않는 것만 우리 말로 올림).
자막 = 화면에 놓인 글 덩어리(text()·tblock() 한 번 호출). 수집은 sub_harvest.harvest(장면표)가 하고, 이 파일이 규칙으로 잰다.
두 단계: 엄격(새로 만드는 영상은 모두 통과) / 완화(10/13 이전에 이미 예약·발행된 영상이 넘지 말아야 할 선).
기준 확정(2026-10-13 08:02 대표): 엄격 기준=새로 만드는 영상(새 렌더)에만, 이미 예약·발행된 영상=완화 기준. 판정: content/audit/sub_base_1013.json 에 든 영상(10/13 이전 것)은 완화, 거기 없는 새 영상은 자동으로 엄격, 10/13 이후 새로 렌더해 예약 칸에 교체한 영상은 STRICT_IDS 에 올려 엄격.
R11 끝 장면 고정 문구('프로필 링크…'·'팔로우…')와 AI 고지·주소는 줄 길이·줄 수에서 뺀다(문구가 R11로 정해져 있음).
사용: python3 pipeline/sub_rules.py [--strict] [--show]   (qa_all 의 '릴스 자막' 줄이 완화 기준으로 부른다)"""
import os, re, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.abspath(os.path.join(HERE, "..")); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(R, "content"))
# ── 숫자 기준(우리 영상 실측으로 정함: 띠 릴스 34초 10장면, 데이터 릴스 24초 7장면, 클립 12초 5장면. 10/13 측정 68편·장면 720개) ──
LIM = {
 "엄격": dict(block_lines=2, line_chars=14, scene_dur=(2.0, 5.0), scene_blocks=3),   # 새 영상: 한 덩어리 두 줄 · 한 줄 14자(공백 빼고, 공백 포함 17자 안팎)
 "완화": dict(block_lines=3, line_chars=16, scene_dur=(2.0, 7.5), scene_blocks=4),   # 이미 예약된 영상: 3줄·16자·6초·덩어리 4개까지
}
LEGEND = re.compile(r"같은 색\s?=")   # 여러 장면에 고정으로 뜨는 범례(R65와 같은 예외): R64 덩어리 수에서 뺀다
FIXED = re.compile(r"프로필 링크|팔로우|zaoseon|AI 캐릭터|생년월일")          # R11 고정 문구·주소·AI 고지(R02·R03·R11)
KORNUM = re.compile(r"(?<![가-힣])(두|세|네|다섯|여섯|일곱|여덟|아홉|열|스무)\s?(명|개|번|장|초|분|시간|배|퍼센트)(?!째)")   # R66: 한 번(한 번 더)은 입말이라 뺀다, '가지'도 뺀다
SOUND = re.compile(r"소리\s?(를\s)?(켜|켠|듣)|들어\s?보|들려\s?드|귀\s?기울")       # R67: 소리가 있어야 이해되는 말
REASON = re.compile(r"[?]|까요|나요|인가요|[0-9]|왜|이유|비밀|사람|띠|해$|해,|vs|VS|몇|어느|차이|다른 말|같은 말|세 가지|맞|고르|세요|보세요")  # R62 첫 자막에 이 영상을 볼 이유: 질문·숫자·대상·대비 중 하나
ADVISE = ("R62", "R66", "R67")   # 완화 단계에서는 권고(걸려도 올리기를 막지 않고 목록만 보여 준다). 엄격 단계에서는 모두 막는다
STRICT_IDS = {"zodiac/양띠", "zodiac/쥐띠", "reels2/데이터v2-four", "reels2/데이터v2-liuyao", "reels2/데이터v2-harak"}   # 10/13 새로 렌더해 예약 칸에 교체한 영상(엄격 통과 확인). 이 밖의 옛 예약본은 완화
try: BASE = set(json.load(open(os.path.join(R, "content", "audit", "sub_base_1013.json"), encoding="utf-8"))["키"])
except Exception: BASE = set()
def level_of(name): return "엄격" if (name in STRICT_IDS or (BASE and name not in BASE)) else "완화"
LEGACY = ("pilots/", "reels/", "reels2/데이터v2-pair", "misc/점격자", "misc/손없는날")   # 이미 발행됐거나 새 틀로 교체돼 예약에 없는 옛 영상(10/13 확인). 검사에서 뺀다
REDO = {"clips2/클립v2-n40-c1": "네이버 클립 10/25 · 장면2 글 덩어리 5개"}   # 소스만 고쳤거나 아직 못 고친 것: 막지는 않고 목록으로 보여 준다      # 10/13 이후 새로 만든·고친 영상 키 (예: "zodiac/개띠"). 여기 든 영상은 엄격 기준
def _norm(s): return re.sub(r"[\s·,.!?~*'\"]", "", s)
def check(name, scenes, level=None):
    """scenes = sub_harvest.harvest() 결과. 돌려주는 값: [(규칙, 장면번호, 설명)]"""
    L = LIM[level or level_of(name)]; out = []
    for s in scenes:
        no, dur, bl = s["no"], s["dur"], s["blocks"]
        body0 = [b for b in bl if not FIXED.search(" ".join(b["lines"])) and len("".join(b["lines"]).replace(" ", "")) > 2]
        if dur < L["scene_dur"][0] or (dur > L["scene_dur"][1] and len(body0) <= 3): out.append(("R63", no, f"컷 길이 {dur}초 ({L['scene_dur'][0]}~{L['scene_dur'][1]}초)"))
        body = [b for b in bl if not FIXED.search(" ".join(b["lines"])) and not LEGEND.search(" ".join(b["lines"])) and len("".join(b["lines"]).replace(" ", "")) > 2]   # 카드 번호 같은 1~2글자 라벨은 덩어리로 세지 않는다
        if len(body) > L["scene_blocks"]: out.append(("R64", no, f"한 장면 글 덩어리 {len(body)}개 ({L['scene_blocks']}개 이하)"))
        for b in body:
            if b["size"] < 44: continue
            if len(b["lines"]) > L["block_lines"]: out.append(("R60", no, f"{len(b['lines'])}줄 '{b['lines'][0]}…' ({L['block_lines']}줄 이하)"))
            for ln in b["lines"]:
                n = len(ln.replace(" ", ""))
                if n > L["line_chars"]: out.append(("R61", no, f"한 줄 {n}자 '{ln}' ({L['line_chars']}자 이하)"))
            t = " ".join(b["lines"])
            if KORNUM.search(t): out.append(("R66", no, f"숫자는 아라비아 숫자로 '{KORNUM.search(t).group(0)}'"))
            if SOUND.search(t): out.append(("R67", no, f"소리가 있어야 이해되는 말 '{SOUND.search(t).group(0)}'"))
    for s in scenes:                                     # R65 화면·자막 중복: 같은 장면에 같은 말이 두 번 나오면 하나를 뺀다(여러 장면에 걸쳐 고정으로 뜨는 범례는 중복이 아니다)
        seen = set()
        for b in s["blocks"]:
            t = _norm("".join(b["lines"]))
            if len(t) < 6 or FIXED.search(t): continue
            if t in seen: out.append(("R65", s["no"], f"같은 말이 겹침 '{' '.join(b['lines'])[:16]}'"))
            seen.add(t)
        for a_ in s["blocks"]:                           # 한 덩어리가 다른 덩어리를 통째로 되풀이하는 경우(작은 글이 큰 글 설명을 그대로 반복)도 겹침
            for b_ in s["blocks"]:
                ta, tb = _norm("".join(a_["lines"])), _norm("".join(b_["lines"]))
                if a_ is not b_ and len(ta) >= 8 and ta == tb and not FIXED.search(ta) and a_["size"] != b_["size"]: out.append(("R65", s["no"], f"같은 말이 크기만 달리 겹침 '{ta[:10]}'"))
    if scenes:                                           # R62 첫 자막에 볼 이유
        first = " ".join(" ".join(b["lines"]) for b in scenes[0]["blocks"] if not FIXED.search(" ".join(b["lines"])))
        if first and not REASON.search(first): out.append(("R62", 1, f"첫 장면 글에 볼 이유(질문·숫자·대상·대비)가 없음 '{first[:20]}'"))
    return out
def registry():
    """검사 대상 장면표(소스에서 바로 모은다). 키는 '묶음/이름'. HTML 편집기로 그린 카드형 영상은 장면표가 없어 여기 없다."""
    import sub_harvest as H, layout_audit as LA, clips_motion_zodiac as Z, pilot_variety as PV
    PV.AUDIT = True; reg = {}
    for g, items in LA.groups().items():
        for nm, sc, cs in items: reg[g + "/" + nm] = H.harvest(sc)
    for n in Z.GEN: reg["zodiac/" + n] = H.harvest(Z.scenes_of(n))
    try:        # 인스타 재활용 릴스(네이버 클립 장면표 12초판) — 게시물형(블로그 이미지)은 장면표가 없어 뺀다
        import reuse_clips as RC
        for (cid, ver), sc in RC.SC.items():
            if ver == "12": reg["reuse/" + cid] = H.harvest(sc)
    except Exception as e: print("재활용 장면표 건너뜀:", str(e)[:60])
    return reg
def run(level=None, show=False, reg=None, gate=False):
    """gate=True: 완화 단계의 권고(R62·R66·R67)는 빼고 막아야 할 것만 돌려준다(qa_all용)."""
    reg = reg or registry(); res = {}
    for k, v in reg.items():
        if gate and (k.startswith(LEGACY) or k in REDO): continue
        r = check(k, v, level); lv = level or level_of(k)
        if gate and lv == "완화": r = [x for x in r if x[0] not in ADVISE]
        if r: res[k] = r
    return res
if __name__ == "__main__":
    lv = "엄격" if "--strict" in sys.argv else None; bad = run(lv, gate="--all" not in sys.argv)
    tot = sum(len(v) for v in bad.values())
    if "--show" in sys.argv:
        for k, v in bad.items():
            for r_, no, m in v: print(f"{k} 장면{no} {r_} {m}")
    for k, m in REDO.items(): print("다시 렌더 대기:", k, "-", m)
    print(f"릴스 자막({lv or '완화/엄격 혼합'}): 걸린 영상 {len(bad)}편 · 위반 {tot}곳")
    sys.exit(1 if tot else 0)
