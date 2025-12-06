from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy import UUID, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import uuid
from datetime import datetime


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)

    created_at: Mapped[datetime] = mapped_column(DateTime)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now() ,onupdate=func.now())