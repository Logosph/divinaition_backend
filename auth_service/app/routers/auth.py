from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from ..db.crud.user import create_user, get_user_by_email, verify_password
from ..schemas.auth import SignupRequest, SigninRequest, AccessTokenResponse
from ..utils.auth import create_access_token
from ..db.db_vitals import get_async_session

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
    
    # Создаем нового пользователя
    user = await create_user(db, user_data.email, user_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not create user"
        )
    
    # Создаем токен доступа
    access_token = create_access_token(data={"sub": user.email})
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
    access_token = create_access_token(data={"sub": user.email})
    return AccessTokenResponse(access_token=access_token) 