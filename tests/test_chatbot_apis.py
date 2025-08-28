#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
챗봇 API 테스트 스크립트
모든 챗봇 기능이 제대로 작동하는지 확인
"""

import requests
import json
from datetime import datetime

def test_api_endpoint(url, method="GET", data=None, headers=None):
    """API 엔드포인트 테스트"""
    try:
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers)
        
        print(f"🔍 {method} {url}")
        print(f"   상태 코드: {response.status_code}")
        
        if response.status_code == 200:
            print("   ✅ 성공!")
            try:
                result = response.json()
                print(f"   응답: {json.dumps(result, ensure_ascii=False, indent=2)}")
            except:
                print(f"   응답: {response.text}")
        else:
            print(f"   ❌ 실패: {response.text}")
        
        print("-" * 50)
        return response.status_code == 200
        
    except Exception as e:
        print(f"   ❌ 오류: {e}")
        print("-" * 50)
        return False

def test_chatbot_apis():
    """모든 챗봇 API 테스트"""
    
    print("🤖 챗봇 API 테스트 시작")
    print("=" * 60)
    
    base_url = "http://localhost:8000"
    
    # 1. 데이터베이스 상태 확인
    print("1️⃣ 데이터베이스 상태 확인")
    test_api_endpoint(f"{base_url}/api/db/health")
    
    # 2. 문제 조회 API
    print("2️⃣ 문제 조회 API")
    test_api_endpoint(f"{base_url}/api/problem/problem_001")
    
    # 3. AI 문제 풀이 API (Auth 필요)
    print("3️⃣ AI 문제 풀이 API (Auth 필요)")
    headers = {"X-Service-Token": "test-token"}
    solve_data = {
        "problem_text": "5 + 3 = ? 이 문제를 풀어주세요.",
        "session_id": "test_session_123"
    }
    test_api_endpoint(f"{base_url}/api/ai/solve", "POST", solve_data, headers)
    
    # 4. AI 개념 설명 API (Auth 필요)
    print("4️⃣ AI 개념 설명 API (Auth 필요)")
    concept_data = {
        "concept_name": "덧셈의 기본 개념",
        "session_id": "test_session_123"
    }
    test_api_endpoint(f"{base_url}/api/ai/concept", "POST", concept_data, headers)
    
    # 5. AI RAG 추천 API (Auth 필요)
    print("5️⃣ AI RAG 추천 API (Auth 필요)")
    rag_data = {
        "problem_text": "덧셈과 관련된 자료를 추천해주세요.",
        "session_id": "test_session_123"
    }
    test_api_endpoint(f"{base_url}/api/ai/rag_recommend", "POST", rag_data, headers)
    
    # 6. 통합 문제 풀이 API (Auth 불필요)
    print("6️⃣ 통합 문제 풀이 API (Auth 불필요)")
    solve_integrated_data = {
        "problem_id": "problem_001",
        "question": "이 문제를 풀어주세요",
        "session_id": "user_session_123"
    }
    test_api_endpoint(f"{base_url}/api/solve_with_problem", "POST", solve_integrated_data)
    
    # 7. 통합 개념 설명 API (Auth 불필요)
    print("7️⃣ 통합 개념 설명 API (Auth 불필요)")
    concept_integrated_data = {
        "problem_id": "problem_001",
        "concept_name": "덧셈의 기본 개념",
        "session_id": "user_session_123"
    }
    test_api_endpoint(f"{base_url}/api/concept_with_problem", "POST", concept_integrated_data)
    
    # 8. 통합 RAG 추천 API (Auth 불필요)
    print("8️⃣ 통합 RAG 추천 API (Auth 불필요)")
    rag_integrated_data = {
        "problem_id": "problem_001",
        "question": "관련 자료를 추천해주세요",
        "session_id": "user_session_123"
    }
    test_api_endpoint(f"{base_url}/api/rag_with_problem", "POST", rag_integrated_data)
    
    print("=" * 60)
    print("🎉 챗봇 API 테스트 완료!")

if __name__ == "__main__":
    test_chatbot_apis()
