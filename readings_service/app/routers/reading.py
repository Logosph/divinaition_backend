from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.db_vitals import get_async_session
from app.db.crud.reading import (
    get_random_cards, create_reading_with_cards, format_prompt,
    get_reading_by_id, update_reading_interpretation, update_reading_note
)
from app.schemas.reading import (
    QuestionReadingRequest, ReadingResponse, GetInterpretationRequest,
    InterpretationResponse, AddNoteRequest
)
from app.schemas.card import CardResponse
from app.utils.auth import get_current_user_id
from app.utils.llm import get_llm_interpretation

router = APIRouter(tags=["Readings"])

@router.post("/get_reading_by_question", response_model=ReadingResponse)
async def get_reading_by_question(
    request: QuestionReadingRequest,
    current_user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_async_session)
):
    """Создание чтения на основе вопроса"""
    # Получаем случайные карты
    cards = await get_random_cards(db)
    if len(cards) != 3:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not get required number of cards"
        )
    
    # Формируем промпт
    prompt = format_prompt(request.question, cards)
    
    # Создаем чтение
    reading, cards = await create_reading_with_cards(
        db=db,
        user_id=current_user_id,
        question=request.question,
        prompt=prompt,
        cards=cards
    )
    
    # Формируем ответ
    return ReadingResponse(
        reading_id=reading.id,
        cards=[
            CardResponse(
                id=card.id,
                name=card.name,
                meaning=card.meaning,
                image_url=card.image_url,
                interpretation_of_day=card.date_description
            ) for card in cards
        ]
    )

@router.put("/get_interpretation", response_model=InterpretationResponse)
async def get_interpretation(
    request: GetInterpretationRequest,
    db: AsyncSession = Depends(get_async_session)
):
    """Получение интерпретации для чтения"""
    # Получаем чтение
    reading = await get_reading_by_id(db, request.reading_id)
    if not reading:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reading not found"
        )
    
    # Если интерпретация уже есть, возвращаем её
    if reading.interpretation:
        return InterpretationResponse(interpretation=reading.interpretation)
    
    # Если нет, получаем от LLM сервиса
    interpretation = await get_llm_interpretation(reading.prompt)
    if not interpretation:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Could not get interpretation from LLM service"
        )
    
    # Сохраняем интерпретацию
    reading = await update_reading_interpretation(db, reading, interpretation)
    return InterpretationResponse(interpretation=reading.interpretation)

@router.put("/add_note")
async def add_note(
    request: AddNoteRequest,
    db: AsyncSession = Depends(get_async_session)
):
    """Добавление или обновление заметки к чтению"""
    # Получаем чтение
    reading = await get_reading_by_id(db, request.reading_id)
    if not reading:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reading not found"
        )
    
    # Обновляем заметку
    await update_reading_note(db, reading, request.note)
    return {"status": "success"} 