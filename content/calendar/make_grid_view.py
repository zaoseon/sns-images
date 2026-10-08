import json,html,collections,datetime as D
E=html.escape
g=json.load(open('/home/claude/grid/grid_2026-11.json',encoding='utf-8')); rep=g['report']; SETS=g['SETS']
FN={'v1_lowbun':'낮은 묶음','v2_straight':'생머리','v3_ponytail':'포니테일','v4_glasses':'안경','v5_halfup_v2':'반 올림','v13_horn_glasses':'뿔테','v8_gesture':'손짓'}
ELC={'불':'#fbe7de','물':'#dee8f4','흙':'#f4ecdc','나무':'#e2f0e2','쇠':'#f6f3ec'}
def md(s): d=D.date.fromisoformat(s); return f"{d.month}/{d.day}"
cells=""
for x in g['ig'][::-1]:
    lab=f"{md(x['date'])} {'아침' if x['slot']=='P08' else '밤'}"
    if x['locked']: cells+=f'<div class="t lock"><b>{lab}</b><span>이미 예약</span><small>표지 확인 필요</small></div>'
    else:
        name,tone,bg,ac=SETS[x['set']]; inner=(f'<i class="face">{E(FN[x["face"]])}</i>' if x['face'] else f'<em>{E(x["kind"])}</em>')
        cells+=f'<div class="t" style="background:{bg}"><b style="color:{ac}">{lab}</b>{inner}<u style="background:{ac}"></u><small>{E(name)}·{E(tone)}</small></div>'
bc=""
for b in g['blog'][::-1]:
    lab=f"{md(b['date'])} {'낮' if b['time']<'16' else '밤'}"; el=b['el'] or '흙'; dark=b['dark']; bgc='#18161e' if dark else ELC[el]; fg='#f4eee2' if dark else '#26201c'
    face=(f'<i class="face sm">{E(FN[b["face"]])}</i>' if b['face'] else '<i class="face sm q">?</i>')
    bc+=f'<div class="s" style="background:{bgc};color:{fg}"><b>{lab}</b><span>{el}{" · 어두운 판" if dark else ""}</span>{face}<small>{"이미 정해짐" if b["locked"] else "새 글"}</small></div>'
wk=collections.defaultdict(list)
for r in g['reels']:
    if r['locked']: continue
    wk[(D.date.fromisoformat(r['date'])-D.date(2026,11,1)).days//7].append(r)
WN=["11/1~7","11/8~14","11/15~21","11/22~28","11/29~30"]; rr=""
for w in sorted(wk):
    items="".join(f'<li><b>{md(r["date"])} {"낮" if r["slot"] in("R08","R12") else "저녁"}</b> {E(r["title"])}<br><span class="c1">장면 {E(r["scene"])}</span><span class="c2">마무리 {E(r["ending"])}</span>{("<span class=c3>정월 "+E(FN[r["face"]])+"</span>") if r["face"] else ""}</li>' for r in wk[w])
    rr+=f'<details class="g"><summary><b>{WN[w]}</b> <small>새 릴스 {len(wk[w])}편</small></summary><ul>{items}</ul></details>'
page=open('/home/claude/grid/grid_template.html',encoding='utf-8').read().replace('@@CELLS@@',cells).replace('@@BLOG@@',bc).replace('@@REELS@@',rr).replace('@@IGNEW@@',str(rep['ig_new'])).replace('@@IGFACE@@',str(rep['ig_face_new'])).replace('@@BNEW@@',str(rep['blog_new'])).replace('@@BDARK@@',str(rep['blog_new_dark'])).replace('@@RNEW@@',str(rep['reel_new'])).replace('@@RFACE@@',str(rep['reel_face']))
open('/mnt/user-data/outputs/zaoseon_grid_2026-11.html','w',encoding='utf-8').write(page); print(len(page)//1024,'KB')
