def test_post_car_returns_201_and_json(client):
    payload = {"make": "Ford", "model": "Fiesta", "year": 2018, "color": "Black"}
    response = client.post("/api/cars", json=payload)
    assert response.status_code == 201
    car = response.json()
    assert car["id"] > 0
    assert car["make"] == "Ford"
    assert response.headers["location"] == f"/api/cars/{car['id']}"

def test_invalid_year_is_not_saved(client, car_payload):
    invalid_payload = car_payload.copy()
    invalid_payload["year"] = 1800
    response = client.post("/api/cars", json=invalid_payload)
    assert response.status_code == 422
    get_response = client.get("/api/cars")
    assert get_response.status_code == 200
    assert get_response.json() == []