"""일간 3회차 캡션 8편 — capfix.rebuild 틀(행동·팔로우·프로필 링크 한 번·브랜드 두 줄·태그 5) + check 0건이어야 저장."""
import os, sys, json, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "pipeline")); import capfix as CF
src = open(os.path.join(HERE, "build.py"), encoding="utf-8").read()
ns = {"__file__": os.path.join(HERE, "build.py")}; exec(src.split("# ── 바탕")[0].replace('if __name__', 'if False'), ns)   # REELS·GAN만 읽는다(렌더 안 함)
GAN = ns["GAN"]
TAIL = ["프로필 링크에서 생년월일만 넣으면 내 첫 글자를 1초 만에 볼 수 있어요.",
        "내 첫 글자가 뭔지는 프로필 링크에서 생년월일로 바로 확인해 보세요.",
        "프로필 링크에 생년월일을 넣으면 내 첫 글자와 타고난 기운이 나와요."]
out = {}
for k, r in enumerate(ns["REELS"]):
    body = [f"{r['hook'][0]} {r['hook'][1]}.", f"{r['sub']}.", f"태어난 날 첫 글자가 {r['name']}({GAN[r['i']]})인 분의 이야기예요.",
            f"{r['gi']}.", f"{' '.join(r['why'])}.", f"오늘 해 볼 것: {' '.join(r['todo'])}."]
    raw = "\n".join(body) + "\n" + TAIL[k % 3] + f"\n#사주 #운세 {r['tag']} #성격테스트 #자기이해"
    t = CF.rebuild(raw); bad = CF.check(t)
    assert not bad, (r["id"], bad, t)
    out[f"ilgan3-{r['id']}"] = t
json.dump(out, open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(out["ilgan3-gab"]); print(len(out), "편 check 0")
