"""사주 밖 운명학 캐러셀 렌더(10/3 밤). 사용: EDITOR_HTML=pipeline/assets/carousel_editor_2026-10-03_v5.html python3 pipeline/topic_carousels.py [--check]
carousel_editor.render 와 같은 편집기·같은 LAYOUT_JS 를 쓰고, 5번 오행 차트 자리를 본문 카드로 바꾼다. 줄 폭 검사 결과를 출력한다."""
import sys, os, inspect
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "content"))
import carousel_editor as CE
import importlib
SETS = importlib.import_module(os.environ.get('TOPIC_SETS','topic_sets_w41')).SETS
CONVERT_JS = r"""
(x) => {
  const FONT='"Noto Sans CJK KR", sans-serif', F=(w,px)=>`${w} ${px}px ${FONT}`;
  const src = slides[1]; const s = Object.assign({}, src); s.panelOverride = Object.assign({}, src.panelOverride);
  s.type = 'body'; s.pageN = 5; s.badge = x.badges[3]; s.title = x.t5; s.body = x.b5;
  slides[4] = s;
  slides[1].badge = x.badges[0]; slides[2].badge = x.badges[1]; slides[3].badge = x.badges[2];
  const out = [];
  [4].forEach(i => { const q = slides[i]; const nb = wrapRich(q.body, W-60, F(700,54.5)).length, nt = wrapRich(q.title, W-100, F(900,100)).length;
    if (nb >= 3) { q.badgeY = 327; q.titleY = 541; q.bodyY = 841; } else { q.badgeY = 350; q.titleY = 597; q.bodyY = 902; }
    if (nt === 1) q.titleY += 61; });
  const tw=(t,w,px)=>{ ctx.font=F(w,px); return ctx.measureText(t).width; };
  [1,2,3,4,5].forEach(i => { const q = slides[i]; const tl = wrapRich(q.title, W-100, F(900,100)), bl = wrapRich(q.body, W-60, F(700,54.5));
    out.push([i+1, tl.length, bl.length, Math.round(Math.max(...q.title.split('\n').map(l=>tw(l,900,100)))), Math.round(Math.max(...q.body.split('\n').map(l=>tw(l,700,54.5))))]); });
  const c = slides[0]; (c.extraTexts||[]).forEach(e => { e.stroke = true; e.color = '#d9d3cd'; });   // 밝은 옷 위에서도 AI 고지가 읽히게 어두운 테두리(10/3 밤 확인: 밝기 114~197 표지에서 회색 글자가 묻힘)
  out.push(['cover', c.titleSize, c.subSize]);
  return out;
}
"""
def main():
    check = "--check" in sys.argv
    outdir = os.path.join(CE.ROOT, os.environ.get("TOPIC_OUT","2026-w41topic"))
    src = inspect.getsource(CE.render)
    old = "n = pg.evaluate(LAYOUT_JS, [d, None]); pg.wait_for_timeout(150)"
    assert old in src
    new = ("n = pg.evaluate(LAYOUT_JS, [d, None]); pg.evaluate(OVERRIDE_JS, S.get('_ov', {})); "
           "print('   검사', date, pg.evaluate(CONVERT_JS, S['_x'])); pg.wait_for_timeout(150)")
    src = src.replace(old, new)
    assert 'quality=93' in src; src = src.replace('quality=93', 'quality=97, subsampling=0, optimize=True')   # 10/4: 글자 가장자리 번짐(4:2:0) 줄이기
    if check: src = src.replace("imgs = []", "imgs = []; continue", 1)   # 이미지는 그리지 않고 검사만
    CE.CONVERT_JS = CONVERT_JS
    exec(src, CE.__dict__)
    sets = {}
    for date, t in SETS.items():
        sl = t["body"]
        s = dict(dayChar="", hanja="", accent=t["accent"], face=t["face"], kicker=t["kicker"], coverTitle=t["coverTitle"], coverSub=t["coverSub"],
                 personality=list(sl[0]), love=list(sl[1]), money=list(sl[2]), advice=list(t["advice"]), chartNote="", values=[0.3]*5, highlight=0,
                 ctaQ=t["ctaQ"], nextTitle=t["nextTitle"], variant=t["variant"])
        s["_ov"] = {"nextBadge": "다음 편", "nextTitle": t["nextTitle"]}
        s["_x"] = {"badges": t["badges"], "t5": sl[3][0], "b5": sl[3][1]}
        sets[date] = s
    CE.render(sets, outdir)
if __name__ == "__main__": main()
