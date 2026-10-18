"""스레드 글 검사(K-136, 대표 10/17 23:05·23:08 + 10/18 07:53 "스레드는 스레드 문법이 맞는 것 같아").

규칙 원본: zaoseon-site docs/스레드_말투_본보기_2026-10-17.md 맨 위 '확정 규칙: 피드 문법', docs/스레드_소통_규칙_2026-10-17.md.
인스타 캡션 검사(capfix.check)는 해요체·팔로우 줄·브랜드 두 줄·태그 5개를 **요구**한다. 스레드는 반대라서 스레드 글에는
capfix.check 를 쓰지 않고 이 검사를 쓴다(CT 10/18 08:00 요청 ②: 스레드 전용 검사로 나눈다).

걸리는 까닭(코드):
  T1 500자 넘음                         T2 해시태그가 1개가 아님(스레드 1, copy_rules.해시태그수)
  T3 면책 문장('재미로…', K-128)         T4 프로필 링크 2번 이상
  T5 첫 줄이 물음표로 끝남(K-107) / 첫 줄 체계 이름·금지어(K-102, copy_rules.첫줄검사)
  T6 인스타 고정 문구를 그대로 옮김(브랜드 두 줄·'매일 저녁 테스트'·'팔로우해 두면') — 규칙 1번
  T7 해요체가 문장 끝의 절반 넘음(반말 기본, 확정 규칙 1번)
  T8 행동 유도 줄이 2줄 넘음(♥·태그 한 줄 + 프로필 링크 한 번, 확정 규칙 5번)
  T9 한 줄이 45자 넘음(한 줄에 한마디, 확정 규칙 4번)
  T10 끝 세 줄에 질문·어울림 말이 없음(끝은 어울림 한 줄, 확정 규칙 5번)
사용: python3 pipeline/thread_rules.py "글"      (한 편 검사)
      python3 pipeline/thread_rules.py --queue   (앱 승인 대기 스레드 글 전부)"""
import os, re, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
import copy_rules as CR
from capfix import DISC_RE

MAX_LEN = 500
LINE_MAX = 45
INSTA_FIXED = ("사주 하나, 별자리 하나만 보면", "자오선은 여섯 가지 운명학을 겹쳐서",
               "매일 저녁, 나를 알아보는 테스트", "매일 저녁 테스트가 올라와요", "팔로우해 두면", "팔로우하고 더 많은")
CTA = re.compile(r"♥|하트|태그|공유|팔로우|프로필 링크")
TOGETHER = re.compile(r"[?？]|같이|함께|스하리|반하리|댓글|알려 ?줘|남겨 ?줘")
# 인사·고지 줄은 해요체 비율에서 뺀다(확정 규칙 1번: 정중한 말은 인사에만)
GREET = re.compile(r"고마워|감사|좋은 아침|안녕|반가워|정월이에요|정월이야")


def _lines(t):
    return [l.strip() for l in t.split("\n") if l.strip()]


def check(t):
    bad = []
    ls = _lines(t)
    if not ls:
        return ["빈 글"]
    if len(t) > MAX_LEN: bad.append(f"T1({len(t)}자)")
    tags = re.findall(r"(?:^|\s)(#[^\s#]+)", t)
    if len(tags) != CR.해시태그수["threads"]: bad.append(f"T2({len(tags)}개)")
    if DISC_RE.search(t) or re.search(r"재미로 즐기는|이 내용은 재미로", t): bad.append("T3")
    if len(re.findall("프로필 링크", t)) > 1: bad.append("T4")
    first = ls[0]
    if first.rstrip().endswith(("?", "？")): bad.append("T5(첫 줄 물음표)")
    if CR.첫줄검사(first): bad.append("T5(첫 줄 체계 이름·금지어)")
    if any(k in t for k in INSTA_FIXED): bad.append("T6")
    body = [l for l in ls if not l.startswith("#")]
    ends = [l for l in body if not GREET.search(l)]
    yo = sum(1 for l in ends if re.search(r"요[.!?~…ㅎㅠㅜ\s♥!]*$", re.sub(r"[\U0001F300-\U0001FAFF☀-➿]", "", l)))
    if ends and yo * 2 > len(ends): bad.append(f"T7(해요체 {yo}/{len(ends)}줄)")
    if sum(1 for l in body if CTA.search(l)) > 2: bad.append("T8")
    if any(len(l) > LINE_MAX for l in body): bad.append("T9")
    if not any(TOGETHER.search(l) for l in body[-3:]): bad.append("T10")
    return bad


def queue():
    """앱 승인 대기(new·wait·hold) 중 스레드에 나갈 글. 스레드만 가는 카드는 caption, 둘 다 가는 카드는 caption_threads."""
    d = json.load(open(os.path.join(R, "content", "reel_swaps.json"), encoding="utf-8"))
    out = []
    for r in d:
        if r.get("status") not in ("new", "wait", "hold"): continue
        if r.get("since", "") < "2026-10-18": continue     # 규칙 확정(10/18 07:53) 뒤에 올린 카드부터 막는다. 그 전 카드는 빚
        ch = r.get("channels") or []
        ps = [p for p in (r.get("posts") or []) if isinstance(p, dict) and p.get("caption")]
        if ch == ["threads"] and ps:      # 여러 편 묶음 카드는 한 편씩 잰다
            out += [(f"{r['id']} {p.get('date', '')} {p.get('time', '')}", p["caption"]) for p in ps]
        elif r.get("caption_threads"): out.append((r["id"], r["caption_threads"]))
        elif ch == ["threads"] and r.get("caption"): out.append((r["id"], r["caption"]))
    return out


def run():
    return [(i, check(t)) for i, t in queue() if check(t)]


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] != "--queue":
        print(check(sys.argv[1]) or "통과")
    else:
        res = run()
        print(f"스레드 글 검사(K-136): 걸린 글 {len(res)}편")
        for i, b in res: print("  ", i, b)
