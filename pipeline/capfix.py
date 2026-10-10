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
    if any(len(l) > 70 for l in t.split("\n")): bad.append("G")
    return bad
