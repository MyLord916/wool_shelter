import pytest

from sqlalchemy import create_engine

from app.core.config import config
from app.models.animal import Animal
from app.core.database import Database, Base


@pytest.fixture(scope="session", autouse=True)
def test_database():
    database = Database(config.database.database_url(test=True))
    Base.metadata.create_all(database.engine)
    yield database
    Base.metadata.drop_all(database.engine)
    config.paths.TEST_DATABSE_FILE.unlink()


# @pytest.fixture(scope="session", autouse=True)
# def test_database():
#     database = Database(config.database.database_url(test=True))
#     Base.metadata.drop_all(database.engine)
#     Base.metadata.create_all(database.engine)
#     yield database
#     Base.metadata.drop_all(database.engine)
#     config.paths.TEST_DATABSE_FILE.unlink()
