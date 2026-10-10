"""올리기 전 검사 — 한 번에(10/7 확정 제작 가이드 8장). 하나라도 걸리면 종료 코드 1, 앱에 올리지 않는다.
사용: python3 pipeline/qa_all.py          (글 검사만, 수 초)  python3 pipeline/qa_all.py --videos   (영상 배치까지, 약 10분)
결과: content/audit/qa_all.json"""
import os, sys, json, re
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.abspath(os.path.join(HERE, "..")); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(R, "content"))
def text_checks():
    out = {}
    import linebreak_audit as LB, claims_audit as CA, caption_rules as CR
    files = [os.path.join(R, "content", x) for x in ("pilot_variety.py", "clips_motion_2027.py", "clips_motion_zodiac.py", "reels_engine.py")] + [os.path.join(R, "pipeline", x) for x in ("data_reels.py", "new_tri_reels.py", "pick_reel.py", "motion_dots.py", "motion_kinetic.py")]
    out["줄바꿈(서술어만 남기기 금지)"] = len(LB.scan(files))
    out["문구 안전(확신·불안·단정)"] = len([1 for w, t in CA.corpus() for k, m in CA.scan_text(t)])
    d = json.load(open(os.path.join(R, "content", "reel_swaps.json"), encoding="utf-8")); out["캡션(프로필 링크 1개·팔로우·반복 금지)"] = len([1 for i, p in CR.audit_all(d) if p])
    import capfix as CF
    ru = json.load(open(os.path.join(R, "content", "reuse.json"), encoding="utf-8")); out["릴스 캡션 전체 구성(CTA·팔로우·프로필 링크 1·브랜드 문장·면책·태그 5·줄 길이)"] = len([1 for r in ru if CF.check(r.get("caption", ""))])
    import natural_audit as NA
    out["자연스러운 한국어(어색한 의문형·번역투)"] = len(NA.scan())
    import trendy_audit as TA
    out["트렌디 표현 사용 규칙"] = len(TA.run()[0])
    lg = json.load(open(os.path.join(R, "content", "music_log.json"), encoding="utf-8")); out["음악 경쾌(R33: 띠 릴스는 밝은 up 곡·템포 112 이상)"] = len([1 for x in lg if x["name"].startswith("zodiac-") and (x.get("mode") != "up" or x.get("bpm", 0) < 112)])
    import clips_motion_zodiac as ZL0
    _o = ("원숭이띠", "개띠", "용띠", "뱀띠", "말띠", "양띠", "닭띠", "돼지띠", "쥐띠"); out["배경 다양(R34: 이웃 영상 배경이 달라야 함)"] = len([1 for a, b in zip(_o, _o[1:]) if ZL0.PLAN[a]["bg"] == ZL0.PLAN[b]["bg"]])
    import clips_motion_zodiac as ZL
    out["영상 장면 배치(박스 글·간격·묶음 위치, R27~R29)"] = len(ZL.zodiac_lint())
    return out
def video_checks():
    out = {}
    import audit_assets as AU, layout_audit as LA
    a = AU.audit(); out["상단 문구·주소 위치(앱 대기 영상·그림)"] = sum(1 for x in a if x["status"] == "미적용")
    PV = __import__("pilot_variety"); PV.AUDIT = True; bad = 0
    for g in ("pilots", "reels", "clips", "misc"):
        res, tot, b = LA.run_group(g); bad += b
    out["글·그림 배치(맨 위 475↑·맨 아래 1375↓·가운데 910±35) 기준 밖 장면"] = bad
    return out
if __name__ == "__main__":
    res = text_checks()
    if "--videos" in sys.argv: res.update(video_checks())
    fail = {k: v for k, v in res.items() if v}
    for k, v in res.items(): print(("통과 " if not v else f"걸림 {v}개 ") + "· " + k)
    json.dump(dict(결과=res, 통과=not fail), open(os.path.join(R, "content", "audit", "qa_all.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("전체:", "통과" if not fail else f"걸린 검사 {len(fail)}가지 — 올리지 않는다"); sys.exit(1 if fail else 0)
