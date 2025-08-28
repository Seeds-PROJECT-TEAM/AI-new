#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MongoDB 데이터베이스 상태 확인 스크립트
생성된 컬렉션들과 인덱스를 확인합니다.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from pymongo import MongoClient

# AI 디렉토리를 Python 경로에 추가
AI_DIR = Path(__file__).parent
sys.path.insert(0, str(AI_DIR))

# .env 파일 로드
load_dotenv(AI_DIR / ".env")

def check_mongodb_status():
    """MongoDB 상태 확인"""
    mongodb_uri = os.getenv("MONGODB_URI")
    if not mongodb_uri:
        print("❌ MONGODB_URI 환경변수가 설정되지 않았습니다.")
        return
    
    try:
        print("🚀 MongoDB 연결 시도 중...")
        client = MongoClient(mongodb_uri)
        db = client.nerdmath
        client.admin.command("ping")
        print("✅ MongoDB 연결 성공!")
        
        print("\n" + "="*60)
        print("📊 데이터베이스 정보")
        print("="*60)
        print(f"데이터베이스명: {db.name}")
        print(f"컬렉션 수: {len(db.list_collection_names())}")
        
        # 컬렉션 목록 및 통계
        print("\n" + "="*60)
        print("📋 컬렉션 목록 및 통계")
        print("="*60)
        
        collections = db.list_collection_names()
        collections.sort()
        
        for collection_name in collections:
            collection = db[collection_name]
            count = collection.count_documents({})
            
            # 인덱스 정보
            indexes = list(collection.list_indexes())
            index_count = len(indexes)
            
            print(f"\n📊 {collection_name}")
            print(f"   문서 수: {count:,}")
            print(f"   인덱스 수: {index_count}")
            
            if index_count > 0:
                print("   인덱스 목록:")
                for idx in indexes:
                    idx_name = idx.get('name', 'unnamed')
                    idx_keys = list(idx['key'])
                    print(f"     - {idx_name}: {idx_keys}")
        
        print("\n" + "="*60)
        print("🎉 MongoDB 상태 확인 완료!")
        print("="*60)
        
    except Exception as e:
        print(f"❌ MongoDB 상태 확인 실패: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        if 'client' in locals():
            client.close()
            print("🔌 MongoDB 연결 종료")

if __name__ == "__main__":
    check_mongodb_status()
