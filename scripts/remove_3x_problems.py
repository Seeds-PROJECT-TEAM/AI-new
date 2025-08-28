#!/usr/bin/env python3
"""방금 추가한 3.x 문제들 삭제"""

import os
from dotenv import load_dotenv
import pymongo

def remove_3x_problems():
    try:
        # .env 파일 로드
        load_dotenv('AI/.env')
        mongodb_uri = os.getenv('MONGODB_URI')
        
        # MongoDB 연결
        client = pymongo.MongoClient(mongodb_uri)
        db = client.nerdmath
        
        print('=== 방금 추가한 3.x 문제들 삭제 ===')
        print()
        
        # 3.x 문제들 삭제
        result = db.problems.delete_many({"unitId": {"$regex": "^3\\."}})
        print(f"✅ 3.x 문제들 {result.deleted_count}개 삭제 완료")
        
        # 확인: 3.x 문제들이 제대로 삭제되었는지 확인
        print("🔍 확인: 3.x 문제들 조회:")
        problems_3x_check = list(db.problems.find({"unitId": {"$regex": "^3\\."}}))
        if problems_3x_check:
            for prob in problems_3x_check:
                print(f"   problem_id: {prob.get('problem_id')}")
                print(f"   unitId: {prob.get('unitId')}")
                print(f"   ---")
        else:
            print("   ✅ 3.x 문제들이 모두 삭제되었습니다")
        
        client.close()
        print("🎯 3.x 문제들 삭제 완료!")
        
    except Exception as e:
        print(f'❌ 오류 발생: {e}')
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    remove_3x_problems()
