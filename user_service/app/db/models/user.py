from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.orm import declarative_base

Base = declarative_base()

def get_utc_now():
    return datetime.now(timezone.utc)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    email = Column(String, unique=True, nullable=False, index=True)
    date_of_registration = Column(DateTime(timezone=True), default=get_utc_now)
    password_hash = Column(String, nullable=False)
    prefs = Column(JSON, nullable=True)
    card_of_the_day = Column(Integer, nullable=True)
    last_card_update = Column(DateTime(timezone=True), nullable=True) 