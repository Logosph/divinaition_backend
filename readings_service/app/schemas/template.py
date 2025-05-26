from pydantic import BaseModel
from typing import List

class TemplateShort(BaseModel):
    template_id: int
    template_name: str

    class Config:
        from_attributes = True

class TemplateCategory(BaseModel):
    category_name: str
    templates: List[TemplateShort]

class CardQuestionResponse(BaseModel):
    id: int
    num: int
    question: str

    class Config:
        from_attributes = True

class TemplateDetailResponse(BaseModel):
    id: int
    name: str
    category: str
    card_questions: List[CardQuestionResponse]

    class Config:
        from_attributes = True 