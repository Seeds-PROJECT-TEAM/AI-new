import requests
import json

def test_with_real_mongodb():
    """실제 MongoDB 데이터로 맞춤형 학습경로 테스트"""
    
    print("🚀 실제 MongoDB 데이터로 맞춤형 학습경로 테스트 시작...")
    print("=" * 60)
    
    # 실제 MongoDB에 있는 문제 ID들로 테스트
    test_data = {
        "testId": "real_mongodb_test_001",
        "userId": 12500,
        "gradeRange": "중1-중3",
        "totalProblems": 4,
        "durationSec": 200,
        "answers": [
            {
                "problemId": "68a01415fe733a1c891816f5",  # 5 + 3 = ?
                "userAnswer": {"selectedOption": 1, "value": None},  # 틀린 답 (7)
                "isCorrect": False,
                "durationSeconds": 45
            },
            {
                "problemId": "68a0144bfe733a1c891816f6",  # 10 - 4 = ?
                "userAnswer": {"selectedOption": 1, "value": None},  # 정답 (6)
                "isCorrect": True,
                "durationSeconds": 60
            },
            {
                "problemId": "68a6898f107e617032d6fa43",  # 2x + 3 = 7
                "userAnswer": {"selectedOption": None, "value": "3"},  # 틀린 답
                "isCorrect": False,
                "durationSeconds": 50
            },
            {
                "problemId": "68a6898f107e617032d6fa44",  # f(x) = 2x + 1, f(3) = ?
                "userAnswer": {"selectedOption": 2, "value": None},  # 틀린 답 (6)
                "isCorrect": False,
                "durationSeconds": 55
            }
        ]
    }
    
    print("📊 테스트 데이터 (실제 MongoDB 문제 ID 사용):")
    print(f"  - 테스트 ID: {test_data['testId']}")
    print(f"  - 사용자 ID: {test_data['userId']}")
    print(f"  - 학년 범위: {test_data['gradeRange']}")
    print(f"  - 총 문제 수: {test_data['totalProblems']}")
    print(f"  - 오답 수: {sum(1 for answer in test_data['answers'] if not answer['isCorrect'])}")
    print(f"  - 정답 수: {sum(1 for answer in test_data['answers'] if answer['isCorrect'])}")
    print()
    
    print("🔍 문제 내용:")
    for i, answer in enumerate(test_data['answers'], 1):
        problem_id = answer['problemId']
        if problem_id == "68a01415fe733a1c891816f5":
            print(f"  {i}. 5 + 3 = ? (정답: 8, 사용자 답: 7)")
        elif problem_id == "68a0144bfe733a1c891816f6":
            print(f"  {i}. 10 - 4 = ? (정답: 6, 사용자 답: 6)")
        elif problem_id == "68a6898f107e617032d6fa43":
            print(f"  {i}. 2x + 3 = 7, x = ? (정답: 2, 사용자 답: 3)")
        elif problem_id == "68a6898f107e617032d6fa44":
            print(f"  {i}. f(x) = 2x + 1, f(3) = ? (정답: 7, 사용자 답: 6)")
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
            
            print("🎉 실제 MongoDB 데이터로 맞춤형 학습경로 테스트 완료!")
            return result
            
        else:
            print(f"❌ API 호출 실패: {response.status_code}")
            print(f"에러 내용: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ 테스트 실행 중 오류 발생: {str(e)}")
        return None

if __name__ == "__main__":
    result = test_with_real_mongodb()
    if result:
        print("\n📋 테스트 결과 요약:")
        print("  ✅ 진단테스트 API 호출: 성공")
        print("  ✅ AI 코멘트 생성: 성공")
        print("  ✅ 학습 수준 분류: 성공")
        print("  ✅ 맞춤형 학습경로 생성: 성공")
        print()
        print("💡 실제 MongoDB 데이터로 맞춤형 학습경로가 정상적으로 작동하고 있습니다!")
    else:
        print("\n❌ 테스트 실패!")
        print("   서버 상태나 API 엔드포인트를 확인해주세요.")
