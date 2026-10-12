"""네이버 클립용 사주·별자리·숫자 4편(10/3 밤): 첫눈 10/10, 티 안 나는 사랑 10/11, 설득 10/12, 달아오름 10/14. 앱이 덮는 곳을 피하는 safe 배치(reel_plan.NAVER_SAFE), 음악 포함.
사용: python3 pipeline/new_tri_clips.py -> 2026-w42reel-new/naver/<키>.mp4"""
import sys, os
sys.path.insert(0,'pipeline'); sys.path.insert(0,'content')
import carousel_editor as CE, reel_v2 as RV, reel_plan as RP, new_tri_reels as N
def clip(face, hook, sub, rows, note, cfg, advice_title="셋 중 두 개 이상\n겹쳤다면"):
    d, ov = N.tri(face, hook, sub, rows, note, "나는 몇 개 *겹치나요*?", N.B3, dict(cfg, safe=RP.NAVER_SAFE, silent=False), advice_title=advice_title, nb="다음 편", nt="블로그에서 더 보기")
    ov["hint"] = "블로그에서 내 기운 확인"; return (d, ov)
CTA_PLUS = {"secret": dict(q="몇 개 겹쳤는지\n*댓글*로 남겨 주세요", nt="스티커 눌러 전체 풀이 보기", hint="무료 풀이에서 생일만 넣어 보세요")}   # 10/12 대표 요청: CTA 보강(댓글 숫자·스티커·무료 풀이, 모두 n26 원고 끝 문구)
S3 = "사주·별자리·숫자, 셋 중 몇 개 겹치나요?"
defs = {
 "first": clip("v1_lowbun", "3초 만에\n사랑에 빠지는 사람", S3, N.defs["first"][0] and [("병화(丙)일생, 도화가 있는 사주","태양처럼 바로 달아오르고, 사람을 끌어요"),("양자리 · 사자자리","직진하는 불의 별자리 (3/21~4/19, 7/23~8/22)"),("3번 · 5번","표현의 3, 새로움에 끌리는 5")],
    "하나도 안 겹친다면, 천천히 스며드는\n사랑을 하는 사람일지도 몰라요.", dict(struct="S1", style="발랄 우쿨렐레", seed=51, key="D")),
 "secret": clip("v13_horn_glasses", "좋아해도\n티가 안 나요", S3, [("무토(戊)·계수(癸)일생","속에 담아 두는 큰 산과\n말없이 스며드는 조용한 비"),("염소자리·물병자리","감정이 이성 뒤에 서는 별자리\n(12/22~1/19, 1/20~2/18)"),("4번·7번","신중하게 쌓는 4,\n속을 잘 안 보이는 7")],
    "마음이 작은 게 아니라\n꺼내는 속도가 다를 뿐이에요.\n오늘 마음을 말 한 줄로 보내 봐요.", dict(struct="S2", style="통통 마림바", seed=52, key="F"), advice_title="두 개 이상\n겹친다면"),   # 10/12 대표 앱 요청(n26 클립 보강: 줄바꿈·본문·CTA). 문구는 n26 원고에서만 가져옴
 "talk": clip("v4_glasses", "이 사람이 말하면\n다들 끄덕여요", S3, [("병화(丙) · 정화(丁)일생","생각을 밖으로 비추는 불의 표현력"),("쌍둥이자리 · 천칭자리","말과 관계의 공기 별자리 (5/21~6/21, 9/23~10/22)"),("3번 · 5번","표현의 3, 순발력의 5")],
    "설명하고 설득하는 일에서 빛나요.\n말이 앞서지 않게만 조심하세요.", dict(struct="S3", style="상큼 팝", seed=53, key="A"), advice_title="말은 무기,\n속도는 조절해요"),
 "heat": clip("v7_hanbok", "빨리 달아오르고\n빨리 식는 사람", S3, [("병화(丙)일생, 불이 많은 사주","태양처럼 밝지만 쉽게 달아오르고 쉽게 식어요"),("양자리 · 사자자리 · 사수자리","불의 별자리 (3/21~4/19, 7/23~8/22, 11/22~12/21)"),("5번","변화와 이동의 숫자. 새로움에 끌려요")],
    "관계에 새로운 불씨를 계속 넣어 주는 게\n오래 가는 비결이에요.", dict(struct="S2", style="경쾌 신스팝", seed=54, key="G"), advice_title="두 개 이상\n겹친다면"),
}
for _k, _c in CTA_PLUS.items():
    defs[_k][0]["ctaQ"] = _c["q"]; defs[_k][0]["nextTitle"] = _c["nt"]; defs[_k][1]["nextTitle"] = _c["nt"]; defs[_k][1]["hint"] = _c["hint"]
if __name__ == "__main__":
    ks = sys.argv[1:] or list(defs); out = os.environ.get("TRI_OUT") or os.path.join(CE.ROOT, "2026-w42reel-new", "naver")
    RV.render(ks, defs, out)
