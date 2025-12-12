# import sys
# from pathlib import Path

# sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from datetime import date

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class User(Base):

    username: Mapped[str]
    password_hash: Mapped[str]
    is_admin: Mapped[bool] = mapped_column(default=False)

    def __repr__(self):
        return f"<User: {self.id} | {self.username}>"
