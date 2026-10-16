"""심리학 단락 강조 (대표 10/16 n64 보고): 🧠 단락의 개념 이름을 굵게.
- 개념 이름 = 단락 안 처음 나오는 작은따옴표 말('스포트라이트 효과'). 없으면 핵심 문장 일부를 지정(n44).
- 출처 줄 작은 글자(12px)는 format_body가 📚 줄에 넣는다.
여러 번 돌려도 같다. 사용: python3 naver/psych_style.py [--dry]"""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); REG = os.path.join(HERE, "pages.json")
SKIP = {"n51"}   # 13:20 확정해 네이버에 이미 걸린 글
CORE = {"n44": ("고를 것이 많을수록<br>고르기 어려워지는 거예요.", "<b>고를 것이 많을수록</b><br><b>고르기 어려워지는</b> 거예요.")}
def apply(reg):
    done, miss = [], []
    for k, v in reg.items():
        b = v.get("body", ""); i = b.find("심리학으로 읽으면")
        if i < 0 or k in SKIP: continue
        j = b.find("<p>📚", i); j = j if j > 0 else len(b); blk = b[i:j]
        if k in CORE:
            a, c = CORE[k]
            if c in blk: continue
            if a not in blk: miss.append(k); continue
            blk = blk.replace(a, c, 1)
        else:
            if "<b>'" in blk or "<b>‘" in blk: continue
            m = re.search(r"(['‘][^'’<]{2,30}['’])", blk)
            if not m: miss.append(k); continue
            blk = blk[:m.start()] + "<b>" + m.group(1) + "</b>" + blk[m.end():]
        v["body"] = b[:i] + blk + b[j:]; done.append(k)
    return done, miss
if __name__ == "__main__":
    reg = json.load(open(REG, encoding="utf-8")); d, m = apply(reg); print("굵게", len(d), "편 · 못 찾음", m)
    if "--dry" not in sys.argv: json.dump(reg, open(REG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
