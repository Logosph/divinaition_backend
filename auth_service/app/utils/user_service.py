import httpx
from app.config.settings import settings

async def create_user_in_user_service(email: str, password_hash: str) -> dict:
    """Отправляет запрос на создание пользователя в user_service"""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{settings.USER_SERVICE_URL}/internal/create",
            json={
                "email": email,
                "password_hash": password_hash
            }
        )
        response.raise_for_status()
        return response.json() 