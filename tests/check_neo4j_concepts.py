#!/usr/bin/env python3
"""Neo4j에 저장된 개념들 확인"""

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'AI', 'app'))

from db.neo4j import run_cypher

def check_neo4j_concepts():
    try:
        print("=== Neo4j에 저장된 개념들 확인 ===")
        
        # 1. 모든 Concept 노드 조회
        print("🔍 1단계: 모든 Concept 노드 조회")
        try:
            query1 = """
            MATCH (c:Concept)
            RETURN c.concept as concept, c.unit as unit, c.grade as grade
            ORDER BY c.unit ASC, c.concept ASC
            LIMIT 20
            """
            
            result1 = run_cypher(query1)
            
            if result1:
                print(f"   ✅ Concept 노드 발견: {len(result1)}개")
                for i, concept in enumerate(result1):
                    print(f"      {i+1}. {concept['concept']} (단원: {concept['unit']}, 학년: {concept['grade']})")
            else:
                print(f"   ⚠️ Concept 노드가 없음")
                
        except Exception as e:
            print(f"   ❌ 쿼리1 오류: {e}")
        
        # 2. PRECEDES 관계가 있는 노드들 조회
        print(f"\n🔍 2단계: PRECEDES 관계가 있는 노드들 조회")
        try:
            query2 = """
            MATCH (c:Concept)-[:PRECEDES]->(other:Concept)
            RETURN c.concept as from_concept, c.unit as from_unit, 
                   other.concept as to_concept, other.unit as to_unit
            ORDER BY c.unit ASC, c.concept ASC
            LIMIT 20
            """
            
            result2 = run_cypher(query2)
            
            if result2:
                print(f"   ✅ PRECEDES 관계 발견: {len(result2)}개")
                for i, rel in enumerate(result2):
                    print(f"      {i+1}. {rel['from_concept']} → {rel['to_concept']}")
            else:
                print(f"   ⚠️ PRECEDES 관계가 없음")
                
        except Exception as e:
            print(f"   ❌ 쿼리2 오류: {e}")
        
        # 3. 특정 개념명으로 검색 (부분 일치)
        print(f"\n🔍 3단계: '좌표'가 포함된 개념 검색")
        try:
            query3 = """
            MATCH (c:Concept)
            WHERE c.concept CONTAINS '좌표'
            RETURN c.concept as concept, c.unit as unit, c.grade as grade
            """
            
            result3 = run_cypher(query3)
            
            if result3:
                print(f"   ✅ '좌표' 포함 개념 발견: {len(result3)}개")
                for i, concept in enumerate(result3):
                    print(f"      {i+1}. {concept['concept']} (단원: {concept['unit']}, 학년: {concept['grade']})")
            else:
                print(f"   ⚠️ '좌표' 포함 개념이 없음")
                
        except Exception as e:
            print(f"   ❌ 쿼리3 오류: {e}")
        
        # 4. 전체 노드 수 확인
        print(f"\n🔍 4단계: 전체 노드 수 확인")
        try:
            query4 = """
            MATCH (n)
            RETURN labels(n) as labels, count(n) as count
            """
            
            result4 = run_cypher(query4)
            
            if result4:
                print(f"   📊 전체 노드 현황:")
                for item in result4:
                    print(f"      {item['labels']}: {item['count']}개")
            else:
                print(f"   ⚠️ 노드 수를 확인할 수 없음")
                
        except Exception as e:
            print(f"   ❌ 쿼리4 오류: {e}")
            
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_neo4j_concepts()
