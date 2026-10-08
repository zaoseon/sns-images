"""대표 캡처의 정답 줄바꿈(golden_breaks.json)과 우리 줄바꿈을 비교한다. 사용: python3 naver/test_golden_breaks.py [-v]"""
import sys, os, re, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import format_body as FB
G = json.load(open(os.path.join(HERE, "golden_breaks.json"), encoding="utf-8"))["items"]
def ours(it):
    if it.get("table"): return [FB.plain_of(l).strip() for l in FB.box_lines(it["s"])]
    lim = FB.BODY_LIMIT
    return [FB.plain_of(l).strip() for l in FB.sent_lines(it["s"], lim)] if not it["s"].startswith(("1.", "3.")) else [FB.plain_of(l).strip() for l in FB.sent_lines(it["s"], lim)]
def main(verbose=False):
    ok = 0; bad = []
    for it in G:
        got = ours(it)
        if got == it["l"]: ok += 1
        else: bad.append((it, got))
    print(f"정답과 같은 문장 {ok}/{len(G)}")
    if verbose:
        for it, got in bad: print("-", it["s"][:36], "\n   정답:", " / ".join(it["l"]), "\n   현재:", " / ".join(got))
    return ok, len(G)
if __name__ == "__main__": main("-v" in sys.argv)
