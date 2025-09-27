from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.service import Service
from app.schemas.service import ServiceCreate, ServiceUpdate
import uuid


def get_service(
    db: Session,
    q: Optional[str] = None,
    price_min: Optional[float] = None,
    price_max: Optional[float] = None,
    active: Optional[bool] = None,
) -> List[Service]:
    query = db.query(Service)

    if q:
        query = query.filter(Service.title.ilike(f"%{q}"))
    
    if price_min is not None:
        query = query.filter(Service.price >= price_min)

    if price_max is not None:
        query = query.filter(Service.price <= price_max)

    if active is not None:
        query = query.filter(Service.is_active == active)

    return query.all()

def get_service(db: Session, service_id: uuid.UUID) -> Optional[Service]:
    return db.query(Service).filter(Service.id == service_id).first()


def create_service(db: Session, service_data: ServiceCreate) -> Service:
    new_service = Service(**service_data.dict())
    db.add(new_service)
    db.commit()
    db.refresh(new_service)
    return new_service


def update_service(db: Session, service_id: uuid.UUID, updates: ServiceUpdate) -> Optional[Service]:
    service = get_service(db, service_id)
    if not service:
        return None

    for field, value in updates.dict(exclude_unset=True).items():
        setattr(service, field, value)

    db.commit()
    db.refresh(service)
    return service


def delete_service(db: Session, service_id: uuid.UUID) -> bool:
    service = get_service(db, service_id)
    if not service:
        return False

    service.is_active = False
    db.commit()
    return True