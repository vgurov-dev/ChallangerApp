import uuid
from sqlalchemy import Column, String, Text, Date
from sqlalchemy.dialects.postgresql import UUID, JSONB
from backend.app.db.base import Base


class Challenge(Base):
    __tablename__ = "challenges"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    description = Column(Text, nullable=True)

    # Основной индикатор и дополнительные индикаторы
    scoring_indicator = Column(JSONB, nullable=True)
    additional_indicators = Column(JSONB, nullable=True)

    # Дни челленджа
    challenge_days = Column(JSONB, nullable=True)
