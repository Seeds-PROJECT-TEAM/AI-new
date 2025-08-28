#!/usr/bin/env python3
"""기존 concepts 데이터로 Neo4j 매핑 테스트"""

import os
from pymongo import MongoClient

def test_existing_concepts():
    try:
        print("=== 기존 concepts 데이터로 Neo4j 매핑 테스트 ===")
        
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
            
            print("🔍 기존 concepts 컬렉션의 모든 개념 확인:")
            concepts = list(db.concepts.find())
            
            for concept in concepts:
                unit_code = concept.get('unitCode')
                unit_title = concept.get('unitTitle')
                concept_id = concept.get('conceptId')
                print(f"   📄 {unit_code}: {unit_title} (ID: {concept_id})")
            
            print(f"\n🎯 Neo4j 매핑 가능한 개념들:")
            print("   이 개념들을 Neo4j에서 선수개념 조회할 수 있습니다:")
            
            for concept in concepts:
                unit_code = concept.get('unitCode')
                unit_title = concept.get('unitTitle')
                print(f"   ✅ {unit_code} → {unit_title}")
            
            print(f"\n🔍 실제 매핑 예시:")
            print("   Express에서 problemId를 보내면:")
            print("   1. MongoDB에서 unitId 조회")
            print("   2. concepts 컬렉션에서 unitCode 조회")
            print("   3. Neo4j에서 해당 개념의 선수개념 조회")
            
            # 구체적인 예시
            example_concept = concepts[0]  # 3.1 순서쌍과 좌표
            unit_code = example_concept.get('unitCode')
            unit_title = example_concept.get('unitTitle')
            
            print(f"\n📝 예시: {unit_code} {unit_title}")
            print(f"   Neo4j 쿼리:")
            print(f"   MATCH (prereq:Concept)-[:PRECEDES]->(current:Concept {{concept: '{unit_title}'}})")
            print(f"   RETURN DISTINCT prereq.concept as concept, prereq.unit as unit, prereq.grade as grade")
            print(f"   ORDER BY prereq.unit ASC, prereq.concept ASC")
            
            client.close()
            
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_existing_concepts()
