from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from typing import List, Tuple
from app.db.models.reading import CardReading, Card, CardsInCardReading

async def get_random_cards(db: AsyncSession, count: int = 3) -> List[Card]:
    """Получение случайных карт из колоды"""
    result = await db.execute(
        select(Card).order_by(func.random()).limit(count)
    )
    return result.scalars().all()

async def create_reading_with_cards(
    db: AsyncSession,
    user_id: int,
    question: str,
    prompt: str,
    cards: List[Card]
) -> Tuple[CardReading, List[Card]]:
    """Создание нового чтения с картами"""
    # Создаем запись о чтении
    reading = CardReading(
        user_id=user_id,
        template_id=None,
        question=question,
        interpretation=None,
        note=None,
        came_true=None,
        prompt=prompt
    )
    db.add(reading)
    await db.flush()  # Получаем id чтения

    # Создаем связи с картами
    for card in cards:
        card_in_reading = CardsInCardReading(
            id_reading=reading.id,
            id_card=card.id
        )
        db.add(card_in_reading)
    
    await db.commit()
    await db.refresh(reading)
    
    return reading, cards

async def get_reading_by_id(db: AsyncSession, reading_id: int) -> CardReading | None:
    """Получение чтения по ID"""
    result = await db.execute(
        select(CardReading).where(CardReading.id == reading_id)
    )
    return result.scalar_one_or_none()

async def update_reading_interpretation(
    db: AsyncSession,
    reading: CardReading,
    interpretation: str
) -> CardReading:
    """Обновление интерпретации чтения"""
    reading.interpretation = interpretation
    await db.commit()
    await db.refresh(reading)
    return reading

async def update_reading_note(
    db: AsyncSession,
    reading: CardReading,
    note: str
) -> CardReading:
    """Обновление заметки к чтению"""
    reading.note = note
    await db.commit()
    await db.refresh(reading)
    return reading

def format_prompt(question: str, cards: List[Card]) -> str:
    """Форматирование промпта для LLM"""
    cards_names = [card.name.upper() for card in cards]
    return (
        f"В роли гадалки на картах таро дай ответ на вопрос: {question}. "
        f"Тебе выпали карты: КАРТА 1: {cards_names[0]}, КАРТА 2: {cards_names[1]}, КАРТА 3: {cards_names[2]}. "
        "Не форматируй ответ, не описывай карты по-отдельности, дай только развернутую общую интерпретацию расклада в 5-10 предложений."
    ) 