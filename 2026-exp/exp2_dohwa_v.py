# 실험 판 2편 목소리·움직이는 자막 판(11/3) — 내용은 exp2_dohwa.py(n79 원고) 그대로, 틀은 voice_reel. 확인형 끝.
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import voice_reel as VR
A = lambda f: "/home/claude/sns-images/assets/pd_art/" + f
씬 = [
 dict(이름="dv-0", 그림=A("003_Hyewon_Wolha_jeongin_3.jpg"), 표지=True, 제목=["도화살", "있는 사람", "특징 5가지"], 강조=[0], 말제목="도화살 있는 사람, 특징 다섯 가지."),
 dict(이름="dv-1", 그림=A("001_Hyewon_Imhatuho.jpg"), 제목=["첫 번째", "끌리는 분위기"], 강조=[1], 말제목="첫 번째, 끌리는 분위기.", 자막=["도화는 *복숭아꽃*", "사람을 끌어당기는", "*매력*으로 읽어요"]),
 dict(이름="dv-2", 그림=A("008_Danwon_Jangteogil.jpg"), 제목=["두 번째", "무대에서 빛나요"], 강조=[1], 말제목="두 번째, 무대에서 빛나요.", 자막=["무대나 영업", "*사람 대하는 일*에서", "빛나요"]),
 dict(이름="dv-3", 그림=A("002_Hyewon_Ssangryuksammae.jpg"), 제목=["세 번째", "자리마다 달라요"], 강조=[1], 말제목="세 번째, 자리마다 달라요.", 자막=["일 칸이면", "*가까운 사이*에서", "월 칸이면 *일터*에서"]),
 dict(이름="dv-4", 그림=A("016_Unknown_Korean_Lotus_Pond_2016_1_Detroit.jpg"), 제목=["네 번째", "바람기와 달라요"], 강조=[1], 말제목="네 번째, 바람기와는 달라요.", 자막=["*매력과 표현*으로", "읽는 글자예요", "태도는 *사람 나름*"]),
 dict(이름="dv-5", 그림=A("011_Crane_and_Pine_National_Museum_of_Korea_.jpg"), 제목=["다섯 번째", "2027년엔 달로 와요"], 강조=[1], 말제목="다섯 번째, 2027년엔 달로 와요.", 자막=["호랑이 말 개띠", "*3월*이고", "소 뱀 닭띠 *6월*"]),
 dict(이름="dv-6", 그림=A("003_Hyewon_Wolha_jeongin_3.jpg"), 자리="70% 40%", 제목=["몇 개나", "해당되세요?"], 강조=[1], 말제목="몇 개나 해당되세요?", 자막=["*숫자 하나만*", "댓글로 남겨 주세요", "프로필에서 1초 확인"]),
]
if __name__ == "__main__":
    only = sys.argv[1:]
    VR.만들기([c for c in 씬 if not only or c["이름"] in only], os.environ.get("ZS_NAME", "exp2_dohwa_v"), out_dir=os.environ.get("ZS_OUTDIR"))
