from app.services.geo import bounding_box, haversine_km


def test_haversine_same_point_is_zero():
    assert haversine_km(14.5826, 120.9787, 14.5826, 120.9787) == 0


def test_haversine_known_distance():
    # Rizal Park to Bonifacio Global City is roughly 9 km.
    distance = haversine_km(14.5826, 120.9787, 14.5503, 121.0493)
    assert 8 < distance < 10


def test_bounding_box_contains_origin():
    min_lat, max_lat, min_lon, max_lon = bounding_box(14.5826, 120.9787, 10)
    assert min_lat < 14.5826 < max_lat
    assert min_lon < 120.9787 < max_lon


def test_bounding_box_clamps_to_valid_range():
    min_lat, max_lat, min_lon, max_lon = bounding_box(89.9, 179.9, 5000)
    assert min_lat >= -90
    assert max_lat <= 90
    assert min_lon >= -180
    assert max_lon <= 180
