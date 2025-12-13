import jwt
from datetime import datetime
from typing import Optional

from app.schemas.user import UserLogin, UserResponse, UserCreate, LoginResponse
from app.core.config import JWTConfig
from app.utils.security import PasswordMixin


class AuthService:
    def __init__(self, user_repository):
        self.user_repository = user_repository
        self.secret_key = JWTConfig.SECRET_KEY
        self.algorithm = JWTConfig.ALGORITHM

    @classmethod
    def create_access_token(cls, user_data: UserResponse):
        # Создать JWT токен с данными пользователя
        expire = datetime.now(datetime.UTC) + JWTConfig.get_access_token_expires
        payload = {"sub": user_data.username, "user_id": user_data.id, "exp": expire}
        return jwt.encode(payload, cls.secret_key, algorithm=cls.algorithm)

    @classmethod
    def verify_token(cls, token: str):
        # Проверить JWT токен и вернуть payload
        return jwt.decode(token, key=cls.secret_key, algorithms=cls.algorithm)

    def register_user(self, register_data: UserCreate) -> UserResponse:

        hashed_password = PasswordMixin.hash_password(register_data.password)
        register_data.password = hashed_password

        return self.user_repository.create_user(register_data)

    def login_user(self, login_data: UserLogin) -> Optional[LoginResponse]:

        db_user = self.user_repository.get_user_by_username()

        if not db_user:
            return None

        if not PasswordMixin.verify_password(
            login_data.password, db_user.password_hash
        ):
            return None

        # Создаем токен
        access_token = self.create_access_token(
            user_data=UserResponse.model_validate(db_user)
        )

        return LoginResponse(
            access_token=access_token, user=UserResponse.model_validate(db_user)
        )

    def authenticate_user(self, user_data: UserLogin):
        return self.user_repository.login_user(user_data)
