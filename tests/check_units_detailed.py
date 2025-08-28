#!/usr/bin/env python3
"""units 컬렉션 상세 정보 확인"""

import os
from pymongo import MongoClient
from pprint import pprint

def check_units_detailed():
    try:
        print("=== units 컬렉션 상세 정보 확인 ===")
        
        # .env 파일에서 MongoDB URI 읽기
        env_path = os.path.join(os.path.dirname(__file__), 'AI', '.env')
        mongodb_uri = None
        
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith('MONGODB_URI='):
                    mongodb_uri = line.strip().split('=', 1)[1]
                    break
        
        if mongodb_uri:
            client = MongoClient(mongodb_uri)
            db = client['nerdmath']
            
            # units 컬렉션의 모든 문서 조회
            units = list(db.units.find())
            print(f"📚 units 컬렉션: 총 {len(units)}개 문서")
            
            for i, unit in enumerate(units):
                print(f"\n🔍 단원 {i+1}:")
                print(f"   ID: {unit.get('_id')}")
                print(f"   unitId: {unit.get('unitId')}")
                print(f"   chapterTitle: {unit.get('chapterTitle')}")
                print(f"   title: {unit.get('title')}")
                print(f"   grade: {unit.get('grade')}")
                
                # 추가 필드들 확인
                for key, value in unit.items():
                    if key not in ['_id', 'unitId', 'chapterTitle', 'title', 'grade']:
                        print(f"   {key}: {value}")
            
            # concepts 컬렉션도 확인
            print(f"\n📚 concepts 컬렉션:")
            concepts = list(db.concepts.find())
            print(f"   총 {len(concepts)}개 문서")
            
            for i, concept in enumerate(concepts[:5]):  # 처음 5개만
                print(f"\n   개념 {i+1}:")
                print(f"     ID: {concept.get('_id')}")
                print(f"     unitId: {concept.get('unitId')}")
                
                # 모든 필드 출력
                for key, value in concept.items():
                    if key not in ['_id']:
                        print(f"     {key}: {value}")
            
            # problems 컬렉션도 확인
            print(f"\n📚 problems 컬렉션:")
            problems = list(db.problems.find())
            print(f"   총 {len(problems)}개 문서")
            
            for i, problem in enumerate(problems[:5]):  # 처음 5개만
                print(f"\n   문제 {i+1}:")
                print(f"     ID: {problem.get('_id')}")
                print(f"     unitId: {problem.get('unitId')}")
                
                # 모든 필드 출력
                for key, value in problem.items():
                    if key not in ['_id']:
                        print(f"     {key}: {value}")
            
            client.close()
            
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_units_detailed()
