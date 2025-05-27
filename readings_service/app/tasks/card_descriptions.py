from datetime import datetime, timezone
from sqlalchemy import select
from app.db.models.reading import Card
from app.db.db_vitals import get_async_session
from app.utils.llm import get_llm_interpretation
import asyncio
from app.config.logging import logger

async def update_card_descriptions():
    """Обновление описаний карт в 00:00 по GMT"""
    async for db in get_async_session():
        try:
            # Получаем все карты
            result = await db.execute(select(Card))
            cards = result.scalars().all()
            
            # Текущая дата
            now = datetime.now(timezone.utc)
            weekday = now.strftime("%A")
            date = now.strftime("%Y-%m-%d")
            
            # Обновляем описание для каждой карты
            for i, card in enumerate(cards):
                # Добавляем задержку между запросами, кроме первого
                if i > 0:
                    logger.info(f"Waiting 10 seconds before processing next card ({i+1}/{len(cards)})")
                    await asyncio.sleep(10)
                
                logger.info(f"Processing card {card.name} ({i+1}/{len(cards)})")
                prompt = (
                    f"Ты - профессиональный таролог. Сегодня - {date}, {weekday}, "
                    f"моя карта дня - {card.name}. Опиши сегодняшний день, опираясь на мою карту дня."
                    f"Твой ответ должен содержать от 3 до 5 предложений."
                    f"Твой ответ должен быть без предисловий, послесловий и лишних слов. Просто текст от лица таролога"
                )
                
                description = await get_llm_interpretation(prompt)
                if description:
                    card.date_description = description
                    await db.commit()  # Сохраняем каждую карту отдельно
            
        except Exception as e:
            logger.error(f"Error updating card descriptions: {str(e)}")
            continue 