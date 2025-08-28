#!/usr/bin/env python3
"""Neo4j 개념명 앞부분 코드 → MongoDB unitCode 매핑 테스트"""

import os
import sys
import re
sys.path.append(os.path.join(os.path.dirname(__file__), 'AI', 'app'))

from db.neo4j import run_cypher
from pymongo import MongoClient

def extract_unit_code_from_concept_name(concept_name):
    """Neo4j 개념명에서 unitCode 추출 (예: '1.5 정수와 유리수의 덧셈, 뺄셈' → '1.5')"""
    if not concept_name:
        return None
    
    # 정규식으로 "숫자.숫자" 패턴 찾기
    match = re.search(r'(\d+\.\d+)', concept_name)
    if match:
        return match.group(1)
    
    return None

def test_code_mapping():
    try:
        print("=== Neo4j 개념명 앞부분 코드 → MongoDB unitCode 매핑 테스트 ===")
        
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
            
            print("🔍 1단계: MongoDB concepts 컬렉션의 unitCode 확인")
            mongo_concepts = list(db.concepts.find())
            mongo_unit_codes = [concept.get('unitCode') for concept in mongo_concepts]
            print(f"   MongoDB unitCode들: {mongo_unit_codes}")
            
            print(f"\n🔍 2단계: Neo4j에서 Concept 노드들의 개념명 확인")
            try:
                neo4j_query = """
                MATCH (c:Concept)
                RETURN c.concept as concept, c.unit as unit, c.grade as grade
                ORDER BY c.unit ASC, c.concept ASC
                LIMIT 20
                """
                
                neo4j_concepts = run_cypher(neo4j_query)
                
                if neo4j_concepts:
                    print(f"   ✅ Neo4j Concept 노드 발견: {len(neo4j_concepts)}개")
                    
                    # 각 Neo4j 개념명에서 unitCode 추출
                    print(f"\n🔍 3단계: Neo4j 개념명에서 unitCode 추출 및 매핑")
                    
                    for i, neo4j_concept in enumerate(neo4j_concepts[:10]):  # 처음 10개만
                        concept_name = neo4j_concept.get('concept')
                        extracted_code = extract_unit_code_from_concept_name(concept_name)
                        
                        print(f"\n   📄 Neo4j 개념 {i+1}: {concept_name}")
                        print(f"      추출된 코드: {extracted_code}")
                        
                        # MongoDB unitCode와 매핑 확인
                        if extracted_code in mongo_unit_codes:
                            print(f"      ✅ MongoDB 매핑 성공! → {extracted_code}")
                            
                            # 해당 MongoDB 개념 정보 찾기
                            mongo_concept = next((c for c in mongo_concepts if c.get('unitCode') == extracted_code), None)
                            if mongo_concept:
                                mongo_title = mongo_concept.get('unitTitle')
                                print(f"      📚 MongoDB 개념: {mongo_title}")
                        else:
                            print(f"      ❌ MongoDB 매핑 실패")
                    
                    print(f"\n🔍 4단계: 매핑 가능한 개념들 요약")
                    successful_mappings = []
                    
                    for neo4j_concept in neo4j_concepts:
                        concept_name = neo4j_concept.get('concept')
                        extracted_code = extract_unit_code_from_concept_name(concept_name)
                        
                        if extracted_code and extracted_code in mongo_unit_codes:
                            successful_mappings.append({
                                'neo4j_concept': concept_name,
                                'extracted_code': extracted_code,
                                'mongo_title': next((c.get('unitTitle') for c in mongo_concepts if c.get('unitCode') == extracted_code), None)
                            })
                    
                    print(f"   🎯 성공적인 매핑: {len(successful_mappings)}개")
                    for mapping in successful_mappings[:5]:  # 처음 5개만
                        print(f"      ✅ {mapping['extracted_code']}: {mapping['neo4j_concept']} → {mapping['mongo_title']}")
                    
                else:
                    print(f"   ⚠️ Neo4j Concept 노드가 없음")
                    
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
    test_code_mapping()
