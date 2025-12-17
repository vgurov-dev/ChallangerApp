from sqlalchemy import String, Text, Date, UUID
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.dialects.postgresql import JSONB
from backend.app.db.base import Base
from typing import Any, Optional, List, Dict
import uuid
from enum import Enum
from backend.app.schemas.challenge import ChallengeDay
from backend.app.exceptions.challenge import (
    ChallengeInvalidStatus,
    ChallengeStatusAlreadyException,
    ChallengeEditNotAllowed
)
from kit.model.types import IntEnumType


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
    status: Mapped[ChallengeStatus] = mapped_column(IntEnumType(ChallengeStatus), nullable=False, default=ChallengeStatus.DRAFT)
    visibility: Mapped[ChallengeVisibility] = mapped_column(IntEnumType(ChallengeVisibility), nullable=False, default=ChallengeVisibility.PRIVATE)
    level: Mapped[ChallengeLevel] = mapped_column(IntEnumType(ChallengeLevel), nullable=False, default=ChallengeLevel.LIGHT)
    public_id: Mapped[uuid.UUID] = mapped_column(UUID, index=True)

    # Основной индикатор и дополнительные индикаторы
    scoring_indicator: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    additional_indicators: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)

    # Дни челленджа
    challenge_days: Mapped[Optional[List[Dict[str, Any]]]] = mapped_column(JSONB, nullable=True)

    def draft(self):
        self.status = ChallengeStatus.DRAFT

    def edit_draft(self, body: Any):
        if self.status != ChallengeStatus.DRAFT:
            raise ChallengeEditNotAllowed("Challenge edit is not allowed")

    def publish(self):
        match self.status:
            case ChallengeStatus.DRAFT:
                self.status = ChallengeStatus.PUBLISHED
            case ChallengeStatus.PUBLISHED:
                raise ChallengeStatusAlreadyException()
        raise ChallengeInvalidStatus("Challenge status is invalid")

    def start(self):
        if ChallengeStatus(self.status) != ChallengeStatus.PUBLISHED:
            raise ChallengeInvalidStatus()
        self.status = ChallengeStatus.STARTED

    def commit_day(self, day: ChallengeDay):
        if not self.status == ChallengeStatus.STARTED:
            raise ChallengeInvalidStatus("Challenge started is invalid")

    def cancel(self):
        if self.status == ChallengeStatus.CANCELLED:
            raise ChallengeStatusAlreadyException()
        if self.status in [ChallengeStatus.STARTED,
                           ChallengeStatus.PUBLISHED,
                           ChallengeStatus.COMPLETED]:
            self.status = ChallengeStatus.CANCELLED
        raise ChallengeInvalidStatus("Challenge cancelled is invalid")

    def complete(self):
        if self.status in [ChallengeStatus.COMPLETED,
                           ChallengeStatus.CANCELLED]:
            raise ChallengeStatusAlreadyException()
        if self.status == ChallengeStatus.DRAFT:
            self.status = ChallengeStatus.COMPLETED
        raise ChallengeInvalidStatus("Challenge completed is invalid")
