"""K-138 관문(대표 10/18 12:48 "제작 가이드 규칙에 반영해, 재발 안 하게"): 그린 그림 속 글자가 배경에 묻혔는지 픽셀로 재고, 걸리면 막는다.
검사 본체는 하나 — zaoseon-site `tools/naver_audit/faint_text_check.py`(대비 1.06~1.9 = 1단 '사실상 안 보임', --weak 는 1.9~3.0).
여기서는 그 파일을 불러 쓰기만 한다(같은 검사를 두 곳에 두지 않는다). zaoseon-site 가 옆에 없으면 경고만 하고 넘긴다.
거는 곳: imgkit.Cv.save(네이버 본문 그림 저장 직후 — 걸리면 방금 쓴 파일을 지우고 멈춤) · card_gate.after(카드·표지) · qa_all '그림 글자 묻힘(K-138)'.
넘기기: ZS_SKIP_GATE=1 (다른 관문과 같음)."""
import os, importlib.util

def _site():
    for p in (os.environ.get("SITE"), os.path.join(os.path.dirname(__file__), "..", "..", "zaoseon-site"), "/home/claude/zaoseon-site"):
        if p and os.path.exists(os.path.join(p, "tools", "naver_audit", "faint_text_check.py")): return p
    return None

_M = None
def _mod():
    global _M
    if _M is None:
        s = _site()
        if not s: return None
        spec = importlib.util.spec_from_file_location("faint_text_check", os.path.join(s, "tools", "naver_audit", "faint_text_check.py"))
        _M = importlib.util.module_from_spec(spec); spec.loader.exec_module(_M)
    return _M

def hits(path, weak=False):
    """-> [(줄 y, 덩어리 수, 가장 낮은 대비)] 비면 통과. 검사 파일이 없으면 None."""
    m = _mod()
    return None if m is None else m.check(path, weak)

def guard(path, what=""):
    """걸리면 SystemExit. 1단(심함)만 막는다 — 2단(약함)은 큰 한자 워터마크 같은 장식도 잡아서 사람이 본다(10/18 ① 확인)."""
    if os.environ.get("ZS_SKIP_GATE") == "1": return []
    h = hits(path)
    if h is None:
        print("  [K-138] 글자 묻힘 검사 파일(zaoseon-site tools/naver_audit/faint_text_check.py)을 못 찾아 건너뜀:", os.path.basename(path)); return []
    if h:
        raise SystemExit(f"\n[막음 K-138] 그림 속 글자가 배경에 묻혔어요: {what or os.path.basename(path)}\n"
                         + "\n".join(f"  · y {y} 근처 글 덩어리 {n}개, 대비 {r}:1" for y, n, r in h[:5])
                         + "\n  칸 위 글은 imgkit.ink(색, 바탕)로 대비 4.5 이상 색을 고르세요.\n")
    return []
