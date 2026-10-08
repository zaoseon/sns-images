"""자연스러운 한국어 검사(R26, 10/8 대표: '여러분은 무슨 띠예요?'처럼 ~예요?는 어색하다. 어색하고 일반적이지 않은 말·AI스러운 말을 자연어로).
영상 속 글·캡션·블로그 글을 훑어 ① 어색한 의문형(~예요?/~어요?) ② 번역투·AI 말투 ③ 사람·사물 호응이 안 맞는 말을 찾는다. 찾은 곳은 content/natural_ko.json의 바꿀 말로 고친다.
사용: python3 pipeline/natural_audit.py [--show]"""
import os, re, json, glob, collections
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.abspath(os.path.join(HERE, ".."))
ZR = os.path.abspath(os.path.join(R, "..", "zaoseon-site"))
EMO = re.compile("[\U0001F300-\U0001FAFF\u2600-\u27BF]")
PAT = [  # (이름, 정규식, 이유·바꿀 말)
 ("의문형 ~예요?/~이에요?", r"(예요|이에요)\s?\?", "입말에서 어색함 → ~인가요? / ~뭔가요? (예: 무슨 띠인가요?)"),
 ("의문형 ~어요?/~해요?", r"(어요|아요|해요|여요|워요|져요|줘요|봐요|와요|쳐요|켜요|려요|겨요|써요|펴요|내요)\s?\?", "입말에서 어색함 → ~나요? / ~는지 / ~까요? (예: 겹치나요?)"),
 ("반말 질문 '~까?'", r"[가-힣]까\?", "→ ~까요? (시청자 질문은 존댓말)"),
 ("어색한 '~같죠?'", r"같죠\?", "→ ~같을까요? / ~같나요?"),
 ("번역투 ~에 대해", r"에 대해", "→ ~을/를, ~이/가 궁금하면"),
 ("번역투 ~에 의해", r"에 의해", "→ ~이/가, ~ 때문에"),
 ("번역투 ~로 인해", r"(으로|로) 인해", "→ ~ 때문에"),
 ("번역투 ~의 경우", r"의 경우", "→ ~라면, ~는"),
 ("번역투 ~에 있어서", r"에 있어서", "→ ~에서, ~할 때"),
 ("AI 말투 '다양한'", r"다양한", "→ 여러, 갖가지, 구체적으로 쓰기"),
 ("AI 말투 '~라고 할 수 있'", r"(라고|이라고) 할 수 있", "→ ~예요, ~인 셈이에요"),
 ("AI 말투 '도움이 됩니다/돼요'", r"도움이 (됩니다|돼요|될 거예요)", "→ 구체적으로 어떻게 돕는지 쓰기"),
 ("AI 말투 '~하는 것이 좋습니다'", r"하는 것이 좋(습니다|아요)", "→ ~해 보세요, ~하면 편해요"),
 ("딱딱한 '~합니다/됩니다'", r"(?<![가-힣])[가-힣]+(합니다|됩니다|드립니다|바랍니다)(?!\?)", "→ ~해요(해요체 통일). 필수 고지 '입니다'는 예외"),
 ("호응 안 맞음 'N명을 계산'", r"[0-9,]+명(을|를)\s?계산", "→ N명의 사주를 계산해 봤어요"),
 ("과한 강조 매우/굉장히/엄청", r"(매우|굉장히|엄청)", "→ 빼거나 구체적인 말로"),
]
OK_LINES = ("정월은 가상의 AI 캐릭터입니다", "본 콘텐츠는", "이용약관")
def corpus():
    out = []
    d = json.load(open(os.path.join(R, "content", "reel_swaps.json"), encoding="utf-8"))
    for r in d:
        if r.get("status") in ("new", "wait", "hold") and r.get("caption"): out.append((f"캡션 {r['id']}", r["caption"]))
    for f in sorted(glob.glob(os.path.join(R, "content", "*.py")) + [os.path.join(R, "pipeline", x) for x in ("data_reels.py", "new_tri_reels.py", "pick_reel.py", "motion_dots.py", "motion_kinetic.py", "card_kit.py", "caption_rules.py", "reels_engine.py")]):
        if not os.path.exists(f): continue
        for ln, line in enumerate(open(f, encoding="utf-8", errors="replace"), 1):
            if line.lstrip().startswith("#"): continue
            for s in re.findall(r"[\"']([^\"'\n]{4,240})[\"']", line):
                if re.search(r"[가-힣]", s) and not re.search(r"(import|def |http|\.py|\.json|\.mp4)", s): out.append((f"{os.path.basename(f)}:{ln}", s.replace("\\n", " ")))
    bp = os.path.join(R, "naver", "pages.json")
    if os.path.exists(bp):
        bd = json.load(open(bp, encoding="utf-8")); items = bd.items() if isinstance(bd, dict) else enumerate(bd)
        for k, v in items:
            def walk(x, path):
                if isinstance(x, str):
                    if re.search(r"[가-힣]", x): out.append((f"블로그 {k}{path}", x))
                elif isinstance(x, list):
                    for i, y in enumerate(x): walk(y, f"{path}[{i}]")
                elif isinstance(x, dict):
                    for kk, y in x.items(): walk(y, f"{path}.{kk}")
            walk(v, "")
    t = os.path.join(R, "content", "trendy_lines.json")
    if os.path.exists(t):
        for k, v in json.load(open(t, encoding="utf-8")).items():
            if v["opener"]: out.append((f"트렌디 {k}", v["opener"]))
    return out
def scan(texts=None):
    texts = texts or corpus(); hits = []
    for where, t in texts:
        if any(o in t for o in OK_LINES) and not re.search(r"(예요|이에요)\s?\?", t): continue
        for name, pat, why in PAT:
            if pat is None:
                m = EMO.search(t)
                if m: hits.append((name, where, t[:70], m.group(0)))
            else:
                for m in re.finditer(pat, t): hits.append((name, where, t[max(0, m.start() - 14):m.end() + 6], m.group(0)))
        n = len(re.findall(r"(일 수 있어요|일 수도 있어요|할 수 있어요)", t))
        if n >= 4: hits.append(("헤징 남발(~일 수 있어요 4번 이상)", where, t[:60], str(n)))
    return hits
if __name__ == "__main__":
    import sys
    h = scan(); c = collections.Counter(x[0] for x in h)
    print(f"훑은 글 {len(corpus())}개 · 걸린 곳 {len(h)}곳"); [print(f"  {k}: {v}곳") for k, v in c.most_common()]
    if "--show" in sys.argv:
        for name in c: 
            print("==", name); [print("   ", x[1], "|", x[2].replace("\n", " ")) for x in h if x[0] == name][:0]
            for x in [y for y in h if y[0] == name][:6]: print("   ", x[1], "|", x[2].replace("\n", " "))
    json.dump(h, open(os.path.join(R, "content", "audit", "natural_audit.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
