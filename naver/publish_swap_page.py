"""교체 작업판(zaoseon-site public/naver/daepyo.html) + 전체 zip 다시 만들기. 사용: python3 publish_swap_page.py"""
import json, os, shutil, zipfile, html, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import links_plan as LP
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
SITE = '/home/claude/zaoseon-site/public/naver'
pub = json.load(open('published.json', encoding='utf-8')); reg = json.load(open('pages.json', encoding='utf-8'))
os.makedirs(SITE + '/img', exist_ok=True); rows = []
for k, v in pub.items():
    if k.startswith('n') and int(k[1:]) >= 26: continue          # n26~ 는 아직 예약 전이라 원고 목록에서 올린다(10/3 n34~n46이 추가돼 범위를 넓힘)
    if not os.path.exists(f'img/sq_{k}.jpg'): continue
    t = (reg.get(k, {}).get('dt') or '')[11:16] or v.get('time') or '12:00'
    rows.append((v['date'] + 'T' + t, k, v['title'])); shutil.copy(f'img/sq_{k}.jpg', f'{SITE}/img/sq_{k}.jpg')
for i in range(26, 34):
    if os.path.exists(f'img/sq_n{i}.jpg'): shutil.copy(f'img/sq_n{i}.jpg', f'{SITE}/img/sq_n{i}.jpg')
rows.sort()
FULL = {k: v['title'] for k, v in pub.items()}
URLS = {k: v.get('url') for k, v in pub.items() if v.get('url')}
def cur_phrase(k):
    m = re.findall(r'<p><b>👇[^<]*</b></p>', (reg.get(k) or {}).get('body', '')); return m[-1][8:-8] if m else ''
with zipfile.ZipFile(SITE + '/sq_all.zip', 'w', zipfile.ZIP_STORED) as z:
    for dt, k, t in rows: z.write(f'img/sq_{k}.jpg', f'{dt[5:10].replace("-","")}_{k}.jpg')
REWRITTEN = {f"n{i}" for i in range(16, 26)}   # 10/3 새로 쓴 본문(문장 겹침 42~48% -> 2%). n26~n33은 아직 예약 전이라 원고 목록에서 올린다
def body_btn(k):
    if k not in REWRITTEN: return ""
    return f'<a href="/naver/{k}.html"><button style="background:#e3b873">새 본문 열기 · 복사</button></a>'
def link_box(k):
    if k in LP.REL_FIX:
        t, ph = LP.REL_FIX[k]; ready = LP.POST_DT[t]; u = URLS.get(t, "")
        cp = cur_phrase(k)
        return (f'<div class="lk" data-ready="{ready}"><p class="lab2">함께 볼 글 바꾸기 <span class="rd"></span></p>'
                + (f'<p class="old">지금 들어 있는 문구: {html.escape(cp)}</p>' if cp else '<p class="old">지금 들어 있는 문구·링크 카드는 지우고 새로 넣어요.</p>')
                + f'<p class="val sm" id="p_{k}">👇 {html.escape(ph)}</p><button onclick="cp(\'p_{k}\',this)">유도 문구 복사(굵게)</button>'
                + f'<p class="val sm" id="g_{k}">{html.escape(FULL.get(t) or LP.TITLE.get(t, t))}</p><button onclick="cp(\'g_{k}\',this)">연결할 글 제목 복사</button>'
                + (f'<p class="val sm" id="u_{k}">{html.escape(u)}</p><button onclick="cp(\'u_{k}\',this)">주소 복사</button>' if u else '<p class="hint">주소는 네이버 글 관리에서 그 글 → 공유 → URL 복사. 문구 아래 줄에 붙이고 엔터 → 링크 카드.</p>')
                + f'<p class="hint">연결할 글 발행: {LP.fmt(ready)}</p>'
                + '</div>')
    if k in LP.FIX_KEEP: return '<div class="lk keep"><p class="old">함께 볼 글은 그대로 두세요(주제가 맞아요).</p></div>'
    return ''
items = ''.join(f'''<div class="box" data-dt="{dt}" id="b_{k}"><p class="lab"><span class="st"></span> {int(dt[5:7])}월 {int(dt[8:10])}일</p>
<img src="/naver/img/sq_{k}.jpg?v=3" alt=""><p class="val" id="t_{k}">{html.escape(t)}</p>
<div class="btns"><a href="/naver/img/sq_{k}.jpg?v=3" download="{dt[5:10].replace("-","")}_{k}.jpg"><button>이미지 저장</button></a><button onclick="cp('t_{k}',this)">제목 복사</button>{body_btn(k)}</div>{link_box(k)}</div>''' for dt, k, t in rows)
page = f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>예약 글 수정 작업판</title><style>
body{{margin:0;background:#f4f1ea;color:#222;font:18.5px/1.65 -apple-system,"Apple SD Gothic Neo","Noto Sans KR",sans-serif}}@media(min-width:760px){{body{{font-size:20px}}}}
.wrap{{max-width:760px;margin:0 auto;padding:20px 16px 80px}}h1{{text-align:center;font-size:28px;margin:8px 0}}.box{{background:#fff;border:1px solid #ddd;border-radius:14px;padding:14px 16px;margin:0 0 14px}}
.box img{{width:100%;max-width:420px;display:block;margin:6px auto;border-radius:10px}}.lab{{font-size:16px;color:#8a6d3b;font-weight:700;margin:0}}.val{{margin:6px 0 0;font-weight:700}}
button{{font:inherit;font-weight:700;font-size:19px;border:0;border-radius:12px;padding:12px 16px;background:#c4a062;color:#111;cursor:pointer;margin:8px 8px 0 0}}.btns{{text-align:center}}button.big{{width:100%;padding:16px;font-size:21px;margin:8px 0}}
.ok{{background:#7fb07a}}.done{{opacity:.45}}.st{{display:inline-block;padding:2px 10px;border-radius:99px;font-size:15px;background:#eee;color:#444}}.st.p{{background:#d9ecd6}}.st.s{{background:#f6e7c4}}
.note{{background:#fff8e6;border:1px solid #e6d3a0}}.lk{{border-top:1px dashed #ccc;margin-top:12px;padding-top:8px}}.lk.keep{{opacity:.6}}.lab2{{font-weight:700;color:#8a6d3b;margin:4px 0}}.sm{{font-size:17px;font-weight:600}}.old{{font-size:15px;color:#777;margin:4px 0}}.hint{{font-size:15px;color:#777;margin:4px 0}}.rd{{font-size:14px;padding:2px 8px;border-radius:99px;background:#eee}}.rd.on{{background:#d9ecd6}}.rd.wait{{background:#f6e7c4}}.lk.done{{opacity:.5}}ol{{padding-left:22px}}li{{margin:6px 0}}.c{{text-align:center}}</style></head><body><div class="wrap">
<h1>예약 글 수정 작업판</h1><p class="c">글 하나를 열 때 대표 이미지와<br>함께 볼 글을 같이 바꿔요.</p>
<div class="box note"><p class="lab">교체 방법 (글 하나에 1분)</p><ol><li>아래 <b>이미지 저장</b>을 누릅니다.</li><li>네이버에서 그 글의 <b>수정</b>을 엽니다. 제목은 <b>제목 복사</b>로 찾으면 돼요.</li><li>본문 맨 위 사진을 지우고, 새 사진을 맨 위에 올립니다. 맨 위 사진이 대표 이미지가 돼요.</li><li>함께 볼 글 칸이 있으면: 본문 맨 아래의 옛 문구와 링크 카드를 지우고, 새 문구를 붙인 뒤 아래 줄에 글 주소를 붙입니다. 엔터를 치면 링크 카드가 생겨요.</li><li><b>새 본문 열기 · 복사</b>가 있는 글(n16~n25)은 본문이 새로 바뀌었어요. 버튼을 눌러 열고 \"본문 전체 복사\"를 누른 뒤, 네이버 수정 화면에서 <b>맨 위 대표 사진은 그대로 두고 그 아래 본문 전체를 지운 다음</b> 붙여 넣어요. 연결 문구와 CTA 배너까지 한 번에 바뀌니 함께 볼 글 칸의 문구·링크는 따로 바꾸지 않아도 돼요(주소 카드만 문구 아래에 붙입니다).</li><li>저장합니다(예약 글은 예약 시각 그대로 두세요).</li></ol><p class="hint">연결할 글이 아직 발행 전이면(칸에 "이후"가 보여요) 그 글이 발행된 뒤에 링크만 따로 바꿔요. 예약만 걸린 글은 주소가 없어요.</p></div>
<a href="/naver/sq_all.zip"><button class="big">전체 이미지 한 번에 저장 (zip)</button></a>
{items}
<div class="box"><p class="lab">앞으로 올릴 글 (n26~n33)</p><p class="val" style="font-weight:400">이 글들은 원고 페이지에 새 이미지가 이미 들어 있어요.<br>원고 목록에서 올리면 됩니다.</p><a href="/naver/"><button>원고 목록 열기</button></a></div>
</div><script>
function cp(id,b){{navigator.clipboard.writeText(document.getElementById(id).innerText).then(function(){{b.textContent="복사됨";b.className="ok"}})}}
function paint(){{var now=new Date(new Date().toLocaleString("en-US",{{timeZone:"Asia/Seoul"}}));
document.querySelectorAll(".box[data-dt]").forEach(function(bx){{var dt=new Date(bx.dataset.dt+":00"),st=bx.querySelector(".st");
 if(dt<=now){{st.textContent="발행됨";st.className="st p"}}else{{st.textContent="예약 중";st.className="st s"}}
}});
document.querySelectorAll('.lk[data-ready]').forEach(function(x){{var r=new Date(x.dataset.ready+':00+09:00'),rd=x.querySelector('.rd'),on=new Date()>=r;rd.textContent=on?'지금 가능':'연결 글 발행 후';rd.className='rd '+(on?'on':'wait');}});
}}
paint();</script></body></html>'''
open(SITE + '/daepyo.html', 'w', encoding='utf-8').write(page); print('swap page', len(rows))
