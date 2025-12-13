import json
from datetime import datetime

from app.core.config import config
from app.services.animal_services import AnimalService
from app.utils.datetime_format import date_to_str


def model_to_dict(model_instance) -> dict:
    data = {}
    for column in model_instance.__table__.columns:
        value = getattr(model_instance, column.name)
        if isinstance(value, datetime):
            value = date_to_str(value)

        data[column.name] = value
    return data


def dump_all(service: AnimalService, filename=config.paths.FIXTURES_FILE):
    """Экспорт всех данных"""
    # Собираем все данные
    all_data = {
        "animals": [model_to_dict(animal) for animal in service.get_animals_for_dump()]
    }

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(all_data, file, indent=2, ensure_ascii=False)

    print(f"\n ✅ Полный дамп создан в {filename}\n")
