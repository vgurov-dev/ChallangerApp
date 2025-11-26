from typing import List

from fastapi import APIRouter, Depends

from sqlalchemy import select

from backend.app.dependeces import get_db
from sqlalchemy.orm import Session

from backend.app.models.challenge import Challenge
from backend.app.schemas.challenge import ChallengeInput


router = APIRouter()

@router.get("/")
async def get_all_challenges(user_id, db: Session = Depends(get_db)):
    challenges_stmt = select(Challenge).where(Challenge.user_id == user_id)
    result = db.execute(challenges_stmt)
    return {"challenges": result.scalars().all()}



@router.post("/")
async def create_challenge_endpoint(challenge: ChallengeInput, db: Session = Depends(get_db)):
    ch = Challenge(
        name=challenge.name,
        description=challenge.description
    )
    db.add(ch)
    db.commit()
    db.refresh(ch)
    return {"message": "ok"}
