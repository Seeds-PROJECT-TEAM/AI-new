from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
import os
from bson.objectid import ObjectId
import datetime
from pathlib import Path

# MongoDB 연결을 지연시켜 서버 시작 속도 향상
mongodb_available = False
problems = None
ping = lambda: False

def init_mongodb():
    """MongoDB 연결을 필요할 때만 초기화"""
    global mongodb_available, problems, ping
    try:
        from .db.mongo import init_mongodb as mongo_init, ping as mongo_ping
        mongo_init()  # MongoDB 연결 초기화
        ping = mongo_ping
        mongodb_available = True
        print("✅ MongoDB 연결 초기화 완료")
    except Exception as e:
        print(f"⚠️ MongoDB 연결 실패 (로컬 모드): {e}")
        mongodb_available = False
        problems = None
        ping = lambda: False

from .api.v1_ai import router as ai_router

app = FastAPI(
    title="AI Math Tutor",
    version="1.0.0",
    description="Simple AI Math Tutor API"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 한글 인코딩을 위한 미들웨어
@app.middleware("http")
async def add_charset_middleware(request, call_next):
    response = await call_next(request)
    if hasattr(response, 'headers'):
        response.headers['content-type'] = 'application/json; charset=utf-8'
    return response

# HTML 파일 서빙
@app.get("/")
async def root():
    return FileResponse("chat_test.html")

@app.get("/chat_test.html")
async def get_chat_page():
    return FileResponse("chat_test.html")

@app.get("/test_chatbot_frontend.html")
async def get_test_page():
    return FileResponse("test_chatbot_frontend.html")

# 기본 헬스체크
@app.get("/health")
def health():
    return {"status": "ok", "message": "Server is healthy"}

# MongoDB 상태 확인
@app.get("/api/db/health")
async def db_health():
    try:
        # MongoDB가 필요할 때만 초기화
        if not mongodb_available:
            init_mongodb()
        
        mongodb_status = "connected" if mongodb_available else "disconnected"
        
        return JSONResponse(
            content={
                "status": "ok" if mongodb_available else "error",
                "mongodb": mongodb_status,
                "timestamp": datetime.datetime.now().isoformat()
            },
            media_type="application/json; charset=utf-8"
        )
    except Exception as e:
        return JSONResponse(
            content={
                "status": "error",
                "mongodb": "error",
                "error": str(e),
                "timestamp": datetime.datetime.now().isoformat()
            },
            media_type="application/json; charset=utf-8"
        )

# 서비스 토큰 검증
@app.post("/api/auth/verify-token")
async def verify_token(request: dict):
    from .core.config import settings
    
    service_token = request.get("service_token")
    
    # 디버깅 정보 추가
    debug_info = {
        "received_token": service_token,
        "expected_token": settings.SERVICE_TOKEN,
        "env_file_path": str(Path(__file__).parent.parent / ".env")
    }
    
    if service_token == settings.SERVICE_TOKEN:
        return JSONResponse(
            content={
                "valid": True,
                "message": "토큰 검증 성공",
                "debug": debug_info
            },
            media_type="application/json; charset=utf-8"
        )
    else:
        return JSONResponse(
            content={
                "valid": False,
                "message": "토큰 검증 실패",
                "debug": debug_info
            },
            media_type="application/json; charset=utf-8"
        )

# 문제 ID로 문제 조회 (MongoDB에서)
@app.get("/api/problems/{problem_id}")
async def get_problem_by_id(problem_id: str):
    try:
        # MongoDB가 필요할 때만 초기화
        if not mongodb_available:
            init_mongodb()
        
        if not mongodb_available:
            return {"error": "MongoDB 연결이 불가능합니다"}
        
        # MongoDB에서 문제 조회
        from .db.mongo import problems
        if problems is None:
            return {"error": "MongoDB 컬렉션에 접근할 수 없습니다"}
        
        # problem_id로 문제 검색
        problem = problems.find_one({"problem_id": problem_id})
        if not problem:
            # 다른 필드로도 검색 시도
            problem = problems.find_one({"_id": problem_id})
            if not problem:
                return {"error": f"문제 ID {problem_id}를 찾을 수 없습니다"}
        
        return {"problem": convert_objectid(problem)}
        
    except Exception as e:
        return {"error": f"문제 조회 중 오류: {str(e)}"}

# 기존 AI API 라우터 포함
app.include_router(ai_router)

# 학습 경로 API 라우터 포함
from .api.v1_learning_path import router as learning_path_router
app.include_router(learning_path_router)

# 간단한 채팅 엔드포인트
@app.post("/api/chat")
async def chat(message: dict):
    try:
        user_message = message.get("message", "")
        if not user_message:
            return {"error": "메시지가 필요합니다."}
        
        # 간단한 AI 응답 시뮬레이션
        if "수학" in user_message or "문제" in user_message:
            response = "수학 문제를 풀어드릴 수 있습니다! /api/solve 엔드포인트를 사용해보세요."
        else:
            response = "안녕하세요! 저는 수학 학습을 도와주는 AI 튜터입니다."
        
        return {"reply": response}
    except Exception as e:
        return {"error": f"채팅 중 오류가 발생했습니다: {str(e)}"}

# ObjectId를 문자열로 변환하는 함수
def convert_objectid(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    elif isinstance(obj, dict):
        return {key: convert_objectid(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_objectid(item) for item in obj]
    return obj

# 문제 ID로 문제 조회 API
@app.get("/api/problem/{problem_id}")
async def get_problem(problem_id: str):
    try:
        # MongoDB가 필요할 때만 초기화
        if not mongodb_available:
            init_mongodb()
        
        if not mongodb_available:
            return {"error": "MongoDB 연결이 불가능합니다"}
        
        # MongoDB에서 문제 조회
        from .db.mongo import problems
        if problems is None:
            return {"error": "MongoDB 컬렉션에 접근할 수 없습니다"}
        
        # problem_id로 문제 검색
        problem = problems.find_one({"problem_id": problem_id})
        if not problem:
            # 다른 필드로도 검색 시도
            problem = problems.find_one({"_id": problem_id})
            if not problem:
                return {"error": f"문제 ID {problem_id}를 찾을 수 없습니다"}
        
        return {"problem": convert_objectid(problem)}
        
    except Exception as e:
        return {"error": f"문제 조회 중 오류: {str(e)}"}

# 통합 문제 풀이 API (프론트에서 한 번에 요청)
@app.post("/api/solve_with_problem")
async def solve_with_problem(request: dict):
    try:
        problem_id = request.get("problem_id")
        question = request.get("question", "")
        session_id = request.get("session_id", "default_session")
        
        if not problem_id:
            return {"error": "problem_id가 필요합니다."}
        
        # MongoDB가 필요할 때만 초기화
        if not mongodb_available:
            init_mongodb()
        
        # 1단계: MongoDB에서 문제 데이터 조회
        problem = problems.find_one({"problem_id": problem_id})
        if not problem:
            return {"error": f"문제 ID {problem_id}를 찾을 수 없습니다."}
        
        # 2단계: 문제 데이터와 질문을 AI에게 전송
        problem_text = f"문제: {problem['content']['question']}\n\n사용자 질문: {question}"
        
        # 3단계: AI 풀이 요청 (직접 OpenAI API 호출)
        import os
        from openai import OpenAI
        
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # 프롬프트 로드
        from .ai.prompts import load_prompt
        prompt_text = load_prompt("solve_prompt_v1")
        
        # OpenAI API 호출
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": prompt_text},
                {"role": "user", "content": problem_text}
            ],
            response_format={"type": "json_object"}
        )
        
        # 4단계: AI 응답 파싱 및 반환
        ai_response = response.choices[0].message.content
        try:
            # JSON 파싱
            import json
            ai_data = json.loads(ai_response)
            return {
                "problem": convert_objectid(problem),
                "ai_solution": ai_data,
                "status": "success"
            }
        except Exception as e:
            return {
                "problem": convert_objectid(problem),
                "ai_solution": {"raw_response": ai_response},
                "status": "partial_success",
                "error": f"AI 응답 파싱 오류: {str(e)}"
            }
            
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        return {"error": f"문제 풀이 중 오류: {str(e)}", "traceback": error_details}

# 통합 개념 설명 API
@app.post("/api/concept_with_problem")
async def concept_with_problem(request: dict):
    try:
        problem_id = request.get("problem_id")
        concept_name = request.get("concept_name", "")
        session_id = request.get("session_id", "default_session")
        
        if not problem_id:
            return {"error": "problem_id가 필요합니다."}
        
        # MongoDB가 필요할 때만 초기화
        if not mongodb_available:
            init_mongodb()
        
        # MongoDB에서 문제 데이터 조회
        problem = problems.find_one({"problem_id": problem_id})
        if not problem:
            return {"error": f"문제 ID {problem_id}를 찾을 수 없습니다."}
        
        # 문제 데이터와 개념을 AI에게 전송
        problem_text = f"문제: {problem['content']['question']}\n\n개념 설명 요청: {concept_name}"
        
        import os
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # 개념 설명 프롬프트 로드
        from .ai.prompts import load_prompt
        prompt_text = load_prompt("concept_prompt_v1")
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": prompt_text},
                {"role": "user", "content": problem_text}
            ],
            response_format={"type": "json_object"}
        )
        
        ai_response = response.choices[0].message.content
        try:
            import json
            ai_data = json.loads(ai_response)
            return {
                "problem": convert_objectid(problem),
                "ai_concept": ai_data,
                "status": "success"
            }
        except Exception as e:
            return {
                "problem": convert_objectid(problem),
                "ai_concept": {"raw_response": ai_response},
                "status": "partial_success",
                "error": f"AI 응답 파싱 오류: {str(e)}"
            }
            
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        return {"error": f"개념 설명 중 오류: {str(e)}", "traceback": error_details}

# 통합 RAG 추천 API
@app.post("/api/rag_with_problem")
async def rag_with_problem(request: dict):
    try:
        problem_id = request.get("problem_id")
        question = request.get("question", "")
        session_id = request.get("session_id", "default_session")
        
        if not problem_id:
            return {"error": "problem_id가 필요합니다."}
        
        # MongoDB가 필요할 때만 초기화
        if not mongodb_available:
            init_mongodb()
        
        # MongoDB에서 문제 데이터 조회
        problem = problems.find_one({"problem_id": problem_id})
        if not problem:
            return {"error": f"문제 ID {problem_id}를 찾을 수 없습니다."}
        
        # 문제 데이터와 질문을 AI에게 전송
        problem_text = f"문제: {problem['content']['question']}\n\n추천 요청: {question}"
        
        import os
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # RAG 추천 프롬프트 로드
        from .ai.prompts import load_prompt
        prompt_text = load_prompt("rag_prompt_v1")
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": prompt_text},
                {"role": "user", "content": problem_text}
            ],
            response_format={"type": "json_object"}
        )
        
        ai_response = response.choices[0].message.content
        try:
            import json
            ai_data = json.loads(ai_response)
            return {
                "problem": convert_objectid(problem),
                "ai_recommendation": ai_data,
                "status": "success"
            }
        except Exception as e:
            return {
                "problem": convert_objectid(problem),
                "ai_recommendation": {"raw_response": ai_response},
                "status": "partial_success",
                "error": f"AI 응답 파싱 오류: {str(e)}"
            }
            
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        return {"error": f"RAG 추천 중 오류: {str(e)}", "traceback": error_details}

# 기존 AI API가 /api/ai/* 경로로 제공됩니다
# - /api/ai/solve: 수학 문제 풀이
# - /api/ai/concept: 개념 설명  
# - /api/ai/rag_recommend: RAG 추천

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)