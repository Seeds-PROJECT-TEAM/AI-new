#!/usr/bin/env python3
"""Neo4j의 모든 Concept 노드 찾기"""

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'AI', 'app'))

from db.neo4j import run_cypher

def find_all_neo4j_concepts():
    try:
        print("=== Neo4j의 모든 Concept 노드 찾기 ===")
        
        # 1. 전체 Concept 노드 수 확인
        print("🔍 1단계: 전체 Concept 노드 수 확인")
        try:
            count_query = """
            MATCH (c:Concept)
            RETURN count(c) as total_count
            """
            
            count_result = run_cypher(count_query)
            if count_result:
                total_count = count_result[0]['total_count']
                print(f"   📊 전체 Concept 노드 수: {total_count}개")
            else:
                print(f"   ⚠️ 노드 수를 확인할 수 없음")
                
        except Exception as e:
            print(f"   ❌ 카운트 쿼리 오류: {e}")
        
        # 2. 모든 Concept 노드 조회 (제한 없이)
        print(f"\n🔍 2단계: 모든 Concept 노드 조회")
        try:
            all_concepts_query = """
            MATCH (c:Concept)
            RETURN c.concept as concept, c.unit as unit, c.grade as grade
            ORDER BY c.unit ASC, c.concept ASC
            """
            
            all_concepts = run_cypher(all_concepts_query)
            
            if all_concepts:
                print(f"   ✅ Concept 노드 발견: {len(all_concepts)}개")
                
                # 모든 개념들을 출력
                for i, concept in enumerate(all_concepts):
                    concept_name = concept.get('concept', 'N/A')
                    unit = concept.get('unit', 'N/A')
                    grade = concept.get('grade', 'N/A')
                    print(f"      {i+1:3d}. [{unit}] {concept_name} (학년: {grade})")
                    
                    # 50개마다 구분선 추가
                    if (i + 1) % 50 == 0:
                        print(f"      {'─' * 60}")
                        
            else:
                print(f"   ⚠️ Concept 노드가 없음")
                
        except Exception as e:
            print(f"   ❌ 전체 조회 쿼리 오류: {e}")
        
        # 3. unit별로 그룹화하여 정리
        print(f"\n🔍 3단계: unit별로 그룹화")
        try:
            if all_concepts:
                # unit별로 그룹화
                unit_groups = {}
                for concept in all_concepts:
                    unit = concept.get('unit', 'N/A')
                    if unit not in unit_groups:
                        unit_groups[unit] = []
                    unit_groups[unit].append(concept)
                
                print(f"   📚 unit별 분류:")
                for unit in sorted(unit_groups.keys()):
                    concepts_in_unit = unit_groups[unit]
                    print(f"\n      🔸 {unit} (총 {len(concepts_in_unit)}개):")
                    
                    for concept in concepts_in_unit[:10]:  # 각 unit당 최대 10개만
                        concept_name = concept.get('concept', 'N/A')
                        grade = concept.get('grade', 'N/A')
                        print(f"         • {concept_name} (학년: {grade})")
                    
                    if len(concepts_in_unit) > 10:
                        print(f"         ... 외 {len(concepts_in_unit) - 10}개 더")
                        
        except Exception as e:
            print(f"   ❌ 그룹화 오류: {e}")
        
        # 4. PRECEDES 관계가 있는 노드들 확인
        print(f"\n🔍 4단계: PRECEDES 관계 확인")
        try:
            precedes_query = """
            MATCH (c:Concept)-[:PRECEDES]->(other:Concept)
            RETURN count(*) as relationship_count
            """
            
            precedes_result = run_cypher(precedes_query)
            if precedes_result:
                rel_count = precedes_result[0]['relationship_count']
                print(f"   🔗 PRECEDES 관계 수: {rel_count}개")
                
                # 실제 관계 예시 몇 개 보기
                example_query = """
                MATCH (c:Concept)-[:PRECEDES]->(other:Concept)
                RETURN c.concept as from_concept, c.unit as from_unit,
                       other.concept as to_concept, other.unit as to_unit
                ORDER BY c.unit ASC, c.concept ASC
                LIMIT 10
                """
                
                examples = run_cypher(example_query)
                if examples:
                    print(f"   📝 관계 예시:")
                    for i, example in enumerate(examples):
                        from_concept = example.get('from_concept', 'N/A')
                        to_concept = example.get('to_concept', 'N/A')
                        print(f"      {i+1}. {from_concept} → {to_concept}")
            else:
                print(f"   ⚠️ PRECEDES 관계가 없음")
                
        except Exception as e:
            print(f"   ❌ PRECEDES 관계 확인 오류: {e}")
            
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    find_all_neo4j_concepts()
