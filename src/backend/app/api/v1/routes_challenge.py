from fastapi import APIRouter
from sqlalchemy import select
from backend.app.dependeces import SessionDep
from backend.app.models.challenge import Challenge
from backend.app.schemas.challenge import ChallengeInput, ChallengeOut, ChallengeOutRow


router = APIRouter()


@router.get("/")
async def get_all_challenges(user_id, session: SessionDep) -> ChallengeOut:
    challenges_stmt = select(Challenge).where(Challenge.user_id == user_id)
    result = await session.execute(challenges_stmt)
    data = result.scalars().all()
    return ChallengeOut(challenges=[ChallengeOutRow.model_validate(row) for row in data])



@router.post("/")
async def create_challenge_endpoint(
        payload: ChallengeInput, session: SessionDep):
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
