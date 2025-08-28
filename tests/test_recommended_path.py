#!/usr/bin/env python3
"""
추천 학습 경로 테스트
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'AI', 'app'))

from models.learning_path import DiagnosticAnalysis
from services.diagnostic_service import DiagnosticService

def test_recommended_path():
    """추천 학습 경로 생성 테스트"""
    
    print("=== 추천 학습 경로 테스트 ===")
    
    # 진단 서비스 생성
    service = DiagnosticService()
    
    # 테스트용 데이터
    wrong_units = ["정수와 유리수", "문자와 식", "함수"]
    accuracy_rate = 65.0  # 65% 정답률
    
    # 추천 경로 생성
    recommended_path = service._generate_recommended_path(wrong_units, accuracy_rate)
    
    print(f"📊 정답률: {accuracy_rate}%")
    print(f"📚 취약 단원: {wrong_units}")
    print(f"🎯 추천 학습 경로:")
    
    for i, path in enumerate(recommended_path, 1):
        print(f"   {i}. {path['unitTitle']}")
        print(f"      - ID: {path['unitId']}")
        print(f"      - 우선순위: {path['priority']}")
        print(f"      - 이유: {path['reason']}")
        print()
    
    # 학습자 클래스 결정
    learner_class = service._determine_learner_class(accuracy_rate, 120.0)
    print(f"🏆 학습자 클래스: {learner_class}")
    
    # DiagnosticAnalysis 객체 생성 테스트
    try:
        analysis = DiagnosticAnalysis(
            analysisId="test_analysis_001",
            testId="test_001",
            userId="user_001",
            weakUnits=wrong_units,
            weakConcepts=["정수와 유리수", "문자와 식"],
            incorrectConcepts=[],
            conceptErrorRates={},
            overallLevel="보통",
            unitLevels={},
            recommendedPath=recommended_path,
            class=learner_class,
            recommendedStartUnit="정수와 유리수",
            recommendedStartConcept="정수의 덧셈"
        )
        
        print("✅ DiagnosticAnalysis 객체 생성 성공!")
        print(f"   - 분석 ID: {analysis.analysisId}")
        print(f"   - 클래스: {analysis.class}")
        print(f"   - 추천 경로 수: {len(analysis.recommendedPath)}")
        
        # MongoDB 저장용 딕셔너리 변환
        analysis_dict = analysis.dict()
        print(f"   - MongoDB 저장용 딕셔너리 생성 성공")
        print(f"   - 클래스 필드: {analysis_dict.get('class')}")
        print(f"   - 추천 경로: {analysis_dict.get('recommendedPath')}")
        
    except Exception as e:
        print(f"❌ DiagnosticAnalysis 객체 생성 실패: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_recommended_path()
