#!/usr/bin/env python3
"""MongoDB 간단 연결 테스트"""

import os
from pymongo import MongoClient

def test_mongodb_simple():
    try:
        print("=== MongoDB 간단 연결 테스트 ===")
        
        # .env 파일에서 MongoDB URI 직접 읽기
        env_path = os.path.join(os.path.dirname(__file__), 'AI', '.env')
        mongodb_uri = None
        
        if os.path.exists(env_path):
            print(f"✅ .env 파일 발견: {env_path}")
            with open(env_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.startswith('MONGODB_URI='):
                        mongodb_uri = line.strip().split('=', 1)[1]
                        break
            
            if mongodb_uri:
                print(f"✅ MongoDB URI 추출 성공")
                print(f"   URI: {mongodb_uri[:50]}...")
                
                # MongoDB 연결 시도
                print(f"\n🔌 MongoDB 연결 시도...")
                client = MongoClient(mongodb_uri)
                
                # 연결 테스트
                client.admin.command('ping')
                print(f"✅ MongoDB 연결 성공!")
                
                # 데이터베이스 목록
                db_list = client.list_database_names()
                print(f"📚 데이터베이스 목록: {db_list}")
                
                # nerdmath 데이터베이스 확인
                if 'nerdmath' in db_list:
                    db = client['nerdmath']
                    collections = db.list_collection_names()
                    print(f"\n📁 nerdmath 컬렉션: {collections}")
                    
                    # 각 컬렉션의 문서 수와 샘플 데이터 확인
                    for collection_name in collections:
                        count = db[collection_name].count_documents({})
                        print(f"\n🔍 {collection_name} 컬렉션: {count}개 문서")
                        
                        if count > 0:
                            # 처음 3개 문서 확인
                            sample = list(db[collection_name].find().limit(3))
                            for i, doc in enumerate(sample):
                                print(f"   📄 문서 {i+1}:")
                                # 주요 필드들만 출력
                                if '_id' in doc:
                                    print(f"     ID: {doc['_id']}")
                                if 'problemId' in doc:
                                    print(f"     problemId: {doc['problemId']}")
                                if 'unitId' in doc:
                                    print(f"     unitId: {doc['unitId']}")
                                if 'concept' in doc:
                                    print(f"     concept: {doc['concept']}")
                                if 'title' in doc:
                                    print(f"     title: {doc['title']}")
                                if 'chapterTitle' in doc:
                                    print(f"     chapterTitle: {doc['chapterTitle']}")
                                if 'pathName' in doc:
                                    print(f"     pathName: {doc['pathName']}")
                                if 'testId' in doc:
                                    print(f"     testId: {doc['testId']}")
                                print()
                else:
                    print(f"⚠️ nerdmath 데이터베이스가 없음")
                
                client.close()
                
            else:
                print(f"❌ MONGODB_URI를 찾을 수 없음")
        else:
            print(f"❌ .env 파일이 없음: {env_path}")
            
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_mongodb_simple()
