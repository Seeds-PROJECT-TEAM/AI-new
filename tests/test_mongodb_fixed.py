#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
수정된 MongoDB 연결 테스트
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# .env 파일 로드
ROOT = Path(__file__).resolve().parents[0]
load_dotenv(ROOT / ".env")

def test_mongodb_connection():
    """수정된 MongoDB 연결 테스트"""
    
    print("🔍 수정된 MongoDB 연결 테스트 시작")
    print("=" * 50)
    
    # MongoDB URI 확인
    mongo_uri = os.getenv("MONGODB_URI")
    if not mongo_uri:
        print("❌ MONGODB_URI 환경변수가 설정되지 않음")
        return
    
    print(f"📋 MongoDB URI: {mongo_uri[:50]}...")
    print(f"🐍 Python 버전: 3.9.6")
    print()
    
    # 방법 1: Python 3.9 호환 SSL 설정
    print("🚀 방법 1: Python 3.9 호환 SSL 설정으로 연결 시도...")
    try:
        from pymongo import MongoClient
        import ssl
        
        client = MongoClient(
            mongo_uri,
            serverSelectionTimeoutMS=15000,
            connectTimeoutMS=15000,
            socketTimeoutMS=15000,
            tls=True,
            tlsAllowInvalidCertificates=True,
            tlsAllowInvalidHostnames=True,
            ssl_cert_reqs=ssl.CERT_NONE,
            ssl_ca_certs=None
        )
        
        # 연결 테스트
        client.admin.command('ping')
        print("✅ 방법 1 성공! MongoDB 연결됨")
        
        # 데이터베이스 선택
        db = client.nerdmath
        print(f"📊 데이터베이스 'nerdmath' 선택됨")
        
        # 컬렉션 확인
        collections = db.list_collection_names()
        print(f"📚 사용 가능한 컬렉션: {collections}")
        
        client.close()
        return True
        
    except Exception as e:
        print(f"❌ 방법 1 실패: {e}")
        
        # 방법 2: SSL 없이 연결
        print("\n🚀 방법 2: SSL 없이 연결 시도...")
        try:
            clean_uri = mongo_uri.replace("mongodb+s://", "mongodb://")
            client = MongoClient(
                clean_uri,
                serverSelectionTimeoutMS=15000,
                connectTimeoutMS=15000,
                socketTimeoutMS=15000,
                tls=False,
                ssl=False
            )
            
            # 연결 테스트
            client.admin.command('ping')
            print("✅ 방법 2 성공! MongoDB 연결됨 (SSL 없음)")
            
            # 데이터베이스 선택
            db = client.nerdmath
            print(f"📊 데이터베이스 'nerdmath' 선택됨")
            
            # 컬렉션 확인
            collections = db.list_collection_names()
            print(f"📚 사용 가능한 컬렉션: {collections}")
            
            client.close()
            return True
            
        except Exception as e2:
            print(f"❌ 방법 2도 실패: {e2}")
            
            # 방법 3: URI 파라미터로 SSL 설정
            print("\n🚀 방법 3: URI 파라미터로 SSL 설정...")
            try:
                if "?" in mongo_uri:
                    uri_with_params = f"{mongo_uri}&ssl=false&ssl_cert_reqs=CERT_NONE"
                else:
                    uri_with_params = f"{mongo_uri}?ssl=false&ssl_cert_reqs=CERT_NONE"
                
                client = MongoClient(
                    uri_with_params,
                    serverSelectionTimeoutMS=15000,
                    connectTimeoutMS=15000,
                    socketTimeoutMS=15000
                )
                
                # 연결 테스트
                client.admin.command('ping')
                print("✅ 방법 3 성공! MongoDB 연결됨 (URI 파라미터)")
                
                # 데이터베이스 선택
                db = client.nerdmath
                print(f"📊 데이터베이스 'nerdmath' 선택됨")
                
                # 컬렉션 확인
                collections = db.list_collection_names()
                print(f"📚 사용 가능한 컬렉션: {collections}")
                
                client.close()
                return True
                
            except Exception as e3:
                print(f"❌ 방법 3도 실패: {e3}")
                print("\n❌ 모든 MongoDB 연결 방법 실패!")
                print("💡 해결 방법:")
                print("   1. Python 3.11+ 업그레이드")
                print("   2. MongoDB Atlas에서 SSL 설정 변경")
                print("   3. 로컬 MongoDB 사용")
                return False
    
    print("=" * 50)
    print("🎉 테스트 완료!")

if __name__ == "__main__":
    test_mongodb_connection()
