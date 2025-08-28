#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
단원테스트_full버전.txt와 진단테스트.txt 파일의 problem 데이터를 MongoDB nerdmath 데이터베이스의 problem 컬렉션에 저장하는 스크립트
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

class ProblemDataLoader:
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
    
    def load_unit_test_problems(self):
        """단원테스트_full버전.txt에서 문제 데이터 로드"""
        problems = []
        file_path = AI_DIR / "data" / "단원테스트_full버전.txt"
        
        try:
            print(f"📖 단원테스트 파일 읽는 중: {file_path}")
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            data = json.loads(content)
            
            for unit in data.get("units", []):
                unit_code = unit.get("code", "")
                unit_title = unit.get("title", "")
                
                for problem in unit.get("problems", []):
                    # problemId를 string으로 변환 (ObjectId가 아닌)
                    problem["problemId"] = str(problem["problemId"])
                    
                    # unitId를 string으로 변환 (예: "3.1" -> "unit_03_01")
                    unit_id = problem.get("unitId", "")
                    if unit_id and "." in unit_id:
                        grade, chapter = unit_id.split(".")
                        problem["unitId"] = f"unit_{grade.zfill(2)}_{chapter.zfill(2)}"
                    
                    # diagnosticTest 필드 추가 (단원테스트는 false)
                    problem["diagnosticTest"] = False
                    
                    # createdAt, updatedAt을 date 타입으로 변환
                    if "createdAt" in problem:
                        problem["createdAt"] = datetime.fromisoformat(problem["createdAt"].replace("Z", "+00:00"))
                    if "updatedAt" in problem:
                        problem["updatedAt"] = datetime.fromisoformat(problem["updatedAt"].replace("Z", "+00:00"))
                    
                    problems.append(problem)
            
            print(f"✅ 단원테스트에서 {len(problems)}개 문제 로드 완료")
            return problems
            
        except Exception as e:
            print(f"❌ 단원테스트 파일 읽기 실패: {e}")
            return []
    
    def load_diagnostic_test_problems(self):
        """진단테스트.txt에서 문제 데이터 로드"""
        problems = []
        file_path = AI_DIR / "data" / "진단테스트.txt"
        
        try:
            print(f"📖 진단테스트 파일 읽는 중: {file_path}")
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            data = json.loads(content)
            
            for test_set in data.get("sets", []):
                for problem in test_set.get("problems", []):
                    # problemId를 string으로 변환
                    problem["problemId"] = str(problem["problemId"])
                    
                    # unitId를 string으로 변환 (예: "3.3" -> "unit_03_03")
                    unit_id = problem.get("unitId", "")
                    if unit_id and "." in unit_id:
                        grade, chapter = unit_id.split(".")
                        problem["unitId"] = f"unit_{grade.zfill(2)}_{chapter.zfill(2)}"
                    
                    # diagnosticTest 필드가 이미 있으면 그대로 사용
                    if "diagnosticTest" not in problem:
                        problem["diagnosticTest"] = True
                    
                    # createdAt, updatedAt을 date 타입으로 변환
                    if "createdAt" in problem:
                        problem["createdAt"] = datetime.fromisoformat(problem["createdAt"].replace("Z", "+00:00"))
                    if "updatedAt" in problem:
                        problem["updatedAt"] = datetime.fromisoformat(problem["updatedAt"].replace("Z", "+00:00"))
                    
                    problems.append(problem)
            
            print(f"✅ 진단테스트에서 {len(problems)}개 문제 로드 완료")
            return problems
            
        except Exception as e:
            print(f"❌ 진단테스트 파일 읽기 실패: {e}")
            return []
    
    def validate_problem_data(self, problem):
        """문제 데이터의 필수 필드 검증"""
        required_fields = [
            "problemId", "unitId", "grade", "chapter", "context", 
            "cognitiveType", "level", "diagnosticTest", "type", 
            "tags", "content", "correctAnswer", "explanation", 
            "createdAt", "updatedAt"
        ]
        
        missing_fields = []
        for field in required_fields:
            if field not in problem:
                missing_fields.append(field)
        
        if missing_fields:
            print(f"⚠️ 필수 필드 누락: {missing_fields}")
            return False
        
        return True
    
    def save_problems_to_mongodb(self, problems):
        """문제들을 MongoDB problem 컬렉션에 저장"""
        if not problems:
            print("❌ 저장할 문제가 없습니다.")
            return False
        
        try:
            problem_collection = self.db.problem
            
            # 기존 데이터 확인
            existing_count = problem_collection.count_documents({})
            print(f"📊 기존 problem 컬렉션 문서 수: {existing_count}")
            
            # 문제 데이터 저장
            saved_count = 0
            skipped_count = 0
            
            for problem in problems:
                try:
                    # 필수 필드 검증
                    if not self.validate_problem_data(problem):
                        skipped_count += 1
                        continue
                    
                    # 중복 확인 (problemId 기준)
                    existing = problem_collection.find_one({"problemId": problem["problemId"]})
                    if existing:
                        print(f"⚠️ 문제 ID 중복: {problem['problemId']}")
                        skipped_count += 1
                        continue
                    
                    # MongoDB에 저장
                    result = problem_collection.insert_one(problem)
                    if result.inserted_id:
                        saved_count += 1
                        if saved_count % 100 == 0:
                            print(f"💾 {saved_count}개 문제 저장 완료...")
                    
                except Exception as e:
                    print(f"❌ 문제 저장 실패 (ID: {problem.get('problemId', 'unknown')}): {e}")
                    skipped_count += 1
            
            print(f"\n📊 문제 저장 완료!")
            print(f"✅ 새로 저장된 문제: {saved_count}개")
            print(f"⚠️ 건너뛴 문제: {skipped_count}개")
            print(f"📈 총 problem 컬렉션 문서 수: {problem_collection.count_documents({})}")
            
            return True
            
        except Exception as e:
            print(f"❌ MongoDB 저장 실패: {e}")
            return False
    
    def create_problem_indexes(self):
        """problem 컬렉션에 인덱스 생성"""
        try:
            problem_collection = self.db.problem
            
            # 기존 인덱스 확인
            existing_indexes = list(problem_collection.list_indexes())
            print(f"🔍 기존 인덱스 수: {len(existing_indexes)}")
            
            # 필요한 인덱스들
            indexes_to_create = [
                [("problemId", 1), ("unique", True)],
                [("unitId", 1)],
                [("grade", 1)],
                [("chapter", 1)],
                [("cognitiveType", 1)],
                [("level", 1)],
                [("diagnosticTest", 1)],
                [("type", 1)],
                [("tags", 1)],
                [("content.text", "text")]
            ]
            
            for index_spec in indexes_to_create:
                try:
                    # 인덱스 이름 생성
                    if "text" in index_spec:
                        index_name = "content_text_text_idx"
                    else:
                        field_names = [str(field[0]) for field in index_spec if field[0] != "unique"]
                        index_name = f"{'_'.join(field_names)}_idx"
                    
                    # 인덱스 생성
                    if "unique" in index_spec:
                        # unique 인덱스
                        fields = [field for field in index_spec if field[0] != "unique"]
                        problem_collection.create_index(fields, unique=True, name=index_name)
                    elif "text" in index_spec:
                        # text 인덱스
                        problem_collection.create_index([("content.text", "text")], name=index_name)
                    else:
                        # 일반 인덱스
                        problem_collection.create_index(index_spec, name=index_name)
                    
                    print(f"✅ 인덱스 '{index_name}' 생성 완료")
                    
                except Exception as e:
                    if "already exists" in str(e):
                        print(f"⚠️ 인덱스 '{index_name}' 이미 존재함")
                    else:
                        print(f"❌ 인덱스 '{index_name}' 생성 실패: {e}")
            
            print("🎉 problem 컬렉션 인덱스 생성 완료!")
            return True
            
        except Exception as e:
            print(f"❌ 인덱스 생성 실패: {e}")
            return False
    
    def load_and_save_all_problems(self):
        """모든 문제 데이터를 로드하고 MongoDB에 저장"""
        try:
            # 1. 단원테스트 문제 로드
            unit_problems = self.load_unit_test_problems()
            
            # 2. 진단테스트 문제 로드
            diagnostic_problems = self.load_diagnostic_test_problems()
            
            # 3. 모든 문제 합치기
            all_problems = unit_problems + diagnostic_problems
            print(f"\n📚 총 {len(all_problems)}개 문제 로드 완료")
            print(f"  - 단원테스트: {len(unit_problems)}개")
            print(f"  - 진단테스트: {len(diagnostic_problems)}개")
            
            # 4. MongoDB에 저장
            if all_problems:
                success = self.save_problems_to_mongodb(all_problems)
                if success:
                    # 5. 인덱스 생성
                    self.create_problem_indexes()
                    return True
            
            return False
            
        except Exception as e:
            print(f"❌ 문제 데이터 처리 실패: {e}")
            return False
    
    def close(self):
        """MongoDB 연결 종료"""
        if self.client:
            self.client.close()
            print("🔌 MongoDB 연결 종료")

def main():
    """메인 함수"""
    print("🚀 Problem 데이터 MongoDB 저장 시작")
    print("=" * 60)
    
    loader = None
    try:
        loader = ProblemDataLoader()
        
        if not loader.connect():
            print("❌ MongoDB 연결 실패")
            return
        
        success = loader.load_and_save_all_problems()
        
        if success:
            print("\n🎉 Problem 데이터 MongoDB 저장 완료!")
        else:
            print("\n❌ Problem 데이터 저장 실패!")
            
    except Exception as e:
        print(f"❌ 스크립트 실행 실패: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        if loader:
            loader.close()

if __name__ == "__main__":
    main()
