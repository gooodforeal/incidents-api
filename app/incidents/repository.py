from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List
from app.incidents.model import Incident, IncidentStatus
from app.incidents.schema import IncidentCreate, IncidentUpdate


class IncidentRepository:
    """Репозиторий для работы с инцидентами в базе данных"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, incident_data: IncidentCreate) -> Incident:
        """Создать новый инцидент в базе данных"""
        incident = Incident(
            description=incident_data.description,
            source=incident_data.source,
            status=IncidentStatus.OPEN,
        )
        self.db.add(incident)
        await self.db.commit()
        await self.db.refresh(incident)
        return incident

    async def get_all(
        self, status: Optional[IncidentStatus] = None
    ) -> List[Incident]:
        """Получить список всех инцидентов с опциональной фильтрацией по статусу"""
        query = select(Incident)
        if status:
            query = query.where(Incident.status == status)
        query = query.order_by(Incident.created_at.desc())
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_by_id(self, incident_id: int) -> Optional[Incident]:
        """Получить инцидент по ID"""
        result = await self.db.execute(
            select(Incident).where(Incident.id == incident_id)
        )
        return result.scalar_one_or_none()

    async def update_status(self, incident: Incident, status: IncidentStatus) -> Incident:
        """Обновить статус инцидента"""
        incident.status = status
        await self.db.commit()
        await self.db.refresh(incident)
        return incident

