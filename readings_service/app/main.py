from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import card, template, reading
from app.config.settings import settings

app = FastAPI(title="Readings Service", root_path="/api/v1/readings")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_CREDENTIALS,
    allow_methods=settings.CORS_METHODS,
    allow_headers=settings.CORS_HEADERS,
)

app.include_router(card.router)
app.include_router(template.router)
app.include_router(reading.router)

@app.get("/")
async def root():
    return {"message": "Readings Service is running"}
