"""인스타·스레드에 올리는 영상에 네이버 전용 CTA(\"블로그 스티커 눌러 보기\")가 남아 있지 않은지 점검한다 (10/5 대표 지적, 10/4 s10 클립이 네이버용 그대로 인스타에 올라감).
 1) reuse/<id>/reel.mp4(인스타용 재활용)가 네이버용 파일(clips_sop/*, clips_post/*, */naver/*, */naver_music/*)과 바이트가 같으면 실패
 2) content/reel_swaps.json의 인스타·스레드용 영상 경로(상태 skip 제외, 글 연결 클립·네이버 클립·카페 제외)가 네이버용 폴더를 가리키면 실패
사용: python3 pipeline/check_ig_videos.py   (예약 전·후에 돌린다. 문제가 있으면 목록을 보이고 종료 코드 1)"""
import os, sys, re, json, glob, hashlib
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
NAVER = ["clips_sop/*.mp4", "clips_post/*/*.mp4", "*/naver/*.mp4", "*/naver_music/*.mp4"]
SKIP_KINDS = ("글 연결 클립", "네이버 클립", "네이버 카페")
def h(p):
    m = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): m.update(b)
    return m.hexdigest()
def main():
    bad = []
    nv = {h(p): os.path.relpath(p, ROOT) for pat in NAVER for p in glob.glob(os.path.join(ROOT, pat))}
    for p in sorted(glob.glob(os.path.join(ROOT, "reuse", "*", "reel.mp4"))):
        k = h(p)
        if k in nv: bad.append(f"재활용 영상 {os.path.relpath(p, ROOT)} 이(가) 네이버용 {nv[k]} 와 똑같음 (인스타용 CTA 끝 장면이 없음)")
    for x in json.load(open(os.path.join(ROOT, "content", "reel_swaps.json"), encoding="utf-8")):
        v = re.sub(r".*/main/", "", x.get("video") or "")
        if x.get("status") == "skip" or x.get("kind") in SKIP_KINDS or not v: continue
        if re.search(r"/naver/|naver_music|clips_sop|clips_post", v): bad.append(f"새 영상 계획 {x['id']}({x['kind']} {x['date']} {x['time']})가 네이버용 영상 {v} 를 가리킴")
    print(f"인스타·스레드 영상 점검: 문제 {len(bad)}건 (네이버용 파일 {len(nv)}개와 대조)"); [print(" -", b) for b in bad]
    return 1 if bad else 0
if __name__ == "__main__": sys.exit(main())
