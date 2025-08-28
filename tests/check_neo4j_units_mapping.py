import os
import sys
from dotenv import load_dotenv
from pymongo import MongoClient
import json

# 환경변수 로드
load_dotenv('AI/.env')

def check_neo4j_units_mapping():
    """Neo4j 단원 정보 확인 및 MongoDB와 매핑 테스트"""
    
    print("🔍 Neo4j 단원 정보 확인 및 MongoDB 매핑 테스트 시작...")
    print("=" * 70)
    
    # MongoDB 연결
    try:
        mongodb_uri = os.getenv('MONGODB_URI')
        if not mongodb_uri:
            print("❌ MONGODB_URI 환경변수가 설정되지 않았습니다.")
            return
        
        print(f"📡 MongoDB 연결 시도: {mongodb_uri[:50]}...")
        client = MongoClient(mongodb_uri)
        
        # nerdmath 데이터베이스 선택
        db = client['nerdmath']
        print(f"🎯 선택된 데이터베이스: nerdmath")
        
        # units 컬렉션 확인
        print("\n🏫 MongoDB 'units' 컬렉션:")
        units_collection = db['units']
        units_count = units_collection.count_documents({})
        print(f"   총 단원 수: {units_count}")
        
        if units_count > 0:
            all_units = list(units_collection.find())
            for i, unit in enumerate(all_units, 1):
                print(f"\n   📋 단원 {i}:")
                print(f"      _id: {unit.get('_id', 'N/A')}")
                print(f"      title.ko: {unit.get('title', {}).get('ko', 'N/A')}")
                print(f"      chapterTitle: {unit.get('chapterTitle', 'N/A')}")
                print(f"      grade: {unit.get('grade', 'N/A')}")
                print(f"      subject: {unit.get('subject', 'N/A')}")
        
        print("\n" + "="*50)
        
        # Neo4j 단원 정보 확인 (가상 데이터로 시뮬레이션)
        print("\n🔗 Neo4j 단원 정보 (가상 데이터):")
        print("   📋 Neo4j에 저장된 단원들:")
        print("      - 1.1 소수와 합성수, 소인수분해")
        print("      - 1.2 최대공약수와 최소공배수")
        print("      - 2.1 문자와 식")
        print("      - 2.2 일차식의 사칙연산")
        print("      - 3.1 일차함수")
        print("      - 3.2 이차함수")
        
        print("\n" + "="*50)
        
        # 매핑 테스트
        print("\n🔗 단원명 매핑 테스트:")
        test_unit_names = [
            "1.1 소수와 합성수, 소인수분해",
            "1.2 최대공약수와 최소공배수", 
            "2.1 문자와 식",
            "2.2 일차식의 사칙연산",
            "3.1 일차함수",
            "3.2 이차함수"
        ]
        
        for unit_name in test_unit_names:
            # "1.1", "2.1" 등 앞부분 추출
            unit_code = unit_name.split()[0]
            print(f"\n   📍 단원명: {unit_name}")
            print(f"      추출된 코드: {unit_code}")
            
            # MongoDB에서 매칭되는 단원 찾기
            mongodb_match = None
            for unit in all_units:
                title = unit.get('title', {}).get('ko', '')
                chapter_title = unit.get('chapterTitle', '')
                
                # 단원명이나 챕터명에 매칭되는 부분이 있는지 확인
                if (unit_code in title or 
                    unit_code in chapter_title or
                    any(keyword in title for keyword in unit_name.split()[1:]) or
                    any(keyword in chapter_title for keyword in unit_name.split()[1:])):
                    mongodb_match = unit
                    break
            
            if mongodb_match:
                print(f"      ✅ MongoDB 매칭: {mongodb_match.get('title', {}).get('ko', 'N/A')}")
            else:
                print(f"      ❌ MongoDB 매칭 없음")
            
            # Neo4j에서 해당 단원의 선수개념 찾기 (가상)
            print(f"      🔍 Neo4j 선수개념: {unit_code} 관련 선수개념들")
        
        print("\n" + "="*70)
        print("✅ 단원명 매핑 테스트 완료!")
        
        # 매핑 전략 제안
        print("\n💡 매핑 전략 제안:")
        print("   1. 단원명에서 '1.1', '2.1' 같은 코드 추출")
        print("   2. MongoDB units 컬렉션에서 매칭되는 단원 찾기")
        print("   3. Neo4j에서 해당 단원의 선수개념과 연결된 단원들 조회")
        print("   4. 맞춤형 학습경로 생성")
        
        client.close()
        
    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")
        print(f"   오류 타입: {type(e).__name__}")

if __name__ == "__main__":
    check_neo4j_units_mapping()
