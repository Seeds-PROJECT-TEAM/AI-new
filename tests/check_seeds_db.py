import os
import sys
from dotenv import load_dotenv
from pymongo import MongoClient
import json

# 환경변수 로드
load_dotenv('AI/.env')

def check_seeds_db():
    """seeds_db 데이터베이스의 단원 정보 확인"""
    
    print("🔍 seeds_db 데이터베이스 단원 정보 확인 시작...")
    print("=" * 60)
    
    # MongoDB 연결
    try:
        mongodb_uri = os.getenv('MONGODB_URI')
        if not mongodb_uri:
            print("❌ MONGODB_URI 환경변수가 설정되지 않았습니다.")
            return
        
        print(f"📡 MongoDB 연결 시도: {mongodb_uri[:50]}...")
        client = MongoClient(mongodb_uri)
        
        # seeds_db 데이터베이스 선택
        db = client['seeds_db']
        print(f"🎯 선택된 데이터베이스: seeds_db")
        
        # 컬렉션 목록 확인
        collections = db.list_collection_names()
        print(f"📁 사용 가능한 컬렉션: {collections}")
        print()
        
        # units 컬렉션 확인
        if 'units' in collections:
            print("🏫 'units' 컬렉션 확인 중...")
            units_collection = db['units']
            units_count = units_collection.count_documents({})
            print(f"   총 단원 수: {units_count}")
            
            if units_count > 0:
                print("   📋 샘플 단원 데이터:")
                sample_units = list(units_collection.find().limit(5))
                for i, unit in enumerate(sample_units, 1):
                    print(f"   {i}. 단원 ID: {unit.get('_id', 'N/A')}")
                    print(f"      제목: {unit.get('title', {}).get('ko', 'N/A')}")
                    print(f"      챕터: {unit.get('chapterTitle', 'N/A')}")
                    print(f"      학년: {unit.get('grade', 'N/A')}")
                    print(f"      과목: {unit.get('subject', 'N/A')}")
                    print()
            else:
                print("   ❌ 단원 데이터가 없습니다.")
        else:
            print("❌ 'units' 컬렉션이 존재하지 않습니다.")
        
        print()
        
        # problems 컬렉션 확인
        if 'problems' in collections:
            print("📝 'problems' 컬렉션 확인 중...")
            problems_collection = db['problems']
            problems_count = problems_collection.count_documents({})
            print(f"   총 문제 수: {problems_count}")
            
            if problems_count > 0:
                print("   📋 샘플 문제 데이터:")
                sample_problems = list(problems_collection.find().limit(5))
                for i, problem in enumerate(sample_problems, 1):
                    print(f"   {i}. 문제 ID: {problem.get('_id', 'N/A')}")
                    print(f"      단원: {problem.get('unit', 'N/A')}")
                    print(f"      단원명: {problem.get('unitName', 'N/A')}")
                    print(f"      챕터: {problem.get('chapter', 'N/A')}")
                    print(f"      과목: {problem.get('subject', 'N/A')}")
                    print()
            else:
                print("   ❌ 문제 데이터가 없습니다.")
        else:
            print("❌ 'problems' 컬렉션이 존재하지 않습니다.")
        
        print()
        
        # express_diagnostic_results 컬렉션 확인
        if 'express_diagnostic_results' in collections:
            print("🔬 'express_diagnostic_results' 컬렉션 확인 중...")
            diagnostic_collection = db['express_diagnostic_results']
            diagnostic_count = diagnostic_collection.count_documents({})
            print(f"   총 진단 결과 수: {diagnostic_count}")
            
            if diagnostic_count > 0:
                print("   📋 샘플 진단 결과:")
                sample_diagnostic = list(diagnostic_collection.find().limit(2))
                for i, diagnostic in enumerate(sample_diagnostic, 1):
                    print(f"   {i}. 테스트 ID: {diagnostic.get('testId', 'N/A')}")
                    print(f"      사용자 ID: {diagnostic.get('userId', 'N/A')}")
                    if 'analysisResult' in diagnostic:
                        analysis = diagnostic['analysisResult']
                        print(f"      AI 코멘트: {analysis.get('aiComment', 'N/A')}")
                        print(f"      클래스: {analysis.get('class', 'N/A')}")
                        recommended_path = analysis.get('recommendedPath', [])
                        print(f"      추천 경로 수: {len(recommended_path)}")
                    print()
            else:
                print("   ❌ 진단 결과 데이터가 없습니다.")
        else:
            print("❌ 'express_diagnostic_results' 컬렉션이 존재하지 않습니다.")
        
        print()
        
        # learning_paths 컬렉션 확인
        if 'learning_paths' in collections:
            print("🛤️ 'learning_paths' 컬렉션 확인 중...")
            learning_paths_collection = db['learning_paths']
            learning_paths_count = learning_paths_collection.count_documents({})
            print(f"   총 학습 경로 수: {learning_paths_count}")
            
            if learning_paths_count > 0:
                print("   📋 샘플 학습 경로:")
                sample_paths = list(learning_paths_collection.find().limit(2))
                for i, path in enumerate(sample_paths, 1):
                    print(f"   {i}. 경로 ID: {path.get('_id', 'N/A')}")
                    print(f"      사용자 ID: {path.get('userId', 'N/A')}")
                    print(f"      생성일: {path.get('createdAt', 'N/A')}")
                    print()
            else:
                print("   ❌ 학습 경로 데이터가 없습니다.")
        else:
            print("❌ 'learning_paths' 컬렉션이 존재하지 않습니다.")
        
        print("=" * 60)
        print("✅ seeds_db 데이터베이스 확인 완료!")
        
        # 요약
        print("\n📊 데이터 현황 요약:")
        print(f"  🏫 단원 데이터: {'있음' if 'units' in collections and db['units'].count_documents({}) > 0 else '없음'}")
        print(f"  📝 문제 데이터: {'있음' if 'problems' in collections and db['problems'].count_documents({}) > 0 else '없음'}")
        print(f"  🔬 진단 결과: {'있음' if 'express_diagnostic_results' in collections and db['express_diagnostic_results'].count_documents({}) > 0 else '없음'}")
        print(f"  🛤️ 학습 경로: {'있음' if 'learning_paths' in collections and db['learning_paths'].count_documents({}) > 0 else '없음'}")
        
        client.close()
        
    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")
        print(f"   오류 타입: {type(e).__name__}")

if __name__ == "__main__":
    check_seeds_db()
