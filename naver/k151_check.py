"""K-151(대표 10/20) + blogon 진단 검토(10/29 CT, 대표 "원고 작성 엔진에 반영할 거 반영"): 새로 쓰는 네이버 원고의 틀 반복을 막는다.
재는 것(새 글만, 이미 예약·발행한 글은 naver/k151_baseline.json에 묶어 두고 건드리지 않음 — K-147):
  1) 고정 문장: 모든 글에 똑같이 들어간 첫 인사·'결론부터' 문장(아래 FIXED) → 막음. 첫 인사를 넣으려면 그 글의 장면으로 새로 쓴다.
  2) 첫 문단(200자)에 제목 핵심어가 없음 → 막음(K-143·N16: 첫 3줄에 정의·직답 한 문장)
  3) 제목 다섯 기준(대표 11/2 14:42 "블로그온 제목 진단 반영", K-161): ① 핵심어가 제목 맨 앞(10자 안)·본문 첫 200자·소제목 하나 이상·본문 2번 이상 ② 숫자 ③ 15~35자 ④ 찾는 말·후킹(법·이유·뜻·날짜·언제·한눈에·가지 등) ⑤ 특수문자 — 괄호·꺾쇠·느낌표·물결·이모지 금지, 쉼표·가운뎃점·물음표 합쳐 3개까지. 비하 표현(R24) 금지 → 막음
  4) 태그에 '자오선'과 본문 핵심어 태그가 있는가(10/7 대표 확정: 10개 이내, '자오선' 고정) → 막음
사용: python3 naver/k151_check.py   (막힐 것이 있으면 종료 코드 1)"""
import os, re, json, html, sys
HERE = os.path.dirname(os.path.abspath(__file__))
FIXED = ("안녕하세요, 자오선의 정월이에요.", "바쁘신 분들을 위해 결론부터 말씀드릴게요.")   # 미발행 원고 38편 중 37~38편에 같은 문장(10/29 실측)
DEMEAN = ("결정장애", "선택장애", "분노조절장애", "정신병", "멘붕")

def plain(body):
    return " ".join(html.unescape(re.sub(r"<[^>]+>", " ", body.replace("&nbsp;", " "))).split())

def core_kw(title):
    head = re.split(r"[,?]", title)[0]
    head = re.sub(r"20\d\d년?\s*", "", head).strip()
    head = re.sub(r"(일까요|이란|란|뜻|보는 법|총정리)$", "", head).strip()
    return [w for w in head.split() if len(w) >= 2][:2]

HOOK = re.compile(r"(법|이유|뜻|정리|날짜|언제|한눈에|가지|차이|순서|찾기|계산|까|표|기준|총정리|\?)")
def title_check(title, body):
    """제목 다섯 기준(K-161). 처방 문장으로 돌려준다."""
    out = []; kw = core_kw(title); t = plain(body)
    heads = re.findall(r"<p><b>([^<]{3,80})</b></p>", body)
    if kw:
        k = kw[0]
        if title.find(k) > 10: out.append(f"제목 핵심어 '{k}'가 뒤에 있어요 → 맨 앞으로")
        if t.count(k) < 2: out.append(f"'{k}'가 본문에 {t.count(k)}번 → 첫 문단·소제목에 2~3번")
        if not any(k in h for h in heads): out.append(f"소제목에 '{k}'가 없어요 → 소제목 하나에 넣기")
    if not re.search(r"\d", title): out.append("제목에 숫자 없음 → 해·날짜·N가지처럼 이 글의 실제 숫자")
    if not 15 <= len(title) <= 35: out.append(f"제목 {len(title)}자 → 15~35자")
    if not HOOK.search(title): out.append("찾는 말 없음 → 법·이유·뜻·날짜·언제·한눈에 중 이 글에 맞는 것")
    if re.search(r"[()\[\]{}<>「」『』!~]|[\U0001F300-\U0001FAFF\u2600-\u27BF]", title): out.append("제목에 괄호·느낌표·이모지 → 빼기(네이버 색인)")
    if len(re.findall(r"[,·?]", title)) > 3: out.append("쉼표·가운뎃점·물음표 4개 이상 → 3개까지")
    return out

def check(pid, v):
    bad = []; title = v.get("title", ""); t = plain(v.get("body", ""))
    for s in FIXED:
        if s in t: bad.append(f"고정 문장 '{s[:12]}…'(K-151)")
    kw = core_kw(title)
    if kw and not any(k in t[:200] for k in kw): bad.append(f"첫 200자에 핵심어({'·'.join(kw)}) 직답 없음(K-143)")
    bad += title_check(title, v.get("body", ""))
    d = [x for x in DEMEAN if x in title]
    if d: bad.append(f"제목 비하 표현 '{d[0]}'(R24)")
    tags = v.get("tags") or []
    if tags and (tags[-1] != "자오선" or len(tags) > 10): bad.append(f"태그 {len(tags)}개·마지막 '{tags[-1]}'(10개 이내, 마지막 '자오선')")
    if tags and kw and not any(any(k.replace(' ', '') in g for k in kw) for g in tags): bad.append("태그에 제목 핵심어 없음")
    return bad

def run():
    pages = json.load(open(os.path.join(HERE, "pages.json"), encoding="utf-8"))
    base = set(json.load(open(os.path.join(HERE, "k151_baseline.json"), encoding="utf-8"))["ids"])
    out = {}
    for pid, v in pages.items():
        if pid in base or v.get("done"): continue
        b = check(pid, v)
        if b: out[pid] = b
    return out, [p for p in pages if p not in base]

if __name__ == "__main__":
    bad, new = run()
    for k, v in bad.items(): print("✗", k, "; ".join(v))
    print(f"K-151: 새 글 {len(new)}편 · 막힌 글 {len(bad)}편")
    sys.exit(1 if bad else 0)
