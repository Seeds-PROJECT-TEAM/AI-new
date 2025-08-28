import os
from pathlib import Path
from dotenv import load_dotenv
from neo4j import GraphDatabase
import pandas as pd

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

def clear_database():
    """기존 데이터베이스 내용 완전 삭제"""
    print("🗑️ 기존 데이터베이스 내용 삭제 중...")
    
    with driver.session() as session:
        # 모든 노드와 관계 삭제
        session.run("MATCH (n) DETACH DELETE n")
        print("✅ 모든 노드와 관계 삭제 완료")

def create_constraints():
    """Neo4j 제약조건 생성"""
    print("🔒 제약조건 생성 중...")
    
    with driver.session() as session:
        try:
            # Concept 노드의 concept 속성에 고유 제약조건 생성
            session.run("CREATE CONSTRAINT concept_concept_unique IF NOT EXISTS FOR (c:Concept) REQUIRE c.concept IS UNIQUE")
            print("✅ concept 속성 고유 제약조건 생성 완료")
        except Exception as e:
            print(f"⚠️ 제약조건 생성 중 오류 (이미 존재할 수 있음): {e}")

def load_nodes():
    """노드 데이터 로드"""
    print("📊 노드 데이터 로드 중...")
    
    # CSV 파일 경로
    nodes_file = Path(__file__).resolve().parents[1] / "data" / "neo4j_nodes.csv"
    
    if not nodes_file.exists():
        print(f"❌ 노드 파일을 찾을 수 없음: {nodes_file}")
        return
    
    # CSV 파일 읽기 (한글 인코딩 처리)
    try:
        df = pd.read_csv(nodes_file, encoding='utf-8')
    except UnicodeDecodeError:
        try:
            df = pd.read_csv(nodes_file, encoding='cp949')
        except UnicodeDecodeError:
            df = pd.read_csv(nodes_file, encoding='euc-kr')
    
    print(f"📁 노드 파일 읽기 완료: {len(df)}개 행")
    
    # 데이터 확인
    print(f"📋 컬럼: {list(df.columns)}")
    print(f"📊 처음 3행:")
    print(df.head(3))
    
    with driver.session() as session:
        # Concept 노드 생성
        for index, row in df.iterrows():
            concept_name = row['concept']
            unit = row['unit']
            grade = row['grade']
            
            # NaN 값 처리
            if pd.isna(unit):
                unit = None
            if pd.isna(grade):
                grade = None
            
            query = """
            CREATE (c:Concept {
                concept: $concept,
                unit: $unit,
                grade: $grade
            })
            """
            
            session.run(query, concept=concept_name, unit=unit, grade=grade)
            
            if (index + 1) % 50 == 0:
                print(f"   진행률: {index + 1}/{len(df)}")
    
    print(f"✅ {len(df)}개 Concept 노드 생성 완료")

def load_edges():
    """관계 데이터 로드"""
    print("🔗 관계 데이터 로드 중...")
    
    # CSV 파일 경로
    edges_file = Path(__file__).resolve().parents[1] / "data" / "neo4j_edges.csv"
    
    if not edges_file.exists():
        print(f"❌ 관계 파일을 찾을 수 없음: {edges_file}")
        return
    
    # CSV 파일 읽기 (한글 인코딩 처리)
    try:
        df = pd.read_csv(edges_file, encoding='utf-8')
    except UnicodeDecodeError:
        try:
            df = pd.read_csv(edges_file, encoding='cp949')
        except UnicodeDecodeError:
            df = pd.read_csv(edges_file, encoding='euc-kr')
    
    print(f"📁 관계 파일 읽기 완료: {len(df)}개 행")
    
    # 데이터 확인
    print(f"📋 컬럼: {list(df.columns)}")
    print(f"📊 처음 3행:")
    print(df.head(3))
    
    with driver.session() as session:
        # PRECEDES 관계 생성
        for index, row in df.iterrows():
            source_concept = row['source']
            target_concept = row['target']
            relationship_type = row['type']
            
            # precedes 관계만 처리
            if relationship_type == 'precedes':
                query = """
                MATCH (source:Concept {concept: $source_concept})
                MATCH (target:Concept {concept: $target_concept})
                CREATE (source)-[:PRECEDES]->(target)
                """
                
                try:
                    session.run(query, source_concept=source_concept, target_concept=target_concept)
                except Exception as e:
                    print(f"⚠️ 관계 생성 실패: {source_concept} -> {target_concept} (오류: {e})")
            
            if (index + 1) % 100 == 0:
                print(f"   진행률: {index + 1}/{len(df)}")
    
    print(f"✅ 관계 데이터 로드 완료")

def verify_data():
    """데이터 검증"""
    print("🔍 데이터 검증 중...")
    
    with driver.session() as session:
        # 노드 수 확인
        result = session.run("MATCH (c:Concept) RETURN count(c) as node_count")
        node_count = result.single()["node_count"]
        print(f"📊 Concept 노드 수: {node_count}")
        
        # 관계 수 확인
        result = session.run("MATCH ()-[r:PRECEDES]->() RETURN count(r) as relationship_count")
        relationship_count = result.single()["relationship_count"]
        print(f"🔗 PRECEDES 관계 수: {relationship_count}")
        
        # 단원별 개념 수
        result = session.run("""
            MATCH (c:Concept)
            WHERE c.unit IS NOT NULL AND c.unit <> ''
            RETURN c.unit as unit, count(c) as count
            ORDER BY count DESC
            LIMIT 10
        """)
        
        print("📚 단원별 개념 수 (상위 10개):")
        for record in result:
            print(f"   {record['unit']}: {record['count']}개")
        
        # 학년별 개념 수
        result = session.run("""
            MATCH (c:Concept)
            WHERE c.grade IS NOT NULL AND c.grade <> ''
            RETURN c.grade as grade, count(c) as count
            ORDER BY grade
        """)
        
        print("🎓 학년별 개념 수:")
        for record in result:
            print(f"   {record['grade']}학년: {record['count']}개")

def main():
    print("🚀 Neo4j 그래프 데이터베이스 재구축 시작!")
    print("=" * 60)
    
    try:
        # 1. 기존 데이터 삭제
        clear_database()
        
        # 2. 제약조건 생성
        create_constraints()
        
        # 3. 노드 로드
        load_nodes()
        
        # 4. 관계 로드
        load_edges()
        
        # 5. 데이터 검증
        verify_data()
        
        print("\n🎉 Neo4j 그래프 데이터베이스 재구축 완료!")
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        driver.close()
        print("🔌 Neo4j 연결 종료")

if __name__ == "__main__":
    main()
