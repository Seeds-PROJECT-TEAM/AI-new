#!/usr/bin/env python3
"""problems 컬렉션의 실제 unitId 구조 확인"""

import os
from dotenv import load_dotenv
import pymongo

def check_real_problems():
    try:
        # .env 파일 로드
        load_dotenv('AI/.env')
        mongodb_uri = os.getenv('MONGODB_URI')
        
        # MongoDB 연결
        client = pymongo.MongoClient(mongodb_uri)
        db = client.nerdmath
        
        print('=== problems 컬렉션의 실제 unitId 구조 확인 ===')
        print()
        
        # problems 컬렉션의 모든 데이터 확인
        print('1️⃣ problems 컬렉션 전체:')
        problems = list(db.problems.find())
        for prob in problems:
            print(f'   problem_id: {prob.get("problem_id")}')
            print(f'   unitId: {prob.get("unitId")} (타입: {type(prob.get("unitId"))})')
            print(f'   ---')
        
        print()
        
        # unitId가 3.1 형태인 것들만 필터링
        print('2️⃣ unitId가 3.x 형태인 problems:')
        problems_3x = [p for p in problems if isinstance(p.get("unitId"), str) and p.get("unitId", "").startswith("3.")]
        for prob in problems_3x:
            print(f'   problem_id: {prob.get("problem_id")}')
            print(f'   unitId: {prob.get("unitId")}')
            print(f'   ---')
        
        print()
        
        # concepts 컬렉션과 비교
        print('3️⃣ concepts 컬렉션의 unitCode:')
        concepts = list(db.concepts.find())
        for concept in concepts:
            print(f'   unitCode: {concept.get("unitCode")}')
            print(f'   unitTitle: {concept.get("unitTitle")}')
            print(f'   ---')
        
        client.close()
        
    except Exception as e:
        print(f'❌ 오류 발생: {e}')
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_real_problems()
