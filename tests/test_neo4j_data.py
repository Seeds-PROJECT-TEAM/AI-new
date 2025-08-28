#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'AI'))

from AI.app.services.diagnostic_service import run_cypher

def test_neo4j_concepts():
    """Neo4j에서 개념 데이터 조회 테스트"""
    
    print("=== Neo4j 개념 데이터 조회 테스트 ===")
    
    # 1. 기본 개념 조회
    print("\n1. 기본 개념 조회:")
    result = run_cypher("MATCH (c:Concept) RETURN c.concept as concept, c.unit as unit, c.grade as grade LIMIT 5")
    for r in result:
        print(f"  - {r.get('concept', 'N/A')} | {r.get('unit', 'N/A')} | {r.get('grade', 'N/A')}")
    
    # 2. 정수와 유리수 관련 개념 조회
    print("\n2. '정수와 유리수' 관련 개념 조회:")
    result = run_cypher("MATCH (c:Concept) WHERE c.concept CONTAINS '정수' OR c.concept CONTAINS '유리수' RETURN c.concept as concept, c.unit as unit, c.grade as grade LIMIT 3")
    for r in result:
        print(f"  - {r.get('concept', 'N/A')} | {r.get('unit', 'N/A')} | {r.get('grade', 'N/A')}")
    
    # 3. 선행 관계 조회
    print("\n3. 선행 관계 조회:")
    result = run_cypher("MATCH (c:Concept)-[:PRECEDES]->(prereq:Concept) RETURN c.concept as concept, prereq.concept as prereq_concept LIMIT 3")
    for r in result:
        print(f"  - {r.get('concept', 'N/A')} -> {r.get('prereq_concept', 'N/A')}")
    
    # 4. 총 노드 수 확인
    print("\n4. 총 노드 수:")
    result = run_cypher("MATCH (n) RETURN count(n) as total")
    if result:
        print(f"  총 노드 수: {result[0].get('total', 0)}")

if __name__ == "__main__":
    test_neo4j_concepts()
