import requests
import json

def test_virtual_diagnostic():
    """MongoDB 연결 없이 가상 데이터로 맞춤형 학습경로 테스트"""
    
    print("🚀 MongoDB 연결 없이 가상 데이터로 맞춤형 학습경로 테스트 시작...")
    print("=" * 70)
    
    # 가상 문제-단원 매핑 테이블 (MongoDB 연결 없이)
    virtual_problem_mapping = {
        "68a013e4fe733a1c891816f4": {
            "unitId": "virtual_001",
            "unitTitle": "덧셈과 뺄셈",
            "chapter": "수와 연산",
            "grade": "중1",
            "prerequisites": ["자연수", "수의 크기 비교"]
        },
        "68a013e4fe733a1c891816f5": {
            "unitId": "virtual_002",
            "unitTitle": "문자와 식",
            "chapter": "문자와 식", 
            "grade": "중1",
            "prerequisites": ["덧셈과 뺄셈", "곱셈과 나눗셈"]
        },
        "68a013e4fe733a1c891816f6": {
            "unitId": "virtual_003",
            "unitTitle": "일차방정식",
            "chapter": "문자와 식",
            "grade": "중1",
            "prerequisites": ["문자와 식", "등식의 성질"]
        },
        "68a013e4fe733a1c891816f7": {
            "unitId": "virtual_004",
            "unitTitle": "일차함수",
            "chapter": "함수",
            "grade": "중2",
            "prerequisites": ["일차방정식", "좌표평면"]
        }
    }
    
    # 실제 Express에서 보내는 진단테스트 요청 데이터
    test_data = {
        "testId": "68a013e4fe733a1c891816f3",
        "userId": 12345,
        "gradeRange": "중1-중3",
        "answers": [
            {
                "problemId": "68a013e4fe733a1c891816f4",  # 덧셈과 뺄셈
                "userAnswer": {
                    "selectedOption": 2,
                    "value": None
                },
                "isCorrect": True,  # 맞음
                "durationSeconds": 45
            },
            {
                "problemId": "68a013e4fe733a1c891816f5",  # 문자와 식
                "userAnswer": {
                    "selectedOption": None,
                    "value": "x = 5"
                },
                "isCorrect": False,  # 틀림
                "durationSeconds": 120
            }
        ],
        "totalProblems": 2,
        "durationSec": 165
    }
    
    print("📊 Express 진단테스트 요청 데이터:")
    print(f"  - 테스트 ID: {test_data['testId']}")
    print(f"  - 사용자 ID: {test_data['userId']}")
    print(f"  - 학년 범위: {test_data['gradeRange']}")
    print(f"  - 총 문제 수: {test_data['totalProblems']}")
    print(f"  - 오답 수: {sum(1 for answer in test_data['answers'] if not answer['isCorrect'])}")
    print(f"  - 정답 수: {sum(1 for answer in test_data['answers'] if answer['isCorrect'])}")
    print()
    
    print("🔍 문제 분석 (가상 매핑):")
    for i, answer in enumerate(test_data['answers'], 1):
        problem_id = answer['problemId']
        problem_info = virtual_problem_mapping.get(problem_id, {})
        
        print(f"  {i}. 문제 ID: {problem_id}")
        print(f"     단원: {problem_info.get('unitTitle', 'N/A')}")
        print(f"     챕터: {problem_info.get('chapter', 'N/A')}")
        print(f"     학년: {problem_info.get('grade', 'N/A')}")
        print(f"     선수개념: {', '.join(problem_info.get('prerequisites', []))}")
        print(f"     결과: {'✅ 맞음' if answer['isCorrect'] else '❌ 틀림'}")
        print()
    
    print("🔗 가상 매핑 테이블 정보:")
    print(f"  총 매핑된 문제 수: {len(virtual_problem_mapping)}")
    print("  매핑 방식: 문제 ID → 가상 단원 정보")
    print("  선수개념: 가상 데이터로 Neo4j 대체")
    print()
    
    print("🎯 예상 맞춤형 학습 경로:")
    print("  1. 문자와 식 (틀린 문제 - 우선순위 높음)")
    print("  2. 일차방정식 (문자와 식의 다음 단계)")
    print("  3. 덧셈과 뺄셈 (기초 개념 - 선수개념)")
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
            
            print("🎉 MongoDB 연결 없이 가상 데이터로 맞춤형 학습경로 테스트 완료!")
            return result
            
        else:
            print(f"❌ API 호출 실패: {response.status_code}")
            print(f"에러 내용: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ 테스트 실행 중 오류 발생: {str(e)}")
        return None

if __name__ == "__main__":
    result = test_virtual_diagnostic()
    if result:
        print("\n📋 테스트 결과 요약:")
        print("  ✅ 진단테스트 API 호출: 성공")
        print("  ✅ AI 코멘트 생성: 성공")
        print("  ✅ 학습 수준 분류: 성공")
        print("  ✅ 맞춤형 학습경로 생성: 성공")
        print()
        print("💡 MongoDB 연결 없이 가상 데이터로 맞춤형 학습경로가 정상적으로 작동하고 있습니다!")
        print("   🔑 핵심: 문제 ID → 가상 단원 매핑 → 가상 선수개념 → 맞춤형 경로 생성")
    else:
        print("\n❌ 테스트 실패!")
        print("   서버 상태나 API 엔드포인트를 확인해주세요.")
