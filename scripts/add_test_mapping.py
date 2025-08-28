#!/usr/bin/env python3
"""MongoDB concepts 컬렉션에 unitId 매핑을 위한 테스트 데이터 추가"""

import os
from dotenv import load_dotenv
import pymongo

def add_test_mapping():
    try:
        # .env 파일 로드
        load_dotenv('AI/.env')
        mongodb_uri = os.getenv('MONGODB_URI')
        
        # MongoDB 연결
        client = pymongo.MongoClient(mongodb_uri)
        db = client.nerdmath
        
        print('=== MongoDB concepts 컬렉션에 unitId 매핑 추가 ===')
        print()
        
        # 현재 concepts 컬렉션 확인
        print('1️⃣ 현재 concepts 컬렉션:')
        concepts = list(db.concepts.find())
        for concept in concepts:
            print(f'   unitCode: {concept.get("unitCode")}')
            print(f'   unitTitle: {concept.get("unitTitle")}')
            print(f'   ---')
        
        print()
        
        # problems 컬렉션의 unitId와 매핑
        print('2️⃣ problems 컬렉션의 unitId:')
        problems = list(db.problems.find())
        for prob in problems:
            print(f'   problem_id: {prob.get("problem_id")}')
            print(f'   unitId: {prob.get("unitId")}')
            print(f'   ---')
        
        print()
        
        # concepts 컬렉션에 unitId 필드 추가 (테스트용)
        print('3️⃣ concepts 컬렉션에 unitId 매핑 추가:')
        
        # 기존 concepts에 unitId 추가
        for i, concept in enumerate(concepts):
            unit_code = concept.get("unitCode")
            if unit_code:
                # unitCode에 따른 unitId 생성 (테스트용)
                if unit_code == "3.1":
                    unit_id = "68a013e4fe733a1c891816f3"  # problems의 unitId와 매핑
                elif unit_code == "3.2":
                    unit_id = "68a013e4fe733a1c891816f4"  # 새로운 unitId
                elif unit_code == "3.3":
                    unit_id = "68a013e4fe733a1c891816f5"  # 새로운 unitId
                else:
                    unit_id = f"test_unit_{i+1:03d}"
                
                # concepts 컬렉션 업데이트
                result = db.concepts.update_one(
                    {"unitCode": unit_code},
                    {"$set": {"unitId": unit_id}}
                )
                
                if result.modified_count > 0:
                    print(f"   ✅ {unit_code} → unitId: {unit_id}")
                else:
                    print(f"   ⚠️ {unit_code} 업데이트 실패")
        
        print()
        
        # 확인: 업데이트된 concepts 확인
        print('4️⃣ 업데이트된 concepts 확인:')
        updated_concepts = list(db.concepts.find())
        for concept in updated_concepts:
            print(f'   unitCode: {concept.get("unitCode")}')
            print(f'   unitTitle: {concept.get("unitTitle")}')
            print(f'   unitId: {concept.get("unitId")}')
            print(f'   ---')
        
        client.close()
        print("🎯 unitId 매핑 추가 완료!")
        
    except Exception as e:
        print(f'❌ 오류 발생: {e}')
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    add_test_mapping()
