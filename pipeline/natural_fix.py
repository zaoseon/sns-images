"""어색한 의문형·호응을 자연어로 고친다(R26). 규칙이 분명한 것만 자동으로 고친다: ① ~예요?/~이에요? → ~인가요? ② 자주 쓴 ~어요? 문장 → ~나요?/~는지 ③ 'N명을 계산했어요' → 'N명의 사주를 계산해 봤어요'.
사용: python3 pipeline/natural_fix.py [--apply]   (기본은 미리보기: 몇 곳 바뀌는지만 센다)"""
import os, re, sys, glob, json
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.abspath(os.path.join(HERE, ".."))
PHRASE = [  # (어색한 말, 자연스러운 말) — 문장째로 확정한 것
 ("몇 개가 겹쳐요?", "몇 개가 겹치나요?"), ("몇 개 겹쳐요?", "몇 개 겹치나요?"), ("*겹쳐요*?", "*겹치나요*?"), ("겹쳐요?", "겹치나요?"),
 ("더 믿어요?", "더 믿으세요?"), ("해당돼요?", "해당되나요?"), ("적 있어요?", "적 있나요?"), ("적 많아요?", "적 많나요?"),
 ("몇 번이 적당해요?", "몇 번이 적당할까요?"), ("주말 밤 뭐 해요?", "주말 밤에는 뭘 하나요?"), ("찔리는 번호 있어요?", "찔리는 번호가 있나요?"),
 ("가장 잘 설명한 건 뭐였어요?", "가장 잘 설명한 건 뭐였나요?"), ("태어난 시간 알아요?", "태어난 시간을 아시나요?"), ("말이 맞아요?", "말이 맞나요?"),
 ("몇 개를 겹쳐요?", "몇 개를 겹치나요?"), ("무작위 3,000명을 계산했어요", "무작위 3,000명의 사주를 계산했어요"),
]
GEN = [(r"뭐예요\?", "뭔가요?"), (r"뭐였어요\?", "뭐였나요?"), (r"(예요|이에요)\?", "인가요?")]    # 명사+예요? → 명사+인가요?
SKIP = ("natural_audit.py", "natural_fix.py", "rules.py", "trendy.py", "trendy_audit.py", "trendy_img.py", "guide_final_img.py", "guide_visual_img.py", "variety_img.py")
def files():
    f = [x for x in glob.glob(os.path.join(R, "content", "*.py")) + glob.glob(os.path.join(R, "pipeline", "*.py")) if os.path.basename(x) not in SKIP]
    f += [os.path.join(R, "naver", "pages.json"), os.path.join(R, "content", "trendy_lines.json"), os.path.join(R, "content", "caption_lines.json")]
    return [x for x in f if os.path.exists(x)]
def fix_text(t):
    n = 0
    for a, b in PHRASE:
        c = t.count(a)
        if c: t = t.replace(a, b); n += c
    for pat, rep in GEN:
        t, c = re.subn(pat, rep, t); n += c
    return t, n
if __name__ == "__main__":
    apply = "--apply" in sys.argv; tot = 0; per = {}
    for f in files():
        s = open(f, encoding="utf-8", errors="replace").read(); t, n = fix_text(s)
        if n: per[os.path.basename(f)] = n; tot += n
        if n and apply: open(f, "w", encoding="utf-8").write(t)
    sw = os.path.join(R, "content", "reel_swaps.json"); d = json.load(open(sw, encoding="utf-8")); cn = 0
    for r in d:
        for k in ("caption", "note", "title"):
            if r.get(k):
                t, n = fix_text(r[k]); cn += n
                if n and apply: r[k] = t
    if apply: json.dump(d, open(sw, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(("적용" if apply else "미리보기") + f": 파일 {len(per)}개 {tot}곳 + 앱 항목 글 {cn}곳"); print(per)
