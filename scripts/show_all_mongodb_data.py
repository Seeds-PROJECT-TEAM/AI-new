#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MongoDB에 저장된 모든 진단테스트 데이터를 상세하게 보여주기
"""

import os
from pymongo import MongoClient
from dotenv import load_dotenv

# AI 폴더의 .env 파일 로드
load_dotenv('AI/.env')

def show_all_mongodb_data():
    try:
        # MongoDB 연결
        client = MongoClient(os.getenv('MONGODB_URI'))
        db = client.nerdmath
        
        print("=== MongoDB에 저장된 모든 진단테스트 데이터 ===\n")
        
        # Express 진단테스트 결과 컬렉션
        express_collection = db.express_diagnostic_results
        all_results = list(express_collection.find().sort('_id', -1))
        
        print(f"📊 총 {len(all_results)}개의 진단테스트 결과가 저장되어 있습니다.\n")
        
        for i, result in enumerate(all_results, 1):
            print(f"{'='*60}")
            print(f"📋 진단테스트 {i}")
            print(f"{'='*60}")
            
            # 기본 정보
            print(f"🆔 ID: {result.get('_id')}")
            print(f"📝 Test ID: {result.get('testId')}")
            print(f"👤 User ID: {result.get('userId')}")
            print(f"📚 Grade Range: {result.get('gradeRange')}")
            print(f"📊 Status: {result.get('status')}")
            print(f"⏰ Created At: {result.get('createdAt')}")
            
            # 진단 데이터
            diagnostic_data = result.get('diagnosticData', {})
            if diagnostic_data:
                print(f"\n📊 진단 데이터:")
                print(f"   총 문제 수: {diagnostic_data.get('totalProblems', 'N/A')}")
                print(f"   총 소요 시간: {diagnostic_data.get('durationSec', 'N/A')}초")
                
                answers = diagnostic_data.get('answers', [])
                if answers:
                    print(f"   답안 ({len(answers)}개):")
                    for j, answer in enumerate(answers, 1):
                        is_correct = "✅" if answer.get('isCorrect') else "❌"
                        duration = answer.get('durationSeconds', 0)
                        print(f"     {j}. {is_correct} {answer.get('problemId', 'N/A')} ({duration}초)")
            
            # 분석 결과
            analysis = result.get('analysisResult', {})
            if analysis:
                print(f"\n🔍 분석 결과:")
                print(f"   Analysis ID: {analysis.get('analysisId', 'N/A')}")
                print(f"   AI Comment: {analysis.get('aiComment', 'N/A')}")
                print(f"   Class: {analysis.get('class', 'N/A')}")
                print(f"   Overall Level: {analysis.get('overallLevel', 'N/A')}")
                print(f"   Grade Range: {analysis.get('gradeRange', 'N/A')}")
                
                # 추천 경로
                recommended_path = analysis.get('recommendedPath', [])
                if recommended_path:
                    print(f"\n🛤️ 추천 학습 경로 ({len(recommended_path)}개):")
                    for j, path_item in enumerate(recommended_path, 1):
                        print(f"   {j}. {path_item.get('unitTitle', 'N/A')}")
                        print(f"      Priority: {path_item.get('priority', 'N/A')}")
                        print(f"      Reason: {path_item.get('reason', 'N/A')}")
                else:
                    print(f"\n🛤️ 추천 학습 경로: 없음")
                
                # 취약 단원/개념
                weak_units = analysis.get('weakUnits', [])
                if weak_units:
                    print(f"\n⚠️ 취약 단원: {', '.join(weak_units)}")
                
                weak_concepts = analysis.get('weakConcepts', [])
                if weak_concepts:
                    print(f"⚠️ 취약 개념: {', '.join(weak_concepts)}")
            
            # 학습 경로
            learning_path = result.get('learningPath', {})
            if learning_path:
                print(f"\n📚 학습 경로:")
                print(f"   Path ID: {learning_path.get('pathId', 'N/A')}")
                print(f"   Path Name: {learning_path.get('pathName', 'N/A')}")
                print(f"   Total Concepts: {learning_path.get('totalConcepts', 'N/A')}")
                print(f"   Status: {learning_path.get('status', 'N/A')}")
                
                nodes = learning_path.get('nodes', [])
                if nodes:
                    print(f"   Nodes ({len(nodes)}개):")
                    for j, node in enumerate(nodes[:3], 1):  # 최대 3개만
                        print(f"     {j}. {node.get('concept', 'N/A')} | {node.get('unit', 'N/A')}")
                    if len(nodes) > 3:
                        print(f"     ... 외 {len(nodes) - 3}개")
            
            print(f"\n")
        
        print(f"✅ 모든 데이터 조회 완료!")
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if 'client' in locals():
            client.close()

if __name__ == "__main__":
    show_all_mongodb_data()
