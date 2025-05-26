from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class CardReading(Base):
    __tablename__ = "card_readings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    template_id = Column(Integer, ForeignKey("reading_templates.id"), nullable=True)
    question = Column(String, nullable=True)
    interpretation = Column(String, nullable=True)
    date = Column(DateTime, default=datetime.utcnow)
    note = Column(String, nullable=True)
    came_true = Column(Boolean, nullable=True)
    prompt = Column(String, nullable=False)

    # Отношения
    template = relationship("ReadingTemplate", back_populates="readings")
    cards = relationship("CardsInCardReading", back_populates="reading")

class CardsInCardReading(Base):
    __tablename__ = "cards_in_card_reading"

    id = Column(Integer, primary_key=True, index=True)
    id_reading = Column(Integer, ForeignKey("card_readings.id"), nullable=False)
    id_card = Column(Integer, ForeignKey("cards.id"), nullable=False)

    # Отношения
    reading = relationship("CardReading", back_populates="cards")
    card = relationship("Card", back_populates="readings")

class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    meaning = Column(String, nullable=False)
    image_url = Column(String, nullable=True)
    date_description = Column(String, nullable=True)

    # Отношения
    readings = relationship("CardsInCardReading", back_populates="card")

class ReadingTemplate(Base):
    __tablename__ = "reading_templates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)

    # Отношения
    readings = relationship("CardReading", back_populates="template")
    questions = relationship("CardQuestion", back_populates="template")

class CardQuestion(Base):
    __tablename__ = "card_questions"

    id = Column(Integer, primary_key=True, index=True)
    template_id = Column(Integer, ForeignKey("reading_templates.id"), nullable=False)
    num = Column(Integer, nullable=False)
    question = Column(String, nullable=False)

    # Отношения
    template = relationship("ReadingTemplate", back_populates="questions") 