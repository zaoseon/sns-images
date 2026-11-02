"""예약 네이버 글 4편(n75·n70·n77·n04) 새 기준 원고 (① 자동 실행 11/2 19:45, CT 11/2 15:15 · 대표 11/2 15:04).
K-151 고정 첫 인사·'결론부터' 빼기 · K-162 첫 200자 정의 문장·출처 2개(확인한 주소만: KASI 페이지는 WebFetch로 내용 확인, DOI는 Crossref로 제목 확인) · K-161 제목.
사진·계산값·본문 풀이는 그대로. 한 번만 돌린다(이미 고친 글은 assert로 멈춤)."""
import os, json, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import k151_check as K
F = os.path.join(HERE, "pages.json")
P = json.load(open(F, encoding="utf-8"))
G1 = "<p>안녕하세요, 자오선의 정월이에요.</p><p>&nbsp;</p>"
G2 = "<p>바쁘신 분들을 위해 결론부터 말씀드릴게요.</p><p>&nbsp;</p>"
G2b = "<p>바쁘신 분들을 위해 결론부터 말씀드릴게요.</p>"

def rep(b, old, new, n=1):
    assert b.count(old) == n, (old[:40], b.count(old)); return b.replace(old, new)

def src(url, label):
    return f'<p>📚 <b>출처</b>: <a href="{url}">{label}</a></p>'

# n75 만세력
v = P["n75"]; b = v["body"]
b = rep(b, G1, ""); b = rep(b, G2, "")
b = rep(b, "<p><b>만세력</b>은 처음에 여덟 글자 표, 그중 일 칸 위 글자(일간), 오행 칸 세 곳만 보면 돼요.</p>",
        "<p><b>만세력</b>은 날짜를 해·달·날·시간 글자(간지)로 바꿔 적어 둔 달력이에요.</p><p>처음에는 여덟 글자 표, 그중 일 칸 위 글자(일간), 오행 칸 세 곳만 보면 돼요.</p>")
b = rep(b, "<p>앱이나 사이트마다 화면 모양은 달라도 들어 있는 칸은 거의 같아요.</p>",
        "<p>앱이나 사이트마다 화면 모양은 달라도 들어 있는 칸은 거의 같아요.</p><p>날짜별 음력과 간지는 한국천문연구원 음양력 변환에서도 확인할 수 있어요.</p>"
        + src("https://astro.kasi.re.kr/life/pageView/5", "한국천문연구원 천문우주지식정보, 음양력 변환"))
v["title"] = "만세력 보는 법 3곳, 일간·오행과 앱마다 시주가 다른 이유"
v["body"] = b

# n70 생일 숫자
v = P["n70"]; b = v["body"]
b = rep(b, G1, ""); b = rep(b, G2, "")
b = rep(b, "1. 내 숫자는 어떻게 만드나요?", "1. 내 생일 숫자는 어떻게 만드나요?", 2)
b = rep(b, "<p>맞는 부분만 가져가고 나머지는 흘려보내도 괜찮아요.</p>",
        "<p>맞는 부분만 가져가고 나머지는 흘려보내도 괜찮아요.</p><p>누구에게나 맞을 법한 설명을 내 얘기로 느끼는 마음을 심리학에서는 '포러 효과'라고 해요.</p><p>다 맞는 것 같을 때일수록 내 경험과 겹치는 한 줄만 골라 보세요.</p>"
        + src("https://doi.org/10.1037/h0059240", "Forer (1949), J. Abnormal and Social Psychology"))
v["title"] = "생일 숫자로 보는 연애 스타일, 수비학 숫자 9가지 한 줄 풀이"
v["body"] = b

# n77 연애운
v = P["n77"]; b = v["body"]
b = rep(b, G1, ""); b = rep(b, G2, "")
b = rep(b, "<p><b>2027년 연애운</b>은 내 일지·인연의 별·도화가 정미(丁未)년 글자와 만나는 곳에서 읽어요.</p>",
        "<p><b>2027년 연애운</b>은 내 일지·인연의 별·도화가 정미(丁未)년 글자와 만나는 곳에서 읽는 신호예요.</p>")
b = rep(b, "<p>좋아한다고 믿은 쪽이 더 다정하게 말했고, 상대도 그 사람을 더 좋아하게 됐어요.</p>",
        "<p>좋아한다고 믿은 쪽이 더 다정하게 말했고, 상대도 그 사람을 더 좋아하게 됐어요.</p>"
        + src("https://doi.org/10.1037/0022-3514.51.2.284", "Curtis &amp; Miller (1986), J. Personality and Social Psychology"))
v["body"] = b

# n04 양띠
v = P["n04"]; b = v["body"]
b = rep(b, "<p><b>2027년 양띠 운세</b>가 궁금하신가요? 안녕하세요, 자오선의 정월이에요.</p>",
        "<p><b>2027년 양띠 운세</b>는 내 띠 글자 미(未)가 한 해를 다스리는 본명년 운세예요.</p>")
b = rep(b, G2b, "")
b = rep(b, "<p>사주의 달은 1일이 아니라 <b>절기</b>로 바뀌어요. 아래 날짜는 그달이 시작하는 날이에요.</p>",
        "<p>사주의 달은 1일이 아니라 <b>절기</b>로 바뀌어요. 아래 날짜는 그달이 시작하는 날이에요.</p><p>2027년 절기 날짜는 한국천문연구원 달력 자료로 맞춰 봤어요.</p>"
        + src("https://astro.kasi.re.kr/kor/life/post/calendarData?year=2027", "한국천문연구원 천문우주지식정보, 2027년 달력 자료"))
v["body"] = b

bad = {p: K.check(p, P[p]) for p in ("n75", "n70", "n77", "n04")}
# n04 는 pages.json dt 가 옛 값(10/07)이라 출처 수 검사가 안 돈다 → 직접 센다
for p, x in bad.items(): print(p, P[p]["title"], len(P[p]["title"]), "자", x or "걸림 0")
json.dump(P, open(F, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
