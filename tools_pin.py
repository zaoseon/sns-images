"""승인 카드의 그림·영상 주소 가운데 '안 열리는 것만' 고친다.

10/16 두 번 틀렸다. ① 옛 커밋 번호의 앞 12자만 갈아 끼워 없는 주소를 만들었다.
② 그림을 커밋하기 전의 번호로 주소를 적었다. 둘 다 대표 화면엔 빈 칸으로만 보인다.
번호를 손으로 넣지 말고 이 도구를 쓴다. 살아 있는 주소는 건드리지 않는다 —
대표가 이미 승인한 카드의 그림이 조용히 바뀌면 안 되기 때문이다.

사용: python3 tools_pin.py        고치고 확인
      python3 tools_pin.py --check  확인만 (커밋 전에 돌린다)
      python3 tools_pin.py ig1016   이름에 ig1016 이 든 그림은 지금 판으로 다시 맞춘다

고른 것만 다시 맞추는 까닭: 주소가 열린다고 지금 그림인 건 아니다. 옛 커밋에도
같은 이름의 예전 그림이 들어 있어 404 가 안 난다. 그렇다고 전부 최신으로 끌어오면
대표가 이미 승인한 옛 카드의 그림까지 조용히 바뀐다. 그래서 이번에 다시 그린 것만
이름으로 골라 맞춘다.
"""
import re, subprocess, sys, urllib.request, os, urllib.parse
ROOT = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(ROOT, "content", "reel_swaps.json")
RAW = "https://raw.githubusercontent.com/zaoseon/sns-images/"
패턴 = re.compile(re.escape(RAW) + r"([0-9a-f]{40})/([^\"\s]+)")


def 열리나(u):
    try:
        urllib.request.urlopen(urllib.request.Request(u, method="HEAD"), timeout=15); return True
    except Exception:
        return False


def 파일커밋(path):
    p = urllib.parse.unquote(path)
    return subprocess.run(["git", "-C", ROOT, "log", "-1", "--format=%H", "--", p],
                          capture_output=True, text=True).stdout.strip()


s = open(P, encoding="utf-8").read()
검사만 = "--check" in sys.argv
def 낡았나(sha, path):
    """주소가 가리키는 커밋의 파일이 지금 저장소 파일과 다른가.
    404 만 보면 못 잡는다 — 옛 커밋에도 같은 이름의 '예전 그림' 이 들어 있어서
    주소는 멀쩡히 열리고 대표만 옛 그림을 본다(10/16)."""
    g = lambda r: subprocess.run(["git", "-C", ROOT, "rev-parse", r], capture_output=True, text=True).stdout.strip()
    옛, 지금 = g(sha + ":" + urllib.parse.unquote(path)), g("HEAD:" + urllib.parse.unquote(path))
    return bool(옛) and bool(지금) and 옛 != 지금

고를것 = [a for a in sys.argv[1:] if not a.startswith("--")]
죽은 = []
for m in 패턴.finditer(s):
    u, sha, path = m.group(0), m.group(1), m.group(2)
    if not 열리나(u):
        죽은.append((u, path))                      # 안 열리는 것은 늘 고친다
    elif 고를것 and any(k in path for k in 고를것) and 낡았나(sha, path):
        죽은.append((u, path))                      # 고른 카드가 옛 그림을 가리키면 고친다
고침, 남은 = 0, []
for u, path in dict.fromkeys(죽은):
    sha = 파일커밋(path)
    새 = RAW + sha + "/" + path if sha else ""
    if 새 and 열리나(새):
        if not 검사만: s = s.replace(u, 새); 고침 += 1
        else: 남은.append((u, "고칠 수 있음 -> " + sha[:12]))
    else:
        남은.append((u, "저장소에 그 파일이 없어요" if not sha else "커밋해 올린 뒤 다시 돌리세요"))
if 고침: open(P, "w", encoding="utf-8").write(s)
print(f"손댈 주소 {len(dict.fromkeys(죽은))}개(안 열림 + 고른 카드의 옛 그림) 중 {고침}개 고침")
if 남은:
    print("\n[!] 아직 안 열리는 주소 — 대표 화면엔 빈 칸으로 보입니다:")
    for u, 왜 in 남은: print("   ", 왜, "\n     ", u)
    sys.exit(1)
print("모든 주소 열림 ✓")
