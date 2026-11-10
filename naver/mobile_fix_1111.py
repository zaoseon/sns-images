"""11/11 대표 폰 캡처(용띠 글): "발행 원고에 아직도 이미지가 모바일 최적화 안 된 게 섞여 있어".
원인: K-137(꽉 찬 판 f)이 *9 도식에만 적용됐고, 한 줄 결론(i4)·표(b4·c4·q4…)는 여백 있는 판(내용 폭 86%) 그대로였다. 한 줄 결론 카드의 작은 글자는 26·28px(폰 8~9px).
고침(발행 전 글만, K-178): ① 한 줄 결론을 큰 글자로 다시 그림(새 이름 *_i5.jpg) ② 여백 있는 본문 사진을 모두 꽉 찬 판(*f.jpg, fullbleed.py)으로 ③ pages.json·사이트 원고 주소를 새 이름으로.
새 이름만(사진 보존 규칙). 사용: python3 naver/mobile_fix_1111.py n59 n41 …"""
import os, sys, re, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "pipeline"))
SITE = os.environ.get("SITE", "/home/claude/zaoseon-site")
import body_v4 as B4, body_v3 as B, cover_v3 as V, fullbleed as FB
PG = os.path.join(HERE, "pages.json")

# 새 글들의 한 줄 결론은 capture 로 못 받아서(제작 스크립트가 다름) 그림에서 읽어 적었다(CT 11/11). 한자는 뺐다 — 글꼴에 한자가 없어 줄 전체가 명조로 바뀌어 보였다.
INTRO = {
 "n67": ("뱀띠는 불의 기운을 타고났어요.", "힘 쓸 달은 8월·9월·1월, 아낄 달은 10월·11월", "달력"),
 "n71": ("여섯 중 네 개 이상이 같은 방향을 가리킨 사람은 100명 중 5명이었어요.", "계산 방법, 몇 개가 같은 말을 하는지, 사주만 혼자 다른 사람", "세 가지"),
 "n59": ("말띠와 2027년은 짝을 이루는 육합이에요.", "힘 쓸 달은 2월·7월·10월, 아낄 달은 12월과 이듬해 1월", "달력"),
 "n41": ("말이 줄어드는 건 소심해서가 아니라 믿음이 생겨야 마음을 여는 방식이에요.", "큰 산과 보석, 처녀·염소자리, 숫자 7", "세 풀이"),
}

def fix(pid):
    n = int(pid[1:]); pages = json.load(open(PG, encoding="utf-8")); body = pages[pid]["body"]
    swap = {}
    # ① 한 줄 결론 다시 그림
    if f"naver_z{n}_i4.jpg" in body:
        d = ("intro",) + INTRO[pid] if pid in INTRO else B4.capture(pid).get(f"naver_z{n}_i.jpg")
        if d and d[0] == "intro":
            pick = json.load(open(B4.PICK, encoding="utf-8")); c = V.Ctx(pick[pid]); T = V.all_configs()
            B.intro_v3(f"naver_z{n}_i5.jpg", c, d[1], d[2], d[3], T[pid].get("face") or "v1_lowbun")
            swap[f"naver_z{n}_i4.jpg"] = f"naver_z{n}_i5.jpg"
        else: print(pid, "한 줄 결론 자료 못 찾음 — i4 를 꽉 찬 판으로만")
    pages = json.load(open(PG, encoding="utf-8"))   # capture 가 pages.json 을 잠깐 바꿨다 되돌리므로 다시 읽음
    names = [x for x in FB.post_images(pid, pages) if not x.startswith("wide/") and "_cta" not in x and not re.search(r"f\.jpg$", x)]
    names = [swap.get(x, x) for x in names]
    dirs = [FB.IMG, os.path.join(FB.IMG, "m1280")]
    for x in names:
        r, why = FB.convert(x, dirs)
        if r: 
            old = [k for k, v in swap.items() if v == x]; swap[old[0] if old else x] = r[0]
        else: print(pid, x, "꽉 찬 판 못 만듦:", why)
    # ③ 주소 바꾸기
    b = pages[pid]["body"]
    for o, nw in swap.items(): b = b.replace(o, nw)
    pages[pid]["body"] = b; json.dump(pages, open(PG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    sf = os.path.join(SITE, "public", "naver", pid + ".html")
    if os.path.exists(sf):
        s = open(sf, encoding="utf-8").read()
        for o, nw in swap.items(): s = s.replace(o, nw)
        open(sf, "w", encoding="utf-8").write(s)
    print(pid, swap)

if __name__ == "__main__":
    for a in sys.argv[1:]: fix(a)
