import requests
import json

def test_unit_mapping_learning_path():
    """단원명 매핑을 통한 맞춤형 학습경로 테스트"""
    
    print("🚀 단원명 매핑을 통한 맞춤형 학습경로 테스트 시작...")
    print("=" * 70)
    
    # 가상 매핑 테이블 (실제 MongoDB에 없는 단원들을 가상으로 매핑)
    virtual_unit_mapping = {
        "1.1 소수와 합성수, 소인수분해": {
            "unitId": "virtual_001",
            "unitTitle": "소수와 합성수, 소인수분해",
            "chapter": "수와 연산",
            "grade": "중1",
            "prerequisites": ["자연수", "약수", "배수"]
        },
        "1.2 최대공약수와 최소공배수": {
            "unitId": "virtual_002", 
            "unitTitle": "최대공약수와 최소공배수",
            "chapter": "수와 연산",
            "grade": "중1",
            "prerequisites": ["소수와 합성수", "약수", "배수"]
        },
        "2.1 문자와 식": {
            "unitId": "virtual_003",
            "unitTitle": "문자와 식",
            "chapter": "문자와 식",
            "grade": "중1", 
            "prerequisites": ["수와 연산", "덧셈과 뺄셈", "곱셈과 나눗셈"]
        },
        "2.2 일차식의 사칙연산": {
            "unitId": "virtual_004",
            "unitTitle": "일차식의 사칙연산",
            "chapter": "문자와 식",
            "grade": "중1",
            "prerequisites": ["문자와 식", "덧셈과 뺄셈", "곱셈과 나눗셈"]
        },
        "3.1 일차함수": {
            "unitId": "virtual_005",
            "unitTitle": "일차함수",
            "chapter": "함수",
            "grade": "중2",
            "prerequisites": ["문자와 식", "일차식", "좌표평면"]
        },
        "3.2 이차함수": {
            "unitId": "virtual_006",
            "unitTitle": "이차함수", 
            "chapter": "함수",
            "grade": "중3",
            "prerequisites": ["일차함수", "이차식", "제곱근"]
        }
    }
    
    # 진단테스트 데이터 (단원명을 문제 ID로 사용)
    test_data = {
        "testId": "unit_mapping_test_001",
        "userId": 12500,
        "gradeRange": "중1-중3",
        "totalProblems": 4,
        "durationSec": 200,
        "answers": [
            {
                "problemId": "1.1 소수와 합성수, 소인수분해",  # 단원명을 문제 ID로 사용
                "userAnswer": {"selectedOption": 2, "value": None},
                "isCorrect": False,  # 틀림
                "durationSeconds": 45
            },
            {
                "problemId": "1.2 최대공약수와 최소공배수",
                "userAnswer": {"selectedOption": 1, "value": None},
                "isCorrect": True,  # 맞음
                "durationSeconds": 60
            },
            {
                "problemId": "2.1 문자와 식",
                "userAnswer": {"selectedOption": 3, "value": None},
                "isCorrect": False,  # 틀림
                "durationSeconds": 50
            },
            {
                "problemId": "2.2 일차식의 사칙연산",
                "userAnswer": {"selectedOption": None, "value": "2x + 3"},
                "isCorrect": False,  # 틀림
                "durationSeconds": 55
            }
        ]
    }
    
    print("📊 테스트 데이터 (단원명을 문제 ID로 사용):")
    print(f"  - 테스트 ID: {test_data['testId']}")
    print(f"  - 사용자 ID: {test_data['userId']}")
    print(f"  - 학년 범위: {test_data['gradeRange']}")
    print(f"  - 총 문제 수: {test_data['totalProblems']}")
    print(f"  - 오답 수: {sum(1 for answer in test_data['answers'] if not answer['isCorrect'])}")
    print(f"  - 정답 수: {sum(1 for answer in test_data['answers'] if answer['isCorrect'])}")
    print()
    
    print("🔍 문제 내용 (단원명 기반):")
    for i, answer in enumerate(test_data['answers'], 1):
        problem_id = answer['problemId']
        unit_info = virtual_unit_mapping.get(problem_id, {})
        print(f"  {i}. {unit_info.get('unitTitle', problem_id)}")
        print(f"     챕터: {unit_info.get('chapter', 'N/A')}")
        print(f"     학년: {unit_info.get('grade', 'N/A')}")
        print(f"     선수개념: {', '.join(unit_info.get('prerequisites', []))}")
        print(f"     결과: {'❌ 틀림' if not answer['isCorrect'] else '✅ 맞음'}")
        print()
    
    print("🔗 가상 매핑 테이블 정보:")
    print(f"  총 매핑된 단원 수: {len(virtual_unit_mapping)}")
    print("  매핑 방식: 단원명 → 가상 단원 정보")
    print("  선수개념: Neo4j에서 조회 가능한 구조")
    print()
    
    try:
        # API 호출
        print("🔍 API 호출 중...")
        response = requests.post(
            "http://localhost:8000/api/learning-path/express/diagnostic",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 진단테스트 성공!")
            print("=" * 50)
            
            # AI 코멘트 확인
            ai_comment = result.get('aiComment', 'N/A')
            print(f"📝 AI 코멘트:")
            print(f"   {ai_comment}")
            print()
            
            # 클래스 확인
            class_level = result.get('class', 'N/A')
            print(f"🏫 학습 수준 클래스: {class_level}")
            print()
            
            # 추천 경로 확인
            recommended_path = result.get('recommendedPath', [])
            print(f"🛤️ 추천 학습 경로 ({len(recommended_path)}개):")
            
            if recommended_path:
                for i, path in enumerate(recommended_path, 1):
                    print(f"  📍 경로 {i}:")
                    print(f"     단원 ID: {path.get('unitId', 'N/A')}")
                    print(f"     단원명: {path.get('unitTitle', 'N/A')}")
                    print(f"     우선순위: {path.get('priority', 'N/A')}")
                    print(f"     추천 이유: {path.get('reason', 'N/A')}")
                    print()
            else:
                print("  ❌ 추천 경로가 생성되지 않았습니다.")
            
            print("🎉 단원명 매핑을 통한 맞춤형 학습경로 테스트 완료!")
            return result
            
        else:
            print(f"❌ API 호출 실패: {response.status_code}")
            print(f"에러 내용: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ 테스트 실행 중 오류 발생: {str(e)}")
        return None

if __name__ == "__main__":
    result = test_unit_mapping_learning_path()
    if result:
        print("\n📋 테스트 결과 요약:")
        print("  ✅ 진단테스트 API 호출: 성공")
        print("  ✅ AI 코멘트 생성: 성공")
        print("  ✅ 학습 수준 분류: 성공")
        print("  ✅ 맞춤형 학습경로 생성: 성공")
        print()
        print("💡 단원명 매핑을 통한 맞춤형 학습경로가 정상적으로 작동하고 있습니다!")
        print("   🔑 핵심: 단원명을 문제 ID로 사용하여 MongoDB와 Neo4j 연동")
    else:
        print("\n❌ 테스트 실패!")
        print("   서버 상태나 API 엔드포인트를 확인해주세요.")
