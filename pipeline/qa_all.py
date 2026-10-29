"""올리기 전 검사 — 한 번에(10/7 확정 제작 가이드 8장). 하나라도 걸리면 종료 코드 1, 앱에 올리지 않는다.
사용: python3 pipeline/qa_all.py          (글 검사만, 수 초)  python3 pipeline/qa_all.py --videos   (영상 배치까지, 약 10분)  python3 pipeline/qa_all.py --images   (그림 속 글자 OCR 포함)
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
    SCHED_MUSIC = ("v2-star", "v2-ziwei", "v2-dang", "v2-liuyao", "v2-harak", "v2-alone", "v2-four", "sky-2027")   # 10/13: 예약된 데이터 릴스·2027 하늘 일정도 R33(up 곡·템포 114 이상)
    out["음악 경쾌(R33: 예약 데이터 릴스·하늘 일정도 up 곡·템포 114 이상)"] = len([1 for x in lg if x["name"] in SCHED_MUSIC and (x.get("mode") != "up" or x.get("bpm", 0) < 114)])
    import clips_motion_zodiac as ZL0
    _o = ("원숭이띠", "개띠", "용띠", "뱀띠", "말띠", "양띠", "닭띠", "돼지띠", "쥐띠"); out["배경 다양(R34: 이웃 영상 배경이 달라야 함)"] = len([1 for a, b in zip(_o, _o[1:]) if ZL0.PLAN[a]["bg"] == ZL0.PLAN[b]["bg"]])
    import clips_motion_zodiac as ZL
    out["영상 장면 배치(박스 글·간격·묶음 위치, R27~R29)"] = len(ZL.zodiac_lint())
    import carousel_rules as CRL   # R58(대표 10/12): 예약된 인스타 캐러셀은 7장 이상
    out["인스타 캐러셀 7장 이상(R58: 표지·본문·해 볼 것·CTA)"] = len(CRL.scan_archive())
    import clip_from_reel as CFR   # D-190(대표 10/12): 릴스 재활용 네이버 클립 — 설명글·문구·소리 없음·규격
    bad = CFR.audit(CFR.spec())
    for c in CFR.spec()["clips"]:
        mp = os.path.join(CFR.OUT, c["id"] + ".mp4")
        if not os.path.exists(mp): bad.append((c["id"], "클립 영상 없음(렌더 필요)"))
        else: bad += [(c["id"], x) for x in CFR.verify(c, mp)[0]]
    out["네이버 클립(릴스 재활용): 설명 300자·태그 5·금지어·소리 없음·1080x1920"] = len(bad)
    import clip_v2 as CV2   # 10/15 대표: 네이버 클립은 하루 1개, 같은 틀 반복 금지(설명 첫·끝 줄, 같은 문장, 태그 묶음·고정 자리, 이웃 날 첫 장면 모양)
    sp2 = json.load(open(CV2.SPEC, encoding="utf-8")); bad2 = CV2.audit(sp2)
    for c in sp2["clips"]:
        if not os.path.exists(os.path.join(CV2.OUT, c["id"] + ".mp4")): bad2.append((c["id"], "클립 영상 없음(python3 pipeline/clip_v2.py)"))
    out["네이버 클립 v2: 하루 1개·같은 틀 반복·금지어·마음과 관계·설명 300자"] = len(bad2)
    # 10/15 대표 2차 지적: v2는 제작 가이드 확정판 규칙을 안 따름 -> v3(content/clips_v3.py, 규칙 엔진). 자막·배치 엄격 검사는 렌더할 때 clips_v3.py가 한다(느려서 여기선 설명 글·영상 파일만)
    sp3 = json.load(open(os.path.join(R, "content", "clips_v3.json"), encoding="utf-8"))["clips"]; bad3 = []
    for k, c in sp3.items():
        d = c["desc"]
        if not os.path.exists(os.path.join(R, "clips_v3s", k + ".mp4")): bad3.append((k, "영상 없음(python3 content/clips_v3.py)"))
        if "http" in d or "상" + "담" in d: bad3.append((k, "주소·금지어"))
        if any(len(x) > 60 for x in d.split("\n")): bad3.append((k, "한 줄 60자 넘음"))
        if not any(w in d for w in ("마음", "관계")): bad3.append((k, "마음·관계 줄 없음"))
    out["네이버 클립 v3: 영상 있음·설명 한 줄 60자·금지어·마음과 관계"] = len(bad3)
    import sub_rules as SR   # 대표 10/13: 릴스 자막 규칙 R60~R67 (소스 장면표에서 수집, 예약본은 완화 기준·STRICT_IDS 영상은 엄격 기준). 걸리면 해당 영상을 고쳐 다시 렌더
    out["릴스 자막(R60 줄 수·R61 줄 길이·R63 컷 길이·R64 덩어리 수·R65 겹침)"] = sum(len(v) for v in SR.run(gate=True).values())
    import banned_words_audit as BW   # 대표 10/12 23:15: '상담' 계열 금지(예외 심리상담사). 소스 전수(두 저장소)·앱 대기 캡션·네이버 미발행 원고
    out["금지어 '상담'(두 저장소 소스·앱 대기 캡션·네이버 미발행 원고)"] = len(BW.scan())
    import thread_rules as TR   # K-136(대표 10/18 07:53): 스레드 글은 인스타 캡션 검사(capfix) 대신 스레드 문법 검사 — 10/18 뒤 앱에 올린 스레드 글
    out["스레드 글 문법(K-136: 500자·태그 1·반말·인스타 고정 문구 금지·행동 유도 줄·끝 어울림)"] = len(TR.run())
    import disclaimer_audit as DA   # K-128(대표 10/17): '재미로…' 면책 문장은 캡션·스레드·네이버 원고·클립에 넣지 않는다(만드는 코드 + 아직 안 나간 글)
    out["면책 문장 '재미로…'(K-128: 만드는 코드·승인 대기 캡션·안 올린 클립 설명·발행 전 원고)"] = len(DA.run())
    sys.path.insert(0, os.path.join(R, "naver")); import cover_audit as CVA   # 대표 10/15: 상강 대표 이미지 목록에서 또 잘림. 글자형 구도는 얼굴 가운데(QCS)만
    out["네이버 대표 이미지(가운데 720 안·글자형은 얼굴 가운데)"] = len(CVA.run())
    if "--images" in sys.argv or "--videos" in sys.argv: out["금지어 '상담' 그림 속 글자(카드 그림 OCR, 느림)"] = len(BW.scan_images())
    return out
def spec_checks():
    """제작 코드가 규격을 읽고 있는지(대표 10/16 "코드 규칙으로 박아놓고 제작에 꼭 반영").
    기존 16곳은 빚으로 적어 두고 새로 생기는 것만 막는다."""
    import card_gate as G
    새, 빚 = G.spec_lint()
    for x in 새:
        print("   ", x)
    if 빚:
        print(f"    (규격을 안 읽는 옛 파일 {빚}곳이 남아 있어요 — content/audit/spec_lint_baseline.json, 건드리는 김에 갚으세요)")
    return {"제작 코드가 채널 규격을 읽는가(새로 생긴 것만)": len(새)}


def set_checks():
    """세트를 통째로 — 캐러셀 장 수(최소 7장, R58)·CTA·속 빈 장.
    대표 10/16 "CTA도 없고 내용도 부실하게 총 3장짜리 캐러셀 만들어지는 그런건 안된다."
    7장 규칙은 가이드라인에만 글로 있었고 코드가 보지 않았다. 빌더 하나가 아니라
    저장소 안의 모든 사양(*/cards.json)을 여기서 센다."""
    import glob, card_gate as G
    나쁨 = []
    for p in sorted(glob.glob(os.path.join(R, "*", "cards.json"))):
        try:
            d = json.load(open(p, encoding="utf-8"))
        except Exception as e:
            나쁨.append(f"{os.path.relpath(p, R)} 를 못 읽어요: {e}")
            continue
        나쁨 += G.세트(d.get("cards") or [], channel="insta_carousel",
                      한편=bool(d.get("한 편")), 이름=os.path.basename(os.path.dirname(p)))
    for x in 나쁨:
        print("   ", x)
    return {"캐러셀 세트(최소 7장·CTA·속 빈 장·심리 한 장 K-022)": len(나쁨)}


def naver_state_checks():
    """네이버 글 상태가 실제와 어긋나 있는지(10/17).
    10/17 에 드러난 일: 예약 시각이 지나 네이버에서 이미 발행된 글 30편을 published.json 이
    아직 'scheduled'·'planned' 로 알고 있었다. 그 바람에 세션이 "54편 남았다"처럼
    사실과 다른 숫자로 보고했다. 파일은 저절로 바뀌지 않으므로 여기서 잰다.
    주소도 같이 본다 — 발행된 글의 주소가 없으면 연결글 카드·클립 연결을 걸 수 없다
    (주소는 서브 노트북 `주소채우기.bat` 가 채운다)."""
    import datetime
    오늘 = datetime.date.today()
    d = json.load(open(os.path.join(R, "naver", "published.json"), encoding="utf-8"))
    지났는데_안바뀜, 발행인데_주소없음 = [], []
    for k, v in sorted(d.items()):
        try:
            날 = datetime.date(*map(int, v["date"].split("-")))
        except Exception:
            continue
        if 날 <= 오늘 and v.get("status") != "published":
            지났는데_안바뀜.append(k)
        if v.get("status") == "published" and not (v.get("url") or "").strip():
            발행인데_주소없음.append(k)
    if 지났는데_안바뀜:
        print("    나갈 시각이 지났는데 상태가 그대로인 글:", " ".join(지났는데_안바뀜),
              "— 네이버에서 확인하고 published 로 고치세요")
    if 발행인데_주소없음:
        print(f"    발행됐는데 주소가 없는 글 {len(발행인데_주소없음)}편 —"
              " 서브 노트북에서 주소채우기.bat 를 돌리세요(연결글 카드·클립 연결이 이 주소를 씁니다)")
    return {"네이버 글 상태가 실제와 맞는가": len(지났는데_안바뀜)}


def k131_checks():
    """K-131(대표 10/17): 네이버 본문 그림 — 다시 그린 글은 도식 2종 이상·옛 틀 2장 이하·이웃 글 첫 도식 다르게. 옛 글은 빚으로 센다."""
    sys.path.insert(0, os.path.join(R, "naver")); import k131_check as KC
    reg_p = os.path.join(R, "naver", "diagrams.json")
    pages = json.load(open(os.path.join(R, "naver", "pages.json"), encoding="utf-8")); reg = json.load(open(reg_p, encoding="utf-8")) if os.path.exists(reg_p) else {}
    bad, debt = KC.check(pages, reg)
    for k, v in KC.k135_check(pages, reg).items(): bad.setdefault(k, []).extend(v)   # K-135 그림 거리(3판 이후 글)
    for k, v in bad.items(): print("   ", k, "; ".join(v))
    if debt: print(f"    (아직 옛 틀인 네이버 글 {len(debt)}편 — data/naver_redraw_plan.json 배치대로 줄인다)")
    return {"네이버 본문 도식(K-131, 다시 그린 글)": len(bad)}


def video_checks():
    out = {}
    import audit_assets as AU, layout_audit as LA
    a = AU.audit(); out["상단 문구·주소 위치(앱 대기 영상·그림)"] = sum(1 for x in a if x["status"] == "미적용")
    PV = __import__("pilot_variety"); PV.AUDIT = True; bad = 0
    for g in ("pilots", "reels", "clips", "misc"):
        res, tot, b = LA.run_group(g); bad += b
    out["글·그림 배치(맨 위 475↑·맨 아래 1375↓·가운데 910±35) 기준 밖 장면"] = bad
    return out

def first_frame_checks():
    """K-139(대표 10/18): 10/19 뒤 올릴 클립(content/post_clips.json)의 0초 프레임에 제목이 보이는지."""
    import re, datetime
    sys.path.insert(0, os.path.join(R, "pipeline")); import clip_first_frame as CFF
    today = datetime.date.today().isoformat(); bad = 0
    for c in json.load(open(os.path.join(R, "content", "post_clips.json"), encoding="utf-8")):
        if (c.get("rec") or "") < max(today, "2026-10-19"): continue
        m = re.search(r"/sns-images/[^/]+/(.+\.mp4)$", c.get("video") or "")
        if not m: continue
        f = os.path.join(R, m.group(1))
        if not os.path.exists(f): continue
        b = CFF.check(f)
        if b: bad += 1; print("   ", c["id"], b[0])
    return {"클립 0초 프레임에 제목(K-139, 올릴 클립)": bad}

def faint_checks():
    """K-138(대표 10/18): 네이버 원고 본문 그림 중 이 환경에 있는 것을 재서 글자가 배경에 묻힌(대비 1.9 밑) 그림을 센다.
    발행 전(done 아님) 글 + 다시 그린 글(k131 꼬리표)의 그림. 그림 파일이 없는 곳(sparse)은 건너뛴다."""
    import re as _re
    from urllib.parse import unquote
    sys.path.insert(0, os.path.join(R, "pipeline")); import faint_gate as FG
    pages = json.load(open(os.path.join(R, "naver", "pages.json"), encoding="utf-8")); seen = set(); bad = 0
    for pid, v in pages.items():
        if v.get("done") and not v.get("k131"): continue
        for u in _re.findall(r'naver/img/([^"/]+\.jpg)"', v.get("body", "")):
            n = unquote(u)
            if n in seen or "cta" in n: continue
            seen.add(n); f = os.path.join(R, "naver", "img", "m1280", n)
            if not os.path.exists(f): continue
            h = FG.hits(f)
            if h: bad += 1; print("   ", pid, n, f"대비 {min(x[2] for x in h)}:1")
    return {"그림 글자 묻힘(K-138, 발행 전·다시 그린 글 본문 그림)": bad}

def intent_checks():
    """K-143(대표 10/18): 검색 의도 카드(naver/intent_cards.json) — 반영(applied)한 글의 첫 3줄·연결글·CTA가 카드와 맞는지. 카드 없는 글은 빚으로 숫자만."""
    sys.path.insert(0, os.path.join(R, "naver")); import intent_check as IC
    bad, wait, none = IC.run()
    for k, v in bad.items(): print("   ", k, "; ".join(v))
    if wait or none: print(f"    (의도 카드 반영 대기 {len(wait)}편 · 카드 없는 글 {len(none)}편 — B4·B5 다시 그리기 때 채운다)")
    return {"네이버 검색 의도 카드(K-143: 첫 3줄 답·연결글·CTA)": len(bad)}

def k151_checks():
    """K-151(대표 10/20) + blogon 진단 검토(10/29): 새로 쓰는 네이버 원고에 고정 첫 인사·'결론부터' 문장, 첫 200자 핵심어 직답, 제목 40자·비하 표현, 태그('자오선' 끝·핵심어). 예약·발행 글은 기준선에 묶어 안 잼."""
    sys.path.insert(0, os.path.join(R, "naver")); import k151_check as KK
    bad, new = KK.run()
    for k, v in bad.items(): print("   ", k, "; ".join(v))
    return {"네이버 새 원고 틀 반복·첫 답·제목·태그(K-151)": len(bad)}

def old_terms_checks():
    """K-086(대표 10/16): '세 지도' 같은 옛 표현이 앞으로 나갈 원고·승인 카드·클립 글에 없는지. 낱말 원본 copy_rules.옛표현."""
    import old_terms_audit as OT
    bad = OT.run()
    for b in bad: print("   ", " · ".join(map(str, b)))
    return {"옛 표현(K-086 세 지도 등): 앞으로 나갈 원고·카드·클립 글": len(bad)}

if __name__ == "__main__":
    res = text_checks()
    res.update(spec_checks())
    res.update(set_checks())
    res.update(naver_state_checks())
    res.update(k131_checks())
    res.update(first_frame_checks())
    res.update(faint_checks())
    res.update(intent_checks())
    res.update(old_terms_checks())
    res.update(k151_checks())
    if "--videos" in sys.argv: res.update(video_checks())
    fail = {k: v for k, v in res.items() if v}
    for k, v in res.items(): print(("통과 " if not v else f"걸림 {v}개 ") + "· " + k)
    json.dump(dict(결과=res, 통과=not fail), open(os.path.join(R, "content", "audit", "qa_all.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("전체:", "통과" if not fail else f"걸린 검사 {len(fail)}가지 — 올리지 않는다"); sys.exit(1 if fail else 0)
