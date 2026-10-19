"""학자 카드(person 틀) 12장 다시 그리기 — 이름 첫 글자 원 → 연구 연도 칸 (대표 10/19 18:11, CT 18:20 → ①).
코드(diagrams_k131c.person)는 fcaccc1 에서 이미 고쳤다. 이 스크립트는 그 틀로 같은 내용을 새 이름(…v.jpg → 여백 없는 판 …vf.jpg)으로 다시 그리고
pages.json·fullbleed_plan.json·content/reel_swaps.json(승인 카드 이미지·모음 시트)의 옛 이름을 새 이름으로 바꾼다. 옛 파일은 지우지 않는다(네이버 보존 규칙).
사용: PREVIEW=폴더 python3 naver/redraw_person_v.py (그림만) · python3 naver/redraw_person_v.py"""
import os, sys, re, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import body_v3 as B, cover_v3 as CV
import build_k131_b2v2 as V2, build_k131_b2v3 as V3, build_k131_b3 as B3m, build_k131_b4a as A

ROOT = os.path.dirname(HERE)


def targets():
    """-> [(pid, 옛 이름, 판, 그리는 함수)] diagrams.json 의 person 12장."""
    out = []
    p3 = V3.plan()
    for pid in ("n26", "n31"):
        sp = p3[pid]; r = sp["R"]; letter, fn = (r[0], r[1]) if len(r) == 4 else (r[1], r[2])
        out.append((pid, f"naver_z{sp['key']}_{letter}7.jpg", V2.pal(pid), fn))
    pb = B3m.plan()
    for pid, sp in pb.items():
        if "D3.person" in _src(sp["R"][0]):
            out.append((pid, f"naver_z{sp['key']}_e8.jpg", CV.Ctx(B3m.PAL_OVR[pid]) if pid in B3m.PAL_OVR else V2.pal(pid), sp["R"][0]))
    pa = A.plan()
    for pid, sp in pa.items():
        if "D3.person" in _src(sp["R"][2]):
            out.append((pid, f"naver_z{sp['key']}_e9.jpg", CV.Ctx(A.PAL_OVR[pid]) if pid in A.PAL_OVR else V2.pal(pid), sp["R"][2]))
    return out


def _src(fn):
    import inspect
    try: return inspect.getsource(fn)
    except Exception: return ""


def vname(old): return old.replace(".jpg", "v.jpg")


def run():
    import fullbleed as FBK
    reg = json.load(open(os.path.join(HERE, "diagrams.json"), encoding="utf-8"))
    T = targets(); rn_ = B3m.remote_names(); swap = {}; rows = {}
    for pid, old, c, fn in T:
        assert reg.get(old) == "person", (old, reg.get(old))
        new = vname(old)
        if not B.PREVIEW:
            assert new not in rn_ and new.replace(".jpg", "f.jpg") not in rn_, ("이미 있는 이름", new)
        fn(new, c)
        if B.PREVIEW: continue
        r, why = FBK.convert(new, [FBK.IMG, os.path.join(FBK.IMG, "m1280")])
        assert r, (new, why)
        swap[old] = new; swap[old.replace(".jpg", "f.jpg")] = r[0]
        rows[pid] = {"pos": None, "old": new, "new": r[0], "how": r[1], "src": "person v 10/19(연도 칸)"}
    if B.PREVIEW: return [t[1] for t in T]
    pat = re.compile("|".join(re.escape(k) for k in sorted(swap, key=len, reverse=True)))
    sub = lambda s: pat.sub(lambda m: swap[m.group(0)], s)
    # pages.json
    pg = os.path.join(HERE, "pages.json"); s = open(pg, encoding="utf-8").read(); n1 = len(pat.findall(s))
    open(pg, "w", encoding="utf-8").write(sub(s))
    # fullbleed_plan.json
    fp = os.path.join(HERE, "fullbleed_plan.json"); plan_ = json.load(open(fp, encoding="utf-8"))
    for pid, row in rows.items():
        if row["old"] not in {x.get("old") for x in plan_.get(pid, [])}: plan_.setdefault(pid, []).append(row)
    json.dump(plan_, open(fp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    # 승인 카드 이미지 목록
    rp = os.path.join(ROOT, "content", "reel_swaps.json"); s = open(rp, encoding="utf-8").read(); n2 = len(pat.findall(s))
    open(rp, "w", encoding="utf-8").write(sub(s))
    return {"그림": swap, "pages.json": n1, "reel_swaps.json": n2}


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=1))
