import re, json, glob, sys
ACTION = "맞으면 ♥, 떠오르는 사람이 있으면 공유하거나 태그해 주세요."
FOLLOW = "매일 저녁, 나를 알아보는 테스트가 올라와요. 팔로우해 두면 다음 편을 놓치지 않아요."
PROFILE = "내 태어난 날의 기운은 프로필 링크에서 생년월일만 넣으면 1초면 볼 수 있어요."
BRAND = ["사주 하나, 별자리 하나만 보면 한쪽 이야기만 듣게 돼요.", "자오선은 여섯 가지 운명학을 겹쳐서, 같은 답이 나오는 곳을 찾아요."]
DISC = "이 내용은 재미로, 그리고 나를 돌아보는 계기로 봐 주세요."
CTA_RE = re.compile(r"프로필 링크|팔로우|저장해|♥|하트|공유|태그|매일 저녁, 나를")
def sents(line):
    return [s for s in re.split(r"(?<=[.?!])\s+", line.strip()) if s]
def split_long(s, lim=60):
    if len(s) <= lim: return [s]
    if ", " in s:
        parts = s.split(", "); best=None
        for i in range(1, len(parts)):
            a = ", ".join(parts[:i]) + ","; b = ", ".join(parts[i:])
            d = abs(len(a) - len(b))
            if best is None or d < best[0]: best = (d, a, b)
        return split_long(best[1], lim) + split_long(best[2], lim)
    return [s]
def rebuild(text):
    raw = text.split("\n")
    tagline = ""
    while raw and not raw[-1].strip(): raw.pop()
    if raw and raw[-1].lstrip().startswith("#") and re.match(r"^(#\S+\s*)+$", raw[-1].strip()):
        tagline = raw.pop().strip()
    tags = tagline.split()
    profile = None; teaser = None; body = []
    for ln in raw:
        if not ln.strip(): body.append(""); continue
        if BRAND[0][:12] in ln or "자오선은 여섯 가지 운명학을 겹쳐서" in ln: continue
        if "이 내용은 재미로" in ln and "※" not in ln: continue
        if ln.strip() == "재미와 자기 이해를 위한 참고로 봐 주세요.": continue
        keep = []
        for s in sents(ln):
            m = re.search(r"내일 저녁: ([^.]+)\.", s)
            if m: teaser = m.group(1)
            if "프로필 링크" in s and profile is None and "무료 풀이에서는" not in s:
                profile = s if s.endswith((".", "요", "다")) else s
                continue
            if CTA_RE.search(s) and not ("번호" in s and "댓글" in s) and not s.startswith("※"):
                continue
            keep.append(s)
        if keep: body.append(keep)
    # flatten: each kept sentence group -> lines
    out = []
    for item in body:
        if item == "": out.append(""); continue
        for s in item:
            out.extend(split_long(s))
    # collapse blank runs, strip edges
    res = []
    for l in out:
        if l == "" and (not res or res[-1] == ""): continue
        res.append(l)
    while res and res[-1] == "": res.pop()
    # tags: exactly 5, #사주 #운세 first
    topic = [t for t in tags if t not in ("#사주", "#운세")]
    for pad in ("#자오선", "#별자리", "#성격"):
        if len(topic) < 3 and pad not in topic: topic.append(pad)
    final_tags = ["#사주", "#운세"] + topic[:3]
    blocks = ["\n".join(res)]
    act = [ACTION]
    if teaser: act.append("내일 저녁: " + teaser + ".")
    act.append(FOLLOW); act.append(profile or PROFILE)
    blocks.append("\n".join(act))
    blocks.append("\n".join(BRAND))
    blocks.append(DISC)
    blocks.append(" ".join(final_tags))
    return "\n\n".join(b for b in blocks if b.strip())
def check(t):
    pl = len(re.findall(r"프로필 링크", t)); bad=[]
    if pl != 1: bad.append(f"A{pl}")
    if "팔로우" not in t: bad.append("B")
    if not (("♥" in t or "하트" in t) and ("태그" in t or "공유" in t)): bad.append("C")
    if "사주 하나, 별자리 하나만 보면" not in t: bad.append("D")
    if "재미로" not in t: bad.append("E")
    tg = re.findall(r"(?:^|\s)(#[^\s#]+)", t.split("\n")[-1]);
    if len(tg) != 5 or "#사주" not in tg or "#운세" not in tg: bad.append("F")
    if t.count("재미와 자기 이해를 위한 참고로") + t.count("재미로, 그리고 나를 돌아보는") > 1: bad.append("I")
    if sum(1 for l in t.split("\n") if "♥" in l) > 1: bad.append("H")
    body = [l for l in t.split("\n") if l.strip() and not l.startswith("#")]
    if any(l.rstrip().endswith((",", "을", "를", "은", "는", "과", "와")) for l in body): bad.append("J")      # 문장이 다음 줄로 이어짐(의미 단위 위반)
    if re.search(r"이라면 이야기예요|안쪽 생각|감각이 큰 사람|한 줄로는 '", t): bad.append("K")                   # 어색한 말(R26)
    if any(len(l) > 60 for l in body): bad.append("L")
    if any(len(l) > 70 for l in t.split("\n")): bad.append("G")
    bad += 앞부분(t)
    return bad


FEED_CUT = 125        # 피드에서 '... 더 보기' 앞에 보이는 글자 수(대표 10/16 레퍼런스 instagram-agent-skill)
_고정 = ("사주 하나, 별자리 하나만 보면", "자오선은 여섯 가지 운명학을 겹쳐서",
         "재미로", "재미와 자기 이해를", "팔로우하고 더 많은", "팔로우해 두면",
         "맞으면 ♥", "맞다 싶으면 ♥", "프로필 링크")


def 앞부분(t):
    """피드에 보이는 앞 125자만 따로 검사한다.

    사람들은 캡션 전체를 안 본다 — '... 더 보기' 앞의 앞부분만 보고 누를지 만다.
    그 자리에 고정 문구(브랜드 두 줄·재미로·팔로우·프로필 링크)가 들어가면 훅 자리를 잡아먹는다.
    M: 앞 125자에 고정 문구가 있다
    N: 앞 125자 안에서 문장이 하나도 안 끝난다 — 보이는 자리가 토막이라 무슨 말인지 모른다

    N 은 '첫 줄이 길다'가 아니다. 줄이 길어도 125자 안에서 문장 하나가 끝나면 읽는 사람은
    온전한 한 마디를 본다. 반대로 짧은 줄이라도 125자까지 문장이 안 끝나면 토막만 보인다.
    """
    bad = []
    앞 = t[:FEED_CUT]
    if any(k in 앞 for k in _고정):
        bad.append("M")
    if not re.search(r"[.!?？！…]|[다요]\s*$|[다요][\s\n]", 앞):
        bad.append("N")
    return bad
