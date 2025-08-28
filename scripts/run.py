from fastapi import FastAPI
import os
from pathlib import Path
from dotenv import load_dotenv

# AI/.env 파일 로드
env_path = Path(__file__).resolve().parents[1] / ".env"
if env_path.exists():
    load_dotenv(env_path)
    print(f"✅ .env 파일 로드됨: {env_path}")

app = FastAPI(
    title="nerdmath",
    version="1.0.0",
    description="Simple Test App with MongoDB Support"
)

@app.get("/")
def root():
    return {"message": "Hello World", "status": "running"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/test")
def test():
    return {"message": "Test endpoint working"}

@app.get("/mongo/status")
def mongo_status():
    """MongoDB 연결 상태 확인"""
    try:
        # 환경변수 확인
        mongodb_uri = os.getenv("MONGODB_URI")
        if not mongodb_uri:
            return {
                "status": "not_configured",
                "message": "MONGODB_URI 환경변수가 설정되지 않음",
                "env_file_exists": Path("../.env").exists()
            }
        
        # MongoDB 연결 시도
        from pymongo import MongoClient
        client = MongoClient(mongodb_uri, serverSelectionTimeoutMS=3000)
        client.admin.command('ping')
        
        # 연결 성공
        db_list = client.list_database_names()
        client.close()
        
        return {
            "status": "connected",
            "message": "MongoDB 연결 성공",
            "available_databases": db_list,
            "uri": mongodb_uri[:50] + "..." if len(mongodb_uri) > 50 else mongodb_uri
        }
        
    except Exception as e:
        return {
            "status": "connection_failed",
            "message": f"MongoDB 연결 실패: {str(e)}",
            "error_type": type(e).__name__
        }

@app.get("/env/check")
def env_check():
    """환경변수 상태 확인"""
    env_vars = {
        "MONGODB_URI": os.getenv("MONGODB_URI"),
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
        "MODEL_CHAT": os.getenv("MODEL_CHAT"),
        "SERVICE_TOKEN": os.getenv("SERVICE_TOKEN")
    }
    
    return {
        "environment_variables": env_vars,
        "env_file_exists": Path("../.env").exists(),
        "current_working_dir": str(Path.cwd())
    }
