import os
import sys
from dotenv import load_dotenv
from pymongo import MongoClient
import json

# 환경변수 로드
load_dotenv('AI/.env')

def check_nerdmath_detail():
    """nerdmath 데이터베이스의 단원과 문제 데이터 상세 확인"""
    
    print("🔍 nerdmath 데이터베이스 상세 확인 시작...")
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
        
        # units 컬렉션 상세 확인
        print("\n🏫 'units' 컬렉션 상세 분석:")
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
                print(f"      전체 필드: {list(unit.keys())}")
        
        print("\n" + "="*50)
        
        # problems 컬렉션 상세 확인
        print("\n📝 'problems' 컬렉션 상세 분석:")
        problems_collection = db['problems']
        problems_count = problems_collection.count_documents({})
        print(f"   총 문제 수: {problems_count}")
        
        if problems_count > 0:
            all_problems = list(problems_collection.find())
            for i, problem in enumerate(all_problems, 1):
                print(f"\n   📋 문제 {i}:")
                print(f"      _id: {problem.get('_id', 'N/A')}")
                print(f"      unit: {problem.get('unit', 'N/A')}")
                print(f"      unitName: {problem.get('unitName', 'N/A')}")
                print(f"      chapter: {problem.get('chapter', 'N/A')}")
                print(f"      subject: {problem.get('subject', 'N/A')}")
                print(f"      전체 필드: {list(problem.keys())}")
                
                # 문제 내용 일부 출력 (너무 길면 잘라서)
                content = problem.get('content', 'N/A')
                if isinstance(content, str) and len(content) > 100:
                    content = content[:100] + "..."
                print(f"      content: {content}")
        
        print("\n" + "="*50)
        
        # 문제-단원 연결 분석
        print("\n🔗 문제-단원 연결 분석:")
        if problems_count > 0 and units_count > 0:
            print("   📊 문제 ID와 단원 연결 상태:")
            
            # 문제 ID에서 단원 정보 추출 시도
            for problem in all_problems[:5]:  # 처음 5개만
                problem_id = str(problem.get('_id', ''))
                print(f"\n      문제 ID: {problem_id}")
                
                # MongoDB에서 단원 찾기 시도
                unit_found = False
                for unit in all_units:
                    if str(unit.get('_id')) in problem_id:
                        print(f"         ✅ 단원 매칭 발견: {unit.get('title', {}).get('ko', 'N/A')}")
                        unit_found = True
                        break
                
                if not unit_found:
                    print(f"         ❌ 단원 매칭 없음")
                    
                    # 문제 ID에서 단원명 추출 시도
                    if '1.1' in problem_id or '소수' in problem_id:
                        print(f"         💡 추정 단원: 1. 수와 연산 (소수와 합성수)")
                    elif '1.2' in problem_id or '최대공약수' in problem_id:
                        print(f"         💡 추정 단원: 1. 수와 연산 (최대공약수와 최소공배수)")
                    elif '2.1' in problem_id or '문자' in problem_id:
                        print(f"         💡 추정 단원: 2. 문자와 식")
                    elif '2.2' in problem_id or '일차식' in problem_id:
                        print(f"         💡 추정 단원: 2. 문자와 식 (일차식의 사칙연산)")
        
        print("\n" + "="*70)
        print("✅ nerdmath 데이터베이스 상세 분석 완료!")
        
        # 맞춤형 학습경로 생성 가능성 평가
        print("\n🎯 맞춤형 학습경로 생성 가능성:")
        if units_count > 0 and problems_count > 0:
            print("   ✅ 기본 데이터는 충분함")
            print("   💡 문제 ID에서 단원 정보 추출 로직 개선 필요")
            print("   💡 Neo4j와의 연동으로 선수개념 파악 가능")
        else:
            print("   ❌ 데이터 부족으로 맞춤형 학습경로 생성 불가")
        
        client.close()
        
    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")
        print(f"   오류 타입: {type(e).__name__}")

if __name__ == "__main__":
    check_nerdmath_detail()
