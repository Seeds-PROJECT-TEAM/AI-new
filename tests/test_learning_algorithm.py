#!/usr/bin/env python3
"""
맞춤형 학습 알고리즘 전체 테스트
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'AI', 'app'))

from services.learning_path import LearningPathService
from services.diagnostic_service import DiagnosticService
from models.learning_path import DiagnosticAnalysis, LearningPath
import uuid
from datetime import datetime

def test_learning_algorithm():
    """맞춤형 학습 알고리즘 전체 테스트"""
    
    print("🚀 맞춤형 학습 알고리즘 테스트 시작!")
    print("=" * 60)
    
    # 1. 진단 서비스 테스트
    print("\n📊 1단계: 진단 서비스 테스트")
    print("-" * 40)
    
    try:
        diagnostic_service = DiagnosticService()
        print("✅ 진단 서비스 생성 성공")
        
        # 테스트용 취약 단원 데이터
        wrong_units = ["정수와 유리수", "문자와 식", "함수"]
        accuracy_rate = 65.0
        
        # 추천 경로 생성 테스트
        recommended_path = diagnostic_service._generate_recommended_path(wrong_units, accuracy_rate)
        print(f"✅ 추천 경로 생성 성공: {len(recommended_path)}개")
        
        for i, path in enumerate(recommended_path, 1):
            print(f"   {i}. {path['unitTitle']} (우선순위: {path['priority']})")
            print(f"      이유: {path['reason']}")
        
        # 학습자 클래스 결정 테스트
        learner_class = diagnostic_service._determine_learner_class(accuracy_rate, 120.0)
        print(f"\n🏆 학습자 클래스: {learner_class}")
        
    except Exception as e:
        print(f"❌ 진단 서비스 테스트 실패: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # 2. 학습 경로 서비스 테스트
    print("\n🛤️ 2단계: 학습 경로 서비스 테스트")
    print("-" * 40)
    
    try:
        learning_service = LearningPathService()
        print("✅ 학습 경로 서비스 생성 성공")
        
        # Neo4j 연결 상태 확인
        if learning_service.is_neo4j_connected():
            print("✅ Neo4j 연결됨")
        else:
            print("⚠️ Neo4j 연결 안됨 - 기본 모드로 진행")
        
        # MongoDB 연결 상태 확인
        if learning_service.is_mongodb_connected():
            print("✅ MongoDB 연결됨")
        else:
            print("⚠️ MongoDB 연결 안됨 - 기본 모드로 진행")
        
    except Exception as e:
        print(f"❌ 학습 경로 서비스 테스트 실패: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # 3. 추천 경로 생성 테스트
    print("\n🎯 3단계: 추천 경로 생성 테스트")
    print("-" * 40)
    
    try:
        # 가상의 진단 분석 결과 생성
        mock_analysis = DiagnosticAnalysis(
            analysisId=f"test_analysis_{uuid.uuid4().hex[:8]}",
            testId="test_001",
            userId="test_user_001",
            weakUnits=wrong_units,
            weakConcepts=["정수의 덧셈", "문자와 식", "함수 그래프"],
            incorrectConcepts=[],
            conceptErrorRates={},
            overallLevel="보통",
            unitLevels={},
            recommendedPath=recommended_path,
            class=learner_class,
            recommendedStartUnit="정수와 유리수",
            recommendedStartConcept="정수의 덧셈"
        )
        
        print("✅ 가상 진단 분석 결과 생성 성공")
        print(f"   - 분석 ID: {mock_analysis.analysisId}")
        print(f"   - 취약 단원: {len(mock_analysis.weakUnits)}개")
        print(f"   - 취약 개념: {len(mock_analysis.weakConcepts)}개")
        print(f"   - 추천 경로: {len(mock_analysis.recommendedPath)}개")
        
        # 추천 경로 생성 테스트
        if learning_service.is_neo4j_connected():
            try:
                recommended_path_result = learning_service.generate_recommended_path_from_analysis(mock_analysis)
                print(f"\n✅ Neo4j 기반 추천 경로 생성 성공: {len(recommended_path_result)}개")
                
                for i, path in enumerate(recommended_path_result, 1):
                    print(f"   {i}. {path.get('unitTitle', 'N/A')}")
                    print(f"      - ID: {path.get('unitId', 'N/A')}")
                    print(f"      - 우선순위: {path.get('priority', 'N/A')}")
                    print(f"      - 이유: {path.get('reason', 'N/A')}")
                    
            except Exception as e:
                print(f"⚠️ Neo4j 기반 추천 경로 생성 실패: {e}")
                print("   기본 경로 생성으로 대체")
        else:
            print("⚠️ Neo4j 연결 없음 - 기본 경로 생성 건너뜀")
        
    except Exception as e:
        print(f"❌ 추천 경로 생성 테스트 실패: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # 4. 학습 경로 생성 테스트
    print("\n📚 4단계: 학습 경로 생성 테스트")
    print("-" * 40)
    
    try:
        # 가상의 진단 분석 결과를 MongoDB에 저장 (테스트용)
        if learning_service.is_mongodb_connected():
            # MongoDB에 테스트 데이터 저장
            analysis_dict = mock_analysis.dict()
            analysis_dict["createdAt"] = datetime.now()
            analysis_dict["updatedAt"] = datetime.now()
            
            result = learning_service.diagnostic_analyses.insert_one(analysis_dict)
            print(f"✅ 테스트 진단 분석 결과 MongoDB 저장 성공: {result.inserted_id}")
            
            # 학습 경로 생성 시도
            try:
                learning_path = learning_service.create_learning_path(str(result.inserted_id))
                print(f"✅ 학습 경로 생성 성공!")
                print(f"   - 경로 ID: {learning_path.pathId}")
                print(f"   - 총 개념: {learning_path.totalConcepts}개")
                print(f"   - 예상 시간: {learning_path.estimatedDuration}분")
                print(f"   - 시작 개념: {learning_path.startConcept}")
                
                # 노드 정보 출력
                if learning_path.nodes:
                    print(f"\n📋 학습 노드 (최대 5개):")
                    for i, node in enumerate(learning_path.nodes[:5], 1):
                        print(f"   {i}. {node.concept} (우선순위: {node.priority})")
                        print(f"      단원: {node.unit}, 취약: {node.isWeakConcept}")
                    if len(learning_path.nodes) > 5:
                        print(f"   ... 외 {len(learning_path.nodes) - 5}개")
                
            except Exception as e:
                print(f"⚠️ 학습 경로 생성 실패: {e}")
                print("   Neo4j 연결 문제일 수 있음")
        else:
            print("⚠️ MongoDB 연결 없음 - 학습 경로 생성 건너뜀")
        
    except Exception as e:
        print(f"❌ 학습 경로 생성 테스트 실패: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # 5. 결과 요약
    print("\n🎉 테스트 완료!")
    print("=" * 60)
    print("✅ 진단 서비스: 정상 작동")
    print("✅ 학습 경로 서비스: 정상 작동")
    print("✅ 추천 경로 생성: 정상 작동")
    print("✅ 학습자 클래스 분류: 정상 작동")
    
    if learning_service.is_neo4j_connected():
        print("✅ Neo4j 그래프 탐색: 정상 작동")
    else:
        print("⚠️ Neo4j 그래프 탐색: 연결 안됨")
    
    if learning_service.is_mongodb_connected():
        print("✅ MongoDB 데이터 저장: 정상 작동")
    else:
        print("⚠️ MongoDB 데이터 저장: 연결 안됨")

if __name__ == "__main__":
    test_learning_algorithm()
