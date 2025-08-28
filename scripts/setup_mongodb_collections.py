#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MongoDB 컬렉션 설정 및 인덱스 생성 스크립트
테이블 정의서 기반으로 필요한 컬렉션들을 생성하고 인덱스를 설정합니다.
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

class MongoDBSetup:
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
        """필요한 컬렉션들을 생성"""
        collections_config = {
            # 사용자 관련 컬렉션
            "users": {
                "validator": {
                    "$jsonSchema": {
                        "bsonType": "object",
                        "required": ["email", "password", "name"],
                        "properties": {
                            "email": {"bsonType": "string"},
                            "password": {"bsonType": "string"},
                            "name": {"bsonType": "string"},
                            "birthDate": {"bsonType": ["string", "null"]},
                            "phoneNumber": {"bsonType": ["string", "null"]},
                            "nickname": {"bsonType": ["string", "null"]},
                            "createdAt": {"bsonType": "date"},
                            "isActive": {"bsonType": "bool"},
                            "agreeTerms": {"bsonType": "bool"},
                            "agreePrivacy": {"bsonType": "bool"},
                            "agreeMarketing": {"bsonType": "bool"}
                        }
                    }
                }
            },
            
            "guardian_info": {
                "validator": {
                    "$jsonSchema": {
                        "bsonType": "object",
                        "required": ["userId", "guardianName", "guardianPhone"],
                        "properties": {
                            "userId": {"bsonType": "objectId"},
                            "guardianName": {"bsonType": "string"},
                            "guardianPhone": {"bsonType": "string"},
                            "relationship": {"bsonType": "string"},
                            "createdAt": {"bsonType": "date"}
                        }
                    }
                }
            },
            
            "user_auth": {
                "validator": {
                    "$jsonSchema": {
                        "bsonType": "object",
                        "required": ["userId", "refreshToken"],
                        "properties": {
                            "userId": {"bsonType": "objectId"},
                            "refreshToken": {"bsonType": "string"},
                            "expiresAt": {"bsonType": "date"},
                            "createdAt": {"bsonType": "date"}
                        }
                    }
                }
            },
            
            "email_verification": {
                "validator": {
                    "$jsonSchema": {
                        "bsonType": "object",
                        "required": ["email", "verificationCode", "expiresAt"],
                        "properties": {
                            "email": {"bsonType": "string"},
                            "verificationCode": {"bsonType": "string"},
                            "expiresAt": {"bsonType": "date"},
                            "isVerified": {"bsonType": "bool"},
                            "createdAt": {"bsonType": "date"}
                        }
                    }
                }
            },
            
            "password_reset": {
                "validator": {
                    "$jsonSchema": {
                        "bsonType": "object",
                        "required": ["email", "resetToken", "expiresAt"],
                        "properties": {
                            "email": {"bsonType": "string"},
                            "resetToken": {"bsonType": "string"},
                            "expiresAt": {"bsonType": "date"},
                            "isUsed": {"bsonType": "bool"},
                            "createdAt": {"bsonType": "date"}
                        }
                    }
                }
            },
            
            "user_withdrawal": {
                "validator": {
                    "$jsonSchema": {
                        "bsonType": "object",
                        "required": ["userId", "withdrawalReason", "withdrawnAt"],
                        "properties": {
                            "userId": {"bsonType": "objectId"},
                            "withdrawalReason": {"bsonType": "string"},
                            "withdrawnAt": {"bsonType": "date"},
                            "createdAt": {"bsonType": "date"}
                        }
                    }
                }
            },
            
            # 학습 관련 컬렉션
            "diagnostic_tests": {
                "validator": {
                    "$jsonSchema": {
                        "bsonType": "object",
                        "required": ["testId", "userId", "grade", "subject"],
                        "properties": {
                            "testId": {"bsonType": "string"},
                            "userId": {"bsonType": "objectId"},
                            "grade": {"bsonType": "int"},
                            "subject": {"bsonType": "string"},
                            "problems": {"bsonType": "array"},
                            "startTime": {"bsonType": "date"},
                            "endTime": {"bsonType": "date"},
                            "score": {"bsonType": "double"},
                            "status": {"bsonType": "string"}
                        }
                    }
                }
            },
            
            "answer_attempts": {
                "validator": {
                    "$jsonSchema": {
                        "bsonType": "object",
                        "required": ["attemptId", "userId", "problemId", "userAnswer"],
                        "properties": {
                            "attemptId": {"bsonType": "string"},
                            "userId": {"bsonType": "objectId"},
                            "problemId": {"bsonType": "string"},
                            "userAnswer": {"bsonType": "string"},
                            "isCorrect": {"bsonType": "bool"},
                            "attemptTime": {"bsonType": "date"},
                            "timeSpent": {"bsonType": "int"}
                        }
                    }
                }
            },
            
            "diagnostic_analysis": {
                "validator": {
                    "$jsonSchema": {
                        "bsonType": "object",
                        "required": ["analysisId", "userId", "testId", "analysisResult"],
                        "properties": {
                            "analysisId": {"bsonType": "string"},
                            "userId": {"bsonType": "objectId"},
                            "testId": {"bsonType": "string"},
                            "analysisResult": {"bsonType": "object"},
                            "weakConcepts": {"bsonType": "array"},
                            "recommendations": {"bsonType": "array"},
                            "createdAt": {"bsonType": "date"},
                            "updatedAt": {"bsonType": "date"}
                        }
                    }
                }
            },
            
            "units": {
                "validator": {
                    "$jsonSchema": {
                        "bsonType": "object",
                        "required": ["unitId", "unitCode", "unitTitle", "grade"],
                        "properties": {
                            "unitId": {"bsonType": "string"},
                            "unitCode": {"bsonType": "string"},
                            "unitTitle": {"bsonType": "string"},
                            "grade": {"bsonType": "int"},
                            "subject": {"bsonType": "string"},
                            "description": {"bsonType": "string"},
                            "prerequisites": {"bsonType": "array"},
                            "createdAt": {"bsonType": "date"}
                        }
                    }
                }
            },
            
            "concepts": {
                "validator": {
                    "$jsonSchema": {
                        "bsonType": "object",
                        "required": ["conceptId", "conceptName", "unitId"],
                        "properties": {
                            "conceptId": {"bsonType": "string"},
                            "conceptName": {"bsonType": "string"},
                            "unitId": {"bsonType": "string"},
                            "description": {"bsonType": "string"},
                            "difficulty": {"bsonType": "string"},
                            "prerequisites": {"bsonType": "array"},
                            "createdAt": {"bsonType": "date"}
                        }
                    }
                }
            },
            
            "learning_time_logs": {
                "validator": {
                    "$jsonSchema": {
                        "bsonType": "object",
                        "required": ["logId", "userId", "conceptId", "studyTime"],
                        "properties": {
                            "logId": {"bsonType": "string"},
                            "userId": {"bsonType": "objectId"},
                            "conceptId": {"bsonType": "string"},
                            "studyTime": {"bsonType": "int"},
                            "startTime": {"bsonType": "date"},
                            "endTime": {"bsonType": "date"},
                            "createdAt": {"bsonType": "date"}
                        }
                    }
                }
            },
            
            # 문제 관련 컬렉션
            "problems": {
                "validator": {
                    "$jsonSchema": {
                        "bsonType": "object",
                        "required": ["problemId", "problemText", "conceptId"],
                        "properties": {
                            "problemId": {"bsonType": "string"},
                            "problemText": {"bsonType": "string"},
                            "problemLatex": {"bsonType": ["string", "null"]},
                            "conceptId": {"bsonType": "string"},
                            "unitId": {"bsonType": "string"},
                            "difficulty": {"bsonType": "string"},
                            "answer": {"bsonType": "string"},
                            "solution": {"bsonType": "string"},
                            "createdAt": {"bsonType": "date"}
                        }
                    }
                }
            },
            
            "problem_sets": {
                "validator": {
                    "$jsonSchema": {
                        "bsonType": "object",
                        "required": ["setId", "setName", "problems"],
                        "properties": {
                            "setId": {"bsonType": "string"},
                            "setName": {"bsonType": "string"},
                            "description": {"bsonType": "string"},
                            "problems": {"bsonType": "array"},
                            "difficulty": {"bsonType": "string"},
                            "estimatedTime": {"bsonType": "int"},
                            "createdAt": {"bsonType": "date"}
                        }
                    }
                }
            },
            
            "vocabulary": {
                "validator": {
                    "$jsonSchema": {
                        "bsonType": "object",
                        "required": ["vocaId", "term", "definition"],
                        "properties": {
                            "vocaId": {"bsonType": "string"},
                            "term": {"bsonType": "string"},
                            "definition": {"bsonType": "string"},
                            "examples": {"bsonType": "array"},
                            "conceptId": {"bsonType": "string"},
                            "createdAt": {"bsonType": "date"}
                        }
                    }
                }
            },
            
            "progress": {
                "validator": {
                    "$jsonSchema": {
                        "bsonType": "object",
                        "required": ["progressId", "userId", "conceptId"],
                        "properties": {
                            "progressId": {"bsonType": "string"},
                            "userId": {"bsonType": "objectId"},
                            "conceptId": {"bsonType": "string"},
                            "completionRate": {"bsonType": "double"},
                            "lastStudyDate": {"bsonType": "date"},
                            "streak": {"bsonType": "int"},
                            "createdAt": {"bsonType": "date"},
                            "updatedAt": {"bsonType": "date"}
                        }
                    }
                }
            },
            
            "activity_logs": {
                "validator": {
                    "$jsonSchema": {
                        "bsonType": "object",
                        "required": ["logId", "userId", "activityType"],
                        "properties": {
                            "logId": {"bsonType": "string"},
                            "userId": {"bsonType": "objectId"},
                            "activityType": {"bsonType": "string"},
                            "activityData": {"bsonType": "object"},
                            "timestamp": {"bsonType": "date"},
                            "createdAt": {"bsonType": "date"}
                        }
                    }
                }
            },
            
            "gamification_state": {
                "validator": {
                    "$jsonSchema": {
                        "bsonType": "object",
                        "required": ["gamifiId", "userId"],
                        "properties": {
                            "gamifiId": {"bsonType": "string"},
                            "userId": {"bsonType": "objectId"},
                            "level": {"bsonType": "int"},
                            "experience": {"bsonType": "int"},
                            "badges": {"bsonType": "array"},
                            "achievements": {"bsonType": "array"},
                            "createdAt": {"bsonType": "date"},
                            "updatedAt": {"bsonType": "date"}
                        }
                    }
                }
            },
            
            "xp_transactions": {
                "validator": {
                    "$jsonSchema": {
                        "bsonType": "object",
                        "required": ["transactionId", "userId", "xpAmount", "reason"],
                        "properties": {
                            "transactionId": {"bsonType": "string"},
                            "userId": {"bsonType": "objectId"},
                            "xpAmount": {"bsonType": "int"},
                            "reason": {"bsonType": "string"},
                            "timestamp": {"bsonType": "date"},
                            "createdAt": {"bsonType": "date"}
                        }
                    }
                }
            },
            
            "bookmarks": {
                "validator": {
                    "$jsonSchema": {
                        "bsonType": "object",
                        "required": ["bookmarkId", "userId", "itemId", "itemType"],
                        "properties": {
                            "bookmarkId": {"bsonType": "string"},
                            "userId": {"bsonType": "objectId"},
                            "itemId": {"bsonType": "string"},
                            "itemType": {"bsonType": "string"},
                            "createdAt": {"bsonType": "date"}
                        }
                    }
                }
            }
        }
        
        print("📋 컬렉션 생성 시작...")
        
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
        
        print("🎉 모든 컬렉션 생성 완료!")
    
    def create_indexes(self):
        """필요한 인덱스들을 생성"""
        indexes_config = {
            "users": [
                [("email", ASCENDING)],
                [("phoneNumber", ASCENDING)],
                [("createdAt", DESCENDING)]
            ],
            
            "guardian_info": [
                [("userId", ASCENDING)]
            ],
            
            "user_auth": [
                [("userId", ASCENDING)],
                [("refreshToken", ASCENDING)]
            ],
            
            "email_verification": [
                [("email", ASCENDING)],
                [("verificationCode", ASCENDING)],
                [("expiresAt", ASCENDING)]
            ],
            
            "password_reset": [
                [("email", ASCENDING)],
                [("resetToken", ASCENDING)],
                [("expiresAt", ASCENDING)]
            ],
            
            "diagnostic_tests": [
                [("testId", ASCENDING)],
                [("userId", ASCENDING)],
                [("grade", ASCENDING)],
                [("createdAt", DESCENDING)]
            ],
            
            "answer_attempts": [
                [("attemptId", ASCENDING)],
                [("userId", ASCENDING)],
                [("problemId", ASCENDING)],
                [("attemptTime", DESCENDING)]
            ],
            
            "diagnostic_analysis": [
                [("analysisId", ASCENDING)],
                [("userId", ASCENDING)],
                [("testId", ASCENDING)],
                [("createdAt", DESCENDING)]
            ],
            
            "units": [
                [("unitId", ASCENDING)],
                [("unitCode", ASCENDING)],
                [("grade", ASCENDING)],
                [("subject", ASCENDING)]
            ],
            
            "concepts": [
                [("conceptId", ASCENDING)],
                [("unitId", ASCENDING)],
                [("difficulty", ASCENDING)]
            ],
            
            "learning_time_logs": [
                [("logId", ASCENDING)],
                [("userId", ASCENDING)],
                [("conceptId", ASCENDING)],
                [("startTime", DESCENDING)]
            ],
            
            "problems": [
                [("problemId", ASCENDING)],
                [("conceptId", ASCENDING)],
                [("unitId", ASCENDING)],
                [("difficulty", ASCENDING)],
                [("problemText", TEXT)]
            ],
            
            "problem_sets": [
                [("setId", ASCENDING)],
                [("difficulty", ASCENDING)]
            ],
            
            "vocabulary": [
                [("vocaId", ASCENDING)],
                [("term", TEXT)],
                [("conceptId", ASCENDING)]
            ],
            
            "progress": [
                [("progressId", ASCENDING)],
                [("userId", ASCENDING)],
                [("conceptId", ASCENDING)],
                [("completionRate", DESCENDING)]
            ],
            
            "activity_logs": [
                [("logId", ASCENDING)],
                [("userId", ASCENDING)],
                [("activityType", ASCENDING)],
                [("timestamp", DESCENDING)]
            ],
            
            "gamification_state": [
                [("gamifiId", ASCENDING)],
                [("userId", ASCENDING)],
                [("level", DESCENDING)]
            ],
            
            "xp_transactions": [
                [("transactionId", ASCENDING)],
                [("userId", ASCENDING)],
                [("timestamp", DESCENDING)]
            ],
            
            "bookmarks": [
                [("bookmarkId", ASCENDING)],
                [("userId", ASCENDING)],
                [("itemId", ASCENDING)],
                [("createdAt", DESCENDING)]
            ]
        }
        
        print("🔍 인덱스 생성 시작...")
        
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
        
        print("🎉 모든 인덱스 생성 완료!")
    
    def setup_database(self):
        """데이터베이스 전체 설정"""
        if not self.connect():
            return False
        
        try:
            self.create_collections()
            self.create_indexes()
            print("\n🎉 MongoDB 데이터베이스 설정 완료!")
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
    print("🚀 MongoDB 컬렉션 설정 시작")
    print("=" * 60)
    
    try:
        setup = MongoDBSetup()
        setup.setup_database()
        
    except Exception as e:
        print(f"❌ 스크립트 실행 실패: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
