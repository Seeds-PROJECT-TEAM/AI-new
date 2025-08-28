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

def load_edges():
    """관계 데이터 로드 (수정된 버전)"""
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
    print(f"📊 처음 5행:")
    print(df.head())
    
    # type 컬럼의 고유값 확인
    print(f"🔍 type 컬럼 고유값: {df['type'].unique()}")
    
    with driver.session() as session:
        # PRECEDES 관계 생성 (대소문자 구분 없이)
        success_count = 0
        error_count = 0
        
        for index, row in df.iterrows():
            source_concept = row['source']
            target_concept = row['target']
            relationship_type = row['type']
            
            # PRECEDES 관계 처리 (대소문자 구분 없이)
            if relationship_type.upper() == 'PRECEDES':
                query = """
                MATCH (source:Concept {concept: $source_concept})
                MATCH (target:Concept {concept: $target_concept})
                CREATE (source)-[:PRECEDES]->(target)
                """
                
                try:
                    session.run(query, source_concept=source_concept, target_concept=target_concept)
                    success_count += 1
                except Exception as e:
                    print(f"⚠️ 관계 생성 실패: {source_concept} -> {target_concept} (오류: {e})")
                    error_count += 1
            
            if (index + 1) % 100 == 0:
                print(f"   진행률: {index + 1}/{len(df)}")
        
        print(f"✅ 관계 데이터 로드 완료")
        print(f"   성공: {success_count}개, 실패: {error_count}개")

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
        
        # 관계 예시 확인
        result = session.run("""
            MATCH (src:Concept)-[:PRECEDES]->(dst:Concept)
            RETURN src.concept as 선행개념, dst.concept as 후행개념
            LIMIT 5
        """)
        
        print("🔗 관계 예시 (처음 5개):")
        for record in result:
            print(f"   {record['선행개념']} -> {record['후행개념']}")

def main():
    print("🔧 Neo4j 관계 데이터 수정 시작!")
    print("=" * 50)
    
    try:
        # 1. 관계 데이터 로드
        load_edges()
        
        # 2. 데이터 검증
        verify_data()
        
        print("\n🎉 관계 데이터 수정 완료!")
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        driver.close()
        print("🔌 Neo4j 연결 종료")

if __name__ == "__main__":
    main()
