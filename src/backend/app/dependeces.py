from typing import AsyncGenerator, Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.db.session import SessionLocal


async def get_session() -> AsyncGenerator[AsyncSession, None] :
    async with SessionLocal() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_session)]