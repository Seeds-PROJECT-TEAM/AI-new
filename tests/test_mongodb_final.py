#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
최종 수정된 MongoDB 연결 테스트
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# .env 파일 로드
ROOT = Path(__file__).resolve().parents[0]
load_dotenv(ROOT / ".env")

def test_mongodb_final():
    """최종 수정된 MongoDB 연결 테스트"""
    
    print("🔍 최종 수정된 MongoDB 연결 테스트 시작")
    print("=" * 50)
    
    # MongoDB URI 확인
    mongo_uri = os.getenv("MONGODB_URI")
    if not mongo_uri:
        print("❌ MONGODB_URI 환경변수가 설정되지 않음")
        return
    
    print(f"📋 MongoDB URI: {mongo_uri[:50]}...")
    print(f"🐍 Python 버전: 3.9.6")
    print()
    
    # 방법 1: 기본 Atlas 연결 (Python 3.9에서 작동하는 설정)
    print("🚀 방법 1: 기본 Atlas 연결 (Python 3.9 호환)...")
    try:
        from pymongo import MongoClient
        
        client = MongoClient(
            mongo_uri,
            serverSelectionTimeoutMS=20000,
            connectTimeoutMS=20000,
            socketTimeoutMS=20000,
            # Python 3.9 호환 설정
            tls=True,
            tlsAllowInvalidCertificates=True,
            tlsAllowInvalidHostnames=True
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
        
        # 방법 2: URI에서 SSL 강제 비활성화
        print("\n🚀 방법 2: SSL 강제 비활성화...")
        try:
            if "mongodb+s://" in mongo_uri:
                # Atlas URI를 표준 MongoDB URI로 변환
                clean_uri = mongo_uri.replace("mongodb+s://", "mongodb://")
                # 기존 파라미터가 있으면 추가, 없으면 새로 생성
                if "?" in clean_uri:
                    clean_uri += "&tls=false"
                else:
                    clean_uri += "?tls=false"
            else:
                clean_uri = mongo_uri
            
            print(f"🔧 변환된 URI: {clean_uri[:50]}...")
            
            client = MongoClient(
                clean_uri,
                serverSelectionTimeoutMS=20000,
                connectTimeoutMS=20000,
                socketTimeoutMS=20000,
                tls=False
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
            print("\n❌ 모든 MongoDB 연결 방법 실패!")
            print("💡 해결 방법:")
            print("   1. Python 3.11+ 업그레이드 (권장)")
            print("   2. MongoDB Atlas에서 SSL 설정 변경")
            print("   3. 로컬 MongoDB 사용")
            print("   4. 현재는 로컬 모드로 작동 (MongoDB 저장 없음)")
            return False
    
    print("=" * 50)
    print("🎉 테스트 완료!")

if __name__ == "__main__":
    test_mongodb_final()
