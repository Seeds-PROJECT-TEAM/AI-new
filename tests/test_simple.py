#!/usr/bin/env python3
"""
간단한 테스트 - 직접 경로 설정
"""

import os
import sys

# 현재 디렉토리를 Python 경로에 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
ai_app_dir = os.path.join(current_dir, 'AI', 'app')
sys.path.insert(0, ai_app_dir)

print(f"🔍 현재 디렉토리: {current_dir}")
print(f"🔍 AI app 디렉토리: {ai_app_dir}")
print(f"🔍 Python 경로에 추가됨: {ai_app_dir in sys.path}")

try:
    print("\n📚 모델 import 시도...")
    from models.learning_path import DiagnosticAnalysis
    print("✅ DiagnosticAnalysis import 성공!")
    
    print("\n🔧 진단 서비스 import 시도...")
    from services.diagnostic_service import DiagnosticService
    print("✅ DiagnosticService import 성공!")
    
    print("\n🛤️ 학습 경로 서비스 import 시도...")
    from services.learning_path import LearningPathService
    print("✅ LearningPathService import 성공!")
    
    print("\n🎯 실제 테스트 시작...")
    
    # 1. 진단 서비스 테스트
    diagnostic_service = DiagnosticService()
    print("✅ 진단 서비스 생성 성공")
    
    # 추천 경로 생성
    wrong_units = ["정수와 유리수", "문자와 식", "함수"]
    accuracy_rate = 65.0
    recommended_path = diagnostic_service._generate_recommended_path(wrong_units, accuracy_rate)
    print(f"🎯 추천 경로 생성: {len(recommended_path)}개")
    
    for i, path in enumerate(recommended_path, 1):
        print(f"   {i}. {path['unitTitle']} (우선순위: {path['priority']})")
        print(f"      이유: {path['reason']}")
    
    # 2. 학습 경로 서비스 테스트
    learning_service = LearningPathService()
    print("\n✅ 학습 경로 서비스 생성 성공")
    
    # 연결 상태 확인
    neo4j_connected = learning_service.is_neo4j_connected()
    print(f"🔗 Neo4j 연결: {'연결됨' if neo4j_connected else '연결 안됨'}")
    
    mongodb_connected = learning_service.is_mongodb_connected()
    print(f"🗄️ MongoDB 연결: {'연결됨' if mongodb_connected else '연결 안됨'}")
    
    # 3. DiagnosticAnalysis 객체 생성 테스트
    analysis = DiagnosticAnalysis(
        analysisId="test_001",
        testId="test_001",
        userId="test_user_001",
        weakUnits=wrong_units,
        weakConcepts=["정수의 덧셈", "문자와 식"],
        incorrectConcepts=[],
        conceptErrorRates={},
        overallLevel="보통",
        unitLevels={},
        recommendedPath=recommended_path,
        aiComment="테스트용 AI 코멘트입니다.",
        recommendedStartUnit="정수와 유리수",
        recommendedStartConcept="정수의 덧셈"
    )
    
    print(f"\n✅ DiagnosticAnalysis 객체 생성 성공!")
    print(f"   - 분석 ID: {analysis.analysisId}")
    print(f"   - AI 코멘트: {analysis.aiComment}")
    print(f"   - 추천 경로 수: {len(analysis.recommendedPath)}")
    
    # MongoDB 저장용 딕셔너리 변환
    analysis_dict = analysis.dict()
    print(f"   - MongoDB 저장용 딕셔너리 생성 성공")
    print(f"   - AI 코멘트: {analysis_dict.get('aiComment')}")
    print(f"   - 추천 경로: {len(analysis_dict.get('recommendedPath', []))}개")
    
    print("\n🎉 모든 테스트 성공!")
    
except Exception as e:
    print(f"\n❌ 오류 발생: {e}")
    import traceback
    traceback.print_exc()
