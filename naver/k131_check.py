"""K-131 검사(대표 10/17 15:25 "내부 이미지도 탬플릿처럼 쓰지 말고 도식화·인포그래픽 넣어라"): 네이버 원고 본문 그림이 옛 틀 반복인지 잰다.
- 도식: diagrams.json(diagrams_k131 이 만든 파일 → 유형) + 심리 개념 도식(concept_img, naver_zNN_p*.jpg).
- 옛 틀: 파일 끝 글자 i·b·s·q·c·d(+숫자) = 결론·배지 목록·흐름·질문·해 볼 것·표.
규칙: 글마다 도식 2장 이상(서로 다른 유형), 옛 틀 2장 이하, 한 글 안에 같은 도식 유형 두 번 금지, 발행일 이웃한 두 글의 첫 도식 유형이 같지 않게,
한 배치(pages.json k131 꼬리표) 안 같은 모양 2번까지(B2 다시, 10/17 17:42), 도식 선 굵기 상수 LW 7·BOX 4 이상(K-133).
막는 범위: 도식이 한 장이라도 들어간 글(= 다시 그린 글)과 인자로 준 글. 나머지 글은 '빚'으로 숫자만 센다(1주 멈춤 기간: 기준을 검사로, 배치마다 줄인다).
사용: python3 naver/k131_check.py            (다시 그린 글만 막고 빚을 센다)
      python3 naver/k131_check.py n01 n02     (이 글들도 막는다)   --all (전부 막는다)"""
import os, sys, json, re
from urllib.parse import unquote
HERE = os.path.dirname(os.path.abspath(__file__))
OLD = re.compile(r"^naver_z\w+?_([ibsqcd])\d*\.jpg$")
PSY = re.compile(r"^naver_z\w+?_p\d*\.jpg$")

def _fullbleed():
    """K-137 여백 제거판(…f.jpg)은 같은 그림이라 원래 이름으로 잰다(fullbleed_plan.json new → old)."""
    p = os.path.join(HERE, "fullbleed_plan.json")
    if not os.path.exists(p): return {}
    m = {}
    for items in json.load(open(p, encoding="utf-8")).values():
        for it in items:
            if it.get("new"): m[it["new"]] = it["old"]
    return m
FB = _fullbleed()

def kinds(body, reg):
    out = []
    for u in re.findall(r'<img[^>]*src="([^"]+)"', body):
        f = unquote(u.split("/")[-1])
        f = FB.get(f, f)
        if "cta" in f: continue
        if f in reg: out.append(("도식", reg[f]))
        elif PSY.match(f): out.append(("도식", "psych"))
        elif OLD.match(f): out.append(("옛 틀", OLD.match(f).group(1)))
    return out

def check(pages, reg, enforce=None, strict=False):
    bad, debt, first = {}, [], []
    for pid, v in sorted(pages.items(), key=lambda kv: kv[1].get("dt", "")):
        ks = kinds(v.get("body", ""), reg); dg = [t for k, t in ks if k == "도식"]; old = [t for k, t in ks if k == "옛 틀"]
        issues = []
        if len(set(dg)) < 2: issues.append(f"도식 {len(set(dg))}종(2종 이상)")
        if len(old) > 2: issues.append(f"옛 틀 {len(old)}장(2장 이하)")
        dup = sorted({t for t in dg if dg.count(t) > 1})
        if dup: issues.append("같은 도식 두 번: " + ",".join(dup))
        must = strict or bool(dg) or (enforce and pid in enforce)
        if must and dg: first.append((pid, dg[0]))
        if issues: (bad.__setitem__(pid, issues) if must else debt.append(pid))
    for (a, ta), (b, tb) in zip(first, first[1:]):
        if ta == tb: bad.setdefault(b, []).append(f"앞 글 {a}와 첫 도식이 같음({ta})")
    # 배치 안 같은 모양 3번 이상 막기(대표 10/17 17:42 "B2 새 틀 다섯을 색만 바꿔 돌려 썼다"): pages.json k131 꼬리표 첫 낱말 = 배치
    by = {}
    for pid, v in pages.items():
        tag = (v.get("k131") or "").split(" ")[0]
        if not tag: continue
        for k, t in kinds(v.get("body", ""), reg):
            if k == "도식": by.setdefault(tag, {}).setdefault(t, []).append(pid)
    for tag, d in by.items():
        for t, ids in d.items():
            if len(ids) >= 3 and tag not in BATCH_DEBT:
                for pid in ids: bad.setdefault(pid, []).append(f"{tag} 배치 안 같은 모양 {t} {len(ids)}번(2번까지)")
    return bad, debt

BATCH_DEBT = {"B1"}


def k135_check(pages, reg):
    """K-135(대표 10/17 18:16 "도형 돌려쓰기 말고 인포그래픽·차트·학자·고전·영화"): 3판 이후 글(k131 꼬리표에 'K-135')은
    도식이 모두 '그림 거리' 모양(diagrams_k131c.KIND: 가 차트·다 학자/실험·라 고전/우화)이어야 하고, 한 배치 안 상자+화살표 모양(ARROWY)은 4장까지."""
    import diagrams_k131c as D3
    bad, arrow = {}, {}
    for pid, v in pages.items():
        tag = v.get("k131") or ""
        if "K-135" not in tag: continue
        dg = [t for k, t in kinds(v.get("body", ""), reg) if k == "도식"]
        off = [t for t in dg if t not in D3.KIND]
        if off: bad.setdefault(pid, []).append("그림 거리 아닌 도형: " + ",".join(off))
        if len(dg) < 2: bad.setdefault(pid, []).append(f"그림 거리 {len(dg)}장(2장 이상)")
        b = tag.split(" ")[0]
        arrow[b] = arrow.get(b, 0) + sum(t in D3.ARROWY for t in dg)
    for b, n in arrow.items():
        if n > 4: bad.setdefault(f"{b} 배치", []).append(f"상자+화살표 {n}장(4장까지)")
    return bad   # B1(띠·시기 7편)은 관계도·열두 달 칸이 글 내용 그대로라 대표가 그림 내용 승인(10/17 17:42) — 빚으로 둔다

B4CARD = re.compile(r"naver_z\d+_b4f?\.jpg")

def b4_debt(pages):
    """'풀이로 보면' 틀 카드(…_b4.jpg / 여백 제거판 _b4f.jpg)가 남은 글. CT 10/19 12:40 'b4f(세 풀이로 보면)는 K-131이 금지한 틀'.
    옛 틀 2장 이하 규칙으로는 안 걸려서 따로 센다(1주 멈춤: 막지 않고 숫자로 — 대체/빼기는 대표 결정 뒤). 돌려주기: (발행 글, 예약 글)"""
    pub, wait = [], []
    for pid, v in sorted(pages.items(), key=lambda kv: kv[1].get("dt", "")):
        if B4CARD.search(v.get("body", "")): (pub if v.get("done") else wait).append(pid)
    return pub, wait

def line_check():
    """K-133(대표 10/17 17:42 '화살표·차트 얇게 말고 두껍게'): 도식 선 굵기 상수가 기준 밑으로 내려가지 않게."""
    import diagrams_k131 as DG
    out = []
    if DG.LW < 7: out.append(f"주 선 LW {DG.LW}px(7 이상)")
    if DG.LW2 < 5: out.append(f"둘째 선 LW2 {DG.LW2}px(5 이상)")
    if DG.BOX < 4: out.append(f"테두리 BOX {DG.BOX}px(4 이상)")
    if DG.AH < 2.5 * DG.LW: out.append(f"화살표 머리 {DG.AH}px(선 굵기의 2.5배 이상)")
    return out

if __name__ == "__main__":
    pages = json.load(open(os.path.join(HERE, "pages.json"), encoding="utf-8"))
    reg = json.load(open(os.path.join(HERE, "diagrams.json"), encoding="utf-8")) if os.path.exists(os.path.join(HERE, "diagrams.json")) else {}
    ids = {a for a in sys.argv[1:] if not a.startswith("-")}
    sys.path.insert(0, HERE)
    bad, debt = check(pages, reg, ids, "--all" in sys.argv)
    for t in line_check(): bad.setdefault("선 굵기(K-133)", []).append(t)
    for k, v in k135_check(pages, reg).items(): bad.setdefault(k, []).extend(v)
    for k, v in bad.items(): print("✗", k, "; ".join(v))
    pub, wait = b4_debt(pages)
    print(f"K-131: 막힌 글 {len(bad)} · 아직 옛 틀인 글(빚) {len(debt)}편 · '풀이로 보면' b4 카드 남은 글 {len(pub) + len(wait)}편(발행 표시 {len(pub)} · 그 밖 {len(wait)})")
    sys.exit(1 if bad else 0)
