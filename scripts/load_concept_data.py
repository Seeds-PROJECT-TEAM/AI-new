#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
concept_cleaned_ndjson.txt 파일의 데이터를 MongoDB nerdmath 데이터베이스의 concept 컬렉션에 저장하는 스크립트
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

class ConceptDataLoader:
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
    
    def load_concept_data(self):
        """concept_cleaned_ndjson.txt 파일에서 데이터를 읽어서 MongoDB에 저장"""
        file_path = AI_DIR / "data" / "concept_cleaned_ndjson.txt"
        
        if not file_path.exists():
            print(f"❌ 파일을 찾을 수 없습니다: {file_path}")
            return False
        
        try:
            print(f"📖 파일 읽기 시작: {file_path}")
            
            # 기존 concept 컬렉션의 데이터 개수 확인
            concept_collection = self.db.concept
            existing_count = concept_collection.count_documents({})
            print(f"📊 기존 concept 컬렉션 문서 수: {existing_count}")
            
            # 파일에서 데이터 읽기
            concepts_data = []
            with open(file_path, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if not line:
                        continue
                    
                    try:
                        # JSON 파싱
                        concept_data = json.loads(line)
                        
                        # MongoDB 스키마에 맞게 데이터 변환
                        mongo_concept = {
                            "_id": ObjectId(),  # 새로운 ObjectId 생성
                            "conceptId": concept_data.get("conceptId", ""),
                            "unitId": concept_data.get("unitId", ""),
                            "blocks": concept_data.get("blocks", []),
                            "createdAt": datetime.fromisoformat(concept_data.get("createdAt", "2025-08-28T06:14:18Z").replace("Z", "+00:00"))
                        }
                        
                        concepts_data.append(mongo_concept)
                        
                    except json.JSONDecodeError as e:
                        print(f"⚠️ JSON 파싱 오류 (줄 {line_num}): {e}")
                        print(f"   문제가 된 줄: {line[:100]}...")
                        continue
                    except Exception as e:
                        print(f"⚠️ 데이터 처리 오류 (줄 {line_num}): {e}")
                        continue
            
            print(f"📋 총 {len(concepts_data)}개의 concept 데이터를 읽었습니다.")
            
            if not concepts_data:
                print("❌ 저장할 데이터가 없습니다.")
                return False
            
            # MongoDB에 데이터 저장
            print("💾 MongoDB에 데이터 저장 시작...")
            
            # 기존 데이터 삭제 (선택사항)
            if existing_count > 0:
                print("🗑️ 기존 concept 데이터 삭제 중...")
                result = concept_collection.delete_many({})
                print(f"   삭제된 문서 수: {result.deleted_count}")
            
            # 새 데이터 삽입
            result = concept_collection.insert_many(concepts_data)
            print(f"✅ {len(result.inserted_ids)}개의 concept 데이터 저장 완료!")
            
            # 저장된 데이터 확인
            final_count = concept_collection.count_documents({})
            print(f"📊 최종 concept 컬렉션 문서 수: {final_count}")
            
            # 샘플 데이터 출력
            print("\n📋 저장된 데이터 샘플:")
            sample_concepts = concept_collection.find().limit(3)
            for i, concept in enumerate(sample_concepts, 1):
                print(f"  {i}. {concept['conceptId']} - {concept['unitId']} (블록 수: {len(concept['blocks'])})")
                # 첫 번째 블록의 제목 출력
                if concept['blocks']:
                    first_block = concept['blocks'][0]
                    print(f"     첫 번째 블록: {first_block.get('title', 'N/A')} ({first_block.get('type', 'N/A')})")
            
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
            
            concept_collection = self.db.concept
            
            # 전체 문서 수 확인
            total_count = concept_collection.count_documents({})
            print(f"📊 전체 concept 문서 수: {total_count}")
            
            # unitId별 통계
            unit_stats = concept_collection.aggregate([
                {"$group": {"_id": "$unitId", "count": {"$sum": 1}}},
                {"$sort": {"_id": 1}}
            ])
            
            print("\n📚 unitId별 concept 수:")
            for stat in unit_stats:
                print(f"  {stat['_id']}: {stat['count']}개")
            
            # 블록 타입별 통계
            block_types = {}
            concepts = concept_collection.find()
            for concept in concepts:
                for block in concept.get('blocks', []):
                    block_type = block.get('type', 'unknown')
                    block_types[block_type] = block_types.get(block_type, 0) + 1
            
            print("\n🔧 블록 타입별 통계:")
            for block_type, count in sorted(block_types.items()):
                print(f"  {block_type}: {count}개")
            
            # 연습문제 통계
            practice_count = 0
            total_problems = 0
            concepts = concept_collection.find()
            for concept in concepts:
                for block in concept.get('blocks', []):
                    if block.get('type') == 'practiceProblems':
                        practice_count += 1
                        problems = block.get('problems', [])
                        total_problems += len(problems)
            
            print(f"\n📝 연습문제 블록: {practice_count}개")
            print(f"📝 총 연습문제 수: {total_problems}개")
            
            # 인덱스 확인
            indexes = list(concept_collection.list_indexes())
            print(f"\n🔍 인덱스 수: {len(indexes)}")
            for idx in indexes:
                print(f"  - {idx.get('name', 'unnamed')}: {list(idx['key'])}")
            
            print("✅ 데이터 검증 완료!")
            return True
            
        except Exception as e:
            print(f"❌ 데이터 검증 실패: {e}")
            return False
    
    def verify_unit_relationships(self):
        """unit 컬렉션과의 관계 검증"""
        try:
            print("\n🔗 Unit 컬렉션과의 관계 검증...")
            
            concept_collection = self.db.concept
            unit_collection = self.db.unit
            
            # concept에 있는 unitId들이 실제 unit 컬렉션에 존재하는지 확인
            concept_unit_ids = set()
            concepts = concept_collection.find({}, {"unitId": 1})
            for concept in concepts:
                concept_unit_ids.add(concept['unitId'])
            
            unit_ids = set()
            units = unit_collection.find({}, {"unitId": 1})
            for unit in units:
                unit_ids.add(unit['unitId'])
            
            # 교집합과 차집합 확인
            common_ids = concept_unit_ids & unit_ids
            concept_only = concept_unit_ids - unit_ids
            unit_only = unit_ids - concept_unit_ids
            
            print(f"📊 Unit ID 통계:")
            print(f"  - Concept에 있는 Unit ID: {len(concept_unit_ids)}개")
            print(f"  - Unit 컬렉션에 있는 Unit ID: {len(unit_ids)}개")
            print(f"  - 공통 Unit ID: {len(common_ids)}개")
            
            if concept_only:
                print(f"  ⚠️ Concept에만 있는 Unit ID: {len(concept_only)}개")
                print(f"    예시: {list(concept_only)[:5]}")
            
            if unit_only:
                print(f"  ⚠️ Unit 컬렉션에만 있는 Unit ID: {len(unit_only)}개")
                print(f"    예시: {list(unit_only)[:5]}")
            
            # 매칭률 계산
            if concept_unit_ids:
                match_rate = len(common_ids) / len(concept_unit_ids) * 100
                print(f"  📈 Unit ID 매칭률: {match_rate:.1f}%")
            
            return True
            
        except Exception as e:
            print(f"❌ 관계 검증 실패: {e}")
            return False
    
    def run(self):
        """전체 프로세스 실행"""
        if not self.connect():
            return False
        
        try:
            success = self.load_concept_data()
            if success:
                self.verify_data()
                self.verify_unit_relationships()
                print("\n🎉 Concept 데이터 로드 완료!")
            else:
                print("\n❌ Concept 데이터 로드 실패!")
            
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
    print("🚀 Concept 데이터 로드 시작")
    print("=" * 60)
    
    try:
        loader = ConceptDataLoader()
        loader.run()
        
    except Exception as e:
        print(f"❌ 스크립트 실행 실패: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
