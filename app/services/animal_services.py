from typing import Optional, List

from app.models.animal import Animal
from app.schemas.animal import AnimalCreate, AnimalUpdate, AnimalResponse
from app.repositories.animal_repo import AnimalRepository


class AnimalService:
    def __init__(self, animal_repo: AnimalRepository):
        self.animal_repo = animal_repo

    def add_animal(self, animal_data: AnimalCreate) -> AnimalResponse:
        added_animal = self.animal_repo.create_animal(animal_data)
        return AnimalResponse.model_validate(added_animal)

    def get_animals(self) -> Optional[List[AnimalResponse]]:
        getter_animals = self.animal_repo.get_all_animals()
        return [AnimalResponse.model_validate(animal) for animal in getter_animals]

    def update_animal(self, animal_id: int, animal: AnimalUpdate) -> AnimalResponse:
        updated_animal = self.animal_repo.update_animals(animal_id, animal)
        return AnimalResponse.model_validate(updated_animal)

    def delete_animal(self, animal_id: int) -> AnimalResponse:
        deleted_animal = self.animal_repo.delete_animal_by_id(animal_id)
        return AnimalResponse.model_validate(deleted_animal)

    def get_animal_by_id(self, animal_id: int) -> AnimalResponse:
        getter_animal = self.animal_repo.get_animal_by_id(animal_id)
        return AnimalResponse.model_validate(getter_animal)

    def get_animals_for_dump(self) -> Optional[List[Animal]]:
        return self.animal_repo.get_all_animals()

    def add_all(self, animals: list[AnimalCreate]) -> None:
        self.animal_repo.add_all_animals(animals)

    def delete_all(self) -> None:
        self.animal_repo.delete_all_animals()
