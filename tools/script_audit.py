#!/usr/bin/env python3
"""릴스 대본 카드 검사 (대표 11/17 18:23 '블로그 원고처럼 릴스 대본 작성 규칙 안만드냐', K-227).
사용: python3 tools/script_audit.py [specs/scripts/파일.json ...]   (인자 없으면 전부)
화면 글자가 대본과 같은지는 motion/html_motion.py 의 대본_검사가 영상에서 잰다."""
import json, glob, sys, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "pipeline")); import channel_specs as CS

def audit(s):
    B = CS.BALANCE; bad = []; words = B.get("cta_words", [])
    def need(path, v, n=1):
        if not v or len(str(v).strip()) < n: bad.append(f"[칸 비었음] {path}")
    need("의도.시청자", s.get("의도", {}).get("시청자")); need("의도.유형", s.get("의도", {}).get("유형"))
    # 11/17 19:40 대표 "시청자 약속 이런거 좀 내세우지 말라고, 규칙 제한 풀어"(K-228): 의도.약속 칸·CTA 이유 줄은 필수가 아니다
    need("표지.훅", s.get("표지", {}).get("훅"), 6); need("근거", s.get("근거"))
    장면 = s.get("장면") or []
    if not 장면: bad.append("[장면 없음]")
    표지글 = [s.get("표지", {}).get("훅", ""), s.get("표지", {}).get("보조", "")]
    prev = 0.0
    for g in 장면:
        gid = g.get("id", "?")
        if not g.get("화면글"): bad.append(f"[{gid}] 화면글 없음")
        if g.get("공개"):
            p = "".join(g["풀이"]) if isinstance(g.get("풀이"), list) else g.get("풀이", "")
            if len(p) < 12: bad.append(f"[{gid}] 공개한 것에 풀이가 없거나 너무 짧아요 — 확대되면 곧바로 뜻·이유를 말해야 해요(K-226)")
        for t in g.get("화면글", []) + (g["풀이"] if isinstance(g.get("풀이"), list) else [g.get("풀이", "")]):
            for c in 표지글:
                if c and (t == c): bad.append(f"[{gid}] 표지 문구 '{c}' 를 본문에 또 씀(K-226)")
            for w in words:
                if w in t: bad.append(f"[{gid}] 본문에 CTA 말 '{w}' (K-226)")
        a, b = g.get("초", [0, 0])
        if b - a < 1.5: bad.append(f"[{gid}] 장면이 {b - a:.1f}초 — 1.5초 이상(풀이 읽을 시간)")
        if a < prev - 1e-6: bad.append(f"[{gid}] 장면 시간이 앞 장면과 겹쳐요")
        prev = b
    # 11/17 20:38 대표 "왜 다 같은 색이고… 다양한 모션 그래픽 적용을 할것이지"(K-231): 장면마다 모션을 적고, 이웃 장면과 같은 모션을 쓰지 않는다. 판(색)도 적는다.
    ms = [str(g.get("모션", "")).split(" · ")[0].strip() for g in 장면]
    if 장면 and not all(ms): bad.append("[모션] 장면마다 '모션' 칸을 적어요(K-231)")
    for k in range(1, len(ms)):
        if ms[k] and ms[k] == ms[k - 1]: bad.append(f"[모션] '{장면[k].get('id')}' 장면 모션이 앞 장면과 같아요 — 이웃 장면은 다른 움직임으로(K-231)")
    if len(장면) >= 4 and len(set(ms)) < 3: bad.append("[모션] 모션이 3가지 미만이에요 — 한 편에 3가지 이상(K-231)")
    if not (s.get("판") or {}).get("id"): bad.append("[판] 대본 '판'(색 판 id)을 적어요(K-231)")
    # 11/17 21:06 대표 "진행해"(유튜브 쇼츠 제목 773편 분석, docs/research/유튜브쇼츠_제목패턴_운세_v1.md): 표지 훅 = 대상(브랜드 hook_target) + 물음표로 끝내지 않음(K-107·K-232)
    # 11/17 22:00 대표 "쥐 용 이렇게만 있는걸 쥐띠 용띠 이렇게"(K-234): 화면글 이름표는 브랜드 label_suffix 를 붙여 쓴다(쥐 → 쥐띠)
    try: _B = json.load(open(os.path.join(ROOT, "pipeline", "brands", (s.get("brand") or "zaoseon") + ".json"), encoding="utf-8"))
    except Exception: _B = {}
    _ls = _B.get("label_suffix") or {}
    for g in 장면:
        for x in g.get("화면글", []):
            if str(x).strip() in _ls.get("words", []): bad.append(f"[{g.get('id')}] 화면글 '{x}' — '{x}{_ls.get('suffix', '')}' 로(K-234)")
    # K-222(대표 11/17 15:27 "저게 생년인 줄 어떻게 아냐"): 화면글의 연도 목록(84·96·08)은 '년생'을 붙인다
    for g in 장면:
        for x in g.get("화면글", []):
            if re.search(r"\d{2}·\d{2}", str(x)) and not str(x).rstrip().endswith("년생"): bad.append(f"[{g.get('id')}] '{x}' — 연도 뒤에 '년생'(K-222)")
    hk = str(s.get("표지", {}).get("훅", "")).strip()
    try:
        tgt = json.load(open(os.path.join(ROOT, "pipeline", "brands", (s.get("brand") or "zaoseon") + ".json"), encoding="utf-8")).get("hook_target")
    except Exception: tgt = None
    if hk and tgt and not re.search(tgt, hk): bad.append(f"[표지 훅] '{hk}' — 누구 얘기인지(대상: {tgt}) 넣어요(K-232, 제목 패턴 1)")
    if hk.endswith("?") and not s.get("표지", {}).get("물음표"): bad.append(f"[표지 훅] '{hk}' — 물음표로 끝내지 않고 명사로 끝내요(K-107·K-232, 제목 패턴 2). 꼭 필요하면 표지.물음표=true")
    c = s.get("CTA", {}); t = c.get("유형")
    if t not in ("댓글질문", "팔로우", "프로필링크", "저장", "공유"): bad.append("[CTA] 유형은 댓글질문·팔로우·프로필링크·저장·공유 중 하나(영상 하나에 하나)")  # 저장·공유: 대표 11/17 19:56
    for k in ("큰말", "단추"): need(f"CTA.{k}", c.get(k), 4)
    if t == "댓글질문" and not str(c.get("질문", "")).strip().endswith("?"): bad.append("[CTA] 댓글 유도는 진짜 질문(물음표로 끝)이 있어야 해요 — 이유 없는 댓글 유도 금지(K-226)")
    if t == "프로필링크" and not c.get("얻는것"): bad.append("[CTA] 링크 유도는 '얻는 것'을 말해야 해요(K-226)")
    # 11/17 19:46 대표 "었어요? 이런 말 안쓴다고. 있었나요?~었나요? 이게 맞지"(K-229): 지난 일을 묻는 말은 '~었나요?'
    import re as _re
    모든글 = [s.get("표지", {}).get("훅", ""), s.get("표지", {}).get("보조", "")] + [c.get(k, "") for k in ("큰말", "이유", "단추", "질문")]
    for g in 장면: 모든글 += g.get("화면글", []) + (g["풀이"] if isinstance(g.get("풀이"), list) else [g.get("풀이", "")])
    for t in 모든글:
        m = _re.search(r"[가-힣]*[었았였]어요\?", str(t))
        if m: bad.append(f"[말투] '{m.group(0)}' — 묻는 말은 '~었나요?'로(K-229)")
    return bad

if __name__ == "__main__":
    fs = sys.argv[1:] or sorted(glob.glob(os.path.join(ROOT, "specs/scripts/*.json"))); n = 0
    for f in fs:
        b = audit(json.load(open(f, encoding="utf-8"))); n += len(b)
        print(("통과 " if not b else "막힘 ") + os.path.basename(f)); [print("  -", x) for x in b]
    sys.exit(1 if n else 0)
