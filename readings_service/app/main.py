from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from app.routers import card, template, reading
from app.config.settings import settings
from app.tasks.card_descriptions import update_card_descriptions

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

# Настройка планировщика
scheduler = AsyncIOScheduler()
scheduler.add_job(
    update_card_descriptions,
    CronTrigger(hour=0, minute=0, timezone="UTC"),
    id="update_card_descriptions",
    replace_existing=True
)

@app.on_event("startup")
async def startup_event():
    scheduler.start()

@app.on_event("shutdown")
async def shutdown_event():
    scheduler.shutdown()

@app.get("/")
async def root():
    return {"message": "Readings Service is running"}
