#!/usr/bin/env python3
"""MongoDB 연결 직접 확인 및 환경 변수 체크"""

import os
from pymongo import MongoClient
from pprint import pprint

def check_mongodb_direct():
    try:
        print("=== MongoDB 직접 연결 확인 ===")
        
        # 1. 환경 변수 확인
        print(f"\n1️⃣ 환경 변수 확인:")
        mongodb_uri = os.getenv('MONGODB_URI')
        print(f"   MONGODB_URI: {mongodb_uri[:50] + '...' if mongodb_uri and len(mongodb_uri) > 50 else mongodb_uri}")
        
        # 2. 직접 MongoDB 연결 시도
        print(f"\n2️⃣ MongoDB 직접 연결 시도:")
        if mongodb_uri:
            try:
                client = MongoClient(mongodb_uri)
                # 연결 테스트
                client.admin.command('ping')
                print(f"   ✅ MongoDB 연결 성공!")
                
                # 데이터베이스 목록
                db_list = client.list_database_names()
                print(f"   📚 데이터베이스 목록: {db_list}")
                
                # nerdmath 데이터베이스 확인
                if 'nerdmath' in db_list:
                    db = client['nerdmath']
                    collections = db.list_collection_names()
                    print(f"   📁 nerdmath 컬렉션: {collections}")
                    
                    # 각 컬렉션의 문서 수 확인
                    for collection_name in collections:
                        count = db[collection_name].count_documents({})
                        print(f"     - {collection_name}: {count}개 문서")
                        
                        # 샘플 데이터 확인 (처음 2개)
                        if count > 0:
                            sample = list(db[collection_name].find().limit(2))
                            print(f"       샘플:")
                            for i, doc in enumerate(sample):
                                print(f"         {i+1}. {str(doc)[:100]}...")
                else:
                    print(f"   ⚠️ nerdmath 데이터베이스가 없음")
                    
                client.close()
                
            except Exception as e:
                print(f"   ❌ MongoDB 연결 실패: {e}")
        else:
            print(f"   ⚠️ MONGODB_URI 환경 변수가 설정되지 않음")
        
        # 3. .env 파일 확인
        print(f"\n3️⃣ .env 파일 확인:")
        env_path = os.path.join(os.path.dirname(__file__), 'AI', '.env')
        if os.path.exists(env_path):
            print(f"   ✅ .env 파일 존재: {env_path}")
            try:
                with open(env_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines = content.split('\n')
                    mongodb_lines = [line for line in lines if 'MONGODB' in line]
                    if mongodb_lines:
                        print(f"   📝 MongoDB 관련 환경 변수:")
                        for line in mongodb_lines:
                            if line.strip() and not line.startswith('#'):
                                print(f"     {line.strip()}")
                    else:
                        print(f"   ⚠️ MongoDB 관련 환경 변수가 없음")
            except Exception as e:
                print(f"   ❌ .env 파일 읽기 실패: {e}")
        else:
            print(f"   ❌ .env 파일이 없음: {env_path}")
            
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_mongodb_direct()
