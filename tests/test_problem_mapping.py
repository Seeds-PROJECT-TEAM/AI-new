#!/usr/bin/env python3
"""problemId → unitId → unitCode → Neo4j 매핑 테스트"""

import os
from pymongo import MongoClient

def test_problem_mapping():
    try:
        print("=== problemId → unitId → unitCode → Neo4j 매핑 테스트 ===")
        
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
            
            print("🔍 1단계: problems 컬렉션에서 problemId와 unitId 매핑 확인")
            problems = list(db.problems.find())
            
            for problem in problems:
                problem_id = problem.get('problem_id')
                unit_id = problem.get('unitId')
                print(f"   📄 {problem_id} → unitId: {unit_id}")
            
            print(f"\n🔍 2단계: units 컬렉션에서 unitId와 단원명 매핑 확인")
            units = list(db.units.find())
            
            for unit in units:
                unit_id = unit.get('_id')
                unit_code = unit.get('unitId')
                title = unit.get('title', {}).get('ko', 'N/A')
                print(f"   📄 {unit_id} → {unit_code} → {title}")
            
            print(f"\n🔍 3단계: concepts 컬렉션에서 unitCode와 개념명 매핑 확인")
            concepts = list(db.concepts.find())
            
            for concept in concepts:
                concept_id = concept.get('_id')
                unit_id = concept.get('unitId')
                unit_code = concept.get('unitCode')
                unit_title = concept.get('unitTitle')
                print(f"   📄 {concept_id} → {unit_id} → {unit_code} → {unit_title}")
            
            print(f"\n🔍 4단계: 실제 매핑 체인 테스트")
            print("   문제: problem_001로 시작해서 Neo4j 개념명까지 찾기")
            
            # problem_001로 시작
            problem_001 = db.problems.find_one({'problem_id': 'problem_001'})
            if problem_001:
                problem_unit_id = problem_001.get('unitId')
                print(f"   ✅ problem_001 → unitId: {problem_unit_id}")
                
                # unitId로 unit 정보 찾기
                unit_info = db.units.find_one({'_id': problem_unit_id})
                if unit_info:
                    unit_code = unit_info.get('unitId')
                    unit_title = unit_info.get('title', {}).get('ko', 'N/A')
                    print(f"   ✅ unitId: {problem_unit_id} → {unit_code} → {unit_title}")
                    
                    # 이제 concepts 컬렉션에서 이 unitId에 해당하는 unitCode 찾기
                    concept_info = db.concepts.find_one({'unitId': problem_unit_id})
                    if concept_info:
                        neo4j_unit_code = concept_info.get('unitCode')
                        neo4j_concept_name = concept_info.get('unitTitle')
                        print(f"   ✅ concepts → unitCode: {neo4j_unit_code} → {neo4j_concept_name}")
                        
                        print(f"\n🎯 최종 매핑 결과:")
                        print(f"   problem_001 → {unit_code} → {neo4j_unit_code} → {neo4j_concept_name}")
                        print(f"   이제 Neo4j에서 '{neo4j_concept_name}'의 선수개념을 조회할 수 있습니다!")
                    else:
                        print(f"   ⚠️ concepts 컬렉션에서 unitId {problem_unit_id}에 해당하는 개념을 찾을 수 없음")
                else:
                    print(f"   ⚠️ units 컬렉션에서 unitId {problem_unit_id}를 찾을 수 없음")
            else:
                print(f"   ❌ problem_001을 찾을 수 없음")
            
            client.close()
            
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_problem_mapping()
