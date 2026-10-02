자오선 웹 인트로 v3 (최적화본)

[바뀐 점]
- 용량: 원본 약 10.1MB(index.html + assets) → 약 452KB (단독 HTML 약 585KB)
- 차트의 한자·별자리·숫자를 글자가 아니라 도형으로 바꿨습니다. 기기에 글꼴이 없어도 깨지지 않고, iOS/안드로이드에서 별자리 기호가 컬러 이모지로 바뀌지 않습니다.
- 모바일(너비 650px 이하)에서는 선과 글자를 더 굵고 진하게 한 차트(assets/chart-m.svg)를 씁니다.
- 글꼴은 이 페이지에 실제로 쓰인 글자만 담은 woff2입니다(제목 Noto Serif KR 900, 본문 Pretendard Variable). 이미지는 WebP입니다.
- 캐릭터·밤하늘 그림과 문구, 움직임 순서는 수정본 그대로입니다.

[파일]
- index.html + assets/ : 함께 두고 열면 재생됩니다.
- meridian_intro_standalone.html : 모든 것을 안에 넣은 단독 파일.
- meridian_intro_v3.mp4 : 같은 화면의 6초/24fps 출력(1280x720).
- compositions/ : 01 차트 배경, 02 캐릭터 결합본(패키지 원본 그대로), 03 PC 인트로, 04 모바일 인트로(새 판에서 다시 뽑음).

[문구를 고칠 때]
src/index.html 의 문구를 고친 뒤 `python3 build.py` 를 실행하면 글꼴이 다시 만들어집니다(제목에 새 글자가 들어가도 깨지지 않음).
필요: pip install fonttools brotli pillow, 제목 글꼴 원본 NotoSerifKR[wght].ttf (환경변수 NOTO_SERIF_KR 로 위치 지정).

[주의]
- 차트는 여섯 체계를 상징하는 그림이며 개인 명식 계산 결과가 아닙니다. 무료 풀이 결과 근처에 둘 때는 "예시 이미지"로 표기하세요.
- 캐릭터가 보이는 곳에는 "정월은 AI로 생성한 가상 캐릭터입니다" 표시가 필요합니다(화면 오른쪽 아래에 "AI 생성 캐릭터 · 상징적 차트" 포함).
- 글꼴 라이선스: assets/fonts 의 *-LICENSE.txt 참고(Noto Serif KR, Pretendard, DejaVu Sans는 차트 별자리 기호 도형에 사용).
- 사이트에 올리기 전에는 사이트가 이미 쓰는 폰트 파일을 다시 받지 않도록 맞춰야 합니다.
