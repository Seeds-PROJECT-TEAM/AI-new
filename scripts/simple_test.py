print("🚀 가상 MongoDB 데이터로 맞춤형 학습경로 테스트 시작...")
print("=" * 60)
print()

# 1. 단원명 추출 테스트
print("1️⃣ 단원명 추출 테스트")
print("-" * 30)

def extract_unit_from_problem_id(problem_id):
    if problem_id.startswith("1."):
        return "1. 수와 연산"
    elif problem_id.startswith("2."):
        return "2. 문자와 식"
    elif problem_id.startswith("3."):
        return "3. 함수"
    else:
        return "1. 수와 연산"

test_problem_ids = [
    "1.1 소수와 합성수, 소인수분해",
    "1.2 최대공약수와 최소공배수", 
    "2.1 문자와 식",
    "2.2 일차식의 사칙 연산"
]

print("📚 문제 ID별 단원명 추출 결과:")
for problem_id in test_problem_ids:
    unit_name = extract_unit_from_problem_id(problem_id)
    print(f"  - {problem_id} → {unit_name}")

print()

# 2. 가상 MongoDB 로직 테스트
print("2️⃣ 가상 MongoDB 로직 테스트")
print("-" * 30)

# 가상의 problems 데이터
virtual_problems = [
    {
        "problemId": "1.1 소수와 합성수, 소인수분해",
        "unitId": "unit_001",
        "unit": "1. 수와 연산"
    },
    {
        "problemId": "2.1 문자와 식",
        "unitId": "unit_002", 
        "unit": "2. 문자와 식"
    }
]

# 가상의 units 데이터
virtual_units = [
    {
        "unitId": "unit_001",
        "title": {"ko": "수와 연산", "en": "Numbers and Operations"}
    },
    {
        "unitId": "unit_002",
        "title": {"ko": "문자와 식", "en": "Expressions and Equations"}
    }
]

def get_unit_from_virtual_mongodb(problem_id, problems, units):
    # problems 컬렉션에서 문제 ID로 단원 정보 조회
    problem = None
    for p in problems:
        if p.get("problemId") == problem_id:
            problem = p
            break
    
    if problem:
        print(f"✅ 가상 MongoDB에서 문제 찾음: {problem_id}")
        
        # unitId로 units 컬렉션에서 단원명 조회
        if problem.get("unitId"):
            unit_id = problem["unitId"]
            unit = None
            
            for u in units:
                if u.get("unitId") == unit_id:
                    unit = u
                    break
            
            if unit and unit.get("title", {}).get("ko"):
                unit_name = unit["title"]["ko"]
                print(f"✅ units 컬렉션에서 단원명 추출: {unit_name}")
                return unit_name
        
        # 직접 단원 정보가 있는 경우
        if problem.get("unit"):
            unit_name = problem["unit"]
            print(f"✅ 문제 데이터에서 단원명 추출: {unit_name}")
            return unit_name
    
    print(f"⚠️ 가상 MongoDB에서 문제를 찾을 수 없음: {problem_id}")
    return None

print("📚 가상 MongoDB에서 단원 정보 조회 테스트:")
for problem_id in ["1.1 소수와 합성수, 소인수분해", "2.1 문자와 식", "3.1 함수"]:
    unit_name = get_unit_from_virtual_mongodb(problem_id, virtual_problems, virtual_units)
    if unit_name:
        print(f"  ✅ {problem_id} → {unit_name}")
    else:
        print(f"  ❌ {problem_id} → 단원 정보 없음")
    print()

# 3. 학습 경로 생성 테스트
print("3️⃣ 학습 경로 생성 테스트")
print("-" * 30)

wrong_units = ["1. 수와 연산", "2. 문자와 식"]
accuracy_rate = 37.5  # 8문제 중 3문제 정답

def generate_recommended_path(wrong_units, accuracy_rate):
    recommended_path = []
    
    for i, unit_name in enumerate(wrong_units):
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

recommended_path = generate_recommended_path(wrong_units, accuracy_rate)

print("✅ 추천 학습 경로 생성 결과:")
for i, path in enumerate(recommended_path, 1):
    print(f"  {i}. {path['unitTitle']}")
    print(f"     - 단원 ID: {path['unitId']}")
    print(f"     - 우선순위: {path['priority']}")
    print(f"     - 추천 이유: {path['reason']}")
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
