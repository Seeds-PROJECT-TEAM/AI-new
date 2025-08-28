#!/usr/bin/env python3
"""Neo4j 1.x 시리즈 개념들로 선수개념 조회 테스트"""

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'AI', 'app'))

from db.neo4j import run_cypher

def test_1x_concepts():
    try:
        print("=== Neo4j 1.x 시리즈 개념들로 선수개념 조회 테스트 ===")
        
        # 1.x 시리즈 개념들로 테스트
        test_concepts = [
            "1.3 정수와 유리수",
            "1.4 절댓값", 
            "1.5 정수와 유리수의 덧셈, 뺄셈",
            "1.6 정수와 유리수의 곱셈, 나눗셈"
        ]
        
        print("🔍 테스트할 1.x 시리즈 개념들:")
        for concept in test_concepts:
            print(f"   📄 {concept}")
        
        print(f"\n🔍 각 개념의 선수개념 조회:")
        
        for concept_name in test_concepts:
            print(f"\n📝 테스트: {concept_name}")
            
            try:
                # 선수개념 조회
                query = """
                MATCH (prereq:Concept)-[:PRECEDES]->(current:Concept {concept: $concept_name})
                RETURN DISTINCT prereq.concept as concept, prereq.unit as unit, prereq.grade as grade
                ORDER BY prereq.unit ASC, prereq.concept ASC
                """
                
                params = {"concept_name": concept_name}
                result = run_cypher(query, params)
                
                if result:
                    print(f"   ✅ 선수개념 발견: {len(result)}개")
                    for i, prereq in enumerate(result[:10]):  # 처음 10개만
                        print(f"      {i+1}. {prereq['concept']} (단원: {prereq['unit']}, 학년: {prereq['grade']})")
                    if len(result) > 10:
                        print(f"      ... 외 {len(result)-10}개 더")
                        
                    # 학습 경로 구성
                    print(f"   🎯 학습 경로 구성:")
                    print(f"      시작: {concept_name}")
                    print(f"      선수개념: {len(result)}개")
                    print(f"      총 학습 단계: {len(result) + 1}단계")
                    
                else:
                    print(f"   ⚠️ 선수개념 없음")
                    
            except Exception as e:
                print(f"   ❌ 쿼리 오류: {e}")
        
        print(f"\n🔍 학습 경로 생성 시나리오:")
        print("   Express에서 problemId를 보내면:")
        print("   1. MongoDB에서 unitId 조회")
        print("   2. Neo4j에서 해당 개념의 선수개념 조회")
        print("   3. 선수개념 + 현재 개념으로 학습 경로 구성")
        print("   4. 순서대로 정렬하여 맞춤형 학습 경로 제공")
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_1x_concepts()
