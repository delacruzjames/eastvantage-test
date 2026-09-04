from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.address import Address
from app.schemas.address import AddressCreate, AddressRead

router = APIRouter()


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
