#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MongoDB에 저장된 진단테스트 데이터를 JSON 형태로 조회
"""

import os
import json
from pymongo import MongoClient
from bson import ObjectId
from dotenv import load_dotenv
from datetime import datetime

# AI 폴더의 .env 파일 로드
load_dotenv('AI/.env')

class DateTimeEncoder(json.JSONEncoder):
    """datetime 객체를 JSON으로 직렬화하기 위한 인코더"""
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, ObjectId):
            return str(obj)
        return super().default(obj)

def check_all_mongodb_data():
    try:
        # MongoDB 연결
        client = MongoClient(os.getenv('MONGODB_URI'))
        db = client.nerdmath
        
        print("=== MongoDB에 저장된 모든 진단테스트 결과 ===\n")
        
        # 1. Express 진단테스트 결과 컬렉션
        print("1. express_diagnostic_results 컬렉션:")
        express_results = list(db.express_diagnostic_results.find().sort('_id', -1))
        
        for i, result in enumerate(express_results, 1):
            print(f"\n--- 진단테스트 {i} ---")
            print(f"ID: {result.get('_id')}")
            print(f"Test ID: {result.get('testId')}")
            print(f"User ID: {result.get('userId')}")
            print(f"Grade Range: {result.get('gradeRange')}")
            print(f"Status: {result.get('status')}")
            print(f"Created At: {result.get('createdAt')}")
            
            # Analysis Result 상세 정보
            analysis = result.get('analysisResult', {})
            if analysis:
                print(f"\n  Analysis Result:")
                print(f"    AI Comment: {analysis.get('aiComment', '')}")
                print(f"    Class: {analysis.get('class', '')}")
                print(f"    Overall Level: {analysis.get('overallLevel', '')}")
                print(f"    Grade Range: {analysis.get('gradeRange', '')}")
                
                # Recommended Path 배열
                recommended_path = analysis.get('recommendedPath', [])
                if recommended_path:
                    print(f"    Recommended Path ({len(recommended_path)}개):")
                    for j, path_item in enumerate(recommended_path, 1):
                        print(f"      {j}. {path_item.get('unitTitle', '')} (Priority: {path_item.get('priority', '')})")
                        print(f"         Reason: {path_item.get('reason', '')}")
                
                # Weak Units & Concepts
                weak_units = analysis.get('weakUnits', [])
                if weak_units:
                    print(f"    Weak Units: {weak_units}")
                
                weak_concepts = analysis.get('weakConcepts', [])
                if weak_concepts:
                    print(f"    Weak Concepts: {weak_concepts}")
            
            # Learning Path 정보
            learning_path = result.get('learningPath', {})
            if learning_path:
                print(f"\n  Learning Path:")
                print(f"    Path ID: {learning_path.get('pathId', '')}")
                print(f"    Path Name: {learning_path.get('pathName', '')}")
                print(f"    Total Concepts: {learning_path.get('totalConcepts', '')}")
                print(f"    Status: {learning_path.get('status', '')}")
                
                # Nodes 정보
                nodes = learning_path.get('nodes', [])
                if nodes:
                    print(f"    Nodes ({len(nodes)}개):")
                    for j, node in enumerate(nodes[:3], 1):  # 최대 3개만
                        print(f"      {j}. {node.get('concept', 'N/A')} | {node.get('unit', 'N/A')}")
                    if len(nodes) > 3:
                        print(f"      ... 외 {len(nodes) - 3}개")
        
        print(f"\n총 {len(express_results)}개의 진단테스트 결과가 저장되어 있습니다.")
        
        # 2. JSON 형태로 전체 데이터 출력
        print("\n" + "="*80)
        print("전체 데이터를 JSON 형태로 출력:")
        print("="*80)
        
        # ObjectId를 문자열로 변환
        for result in express_results:
            result['_id'] = str(result['_id'])
        
        # JSON으로 출력 (보기 좋게 포맷팅)
        json_output = json.dumps(express_results, indent=2, ensure_ascii=False, cls=DateTimeEncoder)
        print(json_output)
        
        # 3. 파일로도 저장
        with open('mongodb_diagnostic_data.json', 'w', encoding='utf-8') as f:
            json.dump(express_results, f, indent=2, ensure_ascii=False, cls=DateTimeEncoder)
        print(f"\n✅ JSON 데이터가 'mongodb_diagnostic_data.json' 파일로 저장되었습니다.")
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if 'client' in locals():
            client.close()

if __name__ == "__main__":
    check_all_mongodb_data()
