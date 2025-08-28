# MongoDB 데이터 로더

이 스크립트는 `개념.txt`, `진단테스트.txt`, `단원테스트_full버전.txt` 파일을 MongoDB에 저장하는 Python 스크립트입니다.

## 기능

- **개념 데이터**: 수학 개념과 설명, 연습문제 등을 저장
- **진단테스트 데이터**: 진단 테스트 세트와 문제들을 저장  
- **단원테스트 데이터**: 단원별 테스트 문제들을 저장
- **자동 인덱싱**: 성능 향상을 위한 데이터베이스 인덱스 자동 생성
- **로깅**: 상세한 로그 기록 및 파일 저장

## 설치 및 설정

### 1. 의존성 패키지 설치

```bash
pip install -r requirements.txt
```

### 2. MongoDB 설정

MongoDB가 실행 중이어야 합니다. 기본적으로 `localhost:27017`에 연결을 시도합니다.

#### 환경변수 설정 (선택사항)

`.env` 파일을 생성하여 MongoDB 연결 정보를 설정할 수 있습니다:

```env
MONGODB_URI=mongodb://localhost:27017/
MONGODB_DB=seeds_db
```

## 사용법

### 기본 실행

```bash
python loadtomongodb.py
```

### 코드에서 사용

```python
from loadtomongodb import MongoDBLoader

# 로더 초기화
loader = MongoDBLoader("mongodb://localhost:27017/")

# 데이터베이스 연결
if loader.connect("seeds_db"):
    # 모든 데이터 로드
    success = loader.load_all_data("AI/data")
    
    # 개별 데이터 로드
    # loader.load_concepts("AI/data/개념.txt")
    # loader.load_diagnostic_tests("AI/data/진단테스트.txt")
    # loader.load_unit_tests("AI/data/단원테스트_full버전.txt")
    
    # 통계 확인
    stats = loader.get_collection_stats()
    
    # 연결 해제
    loader.disconnect()
```

## 데이터 구조

### 1. 개념 (concepts)
- `conceptId`: 고유 개념 ID
- `unitId`: 단원 ID
- `unitCode`: 단원 코드
- `unitTitle`: 단원 제목
- `blocks`: 개념 블록 (설명, 연습문제 등)

### 2. 진단테스트 (diagnostic_tests)
- `test`: 테스트 정보 (ID, 사용자, 등급 범위 등)
- `problems`: 문제 목록

### 3. 단원테스트 (unit_tests)
- `code`: 단원 코드
- `title`: 단원 제목
- `problems`: 문제 목록

## 컬렉션 및 인덱스

스크립트는 다음 컬렉션을 생성합니다:

- `concepts`: 개념 데이터
- `diagnostic_tests`: 진단테스트 데이터
- `unit_tests`: 단원테스트 데이터

각 컬렉션에는 성능 향상을 위한 인덱스가 자동으로 생성됩니다.

## 로그

스크립트 실행 시 다음 로그 파일이 생성됩니다:
- `mongodb_loader.log`: 상세한 로그 기록

## 오류 처리

- MongoDB 연결 실패 시 적절한 오류 메시지 출력
- 파일 읽기 실패 시 상세한 오류 정보 제공
- 데이터 삽입 실패 시 롤백 처리

## 주의사항

1. **기존 데이터 삭제**: 스크립트는 실행 시 기존 데이터를 모두 삭제하고 새로 로드합니다.
2. **파일 경로**: 기본적으로 `AI/data/` 디렉토리에서 파일을 찾습니다.
3. **MongoDB 버전**: MongoDB 4.0 이상을 권장합니다.

## 문제 해결

### MongoDB 연결 실패
- MongoDB 서비스가 실행 중인지 확인
- 연결 문자열과 포트 번호 확인
- 방화벽 설정 확인

### 파일 읽기 실패
- 파일 경로가 올바른지 확인
- 파일 인코딩이 UTF-8인지 확인
- 파일 권한 확인

### 데이터 삽입 실패
- MongoDB 로그 확인
- 디스크 공간 확인
- 데이터 형식 검증
