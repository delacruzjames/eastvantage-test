from datetime import UTC, datetime

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.address import Address
from app.schemas.address import AddressCreate, AddressNearby, AddressRead, AddressUpdate
from app.services.geo import bounding_box, haversine_km

router = APIRouter()


def _get_address_or_404(address_id: int, db: Session) -> Address:
    address = db.get(Address, address_id)
    if address is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Address not found")
    return address


@router.get("", response_model=list[AddressNearby])
def list_addresses_nearby(
    latitude: float = Query(..., ge=-90, le=90, description="Latitude of the search origin"),
    longitude: float = Query(..., ge=-180, le=180, description="Longitude of the search origin"),
    distance: float = Query(..., gt=0, le=20037, description="Search radius in kilometers"),
    db: Session = Depends(get_db),
) -> list[AddressNearby]:
    min_lat, max_lat, min_lon, max_lon = bounding_box(latitude, longitude, distance)

    candidates = (
        db.query(Address)
        .filter(Address.latitude.is_not(None), Address.longitude.is_not(None))
        .filter(Address.latitude.between(min_lat, max_lat))
        .filter(Address.longitude.between(min_lon, max_lon))
        .all()
    )

    matches = []
    for address in candidates:
        distance_km = haversine_km(latitude, longitude, address.latitude, address.longitude)
        if distance_km <= distance:
            matches.append(
                AddressNearby(
                    **AddressRead.model_validate(address).model_dump(),
                    distance_km=round(distance_km, 3),
                )
            )

    return sorted(matches, key=lambda match: match.distance_km)


@router.post("", response_model=AddressRead, status_code=status.HTTP_201_CREATED)
def create_address(payload: AddressCreate, db: Session = Depends(get_db)) -> Address:
    address = Address(
        street=payload.street,
        city=payload.city,
        state=payload.state,
        postal_code=payload.postal_code,
        country=payload.country,
        latitude=payload.latitude,
        longitude=payload.longitude,
    )
    db.add(address)
    db.commit()
    db.refresh(address)
    return address


@router.patch("/{address_id}", response_model=AddressRead)
def update_address(
    address_id: int,
    payload: AddressUpdate,
    db: Session = Depends(get_db),
) -> Address:
    address = _get_address_or_404(address_id, db)
    updates = payload.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(address, field, value)
    address.updated_at = datetime.now(UTC)
    db.commit()
    db.refresh(address)
    return address


@router.delete("/{address_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_address(address_id: int, db: Session = Depends(get_db)) -> None:
    address = _get_address_or_404(address_id, db)
    db.delete(address)
    db.commit()
