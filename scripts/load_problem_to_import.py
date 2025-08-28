#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
problem_to_import.txt 파일의 데이터를 MongoDB nerdmath 데이터베이스의 problem 컬렉션에 저장하는 스크립트
테이블 정의서의 problem 필드와 정확히 매칭되도록 검증하고 저장합니다.
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

# AI 디렉토리를 Python 경로에 추가
AI_DIR = Path(__file__).parent
sys.path.insert(0, str(AI_DIR))

# .env 파일 로드
load_dotenv(AI_DIR / ".env")

class ProblemImportLoader:
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
    
    def load_problem_data(self):
        """problem_to_import.txt 파일에서 문제 데이터 로드"""
        problems = []
        file_path = AI_DIR / "data" / "problem_to_import.txt"
        
        try:
            print(f"📖 problem_to_import.txt 파일 읽는 중: {file_path}")
            
            with open(file_path, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if not line:
                        continue
                    
                    try:
                        # JSON 파싱
                        problem = json.loads(line)
                        
                        # 데이터 검증 및 정리
                        validated_problem = self.validate_and_clean_problem(problem, line_num)
                        if validated_problem:
                            problems.append(validated_problem)
                        
                    except json.JSONDecodeError as e:
                        print(f"⚠️ 라인 {line_num} JSON 파싱 오류: {e}")
                        continue
                    except Exception as e:
                        print(f"⚠️ 라인 {line_num} 처리 오류: {e}")
                        continue
            
            print(f"✅ 총 {len(problems)}개 문제 데이터 로드 완료")
            return problems
            
        except Exception as e:
            print(f"❌ 파일 읽기 실패: {e}")
            return []
    
    def validate_and_clean_problem(self, problem, line_num):
        """문제 데이터 검증 및 정리"""
        try:
            # 1. 필수 필드 검증 (테이블 정의서 기준)
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
                print(f"⚠️ 라인 {line_num}: 필수 필드 누락 - {missing_fields}")
                return None
            
            # 2. 데이터 타입 검증 및 변환
            cleaned_problem = {}
            
            # problemId: string (ObjectId가 아닌)
            cleaned_problem["problemId"] = str(problem["problemId"])
            
            # unitId: string (unit 컬렉션과 연결)
            cleaned_problem["unitId"] = str(problem["unitId"])
            
            # grade: number
            cleaned_problem["grade"] = int(problem["grade"])
            
            # chapter: number
            cleaned_problem["chapter"] = int(problem["chapter"])
            
            # context: object
            cleaned_problem["context"] = problem["context"]
            
            # cognitiveType: string
            cleaned_problem["cognitiveType"] = str(problem["cognitiveType"])
            
            # level: string
            cleaned_problem["level"] = str(problem["level"])
            
            # diagnosticTest: bool
            cleaned_problem["diagnosticTest"] = bool(problem["diagnosticTest"])
            
            # type: string
            cleaned_problem["type"] = str(problem["type"])
            
            # tags: array
            cleaned_problem["tags"] = list(problem["tags"])
            
            # content: object
            cleaned_problem["content"] = problem["content"]
            
            # correctAnswer: string
            cleaned_problem["correctAnswer"] = str(problem["correctAnswer"])
            
            # explanation: object
            cleaned_problem["explanation"] = problem["explanation"]
            
            # imageUrl: string (선택적)
            if "imageUrl" in problem:
                cleaned_problem["imageUrl"] = str(problem["imageUrl"])
            
            # createdAt, updatedAt: date
            try:
                cleaned_problem["createdAt"] = datetime.fromisoformat(
                    problem["createdAt"].replace("Z", "+00:00")
                )
                cleaned_problem["updatedAt"] = datetime.fromisoformat(
                    problem["updatedAt"].replace("Z", "+00:00")
                )
            except Exception as e:
                print(f"⚠️ 라인 {line_num}: 날짜 변환 오류 - {e}")
                return None
            
            # 3. 추가 필드들 (선택적)
            if "diagnosticUnit" in problem:
                cleaned_problem["diagnosticUnit"] = str(problem["diagnosticUnit"])
            
            if "promptVersion" in problem:
                cleaned_problem["promptVersion"] = str(problem["promptVersion"])
            
            if "subunit" in problem:
                cleaned_problem["subunit"] = str(problem["subunit"])
            
            return cleaned_problem
            
        except Exception as e:
            print(f"⚠️ 라인 {line_num}: 데이터 검증/정리 오류 - {e}")
            return None
    
    def check_unit_references(self, problems):
        """unit 컬렉션과의 참조 무결성 확인"""
        try:
            unit_collection = self.db.unit
            valid_unit_ids = set(unit_collection.distinct("unitId"))
            
            invalid_references = []
            valid_problems = []
            
            for problem in problems:
                if problem["unitId"] in valid_unit_ids:
                    valid_problems.append(problem)
                else:
                    invalid_references.append(problem["unitId"])
            
            if invalid_references:
                print(f"⚠️ 유효하지 않은 unitId 참조: {len(set(invalid_references))}개")
                print(f"  - 예시: {list(set(invalid_references))[:5]}")
            
            print(f"✅ 유효한 unitId 참조: {len(valid_problems)}개")
            return valid_problems
            
        except Exception as e:
            print(f"❌ unit 참조 확인 실패: {e}")
            return problems
    
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
            duplicate_count = 0
            
            for i, problem in enumerate(problems, 1):
                try:
                    # 중복 확인 (problemId 기준)
                    existing = problem_collection.find_one({"problemId": problem["problemId"]})
                    if existing:
                        print(f"⚠️ 문제 ID 중복: {problem['problemId']}")
                        duplicate_count += 1
                        continue
                    
                    # MongoDB에 저장
                    result = problem_collection.insert_one(problem)
                    if result.inserted_id:
                        saved_count += 1
                        if saved_count % 10 == 0:
                            print(f"💾 {saved_count}개 문제 저장 완료...")
                    
                except DuplicateKeyError:
                    print(f"⚠️ 중복 키 오류: {problem['problemId']}")
                    duplicate_count += 1
                except Exception as e:
                    print(f"❌ 문제 저장 실패 (ID: {problem.get('problemId', 'unknown')}): {e}")
                    skipped_count += 1
            
            print(f"\n📊 문제 저장 완료!")
            print(f"✅ 새로 저장된 문제: {saved_count}개")
            print(f"⚠️ 건너뛴 문제: {skipped_count}개")
            print(f"🔄 중복 문제: {duplicate_count}개")
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
                [("problemId", 1)],
                [("unitId", 1)],
                [("grade", 1)],
                [("chapter", 1)],
                [("cognitiveType", 1)],
                [("level", 1)],
                [("diagnosticTest", 1)],
                [("type", 1)],
                [("tags", 1)],
                [("content.korean.stem", "text")],
                [("content.english.stem", "text")]
            ]
            
            for index_spec in indexes_to_create:
                try:
                    # 인덱스 이름 생성
                    if "text" in index_spec:
                        field_name = index_spec[0][0].replace(".", "_")
                        index_name = f"{field_name}_text_idx"
                    else:
                        field_name = index_spec[0][0]
                        index_name = f"{field_name}_idx"
                    
                    # 인덱스 생성
                    if "text" in index_spec:
                        # text 인덱스
                        problem_collection.create_index(index_spec, name=index_name)
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
    
    def load_and_save_problems(self):
        """문제 데이터를 로드하고 MongoDB에 저장"""
        try:
            # 1. 문제 데이터 로드
            problems = self.load_problem_data()
            if not problems:
                print("❌ 로드된 문제가 없습니다.")
                return False
            
            # 2. unit 참조 무결성 확인
            valid_problems = self.check_unit_references(problems)
            if not valid_problems:
                print("❌ 유효한 unit 참조가 없습니다.")
                return False
            
            # 3. MongoDB에 저장
            success = self.save_problems_to_mongodb(valid_problems)
            if success:
                # 4. 인덱스 생성
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
    print("🚀 Problem Import 데이터 MongoDB 저장 시작")
    print("=" * 60)
    
    loader = None
    try:
        loader = ProblemImportLoader()
        
        if not loader.connect():
            print("❌ MongoDB 연결 실패")
            return
        
        success = loader.load_and_save_problems()
        
        if success:
            print("\n🎉 Problem Import 데이터 MongoDB 저장 완료!")
        else:
            print("\n❌ Problem Import 데이터 저장 실패!")
            
    except Exception as e:
        print(f"❌ 스크립트 실행 실패: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        if loader:
            loader.close()

if __name__ == "__main__":
    main()
