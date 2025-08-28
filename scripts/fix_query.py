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
    print("=== Neo4j Aura 단원별 개념 수 정확한 확인 ===")
    
    # 1. 단원 정보가 있는 개념들 확인
    query1 = """
    MATCH (c:Concept)
    WHERE c.unit IS NOT NULL AND c.unit <> '' AND c.unit <> 'nan'
    RETURN c.unit as 단원, c.name as 개념명
    ORDER BY c.unit, c.name
    LIMIT 20
    """
    run_query(query1, "1. 단원 정보가 있는 개념들 (20개)")
    
    # 2. 단원별 개념 수 (정확한 버전)
    query2 = """
    MATCH (c:Concept)
    WHERE c.unit IS NOT NULL AND c.unit <> '' AND c.unit <> 'nan'
    RETURN c.unit as 단원, count(c) as 개념수
    ORDER BY c.unit
    """
    run_query(query2, "2. 단원별 개념 수 (정확한 버전)")
    
    # 3. 단원 정보가 없는 개념들 확인
    query3 = """
    MATCH (c:Concept)
    WHERE c.unit IS NULL OR c.unit = '' OR c.unit = 'nan'
    RETURN count(c) as 단원정보없는_개념수
    """
    run_query(query3, "3. 단원 정보가 없는 개념 수")
    
    # 4. 학년별 개념 수
    query4 = """
    MATCH (c:Concept)
    WHERE c.grade IS NOT NULL AND c.grade <> ''
    RETURN c.grade as 학년, count(c) as 개념수
    ORDER BY c.grade
    """
    run_query(query4, "4. 학년별 개념 수")
    
    # 5. 전체 통계
    query5 = """
    MATCH (c:Concept)
    RETURN 
        count(c) as 전체_개념수,
        count(CASE WHEN c.unit IS NOT NULL AND c.unit <> '' AND c.unit <> 'nan' THEN c END) as 단원정보있는_개념수,
        count(CASE WHEN c.unit IS NULL OR c.unit = '' OR c.unit = 'nan' THEN c END) as 단원정보없는_개념수
    """
    run_query(query5, "5. 전체 통계")
    
    driver.close()
    print("\n🎉 단원별 개념 수 정확한 확인 완료!")

if __name__ == "__main__":
    main()
