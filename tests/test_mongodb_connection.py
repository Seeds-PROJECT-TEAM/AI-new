#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MongoDB 연결 테스트 스크립트
여러 가지 연결 방법을 시도하여 MongoDB 연결 상태를 확인합니다.
"""

import os
import sys
from pathlib import Path

# AI 디렉토리를 Python 경로에 추가
AI_DIR = Path(__file__).parent
sys.path.insert(0, str(AI_DIR))

from app.db.mongo import init_mongodb, ping
from app.services.mongo_service import MongoService

def test_mongodb_connection():
    """MongoDB 연결 테스트"""
    print("🔍 MongoDB 연결 테스트 시작")
    print("=" * 50)
    
    # 1. 기본 MongoDB 연결 테스트
    print("📊 1. 기본 MongoDB 연결 테스트")
    try:
        init_mongodb()
        if ping():
            print("✅ 기본 MongoDB 연결 성공!")
        else:
            print("❌ 기본 MongoDB 연결 실패")
    except Exception as e:
        print(f"❌ 기본 MongoDB 연결 오류: {e}")
    
    print()
    
    # 2. MongoDB 서비스 테스트
    print("📊 2. MongoDB 서비스 연결 테스트")
    try:
        mongo_service = MongoService()
        if mongo_service.is_connected:
            print("✅ MongoDB 서비스 연결 성공!")
            
            # 간단한 저장 테스트
            test_data = {"test": "connection", "timestamp": "2025-08-25"}
            result = mongo_service.save_diagnostic_analysis(test_data)
            if result:
                print(f"✅ 테스트 데이터 저장 성공: {result}")
            else:
                print("⚠️ 테스트 데이터 저장 실패")
        else:
            print("❌ MongoDB 서비스 연결 실패")
    except Exception as e:
        print(f"❌ MongoDB 서비스 연결 오류: {e}")
    
    print()
    
    # 3. 환경 변수 확인
    print("📊 3. 환경 변수 확인")
    mongodb_uri = os.getenv("MONGODB_URI")
    if mongodb_uri:
        # 민감한 정보는 가려서 출력
        if "mongodb+s://" in mongodb_uri:
            masked_uri = mongodb_uri.replace(mongodb_uri.split("@")[0], "***:***")
            print(f"✅ MONGODB_URI 설정됨: {masked_uri}")
        else:
            print(f"✅ MONGODB_URI 설정됨: {mongodb_uri[:50]}...")
    else:
        print("❌ MONGODB_URI 환경변수가 설정되지 않음")
    
    print()
    print("=" * 50)
    print("🎉 MongoDB 연결 테스트 완료!")

if __name__ == "__main__":
    test_mongodb_connection()
