#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
concept 컬렉션을 수정된 스키마로 재생성하는 스크립트
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from pymongo import MongoClient, ASCENDING

# AI 디렉토리를 Python 경로에 추가
AI_DIR = Path(__file__).parent
sys.path.insert(0, str(AI_DIR))

# .env 파일 로드
load_dotenv(AI_DIR / ".env")

def fix_concept_collection():
    """concept 컬렉션을 수정된 스키마로 재생성"""
    try:
        # MongoDB 연결
        mongodb_uri = os.getenv("MONGODB_URI")
        if not mongodb_uri:
            print("❌ MONGODB_URI 환경변수가 설정되지 않았습니다.")
            return False
        
        print("🚀 MongoDB 연결 중...")
        client = MongoClient(mongodb_uri)
        db = client.nerdmath
        client.admin.command("ping")
        print("✅ MongoDB 연결 성공!")
        
        # 기존 concept 컬렉션 삭제
        if "concept" in db.list_collection_names():
            print("🗑️ 기존 concept 컬렉션 삭제 중...")
            db.concept.drop()
            print("✅ 기존 concept 컬렉션 삭제 완료")
        
        # 수정된 스키마로 concept 컬렉션 생성
        concept_config = {
            "validator": {
                "$jsonSchema": {
                    "bsonType": "object",
                    "required": ["conceptId", "unitId", "blocks", "createdAt"],
                    "properties": {
                        "conceptId": {"bsonType": "string"},
                        "unitId": {"bsonType": "string"},
                        "blocks": {"bsonType": "array"},
                        "createdAt": {"bsonType": "date"}
                    }
                }
            }
        }
        
        db.create_collection("concept", **concept_config)
        print("✅ 수정된 스키마로 concept 컬렉션 생성 완료")
        
        # 인덱스 생성
        print("🔍 concept 컬렉션 인덱스 생성 중...")
        concept_collection = db.concept
        
        indexes = [
            [("conceptId", ASCENDING)],
            [("unitId", ASCENDING)]
        ]
        
        for index_spec in indexes:
            try:
                index_name = f"{'_'.join([str(field[0]) for field in index_spec])}_idx"
                concept_collection.create_index(index_spec, name=index_name)
                print(f"✅ 인덱스 '{index_name}' 생성 완료")
            except Exception as e:
                print(f"⚠️ 인덱스 '{index_name}' 생성 실패: {e}")
        
        print("🎉 concept 컬렉션 재생성 및 인덱스 생성 완료!")
        
        # 검증
        collections = db.list_collection_names()
        if "concept" in collections:
            print("✅ concept 컬렉션이 존재합니다")
            
            # 스키마 확인
            collection_info = db.get_collection("concept").options()
            if "validator" in collection_info:
                print("✅ 스키마 검증기가 설정되어 있습니다")
                schema = collection_info["validator"]["$jsonSchema"]
                print(f"  - conceptId 타입: {schema['properties']['conceptId']['bsonType']}")
                print(f"  - unitId 타입: {schema['properties']['unitId']['bsonType']}")
            else:
                print("⚠️ 스키마 검증기가 설정되어 있지 않습니다")
        else:
            print("❌ concept 컬렉션이 존재하지 않습니다")
            return False
        
        client.close()
        print("🔌 MongoDB 연결 종료")
        return True
        
    except Exception as e:
        print(f"❌ concept 컬렉션 수정 실패: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Concept 컬렉션 수정 시작")
    print("=" * 60)
    
    success = fix_concept_collection()
    if success:
        print("\n🎉 Concept 컬렉션 수정 완료!")
    else:
        print("\n❌ Concept 컬렉션 수정 실패!")
