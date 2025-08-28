#!/usr/bin/env python3
"""
MongoDB 데이터를 JSON 파일로 내보내기
"""

import json
from datetime import datetime
from AI.app.services.mongo_service import MongoService

def export_mongodb_data():
    """MongoDB 데이터를 JSON 파일로 내보내기"""
    
    # MongoDB 연결
    mongo = MongoService()
    mongo._connect_to_mongodb()
    
    # 데이터 수집
    export_data = {
        "exported_at": datetime.utcnow().isoformat(),
        "total_diagnostic_results": mongo._db.express_diagnostic_results.count_documents({}),
        "total_learning_paths": mongo._db.learning_paths.count_documents({}),
        "diagnostic_results": [],
        "learning_paths": []
    }
    
    # 진단 결과 데이터 수집
    diagnostic_results = list(mongo._db.express_diagnostic_results.find().sort('_id', -1).limit(5))
    for result in diagnostic_results:
        # ObjectId를 문자열로 변환
        result['_id'] = str(result['_id'])
        export_data["diagnostic_results"].append(result)
    
    # 학습 경로 데이터 수집
    learning_paths = list(mongo._db.learning_paths.find().sort('_id', -1).limit(5))
    for path in learning_paths:
        # ObjectId를 문자열로 변환
        path['_id'] = str(path['_id'])
        export_data["learning_paths"].append(path)
    
    # JSON 파일로 저장
    filename = f"mongodb_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, indent=2, ensure_ascii=False, default=str)
    
    print(f"✅ MongoDB 데이터를 {filename}에 저장했습니다!")
    print(f"📊 진단 결과: {len(export_data['diagnostic_results'])}개")
    print(f"📊 학습 경로: {len(export_data['learning_paths'])}개")
    
    return filename

if __name__ == "__main__":
    export_mongodb_data()
