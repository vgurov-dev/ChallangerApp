from pydantic import BaseModel, Field, field_validator
from typing import Optional
import datetime

class ChallengeRangeModel(BaseModel):
    min: float = Field(..., description="Минимальное значение диапазона (включительно)")
    max: float = Field(..., description="Максимальное значение диапазона (исключительно)")

    @field_validator("max")
    def validate_max_greater_than_min(cls, v, values):
        if "min" in values and v <= values["min"]:
            raise ValueError("max должно быть больше min")
        return v

class ChallengeScoringIndicator(BaseModel):
    name: str = Field(..., description="Название индикатора оценки")
    description: Optional[str] = Field(None, description="Описание индикатора")
    min_value: Optional[float] = Field(None, description="Минимально допустимое значение")
    range: Optional[ChallengeRangeModel] = Field(None, description="Диапазон значений [min, max)")


class ChallengeInput(BaseModel):
    name: str = Field(..., description="Название челленджа")
    start_date: datetime.date = Field(..., description="Дата начала челленджа")
    end_date: datetime.date = Field(..., description="Дата окончания челленджа")
    description: Optional[str] = Field(..., description="Описание челленджа")
    scoring_indicator: Optional[ChallengeScoringIndicator] = Field(...,
                                                                   description="Основной индикатор оценки челленджа")