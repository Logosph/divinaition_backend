from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Security
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.db_vitals import get_async_session
from app.db.crud.card import get_all_cards, get_card_by_id
from app.schemas.card import CardResponse
from app.utils.auth import get_current_user_id
from app.utils.user_service import get_user_info
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.tasks.card_descriptions import update_card_descriptions
from app.utils.background_tasks import BackgroundTaskManager

router = APIRouter(tags=["Cards"])
security = HTTPBearer()

@router.get("/get_cards", response_model=List[CardResponse])
async def get_cards(db: AsyncSession = Depends(get_async_session)):
    """Получение списка всех карт"""
    cards = await get_all_cards(db)
    return [
        CardResponse(
            id=card.id,
            name=card.name,
            meaning=card.meaning,
            image_url=card.image_url,
            interpretation_of_day=card.date_description
        ) for card in cards
    ]

@router.get("/get_card_by_id/{card_id}", response_model=CardResponse)
async def get_card(card_id: int, db: AsyncSession = Depends(get_async_session)):
    """Получение карты по ID"""
    card = await get_card_by_id(db, card_id)
    if not card:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Card not found"
        )
    return CardResponse(
        id=card.id,
        name=card.name,
        meaning=card.meaning,
        image_url=card.image_url,
        interpretation_of_day=card.date_description
    )

@router.get("/get_my_card_of_the_day", response_model=CardResponse)
async def get_my_card_of_the_day(
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: AsyncSession = Depends(get_async_session)
):
    """Получение карты дня пользователя"""
    # Получаем информацию о пользователе из user_service, передавая тот же токен
    user_info = await get_user_info(credentials.credentials)
    if not user_info or user_info.get("card_of_the_day") is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Card of the day not found"
        )
    
    # Получаем карту по ID
    card = await get_card_by_id(db, user_info["card_of_the_day"])
    if not card:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Card not found"
        )
    
    return CardResponse(
        id=card.id,
        name=card.name,
        meaning=card.meaning,
        image_url=card.image_url,
        interpretation_of_day=card.date_description
    )

@router.post("/update_card_descriptions")
async def trigger_card_descriptions_update():
    """Ручной запуск обновления описаний карт"""
    try:
        # Запускаем задачу в фоне
        task_id = await BackgroundTaskManager.start_task(
            "update_card_descriptions",
            update_card_descriptions()
        )
        return {
            "status": "started",
            "task_id": task_id,
            "message": "Card descriptions update started in background"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to start card descriptions update: {str(e)}"
        )

@router.get("/update_card_descriptions/status/{task_id}")
async def get_update_status(task_id: str):
    """Получение статуса обновления описаний карт"""
    status = BackgroundTaskManager.get_task_status(task_id)
    if status["status"] == "not_found":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return status 