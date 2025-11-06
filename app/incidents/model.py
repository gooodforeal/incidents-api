from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.sql import func
import enum
from app.core.database import Base


class IncidentStatus(str, enum.Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"


class IncidentSource(str, enum.Enum):
    OPERATOR = "operator"
    MONITORING = "monitoring"
    PARTNER = "partner"


class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)
    status = Column(Enum(IncidentStatus), nullable=False, default=IncidentStatus.OPEN)
    source = Column(Enum(IncidentSource), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

