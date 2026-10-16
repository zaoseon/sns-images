#!/usr/bin/env python3
"""콘텐츠 기획 전에 반드시 먼저 돌린다.
이미 있는 글·예약을 안 보고 기획하는 일을 막는다.

  python3 naver/precheck_plan.py                 # 현황과 진짜 빈칸만 출력
  python3 naver/precheck_plan.py "제목1" "제목2"  # 제안한 제목이 중복인지 검사

규칙 근거: 대표 10/7 지시 "새 콘텐츠를 만들기 전에 기존 일정·전체 균형을 먼저
고려할 것", 10/15 재발 "이미 있는 글을 빈칸이라고 올림".
"""
import json, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

띠 = ["쥐", "소", "호랑이", "토끼", "용", "뱀", "말", "양", "원숭이", "닭", "개", "돼지"]
별자리 = ["양자리", "황소자리", "쌍둥이자리", "게자리", "사자자리", "처녀자리",
          "천칭자리", "전갈자리", "사수자리", "염소자리", "물병자리", "물고기자리"]
시즌키워드 = ["토정비결", "삼재", "이사방향", "손없는날", "정미년", "수성 역행",
              "띠 궁합", "자미두수", "당사주", "수비학", "주역", "만세력",
              "십성", "도화살", "일진", "신년 감정서"]


def load():
    rows = {}
    pub = json.loads((HERE / "published.json").read_text(encoding="utf-8"))
    for k, v in pub.items():
        rows[k] = {"title": v.get("title", ""), "date": v.get("date", ""),
                   "status": v.get("status", "")}
    pages = json.loads((HERE / "pages.json").read_text(encoding="utf-8"))
    for k, v in pages.items():
        r = rows.setdefault(k, {"title": "", "date": "", "status": ""})
        if not r["title"]:
            r["title"] = v.get("title", "")
        if not r["date"]:
            r["date"] = (v.get("dt") or "")[:10]
    return rows


def covered(rows, word):
    hits = [(k, r) for k, r in rows.items() if word in r["title"]]
    return hits


def main():
    rows = load()
    titles = {k: r["title"] for k, r in rows.items()}
    print(f"원고 {len(rows)}편 (발행·예약·작성 예정 전부)\n")

    # 날짜 점유
    by_date = {}
    for k, r in rows.items():
        if r["date"]:
            by_date.setdefault(r["date"], []).append(k)
    full = sorted(d for d, v in by_date.items() if len(v) >= 2)
    if full:
        print(f"하루 2편 이상 찬 날: {len(full)}일  ({full[0]} ~ {full[-1]})")
        print("  -> 이 구간에 새 글을 끼우려면 기존 글을 밀어야 한다. 대표 판단이 필요하다.\n")

    def block(name, words, fmt):
        have, miss = [], []
        for w in words:
            hits = covered(rows, fmt(w))
            (have if hits else miss).append(
                f"{w}({hits[0][0]} {hits[0][1]['date']})" if hits else w)
        print(f"[{name}] 있음 {len(have)}/{len(words)}")
        if miss:
            print(f"  빈칸: {', '.join(miss)}")
        else:
            print("  빈칸 없음")
        print()
        return miss

    block("12띠 2027 운세", 띠, lambda w: f"{w}띠 운세")
    block("12별자리 개별 글", 별자리, lambda w: w)
    block("시즌·지식 키워드", 시즌키워드, lambda w: w)

    # 제안 제목 검사
    props = sys.argv[1:]
    if props:
        print("=" * 56)
        print("제안한 제목 검사")
        for p in props:
            words = [w for w in p.replace(",", " ").split() if len(w) >= 2]
            hit = []
            for k, t in titles.items():
                score = sum(1 for w in words if w in t)
                if score >= 2:
                    hit.append((score, k, rows[k]["date"], t))
            hit.sort(reverse=True)
            if hit:
                s, k, d, t = hit[0]
                print(f"  중복 의심  {p}")
                print(f"             -> {k} {d} {t}")
            else:
                print(f"  새 글 맞음  {p}")
        if any(True for _ in props):
            print()
    print("이 결과를 보기 전에는 기획안을 쓰지 않는다.")


if __name__ == "__main__":
    main()
