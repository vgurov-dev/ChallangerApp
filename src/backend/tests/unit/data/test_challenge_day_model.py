import datetime

from pydantic import ValidationError
import pytest
from backend.app.models.challenge import ChallengeDay


def test_challenge_day_no_empty():
    with pytest.raises(ValidationError):
        ChallengeDay(state="active")


def test_challenge_day_minimal():
    day = ChallengeDay(day_no=1)
    assert day.day_no == 1


def test_challenge_day_full():
    day = ChallengeDay(
        day_no=1,
        state="active",
        date=datetime.date.today(),
        description="Day description"
    )
    assert day.day_no == 1
    assert day.state == "active"
    assert day.date == datetime.date.today()
    assert day.description == "Day description"


def test_challenge_day_negative_day_no():
    with pytest.raises(ValidationError):
        ChallengeDay(day_no=-1)

def test_challenge_day_zero_day_no():
    with pytest.raises(ValidationError):
        day = ChallengeDay(day_no=0)
