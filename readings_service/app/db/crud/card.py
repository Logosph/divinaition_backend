from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.reading import Card

async def get_all_cards(db: AsyncSession):
    result = await db.execute(select(Card))
    return result.scalars().all()

async def get_card_by_id(db: AsyncSession, card_id: int):
    result = await db.execute(select(Card).where(Card.id == card_id))
    return result.scalar_one_or_none() 