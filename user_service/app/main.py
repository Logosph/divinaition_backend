from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import user
from app.config.settings import settings

app = FastAPI(title="User Service", root_path="/api/v1/user")

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_CREDENTIALS,
    allow_methods=settings.CORS_METHODS,
    allow_headers=settings.CORS_HEADERS,
)

# Подключаем роутеры
app.include_router(user.router)

@app.get("/")
async def root():
    return {"message": "User Service is running"}
