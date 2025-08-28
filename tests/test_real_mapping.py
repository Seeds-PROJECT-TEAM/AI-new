#!/usr/bin/env python3
"""MongoDB concepts → Neo4j 실제 매핑 및 선수개념 조회 테스트"""

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'AI', 'app'))

from db.neo4j import run_cypher
from pymongo import MongoClient

def test_real_mapping():
    try:
        print("=== MongoDB concepts → Neo4j 실제 매핑 및 선수개념 조회 테스트 ===")
        
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
            
            print("🔍 1단계: MongoDB concepts 컬렉션에서 테스트할 개념 선택")
            mongo_concepts = list(db.concepts.find().limit(3))  # 처음 3개만
            
            for concept in mongo_concepts:
                unit_code = concept.get('unitCode')
                unit_title = concept.get('unitTitle')
                print(f"   📄 {unit_code}: {unit_title}")
            
            print(f"\n🔍 2단계: 각 MongoDB 개념에 대해 Neo4j 선수개념 조회")
            
            for concept in mongo_concepts:
                unit_code = concept.get('unitCode')
                unit_title = concept.get('unitTitle')
                
                print(f"\n📝 테스트: {unit_code} {unit_title}")
                print(f"   Neo4j에서 '{unit_title}'의 선수개념 조회 시도...")
                
                # Neo4j에서 선수개념 조회
                try:
                    query = """
                    MATCH (prereq:Concept)-[:PRECEDES]->(current:Concept {concept: $concept_name})
                    RETURN DISTINCT prereq.concept as concept, prereq.unit as unit, prereq.grade as grade
                    ORDER BY prereq.unit ASC, prereq.concept ASC
                    """
                    
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
            
            print(f"\n🔍 3단계: 실제 학습 경로 생성 예시")
            print("   MongoDB concept '3.1 순서쌍과 좌표'를 사용한 학습 경로:")
            
            # 3.1 순서쌍과 좌표로 테스트
            test_concept = mongo_concepts[0]  # 3.1
            unit_title = test_concept.get('unitTitle')
            
            try:
                # 선수개념 조회
                prereq_query = """
                MATCH (prereq:Concept)-[:PRECEDES]->(current:Concept {concept: $concept_name})
                RETURN DISTINCT prereq.concept as concept, prereq.unit as unit, prereq.grade as grade
                ORDER BY prereq.unit ASC, prereq.concept ASC
                """
                
                prereq_result = run_cypher(prereq_query, {"concept_name": unit_title})
                
                if prereq_result:
                    print(f"   📚 선수개념들 ({len(prereq_result)}개):")
                    for i, prereq in enumerate(prereq_result):
                        print(f"      {i+1}. {prereq['concept']} (단원: {prereq['unit']}, 학년: {prereq['grade']})")
                    
                    print(f"\n   🎯 학습 경로 구성:")
                    print(f"      시작: {unit_title}")
                    print(f"      선수개념: {len(prereq_result)}개")
                    print(f"      총 학습 단계: {len(prereq_result) + 1}단계")
                    
                else:
                    print(f"   ⚠️ 선수개념이 없어서 단일 개념만 학습")
                    
            except Exception as e:
                print(f"   ❌ 학습 경로 생성 오류: {e}")
            
            client.close()
            
        else:
            print(f"❌ MONGODB_URI를 찾을 수 없음")
            
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_real_mapping()
