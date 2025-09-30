from typing import Generator
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
# from app.core.security import decode_access_token
# from app.models.user import User

# Функция для получения сессии базы данных
def get_db() -> Generator[Session, None, None]:
    """
    Создаёт новую сессию SQLAlchemy для каждого запроса и закрывает после завершения.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# # Пример зависимости для получения текущего пользователя по JWT-токену
# def get_current_user(
#     token: str,
#     db: Session = Depends(get_db)
# ) -> User:
#     """
#     Проверяет JWT-токен, достаёт пользователя из базы.
#     """
#     payload = decode_access_token(token)
#     if payload is None:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid or expired token"
#         )
#     user_id = payload.get("sub")
#     user = db.query(User).filter(User.id == user_id).first()
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="User not found"
#         )
#     return user
