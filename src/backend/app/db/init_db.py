from .session import engine
from .base import Base  # импорт всех моделей через base
from backend.app.models.challenge import Challenge

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)