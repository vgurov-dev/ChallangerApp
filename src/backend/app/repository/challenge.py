from backend.app.models.challenge import Challenge
from backend.app.schemas.challenge import ChallengeDay
from typing import List
import datetime
from kit.infrastructure.repository import SQLAlchemyRepository

class ChallengeSQLAlchemyRepository(SQLAlchemyRepository[Challenge]):
    """
    Class for Challenges DB interactions
    """
    async def get_challenge_by_pub_id(self):
        pass

    async def get_challenge_by_id(self):
        pass