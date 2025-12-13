from datetime import datetime

from sqlalchemy import create_engine, Integer, func
from sqlalchemy.orm import (
    sessionmaker,
    DeclarativeBase,
    Mapped,
    mapped_column,
)


class Database:
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url, echo=True)
        self.session = sessionmaker(bind=self.engine)

    def get_db(self):
        db = self.session()
        try:
            yield db
        finally:
            db.close()


class Base(DeclarativeBase):
    __abctract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )
