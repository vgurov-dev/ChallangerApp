from backend.app.core.config import settings
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

engine = create_async_engine(settings.DATABASE_URL)
SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False, autoflush=False, autocommit=False)
