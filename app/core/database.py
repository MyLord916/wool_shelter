from datetime import datetime

from sqlalchemy import create_engine, Integer, func
from sqlalchemy.orm import (
    sessionmaker,
    DeclarativeBase,
    declared_attr,
    Mapped,
    mapped_column,
)


class Database:
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url, echo=True)
        self.SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )

    def get_db(self):
        db = self.SessionLocal()
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

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + "s"
