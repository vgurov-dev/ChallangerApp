from datetime import date
from typing import Optional

from fastapi import APIRouter, Body, Path, Query
from sqlalchemy import select
from backend.app.dependeces import SessionDep
from backend.app.models.challenge import Challenge
from backend.app.schemas.challenge import (
    ChallengeInput, ChallengeOut, ChallengeOutRow,
    ChallengeDraftIn, DraftListOut, DayCommitOut,
    PublishedListOut
)

router = APIRouter()


@router.get("/draft-list")
async def get_all_challenges(
    user_id,
    session: SessionDep
) -> ChallengeOut:
    """
    View user's challenge drafts.
    GET /api/v1/challenge/draft-list
    """
    challenges_stmt = select(Challenge).where(Challenge.user_id == user_id)
    result = await session.execute(challenges_stmt)
    data = result.scalars().all()
    return ChallengeOut(challenges=[ChallengeOutRow.model_validate(row) for row in data])


@router.post("/draft")
async def create_challenge_endpoint(
    payload: ChallengeInput,
    session: SessionDep
) -> ChallengeOut:
    """
    Create a new challenge draft
    """
    ch = Challenge(
        name=payload.name,
        start_date=payload.start_date,
        user_id=payload.user_id,
        end_date=payload.end_date,
        scoring_indicator=payload.scoring_indicator.model_dump(),
        description=payload.description
    )
    session.add(ch)
    await session.commit()
    return {"id": ch.id}


@router.put("/{challenge_id}", response_model=ChallengeOut)
async def change_draft_endpoint(
    challenge_id: int = Path(..., alias="challenge_id"),
    update: ChallengeDraftIn = Body(...),
    session: SessionDep = SessionDep,
) -> ChallengeOut:
    """
    Update a challenge draft.
    PUT /api/v1/challenge/{challenge_id}
    """
    pass


@router.delete("/{challenge_id}", response_model=ChallengeOut)
async def delete_challenge_endpoint(
    challenge_id: int = Path(..., alias="challenge_id"),
    session: SessionDep = SessionDep,
) -> ChallengeOut:
    """
    Delete a challenge draft.
    DELETE /api/v1/challenge/{challenge_id}
    """
    pass


@router.put("/{challenge_id}/published", response_model=ChallengeOut)
async def publish_challenge_endpoint(
    challenge_id: int = Path(..., alias="challenge_id"),
    session: SessionDep = SessionDep,
) -> ChallengeOut:
    """
    Publish the challenge:
    - Validate challenge data.
    - Status changes: Draft -> Published.
    - Generate challenge days (create day records in DB).
    - Generate a public link and update visibility.
    PUT /api/v1/challenge/{challenge_id}/published
    """
    pass


@router.put("/{challenge_id}/launch", response_model=ChallengeOut)
async def launch_challenge_endpoint(
    challenge_id: int = Path(..., alias="challenge_id"),
    session: SessionDep = SessionDep,
) -> ChallengeOut:
    """
    Launch the challenge starting today.
    - Default visibility: Private (unless specified otherwise).
    - Status changes: Ready to publish -> Active.
    PUT /api/v1/challenge/{challenge_id}/launch
    """
    pass


@router.put("/{challenge_id}/schedule", response_model=ChallengeOut)
async def schedule_challenge_endpoint(
    challenge_id: int = Path(..., alias="challenge_id"),
    scheduled_date: date = Body(..., embed=True, description="Challenge scheduled start date"),
    session: SessionDep = SessionDep,
) -> ChallengeOut:
    """
    Schedule the challenge to start at a future date.
    - Creates a delayed start entry (scheduler/DB).
    PUT /api/v1/challenge/{challenge_id}/schedule
    """
    pass


@router.put("/{challenge_id}/cancel", response_model=ChallengeOut)
async def cancel_challenge_endpoint(
    challenge_id: int = Path(..., alias="challenge_id"),
    session: SessionDep = SessionDep,
) -> ChallengeOut:
    """
    Cancel the challenge prematurely.
    - All remaining days are marked as failed.
    - Status changes from Active to Canceled.
    PUT /api/v1/challenge/{challenge_id}/cancel
    """
    pass


@router.put("/{challenge_id}/day/{day_id}/commit", response_model=DayCommitOut)
async def commit_day_endpoint(
    challenge_id: int = Path(..., alias="challenge_id"),
    day_id: int = Path(..., alias="day_id"),
    session: SessionDep = SessionDep,
) -> DayCommitOut:
    """
    Commit completion of a specific challenge day.
    PUT /api/v1/challenge/{challenge_id}/day/{day_id}/commit
    """
    pass


@router.put("/{challenge_id}/complete", response_model=ChallengeOut)
async def complete_challenge_endpoint(
    challenge_id: int = Path(..., alias="challenge_id"),
    session: SessionDep = SessionDep,
) -> ChallengeOut:
    """
    Complete the challenge after the final day is committed.
    - Allows marking the challenge as completed.
    PUT /api/v1/challenge/{challenge_id}/complete
    """
    pass


@router.put("/{challenge_id}/day/{day_id}/edit", response_model=DayCommitOut)
async def edit_day_endpoint(
    challenge_id: int = Path(..., alias="challenge_id"),
    day_id: int = Path(..., alias="day_id"),
    session: SessionDep = SessionDep,
) -> DayCommitOut:
    """
    Edit a completed day's data.
    PUT /api/v1/challenge/{challenge_id}/day/{day_id}/edit
    """
    pass


@router.post("/{challenge_id}/copy", response_model=ChallengeOut)
async def copy_challenge_endpoint(
    challenge_id: int = Path(..., alias="challenge_id"),
    target_user_id: Optional[int] = Body(
        None,
        embed=True,
        description="User ID to copy challenge for. If omitted, copies for the current user."
    ),
    session: SessionDep = SessionDep,
) -> ChallengeOut:
    """
    Copy a challenge for another user.
    - Keeps original owner_id unless specified otherwise.
    POST /api/v1/challenge/{challenge_id}/copy
    """
    pass


@router.get("/published-list", response_model=PublishedListOut)
async def get_published_challenge_list_endpoint(
    session: SessionDep = SessionDep,
    q: Optional[str] = Query(None, description="Search by name/description"),
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
) -> PublishedListOut:
    """
    Get a list of active/published challenges.
    GET /api/v1/challenge/published-list
    """
    pass
