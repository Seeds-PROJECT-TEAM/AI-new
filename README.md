# Seeds AI Math Tutor Project

AI 기반 수학 교육 플랫폼

## 🚀 프로젝트 개요

이 프로젝트는 AI를 활용한 맞춤형 수학 교육 시스템입니다. 학생의 진단테스트 결과를 바탕으로 개인화된 학습 경로를 생성하고, OpenAI GPT 모델을 활용한 챗봇을 통해 수학 문제 해결을 지원합니다.

## 🏗️ 기술 스택

### 백엔드
- **Python 3.9+** - 메인 백엔드 언어
- **FastAPI 0.104.1** - 웹 API 프레임워크
- **Uvicorn 0.24.0** - ASGI 서버

### 데이터베이스
- **MongoDB 4.6.0** - 메인 데이터베이스 (수학 문제, 진단테스트, 학습경로)
- **Neo4j 5.15.0** - 그래프 데이터베이스 (개념 간 관계, 선수개념)

### AI/ML
- **OpenAI API 1.3.7** - GPT 모델 기반 AI 서비스
- **LangChain** - RAG(Retrieval-Augmented Generation) 구현
- **LangGraph** - AI 워크플로우 및 에이전트 관리

### 기타 도구
- **Mathpix API** - 수학 공식 및 수식 이미지 인식 및 변환
- **Pytest** - Python 백엔드 테스트 프레임워크

## 📁 프로젝트 구조

```
Seeds-PROJECT-TEAM/
├── AI/                    # 메인 애플리케이션
│   ├── app/              # FastAPI 애플리케이션
│   ├── data/             # 데이터 파일들
│   └── scripts/          # 데이터 처리 스크립트
├── docs/                  # 문서 및 스키마
├── scripts/               # 유틸리티 스크립트
├── tests/                 # 테스트 파일들
├── logs/                  # 로그 파일들
└── requirements.txt       # Python 의존성
```

## 🚀 시작하기

### 1. 환경 설정
```bash
# 가상환경 생성
python -m venv venv

# 가상환경 활성화
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 의존성 설치
pip install -r requirements.txt
```

### 2. 환경변수 설정
`.env` 파일을 생성하고 다음 변수들을 설정하세요:
```env
MONGODB_URI=your_mongodb_connection_string
OPENAI_API_KEY=your_openai_api_key
AURA_URI=your_neo4j_connection_string
AURA_USER=your_neo4j_username
AURA_PASS=your_neo4j_password
```

### 3. 서버 실행
```bash
# AI 애플리케이션 실행
cd AI/app
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 🔧 주요 기능

- **진단테스트 시스템** - 학생 수준 파악 및 분석
- **맞춤형 학습 경로** - AI 기반 개인화 학습 계획
- **개념 기반 학습** - Neo4j 그래프 기반 선수개념 분석
- **AI 챗봇** - OpenAI 기반 수학 문제 해결 지원
- **RAG 시스템** - LangChain 기반 지식 검색 및 생성

## 📚 API 문서

서버 실행 후 다음 URL에서 API 문서를 확인할 수 있습니다:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🧪 테스트

```bash
# 테스트 실행
cd tests
pytest

# 특정 테스트 실행
pytest test_learning_path.py
```

## 📝 라이선스

이 프로젝트는 교육 목적으로 개발되었습니다.

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
