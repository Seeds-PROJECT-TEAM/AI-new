#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
problem 컬렉션을 수정된 스키마로 재생성하는 스크립트
unitId와 problemId를 string 타입으로 변경
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from pymongo import MongoClient, ASCENDING, TEXT
from pymongo.errors import CollectionInvalid, OperationFailure

# AI 디렉토리를 Python 경로에 추가
AI_DIR = Path(__file__).parent
sys.path.insert(0, str(AI_DIR))

# .env 파일 로드
load_dotenv(AI_DIR / ".env")

def recreate_problem_collection():
    """problem 컬렉션을 수정된 스키마로 재생성"""
    client = None
    try:
        # MongoDB 연결
        mongodb_uri = os.getenv("MONGODB_URI")
        if not mongodb_uri:
            raise RuntimeError("MONGODB_URI 환경변수가 설정되지 않았습니다.")
        
        print("🚀 MongoDB 연결 시도 중...")
        client = MongoClient(mongodb_uri)
        db = client.nerdmath
        client.admin.command("ping")
        print("✅ MongoDB 연결 성공!")
        
        collection_name = "problem"
        
        # 기존 컬렉션 삭제
        if collection_name in db.list_collection_names():
            print(f"🗑️ 기존 '{collection_name}' 컬렉션 삭제 중...")
            db.drop_collection(collection_name)
            print(f"✅ '{collection_name}' 컬렉션 삭제 완료")
        
        # 수정된 스키마로 컬렉션 생성
        problem_schema = {
            "validator": {
                "$jsonSchema": {
                    "bsonType": "object",
                    "required": ["problemId", "unitId", "grade", "chapter", "context", "cognitiveType", "level", "diagnosticTest", "type", "tags", "content", "correctAnswer", "explanation", "createdAt", "updatedAt"],
                    "properties": {
                        "problemId": {"bsonType": "string"},
                        "unitId": {"bsonType": "string"},
                        "grade": {"bsonType": "number"},
                        "chapter": {"bsonType": "number"},
                        "context": {"bsonType": "object"},
                        "cognitiveType": {"bsonType": "string"},
                        "level": {"bsonType": "string"},
                        "diagnosticTest": {"bsonType": "bool"},
                        "type": {"bsonType": "string"},
                        "tags": {"bsonType": "array"},
                        "content": {"bsonType": "object"},
                        "correctAnswer": {"bsonType": "string"},
                        "explanation": {"bsonType": "object"},
                        "imageUrl": {"bsonType": "string"},
                        "createdAt": {"bsonType": "date"},
                        "updatedAt": {"bsonType": "date"}
                    }
                }
            }
        }
        
        print(f"🔧 '{collection_name}' 컬렉션 생성 중...")
        db.create_collection(collection_name, **problem_schema)
        print(f"✅ '{collection_name}' 컬렉션 생성 완료")
        
        # 인덱스 생성
        problem_collection = db[collection_name]
        indexes_to_create = [
            [("problemId", ASCENDING)],
            [("unitId", ASCENDING)],
            [("grade", ASCENDING)],
            [("chapter", ASCENDING)],
            [("cognitiveType", ASCENDING)],
            [("level", ASCENDING)],
            [("diagnosticTest", ASCENDING)],
            [("type", ASCENDING)],
            [("tags", ASCENDING)],
            [("content.korean.stem", TEXT)],
            [("content.english.stem", TEXT)]
        ]
        
        print("🔍 인덱스 생성 중...")
        for index_spec in indexes_to_create:
            try:
                # 인덱스 이름 생성
                if TEXT in index_spec:
                    field_name = index_spec[0][0].replace(".", "_")
                    index_name = f"{field_name}_text_idx"
                else:
                    field_name = index_spec[0][0]
                    index_name = f"{field_name}_idx"
                
                # 인덱스 생성
                if TEXT in index_spec:
                    problem_collection.create_index(index_spec, name=index_name)
                else:
                    problem_collection.create_index(index_spec, name=index_name)
                
                print(f"✅ 인덱스 '{index_name}' 생성 완료")
                
            except Exception as e:
                if "already exists" in str(e):
                    print(f"⚠️ 인덱스 '{index_name}' 이미 존재함")
                else:
                    print(f"❌ 인덱스 '{index_name}' 생성 실패: {e}")
        
        print("🎉 problem 컬렉션 재생성 및 인덱스 생성 완료!")
        return True
        
    except Exception as e:
        print(f"❌ problem 컬렉션 재생성 실패: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        if client:
            client.close()
            print("🔌 MongoDB 연결 종료")

if __name__ == "__main__":
    print("🚀 Problem 컬렉션 재생성 시작")
    print("=" * 60)
    recreate_problem_collection()
