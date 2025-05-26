from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from ..db.crud.user import get_user_by_id, update_user_name, create_user, update_card_of_the_day
from ..schemas.user import UpdateNameRequest, UserInfoResponse, CreateUserRequest
from ..utils.auth import get_current_user_id
from ..db.db_vitals import get_async_session

router = APIRouter(tags=["Пользователь"])

@router.put("/update_name", response_model=None)
async def update_name(
    request: UpdateNameRequest,
    current_user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_async_session)
):
    user = await update_user_name(db, current_user_id, request.name)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return {"status": "success"}

@router.get("/me", response_model=UserInfoResponse)
async def get_me(
    current_user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_async_session)
):
    user = await get_user_by_id(db, current_user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Обновляем карту дня если необходимо
    user = await update_card_of_the_day(db, user)
    
    return UserInfoResponse(
        uuid=str(user.id),
        name=user.name,
        email=user.email,
        date_of_registration=user.date_of_registration,
        prefs=user.prefs,
        card_of_the_day=user.card_of_the_day
    )

@router.post("/internal/create", response_model=UserInfoResponse)
async def create_new_user(
    user_data: CreateUserRequest,
    db: AsyncSession = Depends(get_async_session)
):
    """Внутренний эндпоинт для создания пользователя из auth_service"""
    user = await create_user(db, user_data)
    return UserInfoResponse(
        uuid=str(user.id),
        email=user.email,
        date_of_registration=user.date_of_registration,
        prefs=user.prefs,
        card_of_the_day=user.card_of_the_day
    ) 