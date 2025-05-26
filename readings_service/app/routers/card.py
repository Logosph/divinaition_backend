from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.db_vitals import get_async_session
from app.db.crud.card import get_all_cards, get_card_by_id
from app.schemas.card import CardResponse

router = APIRouter(tags=["Cards"])

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