#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
unit_nodes_ts_desc_grade_ordered.txt 파일의 데이터를 MongoDB nerdmath 데이터베이스의 unit 컬렉션에 저장하는 스크립트
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from pymongo import MongoClient
from bson import ObjectId

# AI 디렉토리를 Python 경로에 추가
AI_DIR = Path(__file__).parent
sys.path.insert(0, str(AI_DIR))

# .env 파일 로드
load_dotenv(AI_DIR / ".env")

class UnitDataLoader:
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
    
    def load_unit_data(self):
        """unit_nodes_ts_desc_grade_ordered.txt 파일에서 데이터를 읽어서 MongoDB에 저장"""
        file_path = AI_DIR / "data" / "unit_nodes_ts_desc_grade_ordered.txt"
        
        if not file_path.exists():
            print(f"❌ 파일을 찾을 수 없습니다: {file_path}")
            return False
        
        try:
            print(f"📖 파일 읽기 시작: {file_path}")
            
            # 기존 unit 컬렉션의 데이터 개수 확인
            unit_collection = self.db.unit
            existing_count = unit_collection.count_documents({})
            print(f"📊 기존 unit 컬렉션 문서 수: {existing_count}")
            
            # 파일에서 데이터 읽기
            units_data = []
            with open(file_path, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if not line:
                        continue
                    
                    try:
                        # JSON 파싱
                        unit_data = json.loads(line)
                        
                        # MongoDB 스키마에 맞게 데이터 변환
                        mongo_unit = {
                            "_id": ObjectId(),  # 새로운 ObjectId 생성
                            "unitId": unit_data.get("unitId", ""),
                            "subject": unit_data.get("subject", "math"),
                            "title": unit_data.get("title", {}),
                            "grade": unit_data.get("grade", 1),
                            "chapter": unit_data.get("chapter", 1),
                            "chapterTitle": unit_data.get("chapterTitle", ""),
                            "orderInGrade": unit_data.get("orderInGrade", 1),
                            "description": unit_data.get("description", {}),
                            "status": unit_data.get("status", "active"),
                            "createdAt": datetime.fromisoformat(unit_data.get("createdAt", "2025-08-28T10:26:51Z").replace("Z", "+00:00"))
                        }
                        
                        units_data.append(mongo_unit)
                        
                    except json.JSONDecodeError as e:
                        print(f"⚠️ JSON 파싱 오류 (줄 {line_num}): {e}")
                        print(f"   문제가 된 줄: {line[:100]}...")
                        continue
                    except Exception as e:
                        print(f"⚠️ 데이터 처리 오류 (줄 {line_num}): {e}")
                        continue
            
            print(f"📋 총 {len(units_data)}개의 unit 데이터를 읽었습니다.")
            
            if not units_data:
                print("❌ 저장할 데이터가 없습니다.")
                return False
            
            # MongoDB에 데이터 저장
            print("💾 MongoDB에 데이터 저장 시작...")
            
            # 기존 데이터 삭제 (선택사항)
            if existing_count > 0:
                print("🗑️ 기존 unit 데이터 삭제 중...")
                result = unit_collection.delete_many({})
                print(f"   삭제된 문서 수: {result.deleted_count}")
            
            # 새 데이터 삽입
            result = unit_collection.insert_many(units_data)
            print(f"✅ {len(result.inserted_ids)}개의 unit 데이터 저장 완료!")
            
            # 저장된 데이터 확인
            final_count = unit_collection.count_documents({})
            print(f"📊 최종 unit 컬렉션 문서 수: {final_count}")
            
            # 샘플 데이터 출력
            print("\n📋 저장된 데이터 샘플:")
            sample_units = unit_collection.find().limit(3)
            for i, unit in enumerate(sample_units, 1):
                print(f"  {i}. {unit['unitId']} - {unit['title'].get('ko', 'N/A')} (학년 {unit['grade']}, 챕터 {unit['chapter']})")
            
            return True
            
        except Exception as e:
            print(f"❌ 데이터 로드 실패: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def verify_data(self):
        """저장된 데이터 검증"""
        try:
            print("\n🔍 저장된 데이터 검증 시작...")
            
            unit_collection = self.db.unit
            
            # 전체 문서 수 확인
            total_count = unit_collection.count_documents({})
            print(f"📊 전체 unit 문서 수: {total_count}")
            
            # 학년별 통계
            grade_stats = unit_collection.aggregate([
                {"$group": {"_id": "$grade", "count": {"$sum": 1}}},
                {"$sort": {"_id": 1}}
            ])
            
            print("\n📚 학년별 unit 수:")
            for stat in grade_stats:
                print(f"  학년 {stat['_id']}: {stat['count']}개")
            
            # 챕터별 통계
            chapter_stats = unit_collection.aggregate([
                {"$group": {"_id": {"grade": "$grade", "chapter": "$chapter"}, "count": {"$sum": 1}}},
                {"$sort": {"_id.grade": 1, "_id.chapter": 1}}
            ])
            
            print("\n📖 챕터별 unit 수:")
            for stat in chapter_stats:
                grade, chapter = stat['_id']['grade'], stat['_id']['chapter']
                print(f"  학년 {grade} 챕터 {chapter}: {stat['count']}개")
            
            # 인덱스 확인
            indexes = list(unit_collection.list_indexes())
            print(f"\n🔍 인덱스 수: {len(indexes)}")
            for idx in indexes:
                print(f"  - {idx.get('name', 'unnamed')}: {list(idx['key'])}")
            
            print("✅ 데이터 검증 완료!")
            return True
            
        except Exception as e:
            print(f"❌ 데이터 검증 실패: {e}")
            return False
    
    def run(self):
        """전체 프로세스 실행"""
        if not self.connect():
            return False
        
        try:
            success = self.load_unit_data()
            if success:
                self.verify_data()
                print("\n🎉 Unit 데이터 로드 완료!")
            else:
                print("\n❌ Unit 데이터 로드 실패!")
            
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
    print("🚀 Unit 데이터 로드 시작")
    print("=" * 60)
    
    try:
        loader = UnitDataLoader()
        loader.run()
        
    except Exception as e:
        print(f"❌ 스크립트 실행 실패: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
