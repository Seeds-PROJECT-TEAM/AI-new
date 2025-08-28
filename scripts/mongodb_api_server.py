#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FastAPI MongoDB 데이터 로더 서버
개념.txt, 진단테스트.txt, 단원테스트_full버전.txt 파일을 MongoDB에 저장하는 API
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, BulkWriteError
import logging
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('mongodb_api.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# FastAPI 앱 생성
app = FastAPI(
    title="MongoDB 데이터 로더 API",
    description="개념, 진단테스트, 단원테스트 데이터를 MongoDB에 저장하는 API",
    version="1.0.0"
)

class MongoDBService:
    def __init__(self):
        self.client = None
        self.db = None
        
    def connect(self, connection_string: str, database_name: str) -> bool:
        """MongoDB에 연결"""
        try:
            self.client = MongoClient(connection_string)
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
    
    def load_concepts(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """개념 데이터 로드 및 저장"""
        try:
            logger.info("개념 데이터 로드 시작")
            
            if 'concepts' not in data:
                raise ValueError("개념 데이터에 'concepts' 키가 없습니다.")
            
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
    
    def load_diagnostic_tests(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """진단테스트 데이터 로드 및 저장"""
        try:
            logger.info("진단테스트 데이터 로드 시작")
            
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
    
    def load_unit_tests(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """단원테스트 데이터 로드 및 저장"""
        try:
            logger.info("단원테스트 데이터 로드 시작")
            
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
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """컬렉션별 통계 정보 조회"""
        try:
            collections = ['concepts', 'diagnostic_tests', 'unit_tests']
            stats = {}
            
            for collection_name in collections:
                if collection_name in self.db.list_collection_names():
                    collection = self.db[collection_name]
                    count = collection.count_documents({})
                    stats[collection_name] = count
                else:
                    stats[collection_name] = 0
            
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

# MongoDB 서비스 인스턴스
mongodb_service = MongoDBService()

@app.on_event("startup")
async def startup_event():
    """서버 시작 시 MongoDB 연결"""
    connection_string = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
    database_name = os.getenv('MONGODB_DB', 'seeds_db')
    
    if not mongodb_service.connect(connection_string, database_name):
        logger.warning("서버 시작 시 MongoDB 연결에 실패했습니다. API 호출 시 연결을 시도합니다.")

@app.on_event("shutdown")
async def shutdown_event():
    """서버 종료 시 MongoDB 연결 해제"""
    mongodb_service.disconnect()

@app.get("/")
async def root():
    """루트 엔드포인트"""
    return {
        "message": "MongoDB 데이터 로더 API",
        "version": "1.0.0",
        "endpoints": [
            "/docs - API 문서",
            "/load-concepts - 개념 데이터 로드",
            "/load-diagnostic-tests - 진단테스트 데이터 로드",
            "/load-unit-tests - 단원테스트 데이터 로드",
            "/load-all - 모든 데이터 로드",
            "/stats - 컬렉션 통계"
        ]
    }

@app.post("/load-concepts")
async def load_concepts(data: Dict[str, Any]):
    """개념 데이터 로드"""
    try:
        result = mongodb_service.load_concepts(data)
        if result["success"]:
            return JSONResponse(content=result, status_code=200)
        else:
            return JSONResponse(content=result, status_code=400)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"서버 오류: {str(e)}")

@app.post("/load-diagnostic-tests")
async def load_diagnostic_tests(data: Dict[str, Any]):
    """진단테스트 데이터 로드"""
    try:
        result = mongodb_service.load_diagnostic_tests(data)
        if result["success"]:
            return JSONResponse(content=result, status_code=200)
        else:
            return JSONResponse(content=result, status_code=400)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"서버 오류: {str(e)}")

@app.post("/load-unit-tests")
async def load_unit_tests(data: Dict[str, Any]):
    """단원테스트 데이터 로드"""
    try:
        result = mongodb_service.load_unit_tests(data)
        if result["success"]:
            return JSONResponse(content=result, status_code=200)
        else:
            return JSONResponse(content=result, status_code=400)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"서버 오류: {str(e)}")

@app.post("/load-all")
async def load_all_data():
    """모든 데이터 로드"""
    try:
        # 파일에서 데이터 읽기
        data_dir = "AI/data"
        concepts_file = os.path.join(data_dir, "개념.txt")
        diagnostic_file = os.path.join(data_dir, "진단테스트.txt")
        unit_test_file = os.path.join(data_dir, "단원테스트_full버전.txt")
        
        # 파일 존재 확인
        files_to_check = [concepts_file, diagnostic_file, unit_test_file]
        for file_path in files_to_check:
            if not os.path.exists(file_path):
                raise HTTPException(status_code=404, detail=f"파일을 찾을 수 없습니다: {file_path}")
        
        results = {}
        success_count = 0
        
        # 개념 데이터 로드
        with open(concepts_file, 'r', encoding='utf-8') as file:
            concepts_data = json.load(file)
            result = mongodb_service.load_concepts(concepts_data)
            results["concepts"] = result
            if result["success"]:
                success_count += 1
        
        # 진단테스트 데이터 로드
        with open(diagnostic_file, 'r', encoding='utf-8') as file:
            diagnostic_data = json.load(file)
            result = mongodb_service.load_diagnostic_tests(diagnostic_data)
            results["diagnostic_tests"] = result
            if result["success"]:
                success_count += 1
        
        # 단원테스트 데이터 로드
        with open(unit_test_file, 'r', encoding='utf-8') as file:
            unit_test_data = json.load(file)
            result = mongodb_service.load_unit_tests(unit_test_data)
            results["unit_tests"] = result
            if result["success"]:
                success_count += 1
        
        return {
            "success": success_count == 3,
            "message": f"데이터 로드 완료: {success_count}/3 성공",
            "results": results,
            "total_success": success_count
        }
        
    except Exception as e:
        logger.error(f"전체 데이터 로드 실패: {e}")
        raise HTTPException(status_code=500, detail=f"데이터 로드 실패: {str(e)}")

@app.get("/stats")
async def get_stats():
    """컬렉션 통계 조회"""
    try:
        result = mongodb_service.get_collection_stats()
        if result["success"]:
            return result
        else:
            return JSONResponse(content=result, status_code=400)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"통계 조회 실패: {str(e)}")

@app.post("/upload-file")
async def upload_file(
    file: UploadFile = File(...),
    data_type: str = Form(...)
):
    """파일 업로드를 통한 데이터 로드"""
    try:
        # 파일 내용 읽기
        content = await file.read()
        data = json.loads(content.decode('utf-8'))
        
        # 데이터 타입에 따라 처리
        if data_type == "concepts":
            result = mongodb_service.load_concepts(data)
        elif data_type == "diagnostic_tests":
            result = mongodb_service.load_diagnostic_tests(data)
        elif data_type == "unit_tests":
            result = mongodb_service.load_unit_tests(data)
        else:
            raise HTTPException(status_code=400, detail="지원하지 않는 데이터 타입입니다.")
        
        if result["success"]:
            return JSONResponse(content=result, status_code=200)
        else:
            return JSONResponse(content=result, status_code=400)
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"파일 업로드 실패: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
