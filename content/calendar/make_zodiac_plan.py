"""띠 릴스 기획서 화면 + 캡션 초안 + 트렌디 목록 갱신(10/8). 사용: python3 content/calendar/make_zodiac_plan.py"""
import sys, importlib.util, json, html, io, base64, os
R = "/home/claude/repo"; sys.path.insert(0, R + "/pipeline"); sys.path.insert(0, R + "/content")
spec = importlib.util.spec_from_file_location("zz", R + "/content/clips_motion_zodiac.py"); Z = importlib.util.module_from_spec(spec); spec.loader.exec_module(Z)
import caption_rules as CR, clip_motion as CM
from PIL import Image
E = html.escape
ACT = {"원숭이띠": ("맡은 책임 하나를 확실히 끝내 보세요", "모든 일을 혼자 떠안지 마세요"), "개띠": ("올해 맺은 계약을 다시 읽어 보세요", "보증과 명의 빌려주기는 피하세요"), "용띠": ("올해 쌓을 것 하나를 정해 보세요", "남과 나를 비교하지 마세요"), "뱀띠": ("시작할 일 하나를 정해 끝까지 해 보세요", "화가 난 상태에서 결정하지 마세요"), "말띠": ("함께할 사람과 약속 하나를 맺어 보세요", "분위기에 취해 조건 확인을 건너뛰지 마세요"), "양띠": ("올해 정리할 것 세 가지를 적어 보세요", "무리하게 새 판을 벌이지 마세요"), "닭띠": ("내 실력을 보여 줄 기록을 남겨 보세요", "사소한 흠에 매달리지 마세요"), "돼지띠": ("도움 줄 사람 한 명에게 연락해 보세요", "좋은 말만 믿고 서두르지 마세요"), "쥐띠": ("중요한 약속은 글로 남겨 보세요", "가까운 사람과 돈거래는 피하세요")}
POL = {"원숭이띠": ("강점", "주의", "강점"), "개띠": ("강점", "강점", "주의"), "용띠": ("강점", "강점", "주의"), "뱀띠": ("주의", "강점", "강점"), "말띠": ("강점", "강점", "강점"), "양띠": ("주의", "강점", "강점"), "닭띠": ("강점", "강점", "주의"), "돼지띠": ("강점", "강점", "강점"), "쥐띠": ("강점", "강점", "주의")}
def josa(w): c = w.strip("'")[-1]; return "이에요" if (ord(c) - 0xAC00) % 28 else "예요"
def mstr(ms): return "·".join(("내년 1월" if m == 13 else f"{m}월") for m in ms)
raw = json.load(open("/home/claude/zaoseon-site/data/keywords/raw/tag_research_2026-10-07.json", encoding="utf-8"))
def vol(k): v = raw.get(k); return f"{v['합계']:,}" if v else "-"
TREND = {"용띠": ("무지출 챌린지", "널리 쓰는 말", "새는 곳을 막고 쌓는 해라는 풀이와 소비를 줄이는 유행의 방향이 같음", "무지출 챌린지 소개 글(마케팅 트렌드 용어), 트렌디 목록 2026-10"),
         "양띠": ("갓생", "널리 쓰는 말", "정리부터 하면 다시 서는 해라는 풀이와 부지런하게 사는 삶을 가리키는 말의 뜻이 맞음", "브라보 마이 라이프 요즘말 사전 '올해는 갓생 하게 살자고요?'(2026-02-23), 마케팅 용어 소개 글"),
         "닭띠": ("일잘러", "널리 쓰는 말", "실력으로 인정받는 해(꼼꼼함이 드러나는 해)와 '일 잘하는 사람'이라는 뜻이 맞음", "일상·직장에서 널리 쓰는 말(고구마팜 '일잘러 스킬셋' 분류 2026, 마케팅 용어 소개 글)")}
caps = {}; tails = CR.TAIL; follows = CR.FOLLOW
for k, n in enumerate(Z.GEN):
    T = Z.T[n]; P = Z.PLAN[n]; ag, asv = ACT[n]; one = f"'{T['one']}'" + josa(T["one"])
    first = f"2027년 {n} 운세, 한 줄로는 {one}."
    if P.get("sub"): first = f"# {P['term']}, {P['sub']}\n" + first
    body = f"힘 쓸 달은 {mstr(T['good'])}, 아낄 달은 {mstr(T['save'])}이에요.\n힘 쓸 달에는 {ag}. 아낄 달에는 {asv}."
    cap = first + "\n\n" + body + "\n\n" + P["lead"] + "\n" + tails[k % len(tails)] + "\n" + follows[k % len(follows)] + "\n\n이 내용은 재미로, 그리고 나를 돌아보는 계기로 봐 주세요.\n\n" + P["tags"]
    caps[n] = cap; assert CR.check(cap) == [], (n, CR.check(cap))
TL = json.load(open(R + "/content/trendy_lines.json", encoding="utf-8"))
for n in Z.GEN:
    P = Z.PLAN[n]; rid = P["rid"]
    if n in TREND:
        term, ty, fit, src = TREND[n]
        TL[rid] = dict(name=f"{n} 2027 운세 릴스", opener=f"# {term}, {P['sub']}", tags=["#" + term.replace(" ", "")], term=term, type=ty, fit=fit + ". 큰 제목이 아니라 표지의 배지(작은 글)와 캡션 첫 줄에 씀", source=src, review_by="2026-11-08", heavy=False, note="")
    else: TL[rid] = dict(name=f"{n} 2027 운세 릴스", opener="", tags=[], term="", type="", fit="", source="", review_by="", heavy=False, note="맥락에 안 맞거나 같은 말 반복이라 평이한 말로 둠")
json.dump(TL, open(R + "/content/trendy_lines.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
import trendy_audit as TA
o, nu, m, t = TA.run(); print("TRENDY", nu, m, o)
os.makedirs("/home/claude/covers", exist_ok=True)
for n in Z.GEN:
    CM.BG_VARIANT = Z.PLAN[n]["bg"]; CM.still(Z.scenes_of(n), 0, 2.4, f"/home/claude/covers/{n}.png")
def b64(n):
    im = Image.open(f"/home/claude/covers/{n}.png").convert("RGB").resize((216, 384)); b = io.BytesIO(); im.save(b, "JPEG", quality=84); return base64.b64encode(b.getvalue()).decode()
CSS = '''<style>
:root{--bg:#f4f5fa;--card:#fff;--ink:#1d2140;--mute:#5b6082;--acc:#f48c04;--blue:#4a63c9;--line:#dfe2ee;box-sizing:border-box;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}
@media(prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#161a33;--card:#1f2447;--ink:#f1f2fb;--mute:#aab0d6;--blue:#8fa2ff;--line:#343b6b}}
:root[data-theme="dark"]{--bg:#161a33;--card:#1f2447;--ink:#f1f2fb;--mute:#aab0d6;--blue:#8fa2ff;--line:#343b6b}
html{scroll-padding-top:env(safe-area-inset-top,0px)}*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:18px/1.6 'Noto Sans KR',sans-serif}
.w{max-width:760px;margin:0 auto;padding:18px 14px 70px}h1{font-size:24px;margin:6px 0}h2{font-size:21px;margin:30px 0 8px}h3{font-size:20px;margin:0 0 6px}
.lead{color:var(--mute);margin:0 0 10px;font-size:16px}.box{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px;margin:10px 0}
ul{list-style:none;margin:0;padding:0}li{padding:9px 0;border-bottom:1px solid var(--line);font-size:16px}li:last-child{border:0}small{color:var(--mute);font-size:14px}
details.g{background:var(--card);border:1px solid var(--line);border-radius:14px;margin:12px 0}details.g summary{padding:14px;cursor:pointer;list-style:none}details.g summary::-webkit-details-marker{display:none}details.g .in{padding:0 14px 14px}
.sn{display:flex;gap:10px;align-items:flex-start}.sn>b{flex:none;width:30px;height:30px;border-radius:50%;background:var(--blue);color:#fff;display:flex;align-items:center;justify-content:center;font-size:14px;margin-top:2px}.sn div{flex:1}
.tg{display:inline-block;font-size:13px;color:#fff;border-radius:10px;padding:1px 9px;margin:2px 6px 2px 0}.t1{background:var(--blue)}.t2{background:var(--acc)}.t3{background:#2e9e6b}.t4{background:#8a8fa8}
pre{white-space:pre-wrap;font:inherit;font-size:15px;background:rgba(0,0,0,.05);border-radius:10px;padding:10px;margin:6px 0}
.dec{border-left:6px solid var(--acc);padding-left:10px}
.cg{display:grid;grid-template-columns:repeat(3,1fr);gap:6px}.cg figure{margin:0}.cg img{width:100%;border-radius:8px;display:block}.cg figcaption{font-size:13px;color:var(--mute);text-align:center}
</style>'''
cards = ""
for k, n in enumerate(Z.GEN):
    T = Z.T[n]; P = Z.PLAN[n]; cf = Z.CFG[n]; sc = Z.scenes_of(n); dur = sum(x for x, _ in sc)
    def ln(s_): return E(s_.replace("\n", " / "))
    l1m, l2m = (Z.OVER.get(n, {}).get("money") or Z.two(T["money"])); l1w, l2w = Z.two(T["work"]); l1p, l2p = Z.two(T["people"])
    rows = [("표지(키워드)", (f"[배지] # {P['term']} / " if P.get("term") else "") + f"2027 {n} / {T['one']}" + (f" / {P['sub']}" if P.get("sub") else "")), ("출생연도", f"{n} 출생연도 / {cf['years']}"), ("문장", ln(cf["hook"])),
            ("왜 그럴까", f"{cf['l1']} / {cf['l2'].replace(chr(10), ' ')} (그림: {cf['shape']})"), ("힘 쓸 달·아낄 달", f"월 동그라미 12개 → '힘 쓸 달' 금색(살짝 커짐) {mstr(T['good'])} → '아낄 달' 붉은색(살짝 커짐) {mstr(T['save'])}"),
            ("돈", f"{l1m} / {l2m}"), ("일", f"{l1w} / {l2w}"), ("사람", f"{l1p} / {l2p}"), ("행운의 숫자", f"{cf['nums'][0]} · {cf['nums'][1]} / {ln(cf['lucky'])}"),
            ("마무리", ln(cf.get("q") or (cf.get("cm", "") + " / " + cf.get("big", ""))) + " → 팔로우하고 더 많은 이야기 나눠요 → 프로필 링크에서 생년월일 입력하고 내 첫글자와 타고난 기운 알아보기")]
    pol = POL[n]; st = sum(1 for x in pol if x == "강점"); ca = 3 - st
    tr = f"트렌디: <b>{P['term']}</b>({TREND[n][1]})를 표지 배지로 맨 위에, 캡션 첫 줄에도 씀" if n in TREND else "트렌디 표현: 쓰지 않음(맥락이 맞는 말이 없어 평이한 말)"
    scenes = "".join(f'<li class="sn"><b>{i + 1}</b><div><strong>{E(a)}</strong> <small>{sc[i][0]}초</small><br>{E(b)}</div></li>' for i, (a, b) in enumerate(rows))
    cards += f'''<details class="g"><summary><h3>{n} <small>{E(P['date'])} · 연결 글 {E(P['blog'])} · {dur:.1f}초</small></h3><span class="tg t1">강점 {st} : 주의 {ca}</span><span class="tg {'t2' if n in TREND else 't4'}">{'트렌디 표지' if n in TREND else '트렌디 안 씀'}</span><span class="tg t3">마무리 {E(cf['cta'])}</span><span class="tg t1" style="background:#6b5b95">배경 {E(Z.BG_KO[P['bg']])}</span></summary><div class="in"><p class="lead" style="margin:0 0 6px">{tr}</p><ul>{scenes}</ul><p class="lead" style="margin:10px 0 2px"><b>캡션 초안</b>(첫 125자에 '2027년 {n} 운세' 키워드, 유입 한 줄 + 팔로우 한 줄, 월 단위 행동은 캡션에 담음)</p><pre>{E(caps[n])}</pre><p class="lead" style="margin:0"><small>해시태그 검색량: #{n}운세 {vol(n + '운세')} · #정미년 {vol('정미년')} · #2027년운세 {vol('2027년운세')}</small></p></div></details>'''
covers = "".join(f'<figure><img src="data:image/jpeg;base64,{b64(n)}" alt="{n} 표지"><figcaption>{n} · {Z.BG_KO[Z.PLAN[n]["bg"]]}{" · # " + Z.PLAN[n]["term"] if n in TREND else ""}</figcaption></figure>' for n in Z.GEN)
guides = [("감정서 표현가이드 12가지", "그 사람만의 문장(띠 관계로 시작) · 행동 처방(돈·일·사람마다 행동 한 줄) · 강점 2 : 주의 1 표시 · 단정 완화('분명해요' → '기회가 보이는 해예요') · 존중하는 말투 · 시기는 월 단위+행동 하나(달력 장면은 지정하신 그림 그대로, 월별 행동은 캡션) · 반복 금지"), ("릴스 플레이북", "첫 프레임이 곧 제목 · 자막 필수 · 캡션 첫 125자에 '2027년 ○○띠 운세' · 해시태그 5개 · CTA 프로필 링크 1회"), ("통합 운영 매뉴얼", "확신·불안 문구 금지, 면책 1회(캡션 하단 현행 문구), 영상에 가격을 넣지 않음"), ("세계관·캐릭터 설정서", "담백한 존댓말, 약점은 짚되 대안과 함께, 1인칭 인간 서사 없음"), ("확정 규칙 R01~R33", "R33 사운드(경쾌·발랄·상큼, 템포 114 이상) · R13 문장 2초 · R17 캡션 · R19 양산형 방지 · R20 문구 안전 · R24·R25 트렌디(큰 제목은 평이하게, 트렌디는 작은 글, 한 영상 하나, 이웃 연속 금지, 한 주 40% 이하) · R26 자연스러운 한국어 · R27~R29 줄바꿈·박스·간격 · R30 한 장면 한 정보 · R31 강조 전환")]
snd = json.load(open('/home/claude/snd/info.json', encoding='utf-8'))
def a64(n): return base64.b64encode(open(f'/home/claude/snd/{n}.mp3','rb').read()).decode()
SNDH = "".join(f'<li><b>{n}</b> <small>{Z.PLAN[n]["date"]} · {snd[n]["style"]} · 템포 {snd[n]["bpm"]} · {snd[n]["key"]}장조</small><br><audio controls preload="none" style="width:100%"><source src="data:audio/mpeg;base64,{a64(n)}" type="audio/mpeg"></audio></li>' for n in Z.GEN)
gh = "".join(f"<li><b>{E(a)}</b><br><small>{E(b)}</small></li>" for a, b in guides)
tl = "".join(f"<li><b>{n}: {TREND[n][0]}</b> ({TREND[n][1]}, {Z.PLAN[n]['date']})<br><small>{E(TREND[n][2])}. 근거: {E(TREND[n][3])}. 점검일 11월 8일.</small></li>" for n in TREND)
page = f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"><title>띠 릴스 기획서</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap" rel="stylesheet">{CSS}</head><body><div class="w">
<h1>띠 릴스 기획서 (9편)</h1>
<p class="lead">영상을 만들기 전에 띠마다 장면 10개의 화면 문구, 캡션, 트렌디 표현을 정했어요. 아래 화면 문구가 그대로 영상에 들어가요. 띠를 눌러 펼쳐 보세요. 원숭이띠는 대표님이 지정하신 구성이 기준이에요.</p>
<h2>표지 미리보기 (첫 프레임이자 썸네일, 배경 5가지 돌려 쓰기)</h2>
<div class="box"><p class="lead" style="margin:0 0 8px">트렌디 표현은 표지 맨 위 주황 배지로 올려 눈에 띄게 했어요. 큰 제목은 평이한 키워드를 그대로 두고(R25), 배지 아래에 한 줄 풀이를 달았어요. 용·양·닭띠 3편이에요. 배경은 별빛 남색·달빛 보라·노을 버건디·숲 딥그린·청록 바다 5가지를 날짜 순서로 돌려 써서 이웃한 영상은 서로 달라요. 모두 어두운 톤이라 글자 대비는 11배 이상이고, 황도 차트는 그대로예요.</p><div class="cg">{covers}</div></div>
<h2>사운드 미리듣기 (14초)</h2><div class="box"><p class="lead" style="margin:0 0 8px">전부 경쾌하고 발랄하고 상큼한 곡이에요. 밝은 장조에 템포 114~124이고, 느린 곡(오르골·로파이)은 뺐어요. 이웃한 영상끼리 곡·조가 겹치지 않아요. 앞서 만든 영상 중 느린 곡(별빛 오르골 93 등)을 쓴 것은 다시 만들 때 모두 바뀌어요.</p><ul>{SNDH}</ul></div>
<div class="box"><b>이번 기획에 반영한 가이드</b><ul>{gh}</ul></div>
<div class="box dec"><b>정해 주세요 (2건, 모두 권장안이 있어요)</b><ul>
<li><b>영상 길이 약 34초</b><br><small>권장: 띠 릴스는 35초까지 허용해요. 지정하신 장면 10개를 문장 2초 이상(R13)으로 만들면 이만큼 나와요.</small></li>
<li><b>달력 장면에 월별 행동 한 줄을 넣을까요?</b><br><small>권장: 넣지 않아요. 달력 장면은 지정하신 그림만 두고 월별 행동(표현가이드 6번)은 캡션에 담았어요.</small></li></ul></div>
<h2>띠별 기획</h2>{cards}
<h2>트렌디 표현 검토 (R24·R25)</h2><div class="box"><ul>{tl}<li>세 영상은 앞뒤 릴스(다른 영상 포함)와 이웃해 연속 쓰이지 않고(원숭이띠는 다음 날 갑목 영상이 이미 트렌디 표현을 써서 뺐어요)(10/29, 11/7, 11/12), 한 영상에 하나씩, 9편 중 3편(33%)이라 한 주 40% 이하예요. 나머지 6편은 맥락이 맞는 말이 없어서 평이한 말로 뒀어요. 표지 배지는 큰 제목이 아니라 작은 글이라 R25를 지켜요.</li></ul></div>
<h2>다음 순서</h2><div class="box"><ul><li>대표님이 확인해 주시면 9편을 이 문구대로 다시 만들어요. 이미 만든 말·양·닭띠 영상은 문장 장면과 표지가 달라져서 다시 만들어요.</li><li>만든 뒤 장면 프레임과 자동 검사를 모두 통과시켜서 앱에 "대기"로 올려요. 메트리쿨은 확인 뒤에 같은 칸에 덮어써요.</li></ul></div>
</div></body></html>'''
open("/mnt/user-data/outputs/zaoseon_zodiac_plan.html", "w", encoding="utf-8").write(page)
json.dump(dict(caps=caps), open(R + "/content/calendar/zodiac_plan_captions.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("page", len(page) // 1024, "KB")
