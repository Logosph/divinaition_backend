from typing import Optional
import httpx
from app.config.settings import settings
from app.config.logger import logger

async def ask_llm(prompt: str) -> Optional[str]:
    """Асинхронная функция для отправки запроса к LLM"""
    headers = {
        "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": settings.LLM_MODEL,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ]
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                settings.LLM_API_URL,
                headers=headers,
                json=data,
                timeout=30.0  # Увеличенный таймаут для LLM запросов
            )
            
            if response.status_code != 200:
                logger.error(f"LLM API error: {response.status_code} - {response.text}")
                return None

            resp_json = response.json()
            return resp_json['choices'][0]['message']['content']
            
    except Exception as e:
        logger.error(f"Error while calling LLM API: {str(e)}")
        return None 