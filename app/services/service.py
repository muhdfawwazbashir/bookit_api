import uuid
from sqlalchemy.orm import Session
from typing import Optional, List
from app.schemas.service import ServiceCreate, ServiceUpdate
from app.models.service import Service
from app.repositories import service as service_repo


def list_services(
    db: Session,
    q: Optional[str] = None,
    price_min: Optional[float] = None,
    price_max: Optional[float] = None,
    active: Optional[bool] = None,
) -> List[Service]:
    return service_repo.get_services(db, q, price_min, price_max, active)

def get_service_by_id(db: Session, service_id: uuid.UUID) -> Optional[Service]:
    return service_repo.get_service(db, service_id)


def create_service(db: Session, service_data: ServiceCreate) -> Service:
    return service_repo.create_service(db, service_data)


def update_service(db: Session, service_id: uuid.UUID, updates: ServiceUpdate) -> Optional[Service]:
    return service_repo.update_service(db, service_id, updates)


def delete_service(db: Session, service_id: uuid.UUID) -> bool:
    return service_repo.delete_service(db, service_id)