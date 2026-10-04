"""확인용 페이지 생성(휴대폰에서 바로 넘겨 보고 재생 + 항목마다 피드백 저장). 결과: /mnt/user-data/outputs/자오선_콘텐츠_확인.html
피드백은 아티팩트 db(feedback/<id>)에 저장된다. Claude는 Artifact read_db 로 읽는다.
게시: Artifact publish (capabilities: {db:{}, user:{}}), 같은 url 로 갱신."""
import base64, io, os, subprocess, datetime as D
from PIL import Image
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
TMP = "/tmp/gal"; os.makedirs(TMP, exist_ok=True)
def jb64(path, size, q=78):
    im = Image.open(path).convert("RGB").resize(size, Image.LANCZOS); b = io.BytesIO(); im.save(b, "JPEG", quality=q)
    return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()
def vb64(p): return "data:video/mp4;base64," + base64.b64encode(open(p, "rb").read()).decode()
def reel_small(d):
    out = f"{TMP}/v2-{d}.mp4"
    if not os.path.exists(out):
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", f"{R}/2026-w40car3-reel/v2/{d}.mp4", "-vf", "scale=540:960", "-c:v", "libx264", "-crf", "30", "-preset", "veryfast", "-c:a", "aac", "-b:a", "64k", "-movflags", "+faststart", out], check=True)
    return out
W = "월화수목금토일"
CAR = {"1002": "정(丁)", "1003": "무(戊)", "1004": "기(己)", "1006": "경(庚)", "1007": "신(辛)", "1008": "임(壬)", "1009": "계(癸)"}
REEL = {"02": "정(丁) 일간 릴스", "03": "사주·별자리·숫자 #1 헤어진 뒤 다시 연락하는 사람", "04": "기(己) 일간 릴스", "05": "사주·별자리·숫자 #2 돈이 모이는 사람", "06": "경(庚) 일간 릴스",
        "07": "신(辛) 일간 릴스", "08": "임(壬) 일간 릴스", "09": "계(癸) 일간 릴스", "10": "사주·별자리·숫자 #3 빨리 달아오르고 빨리 식는 사람", "11": "사주·별자리·숫자 #4 일단 하자 vs 한 번 더 생각하자"}

def fb(id_, label):
    return (f'<div class="fb" data-id="{id_}" data-label="{label}"><div class="btns">'
            '<button data-s="good">👍 좋아요</button><button data-s="fix">✏️ 수정해 주세요</button><button data-s="redo">❌ 다시 만들어 주세요</button></div>'
            '<textarea placeholder="의견을 적어 주세요 (예: 3번 슬라이드 제목이 너무 길어요)"></textarea>'
            '<div class="row"><button class="save">의견 저장</button><span class="st"></span></div></div>')

def build():
    cmp = []
    for i in range(1, 8):
        s = jb64(f"{R}/samples/carousel_2026-10-01/정-{i}.png", (360, 450), 76); m = jb64(f"{R}/2026-w40car3/1002_{i}.jpg", (360, 450), 76)
        cmp.append(f'<div class="pair"><figure><img src="{s}" alt=""><figcaption>샘플 정-{i}</figcaption></figure><figure><img src="{m}" alt=""><figcaption>내가 만든 것</figcaption></figure></div>')
    days = []
    for dn in range(2, 12):
        dt = D.date(2026, 10, dn); key = f"10{dn:02d}"; d = f"2026-10-{dn:02d}"
        b = f'<section class="day"><h2>10/{dn}({W[dt.weekday()]})</h2>'
        if key in CAR:
            imgs = "".join(f'<img loading="lazy" src="{jb64(f"{R}/2026-w40car3/{key}_{i}.jpg", (540, 675), 80)}" alt="슬라이드 {i}">' for i in range(1, 8))
            b += f'<h3>08:00 인스타 캐러셀 · {CAR[key]}일생 <span>옆으로 넘겨 보세요</span></h3><div class="scroller">{imgs}</div>' + fb(f"car-{key}", f"10/{dn} 캐러셀 {CAR[key]}")
        else:
            b += "<h3>08:00 인스타 · 기존 글(캐러셀 아님)</h3>"
        b += f'<h3>12:00 인스타 릴스 · {REEL[f"{dn:02d}"]}</h3><video controls playsinline preload="metadata" src="{vb64(reel_small(d))}"></video>' + fb(f"reel-{key}", f"10/{dn} 릴스 {REEL[f'{dn:02d}']}") + "</section>"
        days.append(b)
    mix = """<details open><summary>섞기 계획 (표지·본문·CTA 구성을 세트마다 다르게)</summary>
<p>지금 7세트는 구성이 모두 같아요(표지·본문·차트·조언·CTA가 전부 정 샘플 한 가지). 대표님 샘플 두 가지(병, 정)를 보면 이미 구성이 달라요.</p>
<ul>
<li><b>표지</b> - 정: 부제가 제목 위, 얼굴 오른쪽 아래, 패널 없음, AI 문구 포함 / 병: 제목이 아래 패널 안, 부제는 제목 아래, 얼굴 위쪽 크게</li>
<li><b>본문(성격·연애·돈)</b> - 정: 배지가 제목 위 y=327~350, 우주 배경 밴드 216~1132 / 병: 배지 y=278, 제목·본문이 더 위에서 시작, 밴드가 더 위(155~1095)</li>
<li><b>오행 차트</b> - 정: 음양 이미지 배경 / 병: 배경 없음(검정)</li>
<li><b>조언</b> - 정: 얼굴 위쪽 + 어두운 패널 / 병: 우주 배경(얼굴 없음)</li>
<li><b>CTA</b> - 병·정 모두 우주 배경 밴드. 버튼 문구와 위치가 조금 달라요</li>
</ul>
<p>내일 대표님이 만들어 주실 샘플이 오면 표지·본문·CTA마다 <b>변형 A/B/C</b>로 저장해 두고, 세트마다 섞어서 배정할게요. 요일별 콘텐츠 형식을 섞자는 뜻이 아니었던 점, 제가 잘못 이해했어요.</p>""" + fb("mix", "섞기 계획") + "</details>"
    ny = "".join(f'<img loading="lazy" src="{jb64(f"{R}/2026-w40car3/ny_{i}.jpg", (540, 675), 80)}" alt="홍보 {i}">' for i in range(1, 6))
    by = "".join(f'<img loading="lazy" src="{jb64(f"{R}/2026-w40car3/byeong_{i}.jpg", (540, 675), 80)}" alt="병 {i}">' for i in range(1, 8))
    today = ('<details open><summary>내일(10/2) 저녁 예약 2건 - 먼저 확인해 주세요</summary>'
             '<h3>18:30 2027 신년 감정서 얼리버드 (샘플 방식으로 새로 만든 5장)</h3><div class="scroller">' + ny + '</div>' + fb("promo-ny", "10/2 18:30 감정서 홍보") +
             '<h3>19:00 병(丙) 캐러셀 재게시 (대표님 샘플 7장 그대로)</h3><div class="scroller">' + by + '</div>' + fb("byeong-repost", "10/2 19:00 병 재게시") + '</details>')
    v2 = ('<details open><summary>새 릴스 시안 (10/2 정 · 소리 켜고 보세요)</summary>'
          '<p>대표님이 주신 7가지 기준에 맞춘 시안이에요. 컷을 박자에 맞춰 바로 넘기고, 조언(반전) 장면을 뒤쪽에 두고, 마지막에 다음 편 예고를 넣었어요. 음악은 제가 직접 만든 곡이라 저작권 문제가 없어요(13초).</p>'
          '<video controls playsinline preload="metadata" src="' + vb64("/tmp/gal/v2-1002.mp4") + '"></video>' + fb("reel-v2", "새 릴스 시안(음악 포함)") + '</details>')
    overall = '<details><summary>전체 의견 · 만들고 싶은 형식 메모</summary>' + fb("overall", "전체 의견") + "</details>"
    css = """:root{--bg:#f6f3ee;--fg:#1c1a18;--card:#fff;--line:#ddd5c8;--acc:#c4501f;--mut:#8a8176;box-sizing:border-box;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#171513;--fg:#eee8df;--card:#211e1b;--line:#38332d;--acc:#f0825a}}
:root[data-theme="dark"]{--bg:#171513;--fg:#eee8df;--card:#211e1b;--line:#38332d;--acc:#f0825a}
html,body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.6 -apple-system,"Apple SD Gothic Neo","Noto Sans KR",sans-serif}
main{max-width:760px;margin:0 auto;padding:16px 14px 60px}h1{font-size:22px;margin:8px 0 4px}.sub{color:var(--mut);font-size:14px;margin:0 0 16px}
.note{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px 14px;margin:0 0 18px;font-size:15px}
section.day{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:12px 12px 16px;margin:0 0 16px}
h2{font-size:20px;margin:0 0 6px;color:var(--acc)}h3{font-size:15px;margin:14px 0 8px}h3 span{font-weight:400;color:var(--mut);font-size:13px}
.scroller{display:flex;gap:8px;overflow-x:auto;scroll-snap-type:x mandatory;padding-bottom:6px;-webkit-overflow-scrolling:touch}
.scroller img{width:78%;max-width:340px;flex:0 0 auto;scroll-snap-align:start;border-radius:8px;border:1px solid var(--line)}
video{width:100%;max-width:300px;display:block;margin:0 auto;border-radius:10px;background:#000}
.cmp{display:flex;flex-direction:column;gap:10px}.pair{display:flex;gap:8px}.pair figure{margin:0;flex:1}.pair img{width:100%;border-radius:6px;display:block}figcaption{font-size:12px;color:var(--mut);text-align:center}
details{margin:0 0 18px;background:var(--card);border:1px solid var(--line);border-radius:12px;padding:10px 14px}summary{font-weight:700;cursor:pointer}
.fb{margin:10px 0 2px;padding-top:8px;border-top:1px dashed var(--line)}.btns{display:flex;gap:6px;flex-wrap:wrap}
.fb button{font:inherit;font-size:14px;border:1px solid var(--line);background:transparent;color:var(--fg);border-radius:999px;padding:6px 12px}
.fb button.on{background:var(--acc);border-color:var(--acc);color:#fff}
.fb textarea{width:100%;box-sizing:border-box;min-height:56px;margin-top:8px;border:1px solid var(--line);border-radius:8px;background:transparent;color:var(--fg);font:inherit;font-size:15px;padding:8px}
.fb .row{display:flex;align-items:center;gap:10px;margin-top:6px}.st{font-size:13px;color:var(--mut)}
body.nodb .fb{display:none}.nodbmsg{display:none}body.nodb .nodbmsg{display:block}"""
    js = """
(function(){
  var db=null, saved={};
  function q(c){return Array.prototype.slice.call(document.querySelectorAll(c));}
  function paint(box,v){ if(!v) return; q('[data-id="'+box+'"] .btns button').forEach(function(b){b.classList.toggle('on', b.getAttribute('data-s')===v.status);});
    var t=document.querySelector('[data-id="'+box+'"] textarea'); if(t && document.activeElement!==t && v.note!==undefined) t.value=v.note;
    var st=document.querySelector('[data-id="'+box+'"] .st'); if(st) st.textContent=v.at?('저장됨 '+v.at.slice(5,16).replace('T',' ')):''; }
  function save(box){
    var el=document.querySelector('[data-id="'+box+'"]'); var on=el.querySelector('.btns button.on');
    var body={id:box,label:el.getAttribute('data-label'),status:on?on.getAttribute('data-s'):'',note:el.querySelector('textarea').value,at:new Date().toISOString()};
    var st=el.querySelector('.st'); st.textContent='저장 중...';
    db.doc('feedback/'+box).set(body).then(function(){ st.textContent='저장됨'; }).catch(function(e){ st.textContent='저장 실패('+(e&&e.code||'오류')+'). 대화로 의견을 남겨 주세요.'; });
  }
  q('.fb').forEach(function(el){ var id=el.getAttribute('data-id');
    el.querySelectorAll('.btns button').forEach(function(b){ b.addEventListener('click',function(){ el.querySelectorAll('.btns button').forEach(function(x){x.classList.remove('on');}); b.classList.add('on'); if(db) save(id); }); });
    el.querySelector('.save').addEventListener('click',function(){ if(db) save(id); }); });
  document.body.classList.add('nodb');
  claude.use('db').then(function(d){ if(!d) return; db=d; document.body.classList.remove('nodb');
    db.collection('feedback').onSnapshot(function(snap){ snap.docs.forEach(function(x){ var v=x.data(); if(v) paint(x.id,v); }); }, function(){});
  }).catch(function(){});
})();"""
    return f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"><title>자오선 콘텐츠 확인 (10/2~10/11)</title><style>{css}</style></head><body><main>
<h1>자오선 콘텐츠 확인</h1><p class="sub">10/2~10/11 · 인스타 캐러셀(아침 8시)과 릴스(낮 12시)</p>
<p class="note">넘겨 보고, 재생해 보고, 항목마다 <b>👍 / ✏️ / ❌</b>를 누른 뒤 의견을 적어 주세요. 제가 이 페이지에서 바로 읽고 고칠게요. 릴스는 확인용으로 화질을 낮췄어요. 음악이 들어 있으니 소리를 켜고 보세요.</p>
<p class="note nodbmsg">지금 화면에서는 의견을 저장할 수 없어요. 이 대화에 적어 주세요.</p>
{v2}{today}{mix}{overall}
<details><summary>샘플과 비교 (정 세트: 왼쪽 대표님 샘플, 오른쪽 제가 만든 것)</summary><div class="cmp">{"".join(cmp)}</div></details>
{"".join(days)}
</main><script>{js}</script></body></html>'''

if __name__ == "__main__":
    html = build(); out = "/mnt/user-data/outputs/자오선_콘텐츠_확인.html"; open(out, "w", encoding="utf-8").write(html); print(round(len(html) / 1e6, 1), "MB")
