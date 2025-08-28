#!/usr/bin/env python3
"""1.5와 1.6의 선수개념들을 직접 확인하는 테스트"""

from AI.app.db.neo4j import run_cypher

def test_1_5_1_6_prerequisites():
    try:
        print("=== 1.5와 1.6의 선수개념 직접 확인 테스트 ===")
        
        # 1. 1.5 정수와 유리수의 덧셈, 뺄셈의 선수개념들
        print(f"\n1️⃣ 1.5 정수와 유리수의 덧셈, 뺄셈의 선수개념들...")
        prereq_1_5 = run_cypher("""
            MATCH (prereq:Concept)-[:PRECEDES]->(current:Concept {concept: '1.5 정수와 유리수의 덧셈, 뺄셈'})
            RETURN DISTINCT prereq.concept as concept, prereq.unit as unit, prereq.grade as grade
            ORDER BY prereq.unit, prereq.concept
        """)
        
        if prereq_1_5 and isinstance(prereq_1_5, list) and len(prereq_1_5) > 0:
            print(f"✅ 1.5 정수와 유리수의 덧셈, 뺄셈의 선수개념 {len(prereq_1_5)}개 발견:")
            for i, prereq in enumerate(prereq_1_5):
                print(f"   {i+1}. {prereq.get('concept', 'N/A')} (단원: {prereq.get('unit', 'N/A')}, 학년: {prereq.get('grade', 'N/A')}")
        else:
            print(f"⚠️ 1.5 정수와 유리수의 덧셈, 뺄셈의 선수개념이 없음")
            
        # 2. 1.6 정수와 유리수의 곱셈, 나눗셈의 선수개념들
        print(f"\n2️⃣ 1.6 정수와 유리수의 곱셈, 나눗셈의 선수개념들...")
        prereq_1_6 = run_cypher("""
            MATCH (prereq:Concept)-[:PRECEDES]->(current:Concept {concept: '1.6 정수와 유리수의 곱셈, 나눗셈'})
            RETURN DISTINCT prereq.concept as concept, prereq.unit as unit, prereq.grade as grade
            ORDER BY prereq.unit, prereq.concept
        """)
        
        if prereq_1_6 and isinstance(prereq_1_6, list) and len(prereq_1_6) > 0:
            print(f"✅ 1.6 정수와 유리수의 곱셈, 나눗셈의 선수개념 {len(prereq_1_6)}개 발견:")
            for i, prereq in enumerate(prereq_1_6):
                print(f"   {i+1}. {prereq.get('concept', 'N/A')} (단원: {prereq.get('unit', 'N/A')}, 학년: {prereq.get('grade', 'N/A')}")
        else:
            print(f"⚠️ 1.6 정수와 유리수의 곱셈, 나눗셈의 선수개념이 없음")
            
        # 3. 1.5와 1.6이 다른 개념의 선수개념인지 확인
        print(f"\n3️⃣ 1.5와 1.6이 다른 개념의 선수개념인지 확인...")
        
        # 1.5가 선수개념인 개념들
        successors_1_5 = run_cypher("""
            MATCH (current:Concept {concept: '1.5 정수와 유리수의 덧셈, 뺄셈'})-[:PRECEDES]->(successor:Concept)
            RETURN successor.concept as concept, successor.unit as unit, successor.grade as grade
            ORDER BY successor.unit, successor.concept
            LIMIT 10
        """)
        
        if successors_1_5 and isinstance(successors_1_5, list) and len(successors_1_5) > 0:
            print(f"✅ 1.5 정수와 유리수의 덧셈, 뺄셈을 선수개념으로 하는 개념들:")
            for i, successor in enumerate(successors_1_5):
                print(f"   {i+1}. {successor.get('concept', 'N/A')} (단원: {successor.get('unit', 'N/A')}, 학년: {successor.get('grade', 'N/A')}")
        else:
            print(f"⚠️ 1.5 정수와 유리수의 덧셈, 뺄셈을 선수개념으로 하는 개념이 없음")
            
        # 1.6이 선수개념인 개념들
        successors_1_6 = run_cypher("""
            MATCH (current:Concept {concept: '1.6 정수와 유리수의 곱셈, 나눗셈'})-[:PRECEDES]->(successor:Concept)
            RETURN successor.concept as concept, successor.unit as unit, successor.grade as grade
            ORDER BY successor.unit, successor.concept
            LIMIT 10
        """)
        
        if successors_1_6 and isinstance(successors_1_6, list) and len(successors_1_6) > 0:
            print(f"✅ 1.6 정수와 유리수의 곱셈, 나눗셈을 선수개념으로 하는 개념들:")
            for i, successor in enumerate(successors_1_6):
                print(f"   {i+1}. {successor.get('concept', 'N/A')} (단원: {successor.get('unit', 'N/A')}, 학년: {successor.get('grade', 'N/A')}")
        else:
            print(f"⚠️ 1.6 정수와 유리수의 곱셈, 나눗셈을 선수개념으로 하는 개념이 없음")
            
        # 4. 전체적인 관계 구조 확인
        print(f"\n4️⃣ 1.5와 1.6 주변의 관계들...")
        
        # 1.5와 1.6 주변의 관계들
        relationships = run_cypher("""
            MATCH (n1:Concept)-[:PRECEDES]->(n2:Concept)
            WHERE n1.concept IN ['1.5 정수와 유리수의 덧셈, 뺄셈', '1.6 정수와 유리수의 곱셈, 나눗셈'] 
               OR n2.concept IN ['1.5 정수와 유리수의 덧셈, 뺄셈', '1.6 정수와 유리수의 곱셈, 나눗셈']
            RETURN n1.concept as from_concept, n2.concept as to_concept, 
                   n1.unit as from_unit, n2.unit as to_unit
            ORDER BY n1.concept, n2.concept
        """)
        
        if relationships and isinstance(relationships, list) and len(relationships) > 0:
            print(f"✅ 1.5와 1.6 주변의 관계들:")
            for i, rel in enumerate(relationships):
                print(f"   {i+1}. {rel.get('from_concept', 'N/A')} → {rel.get('to_concept', 'N/A')}")
                print(f"      ({rel.get('from_unit', 'N/A')} → {rel.get('to_unit', 'N/A')}")
        else:
            print(f"⚠️ 1.5와 1.6 주변의 관계를 찾을 수 없음")
            
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_1_5_1_6_prerequisites()
