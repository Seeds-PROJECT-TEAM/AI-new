import os
from pathlib import Path
from dotenv import load_dotenv
from neo4j import GraphDatabase

# AI/.env 파일 로드
env_path = Path(__file__).resolve().parents[1] / ".env"
if env_path.exists():
    load_dotenv(env_path)
    print(f"✅ .env 파일 로드됨: {env_path}")
else:
    print(f"❌ .env 파일 없음: {env_path}")

# 환경변수 확인
AURA_URI = os.getenv("AURA_URI")
AURA_USER = os.getenv("AURA_USER")
AURA_PASS = os.getenv("AURA_PASS")

print(f"AURA_URI: {AURA_URI}")
print(f"AURA_USER: {AURA_USER}")
print(f"AURA_PASS: {'*' * len(AURA_PASS) if AURA_PASS else 'None'}")

if not all([AURA_URI, AURA_USER, AURA_PASS]):
    print("❌ Neo4j 환경변수가 모두 설정되지 않음")
    exit(1)

# 연결 테스트
try:
    print(f"\nNeo4j Aura에 연결 시도 중...")
    print(f"URI: {AURA_URI}")
    
    driver = GraphDatabase.driver(AURA_URI, auth=(AURA_USER, AURA_PASS))
    
    # 연결 확인
    with driver.session() as session:
        result = session.run("RETURN 1 as test")
        record = result.single()
        print(f"✅ 연결 성공! 테스트 쿼리 결과: {record['test']}")
        
        # 서버 정보 확인
        server_info = session.run("CALL dbms.components() YIELD name, versions, edition")
        for record in server_info:
            print(f"서버: {record['name']} {record['versions'][0]} ({record['edition']})")
    
    driver.close()
    print("🎉 Neo4j Aura 연결 테스트 완료!")
    
except Exception as e:
    print(f"❌ Neo4j 연결 실패: {e}")
    print(f"에러 타입: {type(e).__name__}")
    
    # 추가 디버깅 정보
    if "Cannot resolve address" in str(e):
        print("\n💡 DNS 해결 문제일 수 있습니다:")
        print("1. 인터넷 연결 확인")
        print("2. 방화벽 설정 확인")
        print("3. Neo4j Aura 클러스터 상태 확인")
    elif "authentication" in str(e).lower():
        print("\n💡 인증 문제일 수 있습니다:")
        print("1. 사용자명/비밀번호 확인")
        print("2. Neo4j Aura 계정 상태 확인")
