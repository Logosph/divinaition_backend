from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth
from app.config.settings import settings

app = FastAPI(title="Auth Service", root_path=f"/api/v1/auth")

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_CREDENTIALS,
    allow_methods=settings.CORS_METHODS,
    allow_headers=settings.CORS_HEADERS,
)

# Подключаем роутеры
app.include_router(auth.router)

@app.get("/")
async def root():
    return {"message": "Auth Service is running"}
