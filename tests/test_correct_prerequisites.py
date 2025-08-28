#!/usr/bin/env python3
"""올바른 방향으로 선수개념 조회 테스트"""

from AI.app.db.neo4j import run_cypher

def test_correct_prerequisites():
    try:
        print("=== 올바른 방향 선수개념 조회 테스트 ===")
        
        # 테스트할 개념명
        target_concept = "1.5 정수와 유리수의 덧셈, 뺄셈"
        print(f"\n🎯 대상 개념: {target_concept}")
        
        # 1. 올바른 방향: 들어오는 화살표 (선수개념들)
        print(f"\n1️⃣ 올바른 방향: 선수개념 조회 (들어오는 화살표)...")
        prereq_result = run_cypher("""
            MATCH (prereq:Concept)-[:PRECEDES]->(current:Concept {concept: $concept_name})
            RETURN prereq.concept as concept, prereq.unit as unit, prereq.grade as grade
            ORDER BY prereq.unit, prereq.concept
        """, {"concept_name": target_concept})
        
        if prereq_result and isinstance(prereq_result, list) and len(prereq_result) > 0:
            print(f"✅ 선수개념 {len(prereq_result)}개 발견:")
            for i, prereq in enumerate(prereq_result):
                print(f"   {i+1}. {prereq.get('concept', 'N/A')} (단원: {prereq.get('unit', 'N/A')}, 학년: {prereq.get('grade', 'N/A')})")
        else:
            print(f"⚠️ 선수개념이 없음")
            
        # 2. 잘못된 방향: 나가는 화살표 (후속개념들)
        print(f"\n2️⃣ 잘못된 방향: 후속개념 조회 (나가는 화살표)...")
        successor_result = run_cypher("""
            MATCH (current:Concept {concept: $concept_name})-[:PRECEDES]->(successor:Concept)
            RETURN successor.concept as concept, successor.unit as unit, successor.grade as grade
            ORDER BY successor.unit, successor.concept
        """, {"concept_name": target_concept})
        
        if successor_result and isinstance(successor_result, list) and len(successor_result) > 0:
            print(f"✅ 후속개념 {len(successor_result)}개 발견:")
            for i, successor in enumerate(successor_result):
                print(f"   {i+1}. {successor.get('concept', 'N/A')} (단원: {successor.get('unit', 'N/A')}, 학년: {successor.get('grade', 'N/A')})")
        else:
            print(f"⚠️ 후속개념이 없음")
            
        # 3. CSV 파일과 비교 검증
        print(f"\n3️⃣ CSV 파일과 비교 검증...")
        print("CSV에서 확인된 관계:")
        print("   - 1.3 정수와 유리수 → 1.5 정수와 유리수의 덧셈, 뺄셈")
        print("   - 1.4 절댓값 → 1.5 정수와 유리수의 덧셈, 뺄셈")
        print("   - 1.5 정수와 유리수의 덧셈, 뺄셈 → 1.6 정수와 유리수의 곱셈, 나눗셈")
        print("   - 1.5 정수와 유리수의 덧셈, 뺄셈 → 1.12 제곱근의 곱셈과 나눗셈, 분모의 유리화")
        print("   - 1.5 정수와 유리수의 덧셈, 뺄셈 → 1.13 제곱근의 덧셈과 뺄셈")
        
        # 4. 다른 개념으로도 테스트
        print(f"\n4️⃣ 다른 개념으로 테스트: 1.13 제곱근의 덧셈과 뺄셈...")
        test_concept2 = "1.13 제곱근의 덧셈과 뺄셈"
        prereq_result2 = run_cypher("""
            MATCH (prereq:Concept)-[:PRECEDES]->(current:Concept {concept: $concept_name})
            RETURN prereq.concept as concept, prereq.unit as unit, prereq.grade as grade
            ORDER BY prereq.unit, prereq.concept
        """, {"concept_name": test_concept2})
        
        if prereq_result2 and isinstance(prereq_result2, list) and len(prereq_result2) > 0:
            print(f"✅ '{test_concept2}'의 선수개념 {len(prereq_result2)}개 발견:")
            for i, prereq in enumerate(prereq_result2):
                print(f"   {i+1}. {prereq.get('concept', 'N/A')} (단원: {prereq.get('unit', 'N/A')}, 학년: {prereq.get('grade', 'N/A')})")
        else:
            print(f"⚠️ '{test_concept2}'의 선수개념이 없음")
            
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_correct_prerequisites()
