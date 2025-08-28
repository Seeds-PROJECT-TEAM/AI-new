#!/usr/bin/env python3
"""
MongoDB 단원 정보 조회 및 추천 학습 경로 테스트
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'AI', 'app'))

from services.mongo_service import MongoService

def test_mongodb_units():
    """MongoDB에서 단원 정보 조회 테스트"""
    
    print("=== MongoDB 단원 정보 조회 테스트 ===")
    
    # MongoDB 연결
    mongo = MongoService()
    mongo._connect_to_mongodb()
    
    if not mongo.is_connected:
        print("❌ MongoDB 연결 실패")
        return
    
    print("✅ MongoDB 연결 성공!")
    
    # units 컬렉션 확인
    try:
        units_collection = mongo._db.units
        units_count = units_collection.count_documents({})
        print(f"📊 units 컬렉션 문서 수: {units_count}")
        
        if units_count > 0:
            # 단원 정보 조회
            units = list(units_collection.find().limit(5))
            print(f"\n📚 단원 정보 (최대 5개):")
            
            for i, unit in enumerate(units, 1):
                print(f"\n   {i}. 단원 ID: {unit.get('_id')}")
                print(f"      전체 필드: {list(unit.keys())}")
                
                # 각 필드의 값 확인
                for key, value in unit.items():
                    if key != '_id':
                        print(f"      {key}: {value}")
                        
        else:
            print("⚠️ units 컬렉션에 데이터가 없습니다")
            
            # 컬렉션 목록 확인
            collections = mongo._db.list_collection_names()
            print(f"📋 사용 가능한 컬렉션: {collections}")
            
    except Exception as e:
        print(f"❌ 단원 정보 조회 실패: {e}")
        import traceback
        traceback.print_exc()

def test_recommended_path_creation():
    """추천 학습 경로 생성 테스트"""
    
    print("\n=== 추천 학습 경로 생성 테스트 ===")
    
    # 테스트용 데이터
    wrong_units = ["정수와 유리수", "문자와 식", "함수"]
    accuracy_rate = 65.0
    
    # MongoDB에서 단원 정보 조회
    mongo = MongoService()
    mongo._connect_to_mongodb()
    
    if not mongo.is_connected:
        print("❌ MongoDB 연결 실패 - 추천 경로 생성 건너뜀")
        return
    
    try:
        # units 컬렉션에서 단원 정보 조회
        units_collection = mongo._db.units
        unit_info_map = {}
        
        units = list(units_collection.find({}))
        for unit in units:
            # 단원명을 찾기 위해 여러 필드 확인
            unit_name = None
            
            # 1. title 필드에서 한국어 텍스트 추출 (우선순위 1)
            if unit.get("title") and isinstance(unit.get("title"), dict):
                title = unit.get("title")
                if "ko" in title:
                    unit_name = title["ko"]
            
            # 2. unitId 필드 사용 (우선순위 2)
            if not unit_name and unit.get("unitId"):
                unit_name = unit.get("unitId")
            
            # 3. chapterTitle 필드 사용 (우선순위 3)
            if not unit_name and unit.get("chapterTitle"):
                unit_name = unit.get("chapterTitle")
            
            if unit_name:
                unit_info_map[unit_name] = {
                    "unitId": str(unit.get("_id", "")),
                    "unit": unit_name,
                    "grade": unit.get("grade", ""),
                    "description": unit.get("description", ""),
                    "difficulty": unit.get("difficulty", ""),
                    "priority": unit.get("priority", 1)
                }
        
        print(f"✅ MongoDB에서 {len(unit_info_map)}개 단원 정보 조회 완료")
        
        # 조회된 단원 정보 출력
        if unit_info_map:
            print(f"\n📋 조회된 단원 정보:")
            for name, info in list(unit_info_map.items())[:3]:  # 최대 3개만 출력
                print(f"   - {name}: {info['unitId']}")
        
        # 추천 경로 생성
        recommended_path = []
        for i, unit_name in enumerate(wrong_units):
            # MongoDB에서 해당 단원 정보 찾기
            unit_info = unit_info_map.get(unit_name)
            
            if unit_info:
                # MongoDB에서 가져온 정보 사용
                unit_id = unit_info.get("unitId", f"unit_{i+1:03d}")
                unit_title = unit_info.get("unit", unit_name)
                priority = unit_info.get("priority", i + 1)
            else:
                # MongoDB에 없는 경우 기본값 사용
                unit_id = f"unit_{i+1:03d}"
                unit_title = unit_name
                priority = i + 1
            
            # 진단테스트 결과를 바탕으로 reason 생성
            error_rate = max(0.1, (100 - accuracy_rate) / 100)  # 최소 10%
            reason = f"오답률 {error_rate:.0%}로 가장 취약한 단원"
            
            recommended_path.append({
                "unitId": unit_id,
                "unitTitle": unit_title,
                "priority": priority,
                "reason": reason
            })
        
        print(f"\n🎯 생성된 추천 학습 경로:")
        for i, path in enumerate(recommended_path, 1):
            print(f"   {i}. {path['unitTitle']}")
            print(f"      - ID: {path['unitId']}")
            print(f"      - 우선순위: {path['priority']}")
            print(f"      - 이유: {path['reason']}")
            print()
            
    except Exception as e:
        print(f"❌ 추천 경로 생성 실패: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_mongodb_units()
    test_recommended_path_creation()
