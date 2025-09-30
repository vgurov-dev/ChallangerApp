# from sqlalchemy.orm import Session
# from backend.app.models.user import User
# from backend.app.schemas.user import UserCreate
# from app.core.security import get_password_hash

# def create_user(db: Session, user_in: UserCreate):
#     user = User(
#         username=user_in.username,
#         email=user_in.email,
#         hashed_password=get_password_hash(user_in.password)
#     )
#     db.add(user)
#     db.commit()
#     db.refresh(user)
#     return user
