import os
import sys
from dotenv import load_dotenv

# AI 디렉토리를 Python 경로에 추가
sys.path.append(os.path.join(os.path.dirname(__file__), 'AI'))

# 환경 변수 로드
load_dotenv('AI/.env')

from AI.app.services.mongo_service import MongoService

def check_collections():
    try:
        # MongoDB 서비스 초기화
        mongo_service = MongoService()
        
        if not mongo_service.is_connected:
            print("❌ MongoDB 연결 실패")
            return
        
        print("✅ MongoDB 연결 성공")
        print(f"📊 데이터베이스: {mongo_service._db.name}")
        print()
        
        # 모든 컬렉션 목록 조회
        collections = mongo_service._db.list_collection_names()
        print(f"📚 총 {len(collections)}개의 컬렉션 발견:")
        
        for i, collection_name in enumerate(collections, 1):
            print(f"  {i}. {collection_name}")
            
            # 각 컬렉션의 문서 수 확인
            try:
                count = mongo_service._db[collection_name].count_documents({})
                print(f"     📄 문서 수: {count}")
                
                # 컬렉션에 데이터가 있으면 샘플 문서 확인
                if count > 0:
                    sample = mongo_service._db[collection_name].find_one()
                    if sample:
                        print(f"     📋 샘플 필드: {list(sample.keys())}")
                        
                        # problems 컬렉션이면 문제 ID와 단원 정보 확인
                        if collection_name == "problems":
                            print(f"     🔍 문제 데이터 샘플:")
                            problems = list(mongo_service._db[collection_name].find().limit(3))
                            for j, problem in enumerate(problems, 1):
                                print(f"        {j}. ID: {problem.get('problemId', 'N/A')}")
                                print(f"           단원: {problem.get('unit', 'N/A')}")
                                print(f"           제목: {problem.get('title', 'N/A')}")
                                print()
                
            except Exception as e:
                print(f"     ❌ 컬렉션 조회 실패: {e}")
            
            print()
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_collections()
