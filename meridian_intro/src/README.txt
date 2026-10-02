자오선 웹 인트로 v3 (최적화본)

[바뀐 점]
- 용량: 원본 약 10.1MB(index.html + assets) → 약 459KB (단독 HTML 약 585KB)
- 차트의 한자·별자리·숫자를 글자가 아니라 도형으로 바꿨습니다. 기기에 글꼴이 없어도 깨지지 않고, iOS/안드로이드에서 별자리 기호가 컬러 이모지로 바뀌지 않습니다.
- 모바일(너비 650px 이하)에서는 선과 글자를 더 굵고 진하게 한 차트(assets/chart-m.svg)를 씁니다.
- 글꼴은 이 페이지에 실제로 쓰인 글자만 담은 woff2입니다(제목 Noto Serif KR 900, 본문 Pretendard Variable). 이미지는 WebP입니다.
- 캐릭터·밤하늘 그림과 문구, 움직임 순서는 수정본 그대로입니다.

[파일]
- index.html + assets/ : 함께 두고 열면 재생됩니다(웹 페이지용, 다시 재생·일시 정지 버튼 포함).
- meridian_intro_standalone.html : 모든 것을 안에 넣은 단독 파일.
- reel.html : 영상(릴스·클립)용 세로 전용 배치. 버튼 없음. 같은 글꼴·이미지.
- video/meridian_intro_vertical.mp4 : 릴스·클립용 세로 1080x1920, 30fps, 6초, 소리 없음, 버튼 없음. 네이버 클립 재생 화면(위 y<125, 오른쪽 x>=905, 아래 y>=1485)과 인스타 릴스 아래 영역을 피해 배치.
- video/meridian_intro_pc_nobuttons.mp4 : 가로 1280x720, 24fps, 6초, 소리 없음, 버튼 없음.
- compositions/ : 01 차트 배경, 02 캐릭터 결합본(패키지 원본 그대로), 03 PC 인트로, 04 모바일 인트로(새 판에서 다시 뽑음).
- 영상은 릴스·클립에만 씁니다. 사이트에는 올리지 않습니다(대표 방침). 영상에는 버튼을 넣지 않습니다.
- 영상에 음악을 넣을 때: 인스타는 예약 도구로 올리기 전에 영상에 음악을 입히고, 네이버 클립은 앱에서 직접 고릅니다.

[문구를 고칠 때]
src/index.html(웹용)과 src/reel.html(영상용)의 문구를 고친 뒤 `python3 build.py` 를 실행하면 글꼴이 다시 만들어집니다(제목에 새 글자가 들어가도 깨지지 않음). 영상은 reel.html 을 1080x1920으로 열어 seekIntro(ms)로 프레임을 찍어 ffmpeg로 만듭니다.
필요: pip install fonttools brotli pillow, 제목 글꼴 원본 NotoSerifKR[wght].ttf (환경변수 NOTO_SERIF_KR 로 위치 지정).

[주의]
- 차트는 여섯 체계를 상징하는 그림이며 개인 명식 계산 결과가 아닙니다. 무료 풀이 결과 근처에 둘 때는 "예시 이미지"로 표기하세요.
- 캐릭터가 보이는 곳에는 "정월은 AI로 생성한 가상 캐릭터입니다" 표시가 필요합니다(화면에 "AI 생성 캐릭터 · 상징적 차트" 포함).
- 글꼴 라이선스: assets/fonts 의 *-LICENSE.txt 참고(Noto Serif KR, Pretendard, DejaVu Sans는 차트 별자리 기호 도형에 사용).
