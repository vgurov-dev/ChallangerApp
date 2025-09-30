from fastapi import FastAPI
from backend.app.api.v1 import routes_challenge
from backend.app.db.init_db import init_db
from contextlib import asynccontextmanager
import logging

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Код, который выполняется при старте
    init_db()
    yield
    # Код, который выполняется при завершении (если нужен)
    # Например, закрытие соединений с БД


logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s]: %(message)s"
    )
logger = logging.getLogger(__name__)


app = FastAPI(title="Challenge App", lifespan=lifespan)

app.include_router(routes_challenge.router, prefix="/api/v1/challenges", tags=["Challenges"])
