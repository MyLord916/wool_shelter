from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Animal(Base):
    __tablename__ = "animals"

    # __table_args__ = {"extend_existing": True}

    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)

    def __repr__(self):
        return f"<Animal: {self.id} | {self.name}>"
