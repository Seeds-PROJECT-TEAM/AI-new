import os
import sys
from dotenv import load_dotenv

# AI 디렉토리를 Python 경로에 추가
sys.path.append(os.path.join(os.path.dirname(__file__), 'AI'))

# 환경 변수 로드
load_dotenv('AI/.env')

from AI.app.services.mongo_service import MongoService

def check_problems_detail():
    try:
        # MongoDB 서비스 초기화
        mongo_service = MongoService()
        
        if not mongo_service.is_connected:
            print("❌ MongoDB 연결 실패")
            return
        
        print("✅ MongoDB 연결 성공")
        print()
        
        # problems 컬렉션에서 모든 문제 조회
        problems_collection = mongo_service._db.problems
        problems = list(problems_collection.find())
        
        print(f"📚 총 {len(problems)}개의 문제 발견:")
        print()
        
        for i, problem in enumerate(problems, 1):
            print(f"🔍 문제 {i}:")
            print(f"   _id: {problem.get('_id')}")
            print(f"   problem_id: {problem.get('problem_id')}")
            print(f"   unitId: {problem.get('unitId')}")
            print(f"   grade: {problem.get('grade')}")
            print(f"   chapter: {problem.get('chapter')}")
            print(f"   context: {problem.get('context')}")
            print(f"   cognitiveType: {problem.get('cognitiveType')}")
            print(f"   level: {problem.get('level')}")
            print(f"   type: {problem.get('type')}")
            print(f"   tags: {problem.get('tags')}")
            content = problem.get('content')
            if content:
                if isinstance(content, str):
                    print(f"   content: {content[:100]}...")
                else:
                    print(f"   content: {content}")
            else:
                print(f"   content: N/A")
            print()
        
        # units 컬렉션도 확인
        print("📚 Units 컬렉션 확인:")
        units_collection = mongo_service._db.units
        units = list(units_collection.find())
        
        for i, unit in enumerate(units, 1):
            print(f"  {i}. unitId: {unit.get('unitId')}")
            print(f"     subject: {unit.get('subject')}")
            print(f"     title: {unit.get('title')}")
            print(f"     grade: {unit.get('grade')}")
            print(f"     chapter: {unit.get('chapter')}")
            print(f"     chapterTitle: {unit.get('chapterTitle')}")
            print()
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_problems_detail()
