import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
import aiohttp
from bot.app.config import settings

bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher()

@dp.message()
async def echo(message: Message):
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{settings.BACKEND_URL}/api/v1/users/", json={
            "username": message.from_user.username or "anon",
            "email": f"{message.from_user.id}@example.com",
            "password": "default"
        }) as resp:
            result = await resp.json()
    await message.answer(f"User created: {result['username']}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
