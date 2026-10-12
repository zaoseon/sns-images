"""인스타 캐러셀 최소 장 수(R58, 대표 10/12 20:56 "캐러셀은 표지·본문·CTA까지 최소 7장이 기본").
- check_count(n, 이름): 만드는 쪽(렌더러)이 그리기 전에 부른다. 7장 미만이면 문제 목록을 돌려준다.
- check_dir(폴더): 올리기 전에 폴더의 {키}_{번호}.jpg 묶음마다 장 수를 센다.
- scan_archive(): 앞으로 예약된 인스타 캐러셀(Metricool 보관본 zaoseon-site data/sns_archive.json, k=POST, 이미지 2장 이상) 중 7장 미만을 찾는다.
  이미지 1장짜리 단일 게시물은 캐러셀이 아니라서 세지 않는다.
사용: python3 pipeline/carousel_rules.py [폴더 ...]   (폴더를 주지 않으면 예약 보관본만 검사)"""
import os, re, sys, json, collections, datetime as D
MIN_SLIDES = 7
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '..'))
SITE = os.environ.get('ZAOSEON_SITE', os.path.abspath(os.path.join(ROOT, '..', 'zaoseon-site')))
def check_count(n, name='캐러셀'):
    return [] if n >= MIN_SLIDES else [f'{name}: {n}장 - 인스타 캐러셀은 {MIN_SLIDES}장 이상(표지·본문·해 볼 것·CTA, R58)']
def check_dir(folder):
    g = collections.defaultdict(set)
    for f in os.listdir(folder):
        m = re.match(r'(.+)_(\d+)\.(jpg|jpeg|png)$', f)
        if m: g[m.group(1)].add(int(m.group(2)))
    return [e for k, v in sorted(g.items()) if len(v) > 1 for e in check_count(len(v), f'{os.path.basename(folder)}/{k}')]
def scan_archive(now=None):
    p = os.path.join(SITE, 'data', 'sns_archive.json')
    if not os.path.exists(p): return [f'보관본 없음: {p}']
    arch = json.load(open(p, encoding='utf-8')); now = now or D.datetime.now(D.timezone(D.timedelta(hours=9))).strftime('%Y-%m-%dT%H:%M'); bad = []
    for v in sorted(arch.values(), key=lambda v: v.get('t', '')):
        if (v.get('t') or '') <= now or v.get('st') not in (None, '', 'PENDING'): continue
        if 'instagram' not in str(v.get('n')) or v.get('k') != 'POST': continue
        try: m = int(v.get('m') or 0)
        except ValueError: continue
        if 2 <= m < MIN_SLIDES: bad += check_count(m, f"예약 {v['t']} [{(v.get('x') or '')[:20]}] id {v.get('id')}")
    return bad
if __name__ == '__main__':
    bad = scan_archive() if len(sys.argv) < 2 else [e for d in sys.argv[1:] for e in check_dir(d)]
    for b in bad: print('걸림:', b)
    print('통과' if not bad else f'{len(bad)}건 걸림'); sys.exit(1 if bad else 0)
