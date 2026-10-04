"""10/1~10/11 밤 6개를 사주·별자리·숫자 테스트로 교체 + 무료 한 줄 사주 번호 다시 매기기(10/5부터 1번, 팔로워 먼저). 9/30"""
import json, os
HT = "#사주 #운세"
DIFF = "사주 하나, 별자리 하나만 보면 한쪽 이야기만 듣게 돼요.\n자오선은 여섯 가지 운명학을 겹쳐서, 같은 답이 나오는 곳을 찾아요."
IG_CTA = "맞다 싶으면 ♥, 떠오르는 사람이 있으면 공유하거나 태그해 주세요.\n매일 저녁, 나를 알아보는 테스트가 올라와요. 놓치지 않으려면 팔로우해 두세요."
TH_CTA = "맞으면 하트, 아니면 댓글로 반박해 주세요.\n떠오르는 사람이 있으면 태그!"
P = []
def x(date, tag, title, hook, rows, note, q, iht, nxt):
    lines = "\n".join(f"{r[0]}({r[1]}): {r[2]} - {r[3]}" for r in rows)
    tease = f"내일 저녁: {nxt}. 팔로우해 두면 이어서 볼 수 있어요."
    th = f"{hook}\n\n사주·별자리·숫자로 보면 이래요.\n{lines}\n\n{note}\n\n{q}\n\n{TH_CTA}\n{tease}\n\n#{tag}"
    ig = f"{hook}\n\n사주·별자리·숫자로 보면 이래요.\n{lines}\n\n{note}\n{q}\n\n{IG_CTA}\n{tease}\n\n{DIFF}\n이 내용은 재미로, 그리고 나를 돌아보는 계기로 봐 주세요.\n\n{HT} {iht}"
    assert len(th) <= 500, (date, len(th))
    P.append(dict(date=date, slot="pm", tag=tag, threads=[th], instagram=ig, threads_image=False,
                  image=dict(type="cross", title=title, rows=rows, note=note, foot=f"내일 저녁 · {nxt}")))
