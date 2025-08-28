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

def analyze_connections():
    """그래프 연결 구조 분석"""
    print("🔍 그래프 연결 구조 분석 중...")
    
    with driver.session() as session:
        # 1. 전체 통계
        print("\n📊 전체 그래프 통계:")
        result = session.run("MATCH (c:Concept) RETURN count(c) as node_count")
        node_count = result.single()["node_count"]
        
        result = session.run("MATCH ()-[r:PRECEDES]->() RETURN count(r) as relationship_count")
        relationship_count = result.single()["relationship_count"]
        
        print(f"   노드 수: {node_count}")
        print(f"   관계 수: {relationship_count}")
        print(f"   평균 연결 수: {relationship_count / node_count:.1f}")
        
        # 2. 가장 많은 선행개념을 가진 개념 (들어오는 연결이 많은 노드)
        print("\n🔽 가장 많은 선행개념을 가진 개념 (Top 10):")
        result = session.run("""
            MATCH (c:Concept)<-[:PRECEDES]-(pre:Concept)
            RETURN c.concept as 개념, count(pre) as 선행개념수
            ORDER BY 선행개념수 DESC
            LIMIT 10
        """)
        
        for record in result:
            print(f"   {record['개념']}: {record['선행개념수']}개 선행개념")
        
        # 3. 가장 많은 후행개념을 가진 개념 (나가는 연결이 많은 노드)
        print("\n🔼 가장 많은 후행개념을 가진 개념 (Top 10):")
        result = session.run("""
            MATCH (c:Concept)-[:PRECEDES]->(post:Concept)
            RETURN c.concept as 개념, count(post) as 후행개념수
            ORDER BY 후행개념수 DESC
            LIMIT 10
        """)
        
        for record in result:
            print(f"   {record['개념']}: {record['후행개념수']}개 후행개념")
        
        # 4. 연결이 없는 고립된 노드 확인
        print("\n🔍 연결이 없는 고립된 노드:")
        result = session.run("""
            MATCH (c:Concept)
            WHERE NOT (c)-[:PRECEDES]->() AND NOT ()-[:PRECEDES]->(c)
            RETURN c.concept as 개념
        """)
        
        isolated_nodes = list(result)
        if isolated_nodes:
            print(f"   {len(isolated_nodes)}개 고립된 노드 발견:")
            for record in isolated_nodes:
                print(f"     - {record['개념']}")
        else:
            print("   고립된 노드 없음 - 모든 노드가 연결됨")
        
        # 5. 연결 분포 히스토그램
        print("\n📈 연결 수 분포:")
        result = session.run("""
            MATCH (c:Concept)
            OPTIONAL MATCH (c)-[:PRECEDES]->()
            WITH c, count(*) as out_degree
            OPTIONAL MATCH ()-[:PRECEDES]->(c)
            WITH c, out_degree, count(*) as in_degree
            WITH c, out_degree + in_degree as total_degree
            RETURN total_degree, count(*) as node_count
            ORDER BY total_degree
        """)
        
        degree_distribution = {}
        for record in result:
            degree = record['total_degree']
            count = record['node_count']
            degree_distribution[degree] = count
        
        print("   연결 수별 노드 수:")
        for degree in sorted(degree_distribution.keys()):
            print(f"     {degree}개 연결: {degree_distribution[degree]}개 노드")

def show_connection_patterns():
    """연결 패턴 시각화"""
    print("\n🔗 연결 패턴 예시:")
    
    with driver.session() as session:
        # 1. 가장 복잡한 연결을 가진 노드의 실제 연결 구조 보기
        print("\n📊 가장 복잡한 연결을 가진 개념의 구조:")
        result = session.run("""
            MATCH (c:Concept)
            OPTIONAL MATCH (c)-[:PRECEDES]->(post:Concept)
            WITH c, count(post) as out_count
            OPTIONAL MATCH (pre:Concept)-[:PRECEDES]->(c)
            WITH c, out_count, count(pre) as in_count
            RETURN c.concept as 개념, in_count as 선행개념수, out_count as 후행개념수
            ORDER BY in_count + out_count DESC
            LIMIT 1
        """)
        
        top_node = result.single()
        if top_node:
            concept_name = top_node['개념']
            print(f"   선택된 개념: {concept_name}")
            print(f"   선행개념: {top_node['선행개념수']}개, 후행개념: {top_node['후행개념수']}개")
            
            # 이 노드의 실제 연결 구조 보기
            print(f"\n   📍 {concept_name}의 선행개념들:")
            result2 = session.run("""
                MATCH (pre:Concept)-[:PRECEDES]->(c:Concept {concept: $concept})
                RETURN pre.concept as 선행개념
                LIMIT 10
            """, concept=concept_name)
            
            for record in result2:
                print(f"     ← {record['선행개념']}")
            
            print(f"\n   📍 {concept_name}의 후행개념들:")
            result3 = session.run("""
                MATCH (c:Concept {concept: $concept})-[:PRECEDES]->(post:Concept)
                RETURN post.concept as 후행개념
                LIMIT 10
            """, concept=concept_name)
            
            for record in result3:
                print(f"     → {record['후행개념']}")
        
        # 2. 순차적 체인이 아닌 복잡한 네트워크 구조 보기
        print("\n🕸️ 복잡한 네트워크 구조 예시:")
        result = session.run("""
            MATCH (c:Concept)-[:PRECEDES]->(post:Concept)
            WHERE c.concept = '1.3 정수와 유리수'
            RETURN c.concept as 시작개념, post.concept as 후행개념
            LIMIT 5
        """)
        
        print("   '1.3 정수와 유리수'에서 시작하는 경로들:")
        for record in result:
            print(f"     {record['시작개념']} → {record['후행개념']}")

def main():
    print("🔍 Neo4j 그래프 연결 구조 분석!")
    print("=" * 60)
    
    try:
        analyze_connections()
        show_connection_patterns()
        print("\n🎉 분석 완료!")
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        driver.close()
        print("🔌 Neo4j 연결 종료")

if __name__ == "__main__":
    main()
