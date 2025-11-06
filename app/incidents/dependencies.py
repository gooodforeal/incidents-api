from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.incidents.repository import IncidentRepository
from app.incidents.service import IncidentService


def get_incident_repository(
    db: AsyncSession = Depends(get_db),
) -> IncidentRepository:
    """Dependency для получения репозитория инцидентов"""
    return IncidentRepository(db)


def get_incident_service(
    repository: IncidentRepository = Depends(get_incident_repository),
) -> IncidentService:
    """Dependency для получения сервиса инцидентов"""
    return IncidentService(repository)

