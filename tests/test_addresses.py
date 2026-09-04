def test_create_address(client):
    response = client.post(
        "/addresses",
        json={
            "street": "123 Main St",
            "city": "Manila",
            "state": "NCR",
            "postal_code": "1000",
            "country": "Philippines",
            "latitude": 14.5995,
            "longitude": 120.9842,
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["id"] >= 1
    assert body["street"] == "123 Main St"
    assert body["city"] == "Manila"
    assert body["country"] == "Philippines"
    assert body["latitude"] == 14.5995
    assert body["longitude"] == 120.9842
    assert body["created_at"]
    assert body["updated_at"]


def test_create_address_without_coordinates(client):
    response = client.post(
        "/addresses",
        json={
            "street": "Ayala Avenue",
            "city": "Makati",
            "state": "NCR",
            "postal_code": "1226",
            "country": "Philippines",
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["latitude"] is None
    assert body["longitude"] is None


def test_create_address_missing_fields(client):
    response = client.post("/addresses", json={"city": "Manila"})
    assert response.status_code == 422
