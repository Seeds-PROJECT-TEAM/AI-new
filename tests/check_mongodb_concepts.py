#!/usr/bin/env python3
"""MongoDB에 저장된 개념들과 학습 경로 데이터 확인"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'AI', 'app'))

from services.mongo_service import MongoService
from pprint import pprint

def check_mongodb_concepts():
    try:
        print("=== MongoDB 개념 데이터 확인 ===")
        
        # MongoDB 서비스 초기화
        mongo_service = MongoService()
        
        # 1. 데이터베이스 연결 상태 확인
        print(f"\n1️⃣ MongoDB 연결 상태:")
        print(f"   연결됨: {mongo_service._db is not None}")
        if mongo_service._db:
            print(f"   데이터베이스: {mongo_service._db.name}")
            print(f"   컬렉션 목록: {mongo_service._db.list_collection_names()}")
        
        # 2. problems 컬렉션 확인
        print(f"\n2️⃣ problems 컬렉션:")
        if mongo_service._db and 'problems' in mongo_service._db.list_collection_names():
            problems = list(mongo_service._db.problems.find().limit(5))
            print(f"   총 문제 수: {mongo_service._db.problems.count_documents({})}")
            if problems:
                print(f"   샘플 문제:")
                for i, problem in enumerate(problems):
                    print(f"     {i+1}. ID: {problem.get('_id')}")
                    print(f"        problemId: {problem.get('problemId', 'N/A')}")
                    print(f"        unitId: {problem.get('unitId', 'N/A')}")
                    print(f"        concept: {problem.get('concept', 'N/A')}")
                    print(f"        grade: {problem.get('grade', 'N/A')}")
                    print()
        else:
            print("   ⚠️ problems 컬렉션이 없음")
        
        # 3. units 컬렉션 확인
        print(f"\n3️⃣ units 컬렉션:")
        if mongo_service._db and 'units' in mongo_service._db.list_collection_names():
            units = list(mongo_service._db.units.find().limit(5))
            print(f"   총 단원 수: {mongo_service._db.units.count_documents({})}")
            if units:
                print(f"   샘플 단원:")
                for i, unit in enumerate(units):
                    print(f"     {i+1}. ID: {unit.get('_id')}")
                    print(f"        unitId: {unit.get('unitId', 'N/A')}")
                    print(f"        chapterTitle: {unit.get('chapterTitle', 'N/A')}")
                    print(f"        title: {unit.get('title', 'N/A')}")
                    print(f"        grade: {unit.get('grade', 'N/A')}")
                    print()
        else:
            print("   ⚠️ units 컬렉션이 없음")
        
        # 4. learning_paths 컬렉션 확인
        print(f"\n4️⃣ learning_paths 컬렉션:")
        if mongo_service._db and 'learning_paths' in mongo_service._db.list_collection_names():
            learning_paths = list(mongo_service._db.learning_paths.find().limit(3))
            print(f"   총 학습 경로 수: {mongo_service._db.learning_paths.count_documents({})}")
            if learning_paths:
                print(f"   최근 학습 경로:")
                for i, path in enumerate(learning_paths):
                    print(f"     {i+1}. pathId: {path.get('pathId', 'N/A')}")
                    print(f"        pathName: {path.get('pathName', 'N/A')}")
                    print(f"        totalConcepts: {path.get('totalConcepts', 'N/A')}")
                    print(f"        nodes 수: {len(path.get('nodes', []))}")
                    if path.get('nodes'):
                        print(f"        노드들:")
                        for j, node in enumerate(path['nodes'][:3]):  # 처음 3개만
                            print(f"          {j+1}. {node.get('concept', 'N/A')} (우선순위: {node.get('priority', 'N/A')})")
                    print()
        else:
            print("   ⚠️ learning_paths 컬렉션이 없음")
        
        # 5. diagnostic_results 컬렉션 확인
        print(f"\n5️⃣ diagnostic_results 컬렉션:")
        if mongo_service._db and 'diagnostic_results' in mongo_service._db.list_collection_names():
            diagnostic_results = list(mongo_service._db.diagnostic_results.find().limit(3))
            print(f"   총 진단 결과 수: {mongo_service._db.diagnostic_results.count_documents({})}")
            if diagnostic_results:
                print(f"   최근 진단 결과:")
                for i, result in enumerate(diagnostic_results):
                    print(f"     {i+1}. ID: {result.get('_id')}")
                    print(f"        testId: {result.get('testId', 'N/A')}")
                    print(f"        userId: {result.get('userId', 'N/A')}")
                    print(f"        weakUnits: {result.get('weakUnits', [])}")
                    print(f"        weakConcepts: {result.get('weakConcepts', [])}")
                    print()
        else:
            print("   ⚠️ diagnostic_results 컬렉션이 없음")
        
        # 6. 전체 컬렉션 통계
        print(f"\n6️⃣ 전체 컬렉션 통계:")
        if mongo_service._db:
            collections = mongo_service._db.list_collection_names()
            for collection_name in collections:
                count = mongo_service._db[collection_name].count_documents({})
                print(f"   {collection_name}: {count}개 문서")
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_mongodb_concepts()
