"""Pydantic schemas for address create, update, and read payloads."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class AddressCreate(BaseModel):
    """Payload for creating an address. Coordinates are required."""

    street: str = Field(..., min_length=1, max_length=255)
    city: str = Field(..., min_length=1, max_length=100)
    state: str = Field(..., min_length=1, max_length=100)
    postal_code: str = Field(..., min_length=1, max_length=20)
    country: str = Field(..., min_length=1, max_length=100)
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)


class AddressUpdate(BaseModel):
    """Partial update. Only fields that are sent are changed."""

    street: str | None = Field(default=None, min_length=1, max_length=255)
    city: str | None = Field(default=None, min_length=1, max_length=100)
    state: str | None = Field(default=None, min_length=1, max_length=100)
    postal_code: str | None = Field(default=None, min_length=1, max_length=20)
    country: str | None = Field(default=None, min_length=1, max_length=100)
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)


class AddressNearby(BaseModel):
    """An address plus how far it sits from the searched coordinates."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    street: str
    city: str
    state: str
    postal_code: str
    country: str
    latitude: float
    longitude: float
    created_at: datetime
    updated_at: datetime
    distance_km: float


class AddressRead(BaseModel):
    """Address as returned by create and update."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    street: str
    city: str
    state: str
    postal_code: str
    country: str
    latitude: float | None
    longitude: float | None
    created_at: datetime
    updated_at: datetime
