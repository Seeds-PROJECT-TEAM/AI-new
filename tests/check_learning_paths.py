#!/usr/bin/env python3
"""
저장된 맞춤형 학습 경로 확인
"""

from AI.app.services.mongo_service import MongoService

def check_learning_paths():
    """저장된 학습 경로 확인"""
    
    # MongoDB 연결
    mongo = MongoService()
    mongo._connect_to_mongodb()
    
    # 학습 경로 데이터 조회
    paths = list(mongo._db.learning_paths.find().sort('_id', -1).limit(5))
    
    print(f"=== 저장된 맞춤형 학습 경로 {len(paths)}개 ===")
    
    for i, path in enumerate(paths, 1):
        print(f"\n📚 {i}번째 학습 경로:")
        print(f"   ID: {path.get('pathId', 'N/A')}")
        print(f"   이름: {path.get('pathName', 'N/A')}")
        print(f"   설명: {path.get('description', 'N/A')}")
        print(f"   노드 수: {len(path.get('nodes', []))}")
        print(f"   총 개념: {path.get('totalConcepts', 0)}개")
        print(f"   예상 시간: {path.get('estimatedDuration', 0)}분")
        print(f"   상태: {path.get('status', 'N/A')}")
        print(f"   생성시간: {path.get('createdAt', 'N/A')}")
        
        # 노드 상세 정보
        nodes = path.get('nodes', [])
        if nodes:
            print(f"   📋 학습 노드:")
            for j, node in enumerate(nodes[:3], 1):  # 최대 3개만 표시
                print(f"      {j}. {node.get('concept', 'N/A')} (우선순위: {node.get('priority', 'N/A')})")
            if len(nodes) > 3:
                print(f"      ... 외 {len(nodes) - 3}개")
        else:
            print(f"   ⚠️ 학습 노드가 없습니다")
    
    print(f"\n✅ 총 {len(paths)}개의 학습 경로를 확인했습니다!")

if __name__ == "__main__":
    check_learning_paths()
