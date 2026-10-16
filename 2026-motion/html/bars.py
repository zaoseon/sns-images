"""숫자가 쌓이는 모션 한 편 — HTML→MP4 길이 실제로 되는지 증명하는 조각(K-073 2단).

PIL 로는 막대가 자라고 숫자가 올라가는 것을 프레임마다 손으로 계산해야 한다.
CSS·JS 는 그것을 그냥 한다. 그래서 '숫자·표가 쌓이는 과정'(K-073 2단)에는 이 길이 맞다.

규칙은 그대로 지킨다
  크기·안전 영역  channel_specs (숫자를 여기 박지 않는다)
  고정 요소      brand_frame (자오선 · 동서양 6개 운명학 교차분석 · zaoseon.com)
  판            color_combos
  글꼴          fonts_kit (base64 로 넣어 헤드리스에서도 같은 글꼴)
  첫 줄         체계 이름 금지(K-102) — "같은 나를 두고 / 왜 말이 다를까요?"
  움직임        정보를 나르는 데만 쓴다(K-073) — 막대가 자라며 숫자가 올라간다

사용: python3 2026-motion/html/bars.py
"""
import os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "pipeline"))
import channel_specs as CS, fonts_kit as K, brand_frame as BF, html_motion as HM

CH = CS.CH["reel"]
W, H = CH["w"], CH["h"]
SX0, SY0, SX1, SY1 = CH["safe"]
PAL = {x["id"]: x for x in json.load(open(os.path.join(ROOT, "assets", "palettes", "color_combos.json"), encoding="utf-8"))["palettes"]}
T = PAL["dg_gold_s"]["theme"]

# 실제로 우리가 센 숫자다(무작위 3,000명). 지어낸 값이 아니다.
막대 = [("사주와 하락이수", 24), ("사주와 별자리", 17), ("사주와 숫자", 14)]
최대 = 30


def html():
    bars = "\n".join(
        f'<div class=row><div class=lab>{n}</div>'
        f'<div class=track><div class=fill data-v="{v}" style="--w:{v / 최대 * 100}%"></div></div>'
        f'<div class=num data-v="{v}">0%</div></div>'
        for n, v in 막대)
    return f"""<!doctype html><html><head><meta charset=utf-8><style>
{K.css_inline(display="pl")}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:{W}px;height:{H}px;background:{T['bg']};overflow:hidden;
     font-family:'JW-B',sans-serif;color:{T['ink']}}}
.safe{{position:absolute;left:{SX0}px;top:{SY0}px;width:{SX1-SX0}px;height:{SY1-SY0}px}}
/* 세로 자리: 안전 영역 330~1470 안에서 끝나야 한다. 아래 고정 줄(zaoseon.com)이 y1465 라
   거기까지 내려가면 겹친다 — 10/16 처음 돌렸을 때 셋째 막대와 겹쳤다. */
h1{{font-family:'JW-D',sans-serif;font-size:96px;line-height:1.25;margin-top:70px;
    opacity:0;transform:translateY(40px)}}
.sub{{font-size:44px;color:{T['acc']};margin-top:20px;opacity:0}}
.rows{{margin-top:70px}}
.row{{margin-bottom:32px;opacity:0}}
.lab{{font-size:38px;color:{T['sub']};margin-bottom:10px}}
.track{{height:32px;background:{T['card']};border-radius:16px;overflow:hidden}}
.fill{{height:100%;width:0;background:{T['acc']};border-radius:16px}}
.num{{font-family:'JW-D',sans-serif;font-size:60px;color:{T['acc']};margin-top:8px}}
.end{{margin-top:24px;font-size:46px;opacity:0}}
{BF.css()}
</style></head><body>
<div class=safe>
  <h1 id=h1>같은 나를 두고<br>왜 말이 다를까요?</h1>
  <div class=sub id=sub>무작위 3,000명을 하나하나 세어 봤어요</div>
  <div class=rows id=rows>{bars}</div>
  <div class=end id=end>같은 말이 나오는 곳이 타고난 자리예요</div>
</div>
{BF.html('reel')}
<script>
// 시각을 우리가 지정한다 — 몇 번을 돌려도 같은 영상이 나온다(화면 녹화와 다른 점).
const E=(x)=>x<0?0:x>1?1:1-Math.pow(1-x,3);
const rows=[...document.querySelectorAll('.row')];
window.seek=(t)=>{{
  const h1=document.getElementById('h1'), sub=document.getElementById('sub'), end=document.getElementById('end');
  let p=E((t-0.1)/0.7); h1.style.opacity=p; h1.style.transform=`translateY(${{(1-p)*40}}px)`;
  sub.style.opacity=E((t-0.8)/0.6);
  rows.forEach((r,i)=>{{
    const s=1.8+i*0.9;                       // 막대가 하나씩 자란다
    r.style.opacity=E((t-s)/0.4);
    const f=r.querySelector('.fill'), n=r.querySelector('.num');
    const g=E((t-s-0.15)/1.1);
    f.style.width=`calc(${{g}} * var(--w))`;
    n.textContent=Math.round(g*(+n.dataset.v))+'%';
  }});
  end.style.opacity=E((t-5.6)/0.7);
}};
window.seek(0);
</script></body></html>"""


def main():
    p = os.path.join(HERE, "bars.html")
    open(p, "w", encoding="utf-8").write(html())
    out, dur = HM.render(p, "bars_3000", 초=8.0, fps=30)
    print(f"  {os.path.relpath(out, ROOT)} · {dur:.1f}초")


if __name__ == "__main__":
    main()
