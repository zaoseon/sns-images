"""예약 전 원고(n26~n33) 전체 점검 - 고친 뒤에는 처음부터 끝까지 다시 돌린다(10/3 대표 원칙 7).
점검: 금지어, 공백 포함 1500자 이상, 본문 이미지 수·파일, 연결 문구 1개와 연결 글, 첫머리 결론, 글 안 같은 문장 반복(목차·소제목 제외), 제목·태그·시각·대표 이미지 불변, 목차=소제목, links_plan 규칙.
사용: python3 naver/qa_posts.py [비교할 옛 pages.json 경로]"""
import json, re, sys, os
from urllib.parse import unquote
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); os.chdir(HERE)
import links_plan as LP
args = sys.argv[1:]; jp = [a for a in args if a.endswith('.json')]; ids = [a for a in args if re.match(r'^n\d+$', a)] or [f'n{i}' for i in range(26, 34)]
reg = json.load(open('pages.json', encoding='utf-8')); before = json.load(open(jp[0], encoding='utf-8')) if jp else None
def plain(h): t = re.sub(r'<(br|/p|/div|/h\d)[^>]*>', '\n', h); t = re.sub(r'<[^>]+>', '', t).replace('&nbsp;', ' '); return re.sub(r'\n{2,}', '\n', t)
def chars(h): return len(re.sub(r'<[^>]+>|&nbsp;', '', h))
ok = True
for k in ids:
    REL = LP.REL_FIX if k in LP.REL_FIX else LP.REL            # 이미 예약한 글(n02~n25)은 새로 계획한 연결(REL_FIX)
    v = reg[k]; b = v['body']; t = plain(b); issues = []
    for bad in ('—', '엔진', '초안', '리포트', '6체계'):
        if bad in t: issues.append('금지어 ' + bad)
    if '지도' in t and not v.get('done'): issues.append('금지어 지도(세 지도·두 지도 같은 비유는 독자가 못 알아듣는다, 10/4 대표 지적): 사주·별자리·숫자를 직접 쓰거나 "풀이"로 쓴다')
    n = chars(b)
    if n < 1500: issues.append(f'{n}자')
    imgs = re.findall(r'<img[^>]*src="([^"]+)"', b)
    if before and len(imgs) != len(re.findall(r'<img', before[k]['body'])): issues.append('본문 이미지 수 달라짐')
    for u in imgs:
        if not os.path.exists('img/' + unquote(u.split('/')[-1])): issues.append('이미지 없음')
    ph = re.findall(r'<p><b>👇 ([^<]+)</b></p>', b)
    if len(ph) != 1 or ph[0].replace('&amp;', '&') != REL[k][1] or v.get('related', {}).get('id') != REL[k][0]: issues.append(f'연결 문구/글 이상({len(ph)})')
    if '한줄요약' not in re.sub(r'\s', '', t)[:300]: issues.append('첫머리에 결론 없음')
    ss = []
    for ln in t.split('\n'):
        ln = ln.strip()
        if not ln or re.match(r'^\d\. ', ln) or ln.startswith('👇'): continue
        ss += [s.strip() for s in re.split(r'(?<=[.?!])\s+', ln) if len(s.strip()) >= 14]
    dup = [s for s in set(ss) if ss.count(s) > 1]
    if dup: issues.append('글 안 반복: ' + '; '.join(d[:24] for d in dup))
    if before and (v['tags'] != before[k]['tags'] or v['title'] != before[k]['title'] or v['dt'] != before[k]['dt'] or v['cover'] != before[k]['cover']): issues.append('제목·태그·시각·대표 이미지가 바뀜')
    if before and before[k].get('done') and not v.get('done'): issues.append('예약 완료 표시가 풀림')
    toc = re.findall(r'<p>(\d)\. ([^<]+)</p>', b)[:6]; heads = re.findall(r'<p><b>(\d)\. ([^<]+)</b></p>', b)
    if toc != heads[:6]: issues.append('목차와 소제목 불일치')
    print(k, f'{n}자', '이상 없음' if not issues else issues); ok = ok and not issues
r = LP.check() + LP.check_fix(); print('links_plan:', r or '위반 없음'); print('전체:', '통과' if ok and not r else '확인 필요'); sys.exit(0 if ok and not r else 1)
