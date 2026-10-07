"""트렌디 표현(○○코어) 적용(10/7 대표 지시 '○○ 코어 같은 트렌디한 표현도 쓰고 그래라'). 규칙 R24: 표지·캡션 첫 줄·해시태그에만, 영상당 하나, 설명 본문·면책·마음이 무거운 소재에는 쓰지 않는다.
사용: import trendy; caption = trendy.apply(caption, "sopclip-n34")   # 캡션 앞에 첫 줄, 뒤에 해시태그를 붙인다(이미 있으면 그대로)"""
import os, json
R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
def table(): return json.load(open(os.path.join(R, "content", "trendy_lines.json"), encoding="utf-8"))
def apply(caption, vid):
    t = table().get(vid)
    if not t or not t["opener"]: return caption
    c = caption or ""
    if t["opener"] not in c: c = t["opener"] + (" " + c if c else "")
    new = [h for h in t["tags"] if h not in c]
    return c + ((" " if not c.endswith(" ") else "") + " ".join(new) if new else "")
