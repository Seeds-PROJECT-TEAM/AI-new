import os
import sys
from dotenv import load_dotenv
from pymongo import MongoClient
import json

# 환경변수 로드
load_dotenv('AI/.env')

def check_all_databases():
    """모든 데이터베이스에서 단원 정보 찾기"""
    
    print("🔍 모든 데이터베이스에서 단원 정보 찾기 시작...")
    print("=" * 70)
    
    # MongoDB 연결
    try:
        mongodb_uri = os.getenv('MONGODB_URI')
        if not mongodb_uri:
            print("❌ MONGODB_URI 환경변수가 설정되지 않았습니다.")
            return
        
        print(f"📡 MongoDB 연결 시도: {mongodb_uri[:50]}...")
        client = MongoClient(mongodb_uri)
        
        # 모든 데이터베이스 목록
        db_list = client.list_database_names()
        print(f"📚 발견된 데이터베이스: {db_list}")
        print()
        
        found_units = False
        found_problems = False
        
        for db_name in db_list:
            if db_name in ['admin', 'local']:  # 시스템 DB는 건너뛰기
                continue
                
            print(f"🔍 {db_name} 데이터베이스 확인 중...")
            db = client[db_name]
            
            # 컬렉션 목록
            collections = db.list_collection_names()
            
            # units 컬렉션 확인
            if 'units' in collections:
                units_collection = db['units']
                units_count = units_collection.count_documents({})
                if units_count > 0:
                    print(f"   ✅ 'units' 컬렉션 발견! (총 {units_count}개)")
                    found_units = True
                    
                    # 샘플 데이터 확인
                    sample_units = list(units_collection.find().limit(3))
                    for i, unit in enumerate(sample_units, 1):
                        print(f"      📋 샘플 {i}:")
                        print(f"         ID: {unit.get('_id', 'N/A')}")
                        print(f"         제목: {unit.get('title', {}).get('ko', 'N/A')}")
                        print(f"         챕터: {unit.get('chapterTitle', 'N/A')}")
                        print(f"         학년: {unit.get('grade', 'N/A')}")
                        print()
                else:
                    print(f"   ❌ 'units' 컬렉션은 있지만 데이터가 없음")
            else:
                print(f"   ❌ 'units' 컬렉션 없음")
            
            # problems 컬렉션 확인
            if 'problems' in collections:
                problems_collection = db['problems']
                problems_count = problems_collection.count_documents({})
                if problems_count > 0:
                    print(f"   ✅ 'problems' 컬렉션 발견! (총 {problems_count}개)")
                    found_problems = True
                    
                    # 샘플 데이터 확인
                    sample_problems = list(problems_collection.find().limit(3))
                    for i, problem in enumerate(sample_problems, 1):
                        print(f"      📋 샘플 {i}:")
                        print(f"         ID: {problem.get('_id', 'N/A')}")
                        print(f"         단원: {problem.get('unit', 'N/A')}")
                        print(f"         단원명: {problem.get('unitName', 'N/A')}")
                        print(f"         챕터: {problem.get('chapter', 'N/A')}")
                        print()
                else:
                    print(f"   ❌ 'problems' 컬렉션은 있지만 데이터가 없음")
            else:
                print(f"   ❌ 'problems' 컬렉션 없음")
            
            print()
        
        print("=" * 70)
        print("✅ 모든 데이터베이스 확인 완료!")
        
        # 최종 요약
        print("\n📊 최종 데이터 현황:")
        print(f"  🏫 단원 데이터: {'발견됨' if found_units else '없음'}")
        print(f"  📝 문제 데이터: {'발견됨' if found_problems else '없음'}")
        
        if not found_units and not found_problems:
            print("\n⚠️  주의사항:")
            print("   현재 MongoDB에 단원이나 문제 데이터가 없습니다.")
            print("   맞춤형 학습경로를 생성하려면 다음 중 하나가 필요합니다:")
            print("   1. MongoDB에 단원/문제 데이터 추가")
            print("   2. _extract_unit_from_problem_id 메서드 개선")
            print("   3. Neo4j에서 직접 단원 정보 가져오기")
        
        client.close()
        
    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")
        print(f"   오류 타입: {type(e).__name__}")

if __name__ == "__main__":
    check_all_databases()
