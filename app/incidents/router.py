from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional, List
from app.incidents.schema import (
    IncidentCreate,
    IncidentUpdate,
    IncidentResponse,
)
from app.incidents.service import IncidentService
from app.incidents.dependencies import get_incident_service
from app.incidents.model import IncidentStatus

router = APIRouter(prefix="/incidents", tags=["incidents"])


@router.post("/", response_model=IncidentResponse, status_code=201)
async def create_incident(
    incident: IncidentCreate,
    service: IncidentService = Depends(get_incident_service),
):
    """Создать новый инцидент"""
    return await service.create_incident(incident)


@router.get("/", response_model=List[IncidentResponse])
async def get_incidents(
    status: Optional[IncidentStatus] = Query(None, description="Фильтр по статусу"),
    service: IncidentService = Depends(get_incident_service),
):
    """Получить список инцидентов с опциональной фильтрацией по статусу"""
    return await service.get_incidents(status)


@router.patch("/{incident_id}/status", response_model=IncidentResponse)
async def update_incident_status(
    incident_id: int,
    status_update: IncidentUpdate,
    service: IncidentService = Depends(get_incident_service),
):
    """Обновить статус инцидента по ID"""
    incident = await service.update_incident_status(incident_id, status_update)
    if not incident:
        raise HTTPException(status_code=404, detail="Инцидент не найден")
    return incident

