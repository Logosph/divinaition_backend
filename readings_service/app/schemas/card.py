from pydantic import BaseModel

class CardResponse(BaseModel):
    id: int
    name: str
    meaning: str
    image_url: str | None = None
    interpretation_of_day: str | None = None  # Используем date_description как interpretation_of_day

    class Config:
        from_attributes = True 