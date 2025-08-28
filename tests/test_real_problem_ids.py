#!/usr/bin/env python3
"""실제 MongoDB problemId를 사용한 3.x 관련 진단 요청 테스트"""

import requests
import json
import time

def test_real_problem_ids():
    try:
        print("=== 실제 MongoDB problemId를 사용한 3.x 관련 진단 요청 테스트 ===")
        
        # 1. 헬스체크
        print("\n🔍 1단계: 서버 헬스체크")
        try:
            response = requests.get("http://localhost:8000/health")
            if response.status_code == 200:
                print(f"   ✅ 서버 정상: {response.json()}")
            else:
                print(f"   ❌ 서버 오류: {response.status_code}")
                return
        except Exception as e:
            print(f"   ❌ 서버 연결 실패: {e}")
            return
        
        # 2. 실제 MongoDB에 존재하는 problemId 사용
        print("\n🔍 2단계: 실제 problemId를 사용한 진단 요청")
        
        # MongoDB에 실제로 존재하는 problemId들 사용
        diagnostic_request_real = {
            "testId": "express_test_real_001",
            "userId": 12345,
            "gradeRange": "중1-중3",
            "answers": [
                {
                    "problemId": "problem_001",  # MongoDB에 존재하는 실제 ID
                    "userAnswer": {"selectedOption": "B", "value": "B"},
                    "isCorrect": False,
                    "durationSeconds": 45
                },
                {
                    "problemId": "problem_002",  # MongoDB에 존재하는 실제 ID
                    "userAnswer": {"selectedOption": "A", "value": "A"},
                    "isCorrect": True,
                    "durationSeconds": 30
                },
                {
                    "problemId": "DIAG_001",    # 진단테스트 문제 ID
                    "userAnswer": {"selectedOption": "C", "value": "C"},
                    "isCorrect": False,
                    "durationSeconds": 60
                }
            ],
            "totalProblems": 3,
            "durationSec": 135
        }
        
        print("   📝 실제 problemId를 사용한 진단 요청:")
        print(f"      문제 수: {diagnostic_request_real['totalProblems']}")
        print(f"      정답률: {sum(1 for a in diagnostic_request_real['answers'] if a['isCorrect'])}/{len(diagnostic_request_real['answers'])}")
        print(f"      사용된 problemId들:")
        for answer in diagnostic_request_real['answers']:
            print(f"        - {answer['problemId']} (정답: {answer['isCorrect']})")
        
        try:
            response = requests.post(
                "http://localhost:8000/api/learning-path/express/diagnostic",
                json=diagnostic_request_real,
                headers={"Content-Type": "application/json", "x-service-token": "test_service_token"}
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"\n   ✅ 응답 성공!")
                print(f"      학습 경로 ID: {result.get('pathId', 'N/A')}")
                print(f"      경로 이름: {result.get('pathName', 'N/A')}")
                print(f"      노드 수: {len(result.get('learningPath', {}).get('nodes', []))}")
                print(f"      추정 시간: {result.get('estimatedDuration', 'N/A')}분")
                
                # 학습 경로 노드 상세 정보
                nodes = result.get('learningPath', {}).get('nodes', [])
                if nodes:
                    print(f"\n   📚 학습 경로 노드들:")
                    for i, node in enumerate(nodes):
                        concept = node.get('concept', 'N/A')
                        priority = node.get('priority', 'N/A')
                        is_prereq = node.get('isPrerequisite', False)
                        prereq_level = node.get('prerequisiteLevel', 'N/A')
                        print(f"      {i+1}. {concept}")
                        print(f"         우선순위: {priority}, 선수개념: {is_prereq}")
                        if is_prereq:
                            print(f"         선수개념 레벨: {prereq_level}")
                else:
                    print(f"\n   ⚠️ 학습 경로 노드가 없음")
                    print(f"      가능한 원인:")
                    print(f"      1. MongoDB에서 problemId를 찾을 수 없음")
                    print(f"      2. concepts 컬렉션에서 unitCode를 찾을 수 없음")
                    print(f"      3. Neo4j에서 선수개념을 찾을 수 없음")
                
            else:
                print(f"   ❌ 응답 실패: {response.status_code}")
                print(f"      오류 내용: {response.text}")
                
        except Exception as e:
            print(f"   ❌ 요청 실패: {e}")
        
        print(f"\n🎯 테스트 완료!")
        print("   Express에서 실제 problemId로 진단 요청을 보내면:")
        print("   1. MongoDB에서 problemId → unitId → concepts 조회")
        print("   2. concepts에서 unitCode와 unitTitle 추출")
        print("   3. Neo4j에서 해당 개념의 선수개념 조회")
        print("   4. 선수개념 + 현재 개념으로 맞춤형 학습 경로 생성")
        print("   5. 순서대로 정렬하여 응답")
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_real_problem_ids()
