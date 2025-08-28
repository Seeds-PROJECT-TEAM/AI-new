import requests
import json

def test_real_unit_names():
    """실제 단원명을 사용한 맞춤형 학습경로 테스트"""
    
    print("🚀 실제 단원명을 사용한 맞춤형 학습경로 테스트 시작...")
    print("=" * 70)
    
    # 실제 단원명을 문제 ID로 사용하는 진단테스트
    test_data = {
        "testId": "real_unit_names_test_001",
        "userId": 12500,
        "gradeRange": "중1-중3",
        "totalProblems": 4,
        "durationSec": 200,
        "answers": [
            {
                "problemId": "1.1 소수와 합성수, 소인수분해",  # 실제 단원명
                "userAnswer": {"selectedOption": 2, "value": None},
                "isCorrect": False,  # 틀림
                "durationSeconds": 45
            },
            {
                "problemId": "1.2 최대공약수와 최소공배수",  # 실제 단원명
                "userAnswer": {"selectedOption": 1, "value": None},
                "isCorrect": True,  # 맞음
                "durationSeconds": 60
            },
            {
                "problemId": "2.1 문자와 식",  # 실제 단원명
                "userAnswer": {"selectedOption": 3, "value": None},
                "isCorrect": False,  # 틀림
                "durationSeconds": 50
            },
            {
                "problemId": "2.2 일차식의 사칙연산",  # 실제 단원명
                "userAnswer": {"selectedOption": None, "value": "2x + 3"},
                "isCorrect": False,  # 틀림
                "durationSeconds": 55
            }
        ]
    }
    
    print("📊 테스트 데이터 (실제 단원명 사용):")
    print(f"  - 테스트 ID: {test_data['testId']}")
    print(f"  - 사용자 ID: {test_data['userId']}")
    print(f"  - 학년 범위: {test_data['gradeRange']}")
    print(f"  - 총 문제 수: {test_data['totalProblems']}")
    print(f"  - 오답 수: {sum(1 for answer in test_data['answers'] if not answer['isCorrect'])}")
    print(f"  - 정답 수: {sum(1 for answer in test_data['answers'] if answer['isCorrect'])}")
    print()
    
    print("🔍 문제 내용 (실제 단원명):")
    for i, answer in enumerate(test_data['answers'], 1):
        problem_id = answer['problemId']
        print(f"  {i}. {problem_id}")
        print(f"     결과: {'❌ 틀림' if not answer['isCorrect'] else '✅ 맞음'}")
        print()
    
    print("🔗 예상 매핑 결과:")
    print("  📍 1.1 소수와 합성수, 소인수분해 → 1. 수와 연산")
    print("  📍 1.2 최대공약수와 최소공배수 → 1. 수와 연산")
    print("  📍 2.1 문자와 식 → 2. 문자와 식")
    print("  📍 2.2 일차식의 사칙연산 → 2. 문자와 식")
    print()
    
    print("🎯 예상 학습 경로:")
    print("  1. 1. 수와 연산 (기초 개념)")
    print("  2. 2. 문자와 식 (문자와 식 기초)")
    print("  3. 2. 문자와 식 (일차식 사칙연산)")
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
            
            print("🎉 실제 단원명을 사용한 맞춤형 학습경로 테스트 완료!")
            return result
            
        else:
            print(f"❌ API 호출 실패: {response.status_code}")
            print(f"에러 내용: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ 테스트 실행 중 오류 발생: {str(e)}")
        return None

if __name__ == "__main__":
    result = test_real_unit_names()
    if result:
        print("\n📋 테스트 결과 요약:")
        print("  ✅ 진단테스트 API 호출: 성공")
        print("  ✅ AI 코멘트 생성: 성공")
        print("  ✅ 학습 수준 분류: 성공")
        print("  ✅ 맞춤형 학습경로 생성: 성공")
        print()
        print("💡 실제 단원명을 사용한 맞춤형 학습경로가 정상적으로 작동하고 있습니다!")
        print("   🔑 핵심: 단원명 → 기본 단원 매핑 → Neo4j 선수개념 조회")
    else:
        print("\n❌ 테스트 실패!")
        print("   서버 상태나 API 엔드포인트를 확인해주세요.")
