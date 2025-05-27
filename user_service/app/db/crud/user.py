from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.user import User, get_utc_now
from ...schemas.user import CreateUserRequest
import random
from datetime import datetime, time, timezone

async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()

async def get_user_by_id(db: AsyncSession, user_id: int):
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()

async def create_user(db: AsyncSession, user_data: CreateUserRequest):
    db_user = User(
        id=user_data.id,
        email=user_data.email,
        password_hash=user_data.password_hash
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def update_user_name(db: AsyncSession, user_id: int, name: str):
    user = await get_user_by_id(db, user_id)
    if user:
        user.name = name
        await db.commit()
        await db.refresh(user)
    return user

async def update_card_of_the_day(db: AsyncSession, user: User) -> User:
    """Обновляет карту дня пользователя если необходимо"""
    now = datetime.now(timezone.utc)
    today_start = datetime.combine(now.date(), time.min, tzinfo=timezone.utc)
    
    # Проверяем, нужно ли обновлять карту
    if not user.last_card_update or user.last_card_update < today_start:
        user.card_of_the_day = random.randint(0, 77)
        user.last_card_update = now
        await db.commit()
        await db.refresh(user)
    
    return user 