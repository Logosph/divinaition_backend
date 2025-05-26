from fastapi import APIRouter, HTTPException, status
from app.schemas.llm import LLMRequest, LLMResponse
from app.utils.llm import ask_llm

router = APIRouter(tags=["LLM"])

@router.post("/ask", response_model=LLMResponse)
async def ask_question(request: LLMRequest):
    """Эндпоинт для отправки запроса к LLM"""
    response = await ask_llm(request.prompt)
    
    if response is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Failed to get response from LLM service"
        )
    
    return LLMResponse(response=response) 