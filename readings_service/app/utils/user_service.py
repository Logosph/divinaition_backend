import httpx
from app.config.settings import settings
from app.config.logging import logger

async def get_user_info(token: str) -> dict | None:
    """Получение информации о пользователе из user_service"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{settings.USER_SERVICE_URL}/me",
                headers={"Authorization": f"Bearer {token}"}
            )
            
            if response.status_code != 200:
                logger.error(f"User service error: {response.status_code} - {response.text}")
                return None

            return response.json()
            
    except Exception as e:
        logger.error(f"Error while calling user service: {str(e)}")
        return None 