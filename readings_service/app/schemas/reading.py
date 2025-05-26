from pydantic import BaseModel
from typing import List
from app.schemas.card import CardResponse

class QuestionReadingRequest(BaseModel):
    question: str

class ReadingResponse(BaseModel):
    reading_id: int
    cards: List[CardResponse]

    class Config:
        from_attributes = True

class GetInterpretationRequest(BaseModel):
    reading_id: int

class InterpretationResponse(BaseModel):
    interpretation: str

class AddNoteRequest(BaseModel):
    reading_id: int
    note: str 