#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI가 생성한 aiComment와 recommendedPath만 간단하게 보여주기
"""

import os
from pymongo import MongoClient
from dotenv import load_dotenv

# AI 폴더의 .env 파일 로드
load_dotenv('AI/.env')

def show_ai_generated_data():
    try:
        # MongoDB 연결
        client = MongoClient(os.getenv('MONGODB_URI'))
        db = client.nerdmath
        
        print("=== AI가 생성한 데이터만 확인 ===\n")
        
        # Express 진단테스트 결과 컬렉션
        express_collection = db.express_diagnostic_results
        all_results = list(express_collection.find().sort('_id', -1))
        
        print(f"📊 총 {len(all_results)}개의 진단테스트 결과\n")
        
        for i, result in enumerate(all_results, 1):
            print(f"{'='*50}")
            print(f"📋 테스트 {i}: {result.get('testId', 'N/A')}")
            print(f"{'='*50}")
            
            # 분석 결과에서 AI 생성 데이터만
            analysis = result.get('analysisResult', {})
            if analysis:
                # AI Comment
                ai_comment = analysis.get('aiComment', 'N/A')
                print(f"💬 AI Comment:")
                print(f"   {ai_comment}")
                
                # 추천 경로
                recommended_path = analysis.get('recommendedPath', [])
                if recommended_path:
                    print(f"\n🛤️ Recommended Path ({len(recommended_path)}개):")
                    for j, path_item in enumerate(recommended_path, 1):
                        unit_title = path_item.get('unitTitle', 'N/A')
                        priority = path_item.get('priority', 'N/A')
                        reason = path_item.get('reason', 'N/A')
                        print(f"   {j}. {unit_title}")
                        print(f"      Priority: {priority}")
                        print(f"      Reason: {reason}")
                else:
                    print(f"\n🛤️ Recommended Path: 없음")
                
                # Class 정보도 함께
                class_info = analysis.get('class', 'N/A')
                print(f"\n🏷️ Class: {class_info}")
            else:
                print("❌ 분석 결과 없음")
            
            print(f"\n")
        
        print(f"✅ AI 생성 데이터 확인 완료!")
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if 'client' in locals():
            client.close()

if __name__ == "__main__":
    show_ai_generated_data()
