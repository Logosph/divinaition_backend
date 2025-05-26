from datetime import datetime
from sqlalchemy import select
from app.db.models.reading import Card
from app.db.db_vitals import get_async_session
from app.utils.llm import get_llm_interpretation

async def update_card_descriptions():
    """Обновление описаний карт в 00:00 по GMT"""
    async for db in get_async_session():
        try:
            # Получаем все карты
            result = await db.execute(select(Card))
            cards = result.scalars().all()
            
            # Текущая дата
            now = datetime.utcnow()
            weekday = now.strftime("%A")
            date = now.strftime("%Y-%m-%d")
            
            # Обновляем описание для каждой карты
            for card in cards:
                prompt = (
                    f"Ты - профессиональный таролог. Сегодня - {date}, {weekday}, "
                    f"моя карта дня - {card.name}. Опиши сегодняшний день, опираясь на мою карту дня"
                )
                
                description = await get_llm_interpretation(prompt)
                if description:
                    card.date_description = description
            
            await db.commit()
            
        except Exception as e:
            print(f"Error updating card descriptions: {str(e)}")
            continue 