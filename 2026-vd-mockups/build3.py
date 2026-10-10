# 자오선 비주얼 방향 3안 시안 v3 (2026-10-10). v2는 좌표를 눈대중으로 정해 R21·R29 간격을 어겼다.
# v3는 pipeline/template_engine.Page(채널 지오메트리·안전영역 검증)로 만들고, 세로 배치는 높이를 더해 계산한다.
# 배치 기준: 묶음은 상단 문구 아래(y108)+75=183 ~ 주소 위(y1340)-75=1265 안, 가운데 y724. 글 덩어리 사이 40px 이상, 그림·박스와 글 사이 60px 이상.
import sys, os, asyncio, base64, io
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..', 'pipeline'))
import template_engine as TE
from template_engine import Page, font, wrap, K, BF
import card_kit as CK
from style_spec import check_page
from PIL import Image
GOLD = '#f6b042'; INK = '#111'; PANEL_C = '#181615'
TOP, BOT = 183, 1265; CEN = (TOP + BOT) / 2; X0, W = 90, 900
TP, BP = K.P['pl_blk'], K.P['pr_xb']
def strip(s): return s.replace('[[', '').replace(']]', '')
def mark(s): return s.replace('[[', f'<span style="color:{GOLD}">').replace(']]', '</span>')
def lines_of(txt, path, size, w, p, name):
    f = font(path, size); ls = wrap(strip(txt), f, w)
    if max(f.getlength(l) for l in ls) > w + 1: p.problems.append(f'{name} 글자가 칸({w}px)보다 넓음')
    return ls
def T(p, txt, size, color='#fff', role='title', lh=1.3, align='left', w=W, name='글', x=None):
    X = X0 if x is None else x
    path = TP if role == 'title' else BP; ls = lines_of(txt, path, size, w, p, name); h = len(ls) * size * lh
    # 표시 줄은 명시한 줄바꿈을 그대로 쓰되, 자동으로 나눈 경우도 같은 줄로 맞춘다
    shown = txt if len(ls) == len(txt.split('\n')) else None
    def draw(top):
        body = mark(shown) if shown else '\n'.join(ls)
        fam = K.D if role == 'title' else K.B; wt = 900 if role == 'title' else 800
        p.add(name, (X, top, X + w, top + h), f'<div style="position:absolute;left:{X}px;top:{top:.0f}px;width:{w}px;text-align:{align};font-family:{fam};font-weight:{wt};font-size:{size}px;line-height:{lh};color:{color};white-space:pre-line">{body}</div>')
    return dict(h=h, kind='text', draw=draw)
def PILL(p, txt, size=44, w=None, align='left', bg=GOLD, fg=INK, name='알약'):
    ls = txt.split('\n'); f = font(BP, size); tw = max(f.getlength(l) for l in ls); h = len(ls) * size * 1.5 + 40; ww = w or tw + 84; x = X0 if align == 'left' else X0 + (W - ww) / 2
    def draw(top):
        p.add(name, (x, top, x + ww, top + h), f'<div style="position:absolute;left:{x:.0f}px;top:{top:.0f}px;width:{ww:.0f}px;height:{h:.0f}px;box-sizing:border-box;background:{bg};color:{fg};border-radius:{min(h/2,60):.0f}px;display:flex;align-items:center;justify-content:center;text-align:center;font-family:{K.B};font-weight:800;font-size:{size}px;line-height:1.5;white-space:pre-line">{txt}</div>')
    return dict(h=h, kind='box', draw=draw)
def BUBBLE(p, txt, w=900, x=X0, size=56, name='말풍선', tail='left', badge=None):
    """엔진 R10 말풍선 모양: 남색 바탕 + 금 테두리 + 금 꼬리, 글 흰색 가운데. badge는 말하는 사람 이름표(정월)."""
    ls = lines_of(txt, BP, size, w - 72, p, name); th = len(ls) * size * 1.5; h = th + 56; tail_h = 36; bd = 31 if badge else 0
    GL = TE.GOLD
    def draw(top):
        bt = top + bd; tx = x + 60 if tail == 'left' else x + w - 60 - 52
        html = (f'<div style="position:absolute;left:{x}px;top:{bt:.0f}px;width:{w}px;height:{h:.0f}px;box-sizing:border-box;background:linear-gradient(145deg,rgba(28,40,92,.95),rgba(9,14,44,.95));border:3px solid {GL};border-radius:36px;display:flex;align-items:center;justify-content:center;text-align:center;font-family:{K.B};font-weight:800;font-size:{size}px;line-height:1.5;color:#fff;white-space:pre-line;z-index:6">{chr(10).join(ls)}</div>'
                f'<div style="position:absolute;left:{tx}px;top:{bt+h-3:.0f}px;width:0;height:0;border-left:26px solid transparent;border-right:26px solid transparent;border-top:36px solid {GL};z-index:6"></div>'
                f'<div style="position:absolute;left:{tx+5}px;top:{bt+h-3:.0f}px;width:0;height:0;border-left:21px solid transparent;border-right:21px solid transparent;border-top:29px solid #0f1a4a;z-index:7"></div>')
        if badge:
            bw = font(K.P['gm_bold'], 44).getlength(badge) + 56
            html += f'<div style="position:absolute;left:{x+30}px;top:{top:.0f}px;width:{bw:.0f}px;height:62px;border-radius:62px;background:{GL};color:#17102b;display:flex;align-items:center;justify-content:center;font-family:{K.D};font-weight:900;font-size:44px;line-height:1;z-index:8">{badge}</div>'
        p.add(name, (x, top, x + w, top + bd + h + tail_h), html)
    return dict(h=bd + h + tail_h, kind='box', draw=draw)
def CHAT(p, msgs, size=60, avatar=None, name=None, name_in=True):
    """카카오톡식 대화창. msgs=[(글,'l'|'r')]. 왼쪽=정월(반투명 칸), 오른쪽=독자(금색 칸·어두운 글). 연속 메시지는 14px로 붙인 한 묶음(R29의 '덩어리' 하나).
    avatar: 정월 얼굴 이름(원형 132px, 첫 메시지 옆). name: 첫 왼쪽 메시지 위 이름(44px 금색)."""
    D = 132; lx = X0 + (D + 24 if avatar else 0); lmax = X0 + W - lx; rmax = 760
    items = []; y = 0
    if name: items.append(('name', y, 62)); y += 62 + 10
    first_l = True
    for txt, side in msgs:
        mw = lmax if side == 'l' else rmax; ls = lines_of(txt, BP, size, mw - 72, p, '대화'); f = font(BP, size); w = max(f.getlength(l) for l in ls) + 72; h = len(ls) * size * 1.5 + 56
        items.append(('msg', y, h, side, w, ls, first_l if side == 'l' else False)); y += h + 14
        if side == 'l': first_l = False
    for side_ in ('l', 'r'):
        ws = [it[4] for it in items if it[0] == 'msg' and it[3] == side_]
        if ws:
            mx = max(ws)
            for k, it in enumerate(items):
                if it[0] == 'msg' and it[3] == side_: items[k] = it[:4] + (mx,) + it[5:]
    H = y - 14
    def draw(top):
        html = ''; first_msg_top = None
        for it in items:
            if it[0] == 'name':
                html += f'<div style="position:absolute;left:{lx}px;top:{top+it[1]:.0f}px;font-family:{K.B};font-weight:800;font-size:44px;line-height:62px;color:{GOLD}">{name}</div>'
            else:
                _, yy, h, side, w, ls, first = it; t = top + yy
                if side == 'l':
                    if first_msg_top is None: first_msg_top = t
                    rad = '8px 30px 30px 30px' if first else '30px'; bg = PANEL_C; col = '#fff'; x = lx
                else: rad = '30px 8px 30px 30px'; bg = GOLD; col = INK; x = X0 + W - w
                html += f'<div style="position:absolute;left:{x:.0f}px;top:{t:.0f}px;width:{w:.0f}px;height:{h:.0f}px;box-sizing:border-box;background:{bg};border-radius:{rad};display:flex;align-items:center;justify-content:center;text-align:center;font-family:{K.B};font-weight:800;font-size:{size}px;line-height:1.5;color:{col};white-space:pre-line">{chr(10).join(ls)}</div>'
        if avatar and first_msg_top is not None:
            p.ai = True
            html += f'<div style="position:absolute;left:{X0}px;top:{first_msg_top:.0f}px;width:{D}px;height:{D}px;border-radius:50%;overflow:hidden;background:#27346f"><img src="data:image/png;base64,{CK.face_b64(avatar)}" style="position:absolute;left:{-D*0.27:.0f}px;top:{-D*0.04:.0f}px;height:{D*2.07:.0f}px"></div>'
        p.add('대화창', (X0, top, X0 + W, top + H), html)
    return dict(h=H, kind='box', draw=draw)
def PANEL(p, kids, pad=56, name='패널'):
    """제작 가이드 §4 '어두운 패널' (#181615). 안의 글 덩어리 사이 40px, 그림·알약과는 60px, 안쪽 여백 위아래 같게(R18)."""
    gaps = [40 if (a['kind'] == 'text' and b['kind'] == 'text') else 60 for a, b in zip(kids, kids[1:])]
    h = sum(k['h'] for k in kids) + sum(gaps) + 2 * pad
    def draw(top):
        p.add(name, (X0, top, X0 + W, top + h), f'<div style="position:absolute;left:{X0}px;top:{top:.0f}px;width:{W}px;height:{h:.0f}px;background:{PANEL_C};opacity:.94;border-radius:40px;z-index:0"></div>')
        y = top + pad
        for k, g in zip(kids, gaps + [0]): k['draw'](y); y += k['h'] + g
    return dict(h=h, kind='box', draw=draw)
def SCREEN(p, name, msgs, size=60):
    """메신저 화면 한 장(카톡 형식 차용). 상단 이름 바 · 대화 영역(아래에서 위로 쌓임) · 하단 입력창. 화면 전체가 묶음 y183~1265.
    msgs: [{'side':'l'|'r','text':..} | {'side':'l','rows':[(라벨,값)]} | {'side':'l','text':..,'btn':..}]. 연속 같은 쪽 메시지는 12px, 쪽이 바뀌면 36px."""
    BAND = BOT - TOP; PADX = 40; HEAD = 150; INP = 150; L_BG = '#2d2b2a'
    inner_w = W - 2 * PADX; items = []
    for m in msgs:
        mw = 700 if m['side'] == 'l' else 560
        if 'rows' in m:
            f = font(BP, size); lab_w = max(f.getlength(a) for a, _ in m['rows']) + 36
            vs = [lines_of(v, BP, size, mw - 72 - lab_w, p, '표값') for _, v in m['rows']]
            rows_h = [max(size * 1.5, len(v) * size * 1.5) for v in vs]; w = mw; h = sum(rows_h) + 56 + 12 * (len(rows_h) - 1)
            items.append(dict(m=m, w=w, h=h, vs=vs, rows_h=rows_h, lab_w=lab_w))
        else:
            ls = lines_of(m['text'], BP, size, mw - 72, p, '대화'); f = font(BP, size); w = max(f.getlength(l) for l in ls) + 72; h = len(ls) * size * 1.5 + 56
            btn = m.get('btn'); bh = 0
            if btn:
                bl = btn.split('\n'); bf = font(BP, size - 8); w = max(w, max(bf.getlength(l) for l in bl) + 72 + 36); bh = len(bl) * (size - 8) * 1.5 + 40 + 24
            items.append(dict(m=m, w=w, h=h + bh, ls=ls, bh=bh))
    for sd in ('l', 'r'):
        ws = [it['w'] for it in items if it['m']['side'] == sd]
        if ws:
            for it in items:
                if it['m']['side'] == sd: it['w'] = max(ws)
    gaps = [12 if a['m']['side'] == b['m']['side'] else 36 for a, b in zip(items, items[1:])]
    stack_h = sum(i['h'] for i in items) + sum(gaps)
    area_top = HEAD + 30; area_bot = BAND - INP - 30
    if stack_h > area_bot - area_top: p.problems.append(f'대화가 화면보다 김({stack_h:.0f}px > {area_bot - area_top:.0f}px)')
    def draw(top):
        h = []
        h.append(f'<div style="position:absolute;left:{X0}px;top:{top:.0f}px;width:{W}px;height:{BAND}px;background:{PANEL_C};border-radius:48px;z-index:0"></div>')
        h.append(f'<div style="position:absolute;left:{X0+PADX}px;top:{top+(HEAD-84)/2:.0f}px;width:84px;height:84px;border-radius:50%;background:{GOLD};color:#17102b;display:flex;align-items:center;justify-content:center;font-family:{K.D};font-weight:900;font-size:48px">{name[0]}</div>')
        h.append(f'<div style="position:absolute;left:{X0+PADX+84+24}px;top:{top:.0f}px;height:{HEAD}px;display:flex;align-items:center;font-family:{K.B};font-weight:800;font-size:52px;color:#fff">{name}</div>')
        h.append(f'<div style="position:absolute;left:{X0}px;top:{top+HEAD:.0f}px;width:{W}px;height:2px;background:rgba(255,255,255,.12)"></div>')
        y = top + area_bot - stack_h + (0)   # 아래에 붙여 쌓는다
        for it, g in zip(items, gaps + [0]):
            m = it['m']; w = it['w']; x = X0 + PADX if m['side'] == 'l' else X0 + W - PADX - w
            bg = L_BG if m['side'] == 'l' else GOLD; col = '#fff' if m['side'] == 'l' else INK; rad = '8px 32px 32px 32px' if m['side'] == 'l' else '32px 8px 32px 32px'
            if 'rows' in m:
                inner = ''; yy = 28
                for (a, _), v, rh in zip(m['rows'], it['vs'], it['rows_h']):
                    inner += f'<div style="position:absolute;left:36px;top:{yy:.0f}px;height:{rh:.0f}px;display:flex;align-items:center;color:{GOLD};font-size:{size}px;line-height:1.5">{a}</div><div style="position:absolute;left:{36+it["lab_w"]:.0f}px;top:{yy:.0f}px;height:{rh:.0f}px;display:flex;align-items:center;color:#fff;font-size:{size}px;line-height:1.5;white-space:pre-line">{chr(10).join(v)}</div>'; yy += rh + 12
                h.append(f'<div style="position:absolute;left:{x:.0f}px;top:{y:.0f}px;width:{w:.0f}px;height:{it["h"]:.0f}px;background:{bg};border-radius:{rad};font-family:{K.B};font-weight:800">{inner}</div>')
            else:
                tp = it['h'] - it['bh']
                body = f'<div style="position:absolute;left:0;top:0;width:{w:.0f}px;height:{tp:.0f}px;display:flex;align-items:center;justify-content:center;text-align:center;font-size:{size}px;line-height:1.5;color:{col};white-space:pre-line">{chr(10).join(it["ls"])}</div>'
                if m.get('btn'):
                    bs = size - 8; bl = m['btn'].split('\n'); bhh = it['bh'] - 24
                    body += f'<div style="position:absolute;left:18px;top:{tp:.0f}px;width:{w-36:.0f}px;height:{bhh:.0f}px;border-radius:{min(bhh/2,40):.0f}px;background:{GOLD};color:{INK};display:flex;align-items:center;justify-content:center;text-align:center;font-size:{bs}px;line-height:1.5;white-space:pre-line">{m["btn"]}</div>'
                h.append(f'<div style="position:absolute;left:{x:.0f}px;top:{y:.0f}px;width:{w:.0f}px;height:{it["h"]:.0f}px;background:{bg};border-radius:{rad};font-family:{K.B};font-weight:800">{body}</div>')
            y += it['h'] + g
        iy = top + BAND - INP + 20
        h.append(f'<div data-deco="1" style="position:absolute;left:{X0+PADX}px;top:{iy:.0f}px;width:{inner_w-100}px;height:{INP-60}px;border-radius:{(INP-60)/2:.0f}px;background:{L_BG};color:rgba(255,255,255,.5);display:flex;align-items:center;padding-left:40px;box-sizing:border-box;font-family:{K.B};font-weight:800;font-size:40px">메시지 입력</div>')
        h.append(f'<div data-deco="1" style="position:absolute;left:{X0+W-PADX-(INP-60)}px;top:{iy:.0f}px;width:{INP-60}px;height:{INP-60}px;border-radius:50%;background:{GOLD}"></div>')
        p.add('메신저 화면', (X0, top, X0 + W, top + BAND), ''.join(h)); p.ai = True
    return dict(h=BAND, kind='box', draw=draw)
def ROW(p, label, sub, val, name='표 행', size=50, vw=540):
    ls = lines_of(val, BP, size, vw, p, name); inner = max(132, len(ls) * size * 1.5); h = inner + 56
    def draw(top):
        p.add(name, (X0, top, X0 + W, top + h), f'<div style="position:absolute;left:{X0}px;top:{top:.0f}px;width:{W}px;height:{h:.0f}px;background:#181615;border-radius:28px"></div>'
              f'<div style="position:absolute;left:{X0}px;top:{top:.0f}px;width:270px;height:{h:.0f}px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;font-family:{K.B};font-weight:800"><div style="font-size:52px;color:{GOLD};line-height:1.3">{label}</div><div style="font-size:40px;color:#fff;opacity:.85;line-height:1.3">{sub}</div></div>'
              f'<div style="position:absolute;left:{X0+300}px;top:{top:.0f}px;width:600px;height:{h:.0f}px;display:flex;align-items:center;font-family:{K.B};font-weight:800;font-size:{size}px;line-height:1.5;color:#fff;white-space:pre-line">{chr(10).join(ls)}</div>')
    return dict(h=h, kind='box', draw=draw)
def FACE(p, name, h, side='right', flip=False):
    w = h * 0.75; p.ai = True
    def draw(top):
        x = X0 if side == 'left' else X0 + W - w if side == 'right' else X0 + (W - w) / 2
        tf = 'transform:scaleX(-1);' if flip else ''
        p.add('정월', (x, top, x + w, top + h), f'<img src="data:image/png;base64,{CK.face_b64(name)}" style="position:absolute;left:{x:.0f}px;top:{top:.0f}px;height:{h}px;{tf}z-index:2">')
    return dict(h=h, kind='gfx', draw=draw, w=w)
def PHONE(p, scale=.6):
    w, h = 330 * scale, 560 * scale
    def draw(top):
        x = X0 + (W - w) / 2
        p.add('휴대폰', (x, top, x + w, top + h), f'<div data-deco="1" style="position:absolute;left:{x:.0f}px;top:{top:.0f}px;width:330px;height:560px;transform:scale({scale});transform-origin:0 0;border:8px solid #e9e4dc;box-sizing:border-box;border-radius:48px;background:rgba(8,8,18,.78);z-index:3"><div style="position:absolute;left:24px;top:60px;width:230px;background:#fff;color:#111;font-size:30px;font-family:{K.B};font-weight:800;line-height:1.5;padding:14px 20px;border-radius:24px 24px 24px 6px;box-sizing:border-box">읽었어요 ✓</div><div style="position:absolute;right:24px;top:190px;width:200px;background:{GOLD};color:#111;font-size:30px;font-family:{K.B};font-weight:800;line-height:1.5;padding:14px 20px;border-radius:24px 24px 6px 24px;box-sizing:border-box">…</div></div>')
    return dict(h=h, kind='gfx', draw=draw)
def SIDE(p, face, blk, face_side='left'):   # 얼굴 + 옆 글/알약을 한 줄로
    h = max(face['h'], blk['h']); fx = X0 if face_side == 'left' else X0 + W - face['w']; tx = (X0 + face['w'] + 30) if face_side == 'left' else X0
    def draw(top):
        face['draw'](top + (h - face['h']) / 2); blk['draw'](top + (h - blk['h']) / 2)
    return dict(h=h, kind='gfx', draw=draw)
def place(p, blocks, justify=False):
    gaps = [60 if 'text' not in (a['kind'], b['kind']) or a['kind'] != b['kind'] and 'text' in (a['kind'], b['kind']) and 'gfx' in (a['kind'], b['kind'], ) or a['kind'] != 'text' or b['kind'] != 'text' else 40 for a, b in zip(blocks, blocks[1:])]
    gaps = [40 if (a['kind'] == b['kind'] and a['kind'] in ('text', 'box')) or (a['kind'] == 'box' and b['kind'] == 'box') else 60 for a, b in zip(blocks, blocks[1:])]
    total = sum(b['h'] for b in blocks) + sum(gaps); band = BOT - TOP
    if total > band + 0.5: p.problems.append(f'묶음 높이 {total:.0f}px가 {band}px보다 큼')
    extra = band - total
    if justify and gaps: gaps = [min(g + extra / len(gaps), 120) for g in gaps]; total = sum(x['h'] for x in blocks) + sum(gaps)   # R46: 간격은 120px까지만 벌린다(남는 높이는 글자를 키워 메운다)
    y = CEN - total / 2
    for b, g in zip(blocks, gaps + [0]): b['draw'](y); y += b['h'] + g
    return p
def new(): return Page('carousel')
S = {}
C_ = 'center'
def A1():
    p = new(); p.bg = 'ink'; place(p, [FACE(p, 'v4_glasses', 560, 'center'), PANEL(p, [T(p, '정월의 연애 테스트', 52, GOLD, 'body', 1.3, 'center', 788, '라벨', X0 + 56), T(p, '3초 만에\n사랑에 빠지는 사람', 92, '#fff', 'title', 1.3, 'center', 788, '제목', X0 + 56)])]); return p
def A2():
    p = new(); place(p, [PILL(p, '정월의 한마디', 52, None, 'center'), T(p, '주변에 꼭\n한 명 있죠?', 130, align=C_, name='제목'), T(p, '사주·별자리·숫자로\n보면 이래요.', 84, '#fff', 'body', 1.5, C_, name='설명')]); return p
def A3():
    p = new(); place(p, [PILL(p, '공통점', 52, None, 'center'), T(p, '사주·별자리·숫자가\n[[같은 말]]을 해요', 84, lh=1.35, align=C_, name='제목'), T(p, '바로 달아오르고,\n먼저 표현하고,\n새로움에 끌려요.', 72, '#fff', 'body', 1.5, C_, name='설명')]); return p
def A4():
    p = new(); place(p, [T(p, '여러분은\n몇 개 겹치나요?', 110, align=C_, name='제목'), T(p, '하나도 안 겹친다면,\n천천히 스며드는 사랑을 하는\n사람일지도 몰라요.', 60, '#fff', 'body', 1.5, C_, name='설명'), PILL(p, '내 숫자를 댓글로 남겨 주세요', 52, 900, 'center')]); return p
def B1():
    p = new(); place(p, [T(p, '사주 · 별자리 · 숫자,\n이렇게 말해요', 72, lh=1.32, align=C_, name='제목'), T(p, '3초 만에 사랑에 빠지는 사람', 56, GOLD, 'body', 1.4, C_, name='부제'),
                         ROW(p, '사주', '동양', '병화일생,\n도화가 있는 사주'), ROW(p, '별자리', '서양', '양자리 · 사자자리'), ROW(p, '숫자', '수비학', '3번 · 5번')]); return p
def B2():
    p = new(); place(p, [T(p, '태양처럼 바로 달아오르고,\n사람을 끌어요', 76, align=C_, name='제목'),
                         ROW(p, '사주', '동양', '병화일생,\n도화가 있는 사주'), ROW(p, '별자리', '서양', '양자리 · 사자자리\n직진하는 불의 별자리'), ROW(p, '숫자', '수비학', '3번 · 5번\n표현의 3, 새로움에 끌리는 5')]); return p
def B3():
    p = new(); place(p, [PILL(p, '몇 개 겹치나요?', 52, None, 'center'), T(p, '겹친 개수로\n읽는 법', 88, align=C_, name='제목'), ROW(p, '1개 이상', '겹침', '첫눈에 빠지는 쪽에\n가까울 수 있어요'), ROW(p, '0개', '안 겹침', '천천히 스며드는 사랑을\n하는 사람일지도 몰라요'), T(p, '사주·별자리·숫자를 함께 읽어요.', 48, '#fff', 'body', 1.5, C_, name='설명')]); return p
def B4():
    p = new(); p.bg = 'ink'; place(p, [FACE(p, 'v4_glasses', 420, 'center'), PANEL(p, [PILL(p, '결과', 52, None, 'center'), T(p, '여러분은 몇 개 겹치나요?', 76, '#fff', 'title', 1.3, 'center', 788, '제목', X0 + 56), T(p, '표를 먼저, 풀이는 그다음에 읽어요.', 52, '#fff', 'body', 1.5, 'center', 788, '설명', X0 + 56)])]); return p
def C1():
    p = new(); place(p, [SCREEN(p, '정월', [dict(side='l', text='3초 만에 사랑에 빠지는 사람,'), dict(side='l', text='주변에 꼭 한 명 있죠?'), dict(side='r', text='있어요, 있어요!')], 72)]); return p
def C2():
    p = new(); place(p, [SCREEN(p, '친구', [dict(side='l', text='아까 그 사람,\n계속 생각나요.'), dict(side='r', text='만난 지\n3분인데요?')], 72)]); return p
def C3():
    p = new(); place(p, [SCREEN(p, '정월', [dict(side='l', text='사주 · 별자리 · 숫자로\n보면 이래요'), dict(side='l', rows=[('사주', '병화일생, 도화'), ('별자리', '양자리 · 사자자리'), ('숫자', '3번 · 5번')])], 60)]); return p
def C4():
    p = new(); place(p, [SCREEN(p, '정월', [dict(side='l', text='하나도 안 겹친다면,'), dict(side='l', text='천천히 스며드는 사랑을\n하는 사람일지도 몰라요.'), dict(side='l', text='여러분은\n몇 개 겹치나요?')], 64)]); return p
def C5():
    p = new(); place(p, [SCREEN(p, '정월', [dict(side='l', text='내 숫자를 댓글로\n남겨 주세요.'), dict(side='l', text='프로필 링크에서\n생년월일을 입력해 보세요.')], 68)]); return p
PAGES = dict(A1=A1, A2=A2, A3=A3, A4=A4, B1=B1, B2=B2, B3=B3, B4=B4, C1=C1, C2=C2, C3=C3, C4=C4, C5=C5)
def metrics(p):
    r = sorted([(n, *b) for n, b in p.els if n != '정월' and n != '휴대폰' or True], key=lambda e: e[2])
    t = min(e[2] for e in r); b = max(e[4] for e in r); return t, b, (t + b) / 2
async def main(out):
    from playwright.async_api import async_playwright
    os.makedirs(out, exist_ok=True); bad = 0
    async with async_playwright() as pw:
        br = await pw.chromium.launch(executable_path='/opt/pw-browsers/chromium'); pg = await br.new_page(viewport={'width': 1080, 'height': 1440})
        for k, fn in PAGES.items():
            p = fn(); t, b, c = metrics(p)
            for pr in p.problems: print('엔진:', k, pr); bad += 1
            if t < TOP - 1 or b > BOT + 1 or abs(c - CEN) > 15: print('배치:', k, f'위 {t:.0f} 아래 {b:.0f} 가운데 {c:.0f}'); bad += 1
            rs = sorted([e for e in p.els], key=lambda e: e[1][1])
            for a, bb in zip(rs, rs[1:]):
                if a[0] not in ('패널', '메신저 화면') and bb[0] not in ('패널', '메신저 화면') and bb[1][1] < a[1][3] - 1 and not (bb[1][0] >= a[1][2] or a[1][0] >= bb[1][2]): print('겹침:', k, a[0], bb[0]); bad += 1
            open('/tmp/v3.html', 'w', encoding='utf-8').write(CK.page(''.join(p.html) + CK.frame(getattr(p, 'ai', False)), getattr(p, 'bg', 'sun'), GOLD)); await pg.goto('file:///tmp/v3.html'); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(350)
            for x in await check_page(pg, k, 'bundle'): print('검사:', x); bad += 1
            await pg.screenshot(path=f'{out}/{k}.png'); print(k, f'묶음 {t:.0f}~{b:.0f} 가운데 {c:.0f}')
        await br.close()
    print('문제', bad, '건')
    ks = list(PAGES); Wd, Hd = 300, 400; sheet = Image.new('RGB', (Wd * 5 + 60, Hd * 3 + 40), (30, 30, 34))
    for i, k in enumerate(ks):
        r = 'ABC'.index(k[0]); c = int(k[1]) - 1; sheet.paste(Image.open(f'{out}/{k}.png').resize((Wd, Hd)), (10 + c * (Wd + 10), 10 + r * (Hd + 10)))
    sheet.save(f'{out}/sheet.png')
if __name__ == '__main__': asyncio.run(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'out')))
