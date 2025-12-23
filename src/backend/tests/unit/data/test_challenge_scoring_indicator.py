from backend.app.models.challenge import (
    ChallengeScoringIndicator,
    ChallengeRangeModel
)
import pytest
from pydantic import ValidationError


def test_scoring_indicator_name_empty():
    with pytest.raises(ValidationError):
        ChallengeScoringIndicator(description="Some...")


def test_scoring_indicator_only_name():
    with pytest.raises(ValidationError):
        ChallengeScoringIndicator(name="Score")


def test_scoring_indicator_full():
    indicator = ChallengeScoringIndicator(
        name="Score",
        description="Description",
        min_value=0,
        range=ChallengeRangeModel(min=0, max=100)
    )
    assert indicator.range.max == 100


def test_scoring_indicator_invalid_range():
    with pytest.raises(ValidationError):
        ChallengeScoringIndicator(
            name="Score",
            range=ChallengeRangeModel(min=10, max=5)
        )
