"""미발행 네이버 원고 18편 블로그온 기준 고치기 (CT 원고 작업자 11/4 20:00, 대표 11/4 19:28 "12편 블로그온 기준으로 고치고", 재발행 일정 docs/네이버_재발행_일정_2026-11-04.md).
K-151 고정 첫 인사·'결론부터' 빼기 · K-162 첫 200자 정의 문장·출처 2개 · K-161 제목 · K-155 연결글은 발행 글만 · kw_vol(zaoseon-site data/keywords/kw_volume.json 11/4 19:52).
출처 주소는 WebFetch·WebSearch 로 확인한 것만(N3). KASI 달력자료 2027 입춘 2/4 10:46 은 페이지에서 확인.
사진·계산값·dt 는 그대로. 한 번만 돌린다(이미 고친 글은 assert로 멈춤)."""
import os, json, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import k151_check as K
F = os.path.join(HERE, "pages.json")
P = json.load(open(F, encoding="utf-8"))
G1 = "<p>안녕하세요, 자오선의 정월이에요.</p><p>&nbsp;</p>"
G2 = "<p>바쁘신 분들을 위해 결론부터 말씀드릴게요.</p><p>&nbsp;</p>"
KW = json.load(open(os.environ.get("ZS_KW", "/home/claude/zaoseon-site/data/keywords/kw_volume.json"), encoding="utf-8"))["posts"]

def rep(b, old, new, n=1):
    assert b.count(old) == n, (old[:40], b.count(old)); return b.replace(old, new)

def src(url, label):
    return f'<p>📚 <b>출처</b>: <a href="{url}">{label}</a></p>'

def after(b, key, add):
    """key 가 들어 있는 문단(</p>로 끝나는 곳) 바로 뒤에 add 를 넣는다. key 는 한 번만 나와야 한다."""
    assert b.count(key) == 1, (key[:30], b.count(key))
    i = b.index(key); j = b.index("</p>", i) + 4
    return b[:j] + add + b[j:]

KASI = src("https://astro.kasi.re.kr/kor/life/post/calendarData?year=2027", "한국천문연구원 천문우주정보, 2027년 달력자료(월력요항)")
IPCHUN = "<p>2027년 입춘은 2월 4일 오전 10시 46분이에요.</p>" + KASI

PUB = {  # data.json naver_all 발행 글 중 검색 노출 '예'(data/checks/naver_search_1104.json, 11/4 19:52)
 "n80": ("2027 띠별 운세, 정미년 12띠 힘 쓸 달과 아낄 달 한눈에", "https://blog.naver.com/zaoseon/224461125363"),
 "n81": ("2027 삼재띠 언제 끝날까, 돼지띠 토끼띠 양띠 날삼재 날짜", "https://blog.naver.com/zaoseon/224462303163"),
 "n55": ("전갈자리 성격과 2027년 전갈자리 운세, 수성 역행은 언제일까", "https://blog.naver.com/zaoseon/224449200915"),
 "n72": ("띠 궁합 제대로 보는 법, 삼합·육합·원진으로 보는 띠별 궁합", "https://blog.naver.com/zaoseon/224447869316"),
 "n75": ("만세력 보는 법 3곳, 일간·오행과 앱마다 시주가 다른 이유", "https://blog.naver.com/zaoseon/224463601442"),
 "n46": ("속마음 숨기는 사람, 웃는 얼굴 뒤에 가면 쓰는 이유", "https://blog.naver.com/zaoseon/224447857559"),
 "n42": ("예민한 사람이 쉽게 피곤한 이유, 감각이 큰 사람의 마음", "https://blog.naver.com/zaoseon/224447837285"),
}

def related(v, rid, lead):
    t, u = PUB[rid]; phrase = f"{lead}, {t}" if not lead.endswith(".") else f"{lead} {t}"
    old = "<p><b>👇 " + v["related"]["phrase"] + "</b></p>"
    v["body"] = rep(v["body"], old, "<p><b>👇 " + phrase + "</b></p>")
    v["related"] = {"id": rid, "title": t, "phrase": phrase, "url": u}

def common(pid, title=None):
    v = P[pid]; b = v["body"]
    b = rep(b, G1, ""); b = rep(b, G2, "")
    if title: v["title"] = title
    v["body"] = b; v["kw_vol"] = KW[pid]["씨앗"]
    return v

def ipchun(v):
    v["body"] = after(v["body"], next(s for s in ["사주에서는 입춘(2월 4일 무렵)을 기준으로 띠를 세서", "띠는 입춘(2월 4일 무렵)을 기준으로 바뀌어서", "사주에서는 입춘(2월 4일 무렵)을 기준으로 띠를 세요.</p><p>&nbsp;</p><p>🔢"] if v["body"].count(s) == 1), IPCHUN)

TTI = "다른 띠도 궁금하다면"
# ── 띠 글 ──
v = common("n49")
v["body"] = rep(v["body"], "<p><b>2027년 돼지띠 운세</b>를 달마다 정리해 봤어요.</p>",
                "<p><b>2027년 돼지띠 운세</b>는 날삼재로 삼재가 끝나는 해이자, 사람을 통해 돈과 기회가 오기 쉬운 해예요.</p>")
ipchun(v); related(v, "n81", "날삼재가 언제 끝나는지 궁금하다면")

v = common("n65"); ipchun(v); related(v, "n80", TTI)
v = common("n66"); ipchun(v); related(v, "n80", TTI)
v = common("n67", "2027년 뱀띠 운세, 속도 조절의 해 힘 쓸 달·아낄 달"); ipchun(v); related(v, "n80", TTI)
v = common("n59", "2027년 말띠 운세, 육합의 해 힘 쓸 달·아낄 달 총정리"); ipchun(v); related(v, "n80", TTI)
v = common("n68", "2027년 닭띠 운세, 인정받는 해 힘 쓸 달·아낄 달 총정리"); ipchun(v); related(v, "n80", TTI)

v = common("n69")
v["body"] = rep(v["body"], "<p><b>2027년 쥐띠</b>는 쥐(子)와",
                "<p><b>2027년 쥐띠 운세</b>는 재물 기회는 분명하고, 말 한마디로 오해가 생기기 쉬운 해예요.</p><p>쥐(子)와")
ipchun(v); related(v, "n80", TTI)

v = common("n73", "날삼재 뜻과 2027년 삼재띠, 돼지·토끼·양띠 이사 괜찮을까")
ipchun(v); related(v, "n81", "날삼재가 끝나는 날짜가 궁금하다면")

v = common("n54", "2027년 정미년 뜻, 2월 4일부터 6일생은 띠가 달라요")
v["body"] = after(v["body"], "<p>2027년 입춘은 2월 4일 오전 10시 46분이에요.</p>", KASI)
related(v, "n80", "내 띠가 확실해졌다면")

# ── 그 밖 ──
v = common("n74")
v["body"] = "<p><b>수성 역행</b>은 지구에서 볼 때 수성이 하늘을 거꾸로 가는 것처럼 보이는 때예요.</p>" + v["body"]
v["body"] = after(v["body"], "'내가 잘 전했겠지'가 과잉 확신이에요.",
                  src("https://pubmed.ncbi.nlm.nih.gov/16393025/", "Kruger 외 (2005), J. Personality and Social Psychology"))
related(v, "n55", "별자리로 보는 2027년이 궁금하다면")

v = common("n76", "2027 신년운세 감정서, 샘플 6쪽과 구성 한눈에")
v["body"] = rep(v["body"], "<p><b>2027 신년 감정서</b>는", "<p><b>2027 신년운세 감정서</b>는")
v["body"] = rep(v["body"], "1. 감정서엔 무엇이 담기나요?", "1. 신년운세 감정서엔 무엇이 담기나요?", 2)
v["body"] = after(v["body"], "실제로 잃은 사람들은 짐작보다 덜 속상했어요.",
                  src("https://doi.org/10.1111/j.1467-9280.2006.01760.x", "Kermer 외 (2006), Psychological Science"))
related(v, "n80", "띠로 먼저 2027년을 보고 싶다면")

v = common("n79", "도화살 뜻과 2027년 도화 달, 도화가 있으면 인기가 많을까")
v["body"] = after(v["body"], "말 한마디 없이도요.",
                  "<p>번(1961)도 강의실 자리를 정해 앉혀 보니, 가까이 앉은 학생끼리 서로 알게 되는 일이 많았다고 했어요.</p>"
                  + src("https://doi.org/10.1177/001872676101400106", "Byrne (1961), Human Relations"))
related(v, "n72", "띠로 보는 궁합이 궁금하다면")

v = common("n58", "십성 뜻 한눈에, 10가지 이름과 내 일간으로 찾는 표")
v["body"] = after(v["body"], "수학 성적이 다시 오르기 시작했어요.",
                  src("https://pubmed.ncbi.nlm.nih.gov/17328703/", "Blackwell 외 (2007), Child Development"))
related(v, "n75", "내 일간을 만세력에서 찾고 싶다면")

v = common("n78")
v["body"] = after(v["body"], "서머타임을 빼지 말고 시계에 적힌 시각 그대로 적어 주세요.",
                  src("https://www.korea.kr/news/policyNewsView.do?newsId=148680709", "대한민국 정책브리핑, 서머타임제(2009)")
                  + "<p>1987~1988년 서머타임은 2년 만인 1989년에 없앴어요.</p>"
                  + src("https://theme.archives.go.kr/next/koreaOfRecord/summerTime.do", "국가기록원, 기록으로 만나는 대한민국 서머타임제"))
related(v, "n75", "시주 칸을 만세력에서 확인하고 싶다면")

v = common("n71", "바넘효과 뜻, 여섯 운명학이 같은 말 할 확률 3000명 계산")
v["body"] = "<p><b>바넘효과</b>는 누구에게나 맞는 말을 내 얘기로 믿는 마음이에요.</p>" + v["body"]
v["body"] = rep(v["body"], "1. 어떻게 계산했나요?", "1. 바넘효과인지 어떻게 계산했나요?", 2)
v["body"] = after(v["body"], "더 잘 맞는다고 답했어요.",
                  "<p>바넘효과 연구를 모은 리뷰(1985)도 풀이를 믿는 정도는 나와 관련 있어 보이는지, 좋게 들리는지에 따라 달라진다고 정리했어요.</p>"
                  + src("https://doi.org/10.2466/pr0.1985.57.2.367", "Dickson &amp; Kelly (1985), Psychological Reports"))
related(v, "n46", "웃는 얼굴 뒤 마음이 궁금하다면")

v = common("n41", "낯가림 심한 사람, 3가지 풀이로 본 말이 줄어드는 이유")
v["body"] = after(v["body"], "말의 양과 사회성은 별개예요.",
                  "<p>수줍음과 사교성은 서로 다른 성향이라는 연구도 있어요.</p>"
                  + src("https://doi.org/10.1037/0022-3514.41.2.330", "Cheek &amp; Buss (1981), J. Personality and Social Psychology"))
related(v, "n42", "낯선 자리가 유독 피곤하다면")

v = common("n43", "소비심리 뜻, 돈 쓰고 후회하는 3가지 모양 사주와 별자리로")
v["body"] = rep(v["body"], "<p><b>소비심리</b>로 보면 돈 쓰고",
                "<p><b>소비심리</b>는 돈을 쓰기 전과 쓴 뒤에 오가는 마음이에요.</p><p>소비심리로 보면 돈 쓰고")
v["body"] = rep(v["body"], "4. 후회는 어디서 올까요?", "4. 소비심리로 보면 후회는 어디서 올까요?", 2)
v["body"] = after(v["body"], "46%만 다시 사겠다고 했어요.",
                  src("https://doi.org/10.1126/science.7455683", "Tversky &amp; Kahneman (1981), Science"))
related(v, "n80", "돈을 쓸 달과 아낄 달을 띠로 보고 싶다면")  # 11/4 20:01 대표: 연결글은 검색 노출 '예' 글만(n18 노출 아니오)

v = common("n45", "무기력, 퇴근 후 아무것도 하기 싫은 이유와 방전 3가지")
v["body"] = rep(v["body"], "4. 방전은 게으름일까요?", "4. 퇴근 후 무기력은 게으름일까요?", 2)
v["body"] = after(v["body"], "그 첫째 얼굴에 가까워요.",
                  src("https://doi.org/10.1002/job.4030020205", "Maslach &amp; Jackson (1981), J. Occupational Behaviour"))
related(v, "n42", "하루가 유독 피곤한 이유가 궁금하다면")

IDS = "n49 n65 n66 n67 n59 n68 n69 n73 n54 n74 n76 n79 n58 n78 n71 n41 n43 n45".split()
import re
for p in IDS:
    x = P[p]; ext = {u for u in re.findall(r'href="(https?://[^"]+)"', x["body"]) if not re.search(r"zaoseon\.com|raw\.githubusercontent|blog\.naver\.com/zaoseon", u)}
    bad = K.check(p, dict(x, dt="2026-11-09T00:00:00"))   # dt 가 옛 값이어도 출처 검사를 돌린다
    print(p, len(x["title"]), x["title"], "출처", len(ext), bad or "걸림 0")
json.dump(P, open(F, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
