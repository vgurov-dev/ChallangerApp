from fastapi import APIRouter, Depends

from app.dependeces import get_db
from sqlalchemy.orm import Session

from app.models.challenge import Challenge
from app.schemas.challenge import ChallengeInput


router = APIRouter()


@router.post("/")
def create_challenge_endpoint(challenge: ChallengeInput, db: Session = Depends(get_db)):
    ch = Challenge(
        name=challenge.name,
        description=challenge.description
    )
    db.add(ch)
    db.commit()
    db.refresh(ch)
    return {"message": "ok"}
