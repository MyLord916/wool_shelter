import pytest

from core.config import config
from models.animal import Animal
from core.database import Database, Base


@pytest.fixture(scope="session", autouse=True)
def test_database():
    database = Database(config.database.database_url(test=True))
    database.engine.echo = False
    Base.metadata.drop_all(bind=database.engine)
    Base.metadata.create_all(bind=database.engine)
    yield database
    Base.metadata.drop_all(bind=database.engine)
    config.paths.TEST_DATABSE_FILE.unlink()
