from sqlalchemy import String, Text, Date, UUID, Integer
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.dialects.postgresql import JSONB
from backend.app.db.base import Base
from typing import Any, Optional, List, Dict
import uuid
from enum import Enum
from backend.app.schemas.challenge import ChallengeDay
from backend.app.exceptions.challenge import ChallengeInvalidStatus, ChallengeStatusAlreadyException


class ChallengeStatus(Enum):
    DRAFT = 1
    PUBLISHED = 2
    STARTED = 3
    COMPLETED = -1
    CANCELLED = -2


class ChallengeVisibility(Enum):
    PRIVATE = 1
    PUBLIC = 2


class ChallengeLevel(Enum):
    LIGHT = 1
    MEDIUM = 2
    HARD = 3
    EXTREME = 4


class Challenge(Base):
    """
    Challenge model.
    """
    __tablename__ = "challenge"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    start_date: Mapped[Date] = mapped_column(Date, nullable=False)
    end_date: Mapped[Date] = mapped_column(Date, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    user_id: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    author_id: Mapped[str] = mapped_column(String(20), nullable=False)
    status: Mapped[int] = mapped_column(Integer, nullable=False, default=ChallengeStatus.DRAFT.value)
    visibility: Mapped[int] = mapped_column(Integer, nullable=False, default=ChallengeVisibility.PRIVATE.value)
    level: Mapped[int] = mapped_column(Integer, nullable=False, default=ChallengeLevel.LIGHT.value)
    public_id: Mapped[uuid.UUID] = mapped_column(UUID, index=True)

    # Основной индикатор и дополнительные индикаторы
    scoring_indicator: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    additional_indicators: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)

    # Дни челленджа
    challenge_days: Mapped[Optional[List[Dict[str, Any]]]] = mapped_column(JSONB, nullable=True)

    def draft(self):
        self.status = ChallengeStatus.DRAFT.value

    def publish(self):
        match self.status:
            case ChallengeStatus.DRAFT.value:
                self.status = ChallengeStatus.PUBLISHED.value
            case ChallengeStatus.PUBLISHED.value:
                raise ChallengeStatusAlreadyException()
        raise ChallengeInvalidStatus("Challenge status is invalid")

    def start(self):
        if self.status != ChallengeStatus.PUBLISHED.value:
            raise ChallengeInvalidStatus()
        self.status = ChallengeStatus.STARTED.value

    def commit_day(self, day: ChallengeDay):
        if not self.status == ChallengeStatus.STARTED.value:
            raise ChallengeInvalidStatus("Challenge started is invalid")

    def cancel(self):
        if self.status == ChallengeStatus.CANCELLED.value:
            raise ChallengeStatusAlreadyException()
        if self.status in [ChallengeStatus.STARTED.value,
                           ChallengeStatus.PUBLISHED.value,
                           ChallengeStatus.COMPLETED.value]:
            self.status = ChallengeStatus.CANCELLED.value
        raise ChallengeInvalidStatus("Challenge cancelled is invalid")

    def complete(self):
        if self.status in [ChallengeStatus.COMPLETED.value,
                           ChallengeStatus.CANCELLED.value]:
            raise ChallengeStatusAlreadyException()
        if self.status == ChallengeStatus.DRAFT.value:
            self.status = ChallengeStatus.COMPLETED.value
        raise ChallengeInvalidStatus("Challenge completed is invalid")
