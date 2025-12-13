from sqlalchemy.exc import IntegrityError

import json

from app.core.config import config
from app.services.animal_services import AnimalService
from app.utils.datetime_format import str_to_date


def load_all(servise: AnimalService, filename=config.paths.FIXTURES_FILE):
    """Импорт всех данных"""
    with open(filename, "r", encoding="utf-8") as f:
        all_data = json.load(f)

        if "animals" in all_data:
            animals = [
                dict(
                    name=animal_data["name"],
                    description=animal_data["description"],
                    id=animal_data["id"],
                    created_at=str_to_date(animal_data["created_at"]),
                    updated_at=str_to_date(animal_data["updated_at"]),
                )
                for animal_data in all_data["animals"]
            ]
            try:
                servise.add_all(animals)
                print(f"\n ✅ Полный импорт данных завершен из {filename}\n")
            except IntegrityError:
                print(
                    "\n ❌ База не может быть заполнена по верх уже имеющихся данных\n"
                )
