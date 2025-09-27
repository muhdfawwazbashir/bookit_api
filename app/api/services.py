import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.service import ServiceOut, ServiceCreate, ServiceUpdate
from app.models.service import Service
from app.services.user import require_admin

router = APIRouter()


@router.get("", response_model=List[ServiceOut])
def list_services(db: Session = Depends(get_db)):
    services = db.query(Service).all()
    return services

@router.get("{service_id}", response_model=ServiceOut)
def get_service(service_id: uuid.UUID, db: Session = Depends(get_db)):
    service = db.query(Service).filter(Service.id == service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return service

@router.post("", response_model=ServiceOut)
def create_service(
    service_data: ServiceCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    new_service = Service(**service_data.model_dump())
    db.add(new_service)
    db.commit()
    db.refresh(new_service)
    return new_service
    
@router.patch("{service_id}", response_model=ServiceOut)
def update_service(
    service_id: uuid.UUID,
    service_update: ServiceUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    service = db.query(Service).filter(Service.id == service_id).first()

    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    
    update_data = service_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(service, key, value)


    db.commit()
    db.refresh(service)
    return service

@router.delete("{service_id}")
def delete_service(
    service_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    service = db.query(Service).filter(Service.id == service_id).first()

    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    db.delete(service)
    db.commit()
    return {"message": "Service deleted successfully"}
