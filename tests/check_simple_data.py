#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MongoDB에서 aiComment와 recommendedPath만 간단하게 확인
"""

import os
from pymongo import MongoClient
from dotenv import load_dotenv

# AI 폴더의 .env 파일 로드
load_dotenv('AI/.env')

def check_simple_data():
    try:
        # MongoDB 연결
        client = MongoClient(os.getenv('MONGODB_URI'))
        db = client.nerdmath
        
        print("=== aiComment와 recommendedPath 확인 ===\n")
        
        # Express 진단테스트 결과에서 필요한 필드만 조회
        express_results = list(db.express_diagnostic_results.find().sort('_id', -1).limit(5))
        
        for i, result in enumerate(express_results, 1):
            print(f"--- 진단테스트 {i} ---")
            print(f"Test ID: {result.get('testId')}")
            print(f"User ID: {result.get('userId')}")
            
            # Analysis Result에서 aiComment와 recommendedPath만
            analysis = result.get('analysisResult', {})
            if analysis:
                print(f"AI Comment: {analysis.get('aiComment', '')}")
                
                recommended_path = analysis.get('recommendedPath', [])
                if recommended_path:
                    print(f"Recommended Path ({len(recommended_path)}개):")
                    for j, path_item in enumerate(recommended_path, 1):
                        print(f"  {j}. {path_item.get('unitTitle', '')} (Priority: {path_item.get('priority', '')})")
                        print(f"     Reason: {path_item.get('reason', '')}")
                else:
                    print("Recommended Path: 없음")
            
            print()  # 구분선
        
        client.close()
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")

if __name__ == "__main__":
    check_simple_data()
