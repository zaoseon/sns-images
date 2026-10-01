"""2027 신년 감정서 얼리버드 홍보 5장 - 샘플(정) 레이아웃 그대로(표지 / 본문 3 / CTA). 문구와 가격은 기존 예약 캡션(10/2 18:30)과 같다."""
import os, sys, io, base64
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import carousel_editor as CE
from playwright.sync_api import sync_playwright
from PIL import Image
D = dict(dayChar="", hanja="", accent="#f36435", face="v2_straight", kicker="2027 신년 감정서", coverTitle="열두 달을\n달력처럼", coverSub="10월 얼리버드, 선착순 50명",
    personality=["열두 달을\n달력처럼 펼쳐요", "힘을 쓸 달과 아낄 달,\n그달에 해 볼 일 하나까지\n정리해 드려요."],
    love=["사주 하나로\n보지 않아요", "사주·자미두수·당사주·하락이수\n점성술·수비학, 여섯 지도를\n겹쳐서 읽어요."],
    money=["10월 31일까지\n선착순 50명", "STANDARD 19,000 → 14,900원\nDELUXE 39,000 → 29,000원\nPREMIUM 59,000 → 45,000원"],
    advice=["", ""], chartNote="", values=[.3,.3,.3,.3,.3], highlight=0, ctaQ="2027년, 어느 달에\n힘을 쓰면 좋을까요?", nextTitle="zaoseon.com/ny")
OV = dict(badges=["구성", "방법", "얼리버드"], nextBadge="10월 얼리버드", nextTitle="zaoseon.com/ny", btn="프로필 링크에서 신청해요", hint="프로필 링크 → 감정서 → 2027 신년")
CE.build_html()
if not os.path.exists(CE.PLATE): CE.make_plate()
out = os.path.join(CE.ROOT, "2026-w40car3")
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1300, "height": 900}); pg.goto("file:///tmp/editor_noto.html"); pg.wait_for_timeout(1500)
    pg.evaluate("Promise.all([400,500,600,700,900].map(w=>document.fonts.load(w+' 40px \"Noto Sans CJK KR\"','가한丁')))")
    pg.evaluate("async ([k,u])=>{FACES[k]=u; const im=new Image(); im.src=u; await im.decode(); imgCache[k]=im;}", ["chart_plate", "data:image/png;base64," + base64.b64encode(open(CE.PLATE, "rb").read()).decode()])
    pg.evaluate(CE.LAYOUT_JS, [D, None]); pg.evaluate(CE.OVERRIDE_JS, OV); pg.wait_for_timeout(150)
    for n, i in enumerate((0, 1, 2, 3, 6), 1):
        url = pg.evaluate(f"(()=>{{active={i}; draw(false); return cv.toDataURL('image/png');}})()")
        Image.open(io.BytesIO(base64.b64decode(url.split(",")[1]))).convert("RGB").save(os.path.join(out, f"ny_{n}.jpg"), quality=93)
    b.close()
print("ok")
