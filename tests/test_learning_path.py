#!/usr/bin/env python3
"""
맞춤형 학습 경로 생성 결과 테스트
"""

import requests
import json

def test_learning_path():
    """맞춤형 학습 경로 생성 테스트"""
    
    # Express 백엔드 요청 형식
    test_request = {
        "testId": "test_68a013e4fe733a1c891816f3",
        "userId": 12345,
        "gradeRange": "중1-중3",
        "answers": [
            {
                "problemId": "problem_001",
                "userAnswer": {
                    "selectedOption": 2,
                    "value": None
                },
                "isCorrect": False,  # 틀린 문제
                "durationSeconds": 45
            },
            {
                "problemId": "problem_002",
                "userAnswer": {
                    "selectedOption": None,
                    "value": "x = 5"
                },
                "isCorrect": False,  # 틀린 문제
                "durationSeconds": 120
            },
            {
                "problemId": "problem_003",
                "userAnswer": {
                    "selectedOption": 1,
                    "value": None
                },
                "isCorrect": True,   # 맞은 문제
                "durationSeconds": 30
            }
        ],
        "totalProblems": 3,
        "durationSec": 195
    }
    
    print("🔍 맞춤형 학습 경로 생성 테스트 시작")
    print("=" * 60)
    print(f"📊 테스트 정보:")
    print(f"   testId: {test_request['testId']}")
    print(f"   userId: {test_request['userId']}")
    print(f"   gradeRange: {test_request['gradeRange']}")
    print(f"   totalProblems: {test_request['totalProblems']}")
    print(f"   durationSec: {test_request['durationSec']}")
    
    print(f"\n📝 답안 분석:")
    correct_count = sum(1 for answer in test_request["answers"] if answer["isCorrect"])
    wrong_count = len(test_request["answers"]) - correct_count
    print(f"   정답: {correct_count}개")
    print(f"   오답: {wrong_count}개")
    print(f"   정답률: {correct_count/len(test_request['answers'])*100:.1f}%")
    
    print(f"\n❌ 틀린 문제들:")
    for i, answer in enumerate(test_request["answers"]):
        if not answer["isCorrect"]:
            print(f"   {i+1}. {answer['problemId']} (소요시간: {answer['durationSeconds']}초)")
    
    print("\n" + "=" * 60)
    
    try:
        # API 요청
        print("🚀 FastAPI 서버로 요청 전송 중...")
        response = requests.post(
            "http://localhost:8000/api/learning-path/express/diagnostic",
            json=test_request,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 요청 성공!")
            
            # 전체 JSON 응답 먼저 출력
            print(f"\n📋 전체 JSON 응답:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            
            # 결과 분석
            print("\n🎯 진단 분석 결과:")
            analysis = result.get("analysis", {})
            if analysis:
                print(f"   분석 ID: {analysis.get('analysisId', 'N/A')}")
                print(f"   전체 수준: {analysis.get('overallLevel', 'N/A')}")
                print(f"   취약 단원: {len(analysis.get('weakUnits', []))}개")
                print(f"   취약 개념: {len(analysis.get('weakConcepts', []))}개")
                
                if analysis.get("weakUnits"):
                    print(f"   취약 단원 목록: {', '.join(analysis['weakUnits'])}")
                
                print(f"\n📖 추천 시작점: {analysis.get('recommendedStart', 'N/A')}")
                print(f"🤖 AI 코멘트: {analysis.get('aiComment', 'N/A')}")
            else:
                print("   분석 결과가 없습니다.")
            
            # 학습 경로 결과
            print("\n🛤️ 맞춤형 학습 경로:")
            learning_path = result.get("learningPath", {})
            print(f"   경로 ID: {learning_path.get('pathId', 'N/A')}")
            print(f"   경로명: {learning_path.get('pathName', 'N/A')}")
            print(f"   설명: {learning_path.get('description', 'N/A')}")
            print(f"   총 개념 수: {learning_path.get('totalConcepts', 'N/A')}개")
            print(f"   예상 소요 시간: {learning_path.get('estimatedDuration', 'N/A')}분")
            
            # 학습 경로 노드들 상세 출력
            print(f"\n📚 학습 경로 노드들:")
            nodes = learning_path.get("nodes", [])
            for i, node in enumerate(nodes, 1):
                print(f"   {i}. {node.get('concept', 'N/A')}")
                print(f"      - 단원: {node.get('unit', 'N/A')}")
                print(f"      - 학년: {node.get('grade', 'N/A')}")
                print(f"      - 우선순위: {node.get('priority', 'N/A')}")
                print(f"      - 취약 개념: {'예' if node.get('isWeakConcept') else '아니오'}")
                print(f"      - 선수과목: {'예' if node.get('isPrerequisite') else '아니오'}")
                if node.get('isPrerequisite'):
                    print(f"        - 선수과목 레벨: {node.get('prerequisiteLevel', 'N/A')}")
                    print(f"        - 선수과목 대상: {node.get('prerequisiteFor', 'N/A')}")
                print()
            
            print("=" * 60)
            print("🎉 테스트 완료!")
            
            # 전체 JSON 응답 출력
            print(f"\n📋 전체 JSON 응답:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            
        else:
            print(f"❌ 요청 실패: {response.status_code}")
            print(f"응답: {response.text}")
            
    except Exception as e:
        print(f"❌ 테스트 중 오류 발생: {e}")

if __name__ == "__main__":
    test_learning_path()
