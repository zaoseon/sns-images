"""릴스 계획(2026-10-02 오후, 대표 지적: 음악이 별로 · 모든 릴스가 같은 구조): 릴스마다 구조(S1/S2/S3)·음악 스타일·조성·템포가 다르고,
표지·조언·CTA 모양은 캐러셀 변형(C/A/T)을 따른다. 병·정·무는 대표 샘플 PNG를 그대로 쓴다(CTA만 필요하면 새로 그림).
사용: python3 pipeline/reel_plan.py ig 2026-10-04 2026-10-06   /   python3 pipeline/reel_plan.py naver byeong jeong"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "content"))
import carousel_editor as CE, reel_v2 as RV
from carousel_sets import SETS
SAMP = os.path.join(CE.ROOT, "samples", "carousel_2026-10-01")
def sample_frames(prefix, upto=6):     # 샘플 파일명: 샘플1.png(병) / 정-1.png / 무-1.png  (슬라이드 0~6)
    names = {"byeong": [f"샘플{i}.png" for i in range(1, 8)], "jeong": [f"정-{i}.png" for i in range(1, 8)], "mu": [f"무-{i}.png" for i in range(1, 8)]}[prefix]
    return {i: os.path.join(SAMP, n) for i, n in enumerate(names[:upto])}
def day_def(date, nxt, naver=False):
    S = SETS[date]; d = dict(dayChar=S["dayChar"], hanja=S["hanja"], accent=S["accent"], face=("v5_halfup_v2" if S["face"] == "v5_halfup" else S["face"]), kicker=S["kicker"], coverTitle=S["coverTitle"], coverSub=S["coverSub"],
        personality=S["personality"], love=S["love"], money=S["money"], advice=S["advice"], chartNote=S["chartNote"], values=S["values"], highlight=S["highlight"], ctaQ=S["ctaQ"], nextTitle=nxt, variant=S.get("variant", {}))
    return d
# 네이버 클립 **재생 화면**(대표가 올린 뒤 캡처, 영상이 화면에 1:1로 나오고 맨 위가 화면 y=95)에서 앱이 영상을 덮는 곳(1080x1920 기준):
#   위: 뒤로 가기·소리 아이콘 y<125 / 오른쪽 아이콘 줄(챌린지·좋아요·댓글·저장·더보기) x>=905, y 830~1780 / 아래: 프로필·곡·설명·칩 줄 y>=1485
#   (편집 화면은 로고·아이콘이 더 넓게 보이지만 실제 재생 화면은 이쪽이 기준)
# 슬라이드(1080x1350)를 0.88배로 줄여 (0,200)에 둔다 → x 0~950, y 200~1388. 오른쪽 아이콘 줄과는 글자가 겹치지 않게(글자 오른쪽 끝 ≤ 889) 폭을 정함
NAVER_SAFE = dict(scale=0.88, x=0, y=200)
NAVER_OV = lambda nxt: dict(nextBadge="다음 편", nextTitle=nxt, hint="블로그에서 내 기운 확인")
NEXT = {"byeong": "정(丁)일생 편", "jeong": "무(戊)일생 편", "mu": "기(己)일생 편", "gi": "경(庚)일생 편", "gyeong": "신(辛)일생 편", "sin": "임(壬)일생 편", "im": "계(癸)일생 편", "gye": "열 가지 한눈에 편"}
DATE = {"jeong": "2026-10-02", "mu": "2026-10-03", "gi": "2026-10-04", "gyeong": "2026-10-06", "sin": "2026-10-07", "im": "2026-10-08", "gye": "2026-10-09"}
def ig_defs():
    base = RV.get_defs(); out = {}
    CFG = {"2026-10-03": dict(style="상큼 팝", seed=3, key="D"), "2026-10-05": dict(style="발랄 우쿨렐레", seed=5, key="F"), "2026-10-10": dict(style="경쾌 신스팝", seed=10, key="C"), "2026-10-11": dict(style="통통 마림바", seed=11, key="D"),
           "2026-10-04": dict(struct="S3", style="상큼 팝", seed=4, key="G"), "2026-10-06": dict(struct="S1", style="발랄 우쿨렐레", seed=6, key="A"), "2026-10-07": dict(struct="S2", style="경쾌 신스팝", seed=7, key="E"),
           "2026-10-08": dict(struct="S3", style="통통 마림바", seed=8, key="G"), "2026-10-09": dict(struct="S2", style="상큼 팝", seed=9, key="F")}
    for k, cfg in CFG.items():
        d, ov = base[k]; d = dict(d)
        if k in SETS and SETS[k].get("variant"): d["variant"] = SETS[k]["variant"]       # 일주 릴스는 같은 날 캐러셀과 같은 모양
        out[k] = (d, dict(ov, _cfg=cfg))
    B = dict(RV.BYEONG); B["variant"] = {"cover": "C2", "advice": "A2", "cta": "T1"}
    out["byeong"] = (B, dict(nextBadge="내일 밤 9시", nextTitle="정(丁)일생 편", _cfg=dict(struct="S2", style="발랄 우쿨렐레", seed=12, key="C", frames=sample_frames("byeong", 7))))
    return out
def naver_defs():
    CFG = {"byeong": dict(struct="S2", style="발랄 우쿨렐레", seed=21, key="D"), "jeong": dict(struct="S1", style="경쾌 신스팝", seed=22, key="C"), "mu": dict(struct="S3", style="통통 마림바", seed=23, key="A"),
           "gi": dict(struct="S2", style="상큼 팝", seed=24, key="F"), "gyeong": dict(struct="S3", style="발랄 우쿨렐레", seed=25, key="G"), "sin": dict(struct="S1", style="경쾌 신스팝", seed=26, key="E"),
           "im": dict(struct="S2", style="통통 마림바", seed=27, key="D"), "gye": dict(struct="S3", style="상큼 팝", seed=28, key="C")}
    out = {}
    for k, cfg in CFG.items():
        if k == "byeong": d = dict(RV.BYEONG); d["variant"] = {"cover": "C2", "advice": "A2", "cta": "T1"}
        else: d = day_def(DATE[k], NEXT[k])
        d["nextTitle"] = NEXT[k]; c = dict(cfg); c["silent"] = os.environ.get("NAVER_SILENT") == "1"     # 10/3: PC 클립 업로드는 음악을 못 넣으므로 기본은 음악 포함(앱에서 직접 고르려면 NAVER_SILENT=1)
        c["safe"] = NAVER_SAFE
        if k in ("byeong", "jeong", "mu"): c["frames"] = sample_frames(k, 6)      # 표지~조언은 대표 샘플 그대로, CTA는 네이버 문구로 새로 그림
        ov = NAVER_OV(NEXT[k])
        if (d.get("variant") or {}).get("cta") == "T2":     # 얼굴형 CTA(T2)는 힌트가 왼쪽 아래 글자(extraTexts)라서 가운데 힌트와 겹치지 않게 그쪽 문구만 네이버용으로
            ov.pop("hint", None); d["hintText"] = "블로그에서\n내 기운 확인"
        out[k] = (d, dict(ov, _cfg=c))
    return out
if __name__ == "__main__":
    kind = sys.argv[1]; keys = sys.argv[2:]; defs = ig_defs() if kind == "ig" else naver_defs()
    RV.render(keys or list(defs), defs, os.path.join(CE.ROOT, "2026-w40car6-reel", kind))
