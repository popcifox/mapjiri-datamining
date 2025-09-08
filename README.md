# mapjiri-datamining

카카오맵 기반 데이터 크롤링/정리 레포지토리입니다. 기본 크롤러(셀레니움/플레이라이트 기반)와 지역(대전) 별 스크립트, 메뉴 사전 등을 포함합니다.

## 주요 기능
- 카카오맵 장소/음식점 데이터 크롤링
- 자치구/행정동 단위의 배치 스크립트(대전 광역시)
- 키워드/메뉴 기반 수집 지원

## 폴더 구조(요약)
- `crawling/basic/`: 기본 크롤러 예제 및 Docker 환경
  - `main.py`: 기본 실행 진입점
  - `requirements.txt`: 파이썬 의존성
  - `Dockerfile`: 컨테이너 실행 환경
  - `install-browser.sh`, `chrome-deps.txt`: 브라우저 설치 스크립트/의존성
- `crawling/formatted_keywords.json`: 크롤링에 사용할 키워드 샘플
- `daejeon/`: 대전광역시 자치구/행정동 단위 스크립트 및 CSV
  - `daejeonDaedeokgu.py`, `daejeonDonggu.py`, `daejeonJunggu.py`, `daejeonSeogu.py`, `daejeonYueseonggu.py`
  - `대전광역시_*_행정동.csv`: 행정동 목록
- `menu/메뉴.csv`: 메뉴/키워드 사전
- `restauants_crawler.py`: 음식점 크롤러(루트). 파일명 오탈자에 유의하세요.

## 빠른 시작
사전 준비:
- Python 3.10 이상(권장), `pip` 사용 가능 환경
- Windows에서 크롬/크롬드라이버 또는 Playwright 설치 권장

### 1) 로컬 실행 (기본 크롤러)
작업 디렉터리: 레포 루트

의존성 설치:
```bash
pip install -r crawling/basic/requirements.txt
```

실행:
```bash
python crawling/basic/main.py
```

키워드 파일을 함께 사용하려면 `crawling/formatted_keywords.json`을 참고하여 스크립트 내 인자/설정을 조정하세요.

### 2) Docker 실행 (권장 재현 환경)
작업 디렉터리: `crawling/basic/`

이미지 빌드:
```bash
docker build -t mapjiri-basic:latest .
```

컨테이너 실행:
```bash
docker run --rm -it \
  -v "$PWD:/app" \
  mapjiri-basic:latest
```

Windows PowerShell에서는 경로 마운트 예시:
```powershell
docker run --rm -it `
  -v ${PWD}:/app `
  mapjiri-basic:latest
```

## 대전 지역 스크립트 실행
대전 각 자치구별 스크립트는 `daejeon/`에 위치합니다. 예시:
```bash
python daejeon/daejeonSeogu.py
```
스크립트는 같은 디렉터리의 `대전광역시_*_행정동.csv`를 참조하여 행정동 단위로 순회할 수 있습니다.

## 메뉴/키워드
- `menu/메뉴.csv`: 메뉴 용어 사전
- `crawling/formatted_keywords.json`: 크롤링 키워드 샘플(필요 시 편집하여 사용)

## 결과 저장
스크립트별로 결과 저장 경로/형식이 다를 수 있습니다. 기본값이나 출력 파일명은 각 스크립트 상단의 설정(상수/인자)을 확인하고 필요 시 수정하세요.

## 개발/기여
PR/이슈 환영합니다. 실행 중 오류(브라우저/의존성 등)가 있을 경우 OS/파이썬 버전, 실행 커맨드, 스택 트레이스를 포함해 이슈를 남겨주세요.

## 주의사항
- 크롤링 대상 서비스의 이용약관/로봇 배제정책을 준수하세요.
- 과도한 요청은 IP 차단 등 제재를 받을 수 있습니다. 지연/재시도 정책을 적절히 설정하세요.
