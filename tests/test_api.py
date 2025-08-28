#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FastAPI 서버 테스트 스크립트
/load-all 엔드포인트를 호출하여 모든 데이터를 MongoDB에 저장
"""

import requests
import json
import time

def test_load_all_data():
    """모든 데이터 로드 테스트"""
    base_url = "http://localhost:8001"
    
    print("🚀 MongoDB 데이터 로더 API 테스트 시작")
    print(f"서버 주소: {base_url}")
    print("-" * 50)
    
    # 1. 서버 상태 확인
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("✅ 서버 연결 성공")
            print(f"서버 응답: {response.json()}")
        else:
            print(f"❌ 서버 응답 오류: {response.status_code}")
            return
    except requests.exceptions.ConnectionError:
        print("❌ 서버에 연결할 수 없습니다. FastAPI 서버가 실행 중인지 확인하세요.")
        return
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        return
    
    print("-" * 50)
    
    # 2. 모든 데이터 로드
    print("📊 모든 데이터 로드 시작...")
    try:
        response = requests.post(f"{base_url}/load-all")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 모든 데이터 로드 성공!")
            print(f"결과: {result['message']}")
            print(f"성공 개수: {result['total_success']}/3")
            
            # 상세 결과 출력
            if 'results' in result:
                print("\n📋 상세 결과:")
                for data_type, data_result in result['results'].items():
                    status = "✅" if data_result['success'] else "❌"
                    print(f"  {status} {data_type}: {data_result['message']}")
        else:
            print(f"❌ 데이터 로드 실패: {response.status_code}")
            try:
                error_detail = response.json()
                print(f"오류 상세: {error_detail}")
            except:
                print(f"오류 내용: {response.text}")
                
    except Exception as e:
        print(f"❌ 데이터 로드 중 오류 발생: {e}")
    
    print("-" * 50)
    
    # 3. 통계 확인
    print("📈 컬렉션 통계 확인...")
    try:
        response = requests.get(f"{base_url}/stats")
        
        if response.status_code == 200:
            stats = response.json()
            if stats['success']:
                print("✅ 통계 조회 성공!")
                print("📊 컬렉션별 문서 수:")
                for collection, count in stats['stats'].items():
                    print(f"  {collection}: {count}개")
            else:
                print(f"❌ 통계 조회 실패: {stats.get('message', '알 수 없는 오류')}")
        else:
            print(f"❌ 통계 조회 실패: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 통계 조회 중 오류 발생: {e}")
    
    print("-" * 50)
    print("🏁 테스트 완료!")

if __name__ == "__main__":
    test_load_all_data()
