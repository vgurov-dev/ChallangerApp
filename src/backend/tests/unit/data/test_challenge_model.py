import pytest
import datetime
from backend.app.models.challenge import (
    Challenge,
    ChallengeStatus,
    ChallengeVisibility,
    ChallengeLevel
)
from backend.app.exceptions.challenge import (
    ChallengeInvalidStatus,
    ChallengeStatusAlreadyException,
    ChallengeEditNotAllowed
)

@pytest.fixture
def challenge():
    return Challenge(
        name="Test challenge",
        start_date=datetime.date.today(),
        end_date=datetime.date.today(),
        user_id="user1",
        author_id="author1"
    )

"""
Enum logic 
"""
@pytest.mark.skip(reason="not implemented")
def test_enum_status_compare(challenge):
    assert ChallengeStatus.PUBLISHED != ChallengeStatus.PUBLISHED.value
    assert challenge.status != ChallengeStatus.DRAFT.value
    assert challenge.status == ChallengeStatus.DRAFT

@pytest.mark.skip(reason="not implemented")
def test_enum_visibility_compare(challenge):
    assert ChallengeVisibility.PRIVATE != ChallengeVisibility.PRIVATE.value
    assert challenge.visibility != ChallengeVisibility.PRIVATE.value
    assert challenge.visibility == ChallengeVisibility.PRIVATE

@pytest.mark.skip(reason="not implemented")
def test_enum_level_compare(challenge):
    light_level_enum: ChallengeLevel = ChallengeLevel.LIGHT
    assert light_level_enum != light_level_enum.value
    assert challenge.level != light_level_enum.value
    assert challenge.level == light_level_enum


"""
Create draft
"""
def test_create_draft_sets_defaults(challenge):
    challenge.create_draft(name="Test draft", description="Test description")
    assert challenge.status == ChallengeStatus.DRAFT
    assert challenge.visibility == ChallengeVisibility.PRIVATE
    assert challenge.level == ChallengeLevel.LIGHT


"""
Edit draft
"""
@pytest.mark.skip(reason="No edit logic")
def test_edit_draft_allowed(challenge):
    challenge.create_draft(name="Test draft", description="Test description")
    challenge.edit_draft(body={})


def test_edit_draft_not_allowed(challenge):
    challenge.status = ChallengeStatus.PUBLISHED
    with pytest.raises(ChallengeEditNotAllowed):
        challenge.edit_draft(body={})


"""
Publish challenge
"""
def test_publish_from_draft(challenge):
    challenge.status = ChallengeStatus.DRAFT
    challenge.public_links = []

    challenge.publish()

    assert challenge.status == ChallengeStatus.PUBLISHED
    assert len(challenge.public_links) == 1


def test_publish_already_published(challenge):
    challenge.create_draft(name="Test", description="Test description")
    challenge.publish()
    with pytest.raises(ChallengeStatusAlreadyException):
        challenge.publish()


"""
Cancel challenge
"""
def test_cancel_from_started(challenge):
    challenge.status = ChallengeStatus.STARTED

    with pytest.raises(ChallengeInvalidStatus):
        challenge.cancel()

    assert challenge.status == ChallengeStatus.CANCELLED


def test_cancel_already_cancelled(challenge):
    challenge.status = ChallengeStatus.CANCELLED
    with pytest.raises(ChallengeStatusAlreadyException):
        challenge.cancel()



"""
Complete Challenge
"""
def test_complete_from_draft(challenge):
    challenge.status = ChallengeStatus.DRAFT

    with pytest.raises(ChallengeInvalidStatus):
        challenge.complete()

    assert challenge.status == ChallengeStatus.COMPLETED


def test_complete_already_completed(challenge):
    challenge.status = ChallengeStatus.COMPLETED
    with pytest.raises(ChallengeStatusAlreadyException):
        challenge.complete()
