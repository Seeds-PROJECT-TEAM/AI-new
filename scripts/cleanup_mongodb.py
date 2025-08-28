#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MongoDB 테스트 데이터 정리
"""

import os
from pymongo import MongoClient
from dotenv import load_dotenv

# AI 폴더의 .env 파일 로드
load_dotenv('AI/.env')

def cleanup_test_data():
    try:
        # MongoDB 연결
        client = MongoClient(os.getenv('MONGODB_URI'))
        db = client.nerdmath
        
        print("=== MongoDB 테스트 데이터 정리 시작 ===\n")
        
        # 1. express_diagnostic_results 컬렉션 정리
        print("1. express_diagnostic_results 컬렉션 정리:")
        express_collection = db.express_diagnostic_results
        
        # 테스트 데이터만 삭제 (실제 운영 데이터는 보존)
        test_ids = [
            'test_express_001', 'test_ai_reason', '68a013e4fe733a1c891816f3',
            'json_save_test', 'perfect_test_001', 'ultimate_test', 'final_fixed_test',
            'fixed_test_001', 'improved_test_001', 'restart_test_001', 'comprehensive_test_001',
            'express_test_001', 'direct_test', 'fixed_nodes_test'
        ]
        
        for test_id in test_ids:
            result = express_collection.delete_many({'testId': test_id})
            if result.deleted_count > 0:
                print(f"  ✅ {test_id}: {result.deleted_count}개 삭제")
        
        # 남은 데이터 확인
        remaining_count = express_collection.count_documents({})
        print(f"  📊 남은 데이터: {remaining_count}개")
        
        # 2. learning_paths 컬렉션 정리
        print("\n2. learning_paths 컬렉션 정리:")
        paths_collection = db.learning_paths
        
        # 테스트 관련 경로 삭제
        test_path_ids = [
            '68afda7965557edcffd8cf75', '68afdb6e4ea69830c78a7ea6',
            '68afdd091813907b42b788e3', '68acb8d5c2ff77e530d868a3',
            '68acb80dc2ff77e530d868a0', '68acb7b6c2ff77e530d8689d',
            '68acb7815f4b35f7bf0abafc', '68acb66a5f4b35f7bf0abaf9',
            '68acb6035f4b35f7bf0abaf6', '68acb53d5f4b35f7bf0abaf3',
            '68acb4ba5f4b35f7bf0abaf0', '68acb2745f4b35f7bf0abaed',
            '68acb2255f4b35f7bf0abaea', '68acb1c65f4b35f7bf0abae7',
            '68acb1625f4b35f7bf0abae4', '68acadb1d4e0a9578fdc6b91'
        ]
        
        for path_id in test_path_ids:
            result = paths_collection.delete_many({'pathId': path_id})
            if result.deleted_count > 0:
                print(f"  ✅ {path_id}: {result.deleted_count}개 삭제")
        
        # 남은 경로 확인
        remaining_paths = paths_collection.count_documents({})
        print(f"  📊 남은 학습 경로: {remaining_paths}개")
        
        print("\n✅ MongoDB 테스트 데이터 정리 완료!")
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if 'client' in locals():
            client.close()

if __name__ == "__main__":
    cleanup_test_data()
