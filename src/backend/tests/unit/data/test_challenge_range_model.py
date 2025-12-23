import pytest
from pydantic import ValidationError
from backend.app.models.challenge import ChallengeRangeModel


def test_range_empty():
    with pytest.raises(ValidationError):
        ChallengeRangeModel()


def test_range_valid():
    model = ChallengeRangeModel(min=1, max=5)
    assert model.min == 1
    assert model.max == 5


def test_range_max_equal_min():
    with pytest.raises(ValidationError):
        ChallengeRangeModel(min=5, max=5)


def test_range_max_less_than_min():
    with pytest.raises(ValidationError):
        ChallengeRangeModel(min=10, max=3)


def test_range_negative_values():
    model = ChallengeRangeModel(min=-10, max=-1)
    assert model.min == -10
