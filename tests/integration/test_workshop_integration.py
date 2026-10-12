from app import database
from app.schemas import CarInput

def test_saved_car_can_be_read_from_sqlite(database_path):
    database.initialize(database_path)
    saved = database.create_car(database_path, CarInput(make="Toyota", model="Yaris", year=2020, color="Blue"))
    loaded = database.get_car(database_path, saved.id)
    assert loaded is not None
    assert loaded.id == saved.id
    assert loaded.make == "Toyota"

def test_deleting_one_car_keeps_the_other(database_path):
    database.initialize(database_path)
    car1 = database.create_car(database_path, CarInput(make="Honda", model="Civic", year=2022, color="Red"))
    car2 = database.create_car(database_path, CarInput(make="Ford", model="Focus", year=2018, color="Black"))

    deleted = database.delete_car(database_path, car1.id)
    assert deleted is True

    assert database.get_car(database_path, car1.id) is None
    remaining = database.get_car(database_path, car2.id)
    assert remaining is not None and remaining.make == "Ford"

    all_cars = database.list_cars(database_path)
    assert len(all_cars) == 1
    assert all_cars[0].id == car2.id