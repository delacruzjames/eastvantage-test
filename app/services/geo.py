"""Geospatial helpers for distance based address lookups."""

from math import asin, cos, radians, sin, sqrt

EARTH_RADIUS_KM = 6371.0088

# One degree of latitude is a near constant distance anywhere on the globe.
KM_PER_DEGREE_LATITUDE = 111.045


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Great-circle distance in kilometers between two coordinate pairs."""
    lat1_rad, lat2_rad = radians(lat1), radians(lat2)
    delta_lat = lat2_rad - lat1_rad
    delta_lon = radians(lon2 - lon1)

    a = sin(delta_lat / 2) ** 2 + cos(lat1_rad) * cos(lat2_rad) * sin(delta_lon / 2) ** 2
    return 2 * EARTH_RADIUS_KM * asin(sqrt(a))


def bounding_box(
    latitude: float,
    longitude: float,
    distance_km: float,
) -> tuple[float, float, float, float]:
    """Latitude/longitude bounds that fully contain the search radius.

    Used to narrow the rows the database returns before the exact haversine
    distance is calculated in Python.
    """
    lat_delta = distance_km / KM_PER_DEGREE_LATITUDE

    # Longitude degrees get shorter towards the poles, so the span widens with
    # latitude and becomes meaningless once cos(latitude) approaches zero.
    cos_latitude = cos(radians(latitude))
    if abs(cos_latitude) < 1e-9:
        lon_delta = 180.0
    else:
        lon_delta = distance_km / (KM_PER_DEGREE_LATITUDE * abs(cos_latitude))

    min_lat = max(latitude - lat_delta, -90.0)
    max_lat = min(latitude + lat_delta, 90.0)
    min_lon = max(longitude - lon_delta, -180.0)
    max_lon = min(longitude + lon_delta, 180.0)

    return min_lat, max_lat, min_lon, max_lon
