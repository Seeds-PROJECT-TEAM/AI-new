import requests
import json

# Neo4j에 실제로 존재하는 문제 ID들을 사용한 진단테스트 데이터
test_data = {
    "testId": "real_neo4j_test_v2",
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

def test_diagnostic():
    try:
        print("🚀 실제 Neo4j 노드들을 사용한 진단테스트 시작...")
        print(f"📊 테스트 ID: {test_data['testId']}")
        print(f"👤 사용자 ID: {test_data['userId']}")
        print(f"📚 학년 범위: {test_data['gradeRange']}")
        print(f"❌ 오답 개수: {sum(1 for answer in test_data['answers'] if not answer['isCorrect'])}")
        print(f"✅ 정답 개수: {sum(1 for answer in test_data['answers'] if answer['isCorrect'])}")
        print()
        
        # API 호출
        response = requests.post(
            "http://localhost:8000/api/learning-path/express/diagnostic",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("🎉 진단테스트 성공!")
            print("=" * 50)
            print(f"📝 AI 코멘트: {result.get('aiComment', 'N/A')}")
            print(f"🏫 클래스: {result.get('class', 'N/A')}")
            print(f"🛤️ 추천 경로 개수: {len(result.get('recommendedPath', []))}")
            print()
            
            # 추천 경로 상세 정보
            for i, path in enumerate(result.get('recommendedPath', []), 1):
                print(f"📍 경로 {i}:")
                print(f"   단원: {path.get('unitName', 'N/A')}")
                print(f"   우선순위: {path.get('priority', 'N/A')}")
                print(f"   이유: {path.get('reason', 'N/A')}")
                print()
                
            return result
        else:
            print(f"❌ API 호출 실패: {response.status_code}")
            print(f"에러 내용: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")
        return None

if __name__ == "__main__":
    result = test_diagnostic()
    if result:
        print("✅ 테스트 완료! MongoDB에 저장된 데이터를 확인해보세요.")
    else:
        print("❌ 테스트 실패!")
