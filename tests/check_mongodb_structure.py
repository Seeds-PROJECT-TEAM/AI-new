#!/usr/bin/env python3
"""MongoDB 데이터 구조 확인"""

import os
from dotenv import load_dotenv
import pymongo

def check_mongodb_structure():
    try:
        # .env 파일 로드
        load_dotenv('AI/.env')
        mongodb_uri = os.getenv('MONGODB_URI')
        
        # MongoDB 연결
        client = pymongo.MongoClient(mongodb_uri)
        db = client.nerdmath
        
        print('=== MongoDB 데이터 구조 확인 ===')
        print()
        
        # 1. problems 컬렉션 확인
        print('1️⃣ problems 컬렉션:')
        problems = list(db.problems.find().limit(3))
        for prob in problems:
            print(f'   problem_id: {prob.get("problem_id")}')
            print(f'   unitId: {prob.get("unitId")}')
            print(f'   ---')
        
        print()
        
        # 2. units 컬렉션 확인  
        print('2️⃣ units 컬렉션:')
        units = list(db.units.find().limit(3))
        for unit in units:
            print(f'   unitId: {unit.get("unitId")}')
            print(f'   title.ko: {unit.get("title", {}).get("ko")}')
            print(f'   ---')
        
        print()
        
        # 3. concepts 컬렉션 확인
        print('3️⃣ concepts 컬렉션:')
        concepts = list(db.concepts.find().limit(3))
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
    check_mongodb_structure()
