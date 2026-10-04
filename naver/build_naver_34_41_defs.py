"""네이버 34~37편 (10/18~10/22 12:00 칸, 10/4 새벽 대표 "계속"). 상황·감정 단위 주제, 운명학은 글마다 다르게.
n34·n37 = 세 풀이(cross), n35·n36 = 자미두수·당사주(free). 정의부는 build_naver_16_22.py 를 그대로 쓴다.
쓰는 사실: 명궁·신궁·당사주 4성 자리는 docs/당사주_하락이수_기준자료_2026-10-03.md 와 engine/ziwei.py 에서 확인한 범위만."""
import os, sys, re, json, datetime as D
from urllib.parse import quote
HERE0 = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE0, "build_naver_16_22.py"), encoding="utf-8").read()
exec(compile(src.split("# ---- 16편")[0], "defs", "exec"), globals())
CAT = "태어난 날(일주) 이야기"
REL = ("n01", "내년 내 운세는 어떨까요? 미리 준비하는 2027년 띠별 운세")

def free(no, date, time, face, el, mark, title, hero2, kicker, scene, summary, read, results, count_h, count_lines, same, diff, actions, faq, tags, trow, arow, related, sections=None):
    """세 풀이가 아닌 글: 읽는 법(read)과 결과(results)를 글마다 다르게 쓴다."""
    key = f"{no:02d}"; pre = f"naver_z{key}"
    N.hero(f"{OUT}/{pre}_a.jpg", el, kicker, hero2, "여러 풀이를 겹쳐 읽었어요", mark, face)
    N.theme(el); N.table(f"{OUT}/{pre}_b.jpg", "풀이로 보면", ["풀이", "나온 값", "한 줄"], trow, [180, 400, 320])
    N.theme(el); N.rows(f"{OUT}/{pre}_c.jpg", "이번에 해 볼 것", arow)
    body = (P(scene, f"<b>{title.split(',')[0]}</b>에 대해 여러 풀이로 읽어 봤어요. 안녕하세요, 자오선의 정월이에요.") + IMG(f"{pre}_a.jpg") +
     P("바쁘신 분들을 위해 결론부터 말씀드릴게요.") + P(*summary) +
     P("<b>📌 이 글의 순서</b>", "1. 이 풀이는 이렇게 읽어요", "2. 풀이로 본 결과", "3. " + count_h, "4. 같은 말을 하는 곳, 다른 말을 하는 곳", "5. 이번에 해 볼 것", "6. 자주 묻는 질문") +
     H("1. 이 풀이는 이렇게 읽어요") + read +
     H("2. 풀이로 본 결과") + IMG(f"{pre}_b.jpg") + results +
     H("3. " + count_h) + P(*count_lines) +
     H("4. 같은 말을 하는 곳, 다른 말을 하는 곳") + P(*same) + P(*diff) +
     H("5. 이번에 해 볼 것") + IMG(f"{pre}_c.jpg") + P(*actions) +
     H("6. 자주 묻는 질문") + "".join(P(f"<b>Q. {q}</b>", f"A. {a}") for q, a in faq) +
     END + P("나는 어느 쪽에 가까운지 댓글로 남겨 주세요. 떠오르는 사람이 있다면 이 글을 공유해 주세요.") + SEAL)
    POSTS.append(dict(no=no, date=date, time=time, title=title, tags=tags, related=related, body=body))
