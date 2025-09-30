from .session import engine
from .base import Base  # импорт всех моделей через base

from app.models.challenge import Challenge

def init_db():
    Base.metadata.create_all(bind=engine)