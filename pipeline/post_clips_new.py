"""새 규칙으로 쓴 네이버 글(n47~n79)의 게시물형 클립: 원고 이미지(a 표지 → i 한눈에 보기 → b 표 → c 이번에 해 볼 것)에 짧은 자막을 얹어 12~15초 영상으로 만든다(2026-10-11 대표 지시).
자막은 새로 쓰지 않고 naver/build_naver_*.py 의 art() 인자(표지 문구·한 줄 요약·표 제목·해 볼 것)에서 뽑는다. n64~n69(띠 글)는 pages.json 제목에서 뽑는다.
결과: clips_sop/<nNN>-p1_12s.mp4 + _thumb.png , content/post_clips_new.json.   사용: python3 pipeline/post_clips_new.py [글번호 ...]"""
import os, sys, re, ast, glob, json, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "..")); sys.path.insert(0, HERE)
from images_to_clip import images_to_clip
from post_clip_caps import CAPS, SKIP, FIRST
IMG = os.path.join(ROOT, "naver", "img"); STY = [("상큼 팝", "A"), ("발랄 우쿨렐레", "D"), ("경쾌 신스팝", "G"), ("통통 마림바", "F")]
def lit(x):
    try: return ast.literal_eval(x)
    except Exception: return None
def art_args():
    out = {}
    for f in sorted(glob.glob(os.path.join(ROOT, "naver", "build_naver_*.py"))):
        try: tree = ast.parse(open(f, encoding="utf-8").read())
        except Exception: continue
        for n in ast.walk(tree):
            if isinstance(n, ast.Call) and getattr(n.func, "id", None) == "art" and len(n.args) >= 13 and isinstance(n.args[0], ast.Constant):
                hook = None
                if isinstance(n.args[6], ast.Call):
                    for k in n.args[6].keywords:
                        if k.arg == "hook": hook = lit(k.value)
                t0 = n.args[11]; out[n.args[0].value] = dict(hook=hook, title=lit(n.args[7]), summary=lit(n.args[9]), arow=lit(n.args[12]), tags=lit(n.args[14]) if len(n.args) > 14 else None, tbl0=lit(t0.elts[0]) if isinstance(t0, ast.Tuple) else None)
    return out
def clean(s): return re.sub(r"<[^>]+>", "", s or "").strip()
def short(s, lim=34):
    s = re.sub(r"^[^\w가-힣]*", "", clean(s)); s = re.sub(r"^(한 줄 요약|해 볼 것|세 가지)\s*:\s*", "", s)
    s = re.split(r"(?<=[.요다])\s", s)[0].rstrip(".")
    if len(s) <= lim: return s
    parts = re.split(r",\s*", s); cur = ""
    for p in parts:
        if len((cur + ", " + p) if cur else p) <= lim: cur = (cur + ", " + p) if cur else p
        else: break
    return cur or s[:lim]
def captions(no, A, title):
    if no in CAPS: return list(CAPS[no])
    a = A.get(no)
    if a and a["hook"] and a["summary"]:
        sm = [clean(x) for x in a["summary"]]; one = next((x for x in sm if "한 줄 요약" in x), sm[0]); three = next((x for x in sm if "세 가지" in x), "")
        first = re.sub(r"^[^\w가-힣]*(한 줄 요약)\s*:\s*", "", one); first = re.split(r"(?<=[.요다])\s", first)[0].rstrip(".")
        if len(first) > 42 and three: first = re.sub(r"^[^\w가-힣]*", "", three).strip()
        elif len(first) > 42: first = short(first, 42)
        acts = [r[1] for r in (a.get("arow") or []) if r and r[1]]
        return [" ".join(a["hook"]), first, a["tbl0"] or short(title), "이번에 해 볼 것: " + " · ".join(acts) if acts else "이번에 해 볼 것"]
    m = re.match(r"(.+?띠 운세), (.+?) 힘 쓸", title)
    return [m.group(1), m.group(2), "힘 쓸 달과 아낄 달", "이번에 해 볼 것"] if m else [short(title), short(title), "표로 한눈에 보기", "이번에 해 볼 것"]
def build(no, A, pages):
    pid = f"{no:02d}"; names = [f"naver_z{pid}_{x}.jpg" for x in "aibc"]; paths = [os.path.join(IMG, "master", x) if os.path.exists(os.path.join(IMG, "master", x)) else os.path.join(IMG, x) for x in names]
    assert all(os.path.exists(p) for p in paths), (no, names)
    caps = captions(no, A, pages[f"n{no}"]["title"]); sty, key = STY[no % 4]; cid = f"n{no}-p1"
    out = os.path.join(ROOT, "clips_sop", f"{cid}_12s.mp4"); t = images_to_clip(out, paths, hold=2.8, first_hold=3.2, last_hold=3.6, captions=caps, style=sty, seed=300 + no, key=key)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", "0.8", "-i", out, "-frames:v", "1", os.path.join(ROOT, "clips_sop", f"{cid}_thumb.png")], check=True)
    return dict(id=cid, post=f"n{no}", title=pages[f"n{no}"]["title"], captions=caps, style=sty, sec=round(t, 1), video=f"clips_sop/{cid}_12s.mp4")
def sentence(x):
    x = re.sub(r"^[^\w가-힣]*(한 줄 요약|해 볼 것|세 가지)\s*:\s*", "", clean(x)); return x if x.endswith((".", "!", "?")) else x + "."
def entry(no, A, pages, date):
    a = A.get(no) or {}; title = pages[f"n{no}"]["title"]; caps = captions(no, A, title); fl = lambda x: x.replace("\n", " "); sm = [clean(x) for x in (a.get("summary") or [])]
    one = next((sentence(x) for x in sm if "한 줄 요약" in x), ""); todo = next((sentence(x) for x in sm if "해 볼 것" in x), "")
    if not one:
        m = re.match(r"(.+?띠 운세), (.+?) 힘 쓸", title); one = f"{m.group(1)}, {m.group(2)}." if m else sentence(title); todo = "힘 쓸 달과 아낄 달을 표로 정리했어요. 힘 쓸 달 하나에 표시해 두세요."
    tags = [t.replace(" ", "") for t in (a.get("tags") or [])][:4]
    if not tags:
        mm = re.search(r"(\S+?띠) 운세", title); z = mm.group(1) if mm else "띠"; tags = ["사주", "2027년운세", z + "운세", "띠별운세"]
    tags = (tags + ["자오선"]) if "자오선" not in tags else tags
    return dict(date=date, id=f"n{no}-p1", post=f"n{no}", type="게시물형(블로그 이미지+캡션)", kicker="글 요약 · " + fl(caps[0]), hook=fl(caps[0]), thumbs=[fl(caps[1]), fl(caps[2]), fl(caps[3])],
                scenes={"12": [dict(kind="hook", dur=2.5, text=fl(caps[0]))]}, desc=" ".join(x for x in (one, todo, "블로그 스티커를 누르면 전체 풀이 글로 이어져요.") if x), tags=tags)
def register(nos=None):
    pages = json.load(open(os.path.join(ROOT, "naver", "pages.json"), encoding="utf-8")); A = art_args(); nos = [n for n in (nos or range(47, 80)) if f"n{n}" in pages and n not in SKIP]
    rest = sorted([n for n in nos if n not in FIRST], key=lambda n: pages[f"n{n}"]["dt"]); nos = rest[:1] + [n for n in FIRST if n in nos] + rest[1:]; d0 = __import__("datetime").date(2026, 11, 1); res = []
    for k, n in enumerate(nos):
        d = d0 + __import__("datetime").timedelta(days=k); assert d.isoformat() > pages[f"n{n}"]["dt"][:10], n
        res.append(entry(n, A, pages, d.isoformat()))
    json.dump(res, open(os.path.join(ROOT, "content", "clips_sop_posts.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1); return res
if __name__ == "__main__" and sys.argv[1:] == ["register"]:
    r = register(); print(len(r), "개 등록", r[0]["date"], "~", r[-1]["date"]); sys.exit()
if __name__ == "__main__":
    pages = json.load(open(os.path.join(ROOT, "naver", "pages.json"), encoding="utf-8")); A = art_args()
    nos = [int(x) for x in sys.argv[1:]] or [n for n in range(47, 80) if f"n{n}" in pages]
    f = os.path.join(ROOT, "content", "post_clips_new.json"); res = {r["id"]: r for r in (json.load(open(f, encoding="utf-8")) if os.path.exists(f) else [])}
    for n in nos:
        r = build(n, A, pages); res[r["id"]] = r; print(r["id"], r["sec"], "s", r["captions"])
    json.dump(list(res.values()), open(f, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
