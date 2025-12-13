import pytest
from contextlib import nullcontext as does_not_raise

from pydantic_core._pydantic_core import ValidationError

from app.schemas.animal import AnimalCreate, AnimalUpdate
from app.services.animal_services import AnimalService


@pytest.mark.usefixtures("test_animal_service")
class TestAnimalsServices:
    @pytest.mark.parametrize(
        "animal, expectations",
        [
            # fmt: off
            (dict(name="test_name_1", description="test_description_1"),does_not_raise()),
            (dict(name="test_name_2", description="test_description_2"),does_not_raise()),
            (dict(name="test_name_3", description=None), does_not_raise()),
            (dict(name=None, description=None), pytest.raises(ValidationError)),
            (dict(name=None, description="dose not animal"),pytest.raises(ValidationError)),
            # fmt: on
        ],
    )
    def test_servises_add_animal(
        self, animal, expectations, test_animal_service: AnimalService
    ):
        with expectations:
            test_animal_service.add_animal(AnimalCreate(**animal))

    def test_get_animals(self, test_animal_service: AnimalService):
        get_animals = test_animal_service.get_animals()
        assert len(get_animals) == 3
        assert get_animals[1].id == 2
        assert get_animals[1].name == "test_name_2"
        assert get_animals[1].description == "test_description_2"

    def test_get_animal_by_id(self, test_animal_service: AnimalService):
        getter_animal = test_animal_service.get_animal_by_id(1)
        assert getter_animal.id == 1
        assert getter_animal.name == "test_name_1"
        assert getter_animal.description == "test_description_1"

    @pytest.mark.parametrize(
        "animal, expectations",
        [
            # fmt: off
            (dict(name="update_test_name_1", description="update_test_description_1"),does_not_raise()),
            (dict(name="update_test_name_2", description=None), does_not_raise()),
            (dict(name=None, description="update_test_description_2"),does_not_raise()),
            (dict(name=None, description=None), does_not_raise())
            # fmt: on
        ],
    )
    def test_update_animal(
        self, animal, expectations, test_animal_service: AnimalService
    ):
        with expectations:
            test_animal_service.update_animal(3, AnimalUpdate(**animal))

    def test_approved_update_animal(self, test_animal_service: AnimalService):
        animal = test_animal_service.get_animal_by_id(3)
        assert animal.name == "update_test_name_2"
        assert animal.description == "update_test_description_2"

    def test_delete_animal(self, test_animal_service: AnimalService):
        delete_animal = test_animal_service.delete_animal(2)
        get_animals = test_animal_service.get_animals()
        assert delete_animal not in get_animals
        assert len(get_animals) == 2

    def test_delete_all(self, test_animal_service: AnimalService):
        test_animal_service.delete_all()
        get_animals = test_animal_service.get_animals()
        assert len(get_animals) == 0

    @pytest.mark.usefixtures("animals")
    def test_add_all(self, animals, test_animal_service: AnimalService):
        test_animal_service.add_all(animals)
        get_animals = test_animal_service.get_animals()
        assert len(get_animals) == 3
        for test_animal, db_animal in zip(animals, get_animals):
            assert test_animal["name"] == db_animal.name
