"""원고 문장 겹침 검사(읽기 전용): 지정한 글의 문장이 다른 글에 똑같이 나오는 비율과 목록. 사용: python3 naver/dupcheck.py n26 n27 ... """
import json, re, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
def sents(html):
    t = re.sub(r'<(br|/p|/div|/h\d)[^>]*>', '\n', html); t = re.sub(r'<[^>]+>', '', t).replace('&nbsp;', ' ')
    out = []
    for ln in t.split('\n'):
        for s in re.split(r'(?<=[.?!])\s+', ln.strip()):
            s = re.sub(r'\s+', ' ', s).strip()
            if len(s) >= 14: out.append(s)
    return out
def report(targets, quiet=False):
    reg = json.load(open(os.path.join(HERE, 'pages.json'), encoding='utf-8'))
    S = {k: set(sents(v.get('body', ''))) for k, v in reg.items() if k.startswith('n') and v.get('body')}
    res = {}
    for k in targets:
        others = set().union(*[S[o] for o in S if o != k]); mine = S[k]; dup = sorted(s for s in mine if s in others)
        res[k] = (len(mine), len(dup), dup)
    tot = sum(r[0] for r in res.values()); d = sum(r[1] for r in res.values())
    if not quiet:
        print(f'대상 {len(targets)}편 | 문장 {tot}개 중 다른 글에도 똑같이 나오는 문장 {d}개 ({d*100//max(1,tot)}%)')
        for k, (n, c, dup) in res.items(): print(f'  {k}: {c}/{n} ({c*100//max(1,n)}%)')
    return res
if __name__ == '__main__':
    r = report(sys.argv[1:] or [f'n{i}' for i in range(26, 34)])
    from collections import Counter
    cnt = Counter(s for _, _, dup in r.values() for s in dup)
    for s, n in cnt.most_common(14): print(n, '편:', s[:80])
