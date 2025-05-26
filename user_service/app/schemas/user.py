from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, EmailStr

class UpdateNameRequest(BaseModel):
    name: str

class UserInfoResponse(BaseModel):
    uuid: str
    name: Optional[str] = None
    email: EmailStr
    date_of_registration: datetime
    prefs: Optional[Dict[str, Any]] = None
    card_of_the_day: Optional[int] = None

    class Config:
        from_attributes = True

class CreateUserRequest(BaseModel):
    """Внутренний запрос от auth_service для создания пользователя"""
    id: int
    email: EmailStr
    password_hash: str 