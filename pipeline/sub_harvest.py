"""릴스 자막 수집기(R60 검사용, 10/13). 렌더 소스의 장면 함수를 그려 보며 '실제로 화면에 놓이는 글 덩어리'를 모은다.
글 덩어리 = text()·tblock() 한 번 호출 = 줄바꿈이 끝난 줄 목록. 장면 길이(초)·글자 크기도 함께 적는다.
사용: import sub_harvest as H; H.harvest(scenes) -> [{"no":1,"dur":2.6,"blocks":[{"lines":[..],"size":96}]}]"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.abspath(os.path.join(HERE, "..")); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(R, "content"))
from PIL import Image
import clip_motion as M
_REC = None
def _txt(ln): return "".join(ch for ch, _h in ln) if ln and isinstance(ln[0], tuple) else (ln if isinstance(ln, str) else "".join(ln))
_wrap0 = M.wrap
def _wrap(text, fnt, maxw):
    out = _wrap0(text, fnt, maxw)
    if _REC is not None: _REC.append(dict(lines=[_txt(l) for l in out], size=getattr(fnt, "size", 0), src=text))
    return out
def _patch_zodiac():
    try: import clips_motion_zodiac as Z
    except Exception: return None
    k0 = Z.kbreak
    def kb(s_, size, maxw, path=Z.BLACK if hasattr(Z, "BLACK") else None):
        out = k0(s_, size, maxw) if path is None else k0(s_, size, maxw, path)
        if _REC is not None: _REC.append(dict(lines=[l if isinstance(l, str) else _txt(l) for l in out], size=size, src=s_))
        return out
    Z.kbreak = kb; return Z
def harvest(scenes, t_frac=.95):
    global _REC
    M.wrap = _wrap; Z = _patch_zodiac(); res = []
    for i, (dur, fn) in enumerate(scenes):
        _REC = []
        for _f in (M.line_layers,) + tuple(getattr(Z, n) for n in dir(Z) if hasattr(getattr(Z, n, None), 'cache_clear')) if Z else (M.line_layers,): _f.cache_clear()   # 같은 글이 되풀이돼도 매번 줄바꿈을 다시 계산해 수집한다
        try:
            fr = Image.new("RGB", (M.W, M.H), (0, 0, 0)); M.DY = 0; fn(M.Ctx(fr, dur * t_frac, dur))
        except Exception as e: _REC.append(dict(lines=[], size=0, src="", err=str(e)[:80]))
        seen = set(); bl = []
        for b in _REC:
            k = (tuple(b["lines"]), b["size"])
            if k in seen or not b["lines"]: continue
            seen.add(k); bl.append(b)
        res.append(dict(no=i + 1, dur=dur, blocks=bl))
    _REC = None; M.wrap = _wrap0
    return res
