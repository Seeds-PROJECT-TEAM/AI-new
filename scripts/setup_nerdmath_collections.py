#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
nerdmath 데이터베이스 컬렉션 설정 스크립트
테이블 정의서 기반으로 정확한 스키마를 가진 컬렉션들을 생성합니다.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from pymongo import MongoClient, ASCENDING, DESCENDING, TEXT
from pymongo.errors import CollectionInvalid, OperationFailure

# AI 디렉토리를 Python 경로에 추가
AI_DIR = Path(__file__).parent
sys.path.insert(0, str(AI_DIR))

# .env 파일 로드
load_dotenv(AI_DIR / ".env")

class NerdMathMongoDBSetup:
    def __init__(self):
        self.client = None
        self.db = None
        self.mongodb_uri = os.getenv("MONGODB_URI")
        
        if not self.mongodb_uri:
            raise RuntimeError("MONGODB_URI 환경변수가 설정되지 않았습니다.")
    
    def connect(self):
        """MongoDB에 연결"""
        try:
            print("🚀 MongoDB 연결 시도 중...")
            self.client = MongoClient(self.mongodb_uri)
            self.db = self.client.nerdmath
            self.client.admin.command("ping")
            print("✅ MongoDB 연결 성공!")
            return True
        except Exception as e:
            print(f"❌ MongoDB 연결 실패: {e}")
            return False
    
    def create_collections(self):
        """테이블 정의서 기반 컬렉션들을 생성"""
        collections_config = {
            # 1. diagnostic_test (진단 테스트)
            "diagnostic_test": {
                "validator": {
                    "$jsonSchema": {
                        "bsonType": "object",
                        "required": ["testid", "userld", "gradeRange", "restartCount", "timeoutMinutes", "startedAt", "endedAt", "durationSec", "completed"],
                        "properties": {
                            "testid": {"bsonType": "objectId"},
                            "userld": {"bsonType": "number"},
                            "gradeRange": {"bsonType": "object"},
                            "selectedRuleSnapshot": {"bsonType": "object"},
                            "restartCount": {"bsonType": "number"},
                            "shuffleSeed": {"bsonType": "number"},
                            "timeoutMinutes": {"bsonType": "number"},
                            "startedAt": {"bsonType": "date"},
                            "endedAt": {"bsonType": "date"},
                            "durationSec": {"bsonType": "number"},
                            "completed": {"bsonType": "bool"}
                        }
                    }
                }
            },
            
            # 2. answer_attempt (문제 풀이·채점 기록)
            "answer_attempt": {
                "validator": {
                    "$jsonSchema": {
                        "bsonType": "object",
                        "required": ["answerld", "userld", "problemld", "mode", "unitid", "userAnswer", "isCorrect", "scoredAt"],
                        "properties": {
                            "answerld": {"bsonType": "objectId"},
                            "userld": {"bsonType": "number"},
                            "problemld": {"bsonType": "objectId"},
                            "mode": {"bsonType": "string"},
                            "setId": {"bsonType": "objectId"},
                            "unitid": {"bsonType": "objectId"},
                            "userAnswer": {"bsonType": "object"},
                            "isCorrect": {"bsonType": "bool"},
                            "vocald": {"bsonType": "objectId"},
                            "scoredAt": {"bsonType": "date"},
                            "explanationShown": {"bsonType": "bool"},
                            "problemOrderIndex": {"bsonType": "number"},
                            "idempotencyKey": {"bsonType": "string"}
                        }
                    }
                }
            },
            
            # 3. diagnostic_analysis (진단 테스트 분석 및 맞춤형 학습)
            "diagnostic_analysis": {
                "validator": {
                    "$jsonSchema": {
                        "bsonType": "object",
                        "required": ["analysisId", "testid", "userld", "analysisType", "aiComment", "recommendedPath", "class", "generatedAt"],
                        "properties": {
                            "analysisId": {"bsonType": "objectId"},
                            "testid": {"bsonType": "objectId"},
                            "userld": {"bsonType": "number"},
                            "analysisType": {"bsonType": "string"},
                            "aiComment": {"bsonType": "string"},
                            "recommendedPath": {"bsonType": "array"},
                            "class": {"bsonType": "string"},
                            "generatedAt": {"bsonType": "date"}
                        }
                    }
                }
            },
            
            # 4. unit (소단원 정보)
            "unit": {
                "validator": {
                    "$jsonSchema": {
                        "bsonType": "object",
                        "required": ["unitId", "subject", "title", "grade", "chapter", "chapterTitle", "orderInGrade", "status", "createdAt"],
                        "properties": {
                            "unitId": {"bsonType": "string"},
                            "subject": {"bsonType": "string"},
                            "title": {"bsonType": "object"},
                            "grade": {"bsonType": "number"},
                            "chapter": {"bsonType": "number"},
                            "chapterTitle": {"bsonType": "string"},
                            "orderInGrade": {"bsonType": "number"},
                            "description": {"bsonType": "object"},
                            "status": {"bsonType": "string"},
                            "createdAt": {"bsonType": "date"}
                        }
                    }
                }
            },
            
            # 5. problem (문제 DB(진단·일반 통합))
            "problem": {
                "validator": {
                    "$jsonSchema": {
                        "bsonType": "object",
                        "required": ["problemId", "unitId", "grade", "chapter", "context", "cognitiveType", "level", "diagnosticTest", "type", "tags", "content", "correctAnswer", "explanation", "createdAt", "updatedAt"],
                        "properties": {
                            "problemId": {"bsonType": "string"},
                            "unitId": {"bsonType": "string"},
                            "grade": {"bsonType": "number"},
                            "chapter": {"bsonType": "number"},
                            "context": {"bsonType": "object"},
                            "cognitiveType": {"bsonType": "string"},
                            "level": {"bsonType": "string"},
                            "diagnosticTest": {"bsonType": "bool"},
                            "type": {"bsonType": "string"},
                            "tags": {"bsonType": "array"},
                            "content": {"bsonType": "object"},
                            "correctAnswer": {"bsonType": "string"},
                            "explanation": {"bsonType": "object"},
                            "imageUrl": {"bsonType": "string"},
                            "createdAt": {"bsonType": "date"},
                            "updatedAt": {"bsonType": "date"}
                        }
                    }
                }
            },
            
            # 6. problem_set (문제 세트 메타 정보)
            "problem_set": {
                "validator": {
                    "$jsonSchema": {
                        "bsonType": "object",
                        "required": ["setId", "userld", "problemids", "createdAt"],
                        "properties": {
                            "setId": {"bsonType": "objectId"},
                            "userld": {"bsonType": "number"},
                            "unitld": {"bsonType": "objectId"},
                            "problemids": {"bsonType": "array"},
                            "ruleSnapshot": {"bsonType": "object"},
                            "mode": {"bsonType": "string"},
                            "title": {"bsonType": "string"},
                            "createdAt": {"bsonType": "date"}
                        }
                    }
                }
            },
            
            # 7. concept (개념 설명)
            "concept": {
                "validator": {
                    "$jsonSchema": {
                        "bsonType": "object",
                        "required": ["conceptId", "unitId", "blocks", "createdAt"],
                        "properties": {
                            "conceptId": {"bsonType": "string"},
                            "unitId": {"bsonType": "string"},
                            "blocks": {"bsonType": "array"},
                            "createdAt": {"bsonType": "date"}
                        }
                    }
                }
            },
            
            # 8. vocabulary (어휘 카드)
            "vocabulary": {
                "validator": {
                    "$jsonSchema": {
                        "bsonType": "object",
                        "required": ["vocald", "type", "category", "word", "meaning", "createdAt"],
                        "properties": {
                            "vocald": {"bsonType": "objectId"},
                            "type": {"bsonType": "string"},
                            "category": {"bsonType": "string"},
                            "unitId": {"bsonType": "objectId"},
                            "word": {"bsonType": "string"},
                            "meaning": {"bsonType": "string"},
                            "etymology": {"bsonType": "string"},
                            "imageUrl": {"bsonType": "string"},
                            "createdAt": {"bsonType": "date"}
                        }
                    }
                }
            },
            
            # 9. progress (학습 진행률)
            "progress": {
                "validator": {
                    "$jsonSchema": {
                        "bsonType": "object",
                        "required": ["progressId", "userld", "unitId", "conceptProgress", "problemProgress", "vocabProgress", "updatedAt"],
                        "properties": {
                            "progressId": {"bsonType": "objectId"},
                            "userld": {"bsonType": "number"},
                            "unitId": {"bsonType": "objectId"},
                            "conceptProgress": {"bsonType": "number"},
                            "problemProgress": {"bsonType": "number"},
                            "vocabProgress": {"bsonType": "number"},
                            "updatedAt": {"bsonType": "date"}
                        }
                    }
                }
            },
            
            # 10. activity_log (사용자 활동 집계)
            "activity_log": {
                "validator": {
                    "$jsonSchema": {
                        "bsonType": "object",
                        "required": ["logld", "userld", "date", "todaySolved", "studyDurationMin", "totalProblems", "totalStudyMinutes", "attendanceCount"],
                        "properties": {
                            "logld": {"bsonType": "objectId"},
                            "userld": {"bsonType": "number"},
                            "date": {"bsonType": "string"},
                            "todaySolved": {"bsonType": "number"},
                            "studyDurationMin": {"bsonType": "number"},
                            "totalProblems": {"bsonType": "number"},
                            "totalStudyMinutes": {"bsonType": "number"},
                            "attendanceCount": {"bsonType": "number"}
                        }
                    }
                }
            },
            
            # 11. gamification_state (게이미피케이션 상태)
            "gamification_state": {
                "validator": {
                    "$jsonSchema": {
                        "bsonType": "object",
                        "required": ["gamifild", "userld", "level", "xp", "totalXp", "nextLevelXp", "equippedCharacterld", "equippedSkinld", "unlockedSkinlds", "createdAt", "updatedAt"],
                        "properties": {
                            "gamifild": {"bsonType": "objectId"},
                            "userld": {"bsonType": "number"},
                            "level": {"bsonType": "number"},
                            "xp": {"bsonType": "number"},
                            "totalXp": {"bsonType": "number"},
                            "nextLevelXp": {"bsonType": "number"},
                            "equippedCharacterld": {"bsonType": "string"},
                            "equippedSkinld": {"bsonType": "string"},
                            "unlockedSkinlds": {"bsonType": "array"},
                            "lastLeveledUpAt": {"bsonType": "date"},
                            "createdAt": {"bsonType": "date"},
                            "updatedAt": {"bsonType": "date"}
                        }
                    }
                }
            },
            
            # 12. xp_transactions (경험치 지급 이력)
            "xp_transactions": {
                "validator": {
                    "$jsonSchema": {
                        "bsonType": "object",
                        "required": ["transactionld", "userld", "amount", "reason", "idempotencyKey", "at"],
                        "properties": {
                            "transactionld": {"bsonType": "objectId"},
                            "userld": {"bsonType": "number"},
                            "amount": {"bsonType": "number"},
                            "reason": {"bsonType": "string"},
                            "reasonRef": {"bsonType": "string"},
                            "idempotencyKey": {"bsonType": "string"},
                            "at": {"bsonType": "date"}
                        }
                    }
                }
            },
            
            # 13. learning_time_log (학습 시간 기록)
            "learning_time_log": {
                "validator": {
                    "$jsonSchema": {
                        "bsonType": "object",
                        "required": ["learningTimeld", "userld", "activityType", "contentid", "startedAt", "endedAt", "durationSeconds", "createdAt"],
                        "properties": {
                            "learningTimeld": {"bsonType": "objectId"},
                            "userld": {"bsonType": "number"},
                            "activityType": {"bsonType": "string"},
                            "contentid": {"bsonType": "objectId"},
                            "sessionld": {"bsonType": "objectId"},
                            "startedAt": {"bsonType": "date"},
                            "endedAt": {"bsonType": "date"},
                            "durationSeconds": {"bsonType": "number"},
                            "createdAt": {"bsonType": "date"}
                        }
                    }
                }
            },
            
            # 14. bookmark (즐겨찾기)
            "bookmark": {
                "validator": {
                    "$jsonSchema": {
                        "bsonType": "object",
                        "required": ["bookmarkid", "userld", "problemld", "bookmarkedAt", "createdAt", "updatedAt"],
                        "properties": {
                            "bookmarkid": {"bsonType": "objectId"},
                            "userld": {"bsonType": "number"},
                            "problemld": {"bsonType": "objectId"},
                            "unitld": {"bsonType": "objectId"},
                            "bookmarkedAt": {"bsonType": "date"},
                            "createdAt": {"bsonType": "date"},
                            "updatedAt": {"bsonType": "date"}
                        }
                    }
                }
            }
        }
        
        print("📋 nerdmath 컬렉션 생성 시작...")
        
        for collection_name, config in collections_config.items():
            try:
                # 컬렉션이 이미 존재하는지 확인
                if collection_name in self.db.list_collection_names():
                    print(f"⚠️ 컬렉션 '{collection_name}' 이미 존재함")
                    continue
                
                # 컬렉션 생성
                self.db.create_collection(collection_name, **config)
                print(f"✅ 컬렉션 '{collection_name}' 생성 완료")
                
            except CollectionInvalid as e:
                print(f"⚠️ 컬렉션 '{collection_name}' 생성 실패 (이미 존재): {e}")
            except Exception as e:
                print(f"❌ 컬렉션 '{collection_name}' 생성 실패: {e}")
        
        print("🎉 모든 nerdmath 컬렉션 생성 완료!")
    
    def create_indexes(self):
        """테이블 정의서 기반 인덱스들을 생성"""
        indexes_config = {
            "diagnostic_test": [
                [("testid", ASCENDING)],
                [("userld", ASCENDING)],
                [("startedAt", DESCENDING)],
                [("completed", ASCENDING)]
            ],
            
            "answer_attempt": [
                [("answerld", ASCENDING)],
                [("userld", ASCENDING)],
                [("problemld", ASCENDING)],
                [("unitid", ASCENDING)],
                [("scoredAt", DESCENDING)],
                [("mode", ASCENDING)]
            ],
            
            "diagnostic_analysis": [
                [("analysisId", ASCENDING)],
                [("testid", ASCENDING)],
                [("userld", ASCENDING)],
                [("generatedAt", DESCENDING)],
                [("analysisType", ASCENDING)]
            ],
            
            "unit": [
                [("unitId", ASCENDING)],
                [("subject", ASCENDING)],
                [("grade", ASCENDING)],
                [("chapter", ASCENDING)],
                [("orderInGrade", ASCENDING)],
                [("status", ASCENDING)]
            ],
            
            "problem": [
                [("problemld", ASCENDING)],
                [("unitId", ASCENDING)],
                [("grade", ASCENDING)],
                [("chapter", ASCENDING)],
                [("cognitiveType", ASCENDING)],
                [("level", ASCENDING)],
                [("diagnosticTest", ASCENDING)],
                [("type", ASCENDING)],
                [("tags", ASCENDING)],
                [("content.text", TEXT)]
            ],
            
            "problem_set": [
                [("setId", ASCENDING)],
                [("userld", ASCENDING)],
                [("unitld", ASCENDING)],
                [("mode", ASCENDING)],
                [("createdAt", DESCENDING)]
            ],
            
            "concept": [
                [("conceptId", ASCENDING)],
                [("unitId", ASCENDING)]
            ],
            
            "vocabulary": [
                [("vocald", ASCENDING)],
                [("type", ASCENDING)],
                [("category", ASCENDING)],
                [("unitId", ASCENDING)],
                [("word", TEXT)]
            ],
            
            "progress": [
                [("progressId", ASCENDING)],
                [("userld", ASCENDING)],
                [("unitId", ASCENDING)],
                [("updatedAt", DESCENDING)]
            ],
            
            "activity_log": [
                [("logld", ASCENDING)],
                [("userld", ASCENDING)],
                [("date", ASCENDING)],
                [("todaySolved", DESCENDING)]
            ],
            
            "gamification_state": [
                [("gamifild", ASCENDING)],
                [("userld", ASCENDING)],
                [("level", DESCENDING)],
                [("totalXp", DESCENDING)]
            ],
            
            "xp_transactions": [
                [("transactionld", ASCENDING)],
                [("userld", ASCENDING)],
                [("reason", ASCENDING)],
                [("at", DESCENDING)]
            ],
            
            "learning_time_log": [
                [("learningTimeld", ASCENDING)],
                [("userld", ASCENDING)],
                [("activityType", ASCENDING)],
                [("contentid", ASCENDING)],
                [("startedAt", DESCENDING)]
            ],
            
            "bookmark": [
                [("bookmarkid", ASCENDING)],
                [("userld", ASCENDING)],
                [("problemld", ASCENDING)],
                [("unitld", ASCENDING)],
                [("bookmarkedAt", DESCENDING)]
            ]
        }
        
        print("🔍 nerdmath 인덱스 생성 시작...")
        
        for collection_name, indexes in indexes_config.items():
            try:
                collection = self.db[collection_name]
                
                for index_spec in indexes:
                    try:
                        # 인덱스 이름 생성
                        index_name = f"{'_'.join([str(field[0]) for field in index_spec])}_idx"
                        
                        # 인덱스 생성
                        collection.create_index(index_spec, name=index_name)
                        print(f"✅ 인덱스 '{index_name}' 생성 완료 ({collection_name})")
                        
                    except OperationFailure as e:
                        if "already exists" in str(e):
                            print(f"⚠️ 인덱스 '{index_name}' 이미 존재함 ({collection_name})")
                        else:
                            print(f"❌ 인덱스 '{index_name}' 생성 실패 ({collection_name}): {e}")
                            
            except Exception as e:
                print(f"❌ 컬렉션 '{collection_name}' 인덱스 생성 실패: {e}")
        
        print("🎉 모든 nerdmath 인덱스 생성 완료!")
    
    def setup_database(self):
        """nerdmath 데이터베이스 전체 설정"""
        if not self.connect():
            return False
        
        try:
            self.create_collections()
            self.create_indexes()
            print("\n🎉 nerdmath MongoDB 데이터베이스 설정 완료!")
            return True
            
        except Exception as e:
            print(f"❌ 데이터베이스 설정 실패: {e}")
            return False
        
        finally:
            if self.client:
                self.client.close()
                print("🔌 MongoDB 연결 종료")

def main():
    """메인 함수"""
    print("🚀 nerdmath MongoDB 컬렉션 설정 시작")
    print("=" * 60)
    
    try:
        setup = NerdMathMongoDBSetup()
        setup.setup_database()
        
    except Exception as e:
        print(f"❌ 스크립트 실행 실패: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
