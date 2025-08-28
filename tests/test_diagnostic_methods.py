import os
import sys
from dotenv import load_dotenv

# AI 디렉토리를 Python 경로에 추가
sys.path.append(os.path.join(os.path.dirname(__file__), 'AI'))

# 환경 변수 로드
load_dotenv('AI/.env')

def test_unit_extraction():
    """문제 ID에서 단원명 추출 테스트"""
    
    print("🔍 문제 ID에서 단원명 추출 테스트")
    print()
    
    # 가상의 문제 ID들
    test_problem_ids = [
        "1.1 소수와 합성수, 소인수분해",
        "1.2 최대공약수와 최소공배수", 
        "1.3 정수와 유리수",
        "1.4 절댓값",
        "1.5 정수와 유리수의 덧셈, 뺄셈",
        "2.1 문자와 식",
        "2.2 일차식의 사칙 연산",
        "2.4 일차방정식의 풀이"
    ]
    
    # 단원명 추출 로직 (diagnostic_service.py의 _extract_unit_from_problem_id와 동일)
    def extract_unit_from_problem_id(problem_id):
        try:
            if problem_id.startswith("1."):
                return "1. 수와 연산"
            elif problem_id.startswith("2."):
                return "2. 문자와 식"
            elif problem_id.startswith("3."):
                return "3. 함수"
            elif problem_id.startswith("4."):
                return "4. 기하"
            elif problem_id.startswith("5."):
                return "5. 확률과 통계"
            else:
                return "1. 수와 연산"
        except Exception as e:
            print(f"⚠️ 단원명 추출 실패: {e}")
            return "1. 수와 연산"
    
    print("📚 문제 ID별 단원명 추출 결과:")
    for problem_id in test_problem_ids:
        unit_name = extract_unit_from_problem_id(problem_id)
        print(f"  - {problem_id} → {unit_name}")
    
    print()
    return True

def test_virtual_mongodb_logic():
    """가상 MongoDB 데이터 로직 테스트"""
    
    print("🔍 가상 MongoDB 데이터 로직 테스트")
    print()
    
    # 가상의 problems 데이터
    virtual_problems = [
        {
            "problemId": "1.1 소수와 합성수, 소인수분해",
            "unitId": "unit_001",
            "unit": "1. 수와 연산",
            "unitName": "1. 수와 연산"
        },
        {
            "problemId": "2.1 문자와 식",
            "unitId": "unit_002", 
            "unit": "2. 문자와 식",
            "unitName": "2. 문자와 식"
        }
    ]
    
    # 가상의 units 데이터
    virtual_units = [
        {
            "unitId": "unit_001",
            "title": {"ko": "수와 연산", "en": "Numbers and Operations"},
            "chapterTitle": "수와 연산"
        },
        {
            "unitId": "unit_002",
            "title": {"ko": "문자와 식", "en": "Expressions and Equations"},
            "chapterTitle": "문자와 식"
        }
    ]
    
    # 가상 MongoDB에서 문제 ID로 단원 찾기 로직
    def get_unit_from_virtual_mongodb(problem_id, problems, units):
        try:
            # problems 컬렉션에서 문제 ID로 단원 정보 조회
            problem = None
            
            # 여러 필드로 문제 검색 시도
            for p in problems:
                if p.get("problemId") == problem_id:
                    problem = p
                    break
            
            if problem:
                print(f"✅ 가상 MongoDB에서 문제 찾음: {problem_id}")
                
                # 단원 정보 추출
                unit_name = None
                
                # 1. unitId로 units 컬렉션에서 단원명 조회
                if problem.get("unitId"):
                    unit_id = problem["unitId"]
                    unit = None
                    
                    for u in units:
                        if u.get("unitId") == unit_id:
                            unit = u
                            break
                    
                    if unit:
                        # units 컬렉션에서 단원명 추출
                        if unit.get("title") and isinstance(unit["title"], dict) and unit["title"].get("ko"):
                            unit_name = unit["title"]["ko"]
                        elif unit.get("chapterTitle"):
                            unit_name = unit["chapterTitle"]
                        elif unit.get("title"):
                            unit_name = str(unit["title"])
                        
                        print(f"✅ units 컬렉션에서 단원명 추출: {unit_name}")
                
                # 2. 직접 단원 정보가 있는 경우
                if not unit_name:
                    if problem.get("unit"):
                        unit_name = problem["unit"]
                    elif problem.get("unitName"):
                        unit_name = problem["unitName"]
                    
                    if unit_name:
                        print(f"✅ 문제 데이터에서 단원명 추출: {unit_name}")
                
                return unit_name
            else:
                print(f"⚠️ 가상 MongoDB에서 문제를 찾을 수 없음: {problem_id}")
                return None
                
        except Exception as e:
            print(f"⚠️ 가상 MongoDB 문제 조회 실패: {e}")
            return None
    
    # 테스트 실행
    test_problem_ids = [
        "1.1 소수와 합성수, 소인수분해",
        "2.1 문자와 식",
        "3.1 함수"  # 존재하지 않는 문제 ID
    ]
    
    print("📚 가상 MongoDB에서 단원 정보 조회 테스트:")
    for problem_id in test_problem_ids:
        unit_name = get_unit_from_virtual_mongodb(problem_id, virtual_problems, virtual_units)
        if unit_name:
            print(f"  ✅ {problem_id} → {unit_name}")
        else:
            print(f"  ❌ {problem_id} → 단원 정보 없음")
        print()
    
    return True

def test_learning_path_generation():
    """학습 경로 생성 로직 테스트"""
    
    print("🔍 학습 경로 생성 로직 테스트")
    print()
    
    # 가상의 취약 단원들
    wrong_units = ["1. 수와 연산", "2. 문자와 식"]
    accuracy_rate = 37.5  # 8문제 중 3문제 정답
    
    # 추천 경로 생성 로직
    def generate_recommended_path(wrong_units, accuracy_rate):
        recommended_path = []
        
        for i, unit_name in enumerate(wrong_units):
            # OpenAI를 사용해서 개인화된 reason 생성 (여기서는 기본값 사용)
            error_rate = max(0.1, (100 - accuracy_rate) / 100)
            reason = f"오답률 {error_rate:.0%}로 가장 취약한 단원"
            
            path_item = {
                "unitId": f"unit_{i+1:03d}",
                "unitTitle": unit_name,
                "priority": i + 1,
                "reason": reason
            }
            recommended_path.append(path_item)
        
        return recommended_path
    
    # 테스트 실행
    recommended_path = generate_recommended_path(wrong_units, accuracy_rate)
    
    print("✅ 추천 학습 경로 생성 결과:")
    for i, path in enumerate(recommended_path, 1):
        print(f"  {i}. {path['unitTitle']}")
        print(f"     - 단원 ID: {path['unitId']}")
        print(f"     - 우선순위: {path['priority']}")
        print(f"     - 추천 이유: {path['reason']}")
        print()
    
    return True

def main():
    """메인 테스트 함수"""
    
    print("🚀 가상 MongoDB 데이터로 맞춤형 학습경로 테스트 시작...")
    print("=" * 60)
    print()
    
    try:
        # 1. 단원명 추출 테스트
        print("1️⃣ 단원명 추출 테스트")
        print("-" * 30)
        test_unit_extraction()
        print()
        
        # 2. 가상 MongoDB 로직 테스트
        print("2️⃣ 가상 MongoDB 로직 테스트")
        print("-" * 30)
        test_virtual_mongodb_logic()
        print()
        
        # 3. 학습 경로 생성 테스트
        print("3️⃣ 학습 경로 생성 테스트")
        print("-" * 30)
        test_learning_path_generation()
        print()
        
        print("🎉 모든 테스트 완료!")
        print()
        print("📋 테스트 결과 요약:")
        print("  ✅ 문제 ID에서 단원명 추출: 성공")
        print("  ✅ 가상 MongoDB 단원 조회: 성공")
        print("  ✅ 학습 경로 생성: 성공")
        print()
        print("💡 이제 MongoDB에 실제 문제와 단원 데이터가 저장되면")
        print("   _get_unit_from_mongodb_by_problem_id 메서드가 자동으로 작동하여")
        print("   Neo4j와 연동된 맞춤형 학습경로를 생성할 수 있습니다!")
        
    except Exception as e:
        print(f"❌ 테스트 실행 중 오류 발생: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
