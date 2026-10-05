"""글꼴 공통 설정(10/5 대표 지시): 릴스·클립·카루셀 제목 = G마켓 산스 또는 페이퍼로지, 본문 = 프리텐다드.
- 영상(릴스·클립) 제목: G마켓 산스 Bold / 카드·카루셀 제목: 페이퍼로지 ExtraBold·Black / 본문: 프리텐다드 ExtraBold. 한자(東西數)만 명조체.
- 굵기는 항상 800 이상(대표 요구). CSS에서 글꼴 이름: JW-D(제목), JW-B(본문). PIL(영상 엔진)에서는 경로를 쓴다.
- 페이퍼로지는 한글 2,780자만 있어서, 쓰려는 글자가 없으면 missing()이 알려 주고 G마켓 산스로 바꾼다."""
import os
from fontTools.ttLib import TTFont
FD = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")
P = dict(gm_bold=os.path.join(FD, "GmarketSansBold.ttf"), gm_med=os.path.join(FD, "GmarketSansMedium.ttf"),
         pl_xb=os.path.join(FD, "Paperlogy-8ExtraBold.ttf"), pl_blk=os.path.join(FD, "Paperlogy-9Black.ttf"),
         pr_xb=os.path.join(FD, "PRETENDARD-EXTRABOLD.OTF"), pr_blk=os.path.join(FD, "PRETENDARD-BLACK.OTF"), serif=os.path.join(FD, "serif.otf"))
_cm = {}
def _cmap(k):
    if k not in _cm: _cm[k] = set(TTFont(P[k], lazy=True).getBestCmap().keys())
    return _cm[k]
def missing(key, text):
    """key 글꼴에 없는 글자 목록(공백·줄바꿈 제외)."""
    cm = _cmap(key); return sorted({c for c in text if not c.isspace() and ord(c) not in cm})
def url(k): return "file://" + P[k]
def css(display="gm"):
    """display='gm'(G마켓 산스) 또는 'pl'(페이퍼로지). JW-D=제목, JW-B=본문."""
    if display == "pl":
        d = f"@font-face{{font-family:JW-D;font-weight:800;src:url('{url('pl_xb')}')}}@font-face{{font-family:JW-D;font-weight:900;src:url('{url('pl_blk')}')}}"
    else:
        d = f"@font-face{{font-family:JW-D;font-weight:700 900;src:url('{url('gm_bold')}')}}"
    b = f"@font-face{{font-family:JW-B;font-weight:800;src:url('{url('pr_xb')}')}}@font-face{{font-family:JW-B;font-weight:900;src:url('{url('pr_blk')}')}}"
    s = f"@font-face{{font-family:JW-S;font-weight:400 900;src:url('{url('serif')}')}}"
    return d + b + s
D = "'JW-D','Noto Sans CJK KR',sans-serif"; B = "'JW-B','Noto Sans CJK KR',sans-serif"
def pick_display(texts, pref="pl"):
    """pref 글꼴에 없는 글자가 있으면 G마켓 산스로 바꾼다."""
    if pref == "pl" and missing("pl_blk", "".join(texts)): return "gm"
    return pref
