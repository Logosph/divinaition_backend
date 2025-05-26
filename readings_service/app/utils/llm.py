import httpx
from app.config.settings import settings
from app.config.logging import logger

async def get_llm_interpretation(prompt: str) -> str | None:
    """Получение интерпретации от LLM сервиса"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{settings.LLM_SERVICE_URL}/ask",
                json={"prompt": prompt},
                timeout=180.0
            )
            
            if response.status_code != 200:
                logger.error(f"LLM service error: {response.status_code} - {response.text}")
                return None

            result = response.json()
            return result["response"]
            
    except Exception as e:
        logger.error(f"Error while calling LLM service: {str(e)}")
        return None 