"""11/14 완성 파일 감사(content_audit body)에서 걸린 발행 전 그림 다시 그리기(K-178: 공개 전 글만, 새 이름만).
n54 한 줄 결론(i5f): 분홍 판에 분홍 '정월의 한 줄 결론' 대비 1.3 → body_v3.intro_v3 가 대비 4.5 미만이면 본문색으로 그림. i5f → i7(→ i7f)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import k193_redraw_1112 as K, body_v3 as B, cover_v3 as V
def intro7(pid, n):
    import mobile_fix_1111 as MF
    d = K.sub(MF.INTRO[pid]); c = V.Ctx(K._pick(pid)); T = V.all_configs()
    B.intro_v3(f"naver_z{n}_i7.jpg", c, d[0], d[1], d[2], T[pid].get("face") or "v1_lowbun"); return (f"naver_z{n}_i5f.jpg", f"naver_z{n}_i7.jpg")
K.JOBS = {"n54": [intro7]}
if __name__ == "__main__":
    for a in sys.argv[1:] or ["n54"]: K.run(a)
