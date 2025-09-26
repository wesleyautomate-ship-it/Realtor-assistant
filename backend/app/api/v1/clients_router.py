"""
Clients Router
==============

FastAPI router providing basic CRUD for clients (CRM) aligned with
frontend types and enhanced SQLAlchemy models.
"""

from typing import List, Optional, Dict, Any
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.middleware import get_current_user, require_agent_or_admin
from app.core.models import User
from app.domain.listings.enhanced_real_estate_models import EnhancedClient


router = APIRouter(prefix="/api/v1/clients", tags=["Clients"])


# ======================
# Pydantic Schemas
# ======================

class ClientBase(BaseModel):
    name: str = Field(..., max_length=255)
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    budget_min: Optional[float] = None
    budget_max: Optional[float] = None
    preferred_location: Optional[str] = None
    requirements: Optional[str] = None
    client_type: Optional[str] = Field(default="buyer")
    client_status: Optional[str] = Field(default="active")
    assigned_agent_id: Optional[int] = None
    relationship_start_date: Optional[date] = None
    notes: Optional[str] = None
    preferences: Optional[Dict[str, Any]] = None


class ClientCreate(ClientBase):
    name: str


class ClientUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    budget_min: Optional[float] = None
    budget_max: Optional[float] = None
    preferred_location: Optional[str] = None
    requirements: Optional[str] = None
    client_type: Optional[str] = None
    client_status: Optional[str] = None
    assigned_agent_id: Optional[int] = None
    relationship_start_date: Optional[date] = None
    notes: Optional[str] = None
    preferences: Optional[Dict[str, Any]] = None


class ClientResponse(ClientBase):
    id: int

    class Config:
        from_attributes = True


# ======================
# Routes
# ======================

@router.get("/", response_model=List[ClientResponse])
async def list_clients(
    limit: int = 50,
    offset: int = 0,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        query = db.query(EnhancedClient).order_by(EnhancedClient.id.desc()).offset(offset).limit(limit)
        return [ClientResponse.model_validate(obj) for obj in query.all()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list clients: {str(e)}")


@router.get("/{client_id}", response_model=ClientResponse)
async def get_client(
    client_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    obj = db.query(EnhancedClient).filter(EnhancedClient.id == client_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Client not found")
    return ClientResponse.model_validate(obj)


@router.post("/", response_model=ClientResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_agent_or_admin)])
async def create_client(
    payload: ClientCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        obj = EnhancedClient(
            name=payload.name,
            email=payload.email,
            phone=payload.phone,
            budget_min=payload.budget_min,
            budget_max=payload.budget_max,
            preferred_location=payload.preferred_location,
            requirements=payload.requirements,
            client_type=payload.client_type or "buyer",
            client_status=payload.client_status or "active",
            assigned_agent_id=payload.assigned_agent_id or current_user.id,
            relationship_start_date=payload.relationship_start_date,
            preferences=payload.preferences or {},
        )
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return ClientResponse.model_validate(obj)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create client: {str(e)}")


@router.put("/{client_id}", response_model=ClientResponse, dependencies=[Depends(require_agent_or_admin)])
async def update_client(
    client_id: int,
    updates: ClientUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    obj = db.query(EnhancedClient).filter(EnhancedClient.id == client_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Client not found")
    try:
        data = updates.model_dump(exclude_unset=True)
        for key, value in data.items():
            setattr(obj, key, value)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return ClientResponse.model_validate(obj)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update client: {str(e)}")


@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_agent_or_admin)])
async def delete_client(
    client_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    obj = db.query(EnhancedClient).filter(EnhancedClient.id == client_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Client not found")
    try:
        db.delete(obj)
        db.commit()
        return None
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete client: {str(e)}")


