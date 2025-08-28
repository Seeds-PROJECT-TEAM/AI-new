#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
기존 unit 컬렉션을 삭제하고 수정된 스키마로 새로 생성하는 스크립트
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.errors import CollectionInvalid, OperationFailure

# AI 디렉토리를 Python 경로에 추가
AI_DIR = Path(__file__).parent
sys.path.insert(0, str(AI_DIR))

# .env 파일 로드
load_dotenv(AI_DIR / ".env")

class UnitCollectionRecreator:
    def __init__(self):
        self.client = None
        self.db = None
        self.mongodb_uri = os.getenv("MONGODB_URI")
        
        if not self.mongodb_uri:
            raise RuntimeError("MONGODB_URI 환경변수가 설정되지 않았습니다.")
    
    def connect(self):
        """MongoDB에 연결"""
        try:
            print("🚀 MongoDB 연결 시도 중...")
            self.client = MongoClient(self.mongodb_uri)
            self.db = self.client.nerdmath
            self.client.admin.command("ping")
            print("✅ MongoDB 연결 성공!")
            return True
        except Exception as e:
            print(f"❌ MongoDB 연결 실패: {e}")
            return False
    
    def recreate_unit_collection(self):
        """unit 컬렉션을 수정된 스키마로 재생성"""
        try:
            print("🔄 unit 컬렉션 재생성 시작...")
            
            # 기존 unit 컬렉션이 있는지 확인
            if "unit" in self.db.list_collection_names():
                print("🗑️ 기존 unit 컬렉션 삭제 중...")
                self.db.unit.drop()
                print("✅ 기존 unit 컬렉션 삭제 완료")
            
            # 수정된 스키마로 unit 컬렉션 생성
            unit_config = {
                "validator": {
                    "$jsonSchema": {
                        "bsonType": "object",
                        "required": ["unitId", "subject", "title", "grade", "chapter", "chapterTitle", "orderInGrade", "status", "createdAt"],
                        "properties": {
                            "unitId": {"bsonType": "string"},  # objectId에서 string으로 변경
                            "subject": {"bsonType": "string"},
                            "title": {"bsonType": "object"},
                            "grade": {"bsonType": "number"},
                            "chapter": {"bsonType": "number"},
                            "chapterTitle": {"bsonType": "string"},
                            "orderInGrade": {"bsonType": "number"},
                            "description": {"bsonType": "object"},
                            "status": {"bsonType": "string"},
                            "createdAt": {"bsonType": "date"}
                        }
                    }
                }
            }
            
            self.db.create_collection("unit", **unit_config)
            print("✅ 수정된 스키마로 unit 컬렉션 생성 완료")
            
            # 인덱스 생성
            print("🔍 unit 컬렉션 인덱스 생성 중...")
            unit_collection = self.db.unit
            
            indexes = [
                [("unitId", ASCENDING)],
                [("subject", ASCENDING)],
                [("grade", ASCENDING)],
                [("chapter", ASCENDING)],
                [("orderInGrade", ASCENDING)],
                [("status", ASCENDING)]
            ]
            
            for index_spec in indexes:
                try:
                    index_name = f"{'_'.join([str(field[0]) for field in index_spec])}_idx"
                    unit_collection.create_index(index_spec, name=index_name)
                    print(f"✅ 인덱스 '{index_name}' 생성 완료")
                except Exception as e:
                    print(f"⚠️ 인덱스 '{index_name}' 생성 실패: {e}")
            
            print("🎉 unit 컬렉션 재생성 및 인덱스 생성 완료!")
            return True
            
        except Exception as e:
            print(f"❌ unit 컬렉션 재생성 실패: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def verify_collection(self):
        """생성된 컬렉션 검증"""
        try:
            print("\n🔍 생성된 unit 컬렉션 검증...")
            
            # 컬렉션 존재 확인
            collections = self.db.list_collection_names()
            if "unit" in collections:
                print("✅ unit 컬렉션이 존재합니다")
            else:
                print("❌ unit 컬렉션이 존재하지 않습니다")
                return False
            
            # 인덱스 확인
            unit_collection = self.db.unit
            indexes = list(unit_collection.list_indexes())
            print(f"📊 인덱스 수: {len(indexes)}")
            for idx in indexes:
                print(f"  - {idx.get('name', 'unnamed')}: {list(idx['key'])}")
            
            # 스키마 검증
            print("\n📋 스키마 정보:")
            collection_info = self.db.get_collection("unit").options()
            if "validator" in collection_info:
                print("✅ 스키마 검증기가 설정되어 있습니다")
                schema = collection_info["validator"]["$jsonSchema"]
                print(f"  - unitId 타입: {schema['properties']['unitId']['bsonType']}")
            else:
                print("⚠️ 스키마 검증기가 설정되어 있지 않습니다")
            
            return True
            
        except Exception as e:
            print(f"❌ 컬렉션 검증 실패: {e}")
            return False
    
    def run(self):
        """전체 프로세스 실행"""
        if not self.connect():
            return False
        
        try:
            success = self.recreate_unit_collection()
            if success:
                self.verify_collection()
                print("\n🎉 Unit 컬렉션 재생성 완료!")
            else:
                print("\n❌ Unit 컬렉션 재생성 실패!")
            
            return success
            
        except Exception as e:
            print(f"❌ 스크립트 실행 실패: {e}")
            import traceback
            traceback.print_exc()
            return False
        
        finally:
            if self.client:
                self.client.close()
                print("🔌 MongoDB 연결 종료")

def main():
    """메인 함수"""
    print("🚀 Unit 컬렉션 재생성 시작")
    print("=" * 60)
    
    try:
        recreator = UnitCollectionRecreator()
        recreator.run()
        
    except Exception as e:
        print(f"❌ 스크립트 실행 실패: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
