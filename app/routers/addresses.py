from datetime import UTC, datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.address import Address
from app.schemas.address import AddressCreate, AddressRead, AddressUpdate

router = APIRouter()


def _get_address_or_404(address_id: int, db: Session) -> Address:
    address = db.get(Address, address_id)
    if address is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Address not found")
    return address


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
