from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.crud.user import create_user, get_user_by_email, verify_password
from app.schemas.auth import SignupRequest, SigninRequest, AccessTokenResponse
from app.utils.auth import create_access_token
from app.utils.user_service import create_user_in_user_service
from app.db.db_vitals import get_async_session

router = APIRouter(tags=["Авторизация"])

@router.post("/signup", response_model=AccessTokenResponse)
async def signup(user_data: SignupRequest, db: AsyncSession = Depends(get_async_session)):
    # Проверяем, существует ли пользователь
    existing_user = await get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Создаем нового пользователя в auth_service
    user = await create_user(db, user_data.email, user_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not create user"
        )
    
    try:
        # Создаем пользователя в user_service
        await create_user_in_user_service(user.email, user.hashed_password)
    except Exception as e:
        # Если не удалось создать пользователя в user_service, удаляем его из auth_service
        await db.delete(user)
        await db.commit()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Could not create user in user service"
        )
    
    # Создаем токен доступа
    access_token = create_access_token(data={"sub": str(user.id)})
    return AccessTokenResponse(access_token=access_token)

@router.post("/signin", response_model=AccessTokenResponse)
async def signin(user_data: SigninRequest, db: AsyncSession = Depends(get_async_session)):
    # Проверяем существование пользователя
    user = await get_user_by_email(db, user_data.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Проверяем пароль
    if not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Создаем токен доступа
    access_token = create_access_token(data={"sub": str(user.id)})
    return AccessTokenResponse(access_token=access_token) 