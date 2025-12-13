from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.repositories.user_repo import UserRepository


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def register_user(self, user_data: UserCreate) -> UserResponse:
        return self.user_repo.register_user(user_data)

    def update_user(self, user_id: int, user_data: UserUpdate) -> UserResponse:
        return self.user_repo.update_user(user_id, user_data)

    def get_users(self) -> list[UserResponse]:
        return self.user_repo.get_all_users()

    def get_by_id(self, user_id: int) -> UserResponse:
        return self.user_repo.get_user_by_id(user_id)

    # def delete_user(self, user_id: int):
    #     return self.user_repo.delete_user_by_id(user_id)

    # def add_all(self, animals: list[Animal]):
    #     return self.animal_repo.add_all_animals(animals)

    # def delete_all(self):
    #     return self.animal_repo.delete_all_animals()
