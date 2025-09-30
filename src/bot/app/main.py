import asyncio
from aiogram import Bot, Dispatcher
from app import settings
from app import register_all_handlers
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)

bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher()

# Register all handlers from the example file
register_all_handlers(dp)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
