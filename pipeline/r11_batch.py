"""10/12 예약 릴스 전수 수정: 모든 예약 릴스 끝에 R11 끝 장면을 붙여 2026-r11/ 에 저장한다. 사용: python3 pipeline/r11_batch.py [일부 키워드]"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import r11_tail as R
ROOT = os.path.abspath(os.path.join(HERE, ".."))
# 원본 -> (질문, 자르기: 'auto'=D-2.2(reuse) / 'det'=장면검출 / 'end'=끝에 이어붙임 / 초, 옵션)
Z = "end"
M = {
 "2026-w40car6-reel/ig/2026-10-10.mp4": ("빨리 식는 편\n나도 그런가요?", "det"),
 "2026-w40car6-reel/ig/2026-10-11.mp4": ("나는 일단 하는 쪽\n생각하는 쪽?", "det"),
 "2026-w42/v3/reel_07.mp4": ("호랑이띠 내년\n내 실력은 어떨까요?", Z),
 "2026-w42reel-sched/gapeul/ig/eul.mp4": ("나는 바람에 눕는 쪽\n다시 서는 쪽?", "det"),
 "2026-w42reel-sched/gapeul/ig/gab.mp4": ("나는 굽히기 싫은\n사람인가요?", "det"),
 "2026-w42reel-sched/ig/2026-10-07.mp4": ("나는 기준이 높은\n사람인가요?", "det"),
 "2026-w42reel-sched/ig/2026-10-08.mp4": ("나는 자유가 필요한\n사람인가요?", "det"),
 "2026-w42reel-sched/ig/2026-10-09.mp4": ("나는 마음을 읽는\n사람인가요?", "det"),
 "2026-w43swap/ig/harak_pair.mp4": ("내 하락이수는\n누구와 닮았나요?", "det"),
 "2026-w43swap/ig/juyeok_coins.mp4": ("내 동전 세 개는\n어떤 괘일까요?", "det"),
 "2026-w43swap/ig/liuyao_lines.mp4": ("내 바뀌는 선은\n몇 개일까요?", "det"),
 "2026-w43swap/ig/numerology_calc.mp4": ("내 숫자는\n무엇일까요?", "det"),
 "2026-w43swap/ig/numerology_life.mp4": ("내 생명수는\n몇 번일까요?", "det"),
 "2026-w43swap/ig/ziwei_pair.mp4": ("내 사주와 자미두수\n같은 말일까요?", "det"),
 "2026-earlybird/halloween.mp4": ("올해 핼러윈\n나는 어떤 마녀?", 7.8),
 "2026-pick/v3/2026-10-17.mp4": ("마음이 복잡한 날\n끌리는 카드는?", 8.2),
 "2026-pick/v3/2026-10-24.mp4": ("마음에 걸린 일\n어느 카드가 끌리나요?", 8.2),
 "reuse/n27-c1/reel.mp4": ("말 한마디로 분위기를\n바꾼 적 있나요?", "auto"),
 "reuse/n28-c1/reel.mp4": ("풀이 하나가 안 맞아\n걱정한 적 있나요?", "auto"),
 "reuse/n28-c2/reel.mp4": ("내 풀이는\n몇 개가 맞았나요?", "auto"),
 "reuse/n28-c3/reel.mp4": ("우리 궁합은\n몇 개가 맞나요?", "auto"),
 "reuse/n30-c1/reel.mp4": ("연애에서 먼저 식는 쪽\n나인가요?", "auto"),
 "reuse/n33-c1/reel.mp4": ("약속 취소가\n반가웠던 적 있나요?", "auto"),
 "reuse/n33-c2/reel.mp4": ("혼자 충전하는 나\n괜찮다고 느끼나요?", "auto"),
 "reuse/n33-c3/reel.mp4": ("이번 주 나를 위한\n충전은 무엇인가요?", "auto"),
 "reuse/n34-c1/reel.mp4": ("쉬는 밤에 드는 생각\n무엇인가요?", "auto"),
 "reuse/n35-c1/reel.mp4": ("월요일이 무거운 나\n어느 쪽인가요?", "auto"),
 "reuse/n36-c1/reel.mp4": ("끝을 못 내는 나\n힘이 빠지는 곳은?", "auto"),
 "reuse/n37-c1/reel.mp4": ("요즘 내 마음\n어디쯤 와 있나요?", "auto"),
 "reuse/n38-c1/reel.mp4": ("상강 무렵 나는\n무엇을 정리할까요?", "auto"),
 "reuse/n39-c1/reel.mp4": ("기다림이 힘든 나\n기한이 있나요?", "auto"),
 "reuse/n40-c1/reel.mp4": ("가족 모임 뒤 지친 나\n맡은 역할은?", "auto"),
 "reuse/n41-c1/reel.mp4": ("낯선 자리에서 나는\n말이 줄어드나요?", "auto"),
 "reuse/n42-c1/reel.mp4": ("섬세한 나\n무엇에 예민한가요?", "auto"),
 "reuse/n43-c1/reel.mp4": ("요즘 내 관계\n어떤 온도인가요?", "auto"),
 "reuse/n44-c1/reel.mp4": ("요즘 내 일상\n무엇이 가장 큰가요?", "auto"),
 "reuse/n45-c1/reel.mp4": ("요즘 내 선택\n마음이 기우는 쪽?", "auto"),
 "reuse/n46-c1/reel.mp4": ("이 달이 가기 전\n나는 무엇을 할까요?", "auto"),
}
# 끝 장면 모양을 돌려 쓴다(R19): 아래 항목은 ② 질문 크게+선택 알약, 나머지는 ④ 한 줄 정리+팔로우(글 효과만 다르게)
CH = {"2026-w42reel-sched/ig/2026-10-07.mp4": ("맞아요", "아니에요"), "2026-w40car6-reel/ig/2026-10-11.mp4": ("바로 해요", "생각해요"), "2026-w43swap/ig/liuyao_lines.mp4": ("1개", "2개 이상"),
      "reuse/n28-c3/reel.mp4": ("한두 개", "세 개"), "2026-w42reel-sched/ig/2026-10-09.mp4": ("맞아요", "아니에요"), "reuse/n39-c1/reel.mp4": ("있어요", "없어요"),
      "2026-w42reel-sched/gapeul/ig/eul.mp4": ("눕는 쪽", "서는 쪽"), "reuse/n28-c2/reel.mp4": ("한두 개", "세 개"), "reuse/n33-c2/reel.mp4": ("괜찮아요", "어색해요")}
if __name__ == "__main__":
    flt = sys.argv[1:]
    for n, (k, (q, mode)) in enumerate(M.items()):
        if flt and not any(f in k for f in flt): continue
        out = os.path.join(ROOT, "2026-r11", k.replace("/", "__"))
        if os.path.exists(out): continue
        src = os.path.join(ROOT, k)
        for pre, grp in (("2026-w40car6-reel/ig/", "w40"), ("2026-w42reel-sched/ig/", "sched"), ("2026-w42reel-sched/gapeul/ig/", "gapeul"), ("2026-w43swap/ig/", "swap")):
            if k.startswith(pre): src = os.path.join(ROOT, "2026-r11", "src", grp, k[len(pre):])      # 라벨을 고쳐 다시 렌더한 원본
        if not os.path.exists(src): print("원본 아직 없음", src); continue
        D = R.dur(src)
        cut = mode if isinstance(mode, float) else (D - 2.2 if mode == "auto" else (D if mode == "end" else R.last_cut(src, thr=0.15)))
        R.attach(src, out, q, cut=cut, fx=["zoom", "wipe", "slide"][n % 3], seed=11 + n, labels=CH.get(k))
