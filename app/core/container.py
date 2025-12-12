from sqlalchemy.orm import Session

from app.repositories.animal_repo import AnimalRepository
from app.services.animal_services import AnimalService
from app.repositories.user_repo import UserRepository
from app.services.user_services import UserService
from app.services.auth_services import AuthService


class Container:
    def __init__(self, db_session: Session):
        self.db_session = db_session
        self._services = {}

    def get_animal_service(self) -> AnimalService:
        if "animal_service" not in self._services:
            animal_repo = AnimalRepository(self.db_session)
            self._services["animal_service"] = AnimalService(animal_repo)
        return self._services["animal_service"]

    def get_user_service(self) -> UserService:
        if "user_service" not in self._services:
            user_repo = UserRepository(self.db_session)
            self._services["user_service"] = UserService(user_repo)
        return self._services["user_service"]

    def get_auth_service(self) -> AuthService:
        if "auth_service" not in self._services:
            self._services["auth_service"] = AuthService
        return self._services["auth_service"]
