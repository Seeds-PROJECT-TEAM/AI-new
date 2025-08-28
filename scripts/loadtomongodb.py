#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MongoDB 데이터 로더
개념.txt, 진단테스트.txt, 단원테스트_full버전.txt 파일을 MongoDB에 저장합니다.
"""

import json
import os
from datetime import datetime
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, BulkWriteError
import logging

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('mongodb_loader.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class MongoDBLoader:
    def __init__(self, connection_string="mongodb://localhost:27017/"):
        """MongoDB 연결 초기화"""
        self.client = None
        self.db = None
        self.connection_string = connection_string
        
    def connect(self, database_name="seeds_db"):
        """MongoDB에 연결"""
        try:
            self.client = MongoClient(self.connection_string)
            # 연결 테스트
            self.client.admin.command('ping')
            self.db = self.client[database_name]
            logger.info(f"MongoDB 연결 성공: {database_name}")
            return True
        except ConnectionFailure as e:
            logger.error(f"MongoDB 연결 실패: {e}")
            return False
    
    def disconnect(self):
        """MongoDB 연결 해제"""
        if self.client:
            self.client.close()
            logger.info("MongoDB 연결 해제")
    
    def load_concepts(self, file_path):
        """개념 데이터 로드 및 저장"""
        try:
            logger.info(f"개념 데이터 로드 시작: {file_path}")
            
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            
            if 'concepts' not in data:
                logger.error("개념 데이터에 'concepts' 키가 없습니다.")
                return False
            
            collection = self.db.concepts
            # 기존 데이터 삭제
            collection.delete_many({})
            logger.info("기존 개념 데이터 삭제 완료")
            
            # 새 데이터 삽입
            result = collection.insert_many(data['concepts'])
            logger.info(f"개념 데이터 저장 완료: {len(result.inserted_ids)}개")
            
            # 인덱스 생성
            collection.create_index("conceptId", unique=True)
            collection.create_index("unitId")
            collection.create_index("unitCode")
            logger.info("개념 컬렉션 인덱스 생성 완료")
            
            return True
            
        except Exception as e:
            logger.error(f"개념 데이터 로드 실패: {e}")
            return False
    
    def load_diagnostic_tests(self, file_path):
        """진단테스트 데이터 로드 및 저장"""
        try:
            logger.info(f"진단테스트 데이터 로드 시작: {file_path}")
            
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            
            if 'sets' not in data:
                logger.error("진단테스트 데이터에 'sets' 키가 없습니다.")
                return False
            
            collection = self.db.diagnostic_tests
            # 기존 데이터 삭제
            collection.delete_many({})
            logger.info("기존 진단테스트 데이터 삭제 완료")
            
            # 새 데이터 삽입
            result = collection.insert_many(data['sets'])
            logger.info(f"진단테스트 데이터 저장 완료: {len(result.inserted_ids)}개")
            
            # 인덱스 생성
            collection.create_index("test.testId", unique=True)
            collection.create_index("test.userId")
            collection.create_index("problems.unitId")
            logger.info("진단테스트 컬렉션 인덱스 생성 완료")
            
            return True
            
        except Exception as e:
            logger.error(f"진단테스트 데이터 로드 실패: {e}")
            return False
    
    def load_unit_tests(self, file_path):
        """단원테스트 데이터 로드 및 저장"""
        try:
            logger.info(f"단원테스트 데이터 로드 시작: {file_path}")
            
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            
            if 'units' not in data:
                logger.error("단원테스트 데이터에 'units' 키가 없습니다.")
                return False
            
            collection = self.db.unit_tests
            # 기존 데이터 삭제
            collection.delete_many({})
            logger.info("기존 단원테스트 데이터 삭제 완료")
            
            # 새 데이터 삽입
            result = collection.insert_many(data['units'])
            logger.info(f"단원테스트 데이터 저장 완료: {len(result.inserted_ids)}개")
            
            # 인덱스 생성
            collection.create_index("code", unique=True)
            collection.create_index("problems.problemId")
            collection.create_index("problems.unitId")
            logger.info("단원테스트 컬렉션 인덱스 생성 완료")
            
            return True
            
        except Exception as e:
            logger.error(f"단원테스트 데이터 로드 실패: {e}")
            return False
    
    def get_collection_stats(self):
        """컬렉션별 통계 정보 출력"""
        try:
            collections = ['concepts', 'diagnostic_tests', 'unit_tests']
            stats = {}
            
            for collection_name in collections:
                if collection_name in self.db.list_collection_names():
                    collection = self.db[collection_name]
                    count = collection.count_documents({})
                    stats[collection_name] = count
                    logger.info(f"{collection_name}: {count}개 문서")
                else:
                    stats[collection_name] = 0
                    logger.warning(f"{collection_name}: 컬렉션이 존재하지 않습니다.")
            
            return stats
            
        except Exception as e:
            logger.error(f"통계 정보 조회 실패: {e}")
            return {}
    
    def load_all_data(self, data_dir="AI/data"):
        """모든 데이터 로드"""
        try:
            logger.info("전체 데이터 로드 시작")
            
            # 파일 경로 설정
            concepts_file = os.path.join(data_dir, "개념.txt")
            diagnostic_file = os.path.join(data_dir, "진단테스트.txt")
            unit_test_file = os.path.join(data_dir, "단원테스트_full버전.txt")
            
            # 파일 존재 확인
            files_to_check = [concepts_file, diagnostic_file, unit_test_file]
            for file_path in files_to_check:
                if not os.path.exists(file_path):
                    logger.error(f"파일을 찾을 수 없습니다: {file_path}")
                    return False
            
            # 각 데이터 타입별로 로드
            success_count = 0
            
            if self.load_concepts(concepts_file):
                success_count += 1
            
            if self.load_diagnostic_tests(diagnostic_file):
                success_count += 1
            
            if self.load_unit_tests(unit_test_file):
                success_count += 1
            
            logger.info(f"데이터 로드 완료: {success_count}/3 성공")
            
            # 통계 정보 출력
            self.get_collection_stats()
            
            return success_count == 3
            
        except Exception as e:
            logger.error(f"전체 데이터 로드 실패: {e}")
            return False

def main():
    """메인 함수"""
    # MongoDB 연결 설정 (필요에 따라 수정)
    connection_string = "mongodb://localhost:27017/"
    database_name = "seeds_db"
    
    # 환경변수에서 설정 가져오기 (선택사항)
    if os.getenv('MONGODB_URI'):
        connection_string = os.getenv('MONGODB_URI')
    if os.getenv('MONGODB_DB'):
        database_name = os.getenv('MONGODB_DB')
    
    loader = MongoDBLoader(connection_string)
    
    try:
        # MongoDB 연결
        if not loader.connect(database_name):
            logger.error("MongoDB 연결에 실패했습니다.")
            return
        
        # 데이터 로드
        if loader.load_all_data():
            logger.info("모든 데이터 로드가 성공적으로 완료되었습니다.")
        else:
            logger.error("일부 데이터 로드에 실패했습니다.")
            
    except KeyboardInterrupt:
        logger.info("사용자에 의해 중단되었습니다.")
    except Exception as e:
        logger.error(f"예상치 못한 오류가 발생했습니다: {e}")
    finally:
        # 연결 해제
        loader.disconnect()

if __name__ == "__main__":
    main()
