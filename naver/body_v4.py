"""원고 한 편의 이미지를 새 틀로 다시 만든다 (10/16 대표: 캡처 조합 판·연속 금지·심리 도식·표지와 같은 문법).
- 판: 표지 판 고르기 pick5(cover_v3) 결과(cover_v5_pick.json). 표지·본문 같은 판.
- 표지 wide/naver_zNN_a4.jpg, 본문 naver_zNN_[i|b|c|s]4.jpg (body_v3 틀), 심리 도식 naver_zNN_q4.jpg(그 글 심리 카드로).
- 새 이름만(사진 보존 규칙). 사이트 사본(zaoseon-site public/naver/img/)도 같이 둔다(K-069).
- pages.json: 표지·본문 주소를 *4로, 심리 단락 출처 줄 바로 뒤에 도식(설명 문장 + 그림) 한 번.
사용: python3 naver/body_v4.py n51 [n52 ...]"""
import os, sys, json, re, shutil, urllib.parse, html
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "pipeline"))
import imgkit as K
import cover_v3 as V, body_v3 as B
from imgkit import Cv, L, RT, SER
SITE = os.environ.get("SITE", "/home/claude/zaoseon-site")
PG = os.path.join(HERE, "pages.json"); PICK = os.path.join(HERE, "cover_v5_pick.json")
CARDS = os.environ.get("CARDS", f"{SITE}/engine/psych_cards2")

def cards():
    import yaml, glob
    out = {}
    for f in sorted(glob.glob(CARDS + "/*.yaml")):
        for c in yaml.safe_load(open(f, encoding="utf-8")): out[c["id"]] = c
    return out

def psych_diagram(name, c, card, act):
    """심리 개념 흐름: 이럴 때 → 그대로 두면 → 이렇게 해 봐요 (굵은 화살표, 장식 없음)"""
    sig = (card.get("신호") or [""])[0]; keep = card.get("그대로") or ""
    steps = [("이럴 때", sig), ("그대로 두면", keep), ("이렇게 해 봐요", act)]
    tmp = Cv(100, c.bg); mw = RT - L - 100; bodies = []
    for lab, t in steps:
        ls = K.balanced(tmp, t, B.SB, 44, mw)
        bodies.append(ls[:3])
    hs = [60 + 56 * len(b) + 40 for b in bodies]; gap = 90
    H = 190 + sum(hs) + gap * 2 + 40; cv = Cv(H, c.bg)
    head = f"{card['이름']}"; cv.text(L + 10, 96, head, B.XB, cv.fit(head, B.XB, 60, RT - L - 220, 44), c.fg, "ls")
    cv.text(RT - 10, 92, card["이론"], B.XB, 32, c.pill if hasattr(c, "pill") else c.acc, "rs")
    y = 150
    for i, ((lab, _), ls) in enumerate(zip(steps, bodies)):
        h = hs[i]; last = i == 2
        cv.rr([L + 10, y, RT - 10, y + h], 28, fill=(c.pill if last else c.card), outline=None if last else c.line, w=2)
        fg = c.pillfg if last else c.fg
        cv.text(L + 46, y + 52, lab, B.XB, 38, fg if last else (c.acc if c.acc != c.fg else c.gray), "lm")
        yy = y + 96
        for l in ls: cv.text(L + 46, yy, l, B.SB, 44, fg, "lm"); yy += 56
        y += h
        if not last:
            cx = (L + RT) / 2; cv.d.rectangle([(cx - 7) * K.S, (y + 12) * K.S, (cx + 7) * K.S, (y + gap - 40) * K.S], fill=c.acc)
            cv.d.polygon([((cx - 30) * K.S, (y + gap - 44) * K.S), ((cx + 30) * K.S, (y + gap - 44) * K.S), (cx * K.S, (y + gap - 10) * K.S)], fill=c.acc)
            y += gap
    B._save(cv, name)

def capture(pid):
    """기존 제작 스크립트가 그리던 데이터(rows·table·intro·bars)를 그대로 받아 온다(새 틀로 다시 그리기 위해)."""
    import rerender_body_images as RB, naver2 as N2, regen_badges as RG
    cap = {}; _save = K.Cv.save
    K._skip = lambda p: False
    K.Cv.save = lambda s_, n: None
    K.rows = lambda path, head, items, note="": cap.setdefault(os.path.basename(path), ("rows", head, [list(i) for i in items]))
    K.table = lambda path, head, cols, rows_, widths: cap.setdefault(os.path.basename(path), ("table", head, cols, rows_))
    K.intro = lambda pid_, summ, maps, path, label="세 풀이": cap.setdefault(os.path.basename(path), ("intro", summ, maps, label))
    K.bars = lambda pid_, title, rws, path: cap.setdefault(os.path.basename(path), ("bars", title, rws))
    N2.title = N2.months = N2.grid = N2.ring = lambda *a, **k: None
    RB.SCRIPTS = ["build_naver_04_07.py", "build_naver_08_12.py", "build_naver_13_15.py", "build_naver_23_25.py"] + RB.SCRIPTS
    import naver as N1
    for fn in dir(N1):
        f_ = getattr(N1, fn)
        if callable(f_) and not fn.startswith("_") and getattr(f_, "__module__", "") == N1.__name__ and fn not in ("rows", "table", "theme"): setattr(N1, fn, lambda *a, **k: None)
    N1.rows = lambda path, head, items, note="": cap.setdefault(os.path.basename(path), ("rows", head, [list(i) for i in items]))
    N1.table = lambda path, head, cols, rows_, widths: cap.setdefault(os.path.basename(path), ("table", head, cols, rows_))
    keep = open(PG, encoding="utf-8").read()
    open(PG, "w", encoding="utf-8").write(re.sub(r"(naver_z\d+_[a-z]+)[34]\.jpg", r"\1.jpg", keep))
    try: RB.main([pid])
    finally: open(PG, "w", encoding="utf-8").write(keep); K.Cv.save = _save
    return cap

def run(pid):
    reg = json.load(open(PG, encoding="utf-8")); v = reg[pid]; pick = json.load(open(PICK, encoding="utf-8"))
    T = V.all_configs(); c = V.Ctx(pick[pid]); n = int(pid[1:]); made = {}
    # 표지
    a4 = f"wide/naver_z{n}_a4.jpg"; V.render(pid, T[pid], os.path.join(HERE, "img", a4), pick[pid]); made["cover"] = a4
    # 본문 정보 이미지
    cap = capture(pid)
    bodyu = urllib.parse.unquote(v["body"])
    for base, d in cap.items():
        if not any(base[:-4] + s_ in bodyu for s_ in (".jpg", "3.jpg", "4.jpg")): continue   # 이 글 본문에 있는 사진만(옛 이름 naver_y03_… 포함)
        new = base.replace(".jpg", "4.jpg")
        if d[0] == "table": B.table_v3(new, c, d[1], d[2], d[3])
        elif d[0] == "rows":   # 해 볼 것은 번호 원, 나머지(날짜·띠·이름이 열쇠인 목록)는 이름표가 앞에 오는 표 모양(10/16: 손없는날 날짜가 작은 줄로 밀린 것 고침)
            if "해 볼" in d[1] or "할 일" in d[1]: B.rows_v3(new, c, d[1], d[2])
            else: B.table_v3(new, c, d[1], [], [[it[0], it[1], (it[2] if len(it) > 2 and it[2] else "")] for it in d[2]])
        elif d[0] == "intro": B.intro_v3(new, c, d[1], d[2], d[3], T[pid].get("face") or "v1_lowbun")
        elif d[0] == "bars": B.table_v3(new, c, d[1], [], [[a, b] for a, b in d[2]])
        made[base] = new
    # 심리 도식
    E = json.load(open(os.path.join(HERE, "enrich_1016.json"), encoding="utf-8")).get(pid, {})
    q = None
    if E.get("psych"):
        card = cards()[E["psych"]["card"]]; act = E["psych"]["lines"][2] if len(E["psych"]["lines"]) > 2 else card.get("한마디", "")
        q = f"naver_z{n}_q4.jpg"; psych_diagram(q, c, card, act)
    # 원고 주소 바꾸기
    b = v["body"]
    for old, new in made.items():
        if old == "cover": continue
        stem = old[:-4]
        for st in (stem, urllib.parse.quote(stem)):
            b = re.sub(rf"(/naver/img/)(?:m1280/)?{re.escape(st)}3?\.jpg", lambda m_: m_.group(1) + urllib.parse.quote(new) if st != stem else m_.group(1) + new, b)
    if q and q not in b:
        i = b.find("심리학으로 읽으면"); j = b.find("<p>📚", i); k = b.find("</p>", j) + 4 if j > 0 else -1
        if k > 3:
            U = "https://raw.githubusercontent.com/zaoseon/sns-images/main/naver/img/"
            alt = html.escape(f"{card['이름']}({card['이론']}) 흐름: 이럴 때, 그대로 두면, 이렇게 해 봐요", quote=True)
            b = b[:k] + "<p>&nbsp;</p><p>이 마음이 흘러가는 모양을 그려 보면 이래요.</p>" + f'<p><img src="{U}{q}" alt="{alt}"></p>' + b[k:]
    v["body"] = b; v.setdefault("cover_v3", v.get("cover")); v["cover"] = a4
    json.dump(reg, open(PG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    # 사이트 사본(K-069)
    files = [a4] + list(x for k_, x in made.items() if k_ != "cover") + ([q] if q else [])
    for f in files:
        src = os.path.join(HERE, "img", f); dst = os.path.join(SITE, "public", "naver", "img", f)
        os.makedirs(os.path.dirname(dst), exist_ok=True); shutil.copy(src, dst)
    return files

if __name__ == "__main__":
    LOCK = {"n51"}   # 10/16 13:20 먼저 확정해 서브 노트북이 예약을 다시 건 글 — 같은 이름으로 다시 만들지 않는다
    for p in [a for a in sys.argv[1:] if a.startswith("n")]:
        if p in LOCK: print(p, "확정된 글이라 건너뜀"); continue
        print(p, run(p))
