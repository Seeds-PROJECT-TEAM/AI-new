#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
직접 MongoDB 데이터 로더
.env 파일의 MongoDB URI를 사용해서 개념, 진단테스트, 단원테스트 데이터를 직접 저장
"""

import json
import os
from datetime import datetime
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, BulkWriteError
import logging
from dotenv import load_dotenv

# AI/.env 파일에서 환경변수 로드
load_dotenv("AI/.env")

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('direct_mongodb_loader.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class DirectMongoDBLoader:
    def __init__(self):
        self.client = None
        self.db = None
        
    def connect(self) -> bool:
        """MongoDB에 연결"""
        try:
            # .env에서 MongoDB URI 가져오기
            mongodb_uri = os.getenv('MONGODB_URI')
            if not mongodb_uri:
                logger.error("MONGODB_URI 환경변수를 찾을 수 없습니다.")
                return False
            
            logger.info(f"MongoDB 연결 시도: {mongodb_uri.split('@')[1] if '@' in mongodb_uri else 'localhost'}")
            
            self.client = MongoClient(mongodb_uri)
            # 연결 테스트
            self.client.admin.command('ping')
            
            # 데이터베이스 이름 추출 (URI에서)
            if 'nerdmath' in mongodb_uri:
                self.db = self.client.nerdmath
                logger.info("nerdmath 데이터베이스에 연결")
            else:
                self.db = self.client.seeds_db
                logger.info("seeds_db 데이터베이스에 연결")
            
            logger.info("MongoDB 연결 성공!")
            return True
            
        except ConnectionFailure as e:
            logger.error(f"MongoDB 연결 실패: {e}")
            return False
        except Exception as e:
            logger.error(f"연결 중 오류 발생: {e}")
            return False
    
    def disconnect(self):
        """MongoDB 연결 해제"""
        if self.client:
            self.client.close()
            logger.info("MongoDB 연결 해제")
    
    def load_concepts(self, file_path: str) -> dict:
        """개념 데이터 로드 및 저장"""
        try:
            logger.info(f"개념 데이터 로드 시작: {file_path}")
            
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            
            if 'concepts' not in data:
                raise ValueError("개념 데이터에 'concepts' 키가 없습니다.")
            
            collection = self.db.concepts
            
            # 기존 인덱스 삭제
            try:
                collection.drop_indexes()
                logger.info("기존 개념 컬렉션 인덱스 삭제 완료")
            except Exception as e:
                logger.warning(f"인덱스 삭제 중 경고: {e}")
            
            # 기존 데이터 삭제
            collection.delete_many({})
            logger.info("기존 개념 데이터 삭제 완료")
            
            # 새 데이터 삽입
            result = collection.insert_many(data['concepts'])
            logger.info(f"개념 데이터 저장 완료: {len(result.inserted_ids)}개")
            
            # 새 인덱스 생성
            collection.create_index("conceptId", unique=True)
            collection.create_index("unitId")
            collection.create_index("unitCode")
            logger.info("개념 컬렉션 새 인덱스 생성 완료")
            
            return {
                "success": True,
                "message": f"개념 데이터 저장 완료: {len(result.inserted_ids)}개",
                "count": len(result.inserted_ids)
            }
            
        except Exception as e:
            logger.error(f"개념 데이터 로드 실패: {e}")
            return {
                "success": False,
                "message": f"개념 데이터 로드 실패: {str(e)}",
                "count": 0
            }
    
    def load_diagnostic_tests(self, file_path: str) -> dict:
        """진단테스트 데이터 로드 및 저장"""
        try:
            logger.info(f"진단테스트 데이터 로드 시작: {file_path}")
            
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            
            if 'sets' not in data:
                raise ValueError("진단테스트 데이터에 'sets' 키가 없습니다.")
            
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
            
            return {
                "success": True,
                "message": f"진단테스트 데이터 저장 완료: {len(result.inserted_ids)}개",
                "count": len(result.inserted_ids)
            }
            
        except Exception as e:
            logger.error(f"진단테스트 데이터 로드 실패: {e}")
            return {
                "success": False,
                "message": f"진단테스트 데이터 로드 실패: {str(e)}",
                "count": 0
            }
    
    def load_unit_tests(self, file_path: str) -> dict:
        """단원테스트 데이터 로드 및 저장"""
        try:
            logger.info(f"단원테스트 데이터 로드 시작: {file_path}")
            
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            
            if 'units' not in data:
                raise ValueError("단원테스트 데이터에 'units' 키가 없습니다.")
            
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
            
            return {
                "success": True,
                "message": f"단원테스트 데이터 저장 완료: {len(result.inserted_ids)}개",
                "count": len(result.inserted_ids)
            }
            
        except Exception as e:
            logger.error(f"단원테스트 데이터 로드 실패: {e}")
            return {
                "success": False,
                "message": f"단원테스트 데이터 로드 실패: {str(e)}",
                "count": 0
            }
    
    def get_collection_stats(self) -> dict:
        """컬렉션별 통계 정보 조회"""
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
            
            return {
                "success": True,
                "stats": stats
            }
            
        except Exception as e:
            logger.error(f"통계 정보 조회 실패: {e}")
            return {
                "success": False,
                "message": f"통계 정보 조회 실패: {str(e)}",
                "stats": {}
            }
    
    def load_all_data(self) -> dict:
        """모든 데이터 로드"""
        try:
            logger.info("전체 데이터 로드 시작")
            
            # 파일 경로 설정
            data_dir = "AI/data"
            concepts_file = os.path.join(data_dir, "개념.txt")
            diagnostic_file = os.path.join(data_dir, "진단테스트.txt")
            unit_test_file = os.path.join(data_dir, "단원테스트_full버전.txt")
            
            # 파일 존재 확인
            files_to_check = [concepts_file, diagnostic_file, unit_test_file]
            for file_path in files_to_check:
                if not os.path.exists(file_path):
                    logger.error(f"파일을 찾을 수 없습니다: {file_path}")
                    return {
                        "success": False,
                        "message": f"파일을 찾을 수 없습니다: {file_path}"
                    }
            
            results = {}
            success_count = 0
            
            # 개념 데이터 로드
            logger.info("=" * 50)
            result = self.load_concepts(concepts_file)
            results["concepts"] = result
            if result["success"]:
                success_count += 1
            
            # 진단테스트 데이터 로드
            logger.info("=" * 50)
            result = self.load_diagnostic_tests(diagnostic_file)
            results["diagnostic_tests"] = result
            if result["success"]:
                success_count += 1
            
            # 단원테스트 데이터 로드
            logger.info("=" * 50)
            result = self.load_unit_tests(unit_test_file)
            results["unit_tests"] = result
            if result["success"]:
                success_count += 1
            
            logger.info("=" * 50)
            logger.info(f"데이터 로드 완료: {success_count}/3 성공")
            
            # 통계 정보 출력
            self.get_collection_stats()
            
            return {
                "success": success_count == 3,
                "message": f"데이터 로드 완료: {success_count}/3 성공",
                "results": results,
                "total_success": success_count
            }
            
        except Exception as e:
            logger.error(f"전체 데이터 로드 실패: {e}")
            return {
                "success": False,
                "message": f"데이터 로드 실패: {str(e)}"
            }

def main():
    """메인 함수"""
    print("🚀 직접 MongoDB 데이터 로더 시작!")
    print("=" * 60)
    
    loader = DirectMongoDBLoader()
    
    try:
        # MongoDB 연결
        if not loader.connect():
            logger.error("MongoDB 연결에 실패했습니다.")
            return
        
        print("✅ MongoDB 연결 성공!")
        print("=" * 60)
        
        # 모든 데이터 로드
        result = loader.load_all_data()
        
        print("\n" + "=" * 60)
        if result["success"]:
            print("🎉 모든 데이터 로드가 성공적으로 완료되었습니다!")
        else:
            print("⚠️ 일부 데이터 로드에 실패했습니다.")
        
        print(f"📊 결과: {result['message']}")
        print(f"✅ 성공 개수: {result['total_success']}/3")
        
        # 상세 결과 출력
        if 'results' in result:
            print("\n📋 상세 결과:")
            for data_type, data_result in result['results'].items():
                status = "✅" if data_result['success'] else "❌"
                print(f"  {status} {data_type}: {data_result['message']}")
        
        print("=" * 60)
        
    except KeyboardInterrupt:
        print("\n⏹️ 사용자에 의해 중단되었습니다.")
    except Exception as e:
        logger.error(f"예상치 못한 오류가 발생했습니다: {e}")
        print(f"❌ 오류 발생: {e}")
    finally:
        # 연결 해제
        loader.disconnect()
        print("🏁 작업 완료!")

if __name__ == "__main__":
    main()
