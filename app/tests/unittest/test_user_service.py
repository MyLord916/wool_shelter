import pytest
from contextlib import nullcontext as does_not_raise

from pydantic_core._pydantic_core import ValidationError

from schemas.user import UserCreate, UserUpdate
from services.user_services import UserService


@pytest.mark.usefixtures("test_user_service")
class TestUserService:
    @pytest.mark.parametrize(
        "user, expectations",
        [
            (dict(username="Jon", password="123456"), does_not_raise()),
            (dict(username="Bob", password="12345"), pytest.raises(ValidationError)),
            (dict(username="Tim", password="123456"), does_not_raise()),
            (dict(username="", password="123456"), pytest.raises(ValidationError)),
        ],
    )
    def test_servises_add_user(
        self, user, expectations, test_user_service: UserService
    ):
        with expectations:
            created_user = test_user_service.add_user(UserCreate(**user))
            assert created_user is not None
            assert created_user.username == user["username"]

    @pytest.mark.parametrize(
        "user, expectations",
        [
            (dict(is_admin=True), does_not_raise()),
            (dict(password="654321"), does_not_raise()),
            (dict(username="Fil"), does_not_raise()),
            (dict(username="Fi"), pytest.raises(ValidationError)),
            (dict(username="user1"), does_not_raise()),
            (dict(password="54321"), pytest.raises(ValidationError)),
        ],
    )
    def test_update_user(self, user, expectations, test_user_service: UserService):
        with expectations:
            res = test_user_service.update_user(1, UserUpdate(**user))

    def test_get_users(self, test_user_service: UserService):
        get_users = test_user_service.get_users()
        assert len(get_users) == 2

    def test_get_by_id(self, test_user_service: UserService):
        get_user = test_user_service.get_by_id(1)
        assert get_user.id == 1
        assert get_user.username == "user1"
