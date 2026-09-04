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


def test_patch_address(client):
    created = client.post(
        "/addresses",
        json={
            "street": "Old Street",
            "city": "Manila",
            "state": "NCR",
            "postal_code": "1000",
            "country": "Philippines",
            "latitude": 14.5995,
            "longitude": 120.9842,
        },
    ).json()

    response = client.patch(
        f"/addresses/{created['id']}",
        json={"street": "New Street", "city": "Makati"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["street"] == "New Street"
    assert body["city"] == "Makati"
    assert body["state"] == "NCR"
    assert body["postal_code"] == "1000"
    assert body["latitude"] == 14.5995


def test_patch_address_not_found(client):
    response = client.patch("/addresses/999", json={"city": "Cebu"})
    assert response.status_code == 404


def test_patch_address_invalid_coordinates(client):
    created = client.post(
        "/addresses",
        json={
            "street": "Rizal Avenue",
            "city": "Manila",
            "state": "NCR",
            "postal_code": "1000",
            "country": "Philippines",
        },
    ).json()

    response = client.patch(
        f"/addresses/{created['id']}",
        json={"latitude": -91},
    )
    assert response.status_code == 422


def test_delete_address(client):
    created = client.post(
        "/addresses",
        json={
            "street": "To Delete",
            "city": "Manila",
            "state": "NCR",
            "postal_code": "1000",
            "country": "Philippines",
        },
    ).json()

    deleted = client.delete(f"/addresses/{created['id']}")
    assert deleted.status_code == 204

    again = client.delete(f"/addresses/{created['id']}")
    assert again.status_code == 404


def test_delete_address_not_found(client):
    response = client.delete("/addresses/999")
    assert response.status_code == 404
