import os
import sys
from dotenv import load_dotenv

# AI 디렉토리를 Python 경로에 추가
sys.path.append(os.path.join(os.path.dirname(__file__), 'AI'))

# 환경 변수 로드
load_dotenv('AI/.env')

from AI.app.services.diagnostic_service import DiagnosticService
from AI.app.services.mongo_service import MongoService
from AI.app.services.ai_comment_service import AICommentService

def create_virtual_mongodb_data():
    """가상의 MongoDB 데이터를 생성하여 맞춤형 학습경로 테스트"""
    
    # 가상의 problems 데이터
    virtual_problems = [
        {
            "problemId": "1.1 소수와 합성수, 소인수분해",
            "unitId": "unit_001",
            "grade": 1,
            "chapter": 1,
            "unit": "1. 수와 연산",
            "unitName": "1. 수와 연산",
            "subject": "math",
            "title": "소수와 합성수, 소인수분해"
        },
        {
            "problemId": "1.2 최대공약수와 최소공배수",
            "unitId": "unit_001",
            "grade": 1,
            "chapter": 1,
            "unit": "1. 수와 연산",
            "unitName": "1. 수와 연산",
            "subject": "math",
            "title": "최대공약수와 최소공배수"
        },
        {
            "problemId": "1.3 정수와 유리수",
            "unitId": "unit_001",
            "grade": 1,
            "chapter": 1,
            "unit": "1. 수와 연산",
            "unitName": "1. 수와 연산",
            "subject": "math",
            "title": "정수와 유리수"
        },
        {
            "problemId": "1.4 절댓값",
            "unitId": "unit_001",
            "grade": 1,
            "chapter": 1,
            "unit": "1. 수와 연산",
            "unitName": "1. 수와 연산",
            "subject": "math",
            "title": "절댓값"
        },
        {
            "problemId": "1.5 정수와 유리수의 덧셈, 뺄셈",
            "unitId": "unit_001",
            "grade": 1,
            "chapter": 1,
            "unit": "1. 수와 연산",
            "unitName": "1. 수와 연산",
            "subject": "math",
            "title": "정수와 유리수의 덧셈, 뺄셈"
        },
        {
            "problemId": "2.1 문자와 식",
            "unitId": "unit_002",
            "grade": 1,
            "chapter": 2,
            "unit": "2. 문자와 식",
            "unitName": "2. 문자와 식",
            "subject": "math",
            "title": "문자와 식"
        },
        {
            "problemId": "2.2 일차식의 사칙 연산",
            "unitId": "unit_002",
            "grade": 1,
            "chapter": 2,
            "unit": "2. 문자와 식",
            "unitName": "2. 문자와 식",
            "subject": "math",
            "title": "일차식의 사칙 연산"
        },
        {
            "problemId": "2.4 일차방정식의 풀이",
            "unitId": "unit_002",
            "grade": 1,
            "chapter": 2,
            "unit": "2. 문자와 식",
            "unitName": "2. 문자와 식",
            "subject": "math",
            "title": "일차방정식의 풀이"
        }
    ]
    
    # 가상의 units 데이터
    virtual_units = [
        {
            "unitId": "unit_001",
            "title": {"ko": "수와 연산", "en": "Numbers and Operations"},
            "chapterTitle": "수와 연산",
            "grade": 1,
            "chapter": 1,
            "subject": "math",
            "description": "정수와 유리수의 기본 개념과 연산"
        },
        {
            "unitId": "unit_002",
            "title": {"ko": "문자와 식", "en": "Expressions and Equations"},
            "chapterTitle": "문자와 식",
            "grade": 1,
            "chapter": 2,
            "subject": "math",
            "description": "문자와 식의 기본 개념과 일차방정식"
        }
    ]
    
    return virtual_problems, virtual_units

def test_diagnostic_with_virtual_data():
    """가상 데이터로 진단테스트 실행"""
    
    print("🚀 가상 MongoDB 데이터로 맞춤형 학습경로 테스트 시작...")
    print()
    
    # 가상 데이터 생성
    virtual_problems, virtual_units = create_virtual_mongodb_data()
    
    print("📚 가상 문제 데이터:")
    for problem in virtual_problems:
        print(f"  - {problem['problemId']} → {problem['unit']}")
    print()
    
    print("📚 가상 단원 데이터:")
    for unit in virtual_units:
        print(f"  - {unit['unitId']}: {unit['title']['ko']}")
    print()
    
    # 진단테스트 데이터
    test_data = {
        "testId": "virtual_mongodb_test",
        "userId": 12500,
        "gradeRange": "중1-중3",
        "totalProblems": 8,
        "durationSec": 300,
        "answers": [
            {
                "problemId": "1.1 소수와 합성수, 소인수분해",
                "userAnswer": {"selectedOption": 2, "value": None},
                "isCorrect": False,
                "durationSeconds": 45
            },
            {
                "problemId": "1.2 최대공약수와 최소공배수",
                "userAnswer": {"selectedOption": 1, "value": None},
                "isCorrect": True,
                "durationSeconds": 60
            },
            {
                "problemId": "1.3 정수와 유리수",
                "userAnswer": {"selectedOption": 3, "value": None},
                "isCorrect": False,
                "durationSeconds": 50
            },
            {
                "problemId": "1.4 절댓값",
                "userAnswer": {"selectedOption": None, "value": "x = 3"},
                "isCorrect": True,
                "durationSeconds": 40
            },
            {
                "problemId": "1.5 정수와 유리수의 덧셈, 뺄셈",
                "userAnswer": {"selectedOption": 2, "value": None},
                "isCorrect": False,
                "durationSeconds": 55
            },
            {
                "problemId": "2.1 문자와 식",
                "userAnswer": {"selectedOption": 1, "value": None},
                "isCorrect": False,
                "durationSeconds": 65
            },
            {
                "problemId": "2.2 일차식의 사칙 연산",
                "userAnswer": {"selectedOption": None, "value": "2x + 3"},
                "isCorrect": True,
                "durationSeconds": 70
            },
            {
                "problemId": "2.4 일차방정식의 풀이",
                "userAnswer": {"selectedOption": 3, "value": None},
                "isCorrect": False,
                "durationSeconds": 80
            }
        ]
    }
    
    print("📊 진단테스트 데이터:")
    print(f"  - 테스트 ID: {test_data['testId']}")
    print(f"  - 사용자 ID: {test_data['userId']}")
    print(f"  - 학년 범위: {test_data['gradeRange']}")
    print(f"  - 총 문제 수: {test_data['totalProblems']}")
    print(f"  - 오답 수: {sum(1 for answer in test_data['answers'] if not answer['isCorrect'])}")
    print(f"  - 정답 수: {sum(1 for answer in test_data['answers'] if answer['isCorrect'])}")
    print()
    
    # 진단서비스 초기화 (가상 데이터로 모킹)
    try:
        # MongoDB 서비스 초기화
        mongo_service = MongoService()
        
        if not mongo_service.is_connected:
            print("❌ MongoDB 연결 실패 - 가상 데이터로 테스트 진행")
            # 가상 데이터를 MongoDB에 임시로 삽입 (테스트 후 삭제)
            problems_collection = mongo_service._db.problems
            units_collection = mongo_service._db.units
            
            # 기존 데이터 백업
            original_problems = list(problems_collection.find())
            original_units = list(units_collection.find())
            
            # 가상 데이터 삽입
            for problem in virtual_problems:
                problems_collection.insert_one(problem)
            
            for unit in virtual_units:
                units_collection.insert_one(unit)
            
            print("✅ 가상 데이터를 MongoDB에 임시 삽입 완료")
            
            # 진단서비스로 테스트 실행
            diagnostic_service = DiagnosticService(mongo_service, None)
            
            # 가상 데이터로 단원 분석 테스트
            print("\n🔍 가상 데이터로 단원 분석 테스트:")
            wrong_units = diagnostic_service._analyze_wrong_units_from_neo4j(test_data['answers'])
            weak_concepts = diagnostic_service._analyze_weak_concepts_from_neo4j(test_data['answers'])
            
            print(f"✅ 분석 결과:")
            print(f"  - 취약 단원: {wrong_units}")
            print(f"  - 취약 개념: {weak_concepts}")
            
            # 추천 경로 생성 테스트
            print("\n🔍 추천 경로 생성 테스트:")
            accuracy_rate = (sum(1 for answer in test_data['answers'] if answer['isCorrect']) / len(test_data['answers'])) * 100
            recommended_path = diagnostic_service._generate_recommended_path(wrong_units, accuracy_rate)
            
            print(f"✅ 추천 경로:")
            for i, path in enumerate(recommended_path, 1):
                print(f"  {i}. {path['unitTitle']} (우선순위: {path['priority']})")
                print(f"     이유: {path['reason']}")
            
            # 가상 데이터 제거
            problems_collection.delete_many({"testId": "virtual_mongodb_test"})
            units_collection.delete_many({"unitId": {"$in": ["unit_001", "unit_002"]}})
            
            # 원본 데이터 복원
            for problem in original_problems:
                problems_collection.insert_one(problem)
            for unit in original_units:
                units_collection.insert_one(unit)
            
            print("\n✅ 가상 데이터 제거 및 원본 데이터 복원 완료")
            
        else:
            print("✅ MongoDB 연결 성공 - 실제 데이터와 함께 테스트")
            # 실제 MongoDB 데이터가 있는 경우 테스트
            diagnostic_service = DiagnosticService(mongo_service, None)
            
            # 단원 분석 테스트
            print("\n🔍 단원 분석 테스트:")
            wrong_units = diagnostic_service._analyze_wrong_units_from_neo4j(test_data['answers'])
            weak_concepts = diagnostic_service._analyze_weak_concepts_from_neo4j(test_data['answers'])
            
            print(f"✅ 분석 결과:")
            print(f"  - 취약 단원: {wrong_units}")
            print(f"  - 취약 개념: {weak_concepts}")
            
            # 추천 경로 생성 테스트
            print("\n🔍 추천 경로 생성 테스트:")
            accuracy_rate = (sum(1 for answer in test_data['answers'] if answer['isCorrect']) / len(test_data['answers'])) * 100
            recommended_path = diagnostic_service._generate_recommended_path(wrong_units, accuracy_rate)
            
            print(f"✅ 추천 경로:")
            for i, path in enumerate(recommended_path, 1):
                print(f"  {i}. {path['unitTitle']} (우선순위: {path['priority']})")
                print(f"     이유: {path['reason']}")
    
    except Exception as e:
        print(f"❌ 테스트 실행 중 오류 발생: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_diagnostic_with_virtual_data()
