#!/usr/bin/env python3
"""Express에서 3.x 관련 진단 요청 시뮬레이션"""

import requests
import json
import time

def test_express_3x_request():
    try:
        print("=== Express에서 3.x 관련 진단 요청 시뮬레이션 ===")
        
        # 서버 시작 대기
        print("🔌 서버 시작 대기 중...")
        time.sleep(3)
        
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
        
        # 2. 3.x 관련 진단 요청 시뮬레이션
        print("\n🔍 2단계: 3.x 관련 진단 요청 시뮬레이션")
        
        # 3.1 순서쌍과 좌표 관련 진단 요청
        diagnostic_request_3_1 = {
            "testId": "express_test_3x_001",
            "userId": 12345,
            "gradeRange": "중1-중3",
            "answers": [
                {
                    "problemId": "problem_3x_001",
                    "userAnswer": {"selectedOption": "B", "value": "B"},
                    "isCorrect": False,
                    "durationSeconds": 45
                },
                {
                    "problemId": "problem_3x_002", 
                    "userAnswer": {"selectedOption": "A", "value": "A"},
                    "isCorrect": True,
                    "durationSeconds": 30
                }
            ],
            "totalProblems": 2,
            "durationSec": 75
        }
        
        print("   📝 3.1 순서쌍과 좌표 관련 진단 요청:")
        print(f"      문제 수: {diagnostic_request_3_1['totalProblems']}")
        print(f"      정답률: {sum(1 for a in diagnostic_request_3_1['answers'] if a['isCorrect'])}/{len(diagnostic_request_3_1['answers'])}")
        
        try:
            response = requests.post(
                "http://localhost:8000/api/learning-path/express/diagnostic",
                json=diagnostic_request_3_1,
                headers={"Content-Type": "application/json", "x-service-token": "test_service_token"}
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ 응답 성공!")
                print(f"      학습 경로 ID: {result.get('pathId', 'N/A')}")
                print(f"      경로 이름: {result.get('pathName', 'N/A')}")
                print(f"      노드 수: {len(result.get('learningPath', {}).get('nodes', []))}")
                print(f"      추정 시간: {result.get('estimatedDuration', 'N/A')}분")
                
                # 학습 경로 노드 상세 정보
                nodes = result.get('learningPath', {}).get('nodes', [])
                if nodes:
                    print(f"\n   📚 학습 경로 노드들:")
                    for i, node in enumerate(nodes):
                        print(f"      {i+1}. {node.get('concept', 'N/A')} (우선순위: {node.get('priority', 'N/A')}, 선수개념: {node.get('isPrerequisite', False)})")
                
            else:
                print(f"   ❌ 응답 실패: {response.status_code}")
                print(f"      오류 내용: {response.text}")
                
        except Exception as e:
            print(f"   ❌ 요청 실패: {e}")
        
        # 3. 3.2 정비례 관련 진단 요청
        print(f"\n🔍 3단계: 3.2 정비례 관련 진단 요청 시뮬레이션")
        
        diagnostic_request_3_2 = {
            "testId": "express_test_3x_002",
            "userId": 12346,
            "gradeRange": "중1-중3",
            "answers": [
                {
                    "problemId": "problem_3x_003",
                    "userAnswer": {"selectedOption": "C", "value": "C"},
                    "isCorrect": False,
                    "durationSeconds": 60
                },
                {
                    "problemId": "problem_3x_004",
                    "userAnswer": {"selectedOption": "D", "value": "D"}, 
                    "isCorrect": False,
                    "durationSeconds": 55
                }
            ],
            "totalProblems": 2,
            "durationSec": 115
        }
        
        print("   📝 3.2 정비례 관련 진단 요청:")
        print(f"      문제 수: {diagnostic_request_3_2['totalProblems']}")
        print(f"      정답률: {sum(1 for a in diagnostic_request_3_2['answers'] if a['isCorrect'])}/{len(diagnostic_request_3_2['answers'])}")
        
        try:
            response = requests.post(
                "http://localhost:8000/api/learning-path/express/diagnostic",
                json=diagnostic_request_3_2,
                headers={"Content-Type": "application/json", "x-service-token": "test_service_token"}
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ 응답 성공!")
                print(f"      학습 경로 ID: {result.get('pathId', 'N/A')}")
                print(f"      경로 이름: {result.get('pathName', 'N/A')}")
                print(f"      노드 수: {len(result.get('learningPath', {}).get('nodes', []))}")
                print(f"      추정 시간: {result.get('estimatedDuration', 'N/A')}분")
                
                # 학습 경로 노드 상세 정보
                nodes = result.get('learningPath', {}).get('nodes', [])
                if nodes:
                    print(f"\n   📚 학습 경로 노드들:")
                    for i, node in enumerate(nodes):
                        print(f"      {i+1}. {node.get('concept', 'N/A')} (우선순위: {node.get('priority', 'N/A')}, 선수개념: {node.get('isPrerequisite', False)})")
                
            else:
                print(f"   ❌ 응답 실패: {response.status_code}")
                print(f"      오류 내용: {response.text}")
                
        except Exception as e:
            print(f"   ❌ 요청 실패: {e}")
        
        print(f"\n🎯 테스트 완료!")
        print("   Express에서 3.x 관련 진단 요청을 보내면:")
        print("   1. MongoDB에서 problemId → unitId → concepts 조회")
        print("   2. Neo4j에서 해당 개념의 선수개념 조회")
        print("   3. 선수개념 + 현재 개념으로 맞춤형 학습 경로 생성")
        print("   4. 순서대로 정렬하여 응답")
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_express_3x_request()
