"""릴스를 '평소 대비 몇 배'로 본다 — 대표 10/16 레퍼런스(instagram-agent-skill)에서 가져온 생각.

왜 배수인가
  절대 조회수는 계정 크기와 발행 시점에 좌우된다. 그래서 조회수로 형식을 판정하면 틀린다
  (10/16 D-328: 교차분석 숫자 형식을 조회·시청시간으로 접으려 했다가 철회했다).
  그 계정 **평소의 몇 배**인지로 보면 그 두 가지가 상쇄된다.

무슨 지표를 보나 — 셋을 나란히 본다
  조회      알고리즘이 얼마나 밀어 줬나. 콘텐츠 품질이 아니다
  평균 시청초 얼마나 오래 봤나. 다만 영상 길이에 휘둘린다
  **3초율**  3초 넘게 본 사람 비율(메트리쿨 IGRE28). 길이에 안 휘둘리고
            '훅이 붙잡았나'를 가장 곧게 잰다 — 이것이 1순위다

기준선은 우리 릴스의 **중앙값**이다(평균이 아니다 — 한 편이 터지면 평균이 끌려간다).

조심할 것: 지금 우리 조회는 19~253이다. 표본이 작아서 한 편의 배수는 운일 수 있다.
**형식을 판정할 때는 그 형식 여러 편의 중앙값으로 본다**(K-103).

사용: python3 pipeline/reel_scoreboard.py            전체 표
      python3 pipeline/reel_scoreboard.py --형식      형식별 묶음
자료: content/audit/reel_metrics.json (메트리쿨에서 받아 갈아 끼운다)
"""
import os, sys, json, statistics as S

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
자료 = os.path.join(ROOT, "content", "audit", "reel_metrics.json")
터짐 = 3.0        # 평소의 3배 넘으면 '신호'(레퍼런스 기준). 1.5배는 버린다


def 읽기():
    d = json.load(open(자료, encoding="utf-8"))
    return [dict(zip(d["_필드"], r)) for r in d["rows"]], d.get("_받은날", "?")


def 기준선(rs):
    return {k: S.median([r[k] for r in rs]) for k in ("조회", "평균시청초", "3초율")}


def 배수(r, m):
    return {k: (r[k] / m[k] if m[k] else 0) for k in m}


def 표(rs, m):
    print(f"{'이름':22}{'형식':14}{'조회':>5}{'배':>5}{'시청':>6}{'배':>5}{'3초율':>7}{'배':>5}")
    for r in sorted(rs, key=lambda x: -(x["3초율"] / m["3초율"] if m["3초율"] else 0)):
        b = 배수(r, m)
        표시 = "  ←신호" if b["3초율"] >= 터짐 else ""
        print(f"{r['이름'][:20]:22}{r['형식'][:12]:14}{r['조회']:>5}{b['조회']:>5.1f}"
              f"{r['평균시청초']:>6.2f}{b['평균시청초']:>5.1f}{r['3초율']:>6.1f}%{b['3초율']:>5.1f}{표시}")


def 형식별(rs, m):
    g = {}
    for r in rs:
        g.setdefault(r["형식"], []).append(r)
    print(f"{'형식':16}{'편':>3}{'3초율 중앙':>10}{'배':>5}{'최고':>7}{'시청 중앙':>9}{'배':>5}")
    for 이름, v in sorted(g.items(), key=lambda kv: -S.median([x["3초율"] for x in kv[1]])):
        r3 = S.median([x["3초율"] for x in v]); w = S.median([x["평균시청초"] for x in v])
        print(f"{이름[:14]:16}{len(v):>3}{r3:>9.1f}%{r3/m['3초율']:>5.1f}"
              f"{max(x['3초율'] for x in v):>6.1f}%{w:>9.2f}{w/m['평균시청초']:>5.1f}")
    print("\n편 수가 1~2편인 형식은 판정하지 않는다 — 운일 수 있다(K-103).")


def main():
    rs, 날 = 읽기(); m = 기준선(rs)
    print(f"릴스 {len(rs)}편 · 받은 날 {날}")
    print(f"평소(중앙값) — 조회 {m['조회']:.0f} · 평균 시청 {m['평균시청초']:.2f}초 · 3초율 {m['3초율']:.1f}%\n")
    (형식별 if "--형식" in sys.argv else 표)(rs, m)
    n = sum(1 for r in rs if 배수(r, m)["3초율"] >= 터짐)
    print(f"\n3초율이 평소의 {터짐:.0f}배 넘는 편: {n}건 / {len(rs)}건")
    if n == 0:
        print("아직 '터진' 편이 없다. 지금 우리가 고르는 것은 잘된 것 중 하나가 아니라 덜 나쁜 것이다.")


if __name__ == "__main__":
    main()
