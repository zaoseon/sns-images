"""네이버 대표 이미지 검사 (10/15 대표 재지적: "상강 섬네일 또 잘림, 제작 가이드 규칙은 왜 만들었냐").
원인: 네이버 블로그 목록은 1200x720 가로 판을 정사각으로 자를 때 가운데가 아니라 정월 얼굴 쪽으로 자른다.
글자만 있는 구도(QL 왼쪽 정렬·QK 흰 카드·CH 큰 상반신)는 얼굴이 오른쪽이라 왼쪽 글자가 잘렸다(n20·n26·n29·n12).
10/14 대표가 승인한 n29 시안(얼굴 가운데)대로, 글자형 대표 이미지는 얼굴을 가운데 위에 둔다(thumb_sq 의 QC·QCS).
표·달력·큰 숫자형(BIG·N·ring·trio·gua·cal)은 큰 그림이 가운데라 잘린 사례가 없어 그대로 둔다(잘리면 이 표에 더한다).
검사(아직 안 올린 글 = pages.json 에서 done 이 아닌 글):
 1) 대표 이미지가 wide/ 1200x720 이고 양옆 240px 띠가 한 색(내용이 가운데 720 안에만 있음)
 2) 글자형 구도이면 cover_layout 이 QC 또는 QCS (얼굴 가운데)
 3) naver/img 에 이미 올라간 이름을 덮어쓰지 않았는지는 git 이 본다(새 이름 *_c.jpg 로만 추가).
사용: python3 naver/cover_audit.py   (걸리면 종료 코드 1, qa_all 에서도 부른다)"""
import json, os, sys
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
TEXT_TYPES = {"QL", "QK", "CH"}
CENTER_OK = {"QC", "QCS"}

def layouts():
    import thumb_sq as TQ, regen_badges as R
    R.load_47_63(); return {k: v.get("d") for k, v in TQ.T.items()}

def run():
    reg = json.load(open(os.path.join(HERE, "pages.json"), encoding="utf-8")); lay = layouts(); bad = []
    for pid, v in reg.items():
        if v.get("done") or "body" not in v: continue
        cov = v.get("cover") or ""; p = os.path.join(HERE, "img", cov)
        if not cov.startswith("wide/") or not os.path.exists(p): bad.append((pid, cov, "대표 이미지가 wide/ 판이 아니거나 파일 없음")); continue
        im = Image.open(p)
        if im.size != (1200, 720): bad.append((pid, cov, f"크기 {im.size}, 1200x720 이어야 함")); continue
        a = np.asarray(im.convert("L"), float)
        if max(a[:, :236].std(), a[:, 964:].std()) > 3: bad.append((pid, cov, "양옆 240px 띠에 글자·그림이 있음(가운데 720 밖)"))
        d = v.get("cover_layout") or lay.get(pid)
        if d in TEXT_TYPES: bad.append((pid, cov, f"글자형 구도 {d}: 정월 얼굴이 옆에 있어 목록에서 얼굴 쪽으로 잘림. thumb_sq 의 QCS(얼굴 가운데)로 새 이름 *_c.jpg 를 만들고 cover_layout='QCS'"))
    return bad

if __name__ == "__main__":
    b = run()
    for x in b: print("걸림", *x)
    print("대표 이미지 검사:", "통과" if not b else f"{len(b)}편 걸림"); sys.exit(1 if b else 0)
