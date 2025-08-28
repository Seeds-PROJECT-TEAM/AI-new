#!/usr/bin/env python3
"""MongoDB 데이터 확인 스크립트"""

from AI.app.services.mongo_service import MongoService

def main():
    try:
        # MongoDB 서비스 초기화
        service = MongoService()
        print(f"MongoDB 연결 상태: {service.is_connected}")
        
        if not service.is_connected:
            print("❌ MongoDB에 연결할 수 없습니다.")
            return
        
        print(f"DB 객체 타입: {type(service._db)}")
        
        # 컬렉션 목록 확인
        collections = service._db.list_collection_names()
        print(f"컬렉션 목록: {collections}")
        
        # Problems 컬렉션 확인
        print("\n=== Problems 컬렉션 ===")
        problems_count = service._db.problems.count_documents({})
        print(f"총 문제 수: {problems_count}")
        
        if problems_count > 0:
            problems = list(service._db.problems.find().limit(3))
            for i, problem in enumerate(problems):
                print(f"문제 {i+1}: {problem}")
        else:
            print("문제 데이터가 없습니다.")
        
        # Units 컬렉션 확인
        print("\n=== Units 컬렉션 ===")
        units_count = service._db.units.count_documents({})
        print(f"총 단원 수: {units_count}")
        
        if units_count > 0:
            units = list(service._db.units.find().limit(3))
            for i, unit in enumerate(units):
                print(f"단원 {i+1}: {unit}")
        else:
            print("단원 데이터가 없습니다.")
            
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
