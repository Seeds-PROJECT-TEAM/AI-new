#!/usr/bin/env python3
"""진단 서비스 디버깅 스크립트"""

from AI.app.services.mongo_service import MongoService
from AI.app.db.neo4j import run_cypher

def debug_diagnostic_logic():
    try:
        print("=== 진단 서비스 디버깅 ===")
        
        # MongoDB 서비스 초기화
        mongo_service = MongoService()
        print(f"MongoDB 연결 상태: {mongo_service.is_connected}")
        
        if not mongo_service.is_connected:
            print("❌ MongoDB에 연결할 수 없습니다.")
            return
        
        # 테스트용 문제 ID
        problem_id = "problem_001"
        print(f"\n🔍 문제 ID '{problem_id}'로 진단 로직 테스트...")
        
        # 1. MongoDB에서 문제 정보 조회
        print("\n1️⃣ MongoDB에서 문제 정보 조회...")
        problems_collection = mongo_service._db.problems
        problem = problems_collection.find_one({"problem_id": problem_id})
        
        if problem:
            print(f"✅ 문제 찾음:")
            print(f"   - problem_id: {problem.get('problem_id')}")
            print(f"   - unitId: {problem.get('unitId')}")
            print(f"   - grade: {problem.get('grade')}")
            print(f"   - chapter: {problem.get('chapter')}")
            
            # 2. unitId로 단원 정보 조회
            unit_id = problem.get('unitId')
            if unit_id:
                print(f"\n2️⃣ 단원 ID '{unit_id}'로 단원 정보 조회...")
                units_collection = mongo_service._db.units
                unit = units_collection.find_one({"_id": unit_id})
                
                if unit:
                    print(f"✅ 단원 정보 찾음:")
                    print(f"   - unitId: {unit.get('unitId')}")
                    print(f"   - title.ko: {unit.get('title', {}).get('ko', 'N/A')}")
                    print(f"   - chapterTitle: {unit.get('chapterTitle', 'N/A')}")
                    print(f"   - grade: {unit.get('grade')}")
                    
                    # 3. Neo4j에서 해당 개념의 선수개념 조회
                    concept_name = unit.get('title', {}).get('ko', '')
                    if concept_name:
                        print(f"\n3️⃣ Neo4j에서 개념 '{concept_name}'의 선수개념 조회...")
                        
                        # 정확한 매칭 시도
                        result = run_cypher("""
                            MATCH (current:Concept {concept: $concept_name})-[:PRECEDES*1..5]->(prereq:Concept)
                            RETURN DISTINCT prereq.concept as concept, prereq.unit as unit
                            ORDER BY unit, concept
                        """, {"concept_name": concept_name})
                        
                        if result and isinstance(result, list) and len(result) > 0:
                            print(f"✅ 정확한 매칭으로 선수개념 {len(result)}개 발견:")
                            for i, prereq in enumerate(result):
                                print(f"   {i+1}. {prereq.get('concept', 'N/A')}")
                        else:
                            print(f"⚠️ 정확한 매칭 실패, 유사한 개념명으로 검색 시도...")
                            
                            # 유사한 개념명으로 검색
                            similar_result = run_cypher("""
                                MATCH (current:Concept)
                                WHERE current.concept CONTAINS $concept_name OR $concept_name CONTAINS current.concept
                                RETURN current.concept as concept, current.unit as unit
                                LIMIT 1
                            """, {"concept_name": concept_name})
                            
                            if similar_result and isinstance(similar_result, list) and len(similar_result) > 0:
                                similar_concept = similar_result[0]
                                neo4j_concept_name = similar_concept.get("concept", "")
                                print(f"✅ 유사한 개념 발견: {concept_name} -> {neo4j_concept_name}")
                                
                                # 찾은 Neo4j 개념명으로 선수개념 조회
                                prereq_result = run_cypher("""
                                    MATCH (current:Concept {concept: $concept_name})-[:PRECEDES*1..5]->(prereq:Concept)
                                    RETURN DISTINCT prereq.concept as concept, prereq.unit as unit
                                    ORDER BY unit, concept
                                """, {"concept_name": neo4j_concept_name})
                                
                                if prereq_result and isinstance(prereq_result, list) and len(prereq_result) > 0:
                                    print(f"✅ 유사한 매칭으로 선수개념 {len(prereq_result)}개 발견:")
                                    for i, prereq in enumerate(prereq_result):
                                        print(f"   {i+1}. {prereq.get('concept', 'N/A')}")
                                else:
                                    print(f"❌ 유사한 매칭으로도 선수개념을 찾을 수 없음")
                            else:
                                print(f"❌ 유사한 개념도 찾을 수 없음")
                    else:
                        print("❌ 단원에서 개념명을 추출할 수 없음")
                else:
                    print(f"❌ unitId '{unit_id}'에 해당하는 단원을 찾을 수 없음")
            else:
                print("❌ 문제에 unitId가 없음")
        else:
            print(f"❌ problem_id '{problem_id}'에 해당하는 문제를 찾을 수 없음")
            
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_diagnostic_logic()
