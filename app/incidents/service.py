from typing import Optional, List
from app.incidents.model import Incident, IncidentStatus
from app.incidents.schema import IncidentCreate, IncidentUpdate
from app.incidents.repository import IncidentRepository


class IncidentService:
    """Сервис для работы с инцидентами (бизнес-логика)"""

    def __init__(self, repository: IncidentRepository):
        self.repository = repository

    async def create_incident(self, incident_data: IncidentCreate) -> Incident:
        """Создать новый инцидент"""
        return await self.repository.create(incident_data)

    async def get_incidents(
        self, status: Optional[IncidentStatus] = None
    ) -> List[Incident]:
        """Получить список инцидентов с опциональной фильтрацией по статусу"""
        return await self.repository.get_all(status)

    async def get_incident_by_id(
        self, incident_id: int
    ) -> Optional[Incident]:
        """Получить инцидент по ID"""
        return await self.repository.get_by_id(incident_id)

    async def update_incident_status(
        self, incident_id: int, status_update: IncidentUpdate
    ) -> Optional[Incident]:
        """Обновить статус инцидента по ID"""
        incident = await self.repository.get_by_id(incident_id)
        if not incident:
            return None
        
        return await self.repository.update_status(
            incident, status_update.status
        )

