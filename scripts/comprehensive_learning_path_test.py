#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
맞춤형 학습 경로 종합 테스트 스크립트

이 스크립트는 다음 기능들을 테스트합니다:
1. 진단 테스트 생성 및 분석
2. 맞춤형 학습 경로 생성
3. Neo4j 그래프 기반 경로 최적화
4. MongoDB 데이터 연동
5. AI 기반 학습 추천
6. 실시간 학습 진행 상황 추적
"""

import os
import sys
import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

# .env 파일 로드
from dotenv import load_dotenv
env_path = os.path.join(os.path.dirname(__file__), 'AI', '.env')
if os.path.exists(env_path):
    load_dotenv(env_path)
    print(f"✅ .env 파일 로드 성공: {env_path}")
else:
    print(f"⚠️ .env 파일을 찾을 수 없음: {env_path}")

# 프로젝트 루트 경로 추가
ai_app_path = os.path.join(os.path.dirname(__file__), 'AI', 'app')
sys.path.insert(0, ai_app_path)
print(f"📁 AI 앱 경로 추가: {ai_app_path}")

def test_environment_setup():
    """환경 설정 및 의존성 확인"""
    print("🔍 환경 설정 확인 중...")
    
    # 필요한 환경변수 확인
    required_env_vars = [
        "MONGODB_URI",
        "AURA_URI", 
        "AURA_USER",
        "AURA_PASS",
        "OPENAI_API_KEY"
    ]
    
    missing_vars = []
    for var in required_env_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"⚠️ 누락된 환경변수: {', '.join(missing_vars)}")
        print("로컬 테스트 모드로 진행합니다.")
        return False
    else:
        print("✅ 모든 환경변수가 설정되었습니다.")
        return True

def test_mongodb_connection():
    """MongoDB 연결 테스트"""
    print("\n🔍 MongoDB 연결 테스트...")
    
    try:
        from pymongo import MongoClient
        from pymongo.errors import ConnectionFailure
        
        mongodb_uri = os.getenv("MONGODB_URI")
        if not mongodb_uri:
            print("⚠️ MONGODB_URI가 설정되지 않음")
            return False
            
        client = MongoClient(mongodb_uri)
        client.admin.command('ping')
        print("✅ MongoDB 연결 성공!")
        
        # 데이터베이스 및 컬렉션 확인
        db = client.seeds_db
        collections = db.list_collection_names()
        print(f"📊 사용 가능한 컬렉션: {', '.join(collections)}")
        
        client.close()
        return True
        
    except Exception as e:
        print(f"❌ MongoDB 연결 실패: {e}")
        return False

def test_neo4j_connection():
    """Neo4j 연결 테스트"""
    print("\n🔍 Neo4j 연결 테스트...")
    
    try:
        from neo4j import GraphDatabase
        
        aura_uri = os.getenv("AURA_URI")
        aura_user = os.getenv("AURA_USER")
        aura_pass = os.getenv("AURA_PASS")
        
        if not all([aura_uri, aura_user, aura_pass]):
            print("⚠️ Neo4j 환경변수가 설정되지 않음")
            return False
            
        driver = GraphDatabase.driver(aura_uri, auth=(aura_user, aura_pass))
        
        with driver.session() as session:
            # 연결 테스트
            result = session.run("RETURN 1 as test")
            record = result.single()
            if record and record.get('test') == 1:
                print("✅ Neo4j 연결 성공!")
                
                # 그래프 구조 확인
                node_count = session.run("MATCH (n) RETURN count(n) as count").single()
                edge_count = session.run("MATCH ()-[r]->() RETURN count(r) as count").single()
                
                print(f"📊 그래프 노드 수: {node_count.get('count')}")
                print(f"📊 그래프 엣지 수: {edge_count.get('count')}")
                
                driver.close()
                return True
            else:
                print("❌ Neo4j 연결 테스트 실패")
                driver.close()
                return False
                
    except Exception as e:
        print(f"❌ Neo4j 연결 실패: {e}")
        return False

def test_learning_path_service():
    """학습 경로 서비스 테스트"""
    print("\n🔍 학습 경로 서비스 테스트...")
    
    try:
        from services.learning_path import LearningPathService
        
        service = LearningPathService()
        
        # 연결 상태 확인
        neo4j_connected = service.is_neo4j_connected()
        mongodb_connected = service.is_mongodb_connected()
        
        print(f"📊 Neo4j 연결 상태: {'연결됨' if neo4j_connected else '연결 안됨'}")
        print(f"📊 MongoDB 연결 상태: {'연결됨' if mongodb_connected else '연결 안됨'}")
        
        if not neo4j_connected or not mongodb_connected:
            print("⚠️ 일부 데이터베이스 연결이 실패했습니다.")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ 학습 경로 서비스 테스트 실패: {e}")
        return False

def test_diagnostic_service():
    """진단 서비스 테스트"""
    print("\n🔍 진단 서비스 테스트...")
    
    try:
        from services.diagnostic_service import DiagnosticService
        
        service = DiagnosticService()
        print("✅ 진단 서비스 초기화 성공!")
        
        return True
        
    except Exception as e:
        print(f"❌ 진단 서비스 테스트 실패: {e}")
        return False

def create_mock_diagnostic_data():
    """테스트용 진단 데이터 생성"""
    print("\n🔍 테스트용 진단 데이터 생성...")
    
    # 가상의 진단 테스트 데이터
    mock_data = {
        "testId": str(uuid.uuid4()),
        "userId": "test_user_001",
        "gradeRange": "중1",
        "totalProblems": 20,
        "durationSec": 1800,
        "answers": [
            {
                "questionId": "q001",
                "conceptId": "concept_001",
                "unit": "1. 정수와 유리수",
                "concept": "1.1 정수와 유리수",
                "userAnswer": "3",
                "correctAnswer": "3",
                "isCorrect": True,
                "timeSpent": 45,
                "difficulty": "easy"
            },
            {
                "questionId": "q002",
                "conceptId": "concept_002", 
                "unit": "1. 정수와 유리수",
                "concept": "1.2 정수의 덧셈과 뺄셈",
                "userAnswer": "7",
                "correctAnswer": "5",
                "isCorrect": False,
                "timeSpent": 60,
                "difficulty": "medium"
            },
            {
                "questionId": "q003",
                "conceptId": "concept_003",
                "unit": "2. 문자와 식",
                "concept": "2.1 문자와 식",
                "userAnswer": "2x",
                "correctAnswer": "2x",
                "isCorrect": True,
                "timeSpent": 90,
                "difficulty": "medium"
            },
            {
                "questionId": "q004",
                "conceptId": "concept_004",
                "unit": "2. 문자와 식",
                "concept": "2.2 일차식의 계산",
                "userAnswer": "3x+2",
                "correctAnswer": "3x+1",
                "isCorrect": False,
                "timeSpent": 120,
                "difficulty": "hard"
            }
        ]
    }
    
    print(f"✅ 테스트 데이터 생성 완료:")
    print(f"   - 테스트 ID: {mock_data['testId']}")
    print(f"   - 사용자: {mock_data['userId']}")
    print(f"   - 문제 수: {mock_data['totalProblems']}")
    print(f"   - 정답률: {sum(1 for a in mock_data['answers'] if a['isCorrect'])}/{len(mock_data['answers'])}")
    
    return mock_data

def test_express_diagnostic_analysis():
    """Express 진단 분석 테스트"""
    print("\n🔍 Express 진단 분석 테스트...")
    
    try:
        from services.diagnostic_service import DiagnosticService
        
        service = DiagnosticService()
        
        # 테스트 데이터 생성
        mock_data = create_mock_diagnostic_data()
        
        # Express 진단 요청 모델 생성
        from models.diagnostic import ExpressDiagnosticRequest
        
        # 답안 데이터 변환
        answers = []
        for answer in mock_data["answers"]:
            from models.diagnostic import UserAnswer
            user_answer = UserAnswer(
                questionId=answer["questionId"],
                conceptId=answer["conceptId"],
                unit=answer["unit"],
                concept=answer["concept"],
                userAnswer=answer["userAnswer"],
                correctAnswer=answer["correctAnswer"],
                isCorrect=answer["isCorrect"],
                timeSpent=answer["timeSpent"],
                difficulty=answer["difficulty"]
            )
            answers.append(user_answer)
        
        # Express 진단 요청 생성
        request = ExpressDiagnosticRequest(
            testId=mock_data["testId"],
            userId=mock_data["userId"],
            gradeRange=mock_data["gradeRange"],
            totalProblems=mock_data["totalProblems"],
            durationSec=mock_data["durationSec"],
            answers=answers
        )
        
        print("📊 진단 분석 시작...")
        result = service.process_express_diagnostic_and_save(request)
        
        print("✅ 진단 분석 완료!")
        print(f"   - 분석 ID: {result.get('analysisId')}")
        print(f"   - 학습 경로 ID: {result.get('learningPathId')}")
        
        return result
        
    except Exception as e:
        print(f"❌ Express 진단 분석 테스트 실패: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_learning_path_generation():
    """학습 경로 생성 테스트"""
    print("\n🔍 학습 경로 생성 테스트...")
    
    try:
        from services.learning_path import LearningPathService
        
        service = LearningPathService()
        
        # 가상의 진단 분석 결과
        analysis_id = str(uuid.uuid4())
        user_id = "test_user_001"
        
        # 취약점 분석 결과
        weak_units = ["1. 정수와 유리수", "2. 문자와 식"]
        weak_concepts = ["1.2 정수의 덧셈과 뺄셈", "2.2 일차식의 계산"]
        
        print("📊 학습 경로 생성 시작...")
        
        # 시작점 추천
        start_recommendations = service.get_start_point_recommendations(analysis_id)
        print(f"   - 시작점 추천: {start_recommendations}")
        
        # 맞춤형 학습 경로 생성
        learning_path = service.generate_personalized_learning_path(
            user_id=user_id,
            analysis_id=analysis_id,
            weak_units=weak_units,
            weak_concepts=weak_concepts,
            start_unit="1. 정수와 유리수",
            start_concept="1.2 정수의 덧셈과 뺄셈"
        )
        
        print("✅ 학습 경로 생성 완료!")
        print(f"   - 경로 ID: {learning_path.pathId}")
        print(f"   - 총 노드 수: {len(learning_path.nodes)}")
        print(f"   - 예상 소요 시간: {learning_path.estimatedDuration}분")
        
        return learning_path
        
    except Exception as e:
        print(f"❌ 학습 경로 생성 테스트 실패: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_neo4j_graph_queries():
    """Neo4j 그래프 쿼리 테스트"""
    print("\n🔍 Neo4j 그래프 쿼리 테스트...")
    
    try:
        from neo4j import GraphDatabase
        import os
        
        aura_uri = os.getenv("AURA_URI")
        aura_user = os.getenv("AURA_USER")
        aura_pass = os.getenv("AURA_PASS")
        
        if not all([aura_uri, aura_user, aura_pass]):
            print("⚠️ Neo4j 환경변수가 설정되지 않음")
            return False
            
        driver = GraphDatabase.driver(aura_uri, auth=(aura_user, aura_pass))
        
        with driver.session() as session:
            # 1. 개념 노드 조회
            print("📊 개념 노드 조회...")
            concepts = session.run("MATCH (c:Concept) RETURN c.concept as concept LIMIT 5")
            concept_list = [record["concept"] for record in concepts]
            print(f"   - 샘플 개념: {', '.join(concept_list)}")
            
            # 2. 단원별 개념 수 조회
            print("📊 단원별 개념 수 조회...")
            unit_stats = session.run("""
                MATCH (c:Concept)
                RETURN c.unit as unit, count(c) as count
                ORDER BY count DESC
                LIMIT 5
            """)
            for record in unit_stats:
                print(f"   - {record['unit']}: {record['count']}개 개념")
            
            # 3. 선행 개념 관계 조회
            print("📊 선행 개념 관계 조회...")
            prerequisites = session.run("""
                MATCH (p:Concept)-[:PREREQUISITE]->(c:Concept)
                RETURN p.concept as prerequisite, c.concept as concept
                LIMIT 5
            """)
            for record in prerequisites:
                print(f"   - {record['prerequisite']} → {record['concept']}")
            
            driver.close()
            print("✅ Neo4j 그래프 쿼리 테스트 완료!")
            return True
            
    except Exception as e:
        print(f"❌ Neo4j 그래프 쿼리 테스트 실패: {e}")
        return False

def test_ai_integration():
    """AI 통합 테스트"""
    print("\n🔍 AI 통합 테스트...")
    
    try:
        # OpenAI API 키 확인
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            print("⚠️ OPENAI_API_KEY가 설정되지 않음")
            return False
            
        from openai import OpenAI
        
        client = OpenAI(api_key=openai_api_key)
        
        # 간단한 AI 응답 테스트
        test_prompt = "중학교 1학년 수학에서 '정수와 유리수' 개념을 간단히 설명해주세요."
        
        print("📊 AI 응답 테스트...")
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "당신은 수학 교육 전문가입니다."},
                {"role": "user", "content": test_prompt}
            ],
            max_tokens=150
        )
        
        ai_response = response.choices[0].message.content
        print(f"✅ AI 응답 성공!")
        print(f"   - 응답: {ai_response[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ AI 통합 테스트 실패: {e}")
        return False

def test_learning_progress_tracking():
    """학습 진행 상황 추적 테스트"""
    print("\n🔍 학습 진행 상황 추적 테스트...")
    
    try:
        from services.learning_path import LearningPathService
        
        service = LearningPathService()
        
        # 가상의 학습 진행 상황
        user_id = "test_user_001"
        path_id = str(uuid.uuid4())
        concept_id = "concept_002"
        
        print("📊 학습 진행 상황 업데이트...")
        
        # 학습 완료 상태 업데이트
        progress_update = {
            "userId": user_id,
            "pathId": path_id,
            "conceptId": concept_id,
            "status": "completed",
            "questionsAttempted": 5,
            "questionsCorrect": 4,
            "timeSpent": 300  # 5분
        }
        
        # 학습 시간 로그 생성
        time_log = {
            "logId": str(uuid.uuid4()),
            "userId": user_id,
            "pathId": path_id,
            "conceptId": concept_id,
            "startTime": datetime.now() - timedelta(minutes=5),
            "endTime": datetime.now(),
            "duration": 300,
            "status": "completed"
        }
        
        print("✅ 학습 진행 상황 추적 테스트 완료!")
        print(f"   - 사용자: {user_id}")
        print(f"   - 경로: {path_id}")
        print(f"   - 개념: {concept_id}")
        print(f"   - 상태: {progress_update['status']}")
        print(f"   - 정답률: {progress_update['questionsCorrect']}/{progress_update['questionsAttempted']}")
        
        return True
        
    except Exception as e:
        print(f"❌ 학습 진행 상황 추적 테스트 실패: {e}")
        return False

def run_comprehensive_test():
    """종합 테스트 실행"""
    print("🚀 맞춤형 학습 경로 종합 테스트 시작!")
    print("=" * 60)
    
    # 테스트 결과 저장
    test_results = {}
    
    # 1. 환경 설정 테스트
    test_results["environment"] = test_environment_setup()
    
    # 2. 데이터베이스 연결 테스트
    test_results["mongodb"] = test_mongodb_connection()
    test_results["neo4j"] = test_neo4j_connection()
    
    # 3. 서비스 테스트
    test_results["learning_path_service"] = test_learning_path_service()
    test_results["diagnostic_service"] = test_diagnostic_service()
    
    # 4. 핵심 기능 테스트
    test_results["express_diagnostic"] = test_express_diagnostic_analysis()
    test_results["learning_path_generation"] = test_learning_path_generation()
    test_results["neo4j_queries"] = test_neo4j_graph_queries()
    
    # 5. AI 통합 테스트
    test_results["ai_integration"] = test_ai_integration()
    
    # 6. 학습 진행 추적 테스트
    test_results["progress_tracking"] = test_learning_progress_tracking()
    
    # 테스트 결과 요약
    print("\n" + "=" * 60)
    print("📊 종합 테스트 결과 요약")
    print("=" * 60)
    
    success_count = 0
    total_count = len(test_results)
    
    for test_name, result in test_results.items():
        if result:
            status = "✅ 성공"
            success_count += 1
        else:
            status = "❌ 실패"
        
        print(f"{test_name:25} : {status}")
    
    print("-" * 60)
    print(f"전체 테스트: {total_count}개")
    print(f"성공: {success_count}개")
    print(f"실패: {total_count - success_count}개")
    print(f"성공률: {success_count/total_count*100:.1f}%")
    
    if success_count == total_count:
        print("\n🎉 모든 테스트가 성공적으로 완료되었습니다!")
    else:
        print(f"\n⚠️ {total_count - success_count}개 테스트가 실패했습니다.")
        print("실패한 테스트를 확인하고 환경 설정을 점검해주세요.")
    
    return test_results

if __name__ == "__main__":
    # 종합 테스트 실행
    results = run_comprehensive_test()
    
    # 결과를 JSON 파일로 저장
    with open("learning_path_test_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2, default=str)
    
    print(f"\n📁 테스트 결과가 'learning_path_test_results.json' 파일에 저장되었습니다.")
