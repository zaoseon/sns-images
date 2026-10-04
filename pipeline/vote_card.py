"""일요일 질문(투표) 카드 1장 1080x1350. 샘플 서체(Noto Sans CJK KR 굵은 고딕, 왼쪽 정렬), 노란 배지, 번호 4개. 사용: python3 pipeline/vote_card.py -> 2026-w42vote/vote_vs.jpg"""
import os
from PIL import Image, ImageDraw, ImageFont
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
FP = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"; FM = "/usr/share/fonts/opentype/noto/NotoSansCJK-Medium.ttc"
def F(p, s): return ImageFont.truetype(p, s, index=1)
W, H = 1080, 1350; Y = (255, 214, 64)
def card(path, badge, q_lines, opts, foot, face="v8_gesture", qsize=92, bar_right=None):
    bar_right = bar_right or (W - 70)
    im = Image.new("RGB", (W, H), (22, 20, 18)); d = ImageDraw.Draw(im)
    f = F(FP, 40); w = d.textlength(badge, font=f) + 60; d.rounded_rectangle([70, 90, 70 + w, 90 + 76], 38, fill=Y); d.text((100, 128), badge, font=f, fill=(30, 26, 20), anchor="lm")
    y = 220
    for l in q_lines: d.text((70, y), l, font=F(FP, qsize), fill=(255, 255, 255)); y += int(qsize * 1.28)
    y += 40
    for n, t in opts:
        d.rounded_rectangle([70, y, bar_right, y + 118], 30, fill=(44, 40, 36)); d.ellipse([92, y + 22, 166, y + 96], fill=Y); d.text((129, y + 59), str(n), font=F(FP, 44), fill=(30, 26, 20), anchor="mm")
        d.text((196, y + 59), t, font=F(FM, 44), fill=(255, 255, 255), anchor="lm"); y += 142
    fp = os.path.join(ROOT, "characters", "cut", face + ".png")
    if os.path.exists(fp):
        fc = Image.open(fp).convert("RGBA"); r = 330 / fc.height; fc = fc.resize((int(fc.width * r), 330)); im.paste(fc, (W - fc.width - 40, H - 330 - 40), fc)
    fl = foot if isinstance(foot, list) else [foot]
    for k, l in enumerate(fl): d.text((70, H - 100 - (len(fl) - 1 - k) * 52), l, font=F(FM, 36), fill=(255, 255, 255) if (len(fl) > 1 and k == 0) else (255, 214, 64))
    d.text((70, H - 50), "zaoseon.com", font=F(FM, 30), fill=(168, 163, 158))
    im.save(path, quality=93)
if __name__ == "__main__":
    os.makedirs(os.path.join(ROOT, "2026-w42vote"), exist_ok=True)
    card(os.path.join(ROOT, "2026-w42vote", "vote_vs.jpg"), "정월의 질문", ["사주와 별자리가", "다른 말을 하면,", "나는?"],
         [(1, "사주 말이 더 맞는 것 같아요"), (2, "별자리 말이 더 맞는 것 같아요"), (3, "둘 다 조금씩 맞아요"), (4, "아직 잘 모르겠어요")], "번호로 댓글을 남겨 주세요")
    card(os.path.join(ROOT, "2026-w42vote", "quiz_four.jpg"), "정월의 퀴즈", ["여섯 운명학 중 넷 이상이", "같은 말을 하는 사람은", "100명 중 몇 명일까요?"],
         [(1, "약 50명"), (2, "약 30명"), (3, "약 15명"), (4, "약 5명")], ["번호로 답해 주세요", "정답은 11월 1일 릴스로 알려 드려요"], qsize=70, bar_right=700)
    print("ok")
