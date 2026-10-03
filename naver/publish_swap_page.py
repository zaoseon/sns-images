"""교체 작업판(zaoseon-site public/naver/daepyo.html) + 전체 zip 다시 만들기. 사용: python3 publish_swap_page.py"""
import json, os, shutil, zipfile, html
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
SITE = '/home/claude/zaoseon-site/public/naver'
pub = json.load(open('published.json', encoding='utf-8')); reg = json.load(open('pages.json', encoding='utf-8'))
os.makedirs(SITE + '/img', exist_ok=True); rows = []
for k, v in pub.items():
    if k in [f'n{i}' for i in range(26, 34)]: continue
    t = (reg.get(k, {}).get('dt') or '')[11:16] or v.get('time') or '12:00'
    rows.append((v['date'] + 'T' + t, k, v['title'])); shutil.copy(f'img/sq_{k}.jpg', f'{SITE}/img/sq_{k}.jpg')
for i in range(26, 34): shutil.copy(f'img/sq_n{i}.jpg', f'{SITE}/img/sq_n{i}.jpg')
rows.sort()
with zipfile.ZipFile(SITE + '/sq_all.zip', 'w', zipfile.ZIP_STORED) as z:
    for dt, k, t in rows: z.write(f'img/sq_{k}.jpg', f'{dt[5:10].replace("-","")}_{k}.jpg')
items = ''.join(f'''<div class="box" data-dt="{dt}" id="b_{k}"><p class="lab"><span class="st"></span> {int(dt[5:7])}월 {int(dt[8:10])}일</p>
<img src="/naver/img/sq_{k}.jpg?v=3" alt=""><p class="val" id="t_{k}">{html.escape(t)}</p>
<div class="btns"><a href="/naver/img/sq_{k}.jpg?v=3" download="{dt[5:10].replace("-","")}_{k}.jpg"><button>이미지 저장</button></a><button onclick="cp('t_{k}',this)">제목 복사</button><button class="chk" data-k="{k}" onclick="ck(this)">교체 완료</button></div></div>''' for dt, k, t in rows)
page = f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>대표 이미지 교체 작업판</title><style>
body{{margin:0;background:#f4f1ea;color:#222;font:18.5px/1.65 -apple-system,"Apple SD Gothic Neo","Noto Sans KR",sans-serif}}@media(min-width:760px){{body{{font-size:20px}}}}
.wrap{{max-width:760px;margin:0 auto;padding:20px 16px 80px}}h1{{text-align:center;font-size:28px;margin:8px 0}}.box{{background:#fff;border:1px solid #ddd;border-radius:14px;padding:14px 16px;margin:0 0 14px}}
.box img{{width:100%;max-width:420px;display:block;margin:6px auto;border-radius:10px}}.lab{{font-size:16px;color:#8a6d3b;font-weight:700;margin:0}}.val{{margin:6px 0 0;font-weight:700}}
button{{font:inherit;font-weight:700;font-size:19px;border:0;border-radius:12px;padding:12px 16px;background:#c4a062;color:#111;cursor:pointer;margin:8px 8px 0 0}}.btns{{text-align:center}}button.big{{width:100%;padding:16px;font-size:21px;margin:8px 0}}
.ok{{background:#7fb07a}}.done{{opacity:.45}}.st{{display:inline-block;padding:2px 10px;border-radius:99px;font-size:15px;background:#eee;color:#444}}.st.p{{background:#d9ecd6}}.st.s{{background:#f6e7c4}}
.note{{background:#fff8e6;border:1px solid #e6d3a0}}ol{{padding-left:22px}}li{{margin:6px 0}}.c{{text-align:center}}</style></head><body><div class="wrap">
<h1>대표 이미지 교체 작업판</h1><p class="c">정사각 대표 이미지예요.<br>글자는 중앙에 크게 들어가 있어요.</p>
<div class="box note"><p class="lab">교체 방법 (글 하나에 1분)</p><ol><li>아래 <b>이미지 저장</b>을 누릅니다.</li><li>네이버에서 그 글의 <b>수정</b>을 엽니다. 제목은 <b>제목 복사</b>로 찾으면 돼요.</li><li>본문 맨 위 사진을 지우고, 새 사진을 맨 위에 올립니다. 맨 위 사진이 대표 이미지가 돼요.</li><li>저장(예약 글은 예약 시각 그대로)하고, 아래 <b>교체 완료</b>를 누릅니다.</li></ol></div>
<a href="/naver/sq_all.zip"><button class="big">전체 이미지 한 번에 저장 (zip)</button></a><p class="c" id="sum"></p>
{items}
<div class="box"><p class="lab">앞으로 올릴 글 (n26~n33)</p><p class="val" style="font-weight:400">이 글들은 원고 페이지에 새 이미지가 이미 들어 있어요.<br>원고 목록에서 올리면 됩니다.</p><a href="/naver/"><button>원고 목록 열기</button></a></div>
</div><script>
function cp(id,b){{navigator.clipboard.writeText(document.getElementById(id).innerText).then(function(){{b.textContent="복사됨";b.className="ok"}})}}
var K="zs_sq_done";function load(){{try{{return JSON.parse(localStorage.getItem(K)||"{{}}")}}catch(e){{return {{}}}}}}
function ck(b){{var d=load();d[b.dataset.k]=!d[b.dataset.k];try{{localStorage.setItem(K,JSON.stringify(d))}}catch(e){{}}paint()}}
function paint(){{var d=load(),n=0,now=new Date(new Date().toLocaleString("en-US",{{timeZone:"Asia/Seoul"}}));
document.querySelectorAll(".box[data-dt]").forEach(function(bx){{var k=bx.id.slice(2),dt=new Date(bx.dataset.dt+":00"),st=bx.querySelector(".st"),c=bx.querySelector(".chk");
 if(dt<=now){{st.textContent="발행됨";st.className="st p"}}else{{st.textContent="예약 중";st.className="st s"}}
 if(d[k]){{bx.classList.add("done");c.textContent="교체 완료 ✓";c.className="chk ok";n++}}else{{bx.classList.remove("done");c.textContent="교체 완료";c.className="chk"}}}});
document.getElementById("sum").textContent="교체 완료 "+n+" / {len(rows)}"}}
paint();</script></body></html>'''
open(SITE + '/daepyo.html', 'w', encoding='utf-8').write(page); print('swap page', len(rows))
