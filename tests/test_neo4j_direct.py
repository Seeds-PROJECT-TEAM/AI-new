#!/usr/bin/env python3
"""Neo4j에서 직접 선수개념 확인 테스트"""

from AI.app.db.neo4j import run_cypher

def test_neo4j_direct():
    try:
        print("=== Neo4j 직접 선수개념 확인 테스트 ===")
        
        # 테스트할 개념명 (MongoDB와 매칭되어야 할 개념)
        target_concept = "1.5 정수와 유리수의 덧셈, 뺄셈"
        print(f"\n🎯 대상 개념: {target_concept}")
        
        # 1. 해당 개념이 존재하는지 확인
        print("\n1️⃣ 개념 존재 여부 확인...")
        existence_check = run_cypher("""
            MATCH (c:Concept {concept: $concept_name})
            RETURN c.concept as concept, c.unit as unit, c.grade as grade
        """, {"concept_name": target_concept})
        
        if existence_check and isinstance(existence_check, list) and len(existence_check) > 0:
            concept_info = existence_check[0]
            print(f"✅ 개념 존재:")
            print(f"   - concept: {concept_info.get('concept', 'N/A')}")
            print(f"   - unit: {concept_info.get('unit', 'N/A')}")
            print(f"   - grade: {concept_info.get('grade', 'N/A')}")
            
            # 2. 해당 개념의 선수개념 조회
            print(f"\n2️⃣ 선수개념 조회 (PRECEDES 관계)...")
            prereq_result = run_cypher("""
                MATCH (current:Concept {concept: $concept_name})-[:PRECEDES*1..5]->(prereq:Concept)
                RETURN DISTINCT prereq.concept as concept, prereq.unit as unit, prereq.grade as grade
                ORDER BY prereq.unit, prereq.concept
            """, {"concept_name": target_concept})
            
            if prereq_result and isinstance(prereq_result, list) and len(prereq_result) > 0:
                print(f"✅ 선수개념 {len(prereq_result)}개 발견:")
                for i, prereq in enumerate(prereq_result):
                    print(f"   {i+1}. {prereq.get('concept', 'N/A')} (단원: {prereq.get('unit', 'N/A')}, 학년: {prereq.get('grade', 'N/A')})")
            else:
                print(f"⚠️ 선수개념이 없음")
                
                # 3. 해당 개념이 다른 개념의 선수개념인지 확인
                print(f"\n3️⃣ 이 개념이 다른 개념의 선수개념인지 확인...")
                successor_result = run_cypher("""
                    MATCH (current:Concept)-[:PRECEDES]->(successor:Concept {concept: $concept_name})
                    RETURN current.concept as concept, current.unit as unit, current.grade as grade
                    LIMIT 3
                """, {"concept_name": target_concept})
                
                if successor_result and isinstance(successor_result, list) and len(successor_result) > 0:
                    print(f"✅ 이 개념을 선수개념으로 하는 개념들:")
                    for i, successor in enumerate(successor_result):
                        print(f"   {i+1}. {successor.get('concept', 'N/A')} (단원: {successor.get('unit', 'N/A')}, 학년: {successor.get('grade', 'N/A')}")
                else:
                    print(f"⚠️ 이 개념을 선수개념으로 하는 개념도 없음")
                    
        else:
            print(f"❌ 개념이 Neo4j에 존재하지 않음: {target_concept}")
            
            # 4. 유사한 개념들 검색
            print(f"\n4️⃣ 유사한 개념들 검색...")
            similar_concepts = run_cypher("""
                MATCH (c:Concept)
                WHERE c.concept CONTAINS $keyword1 OR c.concept CONTAINS $keyword2
                RETURN c.concept as concept, c.unit as unit, c.grade as grade
                ORDER BY c.grade, c.unit
                LIMIT 10
            """, {"keyword1": "덧셈", "keyword2": "뺄셈"})
            
            if similar_concepts and isinstance(similar_concepts, list) and len(similar_concepts) > 0:
                print(f"✅ '덧셈' 또는 '뺄셈'이 포함된 개념들:")
                for i, concept in enumerate(similar_concepts):
                    print(f"   {i+1}. {concept.get('concept', 'N/A')} (단원: {concept.get('unit', 'N/A')}, 학년: {concept.get('grade', 'N/A')}")
            else:
                print("❌ '덧셈' 또는 '뺄셈'이 포함된 개념도 없음")
                
        # 5. 전체 Concept 노드 수와 샘플 확인
        print(f"\n5️⃣ 전체 Concept 노드 현황...")
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
                ORDER BY c.unit, c.concept
                LIMIT 5
            """)
            
            if sample_concepts and isinstance(sample_concepts, list) and len(sample_concepts) > 0:
                print(f"✅ 샘플 Concept 노드들:")
                for i, concept in enumerate(sample_concepts):
                    print(f"   {i+1}. {concept.get('concept', 'N/A')} (단원: {concept.get('unit', 'N/A')}, 학년: {concept.get('grade', 'N/A')}")
        else:
            print("❌ 전체 Concept 노드 수를 확인할 수 없음")
            
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_neo4j_direct()
