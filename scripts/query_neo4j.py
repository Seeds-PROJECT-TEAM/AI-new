import os
from pathlib import Path
from dotenv import load_dotenv
from neo4j import GraphDatabase

# AI/.env 파일 로드
env_path = Path(__file__).resolve().parents[1] / ".env"
if env_path.exists():
    load_dotenv(env_path)
    print(f"✅ .env 파일 로드됨: {env_path}")

# Neo4j 연결
AURA_URI = os.getenv("AURA_URI")
AURA_USER = os.getenv("AURA_USER")
AURA_PASS = os.getenv("AURA_PASS")

driver = GraphDatabase.driver(AURA_URI, auth=(AURA_USER, AURA_PASS))

def run_query(query, description):
    """쿼리 실행 및 결과 출력"""
    print(f"\n=== {description} ===")
    print(f"쿼리: {query}")
    print("-" * 50)
    
    try:
        with driver.session() as session:
            result = session.run(query)
            records = list(result)
            
            if not records:
                print("결과: 데이터 없음")
                return
            
            # 첫 번째 레코드의 키들을 헤더로 사용
            if records:
                headers = list(records[0].keys())
                print(f"컬럼: {' | '.join(headers)}")
                print("-" * 50)
                
                for i, record in enumerate(records):
                    values = [str(record[key]) for key in headers]
                    print(f"{i+1:2d}. {' | '.join(values)}")
                    
                    # 10개까지만 출력
                    if i >= 9:
                        print("... (더 많은 결과가 있습니다)")
                        break
                        
    except Exception as e:
        print(f"❌ 쿼리 실행 오류: {e}")

def main():
    print("=== Neo4j Aura 데이터 확인 시작 ===")
    
    # 1. 개념 노드 조회 (10개)
    query1 = """
    MATCH (c:Concept) 
    RETURN c.name as 개념명, c.unit as 단원, c.grade as 학년
    LIMIT 10
    """
    run_query(query1, "1. 개념 노드 조회 (10개)")
    
    # 2. 선행관계 확인 (10개)
    query2 = """
    MATCH (src:Concept)-[:PRECEDES]->(dst:Concept) 
    RETURN src.name as 선행개념, dst.name as 후행개념
    LIMIT 10
    """
    run_query(query2, "2. 선행관계 확인 (10개)")
    
    # 3. 노드 수 확인
    query3 = """
    MATCH (c:Concept) 
    RETURN count(c) as 개념노드_총개수
    """
    run_query(query3, "3. 노드 수 확인")
    
    # 4. 관계 수 확인
    query4 = """
    MATCH ()-[r:PRECEDES]->() 
    RETURN count(r) as 선행관계_총개수
    """
    run_query(query4, "4. 관계 수 확인")
    
    # 5. 추가 정보: 단원별 개념 수
    query5 = """
    MATCH (c:Concept)
    WHERE c.unit IS NOT NULL AND c.unit <> ''
    RETURN c.unit as 단원, count(c) as 개념수
    ORDER BY 개념수 DESC
    LIMIT 10
    """
    run_query(query5, "5. 단원별 개념 수 (상위 10개)")
    
    driver.close()
    print("\n🎉 Neo4j Aura 데이터 확인 완료!")

if __name__ == "__main__":
    main()
