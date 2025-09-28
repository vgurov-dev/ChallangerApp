from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.dependeces import get_db
from backend.app.db.session import SessionLocal
from backend.app.schemas.challenge import ChallengeInput

# from backend.app.schemas.user import UserCreate, UserOut
# from backend.services.user_service import create_user

router = APIRouter()

@router.post("/")
def create_challenge_endpoint(challenge: ChallengeInput, db: Session = Depends(get_db)):
    return {"message": "ok"}
