from sqlalchemy import String, Text, Date, UUID, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy.dialects.postgresql import JSONB
from backend.app.db.base import Base
from typing import Any, Optional, List, Dict
import uuid
from enum import Enum
from backend.app.exceptions.challenge import (
    ChallengeInvalidStatus,
    ChallengeStatusAlreadyException,
    ChallengeEditNotAllowed
)
from kit.model.types import IntEnumType
from pydantic import BaseModel, Field, field_validator
import datetime


class ChallengeRangeModel(BaseModel):
    """
    Challenge Range model value object
    ChallengeScoringIndicator -> ChallengeRangeModel
    """
    min: int = Field(
        ...,
        description="Минимальное значение диапазона (включительно)"
    )
    max: int = Field(
        ...,
        description="Максимальное значение диапазона (исключительно)"
    )

    @field_validator("max")
    def validate_max_greater_than_min(cls, v, obj):
        min_value = obj.data.get('min')
        if min_value is not None and v <= min_value:
            raise ValueError("max должно быть больше min")
        return v

class ChallengeScoringIndicator(BaseModel):
    """
    Challenge Scoring Indicator value object
    """
    name: str = Field(
        ...,
        description="Название индикатора оценки"
    )
    description: Optional[str] = Field(
        None,
        description="Описание индикатора"
    )
    min_value: Optional[float] = Field(
        None,
        description="Минимально допустимое значение"
    )
    range: Optional[ChallengeRangeModel] = Field(
        ...,
        description="Диапазон значений [min, max)"
    )


class ChallengeDay(BaseModel):
    """
    Challenge day value object
    Challenge.challenge_days -> List[ChallengeDay]
    """
    day_no: int = Field(
        ...,
        description="Номер дня",
        ge=1
    )
    state: Optional[str] = Field(
        None,
        description="Состояние дня (например, активен, завершён)"
    )
    date: Optional[datetime.date] = Field(
        None,
        description="Дата дня"
    )
    description: Optional[str] = Field(
        None,
        description="Описание дня"
    )


class ChallengeStatus(Enum):
    """
    Challenge status Enum
    Challenge.status -> ChallengeStatus
    """
    DRAFT = 1
    PUBLISHED = 2
    STARTED = 3
    COMPLETED = -1
    CANCELLED = -2


class ChallengeVisibility(Enum):
    """
    Challenge visibility Enum
    Challenge.visibility -> ChallengeStatus
    """
    PRIVATE = 1
    PUBLIC = 2


class ChallengeLevel(Enum):
    """
    Challenge level Enum
    ChallengeLevel.level -> ChallengeLevel
    """
    LIGHT = 1
    MEDIUM = 2
    HARD = 3
    EXTREME = 4


class ChallengeRefLink(Base):
    """
    Challenge Public model
    Challenge.public_links -> List[ChallengeRefLink]
    """
    __tablename__ = "challenge_referral_links"

    challenge_id: Mapped[int] = mapped_column(
        ForeignKey("challenge.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    public_id: Mapped[uuid.UUID] = mapped_column(UUID, nullable=False, default=uuid.uuid4, unique=True)

    challenge: Mapped["Challenge"] = relationship(
        back_populates="public_links"
    )


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
    status: Mapped[ChallengeStatus] = mapped_column(
        IntEnumType(ChallengeStatus),
        nullable=False,
        default=ChallengeStatus.DRAFT
    )
    visibility: Mapped[ChallengeVisibility] = mapped_column(
        IntEnumType(ChallengeVisibility),
        nullable=False,
        default=ChallengeVisibility.PRIVATE
    )
    level: Mapped[ChallengeLevel] = mapped_column(
        IntEnumType(ChallengeLevel),
        nullable=False,
        default=ChallengeLevel.LIGHT
    )

    # Основной индикатор и дополнительные индикаторы
    scoring_indicator: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    additional_indicators: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)

    # Дни челленджа
    challenge_days: Mapped[Optional[List[Dict[str, Any]]]] = mapped_column(JSONB, nullable=True)

    public_links: Mapped[List[ChallengeRefLink]] = relationship(
        back_populates="challenge",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

    def create_draft(
            self,
            name: str = "Undefinded challenge",
            description: str = None
    ):
        self.name = name
        self.description = description
        self.status = ChallengeStatus.DRAFT
        self.visibility = ChallengeVisibility.PRIVATE
        self.level = ChallengeLevel.LIGHT

    def edit_draft(self, body: Any):
        if self.status != ChallengeStatus.DRAFT:
            raise ChallengeEditNotAllowed("Challenge edit is not allowed")

    def publish(self):
        match self.status:
            case ChallengeStatus.DRAFT:
                link =  self.__create_public_link()
                self.public_links.append(link)
                self.status = ChallengeStatus.PUBLISHED
                return None
            case ChallengeStatus.PUBLISHED:
                raise ChallengeStatusAlreadyException("Challenge is already published")
        raise ChallengeInvalidStatus("Challenge status is invalid")

    def __create_public_link(self) -> ChallengeRefLink:
        return ChallengeRefLink(id=self.id)

    def start(self):
        if self.status != ChallengeStatus.PUBLISHED:
            raise ChallengeInvalidStatus()
        self.status = ChallengeStatus.STARTED

    def __create_challenge_days(self) -> Mapped[list]:
        self.challenge_days = []
        return self.challenge_days

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
