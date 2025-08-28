#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Neo4j에 있는 실제 단원들과 개념들을 확인하기
"""

import os
from neo4j import GraphDatabase
from dotenv import load_dotenv

# AI 폴더의 .env 파일 로드
load_dotenv('AI/.env')

def check_neo4j_units():
    try:
        # Neo4j 연결 (Aura 환경 변수 사용)
        uri = os.getenv('AURA_URI')
        username = os.getenv('AURA_USER')
        password = os.getenv('AURA_PASS')
        
        if not all([uri, username, password]):
            print("❌ Neo4j 환경 변수 누락")
            return
        
        driver = GraphDatabase.driver(uri, auth=(username, password))
        
        with driver.session() as session:
            print("=== Neo4j 단원 및 개념 정보 ===\n")
            
            # 1. 모든 Concept 노드 조회
            print("🔍 모든 Concept 노드:")
            result = session.run("MATCH (c:Concept) RETURN c.concept as concept, c.unit as unit, c.grade as grade LIMIT 20")
            concepts = []
            for record in result:
                concept = record["concept"]
                unit = record["unit"]
                grade = record["grade"]
                concepts.append((concept, unit, grade))
                print(f"  📚 {concept} | {unit} | {grade}")
            
            print(f"\n총 {len(concepts)}개의 개념 발견\n")
            
            # 2. 단원별로 그룹화
            print("📊 단원별 개념 분포:")
            unit_concepts = {}
            for concept, unit, grade in concepts:
                if unit not in unit_concepts:
                    unit_concepts[unit] = []
                unit_concepts[unit].append(concept)
            
            for unit, concept_list in unit_concepts.items():
                print(f"  🎯 {unit}: {len(concept_list)}개 개념")
                for concept in concept_list[:3]:  # 최대 3개만
                    print(f"    - {concept}")
                if len(concept_list) > 3:
                    print(f"    ... 외 {len(concept_list) - 3}개")
                print()
            
            # 3. 선수개념 관계 확인
            print("🔗 선수개념 관계:")
            result = session.run("MATCH (c:Concept)-[:REQUIRES]->(prereq:Concept) RETURN c.concept as concept, c.unit as unit, prereq.concept as prereq_concept, prereq.unit as prereq_unit LIMIT 15")
            
            relationships = []
            for record in result:
                concept = record["concept"]
                unit = record["unit"]
                prereq_concept = record["prereq_concept"]
                prereq_unit = record["prereq_unit"]
                relationships.append((concept, unit, prereq_concept, prereq_unit))
                print(f"  📚 {concept} ({unit}) → {prereq_concept} ({prereq_unit})")
            
            print(f"\n총 {len(relationships)}개의 선수개념 관계 발견")
            
            # 4. 진단테스트용 문제 ID 추천
            print("\n🎯 진단테스트용 문제 ID 추천:")
            if concepts:
                print("  추천 문제 ID들:")
                for i, (concept, unit, grade) in enumerate(concepts[:10], 1):
                    print(f"    {i}. {concept} ({unit})")
            
        driver.close()
        print("\n✅ Neo4j 조회 완료!")
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_neo4j_units()
