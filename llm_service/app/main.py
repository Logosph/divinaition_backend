from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import llm
from app.config.settings import settings

app = FastAPI(title="LLM Service", root_path="/api/v1/llm")

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_CREDENTIALS,
    allow_methods=settings.CORS_METHODS,
    allow_headers=settings.CORS_HEADERS,
)

# Подключаем роутеры
app.include_router(llm.router)

@app.get("/")
async def root():
    return {"message": "LLM Service is running"} 