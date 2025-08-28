#!/usr/bin/env python3
"""MongoDB 문제 정보 조회 테스트"""

from AI.app.services.mongo_service import MongoService

def test_mongodb_lookup():
    try:
        print("=== MongoDB 문제 정보 조회 테스트 ===")
        
        # MongoDB 서비스 초기화
        mongo_service = MongoService()
        print(f"MongoDB 연결 상태: {mongo_service.is_connected}")
        
        if not mongo_service.is_connected:
            print("❌ MongoDB에 연결할 수 없습니다.")
            return
        
        # 문제 ID로 문제 정보 조회 테스트
        problem_id = "problem_001"
        print(f"\n🔍 문제 ID '{problem_id}'로 조회 시도...")
        
        # 직접 MongoDB에서 조회
        problems_collection = mongo_service._db.problems
        problem = problems_collection.find_one({"problem_id": problem_id})
        
        if problem:
            print(f"✅ MongoDB에서 문제 찾음:")
            print(f"   - problem_id: {problem.get('problem_id')}")
            print(f"   - unitId: {problem.get('unitId')}")
            print(f"   - grade: {problem.get('grade')}")
            print(f"   - chapter: {problem.get('chapter')}")
            
            # unitId로 단원 정보 조회
            unit_id = problem.get('unitId')
            if unit_id:
                units_collection = mongo_service._db.units
                unit = units_collection.find_one({"_id": unit_id})
                
                if unit:
                    print(f"\n✅ 단원 정보 찾음:")
                    print(f"   - unitId: {unit.get('unitId')}")
                    print(f"   - title.ko: {unit.get('title', {}).get('ko', 'N/A')}")
                    print(f"   - chapterTitle: {unit.get('chapterTitle', 'N/A')}")
                    print(f"   - grade: {unit.get('grade')}")
                else:
                    print(f"❌ unitId '{unit_id}'에 해당하는 단원을 찾을 수 없습니다.")
            else:
                print("❌ 문제에 unitId가 없습니다.")
        else:
            print(f"❌ problem_id '{problem_id}'에 해당하는 문제를 찾을 수 없습니다.")
            
        # 다른 문제 ID들도 테스트
        print(f"\n=== 다른 문제 ID들 테스트 ===")
        other_problem_ids = ["problem_002", "DIAG_001"]
        
        for other_id in other_problem_ids:
            print(f"\n🔍 문제 ID '{other_id}'로 조회 시도...")
            other_problem = problems_collection.find_one({"problem_id": other_id})
            
            if other_problem:
                print(f"✅ 문제 찾음: unitId = {other_problem.get('unitId')}")
            else:
                print(f"❌ 문제를 찾을 수 없음")
            
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_mongodb_lookup()
