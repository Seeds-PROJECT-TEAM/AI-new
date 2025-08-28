#!/usr/bin/env python3
"""
Neo4j 연결 상태 확인
"""

import os
from dotenv import load_dotenv

# AI 폴더의 .env 파일 로드
env_path = os.path.join(os.path.dirname(__file__), "AI", ".env")
load_dotenv(env_path)

def test_neo4j_connection():
    """Neo4j 연결 상태 확인"""
    
    print("=== Neo4j 연결 상태 확인 ===")
    
    # 환경 변수 확인
    aura_uri = os.getenv("AURA_URI")
    aura_user = os.getenv("AURA_USER")
    aura_pass = os.getenv("AURA_PASS")
    
    print(f"AURA_URI: {'설정됨' if aura_uri else '설정 안됨'}")
    print(f"AURA_USER: {'설정됨' if aura_user else '설정 안됨'}")
    print(f"AURA_PASS: {'설정됨' if aura_pass else '설정 안됨'}")
    
    if not all([aura_uri, aura_user, aura_pass]):
        print("❌ Neo4j 환경 변수가 완전히 설정되지 않음")
        return False
    
    try:
        # Neo4j 연결 테스트
        from neo4j import GraphDatabase
        
        driver = GraphDatabase.driver(aura_uri, auth=(aura_user, aura_pass))
        
        # 연결 테스트
        with driver.session() as session:
            result = session.run("RETURN 1 as test")
            record = result.single()
            
            if record and record["test"] == 1:
                print("✅ Neo4j 연결 성공!")
                
                # 노드 수 확인
                node_count = session.run("MATCH (n) RETURN count(n) as count").single()
                print(f"📊 총 노드 수: {node_count['count']}")
                
                # 개념 노드 확인
                concept_count = session.run("MATCH (n:Concept) RETURN count(n) as count").single()
                print(f"📚 개념 노드 수: {concept_count['count']}")
                
                # 관계 확인
                rel_count = session.run("MATCH ()-[r]->() RETURN count(r) as count").single()
                print(f"🔗 총 관계 수: {rel_count['count']}")
                
                driver.close()
                return True
            else:
                print("❌ Neo4j 연결 테스트 실패")
                return False
                
    except Exception as e:
        print(f"❌ Neo4j 연결 실패: {e}")
        return False

if __name__ == "__main__":
    test_neo4j_connection()
