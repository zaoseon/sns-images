"""예약 릴스 음악 정리(대표 10/13 08:02 '데이터 릴스 음악 변경', R33: 느린 곡 금지·밝은 장조·템포 114 이상).
10/13 전수 대조: 예약 릴스 중 R33을 어긴 곡은 데이터 릴스 7편(별자리·자미두수·당사주·육효·하락이수·혼자·교차)과 2027 하늘 일정(sky-2027)뿐이었다
(옛 기록이 느린 곡(오르골·맑은 팝) 또는 템포 104~108이었음). 곡은 새로 받지 않고 저장소의 합성 곡 4종(상큼 팝·발랄 우쿨렐레·경쾌 신스팝·통통 마림바, pipeline/reel_music.py)만 쓴다.
이웃 영상(예약 시각 앞뒤 3편)과 같은 곡·같은 조가 겹치지 않게 PICK 표로 정했고, 같은 틀(데이터 릴스)끼리도 (곡, 조)가 다르고 곡 하나를 2편까지만 쓴다.
사용: python3 pipeline/music_fix_1013.py log            -> content/music_log.json 의 해당 항목을 PICK 으로 바꿈
      python3 pipeline/music_fix_1013.py mux 이름 파일.mp4  -> 영상은 그대로 두고 소리만 바꿈(장면 길이에 맞춰 컷 박자 맞춤)"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.abspath(os.path.join(HERE, "..")); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(R, "content"))
PICK = {   # 이름: (곡, 조, 템포, 씨앗)
 "v2-star":   ("발랄 우쿨렐레", "G", 116, 811), "v2-ziwei": ("통통 마림바", "F", 118, 812), "v2-alone": ("상큼 팝", "A", 122, 813), "v2-dang": ("경쾌 신스팝", "D", 120, 814),
 "v2-four":   ("경쾌 신스팝", "E", 120, 815),   "v2-liuyao": ("통통 마림바", "G", 118, 816), "sky-2027": ("상큼 팝", "D", 122, 817), "v2-harak": ("발랄 우쿨렐레", "C", 116, 818),
}
def write_log():
    LOG = os.path.join(R, "content", "music_log.json"); lg = json.load(open(LOG, encoding="utf-8"))
    for x in lg:
        if x["name"] in PICK: s, k, b, sd = PICK[x["name"]]; x.update(style=s, mode="up", bpm=b, key=k, seed=sd)
    json.dump(lg, open(LOG, "w", encoding="utf-8"), ensure_ascii=False, indent=1); print("music_log 갱신", len(PICK), "곡")
def durs_of(name):
    if name == "sky-2027":
        import clips_motion_2027 as C; return [d for d, _ in C.SC]
    import data_reels_v2 as D; return [d for d, _ in D.REELS[name.split("-")[1]][0]()]
if __name__ == "__main__":
    if sys.argv[1] == "log": write_log()
    else:
        import music_plan as MP
        name, mp4 = sys.argv[2], sys.argv[3]; lg = {x["name"]: x for x in json.load(open(os.path.join(R, "content", "music_log.json"), encoding="utf-8"))}; info = lg[name]
        MP.mux(mp4, durs_of(name), info, info["seed"]); print("소리 교체", name, info["style"], info["key"], info["bpm"])
