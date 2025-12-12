import pytest
from datetime import date

from core.container import Container
from core.database import Database


@pytest.fixture(scope="module")
def test_container(test_database: Database):
    return Container(test_database.get_db())


@pytest.fixture(scope="class")
def test_animal_service(test_container: Container):
    return test_container.get_animal_service()


@pytest.fixture(scope="class")
def test_user_service(test_container: Container):
    return test_container.get_user_service()


@pytest.fixture
def animals():

    animals = (
        dict(name="Tom", description="cat"),
        dict(name="Bob", description="dog"),
        dict(name="Sam", description="cat"),
    )
    return animals


@pytest.fixture
def users():

    users = (
        dict(username="Jon", birthday=date(1995, 9, 16), password="123456"),
        dict(username="Bob", birthday=date(1995, 9, 16), password="123456"),
        dict(username="Sem", birthday=date(1995, 9, 16), password="123456"),
    )
    return users
