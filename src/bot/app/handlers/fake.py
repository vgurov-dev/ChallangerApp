import datetime

import aiohttp
from faker import Faker
from aiogram.filters import Command
from aiogram.types import Message

from bot.app.config import settings
from bot.app.schemas.challenge import ChallengeInput


async def create_challenge_service(message: Message):
    pass


def register_faker_command_handlers(dp):

    @dp.message(Command("addfakechallange"))
    async def create_challange(message: Message):
        f = Faker("ru_RU")
        user = message.from_user
        challenge_data = ChallengeInput(
            name=f.building_name(),
            description=f.building_description(),
            user_id=user.id,
            start_date=datetime.date.today(),
            end_date=datetime.date.today()+datetime.timedelta(days=20),

        )
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{settings.BACKEND_URL}/api/v1/challenges",
                                    json=ChallengeInput):
                pass