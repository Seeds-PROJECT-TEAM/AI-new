#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
실제 틀린 문제 데이터로 학습 경로 생성 테스트
Express에서 보내주는 것과 동일한 형식으로 테스트
"""

import requests
import json
from datetime import datetime
from typing import List, Any

# Express에서 보내주는 것과 동일한 답안 데이터 구조
class MockAnswer:
    def __init__(self, problem_id: str, is_correct: bool, time_spent: int):
        self.problemId = problem_id
        self.isCorrect = is_correct
        self.timeSpent = time_spent

def create_mock_test_data():
    """실제 틀린 문제 데이터 생성"""
    
    # Express에서 보내주는 것과 동일한 실제 문제들 (2개)
    # Neo4j에 실제로 존재하는 개념명 사용
    answers = [
        MockAnswer("1.3 정수와 유리수", True, 45),     # 정답 - 정수와 유리수
        MockAnswer("2.1 문자와 식", False, 120),       # 오답 - 문자와 식
    ]
    
    # Express에서 보내주는 것과 동일한 요청 데이터
    test_data = {
        "testId": "68a013e4fe733a1c891816f3",
        "userId": 12345,
        "gradeRange": "중1-중3",
        "answers": [
            {
                "problemId": answer.problemId,
                "userAnswer": {
                    "selectedOption": 2 if answer.isCorrect else None,
                    "value": None if answer.isCorrect else "x = 5"
                },
                "isCorrect": answer.isCorrect,
                "durationSeconds": answer.timeSpent
            }
            for answer in answers
        ],
        "totalProblems": len(answers),
        "durationSec": sum(answer.timeSpent for answer in answers)
    }
    
    return test_data

def test_learning_path_with_real_data():
    """실제 데이터로 학습 경로 생성 테스트"""
    
    print("🔍 실제 틀린 문제 데이터로 학습 경로 생성 테스트 시작")
    print("=" * 60)
    
    # 테스트 데이터 생성
    test_data = create_mock_test_data()
    
    print("📊 테스트 정보:")
    print(f"   testId: {test_data['testId']}")
    print(f"   userId: {test_data['userId']}")
    print(f"   gradeRange: {test_data['gradeRange']}")
    print(f"   totalProblems: {test_data['totalProblems']}")
    print(f"   durationSec: {test_data['durationSec']}")
    
    # 답안 분석
    correct_count = sum(1 for answer in test_data['answers'] if answer['isCorrect'])
    wrong_count = sum(1 for answer in test_data['answers'] if not answer['isCorrect'])
    accuracy_rate = (correct_count / len(test_data['answers'])) * 100
    
    print(f"\n📝 답안 분석:")
    print(f"   정답: {correct_count}개")
    print(f"   오답: {wrong_count}개")
    print(f"   정답률: {accuracy_rate:.1f}%")
    
    print(f"\n❌ 틀린 문제들:")
    for i, answer in enumerate(test_data['answers'], 1):
        if not answer['isCorrect']:
            print(f"   {i}. {answer['problemId']} (소요시간: {answer['durationSeconds']}초)")
    
    print("=" * 60)
    
    # FastAPI 서버로 요청 전송
    print("🚀 FastAPI 서버로 요청 전송 중...")
    
    try:
        response = requests.post(
            "http://localhost:8000/api/learning-path/express/diagnostic",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            print("✅ 요청 성공!")
            result = response.json()
            
            # 결과 분석
            if result.get("success"):
                analysis = result.get("analysis", {})
                learning_path = result.get("learning_path", {})
                
                print(f"\n🎯 진단 분석 결과:")
                print(f"   분석 ID: {analysis.get('analysisId', 'N/A')}")
                print(f"   전체 수준: {analysis.get('overallLevel', 'N/A')}")
                print(f"   취약 단원: {len(analysis.get('weakUnits', []))}개")
                print(f"   취약 개념: {len(analysis.get('weakConcepts', []))}개")
                print(f"   취약 단원 목록: {', '.join(analysis.get('weakUnits', []))}")
                
                print(f"\n📖 추천 시작점: {analysis.get('recommendedStart', 'N/A')}")
                print(f"🤖 AI 코멘트: {analysis.get('aiComment', 'N/A')}")
                
                print(f"\n🛤️ 맞춤형 학습 경로:")
                print(f"   경로 ID: {learning_path.get('pathId', 'N/A')}")
                print(f"   경로명: {learning_path.get('pathName', 'N/A')}")
                print(f"   설명: {learning_path.get('description', 'N/A')}")
                print(f"   총 개념 수: {learning_path.get('totalConcepts', 'N/A')}개")
                print(f"   예상 소요 시간: {learning_path.get('estimatedDuration', 'N/A')}분")
                
                print(f"\n📚 학습 경로 노드들:")
                for i, node in enumerate(learning_path.get('nodes', []), 1):
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
                
                # JSON 결과를 파일로 저장
                output_file = f"learning_path_result_{test_data['testId']}.json"
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(result, f, ensure_ascii=False, indent=2)
                
                print(f"💾 결과가 {output_file} 파일로 저장되었습니다!")
                
            else:
                print(f"❌ 요청 실패: {result.get('message', '알 수 없는 오류')}")
                
        else:
            print(f"❌ HTTP 오류: {response.status_code}")
            print(f"응답 내용: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ FastAPI 서버에 연결할 수 없습니다.")
        print("   서버가 실행 중인지 확인해주세요: python -m uvicorn app.main:app --reload")
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
    
    print("=" * 60)
    print("🎉 테스트 완료!")

if __name__ == "__main__":
    test_learning_path_with_real_data()
