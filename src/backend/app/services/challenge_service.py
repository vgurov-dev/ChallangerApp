from app.models.challenge import Challenge
from app.schemas.challenge import ChallengeDay
from typing import List
import datetime

def create_challenge(challenge: Challenge) -> Challenge:
    pass


def _create_challenge_days(first_date: datetime.date, last_date: datetime.date) -> List[ChallengeDay]:
    pass