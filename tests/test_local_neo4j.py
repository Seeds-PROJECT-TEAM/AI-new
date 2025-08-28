import os
from pathlib import Path
from dotenv import load_dotenv
from neo4j import GraphDatabase

# AI/.env 파일 로드
env_path = Path(__file__).resolve().parents[1] / ".env"
if env_path.exists():
    load_dotenv(env_path)
    print(f"✅ .env 파일 로드됨: {env_path}")

# 연결 옵션들
connection_options = [
    # 로컬 Neo4j
    {
        "name": "로컬 Neo4j",
        "uri": "neo4j://localhost:7687",
        "user": "neo4j",
        "password": "password"  # 기본 비밀번호
    },
    # Neo4j Aura (현재 설정)
    {
        "name": "Neo4j Aura",
        "uri": os.getenv("AURA_URI"),
        "user": os.getenv("AURA_USER"),
        "password": os.getenv("AURA_PASS")
    }
]

def test_connection(conn_info):
    """연결 테스트"""
    if not all([conn_info["uri"], conn_info["user"], conn_info["password"]):
        print(f"❌ {conn_info['name']}: 환경변수 누락")
        return False
    
    try:
        print(f"\n🔗 {conn_info['name']} 연결 시도 중...")
        print(f"URI: {conn_info['uri']}")
        
        driver = GraphDatabase.driver(
            conn_info["uri"], 
            auth=(conn_info["user"], conn_info["password"])
        )
        
        # 연결 확인
        with driver.session() as session:
            result = session.run("RETURN 1 as test")
            record = result.single()
            print(f"✅ {conn_info['name']} 연결 성공! 테스트 결과: {record['test']}")
            
            # 서버 정보 확인
            try:
                server_info = session.run("CALL dbms.components() YIELD name, versions, edition")
                for record in server_info:
                    print(f"  서버: {record['name']} {record['versions'][0]} ({record['edition']})")
            except:
                print("  서버 정보 조회 실패 (권한 부족일 수 있음)")
        
        driver.close()
        return True
        
    except Exception as e:
        print(f"❌ {conn_info['name']} 연결 실패: {e}")
        return False

def main():
    print("=== Neo4j 연결 테스트 시작 ===")
    
    success_count = 0
    for conn_info in connection_options:
        if test_connection(conn_info):
            success_count += 1
    
    print(f"\n=== 테스트 완료 ===")
    print(f"성공한 연결: {success_count}/{len(connection_options)}")
    
    if success_count == 0:
        print("\n💡 해결 방안:")
        print("1. 로컬 Neo4j 설치 및 실행")
        print("2. Neo4j Aura 클러스터 상태 확인")
        print("3. 네트워크/방화벽 설정 확인")
        print("4. .env 파일의 연결 정보 재확인")

if __name__ == "__main__":
    main()
