#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MongoDB 데이터 검증 스크립트
저장된 데이터가 제대로 들어갔는지 확인
"""

import json
import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv
import logging

# AI/.env 파일에서 환경변수 로드
load_dotenv("AI/.env")

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MongoDBVerifier:
    def __init__(self):
        self.client = None
        self.db = None
        
    def connect(self) -> bool:
        """MongoDB에 연결"""
        try:
            mongodb_uri = os.getenv('MONGODB_URI')
            if not mongodb_uri:
                logger.error("MONGODB_URI 환경변수를 찾을 수 없습니다.")
                return False
            
            self.client = MongoClient(mongodb_uri)
            self.client.admin.command('ping')
            
            if 'nerdmath' in mongodb_uri:
                self.db = self.client.nerdmath
            else:
                self.db = self.client.seeds_db
                
            logger.info("MongoDB 연결 성공!")
            return True
            
        except Exception as e:
            logger.error(f"MongoDB 연결 실패: {e}")
            return False
    
    def disconnect(self):
        """MongoDB 연결 해제"""
        if self.client:
            self.client.close()
    
    def verify_concepts(self):
        """개념 데이터 검증"""
        print("\n🔍 개념 데이터 검증")
        print("=" * 50)
        
        collection = self.db.concepts
        count = collection.count_documents({})
        print(f"총 개념 문서 수: {count}")
        
        if count > 0:
            # 첫 번째 문서 조회
            first_doc = collection.find_one({})
            print(f"\n첫 번째 개념 문서:")
            print(f"  conceptId: {first_doc.get('conceptId', 'N/A')}")
            print(f"  unitId: {first_doc.get('unitId', 'N/A')}")
            print(f"  unitCode: {first_doc.get('unitCode', 'N/A')}")
            print(f"  unitTitle: {first_doc.get('unitTitle', 'N/A')}")
            
            # blocks 정보 확인
            if 'blocks' in first_doc:
                print(f"  blocks 수: {len(first_doc['blocks'])}")
                if first_doc['blocks']:
                    first_block = first_doc['blocks'][0]
                    print(f"  첫 번째 block type: {first_block.get('type', 'N/A')}")
                    print(f"  첫 번째 block title: {first_block.get('title', 'N/A')}")
            
            # 인덱스 확인
            indexes = list(collection.list_indexes())
            print(f"\n인덱스 정보:")
            for idx in indexes:
                print(f"  {idx['name']}: {idx['key']}")
    
    def verify_diagnostic_tests(self):
        """진단테스트 데이터 검증"""
        print("\n🔍 진단테스트 데이터 검증")
        print("=" * 50)
        
        collection = self.db.diagnostic_tests
        count = collection.count_documents({})
        print(f"총 진단테스트 문서 수: {count}")
        
        if count > 0:
            # 첫 번째 문서 조회
            first_doc = collection.find_one({})
            print(f"\n첫 번째 진단테스트 문서:")
            if 'test' in first_doc:
                test_info = first_doc['test']
                print(f"  testId: {test_info.get('testId', 'N/A')}")
                print(f"  userId: {test_info.get('userId', 'N/A')}")
                print(f"  gradeRange: {test_info.get('gradeRange', 'N/A')}")
            
            if 'problems' in first_doc:
                print(f"  problems 수: {len(first_doc['problems'])}")
                if first_doc['problems']:
                    first_problem = first_doc['problems'][0]
                    print(f"  첫 번째 problem unitId: {first_problem.get('unitId', 'N/A')}")
                    print(f"  첫 번째 problem type: {first_problem.get('type', 'N/A')}")
            
            # 인덱스 확인
            indexes = list(collection.list_indexes())
            print(f"\n인덱스 정보:")
            for idx in indexes:
                print(f"  {idx['name']}: {idx['key']}")
    
    def verify_unit_tests(self):
        """단원테스트 데이터 검증"""
        print("\n🔍 단원테스트 데이터 검증")
        print("=" * 50)
        
        collection = self.db.unit_tests
        count = collection.count_documents({})
        print(f"총 단원테스트 문서 수: {count}")
        
        if count > 0:
            # 첫 번째 문서 조회
            first_doc = collection.find_one({})
            print(f"\n첫 번째 단원테스트 문서:")
            print(f"  code: {first_doc.get('code', 'N/A')}")
            print(f"  title: {first_doc.get('title', 'N/A')}")
            
            if 'problems' in first_doc:
                print(f"  problems 수: {len(first_doc['problems'])}")
                if first_doc['problems']:
                    first_problem = first_doc['problems'][0]
                    print(f"  첫 번째 problem problemId: {first_problem.get('problemId', 'N/A')}")
                    print(f"  첫 번째 problem unitId: {first_problem.get('unitId', 'N/A')}")
                    print(f"  첫 번째 problem type: {first_problem.get('type', 'N/A')}")
                    
                    # content 확인
                    if 'content' in first_problem:
                        content = first_problem['content']
                        if 'korean' in content:
                            korean = content['korean']
                            print(f"  첫 번째 problem 한국어 문제: {korean.get('stem', 'N/A')[:100]}...")
            
            # 인덱스 확인
            indexes = list(collection.list_indexes())
            print(f"\n인덱스 정보:")
            for idx in indexes:
                print(f"  {idx['name']}: {idx['key']}")
    
    def verify_specific_problem(self):
        """특정 문제 ID로 검증"""
        print("\n🔍 특정 문제 검증 (d224c6982b594531976e5aec)")
        print("=" * 50)
        
        # unit_tests에서 검색
        unit_collection = self.db.unit_tests
        problem = unit_collection.find_one({"problems.problemId": "d224c6982b594531976e5aec"})
        
        if problem:
            print("✅ 단원테스트에서 문제를 찾았습니다!")
            print(f"단원 코드: {problem.get('code')}")
            print(f"단원 제목: {problem.get('title')}")
            
            # 해당 문제 찾기
            for p in problem['problems']:
                if p['problemId'] == "d224c6982b594531976e5aec":
                    print(f"\n문제 상세:")
                    print(f"  problemId: {p['problemId']}")
                    print(f"  unitId: {p['unitId']}")
                    print(f"  type: {p['type']}")
                    if 'content' in p and 'korean' in p['content']:
                        print(f"  한국어 문제: {p['content']['korean']['stem']}")
                    break
        else:
            print("❌ 해당 문제 ID를 찾을 수 없습니다.")
        
        # diagnostic_tests에서도 검색
        diag_collection = self.db.diagnostic_tests
        diag_problem = diag_collection.find_one({"problems.problemId": "d224c6982b594531976e5aec"})
        
        if diag_problem:
            print("\n✅ 진단테스트에서도 문제를 찾았습니다!")
        else:
            print("\n❌ 진단테스트에서는 해당 문제를 찾을 수 없습니다.")
    
    def verify_all_collections(self):
        """모든 컬렉션 검증"""
        print("🚀 MongoDB 데이터 검증 시작")
        print("=" * 60)
        
        # 컬렉션 목록 확인
        collections = self.db.list_collection_names()
        print(f"데이터베이스에 있는 컬렉션: {collections}")
        
        # 각 컬렉션별 검증
        self.verify_concepts()
        self.verify_diagnostic_tests()
        self.verify_unit_tests()
        self.verify_specific_problem()
        
        print("\n" + "=" * 60)
        print("🏁 검증 완료!")

def main():
    verifier = MongoDBVerifier()
    
    try:
        if not verifier.connect():
            return
        
        verifier.verify_all_collections()
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
    finally:
        verifier.disconnect()

if __name__ == "__main__":
    main()
