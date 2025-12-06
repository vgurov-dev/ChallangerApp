from typing import List
from fastapi import APIRouter
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.dependeces import SessionDep
from sqlalchemy.orm import Session
from backend.app.models.challenge import Challenge
from backend.app.schemas.challenge import ChallengeInput


router = APIRouter()


@router.get("/")
async def get_all_challenges(user_id, session: AsyncSession = SessionDep):
    challenges_stmt = select(Challenge).where(Challenge.user_id == user_id)
    result = await session.execute(challenges_stmt)
    return {"challenges": result.scalars().all()}



@router.post("/")
async def create_challenge_endpoint(
        challenge: ChallengeInput,
        session: AsyncSession = SessionDep):
    ch = Challenge(
        name=challenge.name,
        description=challenge.description
    )
    session.add(ch)
    await session.commit()
    return {"message": "ok"}
