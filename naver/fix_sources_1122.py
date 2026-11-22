"""네이버 대기표 n95부터 12편 가운데 남은 11편의 본문 '📚 출처:' 줄을 없앤다 — 대표 11/22 승인(피클 전달), n107 방식.
- 왜: 본문 중간의 📚 출처 줄과 기계적 각주가 글 흐름을 끊고 AI가 쓴 티를 낸다(대표 11/21 n107 확인).
- 어떻게: 출처 줄 문단을 지우고, 그 자료를 이미 말하고 있는 본문 낱말(연구진·백과사전·절기 이름)에 링크만 건다.
  자료 이름이 본문에 없는 네 편(n99·n100·n101·n102)은 절기 이름을 넣은 한 문장을 더해 링크를 그 자리에 건다.
- 지키는 것: K-162(공식·연구 출처 링크 2개 이상)는 그대로 — 지운 출처 줄의 링크 두 개를 본문 안 링크로 옮긴다.
  /dapjang/ 끝 배너·첫 200자 정의 문장·태그·연결글은 건드리지 않는다. n96·n107·n105 가운데 승인 지난 것도 건드리지 않는다(n105는 대상).
- 주의: build_naver_NN.py 를 다시 돌리면 옛 문장으로 돌아간다. 같이 고쳐 두었다.
사용: SITE=<zaoseon-site> python3 naver/fix_sources_1122.py n95 n98 ...
"""
import os, sys, json, re, datetime as D
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "pipeline")); os.chdir(HERE)
import make_page as MP

KASI = "https://astro.kasi.re.kr/life/pageView/5"

# (옛 문장 조각, 새 문장 조각) — 본문에 정확히 한 번만 나와야 한다
EDITS = {
    "n95": [
        # 출처 1(새 출발 효과) — 이미 연구진 이름을 말하는 문장에 링크
        ("와튼 스쿨의 다이, 밀크먼, 리스 연구진은 2014년",
         f'와튼 스쿨의 <a href="https://doi.org/10.1287/mnsc.2014.1901">다이, 밀크먼, 리스 연구진</a>은 2014년'),
        # 출처 2(음양력) — 절기 이름에 링크
        ("⭐ 5월 6일 입하부터는 뱀(巳)의 달이에요.",
         f'⭐ <a href="{KASI}">5월 6일 입하</a>부터는 뱀(巳)의 달이에요.'),
    ],
    "n98": [
        ("미국 심리학자 일레인 아론과 아서 아론은 1997년",
         f'미국 심리학자 <a href="https://doi.org/10.1037/0022-3514.73.2.345">일레인 아론과 아서 아론</a>은 1997년'),
        ("네덜란드 틸뷔르흐대 연구진이 그동안의 울음 연구를 모아 정리했어요(2014).",
         f'네덜란드 <a href="https://doi.org/10.3389/fpsyg.2014.00502">틸뷔르흐대 연구진</a>이 그동안의 울음 연구를 모아 정리했어요(2014).'),
    ],
    "n93": [
        ("스탠퍼드 대학의 버틀러·그로스 연구진은 처음 만난 여성",
         f'스탠퍼드 대학의 <a href="https://doi.org/10.1037/1528-3542.3.1.48">버틀러·그로스 연구진</a>은 처음 만난 여성'),
        ("그로스가 함께한 스리바스타바 연구진은 대학 신입생 278명을",
         f'그로스가 함께한 <a href="https://pmc.ncbi.nlm.nih.gov/articles/PMC4141473/">스리바스타바 연구진</a>은 대학 신입생 278명을'),
    ],
    "n94": [
        ("뷸러, 그리핀, 로스 연구진은 1994년",
         f'<a href="https://doi.org/10.1037/0022-3514.67.3.366">뷸러, 그리핀, 로스 연구진</a>은 1994년'),
        ("2026년 11월 17일에 음력 변환으로 하나씩 다시 셌어요.",
         f'2026년 11월 17일에 <a href="{KASI}">음력 변환</a>으로 하나씩 다시 셌어요.'),
    ],
    "n103": [
        ("절기 날짜는 한국천문연구원 음양력 자료와 같은 방법으로 셈했고",
         f'절기 날짜는 <a href="{KASI}">한국천문연구원 음양력 자료</a>와 같은 방법으로 셈했고'),
        ("심리학자 골비처와 시런은 2006년",
         f'심리학자 <a href="https://doi.org/10.1016/S0065-2601(06)38002-1">골비처와 시런</a>은 2006년'),
    ],
    "n99": [
        ("미국 심리학자 클라이드 헨드릭과 수전 헨드릭이 1986년",
         f'미국 심리학자 <a href="https://doi.org/10.1037/0022-3514.50.2.392">클라이드 헨드릭과 수전 헨드릭</a>이 1986년'),
        # 자료 이름이 본문에 없어 절기 이름을 넣은 한 문장으로 링크(壬午 달 글자의 근거)
        ("주는 연애와 받는 연애가 둘 다 있는 사람이라, 한쪽만 하다 지칠 때 '나도 이게 필요해'라고 한 번 말해 보세요.</p>",
         '주는 연애와 받는 연애가 둘 다 있는 사람이라, 한쪽만 하다 지칠 때 \'나도 이게 필요해\'라고 한 번 말해 보세요.</p>'
         f'<p>달 글자는 절기로 나뉘어요. 6월 12일은 <a href="{KASI}">망종</a> 뒤라 午의 달이고, 위 여덟 글자의 壬午가 여기서 나와요.</p>'),
    ],
    "n100": [
        ("심리학자 응우옌·라이언·데시는 대학생들을 15분 동안",
         f'심리학자 <a href="https://doi.org/10.1177/0146167217733073">응우옌·라이언·데시</a>는 대학생들을 15분 동안'),
        ("2027년에는 띠 묶음마다 역마 글자의 달이 한 번씩 와요. 그달에는 떠날 일이 생기거나 떠나고 싶은 마음이 커지기 쉬워요.</b></p>",
         '2027년에는 띠 묶음마다 역마 글자의 달이 한 번씩 와요. 그달에는 떠날 일이 생기거나 떠나고 싶은 마음이 커지기 쉬워요.</b></p>'
         f'<p>달 경계는 절기라서, 2월 4일 <a href="{KASI}">입춘</a>, 5월 6일 입하, 8월 8일 입추, 11월 8일 입동이 그 시작이에요.</p>'),
    ],
    "n101": [
        ("심리학자 몬토야·호턴·커치너는 실험실과 실제 관계를 다룬",
         f'심리학자 <a href="https://doi.org/10.1177/0265407508096700">몬토야·호턴·커치너</a>는 실험실과 실제 관계를 다룬'),
        ("이런 짝은 다툼이 적은 대신, B가 '늘 맞춰 준다'고 느끼는 날이 쌓이기 쉬워요. 고를 일 하나는 B가 정하게 번갈아 맡기면 균형이 잡혀요.</p>",
         '이런 짝은 다툼이 적은 대신, B가 \'늘 맞춰 준다\'고 느끼는 날이 쌓이기 쉬워요. 고를 일 하나는 B가 정하게 번갈아 맡기면 균형이 잡혀요.</p>'
         f'<p>두 사람의 달 글자도 절기로 나뉘어요. 3월 8일은 <a href="{KASI}">경칩</a> 뒤라 卯의 달, 7월 22일은 소서 뒤라 未의 달이에요.</p>'),
    ],
    "n104": [
        ("음력 생일이라면 한국천문연구원 음양력 변환에서 양력 날짜를 먼저 찾은 뒤 넣어 주세요.",
         f'음력 생일이라면 <a href="{KASI}">한국천문연구원 음양력 변환</a>에서 양력 날짜를 먼저 찾은 뒤 넣어 주세요.'),
        ("2024년에 태어난 아기는 23만 8,300명, 하루에 약 651명이에요.",
         '<a href="https://www.newsis.com/view/NISX20250226_0003079235">2024년에 태어난 아기는 23만 8,300명</a>, 하루에 약 651명이에요.'),
    ],
    "n102": [
        ("심리학자 부스비·쿠니·샌드스트롬·클라크는 처음 만난 두 사람에게",
         f'심리학자 <a href="https://doi.org/10.1177/0956797618783714">부스비·쿠니·샌드스트롬·클라크</a>는 처음 만난 두 사람에게'),
        ("이런 사람은 마음이 없는 게 아니라 확인이 끝난 뒤에야 꺼내요. 상대에게는 그 사이가 '관심 없음'으로 보이기 쉬워요.</p>",
         '이런 사람은 마음이 없는 게 아니라 확인이 끝난 뒤에야 꺼내요. 상대에게는 그 사이가 \'관심 없음\'으로 보이기 쉬워요.</p>'
         f'<p>달 글자도 절기로 나뉘어요. 12월 10일은 <a href="{KASI}">대설</a> 뒤라 子의 달이고, 여덟 글자의 甲子가 여기서 나와요.</p>'),
    ],
    "n105": [
        ("한국민족문화대백과사전은 당사주를",
         '<a href="https://encykorea.aks.ac.kr/Article/E0013895">한국민족문화대백과사전</a>은 당사주를'),
        ("심리학자 쿼이드백·길버트·윌슨은 18세부터 68세까지",
         f'심리학자 <a href="https://doi.org/10.1126/science.1229294">쿼이드백·길버트·윌슨</a>은 18세부터 68세까지'),
    ],
}

def fix(pid, v):
    b = v["body"]; n0 = b.count("📚"); assert n0 == 2, (pid, n0)
    for o, n in EDITS[pid]:
        assert b.count(o) == 1, (pid, o, b.count(o)); b = b.replace(o, n)          # 링크·문장 먼저
    b, k = re.subn(r"<p>📚 <b>출처 [12]</b>: <a href=\"[^\"]+\">[^<]*</a></p>", "", b)   # 출처 줄 문단을 지운다
    assert k == 2, (pid, k)
    while "<p>&nbsp;</p><p>&nbsp;</p>" in b: b = b.replace("<p>&nbsp;</p><p>&nbsp;</p>", "<p>&nbsp;</p>")
    assert "📚" not in b and "출처" not in b, pid
    return b

def cta_of(pid):
    """지금 사이트 원고에 박힌 글별 CTA 배너 이름 — 다시 그릴 때 그림 폴더가 없어도 같은 배너를 쓰게."""
    p = f"{MP.SITE}/public/naver/{pid}.html"
    m = re.search(r"naver/img/(?:m\d+/)?(naver_cta[^\"'?\s]+\.jpg)", open(p, encoding="utf-8").read())
    assert m, pid
    return m.group(1)

if __name__ == "__main__":
    pids = sys.argv[1:]
    reg = json.load(open(MP.REG, encoding="utf-8"))
    live = sorted((v["dt"], k) for k, v in reg.items() if not v.get("done") and "body" in v)
    order = [k for _, k in live]
    for pid in pids:
        v = reg[pid]; assert not v.get("done"), f"{pid} 이미 예약 끝난 글 — 키트로 고쳐야 한다"
        forced = cta_of(pid)
        MP.cta_pick = lambda p_, c_, b_, _f=forced: _f            # 그림 폴더가 없어도 같은 배너를 고른다
        v["body"] = fix(pid, v)
        v["style_v1"] = (v.get("style_v1", "") + " · 11/22 출처 줄 제거(n107 방식)").strip(" ·")
        nxt = order[order.index(pid) + 1] if order.index(pid) + 1 < len(order) else None
        MP.write_page(pid, D.datetime.fromisoformat(v["dt"]), v["title"], v["tags"], v["body"], nxt,
                      v.get("cover"), v.get("related"), v.get("category"), v.get("thumbs"), v.get("cid"),
                      v.get("clips"), v.get("reserve"))
        print(pid, "고침 · 출처 줄 0 · 링크", len(set(re.findall(r'href="(https?://(?!zaoseon\.com|raw\.githubusercontent)[^"]+)"', v["body"]))), "개 · 배너", forced)
    json.dump(reg, open(MP.REG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
