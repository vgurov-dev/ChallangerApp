from sqlalchemy import String, Text, Date
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.dialects.postgresql import JSONB
from backend.app.db.base import Base
from typing import Any, Optional, List, Dict


class Challenge(Base):
    __tablename__ = "challenges"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    start_date: Mapped[Date] = mapped_column(Date, nullable=False)
    end_date: Mapped[Date] = mapped_column(Date, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    user_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)

    # Основной индикатор и дополнительные индикаторы
    scoring_indicator: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    additional_indicators: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)

    # Дни челленджа
    challenge_days: Mapped[Optional[List[Dict[str, Any]]]] = mapped_column(JSONB, nullable=True)