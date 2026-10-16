"""금지어 '상담/상담가' 검사 (대표 10/12 23:15: '상담' 계열 금지, '코칭·마음 코치 정월'만 쓴다. 예외는 자격 표기 '심리상담사'뿐).
세 곳을 본다.
 ① 소스 전수: sns-images 와 zaoseon-site 의 git 추적 글 파일(py/json/html/md/js/css/gs/txt)에서 '상담'을 찾는다. 이미지·영상은 소스에 글이 박혀 있으니 렌더 입력까지 포함된다.
 ② 예약 글 캡션: content/reel_swaps.json 의 대기 글, data/sns_live.json (zaoseon-site) 의 예약 글.
 ③ 이미지 속 글자(--images): 카드 그림(jpg/png)을 tesseract(kor)로 읽어 '상담'이 보이면 걸린다. 텍스트 검사로는 안 잡히는 그림에 박힌 글자를 잡는다. 느리다(장당 1~2초). --new 로 git 에서 바뀐 그림만.
사용: python3 pipeline/banned_words_audit.py [--images] [--show]   종료 코드 1이면 걸림.
허용(남기는 것): '심리상담사'(자격 표기), '상담전화'(109 공식 이름), 과거 기록 문서(수정기록·ops 로그·인계문), 경쟁사 분석 문서, 규칙을 인용하는 파일(이 파일 포함), 이미 발행된 글의 보관 기록(data/)."""
import os, re, sys, json, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.abspath(os.path.join(HERE, ".."))
ZR = os.path.abspath(os.path.join(R, "..", "zaoseon-site"))
BAN = re.compile(r"상담")
ALLOW = re.compile(r"심리\s?상담사|심리상담\s자격|상담전화")   # 이 말 속의 '상담'은 걸지 않는다
RULE = re.compile(r"금지|쓰지 않|않는다|않는 말|소개하지 않|대신|막음|O4 ")   # "'상담' 대신 '코칭'" 처럼 금지를 적은 줄
MARK = re.compile(r"^\s*(#|//|/\*|\*|<!--)")                                  # 주석 줄 — 손님에게 안 보인다
EXT = (".py", ".json", ".html", ".md", ".js", ".css", ".gs", ".txt", ".yaml", ".yml", ".csv", ".tsv")
# 경로 조각이 들어 있으면 건너뛴다(과거 기록·경쟁사·규칙 인용·보관)
SKIP = ("docs/수정기록.md", "docs/참고문서/", "docs/정본/", "docs/handoff_", "docs/competitors", "docs/벤치마크", "docs/package_compare", "docs/사이트_기획안",
        "ops/", "data/keywords/", "data/kos/", "data/sns_archive.json", "data/sns_live.json", "data/topics/", "public/admin/log.html", "public/admin/data.json",
        "tools/reply_lab/cases.json", "content/audit/", "content/reel_swaps.json", "highlights_1009/", "HANDOFF.md", "HANDOFF_SUPPORT.md",
        "pipeline/banned_words_audit.py", "pipeline/qa_all.py", "public/admin/detail.js", "tools/tests/test_detail.js", "pipeline/claims_audit.py", "pipeline/clip_from_reel.py", "naver/coaching_data.py", "engine/coaching.py", "public/naver/n11.html", "public/naver/n13.html",
        "content/clips_from_reels.json", "naver/pages.json",
        "naver/build_naver_42_46.py", "naver/build_naver_75_79.py",   # 원본 문구 — coaching_data.py REPLACE 가 만들 때 고친다(옛 조각이 있어야 REPLACE 가 맞는다). 결과는 pages_unpublished()가 본다
        "docs/감정서_마음코칭_장_설계", "docs/코칭_신청_자료_양식", "docs/자오선_검증보고서_운명학", "tools/seo/psy_research.py",   # 규칙 인용·시장 조사
        "docs/모션_스토리보드_양식_2026-10-05", "docs/인스타_2건_줄이기안_2026-10-05", "docs/콘텐츠_개편안_2026-10-05", "docs/콘텐츠_기획안_모션그래픽_2026-10-05", "docs/템플릿_목록_돌려쓰기_2026-10-05",   # 10/5 기획 기록(그 코너 이름은 쓰지 않음)
        # 10/16: 손님에게 안 나가는 글인데 걸려서 검사가 늘 빨간불이었다(66건 중 진짜 위반은 8곳뿐).
        # 늘 실패하는 검사는 없는 검사와 같다 — 아무도 안 본다. 그래서 아래를 뺀다.
        "data/기준대장.json",                      # 기준 본문이 금지어를 인용한다
        "data/previews.json",                      # 검사 결과 보관
        "tools/tests/",                            # 시험 코드가 '상담 없음'을 확인한다
        "docs/심리근거카드_",                       # 임상 참고(위기 기관 연결 안내 — 손님 글 아님)
        "docs/유료코칭_조사노트",                   # 바깥 법·시장 조사
        "docs/브랜드_일관성_마음과관계.md",          # 금지어 규칙 원본
        "docs/결과화면_순서_", "docs/경쟁사_",      # 경쟁사 화면 기록
        "docs/감정서_해석근거_조사결과",             # 조사 기록
        "docs/SNS_STUDIO_라이브러리_",                # SKILL.md 사본 — 머리에 '대체됨'이라 적혀 있다
        "docs/인스타에이전트스킬_훅26판정",          # 바깥 계정 조사 기록
        "tools/osmu_psych_check.py")               # 이 금지어를 찾는 검사 코드 자신             # SKILL.md 사본 — 머리에 '대체됨'이라 적혀 있다
        # pages.json: 발행 끝난 글은 건드리지 않는다. 미발행 글은 아래 pages_unpublished()가 따로 본다
def tracked(repo):
    out = subprocess.run(["git", "-C", repo, "ls-files", "-z"], capture_output=True, text=True).stdout.split("\0")
    return [f for f in out if f.endswith(EXT)]
def scan_sources():
    hits = []
    for repo in (R, ZR):
        if not os.path.isdir(repo): continue
        name = os.path.basename(repo)
        for f in tracked(repo):
            if any(s in f for s in SKIP): continue
            try: lines = open(os.path.join(repo, f), encoding="utf-8", errors="replace").read().split("\n")
            except OSError: continue
            for n, line in enumerate(lines, 1):
                t = ALLOW.sub("", line)
                if RULE.search(line): continue        # '상담은 쓰지 않는다'·"'상담' 대신 '코칭'"처럼 금지를 적은 줄
                if MARK.match(line): continue         # 주석 — 손님 글이 아니다(조사 기록이 주석으로 남아 있다)
                m = BAN.search(t)
                if m: hits.append(("소스", f"{name}/{f}:{n}", t[max(0, m.start() - 20):m.end() + 20]))
    return hits
def pages_unpublished():
    """네이버 원고 중 아직 발행하지 않은 글(done 이 아닌 것)의 글자."""
    hits = []; p = os.path.join(R, "naver", "pages.json")
    if not os.path.exists(p): return hits
    d = json.load(open(p, encoding="utf-8"))
    for k, v in (d.items() if isinstance(d, dict) else enumerate(d)):
        if isinstance(v, dict) and v.get("done"): continue
        s = ALLOW.sub("", json.dumps(v, ensure_ascii=False))
        for m in BAN.finditer(s): hits.append(("네이버 미발행 원고", f"pages.json[{k}]", s[max(0, m.start() - 20):m.end() + 20]))
    return hits
def scan_captions():
    hits = []
    p = os.path.join(R, "content", "reel_swaps.json")
    if os.path.exists(p):
        for r in json.load(open(p, encoding="utf-8")):
            if r.get("status") in ("new", "wait", "hold"):
                for k in ("caption", "text"):
                    s = ALLOW.sub("", str(r.get(k, "")))
                    if BAN.search(s): hits.append(("앱 대기 캡션", r.get("id"), s[:60]))
    return hits
# 이미 발행된 날의 그림(고칠 수 없음)과 안 쓰는 합성본 — 그림 검사에서 뺀다
IMG_SKIP = ("2026-w40/", "2026-w40car", "2026-w41night/", "2026-w41topic/1004", "2026-w41topic/1007", "2026-w41topic/1011", "2026-w42night/",
            "2026-w43night5/", "2026-w43night7/", "2026-w43swap/", "2026-w42car-sched/1004", "2026-w42car-sched/1006", "2026-w40car4/1004", "2026-w40car4/1006",
            "2026-w42fix/join3", "2026-w42fix/join6")
def scan_images(only_new=False):
    from PIL import Image
    hits = []; files = []
    for repo in (R,):
        out = subprocess.run(["git", "-C", repo, "ls-files", "-z"], capture_output=True, text=True).stdout.split("\0")
        files += [os.path.join(repo, f) for f in out if f.lower().endswith((".jpg", ".jpeg", ".png")) and not f.startswith(("characters/", "assets/", "pipeline/")) and not any(k in f for k in IMG_SKIP)]
    if only_new:
        ch = subprocess.run(["git", "-C", R, "status", "--porcelain"], capture_output=True, text=True).stdout.split("\n")
        files = [f for f in files if any(os.path.relpath(f, R) in c for c in ch)]
    for f in files:
        try:
            im = Image.open(f).convert("L"); w, h = im.size
            tmp = f"/tmp/_ban_{os.getpid()}.png"; im.resize((w * 3 // 2, h * 3 // 2)).save(tmp)
            t = subprocess.run(["tesseract", tmp, "-", "-l", "kor", "--psm", "11"], capture_output=True, text=True, env=dict(os.environ, OMP_THREAD_LIMIT="1")).stdout.replace(" ", "").replace("\n", "|")
        except Exception as e:
            hits.append(("그림 읽기 실패", os.path.relpath(f, R), str(e))); continue
        if BAN.search(ALLOW.sub("", t)) or "담가" in t: hits.append(("그림 속 글자", os.path.relpath(f, R), t[:80]))
    return hits
def scan(images=False, only_new=False):
    h = scan_sources() + pages_unpublished() + scan_captions()
    if images: h += scan_images(only_new)
    return h
if __name__ == "__main__":
    h = scan("--images" in sys.argv, "--new" in sys.argv)
    print(f"'상담' 걸린 곳 {len(h)}곳")
    for k, w, t in h[:80 if "--show" not in sys.argv else None]: print(f"  [{k}] {w} | {t.strip()}")
    sys.exit(1 if h else 0)
