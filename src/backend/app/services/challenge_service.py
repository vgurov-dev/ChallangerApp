from backend.app.models.challenge import Challenge
from backend.app.schemas.challenge import ChallengeDay
from typing import List
import datetime

class ChallengeService:
    ...


class ChallengeRepository:

    @classmethod
    def _create_challenge_days(
            cls, first_date: datetime.date,
            last_date: datetime.date) -> List[ChallengeDay]:
        pass

    @classmethod
    def create_challenge(cls, challenge: Challenge) -> Challenge:
        pass
