import sys

from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import argparse

from main import container
from app.models.animal import Animal

from scripts import dump_data, load_data

animal_servises = container.get_animal_service()


def add_test_animals(amount: int = 10) -> None:
    data = [
        Animal(
            name=f"test_animal_{i}",
            description=f"test_animal_description_{i}",
        )
        for i in range(1, amount + 1)
    ]
    animal_servises.add_all(data)


def clear_db() -> None:
    animal_servises.delete_all()


def main():
    parser = argparse.ArgumentParser(
        description="Script for adding test data to the database"
    )
    parser.add_argument(
        "-a", "--animals", action="store_true", help="Add animals test fields"
    )
    parser.add_argument("-d", "--dump", action="store_true", help="Dump DB to json")
    parser.add_argument("-l", "--load", action="store_true", help="Load DB in json")
    parser.add_argument(
        "-c", "--clear", action="store_true", help="Clears the database"
    )
    parser.add_argument(
        "-t", "--total", type=int, help="Number of records to integrate"
    )

    # checks
    if len(sys.argv) == 1:
        print("\n ❌ Флаги не определены, воспользуйтесь флагом: -h, --help.\n")
        return

    args = parser.parse_args()

    if args.clear and (args.animals or (args.dump or args.load)):
        print("\n ⚠️ Нельзя совмещать флаг очистки с другими.\n")
        return

    # executing
    if args.animals:
        if args.total:
            add_test_animals(args.total)
            print(f"\n ✅ В базу добавленно {args.total} тестовых животны.\n")
        else:
            add_test_animals()
            print("\n ✅ В базу добавленно 10 тестовых животных.\n")
    if args.dump:
        dump_data.dump_all(animal_servises)
    if args.load:
        load_data.load_all(animal_servises)
    if args.clear:
        clear_db()
        print("\n ✅ База данных очищена.\n")


if __name__ == "__main__":
    main()
