#!/usr/bin/env python3
"""
MongoDB 연결 간단 테스트
"""

import os
from dotenv import load_dotenv
from pymongo import MongoClient

def test_mongo_simple():
    """MongoDB 연결 간단 테스트"""
    try:
        # 환경변수 로드
        load_dotenv('AI/.env')
        mongodb_uri = os.getenv('MONGODB_URI')
        
        if not mongodb_uri:
            print("❌ MONGODB_URI 환경변수가 설정되지 않음")
            return False
        
        print(f"🔍 MongoDB URI: {mongodb_uri[:50]}...")
        print("=" * 50)
        
        # 1. 기본 연결 시도
        print("🚀 1️⃣ 기본 MongoDB 연결 시도 중...")
        try:
            client = MongoClient(mongodb_uri)
            result = client.admin.command("ping")
            if result.get("ok") == 1:
                print("✅ 기본 연결 성공!")
                client.close()
                return True
        except Exception as e:
            print(f"❌ 기본 연결 실패: {str(e)[:100]}...")
        
        # 2. SSL 없이 연결 시도
        print("\n🚀 2️⃣ SSL 없이 MongoDB 연결 시도 중...")
        try:
            client = MongoClient(
                mongodb_uri,
                tls=False,
                serverSelectionTimeoutMS=10000
            )
            result = client.admin.command("ping")
            if result.get("ok") == 1:
                print("✅ SSL 없이 연결 성공!")
                client.close()
                return True
        except Exception as e:
            print(f"❌ SSL 없이 연결 실패: {str(e)[:100]}...")
        
        # 3. SSL 옵션으로 연결 시도
        print("\n🚀 3️⃣ SSL 옵션으로 MongoDB 연결 시도 중...")
        try:
            client = MongoClient(
                mongodb_uri,
                tls=True,
                tlsAllowInvalidCertificates=True,
                serverSelectionTimeoutMS=10000
            )
            result = client.admin.command("ping")
            if result.get("ok") == 1:
                print("✅ SSL 옵션으로 연결 성공!")
                client.close()
                return True
        except Exception as e:
            print(f"❌ SSL 옵션으로 연결 실패: {str(e)[:100]}...")
        
        print("\n❌ 모든 연결 방법 실패!")
        return False
            
    except Exception as e:
        print(f"❌ 전체 테스트 실패: {e}")
        return False

if __name__ == "__main__":
    print("🔍 MongoDB 연결 테스트 시작")
    test_mongo_simple()
    print("=" * 50)
    print("테스트 완료")
