#!/usr/bin/env python3
"""Neo4j 선수개념 조회 테스트"""

from AI.app.db.neo4j import run_cypher

def test_neo4j_prerequisites():
    try:
        print("=== Neo4j 선수개념 조회 테스트 ===")
        
        # MongoDB에서 가져온 개념명으로 테스트
        concept_name = "덧셈과 뺄셈"
        print(f"\n🔍 개념 '{concept_name}'의 선수개념 조회 시도...")
        
        # PRECEDES 관계로 선수개념들 조회 (path() 함수 제거)
        result = run_cypher("""
            MATCH (current:Concept {concept: $concept_name})-[:PRECEDES*1..5]->(prereq:Concept)
            RETURN DISTINCT prereq.concept as concept, prereq.unit as unit, 
                   prereq.grade as grade
            ORDER BY prereq.unit, prereq.concept
        """, {"concept_name": concept_name})
        
        if result and isinstance(result, list) and len(result) > 0:
            print(f"✅ Neo4j에서 선수개념 {len(result)}개 발견:")
            for i, prereq in enumerate(result):
                print(f"   {i+1}. {prereq.get('concept', 'N/A')} (단원: {prereq.get('unit', 'N/A')}, 학년: {prereq.get('grade', 'N/A')})")
        else:
            print(f"⚠️ Neo4j에서 선수개념을 찾을 수 없음: {concept_name}")
            
            # 해당 개념이 Neo4j에 존재하는지 확인
            print(f"\n🔍 개념 '{concept_name}'이 Neo4j에 존재하는지 확인...")
            existence_check = run_cypher("""
                MATCH (c:Concept {concept: $concept_name})
                RETURN c.concept as concept, c.unit as unit, c.grade as grade
            """, {"concept_name": concept_name})
            
            if existence_check and isinstance(existence_check, list) and len(existence_check) > 0:
                concept_exists = existence_check[0]
                print(f"✅ 개념 존재: {concept_exists}")
            else:
                print(f"❌ 개념이 Neo4j에 존재하지 않음: {concept_name}")
                
                # 유사한 개념들 검색
                print(f"\n🔍 유사한 개념들 검색...")
                similar_concepts = run_cypher("""
                    MATCH (c:Concept)
                    WHERE c.concept CONTAINS $keyword OR c.unit CONTAINS $keyword
                    RETURN c.concept as concept, c.unit as unit, c.grade as grade
                    LIMIT 5
                """, {"keyword": "덧셈"})
                
                if similar_concepts and isinstance(similar_concepts, list) and len(similar_concepts) > 0:
                    print(f"✅ 유사한 개념들:")
                    for concept in similar_concepts:
                        print(f"   - {concept.get('concept', 'N/A')} (단원: {concept.get('unit', 'N/A')}, 학년: {concept.get('grade', 'N/A')})")
                else:
                    print("❌ 유사한 개념도 없음")
                    
                # 전체 Concept 노드 수 확인
                print(f"\n🔍 전체 Concept 노드 수 확인...")
                total_concepts = run_cypher("""
                    MATCH (c:Concept)
                    RETURN count(c) as total
                """)
                
                if total_concepts and isinstance(total_concepts, list) and len(total_concepts) > 0:
                    total = total_concepts[0].get('total', 0)
                    print(f"✅ 전체 Concept 노드 수: {total}")
                    
                    # 샘플 Concept 노드들 확인
                    sample_concepts = run_cypher("""
                        MATCH (c:Concept)
                        RETURN c.concept as concept, c.unit as unit, c.grade as grade
                        LIMIT 3
                    """)
                    
                    if sample_concepts and isinstance(sample_concepts, list) and len(sample_concepts) > 0:
                        print(f"✅ 샘플 Concept 노드들:")
                        for concept in sample_concepts:
                            print(f"   - {concept.get('concept', 'N/A')} (단원: {concept.get('unit', 'N/A')}, 학년: {concept.get('grade', 'N/A')})")
                else:
                    print("❌ 전체 Concept 노드 수를 확인할 수 없음")
            
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_neo4j_prerequisites()
