from typing import Optional, List

from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import (
    UserCreate,
    UserUpdate,
    UserResponse,
    UserLogin,
    LoginResponse,
)
from app.services.auth_services import AuthService, PasswordMixin


class UserRepository:
    def __init__(self, db: Session):
        self.db = next(db)

    def create_user(self, user_data: UserCreate):

        self.db.add(user_data)
        self.commit()
        self.refresh(user_data)
        return user_data

    def update_user(self, user_id: int, user_data: UserUpdate) -> UserResponse:

        db_user = self.db.query(User).filter(User.id == user_id).first()

        for key, value in user_data:
            if value is not None:
                setattr(db_user, key, value)

        self.db.commit()
        self.db.refresh(db_user)

        return UserResponse.model_validate(db_user)

    def get_all_users(self) -> Optional[List[UserResponse]]:

        db_users = self.db.query(User).all()

        return [UserResponse.model_validate(db_user) for db_user in db_users]

    def get_user_by_id(self, user_id: int) -> Optional[UserResponse]:

        db_user = self.db.query(User).filter(User.id == user_id).first()

        return UserResponse.model_validate(db_user)

    def get_user_by_username(self, username: str) -> UserResponse:
        db_user = self.db.query(User).filter(User.username == username).first()
        return db_user
