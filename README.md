# 자오선 SNS 운영 저장소

인스타그램·스레드 **zaoseon.jeongwol** 계정의 게시물 이미지와 제작 도구를 보관합니다.
Metricool(브랜드 id 7114921, zaoseon@gmail.com)이 이 저장소의 공개 주소에서 이미지를 가져가 예약 게시합니다.

## 폴더

- `2026-w40/` 등 : 2주 단위 게시물 이미지 (폴더 이름 = 시작 주차)
- `content/` : 2주 단위 게시물 원고 JSON (글, 캡션, 태그, 이미지 설계)
- `pipeline/render.py` : JSON -> 이미지 렌더러 (1080x1350)
- `pipeline/fonts/` : Noto Serif KR, Pretendard (둘 다 OFL 라이선스)
- `pipeline/assets/` : 정월 캐릭터 원본

## 2주마다 하는 일 (Claude 작업 순서)

1. 이 저장소를 clone 한다. 접근 키는 대표에게 받는다(키 이름 zaoseon-sns, sns-images 저장소 전용).
2. `content/YYYY-wNN.json` 을 쓴다. 게시물 28개(하루 아침 8시, 저녁 9시).
3. `python3 pipeline/render.py content/YYYY-wNN.json` 으로 이미지를 만든다.
4. 이미지를 확인하고 commit, push 한다.
5. Metricool `createScheduledPost` 로 인스타, 스레드를 각각 예약한다.
   - 이미지 주소: `https://raw.githubusercontent.com/zaoseon/sns-images/main/<폴더>/<파일>`
   - 주간 기운: 인스타는 9장 슬라이드, 스레드는 글 3개 이어쓰기(descendants)
6. `getScheduledPosts` 로 건수를 확인하고, 아래 기록 표에 한 줄 추가한다.

## 게시물 구성 원칙

- 비율: 성격, 관계가 절반 이상. 일, 돈은 일부. 운명학 소개, 절기 이야기.
- 매주 월요일 아침: 이번 주 날마다의 기운(일진). 날 이름을 반드시 풀어서 설명한다.
- 전문용어는 쓰면 바로 풀어 쓴다. "엔진" 표현 금지. 대시 대신 하이픈(-).
- 참여 글("생년월일을 댓글로")은 팔로워 100명 이상일 때 주 1~2회.
- 판매 문장(크몽)은 게시물 5개 중 1개 이하.
- 정월 얼굴이 들어간 이미지에는 "가상인물 · AI로 생성한 캐릭터" 표시.

## content JSON 형식

```json
{"posts":[
 {"date":"2026-10-12","slot":"am","tag":"운세",
  "threads":["첫 글", "이어쓰기(선택)"], "instagram":"캡션 + 해시태그",
  "image":{"type":"week","start":"2026-10-12","days":[{"mean":"첫 줄\n둘째 줄","tip":"한마디"}]}},
 {"date":"2026-10-12","slot":"pm","tag":"사주","threads":["글"],"instagram":"캡션",
  "image":{"type":"card","title":"제목","lines":["줄","→ 금색 줄"],"foot":"아래 문구"}},
 {"image":{"type":"trait","kicker":"작은 제목","big":"큰 제목","mark":"甲",
           "rows":[["성격","..."],["사랑","..."]],"tip":"정월의 한마디"}}
]}
```

`tti` 형식(2027 띠별 캐러셀 5장): name, mark, years, one, hook, rel, why, good/save(달 번호, 13=이듬해 1월), color, num, dir, money, work, people, do, dont. 필드 예시는 `content/build_2026-w42.py`.
게시물에 `"threads_image": false` 를 넣으면 스레드는 이미지 없이 글만 예약한다.
`pipeline/payloads.py` 는 JSON을 Metricool 예약 입력(인스타·스레드 따로)으로 바꿔 /tmp/payloads.json 에 쓴다.

`week` 형식은 `render.week_texts()` 가 스레드 3개 글과 인스타 캡션을 자동으로 만든다.

## 기록

| 폴더 | 기간 | 예약 | 비고 |
|---|---|---|---|
| 2026-w40 | 9/28 ~ 10/11 | 56건 (28x2) | 첫 2주 |
| 2026-w42 | 10/12 ~ 10/25 | 56건 (28x2) + 테스트 릴스 12 | 2027 띠별 캐러셀, 무료 한 줄 사주 1·2, TOP3. 10/25 아침은 10:00 |
