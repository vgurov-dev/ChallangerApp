import uuid
from pydantic import BaseModel, Field, field_validator, ConfigDict
import datetime
from typing import List, Optional


class ChallengeRangeModel(BaseModel):
    min: int = Field(..., description="Минимальное значение диапазона (включительно)")
    max: int = Field(..., description="Максимальное значение диапазона (исключительно)")

    @field_validator("max")
    def validate_max_greater_than_min(cls, v, obj):
        min_value = obj.data.get('min')
        if min_value is not None and v <= min_value:
            raise ValueError("max должно быть больше min")
        return v

class ChallengeScoringIndicator(BaseModel):
    name: str = Field(..., description="Название индикатора оценки")
    description: Optional[str] = Field(None, description="Описание индикатора")
    min_value: Optional[float] = Field(None, description="Минимально допустимое значение")
    range: Optional[ChallengeRangeModel] = Field(None, description="Диапазон значений [min, max)")


class ChallengeDay(BaseModel):
    day_no: int = Field(..., description="Номер дня")
    state: Optional[str] = Field(None, description="Состояние дня (например, активен, завершён)")
    date: Optional[datetime.date] = Field(None, description="Дата дня")
    description: Optional[str] = Field(None, description="Описание дня")


class Challenge(BaseModel):
    name: str = Field(..., description="Название челленджа")
    start_date: datetime.date = Field(..., description="Дата начала челленджа")
    end_date: datetime.date = Field(..., description="Дата окончания челленджа")
    description: Optional[str] = Field(None, description="Описание челленджа")
    scoring_indicator: Optional[ChallengeScoringIndicator] = Field(None, description="Основной индикатор оценки челленджа")
    additional_indicators: List[ChallengeScoringIndicator] = Field(default_factory=list, description="Дополнительные индикаторы оценки")
    challenge_days: List[ChallengeDay] = Field(default_factory=list, description="Список дней челленджа")

    @field_validator("end_date")
    def validate_end_date_after_start_date(cls, v, values):
        start = values.get("start_date")
        if start:
            if v <= start:
                raise ValueError("end_date должен быть позже start_date")
            if v - start > datetime.timedelta(days=365):
                raise ValueError("Разница между start_date и end_date не может быть больше 365 дней")
        return v


class ChallengeInput(BaseModel):
    name: str = Field(
        ...,
        description="Название челленджа",
        examples=['Еще один крутой челлендж'])
    start_date: datetime.date = Field(
        ...,
        description="Дата начала челленджа")
    user_id: str = Field(
        ...,
        description="Ид пользователя",
        examples=["123324"])
    end_date: datetime.date = Field(
        ...,
        description="Дата окончания челленджа")
    description: Optional[str] = Field(
        None,
        description="Описание челленджа",
        examples=['Long Challenge description'])
    scoring_indicator: ChallengeScoringIndicator = Field(
        ...,
        description="Основной индикатор оценки челленджа")

class ChallengeOutRow(BaseModel):
    name: str = Field(..., description="Название челленджа", examples=['Еще один крутой челлендж'])
    start_date: datetime.date = Field(..., description="Дата начала челленджа")
    user_id: str = Field(..., description="Ид пользователя", examples=["123324"])
    end_date: datetime.date = Field(..., description="Дата окончания челленджа")
    description: Optional[str] = Field(..., description="Описание челленджа", examples=['Long Challenge description'])
    scoring_indicator: Optional[ChallengeScoringIndicator] = Field(...,
                                                                   description="Основной индикатор оценки челленджа")
    model_config = ConfigDict(from_attributes=True)


class ChallengeOut(BaseModel):
    challenges: List[ChallengeOutRow]

class ChallengeDraftIn(BaseModel):  # заглушка
    title: str
    description: Optional[str]

class DraftListOut(BaseModel):  # заглушка
    drafts: List[ChallengeOut]

class PublishedListOut(BaseModel):  # заглушка
    published: List[ChallengeOut]

class DayCommitOut(BaseModel):  # заглушка
    day_id: int
    success: bool