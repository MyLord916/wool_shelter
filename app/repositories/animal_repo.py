from typing import Optional, List

from sqlalchemy.orm import Session

from app.models.animal import Animal
from app.schemas.animal import AnimalCreate, AnimalUpdate


class AnimalRepository:
    def __init__(self, db: Session):
        self.db = next(db)

    def create_animal(self, animal: AnimalCreate) -> Animal:
        db_animal = Animal(name=animal.name, description=animal.description)
        self.db.add(db_animal)
        self.db.commit()
        self.db.refresh(db_animal)
        return db_animal

    def get_all_animals(self) -> Optional[List[Animal]]:
        return self.db.query(Animal).all()

    def update_animals(self, animal_id: int, animal: AnimalUpdate) -> Animal:
        db_animal = self.db.query(Animal).filter(Animal.id == animal_id).first()
        if animal.name is not None:
            db_animal.name = animal.name
        if animal.description is not None:
            db_animal.description = animal.description
        self.db.commit()
        self.db.refresh(db_animal)
        return db_animal

    def delete_animal_by_id(self, animal_id: int) -> None:
        db_animal = self.db.query(Animal).filter(Animal.id == animal_id).first()
        if db_animal:
            self.db.delete(db_animal)
            self.db.commit()
        return db_animal

    def get_animal_by_id(self, animal_id: int) -> Optional[Animal]:
        getter_animal = self.db.query(Animal).filter(Animal.id == animal_id).first()
        return getter_animal

    def add_all_animals(self, animals: list[AnimalCreate]) -> None:
        added_animals = [
            Animal(name=animal["name"], description=animal["description"])
            for animal in animals
        ]
        self.db.add_all(added_animals)
        self.db.commit()

    def delete_all_animals(self):
        self.db.query(Animal).delete()
        self.db.commit()
