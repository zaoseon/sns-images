"""K-193(대표 11/12 15:15 '힘 쓸 달·아낄 달' → '좋은 달·조심할 달') 그림 다시 그리기 — 아직 공개 전 글만(K-194).
① 자동 실행 11/12 19:45. 8편(n68·n43·n69·n54·n76·n86·n90·n92)을 눈으로 봐서 옛 말이 그림에 남은 곳만 골랐다:
  n68 표지 a4 · 한 줄 결론 i5f · 한눈에 b4f · 다섯 달 g9f / n69 표지 a4 · 한 줄 결론 i5f · 한눈에 b4f / n76 잃을 때 e9f / n92 달 칸 m3f
  (n43·n54·n86·n90 은 그림에 옛 말 없음 — 글자는 CT 가 11/12 15:50 에 고침)
방법: 처음 그린 함수를 그대로 부르고, 넘기는 글만 copy_rules.바꿀말로 바꾼다(그림 값은 그대로). 새 이름만(naver/img 덮어쓰기 금지):
  a4→a5 · i5→i6 · b4→b5 · g9→g10 · e9→e10 · m3→m4, 그다음 fullbleed 로 꽉 찬 판(*f.jpg).
pages.json·사이트 원고(public/naver/nXX.html) 주소를 바꾸고 사이트 사본(public/naver/img)도 둔다(K-069).
사용: python3 naver/k193_redraw_1112.py n68 n69 n76 n92   (PREVIEW=폴더 → 그림만 그 폴더에)"""
import os, sys, json, re, shutil
from urllib.parse import quote
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "pipeline"))
SITE = os.environ.get("SITE", "/home/claude/zaoseon-site")
import copy_rules as CR
import body_v3 as B, body_v4 as B4, cover_v3 as V, fullbleed as FB, diagrams_k131 as DG
PG = os.path.join(HERE, "pages.json"); IMG = os.path.join(HERE, "img")
PREVIEW = B.PREVIEW
MAP = sorted(CR.바꿀말.items(), key=lambda kv: -len(kv[0]))


def sub(x):
    if isinstance(x, str):
        for o, n in MAP: x = x.replace(o, n)
        return x
    if isinstance(x, (list, tuple)): return type(x)(sub(i) for i in x)
    return x


def old_left(x):
    s = json.dumps(x, ensure_ascii=False); return [o for o, _ in MAP if o in s]


def _pick(pid): return json.load(open(B4.PICK, encoding="utf-8"))[pid]


def cover(pid, n):
    T = V.all_configs(); cfg = T[pid]; assert not old_left(cfg), (pid, "표지 설정에 옛 말", cfg)
    out = f"wide/naver_z{n}_a5.jpg"; dst = os.path.join(PREVIEW, os.path.basename(out)) if PREVIEW else os.path.join(IMG, out)
    if not PREVIEW: assert not os.path.exists(dst), ("이미 있는 이름", out)
    V.render(pid, cfg, dst, _pick(pid)); return {f"wide/naver_z{n}_a4.jpg": out}


def intro(pid, n):
    import mobile_fix_1111 as MF
    d = sub(MF.INTRO[pid]); c = V.Ctx(_pick(pid)); T = V.all_configs()
    B.intro_v3(f"naver_z{n}_i6.jpg", c, d[0], d[1], d[2], T[pid].get("face") or "v1_lowbun"); return (f"naver_z{n}_i5f.jpg", f"naver_z{n}_i6.jpg")


def glance(pid, n):
    cap = B4.capture(pid); d = sub(cap[f"naver_z{n}_b.jpg"]); assert d[0] == "rows", d
    c = V.Ctx(_pick(pid)); B.table_v3(f"naver_z{n}_b5.jpg", c, d[1], [], [[it[0], it[1], (it[2] if len(it) > 2 and it[2] else "")] for it in d[2]])
    return (f"naver_z{n}_b4f.jpg", f"naver_z{n}_b5.jpg")


def wrap(mod, fname):
    """처음 그린 계획(build_k131_*)의 그리기 함수를 감싸 글만 바꿔 부른다."""
    f = getattr(mod, fname)
    def g(name, c, *a, **k): return f(name, c, *sub(a), **{kk: sub(v) for kk, v in k.items()})
    return g


def k131(pid, n, slot, mod_name, old, new):
    import importlib, diagrams_k131c as D3
    M = importlib.import_module(mod_name); P = M.plan(); sp = P[pid][slot]
    keep = {fn: getattr(D3, fn) for fn in ("timeline3", "versus", "compare", "person", "exp", "vbar")}
    try:
        for fn in keep: setattr(D3, fn, wrap(type("m", (), keep), fn))
        sp[2](new, V.Ctx(M.PAL_OVR[pid]) if hasattr(M, "PAL_OVR") and pid in M.PAL_OVR else __import__("build_k131_b2v2").pal(pid))
    finally:
        for fn, f in keep.items(): setattr(D3, fn, f)
    return (old, new)


def n92_month(pid, n):
    import cover_v3 as V_
    c = V_.Ctx("k_neon_s")
    tag = {7: ("한 팀", "up"), 10: ("짝", "up"), 11: ("한 팀", "up"), 8: ("원진", "dn"), 9: ("충", "dn")}   # build_naver_92.py 와 같은 값
    DG.monthgrid("naver_z92_m4.jpg", c, "2027년 토끼띠의 달", [(m, *tag.get(m, ("", None))) for m in list(range(2, 13)) + [1]])
    return ("naver_z92_m3f.jpg", "naver_z92_m4.jpg")


JOBS = {
    "n68": [cover, intro, glance, lambda p, n: k131(p, n, "C", "build_k131_b5f", "naver_z68_g9f.jpg", "naver_z68_g10.jpg")],
    "n69": [cover, intro, glance],
    "n76": [lambda p, n: k131(p, n, "R", "build_k131_b4a", "naver_z76_e9f.jpg", "naver_z76_e10.jpg")],
    "n92": [n92_month],
}


def run(pid):
    n = pid[1:]; swap = {}
    for job in JOBS[pid]:
        r = job(pid, n)
        if isinstance(r, dict): swap.update(r); continue
        old, raw = r
        if PREVIEW: swap[old] = raw; continue
        fr, why = FB.convert(raw, [IMG, os.path.join(IMG, "m1280")])
        assert fr, (pid, raw, "꽉 찬 판 못 만듦", why)
        swap[old] = fr[0]
    if PREVIEW: print(pid, swap); return swap
    pages = json.load(open(PG, encoding="utf-8")); p = pages[pid]
    for o, nw in swap.items():
        if o.startswith("wide/"): assert p["cover"] == o, (pid, p["cover"]); p["cover"] = nw; continue
        assert o in p["body"], (pid, o); p["body"] = p["body"].replace(o, nw)
        try:
            reg = json.load(open(DG.REG, encoding="utf-8"))
            if o in reg: reg[nw] = reg[o]; json.dump(dict(sorted(reg.items())), open(DG.REG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        except Exception: pass
    p.setdefault("k193", []).append({"at": "2026-11-12 ① 자동", "swap": swap})
    json.dump(pages, open(PG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    fp = os.path.join(HERE, "fullbleed_plan.json"); plan = json.load(open(fp, encoding="utf-8"))
    plan.setdefault(pid, []).extend({"pos": None, "old": o, "new": nw, "src": "K-193 11/12"} for o, nw in swap.items() if not o.startswith("wide/"))
    json.dump(plan, open(fp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    sf = os.path.join(SITE, "public", "naver", pid + ".html")
    if os.path.exists(sf):
        s = open(sf, encoding="utf-8").read(); s0 = s
        for o, nw in swap.items(): s = s.replace(o, nw).replace(quote(o), quote(nw))
        open(sf, "w", encoding="utf-8").write(s); print(pid, "사이트 원고", "바뀜" if s != s0 else "주소 없음(표지만)")
    for nw in swap.values():
        dst = os.path.join(SITE, "public", "naver", "img", nw); os.makedirs(os.path.dirname(dst), exist_ok=True); shutil.copy(os.path.join(IMG, nw), dst)
    print(pid, swap); return swap


if __name__ == "__main__":
    for a in sys.argv[1:]: run(a)
