"""K-143 검사(대표 10/18 16:28 '원고마다 검색 의도 카드를 먼저 적고 도입부·구성·이미지·연결글을 그 의도로 정한다').
카드: naver/intent_cards.json. 재는 것:
  1) 10/20 뒤 나갈 원고(done 아님)에 카드가 있는가 — 없으면 '카드 없음'(빚으로 센다)
  2) 카드 칸이 비지 않았는가(keywords·intent·first3·answer_keys·order·images·related)
  3) applied=true 인 글: answer_keys 가 본문 첫 3줄에 모두 있는가, 연결글(related.id)이 카드와 같은가, CTA 문구(cta_copy.json)가 있는가 → 어긋나면 막음
사용: python3 naver/intent_check.py   (막힐 것이 있으면 종료 코드 1)"""
import os, re, json, html, sys
HERE = os.path.dirname(os.path.abspath(__file__))
INTENTS = {"알고 싶다", "내 상황이 맞나", "둘 중 고르고 싶다", "해 보고 싶다"}
FROM = "2026-10-20"

def first3(body):
    t = [html.unescape(re.sub(r"<[^>]+>", "", x)).strip() for x in re.findall(r"<p>(.*?)</p>", body)]
    t = [x for x in t if x and x != "\xa0" and not x.startswith("안녕하세요") and not x.endswith("정월이에요.")]
    return " ".join(t[:3])

def run():
    pages = json.load(open(os.path.join(HERE, "pages.json"), encoding="utf-8"))
    cards = json.load(open(os.path.join(HERE, "intent_cards.json"), encoding="utf-8"))["cards"]
    cta = json.load(open(os.path.join(HERE, "cta_copy.json"), encoding="utf-8"))["posts"]
    bad, wait, none = {}, [], []
    for pid, v in sorted(pages.items(), key=lambda kv: kv[1].get("dt", "")):
        if v.get("done") or (v.get("dt") or "") < FROM: continue
        c = cards.get(pid)
        if not c: none.append(pid); continue
        miss = [k for k in ("keywords", "intent", "first3", "answer_keys", "order", "images", "related") if not c.get(k)]
        if miss: bad.setdefault(pid, []).append("빈 칸: " + ",".join(miss))
        if c.get("intent") and c["intent"] not in INTENTS: bad.setdefault(pid, []).append(f"의도 유형 '{c['intent']}'(넷 중 하나)")
        if not c.get("applied"): wait.append(pid); continue
        f3 = first3(v.get("body", ""))
        lack = [k for k in c.get("answer_keys", []) if k not in f3]
        if lack: bad.setdefault(pid, []).append("첫 3줄에 답 없음: " + ",".join(lack))
        rid = (v.get("related") or {}).get("id")
        if rid != c.get("related"): bad.setdefault(pid, []).append(f"연결글 {rid} ≠ 카드 {c.get('related')}")
        if pid not in cta: bad.setdefault(pid, []).append("CTA 문구 없음(cta_copy.json)")
    return bad, wait, none

if __name__ == "__main__":
    bad, wait, none = run()
    for k, v in bad.items(): print("✗", k, "; ".join(v))
    print(f"K-143: 막힌 글 {len(bad)} · 카드 있고 반영 대기 {len(wait)}편({' '.join(wait)}) · 카드 없는 글 {len(none)}편")
    sys.exit(1 if bad else 0)
