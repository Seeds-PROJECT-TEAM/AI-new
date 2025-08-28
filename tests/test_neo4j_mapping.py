#!/usr/bin/env python3
"""MongoDB concepts → Neo4j 선수개념 조회 테스트"""

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'AI', 'app'))

from db.neo4j import run_cypher
from pymongo import MongoClient

def test_neo4j_mapping():
    try:
        print("=== MongoDB concepts → Neo4j 선수개념 조회 테스트 ===")
        
        # .env 파일에서 MongoDB URI 읽기
        env_path = os.path.join(os.path.dirname(__file__), 'AI', '.env')
        mongodb_uri = None
        
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith('MONGODB_URI='):
                    mongodb_uri = line.strip().split('=', 1)[1]
                    break
        
        if mongodb_uri:
            # MongoDB 연결
            client = MongoClient(mongodb_uri)
            db = client['nerdmath']
            
            # concepts 컬렉션에서 테스트할 개념 선택
            concepts = list(db.concepts.find().limit(3))  # 처음 3개만
            
            print("🔍 MongoDB에서 가져온 개념들:")
            for concept in concepts:
                unit_code = concept.get('unitCode')
                unit_title = concept.get('unitTitle')
                print(f"   📄 {unit_code}: {unit_title}")
            
            print(f"\n🔍 Neo4j에서 선수개념 조회 테스트:")
            
            for concept in concepts:
                unit_code = concept.get('unitCode')
                unit_title = concept.get('unitTitle')
                
                print(f"\n📝 테스트: {unit_code} {unit_title}")
                
                # Neo4j에서 선수개념 조회
                try:
                    query = """
                    MATCH (prereq:Concept)-[:PRECEDES]->(current:Concept {concept: $concept_name})
                    RETURN DISTINCT prereq.concept as concept, prereq.unit as unit, prereq.grade as grade
                    ORDER BY prereq.unit ASC, prereq.concept ASC
                    """
                    
                    # params를 딕셔너리로 전달
                    params = {"concept_name": unit_title}
                    result = run_cypher(query, params)
                    
                    if result:
                        print(f"   ✅ 선수개념 발견: {len(result)}개")
                        for i, prereq in enumerate(result[:5]):  # 처음 5개만
                            print(f"      {i+1}. {prereq['concept']} (단원: {prereq['unit']}, 학년: {prereq['grade']})")
                        if len(result) > 5:
                            print(f"      ... 외 {len(result)-5}개 더")
                    else:
                        print(f"   ⚠️ 선수개념 없음")
                        
                except Exception as e:
                    print(f"   ❌ Neo4j 쿼리 오류: {e}")
            
            client.close()
            
        else:
            print(f"❌ MONGODB_URI를 찾을 수 없음")
            
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_neo4j_mapping()
