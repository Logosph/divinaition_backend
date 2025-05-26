from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=False)
    name = Column(String, nullable=True)
    email = Column(String, unique=True, nullable=False, index=True)
    date_of_registration = Column(DateTime, default=datetime.utcnow)
    password_hash = Column(String, nullable=False)
    prefs = Column(JSON, nullable=True)
    card_of_the_day = Column(Integer, nullable=True)
    last_card_update = Column(DateTime, nullable=True) 