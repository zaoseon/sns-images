# 글꼴 사용 조건 (우리가 쓰는 글꼴)
모두 **SIL Open Font License 1.1(OFL)** 이다. 상업적 사용·수정·재배포가 되고, **글꼴 파일을 단독으로 판매하거나 라이선스를 바꾸는 것만 금지**다. 2026-10-05 공식 안내로 확인함.
| 글꼴 | 쓰는 곳 | 공식 배포처 | 파일 |
|---|---|---|---|
| G마켓 산스 (Gmarket Sans, Bold·Medium) | 릴스·클립 제목 | corp.gmarket.com/fonts (G마켓) | GmarketSansBold.ttf, GmarketSansMedium.ttf |
| 페이퍼로지 (Paperlogy, 이주임·페이퍼로지) | 카루셀·카드 제목 | freesentation.blog/paperlogyfont | Paperlogy-7Bold/8ExtraBold/9Black.ttf |
| 프리텐다드 (Pretendard) | 모든 본문 | github.com/orioncactus/pretendard | PRETENDARD-*.OTF |
- 페이퍼로지는 한글 2,780자만 들어 있다(자주 안 쓰는 글자는 없음). 없는 글자가 있으면 `fonts_kit.missing()`이 알려 주고 G마켓 산스로 바꾼다.
- 한자(東西數)는 위 글꼴에 없어서 명조체(`serif.otf`)만 쓴다.

## 2026-10-15 점검 (대표 요청, 노션 '무료 폰트 50' 2026-10-14 표와 대조)
- 쓰는 3종: G마켓 산스·페이퍼로지·프리텐다드 → 표에서 로고 사용·파일 전달 모두 "가능". 한자용 노토 세리프(`serif.otf`, Noto Serif CJK KR)는 OFL이며 표에는 없다.
- 코드가 부르지 않는 파일 8개가 있다(`pipeline/render.py` 12~13행에서 이름만 정의, 어디에서도 쓰지 않음): BM-DOHYEON, BM-EULJIRO, BM-HANNAPRO, BM-JUA(배민 폰트), NEXON-LV2-BOLD, MAPLESTORY-BOLD, NANUMSQUARE-ROUND-EB, LINE-SEED-SANS-BOLD.
  - 노션 표 기준: 메이플스토리(48번)는 파일 전달 "금지", 주아체(18번)는 "가능". 나머지 7개는 표에 이름이 없어 이 자료로는 확인되지 않는다.
  - 이 저장소는 공개라서 "파일 전달 금지" 폰트를 두면 안 된다. 대표 결정 후 지운다(지워도 과거 기록에는 남는다).
- 시스템 노토 CJK(`/usr/share/fonts/opentype/noto/`)는 한자·보조 글자와 일부 보조 도구(`images_to_clip.py`, `vote_card.py`, `reel_editor.py`, `carousel.py`의 한자)에서 쓴다. OFL이다.
- 2026-10-15 대표 승인: 위 미사용 폰트 8개 파일을 저장소에서 삭제했다. `render.py`의 이름 정의도 지웠다.
