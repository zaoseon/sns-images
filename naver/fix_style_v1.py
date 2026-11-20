"""대기표에 이미 들어간 새 원고를 문체 규격 v1(대표 11/20 14:55 "네이버 블로그 … 다 적용")에 맞춰 고친다 — ① 11/20 19:45.
- 왜: n93~n102 원고는 14:55 전에 관문을 지나 대기표(zaoseon-site public/naver/queue.json)에 들어갔는데, 지금 관문(naver_queue_add --check)이 막는다.
  막는 것: ① 목차 줄과 소제목 줄이 같은 문장(RP-01) ② 추상어·번역투(기운·흐름·에 있어 …).
- 하는 일: pages.json body 에서 목차(📌 묶음 안 굵지 않은 'N. …' 줄)를 짧은 이름으로 바꾸고, 문장 바꿈 표(FIX)를 한 번씩만 적용한 뒤
  dt·제목·태그·연결글은 그대로 두고 사이트 원고 페이지(make_page.write_page)를 다시 만든다. 그림은 건드리지 않는다.
- 주의: build_naver_NN.py 를 다시 돌리면 옛 문장으로 돌아간다. 다시 돌릴 일이 있으면 이 파일의 FIX 를 그 스크립트에도 옮긴다.
사용: SITE=<zaoseon-site> python3 naver/fix_style_v1.py n97 n96"""
import os, sys, json, re, datetime as D
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "pipeline")); os.chdir(HERE)
import make_page as MP

TOC = {   # 목차 짧은 이름(소제목 질문은 그대로)
    "n97": ["별자리 운세가 보는 것", "해마다 바뀌는 별자리 날짜", "별자리 경계와 절기", "별자리 운세 읽는 순서", "읽고 나서 해 볼 것", "묻고 답하기"],
    "n96": ["다시 생각나는 마음", "사주에서 연인을 보는 글자", "2027년 재회운 글자", "1995년 3월 16일생 예시", "연락하기 전 확인할 것", "묻고 답하기"],
    "n95": ["양과 부딪히는 2027년", "소띠 나이와 1월생", "창고에서 꺼낼 것", "움직일 달과 쉬어 갈 달", "태어난 해별로 받는 것", "새 출발 효과", "묻고 답하기"],
    "n98": ["먼저 우는 사람", "울고 난 뒤의 마음", "사주로 보는 눈물", "1993년 11월 24일생 예시", "눈물이 많을 때 해 볼 것", "묻고 답하기"],
    "n93": ["서운함이 터지는 이유", "창고 글자 네 개", "1995년 1월 10일생 예시", "한꺼번에 나오는 날", "참는 것과 관계", "터지기 전에 해 볼 것", "묻고 답하기"],
}
FIX = {   # (옛 문장 조각, 새 문장 조각) — 정확히 한 번 나와야 한다
    "n97": [("한 해와 한 달의 흐름을 읽는 풀이예요.", "한 해와 한 달에 무엇을 하기 좋은지 읽는 풀이예요.")],
    "n96": [("다시 연락할지 정하는 기준은 사주보다 헤어진 이유에 있어요.", "다시 연락할지 정할 때는 사주보다 헤어진 이유를 먼저 보세요.")],
    "n95": [("그 전 1월까지는 2026년 병오년 기운으로 봐요.", "그 전 1월까지는 2026년 병오년으로 봐요.")],
    "n98": [("예민한 게 아니라 따로 있는 기질이라는 뜻이에요.", "예민한 게 아니에요. 따로 있는 기질이에요."),
            ("감정과 생각이 깊이 흐르는 기운으로 봐요.", "한 번 든 감정과 생각이 오래 남는다고 봐요.")],
    "n93": [("창고 글자는 지나간 계절의 기운을 모아 두는 글자예요.", "창고 글자는 지나간 계절의 글자를 속에 모아 두는 글자예요."),
            ("창고에 넣어 두는 편이에요.", "창고에 넣어 둬요.")],
}

def fix(pid, v):
    b = v["body"]; i = b.find("📌"); assert i > 0, pid
    j = b.find("<p>&nbsp;</p>", i); assert j > 0
    blk = b[i:j]; olds = re.findall(r"<p>(\d)\. ([^<]+)</p>", blk)
    assert len(olds) == len(TOC[pid]), (pid, olds)
    for (n, q), s in zip(olds, TOC[pid]):
        assert f"<p><b>{n}. {q}</b></p>" in b, (pid, q)          # 소제목은 질문 그대로 남는다
        blk = blk.replace(f"<p>{n}. {q}</p>", f"<p>{n}. {s}</p>", 1)
    b = b[:i] + blk + b[j:]
    for o, n in FIX.get(pid, []):
        assert b.count(o) == 1, (pid, o, b.count(o)); b = b.replace(o, n)
    return b

if __name__ == "__main__":
    reg = json.load(open(MP.REG, encoding="utf-8"))
    for pid in sys.argv[1:]:
        v = reg[pid]; assert not v.get("done"), f"{pid} 이미 예약 끝난 글 — 키트로 고쳐야 한다"
        v["body"] = fix(pid, v); v["style_v1"] = "11/20 19:45 ① fix_style_v1(목차 짧은 이름·문장 바꿈)"
        MP.write_page(pid, D.datetime.fromisoformat(v["dt"]), v["title"], v["tags"], v["body"], None, v["cover"], v["related"], v["category"])
        print(pid, "고침")
    json.dump(reg, open(MP.REG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    MP.write_index()
